"""Entrée CRON autonome de la relance J+3.

⚠️ POURQUOI CE SCRIPT EXISTE.
Le Render Cron Job appelait jusqu'ici la route HTTP via `curl`. Mais `qeerah.com`
redirige en 301 vers `www.qeerah.com`, et un `curl -fsS` sans `-L` ne suit pas la
redirection : le job renvoyait 0 (« succès ») sans jamais atteindre la route. Le
même piège avait été identifié et corrigé sur `feed-radar-collect` ; ici il n'a
jamais été vérifié — s'il était présent, aucune relance J+3 n'est jamais partie.

Exécuter du Python plutôt qu'un `curl` supprime le problème à la racine : plus de
requête à rediriger, plus de code de sortie trompeur, et le compte d'e-mails
envoyés apparaît directement dans les logs du job.

Configuration Render :
    Cron Job « upsell-j3 »
    Command  : python3 cron_upsell.py
    Schedule : par ex. "0 9 * * *"
    Env      : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, APP_PUBLIC_URL,
               APP_SIGNING_SECRET (signature du lien de désinscription),
               et la configuration d'envoi d'e-mails (Resend / SMTP).

Le code de sortie est non nul si la relance a échoué : Render marque alors le job
en échec au lieu de le passer en vert silencieusement.
"""
from __future__ import annotations

import asyncio

from dotenv import load_dotenv

load_dotenv()


def main() -> int:
    from supabase_client import supabase_service
    import upsell_j3

    if not supabase_service:
        print("❌ upsell-j3 : client Supabase indisponible "
              "(SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY manquants ?)")
        return 1

    resultat = asyncio.run(upsell_j3.run_upsell_j3(supabase_service))
    print("Relance J+3 terminée :", resultat)
    return 0 if resultat.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
