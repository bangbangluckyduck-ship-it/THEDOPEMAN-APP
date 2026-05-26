from __future__ import annotations
import asyncio
import json
import os
import tempfile
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

from analyzer import analyze_video, transcribe_audio
from generate_assets import generate_icons
from security import rate_limit_middleware, security_logger
from auth import get_user_from_request, check_quota, increment_usage, usage_info
from stripe_routes import router as stripe_router
from admin_routes import router as admin_router

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


@app.get("/", response_class=HTMLResponse)
async def home():
    """Landing page avec tool d'analyse intégré."""
    return HTMLResponse(_HOMEPAGE_HTML)


@app.get("/app", response_class=HTMLResponse)
async def app_page():
    """Page d'analyse complète."""
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

        # Contexte marché pour GOLD / AGENCY / BETA uniquement
        market_context: Optional[dict] = None
        tier = user.get("tier", "free")
        if tier in ("gold", "agency", "beta") and _SCRAPER_URL:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    mresp = await client.get(f"{_SCRAPER_URL}/api/coach-context")
                if mresp.is_success:
                    market_context = mresp.json()
            except Exception:
                pass  # On continue sans données marché si le scraper est down

        # IA analysis (increased timeout to 180 seconds for complex videos)
        result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_video, frames_list, transcript, market_context),
            timeout=180.0,
        )
        if user["valid"]:
            increment_usage(user["email"])

        result["transcript"]      = transcript
        result["frames_analyzed"] = len(frames_list)
        result["usage"]           = usage_info(user)
        ip = request.client.host if request.client else "unknown"
        security_logger.analyze_ok(ip, len(frames_list))
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


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    # Allow larger file uploads (up to 100MB) for video + audio
    uvicorn.run(app, host="0.0.0.0", port=port, limit_request_fields=32, limit_request_line=0, limit_concurrency=100)
    # Note: FastAPI also respects multipart form size, ensure it can handle up to 100MB
