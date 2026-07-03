"""
OAuth Google — connexion « Continuer avec Google » (login / inscription).

Contrairement à l'OAuth TikTok (qui LIE un compte TikTok à un utilisateur déjà
connecté), Google sert ici à AUTHENTIFIER : le callback récupère l'email Google
vérifié, crée/récupère le user Supabase, émet un token d'accès Qeerah (même
format que le login e-mail, cf. auth.create_access_token) et redirige vers /app.

Le `state` signé (HMAC, TTL 10 min, comme tiktok_oauth) protège du CSRF.
Toutes les clés viennent de l'environnement — JAMAIS de secret en dur.

Config côté Google Cloud → « OAuth 2.0 Client ID » de type *Web application* :
  - Authorized redirect URI = {APP_PUBLIC_URL}/api/auth/google/callback
  - GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET dans l'environnement.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import time
from typing import Optional
from urllib.parse import urlencode

import httpx

from auth import SECRET_KEY

APP_PUBLIC_URL = os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", f"{APP_PUBLIC_URL}/api/auth/google/callback")
_STATE_TTL_SECONDS = 600

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
SCOPES = os.getenv("GOOGLE_SCOPES", "openid email profile")

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def is_configured() -> bool:
    return bool(CLIENT_ID and CLIENT_SECRET)


# ── State signé (anti-CSRF, TTL 10 min) ──────────────────────────────────────
def make_state() -> str:
    ts = str(int(time.time()))
    nonce = base64.urlsafe_b64encode(os.urandom(12)).decode().rstrip("=")
    payload = f"{ts}|{nonce}"
    sig = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"


def verify_state(state: str) -> bool:
    try:
        payload, sig = state.rsplit(".", 1)
        expected = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return False
        ts, _nonce = payload.split("|", 1)
        return (int(time.time()) - int(ts)) <= _STATE_TTL_SECONDS
    except Exception:
        return False


# ── URL d'autorisation ───────────────────────────────────────────────────────
def build_authorize_url(state: str) -> str:
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "state": state,
        "access_type": "online",
        "prompt": "select_account",
        "include_granted_scopes": "true",
    }
    return f"{AUTHORIZE_URL}?{urlencode(params)}"


# ── Échange code → email Google vérifié ──────────────────────────────────────
async def exchange_code_for_email(code: str) -> Optional[str]:
    """Échange le code contre un access_token puis lit l'email Google VÉRIFIÉ.
    Retourne l'email en minuscules, ou None si échec / email non vérifié."""
    async with httpx.AsyncClient(timeout=20.0) as client:
        tok = await client.post(TOKEN_URL, data={
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }, headers={"Accept": "application/json"})
        tok.raise_for_status()
        access_token = (tok.json() or {}).get("access_token")
        if not access_token:
            return None
        ui = await client.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
        ui.raise_for_status()
        info = ui.json() or {}
    email = (info.get("email") or "").lower().strip()
    # email_verified peut être booléen ou absent selon le compte ; on refuse le faux explicite.
    if not email or info.get("email_verified") is False:
        return None
    return email
