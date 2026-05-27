from __future__ import annotations
import asyncio
import json
import os
import tempfile
import hashlib
from pathlib import Path
from typing import Optional
from datetime import datetime, date

import httpx
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import time

load_dotenv()

from analyzer import analyze_video, transcribe_audio
from generate_assets import generate_icons
from security import rate_limit_middleware, security_logger
from auth import get_user_from_request, check_quota, increment_usage, usage_info
from stripe_routes import router as stripe_router
from admin_routes import router as admin_router
from cache_manager import get_cached_analysis, save_to_cache, normalize_tiktok_url

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

_HOMEPAGE_HTML = Path("templates/homepage.html").read_text(encoding="utf-8")
_APP_HTML = Path("templates/index.html").read_text(encoding="utf-8")
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
async def analytics():
    """Analytics dashboard."""
    return HTMLResponse(_ANALYTICS_HTML)


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
async def analyze(
    request: Request,
    frames: str = Form(...),
    audio: Optional[UploadFile] = File(None),
    product: Optional[str] = Form(None),
):
    if not os.getenv("MISTRAL_API_KEY"):
        raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")

    # Log les agents suspects sans bloquer (monitoring uniquement)
    ua = request.headers.get("User-Agent", "").lower()
    if any(w in ua for w in ["scrapy", "spider", "crawler"]):
        ip = request.client.host if request.client else "unknown"
        security_logger.suspicious_agent(ip, ua)

    user = get_user_from_request(request)
    check_quota(user)

    frames_list: list[str] = json.loads(frames)
    if not frames_list:
        raise HTTPException(status_code=400, detail="Aucune frame reçue.")

    loop = asyncio.get_event_loop()
    audio_path: Optional[str] = None

    try:
        # Save audio to temp file if provided
        if audio:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio_path = tmp.name
                tmp.write(await audio.read())

        # Transcription with 20s timeout
        transcript: Optional[str] = None
        if audio_path:
            try:
                transcript = await asyncio.wait_for(
                    loop.run_in_executor(None, transcribe_audio, audio_path),
                    timeout=20.0,
                )
            except asyncio.TimeoutError:
                transcript = None

        # Contexte marché pour GOLD / AGENCY / BETA / ADMIN
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
                pass  # On continue sans données marché si le scraper est down

        # IA analysis (increased timeout to 180 seconds for complex videos)
        analysis_start = time.time()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_video, frames_list, transcript, market_context, product),
            timeout=180.0,
        )
        analysis_duration_ms = int((time.time() - analysis_start) * 1000)

        if user["valid"]:
            increment_usage(user["email"])

        result["transcript"]      = transcript
        result["frames_analyzed"] = len(frames_list)
        result["usage"]           = usage_info(user)

        # Save result to cache for faster future analyses
        # Extract video URL from request if available (will be null for direct frame uploads)
        video_url_to_cache = request.query_params.get("video_url", f"frames_{len(frames_list)}")
        try:
            await save_to_cache(
                video_url_to_cache,
                result,
                analysis_duration_ms,
                product_id=product
            )
        except Exception as e:
            # Don't fail the analysis if cache save fails
            security_logger.analyze_error(request.client.host if request.client else "unknown", f"Cache save error: {e}")

        ip = request.client.host if request.client else "unknown"
        security_logger.analyze_ok(ip, len(frames_list))

        # Increment analysis count in analytics
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
            except Exception as e:
                pass  # Don't fail the analysis if analytics update fails

        return result

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="L'analyse a pris trop longtemps (>3min). Essaie avec une vidéo plus courte ou une résolution plus basse.")
    except HTTPException:
        raise
    except Exception as e:
        ip = request.client.host if request.client else "unknown"
        security_logger.analyze_error(ip, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if audio_path:
            try:
                os.unlink(audio_path)
            except OSError:
                pass


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
                yield f'data: {json.dumps({"message": "Analyse complète ✅", "source": "cache", "duration_ms": cached_analysis.get("analysis_duration_ms", 0)})}\n\n'

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


# ── ECHOTIK DATA ENDPOINTS ────────────────────────────────────────────────────
@app.get("/api/market-recommendations")
async def market_recommendations():
    """Récupère les données marché complètes depuis TTS Scraper (EchoTik)."""
    if not _SCRAPER_URL:
        return JSONResponse({"ok": False, "error": "TTS_SCRAPER_URL non configuré"}, status_code=503)
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{_SCRAPER_URL}/api/coach-context")
        if resp.is_success:
            return resp.json()
        return JSONResponse({"ok": False, "error": f"Scraper error {resp.status_code}"}, status_code=502)
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=502)


@app.get("/api/product-recommendations/{category}")
async def product_recommendations(category: str):
    """Retourne les recommandations produits pour une catégorie spécifique."""
    import json
    from pathlib import Path

    try:
        # Charger hooks_db.json pour obtenir les infos de catégorie
        db_path = Path("hooks_db.json")
        if not db_path.exists():
            raise HTTPException(status_code=404, detail="Base de données produits non trouvée")

        db = json.loads(db_path.read_text(encoding="utf-8"))

        # Chercher la catégorie dans product_categories
        category_lower = category.lower().replace("-", "_")
        if category_lower not in db.get("product_categories", {}):
            return {
                "ok": False,
                "error": f"Catégorie '{category}' non trouvée",
                "available_categories": list(db.get("product_categories", {}).keys())
            }

        cat_data = db["product_categories"][category_lower]

        # Récupérer les données marché si disponibles
        market_data = None
        if _SCRAPER_URL:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    resp = await client.get(f"{_SCRAPER_URL}/api/coach-context?category={category_lower}")
                if resp.is_success:
                    market_data = resp.json()
            except Exception:
                pass  # Continuer sans données marché

        return {
            "ok": True,
            "category": category_lower,
            "category_names": cat_data.get("names", []),
            "recommended_hooks": cat_data.get("recommended_hooks", []),
            "price_range": cat_data.get("price_range", "unknown"),
            "notes": cat_data.get("notes", ""),
            "market_data": market_data or {
                "top_products": [],
                "trending": [],
                "top_creators": []
            }
        }


# ════════════════════════════════════════════════════════════════════════════
# ANALYTICS ENDPOINTS
# ════════════════════════════════════════════════════════════════════════════

async def track_visitor(page: str, request: Request, user_email: Optional[str] = None):
    """Track visitor to analytics database."""
    if not supabase_client:
        return

    try:
        # Get IP hash
        ip = request.client.ip if request.client else "unknown"
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


@app.get("/api/analytics")
async def get_analytics(password: Optional[str] = Query(None)):
    """Get analytics data (requires admin password)."""
    if not supabase_client:
        return JSONResponse({"error": "Analytics not available"}, status_code=503)

    # Check password
    if password != os.getenv("ANALYTICS_PASSWORD", "admin123"):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    try:
        # Get last 30 days of stats
        stats = supabase_client.table("daily_visitor_stats").select("*").order("date", desc=True).limit(30).execute()

        # Get visitor count summary
        summary = supabase_client.table("daily_visitor_stats").select("visitor_count").execute()
        total_visitors = sum([s["visitor_count"] for s in summary.data]) if summary.data else 0

        return {
            "ok": True,
            "total_visitors": total_visitors,
            "daily_stats": stats.data or [],
            "period": "last_30_days"
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/analytics/today")
async def get_today_analytics(password: Optional[str] = Query(None)):
    """Get today's visitor count (requires admin password)."""
    if not supabase_client:
        return JSONResponse({"error": "Analytics not available"}, status_code=503)

    if password != os.getenv("ANALYTICS_PASSWORD", "admin123"):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    try:
        today = date.today().isoformat()
        result = supabase_client.table("daily_visitor_stats").select("visitor_count").eq("date", today).execute()

        visitor_count = 0
        if result.data:
            visitor_count = result.data[0]["visitor_count"]

        return {
            "ok": True,
            "date": today,
            "visitor_count": visitor_count
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    # Allow larger file uploads (up to 100MB) for video + audio
    uvicorn.run(app, host="0.0.0.0", port=port)
    # Note: FastAPI also respects multipart form size, ensure it can handle up to 100MB
