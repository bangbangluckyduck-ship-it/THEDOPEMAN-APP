"""
Feed Radar — feed de vidéos TikTok Shop virales (≥ seuil de vues), enrichies
d'un thumbnail oEmbed officiel TikTok, d'un GMV estimé et d'une tendance
créateur. Gold/Agency/Beta/Admin = complet, Free/Pro = aperçu (cf. main.py).

Découverte CRÉATEUR-CENTRIQUE (pas d'endpoint "vidéos tendance" générique) :
top créateurs (ranking déjà utilisé par market_creators.get_top_creators) →
leurs vidéos (/influencer/videos) → filtre vues.

GMV et tendance au niveau CRÉATEUR, pas vidéo : les endpoints KeyAPI
vidéo→produit (video/products/analytics) et vidéo→trend (video/trends/analytics)
renvoient systématiquement vide en pratique (testé sur 10 vraies vidéos,
dont une explicitement shop-taguée) — confirmé en direct, pas une supposition.
Le GMV par vidéo est donc un CALCUL, jamais une donnée API brute :

    GMV_estimé = vues × CTOR (taux de conversion) × prix moyen des produits
                 vendus par le créateur

CTOR calibré sur ~65 vraies vidéos TikTok Shop (captures GMV/vues/ventes
réelles fournies par Aimeric, juin 2026) : pour les vidéos ≥ ~100k vues
(la population exacte de Feed Radar), le ratio articles-vendus/vues tourne
autour de 0.03-0.06%, moyenne ≈ 0.04% — PAS 1-2% comme un CTOR "clic→achat"
classique le laisserait penser (la quasi-totalité des vues ne cliquent
jamais). Toujours labellisé "GMV estimé" côté UI (jamais "GMV" nu).

Volumes amplifiés le 2026-07-02 (crédits KeyAPI à écouler avant expiration) :
seuil de vues abaissé (50k), 7 passes de découverte par région (6 catégories
+ 1 classement global), 2 pages de créateurs par passe (~20 au lieu de 10),
20 vidéos par créateur (au lieu de 10). Le coût réel par run n'est PAS
mesuré précisément (le ratio appel KeyAPI ↔ crédit consommé n'est pas connu
ici) — surveiller la conso réelle sur le dashboard KeyAPI après les premiers
runs plutôt que de se fier à une estimation.
"""
from __future__ import annotations

import os
from datetime import date, timedelta
from typing import Optional

import httpx

import market_creators as mc

FEED_RADAR_VIEW_THRESHOLD = int(os.getenv("FEED_RADAR_VIEW_THRESHOLD", "50000"))
# 0.04% = calibré empiriquement sur ~65 vraies vidéos TikTok Shop ≥ ~100k vues
# (articles vendus / vues). PAS 1-2% : ça correspondrait à un taux clic→achat,
# pas vue→achat (l'écrasante majorité des vues ne cliquent jamais).
FEED_RADAR_DEFAULT_CTOR = float(os.getenv("FEED_RADAR_DEFAULT_CTOR", "0.0004"))
# None = classement global (sans filtre catégorie), en plus des 6 catégories —
# capte des créateurs qui ne sortent dans aucun classement par catégorie.
FEED_RADAR_CATEGORIES = ["beaute", "mode", "tech", "fitness", "sante", "maison", None]
# Nb de pages de créateurs récupérées par catégorie/région (10 créateurs/page,
# max API) — 5 pages = jusqu'à 50 créateurs par catégorie. La boucle s'arrête
# d'elle-même dès qu'une page revient vide (pas de gaspillage si le classement
# KeyAPI a moins de créateurs que ça pour une catégorie/région donnée).
FEED_RADAR_CREATOR_PAGES = int(os.getenv("FEED_RADAR_CREATOR_PAGES", "10"))
# Mêmes régions que MARKET_COUNTRIES (static/app_v3.js) — marchés déjà
# confirmés couverts par KeyAPI pour "Créateurs Gagnants". Override possible
# via env (liste séparée par virgules) pour réduire le coût KeyAPI si besoin.
FEED_RADAR_REGIONS = [
    r.strip().upper() for r in os.getenv(
        "FEED_RADAR_REGIONS", "FR,US,GB,BR,DE,ES,IT,ID,MY"  # FR en priorité : audience cœur de cible de l'app
    ).split(",") if r.strip()
]

_TIKTOK_OEMBED_URL = "https://www.tiktok.com/oembed"


def estimate_video_gmv(views: int, avg_product_price: float,
                       ctor: float = FEED_RADAR_DEFAULT_CTOR) -> float:
    """GMV_estimé = vues × CTOR × prix moyen produit. Aucune donnée API réelle
    de conversion par vidéo n'étant exposée par KeyAPI, c'est un calcul
    indicatif — toujours affiché "GMV estimé" côté UI."""
    if not views or not avg_product_price:
        return 0.0
    orders_estimated = views * ctor
    return round(orders_estimated * avg_product_price, 2)


async def fetch_oembed(video_url: str) -> Optional[dict]:
    """API officielle TikTok, sans auth. Renvoie thumbnail_url/html/author_name
    ou None si la vidéo n'est plus accessible publiquement."""
    if not video_url:
        return None
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(_TIKTOK_OEMBED_URL, params={"url": video_url})
        if r.status_code != 200:
            return None
        data = r.json()
        return {
            "thumbnail_url": data.get("thumbnail_url"),
            "html": data.get("html"),
            "author_name": data.get("author_name"),
        }
    except Exception as e:
        print(f"fetch_oembed({video_url}) error: {e}")
        return None


async def discover_candidate_videos(region: str = "US",
                                    categories: Optional[list] = None) -> list[dict]:
    """Découverte créateur-centrique : top créateurs (par catégorie) → leurs
    vidéos → filtre vues >= FEED_RADAR_VIEW_THRESHOLD. Renvoie une liste de
    dicts vidéo (cf. market_creators._clean_video) enrichis de creator_uid/
    creator_unique_id/creator_nickname."""
    categories = categories if categories is not None else FEED_RADAR_CATEGORIES
    seen_video_ids: set = set()
    candidates: list[dict] = []

    seen_creators: set = set()
    for category in categories:
        creators: list = []
        for page in range(1, FEED_RADAR_CREATOR_PAGES + 1):
            try:
                page_creators = await mc.get_top_creators(category, region, limit=10, page_num=page)
            except Exception as e:
                print(f"discover_candidate_videos({category}, page {page}) ranking error: {e}")
                break
            if not page_creators:
                break
            creators.extend(page_creators)
        for creator in creators:
            unique_id = creator.get("unique_id")
            user_id = creator.get("user_id")
            if not unique_id or unique_id in seen_creators:
                continue
            seen_creators.add(unique_id)
            try:
                vdata = await mc._get("/v1/tiktok/influencer/videos",
                                      {"unique_id": unique_id, "page_num": 1, "page_size": 20})
                aweme = (vdata or {}).get("aweme_list") if isinstance(vdata, dict) else None
                videos = [mc._clean_video(v) for v in (aweme or [])]
            except Exception as e:
                print(f"discover_candidate_videos videos({unique_id}) error: {e}")
                continue
            for v in videos:
                vid = v.get("id")
                if not vid or vid in seen_video_ids:
                    continue
                if (v.get("views") or 0) < FEED_RADAR_VIEW_THRESHOLD:
                    continue
                seen_video_ids.add(vid)
                candidates.append({
                    **v,
                    "creator_unique_id": unique_id,
                    "creator_uid": user_id,
                    "creator_nickname": creator.get("nickname"),
                    "region": region,
                })
    return candidates


_collection_running = False


async def run_feed_radar_collection(region: Optional[str] = None) -> dict:
    """Point d'entrée du cron : boucle sur FEED_RADAR_REGIONS (tous les marchés
    déjà couverts par KeyAPI, cf. MARKET_COUNTRIES côté frontend) sauf si un
    `region` précis est fourni (utile pour un déclenchement manuel ciblé).

    Garde anti-chevauchement : un run profond (10 pages × 9 régions) dure ~2h ;
    si le cron (6h) ou un déclenchement manuel repart pendant qu'un run tourne
    encore, on refuse au lieu d'empiler deux collectes dans le process web
    (RAM + crédits KeyAPI doublés)."""
    global _collection_running
    if _collection_running:
        return {"ok": False, "error": "Collecte déjà en cours, réessaie plus tard.",
                "found": 0, "new": 0, "updated": 0}
    from supabase_client import supabase_service as supabase
    if not supabase:
        return {"ok": False, "error": "Supabase indisponible", "found": 0, "new": 0, "updated": 0}

    _collection_running = True
    try:
        return await _run_collection(region, supabase)
    finally:
        _collection_running = False


async def _run_collection(region: Optional[str], supabase) -> dict:
    regions = [region.upper()] if region else FEED_RADAR_REGIONS
    totals = {"found": 0, "new": 0, "updated": 0}
    by_region = {}
    for r in regions:
        try:
            res = await _collect_region(r, supabase)
        except Exception as e:
            print(f"run_feed_radar_collection region {r} error: {e}")
            res = {"found": 0, "new": 0, "updated": 0}
        by_region[r] = res
        totals["found"] += res["found"]
        totals["new"] += res["new"]
        totals["updated"] += res["updated"]

    return {"ok": True, **totals, "by_region": by_region}


async def _collect_region(region: str, supabase) -> dict:
    """Collecte pour UNE région : découverte → filtre vues → GMV estimé +
    tendance créateur → oEmbed (nouvelles vidéos seulement) → upsert."""
    candidates = await discover_candidate_videos(region)
    found = len(candidates)
    new_count = 0
    updated_count = 0

    # Vidéos déjà connues (pour éviter un re-fetch oEmbed inutile).
    existing_ids: set = set()
    try:
        existing_rows = supabase.table("feed_radar_videos").select("video_id") \
            .in_("video_id", [c["id"] for c in candidates]).execute().data or []
        existing_ids = {r["video_id"] for r in existing_rows}
    except Exception as e:
        print(f"_collect_region({region}) existing lookup error: {e}")

    # Cache par créateur (GMV 30j + prix moyen) — évite de répéter les mêmes
    # appels KeyAPI pour chaque vidéo d'un même créateur dans cette collecte.
    creator_cache: dict = {}

    async def _creator_context(uid: Optional[str]):
        if not uid:
            return {"series": [], "avg_price": 0.0, "gmv_30d": 0.0}
        if uid in creator_cache:
            return creator_cache[uid]
        avg_price = 0.0
        series: list = []
        gmv_30d = 0.0
        try:
            gmv_data = await mc.get_creator_gmv_30d(uid, days=30)
            series = gmv_data.get("series") or []
            gmv_30d = gmv_data.get("gmv_30d") or 0.0
        except Exception as e:
            print(f"_creator_context gmv error ({uid}): {e}")
        try:
            best_sellers = await mc.get_creator_best_sellers(uid, limit=10)
            prices = [p.get("price") or 0 for p in best_sellers if p.get("price")]
            avg_price = round(sum(prices) / len(prices), 2) if prices else 0.0
        except Exception as e:
            print(f"_creator_context products error ({uid}): {e}")
        ctx = {"series": series, "avg_price": avg_price, "gmv_30d": gmv_30d}
        creator_cache[uid] = ctx
        return ctx

    for v in candidates:
        video_id = v["id"]
        is_new = video_id not in existing_ids
        ctx = await _creator_context(v.get("creator_uid"))
        gmv_estimated = estimate_video_gmv(v.get("views") or 0, ctx["avg_price"])
        # Garde-fou : même calibré sur des données réelles, un taux moyen linéaire
        # décroche sur les vidéos extrêmement virales (testé : une vidéo à 24,5M
        # vues donnait une estimation à 190% du GMV réel du créateur sur 30j).
        # Le GMV estimé d'UNE vidéo ne peut jamais dépasser le GMV réel du
        # créateur sur 30 jours (donnée réelle, déjà récupérée).
        if ctx["gmv_30d"]:
            gmv_estimated = min(gmv_estimated, ctx["gmv_30d"])

        row = {
            "video_id": video_id,
            "video_url": v.get("url"),
            "creator_unique_id": v.get("creator_unique_id"),
            "creator_nickname": v.get("creator_nickname"),
            "region": v.get("region"),
            "views": v.get("views") or 0,
            "likes": v.get("likes") or 0,
            "comments": v.get("comments") or 0,
            "shares": v.get("shares") or 0,
            "trend_snapshot": ctx["series"],
            "gmv_estimated": gmv_estimated,
            "gmv_estimation_method": "calculated_ctor",
            "ctor_used": FEED_RADAR_DEFAULT_CTOR,
            "avg_product_price": ctx["avg_price"],
            "view_threshold_used": FEED_RADAR_VIEW_THRESHOLD,
        }

        if is_new:
            oembed = await fetch_oembed(v.get("url"))
            if oembed:
                row["oembed_thumbnail_url"] = oembed.get("thumbnail_url")
                row["oembed_html"] = oembed.get("html")
                row["oembed_author_name"] = oembed.get("author_name")
                from datetime import datetime, timezone
                row["oembed_fetched_at"] = datetime.now(timezone.utc).isoformat()
            new_count += 1
        else:
            updated_count += 1

        try:
            supabase.table("feed_radar_videos").upsert(row, on_conflict="video_id").execute()
        except Exception as e:
            print(f"_collect_region({region}) upsert error ({video_id}): {e}")

    return {"found": found, "new": new_count, "updated": updated_count}
