"""Jobs d'analyse vidéo asynchrones — l'utilisateur soumet, on lui renvoie un
job_id, puis il peut poller ou revenir voir le résultat plus tard.

Table Supabase à créer (SQL editor) :

  CREATE TABLE IF NOT EXISTS analysis_jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email      TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'queued',  -- queued|running|done|error
    source          TEXT NOT NULL,                   -- 'url' | 'upload'
    source_url      TEXT,
    product         TEXT,
    price           TEXT,
    video_hash      TEXT,
    title           TEXT,        -- libellé court pour l'historique
    progress_stage  TEXT,        -- dernière étape connue (download|downscale|vision|synthesis)
    result          JSONB,
    error_message   TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    duration_ms     INTEGER
  );
  CREATE INDEX IF NOT EXISTS idx_jobs_user ON analysis_jobs(user_email, created_at DESC);
  CREATE INDEX IF NOT EXISTS idx_jobs_status ON analysis_jobs(status, created_at);
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from supabase_client import supabase_service

logger = logging.getLogger(__name__)

_STATUS_QUEUED = "queued"
_STATUS_RUNNING = "running"
_STATUS_DONE = "done"
_STATUS_ERROR = "error"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_job(user_email: str, source: str, *,
               source_url: Optional[str] = None,
               product: Optional[str] = None,
               price: Optional[str] = None,
               video_hash: Optional[str] = None,
               title: Optional[str] = None) -> Optional[str]:
    """Crée un job en status='queued'. Retourne le job_id (UUID) ou None si Supabase down."""
    if not supabase_service:
        return None
    try:
        row = {
            "user_email": (user_email or "").lower(),
            "status": _STATUS_QUEUED,
            "source": source,
            "source_url": source_url,
            "product": product,
            "price": price,
            "video_hash": video_hash,
            "title": title,
        }
        r = supabase_service.table("analysis_jobs").insert(row).execute()
        return r.data[0]["id"] if r.data else None
    except Exception as e:
        logger.warning("[analysis_jobs] create failed: %s", e)
        return None


def get_job(job_id: str, user_email: Optional[str] = None) -> Optional[dict]:
    """Récupère un job. Si user_email fourni, vérifie l'ownership (sécurité)."""
    if not supabase_service or not job_id:
        return None
    try:
        q = supabase_service.table("analysis_jobs").select("*").eq("id", job_id)
        if user_email:
            q = q.eq("user_email", (user_email or "").lower())
        r = q.limit(1).execute()
        return r.data[0] if r.data else None
    except Exception as e:
        logger.warning("[analysis_jobs] get failed: %s", e)
        return None


def list_user_jobs(user_email: str, limit: int = 20) -> list[dict]:
    """Liste les N derniers jobs d'un user, plus récents en premier."""
    if not supabase_service:
        return []
    try:
        r = (supabase_service.table("analysis_jobs")
             .select("id,status,source,source_url,product,title,progress_stage,error_message,created_at,completed_at,duration_ms")
             .eq("user_email", (user_email or "").lower())
             .order("created_at", desc=True)
             .limit(limit).execute())
        return r.data or []
    except Exception as e:
        logger.warning("[analysis_jobs] list failed: %s", e)
        return []


def mark_running(job_id: str, stage: Optional[str] = None) -> None:
    if not supabase_service or not job_id:
        return
    try:
        upd = {"status": _STATUS_RUNNING, "started_at": _now_iso()}
        if stage:
            upd["progress_stage"] = stage
        supabase_service.table("analysis_jobs").update(upd).eq("id", job_id).execute()
    except Exception as e:
        logger.warning("[analysis_jobs] mark_running failed: %s", e)


def update_stage(job_id: str, stage: str) -> None:
    """Met à jour l'étape courante (pour que le front polling l'affiche)."""
    if not supabase_service or not job_id:
        return
    try:
        supabase_service.table("analysis_jobs").update({"progress_stage": stage}).eq("id", job_id).execute()
    except Exception as e:
        logger.warning("[analysis_jobs] update_stage failed: %s", e)


def mark_done(job_id: str, result: dict, duration_ms: int) -> None:
    if not supabase_service or not job_id:
        return
    try:
        supabase_service.table("analysis_jobs").update({
            "status": _STATUS_DONE,
            "result": result,
            "completed_at": _now_iso(),
            "duration_ms": duration_ms,
        }).eq("id", job_id).execute()
    except Exception as e:
        logger.warning("[analysis_jobs] mark_done failed: %s", e)


def create_done_job(user_email: str, source: str, result: dict, *,
                    source_url: Optional[str] = None,
                    product: Optional[str] = None,
                    price: Optional[str] = None,
                    title: Optional[str] = None,
                    duration_ms: Optional[int] = None) -> Optional[str]:
    """Crée un job déjà en status='done' avec son résultat. Utilisé pour les
    analyses SYNCHRONES (déjà terminées au moment de l'écriture en DB), afin
    qu'elles apparaissent aussi dans "Mes analyses" cross-device, à côté
    des jobs async."""
    if not supabase_service:
        return None
    try:
        row = {
            "user_email": (user_email or "").lower(),
            "status": _STATUS_DONE,
            "source": source,
            "source_url": source_url,
            "product": product,
            "price": price,
            "title": title,
            "result": result,
            "started_at": _now_iso(),
            "completed_at": _now_iso(),
            "duration_ms": duration_ms,
        }
        r = supabase_service.table("analysis_jobs").insert(row).execute()
        return r.data[0]["id"] if r.data else None
    except Exception as e:
        logger.warning("[analysis_jobs] create_done_job failed: %s", e)
        return None


def mark_error(job_id: str, error_message: str) -> None:
    if not supabase_service or not job_id:
        return
    try:
        supabase_service.table("analysis_jobs").update({
            "status": _STATUS_ERROR,
            "error_message": (error_message or "")[:1000],
            "completed_at": _now_iso(),
        }).eq("id", job_id).execute()
    except Exception as e:
        logger.warning("[analysis_jobs] mark_error failed: %s", e)


def cleanup_stale_running(timeout_minutes: int = 10) -> int:
    """Au démarrage de l'app : tous les jobs 'running' qui ont commencé il y a
    plus de N minutes sont marqués 'error' (probablement orphelins après un
    crash/deploy Render). Retourne le nombre de jobs nettoyés."""
    if not supabase_service:
        return 0
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=timeout_minutes)).isoformat()
        r = (supabase_service.table("analysis_jobs")
             .update({
                 "status": _STATUS_ERROR,
                 "error_message": "Job interrompu (worker redémarré). Relance l'analyse.",
                 "completed_at": _now_iso(),
             })
             .eq("status", _STATUS_RUNNING)
             .lt("started_at", cutoff)
             .execute())
        n = len(r.data or [])
        if n > 0:
            logger.info("[analysis_jobs] nettoyé %s job(s) orphelin(s)", n)
        return n
    except Exception as e:
        logger.warning("[analysis_jobs] cleanup failed: %s", e)
        return 0
