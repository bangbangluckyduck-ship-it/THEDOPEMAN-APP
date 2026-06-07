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
import time
from datetime import date, timedelta
from typing import Any, Optional

import httpx

KEYAPI_BASE = "https://api.keyapi.ai"

# ── Disjoncteur quota : si KeyAPI renvoie 402 (quota épuisé), on arrête d'appeler
# l'API pendant _COOLDOWN_SECONDS pour ne pas gaspiller de tentatives. ───────────
_COOLDOWN_SECONDS = 1800  # 30 min
_cooldown_until = 0.0


def _in_cooldown() -> bool:
    return time.time() < _cooldown_until


def _trip_cooldown() -> None:
    global _cooldown_until
    _cooldown_until = time.time() + _COOLDOWN_SECONDS
    print(f"⚠️ KeyAPI quota épuisé → cooldown {_COOLDOWN_SECONDS}s")

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
    """Appel KeyAPI authentifié → renvoie body['data'] (ou lève). Disjoncteur quota intégré."""
    token = _token()
    if not token:
        raise RuntimeError("KEYAPI_TOKEN manquant")
    if _in_cooldown():
        raise RuntimeError("KeyAPI en cooldown (quota récemment épuisé)")
    async with httpx.AsyncClient(timeout=25.0) as client:
        resp = await client.get(
            f"{KEYAPI_BASE}{path}",
            params=params,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
    try:
        body = resp.json()
    except Exception:
        body = None
    # Détection quota épuisé → déclenche le disjoncteur
    msg = str((body or {}).get("message", "")).lower() if isinstance(body, dict) else ""
    if resp.status_code == 402 or (isinstance(body, dict) and body.get("code") == 402) or "quota" in msg:
        _trip_cooldown()
        raise RuntimeError("KeyAPI quota épuisé")
    resp.raise_for_status()
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
        # Followers = total (le champ période vaut 0). Ventes/GMV = PÉRIODE du
        # classement (total_sale_cnt) et non le cumulé all-time (…_history_cnt).
        "followers": r.get("total_followers_history_cnt") or r.get("total_followers_cnt") or 0,
        "sales": r.get("total_sale_cnt") or r.get("total_sale_history_cnt") or 0,
        "gmv": r.get("total_sale_gmv_amt") or r.get("total_sale_gmv_history_amt") or 0,
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
        "url": f"https://www.tiktok.com/view/product/{pid}" if pid else None,
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
        params["category_id"] = cid   # nom de param correct (doc) — était product_category_id
    data = await _get("/v1/tiktok/influencer/ranking/analytics", params)
    rows = data if isinstance(data, list) else []
    # Fallback : si le filtre catégorie ne renvoie rien, on retombe sur le global
    if not rows and cid:
        params.pop("category_id", None)
        data = await _get("/v1/tiktok/influencer/ranking/analytics", params)
        rows = data if isinstance(data, list) else []
    return [_clean_creator(r) for r in rows][:limit]


def _clean_rank_product(p: dict) -> dict:
    """Produit issu du classement officiel (Product Ranking Analytics) — vraies
    ventes sur la période. Pas d'image fournie par ce endpoint."""
    pid = p.get("product_id")
    return {
        "id": pid,
        "name": (p.get("product_name") or "")[:120],
        "image": None,
        "price": p.get("spu_avg_price") or p.get("min_price") or 0,
        "sales": p.get("total_sale_cnt") or 0,
        "gmv": p.get("total_sale_gmv_amt") or 0,
        "videos": p.get("total_video_cnt") or 0,
        "creators_count": p.get("total_ifl_cnt") or 0,
        "region": p.get("region"),
        "url": f"https://www.tiktok.com/view/product/{pid}" if pid else None,
    }


async def get_top_products(category: Optional[str] = None, region: str = "US", limit: int = 8) -> list[dict]:
    """VRAI top produits sur la période (classement officiel par ventes).
    Endpoint « Product Ranking (Analytics) ». Params calqués sur le ranking influenceurs
    (à reconfirmer au 1er test payant)."""
    params = {
        "date": _default_rank_date(),
        "region": region or "US",
        "rank_type": 3,            # 3 = mensuel (~30 jours, dernier mois complet) — doc
        "product_rank_field": 1,   # REQUIS : 1 = tri par ventes (total_sale_cnt)
        "page_num": 1,
        "page_size": min(max(limit, 1), 10),   # doc : page_size max = 10
    }
    cid = CATEGORY_ID_MAP.get((category or "").lower().strip())
    if cid:
        params["category_id"] = cid   # nom de param correct (doc)
    data = await _get("/v1/tiktok/product/ranking/analytics", params)
    rows = data if isinstance(data, list) else []
    if not rows and cid:
        params.pop("category_id", None)
        data = await _get("/v1/tiktok/product/ranking/analytics", params)
        rows = data if isinstance(data, list) else []
    return [_clean_rank_product(r) for r in rows][:limit]


async def get_category_overview(category: Optional[str], region: str = "US") -> dict:
    """Vue catégorie : top créateurs (mensuel) + VRAI top produits (classement 30j).
    Fallback : si le classement produit échoue, on retombe sur les produits portés
    par les meilleurs créateurs (avec images, mais ventes cumulées)."""
    creators = await get_top_creators(category, region, limit=6)

    products: list = []
    try:
        products = await get_top_products(category, region, limit=8)
    except Exception as e:
        print(f"category_overview top_products error: {e}")

    if not products:
        # Fallback (ancien comportement) : produits des 2 meilleurs créateurs.
        seen: set = set()
        for c in creators[:2]:
            uid, user_id = c.get("unique_id"), c.get("user_id")
            if not (uid and user_id):
                continue
            try:
                detail = await get_creator_detail(uid, user_id)
                for p in detail.get("products", []):
                    pid = p.get("id")
                    if pid and pid not in seen:
                        seen.add(pid)
                        products.append(p)
            except Exception as e:
                print(f"category_overview fallback product error: {e}")
        products.sort(key=lambda p: p.get("sales") or 0, reverse=True)
        products = products[:8]

    return {"creators": creators, "products": products}


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints « realtime » (nouveaux 2026) :
#   /v1/tiktok/realtime/product/search       → recherche produits par mot-clé
#   /v1/tiktok/realtime/product/detail_new_app → fiche produit + VRAIE URL
# Schéma validé sur exemples KeyAPI ; params à reconfirmer au 1er test payant.
# ─────────────────────────────────────────────────────────────────────────────

def _clean_search_product(item: dict) -> Optional[dict]:
    """Parse un item de /realtime/product/search (carte Lynx → raw_data JSON string)."""
    try:
        raw = item.get("data", {}).get("raw_data")
        parsed = json.loads(raw) if isinstance(raw, str) else (raw or {})
        vo = parsed.get("view_object") or {}
        clp = (vo.get("commonLogParams") or {}).get("cardLog") or {}
        base = (vo.get("commonLogParams") or {}).get("baseLog") or {}
        pid = clp.get("product_id") or parsed.get("search_result_id")
        if not pid:
            return None
        return {
            "id": pid,
            "name": (clp.get("title_text") or "")[:120],
            "image": (vo.get("dynamicData") or {}).get("cover"),
            "price": clp.get("show_price") or clp.get("sales_price") or "",
            "currency": clp.get("currency") or "",
            "rating": clp.get("rate") or "",
            "sales": clp.get("volume") or 0,
            "seller": base.get("seller_name") or "",
            "url": f"https://www.tiktok.com/view/product/{pid}",
        }
    except Exception:
        return None


async def search_products(keyword: str, region: str = "US", limit: int = 8) -> list[dict]:
    """Recherche les produits tendance pour un mot-clé (reco « produits similaires »)."""
    if not keyword:
        return []
    params = {"keyword": keyword, "region": region or "US"}
    data = await _get("/v1/tiktok/realtime/product/search", params)
    items: list = []
    # structure : data.body.sections[].items[]
    body = (data or {}).get("body") if isinstance(data, dict) else None
    for sec in (body or {}).get("sections", []) if isinstance(body, dict) else []:
        for it in sec.get("items", []) or []:
            cleaned = _clean_search_product(it)
            if cleaned:
                items.append(cleaned)
    return items[:limit]


def _dig(d: Any, *keys: str) -> Any:
    """Navigation défensive dans un dict imbriqué."""
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


async def get_product_detail(product_id: str, region: str = "US") -> Optional[dict]:
    """Fiche produit réelle via detail_new_app → titre, image, prix, ventes, VRAIE URL."""
    if not product_id:
        return None
    data = await _get("/v1/tiktok/realtime/product/detail_new_app",
                      {"product_id": product_id, "region": region or "US"})
    # data = bloc intermédiaire {code, data:{goda_protocol...}, message}
    products = _dig(data, "data", "goda_protocol", "data", "global", "product_info_resp", "products")
    if not (isinstance(products, list) and products):
        return None
    p = products[0]
    base = p.get("product_base") or {}
    price = base.get("price") or {}
    images = base.get("images") or []
    img = None
    if images and isinstance(images[0], dict):
        ul = images[0].get("url_list") or []
        img = ul[0] if ul else None
    review = p.get("product_detail_review") or {}
    seller = p.get("seller") or {}
    # VRAIE URL : share_deep_link nu (sans encode_params de tracking)
    pid = p.get("product_id") or product_id
    return {
        "id": pid,
        "name": (base.get("title") or "")[:160],
        "image": img,
        "price": price.get("real_price") or "",
        "original_price": price.get("original_price") or "",
        "currency": price.get("currency") or "",
        "discount": price.get("discount") or "",
        "sales": base.get("sold_count") or 0,
        "rating": review.get("product_rating") or "",
        "reviews": review.get("review_count") or 0,
        "category": base.get("category_name") or "",
        "seller": seller.get("name") or "",
        "url": f"https://www.tiktok.com/view/product/{pid}",
    }


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
