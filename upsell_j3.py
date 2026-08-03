"""Relance J+3 des comptes gratuits — logique isolée du transport HTTP.

⚠️ POURQUOI CE MODULE EXISTE.
La relance ne vivait que dans la route `GET /api/_cron/upsell-j3`, déclenchée par
un `curl` depuis un Render Cron Job. Or `qeerah.com` redirige en 301 vers
`www.qeerah.com`, et un `curl -fsS` SANS `-L` ne suit pas les redirections : le
job se terminait en succès (code 0) sans jamais atteindre la route. Le piège avait
déjà été constaté et corrigé sur `feed-radar-collect` ; le même bug était
soupçonné ici depuis juillet sans avoir jamais été vérifié — et s'il était bien
présent, AUCUNE relance J+3 n'est jamais partie.

Sortir la logique du transport HTTP supprime la classe de bug entièrement : le
cron exécute désormais du Python (`cron_upsell.py`), il n'y a plus de requête à
rediriger, plus de code de sortie trompeur, et le résultat est directement lisible
dans les logs du job.

La route HTTP est conservée et délègue ici : elle reste utile pour un
déclenchement manuel.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from urllib.parse import quote


# Fenêtre de ciblage : inscrits entre J-4 et J-3. Volontairement large d'un jour
# pour absorber un run manqué sans re-cibler ceux d'avant-hier (le drapeau
# `upsell_j3_sent` sert de garde-fou définitif).
_JOURS_MIN = 3
_JOURS_MAX = 4
_LOT_MAX = 200


async def run_upsell_j3(supabase) -> dict:
    """Envoie la relance J+3 aux comptes gratuits éligibles.

    Ne renvoie jamais d'exception : le résultat porte l'erreur, pour que l'appelant
    (route HTTP ou script cron) décide quoi en faire.
    """
    if not supabase:
        return {"ok": False, "reason": "supabase indisponible", "sent": 0, "skipped": 0}

    from auth import make_unsubscribe_token
    from email_service import email_service

    app_url = os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")
    now = datetime.now(timezone.utc)
    lo = (now - timedelta(days=_JOURS_MAX)).isoformat()
    hi = (now - timedelta(days=_JOURS_MIN)).isoformat()

    sent = 0
    skipped = 0
    failed = 0
    try:
        rows = (supabase.table("users")
                .select("email,tier,marketing_opt_out,upsell_j3_sent,created_at")
                .eq("tier", "free").gte("created_at", lo).lte("created_at", hi)
                .limit(_LOT_MAX).execute())

        for u in (rows.data or []):
            email = (u.get("email") or "").strip().lower()
            # Un désabonnement marketing ou un envoi déjà effectué sont des motifs
            # d'exclusion définitifs — jamais deux relances pour la même personne.
            if not email or u.get("marketing_opt_out") or u.get("upsell_j3_sent"):
                skipped += 1
                continue

            unsub = (f"{app_url}/unsubscribe?e={quote(email)}"
                     f"&s={make_unsubscribe_token(email)}")
            if await email_service.send_upsell_email(email, unsub, kind="j3"):
                # Le drapeau n'est posé qu'APRÈS un envoi réussi : un échec réseau
                # laisse la personne éligible au prochain passage.
                supabase.table("users").update({"upsell_j3_sent": True}) \
                        .eq("email", email).execute()
                sent += 1
            else:
                failed += 1
    except Exception as ex:
        return {"ok": False, "error": str(ex), "sent": sent,
                "skipped": skipped, "failed": failed}

    return {"ok": True, "sent": sent, "skipped": skipped, "failed": failed}
