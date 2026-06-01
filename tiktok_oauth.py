"""
OAuth TikTok — flux « Login Kit / Display API » (TikTok for Developers).

⚠️ Cible = comptes CRÉATEURS. On utilise donc le Display API (developers.tiktok.com),
pas la Business API ni TikTok Shop Partner. Le Display API expose `video.list` qui
renvoie, par vidéo organique, ses métriques réelles (view_count, like_count,
comment_count, share_count) → corrélation contenu ↔ perfs réelles.

Endpoints (OAuth v2 standard) :
  1. Autorisation  : https://www.tiktok.com/v2/auth/authorize/
       params : client_key, scope, response_type=code, redirect_uri, state
  2. Échange code  : POST https://open.tiktokapis.com/v2/oauth/token/
       form-urlencoded : client_key, client_secret, code, grant_type=authorization_code, redirect_uri
       → réponse PLATE : { access_token, expires_in, refresh_token, refresh_expires_in, open_id, scope }
  3. Refresh       : POST https://open.tiktokapis.com/v2/oauth/token/
       form-urlencoded : client_key, client_secret, grant_type=refresh_token, refresh_token

Flux :
  - L'utilisateur connecté clique « Connecter ma boutique TikTok ».
    → GET /api/auth/tiktok/login renvoie l'URL d'autorisation avec un `state`
      signé (HMAC + expiration 10 min) qui porte l'email (anti-CSRF + retrouve
      le compte au retour).
  - TikTok redirige vers /api/auth/tiktok/callback?code=&state=.
  - On vérifie le state, on échange le code, on sauve le token dans Supabase.

Toutes les clés viennent de l'environnement — JAMAIS de secret en dur.
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

# Réutilise la même clé de signature HMAC que l'auth applicative.
from auth import SECRET_KEY

# ── Configuration (env) ──────────────────────────────────────────────────────
# client_key (= App ID côté TikTok for Business) et secret.
APP_ID = os.getenv("TIKTOK_APP_ID", "")
APP_SECRET = os.getenv("TIKTOK_APP_SECRET", "")

# Scopes par défaut = Display API (créateurs). Modifiable via env sans toucher au code.
DEFAULT_SCOPES = "user.info.basic,user.info.profile,user.info.stats,video.list"
SCOPES = os.getenv("TIKTOK_SCOPES", DEFAULT_SCOPES)

# Endpoints (valeurs par défaut = OAuth v2 Display API / Login Kit).
AUTHORIZE_URL = os.getenv("TIKTOK_AUTHORIZE_URL", "https://www.tiktok.com/v2/auth/authorize/")
TOKEN_URL = os.getenv("TIKTOK_TOKEN_URL", "https://open.tiktokapis.com/v2/oauth/token/")
REFRESH_URL = os.getenv("TIKTOK_REFRESH_URL", "https://open.tiktokapis.com/v2/oauth/token/")

APP_PUBLIC_URL = os.getenv("APP_PUBLIC_URL", "https://tiktokshop-analyzer.com").rstrip("/")
REDIRECT_URI = os.getenv(
    "TIKTOK_REDIRECT_URI", f"{APP_PUBLIC_URL}/api/auth/tiktok/callback"
)

# Durée de validité du paramètre state (anti-CSRF).
_STATE_TTL_SECONDS = 600


def is_configured() -> bool:
    """True si les clés minimales sont présentes (sinon le flux reste inactif)."""
    return bool(APP_ID and APP_SECRET)


# ── State signé (anti-CSRF, porte l'email) ───────────────────────────────────
def make_state(email: str) -> str:
    """Crée un state signé HMAC : base64(email)|ts|nonce.signature (TTL 10 min)."""
    ts = str(int(time.time()))
    nonce = base64.urlsafe_b64encode(os.urandom(9)).decode().rstrip("=")
    email_b64 = base64.urlsafe_b64encode(email.encode()).decode().rstrip("=")
    payload = f"{email_b64}|{ts}|{nonce}"
    sig = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"


def verify_state(state: str) -> Optional[str]:
    """Vérifie la signature + l'expiration du state. Retourne l'email ou None."""
    try:
        payload, sig = state.rsplit(".", 1)
        expected = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        email_b64, ts, _nonce = payload.split("|", 2)
        if int(time.time()) - int(ts) > _STATE_TTL_SECONDS:
            return None
        pad = "=" * (-len(email_b64) % 4)
        return base64.urlsafe_b64decode(email_b64 + pad).decode()
    except Exception:
        return None


# ── URL d'autorisation ───────────────────────────────────────────────────────
def build_authorize_url(state: str) -> str:
    """Construit l'URL d'autorisation « titulaire de compte TikTok »."""
    params = {
        "client_key": APP_ID,
        "scope": SCOPES,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": state,
    }
    return f"{AUTHORIZE_URL}?{urlencode(params)}"


# ── Échange / refresh du token (POST form-urlencoded, réponse plate) ─────────
def _unwrap(body: dict) -> dict:
    """
    Normalise la réponse token. Gère :
      - Display API (réponse PLATE { access_token, ... } ou erreur { error, error_description })
      - Business API (réponse encapsulée { code, message, data:{...} })
    """
    if not isinstance(body, dict):
        return {}
    # Erreur OAuth v2 (Display API)
    err = body.get("error")
    if err and err not in ("", "ok"):
        raise RuntimeError(f"TikTok OAuth error: {body.get('error_description') or err}")
    # Encapsulation Business API
    if "data" in body and isinstance(body["data"], dict) and "access_token" in body["data"]:
        if body.get("code") not in (0, None):
            raise RuntimeError(f"TikTok API error: {body.get('message') or body}")
        return body["data"]
    return body


async def exchange_code_for_token(auth_code: str) -> dict:
    """Échange le code reçu sur le callback contre un access/refresh token."""
    data = {
        "client_key": APP_ID,
        "client_secret": APP_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(TOKEN_URL, data=data, headers=headers)
    resp.raise_for_status()
    result = _unwrap(resp.json())
    # Garde-fou : certaines réponses encapsulent l'erreur dans data.error_code
    # sans access_token → on évite de sauver un token vide silencieusement.
    if not isinstance(result, dict) or not result.get("access_token"):
        raise RuntimeError(f"TikTok token exchange: pas d'access_token (réponse: {result})")
    return result


async def refresh_access_token(refresh_token: str) -> dict:
    """Rafraîchit un access_token expiré via le refresh_token."""
    data = {
        "client_key": APP_ID,
        "client_secret": APP_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(REFRESH_URL, data=data, headers=headers)
    resp.raise_for_status()
    return _unwrap(resp.json())


# ── Persistance Supabase ─────────────────────────────────────────────────────
def save_tiktok_token(email: str, data: dict) -> bool:
    """
    Upsert (par email) le token TikTok dans la table `tiktok_tokens`.
    Best effort : retourne False sans lever si Supabase indispo / erreur.
    """
    try:
        from supabase_client import supabase
    except Exception:
        return False
    if not supabase or not isinstance(data, dict):
        return False

    now = int(time.time())
    access_ttl = data.get("expires_in") or data.get("access_token_expire_in")
    refresh_ttl = (
        data.get("refresh_token_expires_in")
        or data.get("refresh_expires_in")
        or data.get("refresh_token_expire_in")
    )

    row = {
        "email": (email or "").lower(),
        "open_id": data.get("open_id") or data.get("seller_id"),
        "seller_name": data.get("seller_name"),  # null pour le flux créateur
        "region": data.get("seller_base_region") or data.get("region"),
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token"),
        "access_token_expires_at": (now + int(access_ttl)) if access_ttl else None,
        "refresh_token_expires_at": (now + int(refresh_ttl)) if refresh_ttl else None,
        "scope": data.get("scope") or data.get("granted_scopes"),
        "updated_at": now,
    }
    try:
        supabase.table("tiktok_tokens").upsert(row, on_conflict="email").execute()
        return True
    except Exception as e:  # pragma: no cover - best effort
        print(f"tiktok_oauth.save_tiktok_token error: {e}")
        return False
