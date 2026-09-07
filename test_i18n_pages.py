"""Tests des PAGES SECONDAIRES multilingues (tarifs, légal, blog, atterrissage).

⚠️ POURQUOI CE FICHIER EXISTE — la même raison que pour l'accueil, en pire.

Ici, la clef de traduction EST le texte français (cf. pages_i18n.py). Deux
silences en découlent, et aucun ne casse quoi que ce soit de visible :

  1. une phrase française reformulée sort du dictionnaire : la page repasse en
     français dans les sept autres langues, sans erreur ;
  2. une variante qui échoue à se construire retombe sur le français.

Les tests ci-dessous transforment ces deux silences en échecs bruyants :
chaque variante doit DIFFÉRER du français, et aucune entrée de dictionnaire ne
doit être orpheline (c'est-à-dire ne plus correspondre à aucun texte de la page).

Le reste couvre ce que Google exige et ce qu'un visiteur attend :
  • une route par langue et par page, sans 404 annoncé par les hreflang ;
  • <html lang>, canonique et hreflang complets sur chaque variante ;
  • toutes les URL traduites au sitemap ;
  • les liens internes qui restent dans la langue lue ;
  • le tableau de /pricing/compare, construit en JavaScript, qui doit rester du
    JavaScript valide une fois traduit (une apostrophe non échappée l'a déjà
    vidé en production — c'est la panne qui a motivé ce contrôle).

Lancement :
    venv/bin/python test_i18n_pages.py
"""
from __future__ import annotations

import os
import re

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

import homepage_i18n
import main
import pages_i18n

PAGES = main._PAGES_TRADUITES
BASE = main._seo_base_url()
AUTRES = [l for l in homepage_i18n.LANGS if l != "fr"]


# ── Construction ─────────────────────────────────────────────────────────────
def _sources() -> dict:
    """Page française source + son dictionnaire, pour chaque page traduite.

    Tenu à jour ici et nulle part ailleurs : une page ajoutée à main.py sans
    entrée ici échoue au test de couverture juste en dessous.
    """
    import pages_translations as T
    import pages_translations_confiance as C
    import pages_translations_legal as L

    return {
        "/pricing": (main._PRICING_HTML, T.T_PRICING),
        "/pricing/compare": (main._PRICING_COMPARE_HTML, T.T_COMPARE),
        "/credits": (main._CREDITS_HTML, T.T_CREDITS),
        "/about": (main._ABOUT_HTML, C.T_ABOUT),
        "/contact": (main._CONTACT_HTML, C.T_CONTACT),
        "/avis": (main._AVIS_HTML, C.T_AVIS),
        "/terms": (main._TERMS_HTML, L.T_TERMS),
        "/mentions-legales": (main._MENTIONS_HTML, L.T_MENTIONS),
        "/cgv": (main._CGV_HTML, L.T_CGV),
        "/privacy": (main._PRIVACY_HTML, L.T_PRIVACY),
    }


def test_chaque_page_traduite_est_couverte_par_les_tests():
    """Sans ça, une page ajoutée à main.py échapperait aux contrôles de
    dictionnaire — et pourrait partir en production à moitié traduite."""
    manquantes = sorted(set(PAGES) - set(_sources()))
    assert not manquantes, f"pages non couvertes par _sources() : {manquantes}"



def test_chaque_page_existe_dans_chaque_langue():
    for chemin, variantes in PAGES.items():
        manquantes = [l for l in homepage_i18n.LANGS if l not in variantes]
        assert not manquantes, f"{chemin} : variantes absentes {manquantes}"


def test_aucune_variante_nest_un_repli_francais():
    """Le filet anti-crash de build() rend le français. Utile en production,
    catastrophique si personne ne le remarque."""
    for chemin, variantes in PAGES.items():
        fr = variantes["fr"]
        identiques = [l for l in AUTRES if variantes[l] == fr]
        assert not identiques, f"{chemin} : non traduit en {identiques}"


def test_aucune_clef_orpheline():
    """Le garde-fou du choix « la clef est le texte ». Une entrée qui ne
    correspond plus à rien signale une phrase française reformulée — et donc
    sept langues devenues muettes à cet endroit."""
    sources = _sources()
    for chemin, (html, dico) in sources.items():
        orphelines = pages_i18n.clefs_orphelines(html, dico)
        assert not orphelines, (
            f"{chemin} : entrées qui ne traduisent plus rien → "
            + "; ".join(f"{l} : {c[:3]}" for l, c in orphelines.items()))


def test_les_dictionnaires_couvrent_les_memes_clefs():
    """Une clef présente en allemand et absente en italien = un trou de langue
    invisible : la page reste partiellement française."""
    for nom, (_html, dico) in _sources().items():
        reference = set(dico["en"])
        for lang in AUTRES:
            assert lang in dico, f"{nom} : langue {lang} absente du dictionnaire"
            manquantes = reference - set(dico[lang])
            assert not manquantes, f"{nom}/{lang} : clefs manquantes {sorted(manquantes)[:5]}"


# ── Ce que lit Google ────────────────────────────────────────────────────────
def test_html_lang_par_variante():
    for chemin, variantes in PAGES.items():
        for lang in homepage_i18n.LANGS:
            attendu = homepage_i18n.HTML_LANG[lang]
            trouve = re.search(r'<html[^>]*lang="([^"]+)"', variantes[lang])
            assert trouve and trouve.group(1) == attendu, (
                f"{chemin}/{lang} : lang={trouve.group(1) if trouve else 'absent'}")


def test_canonical_pointe_sur_la_page_elle_meme():
    for chemin, variantes in PAGES.items():
        for lang in homepage_i18n.LANGS:
            attendu = BASE + homepage_i18n.chemin_langue(lang, chemin)
            trouve = re.search(r'<link rel="canonical" href="([^"]+)"', variantes[lang])
            assert trouve, f"{chemin}/{lang} : aucune canonique"
            assert trouve.group(1) == attendu, (
                f"{chemin}/{lang} : canonique {trouve.group(1)} au lieu de {attendu}")


def test_hreflang_complet_sur_chaque_variante():
    """Google ignore EN BLOC une déclaration hreflang partielle : chaque page
    doit se déclarer elle-même et déclarer toutes les autres."""
    for chemin, variantes in PAGES.items():
        for lang in homepage_i18n.LANGS:
            html = variantes[lang]
            for autre in homepage_i18n.LANGS:
                url = BASE + homepage_i18n.chemin_langue(autre, chemin)
                assert f'href="{url}"' in html, (
                    f"{chemin}/{lang} : hreflang manquant vers {url}")


def test_une_route_repond_par_langue():
    from fastapi.testclient import TestClient

    client = TestClient(main.app)
    for chemin in PAGES:
        for lang in homepage_i18n.LANGS:
            url = homepage_i18n.chemin_langue(lang, chemin)
            r = client.get(url)
            assert r.status_code == 200, f"{url} → {r.status_code}"


def test_toutes_les_urls_traduites_sont_au_sitemap():
    from fastapi.testclient import TestClient

    xml = TestClient(main.app).get("/sitemap.xml").text
    for chemin in PAGES:
        for lang in homepage_i18n.LANGS:
            url = BASE + homepage_i18n.chemin_langue(lang, chemin)
            assert f"<loc>{url}</loc>" in xml, f"absent du sitemap : {url}"


# ── Navigation ───────────────────────────────────────────────────────────────
def test_les_liens_internes_restent_dans_la_langue():
    """Un visiteur allemand qui clique « Preise » ne doit pas quitter
    l'allemand. Le piège corrigé ici : réécrire les liens au fil de la
    construction laissait la première page renvoyer vers des pages françaises,
    simplement parce qu'elles n'étaient pas encore construites."""
    traduits = set(PAGES) | {"/"}
    for chemin, variantes in PAGES.items():
        for lang in AUTRES:
            prefixe = homepage_i18n.LANG_PATHS[lang]
            for balise in re.findall(r"<a\b[^>]*>", variantes[lang]):
                # Un lien qui déclare `hreflang` vise une langue précise : c'est
                # le cas de l'avertissement des pages légales, qui DOIT renvoyer
                # au français. Il est exempté, ici comme dans la réécriture.
                if re.search(r"\bhreflang=", balise):
                    continue
                m = re.search(r'href="(/[^"#?]*)', balise)
                if m and m.group(1) in traduits:
                    lien = m.group(1)
                    assert False, (
                        f"{chemin}/{lang} : le lien {lien} renvoie à la version "
                        f"française (attendu : {prefixe}{'' if lien == '/' else lien})")


def test_le_francais_garde_ses_urls_historiques():
    """Aucune page française ne doit se mettre à pointer vers /fr/… : ces URL
    sont indexées depuis le début, on ne les déplace pas."""
    for chemin, variantes in PAGES.items():
        assert "/fr/" not in variantes["fr"], f"{chemin} : lien /fr/ apparu"


# ── Pages légales : le français fait foi ────────────────────────────────────
LEGALES = ["/terms", "/mentions-legales", "/cgv", "/privacy"]


def test_les_pages_legales_traduites_portent_lavertissement():
    """Décision du 07/09/2026 : on traduit pour être compris, pas pour créer
    sept contrats opposables. Sans cet avertissement, les sept traductions
    vaudraient autant que le français — une nuance mal rendue dans des CGV
    deviendrait la règle applicable."""
    import pages_translations_legal as L

    for chemin in LEGALES:
        for lang in AUTRES:
            html = PAGES[chemin][lang]
            assert L.AVIS[lang][:60] in html, (
                f"{chemin}/{lang} : avertissement « le français fait foi » absent")
            assert f'href="{chemin}"' in html, (
                f"{chemin}/{lang} : l'avertissement ne renvoie pas à la page française")


def test_la_page_legale_francaise_ne_porte_pas_lavertissement():
    """Il n'aurait aucun sens sur l'original : c'est LUI qui fait foi."""
    import pages_translations_legal as L

    for chemin in LEGALES:
        assert L.AVIS["en"][:60] not in PAGES[chemin]["fr"]
        assert "fait foi" not in PAGES[chemin]["fr"].replace("faits", "")


def test_lavertissement_est_place_avant_le_texte_legal():
    """En pied de page, personne ne le lit. Il doit être sous le titre."""
    for chemin in LEGALES:
        html = PAGES[chemin]["de"]
        position_avis = html.find("Übersetzung nur zur Information")
        position_corps = html.find("<h2")
        assert 0 < position_avis < position_corps, (
            f"{chemin} : l'avertissement n'est pas au-dessus du texte")


# ── Le tableau de /pricing/compare, construit en JavaScript ──────────────────
def _script_marque(html: str) -> str:
    m = re.search(r"<script\b[^>]*\bdata-i18n-js\b[^>]*>(.*?)</script>", html, re.S)
    assert m, "script marqué introuvable"
    return m.group(1)


def test_le_script_traduit_reste_du_javascript_valide():
    """La panne réelle : « n:'Studio d'accroches IA' » — une apostrophe non
    échappée dans une chaîne à guillemets simples. Le script entier ne se
    parsait plus et le tableau comparatif était VIDE en production.

    Les traductions italiennes et espagnoles sont pleines d'apostrophes
    (« l'app », « all'anno ») : sans échappement à l'écriture, le même
    tableau retomberait dans le même trou, en sept langues cette fois.
    """
    motif = re.compile(r"'[^'\n]*[a-zA-ZÀ-ÿ]'[a-zA-ZÀ-ÿ]")
    for lang, html in PAGES["/pricing/compare"].items():
        fautes = motif.findall(_script_marque(html))
        assert not fautes, f"compare/{lang} : apostrophe non échappée → {fautes[:2]}"


def test_le_tableau_comparatif_a_le_meme_nombre_de_lignes_partout():
    """Un littéral mal refermé décalerait les frontières de chaînes : le
    nombre de lignes du tableau changerait. C'est un contrôle indirect, mais
    il attrape ce qu'une relecture ne voit pas."""
    reference = len(re.findall(r"\{\s*n\s*:", _script_marque(PAGES["/pricing/compare"]["fr"])))
    assert reference > 20, "tableau comparatif suspicieusement court"
    for lang, html in PAGES["/pricing/compare"].items():
        trouve = len(re.findall(r"\{\s*n\s*:", _script_marque(html)))
        assert trouve == reference, (
            f"compare/{lang} : {trouve} lignes au lieu de {reference}")


def test_le_tableau_comparatif_est_traduit():
    fr = _script_marque(PAGES["/pricing/compare"]["fr"])
    for lang in AUTRES:
        assert _script_marque(PAGES["/pricing/compare"][lang]) != fr, (
            f"compare/{lang} : tableau resté en français")


# ── Le mécanisme lui-même ────────────────────────────────────────────────────
def test_les_nombres_ne_sont_pas_dans_la_clef():
    """C'est ce qui permet de changer un tarif sans décrocher sept langues."""
    cle, nombres = pages_i18n.gabarit("10 analyses de vidéos")
    assert cle == "{0} analyses de vidéos"
    assert nombres == ["10"]
    cle, nombres = pages_i18n.gabarit("29,99 € par mois sur 12 mois")
    assert cle == "{0} € par mois sur {1} mois"
    assert nombres == ["29,99", "12"]


def test_un_texte_inconnu_reste_francais():
    """Le repli doit être le français, jamais un trou."""
    html = "<p>Une phrase absente du dictionnaire</p>"
    assert pages_i18n.traduire_texte(html, {"Autre chose": "Something else"}) == html


def test_le_code_des_scripts_nest_jamais_traduit():
    """Un script non marqué doit rester intact, même si son code contient une
    chaîne qui figure au dictionnaire."""
    html = "<script>var t = 'Tarifs';</script><p>Tarifs</p>"
    sortie = pages_i18n.traduire_texte(html, {"Tarifs": "Pricing"})
    assert "var t = 'Tarifs'" in sortie, "le code du script a été traduit"
    assert "<p>Pricing</p>" in sortie


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
