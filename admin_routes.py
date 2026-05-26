from __future__ import annotations

"""
Routes admin — accessibles uniquement à l'email ADMIN_EMAIL.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from auth import (
    get_user_from_request, is_admin,
    set_user_tier, _user_tiers, _monthly_usage, _daily_usage,
    TIER_CONFIG, usage_info,
)

router = APIRouter(prefix="/admin")


def _require_admin(request: Request) -> dict:
    user = get_user_from_request(request)
    if not is_admin(user):
        raise HTTPException(status_code=403, detail="Accès admin requis.")
    return user


# ── GET /admin/users ─────────────────────────────────────────
@router.get("/users")
async def list_users(request: Request):
    _require_admin(request)
    users = []

    # Try Supabase first, fallback to in-memory
    try:
        from supabase_client import get_all_users, SUPABASE_ENABLED
        if SUPABASE_ENABLED:
            supabase_users = get_all_users()
            for user_data in supabase_users:
                email = user_data["email"]
                tier = user_data.get("tier", "free")
                cfg = TIER_CONFIG.get(tier, TIER_CONFIG["free"])
                users.append({
                    "email": email,
                    "tier": tier,
                    "label": cfg["label"],
                    "customer_id": None,  # Not stored in simple query
                })
            return {"ok": True, "count": len(users), "users": users}
    except Exception as e:
        print(f"Supabase error: {e}")
        pass

    # Fallback to in-memory (for backward compatibility)
    all_emails = set(_user_tiers.keys()) | set(_monthly_usage.keys()) | set(_daily_usage.keys())
    for email in sorted(all_emails):
        tier_data = _user_tiers.get(email, {})
        tier = tier_data.get("tier", "free")
        cfg  = TIER_CONFIG.get(tier, TIER_CONFIG["free"])
        users.append({
            "email":       email,
            "tier":        tier,
            "label":       cfg["label"],
            "customer_id": tier_data.get("customer_id"),
        })
    return {"ok": True, "count": len(users), "users": users}


# ── POST /admin/set-tier ─────────────────────────────────────
class SetTierBody(BaseModel):
    email: str
    tier:  str
    expiry: Optional[str] = None  # ISO date YYYY-MM-DD ou None pour pas d'expiration

@router.post("/set-tier")
async def set_tier(body: SetTierBody, request: Request):
    _require_admin(request)
    if body.tier not in TIER_CONFIG:
        raise HTTPException(status_code=400, detail=f"Tier invalide. Choix : {list(TIER_CONFIG.keys())}")
    set_user_tier(body.email.lower().strip(), body.tier, expiry=body.expiry)
    msg = f"{body.email} → {body.tier.upper()}"
    if body.expiry:
        msg += f" (expire le {body.expiry})"
    return {"ok": True, "email": body.email, "tier": body.tier, "expiry": body.expiry, "message": msg}


# ── POST /admin/grant-beta ───────────────────────────────────
class GrantBetaBody(BaseModel):
    email: str

@router.post("/grant-beta")
async def grant_beta(body: GrantBetaBody, request: Request):
    _require_admin(request)
    set_user_tier(body.email.lower().strip(), "beta")
    return {"ok": True, "email": body.email, "tier": "beta", "message": "Accès beta activé ✅"}


# ── DELETE /admin/revoke ─────────────────────────────────────
class RevokeBody(BaseModel):
    email: str

@router.post("/revoke")
async def revoke(body: RevokeBody, request: Request):
    _require_admin(request)
    set_user_tier(body.email.lower().strip(), "free")
    return {"ok": True, "email": body.email, "tier": "free", "message": "Accès révoqué → free"}
