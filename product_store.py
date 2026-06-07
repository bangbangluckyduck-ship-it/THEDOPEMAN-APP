"""
🧠 Mémoire produits — accumulation anonymisée des produits analysés pour améliorer
la reco au fil du temps. Table Supabase `analyzed_products`.

Aucune donnée personnelle : on ne stocke que produit / catégorie / région / ventes
et un compteur de récurrence (times_seen). Best-effort : ne casse jamais l'analyse.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")[:60]


def _key(product_id: Optional[str], name: Optional[str], category: Optional[str]) -> Optional[str]:
    if product_id:
        return f"id:{product_id}"
    sl = _slug(name or "")
    return f"name:{(category or 'na')}:{sl}" if sl else None


def record_product(supabase, *, product_id: Optional[str] = None, name: Optional[str] = None,
                   category: Optional[str] = None, region: Optional[str] = None,
                   price=None, sales=None) -> None:
    """Upsert un produit analysé (incrémente times_seen s'il existe déjà)."""
    if not supabase:
        return
    key = _key(product_id, name, category)
    if not key:
        return
    try:
        prev = supabase.table("analyzed_products").select("times_seen,product_id").eq("product_key", key).execute()
        seen = 1
        if prev.data:
            seen = (prev.data[0].get("times_seen") or 0) + 1
            product_id = product_id or prev.data[0].get("product_id")  # garde l'id si déjà connu
        row = {
            "product_key": key,
            "product_id": product_id,
            "product_name": (name or "")[:200] or None,
            "categorie": category,
            "region": region,
            "times_seen": seen,
            "last_seen": datetime.now(timezone.utc).isoformat(),
        }
        try:
            if price not in (None, ""):
                row["price"] = float(str(price).replace(",", ".").replace("€", "").replace("$", "").strip())
        except Exception:
            pass
        if sales not in (None, ""):
            try:
                row["last_sales"] = int(sales)
            except Exception:
                pass
        supabase.table("analyzed_products").upsert(row, on_conflict="product_key").execute()
    except Exception as e:
        print(f"record_product error: {e}")


def get_popular(supabase, category: Optional[str] = None, region: Optional[str] = None,
                limit: int = 8) -> list:
    """Produits les plus récurrents dans notre base (reco « populaire chez nous »)."""
    if not supabase:
        return []
    try:
        q = supabase.table("analyzed_products").select(
            "product_id,product_name,categorie,region,price,last_sales,times_seen")
        if category:
            q = q.eq("categorie", category)
        if region:
            q = q.eq("region", region)
        q = q.order("times_seen", desc=True).limit(limit)
        return q.execute().data or []
    except Exception as e:
        print(f"get_popular error: {e}")
        return []
