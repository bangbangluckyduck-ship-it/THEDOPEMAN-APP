"""
Quota journalier de la Recherche de profil TikTok — INDÉPENDANT de check_quota()/
TIER_CONFIG (auth.py) qui sont câblés sur l'analyse vidéo. Une recherche coûte
~5 appels KeyAPI (voir market_creators.search_creator_profile) ; ce module limite
uniquement le volume de recherches PRO, pas l'analyse vidéo.

Gating :
- free            : bloqué (403), vérifié ici pour un message clair
- pro             : PRO_DAILY_LIMIT / jour (429 une fois atteint)
- gold/agency/beta/admin : illimité
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException

from supabase_client import supabase_service as supabase, _get_user_id

PRO_DAILY_LIMIT = 10

_UNLIMITED_TIERS = ("gold", "agency", "beta", "admin")


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def get_recherche_count_today(email: str) -> int:
    """Nombre de recherches déjà effectuées aujourd'hui par cet utilisateur."""
    if not supabase:
        return 0
    try:
        uid = _get_user_id(email)
        r = supabase.table("recherche_search_usage").select("count") \
            .eq("user_id", uid).eq("day", _today()).execute()
        return r.data[0]["count"] if r.data else 0
    except Exception as e:
        print(f"get_recherche_count_today error: {e}")
        return 0


def increment_recherche_count(email: str) -> int:
    """Incrémente le compteur du jour (appelé uniquement sur un vrai cache-miss
    KeyAPI, jamais sur un résultat déjà en cache — cf. main.py)."""
    if not supabase:
        return 1
    try:
        uid = _get_user_id(email)
        day = _today()
        existing = supabase.table("recherche_search_usage").select("*") \
            .eq("user_id", uid).eq("day", day).execute()
        if existing.data:
            new_count = existing.data[0]["count"] + 1
            supabase.table("recherche_search_usage").update({"count": new_count}) \
                .eq("user_id", uid).eq("day", day).execute()
            return new_count
        supabase.table("recherche_search_usage").insert(
            {"user_id": uid, "day": day, "count": 1}).execute()
        return 1
    except Exception as e:
        print(f"increment_recherche_count error: {e}")
        return 1


def check_recherche_quota(user: dict) -> None:
    """Lève HTTPException(403) si free, HTTPException(429) si PRO a épuisé son
    quota du jour. No-op (accès illimité) pour gold/agency/beta/admin."""
    tier = (user.get("tier") or "free").lower()
    if user.get("is_admin") or tier in _UNLIMITED_TIERS:
        return
    if tier != "pro":
        raise HTTPException(
            status_code=403,
            detail="La recherche de profil est réservée aux plans Pro et plus. Passe au plan Pro sur qeerah.com",
        )
    count = get_recherche_count_today(user["email"])
    if count >= PRO_DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Limite de {PRO_DAILY_LIMIT} recherches/jour atteinte (plan Pro). "
                   "Passe au plan Gold pour un accès illimité.",
        )
