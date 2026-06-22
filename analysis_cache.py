"""Cache des analyses vidéo par hash — évite de relancer le pipeline LLM
sur la même vidéo. Hit = retour instantané, 0$ d'appel IA.

Table Supabase à créer (SQL à exécuter dans le SQL editor) :

  CREATE TABLE IF NOT EXISTS analysis_cache (
    video_hash      TEXT PRIMARY KEY,
    result          JSONB NOT NULL,
    pipeline        TEXT NOT NULL,        -- 'free' | 'pro'
    prompt_version  TEXT NOT NULL,        -- pour invalider après changement de prompt
    created_at      TIMESTAMPTZ DEFAULT NOW()
  );
  CREATE INDEX IF NOT EXISTS idx_analysis_cache_created ON analysis_cache(created_at DESC);

Comportement gracieux : si la table n'existe pas ou Supabase est down, on
log et on continue (cache miss silencieux = on relance l'analyse, jamais bloquant).
"""
from __future__ import annotations

import hashlib
import logging
import re
from typing import Any, Optional
from urllib.parse import urlparse, urlunparse

from supabase_client import supabase_service

logger = logging.getLogger(__name__)

# Bump la version quand on change un prompt → invalide tout le cache d'un coup.
PROMPT_VERSION = "v3-gemini-pro-claude-haiku-strict-cache-key"


def _normalize_tiktok_url(url: str) -> str:
    """Retire tracking params, lowercase, garde uniquement /@user/video/ID."""
    try:
        u = urlparse(url.strip())
        # Path : /@username/video/12345
        path = re.sub(r"/+$", "", u.path)
        # Supprimer tous les params (utm, _t, _r, share_app, etc.)
        return urlunparse((u.scheme.lower() or "https", u.netloc.lower(), path, "", "", ""))
    except Exception:
        return url.strip().lower()


def hash_video_url(url: str) -> str:
    return hashlib.sha256(_normalize_tiktok_url(url).encode()).hexdigest()


def hash_video_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_cached(video_hash: str, pipeline: str = "pro") -> Optional[dict]:
    """Retourne le résultat caché ou None. Match exact sur pipeline + version."""
    if not supabase_service:
        return None
    try:
        r = (supabase_service.table("analysis_cache")
             .select("result")
             .eq("video_hash", video_hash)
             .eq("pipeline", pipeline)
             .eq("prompt_version", PROMPT_VERSION)
             .limit(1).execute())
        if r.data and r.data[0].get("result"):
            return r.data[0]["result"]
        return None
    except Exception as e:
        logger.warning("[analysis_cache] lookup failed (%s) — cache miss silencieux", e)
        return None


def store(video_hash: str, result: dict, pipeline: str = "pro") -> None:
    """Stocke (upsert) un résultat d'analyse. Échec silencieux."""
    if not supabase_service or not isinstance(result, dict):
        return
    try:
        supabase_service.table("analysis_cache").upsert({
            "video_hash":     video_hash,
            "result":         result,
            "pipeline":       pipeline,
            "prompt_version": PROMPT_VERSION,
        }, on_conflict="video_hash").execute()
    except Exception as e:
        logger.warning("[analysis_cache] store failed (%s) — résultat non caché", e)
