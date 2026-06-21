"""
OAuth TikTok — 2 providers complémentaires.

  • provider="display"  → TikTok for Developers / Login Kit / Display API.
      Donne les vidéos publiées du créateur + leurs métriques publiques
      (view/like/comment/share counts). Token : open.tiktokapis.com (form-urlencoded).

  • provider="business" → TikTok for Business / Marketing API (creator insights).
      Donne les insights d'AUDIENCE (démographie, activité) via /business/get/.
      Token : business-api.tiktok.com (JSON, réponse {code,message,data}).

Les deux passent par l'écran d'autorisation https://www.tiktok.com/v2/auth/authorize/
mais avec des client_key / scopes / endpoints de token DIFFÉRENTS. Le `state` signé
(HMAC, anti-CSRF, TTL 10 min) porte l'email ET le provider, pour que le callback
unique sache quel flux traiter.

Toutes les clés viennent de l'environnement — JAMAIS de secret en dur.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from datetime import date, timedelta
from typing import Optional, Tuple
from urllib.parse import urlencode

import httpx

from auth import SECRET_KEY

APP_PUBLIC_URL = os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")
REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI", f"{APP_PUBLIC_URL}/api/auth/tiktok/callback")
_STATE_TTL_SECONDS = 600

# ── Scopes par défaut ────────────────────────────────────────────────────────
DEFAULT_DISPLAY_SCOPES = "user.info.basic,user.info.profile,user.info.stats,video.list"
DEFAULT_BUSINESS_SCOPES = (
    "user.info.basic,biz.creator.info,biz.creator.insights,user.info.username,"
    "user.info.stats,user.account.type,user.insights"
)

# ── Champs de données ────────────────────────────────────────────────────────
_USER_FIELDS = (
    "open_id,union_id,avatar_url,display_name,bio_description,profile_deep_link,"
    "follower_count,following_count,likes_count,video_count"
)
_VIDEO_FIELDS = (
    "id,title,video_description,duration,cover_image_url,embed_link,share_url,"
    "like_count,comment_count,share_count,view_count,create_time"
)
# Champs /business/get/ (configurables : les insights audience varient selon l'accès).
_DEFAULT_BIZ_FIELDS = (
    "display_name,profile_image,followers_count,audience_countries,"
    "audience_genders,audience_ages,audience_activity,video_views,likes,comments,shares"
)


def _cfg(provider: str) -> dict:
    """Configuration (clés + endpoints) selon le provider."""
    if provider == "business":
        return {
            "provider": "business",
            "app_id": os.getenv("TIKTOK_BIZ_APP_ID", ""),
            "app_secret": os.getenv("TIKTOK_BIZ_APP_SECRET", ""),
            "scopes": os.getenv("TIKTOK_BIZ_SCOPES", DEFAULT_BUSINESS_SCOPES),
            "authorize_url": os.getenv("TIKTOK_BIZ_AUTHORIZE_URL", "https://www.tiktok.com/v2/auth/authorize/"),
            "token_url": os.getenv("TIKTOK_BIZ_TOKEN_URL", "https://business-api.tiktok.com/open_api/v1.3/tt_user/oauth2/token/"),
            "refresh_url": os.getenv("TIKTOK_BIZ_REFRESH_URL", "https://business-api.tiktok.com/open_api/v1.3/tt_user/oauth2/refresh_token/"),
            "api_base": os.getenv("TIKTOK_BIZ_API_BASE", "https://business-api.tiktok.com/open_api/v1.3").rstrip("/"),
            "token_style": "business",   # JSON, client_id/auth_code, réponse encapsulée
        }
    # display (défaut)
    return {
        "provider": "display",
        "app_id": os.getenv("TIKTOK_APP_ID", ""),
        "app_secret": os.getenv("TIKTOK_APP_SECRET", ""),
        "scopes": os.getenv("TIKTOK_SCOPES", DEFAULT_DISPLAY_SCOPES),
        "authorize_url": os.getenv("TIKTOK_AUTHORIZE_URL", "https://www.tiktok.com/v2/auth/authorize/"),
        "token_url": os.getenv("TIKTOK_TOKEN_URL", "https://open.tiktokapis.com/v2/oauth/token/"),
        "refresh_url": os.getenv("TIKTOK_REFRESH_URL", "https://open.tiktokapis.com/v2/oauth/token/"),
        "api_base": os.getenv("TIKTOK_API_BASE", "https://open.tiktokapis.com/v2").rstrip("/"),
        "token_style": "display",        # form-urlencoded, client_key/code, réponse plate
    }


def is_configured(provider: str = "display") -> bool:
    c = _cfg(provider)
    return bool(c["app_id"] and c["app_secret"])


# ── State signé (porte email + provider) ─────────────────────────────────────
def make_state(email: str, provider: str = "display") -> str:
    ts = str(int(time.time()))
    nonce = base64.urlsafe_b64encode(os.urandom(9)).decode().rstrip("=")
    email_b64 = base64.urlsafe_b64encode(email.encode()).decode().rstrip("=")
    payload = f"{email_b64}|{provider}|{ts}|{nonce}"
    sig = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"


def verify_state(state: str) -> Tuple[Optional[str], Optional[str]]:
    """Retourne (email, provider) ou (None, None) si invalide/expiré."""
    try:
        payload, sig = state.rsplit(".", 1)
        expected = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None, None
        email_b64, provider, ts, _nonce = payload.split("|", 3)
        if int(time.time()) - int(ts) > _STATE_TTL_SECONDS:
            return None, None
        pad = "=" * (-len(email_b64) % 4)
        email = base64.urlsafe_b64decode(email_b64 + pad).decode()
        return email, (provider or "display")
    except Exception:
        return None, None


# ── URL d'autorisation ───────────────────────────────────────────────────────
def build_authorize_url(state: str, provider: str = "display") -> str:
    c = _cfg(provider)
    params = {
        "client_key": c["app_id"],
        "scope": c["scopes"],
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": state,
    }
    return f"{c['authorize_url']}?{urlencode(params)}"


# ── Échange / refresh du token ───────────────────────────────────────────────
def _unwrap(body) -> dict:
    if not isinstance(body, dict):
        return {}
    err = body.get("error")
    if err and err not in ("", "ok"):
        raise RuntimeError(f"TikTok OAuth error: {body.get('error_description') or err}")
    if "data" in body and isinstance(body["data"], dict) and "access_token" in body["data"]:
        if body.get("code") not in (0, None):
            raise RuntimeError(f"TikTok API error: {body.get('message') or body}")
        return body["data"]
    return body


async def exchange_code_for_token(auth_code: str, provider: str = "display") -> dict:
    c = _cfg(provider)
    async with httpx.AsyncClient(timeout=20.0) as client:
        if c["token_style"] == "business":
            payload = {
                "client_id": c["app_id"],
                "client_secret": c["app_secret"],
                "grant_type": "authorization_code",
                "auth_code": auth_code,
            }
            resp = await client.post(c["token_url"], json=payload)
        else:
            data = {
                "client_key": c["app_id"],
                "client_secret": c["app_secret"],
                "code": auth_code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI,
            }
            resp = await client.post(c["token_url"], data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    resp.raise_for_status()
    result = _unwrap(resp.json())
    if not isinstance(result, dict) or not result.get("access_token"):
        raise RuntimeError(f"TikTok token exchange ({provider}): pas d'access_token (réponse: {result})")
    return result


async def refresh_access_token(refresh_token: str, provider: str = "display") -> dict:
    c = _cfg(provider)
    async with httpx.AsyncClient(timeout=20.0) as client:
        if c["token_style"] == "business":
            payload = {
                "client_id": c["app_id"],
                "client_secret": c["app_secret"],
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
            resp = await client.post(c["refresh_url"], json=payload)
        else:
            data = {
                "client_key": c["app_id"],
                "client_secret": c["app_secret"],
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
            resp = await client.post(c["refresh_url"], data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    resp.raise_for_status()
    return _unwrap(resp.json())


# ── Persistance Supabase (1 ligne par email + provider) ──────────────────────
def save_tiktok_token(email: str, data: dict, provider: str = "display") -> bool:
    try:
        from supabase_client import supabase
    except Exception:
        return False
    if not supabase or not isinstance(data, dict):
        return False
    now = int(time.time())
    access_ttl = data.get("expires_in") or data.get("access_token_expire_in")
    refresh_ttl = (
        data.get("refresh_expires_in")
        or data.get("refresh_token_expires_in")
        or data.get("refresh_token_expire_in")
    )
    row = {
        "email": (email or "").lower(),
        "provider": provider,
        "open_id": data.get("open_id") or data.get("seller_id"),
        "seller_name": data.get("seller_name"),
        "region": data.get("seller_base_region") or data.get("region"),
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token"),
        "access_token_expires_at": (now + int(access_ttl)) if access_ttl else None,
        "refresh_token_expires_at": (now + int(refresh_ttl)) if refresh_ttl else None,
        "scope": data.get("scope") or data.get("granted_scopes"),
        "updated_at": now,
    }
    try:
        supabase.table("tiktok_tokens").upsert(row, on_conflict="email,provider").execute()
        return True
    except Exception as e:  # pragma: no cover
        print(f"tiktok_oauth.save_tiktok_token error: {e}")
        return False


def get_saved_token(email: str, provider: str = "display") -> Optional[dict]:
    try:
        from supabase_client import supabase
    except Exception:
        return None
    if not supabase:
        return None
    try:
        r = (
            supabase.table("tiktok_tokens").select("*")
            .eq("email", (email or "").lower()).eq("provider", provider).execute()
        )
        return r.data[0] if r.data else None
    except Exception as e:
        print(f"tiktok_oauth.get_saved_token error: {e}")
        return None


def _persist_refreshed(email: str, provider: str, data: dict) -> None:
    try:
        from supabase_client import supabase
    except Exception:
        return
    if not supabase:
        return
    now = int(time.time())
    access_ttl = data.get("expires_in") or data.get("access_token_expire_in")
    refresh_ttl = data.get("refresh_expires_in") or data.get("refresh_token_expires_in")
    upd = {
        "access_token": data.get("access_token"),
        "access_token_expires_at": (now + int(access_ttl)) if access_ttl else None,
        "updated_at": now,
    }
    if data.get("refresh_token"):
        upd["refresh_token"] = data["refresh_token"]
        if refresh_ttl:
            upd["refresh_token_expires_at"] = now + int(refresh_ttl)
    try:
        supabase.table("tiktok_tokens").update(upd).eq("email", (email or "").lower()).eq("provider", provider).execute()
    except Exception as e:
        print(f"tiktok_oauth._persist_refreshed error: {e}")


async def _ensure_access_token(row: dict, provider: str) -> Optional[str]:
    now = int(time.time())
    exp = int(row.get("access_token_expires_at") or 0)
    access = row.get("access_token")
    if access and now < (exp - 60):
        return access
    refresh = row.get("refresh_token")
    if not refresh:
        return access
    try:
        refreshed = await refresh_access_token(refresh, provider)
    except Exception as e:
        print(f"tiktok_oauth refresh ({provider}) failed: {e}")
        return access
    if refreshed.get("access_token"):
        _persist_refreshed(row.get("email"), provider, refreshed)
        return refreshed["access_token"]
    return access


# ── DISPLAY : profil + vidéos ────────────────────────────────────────────────
async def fetch_user_info(access_token: str) -> dict:
    c = _cfg("display")
    url = f"{c['api_base']}/user/info/?fields={_USER_FIELDS}"
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
    resp.raise_for_status()
    return (resp.json().get("data") or {}).get("user") or {}


async def fetch_video_list(access_token: str, max_count: int = 20) -> list:
    c = _cfg("display")
    url = f"{c['api_base']}/video/list/?fields={_VIDEO_FIELDS}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=25.0) as client:
        resp = await client.post(url, headers=headers, json={"max_count": max_count})
    resp.raise_for_status()
    return (resp.json().get("data") or {}).get("videos") or []


async def get_profile_and_videos(email: str) -> Optional[dict]:
    row = get_saved_token(email, "display")
    if not row or not row.get("access_token"):
        return None
    access = await _ensure_access_token(row, "display")
    if not access:
        return None
    profile, videos = {}, []
    try:
        profile = await fetch_user_info(access)
    except Exception as e:
        print(f"tiktok_oauth.fetch_user_info error: {e}")
    try:
        videos = await fetch_video_list(access)
    except Exception as e:
        print(f"tiktok_oauth.fetch_video_list error: {e}")
    return {"profile": profile, "videos": videos}


# ── BUSINESS : insights d'audience (/business/get/) ──────────────────────────
async def get_audience_insights(email: str) -> Optional[dict]:
    row = get_saved_token(email, "business")
    if not row or not row.get("access_token"):
        return None
    access = await _ensure_access_token(row, "business")
    business_id = row.get("open_id")
    if not access or not business_id:
        return None
    c = _cfg("business")
    fields = os.getenv("TIKTOK_BIZ_FIELDS", _DEFAULT_BIZ_FIELDS).split(",")
    end = date.today()
    start = end - timedelta(days=28)
    params = {
        "business_id": business_id,
        "fields": json.dumps([f.strip() for f in fields if f.strip()]),
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
    }
    url = f"{c['api_base']}/business/get/"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params=params, headers={"Access-Token": access})
        resp.raise_for_status()
        return _unwrap(resp.json())
    except Exception as e:
        print(f"tiktok_oauth.get_audience_insights error: {e}")
        return None
