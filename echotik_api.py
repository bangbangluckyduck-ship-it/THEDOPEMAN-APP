"""
EchoTik API Integration - Récupère vidéos virales avec filtres
"""
import os
import httpx
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

ECHOTIK_API_URL = "https://api.echotik.com/v1"
ECHOTIK_USERNAME = os.getenv("ECHOTIK_USERNAME", "")
ECHOTIK_PASSWORD = os.getenv("ECHOTIK_PASSWORD", "")

# Seuils de ventes minimum par catégorie (flexible)
SALES_THRESHOLDS = {
    "beaute": 500,
    "sante": 400,
    "fashion": 300,
    "electromenager": 250,
    "tech": 200,
    "fitness": 300,
    "complement_sante": 400,
}


class EchoTikAPI:
    """Client pour l'API EchoTik avec gestion d'authentification"""

    def __init__(self):
        self.username = ECHOTIK_USERNAME
        self.password = ECHOTIK_PASSWORD
        self.token = None
        self.token_expires = None

    async def authenticate(self) -> bool:
        """Authentifie avec EchoTik API"""
        if not self.username or not self.password:
            print("❌ EchoTik credentials non configurés")
            return False

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{ECHOTIK_API_URL}/auth/login",
                    json={"username": self.username, "password": self.password}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    self.token = data.get("access_token")
                    self.token_expires = datetime.now() + timedelta(hours=1)
                    return True
                print(f"❌ EchoTik auth failed: {resp.status_code}")
                return False
        except Exception as e:
            print(f"❌ EchoTik auth error: {e}")
            return False

    async def get_viral_videos(
        self,
        category: str,
        min_views: int = 100000
    ) -> List[Dict[str, Any]]:
        """
        Récupère vidéos virales pour une catégorie
        Filtre: views >= min_views + sales >= threshold
        """
        if not self.token or datetime.now() > self.token_expires:
            if not await self.authenticate():
                return []

        sales_threshold = SALES_THRESHOLDS.get(category.lower(), 300)

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{ECHOTIK_API_URL}/videos/search",
                    headers={"Authorization": f"Bearer {self.token}"},
                    params={
                        "category": category,
                        "sort_by": "views",
                        "min_views": min_views,
                        "limit": 100,  # Récupérer 100 pour en filtrer 10
                    }
                )

                if resp.status_code != 200:
                    print(f"❌ EchoTik videos error: {resp.status_code}")
                    return []

                videos = resp.json().get("videos", [])

                # Filtrer par ventes et formater
                filtered = []
                for v in videos:
                    if (v.get("views", 0) >= min_views and
                        v.get("sales", 0) >= sales_threshold):
                        filtered.append({
                            "id": v.get("id"),
                            "thumbnail": v.get("thumbnail_url"),
                            "creator_handle": v.get("creator_handle"),
                            "creator_link": f"https://www.tiktok.com/@{v.get('creator_handle')}",
                            "views": v.get("views", 0),
                            "sales": v.get("sales", 0),
                            "description": v.get("description", ""),
                            "hashtags": v.get("hashtags", []),
                            "url": v.get("video_url"),
                        })

                # Retourner top 10
                return filtered[:10]

        except Exception as e:
            print(f"❌ EchoTik videos error: {e}")
            return []


# Instance globale
echotik_client = EchoTikAPI()
