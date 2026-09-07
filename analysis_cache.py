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
PROMPT_VERSION = "v5-async-gemini-pro-claude-haiku"


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


def _pipeline_key(pipeline: str, lang: Optional[str]) -> str:
    """Segmente le cache PAR LANGUE sans toucher au schéma de la table.

    Depuis que les rapports sont rédigés dans la langue du compte, deux analyses
    de la MÊME vidéo ne sont plus interchangeables. La table n'a pas de colonne
    `lang` et sa contrainte d'unicité porte sur `video_hash` seul : plutôt que
    d'exiger une migration, on encode la langue dans l'étiquette `pipeline`, qui
    fait déjà partie du filtre de lecture.

    Conséquences, assumées :
      • lecture — un rapport allemand ne peut plus être servi à un francophone,
        ni l'inverse : les étiquettes ne correspondent pas, c'est un miss ;
      • écriture — une seule langue reste en cache par vidéo à un instant donné,
        les langues s'évincent. C'est un coût de calcul, jamais une erreur.

    Le français conserve l'étiquette historique (`pro`, `free`…) : tout le cache
    déjà constitué reste valide et n'est pas invalidé par ce changement.
    """
    code = (lang or "fr").strip().lower()
    return pipeline if code in ("", "fr") else f"{pipeline}:{code}"


def get_cached(video_hash: str, pipeline: str = "pro", lang: Optional[str] = None) -> Optional[dict]:
    """Retourne le résultat caché ou None. Match exact sur pipeline + langue + version."""
    if not supabase_service:
        return None
    try:
        r = (supabase_service.table("analysis_cache")
             .select("result")
             .eq("video_hash", video_hash)
             .eq("pipeline", _pipeline_key(pipeline, lang))
             .eq("prompt_version", PROMPT_VERSION)
             .limit(1).execute())
        if r.data and r.data[0].get("result"):
            return r.data[0]["result"]
        return None
    except Exception as e:
        logger.warning("[analysis_cache] lookup failed (%s) — cache miss silencieux", e)
        return None


def store(video_hash: str, result: dict, pipeline: str = "pro",
          lang: Optional[str] = None) -> None:
    """Stocke (upsert) un résultat d'analyse. Échec silencieux."""
    if not supabase_service or not isinstance(result, dict):
        return
    try:
        supabase_service.table("analysis_cache").upsert({
            "video_hash":     video_hash,
            "result":         result,
            "pipeline":       _pipeline_key(pipeline, lang),
            "prompt_version": PROMPT_VERSION,
        }, on_conflict="video_hash").execute()
    except Exception as e:
        logger.warning("[analysis_cache] store failed (%s) — résultat non caché", e)
