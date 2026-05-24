"""
Authentification et gestion des quotas par tier.

Tiers :
  free   → 3 analyses/mois   (0 €)
  pro    → 20 analyses/mois  (9,99 €/mois)
  gold   → 25 analyses/jour  (99 €/mois)
  agency → 125 analyses/jour (249 €/mois — 5 sièges × 25)

Stockage : Supabase PostgreSQL (persiste entre redémarrages).
Fallback : in-memory si Supabase non configuré.
"""
from __future__ import annotations
import os
from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, Request

# Essayer d'importer Supabase, sinon utiliser fallback en mémoire
try:
    from supabase_client import (
        get_or_create_user,
        set_user_tier as supabase_set_user_tier,
        get_user_tier as supabase_get_user_tier,
        get_customer_id as supabase_get_customer_id,
        revoke_by_customer as supabase_revoke_by_customer,
        increment_usage as supabase_increment_usage,
        get_usage as supabase_get_usage,
        get_tier_expiry as supabase_get_tier_expiry,
        _get_monthly_count as supabase_get_monthly_count,
        _get_daily_count as supabase_get_daily_count,
    )
    SUPABASE_ENABLED = True
except (ImportError, Exception):
    SUPABASE_ENABLED = False

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "").lower().strip()

# ── CONFIGURATION DES TIERS ───────────────────────────────────
TIER_CONFIG: dict[str, dict] = {
    "free":   {"monthly": 3,    "daily": None, "seats": 1,  "label": "FREE"},
    "pro":    {"monthly": 20,   "daily": None, "seats": 1,  "label": "PRO"},
    "gold":   {"monthly": None, "daily": 25,   "seats": 1,  "label": "GOLD"},
    "agency": {"monthly": None, "daily": 125,  "seats": 5,  "label": "AGENCY"},
    "beta":   {"monthly": 999,  "daily": None, "seats": 1,  "label": "BETA"},
    "admin":  {"monthly": None, "daily": None, "seats": 99, "label": "ADMIN"},
}

# ── STORES in-memory ──────────────────────────────────────────
# { email: { "tier": str, "customer_id": str|None, "subscription_id": str|None } }
_user_tiers: dict[str, dict] = {}

# { email: { "month": "YYYY-MM", "count": int } }
_monthly_usage: dict[str, dict] = {}

# { email: { "day": "YYYY-MM-DD", "count": int } }
_daily_usage: dict[str, dict] = {}


# ── GESTION DES TIERS ─────────────────────────────────────────

def set_user_tier(
    email: str,
    tier: str,
    customer_id: Optional[str] = None,
    subscription_id: Optional[str] = None,
    expiry: Optional[str] = None,
) -> None:
    """Appelé par le webhook Stripe lors d'un paiement réussi, ou par admin pour accès temporaire.

    expiry: ISO date string (YYYY-MM-DD) ou None pour pas d'expiration.
    """
    if tier not in TIER_CONFIG:
        tier = "free"

    # Utiliser Supabase si disponible
    if SUPABASE_ENABLED:
        supabase_set_user_tier(email, tier, customer_id, subscription_id, expiry)
    else:
        # Fallback en mémoire
        _user_tiers[email] = {
            "tier":            tier,
            "customer_id":     customer_id,
            "subscription_id": subscription_id,
            "expiry":          expiry,
        }


def _check_tier_expiry(email: str) -> None:
    """Vérifie si le tier a expiré et rétrograder en FREE si nécessaire."""
    data = _user_tiers.get(email, {})
    if not data.get("expiry"):
        return  # Pas d'expiration

    expiry_str = data["expiry"]
    try:
        expiry_date = datetime.fromisoformat(expiry_str).date()
        today = datetime.now(timezone.utc).date()
        if today > expiry_date:
            # Expired → downgrade to free
            data["tier"] = "free"
            data["expiry"] = None
    except (ValueError, TypeError):
        pass  # Invalid date format, ignore


def get_user_tier(email: str) -> str:
    if SUPABASE_ENABLED:
        return supabase_get_user_tier(email)
    else:
        _check_tier_expiry(email)
        return _user_tiers.get(email, {}).get("tier", "free")


def get_customer_id(email: str) -> Optional[str]:
    if SUPABASE_ENABLED:
        return supabase_get_customer_id(email)
    else:
        return _user_tiers.get(email, {}).get("customer_id")


def revoke_by_customer(customer_id: str) -> None:
    """Downgrade vers free quand l'abonnement est annulé (webhook)."""
    if SUPABASE_ENABLED:
        supabase_revoke_by_customer(customer_id)
    else:
        for data in _user_tiers.values():
            if data.get("customer_id") == customer_id:
                data["tier"] = "free"
                break


# ── COMPTEURS MENSUELS / JOURNALIERS ──────────────────────────

def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _this_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def _get_monthly_count(email: str) -> int:
    rec = _monthly_usage.get(email, {})
    return rec.get("count", 0) if rec.get("month") == _this_month() else 0


def _get_daily_count(email: str) -> int:
    rec = _daily_usage.get(email, {})
    return rec.get("count", 0) if rec.get("day") == _today() else 0


def _increment_monthly(email: str) -> int:
    month = _this_month()
    rec   = _monthly_usage.get(email, {})
    if rec.get("month") != month:
        rec = {"month": month, "count": 0}
    rec["count"] += 1
    _monthly_usage[email] = rec
    return rec["count"]


def _increment_daily(email: str) -> int:
    day = _today()
    rec = _daily_usage.get(email, {})
    if rec.get("day") != day:
        rec = {"day": day, "count": 0}
    rec["count"] += 1
    _daily_usage[email] = rec
    return rec["count"]


# ── TOKEN / UTILISATEUR ───────────────────────────────────────

def get_user_from_request(request: Request) -> dict:
    """
    Extrait l'utilisateur depuis le header Authorization.
    Format : Bearer <email>
    Retourne un dict user (jamais d'exception si pas de token — anonyme OK).
    """
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return {"email": None, "tier": "free", "valid": False}

    token = auth[7:].strip()
    if not token or "@" not in token or len(token) < 5:
        raise HTTPException(status_code=401, detail="Token invalide.")

    # Admin reconnu automatiquement
    if ADMIN_EMAIL and token.lower() == ADMIN_EMAIL:
        return {"email": token.lower(), "tier": "admin", "valid": True, "is_admin": True}

    tier = get_user_tier(token)
    return {
        "email":    token.lower(),
        "tier":     tier,
        "valid":    True,
        "is_admin": False,
    }


# ── QUOTA ─────────────────────────────────────────────────────

def is_admin(user: dict) -> bool:
    return user.get("is_admin", False) or user.get("tier") == "admin"


def check_quota(user: dict) -> None:
    """Lève 429 si l'utilisateur a atteint sa limite."""
    if not user["valid"]:
        return  # Anonyme : pas bloqué côté serveur

    # Admin et beta ont accès illimité
    if is_admin(user):
        return

    tier   = user["tier"]
    email  = user["email"]
    cfg    = TIER_CONFIG.get(tier, TIER_CONFIG["free"])

    # Quota mensuel
    if cfg["monthly"] is not None:
        if SUPABASE_ENABLED:
            count = supabase_get_monthly_count(email)
        else:
            count = _get_monthly_count(email)
        if count >= cfg["monthly"]:
            label = cfg["label"]
            raise HTTPException(
                status_code=429,
                detail=f"Quota {label} atteint ({cfg['monthly']} analyses/mois). "
                       f"Passe au plan supérieur sur tts-analyzer.fr",
            )

    # Quota journalier
    if cfg["daily"] is not None:
        if SUPABASE_ENABLED:
            count = supabase_get_daily_count(email)
        else:
            count = _get_daily_count(email)
        if count >= cfg["daily"]:
            label = cfg["label"]
            raise HTTPException(
                status_code=429,
                detail=f"Quota journalier {label} atteint ({cfg['daily']}/jour). "
                       f"Reviens demain ou upgrade.",
            )


def increment_usage(email: str) -> None:
    """Incrémente les compteurs appropriés selon le tier."""
    if SUPABASE_ENABLED:
        supabase_increment_usage(email)
    else:
        tier = get_user_tier(email)
        cfg  = TIER_CONFIG.get(tier, TIER_CONFIG["free"])

        if cfg["monthly"] is not None:
            _increment_monthly(email)
        if cfg["daily"] is not None:
            _increment_daily(email)


def usage_info(user: dict) -> dict:
    """Retourne les infos de quota pour l'UI."""
    if not user["valid"]:
        return {"tracked": False}

    email = user["email"]
    tier  = user["tier"]
    cfg   = TIER_CONFIG.get(tier, TIER_CONFIG["free"])

    if SUPABASE_ENABLED:
        used = (
            supabase_get_monthly_count(email) if cfg["monthly"] is not None
            else supabase_get_daily_count(email)
        )
        expiry = supabase_get_tier_expiry(email)
    else:
        used = (
            _get_monthly_count(email) if cfg["monthly"] is not None
            else _get_daily_count(email)
        )
        expiry = _user_tiers.get(email, {}).get("expiry")

    limit = cfg["monthly"] if cfg["monthly"] is not None else cfg["daily"]

    return {
        "tracked":     True,
        "email":       email,
        "tier":        tier,
        "label":       cfg["label"],
        "used":        used,
        "limit":       limit,
        "remaining":   max(0, limit - used) if limit else None,
        "customer_id": get_customer_id(email),
        "expiry":      expiry,
    }


# ── LEGACY (compatibilité main.py existant) ───────────────────
def get_usage(email: str) -> int:
    """Compat : retourne le compteur mensuel ou journalier selon le tier."""
    tier = get_user_tier(email)
    cfg  = TIER_CONFIG.get(tier, TIER_CONFIG["free"])
    if SUPABASE_ENABLED:
        if cfg["monthly"] is not None:
            return supabase_get_monthly_count(email)
        return supabase_get_daily_count(email)
    else:
        if cfg["monthly"] is not None:
            return _get_monthly_count(email)
        return _get_daily_count(email)
