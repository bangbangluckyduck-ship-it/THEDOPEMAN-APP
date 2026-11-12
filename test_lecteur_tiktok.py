"""Feed Radar : le lecteur officiel TikTok remplace les miniatures.

Depuis octobre 2026, l'oEmbed TikTok ne renvoie plus de thumbnail_url : toutes les
cartes du Feed Radar (app et exemples de l'accueil) affichaient l'image grise.
TikTok recommande son lecteur officiel, /player/v1/<id>. Testé dans Chrome le
28/10/2026 : il affiche la couverture, signale une vidéo invalide par
onPlayerError, et une vidéo qui démarre par onStateChange 1.

Ce qui doit rester vrai (pas de Node en CI : on vérifie les fichiers servis) :
  • les cartes de l'app et de l'accueil portent un lecteur à charger, avec repli ;
  • le script est servi et chargé avant le code qui l'utilise ;
  • il n'écoute que les messages venant de TikTok, remet le repli en cas
    d'erreur, et limite les chargements simultanés.

Lancement :  venv/bin/python -m pytest test_lecteur_tiktok.py -v
"""
from __future__ import annotations

import os
import re
from pathlib import Path

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

from fastapi.testclient import TestClient

import main

ICI = Path(__file__).parent
APP = (ICI / "static" / "app_v3.js").read_text(encoding="utf-8")
LECTEUR = (ICI / "static" / "tt_player.js").read_text(encoding="utf-8")
INDEX = (ICI / "templates" / "index.html").read_text(encoding="utf-8")
ACCUEIL = (ICI / "templates" / "homepage.html").read_text(encoding="utf-8")


def _fonction(src: str, nom: str) -> str:
    debut = src.index(f"function {nom}(")
    return src[debut:src.index("\n}\n", debut)]


def test_cartes_de_l_app_portent_le_lecteur():
    carte = _fonction(APP, "renderFeedRadarCard")
    assert 'class="tt-lecteur" data-tt-player="${escapeHtml(String(v.video_id))}"' in carte
    # Repli : couverture du lien de partage stocké, sinon image grise.
    assert ('class="tt-lecteur-repli" src="${escapeHtml(_ttCoverFromShareUrl(v.video_url) '
            "|| '/static/placeholder-thumb.svg')}\"") in carte
    assert "this.src='/static/placeholder-thumb.svg'" in carte   # couverture expirée → image grise
    assert "/thumb" not in carte          # la miniature oEmbed n'existe plus
    assert "window.ttLecteurs.observer(grid)" in _fonction(APP, "loadFeedRadarTab")


def test_couverture_du_lien_de_partage_passe_par_le_proxy():
    # Les liens TikTok Shop portent une couverture signée ~1 an
    # (ec_shared_reflux_dynamic_params.placeholder_origin_cover). Elle doit passer
    # par /api/img-proxy (hôtes CDN filtrés côté serveur), jamais en direct.
    aide = _fonction(APP, "_ttCoverFromShareUrl")
    assert "searchParams.get('ec_shared_reflux_dynamic_params')" in aide
    assert "placeholder_origin_cover" in aide
    assert "_imgProxy(cover)" in aide and "/^https:\\/\\//.test(cover)" in aide
    assert "catch (_) { return ''; }" in aide     # lien sans couverture ou mal formé → ''


def test_modale_et_autres_grilles_utilisent_le_lecteur_officiel():
    modale = _fonction(APP, "openTikTokPlayer")
    assert "https://www.tiktok.com/player/v1/" in modale
    assert "/embed/v2/" not in APP                 # ancien lecteur non documenté
    # Lecteur en échec dans la modale → lien vers TikTok au lieu de l'écran d'erreur.
    assert "d.type !== 'onPlayerError'" in APP and "Ouvrir sur TikTok" in APP
    # « Ses vidéos » d'un créateur et Favoris chargent le lecteur au défilement.
    assert APP.count("window.ttLecteurs.observer(box)") == 2
    assert "/api/tt-thumb?u=" not in _fonction(APP, "renderRechercheResult")


def test_fichier_de_verification_tiktok_servi():
    # Vérification « URL prefix » de l'app TikTok for Developers (Dope Ventures).
    client = TestClient(main.app)
    for jeton in ("ZJSSAnNEMjH61GgDbupDqJ1QKduFCd8l",    # https://www.qeerah.com/
                  "LSnmYARznglT2e364WVpo74L5CDHzHKt"):   # https://qeerah.com/
        r = client.get(f"/tiktok{jeton}.txt")
        assert r.status_code == 200
        assert r.text == f"tiktok-developers-site-verification={jeton}"
    assert client.get("/tiktokINCONNU.txt").status_code == 404   # aucun autre jeton servi


def test_exemples_de_l_accueil_portent_le_lecteur():
    assert "fr-thumb tt-lecteur" in ACCUEIL and "data-tt-player=" in ACCUEIL
    assert "window.ttLecteurs.observer(grille)" in ACCUEIL
    assert "/api/feed-radar/'+encodeURIComponent(v.video_id)+'/thumb" not in ACCUEIL


def test_script_charge_avant_son_usage():
    assert INDEX.index('src="/static/tt_player.js"') < INDEX.index('src="/static/app_v3.js"')
    assert '<script src="/static/tt_player.js" defer></script>' in ACCUEIL


def test_script_servi():
    r = TestClient(main.app).get("/static/tt_player.js")
    assert r.status_code == 200 and "ttLecteurs" in r.text


def test_lecteur_officiel_et_garde_fous():
    assert "ORIGINE + '/player/v1/'" in LECTEUR and "var ORIGINE = 'https://www.tiktok.com'" in LECTEUR
    assert "if (e.origin !== ORIGINE) return;" in LECTEUR        # messages d'autres sites ignorés
    assert "d.type === 'onPlayerError'" in LECTEUR                # erreur → repli
    assert "commande(autres[i], 'pause')" in LECTEUR              # une seule vidéo à la fois
    assert int(re.search(r"CHARGES_MAX = (\d+)", LECTEUR).group(1)) <= 3
    assert "autoplay=0" in LECTEUR                                # jamais de lecture sans geste


def test_les_politiques_de_securite_autorisent_le_lecteur():
    r = TestClient(main.app).get("/")
    csp = r.headers.get("content-security-policy", "")
    assert not csp or "frame-src 'self' https:" in csp


def test_mon_compte_tiktok_montre_chaque_permission_demandee():
    # Revue TikTok for Developers : la vidéo de démo doit montrer l'usage de chaque
    # scope (user.info.profile, user.info.stats, video.list) et l'analyse des vues.
    bloc = _fonction(APP, "loadTikTokData")
    assert "p.bio_description" in bloc and "p.profile_deep_link" in bloc      # user.info.profile
    assert "p.follower_count" in bloc and "p.likes_count" in bloc             # user.info.stats
    assert "data-tt-analyse" in bloc and "v.view_count" in bloc               # video.list → analyse
    assert "_imgProxy(v.cover_image_url)" in bloc                             # couverture via le proxy
    assert "/^https:\/\//.test(v.share_url" in bloc                         # lien vers la vidéo filtré
