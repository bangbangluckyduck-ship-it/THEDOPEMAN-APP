"""Sécurité : rate limiting + logging des abus."""
from __future__ import annotations
import json
import os
from time import time
from typing import Dict, List
from datetime import datetime

from fastapi import Request
from fastapi.responses import JSONResponse


# ── RATE LIMITER ──────────────────────────────────────────────────────────────

class RateLimiter:
    """Max N requêtes par minute par IP. Stockage en mémoire (suffit pour Render free)."""

    def __init__(self, requests_per_minute: int = 10):
        self.limit = requests_per_minute
        self._store: Dict[str, List[float]] = {}

    def is_allowed(self, ip: str) -> bool:
        now = time()
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
    LOG_FILE = "security.log"

    def _write(self, event: str, details: dict):
        entry = {
            "ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "event": event,
            **details,
        }
        try:
            with open(self.LOG_FILE, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
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


# ── MIDDLEWARE ────────────────────────────────────────────────────────────────

security_logger = SecurityLogger()
rate_limiter    = RateLimiter(requests_per_minute=10)


async def rate_limit_middleware(request: Request, call_next):
    """Applique le rate limiting uniquement sur /analyze."""
    if request.url.path == "/analyze":
        ip = request.client.host if request.client else "unknown"
        if not rate_limiter.is_allowed(ip):
            security_logger.rate_limit_exceeded(ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Trop de requêtes. Attends 1 minute avant de réessayer."},
            )
    return await call_next(request)
