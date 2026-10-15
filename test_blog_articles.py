"""Tests des GUIDES du blog (blog_articles.py, contenu dans content/blog/).

Ce que ces tests protègent, et pourquoi c'est silencieux sans eux :

  • la checklist SEO/GEO (title ≤ 60, description ≤ 155, un seul <h1>, deux
    liens internes, sources citées…) : un article qui la viole est quand même
    servi — main.py se contente de l'écrire dans les logs au démarrage ;
  • les huit langues : un fichier de langue oublié retire l'article de cette
    langue sans erreur, et les hreflang des sept autres annoncent un 404 ;
  • les liens : « guide:<id> » non résolu, ou « /pricing » resté français
    dans un guide allemand, ne casse rien de visible.

Lancement :
    venv/bin/python test_blog_articles.py
    (ou python -m pytest test_blog_articles.py)
"""
from __future__ import annotations

import json
import os
import re

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

from fastapi.testclient import TestClient

import blog_articles
import homepage_i18n
import main

client = TestClient(main.app)
GUIDES = main._GUIDES
BASE = main._seo_base_url()


def _page(chemin: str) -> str:
    r = client.get(chemin)
    assert r.status_code == 200, f"{chemin} → {r.status_code}"
    return r.text


def _toutes_les_pages():
    for a in GUIDES:
        for lang in homepage_i18n.LANGS:
            yield a, lang, a.chemin(lang)


# ── Contenu ──────────────────────────────────────────────────────────────────
def test_il_y_a_des_guides():
    assert GUIDES, "aucun guide chargé depuis content/blog/"


def test_la_checklist_seo_est_respectee():
    problemes = blog_articles.controler(GUIDES)
    assert not problemes, "\n".join(problemes)


def test_chaque_guide_existe_dans_chaque_langue():
    for a in GUIDES:
        manquantes = [l for l in blog_articles.LANGUES_REDIGEES if l not in a.corps]
        assert not manquantes, f"{a.id} : langues absentes {manquantes}"


def test_chaque_langue_est_vraiment_traduite():
    """Un fichier copié-collé depuis le français passerait tous les contrôles
    de structure. Le chapô et le corps doivent différer du français."""
    for a in GUIDES:
        fr = a.corps["fr"]
        for lang in blog_articles.LANGUES_REDIGEES:
            if lang == "fr":
                continue
            assert a.corps[lang] != fr, f"{a.id}/{lang} : corps identique au français"
            assert a.langues[lang]["chapo"] != a.langues["fr"]["chapo"], \
                f"{a.id}/{lang} : chapô identique au français"


# ── Ce que lit Google ────────────────────────────────────────────────────────
def test_chaque_page_repond():
    for _a, _lang, chemin in _toutes_les_pages():
        _page(chemin)


def test_un_seul_h1_et_un_title_court():
    for a, lang, chemin in _toutes_les_pages():
        html = _page(chemin)
        assert len(re.findall(r"<h1\b", html)) == 1, f"{chemin} : nombre de <h1> ≠ 1"
        titre = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
        assert len(titre) <= blog_articles.TITRE_MAX, f"{chemin} : title trop long ({len(titre)})"


def test_html_lang_et_canonique():
    for a, lang, chemin in _toutes_les_pages():
        html = _page(chemin)
        assert f'<html lang="{homepage_i18n.HTML_LANG[lang]}"' in html, f"{chemin} : <html lang>"
        assert f'<link rel="canonical" href="{BASE}{chemin}">' in html, f"{chemin} : canonique"
        assert f'content="{homepage_i18n.OG_LOCALE[lang]}"' in html, f"{chemin} : og:locale"


def test_hreflang_complets_et_reciproques():
    """Google ignore une paire hreflang non réciproque : chaque version doit
    déclarer les huit autres, et la même x-default."""
    for a in GUIDES:
        attendu = {(homepage_i18n.HTML_LANG[l], BASE + a.chemin(l)) for l in homepage_i18n.LANGS}
        attendu.add(("x-default", BASE + a.chemin("fr")))
        for lang in homepage_i18n.LANGS:
            html = _page(a.chemin(lang))
            trouves = set(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', html))
            assert trouves == attendu, f"{a.chemin(lang)} : hreflang incohérents"


def test_json_ld_valide():
    for a, lang, chemin in _toutes_les_pages():
        html = _page(chemin)
        blocs = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        assert blocs, f"{chemin} : pas de JSON-LD"
        graphe = json.loads(blocs[0])["@graph"]
        types = {n["@type"] for n in graphe}
        assert {"Article", "BreadcrumbList", "FAQPage"} <= types, f"{chemin} : {types}"
        article = next(n for n in graphe if n["@type"] == "Article")
        assert article["inLanguage"] == homepage_i18n.HTML_LANG[lang]
        assert article["publisher"]["@id"] == f"{BASE}/#organization", \
            "l'éditeur doit être la même entité que l'Organization de l'accueil"


# ── Images ───────────────────────────────────────────────────────────────────
def test_chaque_guide_a_son_image_de_partage():
    """Sinon le guide se partage avec le logo. Relancer generate_og_images.py."""
    for a in GUIDES:
        for lang in blog_articles.LANGUES_REDIGEES:
            f = blog_articles.OG_DOSSIER / blog_articles.nom_image_og(a.id, lang)
            assert f.exists(), f"{f} absente — lancer generate_og_images.py"


def test_l_image_de_partage_est_dans_la_langue_de_la_page():
    for a, lang, chemin in _toutes_les_pages():
        html = _page(chemin)
        attendu = f"/static/og/{blog_articles.nom_image_og(a.id, lang)}"
        assert f'<meta property="og:image" content="{BASE}{attendu}">' in html, f"{chemin} : og:image"
        assert client.get(attendu).status_code == 200, f"{attendu} non servie"


def test_les_schemas_sont_dessines():
    for a, lang, chemin in _toutes_les_pages():
        html = _page(chemin)
        assert "<!--SCHEMA-->" not in html, f"{chemin} : marqueur de schéma non remplacé"
        if a.schema:
            assert '<figure class="schema"><svg' in html, f"{chemin} : schéma absent"


# ── Liens ────────────────────────────────────────────────────────────────────
def test_aucun_lien_guide_non_resolu():
    for _a, _lang, chemin in _toutes_les_pages():
        assert 'href="guide:' not in _page(chemin), f"{chemin} : lien guide: non résolu"


def test_les_liens_internes_restent_dans_la_langue():
    """Dans un guide allemand, « Zurück zum Blog » mène à /de/blog, et le lien
    vers la page d'atterrissage à sa version allemande."""
    for a in GUIDES:
        html = _page(a.chemin("de"))
        assert 'href="/de/blog"' in html, f"{a.id} : retour au blog non localisé"
        assert 'href="/blog"' not in html, f"{a.id} : lien /blog resté français"
        assert 'href="/#tool"' not in html, f"{a.id} : appel à l'action resté français"


def test_les_articles_lies_sont_dans_la_meme_langue():
    for a in GUIDES:
        for lang in homepage_i18n.LANGS:
            html = _page(a.chemin(lang))
            for i in a.lies:
                cible = next(x for x in GUIDES if x.id == i)
                assert f'href="{cible.chemin(lang)}"' in html, \
                    f"{a.chemin(lang)} : lien vers {i} absent ou dans une autre langue"


# ── Intégration au reste du site ─────────────────────────────────────────────
def test_les_guides_sont_au_sitemap():
    xml = _page("/sitemap.xml")
    for _a, _lang, chemin in _toutes_les_pages():
        assert f"<loc>{BASE}{chemin}</loc>" in xml, f"{chemin} absent du sitemap"


def test_les_guides_sont_dans_llms_txt():
    txt = _page("/llms.txt")
    for a in GUIDES:
        assert f"{BASE}{a.chemin('fr')}" in txt, f"{a.id} absent de llms.txt"


def test_le_blog_liste_les_guides_dans_chaque_langue():
    for lang in homepage_i18n.LANGS:
        html = _page(homepage_i18n.chemin_langue(lang, "/blog"))
        assert "GUIDES_" not in html, f"/blog [{lang}] : marqueur non remplacé"
        for a in GUIDES:
            assert f'href="{a.chemin(lang)}"' in html, f"/blog [{lang}] : carte {a.id} absente"


if __name__ == "__main__":
    tests = [(n, o) for n, o in sorted(globals().items())
             if n.startswith("test_") and callable(o)]
    reussis, echoues = 0, []
    for nom, fn in tests:
        try:
            fn()
            print(f"  ok    {nom}")
            reussis += 1
        except Exception as e:
            print(f"  ÉCHEC {nom}\n        {e}")
            echoues.append(nom)

    print(f"\n{reussis}/{len(tests)} tests passent.")
    if echoues:
        print("Échecs : " + ", ".join(echoues))
    raise SystemExit(1 if echoues else 0)
