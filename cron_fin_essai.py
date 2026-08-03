"""Entrée CRON de la séquence « premiers testeurs ».

⚠️ **N'ENVOIE RIEN PAR DÉFAUT.** Sans `--envoyer`, le script simule : il affiche
qui recevrait quoi, sur quelle piste, avec quel sujet — et n'expédie rien. Un
e-mail parti ne se rattrape pas : le mode sûr doit être celui qu'on obtient sans
y penser.

    python3 cron_fin_essai.py                        # simulation des 3 étapes
    python3 cron_fin_essai.py annonce                # simulation d'une étape
    python3 cron_fin_essai.py annonce --envoyer      # envoi réel

Étapes : annonce · essai_termine · derniere_chance (cf. fin_essai.py).

Configuration Render, une fois le texte validé — un seul job quotidien suffit,
chaque étape ne retient que les comptes dans sa fenêtre :
    Cron Job « fin-essai »
    Command  : python3 cron_fin_essai.py --envoyer
    Schedule : "0 9 * * *"
    Env      : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, APP_PUBLIC_URL,
               APP_SIGNING_SECRET + configuration d'envoi (Resend / SMTP).

Prérequis base : trois colonnes booléennes sur `users` —
`trial_mail_annonce`, `trial_mail_essai_termine`, `trial_mail_derniere_chance`.
"""
from __future__ import annotations

import asyncio
import sys

from dotenv import load_dotenv

load_dotenv()


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    envoi_reel = "--envoyer" in sys.argv

    # --exclure a@b.c,d@e.f — écarte des adresses pour CE lancement seulement.
    # Sert aux cas qu'aucune règle automatique ne peut trancher : adresses
    # visiblement issues d'une faute de frappe, dont on ne sait pas si elles
    # existent ni à qui elles appartiennent. Les coder en dur dans le dépôt
    # serait pire ; les décider au lancement laisse la main à l'humain.
    exclus = set()
    for a in sys.argv:
        if a.startswith("--exclure="):
            exclus = {e.strip().lower() for e in a.split("=", 1)[1].split(",") if e.strip()}

    import fin_essai
    from supabase_client import supabase_service

    if not supabase_service:
        print("❌ Client Supabase indisponible "
              "(SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY manquants ?)")
        return 1

    etapes = args or list(fin_essai.ETAPES)
    inconnues = [e for e in etapes if e not in fin_essai.ETAPES]
    if inconnues:
        print(f"❌ Étape(s) inconnue(s) : {', '.join(inconnues)}")
        print(f"   Attendu : {' · '.join(fin_essai.ETAPES)}")
        return 1

    if not envoi_reel:
        print("MODE SIMULATION — aucun e-mail ne sera envoyé.\n")

    if exclus:
        print(f"Écartées à la demande : {', '.join(sorted(exclus))}\n")

    total_env = total_ech = 0
    for etape in etapes:
        r = asyncio.run(fin_essai.envoyer(supabase_service, etape,
                                          simulation=not envoi_reel,
                                          exclure=exclus))
        print(f"── {etape} : {r['cibles']} destinataire(s)")
        for d in r["details"]:
            print(f"     [{d['piste']:7}] {d['email'][:34]:36} "
                  f"{d['analyses']:>2} analyses · « {d['sujet']} »")
        if not r["details"]:
            print("     (personne dans la fenêtre de cette étape)")
        total_env += r["envoyes"]
        total_ech += r["echecs"]
        print()

    if envoi_reel:
        print(f"Envoyés : {total_env}   Échecs : {total_ech}")
    else:
        print("Pour envoyer réellement :")
        print("   python3 cron_fin_essai.py <étape> --envoyer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
