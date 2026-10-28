"""Feed Radar : collecte par le classement des ventes KeyAPI.

Testé en direct le 28/10/2026 : /video/ranking/analytics renvoie, par région, les
vidéos qui ont le plus vendu sur une journée (publiée avec ~2 jours de retard),
avec ventes, produits et stats — là où l'ancienne découverte par créateurs
coûtait ~13 700 appels par run pour une seule région.

Ce qui doit rester vrai :
  • on lit la journée publiée la plus récente, sans dépasser le budget de pages ;
  • les publications photo et les vidéos sans produit ne rentrent jamais ;
  • le GMV stocké est le cumul réel depuis la publication, pas celui de la journée ;
  • une vidéo déjà connue est mise à jour sans perdre ce qui n'est pas dans le classement ;
  • le mode essai n'écrit rien ;
  • France et Brésil sont collectés par défaut.

Lancement :  venv/bin/python -m pytest test_feed_radar_classement.py -v
"""
from __future__ import annotations

import asyncio
import importlib
import types
from datetime import date

import pytest

import feed_radar
import market_creators as mc

# Entrée réelle du classement FR du 26/10/2026 (raccourcie)
LIGNE = {
    "video_id": "7698412688417836320", "unique_id": "fadoua_kimo", "user_id": "7227852904010695706",
    "nick_name": "Fadoua beauty", "region": "FR", "aweme_type": 0, "duration": 30,
    "reflow_cover": "https://exemple.test/cover.jpeg",
    "total_video_sale_cnt": 557, "total_video_sale_gmv_amt": 9843,
    "total_video_sale_history_cnt": 1510, "total_video_sale_gmv_history_amt": 35252,
    "total_views_cnt": 0, "total_views_history_cnt": 499451,
    "total_digg_history_cnt": 2346, "total_comments_history_cnt": 109, "total_shares_history_cnt": 756,
    "video_products": "[1729622472230213698]",
}


def _ligne(vid, **k):
    return {**LIGNE, "video_id": vid, **k}


def test_nettoyage_garde_le_cumul_reel():
    v = mc._clean_ranked_video(LIGNE)
    assert v["id"] == "7698412688417836320"
    assert v["url"] == "https://www.tiktok.com/@fadoua_kimo/video/7698412688417836320"
    assert (v["sales_real"], v["gmv_real"], v["sales_day"]) == (1510, 35252, 557)
    assert v["views"] == 499451
    assert v["video_products"] == ["1729622472230213698"]     # str : ID trop long pour JS
    assert v["is_photo"] is False
    assert mc._clean_ranked_video({**LIGNE, "aweme_type": 150})["is_photo"] is True


def _classement(pages_par_jour):
    """Faux get_video_ranking : {jour: [page1, page2, …]} ; trace les appels."""
    appels = []

    async def faux(region, jour, page_num=1, page_size=10):
        appels.append((region, jour, page_num))
        pages = pages_par_jour.get(jour, [])
        return pages[page_num - 1] if page_num <= len(pages) else []
    return faux, appels


def test_decouverte_prend_la_journee_publiee_la_plus_recente(monkeypatch):
    faux, appels = _classement({
        "2026-10-26": [[_ligne("1"), _ligne("2")], [_ligne("2"), _ligne("3")]],   # « 2 » en double
    })
    monkeypatch.setattr(mc, "get_video_ranking", faux)
    monkeypatch.setattr(feed_radar, "FEED_RADAR_RANKING_PAGES", 5)
    monkeypatch.setattr(feed_radar, "FEED_RADAR_RANKING_DAYS", 1)
    videos, stats = asyncio.run(feed_radar.discover_ranked_videos("FR", today=date(2026, 10, 28)))
    assert [v["id"] for v in videos] == ["1", "2", "3"]
    assert stats["jours"] == ["2026-10-26"]
    # hier vide → avant-hier : page 1, page 2, page 3 vide → arrêt
    assert appels == [("FR", "2026-10-27", 1), ("FR", "2026-10-26", 1),
                      ("FR", "2026-10-26", 2), ("FR", "2026-10-26", 3)]
    assert stats["appels"] == 4


def test_decouverte_respecte_le_budget_de_pages_et_de_jours(monkeypatch):
    plein = [[_ligne(f"{p}-{i}") for i in range(10)] for p in range(9)]
    faux, appels = _classement({"2026-10-27": plein, "2026-10-26": plein})
    monkeypatch.setattr(mc, "get_video_ranking", faux)
    monkeypatch.setattr(feed_radar, "FEED_RADAR_RANKING_PAGES", 2)
    monkeypatch.setattr(feed_radar, "FEED_RADAR_RANKING_DAYS", 2)
    _, stats = asyncio.run(feed_radar.discover_ranked_videos("BR", today=date(2026, 10, 28)))
    assert stats["jours"] == ["2026-10-27", "2026-10-26"]
    assert len(appels) == 4 and stats["appels"] == 4


def test_aucun_classement_publie(monkeypatch):
    faux, appels = _classement({})
    monkeypatch.setattr(mc, "get_video_ranking", faux)
    videos, stats = asyncio.run(feed_radar.discover_ranked_videos("FR", today=date(2026, 10, 28)))
    assert videos == [] and len(appels) == feed_radar._RANKING_MAX_RECUL


class _Base:
    def __init__(self, connues=()):
        self.connues = set(connues)
        self.upserts = []

    def table(self, nom):
        base = self

        class Q:
            def select(self, *_a):
                return self

            def in_(self, _c, ids):
                self._ids = ids
                return self

            def upsert(self, row, **_k):
                base.upserts.append(row)
                return self

            def execute(self):
                ids = getattr(self, "_ids", [])
                return types.SimpleNamespace(data=[{"video_id": i} for i in ids if i in base.connues])
        return Q()


def _decouverte(monkeypatch, lignes):
    async def faux(region, today=None):
        return [{**mc._clean_ranked_video(r), "region": region} for r in lignes], \
            {"appels": 2, "jours": ["2026-10-26"]}
    monkeypatch.setattr(feed_radar, "discover_ranked_videos", faux)

    async def oembed(url):
        return {"thumbnail_url": "https://exemple.test/t.jpg", "html": "<blockquote/>", "author_name": "x"}
    monkeypatch.setattr(feed_radar, "fetch_oembed", oembed)


def test_collecte_ecarte_photos_et_videos_sans_produit(monkeypatch):
    _decouverte(monkeypatch, [
        _ligne("video"),
        _ligne("photo", aweme_type=150, duration=0),
        _ligne("sans-produit", video_products="[]"),
        _ligne("connue"),
    ])
    base = _Base(connues={"connue"})
    res = asyncio.run(feed_radar._collect_region_classement("FR", base))
    assert (res["found"], res["kept"], res["skipped_photo"], res["skipped_non_shop"]) == (4, 2, 1, 1)
    assert (res["new"], res["updated"]) == (1, 1)
    par_id = {r["video_id"]: r for r in base.upserts}
    assert set(par_id) == {"video", "connue"}
    nouvelle, connue = par_id["video"], par_id["connue"]
    assert nouvelle["gmv_source"] == "real_attribution" and nouvelle["gmv_real"] == 35252
    assert nouvelle["sales_real"] == 1510 and nouvelle["view_threshold_used"] == 0
    assert nouvelle["oembed_html"] == "<blockquote/>" and nouvelle["trend_snapshot"] == []
    # une vidéo connue garde sa vignette et ses anciennes données hors classement
    assert "oembed_html" not in connue and "trend_snapshot" not in connue
    assert "gmv_estimated" not in connue


def test_mode_essai_n_ecrit_rien(monkeypatch):
    _decouverte(monkeypatch, [_ligne("video"), _ligne("photo", aweme_type=150)])
    base = _Base()
    res = asyncio.run(feed_radar._collect_region_classement("BR", base, dry_run=True))
    assert base.upserts == []
    assert [a["video_id"] for a in res["apercu"]] == ["video"]
    assert res["apercu"][0]["ventes_jour"] == 557 and res["apercu"][0]["nouvelle"] is True


def test_essai_complet_ne_purge_rien(monkeypatch):
    _decouverte(monkeypatch, [_ligne("video")])
    monkeypatch.setattr(feed_radar, "FEED_RADAR_SOURCE", "classement")
    monkeypatch.setattr(feed_radar, "cleanup_non_shop_rows",
                        lambda *_a, **_k: pytest.fail("purge lancée en mode essai"))
    res = asyncio.run(feed_radar._run_collection(None, _Base(), dry_run=True))
    assert res["dry_run"] and res["new"] == len(feed_radar.FEED_RADAR_REGIONS)


def test_ancienne_collecte_reste_disponible(monkeypatch):
    vus = []

    async def ancienne(region, supabase):
        vus.append(region)
        return {"found": 0, "new": 0, "updated": 0}
    monkeypatch.setattr(feed_radar, "_collect_region", ancienne)
    monkeypatch.setattr(feed_radar, "FEED_RADAR_SOURCE", "createurs")
    monkeypatch.setattr(feed_radar, "cleanup_non_shop_rows", lambda *_a, **_k: 0)
    asyncio.run(feed_radar._run_collection("fr", _Base()))
    assert vus == ["FR"]


def test_france_et_bresil_par_defaut(monkeypatch):
    monkeypatch.delenv("FEED_RADAR_REGIONS", raising=False)
    monkeypatch.delenv("FEED_RADAR_SOURCE", raising=False)
    try:
        m = importlib.reload(feed_radar)
        assert m.FEED_RADAR_REGIONS == ["FR", "BR"] and m.FEED_RADAR_SOURCE == "classement"
    finally:
        importlib.reload(feed_radar)
