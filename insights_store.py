"""
Base de connaissances « structures gagnantes » (Gold / Agency).

À CHAQUE analyse vidéo on enregistre — de façon 100% ANONYMISÉE (aucune donnée
personnelle, ni email, ni IP, ni id utilisateur) — un « insight » :
catégorie produit, nom produit, prix, score global, type de hook, exemples de
hook et (si dispo) script de vente premium.

Quand une nouvelle analyse obtient un score < 75 ET que l'utilisateur est sur un
plan habilité (gold / agency / beta / admin), on interroge cette base pour
remonter les accroches / scripts qui ont obtenu > 75 sur un produit similaire au
même budget, afin de proposer une structure déjà éprouvée.

La base se remplit NATURELLEMENT avec l'usage — aucun pré-remplissage.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from supabase_client import supabase

# Plans habilités à voir les « structures gagnantes ».
WINNING_TIERS = {"gold", "agency", "beta", "admin"}

# Seuil : en dessous on propose des structures gagnantes ; au-dessus on considère
# que la vidéo n'en a pas besoin (et elle alimente elle-même la base).
WINNING_SCORE_THRESHOLD = 75

# Regroupement « similarité produit » par mots-clés (proche de PEAK_SEASONS).
_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "beaute": [
        "serum", "sérum", "creme", "crème", "skincare", "peau", "visage",
        "maquillage", "makeup", "mascara", "rouge", "soin", "hydratant",
        "masque", "cils", "ongle", "lèvre", "levre", "teint", "fond de teint",
    ],
    "parfum": ["parfum", "fragrance", "eau de toilette", "cologne"],
    "cheveux": [
        "cheveux", "shampoing", "lissage", "boucleur", "brosse", "perruque",
        "extension", "lisseur", "sèche-cheveux", "seche-cheveux",
    ],
    "fitness": [
        "fitness", "sport", "muscu", "musculation", "protéine", "proteine",
        "yoga", "minceur", "gym", "abdo", "haltère", "haltere", "elastique",
    ],
    "mode": [
        "robe", "jean", "tshirt", "t-shirt", "vetement", "vêtement",
        "chaussure", "basket", "sac", "veste", "pull", "legging", "mode",
        "lingerie", "maillot", "manteau",
    ],
    "bijoux": [
        "bijou", "collier", "bague", "bracelet", "boucle", "montre",
        "pendentif", "chaine", "chaîne",
    ],
    "maison": [
        "maison", "cuisine", "déco", "deco", "rangement", "lampe", "coussin",
        "tapis", "ustensile", "organisateur", "bougie", "linge",
    ],
    "tech": [
        "écouteur", "ecouteur", "casque", "chargeur", "câble", "cable",
        "gadget", "led", "enceinte", "support", "téléphone", "telephone",
        "powerbank", "montre connectée", "montre connectee", "drone", "camera",
        "caméra",
    ],
    "enfant": [
        "jouet", "enfant", "bébé", "bebe", "peluche", "jeu", "puériculture",
        "puericulture",
    ],
    "animaux": [
        "chien", "chat", "animal", "animaux", "croquette", "laisse", "litière",
        "litiere",
    ],
    "sante": [
        "complément", "complement", "vitamine", "collagène", "collagene",
        "probiotique", "santé", "sante", "sommeil", "magnésium", "magnesium",
    ],
}


def categorize(product_name: Optional[str]) -> str:
    """Déduit une catégorie de regroupement à partir du nom de produit."""
    p = (product_name or "").lower()
    for cat, kws in _CATEGORY_KEYWORDS.items():
        if any(kw in p for kw in kws):
            return cat
    return "autre"


def _price_num(price_str) -> float:
    """Extrait un montant numérique d'une chaîne de prix (ex: '29,90 €' → 29.9)."""
    m = re.search(r"(\d+(?:[.,]\d+)?)", str(price_str or ""))
    return float(m.group(1).replace(",", ".")) if m else 0.0


def save_insight(
    result: dict,
    product: Optional[str] = None,
    price: Optional[str] = None,
) -> None:
    """
    Enregistre (anonymisé) l'insight d'une analyse pour nourrir la base.
    Silencieux en cas d'erreur — ne doit jamais casser le flux d'analyse.
    """
    if not supabase or not isinstance(result, dict):
        return
    try:
        detection = result.get("detection") or {}
        produit = (product or detection.get("produit") or "").strip()[:120]
        if not produit:
            return

        score = result.get("score_global")
        if not isinstance(score, (int, float)) or score <= 0:
            return

        prix = _price_num(price or detection.get("prix_estime"))
        hooks = result.get("recommendations_hooks") or {}
        premium = result.get("strategie_conversion_premium") or {}
        script_obj = premium.get("script_tiktok") if isinstance(premium, dict) else None

        row = {
            "category": categorize(produit),
            "product": produit,
            "price": round(prix, 2) if prix > 0 else None,
            "score_global": int(round(score)),
            "hook_type": (detection.get("hook_type") or hooks.get("hook_type_propose") or "")[:120] or None,
            "hook_examples": (hooks.get("exemples_concrets") or [])[:3],
            "script": script_obj if isinstance(script_obj, dict) else None,
            "verdict": (result.get("verdict") or "")[:600] or None,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        supabase.table("analyzed_insights").insert(row).execute()
    except Exception as e:  # pragma: no cover - best effort
        print(f"insights_store.save_insight error: {e}")


def get_winning_similar(
    product: Optional[str],
    price=None,
    category: Optional[str] = None,
    min_score: int = WINNING_SCORE_THRESHOLD,
    limit: int = 3,
) -> list[dict]:
    """
    Remonte les meilleures structures (score > min_score) sur la même catégorie,
    dans une fourchette de prix ±30%, en priorisant les produits au nom proche.
    """
    if not supabase:
        return []
    try:
        cat = category or categorize(product)
        prix = _price_num(price)

        resp = (
            supabase.table("analyzed_insights")
            .select("*")
            .eq("category", cat)
            .gte("score_global", min_score)
            .order("score_global", desc=True)
            .limit(60)
            .execute()
        )
        rows = resp.data or []
        if not rows:
            return []

        # Fourchette de prix ±30% (on garde les entrées sans prix par défaut).
        if prix > 0:
            lo, hi = prix * 0.7, prix * 1.3
            banded = [
                r for r in rows
                if r.get("price") is None or (lo <= float(r["price"]) <= hi)
            ]
            if banded:
                rows = banded

        # Priorité aux noms de produits qui partagent le plus de mots.
        p_words = set((product or "").lower().split())

        def _rank(r: dict):
            shared = len(p_words & set((r.get("product") or "").lower().split()))
            return (shared, r.get("score_global", 0))

        rows.sort(key=_rank, reverse=True)

        out: list[dict] = []
        for r in rows[:limit]:
            out.append({
                "product": r.get("product"),
                "score": r.get("score_global"),
                "hook_type": r.get("hook_type"),
                "hook_examples": (r.get("hook_examples") or [])[:3],
                "script": r.get("script"),
                "price": r.get("price"),
            })
        return out
    except Exception as e:  # pragma: no cover - best effort
        print(f"insights_store.get_winning_similar error: {e}")
        return []


def build_winning_payload(
    result: dict,
    tier: str,
    product: Optional[str] = None,
    price: Optional[str] = None,
) -> Optional[dict]:
    """
    Construit le payload `structures_gagnantes` à injecter dans le résultat
    quand : tier habilité ET score < seuil ET des structures gagnantes existent.
    """
    if (tier or "free").lower() not in WINNING_TIERS:
        return None
    score = result.get("score_global")
    if not isinstance(score, (int, float)) or score >= WINNING_SCORE_THRESHOLD:
        return None

    detection = result.get("detection") or {}
    prod = product or detection.get("produit") or ""
    prc = price or detection.get("prix_estime")
    winners = get_winning_similar(prod, prc)
    if not winners:
        return None

    return {
        "titre": "🏆 Les structures qui ont mieux fonctionné",
        "intro": (
            f"Ta vidéo a obtenu {int(round(score))}/100. Voici des accroches et scripts "
            "qui ont dépassé 75 sur des produits similaires au même budget. "
            "Inspire-toi de cette structure déjà éprouvée et refais ta vidéo."
        ),
        "items": winners,
    }
