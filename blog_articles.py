"""Articles « guides » du blog : un gabarit, huit langues, zéro copier-coller.

POURQUOI CE MODULE — les articles historiques (blog_*.html) sont des pages
complètes de 400 lignes, chacune avec son <head>, son JSON-LD et son CSS écrits
à la main, traduites ensuite par pages_i18n (la clef est le texte français).
Ce mécanisme tient pour une page courte ; pour un article de 1 200 mots il
oblige à maintenir un dictionnaire phrase par phrase dans sept langues, et la
moindre reformulation française rend l'article muet dans les autres.

Ici, chaque article est un DOSSIER de contenu :

    content/blog/<id>/article.json   métadonnées communes + par langue
    content/blog/<id>/fr.html        corps de l'article (fragment, sans <h1>)
    content/blog/<id>/en.html
    content/blog/<id>/pt-br.html  es.html  it.html  de.html

Tout le reste — <head>, title, description, canonique, hreflang, Open Graph,
JSON-LD (Article + BreadcrumbList + FAQPage), sommaire, FAQ, appel à l'action,
articles liés, sources, sitemap, llms.txt, carte sur /blog — est FABRIQUÉ ici.
Ajouter un article = créer un dossier. Rien d'autre à toucher.

Chaque langue a SON slug, écrit pour la requête du marché : un Allemand tape
« TikTok Shop Videos analysieren », pas « analyser-ses-videos ».

`en-ie` et `es-mx` réutilisent le texte de `en` et `es` (cf. SOURCE_LANGUE) :
même article, mais une URL et une balise hreflang propres, comme le reste du
site.

Rédaction et publication : docs/SEO_GEO.md.
"""
from __future__ import annotations

import html as _html
import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import jinja2
import markupsafe

import homepage_i18n as _hp

CONTENU = Path("content/blog")
LANGS = _hp.LANGS
DEFAULT = _hp.DEFAULT

# Langues qui partagent le texte d'une autre. L'URL, <html lang>, og:locale et
# hreflang restent propres à chacune.
SOURCE_LANGUE = {"en-ie": "en", "es-mx": "es"}
LANGUES_REDIGEES = [l for l in LANGS if l not in SOURCE_LANGUE]

# Bornes de la Partie 1 du brief SEO. Vérifiées par controler() et par les tests.
TITRE_MAX = 60
DESCRIPTION_MAX = 155
DESCRIPTION_MIN = 70
MOTS_FR_MIN = 800
MOTS_FR_MAX = 1700

SUFFIXE_TITRE = " | Qeerah"

_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_H2 = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.S)
_LIEN_GUIDE = re.compile(r'href="guide:([a-z0-9-]+)"')
_MARQUEUR_SCHEMA = "<!--SCHEMA-->"

# Images de partage : générées par generate_og_images.py, versionnées ici.
OG_DOSSIER = Path("static/og")
OG_LARGEUR, OG_HAUTEUR = 1200, 630


def nom_image_og(article_id: str, lang: str) -> str:
    return f"{article_id}-{source(lang)}.jpg"


def source(lang: str) -> str:
    """Langue dont le texte sert à `lang`."""
    return SOURCE_LANGUE.get(lang, lang)


# ── Textes d'interface ───────────────────────────────────────────────────────
# Tout ce qui entoure l'article. Les mois sont là pour dater sans dépendre de la
# locale du serveur (Render tourne en C.UTF-8).
UI: "dict[str, dict]" = {
    "fr": {
        "accueil": "Accueil", "blog": "Blog", "retour": "← Retour au blog",
        "en_bref": "En bref :", "sommaire": "Sommaire", "faq": "Questions fréquentes",
        "sources": "Sources", "a_lire": "À lire aussi", "par": "Par l'équipe Qeerah",
        "lecture": "{n} min de lecture", "maj": "Mis à jour le {d}",
        "lire": "Lire l'article →", "langues": "Lire dans une autre langue",
        "essai": "7 jours d'accès complet, sans carte bancaire.",
        "droits": "© 2026 Qeerah - Dope Ventures. Tous droits réservés.",
        "mois": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
                 "août", "septembre", "octobre", "novembre", "décembre"],
        "date": "{j} {m} {a}",
    },
    "en": {
        "accueil": "Home", "blog": "Blog", "retour": "← Back to blog",
        "en_bref": "In short:", "sommaire": "Contents", "faq": "Frequently asked questions",
        "sources": "Sources", "a_lire": "Read next", "par": "By the Qeerah team",
        "lecture": "{n} min read", "maj": "Updated {d}",
        "lire": "Read the article →", "langues": "Read in another language",
        "essai": "7 days of full access, no card required.",
        "droits": "© 2026 Qeerah - Dope Ventures. All rights reserved.",
        "mois": ["January", "February", "March", "April", "May", "June", "July",
                 "August", "September", "October", "November", "December"],
        "date": "{j} {m} {a}",
    },
    "pt-br": {
        "accueil": "Início", "blog": "Blog", "retour": "← Voltar ao blog",
        "en_bref": "Em resumo:", "sommaire": "Sumário", "faq": "Perguntas frequentes",
        "sources": "Fontes", "a_lire": "Leia também", "par": "Pela equipe Qeerah",
        "lecture": "{n} min de leitura", "maj": "Atualizado em {d}",
        "lire": "Ler o artigo →", "langues": "Ler em outro idioma",
        "essai": "7 dias de acesso completo, sem cartão.",
        "droits": "© 2026 Qeerah - Dope Ventures. Todos os direitos reservados.",
        "mois": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
                 "agosto", "setembro", "outubro", "novembro", "dezembro"],
        "date": "{j} de {m} de {a}",
    },
    "es": {
        "accueil": "Inicio", "blog": "Blog", "retour": "← Volver al blog",
        "en_bref": "En resumen:", "sommaire": "Índice", "faq": "Preguntas frecuentes",
        "sources": "Fuentes", "a_lire": "Sigue leyendo", "par": "Por el equipo de Qeerah",
        "lecture": "{n} min de lectura", "maj": "Actualizado el {d}",
        "lire": "Leer el artículo →", "langues": "Leer en otro idioma",
        "essai": "7 días de acceso completo, sin tarjeta.",
        "droits": "© 2026 Qeerah - Dope Ventures. Todos los derechos reservados.",
        "mois": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
                 "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
        "date": "{j} de {m} de {a}",
    },
    "it": {
        "accueil": "Home", "blog": "Blog", "retour": "← Torna al blog",
        "en_bref": "In breve:", "sommaire": "Indice", "faq": "Domande frequenti",
        "sources": "Fonti", "a_lire": "Leggi anche", "par": "Dal team Qeerah",
        "lecture": "{n} min di lettura", "maj": "Aggiornato il {d}",
        "lire": "Leggi l'articolo →", "langues": "Leggi in un'altra lingua",
        "essai": "7 giorni di accesso completo, senza carta.",
        "droits": "© 2026 Qeerah - Dope Ventures. Tutti i diritti riservati.",
        "mois": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
                 "agosto", "settembre", "ottobre", "novembre", "dicembre"],
        "date": "{j} {m} {a}",
    },
    "de": {
        "accueil": "Startseite", "blog": "Blog", "retour": "← Zurück zum Blog",
        "en_bref": "Kurz gesagt:", "sommaire": "Inhalt", "faq": "Häufige Fragen",
        "sources": "Quellen", "a_lire": "Weiterlesen", "par": "Vom Qeerah-Team",
        "lecture": "{n} Min. Lesezeit", "maj": "Aktualisiert am {d}",
        "lire": "Artikel lesen →", "langues": "In einer anderen Sprache lesen",
        "essai": "7 Tage voller Zugang, ohne Kreditkarte.",
        "droits": "© 2026 Qeerah - Dope Ventures. Alle Rechte vorbehalten.",
        "mois": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
                 "August", "September", "Oktober", "November", "Dezember"],
        "date": "{j}. {m} {a}",
    },
}

# Appels à l'action : une fonctionnalité Qeerah par clef. `chemin` est le
# chemin FRANÇAIS ; la passe finale de main.py le préfixe pour les pages
# traduites (« /#tool » devient « /de#tool »).
CTA: "dict[str, dict]" = {
    "analyse": {
        "chemin": "/#tool",
        "fr": ("Pourquoi cette vidéo vend ?", "Colle le lien d'une vidéo TikTok Shop : Qeerah note l'accroche, la rétention et l'appel à l'action, repère la seconde où l'attention décroche et te dit quoi corriger.", "Analyser ma première vidéo gratuitement"),
        "en": ("Why does this video sell?", "Paste a TikTok Shop video link: Qeerah scores the hook, retention and call to action, finds the second attention drops and tells you what to fix.", "Analyse my first video for free"),
        "pt-br": ("Por que esse vídeo vende?", "Cole o link de um vídeo do TikTok Shop: a Qeerah avalia o gancho, a retenção e a chamada para ação, encontra o segundo em que a atenção cai e diz o que corrigir.", "Analisar meu primeiro vídeo grátis"),
        "es": ("¿Por qué vende este vídeo?", "Pega el enlace de un vídeo de TikTok Shop: Qeerah puntúa el gancho, la retención y la llamada a la acción, localiza el segundo en que cae la atención y te dice qué corregir.", "Analizar mi primer vídeo gratis"),
        "it": ("Perché questo video vende?", "Incolla il link di un video TikTok Shop: Qeerah valuta l'hook, la retention e la call to action, trova il secondo in cui l'attenzione cala e ti dice cosa correggere.", "Analizza il mio primo video gratis"),
        "de": ("Warum verkauft dieses Video?", "Füge den Link eines TikTok-Shop-Videos ein: Qeerah bewertet Hook, Retention und Call-to-Action, findet die Sekunde, in der die Aufmerksamkeit abfällt, und sagt dir, was du ändern solltest.", "Mein erstes Video kostenlos analysieren"),
    },
    "hooks": {
        "chemin": "/#tool",
        "fr": ("Teste ton hook avant de le tourner", "Analyse une vidéo qui vend dans ta niche : Qeerah identifie le type d'accroche, les déclencheurs psychologiques présents et absents, puis réécrit des accroches pour ton produit.", "Analyser une vidéo gratuitement"),
        "en": ("Test your hook before you film it", "Analyse a video that sells in your niche: Qeerah identifies the hook type, the psychological triggers present and missing, then rewrites hooks for your product.", "Analyse a video for free"),
        "pt-br": ("Teste seu gancho antes de gravar", "Analise um vídeo que vende no seu nicho: a Qeerah identifica o tipo de gancho, os gatilhos psicológicos presentes e ausentes e reescreve ganchos para o seu produto.", "Analisar um vídeo grátis"),
        "es": ("Prueba tu gancho antes de grabarlo", "Analiza un vídeo que vende en tu nicho: Qeerah identifica el tipo de gancho, los disparadores psicológicos presentes y ausentes, y reescribe ganchos para tu producto.", "Analizar un vídeo gratis"),
        "it": ("Testa il tuo hook prima di girarlo", "Analizza un video che vende nella tua nicchia: Qeerah identifica il tipo di hook, i trigger psicologici presenti e mancanti, poi riscrive hook per il tuo prodotto.", "Analizza un video gratis"),
        "de": ("Teste deinen Hook, bevor du drehst", "Analysiere ein Video, das in deiner Nische verkauft: Qeerah erkennt den Hook-Typ, vorhandene und fehlende psychologische Trigger und schreibt Hooks für dein Produkt neu.", "Ein Video kostenlos analysieren"),
    },
}


# ── Modèle ───────────────────────────────────────────────────────────────────
@dataclass
class Article:
    id: str
    requete: str                 # requête cible française (suivi, docs)
    intention: str
    publie: date
    maj: date
    lecture_min: int
    cta: str
    lies: "list[str]"
    sources: "list[dict]"
    langues: "dict[str, dict]"   # langue rédigée → métadonnées
    corps: "dict[str, str]"      # langue rédigée → fragment HTML
    schema: str = ""             # type de schéma posé à <!--SCHEMA--> (cf. SCHEMAS)
    brouillon: bool = False
    dossier: Path = field(default_factory=Path)

    def meta(self, lang: str) -> dict:
        return self.langues[source(lang)]

    def chemin(self, lang: str) -> str:
        return _hp.chemin_langue(lang, "/blog/" + self.meta(lang)["slug"])

    def image(self, lang: str, base: str) -> "tuple[str, bool]":
        """(URL de l'image de partage, True si elle est propre à l'article).

        Repli sur le logo si l'image n'a pas été générée : un article publié
        avant d'avoir lancé generate_og_images.py reste partageable."""
        nom = nom_image_og(self.id, lang)
        if (OG_DOSSIER / nom).exists():
            return f"{base}/static/og/{nom}", True
        return f"{base}/static/qeerah-logo.png", False


def _date(v: str) -> date:
    return date.fromisoformat(v)


def charger(dossier: Path = CONTENU) -> "list[Article]":
    """Lit tous les articles publiés, du plus récent au plus ancien.

    Un dossier illisible n'arrête pas le démarrage du site : il est signalé et
    ignoré. Les tests, eux, échouent dessus (cf. test_blog_articles.py).
    """
    articles: list[Article] = []
    if not dossier.is_dir():
        return articles
    for d in sorted(p for p in dossier.iterdir() if p.is_dir()):
        try:
            a = _charger_un(d)
        except Exception as e:  # pragma: no cover - filet au démarrage
            print(f"[blog] article '{d.name}' ignoré : {e}")
            continue
        if not a.brouillon:
            articles.append(a)
    articles.sort(key=lambda a: (a.publie, a.id), reverse=True)
    return articles


def _charger_un(d: Path) -> Article:
    meta = json.loads((d / "article.json").read_text(encoding="utf-8"))
    corps = {}
    for lang in LANGUES_REDIGEES:
        f = d / f"{lang}.html"
        if f.exists():
            corps[lang] = f.read_text(encoding="utf-8")
    return Article(
        id=d.name,
        requete=meta["requete"],
        intention=meta.get("intention", ""),
        publie=_date(meta["publie"]),
        maj=_date(meta.get("maj") or meta["publie"]),
        lecture_min=int(meta["lecture_min"]),
        cta=meta["cta"],
        lies=list(meta.get("lies", [])),
        sources=list(meta.get("sources", [])),
        langues=meta["langues"],
        corps=corps,
        schema=meta.get("schema", ""),
        brouillon=bool(meta.get("brouillon", False)),
        dossier=d,
    )


# ── Contrôle qualité ─────────────────────────────────────────────────────────
def _texte(fragment: str) -> str:
    return _html.unescape(re.sub(r"<[^>]+>", " ", fragment))


def mots(fragment: str) -> int:
    return len(_texte(fragment).split())


def titre_balise(titre: str) -> str:
    """<title> : le titre, suivi de la marque s'il reste la place."""
    return titre + SUFFIXE_TITRE if len(titre + SUFFIXE_TITRE) <= TITRE_MAX else titre


def controler(articles: "list[Article]") -> "list[str]":
    """Tout ce que la checklist SEO/GEO exige d'un article. Vide = conforme."""
    pb: list[str] = []
    ids = {a.id for a in articles}
    slugs: dict[str, set] = {l: set() for l in LANGS}
    for a in articles:
        p = f"[{a.id}]"
        if a.cta not in CTA:
            pb.append(f"{p} cta inconnu : {a.cta}")
        for l in a.lies:
            if l not in ids:
                pb.append(f"{p} article lié introuvable : {l}")
            if l == a.id:
                pb.append(f"{p} se lie à lui-même")
        if not a.sources:
            pb.append(f"{p} aucune source citée")
        nb_faq = None
        for lang in LANGUES_REDIGEES:
            q = f"{p}[{lang}]"
            m = a.langues.get(lang)
            if not m:
                pb.append(f"{q} métadonnées absentes")
                continue
            corps = a.corps.get(lang)
            if not corps:
                pb.append(f"{q} fichier {lang}.html absent")
                continue
            for clef in ("slug", "titre", "h1", "description", "chapo", "categorie", "faq"):
                if not m.get(clef):
                    pb.append(f"{q} champ vide : {clef}")
            if not _SLUG.match(m.get("slug", "")):
                pb.append(f"{q} slug invalide : {m.get('slug')}")
            if len(m.get("titre", "")) > TITRE_MAX:
                pb.append(f"{q} titre > {TITRE_MAX} car. ({len(m['titre'])})")
            n = len(m.get("description", ""))
            if not DESCRIPTION_MIN <= n <= DESCRIPTION_MAX:
                pb.append(f"{q} description hors {DESCRIPTION_MIN}-{DESCRIPTION_MAX} car. ({n})")
            if "<h1" in corps.lower():
                pb.append(f"{q} le corps contient un <h1> (un seul par page : le titre)")
            h2 = _H2.findall(corps)
            if len(h2) < 3:
                pb.append(f"{q} moins de 3 <h2 id=...> (sommaire trop maigre)")
            ids_h2 = [i for i, _ in h2]
            if len(ids_h2) != len(set(ids_h2)):
                pb.append(f"{q} ancres <h2> en double")
            if re.search(r"<h2(?![^>]*\bid=)", corps):
                pb.append(f"{q} <h2> sans id : absent du sommaire")
            for g in _LIEN_GUIDE.findall(corps):
                if g not in ids:
                    pb.append(f"{q} lien guide:{g} vers un article inexistant")
            internes = len(re.findall(r'href="(?:/|guide:)', corps)) + len(a.lies)
            if internes < 2:
                pb.append(f"{q} moins de 2 liens internes")
            pb.extend(f"{q} {e}" for e in _controler_schema(a, m, corps))
            if nb_faq is None:
                nb_faq = len(m.get("faq", []))
            elif len(m.get("faq", [])) != nb_faq:
                pb.append(f"{q} FAQ de longueur différente du français")
        for lang in LANGS:
            if source(lang) in a.langues:
                s = a.meta(lang)["slug"]
                if s in slugs[lang]:
                    pb.append(f"[{a.id}][{lang}] slug déjà utilisé : {s}")
                slugs[lang].add(s)
        if "fr" in a.corps:
            n = mots(a.corps["fr"])
            if not MOTS_FR_MIN <= n <= MOTS_FR_MAX:
                pb.append(f"{p}[fr] {n} mots, attendu {MOTS_FR_MIN}-{MOTS_FR_MAX}")
    return pb


# ── Rendu ────────────────────────────────────────────────────────────────────
_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    autoescape=jinja2.select_autoescape(["html"]),
)


def _date_lisible(d: date, lang: str) -> str:
    ui = UI[source(lang)]
    return ui["date"].format(j=d.day, m=ui["mois"][d.month - 1], a=d.year)


def _json_ld(obj: dict) -> str:
    # « </ » fermerait la balise <script> au milieu d'une chaîne.
    return json.dumps(obj, ensure_ascii=False, indent=2).replace("</", "<\\/")


def _jsonld_article(a: Article, lang: str, base: str) -> str:
    m = a.meta(lang)
    url = base + a.chemin(lang)
    org = {"@type": "Organization", "@id": f"{base}/#organization", "name": "Qeerah",
           "url": f"{base}/",
           "logo": {"@type": "ImageObject", "url": f"{base}/static/qeerah-logo.png"}}
    accueil = base + _hp.chemin_langue(lang, "/")
    blog = base + _hp.chemin_langue(lang, "/blog")
    graphe = [
        {
            "@type": "Article",
            "headline": m["h1"],
            "description": m["description"],
            "image": a.image(lang, base)[0],
            "author": org,
            "publisher": org,
            "datePublished": a.publie.isoformat(),
            "dateModified": a.maj.isoformat(),
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "inLanguage": _hp.HTML_LANG[lang],
            "about": {"@type": "Thing", "name": "TikTok Shop"},
            "citation": [s["url"] for s in a.sources],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": UI[source(lang)]["accueil"], "item": accueil},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": blog},
                {"@type": "ListItem", "position": 3, "name": m["h1"], "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": f["r"]}}
                for f in m["faq"]
            ],
        },
    ]
    return _json_ld({"@context": "https://schema.org", "@graph": graphe})


def _corps(a: Article, lang: str, par_id: "dict[str, Article]") -> str:
    """Fragment de la langue, liens « guide:<id> » résolus dans cette langue."""
    def repl(m: re.Match) -> str:
        cible = par_id.get(m.group(1))
        return f'href="{cible.chemin(lang)}"' if cible else 'href="/blog"'
    corps = _LIEN_GUIDE.sub(repl, a.corps[source(lang)])
    if _MARQUEUR_SCHEMA in corps and a.schema in SCHEMAS:
        corps = corps.replace(_MARQUEUR_SCHEMA, schema_html(a, lang), 1)
    return corps


# ── Schémas ──────────────────────────────────────────────────────────────────
# Dessinés en SVG dans la page, pas en image : quelques centaines d'octets,
# nets à toutes les tailles, et leur texte est lisible par Google et par les
# IA. Les étiquettes viennent de article.json (clef « schema » de chaque
# langue) : un schéma se traduit comme le reste de l'article.
#
# viewBox de 480 de large : sur un téléphone (≈ 340 px utiles), un texte en
# 15 reste lisible à ≈ 11 px.
_POLICE_SVG = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif"
_NAVY, _ACCENT, _OR, _GRIS = "#1F3A70", "#2563EB", "#D4AF37", "#5B6472"


def _t(s: str) -> str:
    return _html.escape(s, quote=True)


def _lignes(texte: str, max_car: int) -> "list[str]":
    lignes, ligne = [], ""
    for mot in texte.split():
        if len(f"{ligne} {mot}".strip()) <= max_car:
            ligne = f"{ligne} {mot}".strip()
        else:
            lignes.append(ligne)
            ligne = mot
    return lignes + [ligne]


def _svg_entonnoir(etiquettes: "list[str]", notes: "list[str]") -> "tuple[int, str]":
    """Cinq étages qui rétrécissent ; entre deux étages, le taux qui les relie."""
    couleurs = [_NAVY, "#24488C", "#2A56A8", _ACCENT, _OR]
    h, ecart, y, out = 38, 26, 10, []
    for i, etiquette in enumerate(etiquettes):
        larg = 440 - i * 60
        x = (480 - larg) / 2
        out.append(f'<rect x="{x}" y="{y}" width="{larg}" height="{h}" rx="8" fill="{couleurs[i]}"/>')
        texte = _NAVY if i == len(etiquettes) - 1 else "#fff"
        out.append(f'<text x="240" y="{y + h / 2}" text-anchor="middle" dominant-baseline="central" '
                   f'font-size="16" font-weight="700" fill="{texte}">{_t(etiquette)}</text>')
        y += h
        if i < len(notes):
            out.append(f'<text x="240" y="{y + ecart / 2}" text-anchor="middle" dominant-baseline="central" '
                       f'font-size="14" fill="{_GRIS}">↓ {_t(notes[i])}</text>')
            y += ecart
    return y + 10, "".join(out)


def _svg_couches(etiquettes: "list[str]", notes: "list[str]") -> "tuple[int, str]":
    """Quatre couches empilées, réunies par une accolade sur une même promesse."""
    couleurs = [_NAVY, "#24488C", "#2A56A8", _ACCENT]
    h, ecart, y0, out = 44, 8, 10, []
    for i, etiquette in enumerate(etiquettes):
        y = y0 + i * (h + ecart)
        out.append(f'<rect x="10" y="{y}" width="300" height="{h}" rx="8" fill="{couleurs[i]}"/>')
        out.append(f'<text x="28" y="{y + h / 2}" dominant-baseline="central" font-size="15" '
                   f'font-weight="700" fill="#fff">{i + 1}. {_t(etiquette)}</text>')
    bas = y0 + len(etiquettes) * (h + ecart) - ecart
    milieu = (y0 + bas) / 2
    out.append(f'<path d="M322 {y0} q12 0 12 12 v{milieu - y0 - 24} q0 12 10 12 q-10 0 -10 12 '
               f'v{bas - milieu - 24} q0 12 -12 12" fill="none" stroke="{_OR}" stroke-width="3"/>')
    lignes = _lignes(notes[0], 14) if notes else []
    for j, ligne in enumerate(lignes):
        y = milieu + (j - (len(lignes) - 1) / 2) * 19
        out.append(f'<text x="356" y="{y}" dominant-baseline="central" font-size="15" '
                   f'font-weight="700" fill="{_NAVY}">{_t(ligne)}</text>')
    return bas + 10, "".join(out)


def _svg_leviers(etiquettes: "list[str]", notes: "list[str]") -> "tuple[int, str]":
    """Cinq leviers numérotés, et la règle qui les gouverne en dessous."""
    larg, ecart, x0, out = 84, 8, 14, []
    for i, etiquette in enumerate(etiquettes):
        x = x0 + i * (larg + ecart)
        cx = x + larg / 2
        out.append(f'<rect x="{x}" y="10" width="{larg}" height="88" rx="10" fill="{_NAVY}"/>')
        out.append(f'<circle cx="{cx}" cy="38" r="15" fill="{_OR}"/>')
        out.append(f'<text x="{cx}" y="38" text-anchor="middle" dominant-baseline="central" '
                   f'font-size="15" font-weight="800" fill="{_NAVY}">{i + 1}</text>')
        out.append(f'<text x="{cx}" y="76" text-anchor="middle" dominant-baseline="central" '
                   f'font-size="14" font-weight="700" fill="#fff">{_t(etiquette)}</text>')
    y = 118
    for ligne in (_lignes(notes[0], 52) if notes else []):
        out.append(f'<text x="240" y="{y}" text-anchor="middle" dominant-baseline="central" '
                   f'font-size="14" font-weight="600" fill="{_NAVY}">{_t(ligne)}</text>')
        y += 19
    return y, "".join(out)


# type → (fonction, nombre d'étiquettes, nombre de notes)
SCHEMAS = {
    "entonnoir": (_svg_entonnoir, 5, 4),
    "couches": (_svg_couches, 4, 1),
    "leviers": (_svg_leviers, 5, 1),
}


def schema_html(a: Article, lang: str) -> str:
    s = a.meta(lang)["schema"]
    dessin, _n, _k = SCHEMAS[a.schema]
    hauteur, contenu = dessin(s["etiquettes"], s.get("notes", []))
    ident = f"schema-{a.id}"
    return (
        f'<figure class="schema">'
        f'<svg viewBox="0 0 480 {hauteur:.0f}" role="img" aria-labelledby="{ident}" '
        f'font-family="{_POLICE_SVG}" xmlns="http://www.w3.org/2000/svg">'
        f'<title id="{ident}">{_t(s["titre"])}</title>{contenu}</svg>'
        f'<figcaption>{_t(s["legende"])}</figcaption></figure>'
    )


def _controler_schema(a: Article, m: dict, corps: str) -> "list[str]":
    pb: list[str] = []
    marque = _MARQUEUR_SCHEMA in corps
    if not a.schema:
        if marque:
            pb.append("marqueur <!--SCHEMA--> sans « schema » dans article.json")
        return pb
    if a.schema not in SCHEMAS:
        return [f"schéma inconnu : {a.schema}"]
    if not marque:
        pb.append("schéma déclaré mais pas de marqueur <!--SCHEMA--> dans le corps")
    s = m.get("schema") or {}
    _f, n, k = SCHEMAS[a.schema]
    if len(s.get("etiquettes", [])) != n:
        pb.append(f"schéma : {n} étiquettes attendues")
    if len(s.get("notes", [])) != k:
        pb.append(f"schéma : {k} notes attendues")
    if not s.get("titre") or not s.get("legende"):
        pb.append("schéma : titre ou légende manquant")
    return pb


def rendre(a: Article, lang: str, base: str, articles: "list[Article]") -> str:
    par_id = {x.id: x for x in articles}
    m = a.meta(lang)
    ui = UI[source(lang)]
    cta = CTA[a.cta]
    corps = _corps(a, lang, par_id)
    sommaire = [(i, _texte(t).strip()) for i, t in _H2.findall(corps)]
    lies = [par_id[i] for i in a.lies if i in par_id]
    alternates = [(_hp.HTML_LANG[l], base + a.chemin(l)) for l in LANGS]
    alternates.append(("x-default", base + a.chemin(DEFAULT)))
    autres = [(_hp.HTML_LANG[l], _hp.LANG_LABEL[l], a.chemin(l))
              for l in LANGS if l != lang]
    image, image_dediee = a.image(lang, base)
    return _ENV.get_template("blog_article.html").render(
        image=image,
        image_dediee=image_dediee,
        og_largeur=OG_LARGEUR,
        og_hauteur=OG_HAUTEUR,
        lang=lang,
        html_lang=_hp.HTML_LANG[lang],
        og_locale=_hp.OG_LOCALE[lang],
        ui=ui,
        m=m,
        titre=titre_balise(m["titre"]),
        url=base + a.chemin(lang),
        base=base,
        alternates=alternates,
        autres_langues=autres,
        jsonld=_markup(_jsonld_article(a, lang, base)),
        corps=_markup(corps),
        sommaire=sommaire,
        publie=a.publie.isoformat(),
        maj=a.maj.isoformat(),
        maj_lisible=_date_lisible(a.maj, lang),
        lecture=ui["lecture"].format(n=a.lecture_min),
        cta_titre=cta[source(lang)][0],
        cta_texte=cta[source(lang)][1],
        cta_bouton=cta[source(lang)][2],
        cta_chemin=cta["chemin"],
        lies=[(x.meta(lang)["h1"], x.chemin(lang), x.meta(lang)["description"]) for x in lies],
        sources=a.sources,
    )


def _markup(s: str) -> markupsafe.Markup:
    """Contenu écrit par nous (fragments du dépôt, JSON-LD) : pas d'échappement."""
    return markupsafe.Markup(s)


def construire(base: str, articles: "list[Article] | None" = None) -> "dict[str, tuple[str, str]]":
    """Toutes les pages, une fois, au démarrage : {chemin: (langue, html)}."""
    articles = charger() if articles is None else articles
    pages: dict[str, tuple[str, str]] = {}
    for a in articles:
        for lang in LANGS:
            if source(lang) not in a.corps:
                continue
            pages[a.chemin(lang)] = (lang, rendre(a, lang, base, articles))
    return pages


# ── Ce que les autres pages en tirent ────────────────────────────────────────
def cartes(lang: str, articles: "list[Article]") -> str:
    """Cartes pour la grille de /blog, au style des cartes existantes."""
    ui = UI[source(lang)]
    morceaux = []
    for a in articles:
        if source(lang) not in a.corps:
            continue
        m = a.meta(lang)
        e = _html.escape
        morceaux.append(
            f'      <div class="article-card" onclick="window.location.href=\'{a.chemin(lang)}\'">\n'
            f'        <div class="article-header">\n'
            f'          <span class="article-category">{e(m["categorie"])}</span>\n'
            f'          <h3>{e(m["h1"])}</h3>\n'
            f'          <div class="article-meta">\n'
            f'            <span>📅 {e(_date_lisible(a.maj, lang))}</span>\n'
            f'            <span>⏱️ {e(ui["lecture"].format(n=a.lecture_min))}</span>\n'
            f'          </div>\n'
            f'        </div>\n'
            f'        <div class="article-body">\n'
            f'          <p class="article-excerpt">{e(m["description"])}</p>\n'
            f'          <a href="{a.chemin(lang)}" class="read-more">{e(ui["lire"])}</a>\n'
            f'        </div>\n'
            f'      </div>\n'
        )
    return "".join(morceaux)


def jsonld_liste(lang: str, base: str, articles: "list[Article]") -> str:
    """ItemList des guides, pour le <head> de /blog."""
    elements = [
        {"@type": "ListItem", "position": i + 1, "url": base + a.chemin(lang),
         "name": a.meta(lang)["h1"]}
        for i, a in enumerate(x for x in articles if source(lang) in x.corps)
    ]
    if not elements:
        return ""
    obj = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": elements}
    return f'<script type="application/ld+json">\n{_json_ld(obj)}\n  </script>'


def entrees_sitemap(articles: "list[Article]") -> "list[tuple[str, str]]":
    """(chemin, lastmod) de chaque page d'article, toutes langues."""
    return [(a.chemin(l), a.maj.isoformat())
            for a in articles for l in LANGS if source(l) in a.corps]


def lignes_llms(base: str, articles: "list[Article]") -> str:
    """Section « Guides pratiques » de /llms.txt (version française)."""
    if not articles:
        return ""
    lignes = "".join(
        f"- [{a.meta('fr')['h1']}]({base}{a.chemin('fr')}) : {a.meta('fr')['description']}\n"
        for a in articles if "fr" in a.corps
    )
    return (
        "## Guides pratiques TikTok Shop\n"
        "Chaque guide répond à sa question dès le premier paragraphe et cite ses "
        "sources. Il existe dans les huit langues du site (balises hreflang).\n"
        + lignes + "\n"
    )
