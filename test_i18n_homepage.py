"""Tests de la page d'accueil multilingue — ce qui doit rester vrai pour que les
huit versions soient servies ET indexées.

⚠️ POURQUOI CE FICHIER EXISTE.
La traduction se fait au DÉMARRAGE, par réécriture du HTML français déjà rendu
(homepage_i18n.build). Une variante qui échoue ne fait pas tomber le site : elle
retombe silencieusement sur le français. C'est le bon comportement en production
— mais ça veut dire qu'une régression de traduction est INVISIBLE sans test.

Le premier contrôle écrit à la main était d'ailleurs trop faible : vérifier que
« 293 B » figure dans /en-ie passait aussi quand la page était retombée en
français, puisque le texte français contient la même mention. Les tests
ci-dessous vérifient donc systématiquement qu'une variante DIFFÈRE du français.

Ce qui est couvert :
  • les huit variantes existent et aucune n'est un repli français déguisé ;
  • <html lang>, canonical et Open Graph pointent bien sur la bonne URL ;
  • chaque page déclare TOUTES les autres en hreflang (exigence de Google :
    une déclaration partielle est ignorée en bloc) ;
  • le prix converti n'apparaît que hors zone euro, et jamais en zone euro ;
  • la mention fiscale française ne fuit pas sur un marché non européen ;
  • le sélecteur marque la bonne option comme sélectionnée ;
  • aucune clef de traduction non résolue ne subsiste dans le HTML servi.

Aucune base de données ni clé d'API n'est requise : tout est calculé au boot.

Lancement :
    venv/bin/python -m pytest test_i18n_homepage.py -v
ou, sans pytest :
    venv/bin/python test_i18n_homepage.py
"""
from __future__ import annotations

import io
import os
import re

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

import homepage_i18n
import main

PAGES = main._HOMEPAGE_BY_LANG
BASE = main._seo_base_url()


# ── Les huit variantes existent, et sont réellement traduites ────────────────
def test_toutes_les_langues_sont_generees():
    manquantes = [l for l in homepage_i18n.LANGS if l not in PAGES]
    assert not manquantes, f"variantes absentes : {manquantes}"


def test_aucune_variante_nest_un_repli_francais():
    """Le filet anti-crash de build() retombe sur le français. Utile en prod,
    catastrophique si personne ne le remarque : ici on l'interdit."""
    fr = PAGES["fr"]
    identiques = [l for l in homepage_i18n.LANGS if l != "fr" and PAGES[l] == fr]
    assert not identiques, (
        f"ces variantes sont identiques au français, donc non traduites : {identiques}"
    )


def test_le_contenu_est_bien_dans_la_langue():
    """Un marqueur propre à chaque langue, pris dans le menu de navigation."""
    marqueurs = {
        "en": "Try it free",
        "en-ie": "Try it free",
        "pt-br": "Testar de graça",
        "es": "Probar gratis",
        "es-mx": "Pruébalo gratis",
        "it": "Provalo gratis",
        "de": "Kostenlos testen",
        "fr": "Tester gratuitement",
    }
    for lang, attendu in marqueurs.items():
        assert attendu in PAGES[lang], f"{lang} : « {attendu} » introuvable"


# ── Indexation ───────────────────────────────────────────────────────────────
def test_html_lang_par_variante():
    for lang in homepage_i18n.LANGS:
        attendu = f'<html lang="{homepage_i18n.HTML_LANG[lang]}"'
        assert attendu in PAGES[lang], f"{lang} : {attendu} absent"


def test_canonical_pointe_sur_la_page_elle_meme():
    """Sans canonique distincte, Google n'indexerait qu'une seule des huit."""
    for lang in homepage_i18n.LANGS:
        url = BASE + homepage_i18n.LANG_PATHS[lang]
        attendu = f'<link rel="canonical" href="{url}">'
        assert attendu in PAGES[lang], f"{lang} : canonique attendue {url}"


def test_og_url_et_locale_suivent_la_langue():
    for lang in homepage_i18n.LANGS:
        url = BASE + homepage_i18n.LANG_PATHS[lang]
        page = PAGES[lang]
        assert f'<meta property="og:url" content="{url}">' in page, f"{lang} : og:url"
        locale = homepage_i18n.OG_LOCALE[lang]
        assert f'<meta property="og:locale" content="{locale}">' in page, f"{lang} : og:locale"


def test_hreflang_complet_sur_chaque_variante():
    """Google exige que CHAQUE version déclare toutes les autres, plus
    x-default. Une déclaration partielle est ignorée en entier."""
    attendu = len(homepage_i18n.LANGS) + 1  # + x-default
    for lang in homepage_i18n.LANGS:
        n = PAGES[lang].count('rel="alternate" hreflang=')
        assert n == attendu, f"{lang} : {n} balises hreflang au lieu de {attendu}"


def test_hreflang_x_default_vers_la_racine():
    for lang in homepage_i18n.LANGS:
        assert f'hreflang="x-default" href="{BASE}/"' in PAGES[lang], lang


def test_toutes_les_langues_sont_au_sitemap():
    for lang in homepage_i18n.LANGS:
        chemin = homepage_i18n.LANG_PATHS[lang]
        assert chemin in main._SITEMAP_PATHS, f"{chemin} absent du sitemap"


def test_une_route_repond_par_langue():
    from fastapi.testclient import TestClient

    with TestClient(main.app) as client:
        for lang in homepage_i18n.LANGS:
            r = client.get(homepage_i18n.LANG_PATHS[lang])
            assert r.status_code == 200, f"{lang} : HTTP {r.status_code}"
            assert f'<html lang="{homepage_i18n.HTML_LANG[lang]}"' in r.text, lang


# ── Prix et mention fiscale ──────────────────────────────────────────────────
def test_prix_converti_uniquement_hors_zone_euro():
    for lang in homepage_i18n.LANGS:
        # Le conteneur porte un attribut `style` : on ne peut pas se contenter
        # de chercher `id="pr-approx">`, il faut lire ce qu'il contient.
        bloc = re.search(r'<div id="pr-approx"[^>]*>(.*?)</div>', PAGES[lang], re.S)
        assert bloc, f"{lang} : conteneur pr-approx introuvable"
        a_une_conversion = bool(bloc.group(1).strip())
        attendu = lang in homepage_i18n.DISPLAY_CURRENCIES
        assert a_une_conversion == attendu, (
            f"{lang} : conversion {'attendue' if attendu else 'inattendue'}"
        )


def test_montants_convertis_corrects():
    """Les taux ne servent qu'à l'affichage, mais un montant faux décrédibilise
    la page autant qu'un bug. On vérifie qu'ils sortent bien du site_content."""
    import site_content

    for lang, devises in homepage_i18n.DISPLAY_CURRENCIES.items():
        prix = homepage_i18n.prix_affiches(lang)
        assert prix is not None, f"{lang} : aucun prix calculé"
        for devise in devises:
            taux, _ = homepage_i18n.FX[devise]
            attendu = round(site_content.PRICE_MONTH * taux)
            assert str(attendu) in prix[0].replace(",", "").replace(".", ""), (
                f"{lang}/{devise} : {attendu} absent de « {prix[0]} »"
            )


def test_mention_fiscale_francaise_absente_hors_ue():
    """Le vrai piège : « 293 B » est une mention du code des impôts FRANÇAIS.
    La voir sur /es-mx ou /en serait une erreur de fond, pas de traduction."""
    for lang in homepage_i18n.NON_EU_MARKETS:
        assert "293 B" not in PAGES[lang], f"{lang} : mention fiscale française servie"


def test_mention_fiscale_presente_en_zone_euro():
    for lang in homepage_i18n.LANGS:
        if lang in homepage_i18n.NON_EU_MARKETS:
            continue
        assert "293 B" in PAGES[lang], f"{lang} : mention 293 B manquante"


def test_irlande_est_traitee_comme_zone_euro():
    """Cas limite qui a motivé la variante : anglophone MAIS zone euro."""
    page = PAGES["en-ie"]
    assert page != PAGES["fr"], "en-ie est retombé sur le français"
    assert "Try it free" in page, "en-ie n'est pas en anglais"
    assert "293 B" in page, "en-ie devrait porter la mention européenne"
    assert "US$" not in page and "£" not in page, "en-ie ne doit pas convertir"


# ── Sélecteur et propreté du HTML ────────────────────────────────────────────
def test_selecteur_marque_la_langue_courante():
    for lang in homepage_i18n.LANGS:
        attendu = f'<option value="{lang}" selected>'
        assert attendu in PAGES[lang], f"{lang} : option non sélectionnée"
        assert PAGES[lang].count(" selected>") == 1, f"{lang} : plusieurs options sélectionnées"


def test_selecteur_propose_toutes_les_langues():
    for lang in homepage_i18n.LANGS:
        for autre in homepage_i18n.LANGS:
            assert f'<option value="{autre}"' in PAGES[lang], f"{lang} : {autre} absent du menu"


def test_aucun_jeton_de_traduction_non_resolu():
    """{trial}, {count}, {dims}… doivent tous avoir été remplacés."""
    for lang in homepage_i18n.LANGS:
        restants = re.findall(
            r"\{(trial|trial_full|count|dims|m|y)\}", PAGES[lang]
        )
        assert not restants, f"{lang} : jetons non résolus {set(restants)}"


def test_toutes_les_clefs_existent_dans_chaque_langue():
    """Une clef absente retombe en silence sur le français : c'est exactement
    le genre de trou qu'on ne voit pas à l'œil nu sur une page de 3000 lignes."""
    # Chemin relatif AU FICHIER, pas au répertoire courant : le test doit
    # passer qu'on le lance depuis la racine ou depuis ailleurs.
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "templates", "homepage.html")
    with open(chemin, encoding="utf-8") as f:
        gabarit = f.read()
    utilisees = set(re.findall(r'data-i18n(?:-html|-ph|-aria)?="(\w+)"', gabarit))
    for lang in homepage_i18n.LANGS:
        if lang == "fr":
            continue  # le français EST le gabarit
        manquantes = utilisees - set(homepage_i18n.T[lang])
        assert not manquantes, f"{lang} : {len(manquantes)} clefs manquantes {sorted(manquantes)[:5]}"


# ── Langue des ANALYSES ──────────────────────────────────────────────────────
# Ces fonctions décident dans quelle langue un abonné reçoit son rapport, et si
# le cache peut lui servir celui d'un autre. Ce sont des fonctions pures : les
# tester coûte quelques millisecondes et couvre le chemin le plus risqué.
def test_normalisation_des_langues_regionales():
    import analyzer

    cas = {
        "en-ie": "en", "en-gb": "en", "en-US": "en",   # variantes anglaises
        "pt": "pt-br", "pt-BR": "pt-br",
        "es-mx": "es-mx", "es": "es",                  # le Mexique reste distinct
        "de": "de", "it": "it", "fr": "fr",
        "": "fr", None: "fr", "klingon": "fr",         # inconnu → français
        "zh-Hans": "fr",                               # marché non ouvert
    }
    for entree, attendu in cas.items():
        obtenu = analyzer.normaliser_langue(entree)
        assert obtenu == attendu, f"{entree!r} → {obtenu!r} au lieu de {attendu!r}"


def test_le_prompt_francais_est_inchange():
    """Propriété de sécurité : en français, la consigne de langue est VIDE, donc
    le prompt est identique au caractère près à ce qu'il était avant. Le marché
    historique ne doit rien voir passer."""
    import analyzer

    assert analyzer._directive_langue("fr") == ""
    assert analyzer._directive_langue(None) == ""
    assert analyzer._directive_langue("klingon") == ""


def test_la_consigne_protege_les_clefs_json():
    """Le post-traitement et le front lisent des clefs françaises en dur : la
    consigne doit interdire explicitement de les traduire."""
    import analyzer

    for lang in ("en", "de", "es-mx", "pt-br"):
        directive = analyzer._directive_langue(lang)
        assert directive, f"{lang} : aucune consigne de langue"
        assert "CLÉS" in directive, f"{lang} : les clefs ne sont pas protégées"
        assert analyzer.LANGUES_ANALYSE[lang] in directive, f"{lang} : langue non nommée"


def test_le_cache_ne_melange_pas_les_langues():
    """Le bug qui aurait servi un rapport français à un Allemand : la table n'a
    pas de colonne `lang`, la langue est encodée dans l'étiquette `pipeline`."""
    import analysis_cache

    # Le français garde l'étiquette historique → le cache déjà constitué survit.
    assert analysis_cache._pipeline_key("pro", "fr") == "pro"
    assert analysis_cache._pipeline_key("pro", None) == "pro"
    assert analysis_cache._pipeline_key("pro", "") == "pro"
    # Toute autre langue est isolée.
    assert analysis_cache._pipeline_key("pro", "de") == "pro:de"
    assert analysis_cache._pipeline_key("pro", "es-mx") == "pro:es-mx"
    # Et deux langues ne peuvent pas se confondre.
    cles = {analysis_cache._pipeline_key("pro", l)
            for l in ("fr", "en", "de", "es", "es-mx", "it", "pt-br")}
    assert len(cles) == 7, f"collision d'étiquettes de cache : {cles}"


def test_les_emails_danalyse_couvrent_toutes_les_langues():
    import analysis_runner

    attendues = {"fr", "en", "pt-br", "es", "es-mx", "it", "de"}
    assert set(analysis_runner._MAILS) == attendues
    reference = set(analysis_runner._MAILS["fr"])
    for lang, textes in analysis_runner._MAILS.items():
        manquantes = reference - set(textes)
        assert not manquantes, f"e-mail {lang} : clefs manquantes {manquantes}"


# ── Bandeau cookies (JavaScript, mais vérifiable d'ici) ─────────────────────
def _textes_du_bandeau() -> dict:
    """Extrait le dictionnaire `TEXTES` de static/qeerah-consent.js.

    Le bandeau est écrit en JavaScript ; ses traductions n'ont donc aucun test
    Python « naturel ». Elles en méritent quand même un : c'est le seul texte
    servi sur les huit pages d'accueil, et c'est par lui qu'on recueille un
    consentement — un consentement n'est éclairé que s'il est compris. On lit
    donc le fichier et on vérifie sa structure, sans interpréteur JS.
    """
    source = io.open("static/qeerah-consent.js", encoding="utf-8").read()
    debut = source.index("var TEXTES = {")
    ouvrant = source.index("{", debut)
    profondeur = 0
    for i in range(ouvrant, len(source)):
        if source[i] == "{":
            profondeur += 1
        elif source[i] == "}":
            profondeur -= 1
            if profondeur == 0:
                fin = i
                break
    bloc = source[ouvrant:fin + 1]
    morceaux = re.split(r'\n    (?:"([a-z-]+)"|([a-z-]+)):\s*\{', bloc)
    langues = {}
    for i in range(1, len(morceaux), 3):
        nom = morceaux[i] or morceaux[i + 1]
        langues[nom] = set(re.findall(r"(?:^|\n)\s{6}([a-z_]+):", morceaux[i + 2]))
    return langues


def test_le_bandeau_cookies_couvre_toutes_les_langues_servies():
    """Chaque langue de la page d'accueil doit avoir son bandeau — directement,
    ou par le rabattement d'une variante régionale (es-mx → es)."""
    langues = _textes_du_bandeau()
    source = io.open("static/qeerah-consent.js", encoding="utf-8").read()
    rabattues = dict(re.findall(r'"([a-z-]+)":\s*"([a-z-]+)"',
                                source[source.index("var LANGUES_RABATTUES"):
                                       source.index("function normaliserLangue")]))
    manquantes = [l for l in homepage_i18n.LANGS
                  if l not in langues and rabattues.get(l) not in langues]
    assert not manquantes, f"bandeau cookies absent pour : {manquantes}"


def test_le_bandeau_cookies_na_aucun_trou_de_texte():
    """Une clef oubliée dans une langue afficherait « undefined » dans le
    bandeau — pire que du français, illisible."""
    langues = _textes_du_bandeau()
    reference = langues["fr"]
    for lang, clefs in langues.items():
        manquantes = reference - clefs
        assert not manquantes, f"bandeau {lang} : clefs manquantes {manquantes}"


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
