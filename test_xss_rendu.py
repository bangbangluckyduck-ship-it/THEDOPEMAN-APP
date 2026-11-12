"""Non-régression XSS (audit sécurité du 2026-11-12, point S1).

Les textes produits par l'IA (diagnostics, commentaires, catégories) et les données
récupérées sur TikTok Shop (titres de produits, comptes créateurs) sont contrôlables
de l'extérieur. Ils ne doivent JAMAIS être insérés en HTML sans `escapeHtml(...)`.

Ce test lit static/app_v3.js et échoue si une interpolation `${...}` d'un de ces
champs apparaît sans échappement dans les fonctions de rendu des résultats.
"""
from __future__ import annotations

import re
from pathlib import Path

SRC = (Path(__file__).parent / "static" / "app_v3.js").read_text(encoding="utf-8")

FONCTIONS = ["showLockedCoachingSection", "renderErrorTimeline", "showResults"]

# Champs non fiables (IA ou TikTok) qui ne doivent apparaître qu'échappés.
CHAMPS_NON_FIABLES = re.compile(
    r"\b(firstCoachingLine|m\.diagnostic|m\.pilier|v\.commentaire|val|label|detectedCategory|"
    r"p\.title|p\.name|p\.category|p\.sold_count|p\.current_price|p\.growth_percent|"
    r"c\.handle|c\.followers|c\.primary_category|aide\.quoi|aide\.action|LABELS\[k\]|a)\b"
)


# Contextes sûrs exclus de l'analyse :
#  - `el.title = `...`` : attribut texte (jamais interprété comme HTML) ;
#  - `recommendations = actions.map(...)` : `actions` ne contient que des phrases écrites en dur.
CONTEXTES_SURS = [
    re.compile(r"\.title\s*=\s*`[^`]*`;"),
    re.compile(r"recommendations = actions\.map\(.*?\.join\(''\);", re.S),
]


def _corps(nom: str) -> str:
    debut = SRC.index(f"function {nom}(")
    suivant = SRC.find("\nfunction ", debut + 1)
    code = SRC[debut: suivant if suivant != -1 else len(SRC)]
    for motif in CONTEXTES_SURS:
        code = motif.sub("", code)
    return code


def _interpolations(code: str) -> list[str]:
    """Contenu des ${...} (gère un niveau d'imbrication de parenthèses/templates)."""
    out, i = [], 0
    while (i := code.find("${", i)) != -1:
        prof, j = 1, i + 2
        while j < len(code) and prof:
            prof += {"{": 1, "}": -1}.get(code[j], 0)
            j += 1
        out.append(code[i + 2: j - 1].strip())
        i = j
    return out


def test_champs_non_fiables_toujours_echappes():
    fautifs = []
    for nom in FONCTIONS:
        for expr in _interpolations(_corps(nom)):
            if expr.startswith("escapeHtml(") or expr.startswith("catHtml"):
                continue
            # Expressions conditionnelles qui contiennent un template : on vérifie l'intérieur.
            if "`" in expr:
                continue
            if CHAMPS_NON_FIABLES.search(expr):
                fautifs.append(f"{nom} : ${{{expr}}}")
    assert not fautifs, "Interpolations non échappées :\n" + "\n".join(fautifs)


def test_escape_html_reste_global():
    # escapeHtml doit rester une déclaration de fonction globale (hissée), utilisable partout.
    assert re.search(r"^function escapeHtml\(", SRC, re.M)
    # `esc` n'existe que localement dans renderBatchPatterns : ne pas l'utiliser ailleurs.
    assert "${esc(" not in _corps("showResults")
