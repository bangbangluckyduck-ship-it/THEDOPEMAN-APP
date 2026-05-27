"""
KeyAPI Integration - Récupère vidéos virales TikTok avec analytics
Uses proper REST API at api.keyapi.ai/v1/
"""
import os
import httpx
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

KEYAPI_URL_BASE = "https://api.keyapi.ai/v1"
KEYAPI_TOKEN = os.getenv("KEYAPI_TOKEN", "")

# Seuils de vues minimum par catégorie
MIN_VIEWS_THRESHOLDS = {
    "beaute": 100000,
    "sante": 100000,
    "fashion": 100000,
    "electromenager": 100000,
    "tech": 100000,
    "fitness": 100000,
    "complement_sante": 100000,
}


class KeyAPIClient:
    """Client pour l'API KeyAPI TikTok REST"""

    def __init__(self):
        self.token = KEYAPI_TOKEN
        self.base_url = KEYAPI_URL_BASE

    async def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Fait une requête GET à KeyAPI
        """
        if not self.token:
            print("❌ KeyAPI token not configured")
            return {"error": "Token missing"}

        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(
                    url,
                    params=params,
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    }
                )

                print(f"[KeyAPI] {endpoint} response: {resp.status_code}")

                if resp.status_code != 200:
                    print(f"❌ KeyAPI error: {resp.status_code} - {resp.text[:200]}")
                    return {"error": f"Status {resp.status_code}"}

                result = resp.json()
                if result.get("code") != 0:
                    print(f"❌ KeyAPI API error: {result.get('message')}")
                    return {"error": result.get("message")}

                return result.get("data", {})

        except Exception as e:
            print(f"❌ KeyAPI request error: {e}")
            return {"error": str(e)}

    async def get_viral_videos(
        self,
        category: str,
        region: str = "US",
        min_views: int = 100000
    ) -> List[Dict[str, Any]]:
        """
        Récupère produits viraux par catégorie via /v1/tiktok/product/list/analytics
        Filtre: vues >= 100K, triés par vues décroissantes
        """
        print(f"[KeyAPI] Fetching viral products for category: {category}")

        try:
            # Appeler /product/list/analytics avec filtres
            # Note: category_id doit être numérique, pas un string comme "fashion"
            # Pour l'instant, on ne filtre pas par catégorie
            params = {
                "region": region,
                "page_num": 1,
                "page_size": 10,
                "product_sort_field": 1,  # Sort by total_sale_cnt (most sold)
                "sort_type": 1,  # Descending
                "min_total_views_cnt": min_views,
                "sales_flag": 1  # Video e-commerce only
            }

            print(f"[KeyAPI] Request params: {params}")

            result = await self._make_request(
                "/tiktok/product/list/analytics",
                params
            )

            if "error" in result:
                print(f"❌ KeyAPI error: {result}")
                return []

            # Result should be a list of products
            products_raw = result if isinstance(result, list) else result.get("products", [])

            print(f"[KeyAPI] Got {len(products_raw)} products from API")
            if products_raw:
                print(f"[KeyAPI] First product sample: {json.dumps(products_raw[0], indent=2)[:500]}")

            # Transform to video format
            formatted_videos = []
            for product in products_raw:
                views = product.get("total_views_cnt", 0) or 0
                gmv = product.get("total_sale_gmv_amt", 0) or 0
                sales = product.get("total_sale_cnt", 0) or 0

                if views >= min_views:
                    formatted_videos.append({
                        "id": product.get("product_id", ""),
                        "title": product.get("product_name", ""),
                        "views": int(views),
                        "likes": product.get("total_ifl_cnt", 0) or 0,
                        "comments": product.get("total_video_cnt", 0) or 0,
                        "shares": 0,
                        "creator_handle": product.get("seller_name", ""),
                        "creator_link": f"https://www.tiktok.com/discover/{product.get('product_id', '')}",
                        "url": f"https://www.tiktok.com/discover/{product.get('product_id', '')}",
                        "video_sale_cnt": int(sales),
                        "video_sale_gmv": float(gmv),
                        "category": category,
                        "price": product.get("spu_avg_price", 0)
                    })

            print(f"[KeyAPI] Formatted {len(formatted_videos)} products")
            return formatted_videos[:10]

        except Exception as e:
            print(f"❌ KeyAPI get_viral_videos error: {e}")
            import traceback
            traceback.print_exc()
            return []


# Instance globale
keyapi_client = KeyAPIClient()
