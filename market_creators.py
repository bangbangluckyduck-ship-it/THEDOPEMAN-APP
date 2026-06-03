"""
Intelligence marché « Créateurs Gagnants » (Gold / Agency) via KeyAPI.

Chaîne créateur-centric (validée 2/6) :
  1. /v1/tiktok/influencer/ranking/analytics  → top créateurs (ventes)
  2. /v1/tiktok/influencer/videos              → leurs vidéos (param unique_id)
  3. /v1/tiktok/influencer/products/analytics  → leurs produits (param user_id)

Données 100% réelles : liens directs (profil @unique_id, vidéo share_url, fiche
produit), vraies miniatures, vraies stats. Aucune fabrication.
"""
from __future__ import annotations

import json
import os
from datetime import date, timedelta
from typing import Any, Optional

import httpx

KEYAPI_BASE = "https://api.keyapi.ai"

# app category → product_category_id TikTok (filtre optionnel du ranking)
CATEGORY_ID_MAP: dict[str, str] = {
    "beaute": "601450", "beauté": "601450",
    "mode": "601152", "fashion": "601152",
    "tech": "601739", "electronique": "601739",
    "fitness": "603014", "sport": "603014",
    "sante": "700645", "santé": "700645",
    "maison": "600942",
}


def _token() -> str:
    return os.getenv("KEYAPI_TOKEN", "")


async def _get(path: str, params: dict) -> Any:
    """Appel KeyAPI authentifié → renvoie body['data'] (ou lève)."""
    token = _token()
    if not token:
        raise RuntimeError("KEYAPI_TOKEN manquant")
    async with httpx.AsyncClient(timeout=25.0) as client:
        resp = await client.get(
            f"{KEYAPI_BASE}{path}",
            params=params,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
    resp.raise_for_status()
    body = resp.json()
    if isinstance(body, dict) and body.get("code") not in (0, None):
        raise RuntimeError(f"KeyAPI error: {body.get('message') or body}")
    return body.get("data") if isinstance(body, dict) else None


def _default_rank_date() -> str:
    """1er jour du mois précédent (ranking mensuel = données complètes)."""
    today = date.today()
    first_this = today.replace(day=1)
    last_prev = first_this - timedelta(days=1)
    return last_prev.replace(day=1).isoformat()


def _first_cover(cover_field: Any) -> Optional[str]:
    """Extrait la 1ère URL d'un champ cover_url (string JSON ou liste)."""
    if not cover_field:
        return None
    try:
        data = json.loads(cover_field) if isinstance(cover_field, str) else cover_field
        if isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict):
                return first.get("url")
            if isinstance(first, str):
                return first
    except Exception:
        pass
    return None


def _clean_creator(r: dict) -> dict:
    uid = r.get("unique_id")
    return {
        "unique_id": uid,
        "user_id": r.get("user_id"),
        "nickname": r.get("nick_name") or uid,
        "avatar": r.get("avatar"),
        "profile_url": f"https://www.tiktok.com/@{uid}" if uid else None,
        "followers": r.get("total_followers_history_cnt") or r.get("total_followers_cnt") or 0,
        "sales": r.get("total_sale_history_cnt") or r.get("total_sale_cnt") or 0,
        "gmv": r.get("total_sale_gmv_history_amt") or r.get("total_sale_gmv_amt") or 0,
        "videos_count": r.get("total_post_video_history_cnt") or 0,
        "products_count": r.get("total_product_history_cnt") or 0,
        "category_id": r.get("most_category_id"),
        "region": r.get("region"),
    }


def _clean_video(v: dict) -> dict:
    stats = v.get("statistics") or {}
    vobj = v.get("video") or {}
    author = v.get("author") or {}
    uid = author.get("unique_id")
    vid = v.get("aweme_id")
    cover = None
    for key in ("cover", "origin_cover", "dynamic_cover"):
        ul = (vobj.get(key) or {}).get("url_list") or []
        if ul:
            cover = ul[0]
            break
    return {
        "id": vid,
        "desc": (v.get("desc") or "")[:150],
        "url": v.get("share_url") or (f"https://www.tiktok.com/@{uid}/video/{vid}" if uid and vid else None),
        "cover": cover,
        "views": stats.get("play_count") or 0,
        "likes": stats.get("digg_count") or 0,
        "comments": stats.get("comment_count") or 0,
        "shares": stats.get("share_count") or 0,
    }


def _clean_product(p: dict) -> dict:
    pid = p.get("product_id")
    return {
        "id": pid,
        "name": (p.get("product_name") or "")[:120],
        "image": _first_cover(p.get("cover_url")),
        "price": p.get("spu_avg_price") or 0,
        "sales": p.get("total_sale_cnt") or 0,
        "gmv": p.get("total_sale_gmv_amt") or 0,
        "url": f"https://shop.tiktok.com/view/product/{pid}" if pid else None,
    }


async def get_top_creators(category: Optional[str] = None, region: str = "US", limit: int = 10) -> list[dict]:
    params = {
        "date": _default_rank_date(),
        "region": region or "US",
        "rank_type": 3,            # mensuel
        "influencer_rank_field": 2,  # tri par ventes
        "page_num": 1,
        "page_size": min(max(limit, 1), 10),
    }
    cid = CATEGORY_ID_MAP.get((category or "").lower().strip())
    if cid:
        params["product_category_id"] = cid
    data = await _get("/v1/tiktok/influencer/ranking/analytics", params)
    rows = data if isinstance(data, list) else []
    return [_clean_creator(r) for r in rows][:limit]


async def get_creator_detail(unique_id: str, user_id: str, region: str = "US") -> dict:
    videos: list = []
    products: list = []
    try:
        vdata = await _get("/v1/tiktok/influencer/videos",
                           {"unique_id": unique_id, "page_num": 1, "page_size": 6})
        aweme = (vdata or {}).get("aweme_list") if isinstance(vdata, dict) else None
        videos = [_clean_video(v) for v in (aweme or [])][:6]
    except Exception as e:
        print(f"market_creators videos error: {e}")
    if user_id:
        try:
            pdata = await _get("/v1/tiktok/influencer/products/analytics",
                               {"user_id": user_id, "page_num": 1, "page_size": 6})
            prows = pdata if isinstance(pdata, list) else []
            products = [_clean_product(p) for p in prows][:6]
        except Exception as e:
            print(f"market_creators products error: {e}")
    return {"unique_id": unique_id, "videos": videos, "products": products}
