"""Rappel « ton essai se termine bientôt » — logique isolée du transport.

⚠️ POURQUOI CE MODULE EXISTE.
Aucun e-mail n'annonçait la fin de l'essai. Les utilisateurs découvraient le mur
de paiement en cliquant sur « Analyser », sans préavis — après, pour certains,
trois mois d'usage libre. C'est la pire façon de présenter un abonnement : on ne
demande rien, on bloque.

Le cas est aigu au 03/08/2026 : la migration tarifaire du 2 août a donné 7 jours
d'essai à TOUS les comptes gratuits d'un coup, donc 14 d'entre eux expirent le
même jour, le 8 août.

Ce module reste utile ensuite : il envoie le rappel à quiconque arrive à ~2 jours
de la fin, quelle que soit sa date d'inscription.

Garanties :
  · un seul envoi par personne, jamais deux (drapeau `trial_ending_sent`) ;
  · `marketing_opt_out` respecté ;
  · lien de désinscription signé dans chaque message ;
  · mode SIMULATION par défaut — rien ne part tant qu'on ne le demande pas
    explicitement. Un e-mail envoyé ne se rattrape pas.
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

# Fenêtre de ciblage : essai se terminant dans 1 à 3 jours. Assez large pour
# absorber un run manqué, assez étroite pour rester un « bientôt » crédible.
JOURS_MIN = 1
JOURS_MAX = 3
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


def _jours_restants(fin: datetime, maintenant: datetime) -> int:
    return max(0, round((fin - maintenant).total_seconds() / 86400))


def corps_email(jours: int, lien_desinscription: str) -> tuple[str, str]:
    """(sujet, html). Le ton dit ce qui se passe, sans dramatiser ni culpabiliser.

    Le message rappelle ce que la personne a DÉJÀ fait avec l'outil plutôt que de
    vanter des fonctionnalités : à ce stade elle connaît le produit, l'argumentaire
    commercial n'a plus rien à lui apprendre.
    """
    from email_service import _button, _wrap
    import site_content as sc

    quand = "demain" if jours <= 1 else f"dans {jours} jours"
    sujet = f"Ton accès complet à Qeerah se termine {quand}"

    prix = f"{sc.PRICE_MONTH:.2f}".rstrip("0").rstrip(".").replace(".", ",")
    app = os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")

    corps = (
        f"<p>Salut,</p>"
        f"<p>Ton accès complet à Qeerah se termine <strong>{quand}</strong>.</p>"
        f"<p>D'ici là, rien ne change : tu peux continuer à analyser tes vidéos "
        f"normalement. Après, tes analyses passées restent consultables, mais tu "
        f"ne pourras plus en lancer de nouvelles.</p>"
        f"<p>Si l'outil t'a été utile, l'abonnement est à <strong>{prix} €/mois</strong>, "
        f"sans engagement, résiliable en deux clics depuis ton espace.</p>"
        f"{_button('Continuer avec Qeerah Pro →', app + '/pricing')}"
        f"<p style=\"font-size:14px;color:#666\">Si ce n'est pas pour toi, aucun souci — "
        f"tu n'as rien à faire, et rien ne te sera prélevé. Tu n'as jamais eu à donner "
        f"de carte bancaire.</p>"
        f"<p style=\"font-size:13px;color:#888\">Une remarque, un blocage, une "
        f"fonctionnalité qui manque ? Réponds directement à ce message, je lis tout.</p>"
        f"<p style=\"font-size:11px;color:#aaa;margin-top:28px\">"
        f"Tu reçois ce message parce que tu as un compte Qeerah. "
        f"<a href=\"{lien_desinscription}\" style=\"color:#aaa\">Ne plus recevoir d'e-mails</a>.</p>"
    )
    return sujet, _wrap(sujet, corps)


def destinataires(supabase, maintenant: datetime | None = None) -> list[dict]:
    """Comptes dont l'essai se termine bientôt et qui n'ont pas encore été prévenus."""
    maintenant = maintenant or datetime.now(timezone.utc)
    debut = (maintenant + timedelta(days=JOURS_MIN)).isoformat()
    fin = (maintenant + timedelta(days=JOURS_MAX)).isoformat()

    lignes = (supabase.table("users")
              .select("email,tier,trial_ends_at,marketing_opt_out,trial_ending_sent")
              .gte("trial_ends_at", debut).lte("trial_ends_at", fin)
              .limit(LOT_MAX).execute()).data or []

    retenus = []
    for u in lignes:
        # Un abonné n'a pas d'essai à perdre ; un désabonné marketing n'est pas
        # sollicité ; un déjà-prévenu ne l'est pas deux fois.
        if (u.get("tier") or "free") != "free":
            continue
        if u.get("marketing_opt_out") or u.get("trial_ending_sent"):
            continue
        fin_essai = _parse(u.get("trial_ends_at"))
        if not fin_essai:
            continue
        retenus.append({"email": (u.get("email") or "").strip().lower(),
                        "fin": fin_essai,
                        "jours": _jours_restants(fin_essai, maintenant)})
    return [r for r in retenus if r["email"]]


async def envoyer(supabase, *, simulation: bool = True) -> dict:
    """Envoie le rappel. **Simulation par défaut** : rien ne part, on renvoie la
    liste de ce qui PARTIRAIT. Passer `simulation=False` pour l'envoi réel."""
    from auth import make_unsubscribe_token
    from email_service import email_service

    app = os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")
    cibles = destinataires(supabase)
    envoyes, echecs = 0, 0

    for c in cibles:
        lien = f"{app}/unsubscribe?e={quote(c['email'])}&s={make_unsubscribe_token(c['email'])}"
        sujet, html = corps_email(c["jours"], lien)
        if simulation:
            continue
        if await email_service._send(c["email"], sujet, html):
            # Drapeau posé APRÈS l'envoi réussi : un échec réseau laisse la
            # personne éligible au prochain passage.
            supabase.table("users").update({"trial_ending_sent": True}) \
                    .eq("email", c["email"]).execute()
            envoyes += 1
        else:
            echecs += 1

    return {"ok": True, "simulation": simulation, "cibles": len(cibles),
            "envoyes": envoyes, "echecs": echecs,
            "details": [{"email": c["email"], "jours": c["jours"]} for c in cibles]}
