"""Séquence e-mail de l'essai — une étape de mission = un e-mail.

⚠️ POURQUOI CE MODULE EXISTE.
L'essai n'avait qu'une relance J+3 purement promotionnelle (« Passe à la vitesse
supérieure », liste de fonctionnalités). Or un compte en essai qui n'a encore rien
compris n'a aucune raison de payer : il faut d'abord qu'il vive le déclic. Chaque
e-mail pousse donc UNE action — la prochaine étape de sa mission — et un seul, le
dernier, parle de l'offre, APRÈS le bilan de ce qu'il a obtenu.

  J0  bienvenue (envoyé à l'inscription, cf. email_service.send_welcome_email)
  J2  prochaine étape non faite de la mission
  J5  prochaine étape non faite (rien si la mission est accomplie)
  J7  veille de la fin d'essai : « Ton essai en chiffres », puis l'offre

Garanties (reprises de fin_essai.py) :
- un envoi par personne et par étape, drapeau posé APRÈS l'envoi réussi ;
- `marketing_opt_out` respecté, lien de désinscription signé ;
- adresses de test exclues (réputation d'expédition) ;
- **mode simulation par défaut** : rien ne part tant que ESSAI_EMAILS_ACTIFS=1
  n'est pas posé sur Render. Un e-mail parti ne se rattrape pas.

Suivi des envois dans `market_cache` (clé « mail_essai:<étape>:<email> ») : table
clé/valeur déjà en place, donc aucune migration à jouer.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from html import escape
from urllib.parse import quote

import mission
from fin_essai import adresse_envoyable

LOT_MAX = 500
TRIAL_DAYS = 7

# Fenêtre d'envoi de chaque étape, en jours depuis le DÉBUT de l'essai. Large d'un
# jour ou deux pour absorber un passage manqué du cron ; le drapeau d'envoi reste
# le garde-fou définitif contre les doublons.
FENETRES = {
    "j2": (2, 4),
    "j5": (5, 6),
    "j7": (6, 8),   # du jour 6 (veille de la fin) jusqu'à 1 jour après la fin
}

# Ce que dit chaque étape de mission, et où elle mène.
_ETAPES = {
    1: {
        "objet": "Tu n'as pas encore vu pourquoi elle vend",
        "titre": "Décrypte une vidéo qui vend",
        "texte": ("Choisis une vidéo qui vend en ce moment dans le Feed Radar, colle son lien, "
                  "et regarde ce que tu n'avais pas vu : l'accroche, l'argument, la seconde où "
                  "tout bascule. C'est la base de tout le reste."),
        "bouton": "Décrypter une vidéo qui vend",
        "chemin": "/app",
    },
    2: {
        "objet": "Et pour ton produit, ça donne quoi ?",
        "titre": "Et pour ton produit ?",
        "texte": ("Tu as vu pourquoi une vidéo vend. Maintenant, entre TON produit : tu reçois "
                  "plusieurs angles, chacun avec son accroche, prêts à tester."),
        "bouton": "Trouver mes angles",
        "chemin": "/scripts?mission=2",
    },
    3: {
        "objet": "Ta prochaine vidéo est presque écrite",
        "titre": "Prépare ta prochaine vidéo",
        "texte": ("Choisis le script que tu vas tourner et garde-le (« Je tourne celui-là »). "
                  "Tu n'as plus qu'à filmer."),
        "bouton": "Choisir mon script",
        "chemin": "/scripts?mission=3",
    },
    4: {
        "objet": "Ta vidéo est en ligne ? Regarde ce qu'elle donne",
        "titre": "Reviens décrypter ta vidéo",
        "texte": ("Colle le lien de la vidéo que tu as publiée : tu vois ce qui a marché, ce qui "
                  "a fait décrocher, et ce que tu changes dans la suivante."),
        "bouton": "Décrypter ma vidéo",
        "chemin": "/app",
    },
}


def actif() -> bool:
    return os.getenv("ESSAI_EMAILS_ACTIFS", "").strip() == "1"


def _parse(valeur) -> datetime | None:
    if not valeur:
        return None
    try:
        d = datetime.fromisoformat(str(valeur).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def etape_due(trial_ends_at: datetime, maintenant: datetime) -> str | None:
    """Étape d'e-mail dont la fenêtre contient `maintenant` (la plus avancée)."""
    debut = trial_ends_at - timedelta(days=TRIAL_DAYS)
    jours = (maintenant - debut).total_seconds() / 86400
    dues = [k for k, (lo, hi) in FENETRES.items() if lo <= jours < hi]
    return dues[-1] if dues else None


# ── Contenus ──────────────────────────────────────────────────────────────
def contenu(etape: str, etat: dict, app_url: str) -> tuple[str, str, str] | None:
    """(objet, titre, corps HTML) — ou None s'il n'y a rien d'utile à dire."""
    from email_service import _button

    if etape in ("j2", "j5"):
        prochaine = etat.get("prochaine")
        if prochaine is None:
            return None          # mission accomplie : pas de relance inutile
        e = _ETAPES[prochaine]
        n = etat.get("terminees", 0)
        avance = (f"<p>Tu en es à <strong>{n}/4</strong> dans ta mission. Prochaine étape :</p>"
                  if n else "<p>Ta mission d'essai tient en 4 étapes. La première :</p>")
        corps = (
            "<p>Salut,</p>"
            f"{avance}"
            f"<p style=\"font-size:17px;font-weight:800;margin:14px 0 6px;\">{escape(e['titre'])}</p>"
            f"<p>{escape(e['texte'])}</p>"
            f"{_button(e['bouton'], app_url + e['chemin'])}"
            "<p>À tout de suite,<br>Qeerah</p>"
        )
        return e["objet"], e["titre"], corps

    if etape == "j7":
        b = etat.get("bilan", {})
        v, g, s = b.get("videos_decryptees", 0), b.get("generations_scripts", 0), b.get("scripts_gardes", 0)
        if not (v or g or s):
            corps = (
                "<p>Salut,</p>"
                "<p>Ton essai se termine. Tu n'as pas eu le temps de décrypter une vidéo ?</p>"
                "<p>Avec Qeerah Pro, tu vois chaque mois pourquoi les vidéos TikTok Shop vendent, "
                "et quoi reproduire dans les tiennes.</p>"
                f"{_button('Passer à Qeerah Pro', app_url + '/pricing')}"
                "<p>Qeerah</p>"
            )
            return "Ton essai se termine", "Ton essai se termine", corps
        pl = lambda x: "s" if x > 1 else ""
        corps = (
            "<p>Salut,</p>"
            "<p>Ton essai se termine. Voilà ce que tu as fait :</p>"
            "<ul style=\"padding-left:18px;line-height:1.9;\">"
            f"<li><strong>{v}</strong> vidéo{pl(v)} décryptée{pl(v)}</li>"
            f"<li><strong>{g}</strong> série{pl(g)} d'angles pour ton produit</li>"
            f"<li><strong>{s}</strong> script{pl(s)} prêt{pl(s)} à tourner</li>"
            "</ul>"
            "<p>Pour continuer à comprendre ce qui vend et à le reproduire chaque mois, passe à "
            "Qeerah Pro. Tes analyses et tes favoris restent là.</p>"
            f"{_button('Passer à Qeerah Pro', app_url + '/pricing')}"
            "<p>Qeerah</p>"
        )
        return "Ton essai en chiffres", "Ton essai en chiffres", corps
    return None


# ── Traçage des envois (market_cache, sans migration) ─────────────────────
def _cle(etape: str, email: str) -> str:
    return f"mail_essai:{etape}:{email}"


def _deja_envoye(supabase, etape: str, email: str) -> bool:
    try:
        r = (supabase.table("market_cache").select("cache_key")
             .eq("cache_key", _cle(etape, email)).limit(1).execute())
        return bool(r.data)
    except Exception as e:
        # Dans le doute, on s'abstient : un message manquant vaut mieux qu'un doublon.
        print(f"[essai_emails] _deja_envoye({email}) : {e} → on s'abstient")
        return True


def _marquer(supabase, etape: str, email: str) -> None:
    maintenant = datetime.now(timezone.utc)
    try:
        supabase.table("market_cache").upsert({
            "cache_key": _cle(etape, email),
            "payload": {"etape": etape, "envoye_le": maintenant.isoformat()},
            "expires_at": (maintenant + timedelta(days=3650)).isoformat(),
        }).execute()
    except Exception as e:
        print(f"⚠️  [essai_emails] {email} : envoi réussi mais marquage KO ({e}) — "
              f"risque de doublon au prochain passage.")


# ── Passage quotidien ─────────────────────────────────────────────────────
async def run(supabase, maintenant: datetime | None = None) -> dict:
    """Envoie (ou simule) les e-mails dus aujourd'hui. Ne lève jamais d'exception."""
    if not supabase:
        return {"ok": False, "reason": "supabase indisponible", "sent": 0}

    from auth import make_unsubscribe_token
    from email_service import email_service, _wrap

    maintenant = maintenant or datetime.now(timezone.utc)
    simulation = not actif()
    app_url = os.getenv("APP_PUBLIC_URL", "https://www.qeerah.com").rstrip("/")
    compte = {"ok": True, "simulation": simulation, "sent": 0, "skipped": 0, "failed": 0,
              "par_etape": {}}

    try:
        # Essais en cours ou terminés depuis moins de 2 jours.
        borne = (maintenant - timedelta(days=2)).isoformat()
        rows = (supabase.table("users")
                .select("email,tier,marketing_opt_out,trial_ends_at")
                .eq("tier", "free").gte("trial_ends_at", borne)
                .limit(LOT_MAX).execute())
    except Exception as ex:
        return {**compte, "ok": False, "error": str(ex)}

    for u in (rows.data or []):
        email = (u.get("email") or "").strip().lower()
        fin = _parse(u.get("trial_ends_at"))
        envoyable, _motif = adresse_envoyable(email)
        if not email or not fin or u.get("marketing_opt_out") or not envoyable:
            compte["skipped"] += 1
            continue
        etape = etape_due(fin, maintenant)
        if not etape or _deja_envoye(supabase, etape, email):
            compte["skipped"] += 1
            continue

        c = contenu(etape, mission.etat(supabase, email), app_url)
        if not c:
            compte["skipped"] += 1
            continue
        objet, titre, corps = c
        unsub = f"{app_url}/unsubscribe?e={quote(email)}&s={make_unsubscribe_token(email)}"
        corps += (f'<p style="font-size:12px;color:#9a9ab0;margin-top:22px;">Tu reçois cet e-mail '
                  f'parce que ton essai Qeerah est en cours. <a href="{unsub}" style="color:#9a9ab0;">'
                  f'Ne plus recevoir ces e-mails</a>.</p>')

        if simulation:
            print(f"[essai_emails] SIMULATION {etape} → {email} : « {objet} »")
            compte["par_etape"][etape] = compte["par_etape"].get(etape, 0) + 1
            continue

        if await email_service._send(email, objet, _wrap(escape(titre), corps)):
            _marquer(supabase, etape, email)
            compte["sent"] += 1
            compte["par_etape"][etape] = compte["par_etape"].get(etape, 0) + 1
        else:
            compte["failed"] += 1
    return compte
