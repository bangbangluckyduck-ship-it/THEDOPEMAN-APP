"""
INTELLIGENCE PRODUIT — scoring déterministe du potentiel viral d'un PRODUIT.

Fondement (décodage de ~180 vidéos deals TikTok Shop, 6 comptes US+FR) : sur
CHAQUE compte, les flops utilisent les mêmes scripts que les cartons. Le format
est un PLANCHER de qualité ; la variance de reach vient d'abord du PRODUIT
(catégorie satisfaisante / utile / anxiogène-sécurité / astuce / prix waouh),
puis de la 1re seconde visuelle, de la loterie algo et du volume.

Ce module ne remplace pas le LLM : il produit un signal DÉTERMINISTE (comme le
momentum saisonnier) injecté dans la synthèse, pour que l'analyse et le coaching
pondèrent le potentiel produit AU-DESSUS des dimensions purement textuelles.
Aucune dépendance externe → testable en isolation, jamais bloquant.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Optional


def _norm(s: str) -> str:
    """minuscule + sans accents, pour un matching robuste des mots-clés."""
    s = (s or "").lower().strip()
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# ── CATÉGORIES DE POTENTIEL (ordonnées par reach observé dans le corpus) ───────
# Chaque catégorie : (score de base /100, mots-clés). Le score de base reflète le
# reach relatif observé, PAS une garantie : c'est un a priori de potentiel produit.
_CATEGORIES: list[tuple[str, int, str, tuple[str, ...]]] = [
    # id, base_score, libellé, mots-clés (normalisés)
    ("anxiogene_securite", 86, "anxiogène / sécurité (peur = reach max)", (
        "securite", "surveillance", "camera", "incendie", "anti-feu", "anti feu",
        "detecteur", "alarme", "serrure", "ethylotest", "demarreur", "extincteur",
        "protection", "secours", "urgence",
    )),
    ("astuce_maline", 80, "astuce maline / hack maison (très partageable FR)", (
        "moustiquaire", "sans percage", "anti vis-a-vis", "anti vis a vis", "store",
        "voilage", "rangement", "organiseur", "gain de place", "pliable", "extensible",
        "astuce", "adhesif", "sans trou",
    )),
    ("satisfaisant_demo", 73, "satisfaisant / démo visuelle (avant-après)", (
        "nettoyeur", "detachant", "aspirateur", "shampouineuse", "vapeur", "tapis",
        "litiere", "laveur", "nettoyage", "detartrage", "vitre", "lave-vitre",
    )),
    ("prix_waouh_marque", 76, "prix waouh sur marque connue (ancrage fort)", (
        "ninja", "shark", "philips", "moulinex", "dyson", "ps5", "iphone", "samsung",
        "kukirine", "nespresso", "bissell", "dreame", "tv", "qled", "trottinette",
        "airfryer", "air fryer", "slushi", "creami", "crispi",
    )),
    ("utile_quotidien", 66, "utile au quotidien (universel)", (
        "chargeur", "power bank", "batterie externe", "carplay", "support",
        "ventilateur", "oreiller", "refroidisseur", "gourde", "blender", "diffuseur",
        "cable", "ecouteurs", "gonfleur",
    )),
]

# Catégories saturées : le corpus note des flops récurrents sur des produits
# redondants « énième X sans marque forte ». On flague pour tempérer le score.
_SATURATED_KEYWORDS: tuple[str, ...] = (
    "coque", "gourde", "anneau lumineux", "ring light", "cable usb",
    "pop socket", "popsocket", "support telephone",
)

# Marques connues = objection prix désamorcée + légitimité (booster conversion FR).
_KNOWN_BRANDS: tuple[str, ...] = (
    "ninja", "shark", "philips", "moulinex", "dyson", "bissell", "dreame",
    "nespresso", "samsung", "apple", "iphone", "ps5", "kukirine", "carrefour",
)


def _price_band(price: Optional[str]) -> tuple[str, float, str]:
    """(libellé, multiplicateur viral, facteur_prix) à partir d'un prix libre.
    Reprend les paliers de hooks_db.price_factors (sweet spot 15-40€)."""
    if not price:
        return ("inconnu", 1.0, "non détecté")
    m = re.search(r"(\d+(?:[.,]\d+)?)", str(price))
    if not m:
        return ("inconnu", 1.0, "non détecté")
    try:
        val = float(m.group(1).replace(",", "."))
    except ValueError:
        return ("inconnu", 1.0, "non détecté")
    if val < 10:
        return ("très bas (<10€)", 0.8, "très bas <15€")
    if val <= 40:
        return ("optimal (15-40€)", 1.3, "bon 15-40€")
    if val <= 100:
        return ("milieu de gamme (40-100€)", 1.1, "élevé 40-100€")
    return ("premium (100€+)", 0.7, "premium 100€+")


def score_product(product_name: Optional[str], price: Optional[str] = None) -> dict:
    """Évalue le potentiel viral du PRODUIT (déterministe, 0-100).

    Retour :
      {
        "potential_score": int 0-100,
        "category_id": str, "category_label": str,
        "price_band": str, "facteur_prix": str, "viral_multiplier": float,
        "is_branded": bool, "saturation_risk": "faible|moyen|élevé",
        "levier_dominant": str,   # produit vs script (toujours produit ici)
        "rationale": str,
      }
    """
    norm = _norm(product_name or "")

    # 1) Catégorie de potentiel : première correspondance par ordre de reach.
    cat_id, base, cat_label = "generique", 55, "générique / non catégorisé"
    if norm:
        for cid, cbase, clabel, keywords in _CATEGORIES:
            if any(k in norm for k in keywords):
                cat_id, base, cat_label = cid, cbase, clabel
                break

    # 2) Prix → multiplicateur.
    band_label, mult, facteur_prix = _price_band(price)

    # 3) Marque connue → bonus (légitimité + objection prix désamorcée).
    is_branded = any(b in norm for b in _KNOWN_BRANDS)
    brand_bonus = 6 if is_branded else 0

    # 4) Saturation → malus + drapeau.
    saturated = any(k in norm for k in _SATURATED_KEYWORDS) or (
        not is_branded and cat_id == "utile_quotidien"
    )
    if any(k in norm for k in _SATURATED_KEYWORDS):
        saturation_risk, sat_malus = "élevé", 18
    elif saturated:
        saturation_risk, sat_malus = "moyen", 8
    else:
        saturation_risk, sat_malus = "faible", 0

    # 5) Score final : base × multiplicateur prix (recentré) + bonus − malus.
    #    Le multiplicateur (0.7-1.3) module ±~15 % autour de la base.
    score = base * (0.85 + 0.15 * mult) + brand_bonus - sat_malus
    score = int(max(0, min(100, round(score))))

    rationale = (
        f"Produit classé « {cat_label} » (a priori de reach {base}/100). "
        f"Prix {band_label} → multiplicateur ×{mult}. "
        f"{'Marque connue (+légitimité). ' if is_branded else ''}"
        f"Risque de saturation : {saturation_risk}. "
        f"Rappel : le produit et la 1re seconde pèsent plus que le script."
    )

    return {
        "potential_score": score,
        "category_id": cat_id,
        "category_label": cat_label,
        "price_band": band_label,
        "facteur_prix": facteur_prix,
        "viral_multiplier": mult,
        "is_branded": is_branded,
        "saturation_risk": saturation_risk,
        "levier_dominant": "produit",
        "rationale": rationale,
    }


def format_for_prompt(product_name: Optional[str], price: Optional[str] = None) -> str:
    """Bloc texte déterministe à injecter dans la synthèse (comme le momentum)."""
    r = score_product(product_name, price)
    label = (product_name or "produit inconnu").strip() or "produit inconnu"
    return (
        "\n\n████████████████████████████████████████████████████████████████████████████████\n"
        "█  INTELLIGENCE PRODUIT — POTENTIEL VIRAL (signal déterministe, PRIORITAIRE)\n"
        "████████████████████████████████████████████████████████████████████████████████\n"
        f"Produit : « {label} »\n"
        f"➤ Score de potentiel PRODUIT : {r['potential_score']}/100 "
        f"(catégorie : {r['category_label']})\n"
        f"➤ Prix : {r['price_band']} — facteur {r['facteur_prix']} (×{r['viral_multiplier']})\n"
        f"➤ Marque connue : {'oui' if r['is_branded'] else 'non'} | "
        f"Risque saturation : {r['saturation_risk']}\n\n"
        "RÈGLES :\n"
        "  1. Ce score PRODUIT est un signal fort : intègre-le dans viral_potential et le verdict.\n"
        "  2. Si le potentiel produit est faible (<50) mais le script est bon, dis explicitement\n"
        "     que le script sécurise le plancher mais que le PRODUIT limite le plafond de reach.\n"
        "  3. Si le potentiel produit est élevé (≥75), encourage le VOLUME et le recyclage\n"
        "     multi-angles de ce produit gagnant.\n"
        "  4. Ne présente jamais un bon score comme une garantie de vues (loterie algo).\n"
        "████████████████████████████████████████████████████████████████████████████████"
    )
