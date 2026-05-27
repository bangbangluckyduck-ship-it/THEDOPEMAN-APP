"""
KeyAPI Integration - Récupère vidéos virales TikTok avec analytics
Remplace EchoTik par une vrai API TikTok
"""
import os
import httpx
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

KEYAPI_URL = "https://mcp.keyapi.ai/tiktok/mcp"
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
    """Client pour l'API KeyAPI TikTok avec MCP"""

    def __init__(self):
        self.token = KEYAPI_TOKEN
        self.base_url = KEYAPI_URL

    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        Liste tous les outils disponibles
        """
        if not self.token:
            print("❌ KeyAPI token not configured")
            return []

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "outils/liste",
            "params": {}
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(
                    self.base_url,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    }
                )
                result = resp.json()
                print(f"[KeyAPI] Available tools: {json.dumps(result, indent=2)}")
                return result.get("result", {}).get("tools", [])
        except Exception as e:
            print(f"❌ KeyAPI list_tools error: {e}")
            return []

    async def call_tool(
        self,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Appelle un outil KeyAPI via JSON-RPC 2.0
        """
        if not self.token:
            print("❌ KeyAPI token not configured")
            return {"error": "Token missing"}

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "outils/appel",
            "params": {
                "nom": tool_name,
                "arguments": params
            }
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(
                    self.base_url,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    }
                )

                print(f"[KeyAPI] {tool_name} response: {resp.status_code}")

                if resp.status_code != 200:
                    print(f"❌ KeyAPI error: {resp.status_code} - {resp.text[:200]}")
                    return {"error": f"Status {resp.status_code}"}

                result = resp.json()
                if "error" in result:
                    print(f"❌ KeyAPI RPC error: {result['error']}")
                    return result

                return result.get("result", {})

        except Exception as e:
            print(f"❌ KeyAPI call error: {e}")
            return {"error": str(e)}

    async def get_viral_videos(
        self,
        category: str,
        region: str = "US",
        min_views: int = 100000
    ) -> List[Dict[str, Any]]:
        """
        Récupère vidéos virales par catégorie using influencer_list_analytics
        Filtre: vues >= 100K, sorted by views descending
        """
        print(f"[KeyAPI] Fetching viral videos for category: {category}")

        try:
            # Appeler influencer_list_analytics pour les vidéos de produits
            result = await self.call_tool(
                "influencer_list_analytics",
                {
                    "region": region,
                    "category": category,
                    "page_num": 1,
                    "page_size": 10,  # Top 10
                    "sort_by": "views",
                    "sort_type": "desc"  # Descending (highest views first)
                }
            )

            if "error" in result:
                print(f"❌ KeyAPI returned error: {result}")
                return []

            print(f"[KeyAPI] Raw result: {result}")
            print(f"[KeyAPI] Result keys: {list(result.keys())}")

            # Try different key names
            videos_raw = result.get("data", [])
            if not videos_raw:
                videos_raw = result.get("videos", [])
            if not videos_raw:
                videos_raw = result.get("list", [])

            print(f"[KeyAPI] Got {len(videos_raw)} videos from API")
            if videos_raw:
                print(f"[KeyAPI] First video sample: {json.dumps(videos_raw[0], indent=2)}")

            # Transformer en format standard (influencers/creators)
            formatted_videos = []
            for creator in videos_raw:
                # Use median video views as proxy for viral potential
                views = creator.get("video_med_view_cnt", 0) or creator.get("ec_video_med_view_cnt", 0)
                sales_gmv = creator.get("vidéo_gmv", 0) or creator.get("live_gmv", 0)

                if views >= min_views:
                    formatted_videos.append({
                        "id": creator.get("créateur_oecuid", ""),
                        "title": f"@{creator.get('poignée', '')} - {creator.get('surnom', '')}",
                        "views": int(views),
                        "likes": creator.get("engagement vidéo", 0) or 0,
                        "comments": creator.get("numéro_produit_promo", 0) or 0,
                        "shares": 0,
                        "creator_handle": creator.get("poignée", ""),
                        "creator_link": f"https://www.tiktok.com/@{creator.get('poignée', '')}",
                        "url": f"https://www.tiktok.com/@{creator.get('poignée', '')}",
                        "engagement_ec": creator.get("engagement en direct ec", 0) or 0,
                        "video_sale_gmv": int(sales_gmv),
                        "category": category,
                        "follower_cnt": creator.get("suiveur_cnt", 0) or 0
                    })

            print(f"[KeyAPI] Formatted {len(formatted_videos)} creators")
            return formatted_videos[:10]  # Return top 10

        except Exception as e:
            print(f"❌ KeyAPI get_viral_videos error: {e}")
            import traceback
            traceback.print_exc()
            return []


# Instance globale
keyapi_client = KeyAPIClient()
