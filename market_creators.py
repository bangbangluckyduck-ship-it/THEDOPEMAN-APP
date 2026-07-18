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

import asyncio
import json
import os
import re
import time
from datetime import date, datetime, timedelta
from typing import Any, Optional
from urllib.parse import quote

import httpx


# Heuristique d'exclusion des comptes « shop / boutique » (on veut des créateurs).
_SHOP_TOKENS = ("shop", "store", "official", "boutique", "mall", "outlet",
                "™", "officiel", "flagship")


def is_shop_account(nickname: Optional[str], unique_id: Optional[str]) -> bool:
    blob = f"{nickname or ''} {unique_id or ''}".lower()
    return any(tok in blob for tok in _SHOP_TOKENS)

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
    "sante": "700645", "santé": "700645", "complement_sante": "700645",
    "maison": "600942", "electromenager": "600942",
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
    # Surface le message d'erreur RÉEL de KeyAPI (souvent : quel param manque)
    if resp.status_code >= 400:
        raise RuntimeError(f"KeyAPI {resp.status_code}: {resp.text[:400]}")
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
    # Post photo-carrousel TikTok (photo mode) : présence de image_post_info.
    # Feed Radar veut les mettre en avant (même format que ce que l'user génère).
    img_post = v.get("image_post_info") if isinstance(v.get("image_post_info"), dict) else None
    carousel_images = (img_post or {}).get("images") or []
    return {
        "id": vid,
        "desc": (v.get("desc") or "")[:150],
        "url": v.get("share_url") or (f"https://www.tiktok.com/@{uid}/video/{vid}" if uid and vid else None),
        "cover": cover,
        "views": stats.get("play_count") or 0,
        "likes": stats.get("digg_count") or 0,
        "comments": stats.get("comment_count") or 0,
        "shares": stats.get("share_count") or 0,
        "is_carousel": bool(carousel_images),
        "image_count": len(carousel_images),
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


async def get_top_creators(category: Optional[str] = None, region: str = "US", limit: int = 10,
                           page_num: int = 1) -> list[dict]:
    params = {
        "date": _default_rank_date(),
        "region": region or "US",
        "rank_type": 3,            # mensuel
        "influencer_rank_field": 2,  # tri par ventes
        "page_num": page_num,
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
    cleaned = [_clean_creator(r) for r in rows]
    # Exclure les comptes shop/boutique (on veut des créateurs).
    cleaned = [c for c in cleaned if not is_shop_account(c.get("nickname"), c.get("unique_id"))]
    return cleaned[:limit]


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


def _trend_pct_change(rows: list[dict]) -> Optional[float]:
    """Delta % entre le jour le plus ancien et le plus récent d'une série de snapshots
    quotidiens triés ou non (clé `dt`, valeur `total_sale_gmv_1d_amt`). `None` explicite
    si la série est trop courte ou si le jour de référence est à 0 (jamais de chiffre
    inventé par division par zéro)."""
    if not rows or len(rows) < 2:
        return None
    ordered = sorted(rows, key=lambda r: r.get("dt") or "")
    first = ordered[0].get("total_sale_gmv_1d_amt") or 0
    last = ordered[-1].get("total_sale_gmv_1d_amt") or 0
    if not first:
        return None
    return round((last - first) / first * 100, 1)


async def get_product_momentum(product_id: str, days: int = 14) -> Optional[dict]:
    """Momentum GMV d'un produit sur `days` jours (endpoint /product/trends/analytics,
    corrigé mi-2026 en même temps que le GMV vidéo). 1 appel, page_size=10. Les snapshots
    quotidiens sont ÉPARS en pratique (vérifié en live : 3 jours de données sur une fenêtre
    de 14, pas un point par jour) — fenêtre élargie à 14j (vs. 7j initialement prévu) pour
    avoir une chance raisonnable de capter ≥2 points de comparaison."""
    if not product_id:
        return None
    end = date.today()
    start = end - timedelta(days=days - 1)
    try:
        rows = await _get("/v1/tiktok/product/trends/analytics", {
            "product_id": str(product_id),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "page_num": 1,
            "page_size": 10,
        })
    except Exception as e:
        print(f"get_product_momentum({product_id}) error: {e}")
        return None
    rows = rows if isinstance(rows, list) else []
    pct = _trend_pct_change(rows)
    if pct is None:
        return {"pct_change": None, "direction": None, "days_covered": len(rows)}
    direction = "up" if pct > 0 else ("down" if pct < 0 else "flat")
    return {"pct_change": pct, "direction": direction, "days_covered": len(rows)}


async def enrich_products_momentum(products: list[dict], region: str) -> list[dict]:
    """Attache un `momentum` (delta GMV 7j) à chaque produit d'une liste déjà bornée
    (~8 max, comme affiché côté UI) — jamais crash sur un échec individuel."""
    async def _one(p: dict) -> dict:
        try:
            mom = await get_product_momentum(p.get("id"))
        except Exception as e:
            print(f"enrich_products_momentum({p.get('id')}) error: {e}")
            mom = None
        return {**p, "momentum": mom}
    return list(await asyncio.gather(*(_one(p) for p in products)))


async def get_category_momentum(region: str = "US") -> list[dict]:
    """DÉSACTIVÉ — vérifié en live 2026-07 : /category/trend/analytics ne se comporte PAS
    comme documenté quand on interroge un category_id de niveau 1 seul (sans
    category_l2_id/category_l3_id) : au lieu d'une série temporelle multi-jours, il
    renvoie une VENTILATION PAR SOUS-CATÉGORIE sur un seul jour (page_num pagine les
    sous-catégories, pas les dates — confirmé : page 1 et page 2 renvoient toutes les
    deux dt=même jour, avec des category_l2_id/l3_id différents). Une vraie série
    temporelle n'apparaît qu'en scopant sur UN category_l2_id + category_l3_id précis
    — mais le nombre de sous-catégories par catégorie canonique n'est pas connu, donc
    impossible d'agréger un delta L1 fiable sans un fan-out de cardinalité inconnue
    (violerait la règle "jamais de troncature silencieuse"). Retourne [] tant que ce
    n'est pas correctement rebâti — mieux vaut une fonctionnalité absente qu'un signal
    structurellement biaisé affiché comme fiable."""
    return []


async def get_category_overview(category: Optional[str], region: str = "US") -> dict:
    """Vue catégorie : top créateurs (mensuel) + VRAI top produits (classement 30j, enrichis
    d'un momentum GMV 7j). Fallback : si le classement produit échoue, on retombe sur les
    produits portés par les meilleurs créateurs (avec images, mais ventes cumulées)."""
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

    try:
        products = await enrich_products_momentum(products, region)
    except Exception as e:
        print(f"category_overview momentum error: {e}")

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


# ── Extraction product_id depuis une URL TikTok Shop + fiche officielle ──────────
_PRODUCT_ID_RE = re.compile(r"/product/(\d{6,})")
_LONG_DIGITS_RE = re.compile(r"(\d{12,})")


def extract_product_id(url: str) -> Optional[str]:
    """Extrait le product_id numérique d'une URL TikTok Shop.
    Gère .../view/product/<id>, shop.tiktok.com/..., ou un long id numérique en repli."""
    if not url:
        return None
    m = _PRODUCT_ID_RE.search(url)
    if m:
        return m.group(1)
    m = _LONG_DIGITS_RE.search(url)
    return m.group(1) if m else None


async def _resolve_short_url(url: str) -> str:
    """Suit les redirections des liens courts TikTok (vt/vm.tiktok.com) → URL finale."""
    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as c:
            r = await c.get(url, headers={"User-Agent": "Mozilla/5.0"})
            return str(r.url)
    except Exception:
        return url


async def get_product_detail_from_url(url: str, regions: Optional[list] = None) -> Optional[dict]:
    """URL TikTok Shop → fiche produit OFFICIELLE (nom, image HD, prix, catégorie).
    La région n'est pas dans l'URL → on essaie plusieurs régions (CAROUSEL_PRODUCT_REGIONS)."""
    if not url:
        return None
    pid = extract_product_id(url)
    if not pid:
        # Lien court → suivre la redirection puis réessayer.
        pid = extract_product_id(await _resolve_short_url(url))
    if not pid:
        return None
    if regions is None:
        regions = [r.strip().upper() for r in
                   os.getenv("CAROUSEL_PRODUCT_REGIONS", "US,GB,FR").split(",") if r.strip()]
    for region in regions:
        try:
            d = await get_product_detail(pid, region)
        except Exception:
            d = None
        if d and d.get("name"):
            d["_region"] = region
            return d
    return None


def _clean_pc_creator(r: dict) -> dict:
    """Créateur issu de Product Creators (promoteurs d'un produit). PAS de unique_id
    → lien = recherche TikTok sur le pseudo en repli. Avatar privé → initiales côté UI."""
    uid = r.get("unique_id")           # souvent absent dans ce endpoint
    nick = r.get("nick_name") or uid or ""
    if uid:
        profile = f"https://www.tiktok.com/@{uid}"
    elif nick:
        profile = f"https://www.tiktok.com/search/user?q={quote(nick)}"
    else:
        profile = None
    return {
        "unique_id": uid,
        "user_id": r.get("user_id"),
        "nickname": nick,
        "avatar": r.get("avatar"),
        "followers": r.get("total_followers_cnt") or 0,
        "views": r.get("total_views_cnt") or 0,
        "videos": r.get("total_post_video_cnt") or 0,
        "sales": r.get("per_product_ifl_sale_cnt") or 0,
        "category": r.get("category"),
        "region": r.get("region"),
        "profile_url": profile,
    }


async def get_product_creators(product_id: str, region: str = "US", limit: int = 10) -> list[dict]:
    """Créateurs qui font la promo d'un produit (Product Creators Analytics)."""
    if not product_id:
        return []
    params = {
        "date": _default_rank_date(),
        "region": region or "US",
        "rank_type": 3,
        "product_id": product_id,
        "page_num": 1,
        "page_size": min(max(limit, 1), 10),
    }
    data = await _get("/v1/tiktok/product/creators/analytics", params)
    rows = data if isinstance(data, list) else []
    return [_clean_pc_creator(r) for r in rows][:limit]


async def get_category_creators(category: Optional[str], region: str = "US", limit: int = 8) -> list[dict]:
    """« Créateurs gagnants de la catégorie » : top produits de la catégorie → leurs
    créateurs, dédupliqués, triés par followers. Exclut les comptes shop."""
    products = await get_top_products(category, region, limit=3)
    creators: list = []
    seen: set = set()
    for p in products[:3]:
        pid = p.get("id")
        if not pid:
            continue
        try:
            for c in await get_product_creators(pid, region, limit=10):
                key = c.get("user_id") or c.get("unique_id")
                if not key or key in seen:
                    continue
                if is_shop_account(c.get("nickname"), c.get("unique_id")):
                    continue
                seen.add(key)
                creators.append(c)
        except Exception as e:
            print(f"get_category_creators product {pid} error: {e}")
    creators.sort(key=lambda c: c.get("followers") or 0, reverse=True)
    return creators[:limit]


def _clean_video_product(r: dict) -> dict:
    return {
        "product_id": r.get("product_id"),
        "video_id": r.get("video_id"),
        "region": r.get("region"),
        "cover": r.get("reflow_cover"),
        "desc": (r.get("video_desc") or "")[:200],
        "views": r.get("total_views_cnt") or 0,
        "sales": r.get("total_video_sale_cnt") or 0,
        "url": f"https://www.tiktok.com/view/product/{r.get('product_id')}" if r.get("product_id") else None,
    }


async def get_video_products(video_id: str, region: Optional[str] = None) -> list[dict]:
    """Produit(s) réellement taggé(s) dans une vidéo TikTok (Video Products Analytics).
    Params devinés (video_id + region) — à confirmer au 1er test."""
    if not video_id:
        return []
    params: dict = {"video_id": str(video_id), "page_num": 1, "page_size": 10}
    if region:
        params["region"] = region
    data = await _get("/v1/tiktok/video/products/analytics", params)
    rows = data if isinstance(data, list) else []
    return [_clean_video_product(r) for r in rows if r.get("product_id")]


def _chunks(items: list, n: int = 10) -> list[list]:
    """Découpe une liste en lots de taille ≤ n (KeyAPI plafonne video_ids à 10/appel)."""
    return [items[i:i + n] for i in range(0, len(items), n)]


def _parse_maybe_json_list(v) -> list[str]:
    """Certains champs KeyAPI (video_products, product_category_list) reviennent tantôt en
    JSON natif (list), tantôt en chaîne JSON-encodée (str), tantôt absents (None) — jamais
    supposer un seul type. Chaque élément est casté en str : les IDs produit TikTok font
    ~19 chiffres, au-delà de Number.MAX_SAFE_INTEGER côté navigateur (JSON.parse arrondirait
    silencieusement un entier brut)."""
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v if x is not None]
    if isinstance(v, str):
        try:
            parsed = json.loads(v)
        except Exception:
            return []
        if isinstance(parsed, list):
            return [str(x) for x in parsed if x is not None]
    return []


def _clean_video_detail(r: dict) -> dict:
    """Parse une entrée de /v1/tiktok/video/detail/analytics (GMV/ventes RÉELS attribués à
    cette vidéo — endpoint corrigé par KeyAPI mi-2026, confirmé non-zéro en live sur un compte
    FR réel). video_products = produits tagués dans la vidéo (nouvelle donnée, absente avant)."""
    vid = r.get("video_id")
    products = _parse_maybe_json_list(r.get("video_products"))
    return {
        "video_id": str(vid) if vid is not None else None,
        "gmv_real": r.get("total_video_sale_gmv_amt") or 0,
        "sales_real": r.get("total_video_sale_cnt") or 0,
        "video_products": products,
        "product_category_list": _parse_maybe_json_list(r.get("product_category_list")),
        "is_ad": bool(r.get("is_ad")),
        "create_time": r.get("create_time"),
        "region": r.get("region"),
    }


async def get_videos_detail(video_ids: list[str]) -> dict[str, dict]:
    """GMV/ventes RÉELS par vidéo, batché (≤10 video_ids/appel, 1 crédit/appel). Renvoie un
    dict {video_id: detail_nettoyé} pour lookup direct — les IDs absents du résultat (échec
    KeyAPI sur leur lot, ou vidéo non couverte) sont simplement absents du dict, jamais une
    valeur fictive : à l'appelant de gérer le fallback (cf. feed_radar._collect_region)."""
    ids = [str(v) for v in dict.fromkeys(video_ids) if v]  # dédup en préservant l'ordre
    if not ids:
        return {}
    sem = asyncio.Semaphore(5)

    async def _fetch_chunk(chunk: list[str]) -> list[dict]:
        async with sem:
            try:
                data = await _get("/v1/tiktok/video/detail/analytics",
                                  {"video_ids": ",".join(chunk)})
            except Exception as e:
                print(f"get_videos_detail chunk error ({len(chunk)} ids): {e}")
                return []
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
        return []

    chunk_results = await asyncio.gather(*(_fetch_chunk(c) for c in _chunks(ids, 10)))
    out: dict[str, dict] = {}
    for rows in chunk_results:
        for r in rows:
            detail = _clean_video_detail(r)
            if detail["video_id"]:
                out[detail["video_id"]] = detail
    return out


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


# ════════════════════════════════════════════════════════════════════════════
# RECHERCHE DE PROFIL (Pro / Gold / Agency) — recherche libre par @handle, sans
# passer par le ranking. Chaîne : /influencer/detail (handle → uid) →
# /influencer/trends/analytics (uid → GMV réel fenêtre glissante) →
# /influencer/products/analytics (uid → meilleures ventes lifetime).
# ════════════════════════════════════════════════════════════════════════════
def _clean_influencer_profile(u: dict) -> dict:
    uid = u.get("uid")
    unique_id = u.get("unique_id")
    return {
        "uid": str(uid) if uid else None,
        "unique_id": unique_id,
        "nickname": u.get("nickname") or unique_id or "",
        "avatar": ((u.get("avatar_larger") or {}).get("url_list") or [None])[0],
        "followers": u.get("follower_count") or 0,
        "total_favorited": u.get("total_favorited") or 0,
        "signature": (u.get("signature") or "")[:300],
        "aweme_count": u.get("aweme_count") or 0,
        "profile_url": f"https://www.tiktok.com/@{unique_id}" if unique_id else None,
    }


async def get_influencer_profile(handle: str) -> Optional[dict]:
    """Étape 1 : @handle (recherche libre) → profil + uid interne, requis pour
    les appels suivants. Renvoie None si le handle n'existe pas — l'API renvoie
    une erreur explicite ("unique_id is invalid", statut 200 + code non-zéro,
    PAS un 404 HTTP classique) pour un handle inconnu, traitée ici comme "not found"."""
    handle = (handle or "").lstrip("@").strip()
    if not handle:
        return None
    try:
        data = await _get("/v1/tiktok/influencer/detail", {"unique_id": handle})
    except Exception as e:
        print(f"get_influencer_profile({handle}) error: {e}")
        return None
    user = (data or {}).get("user") if isinstance(data, dict) else None
    if not user or not user.get("uid"):
        return None
    return _clean_influencer_profile(user)


async def get_creator_gmv_30d(uid: str, days: int = 30) -> dict:
    """Étape 2 : uid → GMV/ventes RÉELS sur une fenêtre glissante de `days` jours.
    Pagine /influencer/trends/analytics (page_size plafonné à 10 par l'API →
    ~3 pages pour 30j). Les jours absents de la réponse comptent pour 0€, jamais
    une erreur. C'est la SEULE source de vérité pour un GMV daté (les endpoints
    produits sont cumulés lifetime, start_date/end_date y sont ignorés)."""
    end = date.today()
    start = end - timedelta(days=days - 1)
    by_day: dict = {}
    page_num = 1
    while True:
        rows = await _get("/v1/tiktok/influencer/trends/analytics", {
            "user_id": uid,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "page_num": page_num,
            "page_size": 10,
        })
        rows = rows if isinstance(rows, list) else []
        if not rows:
            break
        for r in rows:
            dt = r.get("dt")
            if dt:
                by_day[dt] = r
        if len(rows) < 10 or page_num >= 6:  # garde-fou : ~60j de pagination max
            break
        page_num += 1

    gmv_total = sum((r.get("total_sale_gmv_1d_amt") or 0) for r in by_day.values())
    sales_total = sum((r.get("total_sale_1d_cnt") or 0) for r in by_day.values())

    series = []
    cur = start
    while cur <= end:
        key = cur.isoformat()
        row = by_day.get(key, {})
        series.append({
            "date": key,
            "gmv": row.get("total_sale_gmv_1d_amt") or 0,
            "sales": row.get("total_sale_1d_cnt") or 0,
        })
        cur += timedelta(days=1)

    return {"gmv_30d": gmv_total, "sales_30d": sales_total, "days": days, "series": series}


async def get_creator_prior_activity(uid: str, days_back: int = 90, skip_recent: int = 30) -> dict:
    """Quand le GMV 30j est à 0 : regarde la fenêtre J-90 → J-30 pour distinguer
    « compte suivi mais sans ventes récentes » (cas @thedopeman99, vérifié
    2026-07-03 : ventes journalières trackées jusqu'au 24/05 puis 0) de
    « compte sans aucune donnée de ventes ». L'historique KeyAPI ne remonte
    qu'à ~6-7 mois, inutile d'aller plus loin.

    Retourne {"gmv_prior": float, "sales_prior": int, "last_sale_date": str|None}."""
    end = date.today() - timedelta(days=skip_recent)
    start = date.today() - timedelta(days=days_back)
    gmv_prior, sales_prior, last_sale = 0.0, 0, None
    page_num = 1
    while True:
        rows = await _get("/v1/tiktok/influencer/trends/analytics", {
            "user_id": uid,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "page_num": page_num,
            "page_size": 10,
        })
        rows = rows if isinstance(rows, list) else []
        if not rows:
            break
        for r in rows:
            g = r.get("total_sale_gmv_1d_amt") or 0
            if g > 0:
                gmv_prior += g
                sales_prior += r.get("total_sale_1d_cnt") or 0
                dt = r.get("dt")
                if dt and (last_sale is None or dt > last_sale):
                    last_sale = dt
        if len(rows) < 10 or page_num >= 8:
            break
        page_num += 1
    return {"gmv_prior": gmv_prior, "sales_prior": sales_prior, "last_sale_date": last_sale}


async def get_creator_best_sellers(uid: str, limit: int = 10) -> list[dict]:
    """Étape 3 : uid → produits de la VITRINE du créateur, dans l'ordre natif
    renvoyé par KeyAPI (= ordre de sa vitrine TikTok, ce qu'il met en avant
    en ce moment — les récents/featured en tête).

    ⚠️ On NE re-trie PLUS par GMV : le tri GMV faisait remonter les
    best-sellers de toujours, alors qu'on veut les produits actuels du compte.
    Vérifié en live 2026-07-03 : KeyAPI n'expose AUCUNE date de publication
    produit (pas de champ date, params de tri ignorés, tags produit des vidéos
    vides) → l'ordre natif de la vitrine est le meilleur proxy disponible pour
    "produits récents". On préserve donc l'ordre tel quel.

    ⚠️ `total_sale_gmv_amt`/`total_sale_cnt` (→ champs `gmv`/`sales` de
    _clean_product) restent le GMV/ventes GLOBAUX du produit, TOUS vendeurs
    confondus — PAS la part de ce créateur. À présenter côté UI comme
    "performance du produit", jamais comme les ventes du créateur."""
    data = await _get("/v1/tiktok/influencer/products/analytics",
                      {"user_id": uid, "page_num": 1, "page_size": 10})
    rows = data if isinstance(data, list) else []
    return [_clean_product(p) for p in rows][:limit]


async def get_creator_video_attribution(unique_id: str, user_id: str,
                                        limit_videos: int = 20, limit_products: int = 8) -> dict:
    """Attribution RÉELLE de GMV/ventes par produit pour CE créateur, calculée à partir de
    ses `limit_videos` dernières vidéos (endpoint /video/detail/analytics, corrigé mi-2026 —
    cf. get_videos_detail). Complémentaire de `get_creator_best_sellers` (vitrine, ordre natif,
    chiffres GLOBAUX tous vendeurs) : ici, chiffres RÉELS mais bornés à une fenêtre de vidéos
    récentes, jamais un total lifetime.

    ⚠️ Une vidéo qui tague plusieurs produits attribue la TOTALITÉ de son GMV à CHACUN
    (KeyAPI ne fournit pas de répartition par produit dans une même vidéo) — les totaux
    sommés sur plusieurs produits peuvent donc dépasser le vrai total combiné. À rappeler
    explicitement côté UI, jamais présenté comme une répartition exacte."""
    empty = {"products": [], "videos_analyzed": 0, "video_count": 0, "window_label": None}
    if not unique_id:
        return empty
    try:
        vdata = await _get("/v1/tiktok/influencer/videos",
                           {"unique_id": unique_id, "page_num": 1, "page_size": limit_videos})
        aweme = (vdata or {}).get("aweme_list") if isinstance(vdata, dict) else None
        videos = [_clean_video(v) for v in (aweme or [])]
    except Exception as e:
        print(f"get_creator_video_attribution({unique_id}) videos error: {e}")
        return empty

    video_ids = [str(v["id"]) for v in videos if v.get("id")]
    if not video_ids:
        return empty

    try:
        detail_map = await get_videos_detail(video_ids)
    except Exception as e:
        print(f"get_creator_video_attribution({unique_id}) detail error: {e}")
        return {**empty, "video_count": len(videos)}

    # Lookup video_id → métadonnées (url/cover) pour rattacher une vidéo à chaque produit.
    vid_meta = {str(v["id"]): v for v in videos if v.get("id")}

    by_product: dict[str, dict] = {}
    create_times: list = []
    region_hint = "US"
    for vid_key, detail in detail_map.items():
        if detail.get("create_time"):
            create_times.append(detail["create_time"])
        if detail.get("region"):
            region_hint = detail["region"]
        d_gmv = detail.get("gmv_real") or 0
        meta = vid_meta.get(str(detail.get("video_id") or vid_key)) or {}
        for pid in detail.get("video_products") or []:
            entry = by_product.setdefault(pid, {"product_id": pid, "gmv_real": 0,
                                                 "sales_real": 0, "video_count": 0,
                                                 "_top_video_gmv": -1, "video_id": None,
                                                 "video_url": None, "video_cover": None})
            entry["gmv_real"] += d_gmv
            entry["sales_real"] += detail.get("sales_real") or 0
            entry["video_count"] += 1
            # Vidéo représentative = celle qui a généré le plus de GMV pour CE produit
            # (c'est elle qu'on affiche à côté du produit côté Recherche).
            if d_gmv >= entry["_top_video_gmv"]:
                entry["_top_video_gmv"] = d_gmv
                entry["video_id"] = str(detail.get("video_id") or vid_key)
                entry["video_url"] = meta.get("url")
                entry["video_cover"] = meta.get("cover")

    top = sorted(by_product.values(), key=lambda p: p["gmv_real"], reverse=True)[:limit_products]

    enriched: list[dict] = []
    for entry in top:
        try:
            detail_prod = await get_product_detail(entry["product_id"], region_hint)
        except Exception as e:
            print(f"get_creator_video_attribution product_detail({entry['product_id']}) error: {e}")
            detail_prod = None
        base = detail_prod or {"id": entry["product_id"], "name": "", "image": None, "url":
                               f"https://www.tiktok.com/view/product/{entry['product_id']}"}
        enriched.append({**base, "gmv_real": entry["gmv_real"], "sales_real": entry["sales_real"],
                         "video_count": entry["video_count"], "video_id": entry.get("video_id"),
                         "video_url": entry.get("video_url"), "video_cover": entry.get("video_cover")})

    window_label = None
    if create_times:
        try:
            lo, hi = min(create_times), max(create_times)
            lo_d = datetime.fromtimestamp(int(lo)).strftime("%d/%m/%Y")
            hi_d = datetime.fromtimestamp(int(hi)).strftime("%d/%m/%Y")
            window_label = f"{len(detail_map)} dernières vidéos, {lo_d} → {hi_d}"
        except Exception:
            window_label = f"{len(detail_map)} dernières vidéos"

    return {"products": enriched, "videos_analyzed": len(detail_map),
           "video_count": len(videos), "window_label": window_label}


async def _enrich_zero_gmv(uid: str, gmv_data: dict, products: list) -> dict:
    """Qualifie un gmv_30d=0 (vérifié en live 2026-07-03, cf.
    get_creator_prior_activity) en sondant la fenêtre J-90 → J-30 :
    - ventes trouvées → le compte EST suivi, le 0 sur 30j est une vraie donnée.
      On renvoie `last_sale_date` + `gmv_prior_90d` pour l'afficher.
    - rien trouvé mais des produits en vitrine → données indisponibles
      (`reliable: false`), sans AUCUN montant de repli : le "GMV lifetime" des
      produits (`total_sale_gmv_amt`) est le GMV GLOBAL du produit tous
      vendeurs confondus, pas la part du créateur (598k$ trompeurs sur
      @thedopeman99, 3,55M$ sur @hannaholala pour ~211k$/30j réels ; le champ
      d'attribution `total_video_sale_gmv_amt` était à 0 partout — CONFIRMÉ CORRIGÉ
      mi-2026 côté /video/detail/analytics, cf. get_creator_video_attribution, mais
      cette fonction-ci ne consomme PAS ce champ : elle reste inchangée).
    - rien nulle part et pas de produits → 0 affiché tel quel."""
    if (gmv_data.get("gmv_30d") or 0) > 0:
        gmv_data["reliable"] = True
        return gmv_data
    try:
        prior = await get_creator_prior_activity(uid)
    except Exception as e:
        print(f"_enrich_zero_gmv prior activity error: {e}")
        prior = {"gmv_prior": 0, "sales_prior": 0, "last_sale_date": None}
    if prior.get("last_sale_date"):
        gmv_data["reliable"] = True
        gmv_data["last_sale_date"] = prior["last_sale_date"]
        gmv_data["gmv_prior_90d"] = prior["gmv_prior"]
        gmv_data["sales_prior_90d"] = prior["sales_prior"]
    else:
        gmv_data["reliable"] = not bool(products)
    return gmv_data


async def search_creator_profile(handle: str) -> Optional[dict]:
    """Orchestration complète de la Recherche de profil : profil + GMV 30j réel +
    meilleures ventes (vitrine) + attribution vidéo réelle par produit.
    ~7-13 appels KeyAPI (la plupart des enrichissements produit sont amortis par
    le cache 7j de get_product_detail). None si le handle n'existe pas."""
    profile = await get_influencer_profile(handle)
    if not profile or not profile.get("uid"):
        return None
    uid = profile["uid"]
    unique_id = profile.get("unique_id") or handle

    async def _safe_gmv():
        try:
            return await get_creator_gmv_30d(uid, days=30)
        except Exception as e:
            print(f"search_creator_profile gmv error: {e}")
            return {"gmv_30d": 0, "sales_30d": 0, "days": 30, "series": []}

    async def _safe_products():
        try:
            return await get_creator_best_sellers(uid, limit=10)
        except Exception as e:
            print(f"search_creator_profile products error: {e}")
            return []

    async def _safe_attribution():
        try:
            return await get_creator_video_attribution(unique_id, uid)
        except Exception as e:
            print(f"search_creator_profile attribution error: {e}")
            return {"products": [], "videos_analyzed": 0, "video_count": 0, "window_label": None}

    gmv_data, products, attribution = await asyncio.gather(
        _safe_gmv(), _safe_products(), _safe_attribution())
    gmv_data = await _enrich_zero_gmv(uid, gmv_data, products)
    return {"profile": profile, "gmv": gmv_data, "best_sellers": products,
           "video_attribution": attribution}


async def get_creator_gmv_only(handle: str) -> Optional[dict]:
    """Outil ADMIN minimal : @handle → profil léger + GMV 30j (+ appels
    supplémentaires UNIQUEMENT pour qualifier un 0€, cf. _enrich_zero_gmv).
    Pas de cache/quota — appelant (admin_routes.py) gère ça."""
    profile = await get_influencer_profile(handle)
    if not profile or not profile.get("uid"):
        return None
    uid = profile["uid"]
    gmv_data = await get_creator_gmv_30d(uid, days=30)
    if (gmv_data.get("gmv_30d") or 0) == 0:
        try:
            products = await get_creator_best_sellers(uid, limit=10)
        except Exception:
            products = []
        gmv_data = await _enrich_zero_gmv(uid, gmv_data, products)
    else:
        gmv_data["reliable"] = True
    return {
        "unique_id": profile.get("unique_id"),
        "nickname": profile.get("nickname"),
        "gmv_30d": gmv_data.get("gmv_30d"),
        "sales_30d": gmv_data.get("sales_30d"),
        "reliable": gmv_data.get("reliable", True),
        "last_sale_date": gmv_data.get("last_sale_date"),
        "gmv_prior_90d": gmv_data.get("gmv_prior_90d"),
    }
