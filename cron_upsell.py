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
    Schedule : "0 * * * *" — CHAQUE HEURE (séquence d'essai v2, fenêtres de 24 h)
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
    # Le job Render s'appelle toujours « upsell-j3 », mais il exécute la séquence
    # d'essai v2 (essai_emails.py) : bienvenue, +24 h, jour 3, 6, 7 et 10, selon ce
    # que l'utilisateur a fait. À passer en horaire sur Render ("0 * * * *").
    # MODE TEST par défaut : rien ne part tant que ESSAI_EMAILS_ACTIFS ≠ 1.
    from supabase_client import supabase_service
    import essai_emails

    if not supabase_service:
        print("❌ essai-emails : client Supabase indisponible "
              "(SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY manquants ?)")
        return 1

    resultat = asyncio.run(essai_emails.run(supabase_service))
    print("Séquence d'essai terminée :", resultat)
    return 0 if resultat.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
