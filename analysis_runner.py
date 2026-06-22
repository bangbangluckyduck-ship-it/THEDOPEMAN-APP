"""Pipeline d'analyse vidéo Pro+ encapsulé pour mode asynchrone.

Réutilise les briques existantes (analyze_video_native + synthesize_analysis)
mais en mettant à jour le job Supabase à chaque étape, pour que le frontend
qui poll voit la progression.

Le pipeline est strictement le même qu'en mode synchrone — c'est juste
l'enrobage qui change (status + stage + result dans la DB).
"""
from __future__ import annotations

import asyncio
import logging
import os
import tempfile
import time
from typing import Optional

import analysis_cache
import analysis_jobs

logger = logging.getLogger(__name__)


async def _run_url_pipeline(url: str, product: Optional[str], price: Optional[str],
                            user_tier: str) -> dict:
    """Download URL → downscale → Gemini Pro vidéo → synthèse."""
    from analyzer import analyze_video_native, synthesize_analysis
    from video_processor import downscale_720p

    loop = asyncio.get_event_loop()
    tmpdir = tempfile.mkdtemp(prefix="async_url_")
    video_path: Optional[str] = None
    downscaled_path: Optional[str] = None
    try:
        # 1. Téléchargement yt-dlp
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

        video_path = await asyncio.wait_for(loop.run_in_executor(None, _download), timeout=90.0)
        if not video_path or not os.path.exists(video_path):
            raise Exception("Vidéo introuvable après téléchargement")

        # 2. Downscale 720p
        downscaled_path = await loop.run_in_executor(None, downscale_720p, video_path)

        # 3. Gemini Pro vidéo native
        visual_result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_video_native, downscaled_path, product, price),
            timeout=240.0,
        )
        transcript = visual_result.get("transcript") if isinstance(visual_result, dict) else None

        # 4. Synthèse
        result = await asyncio.wait_for(
            loop.run_in_executor(None, synthesize_analysis, visual_result, transcript, None, product, user_tier, price),
            timeout=180.0,
        )
        result["transcript"] = transcript
        result["pipeline"] = "gemini-pro-native-async"
        result["cta_visuel"] = visual_result.get("cta_visuel") if isinstance(visual_result, dict) else None
        result["cta_audio"] = visual_result.get("cta_audio") if isinstance(visual_result, dict) else None
        result["source"] = "url"
        result["source_url"] = url
        return result
    finally:
        if downscaled_path and downscaled_path != video_path:
            try: os.unlink(downscaled_path)
            except Exception: pass
        try:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
        except Exception: pass


async def _run_upload_pipeline(video_bytes: bytes, product: Optional[str],
                               price: Optional[str], user_tier: str) -> dict:
    """Upload vidéo → downscale → Gemini Pro → synthèse."""
    from analyzer import analyze_video_native, synthesize_analysis
    from video_processor import downscale_720p

    loop = asyncio.get_event_loop()
    video_path: Optional[str] = None
    downscaled_path: Optional[str] = None
    try:
        # 1. Écrire en fichier tmp
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            video_path = tmp.name
            tmp.write(video_bytes)

        # 2. Downscale 720p
        downscaled_path = await loop.run_in_executor(None, downscale_720p, video_path)

        # 3. Gemini Pro vidéo native
        visual_result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_video_native, downscaled_path, product, price),
            timeout=240.0,
        )
        transcript = visual_result.get("transcript") if isinstance(visual_result, dict) else None

        # 4. Synthèse
        result = await asyncio.wait_for(
            loop.run_in_executor(None, synthesize_analysis, visual_result, transcript, None, product, user_tier, price),
            timeout=180.0,
        )
        result["transcript"] = transcript
        result["pipeline"] = "gemini-pro-native-async"
        result["cta_visuel"] = visual_result.get("cta_visuel") if isinstance(visual_result, dict) else None
        result["cta_audio"] = visual_result.get("cta_audio") if isinstance(visual_result, dict) else None
        result["source"] = "upload"
        return result
    finally:
        if downscaled_path and downscaled_path != video_path:
            try: os.unlink(downscaled_path)
            except Exception: pass
        if video_path:
            try: os.unlink(video_path)
            except Exception: pass


async def process_url_job(job_id: str, url: str, product: Optional[str],
                          price: Optional[str], user_tier: str,
                          user_email: str, video_hash: Optional[str] = None) -> None:
    """Coroutine de traitement d'un job URL. Met à jour le job au fil de l'eau."""
    started = time.time()
    try:
        analysis_jobs.mark_running(job_id, stage="download")

        # Cache lookup si pas de product/price custom
        can_cache = not product and not price
        cache_key = video_hash or (analysis_cache.hash_video_url(url) if can_cache else None)
        if can_cache and cache_key:
            cached = analysis_cache.get_cached(cache_key, pipeline="pro")
            if cached:
                cached["from_cache"] = True
                analysis_jobs.mark_done(job_id, cached, duration_ms=int((time.time() - started) * 1000))
                return

        analysis_jobs.update_stage(job_id, "vision")
        result = await _run_url_pipeline(url, product, price, user_tier)
        result["from_cache"] = False

        # Cache store si autorisé
        if can_cache and cache_key:
            try:
                analysis_cache.store(cache_key, result, pipeline="pro")
            except Exception:
                pass

        duration_ms = int((time.time() - started) * 1000)
        result["analysis_duration_ms"] = duration_ms
        analysis_jobs.mark_done(job_id, result, duration_ms=duration_ms)
    except Exception as e:
        logger.exception("[analysis_runner] URL job %s failed", job_id)
        analysis_jobs.mark_error(job_id, str(e)[:500])


async def process_upload_job(job_id: str, video_bytes: bytes, product: Optional[str],
                             price: Optional[str], user_tier: str,
                             user_email: str, video_hash: Optional[str] = None) -> None:
    """Coroutine de traitement d'un job upload. Met à jour le job au fil de l'eau."""
    started = time.time()
    try:
        analysis_jobs.mark_running(job_id, stage="downscale")

        can_cache = not product and not price
        cache_key = video_hash if can_cache else None
        if can_cache and cache_key:
            cached = analysis_cache.get_cached(cache_key, pipeline="pro")
            if cached:
                cached["from_cache"] = True
                analysis_jobs.mark_done(job_id, cached, duration_ms=int((time.time() - started) * 1000))
                return

        analysis_jobs.update_stage(job_id, "vision")
        result = await _run_upload_pipeline(video_bytes, product, price, user_tier)
        result["from_cache"] = False

        if can_cache and cache_key:
            try:
                analysis_cache.store(cache_key, result, pipeline="pro")
            except Exception:
                pass

        duration_ms = int((time.time() - started) * 1000)
        result["analysis_duration_ms"] = duration_ms
        analysis_jobs.mark_done(job_id, result, duration_ms=duration_ms)
    except Exception as e:
        logger.exception("[analysis_runner] Upload job %s failed", job_id)
        analysis_jobs.mark_error(job_id, str(e)[:500])
