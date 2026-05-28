from __future__ import annotations
import asyncio
import json
import os
import tempfile
import hashlib
from pathlib import Path
from typing import Optional
from datetime import datetime, date, timedelta

import httpx
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import time

load_dotenv()

from analyzer import analyze_video, transcribe_audio, analyze_visual, synthesize_analysis
from generate_assets import generate_icons
from security import rate_limit_middleware, security_logger
from auth import get_user_from_request, check_quota, increment_usage, usage_info
from stripe_routes import router as stripe_router
from admin_routes import router as admin_router
from cache_manager import get_cached_analysis, save_to_cache, normalize_tiktok_url
from keyapi_integration import keyapi_client

# Import Supabase for analytics
from supabase import create_client, Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
try:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
except Exception as e:
    print(f"⚠️  Supabase analytics client init failed: {e}")
    supabase_client = None

generate_icons()

app = FastAPI(title="TikTok Shop Analyzer")

# --- PROTECTION ANTI-CRASH : FILE D'ATTENTE GLOBALE ---
# Limite le traitement lourd à 1 seule vidéo à la fois sur l'instance Render
ANALYSIS_SEMAPHORE = asyncio.Semaphore(1)

# Configure max file upload size (100MB for video + audio)
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

app.add_middleware(LimitUploadSize, max_upload_size=100*1024*1024)  # 100MB
app.middleware("http")(rate_limit_middleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(stripe_router)   # /create-checkout-session  /customer-portal  /webhook
app.include_router(admin_router)    # /admin/users  /admin/set-tier  /admin/grant-beta

# Cache-busting: version basée sur mtime des fichiers JS (bump auto à chaque deploy)
def _asset_version() -> str:
    try:
        v3 = int(Path("static/app_v3.js").stat().st_mtime)
        v2 = int(Path("static/app_v2.js").stat().st_mtime)
        return str(max(v3, v2))
    except Exception:
        return "1"

_ASSET_V = _asset_version()

def _bust(html: str) -> str:
    """Append ?v=... to local /static/ JS & CSS URLs to bust mobile browser caches."""
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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Landing page avec tool d'analyse intégré."""
    await track_visitor("/", request)
    return HTMLResponse(_HOMEPAGE_HTML)


@app.get("/app", response_class=HTMLResponse)
async def app_page(request: Request):
    """Page d'analyse complète."""
    await track_visitor("/app", request)
    return HTMLResponse(_APP_HTML)


@app.get("/blog", response_class=HTMLResponse)
async def blog():
    """Page d'accueil du blog."""
    return HTMLResponse(_BLOG_HTML)


@app.get("/blog/histoire-tiktok-shop", response_class=HTMLResponse)
async def blog_histoire():
    """Article : Histoire de TikTok Shop."""
    return HTMLResponse(_BLOG_HISTOIRE_HTML)


@app.get("/blog/createurs-millionnaires", response_class=HTMLResponse)
async def blog_createurs():
    """Article : Créateurs millionnaires."""
    return HTMLResponse(_BLOG_CREATEURS_HTML)


@app.get("/blog/tendances-2026", response_class=HTMLResponse)
async def blog_tendances():
    """Article : Tendances 2026."""
    return HTMLResponse(_BLOG_TENDANCES_HTML)


@app.get("/blog/guide-complet", response_class=HTMLResponse)
async def blog_guide():
    """Article : Guide complet."""
    return HTMLResponse(_BLOG_GUIDE_HTML)


@app.get("/contact", response_class=HTMLResponse)
async def contact():
    """Page de contact."""
    return HTMLResponse(_CONTACT_HTML)


@app.get("/about", response_class=HTMLResponse)
async def about():
    """Page à propos."""
    return HTMLResponse(_ABOUT_HTML)


@app.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    """Analytics dashboard - ADMIN ONLY."""
    try:
        user = get_user_from_request(request)
        if not user.get("valid") or user.get("tier") != "admin":
            return HTMLResponse("""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Analytics - Accès Refusé</title><style>
body { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif; background: linear-gradient(135deg, #F5F7FA 0%, #EEF0F6 100%); display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; margin: 0; }
.container { background: white; border-radius: 12px; padding: 40px; text-align: center; max-width: 400px; box-shadow: 0 4px 20px rgba(0,0,0,0.07); }
h1 { font-size: 24px; margin-bottom: 12px; color: #1F3A70; }
p { font-size: 14px; color: #6B7280; margin-bottom: 24px; line-height: 1.6; }
a { display: inline-block; background: linear-gradient(135deg, #1F3A70, #2563EB); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 14px; }
</style></head><body><div class="container"><h1>🔐 Accès Refusé</h1><p>Le dashboard analytics est réservé aux administrateurs.</p><p>Connecte-toi avec un compte admin pour accéder à ce dashboard.</p><a href="/app">← Retour à l'app</a></div></body></html>""", status_code=403)

        return HTMLResponse(_ANALYTICS_HTML)
    except Exception as e:
        return JSONResponse({"error": f"Internal error: {str(e)}"}, status_code=500)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/user-info")
async def user_info(request: Request):
    """Retourne les infos de l'utilisateur connecté (tier, usage, etc)."""
    user = get_user_from_request(request)
    if not user["valid"]:
        return {"tier": "free", "email": None, "usage": usage_info(user)}
    return {
        "tier": user["tier"],
        "email": user["email"],
        "is_admin": user.get("is_admin", False),
        "usage": usage_info(user),
    }


@app.post("/api/register")
async def register(request: Request):
    """Enregistre automatiquement un nouvel utilisateur comme FREE si pas déjà existant."""
    user = get_user_from_request(request)
    if not user["valid"]:
        raise HTTPException(status_code=401, detail="Authentification requise.")

    email = user["email"]
    # Si l'utilisateur n'existe pas, le créer en FREE
    from auth import _user_tiers
    if email not in _user_tiers:
        from auth import set_user_tier
        set_user_tier(email, "free")
        return {"ok": True, "email": email, "tier": "free", "created": True}

    # Utilisateur existe déjà
    return {"ok": True, "email": email, "tier": user["tier"], "created": False}


@app.post("/api/login")
async def login(request: Request):
    """Login/Register avec email + password."""
    import bcrypt
    from supabase_client import supabase

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

        # Chercher l'utilisateur
        try:
            response = supabase.table("users").select("id, password").eq("email", email).execute()
            response_data = response.data if response else None
        except Exception as e:
            print(f"Supabase select error: {e}")
            response_data = None

        if response_data:
            # Utilisateur existe - vérifier mot de passe
            user = response_data[0]
            stored_hash = user.get("password", "")

            if stored_hash and bcrypt.checkpw(password.encode(), stored_hash.encode()):
                # Mot de passe correct
                return {"ok": True, "email": email, "message": "Connecté"}
            else:
                raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
        else:
            # Nouvel utilisateur - créer avec mot de passe
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            try:
                new_user = {
                    "email": email,
                    "tier": "free",
                    "password": password_hash,
                }
                supabase.table("users").insert(new_user).execute()
                return {"ok": True, "email": email, "message": "Compte créé", "created": True}
            except Exception as e:
                print(f"Supabase insert error: {e}")
                raise HTTPException(status_code=500, detail=f"Erreur création compte: {str(e)}")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── PASSWORD RESET ENDPOINTS ──────────────────────────────────
@app.post("/api/forgot-password")
async def forgot_password(request: Request):
    """User forgot password - send temporary password by email."""
    import bcrypt
    from supabase_client import supabase
    from password_reset import (
        generate_temporary_password,
        hash_token,
        create_password_reset_token,
        check_rate_limit,
    )
    from email_service import email_service

    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
        new_password = body.get("password", "").strip()

        # Validation
        if not email or "@" not in email:
            raise HTTPException(status_code=400, detail="Email invalide")
        if not new_password or len(new_password) < 6:
            raise HTTPException(status_code=400, detail="Mot de passe min 6 caractères")

        # Rate limiting (max 5 attempts per hour)
        ip = request.client.host if request.client else "unknown"
        if not check_rate_limit(email, max_attempts=5, window_hours=1):
            security_logger.password_reset_requested(email, ip)
            raise HTTPException(status_code=429, detail="Trop de tentatives. Réessayez plus tard.")

        # Check if user exists (don't reveal if email exists for security)
        if not supabase:
            raise HTTPException(status_code=500, detail="BD non disponible")

        try:
            user_exists = supabase.table("users").select("id").eq("email", email).execute()
        except Exception:
            raise HTTPException(status_code=500, detail="Erreur BD")

        if not user_exists.data:
            # Don't reveal non-existent emails (security best practice)
            security_logger.password_reset_requested(email, ip, success=False)
            return {"ok": True, "message": "Email de réinitialisation envoyé si le compte existe"}

        # Hash new password
        password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

        # Create reset token (type = temporary_password)
        success, token_plaintext, token_hash = create_password_reset_token(
            email, "temporary_password", password_hash
        )

        if not success:
            raise HTTPException(status_code=500, detail="Erreur création token")

        # Send email with temporary password
        email_sent = await email_service.send_temporary_password_email(email, new_password)

        if not email_sent:
            security_logger.password_reset_requested(email, ip, success=False)
            raise HTTPException(status_code=500, detail="Erreur envoi email")

        security_logger.password_reset_requested(email, ip, success=True)
        return {"ok": True, "message": "Email de réinitialisation envoyé"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Forgot password error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/change-password")
async def change_password(request: Request):
    """Change password using reset token or after forgot password."""
    import bcrypt
    from supabase_client import supabase
    from password_reset import validate_reset_token, mark_token_as_used
    from email_service import email_service

    try:
        body = await request.json()
        reset_token = body.get("reset_token", "").strip()
        new_password = body.get("new_password", "").strip()
        email = body.get("email", "").lower().strip()

        # Validation
        if not reset_token or not new_password or not email:
            raise HTTPException(status_code=400, detail="Paramètres manquants")
        if len(new_password) < 6:
            raise HTTPException(status_code=400, detail="Mot de passe min 6 caractères")

        # Validate token
        is_valid, token_data = validate_reset_token(reset_token, email)
        if not is_valid:
            raise HTTPException(status_code=400, detail="Lien expiré ou invalide")

        # Hash new password
        password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

        if not supabase:
            raise HTTPException(status_code=500, detail="BD non disponible")

        try:
            # Update user password
            supabase.table("users").update({"password": password_hash}).eq("email", email).execute()

            # Mark token as used
            mark_token_as_used(email, reset_token)

            # Send confirmation email
            await email_service.send_password_changed_notification(email)

            security_logger.password_changed_success(email, request.client.host if request.client else "unknown")
            return {"ok": True, "message": "Mot de passe modifié avec succès"}

        except Exception as e:
            print(f"Error updating password: {e}")
            raise HTTPException(status_code=500, detail="Erreur mise à jour mot de passe")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Change password error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Market data proxy (depuis tts-scraper API) ────────────────
_SCRAPER_URL = os.getenv("TTS_SCRAPER_URL", "").rstrip("/")

@app.get("/api/market-data")
async def market_data(category: Optional[str] = None):
    """Proxy vers l'API TTS Scraper — retourne top produits + trending + créateurs."""
    if not _SCRAPER_URL:
        return JSONResponse({"ok": False, "error": "TTS_SCRAPER_URL non configuré"}, status_code=503)
    try:
        url = f"{_SCRAPER_URL}/api/coach-context"
        params = {"category": category} if category else {}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
        if resp.is_success:
            return resp.json()
        return JSONResponse({"ok": False, "error": f"Scraper error {resp.status_code}"}, status_code=502)
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=502)


@app.post("/analyze")
async def analyze_stream_sse(
    request: Request,
    frames: str = Form(...),
    audio: Optional[UploadFile] = File(None),
    product: Optional[str] = Form(None),
):
    """
    Analyse vidéo avec streaming Server-Sent Events (SSE).
    Les diagnostics s'affichent au fur et à mesure (vs. tout à la fin).
    """
    if not os.getenv("MISTRAL_API_KEY"):
        raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")

    ua = request.headers.get("User-Agent", "").lower()
    if any(w in ua for w in ["scrapy", "spider", "crawler"]):
        ip = request.client.host if request.client else "unknown"
        security_logger.suspicious_agent(ip, ua)

    user = get_user_from_request(request)
    check_quota(user)

    try:
        frames_list: list[str] = json.loads(frames)
    except json.JSONDecodeError as e:
        print(f"[/analyze] Bad frames JSON: {e} | preview={frames[:200] if frames else 'EMPTY'}")
        raise HTTPException(status_code=400, detail="Frames JSON invalide. Réessaie de sélectionner la vidéo.")
    if not frames_list:
        print(f"[/analyze] Empty frames list from {request.client.host if request.client else '?'}")
        raise HTTPException(status_code=400, detail="Aucune image extraite de la vidéo. Vérifie que la vidéo est valide (mp4, mov) et réessaie.")
    if not isinstance(frames_list, list) or not all(isinstance(f, str) for f in frames_list):
        raise HTTPException(status_code=400, detail="Format frames invalide.")
    print(f"[/analyze] OK frames={len(frames_list)} audio={'yes' if audio else 'no'} product={product or 'auto'}")

    async def stream_analysis():
        """Stream analysis progress as it happens with queue management."""
        loop = asyncio.get_event_loop()
        audio_path: Optional[str] = None
        semaphore_acquired = False

        try:
            # Send start event
            yield 'event: start\n'
            yield 'data: {"message": "🎬 Connexion au serveur établie...", "stage": "start"}\n\n'

            # Vérification immédiate si le serveur est occupé
            if ANALYSIS_SEMAPHORE.locked():
                yield 'event: progress\n'
                yield 'data: {"message": "⏳ Serveur occupé. Placement dans la file d\'attente...", "stage": "queue_waiting"}\n\n'

            # L'utilisateur attend ici que la place se libère
            await ANALYSIS_SEMAPHORE.acquire()
            semaphore_acquired = True

            yield 'event: progress\n'
            yield 'data: {"message": "🚀 Place libérée ! Initialisation de l\'analyse...", "stage": "queue_released"}\n\n'

            # Save audio to temp file if provided
            if audio:
                yield 'event: progress\n'
                yield 'data: {"message": "📥 Audio en cours de traitement...", "stage": "audio_processing"}\n\n'
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    audio_path = tmp.name
                    tmp.write(await audio.read())

            # Market context (rapide, en async direct)
            market_context: Optional[dict] = None
            tier = user.get("tier", "free")
            is_admin = user.get("is_admin", False)
            if (tier in ("gold", "agency", "beta") or is_admin) and _SCRAPER_URL:
                try:
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        mresp = await client.get(f"{_SCRAPER_URL}/api/coach-context")
                    if mresp.is_success:
                        market_context = mresp.json()
                except Exception:
                    pass

            # ─────────────────────────────────────────────────────────────
            # ⚡ PIPELINE PARALLÈLE :
            #   - Transcription audio (5-15s)        ┐
            #   - Vision Mistral Pixtral (10-15s)    ┘─ EN PARALLÈLE via asyncio.gather
            # Puis synthèse Mistral-small (5-10s, text-only)
            # Total ~20-30s au lieu de 50-90s
            # ─────────────────────────────────────────────────────────────
            analysis_start = time.time()

            yield 'event: progress\n'
            yield 'data: {"message": "🚀 Lancement analyse parallèle (vision + audio)...", "stage": "parallel_start"}\n\n'

            async def _do_transcribe():
                if not audio_path:
                    return None
                try:
                    return await asyncio.wait_for(
                        loop.run_in_executor(None, transcribe_audio, audio_path),
                        timeout=25.0,
                    )
                except asyncio.TimeoutError:
                    return None

            async def _do_visual():
                return await asyncio.wait_for(
                    loop.run_in_executor(None, analyze_visual, frames_list, product),
                    timeout=60.0,
                )

            # Lancer en parallèle
            transcript_task = asyncio.create_task(_do_transcribe())
            visual_task = asyncio.create_task(_do_visual())

            # Streaming progress en attendant
            yield 'event: progress\n'
            yield 'data: {"message": "🎤 Transcription audio + 👁️ Analyse visuelle en cours...", "stage": "parallel_running"}\n\n'

            # Attendre les deux
            transcript, visual_result = await asyncio.gather(
                transcript_task, visual_task, return_exceptions=True
            )

            # Gérer les exceptions
            if isinstance(transcript, Exception):
                print(f"⚠️ Transcript error: {transcript}")
                transcript = None
            if isinstance(visual_result, Exception):
                print(f"❌ Visual error: {visual_result}")
                yield 'event: error\n'
                yield f'data: {json.dumps({"error": f"Erreur analyse visuelle: {str(visual_result)[:200]}"})}\n\n'
                return

            detected_product = ""
            if isinstance(visual_result, dict):
                detected_product = str(visual_result.get("produit") or "")[:60]
            vision_msg = f"✅ Vision OK — produit détecté: {detected_product}" if detected_product else "✅ Vision OK"
            yield 'event: progress\n'
            yield f'data: {json.dumps({"message": vision_msg, "stage": "vision_done"})}\n\n'

            if transcript:
                yield 'event: progress\n'
                yield 'data: {"message": "✅ Transcription complète", "stage": "transcription_done"}\n\n'

            # Synthèse texte (rapide car pas de vision)
            yield 'event: progress\n'
            yield 'data: {"message": "🤖 Synthèse finale (scoring + conseils)...", "stage": "synthesis"}\n\n'

            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(
                        None, synthesize_analysis, visual_result, transcript, market_context, product
                    ),
                    timeout=90.0,
                )
            except asyncio.TimeoutError:
                yield 'event: error\n'
                yield 'data: {"error": "La synthèse a pris trop longtemps. Réessaie avec une vidéo plus courte."}\n\n'
                return

            analysis_duration_ms = int((time.time() - analysis_start) * 1000)

            yield 'event: progress\n'
            yield f'data: {json.dumps({"message": f"✅ Analyse complète en {analysis_duration_ms/1000:.1f}s", "stage": "ai_analysis_done"})}\n\n'

            if user["valid"]:
                increment_usage(user["email"])

            result["transcript"]      = transcript
            result["frames_analyzed"] = len(frames_list)
            result["usage"]           = usage_info(user)
            result["analysis_duration_ms"] = analysis_duration_ms

            # Save to cache
            video_url_to_cache = request.query_params.get("video_url", f"frames_{len(frames_list)}")
            try:
                await save_to_cache(
                    video_url_to_cache,
                    result,
                    analysis_duration_ms,
                    product_id=product
                )
            except Exception as e:
                security_logger.analyze_error(request.client.host if request.client else "unknown", f"Cache save error: {e}")

            ip = request.client.host if request.client else "unknown"
            security_logger.analyze_ok(ip, len(frames_list))

            # Analytics
            if supabase_client:
                try:
                    today = date.today().isoformat()
                    existing = supabase_client.table("daily_visitor_stats").select("id,analysis_count").eq("date", today).execute()
                    if existing.data:
                        new_count = (existing.data[0].get("analysis_count") or 0) + 1
                        supabase_client.table("daily_visitor_stats").update({
                            "analysis_count": new_count,
                            "updated_at": datetime.now().isoformat()
                        }).eq("date", today).execute()
                except Exception:
                    pass

            # Send complete result
            yield 'event: complete\n'
            yield f'data: {json.dumps(result)}\n\n'

        except asyncio.TimeoutError:
            yield 'event: error\n'
            yield 'data: {"error": "L\'analyse a pris trop longtemps (>3min). Essaie avec une vidéo plus courte."}\n\n'
        except Exception as e:
            ip = request.client.host if request.client else "unknown"
            security_logger.analyze_error(ip, str(e))
            yield 'event: error\n'
            yield f'data: {json.dumps({"error": str(e)})}\n\n'
        finally:
            if semaphore_acquired:
                ANALYSIS_SEMAPHORE.release()
            if audio_path:
                try:
                    os.unlink(audio_path)
                except OSError:
                    pass

    return StreamingResponse(stream_analysis(), media_type="text/event-stream")


# ── STREAMING ANALYSIS ENDPOINT (SSE) ─────────────────────────────────────────
@app.get("/api/analyze/stream")
async def analyze_stream(
    request: Request,
    video_url: str = Query(...),
    product: Optional[str] = Query(None),
):
    """
    Stream analysis results progressively using Server-Sent Events (SSE).
    If result is cached: stream sections with visual delays (~300-500ms each).
    If cache miss: stream real-time analysis as Mistral processes the video.
    Query params:
    - video_url: TikTok URL to analyze
    - product: (optional) Product name hint for analysis
    """
    if not os.getenv("MISTRAL_API_KEY"):
        raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")

    user = get_user_from_request(request)
    check_quota(user)

    # Normalize URL for consistent caching
    try:
        normalized_url, video_id = normalize_tiktok_url(video_url)
    except Exception:
        normalized_url = video_url
        video_id = "unknown"

    async def stream_generator():
        """Generate SSE stream of analysis sections."""
        start_time = time.time()

        try:
            # Check cache first
            cached_analysis = await get_cached_analysis(normalized_url)

            if cached_analysis:
                # CACHE HIT: Stream from cache with visual delays
                yield 'event: start\n'
                yield f'data: {json.dumps({"message": "Analyse trouvée en cache ✨", "source": "cache"})}\n\n'

                # Stream each section with visual delay for perception of speed
                sections_to_stream = [
                    'hook_type',
                    'retention_type',
                    'vente_points',
                    'positionnement',
                    'format_visuel',
                    'emotion',
                    'conversion_strategy',
                    'algorithme',
                    'plan_reproduction',
                    'score_global'
                ]

                for section_name in sections_to_stream:
                    if section_name in cached_analysis:
                        await asyncio.sleep(0.35)  # Visual delay ~350ms per section
                        yield 'event: section\n'
                        yield f'data: {json.dumps({"name": section_name, "data": cached_analysis[section_name]})}\n\n'

                yield 'event: complete\n'
                yield f'data: {json.dumps({"message": "Analyse completa ✅", "source": "cache", "duration_ms": cached_analysis.get("analysis_duration_ms", 0)})}\n\n'

                if user["valid"]:
                    increment_usage(user["email"])

            else:
                # CACHE MISS: Stream real-time analysis
                yield 'event: start\n'
                yield f'data: {json.dumps({"message": "Analyse en cours... 🔄", "source": "live"})}\n\n'

                # Signal that we're doing real-time analysis (this will take longer)
                # The frontend can show a "downloading" state
                await asyncio.sleep(0.1)

                # For now, fall back to requesting full analysis via HTTP
                # In a future optimization, we could stream Mistral's response directly
                # but that would require significant refactoring of the analyze_video function

                yield 'event: error\n'
                yield f'data: {json.dumps({"message": "Mode stream nécessite cache. Utilisez /analyze pour analyses en direct."})}\n\n'

        except Exception as e:
            yield 'event: error\n'
            yield f'data: {json.dumps({"error": str(e)})}\n\n'

    return StreamingResponse(stream_generator(), media_type="text/event-stream")


# ── MARKET RECOMMENDATIONS (KeyAPI réel, filtré par catégorie) ────────────────
from keyapi_integration import CATEGORY_ID_MAP as _KEYAPI_CAT_MAP


def _format_price(p: float) -> str:
    if not p:
        return "—"
    return f"${p:.2f}" if p < 1000 else f"${p:.0f}"


def _viral_score(p: dict) -> float:
    """Score 0-10 basé sur views + sales + GMV (échelle log)."""
    import math
    views = p.get("views", 0) or 0
    sales = p.get("sales", 0) or 0
    gmv = p.get("gmv", 0) or 0
    score = 0
    if views > 0:
        score += min(4.0, math.log10(views) - 4)  # 100K→0, 1M→2, 100M→4
    if sales > 0:
        score += min(3.0, math.log10(sales) - 2)  # 100→0, 10K→2, 1M→4
    if gmv > 0:
        score += min(3.0, math.log10(gmv) - 4)
    return round(max(1.0, min(10.0, score + 5.0)), 1)


def _trend_emoji(sales: int) -> str:
    if sales > 100000:
        return "🚀🚀🚀"
    if sales > 10000:
        return "🚀🚀"
    if sales > 1000:
        return "🚀"
    return "⬆️"


def _format_followers(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(n)


async def _fetch_market_for_category(category: str) -> dict:
    """Construit market_context réel depuis KeyAPI pour une catégorie."""
    # Top produits (par ventes totales)
    top_products_raw = await keyapi_client.get_viral_videos(
        category, page_size=10, sort_field=1  # total_sale_cnt
    )
    # Tendances haussières
    trending_raw = await keyapi_client.get_trending_up(category, page_size=10)

    top_products = [
        {
            "name": p["title"],
            "image": p.get("image"),
            "url": p.get("tiktok_search_url") or p.get("url"),
            "price": _format_price(p.get("price", 0)),
            "viral_score": _viral_score(p),
            "trend": "⬆️ Hausse" if p.get("sales", 0) > 1000 else "→ Stable",
            "sales": p.get("sales", 0),
            "gmv": p.get("gmv", 0),
            "views": p.get("views", 0),
        }
        for p in top_products_raw[:5]
    ]

    trending = [
        {
            "name": p["title"],
            "image": p.get("image"),
            "url": p.get("tiktok_search_url") or p.get("url"),
            "trend_momentum": _trend_emoji(p.get("sales", 0)),
            "creator_count": p.get("creators_count", 0),
            "video_count": p.get("video_count", 0),
            "price": _format_price(p.get("price", 0)),
        }
        for p in trending_raw[:5]
        if p["title"] not in {tp["name"] for tp in top_products}
    ][:5]

    # Top créateurs synthétisés depuis produits (les produits avec le plus de créateurs)
    creators_pool = sorted(
        top_products_raw + trending_raw,
        key=lambda x: x.get("creators_count", 0),
        reverse=True,
    )
    seen_ids = set()
    top_creators = []
    for p in creators_pool:
        pid = p.get("id")
        if pid in seen_ids:
            continue
        seen_ids.add(pid)
        cc = p.get("creators_count", 0)
        if cc <= 0:
            continue
        top_creators.append({
            "handle": (p.get("title", "creator")[:25] or "creator").lower().replace(" ", "_"),
            "product": p.get("title", "")[:60],
            "image": p.get("image"),
            "followers_display": _format_followers(cc * 1000),  # estimation
            "video_count": p.get("video_count", 0),
            "url": f"https://www.tiktok.com/search/user?q={(p.get('title') or '').split()[0]}",
        })
        if len(top_creators) >= 5:
            break

    return {
        "top_products": top_products,
        "trending": trending,
        "top_creators": top_creators,
    }


@app.get("/api/market-recommendations")
async def market_recommendations(category: Optional[str] = None):
    """
    Retourne données marché TikTok Shop RÉELLES depuis KeyAPI.
    - Si `category` fournie : filtre par catégorie de l'analyse
    - Sinon : utilise 'beaute' par défaut (la catégorie la plus active)
    Cache 24h par catégorie dans Supabase (table viral_videos_cache).
    """
    cat = (category or "").lower().strip()
    if cat not in _KEYAPI_CAT_MAP:
        cat = "beaute"  # défaut

    cache_key = f"market_{cat}"

    # 1. Tenter cache 24h
    if supabase_client:
        try:
            cached = supabase_client.table("viral_videos_cache").select("*").eq(
                "category", cache_key
            ).execute()
            if cached.data:
                entry = cached.data[0]
                from datetime import datetime as dt
                expires_at = dt.fromisoformat(entry["expires_at"].replace("Z", "+00:00"))
                if dt.now(expires_at.tzinfo) < expires_at:
                    return {
                        "ok": True,
                        "category": cat,
                        "market_context": entry["videos"],
                        "cached": True,
                    }
        except Exception as e:
            print(f"⚠️  Market cache read error: {e}")

    # 2. Fetch KeyAPI réel
    try:
        market_context = await _fetch_market_for_category(cat)
    except Exception as e:
        print(f"❌ Market fetch error: {e}")
        return JSONResponse(
            {"ok": False, "error": str(e), "category": cat, "market_context": None},
            status_code=502,
        )

    # 3. Cache 24h
    if supabase_client and market_context.get("top_products"):
        try:
            supabase_client.table("viral_videos_cache").upsert({
                "category": cache_key,
                "videos": market_context,
                "cached_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            }, on_conflict="category").execute()
        except Exception as e:
            print(f"⚠️  Market cache write error: {e}")

    return {
        "ok": True,
        "category": cat,
        "market_context": market_context,
        "cached": False,
    }




# ════════════════════════════════════════════════════════════════════════════
# ANALYTICS ENDPOINTS
# ════════════════════════════════════════════════════════════════════════════

async def track_visitor(page: str, request: Request, user_email: Optional[str] = None):
    """Track visitor to analytics database."""
    if not supabase_client:
        return

    try:
        # Get IP hash (starlette Address uses .host, not .ip)
        ip = request.client.host if request.client else "unknown"
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]

        # Get user agent hash
        user_agent = request.headers.get("user-agent", "")
        ua_hash = hashlib.sha256(user_agent.encode()).hexdigest()[:16]

        today = date.today().isoformat()

        # Log individual visit
        supabase_client.table("visitor_logs").insert({
            "page": page,
            "ip_hash": ip_hash,
            "user_agent_hash": ua_hash,
            "user_email": user_email,
            "timestamp": datetime.now().isoformat()
        }).execute()

        # Update daily stats (upsert)
        existing = supabase_client.table("daily_visitor_stats").select("id,visitor_count").eq("date", today).execute()

        if existing.data:
            # Update existing
            supabase_client.table("daily_visitor_stats").update({
                "visitor_count": existing.data[0]["visitor_count"] + 1,
                "updated_at": datetime.now().isoformat()
            }).eq("date", today).execute()
        else:
            # Insert new
            supabase_client.table("daily_visitor_stats").insert({
                "date": today,
                "visitor_count": 1,
                "unique_visitors": 0,
                "analysis_count": 0
            }).execute()
    except Exception as e:
        print(f"⚠️  Analytics tracking error: {e}")


# Analytics endpoints disabled - use dashboard at /analytics instead
# @app.get("/api/analytics")
# async def get_analytics(...): pass
# @app.get("/api/analytics/today")
# async def get_today_analytics(...): pass


# ════════════════════════════════════════════════════════════════════════════
# VIRAL VIDEOS ENDPOINT (EchoTik API)
# ════════════════════════════════════════════════════════════════════════════

@app.get("/api/viral-videos/{category}")
async def get_viral_videos(category: str):
    """
    Récupère vidéos virales (100K+ vues) avec ventes selon catégorie.
    Cache 24h pour économiser requêtes API EchoTik (100/mois).
    """
    if not supabase_client:
        return JSONResponse({
            "ok": False,
            "error": "Database non configurée"
        }, status_code=503)

    try:
        # Vérifier cache
        cached = supabase_client.table("viral_videos_cache").select("*").eq(
            "category", category.lower()
        ).execute()

        if cached.data and cached.data[0]:
            cache_entry = cached.data[0]
            # Vérifier se encore valide (< 24h)
            from datetime import datetime as dt
            expires_at = dt.fromisoformat(cache_entry["expires_at"].replace("Z", "+00:00"))
            if dt.now(expires_at.tzinfo) < expires_at:
                return {
                    "ok": True,
                    "category": category,
                    "videos": cache_entry["videos"],
                    "cached": True,
                    "cached_at": cache_entry["cached_at"]
                }

        # Pas de cache valide → récupérer depuis KeyAPI
        videos = await keyapi_client.get_viral_videos(category)

        if videos:
            # Sauvegarder en cache
            supabase_client.table("viral_videos_cache").upsert({
                "category": category.lower(),
                "videos": videos,
                "cached_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
            }, on_conflict="category").execute()

        return {
            "ok": True,
            "category": category,
            "videos": videos,
            "cached": False,
            "count": len(videos)
        }

    except Exception as e:
        print(f"❌ Viral videos error: {e}")
        return JSONResponse({
            "ok": False,
            "category": category,
            "error": str(e),
            "videos": []
        }, status_code=500)


# Stratégies produits par catégorie
CATEGORY_STRATEGIES = {
    "fashion": {
        "name": "Fashion & Vêtements",
        "hooks": ["Before/After looks", "Outfit transitions", "Styling tips", "Haul videos", "Fashion hacks"],
        "price_positioning": "mid-premium",
        "conversion_timing": "instant-30d",
        "viral_multiplier": 1.3,
        "average_price": "$30-80",
        "best_creators": "Lifestyle, Fashion, Trending",
        "key_metrics": ["Views", "Likes", "Creator followers"]
    },
    "beaute": {
        "name": "Beauté & Cosmétiques",
        "hooks": ["Makeup tutorials", "Before/After transformation", "Product reviews", "Skincare routines", "Beauty hacks"],
        "price_positioning": "mid-premium",
        "conversion_timing": "7-30d",
        "viral_multiplier": 1.5,
        "average_price": "$15-50",
        "best_creators": "Makeup artists, Beauty influencers",
        "key_metrics": ["Views", "Product mentions", "Sales velocity"]
    },
    "sante": {
        "name": "Santé & Bien-être",
        "hooks": ["Health tips", "Wellness transformation", "Product testimonials", "Health routines", "Doctor reviews"],
        "price_positioning": "premium",
        "conversion_timing": "14-90d",
        "viral_multiplier": 1.6,
        "average_price": "$25-100",
        "best_creators": "Health experts, Wellness coaches, Doctors",
        "key_metrics": ["Views", "Comments", "Trust indicators"]
    },
    "complement_sante": {
        "name": "Compléments Nutritionnels",
        "hooks": ["Before/After results", "Ingredient breakdown", "Expert testimonials", "Daily routines", "Performance demos"],
        "price_positioning": "mid-premium",
        "conversion_timing": "30-90d",
        "viral_multiplier": 1.4,
        "average_price": "$20-60",
        "best_creators": "Nutritionists, Fitness influencers, Doctors",
        "key_metrics": ["Views", "Testimonials", "Engagement rate"]
    },
    "tech": {
        "name": "Technologie & Gadgets",
        "hooks": ["Unboxing", "Tech reviews", "How-to demos", "Comparison videos", "Tech hacks"],
        "price_positioning": "premium",
        "conversion_timing": "30-90d",
        "viral_multiplier": 1.2,
        "average_price": "$50-300",
        "best_creators": "Tech reviewers, DIY enthusiasts",
        "key_metrics": ["Views", "Comments", "Share rate"]
    },
    "fitness": {
        "name": "Fitness & Équipement",
        "hooks": ["Transformation stories", "Workout clips", "Before/After", "Equipment reviews", "Fitness tips"],
        "price_positioning": "mid",
        "conversion_timing": "14-60d",
        "viral_multiplier": 1.4,
        "average_price": "$20-150",
        "best_creators": "Fitness trainers, Health coaches, Athletes",
        "key_metrics": ["Views", "Engagement", "Comments"]
    },
    "electromenager": {
        "name": "Électroménager & Maison",
        "hooks": ["Unboxing", "Product demo", "Before/After cleanup", "Life hacks", "Time-saving tips"],
        "price_positioning": "mid-premium",
        "conversion_timing": "30-90d",
        "viral_multiplier": 1.1,
        "average_price": "$40-200",
        "best_creators": "Home organizers, Lifestyle influencers",
        "key_metrics": ["Views", "Shares", "Practicality indicators"]
    }
}


@app.get("/api/product-recommendations/{category}")
async def get_product_recommendations(category: str):
    """Retourne produits recommandés + stratégie pour une catégorie"""
    import json
    from pathlib import Path

    category_lower = category.lower()

    # Récupérer la stratégie
    strategy = CATEGORY_STRATEGIES.get(category_lower, {
        "name": category.capitalize(),
        "hooks": ["Feature highlight", "Product demo"],
        "price_positioning": "mid",
        "conversion_timing": "30d",
        "viral_multiplier": 1.0,
        "average_price": "variable",
        "best_creators": "Relevant niche",
        "key_metrics": ["Views", "Engagement", "Sales"]
    })

    # Récupérer les vidéos virales comme base de recommandations
    videos = await keyapi_client.get_viral_videos(category_lower)

    # Essayer de charger données additionnelles depuis hooks_db.json
    additional_data = {}
    try:
        db_path = Path("hooks_db.json")
        if db_path.exists():
            db = json.loads(db_path.read_text(encoding="utf-8"))
            # Convertir category_lower (ex: "beaute") pour chercher dans product_categories
            product_cat_key = category_lower.replace("-", "_")
            if product_cat_key in db.get("product_categories", {}):
                cat_data = db["product_categories"][product_cat_key]
                additional_data = {
                    "category_names": cat_data.get("names", []),
                    "recommended_hooks_db": cat_data.get("recommended_hooks", []),
                    "price_range": cat_data.get("price_range", "unknown"),
                    "notes": cat_data.get("notes", "")
                }
    except Exception:
        pass  # Continuer sans données supplémentaires

    return {
        "ok": True,
        "category": category_lower,
        "strategy": strategy,
        "recommended_products": videos[:5] if videos else [],
        "product_count": len(videos) if videos else 0,
        **additional_data  # Inclure les données additionnelles si disponibles
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    # Allow larger file uploads (up to 100MB) for video + audio
    uvicorn.run(app, host="0.0.0.0", port=port)
    # Note: FastAPI also respects multipart form size, ensure it can handle up to 100MB
