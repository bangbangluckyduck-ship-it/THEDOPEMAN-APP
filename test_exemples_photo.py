"""Publications photo : hors des exemples de l'accueil, et sans coûter l'essai.

Incident du 27/10/2026 : les 3 exemples du Feed Radar sur l'accueil étaient des
publications photo (le fournisseur ne les signalait pas). Chaque visiteur qui
cliquait « Décrypter » recevait « carrousel photo » — et perdait l'un de ses
deux essais sans compte.

Ce qui doit rester vrai :
  • une publication sans piste vidéo est reconnue comme photo, sans téléchargement ;
  • les exemples ne gardent que des vidéos (un verdict inconnu ne retire rien) ;
  • une analyse qui tombe sur une photo la retire des exemples ;
  • un lien refusé rend l'essai sans compte du visiteur.

Lancement :  venv/bin/python -m pytest test_exemples_photo.py -v
"""
from __future__ import annotations

import asyncio
import os
import types

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

import pytest

import main
import video_processor


def _yt_dlp(formats=None, erreur=False):
    class Faux:
        def __init__(self, *_a, **_k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_a):
            return False

        def extract_info(self, url, download=True):
            assert download is False      # jamais de téléchargement pour vérifier
            if erreur:
                raise RuntimeError("TikTok injoignable")
            return {"formats": formats}
    return types.SimpleNamespace(YoutubeDL=Faux)


AUDIO = {"format_id": "audio", "vcodec": "none", "acodec": "mp3"}
VIDEO = {"format_id": "h264_540p", "vcodec": "h264", "height": 1024}
FILIGRANE = {"format_id": "download", "vcodec": "h264", "height": None}


@pytest.mark.parametrize("formats,attendu", [
    ([AUDIO], False),                     # publication photo : bande son seule
    ([AUDIO, FILIGRANE, VIDEO], True),
    ([AUDIO, FILIGRANE], None),           # le filigrané seul ne prouve rien
    ([], None),
])
def test_est_une_video(monkeypatch, formats, attendu):
    import sys
    monkeypatch.setitem(sys.modules, "yt_dlp", _yt_dlp(formats))
    assert video_processor.est_une_video("https://www.tiktok.com/@a/video/1") is attendu


def test_tiktok_injoignable_verdict_inconnu(monkeypatch):
    import sys
    monkeypatch.setitem(sys.modules, "yt_dlp", _yt_dlp(erreur=True))
    assert video_processor.est_une_video("https://www.tiktok.com/@a/video/1") is None


# ── Exemples de l'accueil ──────────────────────────────────────────────────
def test_les_exemples_ne_gardent_que_des_videos(monkeypatch):
    verdicts = {"1": False, "2": True, "3": None, "4": True, "5": True, "6": True}
    vus = []
    monkeypatch.setattr(main, "_nature_publication", lambda r: vus.append(r["video_id"]) or verdicts[r["video_id"]])
    rows = [{"video_id": k} for k in verdicts]
    gardes, tout_verifie = asyncio.run(main._exemples_video(rows))
    # vidéos confirmées d'abord ; l'incertaine ne sert qu'à compléter
    assert [r["video_id"] for r in gardes] == ["2", "4", "5"] and tout_verifie
    assert vus == ["1", "2", "3", "4", "5"]      # un par un, arrêt à 3 confirmées


def test_incertain_complete_mais_cache_court(monkeypatch):
    verdicts = {"1": None, "2": True, "3": False}
    monkeypatch.setattr(main, "_nature_publication", lambda r: verdicts[r["video_id"]])
    gardes, tout_verifie = asyncio.run(main._exemples_video([{"video_id": k} for k in verdicts]))
    assert [r["video_id"] for r in gardes] == ["2", "1"] and not tout_verifie


class _Base:
    def __init__(self):
        self.ops = []

    def table(self, nom):
        base = self

        class Q:
            def update(self, d):
                base.ops.append(("update", nom, d))
                return self

            def delete(self):
                base.ops.append(("delete", nom))
                return self

            def eq(self, c, v):
                base.ops.append(("eq", c, v))
                return self

            def like(self, c, v):
                base.ops.append(("like", c, v))
                return self

            def upsert(self, d, **_k):
                base.ops.append(("upsert", nom, d["cache_key"], d["payload"]))
                return self

            def execute(self):
                return types.SimpleNamespace(data=[])
        return Q()


def test_une_analyse_photo_retire_la_publication_des_exemples(monkeypatch):
    base = _Base()
    monkeypatch.setattr(main, "supabase_client", base)
    main._marquer_publication_photo("https://www.tiktok.com/@riccy_arsyah/video/7548578503013190918?lang=fr")
    assert ("update", "feed_radar_videos", {"is_carousel": True}) in base.ops
    assert ("eq", "video_id", "7548578503013190918") in base.ops
    assert any(o[0] == "upsert" and o[2].endswith("feedradar::nature::7548578503013190918")
               and o[3] == {"video": False} for o in base.ops)
    assert any(o[0] == "like" and "feedradar::teaser::v6::" in o[2] for o in base.ops)


# ── Essai sans compte ──────────────────────────────────────────────────────
def test_un_lien_refuse_rend_l_essai(monkeypatch):
    requete = types.SimpleNamespace(client=types.SimpleNamespace(host="203.0.113.7"))
    main._ANON_IP_USAGE.pop("203.0.113.7", None)
    main._consume_anon_quota(requete)
    main._consume_anon_quota(requete)
    assert len(main._ANON_IP_USAGE["203.0.113.7"]) == 2
    main._rendre_anon_quota(requete)
    assert len(main._ANON_IP_USAGE["203.0.113.7"]) == 1
    main._consume_anon_quota(requete)          # l'essai rendu est réutilisable
    with pytest.raises(main.HTTPException):
        main._consume_anon_quota(requete)
    main._ANON_IP_USAGE.pop("203.0.113.7", None)


def test_publication_photo_sur_analyze_url_rend_l_essai(monkeypatch, tmp_path):
    """Parcours réel de la route : téléchargement simulé d'un mp3 → 422, essai rendu."""
    from fastapi.testclient import TestClient
    import sys

    mp3 = tmp_path / "video.mp3"
    mp3.write_bytes(b"0" * 4096)

    class Ydl:
        def __init__(self, *_a, **_k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_a):
            return False

        def extract_info(self, url, download=True):
            return {}

        def prepare_filename(self, info):
            return str(mp3)

    monkeypatch.setitem(sys.modules, "yt_dlp", types.SimpleNamespace(YoutubeDL=Ydl))
    monkeypatch.setattr(main.ai_providers, "any_ai_key", lambda: True)
    monkeypatch.setattr(main, "supabase_client", _Base())
    import analysis_cache
    monkeypatch.setattr(analysis_cache, "get_cached", lambda *a, **k: None)
    client = TestClient(main.app)
    main._ANON_IP_USAGE.clear()
    r = client.post("/analyze-url", json={"url": "https://www.tiktok.com/@a/video/123"})
    assert r.status_code == 422 and "carrousel photo" in r.json()["detail"]
    assert not any(main._ANON_IP_USAGE.values())    # l'essai a été rendu
