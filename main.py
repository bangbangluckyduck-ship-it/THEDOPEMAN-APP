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
app.middleware("http")(rate_limit_middleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(stripe_router)   # /create-checkout-session  /customer-portal  /webhook
app.include_router(admin_router)    # /admin/users  /admin/set-tier  /admin/grant-beta

_HTML = Path("templates/index.html").read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(_HTML)


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

        # IA analysis
        result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_video, frames_list, transcript, market_context),
            timeout=90.0,
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
        raise HTTPException(status_code=504, detail="Analyse trop longue. Réessaie.")
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
    uvicorn.run(app, host="0.0.0.0", port=port)
