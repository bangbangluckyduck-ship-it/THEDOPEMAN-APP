"""
Authentification et gestion des quotas par tier.

Tiers :
  free   → 3 analyses/mois (upload uniquement) (0 €)
  pro    → 300 analyses/mois  (19,90 €/mois)
  gold   → 1000 analyses/mois (99 €/mois)
  agency → 5000 analyses/mois (5 comptes Gold × 1000)

Stockage : Supabase PostgreSQL (persiste entre redémarrages).
Fallback : in-memory si Supabase non configuré.
"""
from __future__ import annotations
import os
import hmac
import hashlib
import base64
from time import time
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
# Clé secrète pour signer les tokens de session (HMAC).
# Aucune valeur par défaut : un secret par défaut connu permettrait à quiconque de
# forger des tokens valides. Si aucun secret n'est configuré, l'app refuse de
# démarrer (fail-fast au boot) plutôt que de tourner avec un secret prévisible.
#
# ⚠️ SÉCURITÉ (recommandé) : privilégie APP_SIGNING_SECRET, une valeur DÉDIÉE et
# réellement secrète (ex. `python -c "import secrets; print(secrets.token_urlsafe(48))"`).
# SUPABASE_ANON_KEY est conservé comme repli pour ne rien casser, MAIS la clé « anon »
# de Supabase est conçue pour être PUBLIQUE (rôle anon, embarquée côté client) : si elle
# fuite, un attaquant pourrait forger un token pour n'importe quel email — y compris
# l'admin, identifié par simple égalité d'email. Définir APP_SIGNING_SECRET coupe ce
# risque (les sessions existantes devront se reconnecter une fois la variable posée).
_SECRET_KEY_RAW = (
    os.getenv("APP_SIGNING_SECRET", "").strip()
    or os.getenv("SUPABASE_ANON_KEY", "").strip()
)
if not _SECRET_KEY_RAW:
    raise RuntimeError(
        "Aucun secret de signature configuré : définis APP_SIGNING_SECRET (recommandé, "
        "valeur dédiée et secrète) ou, à défaut, SUPABASE_ANON_KEY, dans l'environnement "
        "(.env / Render) avant de démarrer. Aucun secret par défaut n'est autorisé."
    )
SECRET_KEY = _SECRET_KEY_RAW.encode()

# ── CONFIGURATION DES TIERS ───────────────────────────────────
TIER_CONFIG: dict[str, dict] = {
    "free":   {"monthly": 3,    "daily": None, "seats": 1,  "label": "FREE"},
    "pro":    {"monthly": 300,  "daily": None, "seats": 1,  "label": "PRO"},
    "gold":   {"monthly": 1000, "daily": None, "seats": 1,  "label": "GOLD"},
    "agency": {"monthly": 5000, "daily": None, "seats": 5,  "label": "AGENCY"},
    "beta":   {"monthly": 999999, "daily": None, "seats": 1, "label": "BETA"},
    "admin":  {"monthly": None, "daily": None, "seats": 99, "label": "ADMIN"},
}

# ── STORES in-memory ──────────────────────────────────────────
_user_tiers: dict[str, dict] = {}
_monthly_usage: dict[str, dict] = {}
_daily_usage: dict[str, dict] = {}

# ── GESTION DES TIERS ─────────────────────────────────────────

def set_user_tier(
    email: str,
    tier: str,
    customer_id: Optional[str] = None,
    subscription_id: Optional[str] = None,
    expiry: Optional[str] = None,
) -> None:
    if tier not in TIER_CONFIG:
        tier = "free"

    if SUPABASE_ENABLED:
        supabase_set_user_tier(email, tier, customer_id, subscription_id, expiry)
    else:
        _user_tiers[email] = {
            "tier":            tier,
            "customer_id":     customer_id,
            "subscription_id": subscription_id,
            "expiry":          expiry,
        }

def _check_tier_expiry(email: str) -> None:
    data = _user_tiers.get(email, {})
    if not data.get("expiry"):
        return

    expiry_str = data["expiry"]
    try:
        expiry_date = datetime.fromisoformat(expiry_str).date()
        today = datetime.now(timezone.utc).date()
        if today > expiry_date:
            data["tier"] = "free"
            data["expiry"] = None
    except (ValueError, TypeError):
        pass

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


# ── TOKEN / UTILISATEUR (SÉCURISÉ HMAC) ───────────────────────

def _session_ttl_seconds() -> int:
    """Durée de vie d'un token de session, en secondes (0 = pas d'expiration).
    Configurable via SESSION_TTL_DAYS (défaut : 30 jours)."""
    try:
        days = float(os.getenv("SESSION_TTL_DAYS", "30"))
    except (TypeError, ValueError):
        days = 30.0
    return int(days * 86400) if days > 0 else 0


def create_access_token(email: str) -> str:
    """Crée un token de session signé HMAC, horodaté et à durée de vie limitée.

    Format v2 : base64(email).timestamp.signature  où
    signature = HMAC(SECRET_KEY, "email|timestamp"). Le timestamp permet
    d'expirer le token (cf. SESSION_TTL_DAYS) — un token volé n'est plus valable
    indéfiniment. Les anciens tokens (format v1 sans horodatage) restent acceptés
    en vérification pour ne pas déconnecter brutalement les sessions en cours ;
    ils disparaissent à la reconnexion (nouveau token v2) ou lors d'une rotation
    de APP_SIGNING_SECRET."""
    ts = str(int(time()))
    email_b64 = base64.b64encode(email.encode()).decode()
    payload = f"{email}|{ts}"
    signature = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return f"{email_b64}.{ts}.{signature}"

def verify_access_token(token: str) -> Optional[str]:
    """Vérifie la signature cryptographique du token et retourne l'email.
    Rejette les tokens v2 expirés. compare_digest empêche les attaques temporelles."""
    try:
        if not token or "." not in token:
            return None
        parts = token.split(".")
        if len(parts) == 3:
            # ── Format v2 : email_b64 . ts . signature ──
            email_b64, ts_str, signature = parts
            email = base64.b64decode(email_b64).decode()
            expected = hmac.new(SECRET_KEY, f"{email}|{ts_str}".encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected):
                return None
            ttl = _session_ttl_seconds()
            if ttl > 0:
                try:
                    issued = int(ts_str)
                except (TypeError, ValueError):
                    return None
                if time() - issued > ttl:
                    return None  # token expiré
            return email
        if len(parts) == 2:
            # ── Format v1 (legacy, sans horodatage) : accepté en rétro-compat ──
            email_b64, signature = parts
            email = base64.b64decode(email_b64).decode()
            expected = hmac.new(SECRET_KEY, email.encode(), hashlib.sha256).hexdigest()
            if hmac.compare_digest(signature, expected):
                return email
    except Exception:
        pass
    return None


def make_unsubscribe_token(email: str) -> str:
    """Signature HMAC pour le lien de désinscription marketing (anti-falsification)."""
    return hmac.new(SECRET_KEY, ("unsub:" + (email or "").lower()).encode(), hashlib.sha256).hexdigest()


def verify_unsubscribe_token(email: str, token: str) -> bool:
    return hmac.compare_digest(token or "", make_unsubscribe_token(email))

def get_user_from_request(request: Request) -> dict:
    """
    Extrait et valide l'utilisateur depuis le header Authorization.
    Format attendu : Bearer <token_hmac>
    """
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return {"email": None, "tier": "free", "valid": False}

    token = auth[7:].strip()
    
    # Vérification stricte du token (empêche la modification du localStorage)
    email = verify_access_token(token)
    
    if not email:
        raise HTTPException(status_code=401, detail="Session expirée ou non valide. Veuillez vous reconnecter.")

    # Admin reconnu automatiquement
    if ADMIN_EMAIL and email.lower() == ADMIN_EMAIL:
        return {"email": email.lower(), "tier": "admin", "valid": True, "is_admin": True}

    tier = get_user_tier(email)
    return {
        "email":    email.lower(),
        "tier":     tier,
        "valid":    True,
        "is_admin": False,
    }

# ── QUOTA ─────────────────────────────────────────────────────

def is_admin(user: dict) -> bool:
    return user.get("is_admin", False) or user.get("tier") == "admin"

def check_quota(user: dict) -> None:
    if not user["valid"]:
        return

    if is_admin(user):
        return

    tier   = user["tier"]
    email  = user["email"]
    cfg    = TIER_CONFIG.get(tier, TIER_CONFIG["free"])

    if cfg["monthly"] is not None:
        if SUPABASE_ENABLED:
            count = supabase_get_monthly_count(email)
        else:
            count = _get_monthly_count(email)
        if count >= cfg["monthly"]:
            label = cfg["label"]
            raise HTTPException(
                status_code=429,
                detail=f"Quota {label} atteint ({cfg['monthly']} analyses/mois). Passe au plan supérieur sur qeerah.com",
            )

    if cfg["daily"] is not None:
        if SUPABASE_ENABLED:
            count = supabase_get_daily_count(email)
        else:
            count = _get_daily_count(email)
        if count >= cfg["daily"]:
            label = cfg["label"]
            raise HTTPException(
                status_code=429,
                detail=f"Quota journalier {label} atteint ({cfg['daily']}/jour). Reviens demain ou upgrade.",
            )

def increment_usage(email: str) -> None:
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

def get_usage(email: str) -> int:
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
