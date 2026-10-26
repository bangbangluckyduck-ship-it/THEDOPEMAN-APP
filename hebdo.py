"""E-mail hebdo « Ce qui vend cette semaine dans ton pays » (lot 5).

Construit à partir du Feed Radar : les 3 vidéos les plus vues de la semaine dans
le pays de l'utilisateur, et, pour chacune, une phrase sur le POURQUOI — prise
dans une analyse déjà faite de cette vidéo (cache d'analyse). Sans analyse, on
ne l'invente pas : l'e-mail invite à l'analyser. Un seul lien, vers l'app.

Destinataires :
  • les abonnés → le lien ouvre le Feed Radar ;
  • les anciens essais non convertis → le lien ouvre Stripe Checkout (signé),
    avec une phrase qui le dit.
Désinscription en un clic (lien dédié : coupe l'hebdo seulement) et réglage dans
l'app (onglet Compte). `marketing_opt_out` coupe tout, comme ailleurs.

Un envoi par personne et par semaine (journal email_log, clé « hebdo:AAAA-Sss »).
MODE TEST PAR DÉFAUT : rien ne part tant que HEBDO_ACTIF ≠ 1 — les e-mails sont
écrits dans les journaux du cron.

    Cron Job Render « hebdo » : python3 cron_hebdo.py — "0 8 * * 1" (lundi 8 h UTC)
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone
from html import escape
from urllib.parse import quote

import essai_emails
from fin_essai import adresse_envoyable

LOT_MAX = 2000
TIERS_ABONNES = ("pro", "gold", "agency", "beta")

TEXTES = {
    "fr": {"objet": "ce qui vend cette semaine", "intro": "Voici les 3 vidéos qui vendent le plus cette semaine dans ton pays.",
           "vues": "{n} vues", "pourquoi": "Pourquoi elle vend : ", "a_analyser": "Analyse-la pour voir pourquoi elle vend.",
           "abonne_fin": "Ouvre le Feed Radar pour les analyser et trouver ton prochain angle.", "abonne_btn": "Voir ce qui vend",
           "ancien_fin": "Pour les analyser et adapter ce qui marche à tes produits, reprends Qeerah Pro.", "ancien_btn": "Reprendre avec Qeerah Pro",
           "pied": "Tu reçois cet e-mail chaque lundi. ", "desinscription": "Ne plus recevoir l'e-mail de la semaine"},
    "en": {"objet": "what is selling this week", "intro": "Here are the 3 videos selling the most this week in your country.",
           "vues": "{n} views", "pourquoi": "Why it sells: ", "a_analyser": "Analyse it to see why it sells.",
           "abonne_fin": "Open the Feed Radar to analyse them and find your next angle.", "abonne_btn": "See what is selling",
           "ancien_fin": "To analyse them and adapt what works to your products, pick up Qeerah Pro again.", "ancien_btn": "Pick up with Qeerah Pro",
           "pied": "You receive this email every Monday. ", "desinscription": "Stop receiving the weekly email"},
    "pt-br": {"objet": "o que está vendendo esta semana", "intro": "Estes são os 3 vídeos que mais vendem esta semana no seu país.",
              "vues": "{n} visualizações", "pourquoi": "Por que vende: ", "a_analyser": "Analise para ver por que ele vende.",
              "abonne_fin": "Abra o Feed Radar para analisá-los e encontrar seu próximo ângulo.", "abonne_btn": "Ver o que está vendendo",
              "ancien_fin": "Para analisá-los e adaptar o que funciona aos seus produtos, volte ao Qeerah Pro.", "ancien_btn": "Retomar com o Qeerah Pro",
              "pied": "Você recebe este e-mail toda segunda-feira. ", "desinscription": "Não receber mais o e-mail da semana"},
    "es": {"objet": "lo que se vende esta semana", "intro": "Estos son los 3 vídeos que más venden esta semana en tu país.",
           "vues": "{n} visualizaciones", "pourquoi": "Por qué vende: ", "a_analyser": "Analízalo para ver por qué vende.",
           "abonne_fin": "Abre el Feed Radar para analizarlos y encontrar tu próximo ángulo.", "abonne_btn": "Ver lo que se vende",
           "ancien_fin": "Para analizarlos y adaptar lo que funciona a tus productos, vuelve a Qeerah Pro.", "ancien_btn": "Retomar con Qeerah Pro",
           "pied": "Recibes este correo cada lunes. ", "desinscription": "No recibir más el correo semanal"},
    "it": {"objet": "cosa vende questa settimana", "intro": "Ecco i 3 video che vendono di più questa settimana nel tuo paese.",
           "vues": "{n} visualizzazioni", "pourquoi": "Perché vende: ", "a_analyser": "Analizzalo per vedere perché vende.",
           "abonne_fin": "Apri il Feed Radar per analizzarli e trovare il tuo prossimo angolo.", "abonne_btn": "Vedi cosa vende",
           "ancien_fin": "Per analizzarli e adattare ciò che funziona ai tuoi prodotti, riprendi Qeerah Pro.", "ancien_btn": "Riprendi con Qeerah Pro",
           "pied": "Ricevi questa email ogni lunedì. ", "desinscription": "Non ricevere più l'email settimanale"},
    "de": {"objet": "was diese woche verkauft", "intro": "Das sind die 3 Videos, die diese Woche in deinem Land am meisten verkaufen.",
           "vues": "{n} Aufrufe", "pourquoi": "Warum es verkauft: ", "a_analyser": "Analysiere es, um zu sehen, warum es verkauft.",
           "abonne_fin": "Öffne den Feed Radar, um sie zu analysieren und deinen nächsten Blickwinkel zu finden.", "abonne_btn": "Sehen, was verkauft",
           "ancien_fin": "Um sie zu analysieren und das, was funktioniert, auf deine Produkte zu übertragen, mach mit Qeerah Pro weiter.", "ancien_btn": "Mit Qeerah Pro weitermachen",
           "pied": "Du bekommst diese E-Mail jeden Montag. ", "desinscription": "Die Wochen-E-Mail nicht mehr erhalten"},
}
TEXTES["es-mx"] = {**TEXTES["es"], "intro": "Estos son los 3 videos que más venden esta semana en tu país.",
                   "a_analyser": "Analízalo para ver por qué vende."}


def actif() -> bool:
    return os.getenv("HEBDO_ACTIF", "0").strip() == "1"


def cle_semaine(maintenant: datetime) -> str:
    annee, semaine, _ = maintenant.isocalendar()
    return f"hebdo:{annee}-S{semaine:02d}"


def _premiere_phrase(texte: str) -> str:
    texte = (texte or "").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", texte)
    return (m.group(1) if m else texte)[:220]


def pourquoi(url: str, lang: str) -> str | None:
    """Première phrase du verdict d'une analyse déjà faite de cette vidéo."""
    try:
        import analysis_cache
        r = analysis_cache.get_cached(f"{analysis_cache.hash_video_url(url)}:none", pipeline="pro", lang=lang)
        return _premiere_phrase((r or {}).get("verdict")) or None
    except Exception:
        return None


def videos_de_la_semaine(supabase, lang: str, maintenant: datetime) -> list[dict]:
    region = essai_emails.REGION_PAR_LANGUE.get(essai_emails.langue(lang), "FR")
    depuis = (maintenant - timedelta(days=7)).isoformat()
    try:
        r = (supabase.table("feed_radar_videos").select("video_url,oembed_author_name,views")
             .eq("region", region).gte("collected_at", depuis)
             .order("views", desc=True).limit(3).execute())
        videos = r.data or []
    except Exception as e:
        print(f"[hebdo] Feed Radar {region} : {e}")
        return []
    for v in videos:
        v["video_url"] = (v.get("video_url") or "").split("?", 1)[0]
        v["pourquoi"] = pourquoi(v["video_url"], essai_emails.langue(lang))
    return [v for v in videos if v["video_url"]]


def contenu(videos: list[dict], lang: str, abonne: bool, lien: str) -> tuple[str, str]:
    """(objet, corps HTML) — un seul lien : le bouton."""
    from email_service import _button
    T = TEXTES.get(essai_emails.langue(lang), TEXTES["fr"])
    items = "".join(
        "<li style=\"margin-bottom:12px;\">"
        f"<strong>@{escape(str(v.get('oembed_author_name') or '').lstrip('@'))}</strong> · "
        f"{escape(T['vues'].format(n=essai_emails._vues(v.get('views'))))}<br>"
        + (escape(T["pourquoi"] + v["pourquoi"]) if v.get("pourquoi") else escape(T["a_analyser"]))
        + "</li>" for v in videos)
    fin = T["abonne_fin"] if abonne else T["ancien_fin"]
    bouton = T["abonne_btn"] if abonne else T["ancien_btn"]
    corps = (f"<p>{escape(essai_emails.TEXTES[essai_emails.langue(lang)]['salut'])}</p>"
             f"<p>{escape(T['intro'])}</p><ol style=\"padding-left:18px;\">{items}</ol>"
             f"<p>{escape(fin)}</p>{_button(escape(bouton), lien)}<p>{escape(essai_emails.SIGNATURE)}</p>")
    return T["objet"], corps


def _destinataires(supabase, maintenant: datetime) -> list[dict]:
    for cols in ("email,tier,marketing_opt_out,trial_ends_at,lang,hebdo_opt_out",
                 "email,tier,marketing_opt_out,trial_ends_at"):
        try:
            r = supabase.table("users").select(cols).limit(LOT_MAX).execute()
            break
        except Exception as e:
            print(f"[hebdo] lecture des comptes ({cols}) : {e}")
    else:
        raise RuntimeError("lecture des comptes impossible")
    out = []
    for u in r.data or []:
        tier = (u.get("tier") or "free").lower()
        fin = essai_emails._parse(u.get("trial_ends_at"))
        ancien_essai = tier == "free" and fin is not None and fin < maintenant
        if tier in TIERS_ABONNES or ancien_essai:
            out.append({**u, "abonne": tier in TIERS_ABONNES})
    return out


async def run(supabase, maintenant: datetime | None = None) -> dict:
    """Envoi (ou simulation) de l'e-mail de la semaine. Ne lève jamais."""
    from email_service import email_service, _wrap
    from auth import make_unsubscribe_token

    if not supabase:
        return {"ok": False, "reason": "supabase indisponible"}
    maintenant = maintenant or datetime.now(timezone.utc)
    simulation = not actif()
    cle = cle_semaine(maintenant)
    app_url = os.getenv("APP_PUBLIC_URL", "https://www.qeerah.com").rstrip("/")
    compte = {"ok": True, "simulation": simulation, "semaine": cle, "sent": 0, "skipped": 0, "failed": 0}
    try:
        comptes = _destinataires(supabase, maintenant)
    except Exception as ex:
        return {**compte, "ok": False, "error": str(ex)}

    par_langue: dict[str, list[dict]] = {}
    for u in comptes:
        email = (u.get("email") or "").strip().lower()
        envoyable, _ = adresse_envoyable(email)
        if not email or not envoyable or u.get("marketing_opt_out") or u.get("hebdo_opt_out"):
            compte["skipped"] += 1
            continue
        lang = essai_emails.langue(u.get("lang"))
        if lang not in par_langue:
            par_langue[lang] = videos_de_la_semaine(supabase, lang, maintenant)
        videos = par_langue[lang]
        if not videos or essai_emails.deja_envoye(supabase, email, cle):
            compte["skipped"] += 1
            continue
        page = "/app?onglet=feedradar" if u["abonne"] else "/abonnement/payer"
        lien = essai_emails.lien_suivi(app_url, "hebdo", page, email)
        objet, corps = contenu(videos, lang, u["abonne"], lien)
        T = TEXTES.get(lang, TEXTES["fr"])
        desinscription = f"{app_url}/unsubscribe?e={quote(email)}&s={make_unsubscribe_token(email)}&type=hebdo"
        corps += (f'<p style="font-size:12px;color:#9a9ab0;margin-top:22px;">{escape(T["pied"])}'
                  f'<a href="{desinscription}" style="color:#9a9ab0;">{escape(T["desinscription"])}</a>.</p>')
        if simulation:
            print(f"[hebdo] SIMULATION {cle} ({lang}) → {email} : « {objet} »\n{corps}")
            compte["skipped"] += 1
            continue
        titre = escape(objet[:1].upper() + objet[1:])
        if await email_service._send(email, objet, _wrap(titre, corps, lang=lang)):
            essai_emails.journaliser(supabase, email, cle)
            try:
                import entonnoir
                entonnoir.enregistrer(supabase, "email_envoye", detail="hebdo", lang=lang)
            except Exception:
                pass
            compte["sent"] += 1
        else:
            compte["failed"] += 1
    return compte
