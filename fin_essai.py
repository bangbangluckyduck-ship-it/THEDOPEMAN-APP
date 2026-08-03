"""Séquence « premiers testeurs » — fin d'essai + offre à vie à 9,90 €.

⚠️ POURQUOI CE MODULE EXISTE.
Aucun e-mail n'annonçait la fin de l'essai : les utilisateurs découvraient le mur
de paiement en cliquant sur « Analyser ». Pour dix d'entre eux, après trois mois
d'usage libre. On ne demande rien, on bloque — la pire façon de présenter un
abonnement.

Le cas est immédiat : la migration tarifaire du 2 août ayant donné 7 jours
d'essai à tous les comptes gratuits d'un coup, 14 personnes expirent le 8 août
sans le savoir.

## DEUX PISTES, parce que la population n'est pas homogène

Constat mesuré le 03/08 sur les 15 comptes en essai : **3 seulement ont lancé au
moins une analyse, 12 n'ont jamais rien fait.** Leur envoyer le même message
serait absurde — on ne dit pas « tu vas perdre ton accès » à quelqu'un qui n'a
jamais ouvert l'outil, et on ne réexplique pas le produit à quelqu'un qui
l'utilise depuis mai.

  · piste ACTIF   : rappelle ce qu'il a fait (analyses, note moyenne) et ce
                    qu'il garde.
  · piste DORMANT : ne parle pas de perte, propose de faire la première analyse
                    pendant qu'il en a encore.

## TROIS ÉTAPES

  1. `annonce`         — l'offre à vie et l'échéance
  2. `essai_termine`   — après la fin de l'essai, l'offre court encore
  3. `derniere_chance` — 2 jours avant l'expiration du code

Garanties : un envoi par personne ET par étape, `marketing_opt_out` respecté,
lien de désinscription signé, drapeau posé APRÈS l'envoi réussi, et **mode
simulation par défaut** — un e-mail parti ne se rattrape pas.
"""
from __future__ import annotations

import os
import re
from datetime import date, datetime, timedelta, timezone
from urllib.parse import quote

# ── L'offre ───────────────────────────────────────────────────────────────
CODE_PROMO = os.getenv("CODE_PROMO_TESTEURS", "TESTEURS990")
PRIX_OFFRE = 9.90
FIN_OFFRE = date(2026, 8, 17)

ETAPES = ("annonce", "essai_termine", "derniere_chance")
LOT_MAX = 500


def _parse(valeur):
    """Horodatage Supabase → datetime aware. Tolère 5 chiffres de fraction de
    seconde, que `fromisoformat` refuse avant Python 3.11."""
    if not valeur:
        return None
    txt = str(valeur).replace("Z", "+00:00")
    for essai in (re.sub(r"\.(\d+)", lambda m: "." + m.group(1)[:6].ljust(6, "0"), txt),
                  re.sub(r"\.\d+", "", txt)):
        try:
            d = datetime.fromisoformat(essai)
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return None


def _eur(v: float) -> str:
    """Montant à la française : « 9,90 » et non « 9,9 ».

    ⚠️ Ne pas reprendre le helper `site_content.eur`, qui rogne les zéros de fin :
    correct pour 299 €, mais il transforme 9,90 en « 9,9 » — sur un prix, ça se
    voit et ça fait négligé. On ne supprime les décimales que si le montant est
    entier.
    """
    return (f"{v:.0f}" if float(v).is_integer()
            else f"{v:.2f}".replace(".", ","))


def stats_utilisateur(supabase, email: str) -> dict:
    """Ce que la personne a réellement fait. Sert à choisir la piste ET à
    personnaliser — jamais à inventer un chiffre : si rien n'est trouvé, on
    renvoie zéro et le message s'adapte."""
    vide = {"analyses": 0, "note_moyenne": None, "meilleure": None}
    try:
        lignes = (supabase.table("analysis_jobs")
                  .select("result,title").eq("user_email", email)
                  .eq("status", "done").limit(200).execute()).data or []
    except Exception as e:
        print(f"stats_utilisateur({email}): {e}")
        return vide
    if not lignes:
        return vide

    notes = []
    meilleure = None
    for l in lignes:
        r = l.get("result") or {}
        n = r.get("score_global")
        if isinstance(n, (int, float)):
            notes.append(n)
            if meilleure is None or n > meilleure[0]:
                meilleure = (n, (l.get("title") or "").strip()[:60])
    return {
        "analyses": len(lignes),
        "note_moyenne": round(sum(notes) / len(notes)) if notes else None,
        "meilleure": meilleure,
    }


# ── Rédaction ─────────────────────────────────────────────────────────────

def _bloc_offre(aujourdhui: date) -> str:
    """L'offre, présentée pareil dans les trois étapes : ce qui change, c'est
    seulement l'urgence autour."""
    restant = (FIN_OFFRE - aujourdhui).days
    echeance = ("aujourd'hui" if restant <= 0
                else "demain" if restant == 1
                else f"jusqu'au {FIN_OFFRE:%d} août")
    return (
        f'<div style="background:#FAF6EA;border:1px solid #D8C89A;border-radius:10px;'
        f'padding:18px 20px;margin:22px 0">'
        f'<div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;'
        f'color:#8A6D1F;font-weight:700;margin-bottom:6px">Offre premiers testeurs</div>'
        f'<div style="font-size:26px;font-weight:800;color:#1F3A70;line-height:1.2">'
        f'{_eur(PRIX_OFFRE)} € par mois — à vie</div>'
        f'<div style="font-size:14px;color:#555;margin-top:8px">'
        f'Au lieu de 29,99 €. Le tarif ne bouge plus, tant que tu restes abonné.<br>'
        f'Code <strong style="font-family:monospace;font-size:15px">{CODE_PROMO}</strong> '
        f'à saisir au paiement, valable {echeance}.</div>'
        f'</div>'
    )


def corps_email(etape: str, stats: dict, jours_essai: int,
                lien_desinscription: str, aujourdhui: date | None = None) -> tuple[str, str]:
    """(sujet, html) pour une étape et un profil donnés."""
    from email_service import _button, _wrap

    aujourdhui = aujourdhui or datetime.now(timezone.utc).date()
    app = os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")
    actif = stats["analyses"] > 0
    offre = _bloc_offre(aujourdhui)
    cta = _button(f"Prendre l'offre à {_eur(PRIX_OFFRE)} € →", f"{app}/pricing")

    # ── 1. Annonce ────────────────────────────────────────────────────────
    if etape == "annonce":
        quand = ("demain" if jours_essai <= 1
                 else f"dans {jours_essai} jours" if jours_essai > 0
                 else "aujourd'hui")
        if actif:
            sujet = "Tu fais partie des premiers testeurs de Qeerah"
            rappel = f"<strong>{stats['analyses']} analyse" \
                     f"{'s' if stats['analyses'] > 1 else ''}</strong>"
            if stats["note_moyenne"] is not None:
                rappel += f", note moyenne <strong>{stats['note_moyenne']}/100</strong>"
            detail = ""
            if stats["meilleure"] and stats["meilleure"][1]:
                detail = (f"<p>Ta meilleure : « {stats['meilleure'][1]} », "
                          f"{stats['meilleure'][0]}/100.</p>")
            corps = (
                f"<p>Salut,</p>"
                f"<p>Tu utilises Qeerah depuis le début, avant même que l'abonnement "
                f"existe. Tu as lancé {rappel}.</p>"
                f"{detail}"
                f"<p>Ton accès complet se termine <strong>{quand}</strong>. Comme tu es "
                f"parmi les tout premiers à avoir testé l'outil, je te réserve un tarif "
                f"que je ne proposerai plus ensuite :</p>"
                f"{offre}{cta}"
            )
        else:
            sujet = "Il te reste quelques jours pour tester Qeerah"
            corps = (
                f"<p>Salut,</p>"
                f"<p>Tu as créé un compte Qeerah mais tu n'as pas encore lancé "
                f"d'analyse — et ton accès complet se termine <strong>{quand}</strong>.</p>"
                f"<p>Ça prend deux minutes : tu colles le lien d'une vidéo TikTok Shop "
                f"qui marche, et tu obtiens le détail de ce qui la fait vendre — "
                f"l'accroche, le rythme, l'argumentaire, le moment du call-to-action.</p>"
                f"{_button('Analyser une vidéo maintenant →', f'{app}/app')}"
                f"<p>Et parce que tu fais partie des premiers inscrits, si l'outil te "
                f"convainc :</p>"
                f"{offre}"
            )

    # ── 2. L'essai vient de se terminer ───────────────────────────────────
    elif etape == "essai_termine":
        restant = (FIN_OFFRE - aujourdhui).days
        sujet = f"Ton offre à {_eur(PRIX_OFFRE)} € court encore {restant} jours"
        intro = (f"<p>Ton accès complet s'est terminé — tes analyses restent "
                 f"consultables, mais tu ne peux plus en lancer de nouvelles.</p>"
                 if actif else
                 f"<p>Ton accès d'essai s'est terminé. Tu n'as pas eu l'occasion de "
                 f"tester l'outil, et c'est peut-être simplement que ce n'était pas le "
                 f"bon moment.</p>")
        corps = (
            f"<p>Salut,</p>{intro}"
            f"<p>Le tarif réservé aux premiers testeurs, lui, est encore ouvert "
            f"<strong>{restant} jours</strong> :</p>"
            f"{offre}{cta}"
            f"<p style=\"font-size:14px;color:#666\">Sans engagement, résiliable en deux "
            f"clics depuis ton espace. Après le {FIN_OFFRE:%d} août, ce sera 29,99 €.</p>"
        )

    # ── 3. Dernière chance ────────────────────────────────────────────────
    else:
        restant = max(0, (FIN_OFFRE - aujourdhui).days)
        quand = "ce soir" if restant <= 0 else "demain" if restant == 1 else f"dans {restant} jours"
        sujet = f"Dernier jour pour {_eur(PRIX_OFFRE)} € à vie" if restant <= 1 \
                else f"Plus que {restant} jours pour {_eur(PRIX_OFFRE)} € à vie"
        corps = (
            f"<p>Salut,</p>"
            f"<p>Le code <strong>{CODE_PROMO}</strong> expire <strong>{quand}</strong>. "
            f"Après, le tarif repasse à 29,99 € — pour tout le monde, y compris toi.</p>"
            f"{offre}{cta}"
            f"<p style=\"font-size:14px;color:#666\">Si ce n'est pas pour toi, ignore ce "
            f"message : c'est le dernier sur le sujet, et rien ne te sera jamais "
            f"prélevé. Tu n'as pas donné de carte bancaire.</p>"
        )

    corps += (
        f"<p style=\"font-size:13px;color:#888;margin-top:24px\">Une remarque, un blocage, "
        f"une fonctionnalité qui manque ? Réponds directement à ce message, je lis tout.</p>"
        f"<p style=\"font-size:11px;color:#aaa;margin-top:22px\">Tu reçois ce message parce "
        f"que tu as un compte Qeerah. "
        f"<a href=\"{lien_desinscription}\" style=\"color:#aaa\">Ne plus recevoir d'e-mails</a>.</p>"
    )
    return sujet, _wrap(sujet, corps)


# ── Sélection et envoi ────────────────────────────────────────────────────

def _colonne(etape: str) -> str:
    return f"trial_mail_{etape}"


def destinataires(supabase, etape: str, maintenant: datetime | None = None) -> list[dict]:
    """Comptes éligibles à CETTE étape, jamais encore sollicités pour elle."""
    maintenant = maintenant or datetime.now(timezone.utc)
    colonne = _colonne(etape)

    lignes = (supabase.table("users")
              .select(f"email,tier,trial_ends_at,marketing_opt_out,{colonne}")
              .not_.is_("trial_ends_at", "null").limit(LOT_MAX).execute()).data or []

    retenus = []
    for u in lignes:
        if (u.get("tier") or "free") != "free":
            continue                      # un abonné n'est plus concerné
        if u.get("marketing_opt_out") or u.get(colonne):
            continue                      # désabonné, ou déjà servi pour cette étape
        fin = _parse(u.get("trial_ends_at"))
        if not fin:
            continue
        jours = round((fin - maintenant).total_seconds() / 86400)

        # Chaque étape a sa fenêtre. On ne prévient pas de la fin d'un essai
        # terminé depuis deux semaines, ni d'une offre déjà expirée.
        if etape == "annonce" and not (0 <= jours <= 7):
            continue
        if etape == "essai_termine" and not (-7 <= jours < 0):
            continue
        if etape == "derniere_chance" and (FIN_OFFRE - maintenant.date()).days > 2:
            continue

        email = (u.get("email") or "").strip().lower()
        if email:
            retenus.append({"email": email, "jours_essai": max(0, jours)})
    return retenus


async def envoyer(supabase, etape: str, *, simulation: bool = True) -> dict:
    """Envoie une étape. **Simulation par défaut** : renvoie ce qui PARTIRAIT."""
    if etape not in ETAPES:
        return {"ok": False, "erreur": f"étape inconnue : {etape}"}

    from auth import make_unsubscribe_token
    from email_service import email_service

    app = os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")
    cibles = destinataires(supabase, etape)
    envoyes = echecs = 0
    details = []

    for c in cibles:
        stats = stats_utilisateur(supabase, c["email"])
        lien = f"{app}/unsubscribe?e={quote(c['email'])}&s={make_unsubscribe_token(c['email'])}"
        sujet, html = corps_email(etape, stats, c["jours_essai"], lien)
        details.append({"email": c["email"], "piste": "actif" if stats["analyses"] else "dormant",
                        "analyses": stats["analyses"], "sujet": sujet})
        if simulation:
            continue
        if await email_service._send(c["email"], sujet, html):
            supabase.table("users").update({_colonne(etape): True}) \
                    .eq("email", c["email"]).execute()
            envoyes += 1
        else:
            echecs += 1

    return {"ok": True, "etape": etape, "simulation": simulation,
            "cibles": len(cibles), "envoyes": envoyes, "echecs": echecs, "details": details}
