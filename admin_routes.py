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


# ── POST /admin/reset-user-password ──────────────────────────
class ResetPasswordBody(BaseModel):
    email: str
    reset_type: str  # 'magic_link' or 'temporary_password'

@router.post("/reset-user-password")
async def reset_user_password(body: ResetPasswordBody, request: Request):
    """Admin reset user password with 2 options."""
    import bcrypt
    from supabase_client import supabase
    from password_reset import (
        generate_reset_token,
        generate_temporary_password,
        hash_token,
        create_password_reset_token,
    )
    from email_service import email_service

    _require_admin(request)

    email = body.email.lower().strip()
    reset_type = body.reset_type.lower()

    if reset_type not in ["magic_link", "temporary_password"]:
        raise HTTPException(status_code=400, detail="Type invalide: magic_link ou temporary_password")

    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")

    try:
        # Verify user exists
        user_exists = supabase.table("users").select("id").eq("email", email).execute()
        if not user_exists.data:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        if reset_type == "magic_link":
            # Generate magic link
            reset_token = generate_reset_token()
            token_hash = hash_token(reset_token)

            success, _, _ = create_password_reset_token(email, "magic_link")
            if not success:
                raise HTTPException(status_code=500, detail="Erreur création token")

            # Send email with magic link
            reset_link = f"https://tts-analyzer.fr/reset-password?token={reset_token}&email={email}"
            email_sent = await email_service.send_magic_link_email(email, reset_link)

            if not email_sent:
                raise HTTPException(status_code=500, detail="Erreur envoi email")

            return {
                "ok": True,
                "email": email,
                "method": "magic_link",
                "message": "Lien magique envoyé par email à l'utilisateur"
            }

        else:  # temporary_password
            # Generate temporary password
            temp_password = generate_temporary_password()
            password_hash = bcrypt.hashpw(temp_password.encode(), bcrypt.gensalt()).decode()

            success, _, _ = create_password_reset_token(email, "temporary_password", password_hash)
            if not success:
                raise HTTPException(status_code=500, detail="Erreur création token")

            # Send email with temporary password
            email_sent = await email_service.send_temporary_password_email(email, temp_password)

            if not email_sent:
                raise HTTPException(status_code=500, detail="Erreur envoi email")

            return {
                "ok": True,
                "email": email,
                "method": "temporary_password",
                "temp_password": temp_password,  # Return to admin to communicate if needed
                "message": "Mot de passe temporaire généré et envoyé par email"
            }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Admin reset password error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
