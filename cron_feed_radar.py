"""Entrée CRON autonome de la collecte Feed Radar.

⚠️ POURQUOI CE SCRIPT EXISTE (fix OOM) :
La collecte (découverte créateurs → vidéos → GMV réel/estimé → oEmbed, ~9 régions)
est longue et gourmande en RAM. Tant qu'elle était déclenchée via l'endpoint HTTP
`/api/_cron/feed-radar-collect`, elle tournait DANS le process web (512 Mo, 2 workers)
et le faisait tomber en OOM à l'heure du cron — d'où une collecte qui ne finissait
jamais (base qui ne se rafraîchissait que de ~40 lignes/jour).

Ce script fait tourner la MÊME collecte dans un process DÉDIÉ (Render Cron Job), isolé
du web. Configuration Render :
    Cron Job « feed-radar-collect »
    Command : python3 cron_feed_radar.py
    Schedule : par ex. "30 1,4 * * *" (heures creuses FR)
    (même env group que le web : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, KEYAPI_TOKEN…)

Usage manuel / ciblé :
    python3 cron_feed_radar.py            # toutes les régions
    python3 cron_feed_radar.py FR         # une seule région
"""
from __future__ import annotations

import asyncio
import sys


def main() -> int:
    region = sys.argv[1].strip().upper() if len(sys.argv) > 1 and sys.argv[1].strip() else None
    import feed_radar
    summary = asyncio.run(feed_radar.run_feed_radar_collection(region))
    print("Feed Radar collect terminé :", summary)
    # Code de sortie non-nul si la collecte a échoué → visible dans les logs Render.
    return 0 if summary.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
