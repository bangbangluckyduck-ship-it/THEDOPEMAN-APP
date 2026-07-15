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
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, Response, RedirectResponse, FileResponse
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
from insights_store import save_insight, build_winning_payload
import tiktok_oauth
import google_oauth
import market_creators
import recherche_quota
import photo_slide
import product_store
import credits as credits_mod
import video_prompt
import image_gen
import carousel
import ai_providers
import hashlib
from urllib.parse import quote


def _ip_hash(request: Request) -> str:
    ip = request.client.host if request.client else "unknown"
    return hashlib.sha256(("tts:" + ip).encode()).hexdigest()[:32]

_PROMPT_STUDIO_TIERS = {"pro", "gold", "agency", "beta", "admin"}


def _record_analyzed_product(result: dict, region: Optional[str] = None) -> None:
    """Best-effort : enregistre le produit détecté dans la mémoire produits."""
    try:
        det = (result or {}).get("detection") or {}
        produit = det.get("produit")
        if not produit or str(produit).lower() in ("non détecté", "non detecte", ""):
            return
        product_store.record_product(
            supabase_client,
            name=produit,
            category=det.get("categorie_marche"),
            region=region,
            price=det.get("prix_estime"),
        )
    except Exception:
        pass

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
    p: tier
    for p, tier in [
        (os.getenv("STRIPE_PRICE_PRO", ""),              "pro"),
        (os.getenv("STRIPE_PRICE_PRO_YEAR", ""),         "pro"),
        (os.getenv("STRIPE_PRICE_PRO_999", ""),          "pro"),
        (os.getenv("STRIPE_PRICE_PRO_999_YEAR", ""),     "pro"),
        (os.getenv("STRIPE_PRICE_PRO_1199", ""),         "pro"),
        (os.getenv("STRIPE_PRICE_PRO_1199_YEAR", ""),    "pro"),
        (os.getenv("STRIPE_PRICE_GOLD", ""),             "gold"),
        (os.getenv("STRIPE_PRICE_GOLD_YEAR", ""),        "gold"),
        (os.getenv("STRIPE_PRICE_GOLD_LAUNCH", ""),      "gold"),
        (os.getenv("STRIPE_PRICE_GOLD_LAUNCH_YEAR", ""), "gold"),
        (os.getenv("STRIPE_PRICE_AGENCY", ""),           "agency"),
        (os.getenv("STRIPE_PRICE_AGENCY_YEAR", ""),      "agency"),
    ]
    if p  # exclut les clés vides
}
try:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
except Exception as e:
    print(f"⚠️  Supabase analytics client init failed: {e}")
    supabase_client = None

def _persist_sync_analysis(user: dict, result: dict, *, source: str,
                           source_url=None, product=None, price=None,
                           title=None, duration_ms=None) -> None:
    """Persiste une analyse sync dans analysis_jobs (status='done') pour qu'elle
    apparaisse dans "Mes analyses" cross-device. Best-effort, jamais bloquant.

    Skip si :
    - utilisateur non connecté (pas de stockage anonyme dans la table)
    - result vient du cache (déjà persisté lors de la 1re analyse)
    """
    try:
        if not user or not user.get("valid") or not user.get("email"):
            return
        if isinstance(result, dict) and result.get("from_cache"):
            return
        import analysis_jobs as _aj
        # Titre court : product → filename → "Analyse vidéo"
        t = title or product or (source_url[:60] if source_url else "Analyse vidéo")
        _aj.create_done_job(
            user_email=user["email"], source=source, result=result,
            source_url=source_url, product=product, price=price,
            title=t[:80], duration_ms=duration_ms,
        )
    except Exception as e:
        print(f"[_persist_sync_analysis] KO: {e}")


generate_icons()

# Nettoyage des jobs orphelins au démarrage : si Render a redéployé pendant
# qu'un job était en cours, le worker a été tué → le job reste "running"
# pour l'éternité. On marque "error" tous les jobs running depuis >10 min.
try:
    import analysis_jobs as _aj_startup
    _aj_startup.cleanup_stale_running(timeout_minutes=10)
except Exception as _e_startup:
    print(f"[startup] cleanup_stale_running KO: {_e_startup}")

app = FastAPI(title="Qeerah")

# --- PROTECTION ANTI-CRASH : FILE D'ATTENTE GLOBALE ---
ANALYSIS_SEMAPHORE = asyncio.Semaphore(1)

# --- "Aha! Moment" : blindage backend des essais anonymes par IP ---
# Stocke les timestamps des requêtes anonymes par IP (fenêtre glissante 24h).
# 1 essai gratuit + 1 marge d'erreur réseau => on bloque à partir de la 3e requête.
_ANON_IP_USAGE: dict[str, list[float]] = {}
_ANON_WINDOW_SECONDS = 24 * 60 * 60   # 24h
_ANON_MAX_REQUESTS = 2                 # 1 essai + 1 marge

# ⚠️ Middleware ASGI PUR (et non BaseHTTPMiddleware) : BaseHTTPMiddleware bufferise
# les réponses en streaming (il accumule tout le corps avant de l'envoyer), ce qui
# casse le SSE (analyse vidéo + Photo Slide). En ASGI pur on ne touche jamais au
# corps de la réponse → le streaming passe chunk par chunk.
class LimitUploadSize:
    def __init__(self, app, max_upload_size: int):
        self.app = app
        self.max_upload_size = max_upload_size

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http" and scope.get("method") == "POST":
            for k, v in scope.get("headers") or []:
                if k == b"content-length":
                    try:
                        if int(v) > self.max_upload_size:
                            resp = JSONResponse(
                                status_code=413,
                                content={"detail": f"File too large. Max size: {self.max_upload_size/1024/1024:.0f}MB"},
                            )
                            await resp(scope, receive, send)
                            return
                    except ValueError:
                        pass
                    break
        await self.app(scope, receive, send)

class CanonicalHostRedirect:
    """Redirige (308) toute requête arrivant par l'URL technique Render (*.onrender.com)
    vers le domaine officiel → AUCUNE URL Render n'est jamais visible, quel que soit le
    lien cliqué. /health exclu (sonde interne Render). ASGI pur (pas de buffering SSE)."""
    def __init__(self, app, canonical_host: str):
        self.app = app
        self.canonical_host = (canonical_host or "").strip().lower().rstrip("/")

    async def __call__(self, scope, receive, send):
        if self.canonical_host and scope.get("type") == "http":
            host = ""
            for k, v in scope.get("headers") or []:
                if k == b"host":
                    host = v.decode("latin-1").split(":")[0].lower()
                    break
            path = scope.get("path") or "/"
            if host.endswith(".onrender.com") and path != "/health":
                qs = (scope.get("query_string") or b"").decode("latin-1")
                url = f"https://{self.canonical_host}{path}" + (f"?{qs}" if qs else "")
                resp = RedirectResponse(url, status_code=308)
                await resp(scope, receive, send)
                return
        await self.app(scope, receive, send)


# ── En-têtes de sécurité HTTP (injectés sur TOUTES les réponses) ──────────────
# ASGI pur (pas de BaseHTTPMiddleware) pour ne pas bufferiser le SSE (analyse vidéo,
# Photo Slide). On n'ajoute un en-tête que s'il n'est pas déjà présent, pour laisser
# une éventuelle route surcharger une valeur au cas par cas.
# La CSP est volontairement PERMISSIVE au départ (autorise https:, inline, eval) afin
# de ne rien casser sur la homepage (styles/scripts inline, Turnstile, Stripe, TikTok).
# À durcir progressivement ensuite (retirer 'unsafe-inline'/'unsafe-eval', lister les
# domaines précis) une fois le comportement validé en prod.
_CSP_POLICY = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; "
    "style-src 'self' 'unsafe-inline' https:; "
    "img-src 'self' data: blob: https:; "
    "font-src 'self' data: https:; "
    "connect-src 'self' https:; "
    "frame-src 'self' https:; "
    "media-src 'self' blob: https:; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "frame-ancestors 'self'"
)
_SECURITY_HEADERS = [
    (b"strict-transport-security", b"max-age=31536000; includeSubDomains"),
    # Temporairement en Report-Only (n'bloque RIEN, remonte juste les violations)
    # le temps de confirmer qu'aucune intégration (Google login, etc.) n'est cassée.
    # Repasser à "content-security-policy" (bloquant) une fois validé en navigateur.
    (b"content-security-policy-report-only", _CSP_POLICY.encode("latin-1")),
    (b"x-frame-options", b"SAMEORIGIN"),
    (b"x-content-type-options", b"nosniff"),
    (b"referrer-policy", b"strict-origin-when-cross-origin"),
    (b"permissions-policy", b"camera=(), microphone=(), geolocation=(), browsing-topics=()"),
]


class SecurityHeaders:
    """Middleware ASGI pur : ajoute les 6 en-têtes de sécurité manquants à chaque réponse."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_headers(message):
            if message.get("type") == "http.response.start":
                headers = message.setdefault("headers", [])
                present = {k.lower() for k, _ in headers}
                for name, value in _SECURITY_HEADERS:
                    if name not in present:
                        headers.append((name, value))
            await send(message)

        await self.app(scope, receive, send_with_headers)


app.add_middleware(LimitUploadSize, max_upload_size=100*1024*1024)
app.add_middleware(CanonicalHostRedirect,
                   canonical_host=os.getenv("CANONICAL_HOST", "qeerah.com"))
app.add_middleware(SecurityHeaders)
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
    # NOTE (rollback point 6) : le basculement automatique vers les .min.js a été
    # temporairement retiré (suspicion de régression sur /app). On sert de nouveau
    # les fichiers .js d'origine. À réintroduire après validation en navigateur.
    import re
    return re.sub(
        r'(/static/[^"\'?\s>]+\.(?:js|css))(?=["\'\s>])',
        lambda m: f"{m.group(1)}?v={_ASSET_V}",
        html,
    )

_HOMEPAGE_HTML = _bust(Path("templates/homepage.html").read_text(encoding="utf-8"))
_APP_HTML = _bust(Path("templates/index.html").read_text(encoding="utf-8"))
_CAROUSEL_PAGE_HTML = _bust(Path("templates/carousel.html").read_text(encoding="utf-8"))
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
_CGV_HTML = Path("templates/cgv.html").read_text(encoding="utf-8")
# Pages tarifs/crédits dédiées (dynamiques côté client via /api/plans/*)
_PRICING_HTML = _bust(Path("templates/pricing.html").read_text(encoding="utf-8"))
_PRICING_COMPARE_HTML = _bust(Path("templates/pricing_compare.html").read_text(encoding="utf-8"))
_CREDITS_HTML = _bust(Path("templates/credits.html").read_text(encoding="utf-8"))
# Témoignages (Feature 2)
_AVIS_HTML = _bust(Path("templates/avis.html").read_text(encoding="utf-8"))
_TEMOIGNAGES_HTML = _bust(Path("templates/temoignages.html").read_text(encoding="utf-8"))
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

@app.get("/carousel", response_class=HTMLResponse)
async def carousel_page(request: Request):
    await track_visitor("/carousel", request)
    return HTMLResponse(_CAROUSEL_PAGE_HTML)

@app.get("/confidentialite", response_class=HTMLResponse)
@app.get("/privacy", response_class=HTMLResponse)
async def privacy_page(): return HTMLResponse(_PRIVACY_HTML)

@app.get("/conditions", response_class=HTMLResponse)
@app.get("/terms", response_class=HTMLResponse)
async def terms_page(): return HTMLResponse(_TERMS_HTML)

@app.get("/cgv", response_class=HTMLResponse)
@app.get("/conditions-de-vente", response_class=HTMLResponse)
async def cgv_page(): return HTMLResponse(_CGV_HTML)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon(): return FileResponse("static/favicon.ico")
@app.get("/apple-touch-icon.png", include_in_schema=False)
@app.get("/apple-touch-icon-precomposed.png", include_in_schema=False)
async def apple_touch(): return FileResponse("static/apple-touch-icon.png")

@app.get("/pricing", response_class=HTMLResponse)
@app.get("/tarifs", response_class=HTMLResponse)
async def pricing_page(): return HTMLResponse(_PRICING_HTML)

@app.get("/pricing/compare", response_class=HTMLResponse)
@app.get("/tarifs/comparer", response_class=HTMLResponse)
async def pricing_compare_page(): return HTMLResponse(_PRICING_COMPARE_HTML)

@app.get("/credits", response_class=HTMLResponse)
@app.get("/credits.html", response_class=HTMLResponse)
async def credits_page(): return HTMLResponse(_CREDITS_HTML)

@app.get("/avis", response_class=HTMLResponse)
@app.get("/temoignage", response_class=HTMLResponse)
async def avis_page(): return HTMLResponse(_AVIS_HTML)

@app.get("/temoignages", response_class=HTMLResponse)
async def temoignages_page(): return HTMLResponse(_TEMOIGNAGES_HTML)

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


# ── SEO : robots.txt + sitemap.xml ────────────────────────────────────────────
def _seo_base_url() -> str:
    """URL canonique publique (sans slash final) pour les liens du sitemap."""
    host = (os.getenv("CANONICAL_HOST", "qeerah.com") or "qeerah.com").strip().rstrip("/")
    if host.startswith("http://") or host.startswith("https://"):
        return host.rstrip("/")
    return f"https://{host}"

# Pages publiques indexables (chemin canonique unique par page).
_SITEMAP_PATHS = [
    "/",
    "/app",
    "/pricing",
    "/pricing/compare",
    "/credits",
    "/temoignages",
    "/avis",
    "/about",
    "/contact",
    "/blog",
    "/blog/histoire-tiktok-shop",
    "/blog/createurs-millionnaires",
    "/blog/tendances-2026",
    "/blog/guide-complet",
    "/privacy",
    "/terms",
    "/cgv",
]

@app.get("/robots.txt", include_in_schema=False)
async def robots_txt():
    base = _seo_base_url()
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        # Espaces privés / techniques : inutiles pour l'indexation.
        "Disallow: /api/\n"
        "Disallow: /dope-admin\n"
        f"\nSitemap: {base}/sitemap.xml\n"
    )
    return Response(content=body, media_type="text/plain")

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap_xml():
    base = _seo_base_url()
    urls = "".join(
        f"  <url><loc>{base}{p}</loc><changefreq>weekly</changefreq></url>\n"
        for p in _SITEMAP_PATHS
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}"
        "</urlset>\n"
    )
    return Response(content=xml, media_type="application/xml")


# ════════════════════════════════════════════════════════════════════════════
# EMAILS D'INCITATION FREE → PAYANT (déclencheur quota + relance J+3) + désinscription
# ════════════════════════════════════════════════════════════════════════════
async def _maybe_upsell_free_quota(user: dict) -> None:
    """Free qui vient d'atteindre sa limite mensuelle → email d'upsell (1×/mois, opt-out
    respecté). Best-effort : ne casse jamais l'analyse."""
    try:
        if not supabase_client or not user.get("valid"):
            return
        if (user.get("tier") or "free").lower() != "free":
            return
        email = user["email"]
        from auth import supabase_get_monthly_count, make_unsubscribe_token, TIER_CONFIG
        limit = (TIER_CONFIG.get("free") or {}).get("monthly") or 3
        if supabase_get_monthly_count(email) < limit:
            return  # pas encore à la limite
        month = date.today().strftime("%Y-%m")
        row = supabase_client.table("users").select(
            "marketing_opt_out,upsell_quota_email_month").eq("email", email).limit(1).execute()
        u = (row.data or [{}])[0] if getattr(row, "data", None) else {}
        if u.get("marketing_opt_out") or u.get("upsell_quota_email_month") == month:
            return  # désinscrit, ou déjà relancé ce mois-ci
        from email_service import email_service
        from urllib.parse import quote as _q
        unsub = f"{tiktok_oauth.APP_PUBLIC_URL}/unsubscribe?e={_q(email)}&s={make_unsubscribe_token(email)}"
        if await email_service.send_upsell_email(email, unsub, kind="quota"):
            supabase_client.table("users").update(
                {"upsell_quota_email_month": month}).eq("email", email).execute()
    except Exception as e:
        print(f"[upsell] quota KO: {e}")


@app.get("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(e: str = Query(...), s: str = Query(...)):
    """Désinscription des emails promotionnels (lien signé dans les emails). RGPD."""
    from auth import verify_unsubscribe_token
    email = (e or "").strip().lower()
    ok = bool(email) and verify_unsubscribe_token(email, s)
    if ok and supabase_client:
        try:
            supabase_client.table("users").update({"marketing_opt_out": True}).eq("email", email).execute()
        except Exception as ex:
            print(f"[unsubscribe] KO: {ex}")
            ok = False
    msg = ("Tu es bien désinscrit des emails promotionnels. Tu continueras à recevoir les emails "
           "essentiels (sécurité, mot de passe)." if ok else
           "Lien de désinscription invalide ou expiré. Écris-nous si besoin.")
    return HTMLResponse(
        f"<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
        f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>Désinscription</title></head>"
        f"<body style='font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#f4f5f7;margin:0;padding:40px 16px;'>"
        f"<div style='max-width:480px;margin:0 auto;background:#fff;border-radius:16px;padding:32px;text-align:center;box-shadow:0 4px 24px rgba(0,0,0,.06)'>"
        f"<div style='font-size:40px'>{'✅' if ok else '⚠️'}</div>"
        f"<p style='font-size:15px;color:#1a1a2e;line-height:1.6'>{msg}</p>"
        f"<a href='{tiktok_oauth.APP_PUBLIC_URL}' style='color:#6c5ce7;text-decoration:none;font-weight:600'>← Retour au site</a>"
        f"</div></body></html>")


@app.get("/api/_cron/upsell-j3")
async def cron_upsell_j3(key: str = Query("")):
    """Tâche planifiée (cron quotidien) : relance les Free inscrits il y a ~3 jours.
    Protégé par CRON_SECRET. À appeler 1×/jour (Render Cron ou cron externe)."""
    cron_secret = os.getenv("CRON_SECRET", "")
    if not cron_secret or key != cron_secret:
        raise HTTPException(status_code=403, detail="Clé cron invalide.")
    if not supabase_client:
        return {"ok": False, "reason": "supabase indisponible"}
    from datetime import timedelta as _td
    from auth import make_unsubscribe_token
    from email_service import email_service
    from urllib.parse import quote as _q
    now = datetime.now(timezone.utc)
    lo = (now - _td(days=4)).isoformat()
    hi = (now - _td(days=3)).isoformat()
    sent = 0
    skipped = 0
    try:
        rows = (supabase_client.table("users")
                .select("email,tier,marketing_opt_out,upsell_j3_sent,created_at")
                .eq("tier", "free").gte("created_at", lo).lte("created_at", hi)
                .limit(200).execute())
        for u in (rows.data or []):
            email = (u.get("email") or "").strip().lower()
            if not email or u.get("marketing_opt_out") or u.get("upsell_j3_sent"):
                skipped += 1
                continue
            unsub = f"{tiktok_oauth.APP_PUBLIC_URL}/unsubscribe?e={_q(email)}&s={make_unsubscribe_token(email)}"
            if await email_service.send_upsell_email(email, unsub, kind="j3"):
                supabase_client.table("users").update({"upsell_j3_sent": True}).eq("email", email).execute()
                sent += 1
    except Exception as ex:
        return {"ok": False, "error": str(ex), "sent": sent}
    return {"ok": True, "sent": sent, "skipped": skipped}


@app.get("/api/_cron/feed-radar-collect")
async def cron_feed_radar_collect(key: str = Query(""), region: Optional[str] = Query(None)):
    """Tâche planifiée (cron ~6h) : collecte Feed Radar (découverte créateurs
    → vidéos ≥ seuil de vues → GMV estimé + tendance créateur → oEmbed) sur
    tous les marchés de FEED_RADAR_REGIONS (mêmes marchés que "Créateurs
    Gagnants") — précise ?region=XX pour un déclenchement manuel ciblé.
    Protégé par CRON_SECRET. À appeler via Render Cron Job / pinger externe —
    aucun scheduler n'existe dans ce repo, cf. mémoire projet."""
    cron_secret = os.getenv("CRON_SECRET", "")
    if not cron_secret or key != cron_secret:
        raise HTTPException(status_code=403, detail="Clé cron invalide.")
    import feed_radar
    try:
        summary = await feed_radar.run_feed_radar_collection(region)
    except Exception as e:
        print(f"/api/_cron/feed-radar-collect error: {e}")
        return JSONResponse({"ok": False, "error": str(e)}, status_code=502)
    return summary


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
        from supabase_client import supabase_service as supabase, SUPABASE_ENABLED
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

# Création de compte SÉCURISÉE.
# ⚠️ CORRECTIF SÉCURITÉ : cette route délivrait auparavant un token de session valide
# pour N'IMPORTE QUEL email, sans mot de passe ni preuve de possession de l'adresse
# (usurpation de compte triviale). Elle exige désormais un mot de passe, hache celui-ci
# avec bcrypt et ne renvoie un token qu'après création effective du compte — exactement
# comme la branche « nouveau compte » de /api/login. Un CAPTCHA anti-bot (Turnstile) est
# également exigé quand il est configuré.
@app.post("/api/register")
async def register(request: Request):
    import bcrypt
    from supabase_client import supabase_service as supabase
    from auth import create_access_token

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Corps de requête invalide")

    email = body.get("email", "").lower().strip() if isinstance(body, dict) else ""
    password = body.get("password", "") if isinstance(body, dict) else ""

    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Email invalide")
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Mot de passe min 6 caractères")

    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")

    # Anti-bot AVANT toute écriture / envoi d'email (no-op si Turnstile non configuré).
    cf_token = body.get("cf_turnstile_token", "")
    remote_ip = request.client.host if request.client else ""
    if not await verify_turnstile(cf_token, remote_ip):
        raise HTTPException(status_code=400, detail="Vérification anti-robot échouée. Merci de réessayer.")

    # Compte déjà existant → on ne délivre pas de token (il faut passer par /api/login).
    try:
        existing = supabase.table("users").select("id").eq("email", email).execute()
        if existing and existing.data:
            raise HTTPException(status_code=409, detail="Un compte existe déjà pour cet email. Connecte-toi.")
    except HTTPException:
        raise
    except Exception as e:
        print(f"[register] vérification email existant impossible : {e}")
        raise HTTPException(status_code=500, detail="BD non disponible")

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        supabase.table("users").insert(
            {"email": email, "tier": "free", "password": password_hash}
        ).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur création compte: {str(e)}")

    # Email de bienvenue best-effort (un échec ne bloque jamais l'inscription).
    try:
        from email_service import email_service
        await email_service.send_welcome_email(email)
    except Exception as mail_err:
        print(f"[email] bienvenue non envoyé à {email} : {mail_err}")

    token = create_access_token(email)
    return {"ok": True, "email": email, "tier": "free", "created": True, "token": token}

# 3. MODIFICATION : Génération et distribution du Token sur /login
@app.post("/api/login")
async def login(request: Request):
    import bcrypt
    from supabase_client import supabase_service as supabase
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
    """Demande de réinitialisation : envoie un LIEN magique sécurisé par email.
    Le mot de passe n'est PAS modifié ici — il le sera sur /reset-password (preuve
    de possession de la boîte mail), via /api/change-password. Anti-énumération : même
    réponse que le compte existe ou non."""
    from supabase_client import supabase_service as supabase
    from password_reset import create_password_reset_token, check_rate_limit
    from email_service import email_service
    from urllib.parse import quote as _q

    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
        if not email or "@" not in email:
            raise HTTPException(status_code=400, detail="Email invalide")

        ip = request.client.host if request.client else "unknown"
        if not check_rate_limit(email, max_attempts=5, window_hours=1):
            security_logger.password_reset_requested(email, ip)
            raise HTTPException(status_code=429, detail="Trop de tentatives. Réessaie dans 1 heure.")

        exists = False
        if supabase:
            try:
                exists = bool(supabase.table("users").select("id").eq("email", email).execute().data)
            except Exception:
                exists = False

        if exists:
            success, token_plaintext, _ = create_password_reset_token(email, "magic_link")
            if success:
                link = f"{tiktok_oauth.APP_PUBLIC_URL}/reset-password?token={token_plaintext}&email={_q(email)}"
                await email_service.send_magic_link_email(email, link)
                security_logger.password_reset_requested(email, ip, success=True)
        else:
            security_logger.password_reset_requested(email, ip, success=False)

        # Réponse volontairement identique (anti-énumération de comptes)
        return {"ok": True, "message": "Si un compte existe pour cet email, un lien de réinitialisation vient d'être envoyé (valable 24h)."}

    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/change-password")
async def change_password(request: Request):
    import bcrypt
    from supabase_client import supabase_service as supabase
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

@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page():
    """Page de définition du nouveau mot de passe (atteinte via le lien magique de l'email).
    Lit token+email depuis l'URL et poste sur /api/change-password (qui applique le MDP)."""
    html = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Réinitialiser le mot de passe</title>
<style>*{box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f4f5f7;margin:0;padding:40px 16px;color:#1a1a2e}
.card{max-width:420px;margin:0 auto;background:#fff;border-radius:16px;padding:32px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
h1{font-size:20px;margin:0 0 6px}p{font-size:14px;color:#3a3a4a}input{width:100%;padding:12px;border:1px solid #e3e8ef;border-radius:8px;font-size:15px;margin-top:10px}
button{width:100%;padding:13px;border:none;border-radius:10px;background:#6c5ce7;color:#fff;font-size:15px;font-weight:700;cursor:pointer;margin-top:16px}
.msg{margin-top:14px;font-size:14px;text-align:center}.ok{color:#0a7c3c}.err{color:#c0392b}</style></head>
<body><div class="card">
<h1>🔐 Nouveau mot de passe</h1>
<p>Choisis un nouveau mot de passe pour ton compte.</p>
<form id="f" onsubmit="return go(event)">
  <input type="password" id="p1" placeholder="Nouveau mot de passe (min. 6)" required minlength="6">
  <input type="password" id="p2" placeholder="Confirmer le mot de passe" required minlength="6">
  <button type="submit">Réinitialiser</button>
</form>
<div id="m" class="msg"></div>
</div>
<script>
const qs=new URLSearchParams(location.search);const token=qs.get('token')||'';const email=(qs.get('email')||'').toLowerCase();
const m=document.getElementById('m');
if(!token||!email){m.className='msg err';m.textContent='Lien invalide ou incomplet.';document.getElementById('f').style.display='none';}
async function go(e){e.preventDefault();
  const p1=document.getElementById('p1').value,p2=document.getElementById('p2').value;
  if(p1!==p2){m.className='msg err';m.textContent='Les mots de passe ne correspondent pas.';return false;}
  m.className='msg';m.textContent='⏳ En cours…';
  try{const r=await fetch('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({reset_token:token,new_password:p1,email})});
    const d=await r.json().catch(()=>({}));
    if(r.ok){m.className='msg ok';m.innerHTML='✅ Mot de passe modifié ! <a href="/app">Se connecter →</a>';document.getElementById('f').style.display='none';}
    else{m.className='msg err';m.textContent='❌ '+(d.detail||'Lien expiré ou invalide. Refais une demande.');}
  }catch(_){m.className='msg err';m.textContent='❌ Erreur réseau.';}
  return false;}
</script></body></html>"""
    return HTMLResponse(html)


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
    video: Optional[UploadFile] = File(None),
    product: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    user_role: Optional[str] = Form(None),
):
    # Rôle choisi par l'utilisateur (Affilié/Vendeur) à CETTE analyse — normalisé
    # ici une bonne fois, propagé tel quel à synthesize_analysis().
    user_role = (user_role or "").strip().lower() or None
    if user_role not in ("affilie", "vendeur"):
        user_role = None
    # Si l'utilisateur est Pro+ ET qu'il a uploadé la vidéo entière → on bascule
    # sur le pipeline natif Gemini Pro (visuel + audio en un appel, qualité
    # identique au pipeline URL). Sinon → ancien pipeline frames+AssemblyAI.
    if not ai_providers.any_ai_key(): raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")

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

    # ── Dispatcher de pipeline : si Pro+ ET vidéo uploadée → nouveau pipeline ──
    _paid_tiers = {"pro", "gold", "agency", "beta", "admin"}
    _user_tier = user.get("tier", "free")
    _use_native_pipeline = (_user_tier in _paid_tiers) and (video is not None)
    _video_upload = video  # référence conservée pour lecture DANS le stream

    async def stream_analysis():
        loop = asyncio.get_event_loop()
        audio_path: Optional[str] = None
        video_path_tmp: Optional[str] = None
        downscaled_path: Optional[str] = None
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

            market_context = None
            tier = _user_tier

            # ════════════════════════════════════════════════════════════════
            # PIPELINE PRO+ : Gemini Pro vidéo native (visuel + audio en un appel)
            # ════════════════════════════════════════════════════════════════
            if _use_native_pipeline and _video_upload is not None:
                # Annonce d'attente DÈS LE DÉBUT (psychologiquement, le user
                # accepte d'attendre s'il sait à quoi s'attendre).
                yield 'event: progress\n'
                yield 'data: {"message": "\\ud83d\\udd0d Analyse approfondie en cours\\u2026", "stage": "init", "info": "L\'analyse Pro prend g\\u00e9n\\u00e9ralement 30 \\u00e0 60 secondes \\u2014 on traite ta vid\\u00e9o enti\\u00e8re (image + audio + d\\u00e9tection CTA)."}\n\n'

                # Streaming UploadFile → fichier temporaire SANS jamais charger
                # la vidéo entière en RAM (Render 512 MB → OOM sinon).
                yield 'event: progress\n'
                yield 'data: {"message": "\\ud83d\\udce4 R\\u00e9ception de la vid\\u00e9o\\u2026", "stage": "video_upload"}\n\n'
                import hashlib
                hasher = hashlib.sha256()
                try:
                    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
                        video_path_tmp = tmp.name
                        while True:
                            chunk = await _video_upload.read(1024 * 1024)  # 1 MB par chunk
                            if not chunk:
                                break
                            tmp.write(chunk)
                            hasher.update(chunk)
                except Exception as e:
                    yield 'event: error\n'
                    _err = "Réception vidéo échouée : " + str(e)[:200]
                    yield f'data: {json.dumps({"error": _err})}\n\n'
                    return
                if not video_path_tmp or os.path.getsize(video_path_tmp) == 0:
                    yield 'event: error\n'
                    yield 'data: {"error": "Fichier vid\\u00e9o vide."}\n\n'
                    return

                import analysis_cache
                # On ne lit/écrit le cache QUE si l'utilisateur n'a pas fourni
                # de product/price custom — sinon le résultat dépend de ses inputs,
                # pas seulement du contenu vidéo (= risque de retourner le résultat
                # d'un autre user qui avait analysé la même vidéo avec d'autres inputs).
                # user_role est inclus DANS la clé (pas un facteur qui désactive le cache) :
                # même vidéo + rôle différent = résultat différent, donc entrée distincte.
                can_cache = not product and not price
                cache_key = f"{hasher.hexdigest()}:{user_role or 'none'}" if can_cache else None
                if cache_key:
                    cached = analysis_cache.get_cached(cache_key, pipeline="pro")
                    if cached:
                        cached["usage"] = usage_info(user)
                        cached["source"] = "upload"
                        cached["from_cache"] = True
                        yield 'event: progress\n'
                        yield 'data: {"message": "\\u26a1 R\\u00e9sultat trouv\\u00e9 en cache", "stage": "cache_hit"}\n\n'
                        yield 'event: complete\n'
                        yield f'data: {json.dumps(cached)}\n\n'
                        return

                yield 'event: progress\n'
                yield 'data: {"message": "\\ud83c\\udfac Pr\\u00e9paration de la vid\\u00e9o (720p)\\u2026", "stage": "downscale"}\n\n'
                from video_processor import downscale_720p
                downscaled_path = await loop.run_in_executor(None, downscale_720p, video_path_tmp)

                analysis_start = time.time()
                yield 'event: progress\n'
                yield 'data: {"message": "\\ud83c\\udfa5 Analyse approfondie en cours (image + audio)\\u2026", "stage": "vision", "eta_seconds": 60, "info": "L\'analyse Pro prend g\\u00e9n\\u00e9ralement 30 \\u00e0 60 secondes \\u2014 on traite ta vid\\u00e9o enti\\u00e8re (image + audio + d\\u00e9tection CTA)."}\n\n'

                from analyzer import analyze_video_native
                vis_task = loop.run_in_executor(None, analyze_video_native, downscaled_path, product, price)
                _w = 0.0
                while True:
                    _d, _pending = await asyncio.wait({vis_task}, timeout=4.0)
                    if not _pending:
                        break
                    _w += 4.0
                    if _w >= 180:
                        vis_task.cancel()
                        yield 'event: error\n'
                        yield 'data: {"error": "L\'analyse a pris trop longtemps."}\n\n'
                        return
                    yield ': keepalive\n\n'
                try:
                    visual_result = vis_task.result()
                except Exception as e:
                    yield 'event: error\n'
                    yield f'data: {json.dumps({"error": f"Analyse visuelle : {str(e)[:200]}"})}\n\n'
                    return

                transcript = visual_result.get("transcript") if isinstance(visual_result, dict) else None
                detected_product = str(visual_result.get("produit") or "")[:60] if isinstance(visual_result, dict) else ""

                if isinstance(visual_result, dict):
                    partial_payload = {
                        "produit": detected_product,
                        "description_visuelle": str(visual_result.get("description_visuelle") or "")[:400],
                        "qualite_visuelle_score": visual_result.get("qualite_visuelle_score"),
                        "format_visuel_score": visual_result.get("format_visuel_score"),
                        "hook_visuel_score": visual_result.get("hook_visuel_score"),
                        "cta_visuel": visual_result.get("cta_visuel"),
                        "cta_audio": visual_result.get("cta_audio"),
                        "transcript_preview": (transcript or "")[:200],
                    }
                    yield 'event: partial\n'
                    yield f'data: {json.dumps(partial_payload)}\n\n'

                yield 'event: progress\n'
                yield 'data: {"message": "\\ud83e\\udd16 Synth\\u00e8se finale\\u2026", "stage": "synthesis"}\n\n'
                synth_task = loop.run_in_executor(
                    None, synthesize_analysis, visual_result, transcript, market_context, product, tier, price, user_role)
                _w = 0.0
                result = None
                while True:
                    _d, _pending = await asyncio.wait({synth_task}, timeout=4.0)
                    if synth_task in _d:
                        try:
                            result = synth_task.result()
                        except Exception as e:
                            yield 'event: error\n'
                            _err = "Synthèse : " + str(e)[:200]
                            yield f'data: {json.dumps({"error": _err})}\n\n'
                            return
                        break
                    _w += 4.0
                    if _w >= 140:
                        synth_task.cancel()
                        yield 'event: error\n'
                        yield 'data: {"error": "La synth\\u00e8se a pris trop longtemps."}\n\n'
                        return
                    yield ': keepalive\n\n'

                analysis_duration_ms = int((time.time() - analysis_start) * 1000)
                if user["valid"]:
                    increment_usage(user["email"])
                _record_analyzed_product(result)

                result["transcript"] = transcript
                result["pipeline"] = "gemini-pro-native"
                result["cta_visuel"] = visual_result.get("cta_visuel") if isinstance(visual_result, dict) else None
                result["cta_audio"] = visual_result.get("cta_audio") if isinstance(visual_result, dict) else None
                result["usage"] = usage_info(user)
                result["analysis_duration_ms"] = analysis_duration_ms
                result["source"] = "upload"
                result["from_cache"] = False

                try: save_insight(result, product=product, price=price)
                except Exception: pass
                try:
                    winning = build_winning_payload(result, tier, product=product, price=price)
                    if winning: result["structures_gagnantes"] = winning
                except Exception: pass

                # Cache store (uniquement si pas de product/price custom)
                if cache_key:
                    try:
                        analysis_cache.store(cache_key, result, pipeline="pro")
                    except Exception: pass

                # Persiste dans analysis_jobs pour qu'elle apparaisse dans Mes analyses
                _persist_sync_analysis(
                    user, result, source="upload",
                    product=product, price=price,
                    title=product or (getattr(_video_upload, "filename", None) or "Vidéo uploadée"),
                    duration_ms=analysis_duration_ms,
                )

                yield 'event: complete\n'
                yield f'data: {json.dumps(result)}\n\n'
                await _maybe_upsell_free_quota(user)
                return

            # ════════════════════════════════════════════════════════════════
            # PIPELINE LEGACY (Free, ou pas de vidéo uploadée) : frames + AssemblyAI
            # ════════════════════════════════════════════════════════════════
            if audio:
                yield 'event: progress\n'
                yield 'data: {"message": "📥 Audio en cours de traitement...", "stage": "audio_processing"}\n\n'
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    audio_path = tmp.name
                    tmp.write(await audio.read())

            analysis_start = time.time()
            yield 'event: progress\n'
            yield 'data: {"message": "🚀 Lancement analyse parallèle (vision + audio)...", "stage": "parallel_start"}\n\n'

            async def _do_transcribe():
                if not audio_path: return None
                try: return await asyncio.wait_for(loop.run_in_executor(None, transcribe_audio, audio_path), timeout=120.0)
                except asyncio.TimeoutError: return None

            async def _do_visual():
                return await asyncio.wait_for(loop.run_in_executor(None, analyze_visual, frames_list, product, price), timeout=60.0)

            transcript_task = asyncio.create_task(_do_transcribe())
            visual_task = asyncio.create_task(_do_visual())
            yield 'event: progress\n'
            yield 'data: {"message": "🎤 Transcription audio + 👁️ Analyse visuelle en cours...", "stage": "parallel_running"}\n\n'

            # Keepalive pendant vision+transcription (sinon silence jusqu'à 60s →
            # le proxy Render coupe la connexion SSE → "network error" côté client).
            while True:
                _d, _pending = await asyncio.wait({transcript_task, visual_task}, timeout=4.0)
                if not _pending:
                    break
                yield ': keepalive\n\n'
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

            # ── Aperçu progressif : on envoie déjà ce que la vision a vu (produit +
            # scores visuels préliminaires) pour l'afficher AVANT la synthèse finale.
            if isinstance(visual_result, dict):
                partial_payload = {
                    "produit": detected_product,
                    "description_visuelle": str(visual_result.get("description_visuelle") or "")[:400],
                    "qualite_visuelle_score": visual_result.get("qualite_visuelle_score"),
                    "format_visuel_score": visual_result.get("format_visuel_score"),
                    "hook_visuel_score": visual_result.get("hook_visuel_score"),
                }
                yield 'event: partial\n'
                yield f'data: {json.dumps(partial_payload)}\n\n'

            if transcript:
                yield 'event: progress\n'
                yield 'data: {"message": "✅ Transcription complète", "stage": "transcription_done"}\n\n'

            yield 'event: progress\n'
            yield 'data: {"message": "🤖 Synthèse finale (scoring + conseils)...", "stage": "synthesis"}\n\n'

            # Keepalive pendant la synthèse (medium/large peut être long) : un ping
            # toutes les 4s → la connexion n'est jamais muette (pas de coupure proxy).
            synth_task = loop.run_in_executor(
                None, synthesize_analysis, visual_result, transcript, market_context, product, tier, price, user_role)
            _waited = 0.0
            result = None
            while True:
                done, _pending = await asyncio.wait({synth_task}, timeout=4.0)
                if synth_task in done:
                    try:
                        result = synth_task.result()
                    except Exception as e:
                        yield 'event: error\n'
                        yield f'data: {json.dumps({"error": f"Synthèse: {str(e)[:200]}"})}\n\n'
                        return
                    break
                _waited += 4.0
                if _waited >= 140.0:
                    synth_task.cancel()
                    yield 'event: error\n'
                    yield 'data: {"error": "La synthèse a pris trop longtemps."}\n\n'
                    return
                yield ': keepalive\n\n'

            analysis_duration_ms = int((time.time() - analysis_start) * 1000)
            yield 'event: progress\n'
            yield f'data: {json.dumps({"message": f"✅ Analyse complète en {analysis_duration_ms/1000:.1f}s", "stage": "ai_analysis_done"})}\n\n'

            if user["valid"]: increment_usage(user["email"])

            _record_analyzed_product(result)   # 🧠 mémoire produits (anonyme)

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

            # Persiste l'analyse legacy aussi pour qu'elle apparaisse dans Mes analyses
            _persist_sync_analysis(
                user, result, source="upload",
                product=product, price=price,
                title=product or "Vidéo uploadée",
                duration_ms=analysis_duration_ms,
            )

            yield 'event: complete\n'
            yield f'data: {json.dumps(result)}\n\n'

            # Résultat déjà envoyé → on tente l'email d'upsell APRÈS (ne retarde pas l'affichage).
            await _maybe_upsell_free_quota(user)

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
            # Nettoyage des fichiers temporaires du pipeline natif vidéo
            if downscaled_path and downscaled_path != video_path_tmp:
                try: os.unlink(downscaled_path)
                except OSError: pass
            if video_path_tmp:
                try: os.unlink(video_path_tmp)
                except OSError: pass

    return StreamingResponse(stream_analysis(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@app.get("/api/analyze/stream")
async def analyze_stream(request: Request, video_url: str = Query(...), product: Optional[str] = Query(None)):
    if not ai_providers.any_ai_key(): raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")
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


# ════════════════════════════════════════════════════════════════════════════
# ANALYSE PAR LIEN TIKTOK (Pro / Gold / Agency uniquement)
# ════════════════════════════════════════════════════════════════════════════
_URL_ANALYSIS_TIERS = {"pro", "gold", "agency", "beta", "admin"}


def _extract_frames_opencv(video_path: str, n_frames: int = 9) -> list[str]:
    """Extrait n_frames échantillonnées en TEMPS RÉEL (pas en fractions) pour
    capturer le hook (0-3s), le milieu, et surtout le CTA des 2 dernières secondes.

    Le bug précédent : positions fractionnaires (...0.94) ratait systématiquement
    la dernière seconde où apparaît le CTA visuel sur TikTok Shop."""
    import cv2
    import base64
    cap = cv2.VideoCapture(video_path)
    try:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = (total / fps) if (total > 0 and fps > 0) else 0.0
        frames_b64: list[str] = []

        if total <= 0 or duration <= 0:
            # Fallback : lecture séquentielle si le compteur de frames est indisponible
            ok, frame = cap.read()
            while ok and len(frames_b64) < n_frames:
                success, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if success:
                    frames_b64.append(base64.b64encode(buf).decode("utf-8"))
                ok, frame = cap.read()
            return frames_b64

        # Timestamps absolus : hook (0-3s) + milieu + CTA (dernières 2s)
        # Garantit qu'on capte le CTA même sur les vidéos très courtes ou longues.
        timestamps: list[float] = []
        # Hook : 0.5s, 1.5s, 2.5s (les 3 premières secondes = accroche)
        for t in (0.5, 1.5, 2.5):
            if t < duration:
                timestamps.append(t)
        # Milieu : 3 frames réparties entre 3s et (duration-2s)
        mid_start = 3.0
        mid_end = max(duration - 2.0, mid_start + 0.1)
        if mid_end > mid_start:
            for i in range(3):
                timestamps.append(mid_start + (mid_end - mid_start) * i / 2)
        # CTA : dernières 2 secondes — 3 frames pour maximiser la détection
        for offset in (2.0, 1.0, 0.3):
            t = duration - offset
            if t > 0:
                timestamps.append(t)

        # Conversion timestamp → index de frame, dédupliqué et borné
        seen_idx = set()
        for t in timestamps:
            idx = max(0, min(total - 1, int(t * fps)))
            if idx in seen_idx:
                continue
            seen_idx.add(idx)
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ok, frame = cap.read()
            if not ok:
                continue
            success, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if success:
                frames_b64.append(base64.b64encode(buf).decode("utf-8"))
            if len(frames_b64) >= n_frames:
                break
        return frames_b64
    finally:
        cap.release()


@app.post("/analyze-url")
async def analyze_url(request: Request):
    """
    Analyse une vidéo TikTok à partir de son lien — pipeline Pro+ Gemini natif vidéo.

    Pipeline (Pro / Gold / Agency / beta / admin) :
      1. Cache lookup par hash d'URL → hit = retour instantané (0 appel LLM)
      2. yt-dlp download
      3. Downscale 720p (gain temps Gemini)
      4. Gemini Pro vidéo native (visuel + audio en un seul appel)
      5. Synthèse Claude Haiku 4.5 (raisonnement + JSON final)
      6. Stockage cache
    """
    if not ai_providers.any_ai_key():
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
    user_role = (body.get("user_role") or "").strip().lower() or None
    if user_role not in ("affilie", "vendeur"):
        user_role = None
    # Tuyauterie future : stats réelles de la vidéo (ventes/vues) une fois le compte
    # TikTok connecté. None tant que la connexion n'existe pas — passé tel quel au résultat.
    performance = body.get("performance") if isinstance(body.get("performance"), dict) else None
    if not url or not url.lower().startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL TikTok invalide.")
    # Multi-liens (batch) = analyse de patterns → produit/prix facultatifs.

    # ── CACHE LOOKUP : URL identique déjà analysée ? ──
    # On cache UNIQUEMENT quand l'utilisateur n'a pas fourni de product/price
    # custom (sinon le résultat dépend de ses inputs, pas seulement de la vidéo).
    import analysis_cache
    can_cache = not product and not price
    cache_key = f"{analysis_cache.hash_video_url(url)}:{user_role or 'none'}" if can_cache else None
    if cache_key:
        cached = analysis_cache.get_cached(cache_key, pipeline="pro")
        if cached:
            cached["usage"] = usage_info(user)
            cached["source"] = "url"
            cached["source_url"] = url
            cached["from_cache"] = True
            cached["performance"] = performance
            return JSONResponse(cached)

    loop = asyncio.get_event_loop()
    tmpdir = tempfile.mkdtemp(prefix="ttsurl_")
    video_path: Optional[str] = None
    downscaled_path: Optional[str] = None
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

        # ── 3. Downscale 720p (réduit le temps d'upload + processing Gemini) ──
        from video_processor import downscale_720p
        downscaled_path = await loop.run_in_executor(None, downscale_720p, video_path)

        # ── 4. Contexte marché : scraper retiré (données marché via KeyAPI côté UI) ──
        market_context = None

        # ── 5. Pipeline NATIF Gemini Pro vidéo (visuel + audio en un appel) ──
        from analyzer import analyze_video_native
        analysis_start = time.time()
        visual_result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_video_native, downscaled_path, product, price),
            timeout=180.0,  # Gemini Pro sur vidéo complète peut être plus lent que sur frames
        )
        # Le transcript est retourné par Gemini Pro directement
        transcript = visual_result.get("transcript")

        # ── 6. Synthèse via Claude Haiku (provider sélectionné selon tier) ──
        result = await asyncio.wait_for(
            loop.run_in_executor(None, synthesize_analysis, visual_result, transcript, market_context, product, tier, price, user_role),
            timeout=140.0,
        )
        analysis_duration_ms = int((time.time() - analysis_start) * 1000)

        if user["valid"]:
            increment_usage(user["email"])

        _record_analyzed_product(result)   # 🧠 mémoire produits (anonyme)

        # 🎯 Flux URL : on récupère le VRAI product_id taggé dans la vidéo (Video
        # Products) → mémoire produits précise + exposé au front. Best-effort.
        try:
            _nu, _vid = normalize_tiktok_url(url)
            if _vid and _vid != "unknown":
                _vps = await market_creators.get_video_products(_vid)
                if _vps:
                    _vp = _vps[0]
                    _det = result.get("detection") or {}
                    product_store.record_product(
                        supabase_client, product_id=_vp.get("product_id"),
                        name=_det.get("produit"), category=_det.get("categorie_marche"),
                        region=_vp.get("region"), price=_det.get("prix_estime"), sales=_vp.get("sales"))
                    result["video_product"] = _vp
        except Exception as e:
            print(f"video_products enrich error: {e}")

        result["transcript"] = transcript
        result["pipeline"] = "gemini-pro-native"
        result["cta_visuel"] = visual_result.get("cta_visuel")
        result["cta_audio"] = visual_result.get("cta_audio")
        result["usage"] = usage_info(user)
        result["analysis_duration_ms"] = analysis_duration_ms
        result["source"] = "url"
        result["source_url"] = url
        result["performance"] = performance  # None pour l'instant (futur : stats TikTok)
        result["from_cache"] = False

        # Nourrit la base de connaissances (anonymisé) — best effort.
        try: save_insight(result, product=product, price=price)
        except Exception: pass
        # 🏆 Structures gagnantes (Gold/Agency) si score < 75.
        try:
            winning = build_winning_payload(result, tier, product=product, price=price)
            if winning: result["structures_gagnantes"] = winning
        except Exception: pass

        # ── Cache store (seulement si l'utilisateur n'a pas fourni d'input custom) ──
        if cache_key:
            try:
                analysis_cache.store(cache_key, result, pipeline="pro")
            except Exception as e:
                print(f"[analyze-url] cache store error: {e}")

        # Persiste dans analysis_jobs pour qu'elle apparaisse dans Mes analyses
        _persist_sync_analysis(
            user, result, source="url", source_url=url,
            product=product, price=price,
            title=product or url[:60],
            duration_ms=analysis_duration_ms,
        )

        ip = request.client.host if request.client else "unknown"
        security_logger.analyze_ok(ip, 0)  # frames_analyzed n'a plus de sens avec Gemini natif
        return JSONResponse(result)

    finally:
        # ── PROTECTION SERVEUR : nettoie TOUT, quoi qu'il arrive ──
        if semaphore_acquired:
            ANALYSIS_SEMAPHORE.release()
        # Supprimer le fichier downscalé temporaire si différent du path tmpdir
        if downscaled_path and downscaled_path != video_path:
            try:
                os.unlink(downscaled_path)
            except Exception:
                pass
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


@app.post("/analyze-url/stream")
async def analyze_url_stream(request: Request):
    """Analyse 1 lien TikTok en SSE (affichage dynamique : download → vision → synthèse).
    PRO+. Nom produit + prix obligatoires. Additif : ne touche pas /analyze-url (batch)."""
    if not ai_providers.any_ai_key():
        raise HTTPException(status_code=400, detail="Aucune clé IA configurée.")
    user = get_user_from_request(request)
    tier = user.get("tier", "free")
    if not user.get("valid") or tier not in _URL_ANALYSIS_TIERS:
        raise HTTPException(status_code=403, detail="L'analyse par lien est réservée aux plans Pro, Gold et Agency.")
    check_quota(user)
    body = await request.json()
    url = (body.get("url") or "").strip()
    product = (body.get("product") or "").strip() or None
    price = (body.get("price") or "").strip() or None
    user_role = (body.get("user_role") or "").strip().lower() or None
    if user_role not in ("affilie", "vendeur"):
        user_role = None
    if not url or not url.lower().startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL TikTok invalide.")
    if not product or not price:
        raise HTTPException(status_code=422, detail="Le nom du produit et le prix sont obligatoires pour l'analyse par lien.")

    loop = asyncio.get_event_loop()

    async def stream():
        tmpdir = tempfile.mkdtemp(prefix="ttsurls_")
        video_path = None
        downscaled_path = None
        semaphore_acquired = False
        try:
            yield 'event: start\n'
            yield 'data: {"message": "Analyse du lien en cours\\u2026"}\n\n'

            # Annonce d'attente DÈS LE DÉBUT
            yield 'event: progress\n'
            yield 'data: {"message": "\\ud83d\\udd0d Analyse approfondie en cours\\u2026", "stage": "init", "info": "L\'analyse Pro prend g\\u00e9n\\u00e9ralement 30 \\u00e0 60 secondes \\u2014 on traite ta vid\\u00e9o enti\\u00e8re (image + audio + d\\u00e9tection CTA)."}\n\n'

            # ── 0. Cache lookup ──
            # Sur /analyze-url/stream, product et price sont OBLIGATOIRES (gate
            # en amont). Donc le résultat dépend de ces inputs, pas seulement
            # de la vidéo : on désactive le cache pour éviter qu'un user reçoive
            # le résultat d'un autre user qui avait fourni d'autres inputs.
            import analysis_cache
            cache_key = None

            # 1. Téléchargement (keepalive pendant l'attente)
            yield 'event: progress\n'
            yield 'data: {"message": "\\u2b07\\ufe0f T\\u00e9l\\u00e9chargement de la vid\\u00e9o\\u2026", "stage": "download"}\n\n'

            def _download() -> str:
                import yt_dlp
                ydl_opts = {
                    "outtmpl": os.path.join(tmpdir, "video.%(ext)s"),
                    "format": "best[height<=720][ext=mp4]/best[height<=720]/mp4/best",
                    "quiet": True, "no_warnings": True, "noplaylist": True,
                    "max_filesize": 80 * 1024 * 1024,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    return ydl.prepare_filename(info)

            dl_task = loop.run_in_executor(None, _download)
            _w = 0.0
            while True:
                _d, _pending = await asyncio.wait({dl_task}, timeout=4.0)
                if not _pending:
                    break
                _w += 4.0
                if _w >= 60:
                    dl_task.cancel()
                    yield 'event: error\n'
                    yield 'data: {"error": "Le t\\u00e9l\\u00e9chargement a pris trop longtemps."}\n\n'
                    return
                yield ': keepalive\n\n'
            try:
                video_path = dl_task.result()
            except Exception as e:
                yield 'event: error\n'
                yield f'data: {json.dumps({"error": f"Impossible de récupérer cette vidéo : {str(e)[:160]}"})}\n\n'
                return
            if not video_path or not os.path.exists(video_path):
                yield 'event: error\n'
                yield 'data: {"error": "Vid\\u00e9o introuvable apr\\u00e8s t\\u00e9l\\u00e9chargement."}\n\n'
                return

            await ANALYSIS_SEMAPHORE.acquire()
            semaphore_acquired = True

            # 2. Downscale 720p (économise upload + processing Gemini)
            yield 'event: progress\n'
            yield 'data: {"message": "\\ud83c\\udfac Pr\\u00e9paration de la vid\\u00e9o (720p)\\u2026", "stage": "downscale"}\n\n'
            from video_processor import downscale_720p
            downscaled_path = await loop.run_in_executor(None, downscale_720p, video_path)

            analysis_start = time.time()

            # 3. Gemini Pro vidéo native : visuel + audio en un seul appel
            yield 'event: progress\n'
            yield 'data: {"message": "\\ud83c\\udfa5 Analyse approfondie de la vid\\u00e9o (image + audio)\\u2026", "stage": "vision", "eta_seconds": 60, "info": "L\'analyse Pro prend g\\u00e9n\\u00e9ralement 30 \\u00e0 60 secondes \\u2014 on traite ta vid\\u00e9o enti\\u00e8re (image + audio + d\\u00e9tection CTA)."}\n\n'
            from analyzer import analyze_video_native
            vis_task = loop.run_in_executor(None, analyze_video_native, downscaled_path, product, price)
            _w = 0.0
            while True:
                _d, _pending = await asyncio.wait({vis_task}, timeout=4.0)
                if not _pending:
                    break
                _w += 4.0
                if _w >= 180:
                    vis_task.cancel()
                    yield 'event: error\n'
                    yield 'data: {"error": "L\'analyse Gemini a pris trop longtemps."}\n\n'
                    return
                yield ': keepalive\n\n'
            try:
                visual_result = vis_task.result()
            except Exception as e:
                yield 'event: error\n'
                yield f'data: {json.dumps({"error": f"Analyse visuelle : {str(e)[:160]}"})}\n\n'
                return
            transcript = visual_result.get("transcript") if isinstance(visual_result, dict) else None
            detected_product = str(visual_result.get("produit") or "")[:60] if isinstance(visual_result, dict) else ""
            if isinstance(visual_result, dict):
                partial_payload = {
                    "produit": detected_product,
                    "description_visuelle": str(visual_result.get("description_visuelle") or "")[:400],
                    "qualite_visuelle_score": visual_result.get("qualite_visuelle_score"),
                    "format_visuel_score": visual_result.get("format_visuel_score"),
                    "hook_visuel_score": visual_result.get("hook_visuel_score"),
                    "cta_visuel": visual_result.get("cta_visuel"),
                    "cta_audio": visual_result.get("cta_audio"),
                    "transcript_preview": (transcript or "")[:200],
                }
                yield 'event: partial\n'
                yield f'data: {json.dumps(partial_payload)}\n\n'

            # 4. Synthèse (keepalive)
            yield 'event: progress\n'
            yield 'data: {"message": "\\ud83e\\udd16 Synth\\u00e8se finale (scoring + conseils)\\u2026", "stage": "synthesis"}\n\n'
            synth_task = loop.run_in_executor(
                None, synthesize_analysis, visual_result, transcript, None, product, tier, price, user_role)
            _w = 0.0
            result = None
            while True:
                _d, _pending = await asyncio.wait({synth_task}, timeout=4.0)
                if synth_task in _d:
                    try:
                        result = synth_task.result()
                    except Exception as e:
                        yield 'event: error\n'
                        yield f'data: {json.dumps({"error": f"Synthèse : {str(e)[:200]}"})}\n\n'
                        return
                    break
                _w += 4.0
                if _w >= 140:
                    synth_task.cancel()
                    yield 'event: error\n'
                    yield 'data: {"error": "La synth\\u00e8se a pris trop longtemps."}\n\n'
                    return
                yield ': keepalive\n\n'

            dur = int((time.time() - analysis_start) * 1000)
            if user["valid"]:
                increment_usage(user["email"])
            _record_analyzed_product(result)
            try:
                _nu, _vid = normalize_tiktok_url(url)
                if _vid and _vid != "unknown":
                    _vps = await market_creators.get_video_products(_vid)
                    if _vps:
                        result["video_products"] = _vps
            except Exception:
                pass
            result["transcript"] = transcript
            result["pipeline"] = "gemini-pro-native"
            result["cta_visuel"] = visual_result.get("cta_visuel") if isinstance(visual_result, dict) else None
            result["cta_audio"] = visual_result.get("cta_audio") if isinstance(visual_result, dict) else None
            result["usage"] = usage_info(user)
            result["analysis_duration_ms"] = dur
            result["source"] = "url"
            result["source_url"] = url
            result["from_cache"] = False
            # Persiste dans analysis_jobs pour qu'elle apparaisse dans Mes analyses
            _persist_sync_analysis(
                user, result, source="url", source_url=url,
                product=product, price=price,
                title=product or url[:60], duration_ms=dur,
            )
            # Pas de store en cache : product/price obligatoires sur cet endpoint
            # donc le résultat est trop spécifique à l'utilisateur pour être partagé.
            try:
                await save_to_cache(normalize_tiktok_url(url)[0], result, dur, product_id=product)
            except Exception:
                pass
            try:
                save_insight(result, product=product, price=price)
            except Exception:
                pass
            try:
                winning = build_winning_payload(result, tier, product=product, price=price)
                if winning:
                    result["structures_gagnantes"] = winning
            except Exception:
                pass
            yield 'event: complete\n'
            yield f'data: {json.dumps(result)}\n\n'
        except Exception as e:
            yield 'event: error\n'
            yield f'data: {json.dumps({"error": str(e)})}\n\n'
        finally:
            if semaphore_acquired:
                ANALYSIS_SEMAPHORE.release()
            # Supprimer le fichier downscalé temporaire si différent du path tmpdir
            if downscaled_path and downscaled_path != video_path:
                try:
                    os.unlink(downscaled_path)
                except Exception:
                    pass
            try:
                import shutil
                shutil.rmtree(tmpdir, ignore_errors=True)
            except Exception:
                pass
            try:
                import gc
                gc.collect()
            except Exception:
                pass

    return StreamingResponse(stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ════════════════════════════════════════════════════════════════════════════
# ANALYSE ASYNCHRONE (Pro+) — soumets, ferme l'onglet, reviens voir le résultat
# ════════════════════════════════════════════════════════════════════════════
# Architecture : POST /api/jobs/create renvoie un job_id immédiatement, le
# traitement tourne en background (asyncio.create_task), le frontend poll
# GET /api/jobs/{id} jusqu'à status='done' ou 'error'.
# Sécurité : ownership vérifiée à chaque GET/list par user_email.


@app.post("/api/jobs/create-url")
async def jobs_create_url(request: Request):
    """Crée un job d'analyse à partir d'une URL TikTok. Renvoie {job_id}."""
    if not ai_providers.any_ai_key():
        raise HTTPException(status_code=400, detail="Aucune clé IA configurée.")
    user = get_user_from_request(request)
    tier = user.get("tier", "free")
    if not user.get("valid") or tier not in _URL_ANALYSIS_TIERS:
        raise HTTPException(status_code=403, detail="L'analyse par lien est réservée aux plans Pro, Gold et Agency.")
    check_quota(user)

    body = await request.json()
    url = (body.get("url") or "").strip()
    product = (body.get("product") or "").strip() or None
    price = (body.get("price") or "").strip() or None
    user_role = (body.get("user_role") or "").strip().lower() or None
    if user_role not in ("affilie", "vendeur"):
        user_role = None
    if not url or not url.lower().startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL TikTok invalide.")
    if not product or not price:
        raise HTTPException(status_code=422, detail="Le nom du produit et le prix sont obligatoires.")

    import analysis_jobs as _jobs
    import analysis_runner as _runner
    title = f"{product[:40]}" if product else "Analyse vidéo"
    job_id = _jobs.create_job(
        user_email=user["email"], source="url", source_url=url,
        product=product, price=price, title=title,
    )
    if not job_id:
        raise HTTPException(status_code=500, detail="Impossible de créer le job (Supabase indisponible).")

    # Quota déduit dès la création (sinon spam possible avant fin du job)
    if user["valid"]:
        increment_usage(user["email"])

    # Lance le traitement en background (continue après le return de l'endpoint)
    asyncio.create_task(_runner.process_url_job(
        job_id=job_id, url=url, product=product, price=price,
        user_tier=tier, user_email=user["email"], job_title=title,
        user_role=user_role,
    ))
    return JSONResponse({"job_id": job_id, "status": "queued"})


@app.post("/api/jobs/create-upload")
async def jobs_create_upload(
    request: Request,
    video: UploadFile = File(...),
    product: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    user_role: Optional[str] = Form(None),
):
    """Crée un job d'analyse à partir d'un upload vidéo. Renvoie {job_id}."""
    if not ai_providers.any_ai_key():
        raise HTTPException(status_code=400, detail="Aucune clé IA configurée.")
    user = get_user_from_request(request)
    tier = user.get("tier", "free")
    if not user.get("valid") or tier not in {"pro", "gold", "agency", "beta", "admin"}:
        raise HTTPException(status_code=403, detail="L'analyse asynchrone est réservée aux plans Pro, Gold et Agency.")
    check_quota(user)

    # Stream → tmpfile sur disque, JAMAIS la vidéo entière en RAM (Render 512 MB :
    # plusieurs jobs concurrents × 5-30 MB de bytes retenus pendant toute la durée
    # du job = OOM). Le worker reçoit le path et supprime le fichier en fin de job.
    import hashlib
    hasher = hashlib.sha256()
    video_tmp_path: Optional[str] = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            video_tmp_path = tmp.name
            while True:
                chunk = await video.read(1024 * 1024)
                if not chunk:
                    break
                tmp.write(chunk)
                hasher.update(chunk)
    except Exception as e:
        if video_tmp_path:
            try: os.unlink(video_tmp_path)
            except Exception: pass
        raise HTTPException(status_code=400, detail=f"Lecture vidéo échouée : {str(e)[:200]}")
    if not video_tmp_path or os.path.getsize(video_tmp_path) == 0:
        if video_tmp_path:
            try: os.unlink(video_tmp_path)
            except Exception: pass
        raise HTTPException(status_code=400, detail="Fichier vidéo vide.")
    video_hash = hasher.hexdigest()

    p = (product or "").strip() or None
    pr = (price or "").strip() or None
    ur = (user_role or "").strip().lower() or None
    if ur not in ("affilie", "vendeur"):
        ur = None

    import analysis_jobs as _jobs
    import analysis_runner as _runner
    title = (p or (video.filename or "Vidéo uploadée"))[:60]
    job_id = _jobs.create_job(
        user_email=user["email"], source="upload",
        product=p, price=pr, video_hash=video_hash, title=title,
    )
    if not job_id:
        raise HTTPException(status_code=500, detail="Impossible de créer le job.")

    if user["valid"]:
        increment_usage(user["email"])

    asyncio.create_task(_runner.process_upload_job(
        job_id=job_id, video_path=video_tmp_path, product=p, price=pr,
        user_tier=tier, user_email=user["email"], video_hash=video_hash,
        job_title=title, user_role=ur,
    ))
    return JSONResponse({"job_id": job_id, "status": "queued"})


@app.get("/api/jobs/{job_id}")
async def jobs_get(job_id: str, request: Request):
    """Status + résultat d'un job. Ownership vérifiée par user_email."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    import analysis_jobs as _jobs
    job = _jobs.get_job(job_id, user_email=user["email"])
    if not job:
        raise HTTPException(status_code=404, detail="Job introuvable ou ne vous appartient pas.")
    # On ne retourne pas le video_hash brut (interne)
    job.pop("video_hash", None)
    return JSONResponse(job)


@app.get("/api/jobs")
async def jobs_list(request: Request, limit: int = 20):
    """Historique des N derniers jobs de l'utilisateur connecté."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    import analysis_jobs as _jobs
    limit = max(1, min(int(limit or 20), 100))
    return JSONResponse({"jobs": _jobs.list_user_jobs(user["email"], limit=limit)})


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
    if not ai_providers.any_ai_key():
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
# OAUTH GOOGLE — connexion « Continuer avec Google » (login / inscription)
# ════════════════════════════════════════════════════════════════════════════
def _google_host_base(request: Request) -> str:
    """Host RÉEL de l'utilisateur (www.qeerah.com), depuis les en-têtes proxy.
    Essentiel : garder tout le flux OAuth sur le même host évite le 301
    qeerah.com↔www.qeerah.com au milieu de l'échange (qui casse la connexion)."""
    host = (request.headers.get("x-forwarded-host") or request.headers.get("host")
            or request.url.hostname or "")
    proto = request.headers.get("x-forwarded-proto") or "https"
    return f"{proto}://{host}".rstrip("/")


def _google_redirect_uri(request: Request) -> str:
    forced = os.getenv("GOOGLE_REDIRECT_URI")
    return forced if forced else f"{_google_host_base(request)}/api/auth/google/callback"


@app.get("/api/auth/google/login")
async def google_login(request: Request):
    """Démarre le flux Google et redirige vers l'écran de consentement."""
    if not google_oauth.is_configured():
        raise HTTPException(status_code=503,
                            detail="Connexion Google indisponible (configuration manquante).")
    ru = _google_redirect_uri(request)
    return RedirectResponse(google_oauth.build_authorize_url(google_oauth.make_state(), ru))


@app.get("/api/auth/google/callback")
async def google_callback(request: Request, code: Optional[str] = Query(None),
                          state: Optional[str] = Query(None)):
    """Callback Google : vérifie le state → email vérifié → user + token → /app.
    redirect_uri reconstruit depuis le MÊME host qu'à l'autorisation (cohérence)."""
    app_url = _google_host_base(request) or google_oauth.APP_PUBLIC_URL
    if not code or not state or not google_oauth.verify_state(state):
        return RedirectResponse(f"{app_url}/app?gauth=error&reason=state")
    try:
        email = await google_oauth.exchange_code_for_email(code, _google_redirect_uri(request))
    except Exception as e:
        print(f"❌ Google OAuth exchange failed: {e}")
        return RedirectResponse(f"{app_url}/app?gauth=error&reason=exchange")
    if not email:
        return RedirectResponse(f"{app_url}/app?gauth=error&reason=email")
    try:
        from supabase_client import get_or_create_user
        get_or_create_user(email)          # crée le compte s'il n'existe pas (tier free)
    except Exception as e:
        print(f"google_callback get_or_create_user warn: {e}")
    token = create_access_token(email)
    # Token en FRAGMENT (#) : jamais envoyé au serveur ni journalisé (contrairement à ?).
    return RedirectResponse(f"{app_url}/app#gauth={token}")


# ════════════════════════════════════════════════════════════════════════════
# OAUTH TIKTOK — 2 providers : "display" (vidéos+perfs) & "business" (audience)
# ════════════════════════════════════════════════════════════════════════════
_TIKTOK_PROVIDERS = {"display", "business"}


@app.get("/api/auth/tiktok/login")
async def tiktok_login(request: Request, provider: str = Query("display")):
    """Démarre l'autorisation TikTok et renvoie l'URL (le frontend redirige)."""
    provider = provider if provider in _TIKTOK_PROVIDERS else "display"
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    if not tiktok_oauth.is_configured(provider):
        raise HTTPException(
            status_code=503,
            detail="Connexion TikTok indisponible (configuration manquante).",
        )
    state = tiktok_oauth.make_state(user["email"], provider)
    return {"authorize_url": tiktok_oauth.build_authorize_url(state, provider)}


@app.get("/api/auth/tiktok/callback")
async def tiktok_callback(
    request: Request,
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
):
    """Callback OAuth (commun aux 2 providers) : vérifie le state → échange → sauve."""
    app_url = tiktok_oauth.APP_PUBLIC_URL

    if not code or not state:
        return RedirectResponse(f"{app_url}/app?tiktok=error&reason=missing_params")

    email, provider = tiktok_oauth.verify_state(state)
    if not email:
        return RedirectResponse(f"{app_url}/app?tiktok=error&reason=invalid_state")
    provider = provider or "display"

    try:
        token_data = await tiktok_oauth.exchange_code_for_token(code, provider)
    except Exception as e:
        print(f"❌ TikTok token exchange failed ({provider}): {e}")
        return RedirectResponse(f"{app_url}/app?tiktok=error&reason=exchange_failed")

    saved = tiktok_oauth.save_tiktok_token(email, token_data, provider)
    status = "connected" if saved else "warn_not_saved"
    return RedirectResponse(f"{app_url}/app?tiktok={status}&provider={provider}")


@app.get("/api/tiktok/me")
async def tiktok_me(request: Request):
    """Profil + vidéos (métriques réelles) du compte TikTok connecté (display)."""
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


@app.get("/api/tiktok/insights")
async def tiktok_insights(request: Request):
    """Insights d'audience (démographie) via le provider business."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    try:
        data = await tiktok_oauth.get_audience_insights(user["email"])
    except Exception as e:
        print(f"/api/tiktok/insights error: {e}")
        data = None
    if not data:
        return {"connected": False}
    return {"connected": True, "insights": data}


@app.get("/api/auth/tiktok/status")
async def tiktok_status(request: Request):
    """État des connexions TikTok de l'utilisateur (par provider)."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    out = {"connected": False, "providers": {}}
    if not supabase_client:
        return out
    try:
        resp = (
            supabase_client.table("tiktok_tokens")
            .select("provider,seller_name,open_id,access_token_expires_at")
            .eq("email", user["email"])
            .execute()
        )
        for row in (resp.data or []):
            prov = row.get("provider") or "display"
            connected = bool(row.get("access_token_expires_at"))
            out["providers"][prov] = {"connected": connected, "seller_name": row.get("seller_name")}
            if prov == "display" and connected:
                out["connected"] = True
                out["seller_name"] = row.get("seller_name")
    except Exception:
        pass
    return out


# ════════════════════════════════════════════════════════════════════════════
# MARCHÉ — Créateurs Gagnants (Gold/Agency) — KeyAPI créateur-centric
# ════════════════════════════════════════════════════════════════════════════
_MARKET_PREMIUM_TIERS = {"gold", "agency", "beta", "admin"}


# Version du cache marché : on l'incrémente pour invalider TOUTES les entrées d'un
# coup quand la logique KeyAPI change (params, filtres…). v2 = filtre category_id +
# product_rank_field + ventes période + avatars echosell.
_MARKET_CACHE_VER = "v2"


def _market_cache_get(key: str):
    if not supabase_client:
        return None
    key = f"{_MARKET_CACHE_VER}:{key}"
    try:
        r = supabase_client.table("market_cache").select("payload,expires_at").eq("cache_key", key).execute()
        if r.data:
            from datetime import datetime as _dt
            exp = r.data[0].get("expires_at")
            if exp:
                exp_dt = _dt.fromisoformat(str(exp).replace("Z", "+00:00"))
                now = _dt.now(exp_dt.tzinfo) if exp_dt.tzinfo else _dt.now()
                if now < exp_dt:
                    return r.data[0].get("payload")
    except Exception:
        pass
    return None


def _market_cache_set(key: str, payload, hours: int = 24):
    if not supabase_client:
        return
    key = f"{_MARKET_CACHE_VER}:{key}"
    try:
        supabase_client.table("market_cache").upsert({
            "cache_key": key,
            "payload": payload,
            "expires_at": (datetime.now() + timedelta(hours=hours)).isoformat(),
        }, on_conflict="cache_key").execute()
    except Exception:
        pass


@app.get("/api/market/creators")
async def market_creators_list(request: Request, category: Optional[str] = Query(None), region: str = Query("US")):
    """Top créateurs (ventes). Gold/Agency = complet ; free/pro = aperçu partiel flouté."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    premium = (user.get("tier") or "free").lower() in _MARKET_PREMIUM_TIERS

    cache_key = f"creators::{(category or 'all').lower()}::{region}"
    creators = _market_cache_get(cache_key)
    if creators is None:
        try:
            creators = await market_creators.get_top_creators(category, region, limit=10)
        except Exception as e:
            print(f"/api/market/creators error: {e}")
            return JSONResponse({"ok": False, "error": str(e), "creators": []}, status_code=502)
        if creators:
            _market_cache_set(cache_key, creators, hours=24)  # 24h : URLs avatars TikTok signées expirent ~24h

    if not premium:
        return {"ok": True, "preview": True, "creators": (creators or [])[:2]}
    return {"ok": True, "preview": False, "creators": creators or []}


@app.get("/api/market/category")
async def market_category_overview(request: Request, category: Optional[str] = Query(None), region: str = Query("US")):
    """Vue catégorie (créateurs + produits) pour la reco auto post-analyse.
    Gold/Agency = complet ; free/pro = aperçu partiel (preview=True)."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    premium = (user.get("tier") or "free").lower() in _MARKET_PREMIUM_TIERS

    cache_key = f"catov::{(category or 'all').lower()}::{region}"
    ov = _market_cache_get(cache_key)
    if ov is None:
        try:
            ov = await market_creators.get_category_overview(category, region)
        except Exception as e:
            print(f"/api/market/category error: {e}")
            return JSONResponse({"ok": False, "error": str(e)}, status_code=502)
        if ov and (ov.get("creators") or ov.get("products")):
            _market_cache_set(cache_key, ov, hours=24)  # 24h : contient avatars/images signés (expirent ~24h)

    ov = ov or {"creators": [], "products": []}
    if not premium:
        return {"ok": True, "preview": True,
                "creators": (ov.get("creators") or [])[:2],
                "products": (ov.get("products") or [])[:2]}
    return {"ok": True, "preview": False,
            "creators": ov.get("creators") or [], "products": ov.get("products") or []}


@app.get("/api/market/creator/{unique_id}")
async def market_creator_detail(request: Request, unique_id: str, user_id: str = Query(...)):
    """Vidéos + produits d'un créateur. Réservé Gold/Agency."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    if (user.get("tier") or "free").lower() not in _MARKET_PREMIUM_TIERS:
        raise HTTPException(status_code=403, detail="Réservé aux plans Gold et Agency.")

    cache_key = f"creator::{unique_id}::{user_id}"
    detail = _market_cache_get(cache_key)
    if detail is None:
        try:
            detail = await market_creators.get_creator_detail(unique_id, user_id)
        except Exception as e:
            print(f"/api/market/creator error: {e}")
            return JSONResponse({"ok": False, "error": str(e)}, status_code=502)
        _market_cache_set(cache_key, detail, hours=12)
    return {"ok": True, **(detail or {})}


@app.get("/api/market/video-products")
async def market_video_products(request: Request, video_id: str = Query(...),
                                region: Optional[str] = Query(None), token: Optional[str] = Query(None)):
    """Produit(s) réellement taggé(s) dans une vidéo (Video Products Analytics).
    Sert à valider les params. Auth via header OU ?token= (test navigateur)."""
    ok = False
    try:
        u = get_user_from_request(request)
        ok = bool(u.get("valid") and ((u.get("tier") or "free").lower() in _MARKET_PREMIUM_TIERS or u.get("is_admin")))
    except Exception:
        ok = False
    if not ok and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            email = verify_access_token(token.replace(" ", "+"))
            ok = bool(email and ADMIN_EMAIL and email.lower() == ADMIN_EMAIL)
        except Exception:
            ok = False
    if not ok:
        raise HTTPException(status_code=403, detail="Réservé aux plans Gold et Agency.")
    try:
        products = await market_creators.get_video_products(video_id, region)
    except Exception as e:
        print(f"/api/market/video-products error: {e}")
        return JSONResponse({"ok": False, "error": str(e), "products": []}, status_code=502)
    return {"ok": True, "video_id": video_id, "count": len(products), "products": products}


@app.get("/api/market/popular")
async def market_popular(request: Request, category: Optional[str] = Query(None)):
    """Reco « populaire chez nos utilisateurs » : produits les plus récurrents dans
    notre base d'analyses (signal maison). Premium. Se bonifie au fil du temps."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    if not ((user.get("tier") or "free").lower() in _MARKET_PREMIUM_TIERS or user.get("is_admin")):
        raise HTTPException(status_code=403, detail="Réservé aux plans Gold et Agency.")
    rows = product_store.get_popular(supabase_client, category=category, limit=8)
    products = [{
        "id": r.get("product_id"),
        "name": r.get("product_name") or "Produit",
        "categorie": r.get("categorie"),
        "times_seen": r.get("times_seen") or 1,
        "price": r.get("price"),
        "url": (f"https://www.tiktok.com/view/product/{r.get('product_id')}" if r.get("product_id")
                else f"https://www.tiktok.com/search?q={quote(r.get('product_name') or '')}"),
    } for r in rows]
    return {"ok": True, "products": products}


@app.get("/api/market/category-creators")
async def market_category_creators(request: Request, category: Optional[str] = Query(None), region: str = Query("US")):
    """Créateurs gagnants d'une catégorie (chaîne top produits → leurs créateurs).
    Gold/Agency = complet ; free/pro = aperçu partiel. Cache 24h."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    premium = (user.get("tier") or "free").lower() in _MARKET_PREMIUM_TIERS or user.get("is_admin")

    cache_key = f"catcr::{(category or 'all').lower()}::{region}"
    creators = _market_cache_get(cache_key)
    if creators is None:
        try:
            creators = await market_creators.get_category_creators(category, region, limit=8)
        except Exception as e:
            print(f"/api/market/category-creators error: {e}")
            return JSONResponse({"ok": False, "error": str(e), "creators": []}, status_code=502)
        if creators:
            _market_cache_set(cache_key, creators, hours=24)

    creators = creators or []
    if not premium:
        return {"ok": True, "preview": True, "creators": creators[:2]}
    return {"ok": True, "preview": False, "creators": creators}


@app.get("/api/market/products/search")
async def market_products_search(request: Request, keyword: str = Query(...), region: str = Query("US")):
    """Produits tendance pour un mot-clé (reco « produits similaires en tendance »).
    Gold/Agency = complet ; free/pro = aperçu partiel flouté. Cache 7j (realtime → on limite la conso)."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    premium = (user.get("tier") or "free").lower() in _MARKET_PREMIUM_TIERS

    cache_key = f"psearch::{keyword.lower().strip()}::{region}"
    products = _market_cache_get(cache_key)
    if products is None:
        try:
            products = await market_creators.search_products(keyword, region, limit=8)
        except Exception as e:
            print(f"/api/market/products/search error: {e}")
            return JSONResponse({"ok": False, "error": str(e), "products": []}, status_code=502)
        if products:
            _market_cache_set(cache_key, products, hours=24)  # images produits signées (expirent ~24h)

    products = products or []
    if not premium:
        return {"ok": True, "preview": True, "products": products[:2]}
    return {"ok": True, "preview": False, "products": products}


@app.get("/api/market/product/{product_id}")
async def market_product_detail(request: Request, product_id: str, region: str = Query("US")):
    """Fiche produit réelle (titre, image, prix, ventes, VRAIE URL). Réservé Gold/Agency. Cache 7j."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    if (user.get("tier") or "free").lower() not in _MARKET_PREMIUM_TIERS:
        raise HTTPException(status_code=403, detail="Réservé aux plans Gold et Agency.")

    cache_key = f"pdetail::{product_id}::{region}"
    detail = _market_cache_get(cache_key)
    if detail is None:
        try:
            detail = await market_creators.get_product_detail(product_id, region)
        except Exception as e:
            print(f"/api/market/product error: {e}")
            return JSONResponse({"ok": False, "error": str(e)}, status_code=502)
        if detail:
            _market_cache_set(cache_key, detail, hours=168)
    if not detail:
        return JSONResponse({"ok": False, "error": "introuvable"}, status_code=404)
    return {"ok": True, "product": detail}


# ════════════════════════════════════════════════════════════════════════════
# RECHERCHE DE PROFIL TIKTOK — recherche libre par @handle (GMV réel 30j +
# meilleures ventes). Pro (10/jour) / Gold+/Agency/Beta/Admin (illimité).
# Free = bloqué. Distinct de "Créateurs Gagnants" (qui part d'un ranking) :
# ici l'utilisateur tape n'importe quel handle, même hors ranking.
# ════════════════════════════════════════════════════════════════════════════
@app.get("/api/recherche/profile")
async def recherche_profile(request: Request, handle: str = Query(...)):
    """Profil + GMV réel 30 derniers jours + meilleures ventes pour un @handle."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    recherche_quota.check_recherche_quota(user)  # 403 free / 429 pro épuisé / no-op gold+

    handle_clean = (handle or "").lstrip("@").strip().lower()
    if not handle_clean:
        raise HTTPException(status_code=422, detail="Handle manquant.")

    cache_key = f"recherche::{handle_clean}"
    result = _market_cache_get(cache_key)
    is_fresh_fetch = result is None
    if result is None:
        try:
            result = await market_creators.search_creator_profile(handle_clean)
        except Exception as e:
            print(f"/api/recherche/profile error: {e}")
            return JSONResponse({"ok": False, "error": str(e)}, status_code=502)
        if result is None:
            # Handle introuvable : jamais mis en cache (évite de figer une erreur transitoire).
            return JSONResponse({"ok": False, "error": "Profil introuvable."}, status_code=404)
        _market_cache_set(cache_key, result, hours=8)  # 8h : compromis fraîcheur GMV / coût crédits

    tier = (user.get("tier") or "free").lower()
    quota_info = {"tier": tier, "remaining_today": None, "limit": None}
    if tier == "pro":
        # Le quota ne compte QUE les vrais appels KeyAPI, jamais un résultat déjà en cache.
        if is_fresh_fetch:
            recherche_quota.increment_recherche_count(user["email"])
        remaining = max(0, recherche_quota.PRO_DAILY_LIMIT - recherche_quota.get_recherche_count_today(user["email"]))
        quota_info = {"tier": "pro", "remaining_today": remaining, "limit": recherche_quota.PRO_DAILY_LIMIT}

    return {"ok": True, **result, "quota": quota_info}


# ════════════════════════════════════════════════════════════════════════════
# FEED RADAR — feed de vidéos TikTok Shop virales (≥ seuil de vues), thumbnail
# oEmbed officiel, GMV estimé (calcul), tendance créateur. Même gating que
# "Créateurs Gagnants" : Gold/Agency/Beta/Admin complet, Free/Pro = aperçu 3.
# ════════════════════════════════════════════════════════════════════════════
@app.get("/api/feed-radar")
async def feed_radar_list(request: Request, region: str = Query("US"), limit: int = Query(24),
                          carousel_only: bool = Query(False)):
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    premium = (user.get("tier") or "free").lower() in _MARKET_PREMIUM_TIERS

    import random
    _base_cols = ("video_id,video_url,creator_unique_id,creator_nickname,region,views,likes,"
                  "comments,shares,oembed_thumbnail_url,oembed_author_name,trend_snapshot,"
                  "gmv_estimated,gmv_estimation_method,collected_at")
    # On récupère un POOL plus large des meilleures vues, puis on en tire un
    # échantillon aléatoire → variété à chaque visite tout en restant sur des
    # posts performants (l'utilisateur voyait toujours les mêmes 24 sinon).
    pool = max(limit * 5, 80)
    try:
        q = (supabase_client.table("feed_radar_videos")
             .select(_base_cols + ",is_carousel,image_count")
             .eq("region", region).order("views", desc=True).limit(pool))
        if carousel_only:
            q = q.eq("is_carousel", True)   # carrousels photo à fortes vues uniquement
        rows = q.execute().data or []
    except Exception as e:
        # Migration supabase_migrations_feed_radar_carousel.sql pas encore appliquée :
        # colonnes is_carousel/image_count absentes → on retombe sur l'ancien schéma
        # pour ne jamais casser le Feed Radar. Le filtre carrousel est alors inopérant.
        print(f"/api/feed-radar carousel-cols fallback: {e}")
        try:
            rows = (supabase_client.table("feed_radar_videos").select(_base_cols)
                    .eq("region", region).order("views", desc=True).limit(pool)
                    .execute().data or [])
        except Exception as e2:
            print(f"/api/feed-radar error: {e2}")
            return JSONResponse({"ok": False, "error": str(e2), "videos": []}, status_code=502)

    random.shuffle(rows)
    if not premium:
        return {"ok": True, "preview": True, "region": region, "videos": rows[:3]}
    return {"ok": True, "preview": False, "region": region, "videos": rows[:limit]}


@app.get("/api/feed-radar/{video_id}/embed")
async def feed_radar_video_embed(request: Request, video_id: str):
    """Blockquote oEmbed complet pour hydratation au TAP (jamais au scroll)."""
    user = get_user_from_request(request)
    if not user.get("valid") or (user.get("tier") or "free").lower() not in _MARKET_PREMIUM_TIERS:
        raise HTTPException(status_code=403, detail="Réservé aux plans Gold et Agency.")
    try:
        r = supabase_client.table("feed_radar_videos").select("oembed_html,oembed_fetched_at,video_url") \
            .eq("video_id", video_id).execute()
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=502)
    if not r.data:
        return JSONResponse({"ok": False, "error": "Vidéo introuvable"}, status_code=404)
    return {"ok": True, **r.data[0]}


@app.get("/api/feed-radar/teaser")
async def feed_radar_teaser(region: Optional[str] = Query(None)):
    """3 vidéos top pour la homepage publique. Pas d'auth. Cache 6h.
    Filtré par région du visiteur si fournie ; repli sur le top global si
    cette région n'a pas encore de données collectées."""
    region = (region or "").strip().upper() or None
    cache_key = f"feedradar::teaser::{region or 'all'}"
    teaser = _market_cache_get(cache_key)
    if teaser is None:
        try:
            cols = "video_id,oembed_thumbnail_url,oembed_author_name,views,gmv_estimated"
            teaser = []
            if region:
                teaser = (supabase_client.table("feed_radar_videos").select(cols)
                          .eq("region", region).order("views", desc=True).limit(3)
                          .execute().data or [])
            if not teaser:
                teaser = (supabase_client.table("feed_radar_videos").select(cols)
                          .order("views", desc=True).limit(3).execute().data or [])
        except Exception as e:
            print(f"/api/feed-radar/teaser error: {e}")
            teaser = []
        _market_cache_set(cache_key, teaser, hours=6)
    return {"ok": True, "videos": teaser or []}


@app.post("/api/photo-slide/generate")
async def photo_slide_generate(
    request: Request,
    image: str = Form(...),                       # image produit en base64 (sans préfixe data:)
    product_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    currency: str = Form("EUR"),
    niche: Optional[str] = Form(None),
    preferred_style: Optional[str] = Form(None),  # auto | quad_photo | fond_blanc | ia_cartoon
):
    """📸 Photo Slide Coach — plan de carrousel TikTok Shop. Réservé Gold/Agency."""
    if not ai_providers.any_ai_key():
        raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    premium = (user.get("tier") or "free").lower() in _MARKET_PREMIUM_TIERS or user.get("is_admin")
    if not premium:
        raise HTTPException(status_code=403, detail="Réservé aux plans Gold et Agency.")

    img = (image or "").strip()
    if "," in img and img.lower().startswith("data:"):
        img = img.split(",", 1)[1]              # tolère un data-URL complet
    if not img:
        raise HTTPException(status_code=400, detail="Image produit manquante.")

    async def stream():
        loop = asyncio.get_event_loop()

        async def _run(fn, timeout):
            """Exécute fn dans un thread en envoyant un keepalive toutes les 4s.
            Renvoie un générateur : yields des pings (str) puis ('RESULT', valeur)."""
            task = loop.run_in_executor(None, fn)
            waited = 0.0
            while True:
                done, _pending = await asyncio.wait({task}, timeout=4.0)
                if task in done:
                    yield ("RESULT", task.result())
                    return
                waited += 4.0
                if waited >= timeout:
                    task.cancel()
                    raise asyncio.TimeoutError()
                yield (": keepalive\n\n", None)  # commentaire SSE → garde la connexion vivante

        try:
            # ── ÉTAPE 1 : stratégie (vision) ──
            yield 'event: progress\n'
            yield 'data: {"message": "\\ud83d\\udc41\\ufe0f Analyse de l\'image produit\\u2026", "stage": "strategy"}\n\n'
            strategy = None
            async for kind, val in _run(
                lambda: photo_slide.generate_strategy(
                    img, product_name, price, currency, description, niche, preferred_style), 75.0):
                if kind == "RESULT":
                    strategy = val
                else:
                    yield kind
            yield 'event: strategy\n'
            yield f'data: {json.dumps(strategy)}\n\n'

            # ── ÉTAPE 2 : contenu (texte) ──
            yield 'event: progress\n'
            yield 'data: {"message": "\\u270d\\ufe0f R\\u00e9daction des slides\\u2026", "stage": "content"}\n\n'
            content = None
            async for kind, val in _run(
                lambda: photo_slide.generate_content(
                    strategy, product_name, price, currency, description, niche), 75.0):
                if kind == "RESULT":
                    content = val
                else:
                    yield kind
            yield 'event: content\n'
            yield f'data: {json.dumps(content)}\n\n'

            yield 'event: complete\n'
            yield f'data: {json.dumps({**strategy, **content})}\n\n'
        except asyncio.TimeoutError:
            yield 'event: error\n'
            yield 'data: {"error": "La g\\u00e9n\\u00e9ration a pris trop longtemps."}\n\n'
        except Exception as e:
            print(f"/api/photo-slide/generate error: {e}")
            yield 'event: error\n'
            yield f'data: {json.dumps({"error": str(e)})}\n\n'

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no", "Connection": "keep-alive"},
    )


_IMG_PROXY_ALLOWED = ("tiktokcdn", "ibyteimg", "ttcdn", "byteimg", "muscdn",
                      "tiktokcdn-us", "p16-", "p19-", "akamaized", "ttwstatic",
                      # Host propre de KeyAPI (avatars créateurs) — URLs stables :
                      "echosell-images", "volces.com", "byteplus")
_IMG_CACHE: "dict[str, tuple[bytes, str]]" = {}   # url -> (bytes, content_type)
_IMG_CACHE_MAX = 400
# Budget RAM total du cache (Render 512 MB) : au-delà, on évince les plus
# anciennes entrées. Les images > _IMG_CACHE_ITEM_MAX ne sont jamais cachées
# (le navigateur les garde de toute façon via Cache-Control 24h).
_IMG_CACHE_MAX_BYTES = 25_000_000
_IMG_CACHE_ITEM_MAX = 400_000
_IMG_CACHE_BYTES = 0


@app.get("/api/img-proxy")
async def img_proxy(url: str = Query(...)):
    """Proxy d'images CDN TikTok (avatars créateurs, covers vidéos, images produits).
    Contourne la protection hotlink/signature : on récupère l'image côté serveur
    (sans Referer) puis on la re-sert. Whitelist stricte (anti-SSRF) + cache mémoire
    (évite de re-télécharger en rafale → moins de scintillement sous charge)."""
    u = (url or "").strip()
    if not u.lower().startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL invalide.")
    if not any(tok in u for tok in _IMG_PROXY_ALLOWED):
        raise HTTPException(status_code=400, detail="Domaine non autorisé.")

    cached = _IMG_CACHE.get(u)
    if cached is not None:
        return Response(content=cached[0], media_type=cached[1],
                        headers={"Cache-Control": "public, max-age=86400"})
    try:
        async with httpx.AsyncClient(timeout=6.0, follow_redirects=True) as client:
            r = await client.get(u, headers={
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
                "Referer": "",
            })
    except Exception:
        raise HTTPException(status_code=502, detail="Image inaccessible.")
    if not r.is_success:
        raise HTTPException(status_code=404, detail="Image introuvable.")
    ct = r.headers.get("content-type", "image/jpeg")
    if "image" not in ct:
        ct = "image/jpeg"
    content = r.content
    if len(content) <= _IMG_CACHE_ITEM_MAX:   # ne cache pas les images lourdes
        global _IMG_CACHE_BYTES
        # Éviction FIFO (dict Python = ordre d'insertion) jusqu'à tenir dans
        # le budget entrées ET octets.
        while _IMG_CACHE and (len(_IMG_CACHE) >= _IMG_CACHE_MAX
                              or _IMG_CACHE_BYTES + len(content) > _IMG_CACHE_MAX_BYTES):
            try:
                old, _old_ct = _IMG_CACHE.pop(next(iter(_IMG_CACHE)))
                _IMG_CACHE_BYTES -= len(old)
            except Exception:
                _IMG_CACHE.clear(); _IMG_CACHE_BYTES = 0
        _IMG_CACHE[u] = (content, ct)
        _IMG_CACHE_BYTES += len(content)
    return Response(content=content, media_type=ct,
                    headers={"Cache-Control": "public, max-age=86400"})


@app.get("/api/_admin/aiml-models")
async def aiml_models(request: Request, token: Optional[str] = Query(None), filter: str = Query("")):
    """Liste les IDs de modèles dispo de la clé AIML (pour configurer les bons modèles).
    ?filter= pour ne garder que les IDs contenant un mot-clé (ex: flux, kontext, imagen…)."""
    ok_admin = False
    try:
        u = get_user_from_request(request)
        ok_admin = bool(u.get("is_admin") or u.get("tier") == "admin")
    except Exception:
        ok_admin = False
    if not ok_admin and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            email = verify_access_token(token.replace(" ", "+"))
            ok_admin = bool(email and ADMIN_EMAIL and email.lower() == ADMIN_EMAIL)
        except Exception:
            ok_admin = False
    if not ok_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis.")

    raw = image_gen.list_models()
    # Extrait les IDs (formats AIML possibles : {data:[{id}]} ou liste)
    rows = raw.get("data") if isinstance(raw, dict) else raw
    ids = []
    for m in (rows or []):
        mid = m.get("id") if isinstance(m, dict) else (m if isinstance(m, str) else None)
        if not mid:
            continue
        # garde les modèles d'image probables
        low = str(mid).lower()
        if any(k in low for k in ("image", "flux", "dall", "imagen", "kontext", "seed", "recraft",
                                   "stable", "sd", "gemini", "kling", "reve", "qwen", "wan", "topaz")):
            ids.append(mid)
    f = (filter or "").lower().strip()
    if f:
        ids = [i for i in ids if f in str(i).lower()]
    return {"ok": True, "count": len(ids), "image_models": sorted(ids),
            "current_edit_model": image_gen.edit_model(),
            "note": "Repère l'ID FLUX Kontext / Google image-edit / SeedEdit pour la fidélité produit."}


@app.get("/api/_admin/image-selftest")
async def image_selftest(request: Request, token: Optional[str] = Query(None),
                         provider: str = Query("flux"), style: str = Query("fond_blanc"),
                         phase: str = Query("Hook")):
    """Teste la génération d'image (AIML) → valide la clé + l'ID de modèle.
    Auth admin via header OU ?token=."""
    ok_admin = False
    try:
        u = get_user_from_request(request)
        ok_admin = bool(u.get("is_admin") or u.get("tier") == "admin")
    except Exception:
        ok_admin = False
    if not ok_admin and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            email = verify_access_token(token.replace(" ", "+"))
            ok_admin = bool(email and ADMIN_EMAIL and email.lower() == ADMIN_EMAIL)
        except Exception:
            ok_admin = False
    if not ok_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis.")

    out = {"has_key": image_gen.has_image_key(), "provider": provider, "style": style, "phase": phase,
           "quality": ("prod" if image_gen._is_prod_quality() else "test (FLUX schnell)"),
           "model": image_gen.model_for(provider, style, "beaute"),
           "edit_model": image_gen.edit_model()}
    if not image_gen.has_image_key():
        out["verdict"] = "❌ AIMLAPI_KEY absente"
        return out
    loop = asyncio.get_event_loop()
    try:
        imgs = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: image_gen.generate_slide_images(
                "Sérum visage premium", style, provider, "beaute", [phase])),
            timeout=90.0)
        first = imgs[0] if imgs else {}
        out["result"] = first
        out["verdict"] = "✅ Image générée" if first.get("url") else "⚠️ Pas d'URL (voir aiml_last_error)"
    except Exception as e:
        out["verdict"] = "❌ Erreur"
        out["error"] = str(e)
    out["aiml_last_error"] = image_gen.last_error()
    return out


@app.get("/api/_admin/ai-selftest")
async def ai_selftest(request: Request, token: Optional[str] = Query(None)):
    """Valide la couche IA (Mistral/Gemini/Claude) : quelles clés sont posées, quel
    fournisseur est résolu par tier, et un vrai aller-retour TEXTE. Auth admin (header ou ?token=)."""
    ok_admin = False
    try:
        u = get_user_from_request(request)
        ok_admin = bool(u.get("is_admin") or u.get("tier") == "admin")
    except Exception:
        ok_admin = False
    if not ok_admin and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            email = verify_access_token(token.replace(" ", "+"))
            ok_admin = bool(email and ADMIN_EMAIL and email.lower() == ADMIN_EMAIL)
        except Exception:
            ok_admin = False
    if not ok_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis.")

    out = {
        "keys": {
            "mistral": bool(os.getenv("MISTRAL_API_KEY")),
            "gemini": bool(os.getenv("GEMINI_API_KEY")),
            "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
        },
        "resolved": {"vision": ai_providers._resolve("vision"), "text": ai_providers._resolve("text")},
        "models": {"vision_gemini": ai_providers.GEMINI_VISION_MODEL, "text_claude": ai_providers.CLAUDE_TEXT_MODEL},
    }
    loop = asyncio.get_event_loop()
    # 1) Tier TEXTE (Claude si dispo)
    try:
        txt = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: ai_providers.text_complete(
                "Réponds en UN seul mot : OK", timeout=30.0, max_tokens=20)),
            timeout=40.0)
        out["text_roundtrip"] = (txt or "").strip()[:80]
        out["text_provider_used"] = ai_providers.last_providers().get("text")
    except Exception as e:
        out["text_error"] = str(e)
    # 2) Tier VISION (Gemini si dispo) sur une mini-image 1x1 (valide la chaîne image)
    _TINY_PNG = ("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8z8BQDwAE"
                 "hQGAhKmMIQAAAABJRU5ErkJggg==")
    try:
        blocks = [
            {"type": "text", "text": "Réponds en UN mot la couleur dominante de cette image."},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + _TINY_PNG}},
        ]
        v = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: ai_providers.vision_complete(blocks, timeout=30.0)),
            timeout=40.0)
        out["vision_roundtrip"] = (v or "").strip()[:80]
        out["vision_provider_used"] = ai_providers.last_providers().get("vision")
    except Exception as e:
        out["vision_error"] = str(e)
    ok_t = bool(out.get("text_roundtrip")) and "text_error" not in out
    ok_v = bool(out.get("vision_roundtrip")) and "vision_error" not in out
    out["verdict"] = ("✅ Couche IA opérationnelle (texte + vision)" if ok_t and ok_v
                      else "⚠️ Partiel — voir text_error / vision_error" if (ok_t or ok_v)
                      else "❌ Échec des deux tiers")
    return out


@app.get("/api/_admin/email-selftest")
async def email_selftest(request: Request, token: Optional[str] = Query(None), to: Optional[str] = Query(None)):
    """Envoie un email de test (transport Resend si configuré, sinon SMTP) pour valider
    la config. Auth admin via header OU ?token=. Usage : ?to=ton@email.com&token=..."""
    ok_admin = False
    try:
        u = get_user_from_request(request)
        ok_admin = bool(u.get("is_admin") or u.get("tier") == "admin")
    except Exception:
        ok_admin = False
    if not ok_admin and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            em = verify_access_token(token.replace(" ", "+"))
            ok_admin = bool(em and ADMIN_EMAIL and em.lower() == ADMIN_EMAIL)
        except Exception:
            ok_admin = False
    if not ok_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis.")

    import email_service as _es
    dest = (to or "").strip()
    if not dest:
        try:
            from auth import ADMIN_EMAIL
            dest = ADMIN_EMAIL or ""
        except Exception:
            dest = ""
    out = {
        "transport": "resend" if _es.RESEND_ENABLED else ("smtp" if _es.SMTP_ENABLED else "aucun"),
        "from": _es.EMAIL_FROM, "to": dest,
    }
    if not dest:
        out["verdict"] = "⚠️ Précise ?to=ton@email.com"
        return out
    try:
        ok = await _es.email_service.send_welcome_email(dest)
        out["sent"] = ok
        out["verdict"] = "✅ Envoyé (vérifie boîte + spam)" if ok else "❌ Échec (voir logs Render)"
    except Exception as e:
        out["error"] = str(e)
        out["verdict"] = "❌ Erreur"
    return out


@app.get("/api/_admin/keyapi-selftest")
async def keyapi_selftest(request: Request, token: Optional[str] = Query(None)):
    """Auto-test KeyAPI Video Products sur la vidéo d'exemple de la doc (indexée à
    coup sûr) → confirme que l'intégration marche, sans chercher de video_id."""
    ok_admin = False
    try:
        u = get_user_from_request(request)
        ok_admin = bool(u.get("is_admin") or u.get("tier") == "admin")
    except Exception:
        ok_admin = False
    if not ok_admin and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            email = verify_access_token(token.replace(" ", "+"))
            ok_admin = bool(email and ADMIN_EMAIL and email.lower() == ADMIN_EMAIL)
        except Exception:
            ok_admin = False
    if not ok_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis.")

    # Vidéo d'exemple de la doc KeyAPI (région ID) — indexée à coup sûr.
    sample_video = "6994372454948900122"
    """Auto-test KeyAPI Video Products sur la vidéo d'exemple de la doc (indexée à
    coup sûr) → confirme que l'intégration marche, sans chercher de video_id."""
    ok_admin = False
    try:
        u = get_user_from_request(request)
        ok_admin = bool(u.get("is_admin") or u.get("tier") == "admin")
    except Exception:
        ok_admin = False
    if not ok_admin and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            email = verify_access_token(token.replace(" ", "+"))
            ok_admin = bool(email and ADMIN_EMAIL and email.lower() == ADMIN_EMAIL)
        except Exception:
            ok_admin = False
    if not ok_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis.")

    # Vidéo d'exemple de la doc KeyAPI (région ID) — indexée à coup sûr.
    sample_video = "6994372454948900122"
    out = {"sample_video_id": sample_video}
    try:
        prods = await market_creators.get_video_products(sample_video, region="ID")
        out["ok"] = True
        out["count"] = len(prods)
        out["products"] = prods
        out["verdict"] = ("✅ Video Products FONCTIONNE" if prods
                          else "⚠️ 0 produit (params OK mais réponse vide)")
    except Exception as e:
        out["ok"] = False
        out["error"] = str(e)
        out["verdict"] = "❌ Erreur KeyAPI (voir error)"
    return out


@app.get("/api/_admin/analyzed-products")
async def admin_analyzed_products(request: Request, token: Optional[str] = Query(None), limit: int = Query(50)):
    """Dump des dernières lignes de la mémoire produits (admin). Auth via header
    Authorization OU ?token=<token_admin> (pratique pour ouvrir dans le navigateur)."""
    ok_admin = False
    try:
        u = get_user_from_request(request)
        ok_admin = bool(u.get("is_admin") or u.get("tier") == "admin")
    except Exception:
        ok_admin = False
    if not ok_admin and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            email = verify_access_token(token.replace(" ", "+"))
            ok_admin = bool(email and ADMIN_EMAIL and email.lower() == ADMIN_EMAIL)
        except Exception:
            ok_admin = False
    if not ok_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis.")
    if not supabase_client:
        return {"ok": False, "error": "Supabase indisponible"}
    try:
        r = (supabase_client.table("analyzed_products")
             .select("product_key,product_id,product_name,categorie,region,price,last_sales,times_seen,last_seen")
             .order("last_seen", desc=True).limit(min(max(limit, 1), 200)).execute())
        rows = r.data or []
        with_id = sum(1 for x in rows if x.get("product_id"))
        return {"ok": True, "total": len(rows), "avec_product_id": with_id, "rows": rows}
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=502)


# ════════════════════════════════════════════════════════════════════════════
# 🎬 AI VIDEO PROMPT STUDIO + 💎 CRÉDITS
# ════════════════════════════════════════════════════════════════════════════
@app.get("/api/credits/balance")
async def credits_balance(request: Request):
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    bal = credits_mod.get_balance(supabase_client, user["email"], user.get("tier", "free"))
    return {"ok": True, **bal}


@app.get("/api/credits/packs")
async def credits_packs():
    return {"ok": True, "packs": credits_mod.CREDIT_PACKS, "level_cost": credits_mod.LEVEL_COST}


# ── Plans & prix dynamiques (pilotés par la roadmap, 100 % serveur) ──────────
@app.get("/api/plans/available")
async def plans_available():
    import feature_flags
    return {"ok": True, "plans": feature_flags.available_plans(),
            "dates": feature_flags.availability_dates()}


@app.get("/api/plans/prices")
async def plans_prices():
    import feature_flags
    return {"ok": True, "prices": feature_flags.current_prices()}


@app.get("/api/ltd/availability")
async def ltd_availability():
    import feature_flags
    return {"ok": True, "enabled": feature_flags.is_enabled("ltd_available"),
            "date": feature_flags.availability_dates()["ltd"]}


@app.get("/api/_admin/feature-flags")
async def admin_feature_flags(request: Request, token: Optional[str] = Query(None)):
    ok_admin = False
    try:
        u = get_user_from_request(request)
        ok_admin = bool(u.get("is_admin") or u.get("tier") == "admin")
    except Exception:
        ok_admin = False
    if not ok_admin and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            email = verify_access_token(token.replace(" ", "+"))
            ok_admin = bool(email and ADMIN_EMAIL and email.lower() == ADMIN_EMAIL)
        except Exception:
            ok_admin = False
    if not ok_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis.")
    import feature_flags
    return {"ok": True, **feature_flags.snapshot()}


# ── « 🔔 Me notifier » : capture d'email pour un plan pas encore ouvert ──────
@app.post("/api/notify-me")
async def notify_me(request: Request):
    body = await request.json()
    email = (body.get("email") or "").strip().lower()
    plan = (body.get("plan") or "").strip().lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=422, detail="Email invalide.")
    if plan not in ("pro", "gold", "agency", "ltd"):
        raise HTTPException(status_code=422, detail="Plan invalide.")
    try:
        # upsert best-effort : email + plan unique. La table peut ne pas exister encore.
        supabase_client.table("plan_notify_signups").upsert(
            {"email": email, "plan": plan}, on_conflict="email,plan"
        ).execute()
    except Exception as e:
        print(f"[notify-me] insert skipped: {e}")
    return {"ok": True, "message": "On te préviendra dès l'ouverture 🔔"}


# ── FEATURE 1 — Banque de Hooks (public, gating 100 % serveur) ───────────────
@app.get("/api/hooks")
async def list_hooks(request: Request, category: Optional[str] = Query(None)):
    import hooks_lib
    user = get_user_from_request(request)
    tier = (user.get("tier") or "free").lower() if user.get("valid") else "free"
    rows = []
    try:
        q = supabase_client.table("hooks").select("*").order("created_at", desc=True)
        if category and category not in ("all", ""):
            q = q.eq("categorie", category)
        rows = q.execute().data or []
    except Exception as e:
        print(f"[hooks] list error: {e}")
    items = [hooks_lib.public_payload(h, tier) for h in rows]
    return {
        "ok": True, "tier": tier,
        "categories": hooks_lib.HOOK_CATEGORIES,
        "category_labels": hooks_lib.CATEGORY_LABELS,
        "count": len(items), "locked_count": sum(1 for i in items if i["locked"]),
        "items": items,
    }


# ── FEATURE 2 — Témoignages (public) ────────────────────────────────────────
@app.get("/api/temoignages")
async def list_temoignages(featured: Optional[int] = Query(None), limit: Optional[int] = Query(None)):
    rows = []
    try:
        q = (supabase_client.table("temoignages").select("*")
             .eq("statut", "publie")
             .order("mis_en_avant", desc=True).order("date_publication", desc=True))
        if featured:
            q = q.eq("mis_en_avant", True)
        if limit:
            q = q.limit(int(limit))
        rows = q.execute().data or []
    except Exception as e:
        print(f"[temoignages] list error: {e}")
    # On n'expose que les champs publics
    items = [{"nom": r.get("nom"), "texte": r.get("texte"), "lien_tiktok": r.get("lien_tiktok"),
              "photo_url": r.get("photo_url"), "metrique": r.get("metrique"), "note": r.get("note")}
             for r in rows]
    return {"ok": True, "count": len(items), "items": items}


@app.post("/api/temoignages")
async def submit_temoignage(request: Request):
    body = await request.json()
    nom = (body.get("nom") or "").strip()[:80]
    texte = (body.get("texte") or "").strip()[:1000]
    lien = (body.get("lien_tiktok") or "").strip()[:200] or None
    note = body.get("note")
    if not nom or len(texte) < 10:
        raise HTTPException(status_code=422, detail="Nom et témoignage (≥10 caractères) requis.")
    try:
        note = int(note) if note not in (None, "") else None
    except Exception:
        note = None
    try:
        supabase_client.table("temoignages").insert({
            "nom": nom, "texte": texte, "lien_tiktok": lien, "note": note, "statut": "en_attente",
        }).execute()
    except Exception as e:
        print(f"[temoignages] insert error: {e}")
        raise HTTPException(status_code=500, detail="Enregistrement impossible.")
    # Alerte admin (push) : un avis à valider
    try:
        import push
        push.send_to_admins(supabase_client, {
            "title": "🆕 Nouveau témoignage à valider",
            "body": f"{nom} : {texte[:80]}",
            "url": "/dope-admin",
        })
    except Exception as e:
        print(f"[temoignages] admin push skipped: {e}")
    return {"ok": True, "message": "Merci ! Ton témoignage sera publié après validation."}


@app.post("/api/request-testimonial-email")
async def request_testimonial_email(request: Request):
    """Déclenché par le front après X analyses. Envoie UNE fois un email de
    relance invitant à laisser un avis (lien vers /avis pré-rempli)."""
    user = get_user_from_request(request)
    if not user.get("valid"):
        return {"ok": False, "reason": "not_logged_in"}
    email = user["email"]
    try:
        r = supabase_client.table("users").select("testimonial_email_sent").eq("email", email).execute()
        if r.data and r.data[0].get("testimonial_email_sent"):
            return {"ok": True, "already_sent": True}
    except Exception as e:
        print(f"[testimonial-email] check error: {e}")
    # Envoi
    try:
        from email_service import send_transactional_email
        app_url = os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")
        link = f"{app_url}/avis?nom={quote((user.get('name') or email.split('@')[0]))}"
        html = f"""<div style="font-family:sans-serif;max-width:520px;margin:auto">
          <h2>Ton avis compte 🙏</h2>
          <p>Tu utilises Qeerah depuis quelques analyses — ça nous aiderait énormément que tu partages ton retour.</p>
          <p>Ça prend 1 minute, et ça aide d'autres créateurs à se lancer.</p>
          <p style="margin:24px 0"><a href="{link}" style="background:#2563EB;color:#fff;padding:12px 22px;border-radius:8px;text-decoration:none;font-weight:700">Laisser mon avis →</a></p>
          <p style="font-size:12px;color:#888">Qeerah · L'outil d'analyse pensé par des créateurs, pour des créateurs.</p>
        </div>"""
        sent = send_transactional_email(email, "Ton avis sur Qeerah 🙏", html)
        if sent:
            supabase_client.table("users").update({"testimonial_email_sent": True}).eq("email", email).execute()
        return {"ok": bool(sent)}
    except Exception as e:
        print(f"[testimonial-email] send error: {e}")
        return {"ok": False}


# ── NOTIFICATIONS — Web Push (PWA) ──────────────────────────────────────────
@app.get("/api/push/public-key")
async def push_public_key():
    import push
    return {"ok": True, "key": push.VAPID_PUBLIC_KEY, "enabled": push.is_configured()}


@app.post("/api/push/subscribe")
async def push_subscribe(request: Request):
    import push
    body = await request.json()
    sub = body.get("subscription") or body
    user = get_user_from_request(request)
    email = user["email"] if user.get("valid") else None
    is_admin = bool(user.get("is_admin") or user.get("tier") == "admin")
    ua = request.headers.get("user-agent", "")
    ok = push.save_subscription(supabase_client, sub, email, is_admin, ua)
    if not ok:
        raise HTTPException(status_code=422, detail="Abonnement invalide.")
    return {"ok": True}


@app.post("/api/push/unsubscribe")
async def push_unsubscribe(request: Request):
    import push
    body = await request.json()
    endpoint = body.get("endpoint")
    if endpoint:
        push.remove_subscription(supabase_client, endpoint)
    return {"ok": True}


@app.post("/api/credits/purchase")
async def credits_purchase(request: Request):
    # Paiement Stripe DIFFÉRÉ (société non créée) → stub jusqu'à mise en prod.
    raise HTTPException(status_code=503,
                        detail="L'achat de crédits sera disponible très bientôt (paiement en cours d'activation).")


@app.get("/api/video-prompt/history")
async def video_prompt_history(request: Request):
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    try:
        r = (supabase_client.table("video_prompt_generations")
             .select("id,created_at,prompt_level,credits_used,ai_platform,product_name,generated_prompt")
             .eq("email", user["email"]).order("created_at", desc=True).limit(30).execute())
        return {"ok": True, "items": r.data or []}
    except Exception:
        return {"ok": True, "items": []}


@app.post("/api/video-prompt/generate")
async def video_prompt_generate(
    request: Request,
    level: int = Form(...),
    platform: str = Form("sora2"),
    image: Optional[str] = Form(None),
    product_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    currency: str = Form("EUR"),
    niche: Optional[str] = Form(None),
    visual_style: Optional[str] = Form(None),
    mood: Optional[str] = Form(None),
    emotion_target: Optional[str] = Form(None),
    color_tone: Optional[str] = Form(None),
    avoid: Optional[str] = Form(None),
    product_url: Optional[str] = Form(None),
    user_region: Optional[str] = Form(None),
):
    """Génère un prompt vidéo IA. PRO+ requis. Débite les crédits (abonnement→achats)."""
    if not ai_providers.any_ai_key():
        raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")
    if not ((image or "").strip() and (product_name or "").strip() and (description or "").strip()):
        raise HTTPException(status_code=422, detail="Image, nom et description du produit sont obligatoires.")
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    tier = (user.get("tier") or "free").lower()
    if tier not in _PROMPT_STUDIO_TIERS and not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Réservé aux plans Pro, Gold et Agency.")

    try:
        lvl = max(1, min(5, int(level)))
    except Exception:
        lvl = 1
    cost = credits_mod.level_cost(lvl, platform)
    email = user["email"]

    # Vérif crédits AVANT (réponse claire pour le front si insuffisant)
    bal = credits_mod.get_balance(supabase_client, email, tier)
    if bal.get("total_available", 0) < cost:
        return JSONResponse({"ok": False, "reason": "insufficient_credits",
                             "cost": cost, "available": bal.get("total_available", 0)}, status_code=402)

    img = (image or "").strip()
    if img.lower().startswith("data:") and "," in img:
        img = img.split(",", 1)[1]

    # Enrichissement via lien produit TikTok Shop (KeyAPI) : nom officiel, catégorie,
    # prix + image HD officielle (2ᵉ référence visuelle pour pixtral).
    product_name, niche, price, product_image_url = await _enrich_from_product_url(
        product_url, product_name, niche, price, user_region)

    async def stream():
        loop = asyncio.get_event_loop()
        try:
            yield 'event: progress\n'
            yield 'data: {"message": "\\ud83c\\udfac G\\u00e9n\\u00e9ration du prompt vid\\u00e9o\\u2026"}\n\n'
            task = loop.run_in_executor(None, lambda: video_prompt.generate_video_prompt(
                img or None, lvl, platform, product_name, description, price, currency,
                niche, visual_style, mood, emotion_target, color_tone, avoid,
                image_url=product_image_url))
            waited = 0.0
            result = None
            while True:
                done, _ = await asyncio.wait({task}, timeout=4.0)
                if task in done:
                    result = task.result()
                    break
                waited += 4.0
                if waited >= 90.0:
                    task.cancel()
                    yield 'event: error\n'
                    yield 'data: {"error": "La g\\u00e9n\\u00e9ration a pris trop longtemps."}\n\n'
                    return
                yield ': keepalive\n\n'

            # Débit + historique (best-effort) APRÈS succès
            credits_mod.debit(supabase_client, email, tier, cost)
            try:
                supabase_client.table("video_prompt_generations").insert({
                    "email": email, "prompt_level": lvl, "credits_used": cost,
                    "ai_platform": platform, "product_name": product_name, "niche": niche,
                    "generated_prompt": result,
                }).execute()
            except Exception:
                pass

            new_bal = credits_mod.get_balance(supabase_client, email, tier)
            payload = {"result": result, "credits_used": cost, "balance": new_bal}
            yield 'event: complete\n'
            yield f'data: {json.dumps(payload)}\n\n'
        except Exception as e:
            print(f"/api/video-prompt/generate error: {e}")
            yield 'event: error\n'
            yield f'data: {json.dumps({"error": str(e)})}\n\n'

    return StreamingResponse(stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ════════════════════════════════════════════════════════════════════════════
# 📸 CAROUSEL CREATOR (Photo Slide Coach v4) — homepage + anonyme + pay-as-you-go
# ════════════════════════════════════════════════════════════════════════════
async def _enrich_from_product_url(product_url: Optional[str], product_name: Optional[str],
                                   niche: Optional[str], price: Optional[str],
                                   user_region: Optional[str] = None):
    """Lien TikTok Shop → fiche OFFICIELLE (KeyAPI) : nom, catégorie, prix, image HD.
    Le nom officiel prime (identification fiable). user_region = pays détecté côté
    navigateur → essayé EN PREMIER (le pays n'est pas dans l'URL). Retourne
    (product_name, niche, price, product_image_url). Best-effort : silencieux si échec."""
    product_image_url = None
    if not product_url:
        return product_name, niche, price, product_image_url
    # Région utilisateur d'abord, puis liste de repli (CAROUSEL_PRODUCT_REGIONS).
    regions = None
    if user_region:
        defaults = [r.strip().upper() for r in
                    os.getenv("CAROUSEL_PRODUCT_REGIONS", "US,GB,FR").split(",") if r.strip()]
        ur = user_region.strip().upper()[:2]
        regions = [ur] + [r for r in defaults if r != ur]
    try:
        detail = await market_creators.get_product_detail_from_url(product_url, regions=regions)
    except Exception:
        detail = None
    if detail:
        if detail.get("name"):
            product_name = detail["name"]                 # nom officiel = identification fiable
        if not niche and detail.get("category"):
            niche = detail["category"]
        if not price and detail.get("price"):
            price = f'{detail["price"]}{detail.get("currency") or ""}'
        if detail.get("image"):
            product_image_url = detail["image"]           # image HD officielle → img2img + pixtral
    return product_name, niche, price, product_image_url


def _sse_carousel(gen_callable):
    """Wrapper SSE commun (keepalive pendant la génération)."""
    async def stream():
        loop = asyncio.get_event_loop()
        try:
            yield 'event: progress\n'
            yield 'data: {"message": "\\ud83d\\udcf8 G\\u00e9n\\u00e9ration du carrousel\\u2026"}\n\n'
            task = loop.run_in_executor(None, gen_callable)
            waited = 0.0
            result = None
            while True:
                done, _ = await asyncio.wait({task}, timeout=4.0)
                if task in done:
                    result = task.result()
                    break
                waited += 4.0
                if waited >= 120.0:
                    task.cancel()
                    yield 'event: error\n'
                    yield 'data: {"error": "La g\\u00e9n\\u00e9ration a pris trop longtemps."}\n\n'
                    return
                yield ': keepalive\n\n'
            yield 'event: complete\n'
            yield f'data: {json.dumps(result)}\n\n'
        except Exception as e:
            print(f"carousel sse error: {e}")
            yield 'event: error\n'
            yield f'data: {json.dumps({"error": str(e)})}\n\n'
    return StreamingResponse(stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/api/carousel/providers")
async def carousel_providers():
    """Liste des IA images (label, coûts, prix) pour le wizard."""
    return {"ok": True, "providers": image_gen.IMAGE_PROVIDERS}


@app.get("/api/carousel/product-info")
async def carousel_product_info(url: str = Query(...), region: Optional[str] = Query(None)):
    """Pré-remplissage du créateur de carrousel : lien TikTok Shop → fiche produit
    officielle (nom, catégorie, prix, image HD). Sert aussi la boucle « Recréer »
    depuis Feed Radar / Créateurs Gagnants. Best-effort, jamais bloquant."""
    if not url or "tiktok" not in url.lower():
        return {"ok": False}
    try:
        name, niche, price, image = await _enrich_from_product_url(url, None, None, None, region)
    except Exception:
        return {"ok": False}
    return {"ok": bool(name or price or image), "name": name, "niche": niche,
            "price": price, "image": image}


@app.get("/api/_admin/product-detail-selftest")
async def product_detail_selftest(request: Request, token: Optional[str] = Query(None),
                                  url: str = Query(...)):
    """Valide l'extraction product_id + KeyAPI detail_new_app depuis une vraie URL TikTok Shop.
    Auth admin via header OU ?token=. Usage: ?url=https://www.tiktok.com/view/product/...&token=..."""
    ok_admin = False
    try:
        u = get_user_from_request(request)
        ok_admin = bool(u.get("is_admin") or u.get("tier") == "admin")
    except Exception:
        ok_admin = False
    if not ok_admin and token:
        try:
            from auth import verify_access_token, ADMIN_EMAIL
            email = verify_access_token(token.replace(" ", "+"))
            ok_admin = bool(email and ADMIN_EMAIL and email.lower() == ADMIN_EMAIL)
        except Exception:
            ok_admin = False
    if not ok_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis.")

    out = {"url": url, "product_id": market_creators.extract_product_id(url)}
    try:
        detail = await market_creators.get_product_detail_from_url(url)
        out["detail"] = detail
        out["verdict"] = ("✅ Fiche produit OK (nom + image officielle)" if detail and detail.get("image")
                          else "⚠️ product_id trouvé mais pas de fiche (région/endpoint ?)" if out["product_id"]
                          else "❌ Aucun product_id extrait de l'URL")
    except Exception as e:
        out["error"] = str(e)
        out["verdict"] = "❌ Erreur KeyAPI"
    return out


@app.post("/api/carousel/anon/generate")
async def carousel_anon_generate(
    request: Request,
    image: Optional[str] = Form(None),
    mode: str = Form("prompts"),
    product_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    currency: str = Form("EUR"),
    niche: Optional[str] = Form(None),
    style: Optional[str] = Form(None),
    user_idea: Optional[str] = Form(None),
    product_url: Optional[str] = Form(None),
    user_region: Optional[str] = Form(None),
    avoid: Optional[str] = Form(None),
    cookie_id: Optional[str] = Form(None),
):
    """DÉPRÉCIÉ : le carrousel exige désormais un compte. (L'analyse vidéo, elle,
    reste testable en anonyme.) On renvoie 401 pour fermer toute génération anonyme."""
    return JSONResponse({"ok": False, "reason": "account_required",
                         "message": "Crée un compte gratuit pour générer un carrousel (3/mois inclus)."},
                        status_code=401)
    # --- ancien parcours anonyme désactivé ci-dessous ---
    if not ai_providers.any_ai_key():
        raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")
    if not ((product_name or "").strip() and (description or "").strip() and (price or "").strip()):
        raise HTTPException(status_code=422, detail="Nom, description et prix du produit sont obligatoires.")
    if mode == "images":
        return JSONResponse({"ok": False, "reason": "payment_required",
                             "message": "Le mode Images IA nécessite un achat (bientôt disponible)."}, status_code=402)

    ip = _ip_hash(request)
    # 1 essai gratuit par IP+cookie
    if supabase_client:
        try:
            q = supabase_client.table("anonymous_generations").select("id").eq("ip_hash", ip)
            if cookie_id:
                q = q.eq("cookie_id", cookie_id)
            if (q.limit(1).execute().data or []):
                return JSONResponse({"ok": False, "reason": "free_used",
                                     "message": "Essai gratuit déjà utilisé. Crée un compte (3 gratuits/mois) ou abonne-toi."}, status_code=402)
        except Exception:
            pass

    # Enrichissement via lien produit TikTok Shop (KeyAPI) : identification fiable.
    product_name, niche, price, product_image_url = await _enrich_from_product_url(
        product_url, product_name, niche, price, user_region)

    img = (image or "").strip()
    if img.lower().startswith("data:") and "," in img:
        img = img.split(",", 1)[1]

    def _gen():
        res = carousel.generate_carousel(img or None, "prompts", style, "flux",
                                         product_name, description, price, currency, niche, user_idea,
                                         product_image_url=product_image_url, avoid=avoid)
        try:
            supabase_client.table("anonymous_generations").insert({
                "ip_hash": ip, "cookie_id": cookie_id, "generation_mode": "prompts",
                "product_name": product_name, "generation_data": res,
            }).execute()
        except Exception:
            pass
        res["anonymous"] = True
        return res

    return _sse_carousel(_gen)


@app.post("/api/carousel/generate")
async def carousel_generate(
    request: Request,
    image: Optional[str] = Form(None),
    mode: str = Form("prompts"),
    provider: str = Form("auto"),
    product_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    currency: str = Form("EUR"),
    niche: Optional[str] = Form(None),
    style: Optional[str] = Form(None),
    user_idea: Optional[str] = Form(None),
    product_url: Optional[str] = Form(None),
    user_region: Optional[str] = Form(None),
    avoid: Optional[str] = Form(None),
):
    """Utilisateur connecté. Mode A : gratuit 3/mois (FREE) sinon illimité. Mode B :
    débite les crédits (coût selon l'IA)."""
    if not ai_providers.any_ai_key():
        raise HTTPException(status_code=400, detail="Clé API Mistral manquante.")
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")

    # Enrichissement AVANT validation : le lien TikTok Shop remplit nom/prix/image
    # officiels (identification fiable). Il faut donc enrichir d'abord, PUIS valider.
    product_name, niche, price, product_image_url = await _enrich_from_product_url(
        product_url, product_name, niche, price, user_region)
    # Seul le NOM est requis (après enrichissement). Description et prix sont
    # optionnels : l'IA travaille à partir du nom + niche + angle. « Colle le
    # lien → génère » sans ressaisie manuelle.
    if not (product_name or "").strip():
        raise HTTPException(status_code=422,
                            detail="Produit non identifié depuis le lien — ajoute au moins le nom du produit.")
    email = user["email"]
    tier = (user.get("tier") or "free").lower()
    is_paid = tier in ("pro", "gold", "agency", "beta", "admin") or user.get("is_admin")

    img = (image or "").strip()
    if img.lower().startswith("data:") and "," in img:
        img = img.split(",", 1)[1]

    cost = 0
    payment_method = "free"
    # L'image est toujours générée en flux → on facture le coût réel de flux
    # (cohérence : pas de décalage entre prix affiché et IA utilisée).
    gen_provider = "flux"
    if mode == "images":
        cost = image_gen.provider_credits(gen_provider)
        bal = credits_mod.get_balance(supabase_client, email, tier)
        if bal.get("total_available", 0) < cost:
            return JSONResponse({"ok": False, "reason": "insufficient_credits",
                                 "cost": cost, "available": bal.get("total_available", 0)}, status_code=402)
        payment_method = "credits"
    else:
        # Mode A : quota FREE = 3/mois
        if not is_paid and supabase_client:
            try:
                from datetime import datetime as _dt, timezone as _tz
                month_start = _dt.now(_tz.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
                cnt = supabase_client.table("photo_slide_generations").select("id", count="exact").eq("email", email).gte("created_at", month_start).execute()
                used = cnt.count if cnt.count is not None else len(cnt.data or [])
                if used >= 3:
                    return JSONResponse({"ok": False, "reason": "free_quota",
                                         "message": "3 prompts gratuits/mois atteints. Passe Pro pour l'illimité."}, status_code=402)
            except Exception:
                pass

    def _gen():
        res = carousel.generate_carousel(img or None, mode, style, gen_provider,
                                         product_name, description, price, currency, niche, user_idea,
                                         product_image_url=product_image_url, avoid=avoid)
        if cost > 0:
            credits_mod.debit(supabase_client, email, tier, cost)
        try:
            supabase_client.table("photo_slide_generations").insert({
                "email": email, "generation_mode": mode, "chosen_style": (res.get("strategy") or {}).get("chosen_style"),
                "chosen_ai": "flux" if mode == "images" else None, "product_name": product_name,
                "niche": niche, "generated_data": res, "credits_used": cost, "payment_method": payment_method,
            }).execute()
        except Exception:
            pass
        res["credits_used"] = cost
        res["balance"] = credits_mod.get_balance(supabase_client, email, tier)
        return res

    return _sse_carousel(_gen)


@app.get("/api/carousel/history")
async def carousel_history(request: Request):
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    try:
        r = (supabase_client.table("photo_slide_generations")
             .select("id,created_at,generation_mode,chosen_style,product_name,generated_data,credits_used")
             .eq("email", user["email"]).order("created_at", desc=True).limit(30).execute())
        return {"ok": True, "items": r.data or []}
    except Exception:
        return {"ok": True, "items": []}


# ════════════════════════════════════════════════════════════════════════════
# FAVORIS — créateurs / produits / posts gagnants sauvegardés par l'utilisateur
# (dégrade proprement si la table user_favorites n'est pas encore migrée)
# ════════════════════════════════════════════════════════════════════════════
_FAV_TYPES = {"creator", "product", "video"}


@app.get("/api/favorites")
async def favorites_list(request: Request):
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    try:
        r = (supabase_client.table("user_favorites")
             .select("item_type,item_id,payload,created_at")
             .eq("email", user["email"]).order("created_at", desc=True).limit(200).execute())
        return {"ok": True, "items": r.data or []}
    except Exception as e:
        print(f"/api/favorites list warn (table migrée ?): {e}")
        return {"ok": True, "items": []}   # table absente → vide, jamais de crash


@app.post("/api/favorites")
async def favorites_add(request: Request):
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    body = await request.json()
    item_type = (body.get("item_type") or "").strip().lower()
    item_id = str(body.get("item_id") or "").strip()
    if item_type not in _FAV_TYPES or not item_id:
        raise HTTPException(status_code=400, detail="Favori invalide.")
    payload = body.get("payload") if isinstance(body.get("payload"), dict) else {}
    row = {"email": user["email"], "item_type": item_type, "item_id": item_id, "payload": payload}
    try:
        supabase_client.table("user_favorites").upsert(
            row, on_conflict="email,item_type,item_id").execute()
        return {"ok": True}
    except Exception as e:
        print(f"/api/favorites add error: {e}")
        return JSONResponse({"ok": False, "error": "unavailable"}, status_code=503)


@app.delete("/api/favorites")
async def favorites_remove(request: Request, item_type: str = Query(...), item_id: str = Query(...)):
    user = get_user_from_request(request)
    if not user.get("valid"):
        raise HTTPException(status_code=401, detail="Connexion requise.")
    try:
        (supabase_client.table("user_favorites").delete()
         .eq("email", user["email"]).eq("item_type", item_type.lower())
         .eq("item_id", item_id).execute())
        return {"ok": True}
    except Exception as e:
        print(f"/api/favorites remove error: {e}")
        return JSONResponse({"ok": False}, status_code=503)


@app.post("/api/carousel/pay")
async def carousel_pay(request: Request):
    # Stripe différé (société non créée) → stub.
    raise HTTPException(status_code=503,
                        detail="Le paiement sera disponible très bientôt (activation en cours).")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
