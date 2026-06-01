from __future__ import annotations
import asyncio
import json
import os
import tempfile
import hashlib
from pathlib import Path
from typing import Optional
from datetime import datetime, date, timedelta, timezone

import httpx
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import time

load_dotenv()

from analyzer import analyze_video, transcribe_audio, analyze_visual, synthesize_analysis, synthesize_batch_patterns
from generate_assets import generate_icons
from security import rate_limit_middleware, security_logger
# 1. Ajout de create_access_token dans l'import
from auth import get_user_from_request, check_quota, increment_usage, usage_info, create_access_token, set_user_tier
from stripe_routes import router as stripe_router
from admin_routes import router as admin_router
from cache_manager import get_cached_analysis, save_to_cache, normalize_tiktok_url
from keyapi_integration import keyapi_client
from insights_store import save_insight, build_winning_payload
import tiktok_oauth

from supabase import create_client, Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# ── STRIPE (paiements automatiques) ───────────────────────────
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
# Mapping price_id Stripe → tier interne (rempli via env Render une fois les prix créés)
STRIPE_PRICE_TO_TIER: dict[str, str] = {
    os.getenv("STRIPE_PRICE_PRO", ""):    "pro",
    os.getenv("STRIPE_PRICE_GOLD", ""):   "gold",
    os.getenv("STRIPE_PRICE_AGENCY", ""): "agency",
}
try:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
except Exception as e:
    print(f"⚠️  Supabase analytics client init failed: {e}")
    supabase_client = None

generate_icons()

app = FastAPI(title="TikTok Shop Analyzer")

# --- PROTECTION ANTI-CRASH : FILE D'ATTENTE GLOBALE ---
ANALYSIS_SEMAPHORE = asyncio.Semaphore(1)

# --- "Aha! Moment" : blindage backend des essais anonymes par IP ---
# Stocke les timestamps des requêtes anonymes par IP (fenêtre glissante 24h).
# 1 essai gratuit + 1 marge d'erreur réseau => on bloque à partir de la 3e requête.
_ANON_IP_USAGE: dict[str, list[float]] = {}
_ANON_WINDOW_SECONDS = 24 * 60 * 60   # 24h
_ANON_MAX_REQUESTS = 2                 # 1 essai + 1 marge

from starlette.middleware.base import BaseHTTPMiddleware
class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next):
        if request.method == 'POST':
            if 'content-length' in request.headers:
                content_length = int(request.headers['content-length'])
                if content_length > self.max_upload_size:
                    return JSONResponse(
                        status_code=413,
                        content={"detail": f"File too large. Max size: {self.max_upload_size/1024/1024:.0f}MB"}
                    )
        return await call_next(request)

app.add_middleware(LimitUploadSize, max_upload_size=100*1024*1024)
app.middleware("http")(rate_limit_middleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(stripe_router)
app.include_router(admin_router)

def _asset_version() -> str:
    try:
        v3 = int(Path("static/app_v3.js").stat().st_mtime)
        v2 = int(Path("static/app_v2.js").stat().st_mtime)
        return str(max(v3, v2))
    except Exception:
        return "1"

_ASSET_V = _asset_version()

def _bust(html: str) -> str:
    import re
    return re.sub(
        r'(/static/[^"\'?\s>]+\.(?:js|css))(?=["\'\s>])',
        lambda m: f"{m.group(1)}?v={_ASSET_V}",
        html,
    )

_HOMEPAGE_HTML = _bust(Path("templates/homepage.html").read_text(encoding="utf-8"))
_APP_HTML = _bust(Path("templates/index.html").read_text(encoding="utf-8"))
_BLOG_HTML = Path("templates/blog.html").read_text(encoding="utf-8")
_BLOG_HISTOIRE_HTML = Path("templates/blog_histoire.html").read_text(encoding="utf-8")
_BLOG_CREATEURS_HTML = Path("templates/blog_createurs.html").read_text(encoding="utf-8")
_BLOG_TENDANCES_HTML = Path("templates/blog_tendances.html").read_text(encoding="utf-8")
_BLOG_GUIDE_HTML = Path("templates/blog_guide.html").read_text(encoding="utf-8")
_CONTACT_HTML = Path("templates/contact.html").read_text(encoding="utf-8")
_ABOUT_HTML = Path("templates/about.html").read_text(encoding="utf-8")
_ANALYTICS_HTML = Path("templates/analytics.html").read_text(encoding="utf-8")
# Pages légales publiques (URLs dédiées exigées par TikTok / RGPD)
_PRIVACY_HTML = Path("templates/privacy.html").read_text(encoding="utf-8")
_TERMS_HTML = Path("templates/terms.html").read_text(encoding="utf-8")
# Back-office admin isolé (vue + JS dédiés, hors espace client)
_DOPE_ADMIN_HTML = _bust(Path("templates/dope_admin.html").read_text(encoding="utf-8"))

# ── CAPTCHA anti-bot (Cloudflare Turnstile) ──────────────────────────────────
# Protège la création de compte (qui déclenche un email) contre le spam de bots.
# Clés lues depuis l'environnement — aucun secret hardcodé. Tant que les clés ne
# sont pas configurées, le CAPTCHA est inactif (l'app fonctionne normalement).
TURNSTILE_SITE_KEY = os.getenv("TURNSTILE_SITE_KEY", "")
TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY", "")


def _inject_turnstile(html: str) -> str:
    """Remplace les marqueurs <!--TURNSTILE_*--> par le widget/script Cloudflare.
    Si aucune clé de site n'est configurée, les marqueurs sont retirés (no-op)."""
    if TURNSTILE_SITE_KEY:
        widget = (
            f'<div class="cf-turnstile" data-sitekey="{TURNSTILE_SITE_KEY}" '
            f'data-theme="auto" style="margin:14px 0;"></div>'
        )
        script = '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>'
    else:
        widget = ""
        script = ""
    return html.replace("<!--TURNSTILE_WIDGET-->", widget).replace("<!--TURNSTILE_SCRIPT-->", script)


_HOMEPAGE_HTML = _inject_turnstile(_HOMEPAGE_HTML)
_APP_HTML = _inject_turnstile(_APP_HTML)


# ── Vérification de propriété de domaine TikTok (URL properties) ─────────────
# TikTok demande de prouver que tu possèdes le domaine. Méthode « balise meta » :
# on insère <meta name="tiktok-developers-site-verification" content="..."> dans
# le <head> de la page d'accueil. Le code de vérification vient de l'env (aucun
# hardcode) → il suffit de définir TIKTOK_SITE_VERIFICATION sur Render.
TIKTOK_SITE_VERIFICATION = os.getenv("TIKTOK_SITE_VERIFICATION", "")


def _inject_tiktok_verification(html: str) -> str:
    if TIKTOK_SITE_VERIFICATION:
        tag = f'<meta name="tiktok-developers-site-verification" content="{TIKTOK_SITE_VERIFICATION}" />'
        return html.replace("</head>", tag + "\n</head>", 1)
    return html


_HOMEPAGE_HTML = _inject_tiktok_verification(_HOMEPAGE_HTML)


async def verify_turnstile(token: str, remote_ip: str = "") -> bool:
    """Vérifie un token Turnstile auprès de Cloudflare.

    - Si TURNSTILE_SECRET_KEY n'est pas configurée → renvoie True (CAPTCHA désactivé).
    - Token manquant alors que le CAPTCHA est actif → False (on bloque).
    - Erreur réseau vers Cloudflare → True (fail-open : on ne bloque pas les
      inscriptions légitimes si Cloudflare est momentanément injoignable).
    """
    if not TURNSTILE_SECRET_KEY:
        return True
    if not token:
        return False
    try:
        data = {"secret": TURNSTILE_SECRET_KEY, "response": token}
        if remote_ip:
            data["remoteip"] = remote_ip
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify", data=data
            )
            return bool(resp.json().get("success"))
    except Exception as e:
        print(f"[turnstile] vérification impossible (fail-open) : {e}")
        return True

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    await track_visitor("/", request)
    return HTMLResponse(_HOMEPAGE_HTML)

@app.get("/app", response_class=HTMLResponse)
async def app_page(request: Request):
    await track_visitor("/app", request)
    return HTMLResponse(_APP_HTML)

@app.get("/confidentialite", response_class=HTMLResponse)
@app.get("/privacy", response_class=HTMLResponse)
async def privacy_page(): return HTMLResponse(_PRIVACY_HTML)

@app.get("/conditions", response_class=HTMLResponse)
@app.get("/terms", response_class=HTMLResponse)
async def terms_page(): return HTMLResponse(_TERMS_HTML)

# ── Fichier de vérification de propriété TikTok (méthode « préfixe d'URL ») ───
# TikTok fournit un fichier de signature à héberger à la racine du domaine. On le
# sert dynamiquement à partir de 2 variables d'env (aucun secret hardcodé, aucun
# redeploy de code nécessaire) :
#   TIKTOK_VERIFY_FILENAME = nom exact du fichier (ex: tiktokXXXXXXXX.txt)
#   TIKTOK_VERIFY_CONTENT  = contenu exact du fichier
_TIKTOK_VERIFY_FILENAME = os.getenv("TIKTOK_VERIFY_FILENAME", "").strip().lstrip("/")
_TIKTOK_VERIFY_CONTENT = os.getenv("TIKTOK_VERIFY_CONTENT", "")
if _TIKTOK_VERIFY_FILENAME and _TIKTOK_VERIFY_CONTENT:
    @app.get("/" + _TIKTOK_VERIFY_FILENAME)
    async def _tiktok_verify_file():
        return Response(content=_TIKTOK_VERIFY_CONTENT, media_type="text/plain")

@app.get("/blog", response_class=HTMLResponse)
async def blog(): return HTMLResponse(_BLOG_HTML)

@app.get("/blog/histoire-tiktok-shop", response_class=HTMLResponse)
async def blog_histoire(): return HTMLResponse(_BLOG_HISTOIRE_HTML)

@app.get("/blog/createurs-millionnaires", response_class=HTMLResponse)
async def blog_createurs(): return HTMLResponse(_BLOG_CREATEURS_HTML)

@app.get("/blog/tendances-2026", response_class=HTMLResponse)
async def blog_tendances(): return HTMLResponse(_BLOG_TENDANCES_HTML)

@app.get("/blog/guide-complet", response_class=HTMLResponse)
async def blog_guide(): return HTMLResponse(_BLOG_GUIDE_HTML)

@app.get("/contact", response_class=HTMLResponse)
async def contact(): return HTMLResponse(_CONTACT_HTML)

@app.get("/about", response_class=HTMLResponse)
async def about(): return HTMLResponse(_ABOUT_HTML)

@app.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    try:
        user = get_user_from_request(request)
        if not user.get("valid") or user.get("tier") != "admin":
            return HTMLResponse("""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><title>Accès Refusé</title></head><body><h1>🔐 Accès Refusé</h1><a href="/app">Retour</a></body></html>""", status_code=403)
        return HTMLResponse(_ANALYTICS_HTML)
    except Exception as e:
        return JSONResponse({"error": f"Internal error: {str(e)}"}, status_code=500)

# ════════════════════════════════════════════════════════════════════════════
# BACK-OFFICE ADMIN ISOLÉ — /dope-admin
# La page elle-même est servie en clair (le navigateur ne peut pas envoyer de
# header Bearer sur une navigation) : la sécurité front est dans dope_admin.html
# (redirection si pas de token / rôle ≠ admin) et la sécurité réelle est sur les
# routes de données /admin/* qui exigent un Bearer admin valide.
# ════════════════════════════════════════════════════════════════════════════
@app.get("/dope-admin", response_class=HTMLResponse)
async def dope_admin():
    return HTMLResponse(_DOPE_ADMIN_HTML)


@app.get("/dope-admin-sw.js")
async def dope_admin_sw():
    """
    Service worker de l'app admin, servi depuis la racine pour avoir un scope
    qui couvre /dope-admin (installable sur l'écran d'accueil du téléphone).
    Volontairement sans cache : un back-office doit toujours afficher des
    données et un code à jour.
    """
    js = (
        "self.addEventListener('install', e => self.skipWaiting());\n"
        "self.addEventListener('activate', e => self.clients.claim());\n"
        "self.addEventListener('fetch', e => { return; });\n"
    )
    return Response(content=js, media_type="application/javascript")


# Comptes internes/bots à exclure des statistiques (configurable via env).
# Par défaut : tous les bots de test sur le domaine @tts-test.com (setup_test_bots.py).
_STATS_EXCLUDED_DOMAINS = [
    d.strip().lower()
    for d in os.getenv("STATS_EXCLUDED_DOMAINS", "tts-test.com").split(",")
    if d.strip()
]
_STATS_EXCLUDED_EMAILS = [
    e.strip().lower()
    for e in os.getenv("STATS_EXCLUDED_EMAILS", "").split(",")
    if e.strip()
]


def _exclude_internal_users(query):
    """Applique les filtres d'exclusion (bots/comptes internes) à une requête users."""
    for domain in _STATS_EXCLUDED_DOMAINS:
        query = query.not_.ilike("email", f"%@{domain}")
    for email in _STATS_EXCLUDED_EMAILS:
        query = query.neq("email", email)
    return query


@app.get("/admin/stats")
async def admin_stats(request: Request):
    """
    KPIs SaaS pour le pilotage : total inscrits, répartition par plan, total
    d'analyses effectuées. Réservé aux admins. Requêtes optimisées : count()
    côté Supabase (head=True) pour ne télécharger aucune ligne sur la table users.
    Les bots de test (@tts-test.com) et comptes internes sont exclus des chiffres.
    """
    user = get_user_from_request(request)
    if not user.get("valid") or not (user.get("is_admin") or user.get("tier") == "admin"):
        raise HTTPException(status_code=403, detail="Accès admin requis.")

    try:
        from supabase_client import supabase, SUPABASE_ENABLED
    except Exception:
        supabase, SUPABASE_ENABLED = None, False

    tiers = ["free", "pro", "gold", "agency", "beta", "admin"]
    by_tier = {t: 0 for t in tiers}
    total_users = 0
    total_analyses = 0
    excluded_count = 0

    if SUPABASE_ENABLED and supabase:
        # IDs des comptes internes/bots — pour les retirer aussi des analyses
        excluded_ids = set()
        try:
            for domain in _STATS_EXCLUDED_DOMAINS:
                rr = supabase.table("users").select("id").ilike("email", f"%@{domain}").execute()
                excluded_ids.update(row["id"] for row in (rr.data or []) if row.get("id"))
            for email in _STATS_EXCLUDED_EMAILS:
                rr = supabase.table("users").select("id").eq("email", email).execute()
                excluded_ids.update(row["id"] for row in (rr.data or []) if row.get("id"))
        except Exception as e:
            print(f"[admin/stats] récupération IDs exclus échouée : {e}")
        excluded_count = len(excluded_ids)

        # Total inscrits — count exact sans rapatrier les lignes (bots exclus)
        try:
            q = _exclude_internal_users(supabase.table("users").select("*", count="exact", head=True))
            total_users = q.execute().count or 0
        except Exception as e:
            print(f"[admin/stats] total users échoué : {e}")

        # Répartition par plan — un count() ciblé par tier (bots exclus)
        for t in tiers:
            try:
                q = _exclude_internal_users(
                    supabase.table("users").select("*", count="exact", head=True).eq("tier", t)
                )
                by_tier[t] = q.execute().count or 0
            except Exception as e:
                print(f"[admin/stats] count tier {t} échoué : {e}")

        # Total analyses = somme des compteurs d'usage (mensuel free/pro + journalier gold/agency),
        # en ignorant les lignes appartenant aux comptes internes/bots.
        for table in ("monthly_usage", "daily_usage"):
            try:
                resp = supabase.table(table).select("count, user_id").execute()
                for row in (resp.data or []):
                    if row.get("user_id") in excluded_ids:
                        continue
                    total_analyses += int(row.get("count") or 0)
            except Exception as e:
                print(f"[admin/stats] somme {table} échouée : {e}")

    return {
        "ok": True,
        "total_users": total_users,
        "by_tier": by_tier,
        "total_analyses": total_analyses,
        "excluded_accounts": excluded_count,
    }


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/user-info")
async def user_info(request: Request):
    user = get_user_from_request(request)
    if not user["valid"]:
        return {"tier": "free", "email": None, "usage": usage_info(user)}
    return {
        "tier": user["tier"],
        "email": user["email"],
        "is_admin": user.get("is_admin", False),
        "usage": usage_info(user),
    }

# 2. MODIFICATION : Génération et distribution du Token sur /register
@app.post("/api/register")
async def register(request: Request):
    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Corps de requête invalide")
        
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Email invalide")

    from auth import _user_tiers, set_user_tier, get_user_tier, create_access_token
    token = create_access_token(email)
    tier = get_user_tier(email)
    
    if tier == "free" and email not in _user_tiers:
        set_user_tier(email, "free")
        return {"ok": True, "email": email, "tier": "free", "created": True, "token": token}

    return {"ok": True, "email": email, "tier": tier, "created": False, "token": token}

# 3. MODIFICATION : Génération et distribution du Token sur /login
@app.post("/api/login")
async def login(request: Request):
    import bcrypt
    from supabase_client import supabase
    from auth import create_access_token

    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
        password = body.get("password", "")

        if not email or "@" not in email:
            raise HTTPException(status_code=400, detail="Email invalide")
        if not password or len(password) < 6:
            raise HTTPException(status_code=400, detail="Mot de passe min 6 caractères")

        if not supabase:
            raise HTTPException(status_code=500, detail="BD non disponible")

        try:
            response = supabase.table("users").select("id, password").eq("email", email).execute()
            response_data = response.data if response else None
        except Exception as e:
            print(f"Supabase select error: {e}")
            response_data = None

        if response_data:
            user = response_data[0]
            stored_hash = user.get("password", "")
            if stored_hash and bcrypt.checkpw(password.encode(), stored_hash.encode()):
                token = create_access_token(email)
                return {"ok": True, "email": email, "message": "Connecté", "token": token}
            else:
                raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
        else:
            # Nouveau compte → cette branche déclenche un email de bienvenue.
            # On exige une vérification anti-bot (Turnstile) AVANT toute création,
            # pour ne pas laisser des bots générer des envois en masse.
            cf_token = body.get("cf_turnstile_token", "") if isinstance(body, dict) else ""
            remote_ip = request.client.host if request.client else ""
            if not await verify_turnstile(cf_token, remote_ip):
                raise HTTPException(status_code=400, detail="Vérification anti-robot échouée. Merci de réessayer.")

            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            try:
                new_user = {"email": email, "tier": "free", "password": password_hash}
                supabase.table("users").insert(new_user).execute()
                token = create_access_token(email)

                # Email de bienvenue (best-effort : un échec ne bloque jamais l'inscription)
                try:
                    from email_service import email_service
                    await email_service.send_welcome_email(email)
                except Exception as mail_err:
                    print(f"[email] bienvenue non envoyé à {email} : {mail_err}")

                return {"ok": True, "email": email, "message": "Compte créé", "created": True, "token": token}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur création compte: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/forgot-password")
async def forgot_password(request: Request):
    import bcrypt
    from supabase_client import supabase
    from password_reset import generate_temporary_password, hash_token, create_password_reset_token, check_rate_limit
    from email_service import email_service

    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
        new_password = body.get("password", "").strip()

        if not email or "@" not in email: raise HTTPException(status_code=400, detail="Email invalide")
        if not new_password or len(new_password) < 6: raise HTTPException(status_code=400, detail="Mot de passe min 6 caractères")

        ip = request.client.host if request.client else "unknown"
        if not check_rate_limit(email, max_attempts=5, window_hours=1):
            security_logger.password_reset_requested(email, ip)
            raise HTTPException(status_code=429, detail="Trop de tentatives.")

        if not supabase: raise HTTPException(status_code=500, detail="BD non disponible")

        try:
            user_exists = supabase.table("users").select("id").eq("email", email).execute()
        except Exception:
            raise HTTPException(status_code=500, detail="Erreur BD")

        if not user_exists.data:
            security_logger.password_reset_requested(email, ip, success=False)
            return {"ok": True, "message": "Email envoyé si le compte existe"}

        password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        success, token_plaintext, token_hash = create_password_reset_token(email, "temporary_password", password_hash)

        if not success: raise HTTPException(status_code=500, detail="Erreur création token")
        email_sent = await email_service.send_temporary_password_email(email, new_password)
        if not email_sent:
            security_logger.password_reset_requested(email, ip, success=False)
            raise HTTPException(status_code=500, detail="Erreur envoi email")

        security_logger.password_reset_requested(email, ip, success=True)
        return {"ok": True, "message": "Email de réinitialisation envoyé"}

    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/change-password")
async def change_password(request: Request):
    import bcrypt
    from supabase_client import supabase
    from password_reset import validate_reset_token, mark_token_as_used
    from email_service import email_service

    try:
        body = await request.json()
        reset_token = body.get("reset_token", "").strip()
        new_password = body.get("new_password", "").strip()
        email = body.get("email", "").lower().strip()

        if not reset_token or not new_password or not email: raise HTTPException(status_code=400, detail="Paramètres manquants")
        if len(new_password) < 6: raise HTTPException(status_code=400, detail="Mot de passe min 6 caractères")

        is_valid, token_data = validate_reset_token(reset_token, email)
        if not is_valid: raise HTTPException(status_code=400, detail="Lien expiré ou invalide")

        password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

        if not supabase: raise HTTPException(status_code=500, detail="BD non disponible")

        try:
            supabase.table("users").update({"password": password_hash}).eq("email", email).execute()
            mark_token_as_used(email, reset_token)
            await email_service.send_password_changed_notification(email)
            security_logger.password_changed_success(email, request.client.host if request.client else "unknown")
            return {"ok": True, "message": "Mot de passe modifié avec succès"}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erreur mise à jour")
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

_SCRAPER_URL = os.getenv("TTS_SCRAPER_URL", "").rstrip("/")

@app.get("/api/market-data")
async def market_data(category: Optional[str] = None):
    if not _SCRAPER_URL:
        return JSONResponse({"ok": False, "error": "TTS_SCRAPER_URL non configuré"}, status_code=503)
    try:
        url = f"{_SCRAPER_URL}/api/coach-context"
        params = {"category": category} if category else {}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
        if resp.is_success: return resp.json()
        return JSONResponse({"ok": False, "error": f"Scraper error {resp.status_code}"}, status_code=502)
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=502)

@app.post("/analyze")
async def analyze_stream_sse(
    request: Request,
    frames: str = Form(...),
    audio: Optional[UploadFile] = File(None),
    product: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
):
    if not os.getenv("MISTRAL_API_KEY"): raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")

    ua = request.headers.get("User-Agent", "").lower()
    if any(w in ua for w in ["scrapy", "spider", "crawler"]):
        ip = request.client.host if request.client else "unknown"
        security_logger.suspicious_agent(ip, ua)

    user = get_user_from_request(request)
    check_quota(user)

    # ── "Aha! Moment" : blindage backend des anonymes ──
    # Utilisateur authentifié (token valide) => limite classique via check_quota (plan Supabase).
    # Utilisateur ANONYME (pas de token) => limite stricte par IP, fenêtre glissante 24h.
    if not user["valid"]:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        timestamps = [t for t in _ANON_IP_USAGE.get(client_ip, []) if now - t < _ANON_WINDOW_SECONDS]
        if len(timestamps) >= _ANON_MAX_REQUESTS:
            _ANON_IP_USAGE[client_ip] = timestamps
            raise HTTPException(status_code=429, detail="Quota anonyme atteint. Créez un compte gratuit.")
        timestamps.append(now)
        _ANON_IP_USAGE[client_ip] = timestamps

    try: frames_list: list[str] = json.loads(frames)
    except json.JSONDecodeError as e: raise HTTPException(status_code=400, detail="Frames JSON invalide.")
    if not frames_list: raise HTTPException(status_code=400, detail="Aucune image extraite de la vidéo.")

    async def stream_analysis():
        loop = asyncio.get_event_loop()
        audio_path: Optional[str] = None
        semaphore_acquired = False
        try:
            yield 'event: start\n'
            yield 'data: {"message": "🎬 Connexion au serveur établie...", "stage": "start"}\n\n'

            if ANALYSIS_SEMAPHORE.locked():
                yield 'event: progress\n'
                yield 'data: {"message": "⏳ Serveur occupé. Placement dans la file d\'attente...", "stage": "queue_waiting"}\n\n'

            await ANALYSIS_SEMAPHORE.acquire()
            semaphore_acquired = True

            yield 'event: progress\n'
            yield 'data: {"message": "🚀 Place libérée ! Initialisation...", "stage": "queue_released"}\n\n'

            if audio:
                yield 'event: progress\n'
                yield 'data: {"message": "📥 Audio en cours de traitement...", "stage": "audio_processing"}\n\n'
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    audio_path = tmp.name
                    tmp.write(await audio.read())

            market_context = None
            tier = user.get("tier", "free")
            if (tier in ("gold", "agency", "beta") or user.get("is_admin")) and _SCRAPER_URL:
                try:
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        mresp = await client.get(f"{_SCRAPER_URL}/api/coach-context")
                    if mresp.is_success: market_context = mresp.json()
                except Exception: pass

            analysis_start = time.time()
            yield 'event: progress\n'
            yield 'data: {"message": "🚀 Lancement analyse parallèle (vision + audio)...", "stage": "parallel_start"}\n\n'

            async def _do_transcribe():
                if not audio_path: return None
                try: return await asyncio.wait_for(loop.run_in_executor(None, transcribe_audio, audio_path), timeout=25.0)
                except asyncio.TimeoutError: return None

            async def _do_visual():
                return await asyncio.wait_for(loop.run_in_executor(None, analyze_visual, frames_list, product, price), timeout=60.0)

            transcript_task = asyncio.create_task(_do_transcribe())
            visual_task = asyncio.create_task(_do_visual())
            yield 'event: progress\n'
            yield 'data: {"message": "🎤 Transcription audio + 👁️ Analyse visuelle en cours...", "stage": "parallel_running"}\n\n'

            transcript, visual_result = await asyncio.gather(transcript_task, visual_task, return_exceptions=True)

            if isinstance(transcript, Exception): transcript = None
            if isinstance(visual_result, Exception):
                yield 'event: error\n'
                yield f'data: {json.dumps({"error": f"Erreur analyse visuelle: {str(visual_result)[:200]}"})}\n\n'
                return

            detected_product = ""
            if isinstance(visual_result, dict): detected_product = str(visual_result.get("produit") or "")[:60]
            vision_msg = f"✅ Vision OK — produit détecté: {detected_product}" if detected_product else "✅ Vision OK"
            yield 'event: progress\n'
            yield f'data: {json.dumps({"message": vision_msg, "stage": "vision_done"})}\n\n'

            if transcript:
                yield 'event: progress\n'
                yield 'data: {"message": "✅ Transcription complète", "stage": "transcription_done"}\n\n'

            yield 'event: progress\n'
            yield 'data: {"message": "🤖 Synthèse finale (scoring + conseils)...", "stage": "synthesis"}\n\n'

            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, synthesize_analysis, visual_result, transcript, market_context, product, tier, price),
                    timeout=90.0
                )
            except asyncio.TimeoutError:
                yield 'event: error\n'
                yield 'data: {"error": "La synthèse a pris trop longtemps."}\n\n'
                return

            analysis_duration_ms = int((time.time() - analysis_start) * 1000)
            yield 'event: progress\n'
            yield f'data: {json.dumps({"message": f"✅ Analyse complète en {analysis_duration_ms/1000:.1f}s", "stage": "ai_analysis_done"})}\n\n'

            if user["valid"]: increment_usage(user["email"])

            result["transcript"] = transcript
            result["frames_analyzed"] = len(frames_list)
            result["usage"] = usage_info(user)
            result["analysis_duration_ms"] = analysis_duration_ms

            video_url_to_cache = request.query_params.get("video_url", f"frames_{len(frames_list)}")
            try: await save_to_cache(video_url_to_cache, result, analysis_duration_ms, product_id=product)
            except Exception: pass

            # Nourrit la base de connaissances (anonymisé) — best effort.
            try: save_insight(result, product=product, price=price)
            except Exception: pass
            # 🏆 Structures gagnantes (Gold/Agency) : si score < 75, propose des
            # accroches/scripts qui ont dépassé 75 sur un produit similaire.
            # Ajouté APRÈS le cache (donnée gated par tier, ne doit pas être cachée).
            try:
                winning = build_winning_payload(result, tier, product=product, price=price)
                if winning: result["structures_gagnantes"] = winning
            except Exception: pass

            ip = request.client.host if request.client else "unknown"
            security_logger.analyze_ok(ip, len(frames_list))

            if supabase_client:
                try:
                    today = date.today().isoformat()
                    existing = supabase_client.table("daily_visitor_stats").select("id,analysis_count").eq("date", today).execute()
                    if existing.data:
                        new_count = (existing.data[0].get("analysis_count") or 0) + 1
                        supabase_client.table("daily_visitor_stats").update({"analysis_count": new_count, "updated_at": datetime.now().isoformat()}).eq("date", today).execute()
                except Exception: pass

            yield 'event: complete\n'
            yield f'data: {json.dumps(result)}\n\n'

        except asyncio.TimeoutError:
            yield 'event: error\n'
            yield 'data: {"error": "L\'analyse a pris trop longtemps."}\n\n'
        except Exception as e:
            yield 'event: error\n'
            yield f'data: {json.dumps({"error": str(e)})}\n\n'
        finally:
            if semaphore_acquired: ANALYSIS_SEMAPHORE.release()
            if audio_path:
                try: os.unlink(audio_path)
                except OSError: pass

    return StreamingResponse(stream_analysis(), media_type="text/event-stream")

@app.get("/api/analyze/stream")
async def analyze_stream(request: Request, video_url: str = Query(...), product: Optional[str] = Query(None)):
    if not os.getenv("MISTRAL_API_KEY"): raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")
    user = get_user_from_request(request)
    check_quota(user)
    try: normalized_url, video_id = normalize_tiktok_url(video_url)
    except Exception: normalized_url = video_url; video_id = "unknown"

    async def stream_generator():
        start_time = time.time()
        try:
            cached_analysis = await get_cached_analysis(normalized_url)
            if cached_analysis:
                yield 'event: start\n'
                yield f'data: {json.dumps({"message": "Analyse trouvée en cache ✨", "source": "cache"})}\n\n'
                sections_to_stream = ['hook_type','retention_type','vente_points','positionnement','format_visuel','emotion','conversion_strategy','algorithme','plan_reproduction','score_global']
                for section_name in sections_to_stream:
                    if section_name in cached_analysis:
                        await asyncio.sleep(0.35)
                        yield 'event: section\n'
                        yield f'data: {json.dumps({"name": section_name, "data": cached_analysis[section_name]})}\n\n'
                yield 'event: complete\n'
                yield f'data: {json.dumps({"message": "Analyse completa ✅", "source": "cache", "duration_ms": cached_analysis.get("analysis_duration_ms", 0)})}\n\n'
                if user["valid"]: increment_usage(user["email"])
            else:
                yield 'event: start\n'
                yield f'data: {json.dumps({"message": "Analyse en cours... 🔄", "source": "live"})}\n\n'
                await asyncio.sleep(0.1)
                yield 'event: error\n'
                yield f'data: {json.dumps({"message": "Mode stream nécessite cache. Utilisez /analyze pour analyses en direct."})}\n\n'
        except Exception as e:
            yield 'event: error\n'
            yield f'data: {json.dumps({"error": str(e)})}\n\n'
    return StreamingResponse(stream_generator(), media_type="text/event-stream")

from keyapi_integration import CATEGORY_ID_MAP as _KEYAPI_CAT_MAP
def _format_price(p: float) -> str: return "—" if not p else f"${p:.2f}" if p < 1000 else f"${p:.0f}"
def _viral_score(p: dict) -> float:
    import math
    views = p.get("views", 0) or 0
    sales = p.get("sales", 0) or 0
    gmv = p.get("gmv", 0) or 0
    score = 0
    if views > 0: score += min(4.0, math.log10(views) - 4)
    if sales > 0: score += min(3.0, math.log10(sales) - 2)
    if gmv > 0: score += min(3.0, math.log10(gmv) - 4)
    return round(max(1.0, min(10.0, score + 5.0)), 1)
def _trend_emoji(sales: int) -> str: return "🚀🚀🚀" if sales > 100000 else "🚀🚀" if sales > 10000 else "🚀" if sales > 1000 else "⬆️"
def _format_followers(n: int) -> str: return f"{n/1_000_000:.1f}M" if n >= 1_000_000 else f"{n/1_000:.0f}K" if n >= 1_000 else str(n)

async def _fetch_market_for_category(category: str) -> dict:
    top_products_raw = await keyapi_client.get_viral_videos(category, page_size=10, sort_field=1)
    trending_raw = await keyapi_client.get_trending_up(category, page_size=10)
    top_products = [{"name": p["title"], "image": p.get("image"), "url": p.get("tiktok_search_url") or p.get("url"), "price": _format_price(p.get("price", 0)), "viral_score": _viral_score(p), "trend": "⬆️ Hausse" if p.get("sales", 0) > 1000 else "→ Stable", "sales": p.get("sales", 0), "gmv": p.get("gmv", 0), "views": p.get("views", 0)} for p in top_products_raw[:5]]
    trending = [{"name": p["title"], "image": p.get("image"), "url": p.get("tiktok_search_url") or p.get("url"), "trend_momentum": _trend_emoji(p.get("sales", 0)), "creator_count": p.get("creators_count", 0), "video_count": p.get("video_count", 0), "price": _format_price(p.get("price", 0))} for p in trending_raw[:5] if p["title"] not in {tp["name"] for tp in top_products}][:5]
    creators_pool = sorted(top_products_raw + trending_raw, key=lambda x: x.get("creators_count", 0), reverse=True)
    seen_ids = set()
    top_creators = []
    for p in creators_pool:
        pid = p.get("id")
        if pid in seen_ids: continue
        seen_ids.add(pid)
        cc = p.get("creators_count", 0)
        if cc <= 0: continue
        top_creators.append({"handle": (p.get("title", "creator")[:25] or "creator").lower().replace(" ", "_"), "product": p.get("title", "")[:60], "image": p.get("image"), "followers_display": _format_followers(cc * 1000), "video_count": p.get("video_count", 0), "url": f"https://www.tiktok.com/search/user?q={(p.get('title') or '').split()[0]}"})
        if len(top_creators) >= 5: break
    return {"top_products": top_products, "trending": trending, "top_creators": top_creators}

@app.get("/api/market-recommendations")
async def market_recommendations(category: Optional[str] = None):
    cat = (category or "").lower().strip()
    if cat not in _KEYAPI_CAT_MAP: cat = "beaute"
    cache_key = f"market_{cat}"
    if supabase_client:
        try:
            cached = supabase_client.table("viral_videos_cache").select("*").eq("category", cache_key).execute()
            if cached.data:
                entry = cached.data[0]
                from datetime import datetime as dt
                expires_at = dt.fromisoformat(entry["expires_at"].replace("Z", "+00:00"))
                if dt.now(expires_at.tzinfo) < expires_at:
                    return {"ok": True, "category": cat, "market_context": entry["videos"], "cached": True}
        except Exception: pass
    try: market_context = await _fetch_market_for_category(cat)
    except Exception as e: return JSONResponse({"ok": False, "error": str(e), "category": cat, "market_context": None}, status_code=502)
    if supabase_client and market_context.get("top_products"):
        try:
            supabase_client.table("viral_videos_cache").upsert({"category": cache_key, "videos": market_context, "cached_at": datetime.now().isoformat(), "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()}, on_conflict="category").execute()
        except Exception: pass
    return {"ok": True, "category": cat, "market_context": market_context, "cached": False}

async def track_visitor(page: str, request: Request, user_email: Optional[str] = None):
    if not supabase_client: return
    try:
        ip = request.client.host if request.client else "unknown"
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]
        ua_hash = hashlib.sha256(request.headers.get("user-agent", "").encode()).hexdigest()[:16]
        today = date.today().isoformat()
        supabase_client.table("visitor_logs").insert({"page": page, "ip_hash": ip_hash, "user_agent_hash": ua_hash, "user_email": user_email, "timestamp": datetime.now().isoformat()}).execute()
        existing = supabase_client.table("daily_visitor_stats").select("id,visitor_count").eq("date", today).execute()
        if existing.data:
            supabase_client.table("daily_visitor_stats").update({"visitor_count": existing.data[0]["visitor_count"] + 1, "updated_at": datetime.now().isoformat()}).eq("date", today).execute()
        else:
            supabase_client.table("daily_visitor_stats").insert({"date": today, "visitor_count": 1, "unique_visitors": 0, "analysis_count": 0}).execute()
    except Exception: pass

@app.get("/api/viral-videos/{category}")
async def get_viral_videos(category: str):
    cat = category.lower()

    # ── 1. Lecture cache Supabase (best-effort : ne doit JAMAIS faire planter la route) ──
    if supabase_client:
        try:
            cached = supabase_client.table("viral_videos_cache").select("*").eq("category", cat).execute()
            if cached.data and cached.data[0] and cached.data[0].get("expires_at"):
                from datetime import datetime as dt
                entry = cached.data[0]
                expires_at = dt.fromisoformat(str(entry["expires_at"]).replace("Z", "+00:00"))
                now = dt.now(expires_at.tzinfo) if expires_at.tzinfo else dt.now()
                if now < expires_at:
                    return {"ok": True, "category": category, "videos": entry.get("videos") or [], "cached": True, "cached_at": entry.get("cached_at")}
        except Exception as e:
            print(f"[viral-videos] lecture cache échouée ({cat}): {e}")

    # ── 2. Appel KeyAPI (source réelle) ──
    try:
        videos = await keyapi_client.get_viral_videos(cat)
    except Exception as e:
        print(f"[viral-videos] KeyAPI échoué ({cat}): {e}")
        return JSONResponse({"ok": False, "category": category, "error": str(e), "videos": []}, status_code=502)

    # ── 3. Écriture cache (best-effort) ──
    if supabase_client and videos:
        try:
            supabase_client.table("viral_videos_cache").upsert(
                {"category": cat, "videos": videos, "cached_at": datetime.now().isoformat(),
                 "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()},
                on_conflict="category",
            ).execute()
        except Exception as e:
            print(f"[viral-videos] écriture cache échouée ({cat}): {e}")

    return {"ok": True, "category": category, "videos": videos or [], "cached": False, "count": len(videos or [])}

CATEGORY_STRATEGIES = {
    "fashion": {"name": "Fashion & Vêtements", "hooks": ["Before/After looks", "Outfit transitions"], "price_positioning": "mid-premium", "conversion_timing": "instant-30d", "viral_multiplier": 1.3, "average_price": "$30-80", "best_creators": "Lifestyle, Fashion", "key_metrics": ["Views"]},
    "beaute": {"name": "Beauté & Cosmétiques", "hooks": ["Makeup tutorials", "Before/After transformation"], "price_positioning": "mid-premium", "conversion_timing": "7-30d", "viral_multiplier": 1.5, "average_price": "$15-50", "best_creators": "Makeup artists", "key_metrics": ["Views"]}
}

@app.get("/api/product-recommendations/{category}")
async def get_product_recommendations(category: str):
    import json
    from pathlib import Path
    category_lower = category.lower()
    strategy = CATEGORY_STRATEGIES.get(category_lower, {"name": category.capitalize(), "hooks": ["Feature highlight"], "price_positioning": "mid", "conversion_timing": "30d", "viral_multiplier": 1.0, "average_price": "variable", "best_creators": "Relevant niche", "key_metrics": ["Views"]})
    videos = await keyapi_client.get_viral_videos(category_lower)
    additional_data = {}
    try:
        db_path = Path("hooks_db.json")
        if db_path.exists():
            db = json.loads(db_path.read_text(encoding="utf-8"))
            product_cat_key = category_lower.replace("-", "_")
            if product_cat_key in db.get("product_categories", {}):
                cat_data = db["product_categories"][product_cat_key]
                additional_data = {"category_names": cat_data.get("names", []), "recommended_hooks_db": cat_data.get("recommended_hooks", []), "price_range": cat_data.get("price_range", "unknown"), "notes": cat_data.get("notes", "")}
    except Exception: pass
    return {"ok": True, "category": category_lower, "strategy": strategy, "recommended_products": videos[:5] if videos else [], "product_count": len(videos) if videos else 0, **additional_data}

# ════════════════════════════════════════════════════════════════════════════
# ANALYSE PAR LIEN TIKTOK (Pro / Gold / Agency uniquement)
# ════════════════════════════════════════════════════════════════════════════
_URL_ANALYSIS_TIERS = {"pro", "gold", "agency", "beta", "admin"}


def _extract_frames_opencv(video_path: str, n_frames: int = 6) -> list[str]:
    """Extrait n_frames réparties sur la durée de la vidéo → liste de base64 JPEG (sans préfixe)."""
    import cv2
    import base64
    cap = cv2.VideoCapture(video_path)
    try:
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames_b64: list[str] = []
        if total <= 0:
            # Fallback : lecture séquentielle si le compteur de frames est indisponible
            ok, frame = cap.read()
            while ok and len(frames_b64) < n_frames:
                success, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if success:
                    frames_b64.append(base64.b64encode(buf).decode("utf-8"))
                ok, frame = cap.read()
            return frames_b64
        # Positions réparties (évite la toute 1ère et la toute dernière frame)
        fractions = [0.05, 0.22, 0.40, 0.58, 0.76, 0.94][:n_frames]
        for f in fractions:
            idx = max(0, min(total - 1, int(total * f)))
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ok, frame = cap.read()
            if not ok:
                continue
            success, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if success:
                frames_b64.append(base64.b64encode(buf).decode("utf-8"))
        return frames_b64
    finally:
        cap.release()


@app.post("/analyze-url")
async def analyze_url(request: Request):
    """
    Analyse une vidéo TikTok à partir de son lien.
    Réservé aux plans Pro / Gold / Agency (et beta/admin).
    Télécharge via yt-dlp → extrait 6 frames (OpenCV) + audio → pipeline Mistral.
    """
    if not os.getenv("MISTRAL_API_KEY"):
        raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")

    # ── SÉCURITÉ : tier requis ──
    user = get_user_from_request(request)
    tier = user.get("tier", "free")
    if not user.get("valid") or tier not in _URL_ANALYSIS_TIERS:
        raise HTTPException(
            status_code=403,
            detail="L'analyse par lien est réservée aux plans Pro, Gold et Agency. Passez au plan Pro (9,99€) pour analyser des liens TikTok directement.",
        )

    # Quota classique selon le plan
    check_quota(user)

    body = await request.json()
    url = (body.get("url") or "").strip()
    product = (body.get("product") or "").strip() or None
    price = (body.get("price") or "").strip() or None
    # Tuyauterie future : stats réelles de la vidéo (ventes/vues) une fois le compte
    # TikTok connecté. None tant que la connexion n'existe pas — passé tel quel au résultat.
    performance = body.get("performance") if isinstance(body.get("performance"), dict) else None
    if not url or not url.lower().startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL TikTok invalide.")

    loop = asyncio.get_event_loop()
    tmpdir = tempfile.mkdtemp(prefix="ttsurl_")
    video_path: Optional[str] = None
    semaphore_acquired = False
    try:
        # ── 1. Téléchargement yt-dlp (dans un thread, bloquant) ──
        def _download() -> str:
            import yt_dlp
            ydl_opts = {
                "outtmpl": os.path.join(tmpdir, "video.%(ext)s"),
                # Privilégie une résolution ≤720p pour limiter la RAM/le temps de décodage
                "format": "best[height<=720][ext=mp4]/best[height<=720]/mp4/best",
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "max_filesize": 80 * 1024 * 1024,  # 80 Mo garde-fou
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        try:
            video_path = await asyncio.wait_for(loop.run_in_executor(None, _download), timeout=60.0)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Le téléchargement de la vidéo a pris trop longtemps.")
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Impossible de récupérer cette vidéo TikTok : {str(e)[:160]}")

        if not video_path or not os.path.exists(video_path):
            raise HTTPException(status_code=422, detail="Vidéo introuvable après téléchargement.")

        # ── 2. Limite de débit serveur (réutilise le sémaphore global anti-crash) ──
        await ANALYSIS_SEMAPHORE.acquire()
        semaphore_acquired = True

        # ── 3. Extraction frames (OpenCV) + transcription, en parallèle ──
        async def _do_frames():
            return await asyncio.wait_for(loop.run_in_executor(None, _extract_frames_opencv, video_path, 6), timeout=45.0)

        async def _do_transcribe():
            try:
                return await asyncio.wait_for(loop.run_in_executor(None, transcribe_audio, video_path), timeout=40.0)
            except asyncio.TimeoutError:
                return None

        frames_list, transcript = await asyncio.gather(_do_frames(), _do_transcribe(), return_exceptions=True)
        if isinstance(transcript, Exception):
            transcript = None
        if isinstance(frames_list, Exception) or not frames_list:
            raise HTTPException(status_code=422, detail="Impossible d'extraire les images de la vidéo.")

        # ── 4. Contexte marché (Gold+) ──
        market_context = None
        if (tier in ("gold", "agency", "beta") or user.get("is_admin")) and _SCRAPER_URL:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    mresp = await client.get(f"{_SCRAPER_URL}/api/coach-context")
                if mresp.is_success:
                    market_context = mresp.json()
            except Exception:
                pass

        # ── 5. Pipeline Mistral : vision → synthèse ──
        analysis_start = time.time()
        visual_result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_visual, frames_list, product, price), timeout=60.0
        )
        result = await asyncio.wait_for(
            loop.run_in_executor(None, synthesize_analysis, visual_result, transcript, market_context, product, tier, price),
            timeout=90.0,
        )
        analysis_duration_ms = int((time.time() - analysis_start) * 1000)

        if user["valid"]:
            increment_usage(user["email"])

        result["transcript"] = transcript
        result["frames_analyzed"] = len(frames_list)
        result["usage"] = usage_info(user)
        result["analysis_duration_ms"] = analysis_duration_ms
        result["source"] = "url"
        result["source_url"] = url
        result["performance"] = performance  # None pour l'instant (futur : stats TikTok)

        # Nourrit la base de connaissances (anonymisé) — best effort.
        try: save_insight(result, product=product, price=price)
        except Exception: pass
        # 🏆 Structures gagnantes (Gold/Agency) si score < 75.
        try:
            winning = build_winning_payload(result, tier, product=product, price=price)
            if winning: result["structures_gagnantes"] = winning
        except Exception: pass

        ip = request.client.host if request.client else "unknown"
        security_logger.analyze_ok(ip, len(frames_list))
        return JSONResponse(result)

    finally:
        # ── PROTECTION SERVEUR : nettoie TOUT, quoi qu'il arrive ──
        if semaphore_acquired:
            ANALYSIS_SEMAPHORE.release()
        try:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
        except Exception:
            pass
        # Rend la mémoire au système entre 2 analyses (évite l'OOM en batch sur Render)
        try:
            import gc
            gc.collect()
        except Exception:
            pass


# ════════════════════════════════════════════════════════════════════════════
# MÉTA-SYNTHÈSE MULTI-VIDÉOS — patterns gagnants / perdants (Gold / Agency)
# ════════════════════════════════════════════════════════════════════════════
_BATCH_PATTERNS_TIERS = {"gold", "agency", "beta", "admin"}


@app.post("/analyze-batch-patterns")
async def analyze_batch_patterns(request: Request):
    """
    Reçoit les N analyses d'un lot multi-liens et fait émerger les patterns
    gagnants/perdants récurrents du créateur. Réservé Gold / Agency (analyse en masse).
    Body : {"analyses": [ {...}, ... ], "performances": [ {...}|null, ... ] }
    """
    if not os.getenv("MISTRAL_API_KEY"):
        raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")

    user = get_user_from_request(request)
    tier = user.get("tier", "free")
    if not user.get("valid") or tier not in _BATCH_PATTERNS_TIERS:
        raise HTTPException(
            status_code=403,
            detail="La détection de patterns multi-vidéos est réservée aux plans Gold et Agency.",
        )

    body = await request.json()
    analyses = body.get("analyses") or []
    performances = body.get("performances") if isinstance(body.get("performances"), list) else None
    if not isinstance(analyses, list) or len(analyses) < 2:
        raise HTTPException(status_code=400, detail="Au moins 2 analyses sont nécessaires pour détecter des patterns.")

    loop = asyncio.get_event_loop()
    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(None, synthesize_batch_patterns, analyses, performances),
            timeout=70.0,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="La synthèse des patterns a pris trop longtemps.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur synthèse patterns : {str(e)[:160]}")

    return JSONResponse(result)


# ════════════════════════════════════════════════════════════════════════════
# STRIPE WEBHOOK — activation automatique des abonnements
# ════════════════════════════════════════════════════════════════════════════
@app.post("/api/v1/stripe/webhook")
async def stripe_webhook_v1(request: Request):
    """
    Reçoit les notifications Stripe et met à jour le tier utilisateur dans Supabase.
    Événement écouté : checkout.session.completed.
    Configure l'URL dans Stripe Dashboard → Webhooks :
      https://<domaine>/api/v1/stripe/webhook
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook Stripe non configuré (STRIPE_WEBHOOK_SECRET manquant).")

    # ── Vérification cryptographique de la signature ──
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError:
        raise HTTPException(status_code=400, detail="Payload invalide.")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Signature webhook invalide.")

    etype = event.get("type", "")
    obj = event.get("data", {}).get("object", {})

    # ── Paiement réussi → activer le plan ──
    if etype == "checkout.session.completed":
        # 1) Email de l'acheteur
        email = (obj.get("customer_details") or {}).get("email") or obj.get("customer_email")
        client_ref = obj.get("client_reference_id")  # peut contenir l'email/ID interne
        if not email and client_ref and "@" in str(client_ref):
            email = client_ref

        cust_id = obj.get("customer")
        sub_id = obj.get("subscription")

        # 2) Identifier le plan : d'abord par price_id, sinon via metadata
        plan = (obj.get("metadata") or {}).get("plan")
        if not plan and sub_id:
            try:
                sub = stripe.Subscription.retrieve(sub_id)
                price_id = sub["items"]["data"][0]["price"]["id"]
                plan = STRIPE_PRICE_TO_TIER.get(price_id)
            except Exception:
                plan = None
        if plan not in ("pro", "gold", "agency"):
            plan = "pro"  # fallback sûr

        # 3) Date de fin d'abonnement (current_period_end)
        expiry = None
        if sub_id:
            try:
                sub = stripe.Subscription.retrieve(sub_id)
                period_end = sub.get("current_period_end")
                if period_end:
                    expiry = datetime.fromtimestamp(period_end, tz=timezone.utc).date().isoformat()
            except Exception:
                pass

        # 4) Mise à jour Supabase
        if email:
            set_user_tier(email.lower().strip(), plan, customer_id=cust_id, subscription_id=sub_id, expiry=expiry)

    # ── Abonnement annulé / expiré → downgrade ──
    elif etype == "customer.subscription.deleted":
        cust_id = obj.get("customer")
        if cust_id:
            from auth import revoke_by_customer
            revoke_by_customer(cust_id)

    return {"received": True}


# ════════════════════════════════════════════════════════════════════════════
# OAUTH TIKTOK SHOP (Partner API) — autorisation marchand
# ════════════════════════════════════════════════════════════════════════════
@app.get("/api/auth/tiktok/login")
async def tiktok_login(request: Request):
    """
    Démarre l'autorisation TikTok Shop pour l'utilisateur connecté.
    Renvoie l'URL d'autorisation (le frontend redirige dessus).
    """
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    if not tiktok_oauth.is_configured():
        raise HTTPException(
            status_code=503,
            detail="Connexion TikTok Shop indisponible (configuration manquante).",
        )
    state = tiktok_oauth.make_state(user["email"])
    return {"authorize_url": tiktok_oauth.build_authorize_url(state)}


@app.get("/api/auth/tiktok/callback")
async def tiktok_callback(
    request: Request,
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
):
    """
    Callback OAuth TikTok Shop : vérifie le state, échange le code contre un token
    et le sauvegarde (rattaché à l'email), puis redirige vers l'app.
    """
    app_url = tiktok_oauth.APP_PUBLIC_URL

    if not code or not state:
        return RedirectResponse(f"{app_url}/app?tiktok=error&reason=missing_params")

    email = tiktok_oauth.verify_state(state)
    if not email:
        return RedirectResponse(f"{app_url}/app?tiktok=error&reason=invalid_state")

    try:
        token_data = await tiktok_oauth.exchange_code_for_token(code)
    except Exception as e:
        print(f"❌ TikTok token exchange failed: {e}")
        return RedirectResponse(f"{app_url}/app?tiktok=error&reason=exchange_failed")

    saved = tiktok_oauth.save_tiktok_token(email, token_data)
    status = "connected" if saved else "warn_not_saved"
    return RedirectResponse(f"{app_url}/app?tiktok={status}")


@app.get("/api/tiktok/me")
async def tiktok_me(request: Request):
    """Profil + vidéos (avec métriques réelles) du compte TikTok connecté."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    try:
        data = await tiktok_oauth.get_profile_and_videos(user["email"])
    except Exception as e:
        print(f"/api/tiktok/me error: {e}")
        data = None
    if not data:
        return {"connected": False}
    return {"connected": True, "profile": data.get("profile") or {}, "videos": data.get("videos") or []}


@app.get("/api/auth/tiktok/status")
async def tiktok_status(request: Request):
    """Indique si l'utilisateur connecté a déjà relié sa boutique TikTok Shop."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    if not supabase_client:
        return {"connected": False}
    try:
        resp = (
            supabase_client.table("tiktok_tokens")
            .select("seller_name,open_id,access_token_expires_at")
            .eq("email", user["email"])
            .execute()
        )
        if resp.data:
            row = resp.data[0]
            return {
                "connected": bool(row.get("access_token_expires_at")),
                "seller_name": row.get("seller_name"),
            }
    except Exception:
        pass
    return {"connected": False}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
