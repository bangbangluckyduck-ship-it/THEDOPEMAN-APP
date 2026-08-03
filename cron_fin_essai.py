"""Entrée CRON du rappel « ton essai se termine bientôt ».

⚠️ **N'ENVOIE RIEN PAR DÉFAUT.** Sans argument, le script simule : il affiche qui
recevrait le message et à quelle échéance, sans rien expédier. Un e-mail parti ne
se rattrape pas — la simulation est le mode sûr, l'envoi est le mode explicite.

    python3 cron_fin_essai.py              # simulation, aucun envoi
    python3 cron_fin_essai.py --envoyer    # envoi réel

Configuration Render (quotidien, une fois le texte validé) :
    Cron Job « fin-essai »
    Command  : python3 cron_fin_essai.py --envoyer
    Schedule : "0 9 * * *"
    Env      : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, APP_PUBLIC_URL,
               APP_SIGNING_SECRET, et la configuration d'envoi (Resend / SMTP).

Prérequis base : une colonne booléenne `trial_ending_sent` sur `users` — elle
garantit qu'une même personne n'est jamais sollicitée deux fois.
"""
from __future__ import annotations

import asyncio
import sys

from dotenv import load_dotenv

load_dotenv()


def main() -> int:
    envoi_reel = "--envoyer" in sys.argv

    from supabase_client import supabase_service
    import fin_essai

    if not supabase_service:
        print("❌ Client Supabase indisponible "
              "(SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY manquants ?)")
        return 1

    resultat = asyncio.run(fin_essai.envoyer(supabase_service, simulation=not envoi_reel))

    if resultat["simulation"]:
        print("MODE SIMULATION — aucun e-mail envoyé.\n")
    print(f"{resultat['cibles']} destinataire(s) éligible(s) :")
    for d in resultat["details"]:
        quand = "demain" if d["jours"] <= 1 else f"dans {d['jours']} jours"
        print(f"   · {d['email']:38} essai terminé {quand}")

    if resultat["simulation"]:
        print("\nPour envoyer réellement : python3 cron_fin_essai.py --envoyer")
    else:
        print(f"\nEnvoyés : {resultat['envoyes']}   Échecs : {resultat['echecs']}")

    return 0 if resultat["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
