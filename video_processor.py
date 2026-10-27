from __future__ import annotations
import subprocess
import os
import re
import base64
import tempfile
from typing import List, Optional


# TikTok sert un challenge anti-bot aux IP de datacenter (Render) : la voie
# « page web » de yt-dlp n'y trouve ni les données du challenge ni le marqueur
# d'attente et abandonne sur « Unexpected response from webpage request »
# (diagnostiqué le 2026-09-04 : 5 analyses par lien sur 5, alors que la MÊME
# vidéo se télécharge sans erreur depuis une IP résidentielle, et que la prod
# tourne déjà le dernier yt-dlp — le « mettez-vous à jour » du message est un
# faux ami).
#
# `app_info` fait tenter D'ABORD l'API mobile, qui ne passe jamais par cette
# page. Si elle échoue, yt-dlp retombe tout seul sur la voie web : l'option ne
# peut donc rien casser, seulement ajouter une chance de réussite.
# À passer tel quel dans les `ydl_opts` de TOUT appel yt-dlp sur TikTok.
YDL_TIKTOK_EXTRACTOR_ARGS = {"tiktok": {"app_info": [""]}}

# Format à demander à yt-dlp pour TOUTE vidéo envoyée à l'analyse.
#
# TikTok sert souvent la même vidéo en H.265 (« bytevc1 », jusqu'en 1080p) ET en
# H.264 (540p). `best` prenait la 1080p H.265 — que Google n'accepte pas sous
# l'étiquette « video/mp4 » : downscale_720p la ré-encodait donc, 30 à 60 s
# mesurées en production le 26/10 pour descendre… en 405×720. La version H.264
# native (576×1024) est prête à partir, et plus nette que ce ré-encodage.
# Pas de H.264 proposé → on retombe sur l'ancien choix, et le ré-encodage reste
# le filet.
#
# `[height>0]` écarte le format « download » (H.264 lui aussi, mais filigrané,
# « Untested », sans résolution connue). Sans ce filtre, une vraie vidéo de 50 s
# est ressortie en « carrousel photo » en production le 27/10 : quand les 540p
# manquent, c'est lui que le filtre H.264 retenait. Un champ absent fait échouer
# le filtre dans yt-dlp : ce format n'est donc jamais choisi par la 1re règle.
YDL_FORMAT_VIDEO = "best[ext=mp4][vcodec~='^(avc1|h264)'][height>0]/best[ext=mp4]/best"


class PasDeVideo(Exception):
    """Le fichier n'a aucune image à analyser.

    Cas réel (26/10/2026) : une publication TikTok en mode photo (diaporama +
    musique). yt-dlp n'en récupère que la bande son (.mp3) ; ré-encodée en
    « mp4 » sans image, elle partait chez Gemini qui la rejetait (« The file
    failed to be processed », code 13) — l'utilisateur recevait une erreur 500.
    Le message est destiné à l'utilisateur : les routes le lui renvoient tel quel.
    """


MESSAGE_PAS_DE_VIDEO = ("Cette publication TikTok est un carrousel photo : il n'y a pas "
                        "de vidéo à analyser. Colle le lien d'une vidéo.")


def est_une_video(url: str) -> Optional[bool]:
    """La publication TikTok a-t-elle une vraie vidéo ? Sans rien télécharger.

    True = vidéo, False = publication photo (seule la bande son est proposée),
    None = impossible à savoir (TikTok injoignable…) — l'appelant décide.

    Pourquoi : le fournisseur du Feed Radar ne signale pas toujours les
    publications photo (`image_post_info` absent). Les 3 exemples de l'accueil
    en étaient le 27/10 : chaque visiteur qui cliquait recevait « carrousel
    photo ». yt-dlp, lui, liste ce que TikTok sert réellement.
    """
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "noplaylist": True,
                               "extractor_args": YDL_TIKTOK_EXTRACTOR_ARGS}) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception:
        return None
    formats = (info or {}).get("formats") or []
    if not formats:
        return None
    images = [f for f in formats if (f.get("vcodec") or "none") != "none"]
    if not images:
        return False          # bande son seule : publication photo
    # Le format « download » (filigrané, sans résolution) ne prouve rien : seule
    # une vraie piste avec hauteur connue tranche (cf. YDL_FORMAT_VIDEO).
    if any((f.get("height") or 0) > 0 for f in images):
        return True
    return None

_EXT_AUDIO = {".mp3", ".m4a", ".aac", ".wav", ".ogg", ".opus", ".flac"}


def _ffmpeg() -> str:
    # Use system ffmpeg (installed via apt on Render)
    return "ffmpeg"


def _probe(video_path: str) -> dict:
    """Caractéristiques de la vidéo, via ffprobe. Dict vide si indisponible.

    Coût : ~0,1 s (lecture d'en-têtes, aucun décodage). À comparer aux dizaines
    de secondes d'un ré-encodage — d'où l'intérêt de demander avant de faire.
    """
    # Sortie JSON, un objet par flux. L'ancienne lecture ligne à ligne supposait
    # que `codec_type` précède `codec_name` ; ffprobe écrit l'inverse. Le codec
    # vidéo n'était donc jamais reconnu : toute vidéo passait pour « non
    # conforme » et était ré-encodée (~30 s mesurées en production le 26/10).
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "stream=codec_name,codec_type,height", "-of", "json", video_path],
            capture_output=True, timeout=15, text=True,
        )
        if out.returncode != 0:
            return {}
        import json
        infos: dict = {"height": 0, "vcodec": "", "acodec": ""}
        for flux in json.loads(out.stdout or "{}").get("streams", []):
            nom = flux.get("codec_name") or ""
            if flux.get("codec_type") == "video":
                # Une pochette d'album (mjpeg/png dans un mp3) n'est pas une vidéo.
                if nom in ("mjpeg", "png", "bmp", "gif") and os.path.splitext(video_path)[1].lower() in _EXT_AUDIO:
                    continue
                infos["vcodec"] = infos["vcodec"] or nom
                infos["height"] = max(infos["height"], int(flux.get("height") or 0))
            elif flux.get("codec_type") == "audio":
                infos["acodec"] = infos["acodec"] or nom
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

    # ⚠️ Ce ré-encodage était INCONDITIONNEL, et il coûtait 26 s mesurées sur une
    # vidéo de 5 Mo — pour économiser une seconde ou deux d'envoi vers Google.
    # Le calcul est perdant d'un ordre de grandeur.
    #
    # Le critère de décision n'est donc PAS la résolution mais le POIDS, car
    # c'est le seul coût réel qu'un ré-encodage supprime : le temps de transfert.
    # Une première version filtrait sur `height <= 720` ; elle ne servait à rien
    # ici, parce qu'une vidéo TikTok est verticale — 1080×1920 — et que sa
    # « hauteur » vaut donc 1920. Le filtre ne se déclenchait jamais. (Même
    # raison pour laquelle le `best[height<=720]` de yt-dlp ne matche jamais et
    # retombe sur la meilleure qualité disponible.)
    #
    # La résolution, elle, ne coûte quasiment rien : le modèle échantillonne la
    # vidéo à sa propre résolution interne. Lui envoyer du 1080p vertical plutôt
    # que du 405×720 ne change ni son temps d'analyse ni sa précision.
    seuil_mo = float(os.getenv("VIDEO_REENCODE_MIN_MB", "25"))
    try:
        taille_mo = os.path.getsize(video_path) / (1024 * 1024)
    except Exception:
        taille_mo = float("inf")   # taille illisible → on ré-encode, comme avant

    # Le poids décide du GAIN d'un ré-encodage, jamais de sa NÉCESSITÉ.
    #
    # L'upload vers Gemini annonce « video/mp4 » en dur (ai_providers._gemini_video).
    # Livrer un webm/VP9 sous cette étiquette — ce que yt-dlp rapporte dès que
    # TikTok ne sert pas de mp4 — fait échouer le transcodage côté Google, qui
    # marque le fichier FAILED. Tant que le ré-encodage était inconditionnel, il
    # normalisait le conteneur au passage et masquait le problème ; l'avoir rendu
    # conditionnel au poids a retiré ce filet pour toutes les vidéos légères,
    # c'est-à-dire pour la quasi-totalité d'entre elles.
    #
    # _probe coûte ~0,1 s : on peut se permettre de demander avant de décider.
    infos = _probe(video_path)
    ext = os.path.splitext(video_path)[1].lower()
    # Aucune image : rien à ré-encoder ni à envoyer (publication en mode photo).
    # Un _probe vide (ffprobe absent) ne prouve rien : seul le conteneur audio,
    # ou une lecture réussie sans flux vidéo, tranche.
    if ext in _EXT_AUDIO or (infos and not infos.get("vcodec") and not infos.get("height")):
        raise PasDeVideo(MESSAGE_PAS_DE_VIDEO)
    conforme = ext == ".mp4" and infos.get("vcodec") == "h264"

    if conforme and taille_mo <= seuil_mo:
        print(f"[video] ⏱ préparation : {_t.monotonic() - _t0:.1f}s — "
              f"{taille_mo:.1f} Mo, sous le seuil de {seuil_mo:.0f} Mo : "
              f"ré-encodage évité", flush=True)
        return video_path

    if not conforme:
        # _probe vide (ffprobe absent ou fichier illisible) tombe ici aussi :
        # on ré-encode, seul choix sûr quand on ne sait pas ce qu'on tient.
        print(f"[video] format non conforme (ext={ext or '?'}, "
              f"vcodec={infos.get('vcodec') or '?'}) : ré-encodage imposé", flush=True)

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
            sortie = _probe(out_path)
            print(f"[video] ⏱ préparation : {_t.monotonic() - _t0:.1f}s — ré-encodage "
                  f"(source {infos.get('height') or '?'}p {infos.get('vcodec') or '?'} → "
                  f"{sortie.get('height') or '?'}p {sortie.get('vcodec') or '?'})", flush=True)
            if sortie and not sortie.get("vcodec"):
                # Ré-encodage « réussi » mais sans image : même cas qu'un mp3.
                os.unlink(out_path)
                raise PasDeVideo(MESSAGE_PAS_DE_VIDEO)
            return out_path
    except PasDeVideo:
        raise
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
