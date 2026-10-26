"""Entrée CRON de l'e-mail hebdo « Ce qui vend cette semaine » (hebdo.py).

Normalement lancé par le cron horaire « upsell-j3 » (cron_upsell.py), le lundi à
8 h UTC — pas de service Render de plus. Ce script reste utile pour un envoi à la
main ou si un cron dédié est créé un jour :
    Command  : python3 cron_hebdo.py
    Schedule : "0 8 * * 1"   (lundi, 8 h UTC)
    Env      : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, APP_PUBLIC_URL,
               APP_SIGNING_SECRET, configuration d'envoi (Resend / SMTP),
               HEBDO_ACTIF=1 une fois les textes validés (sinon : simulation,
               les e-mails sont écrits dans les journaux, rien ne part).

Le code de sortie est non nul en cas d'échec : Render marque alors le job en
échec au lieu de le passer en vert silencieusement.
"""
from __future__ import annotations

import asyncio

from dotenv import load_dotenv

load_dotenv()


def main() -> int:
    from supabase_client import supabase_service
    import hebdo

    if not supabase_service:
        print("❌ hebdo : client Supabase indisponible "
              "(SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY manquants ?)")
        return 1
    resultat = asyncio.run(hebdo.run(supabase_service))
    print("E-mail hebdo :", resultat)
    return 0 if resultat.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
