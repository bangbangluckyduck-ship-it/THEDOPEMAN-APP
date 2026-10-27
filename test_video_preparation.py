"""Tests de la préparation vidéo et de l'appel Gemini (incident du 26/10/2026).

Ce qui doit rester vrai :
  • ffprobe est lu correctement : une vidéo h264 est reconnue comme telle (la
    lecture ligne à ligne ne voyait jamais le codec → ré-encodage systématique) ;
  • une publication en mode photo (mp3, aucune image) est refusée avec un
    message clair au lieu de partir chez Gemini ;
  • une réponse VIDE de Gemini fait passer au modèle de secours, avec la raison.

Lancement :  venv/bin/python -m pytest test_video_preparation.py -v
"""
from __future__ import annotations

import json
import os
import types

import pytest

import ai_providers
import video_processor


def _ffprobe(streams):
    def faux_run(cmd, **_k):
        return types.SimpleNamespace(returncode=0, stdout=json.dumps({"streams": streams}))
    return faux_run


def test_probe_reconnait_le_codec_video(monkeypatch):
    # Ordre réel de ffprobe : codec_name AVANT codec_type.
    monkeypatch.setattr(video_processor.subprocess, "run", _ffprobe([
        {"codec_name": "h264", "codec_type": "video", "height": 1024},
        {"codec_name": "aac", "codec_type": "audio"}]))
    assert video_processor._probe("x.mp4") == {"height": 1024, "vcodec": "h264", "acodec": "aac"}


def test_video_h264_legere_n_est_plus_reencodee(monkeypatch, tmp_path):
    f = tmp_path / "v.mp4"
    f.write_bytes(b"0" * 2048)
    monkeypatch.setattr(video_processor.subprocess, "run", _ffprobe([
        {"codec_name": "h264", "codec_type": "video", "height": 1920}]))
    assert video_processor.downscale_720p(str(f)) == str(f)


def test_publication_photo_refusee_clairement(tmp_path, monkeypatch):
    f = tmp_path / "v.mp3"
    f.write_bytes(b"0" * 2048)
    monkeypatch.setattr(video_processor.subprocess, "run", _ffprobe([
        {"codec_name": "mp3", "codec_type": "audio"},
        {"codec_name": "mjpeg", "codec_type": "video", "height": 600}]))   # pochette
    with pytest.raises(video_processor.PasDeVideo, match="carrousel photo"):
        video_processor.downscale_720p(str(f))


def test_mp4_sans_flux_video_refuse(tmp_path, monkeypatch):
    f = tmp_path / "v.mp4"
    f.write_bytes(b"0" * 2048)
    monkeypatch.setattr(video_processor.subprocess, "run", _ffprobe([
        {"codec_name": "aac", "codec_type": "audio"}]))
    with pytest.raises(video_processor.PasDeVideo):
        video_processor.downscale_720p(str(f))


def test_raison_reponse_vide():
    resp = types.SimpleNamespace(prompt_feedback=None, text="",
                                 candidates=[types.SimpleNamespace(finish_reason="SAFETY")])
    assert ai_providers._raison_reponse_vide(resp) == "fin : SAFETY"
    assert "aucun candidat" in ai_providers._raison_reponse_vide(types.SimpleNamespace(candidates=[]))


def test_reponse_vide_passe_au_modele_de_secours(monkeypatch, tmp_path):
    """Avec un faux client Gemini : le 1er modèle rend du vide, le 2e répond."""
    f = tmp_path / "v.mp4"
    f.write_bytes(b"0" * 2048)
    appels = []

    class Modeles:
        def generate_content(self, model, contents, config=None):
            appels.append(model)
            if len(appels) == 1:
                return types.SimpleNamespace(text="", prompt_feedback=None,
                                             candidates=[types.SimpleNamespace(finish_reason="OTHER")])
            return types.SimpleNamespace(text='{"ok": true}')

    class Fichiers:
        def upload(self, file, config=None):
            return types.SimpleNamespace(state=types.SimpleNamespace(name="ACTIVE"), uri="u", name="n")

        def get(self, name):
            return self.upload(None)

        def delete(self, name):
            return None

    client = types.SimpleNamespace(models=Modeles(), files=Fichiers())
    monkeypatch.setenv("GEMINI_API_KEY", "x")
    monkeypatch.setenv("GEMINI_VIDEO_FALLBACK_MODEL", "modele-de-secours")
    from google import genai
    monkeypatch.setattr(genai, "Client", lambda **_k: client)   # aucun appel réseau
    out = ai_providers.video_complete(str(f), "prompt")
    assert out == '{"ok": true}'
    assert appels[-1] == "modele-de-secours" and len(appels) == 2


def test_video_bloquee_par_google_message_clair(monkeypatch, tmp_path):
    """Les deux modèles refusent la vidéo (« prompt bloqué ») : relancer ne sert à
    rien, l'utilisateur doit l'apprendre et choisir une autre vidéo."""
    f = tmp_path / "v.mp4"
    f.write_bytes(b"0" * 2048)
    bloque = types.SimpleNamespace(text="", candidates=[],
                                   prompt_feedback=types.SimpleNamespace(block_reason="OTHER"))

    class Modeles:
        def generate_content(self, model, contents, config=None):
            return bloque

    class Fichiers:
        def upload(self, file, config=None):
            return types.SimpleNamespace(state=types.SimpleNamespace(name="ACTIVE"), uri="u", name="n")

        def get(self, name):
            return self.upload(None)

        def delete(self, name):
            return None

    from google import genai
    monkeypatch.setenv("GEMINI_API_KEY", "x")
    monkeypatch.setattr(genai, "Client", lambda **_k: types.SimpleNamespace(models=Modeles(), files=Fichiers()))
    with pytest.raises(ai_providers.VideoRefusee, match="Essaie avec une autre vidéo"):
        ai_providers.video_complete(str(f), "prompt")


def _choix_format(formats):
    """Format que yt-dlp retiendrait, sans réseau (sélecteur appliqué à une liste)."""
    import yt_dlp
    ydl = yt_dlp.YoutubeDL({"quiet": True})
    info = {"id": "x", "extractor": "TikTok", "formats": formats}
    ydl.sort_formats(info)
    choix = list(ydl.build_format_selector(video_processor.YDL_FORMAT_VIDEO)(
        {"formats": info["formats"], "has_merged_format": True, "incomplete_formats": False}))
    return choix[0]["format_id"]


def _fmt(fid, vcodec, w, h, tbr, pref=None):
    return {"format_id": fid, "ext": "mp4", "vcodec": vcodec, "acodec": "aac", "width": w,
            "height": h, "tbr": tbr, "url": f"https://x/{fid}", "protocol": "https",
            **({"preference": pref} if pref is not None else {})}


def test_telechargement_prefere_le_h264():
    """Liste réelle relevée le 27/10 : `best` prenait la 1080p H.265, ré-encodée
    ensuite pendant 60 s. Le H.264 natif doit gagner."""
    formats = [
        _fmt("download", "h264", None, None, None, pref=-2),   # filigrane
        _fmt("h264_540p_968752-0", "h264", 576, 1024, 968),
        _fmt("h264_540p_1754343-0", "h264", 576, 1024, 1754),
        _fmt("bytevc1_720p_785474-0", "h265", 720, 1280, 785),
        _fmt("bytevc1_1080p_1261782-0", "h265", 1080, 1920, 1261),
    ]
    assert _choix_format(formats) == "h264_540p_1754343-0"


def test_sans_h264_on_garde_le_meilleur_mp4():
    formats = [_fmt("bytevc1_720p", "h265", 720, 1280, 785),
               _fmt("bytevc1_1080p", "h265", 1080, 1920, 1261)]
    assert _choix_format(formats) == "bytevc1_1080p"
