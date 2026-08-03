"""Sécurité : rate limiting + logging des abus."""
from __future__ import annotations
import json
import os
from time import time
from typing import Dict, List
from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse


# ── RATE LIMITER ──────────────────────────────────────────────────────────────

class RateLimiter:
    """Max N requêtes par minute par IP. Stockage en mémoire (suffit pour Render free)."""

    def __init__(self, requests_per_minute: int = 10):
        self.limit = requests_per_minute
        self._store: Dict[str, List[float]] = {}
        self._last_sweep: float = 0.0

    def _sweep(self, now: float) -> None:
        """Retire les adresses devenues inactives.

        Sans ce balayage, `_store` ne perdait JAMAIS une adresse : chaque IP vue
        une seule fois y laissait une entrée définitive. Sur un processus qui vit
        des semaines, c'est une fuite mémoire lente — et la mémoire est déjà la
        ressource critique de cette instance. Au plus une fois par minute, donc
        négligeable devant le coût d'une requête.
        """
        if now - self._last_sweep < 60:
            return
        self._last_sweep = now
        for ip in [k for k, v in self._store.items() if not v or now - v[-1] >= 60]:
            self._store.pop(ip, None)

    def is_allowed(self, ip: str) -> bool:
        now = time()
        self._sweep(now)
        bucket = self._store.setdefault(ip, [])
        # Purge les entrées > 60 s
        self._store[ip] = [t for t in bucket if now - t < 60]
        if len(self._store[ip]) >= self.limit:
            return False
        self._store[ip].append(now)
        return True

    def remaining(self, ip: str) -> int:
        now = time()
        recent = [t for t in self._store.get(ip, []) if now - t < 60]
        return max(0, self.limit - len(recent))


# ── SECURITY LOGGER ───────────────────────────────────────────────────────────

class SecurityLogger:
    """Journal des événements de sécurité, émis sur la sortie standard.

    ⚠️ Ces événements étaient écrits dans un fichier local `security.log`. Or le
    disque d'une instance Render est ÉPHÉMÈRE : tout le journal disparaissait à
    chaque déploiement et à chaque redémarrage — c'est-à-dire précisément quand on
    aurait besoin de le relire. Sur stdout, il est capté par la journalisation
    Render (consultable et interrogeable) et par n'importe quel agrégateur branché
    plus tard, sans rien changer ici.
    """

    def _write(self, event: str, details: dict):
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "event": event,
            **details,
        }
        try:
            print("[security] " + json.dumps(entry, ensure_ascii=False), flush=True)
        except Exception:
            pass  # Ne jamais crasher à cause du logging

    def rate_limit_exceeded(self, ip: str):
        self._write("rate_limit", {"ip": ip})

    def analyze_ok(self, ip: str, frames: int):
        self._write("analyze_ok", {"ip": ip, "frames": frames})

    def analyze_error(self, ip: str, error: str):
        self._write("analyze_error", {"ip": ip, "error": error[:120]})

    def suspicious_agent(self, ip: str, user_agent: str):
        self._write("suspicious_agent", {"ip": ip, "ua": user_agent[:120]})

    def password_reset_requested(self, email: str, ip: str, success: bool = True):
        self._write("password_reset_requested", {"email": email, "ip": ip, "success": success})

    def password_changed_success(self, email: str, ip: str):
        self._write("password_changed", {"email": email, "ip": ip})


# ── MIDDLEWARE ────────────────────────────────────────────────────────────────

security_logger = SecurityLogger()
rate_limiter    = RateLimiter(requests_per_minute=10)

# Limiteur dédié aux routes d'authentification (login / register / forgot-password).
# Plus strict que /analyze pour freiner le bruteforce de mots de passe et le spam
# d'emails : 8 requêtes/minute/IP.
auth_rate_limiter = RateLimiter(requests_per_minute=8)
_AUTH_PROTECTED_PATHS = {"/api/login", "/api/register", "/api/forgot-password"}

# Limiteur des routes COÛTEUSES : chacune déclenche soit du calcul vidéo (CPU,
# mémoire, crédits IA), soit un appel au fournisseur de données payant, soit un
# envoi d'e-mail. Seul `/analyze` était protégé — tout le reste, y compris les
# chemins réellement empruntés par l'application, était en accès libre.
# 20/min laisse largement passer un usage humain normal.
costly_rate_limiter = RateLimiter(requests_per_minute=20)
_COSTLY_EXACT_PATHS = {
    "/analyze-url",
    "/analyze-url/stream",
    "/analyze-batch-patterns",
    "/api/jobs/create-url",
    "/api/jobs/create-upload",
    "/api/temoignages",
    "/api/img-proxy",
    "/api/tt-thumb",
    "/api/recherche/profile",
    "/create-checkout-session",
    "/create-credits-checkout-session",
    "/customer-portal",
    "/api/carousel/generate",
    "/api/photo-slide/generate",
    "/api/video-prompt/generate",
    "/api/scripts/multi-angle",
    "/api/request-testimonial-email",
}
_COSTLY_PREFIXES = ("/api/market/",)


def _is_costly(path: str) -> bool:
    return path in _COSTLY_EXACT_PATHS or path.startswith(_COSTLY_PREFIXES)


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting : /analyze (10/min), routes d'auth (8/min), routes coûteuses (20/min)."""
    path = request.url.path
    ip = request.client.host if request.client else "unknown"

    if path == "/analyze":
        if not rate_limiter.is_allowed(ip):
            security_logger.rate_limit_exceeded(ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Trop de requêtes. Attends 1 minute avant de réessayer."},
            )
    elif path in _AUTH_PROTECTED_PATHS:
        if not auth_rate_limiter.is_allowed(ip):
            security_logger.rate_limit_exceeded(ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Trop de tentatives. Attends 1 minute avant de réessayer."},
            )
    elif _is_costly(path):
        if not costly_rate_limiter.is_allowed(ip):
            security_logger.rate_limit_exceeded(ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Trop de requêtes d'affilée. Attends une minute puis réessaie."},
            )
    return await call_next(request)
