"""
Client Supabase pour gérer les utilisateurs, tiers, et usage.
"""
import os
from datetime import datetime, timezone
from typing import Optional
from supabase import create_client, Client

# Initialiser le client Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "")

supabase: Optional[Client] = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ── UTILISATEURS ──────────────────────────────────────────

def get_or_create_user(email: str) -> dict:
    """Récupère ou crée un utilisateur."""
    if not supabase:
        return {"email": email, "tier": "free"}

    try:
        # Récupérer l'utilisateur
        response = supabase.table("users").select("*").eq("email", email).execute()

        if response.data:
            return response.data[0]

        # Créer un nouvel utilisateur
        new_user = {
            "email": email,
            "tier": "free",
        }
        response = supabase.table("users").insert(new_user).execute()
        return response.data[0] if response.data else new_user

    except Exception as e:
        print(f"Erreur get_or_create_user: {e}")
        return {"email": email, "tier": "free"}


def set_user_tier(email: str, tier: str, customer_id: Optional[str] = None,
                  subscription_id: Optional[str] = None, expiry: Optional[str] = None) -> None:
    """Met à jour le tier d'un utilisateur."""
    if not supabase:
        return

    try:
        data = {
            "tier": tier,
            "customer_id": customer_id,
            "subscription_id": subscription_id,
            "tier_expiry": expiry,
        }
        supabase.table("users").update(data).eq("email", email).execute()
    except Exception as e:
        print(f"Erreur set_user_tier: {e}")


def get_user_tier(email: str) -> str:
    """Récupère le tier d'un utilisateur."""
    if not supabase:
        return "free"

    try:
        user = get_or_create_user(email)

        # Vérifier l'expiration du tier
        if user.get("tier_expiry"):
            try:
                expiry_date = datetime.fromisoformat(user["tier_expiry"]).date()
                today = datetime.now(timezone.utc).date()
                if today > expiry_date:
                    set_user_tier(email, "free")
                    return "free"
            except (ValueError, TypeError):
                pass

        return user.get("tier", "free")
    except Exception as e:
        print(f"Erreur get_user_tier: {e}")
        return "free"


def get_customer_id(email: str) -> Optional[str]:
    """Récupère le customer ID Stripe."""
    if not supabase:
        return None

    try:
        user = get_or_create_user(email)
        return user.get("customer_id")
    except Exception as e:
        print(f"Erreur get_customer_id: {e}")
        return None


def revoke_by_customer(customer_id: str) -> None:
    """Downgrade vers free quand l'abonnement est annulé."""
    if not supabase:
        return

    try:
        supabase.table("users").update({"tier": "free"}).eq("customer_id", customer_id).execute()
    except Exception as e:
        print(f"Erreur revoke_by_customer: {e}")


# ── USAGE ─────────────────────────────────────────────────

def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _this_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def _get_monthly_count(email: str) -> int:
    """Récupère le compteur mensuel."""
    if not supabase:
        return 0

    try:
        response = supabase.table("monthly_usage").select("count").eq("user_id", _get_user_id(email)).eq("month", _this_month()).execute()
        return response.data[0]["count"] if response.data else 0
    except Exception:
        return 0


def _get_daily_count(email: str) -> int:
    """Récupère le compteur journalier."""
    if not supabase:
        return 0

    try:
        response = supabase.table("daily_usage").select("count").eq("user_id", _get_user_id(email)).eq("day", _today()).execute()
        return response.data[0]["count"] if response.data else 0
    except Exception:
        return 0


def _get_user_id(email: str) -> str:
    """Récupère l'ID utilisateur."""
    if not supabase:
        return ""

    try:
        user = get_or_create_user(email)
        return user.get("id", "")
    except Exception:
        return ""


def _increment_monthly(email: str) -> int:
    """Incrémente le compteur mensuel."""
    if not supabase:
        return 1

    try:
        user_id = _get_user_id(email)
        month = _this_month()

        # Essayer de mettre à jour
        response = supabase.table("monthly_usage").select("*").eq("user_id", user_id).eq("month", month).execute()

        if response.data:
            # Mettre à jour
            new_count = response.data[0]["count"] + 1
            supabase.table("monthly_usage").update({"count": new_count}).eq("user_id", user_id).eq("month", month).execute()
            return new_count
        else:
            # Créer une nouvelle entrée
            supabase.table("monthly_usage").insert({"user_id": user_id, "month": month, "count": 1}).execute()
            return 1
    except Exception as e:
        print(f"Erreur _increment_monthly: {e}")
        return 1


def _increment_daily(email: str) -> int:
    """Incrémente le compteur journalier."""
    if not supabase:
        return 1

    try:
        user_id = _get_user_id(email)
        day = _today()

        # Essayer de mettre à jour
        response = supabase.table("daily_usage").select("*").eq("user_id", user_id).eq("day", day).execute()

        if response.data:
            # Mettre à jour
            new_count = response.data[0]["count"] + 1
            supabase.table("daily_usage").update({"count": new_count}).eq("user_id", user_id).eq("day", day).execute()
            return new_count
        else:
            # Créer une nouvelle entrée
            supabase.table("daily_usage").insert({"user_id": user_id, "day": day, "count": 1}).execute()
            return 1
    except Exception as e:
        print(f"Erreur _increment_daily: {e}")
        return 1


def increment_usage(email: str) -> None:
    """Incrémente les compteurs selon le tier."""
    tier = get_user_tier(email)

    # Tiers avec limite mensuelle
    if tier in ("free", "pro"):
        _increment_monthly(email)
    # Tiers avec limite journalière
    elif tier in ("gold", "agency"):
        _increment_daily(email)
    # Admin et beta: pas de limite


def get_usage(email: str) -> int:
    """Récupère le compteur mensuel ou journalier selon le tier."""
    tier = get_user_tier(email)

    if tier in ("free", "pro"):
        return _get_monthly_count(email)
    elif tier in ("gold", "agency"):
        return _get_daily_count(email)
    return 0


def get_tier_expiry(email: str) -> Optional[str]:
    """Récupère la date d'expiration du tier."""
    if not supabase:
        return None

    try:
        user = get_or_create_user(email)
        return user.get("tier_expiry")
    except Exception:
        return None


def get_all_users() -> list[dict]:
    """Récupère tous les utilisateurs depuis Supabase."""
    if not supabase:
        print("get_all_users: supabase client not available")
        return []

    try:
        response = supabase.table("users").select("*").execute()
        print(f"get_all_users: response data count = {len(response.data) if response.data else 0}")
        if not response.data:
            print("get_all_users: no data from supabase")
            return []

        users = []
        for row in response.data:
            users.append({
                "email": row.get("email"),
                "tier": row.get("tier", "free"),
                "expiry": row.get("tier_expiry")
            })
        print(f"get_all_users: returning {len(users)} users")
        return users
    except Exception as e:
        print(f"Erreur Supabase get_all_users: {e}")
        import traceback
        traceback.print_exc()
        return []
