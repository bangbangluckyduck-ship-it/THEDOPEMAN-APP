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


# ── Plafond de concurrence des jobs ──────────────────────────────────────
# Les routes SYNCHRONES de main.py sont sérialisées par ANALYSIS_SEMAPHORE, mais
# ce module — le chemin asynchrone, celui vers lequel tous les comptes payants
# sont dirigés — n'avait AUCUNE limite : chaque job lancé par
# `asyncio.create_task()` démarrait immédiatement. N jobs simultanés = N ffmpeg
# de downscale + N envois vidéo en parallèle sur une instance à 1 CPU / 2 Go,
# c'est-à-dire exactement la cause des OOM de juillet, réintroduite par une autre
# porte.
#
# Le job attend son tour au lieu d'échouer : l'utilisateur est déjà en
# asynchrone, il ne perçoit qu'un temps de traitement un peu plus long.
# Réglable sans redéploiement si le profil mémoire réel le permet.
_MAX_CONCURRENT_JOBS = max(1, int(os.getenv("ANALYSIS_MAX_CONCURRENT_JOBS", "2")))
_JOB_SEMAPHORE = asyncio.Semaphore(_MAX_CONCURRENT_JOBS)
_QUEUED_STAGE = "En file d'attente…"


# ── Notifications email à la fin du job ──────────────────────────────────
def _app_url() -> str:
    return os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")


def _safe_send_email(user_email: str, subject: str, html: str) -> None:
    """Best-effort : ne fait jamais planter le job si l'envoi échoue."""
    try:
        from email_service import send_transactional_email, _wrap, _button
        send_transactional_email(user_email, subject, html)
    except Exception as e:
        logger.warning("[analysis_runner] email send failed for %s: %s", user_email, e)


# ── Textes des e-mails d'analyse ─────────────────────────────────────────────
# Ces deux e-mails-là sont traduisibles parce que le job connaît la langue
# demandée (capturée au moment de la soumission). Les e-mails d'authentification
# — bienvenue, mot de passe oublié — ne le sont PAS : ils partent hors de tout
# contexte de requête et il n'existe aucune colonne `lang` sur la table `users`
# pour retrouver la préférence. Les traduire demande d'abord cette colonne.
_MAILS = {
    "fr": {
        "objet_ok": "✅ Ton analyse Qeerah est prête",
        "titre_ok": "Ton analyse est prête ✅",
        "salut": "Salut,", "bonne_nouvelle": "Bonne nouvelle 🎉 —",
        "vient_de_terminer": "vient de terminer.",
        "note": "Note", "retrouver": "Tu peux la retrouver dans",
        "mes_analyses": "Mes analyses", "bouton_ok": "Voir mon analyse →",
        "defaut_titre": "Ton analyse",
        "pied": "Ce mail t'a été envoyé parce que tu as lancé une analyse en arrière-plan sur Qeerah.",
        "objet_ko": "❌ Ton analyse Qeerah a échoué", "titre_ko": "Analyse échouée ❌",
        "aie": "Aïe —", "pas_analysee": "n'a pas pu être analysée.",
        "relancer": "Tu peux relancer l'analyse depuis l'app :",
        "bouton_ko": "Retour à l'app", "err_inconnue": "Erreur inconnue",
    },
    "en": {
        "objet_ok": "✅ Your Qeerah analysis is ready",
        "titre_ok": "Your analysis is ready ✅",
        "salut": "Hi,", "bonne_nouvelle": "Good news 🎉 —",
        "vient_de_terminer": "has just finished.",
        "note": "Score", "retrouver": "You'll find it in",
        "mes_analyses": "My analyses", "bouton_ok": "See my analysis →",
        "defaut_titre": "Your analysis",
        "pied": "You're getting this email because you started a background analysis on Qeerah.",
        "objet_ko": "❌ Your Qeerah analysis failed", "titre_ko": "Analysis failed ❌",
        "aie": "Ouch —", "pas_analysee": "could not be analysed.",
        "relancer": "You can start the analysis again from the app:",
        "bouton_ko": "Back to the app", "err_inconnue": "Unknown error",
    },
    "pt-br": {
        "objet_ok": "✅ Sua análise Qeerah está pronta",
        "titre_ok": "Sua análise está pronta ✅",
        "salut": "Oi,", "bonne_nouvelle": "Boa notícia 🎉 —",
        "vient_de_terminer": "acabou de terminar.",
        "note": "Nota", "retrouver": "Você encontra ela em",
        "mes_analyses": "Minhas análises", "bouton_ok": "Ver minha análise →",
        "defaut_titre": "Sua análise",
        "pied": "Você recebeu este e-mail porque iniciou uma análise em segundo plano na Qeerah.",
        "objet_ko": "❌ Sua análise Qeerah falhou", "titre_ko": "Análise falhou ❌",
        "aie": "Ops —", "pas_analysee": "não pôde ser analisada.",
        "relancer": "Você pode rodar a análise de novo pelo app:",
        "bouton_ko": "Voltar ao app", "err_inconnue": "Erro desconhecido",
    },
    "es": {
        "objet_ok": "✅ Tu análisis de Qeerah está listo",
        "titre_ok": "Tu análisis está listo ✅",
        "salut": "Hola:", "bonne_nouvelle": "Buenas noticias 🎉 —",
        "vient_de_terminer": "acaba de terminar.",
        "note": "Puntuación", "retrouver": "Lo encuentras en",
        "mes_analyses": "Mis análisis", "bouton_ok": "Ver mi análisis →",
        "defaut_titre": "Tu análisis",
        "pied": "Recibes este correo porque lanzaste un análisis en segundo plano en Qeerah.",
        "objet_ko": "❌ Tu análisis de Qeerah ha fallado", "titre_ko": "Análisis fallido ❌",
        "aie": "Vaya —", "pas_analysee": "no se ha podido analizar.",
        "relancer": "Puedes volver a lanzar el análisis desde la app:",
        "bouton_ko": "Volver a la app", "err_inconnue": "Error desconocido",
    },
    "es-mx": {
        "objet_ok": "✅ Tu análisis de Qeerah ya está listo",
        "titre_ok": "Tu análisis ya está listo ✅",
        "salut": "Hola:", "bonne_nouvelle": "Buenas noticias 🎉 —",
        "vient_de_terminer": "acaba de terminar.",
        "note": "Puntuación", "retrouver": "Lo encuentras en",
        "mes_analyses": "Mis análisis", "bouton_ok": "Ver mi análisis →",
        "defaut_titre": "Tu análisis",
        "pied": "Recibes este correo porque lanzaste un análisis en segundo plano en Qeerah.",
        "objet_ko": "❌ Tu análisis de Qeerah falló", "titre_ko": "Análisis fallido ❌",
        "aie": "Uy —", "pas_analysee": "no se pudo analizar.",
        "relancer": "Puedes volver a lanzar el análisis desde la app:",
        "bouton_ko": "Volver a la app", "err_inconnue": "Error desconocido",
    },
    "it": {
        "objet_ok": "✅ La tua analisi Qeerah è pronta",
        "titre_ok": "La tua analisi è pronta ✅",
        "salut": "Ciao,", "bonne_nouvelle": "Buona notizia 🎉 —",
        "vient_de_terminer": "ha appena finito.",
        "note": "Punteggio", "retrouver": "La ritrovi in",
        "mes_analyses": "Le mie analisi", "bouton_ok": "Vedi la mia analisi →",
        "defaut_titre": "La tua analisi",
        "pied": "Ricevi questa mail perché hai avviato un'analisi in background su Qeerah.",
        "objet_ko": "❌ La tua analisi Qeerah non è riuscita",
        "titre_ko": "Analisi non riuscita ❌",
        "aie": "Ahi —", "pas_analysee": "non è stata analizzata.",
        "relancer": "Puoi rilanciare l'analisi dall'app:",
        "bouton_ko": "Torna all'app", "err_inconnue": "Errore sconosciuto",
    },
    "de": {
        "objet_ok": "✅ Deine Qeerah-Analyse ist fertig",
        "titre_ok": "Deine Analyse ist fertig ✅",
        "salut": "Hallo,", "bonne_nouvelle": "Gute Nachricht 🎉 —",
        "vient_de_terminer": "ist gerade fertig geworden.",
        "note": "Wertung", "retrouver": "Du findest sie unter",
        "mes_analyses": "Meine Analysen", "bouton_ok": "Meine Analyse ansehen →",
        "defaut_titre": "Deine Analyse",
        "pied": "Du bekommst diese Mail, weil du auf Qeerah eine Analyse im Hintergrund gestartet hast.",
        "objet_ko": "❌ Deine Qeerah-Analyse ist fehlgeschlagen",
        "titre_ko": "Analyse fehlgeschlagen ❌",
        "aie": "Autsch —", "pas_analysee": "konnte nicht analysiert werden.",
        "relancer": "Du kannst die Analyse in der App neu starten:",
        "bouton_ko": "Zurück zur App", "err_inconnue": "Unbekannter Fehler",
    },
}


def _mail_textes(lang: Optional[str]) -> dict:
    """Textes de l'e-mail dans la langue du job. Repli : français."""
    try:
        from analyzer import normaliser_langue
        code = normaliser_langue(lang)
    except Exception:
        code = "fr"
    return _MAILS.get(code) or _MAILS["fr"]


def _send_done_email(user_email: str, result: dict, job_id: str,
                     title: Optional[str] = None, lang: str = "fr") -> None:
    """Email à l'utilisateur : analyse terminée + lien vers Mes analyses."""
    if not user_email:
        return
    try:
        from email_service import _wrap, _button
    except Exception:
        return
    tx = _mail_textes(lang)
    score = None
    if isinstance(result, dict):
        score = result.get("score_global") or result.get("note_globale") or result.get("note")
    label = (title or tx["defaut_titre"])[:80]
    score_html = (
        f'<p style="font-size:24px;font-weight:800;color:#6c5ce7;margin:8px 0">'
        f'{tx["note"]}&nbsp;: {score}/100</p>'
    ) if score is not None else ''
    btn_html = _button(tx["bouton_ok"], f"{_app_url()}/app?job={job_id}")
    body = (
        f"<p>{tx['salut']}</p>"
        f"<p>{tx['bonne_nouvelle']} <strong>{label}</strong> {tx['vient_de_terminer']}</p>"
        f"{score_html}"
        f"<p>{tx['retrouver']} <strong>{tx['mes_analyses']}</strong> :</p>"
        f"{btn_html}"
        f'<p style="font-size:13px;color:#9a9ab0;margin-top:24px">{tx["pied"]}</p>'
    )
    html = _wrap(tx["titre_ok"], body)
    _safe_send_email(user_email, tx["objet_ok"], html)


def _result_utilisable(result) -> bool:
    """Un résultat sans contenu ne doit JAMAIS être présenté comme une analyse.

    Incident du 04/09/2026 : la synthèse est revenue tronquée, le parsing a
    rendu `{"error": ...}`, et le job a quand même été marqué « réussi » avec
    l'email « ✅ ton analyse est prête ». L'utilisateur a reçu un écran vide, en
    plein démarchage, sans le moindre signal d'erreur nulle part. Un échec doit
    ressembler à un échec : job en erreur, email d'échec, crédit rendu.
    """
    if not isinstance(result, dict) or result.get("error"):
        return False
    return any(result.get(k) for k in
               ("analyse_8_dimensions", "scores", "detection", "score_global"))


def _rendre_le_credit(user_email: str, user_tier: str) -> None:
    """Le quota est débité à la CRÉATION du job (anti-spam) : sur échec, on rend."""
    try:
        import analysis_quota
        analysis_quota.decrement(user_email, user_tier)
    except Exception as e:
        logger.warning("[analysis_runner] remboursement quota impossible : %s", e)


def _send_error_email(user_email: str, error_message: str, job_id: str,
                      title: Optional[str] = None, lang: str = "fr") -> None:
    """Email à l'utilisateur : l'analyse a échoué."""
    if not user_email:
        return
    try:
        from email_service import _wrap, _button
    except Exception:
        return
    tx = _mail_textes(lang)
    label = (title or tx["defaut_titre"])[:80]
    # Le message d'erreur technique lui-même reste tel quel : il vient du
    # pipeline, pas d'un texte d'interface, et le traduire n'aiderait personne
    # à le diagnostiquer.
    err_short = error_message[:300] if error_message else tx["err_inconnue"]
    btn_html = _button(tx["bouton_ko"], f"{_app_url()}/app?job={job_id}")
    body = (
        f"<p>{tx['salut']}</p>"
        f"<p>{tx['aie']} <strong>{label}</strong> {tx['pas_analysee']}</p>"
        f'<p style="background:#fff5f5;border-left:3px solid #e74c3c;padding:12px;border-radius:6px;font-size:13px;color:#7a2020">{err_short}</p>'
        f"<p>{tx['relancer']}</p>"
        f"{btn_html}"
    )
    html = _wrap(tx["titre_ko"], body)
    _safe_send_email(user_email, tx["objet_ko"], html)


async def _run_url_pipeline(url: str, product: Optional[str], price: Optional[str],
                            user_tier: str, user_role: Optional[str] = None,
                            on_stage=None, lang: str = "fr") -> dict:
    """Download URL → downscale → Gemini vidéo → synthèse.

    `on_stage(nom)` signale les étapes qui se produisent À L'INTÉRIEUR du
    pipeline. Sans ce rappel, la dernière étape connue du client restait
    « vision » pendant toute la rédaction : la barre de progression semblait
    figée alors que le travail avançait.
    """
    from analyzer import analyze_video_native, synthesize_analysis
    from video_processor import downscale_720p, YDL_TIKTOK_EXTRACTOR_ARGS

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
                "extractor_args": YDL_TIKTOK_EXTRACTOR_ARGS,   # contourne le challenge anti-bot TikTok
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
            loop.run_in_executor(None, analyze_video_native, downscaled_path, product, price, lang),
            timeout=240.0,
        )
        transcript = visual_result.get("transcript") if isinstance(visual_result, dict) else None

        # 4. Synthèse
        if on_stage:
            try: on_stage("synthesis")
            except Exception: pass
        result = await asyncio.wait_for(
            loop.run_in_executor(None, synthesize_analysis, visual_result, transcript, None, product, user_tier, price, user_role, lang),
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


async def _run_upload_pipeline(video_path: str, product: Optional[str],
                               price: Optional[str], user_tier: str,
                               user_role: Optional[str] = None,
                               on_stage=None, lang: str = "fr") -> dict:
    """Upload vidéo (déjà sur disque, streamée par la route) → downscale →
    Gemini → synthèse. Ne charge jamais la vidéo entière en RAM.

    `on_stage(nom)` : cf. _run_url_pipeline."""
    from analyzer import analyze_video_native, synthesize_analysis
    from video_processor import downscale_720p

    loop = asyncio.get_event_loop()
    downscaled_path: Optional[str] = None
    try:
        # 1. Downscale 720p
        downscaled_path = await loop.run_in_executor(None, downscale_720p, video_path)

        # 3. Gemini Pro vidéo native
        visual_result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_video_native, downscaled_path, product, price, lang),
            timeout=240.0,
        )
        transcript = visual_result.get("transcript") if isinstance(visual_result, dict) else None

        # 4. Synthèse
        if on_stage:
            try: on_stage("synthesis")
            except Exception: pass
        result = await asyncio.wait_for(
            loop.run_in_executor(None, synthesize_analysis, visual_result, transcript, None, product, user_tier, price, user_role, lang),
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
        try: os.unlink(video_path)
        except Exception: pass


async def process_url_job(job_id: str, url: str, product: Optional[str],
                          price: Optional[str], user_tier: str,
                          user_email: str, video_hash: Optional[str] = None,
                          job_title: Optional[str] = None,
                          user_role: Optional[str] = None,
                          lang: str = "fr") -> None:
    """Coroutine de traitement d'un job URL. Met à jour le job au fil de l'eau.

    `lang` est capturé au moment de la DEMANDE, pas au moment de l'exécution :
    le job tourne en tâche de fond, il n'y a plus de requête ni de cookie à
    consulter quand la rédaction commence.
    """
    started = time.time()
    try:
        analysis_jobs.mark_running(job_id, stage="download")

        # Cache lookup si pas de product/price custom. user_role fait partie de
        # la clé (pas un facteur qui désactive le cache) : même vidéo + rôle
        # différent = résultat différent, donc entrée de cache distincte.
        can_cache = not product and not price
        _base_key = video_hash or (analysis_cache.hash_video_url(url) if can_cache else None)
        cache_key = f"{_base_key}:{user_role or 'none'}" if _base_key else None
        if can_cache and cache_key:
            cached = analysis_cache.get_cached(cache_key, pipeline="pro", lang=lang)
            if cached:
                cached["from_cache"] = True
                analysis_jobs.mark_done(job_id, cached, duration_ms=int((time.time() - started) * 1000))
                _send_done_email(user_email, cached, job_id, title=job_title, lang=lang)
                return

        # Le sémaphore est pris APRÈS la recherche en cache : un cache-hit ne
        # consomme aucune ressource lourde, il ne doit pas attendre son tour.
        if _JOB_SEMAPHORE.locked():
            analysis_jobs.update_stage(job_id, _QUEUED_STAGE)
        async with _JOB_SEMAPHORE:
            analysis_jobs.update_stage(job_id, "vision")
            result = await _run_url_pipeline(
                url, product, price, user_tier, user_role,
                on_stage=lambda s: analysis_jobs.update_stage(job_id, s),
                lang=lang)
        result["from_cache"] = False

        # Cache store si autorisé
        if can_cache and cache_key:
            try:
                analysis_cache.store(cache_key, result, pipeline="pro", lang=lang)
            except Exception:
                pass

        duration_ms = int((time.time() - started) * 1000)
        result["analysis_duration_ms"] = duration_ms
        # Dernier verrou avant livraison : rien de vide ne sort d'ici en « réussi ».
        if not _result_utilisable(result):
            raise Exception(result.get("error") if isinstance(result, dict) and result.get("error")
                            else "L'analyse n'a rien produit d'exploitable.")
        analysis_jobs.mark_done(job_id, result, duration_ms=duration_ms)
        _send_done_email(user_email, result, job_id, title=job_title, lang=lang)
    except Exception as e:
        logger.exception("[analysis_runner] URL job %s failed", job_id)
        err_msg = str(e)[:500]
        analysis_jobs.mark_error(job_id, err_msg)
        _rendre_le_credit(user_email, user_tier)
        _send_error_email(user_email, err_msg, job_id, title=job_title, lang=lang)


async def process_upload_job(job_id: str, video_path: str, product: Optional[str],
                             price: Optional[str], user_tier: str,
                             user_email: str, video_hash: Optional[str] = None,
                             job_title: Optional[str] = None,
                             user_role: Optional[str] = None,
                             lang: str = "fr") -> None:
    """Coroutine de traitement d'un job upload. Met à jour le job au fil de l'eau.

    `lang` : cf. process_url_job — capturé à la demande, pas à l'exécution."""
    started = time.time()
    try:
        analysis_jobs.mark_running(job_id, stage="downscale")

        can_cache = not product and not price
        cache_key = f"{video_hash}:{user_role or 'none'}" if (can_cache and video_hash) else None
        if can_cache and cache_key:
            cached = analysis_cache.get_cached(cache_key, pipeline="pro", lang=lang)
            if cached:
                cached["from_cache"] = True
                analysis_jobs.mark_done(job_id, cached, duration_ms=int((time.time() - started) * 1000))
                _send_done_email(user_email, cached, job_id, title=job_title, lang=lang)
                return

        if _JOB_SEMAPHORE.locked():
            analysis_jobs.update_stage(job_id, _QUEUED_STAGE)
        async with _JOB_SEMAPHORE:
            analysis_jobs.update_stage(job_id, "vision")
            result = await _run_upload_pipeline(
                video_path, product, price, user_tier, user_role,
                on_stage=lambda s: analysis_jobs.update_stage(job_id, s),
                lang=lang)
        result["from_cache"] = False

        if can_cache and cache_key:
            try:
                analysis_cache.store(cache_key, result, pipeline="pro", lang=lang)
            except Exception:
                pass

        duration_ms = int((time.time() - started) * 1000)
        result["analysis_duration_ms"] = duration_ms
        # Dernier verrou avant livraison : rien de vide ne sort d'ici en « réussi ».
        if not _result_utilisable(result):
            raise Exception(result.get("error") if isinstance(result, dict) and result.get("error")
                            else "L'analyse n'a rien produit d'exploitable.")
        analysis_jobs.mark_done(job_id, result, duration_ms=duration_ms)
        _send_done_email(user_email, result, job_id, title=job_title, lang=lang)
    except Exception as e:
        logger.exception("[analysis_runner] Upload job %s failed", job_id)
        err_msg = str(e)[:500]
        analysis_jobs.mark_error(job_id, err_msg)
        _rendre_le_credit(user_email, user_tier)
        _send_error_email(user_email, err_msg, job_id, title=job_title, lang=lang)
    finally:
        # Cache-hit / erreur avant le pipeline : le tmpfile n'a pas encore été
        # supprimé par _run_upload_pipeline. Double unlink = no-op silencieux.
        try: os.unlink(video_path)
        except Exception: pass
