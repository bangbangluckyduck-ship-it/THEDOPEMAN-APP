"""
KeyAPI Integration - TikTok Shop product analytics (REST API)
- Filtre par catégorie réelle (category_id mapping TikTok Shop officiel)
- Extrait cover image, prix, ventes, vues, GMV
"""
import os
import httpx
import json
from typing import Any, Dict, List, Optional

KEYAPI_URL_BASE = "https://api.keyapi.ai/v1"
KEYAPI_TOKEN = os.getenv("KEYAPI_TOKEN", "")

# Mapping app category → TikTok Shop primary category_id (réels, vérifiés via API)
CATEGORY_ID_MAP: Dict[str, str] = {
    "beaute":           "601450",  # Beauty & Personal Care
    "fashion":          "601152",  # Womenswear & Underwear
    "tech":             "601739",  # Phones & Electronics
    "fitness":          "603014",  # Sports & Outdoor
    "sante":            "700645",  # Health
    "complement_sante": "700645",  # Health (compléments dans Health)
    "electromenager":   "600942",  # Household Appliances
}

# Inverse: ID → nom convivial pour affichage
CATEGORY_ID_TO_NAME: Dict[str, str] = {
    "601450": "Beauty & Personal Care",
    "601152": "Womenswear & Underwear",
    "601739": "Phones & Electronics",
    "603014": "Sports & Outdoor",
    "700645": "Health",
    "600942": "Household Appliances",
}


def _first_cover_url(cover_field: Any) -> Optional[str]:
    """Extract first image URL from cover_url JSON field (string or list)."""
    if not cover_field:
        return None
    try:
        if isinstance(cover_field, str):
            data = json.loads(cover_field)
        else:
            data = cover_field
        if isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict):
                return first.get("url")
            if isinstance(first, str):
                return first
    except Exception:
        pass
    return None


class KeyAPIClient:
    """Client REST KeyAPI TikTok Shop."""

    def __init__(self) -> None:
        self.token = KEYAPI_TOKEN
        self.base_url = KEYAPI_URL_BASE

    async def _get(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if not self.token:
            print("❌ KeyAPI token not configured")
            return {"error": "Token missing"}

        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.get(
                    url,
                    params=params,
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json",
                    },
                )
            print(f"[KeyAPI] {endpoint} → {resp.status_code}")

            # ── 🚨 DEBUG : audit de la qualité des données KeyAPI ──────────────
            # Imprime la réponse BRUTE exacte reçue (corps complet), y compris en
            # cas d'erreur HTTP (401/403/429…) ou de JSON vide. Logging uniquement,
            # n'altère en rien le comportement de l'application.
            print("🚨 DEBUG KEYAPI RAW DATA 🚨")
            print(f"   endpoint : {endpoint}")
            print(f"   params   : {params}")
            print(f"   status   : {resp.status_code}")
            _raw_body = resp.text
            if not _raw_body or not _raw_body.strip():
                print("   ⚠️ CORPS VIDE — la réponse KeyAPI ne contient aucune donnée.")
            else:
                print(f"   body     : {_raw_body}")
            print("🚨 FIN DEBUG KEYAPI RAW DATA 🚨")
            # ───────────────────────────────────────────────────────────────────

            if resp.status_code != 200:
                # Erreur complète (status + corps entier, non tronqué)
                print(f"❌ KeyAPI HTTP error {resp.status_code} (erreur complète): {resp.text}")
                return {"error": f"Status {resp.status_code}"}
            result = resp.json()
            if result.get("code") != 0:
                print(f"❌ KeyAPI API error (réponse complète): {result}")
                return {"error": result.get("message", "Unknown error")}
            return result
        except Exception as e:
            print(f"❌ KeyAPI request exception: {e}")
            return {"error": str(e)}

    def _format_product(self, raw: Dict[str, Any], app_category: str) -> Dict[str, Any]:
        views = int(raw.get("total_views_cnt") or 0)
        gmv = float(raw.get("total_sale_gmv_amt") or 0)
        sales = int(raw.get("total_sale_cnt") or 0)
        product_id = raw.get("product_id") or ""
        title = raw.get("product_name") or ""
        # Truncate très longs noms TikTok
        short_title = title.split("|")[0].strip()[:120] if title else "Produit"
        return {
            "id": product_id,
            "title": short_title,
            "title_full": title,
            "image": _first_cover_url(raw.get("cover_url")),
            "url": f"https://www.tiktok.com/search?q={product_id}",
            "tiktok_search_url": f"https://www.tiktok.com/search?q={short_title.split()[0] if short_title else ''}",
            "views": views,
            "sales": sales,
            "gmv": gmv,
            "video_count": int(raw.get("total_video_cnt") or 0),
            "creators_count": int(raw.get("total_ifl_cnt") or 0),
            "price": float(raw.get("spu_avg_price") or 0),
            "category_id": raw.get("category_id"),
            "category": app_category,
            "rating": float(raw.get("product_rating") or 0) if raw.get("product_rating") else None,
        }

    async def get_viral_videos(
        self,
        category: str,
        region: str = "US",
        min_views: int = 100000,
        page_size: int = 10,
        sort_field: int = 4,  # 4 = total_sale_7d_cnt (récents tendance)
    ) -> List[Dict[str, Any]]:
        """Retourne produits viraux pour une catégorie app (mappée vers TikTok category_id)."""
        category_lower = (category or "").lower().strip()
        category_id = CATEGORY_ID_MAP.get(category_lower)

        params: Dict[str, Any] = {
            "region": region,
            "page_num": 1,
            "page_size": min(page_size, 10),
            "product_sort_field": sort_field,
            "sort_type": 1,  # desc
            "min_total_views_cnt": min_views,
            "sales_flag": 1,  # vidéo e-commerce
        }
        if category_id:
            params["category_id"] = category_id

        print(f"[KeyAPI] get_viral_videos cat={category_lower} → category_id={category_id}")

        result = await self._get("/tiktok/product/list/analytics", params)
        if "error" in result:
            return []

        data = result.get("data", [])
        if not isinstance(data, list):
            return []

        products = [self._format_product(p, category_lower) for p in data]
        # Filtre final par vues
        products = [p for p in products if p["views"] >= min_views]
        print(f"[KeyAPI] returned {len(products)} products for {category_lower}")
        return products

    async def get_trending_up(
        self,
        category: str,
        region: str = "US",
        page_size: int = 5,
    ) -> List[Dict[str, Any]]:
        """Produits en tendance haussière (sales_trend_flag=1)."""
        category_lower = (category or "").lower().strip()
        category_id = CATEGORY_ID_MAP.get(category_lower)
        params: Dict[str, Any] = {
            "region": region,
            "page_num": 1,
            "page_size": min(page_size, 10),
            "product_sort_field": 5,  # total_sale_30d_cnt
            "sort_type": 1,
            "sales_trend_flag": 1,  # up
            "sales_flag": 1,
        }
        if category_id:
            params["category_id"] = category_id

        result = await self._get("/tiktok/product/list/analytics", params)
        if "error" in result:
            return []
        data = result.get("data", []) or []
        return [self._format_product(p, category_lower) for p in data]


# Instance globale
keyapi_client = KeyAPIClient()
