"""
Authentification et gestion des quotas.
Phase 1 (beta) : token = email simple, comptage in-memory.
Phase 2 (juillet) : magic link + Stripe + base de données.
"""
from __future__ import annotations
from typing import Optional
from fastapi import HTTPException, Request

# ── CONFIGURATION ─────────────────────────────────────────────
FREE_LIMIT = 5  # analyses gratuites par session serveur

# Comptage in-memory par email (resets au redémarrage Render — OK pour beta)
_usage_store: dict[str, int] = {}


# ── TOKEN / UTILISATEUR ───────────────────────────────────────

def get_user_from_request(request: Request) -> dict:
    """
    Extrait l'utilisateur depuis le header Authorization.
    Format attendu : Bearer <email>
    Retourne un dict user (jamais d'exception si pas de token — anonyme autorisé).
    """
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return {"email": None, "tier": "free", "valid": False}

    token = auth[7:].strip()
    if not token or "@" not in token or len(token) < 5:
        raise HTTPException(status_code=401, detail="Token invalide.")

    return {
        "email": token,
        "tier":  "free",   # → "pro" une fois Stripe intégré
        "valid": True,
    }


# ── QUOTA ─────────────────────────────────────────────────────

def get_usage(email: str) -> int:
    return _usage_store.get(email, 0)


def increment_usage(email: str) -> int:
    _usage_store[email] = get_usage(email) + 1
    return _usage_store[email]


def check_quota(user: dict) -> None:
    """
    Lève une HTTPException 429 si l'utilisateur a atteint sa limite.
    Les anonymes (non connectés) ne sont pas bloqués ici — le client gère.
    Les utilisateurs pro ont un quota illimité.
    """
    if not user["valid"]:
        return  # Anonyme : limite gérée côté client uniquement

    if user["tier"] == "pro":
        return  # Illimité

    count = get_usage(user["email"])
    if count >= FREE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Limite gratuite atteinte ({FREE_LIMIT} analyses). Reviens en juillet pour le plan premium."
        )


def usage_info(user: dict) -> dict:
    """Retourne les infos de quota pour l'utilisateur."""
    if not user["valid"]:
        return {"tracked": False}
    count = get_usage(user["email"])
    return {
        "tracked":   True,
        "email":     user["email"],
        "used":      count,
        "limit":     None if user["tier"] == "pro" else FREE_LIMIT,
        "remaining": None if user["tier"] == "pro" else max(0, FREE_LIMIT - count),
    }
