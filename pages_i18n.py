"""Traduction des pages SECONDAIRES — tarifs, légal, blog, atterrissage.

Pourquoi un second mécanisme alors que homepage_i18n existe déjà ?

La page d'accueil est traduite par des clefs `data-i18n` posées dans le gabarit.
C'est le bon outil là-bas : elle est réécrite souvent, ses textes bougent, et
une clef stable survit à une reformulation. Le prix à payer est d'annoter le
gabarit — acceptable pour UNE page, insoutenable pour dix-neuf, et carrément
déconseillé sur les pages légales, où toucher au balisage d'un contrat pour y
glisser des attributs est une prise de risque inutile.

Ici, la clef EST le texte français. Aucun gabarit n'est modifié : on relit le
HTML déjà rendu et on remplace les nœuds de texte dont le contenu figure au
dictionnaire. Conséquences assumées :

  • un texte français reformulé sort du dictionnaire et redevient français,
    au lieu d'afficher une traduction devenue fausse. C'est le bon défaut ;
  • pour que ce silence ne passe pas inaperçu, `clefs_orphelines()` liste les
    entrées qui ne correspondent plus à rien, et un test échoue dessus.

LES NOMBRES NE SONT PAS DANS LA CLEF. « 10 analyses de vidéos » est indexé
« {0} analyses de vidéos », et le nombre rencontré est réinjecté dans la
traduction. Sans ça, changer un tarif ou un quota décrocherait silencieusement
toutes les traductions qui le mentionnent — le genre de panne qu'on ne voit
que des mois plus tard. Les montants sont réinjectés TELS QUELS, dans leur
écriture française : le produit est facturé en euros, l'ordre de grandeur en
devise locale reste l'affaire de la page d'accueil (homepage_i18n._price_block).

Le reste — langues servies, chemins, hreflang, canonique — vient de
homepage_i18n : une seule liste de langues pour tout le site.
"""
from __future__ import annotations

import html as _html
import re

import homepage_i18n as _hp

LANGS = _hp.LANGS
DEFAULT = _hp.DEFAULT


# ── Clef d'un texte ──────────────────────────────────────────────────────────
# Un nombre = une suite de chiffres, éventuellement coupée par une virgule, un
# point ou une espace fine (29,99 · 1 000 · 293). Le « % » et le « € » qui le
# suivent restent dans la clef : ils font partie de la phrase, pas du nombre.
_NOMBRE = re.compile(r"\d+(?:[    .,]\d+)*")


def gabarit(texte: str) -> tuple[str, list[str]]:
    """« 10 analyses » → (« {0} analyses », [« 10 »])."""
    nombres: list[str] = []

    def repl(m: re.Match) -> str:
        nombres.append(m.group(0))
        return "{%d}" % (len(nombres) - 1)

    return _NOMBRE.sub(repl, texte), nombres


def _remplir(traduction: str, nombres: list[str]) -> str:
    """Réinjecte les nombres. Une traduction qui en oublie un ne casse pas la
    page : on la rend telle quelle plutôt que de lever."""
    try:
        return traduction.format(*nombres)
    except Exception:
        return traduction


# ── Remplacement des nœuds de texte ──────────────────────────────────────────
# Les <script> et <style> sont masqués avant le balayage : leur contenu n'est
# pas du texte de page, et une chaîne de code qui ressemblerait à une phrase
# française n'a rien à faire dans un dictionnaire de traduction.
_MASQUES = re.compile(r"<(script|style)\b.*?</\1>|<!--.*?-->", re.S | re.I)


def _zones_masquees(html: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in _MASQUES.finditer(html)]


def _dans_zone(pos: int, zones: list[tuple[int, int]]) -> bool:
    return any(d <= pos < f for d, f in zones)


def traduire_texte(html: str, dico: dict[str, str]) -> str:
    """Remplace chaque nœud de texte dont le contenu figure au dictionnaire.

    Le nœud est remplacé ENTIER, jamais par morceaux : une correspondance
    partielle traduirait un bout de phrase au milieu d'une autre.
    L'espacement d'origine est conservé — il porte parfois la mise en page.
    """
    if not dico:
        return html
    zones = _zones_masquees(html)

    def repl(m: re.Match) -> str:
        if _dans_zone(m.start(), zones):
            return m.group(0)
        brut = m.group(1)
        noyau = brut.strip()
        if not noyau:
            return m.group(0)
        cle, nombres = gabarit(_html.unescape(noyau))
        val = dico.get(cle)
        if val is None:
            return m.group(0)
        avant = brut[:len(brut) - len(brut.lstrip())]
        apres = brut[len(brut.rstrip()):]
        return ">" + avant + _html.escape(_remplir(val, nombres), quote=False) + apres + "<"

    return re.sub(r">([^<>]+)<", repl, html)


# Attributs porteurs de texte visible ou lu par un lecteur d'écran.
_ATTRIBUTS = ("alt", "placeholder", "aria-label", "title")


def traduire_attributs(html: str, dico: dict[str, str]) -> str:
    if not dico:
        return html
    zones = _zones_masquees(html)

    def repl(m: re.Match) -> str:
        if _dans_zone(m.start(), zones):
            return m.group(0)
        nom, valeur = m.group(1), m.group(2)
        cle, nombres = gabarit(_html.unescape(valeur.strip()))
        val = dico.get(cle)
        if val is None:
            return m.group(0)
        return f'{nom}="{_html.escape(_remplir(val, nombres), quote=True)}"'

    return re.sub(r'\b(' + "|".join(_ATTRIBUTS) + r')="([^"]+)"', repl, html)


# ── Chaînes de caractères d'un script marqué ─────────────────────────────────
# Certaines pages construisent leur contenu en JavaScript — le tableau
# comparatif de /pricing/compare, par exemple, est un tableau de trente
# libellés. Ce texte-là est invisible pour le balayage des nœuds : il vit dans
# un <script>, que l'on masque justement pour ne pas traduire du code.
#
# Un script qui veut être traduit le DEMANDE, en portant `data-i18n-js`. On n'y
# remplace alors que des littéraux de chaîne dont le contenu figure au
# dictionnaire — jamais un identifiant, jamais une clef d'objet, jamais une
# chaîne inconnue. Un script non marqué n'est pas touché.
_LITTERAL = re.compile(r"'((?:[^'\\\n]|\\.)*)'" + r'|"((?:[^"\\\n]|\\.)*)"')


def traduire_script(html: str, dico: dict[str, str]) -> str:
    """Traduit les chaînes des <script data-i18n-js>."""
    if not dico:
        return html

    def dans_script(m: re.Match) -> str:
        ouvrant, corps, fermant = m.group(1), m.group(2), m.group(3)

        def litteral(lm: re.Match) -> str:
            simple = lm.group(1) is not None
            brut = lm.group(1) if simple else lm.group(2)
            # Déséchappe ce que JavaScript échappe, pour retrouver le texte lu.
            texte = brut.replace("\\'", "'").replace('\\"', '"').strip()
            if not texte:
                return lm.group(0)
            cle, nombres = gabarit(texte)
            val = dico.get(cle)
            if val is None:
                return lm.group(0)
            val = _remplir(val, nombres)
            if simple:
                return "'" + val.replace("\\", "\\\\").replace("'", "\\'") + "'"
            return '"' + val.replace("\\", "\\\\").replace('"', '\\"') + '"'

        return ouvrant + _LITTERAL.sub(litteral, corps) + fermant

    return re.sub(r"(<script\b[^>]*\bdata-i18n-js\b[^>]*>)(.*?)(</script>)",
                  dans_script, html, flags=re.S)


def textes_de_script(html: str) -> set[str]:
    """Chaînes traduisibles des scripts marqués — pour les tests."""
    trouves: set[str] = set()
    for m in re.finditer(r"<script\b[^>]*\bdata-i18n-js\b[^>]*>(.*?)</script>",
                         html, re.S):
        for lm in _LITTERAL.finditer(m.group(1)):
            brut = lm.group(1) if lm.group(1) is not None else lm.group(2)
            texte = brut.replace("\\'", "'").replace('\\"', '"').strip()
            if texte:
                trouves.add(gabarit(texte)[0])
    return trouves


# ── Liens internes ───────────────────────────────────────────────────────────
# Un visiteur allemand qui clique « Preise » depuis /de doit arriver sur
# /de/pricing, pas sur la page française. Les chemins traduits sont enregistrés
# ici par main.py au démarrage ; tout ce qui n'y figure pas (l'app, le blog non
# traduit, un lien externe) est laissé intact — mieux vaut un lien français
# qu'un lien mort.
CHEMINS_TRADUITS: set[str] = set()


def enregistrer_chemin(chemin_fr: str) -> None:
    CHEMINS_TRADUITS.add(chemin_fr)


def liens_internes(html: str, lang: str) -> str:
    """Préfixe les liens internes déjà traduits par le code de langue.

    Exception : un lien qui déclare `hreflang` désigne explicitement une
    version linguistique et n'est jamais réécrit. C'est ce qui permet à
    l'avertissement des pages légales — « seule la version française fait
    foi » — de renvoyer réellement au français, et non à la traduction que le
    visiteur est déjà en train de lire.
    """
    if lang == DEFAULT or not CHEMINS_TRADUITS:
        return html
    prefixe = _hp.LANG_PATHS[lang]

    def repl(m: re.Match) -> str:
        balise = m.group(0)
        if re.search(r"\bhreflang=", balise):
            return balise

        def href(hm: re.Match) -> str:
            chemin = hm.group(2)
            base = chemin.split("#")[0].split("?")[0]
            if base not in CHEMINS_TRADUITS:
                return hm.group(0)
            suite = chemin[len(base):]       # ancre ou requête conservée
            cible = prefixe if base == "/" else prefixe + base
            return f"{hm.group(1)}{cible}{suite}{hm.group(3)}"

        return re.sub(r'(href=")(/[^"]*)(")', href, balise)

    return re.sub(r"<a\b[^>]*>", repl, html)


def reecrire_les_liens(pages_par_langue: "dict[str, str]") -> "dict[str, str]":
    """Passe finale : préfixe les liens internes de chaque variante.

    Séparée de `build()` parce que l'ordre compte. Réécrire au fil de l'eau
    donnait une page tarifs allemande qui renvoyait vers /credits en français,
    simplement parce que /credits n'était pas encore construit au moment où
    /pricing l'a été. Ici, tout est connu.
    """
    return {lang: liens_internes(html, lang) for lang, html in pages_par_langue.items()}


# ── Pages déjà écrites dans une autre langue ─────────────────────────────────
# Certaines pages existent DÉJÀ, écrites à la main, dans une langue étrangère :
# /en/blog/what-is-tiktok-shop est la version anglaise de l'article sur
# l'expansion mondiale, rédigée pour le marché et non traduite.
#
# Sans ce mécanisme, la traduction automatique en créait une SECONDE, et les
# deux se concurrençaient : deux pages anglaises du même article, chacune se
# déclarant canonique, avec des `hreflang` qui se contredisaient (l'article
# français désignait la traduction, la page écrite à la main se désignait
# elle-même). Google ignore en bloc une paire hreflang non réciproque.
#
# Un alias dit : « pour cette langue, l'adresse est celle-là, et on ne fabrique
# pas de variante ». C'est la page écrite pour le marché qui gagne — exactement
# la réserve posée en tête de pages_translations_seo.py.
ALIAS: "dict[str, dict[str, str]]" = {}


def poser_alias(chemin_fr: str, alias: "dict[str, str]") -> None:
    ALIAS[chemin_fr] = dict(alias)


def langue_aliasee(chemin_fr: str, lang: str) -> bool:
    """Cette langue est-elle servie par une page écrite à la main ?"""
    return lang in ALIAS.get(chemin_fr, {})


def url_langue(chemin_fr: str, lang: str) -> str:
    """Chemin public d'une page dans une langue — alias compris."""
    a = ALIAS.get(chemin_fr, {})
    return a.get(lang) or _hp.chemin_langue(lang, chemin_fr)


def bloc_hreflang(base: str, chemin_fr: str) -> str:
    """Les `alternate` d'une page, alias compris.

    Remplace `homepage_i18n._hreflang_block` pour les pages secondaires : lui
    ne connaît pas les alias et pointerait vers une URL qui n'existe pas.
    """
    liens = "".join(
        f'  <link rel="alternate" hreflang="{_hp.HTML_LANG[l]}" '
        f'href="{base}{url_langue(chemin_fr, l)}">\n'
        for l in LANGS
    )
    liens += f'  <link rel="alternate" hreflang="x-default" href="{base}{chemin_fr}">\n'
    return liens


def poser_alternates(html: str, chemin_fr: str, base: str) -> str:
    """Rend cohérents les `alternate` d'une page écrite à la main.

    Elle en portait trois, écrits en dur et incomplets. On les retire et on
    pose le même bloc que partout ailleurs, pour que les huit versions se
    déclarent mutuellement — condition pour que Google les prenne en compte.
    Sa canonique n'est pas touchée : elle EST l'adresse anglaise.
    """
    html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">', "", html)
    return html.replace("</head>", bloc_hreflang(base, chemin_fr) + "</head>", 1)


# ── Métadonnées ──────────────────────────────────────────────────────────────
def _metadonnees(html: str, lang: str, base: str, chemin_fr: str,
                 dico: dict[str, str]) -> str:
    """`lang` du document, canonique, Open Graph, hreflang.

    Le titre et la description passent par le dictionnaire comme le reste :
    leur clef est le texte français rendu.
    """
    url = base + url_langue(chemin_fr, lang)

    html = re.sub(r'<html lang="[^"]*"', f'<html lang="{_hp.HTML_LANG[lang]}"',
                  html, count=1)

    def pose(pattern: str, valeur: str, html: str) -> str:
        if re.search(pattern, html):
            return re.sub(pattern, lambda m: m.group(1) + valeur + m.group(2),
                          html, count=1)
        return html

    html = pose(r'(<link rel="canonical" href=")[^"]*(">)', url, html)
    html = pose(r'(<meta property="og:url" content=")[^"]*(">)', url, html)
    html = pose(r'(<meta property="og:locale" content=")[^"]*(">)',
                _hp.OG_LOCALE[lang], html)

    # Canonique absente du gabarit : on la pose, sinon les huit variantes se
    # concurrencent entre elles dans l'index.
    if "rel=\"canonical\"" not in html:
        html = html.replace("</head>",
                            f'  <link rel="canonical" href="{url}">\n</head>', 1)

    # Les `alternate` écrits en dur dans le gabarit sont retirés d'abord.
    # Sans ça, l'article sur l'expansion mondiale se retrouvait avec DEUX
    # `x-default` pointant vers des URL différentes — de quoi faire ignorer
    # toute la déclaration.
    html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">', "", html)
    html = html.replace("</head>", bloc_hreflang(base, chemin_fr) + "</head>", 1)
    return html


# ── Construction ─────────────────────────────────────────────────────────────
def inserer_apres_entete(html: str, fragment: str) -> str:
    """Glisse un fragment juste après le titre de la page (`</header>`).

    Sert à poser l'avertissement des pages légales — « en cas de divergence,
    la version française fait foi » — là où il est lu : au-dessus du texte,
    pas en bas de page. Si le gabarit n'a pas d'en-tête, on retombe sur le
    premier `<h1>` ; s'il n'en a pas non plus, on ne pose rien plutôt que de
    placer l'avis n'importe où.
    """
    if "</header>" in html:
        return html.replace("</header>", "</header>\n" + fragment, 1)
    m = re.search(r"</h1>", html)
    if m:
        return html[:m.end()] + "\n" + fragment + html[m.end():]
    return html


def build(html_fr: str, chemin_fr: str, dico: "dict[str, dict[str, str]]",
          base_url: str, avis: "dict[str, str] | None" = None) -> dict[str, str]:
    """Fabrique une variante par langue. Le français est la source et le repli.

    Comme pour l'accueil, tout se joue AU DÉMARRAGE : aucune requête ne paie le
    coût de la traduction. Une langue qui échoue retombe sur le français —
    jamais une page en erreur.

    Les liens internes ne sont PAS réécrits ici : il faudrait connaître toutes
    les pages traduites, et la première construite ne les connaît pas encore.
    C'est le rôle de `reecrire_les_liens()`, appelé une fois tout construit.
    """
    enregistrer_chemin(chemin_fr)
    pages: dict[str, str] = {}
    for lang in LANGS:
        if langue_aliasee(chemin_fr, lang):
            # Cette langue a sa page écrite à la main : ne rien fabriquer.
            # Garder en mémoire une variante que personne ne sert serait au
            # mieux du gaspillage, au pire un piège — quelqu'un finirait par
            # lui poser une route et recréer la page en double.
            continue
        try:
            page = html_fr
            if lang != DEFAULT:
                d = dico.get(lang) or {}
                page = traduire_texte(page, d)
                page = traduire_attributs(page, d)
                page = traduire_script(page, d)
                page = _titre(page, d)
                if avis and avis.get(lang):
                    page = inserer_apres_entete(page, avis[lang])
            page = _metadonnees(page, lang, base_url, chemin_fr, dico.get(lang) or {})
            pages[lang] = page
        except Exception as e:  # pragma: no cover - filet au démarrage
            print(f"[i18n] '{chemin_fr}' variante '{lang}' non générée ({e}) — repli français")
            pages[lang] = html_fr
    return pages


def _titre(html: str, dico: dict[str, str]) -> str:
    """<title> et meta description : mêmes clefs, mêmes règles."""
    def repl_titre(m: re.Match) -> str:
        cle, nombres = gabarit(_html.unescape(m.group(1).strip()))
        val = dico.get(cle)
        return f"<title>{_html.escape(_remplir(val, nombres), quote=False)}</title>" if val else m.group(0)

    html = re.sub(r"<title>(.*?)</title>", repl_titre, html, count=1, flags=re.S)

    for pattern in (r'(<meta name="description" content=")([^"]*)(">)',
                    r'(<meta property="og:title" content=")([^"]*)(">)',
                    r'(<meta property="og:description" content=")([^"]*)(">)',
                    r'(<meta name="twitter:title" content=")([^"]*)(">)',
                    r'(<meta name="twitter:description" content=")([^"]*)(">)'):
        def repl(m: re.Match) -> str:
            cle, nombres = gabarit(_html.unescape(m.group(2).strip()))
            val = dico.get(cle)
            if val is None:
                return m.group(0)
            return m.group(1) + _html.escape(_remplir(val, nombres), quote=True) + m.group(3)
        html = re.sub(pattern, repl, html, count=1)
    return html


# ── Contrôle des dictionnaires ───────────────────────────────────────────────
def textes_de_la_page(html: str) -> set[str]:
    """Toutes les clefs qu'une page peut consommer — nœuds de texte, attributs,
    titre et métadonnées. Sert aux tests : une entrée de dictionnaire absente
    d'ici ne traduit plus rien."""
    zones = _zones_masquees(html)
    trouves: set[str] = set()

    for m in re.finditer(r">([^<>]+)<", html):
        if _dans_zone(m.start(), zones):
            continue
        noyau = m.group(1).strip()
        if noyau:
            trouves.add(gabarit(_html.unescape(noyau))[0])

    for m in re.finditer(r'\b(?:' + "|".join(_ATTRIBUTS) + r')="([^"]+)"', html):
        if not _dans_zone(m.start(), zones):
            trouves.add(gabarit(_html.unescape(m.group(1).strip()))[0])

    trouves |= textes_de_script(html)

    for pattern in (r"<title>(.*?)</title>",
                    r'<meta name="description" content="([^"]*)"',
                    r'<meta property="og:title" content="([^"]*)"',
                    r'<meta property="og:description" content="([^"]*)"',
                    r'<meta name="twitter:title" content="([^"]*)"',
                    r'<meta name="twitter:description" content="([^"]*)"'):
        for m in re.finditer(pattern, html, re.S):
            trouves.add(gabarit(_html.unescape(m.group(1).strip()))[0])

    return trouves


def clefs_orphelines(html_fr: str, dico: "dict[str, dict[str, str]]") -> dict[str, list[str]]:
    """Entrées qui ne correspondent à aucun texte de la page — donc mortes.

    C'est le garde-fou du choix « la clef est le texte » : une reformulation
    française rend la page muette dans les sept autres langues, sans rien
    casser de visible. Ce contrôle la rend bruyante.
    """
    presents = textes_de_la_page(html_fr)
    return {lang: sorted(k for k in d if k not in presents)
            for lang, d in dico.items() if any(k not in presents for k in d)}
