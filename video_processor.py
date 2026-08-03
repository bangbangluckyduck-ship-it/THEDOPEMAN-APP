from __future__ import annotations
import subprocess
import os
import re
import base64
import tempfile
from typing import List, Optional


def _ffmpeg() -> str:
    # Use system ffmpeg (installed via apt on Render)
    return "ffmpeg"


def _probe(video_path: str) -> dict:
    """Caractéristiques de la vidéo, via ffprobe. Dict vide si indisponible.

    Coût : ~0,1 s (lecture d'en-têtes, aucun décodage). À comparer aux dizaines
    de secondes d'un ré-encodage — d'où l'intérêt de demander avant de faire.
    """
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "stream=codec_name,codec_type,height", "-of", "default=nw=1", video_path],
            capture_output=True, timeout=15, text=True,
        )
        if out.returncode != 0:
            return {}
        infos: dict = {"height": 0, "vcodec": "", "acodec": ""}
        courant = None
        for ligne in out.stdout.splitlines():
            cle, _, val = ligne.partition("=")
            if cle == "codec_type":
                courant = val
            elif cle == "codec_name":
                if courant == "video" and not infos["vcodec"]:
                    infos["vcodec"] = val
                elif courant == "audio" and not infos["acodec"]:
                    infos["acodec"] = val
            elif cle == "height" and val.isdigit():
                infos["height"] = max(infos["height"], int(val))
        return infos
    except Exception:
        return {}


def downscale_720p(video_path: str) -> str:
    """Downscale une vidéo à 720p H.264 + audio AAC pour réduire le temps d'upload
    et de processing Gemini. Garde le ratio, qualité d'analyse identique.

    Retourne le path du fichier downscalé (à supprimer par l'appelant après usage).
    Si la conversion échoue, retourne le path original (jamais bloquant)."""
    import time as _t
    _t0 = _t.monotonic()

    # ⚠️ Ce ré-encodage était INCONDITIONNEL. Or le téléchargement demande déjà
    # `best[height<=720]` : on ré-encodait donc du 720p en 720p, pour rien —
    # environ 25 s de calcul H.264 sur l'unique processeur de Render, à chaque
    # analyse. C'était le deuxième poste de temps du pipeline, derrière la
    # rédaction, et personne ne le voyait.
    #
    # On sonde d'abord (~0,1 s). Si la vidéo est DÉJÀ conforme à ce que produirait
    # la conversion — pas plus haute que 720p, H.264, audio AAC ou muette, dans un
    # conteneur mp4 — le ré-encodage ne changerait rien d'utile : on la garde.
    infos = _probe(video_path)
    deja_conforme = (
        infos
        and 0 < infos.get("height", 0) <= 720
        and infos.get("vcodec") == "h264"
        and infos.get("acodec", "") in ("aac", "")
        and video_path.lower().endswith(".mp4")
    )
    if deja_conforme:
        print(f"[video] ⏱ préparation : {_t.monotonic() - _t0:.1f}s — déjà conforme "
              f"({infos.get('height')}p {infos.get('vcodec')}), ré-encodage évité", flush=True)
        return video_path

    out_fd, out_path = tempfile.mkstemp(suffix="_720p.mp4")
    os.close(out_fd)
    try:
        result = subprocess.run(
            [
                _ffmpeg(), "-y", "-i", video_path,
                "-vf", "scale=-2:720",  # hauteur 720, largeur auto (multiple de 2)
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
                "-c:a", "aac", "-b:a", "96k",
                "-movflags", "+faststart",
                out_path,
            ],
            capture_output=True, timeout=60,
        )
        if result.returncode == 0 and os.path.getsize(out_path) > 1024:
            print(f"[video] ⏱ préparation : {_t.monotonic() - _t0:.1f}s — ré-encodage "
                  f"(source {infos.get('height') or '?'}p {infos.get('vcodec') or '?'})", flush=True)
            return out_path
    except Exception:
        pass
    # Échec → on retourne le path original (jamais bloquant)
    try:
        os.unlink(out_path)
    except Exception:
        pass
    return video_path


def get_duration(video_path: str) -> float:
    result = subprocess.run(
        [_ffmpeg(), "-i", video_path, "-hide_banner"],
        capture_output=True, text=True
    )
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if match:
        h, m, s = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def extract_frames(video_path: str, num_frames: int = 12) -> List[str]:
    """Extract evenly-spaced frames with extra density at start (hook) and end (CTA)."""
    duration = get_duration(video_path)
    if duration <= 0:
        duration = 30.0

    timestamps: List[float] = []

    # Hook: first 3 seconds (3 frames)
    for i in range(3):
        timestamps.append(min(i * 1.0, duration - 0.1))

    # Middle content
    mid = num_frames - 5
    for i in range(mid):
        t = 3.0 + (max(duration - 5.0, 0.1)) * i / max(mid - 1, 1)
        timestamps.append(min(t, duration - 0.1))

    # CTA: last 2 seconds (2 frames)
    timestamps.append(max(duration - 2.0, 0.1))
    timestamps.append(max(duration - 0.5, 0.1))

    frames: List[str] = []
    for ts in timestamps[:num_frames]:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name

        subprocess.run(
            [
                _ffmpeg(), "-ss", str(ts), "-i", video_path,
                "-vframes", "1", "-q:v", "3",
                "-vf", "scale=480:-2",
                "-y", tmp_path,
            ],
            capture_output=True,
        )

        if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
            with open(tmp_path, "rb") as f:
                frames.append(base64.b64encode(f.read()).decode())
            os.unlink(tmp_path)

    return frames


def extract_audio(video_path: str) -> Optional[str]:
    """Extract audio as 16kHz mono WAV. Returns temp file path or None."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_path = tmp.name

    subprocess.run(
        [
            _ffmpeg(), "-i", video_path,
            "-ar", "16000", "-ac", "1",
            "-y", audio_path,
        ],
        capture_output=True,
    )

    if os.path.exists(audio_path) and os.path.getsize(audio_path) > 100:
        return audio_path
    return None
