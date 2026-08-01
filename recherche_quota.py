"""
Quota journalier de la Recherche de profil TikTok — INDÉPENDANT du quota
d'analyses (analysis_quota.py). Une recherche coûte ~5 appels KeyAPI (voir
market_creators.search_creator_profile) : ce plafond protège le quota du
fournisseur de données, il ne mesure pas la valeur rendue au client.

Gating depuis la refonte tarifaire :
- abonné Qeerah Pro et essai en cours : PRO_DAILY_LIMIT / jour (429 au-delà)
- essai expiré sans abonnement        : bloqué (402)
- admin                                : illimité

Le plafond journalier est conservé pour les deux premiers cas : c'est la seule
ressource du produit dont le coût est plafonné en amont par un tiers, et
l'ouvrir en illimité épuiserait le quota fournisseur pour tout le monde.
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException

from supabase_client import supabase_service as supabase, _get_user_id

PRO_DAILY_LIMIT = 10


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
    """Lève HTTPException(402) si l'essai est terminé sans abonnement,
    HTTPException(429) si le plafond journalier est atteint. No-op pour admin."""
    if user.get("is_admin") or (user.get("tier") or "").lower() == "admin":
        return

    from auth import has_full_access
    if not has_full_access(user):
        raise HTTPException(
            status_code=402,
            detail="Ton essai gratuit est terminé. Abonne-toi à Qeerah Pro sur "
                   "qeerah.com pour continuer à rechercher des profils.",
        )

    count = get_recherche_count_today(user["email"])
    if count >= PRO_DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Limite de {PRO_DAILY_LIMIT} recherches de profil par jour atteinte. "
                   "Le compteur repart demain.",
        )
