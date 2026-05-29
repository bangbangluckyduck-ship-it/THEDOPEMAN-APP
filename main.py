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
# 1. Ajout de create_access_token dans l'import
from auth import get_user_from_request, check_quota, increment_usage, usage_info, create_access_token
from stripe_routes import router as stripe_router
from admin_routes import router as admin_router
from cache_manager import get_cached_analysis, save_to_cache, normalize_tiktok_url
from keyapi_integration import keyapi_client

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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    await track_visitor("/", request)
    return HTMLResponse(_HOMEPAGE_HTML)

@app.get("/app", response_class=HTMLResponse)
async def app_page(request: Request):
    await track_visitor("/app", request)
    return HTMLResponse(_APP_HTML)

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
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            try:
                new_user = {"email": email, "tier": "free", "password": password_hash}
                supabase.table("users").insert(new_user).execute()
                token = create_access_token(email)
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
                return await asyncio.wait_for(loop.run_in_executor(None, analyze_visual, frames_list, product), timeout=60.0)

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
                    loop.run_in_executor(None, synthesize_analysis, visual_result, transcript, market_context, product),
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
    if not supabase_client: return JSONResponse({"ok": False, "error": "Database non configurée"}, status_code=503)
    try:
        cached = supabase_client.table("viral_videos_cache").select("*").eq("category", category.lower()).execute()
        if cached.data and cached.data[0]:
            cache_entry = cached.data[0]
            from datetime import datetime as dt
            expires_at = dt.fromisoformat(cache_entry["expires_at"].replace("Z", "+00:00"))
            if dt.now(expires_at.tzinfo) < expires_at:
                return {"ok": True, "category": category, "videos": cache_entry["videos"], "cached": True, "cached_at": cache_entry["cached_at"]}
        videos = await keyapi_client.get_viral_videos(category)
        if videos:
            supabase_client.table("viral_videos_cache").upsert({"category": category.lower(), "videos": videos, "cached_at": datetime.now().isoformat(), "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()}, on_conflict="category").execute()
        return {"ok": True, "category": category, "videos": videos, "cached": False, "count": len(videos)}
    except Exception as e: return JSONResponse({"ok": False, "category": category, "error": str(e), "videos": []}, status_code=500)

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
