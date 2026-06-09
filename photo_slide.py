"""
📸 Photo Slide Coach (feature premium GOLD / AGENCY / BETA / ADMIN).

À partir d'une image produit + (nature, prix, description), l'IA propose un plan
de carrousel TikTok Shop optimisé. Génération en **2 étapes streamées** (SSE) :

  ÉTAPE 1 — STRATÉGIE (vision pixtral-12b, ~15-25s) :
    type de slide recommandé, Hook (1ʳᵉ image), titre carrousel (+variantes), niche.
  ÉTAPE 2 — CONTENU (texte mistral-small, rapide ~8-15s) :
    plan slide par slide AVEC type de photo à prendre, CTA, description optimisée,
    hashtags, conseils saves.

L'utilisateur voit donc la stratégie + le hook AVANT que tout soit fini.

⚠️ ZONES ÉDITABLES : les blocs entre « ⬇️ ZONE ÉDITABLE … » et « ⬆️ FIN ZONE ÉDITABLE »
   (dans PHOTO_SLIDE_KNOWLEDGE) sont prévus pour que le product owner enrichisse l'IA
   (hooks gagnants, patterns de slides) SANS toucher au reste du code.
"""
from __future__ import annotations

import os
from typing import Optional

from analyzer import _mistral_call, _extract_json


# ════════════════════════════════════════════════════════════════════════════
# CONNAISSANCES PARTAGÉES (utilisées par les 2 étapes)
# ════════════════════════════════════════════════════════════════════════════
PHOTO_SLIDE_KNOWLEDGE = """Tu es un expert en stratégie de carrousels (« Photo Slides ») TikTok Shop.
Objectif d'un carrousel : maximiser le DWELL TIME (le swipe = signal algorithmique fort → « Pour Toi »),
inciter aux SAVES (format liste/fiche pratique = reach), et CONVERTIR vers le panier TikTok Shop.

# PROCESS DE VENTE OBLIGATOIRE (ordre impératif des slides)
ACCROCHE → PROBLÈME → SOLUTION → PRODUIT → CTA
- SLIDE 1 (ACCROCHE) : hook stop-scroll qui SOULÈVE LE PROBLÈME. ⚠️ LE PRODUIT N'APPARAÎT JAMAIS sur la slide 1.
- PROBLÈME : on enfonce la douleur / la frustration que vit le spectateur.
- SOLUTION : on présente comment c'est résolu (le produit entre en scène).
- PRODUIT : mise en valeur du produit (bénéfices, preuves, réassurance).
- CTA (dernière) : appel à l'action vers le panier jaune TikTok Shop, urgence + bénéfice clair.
Chaque étape du process doit apparaître dans le plan de slides, dans cet ordre.

# LES 3 STYLES DE SLIDES
## « quad_photo » — 4 photos divisées (grille 2x2)
4 quadrants (symptôme / problème / bénéfice / signe), texte centré. Idéal : listes de symptômes/signes,
bénéfices, top 4 caractéristiques, comparaisons. Niches : santé, beauté, fitness, éducation. 1 slide composite (parfois 2-3).
## « fond_blanc » — produit épuré + texte
Photo propre, fond blanc impeccable, typo soignée, minimaliste premium. Idéal : produit premium, listes
éducatives, conseils experts, listes de signes/erreurs. Niches : cosmétique premium, soins, conseils. 3-5 slides.
## « ia_cartoon » — personnage transformation (split screen)
Gauche : personnage avec problème (style IA/cartoon/anime, triste). Droite : transformé (heureux, bénéfices).
Idéal : avant/après, transformation, problème→solution, aspiration. Niches : fitness, cosmétique transformative,
compléments, lifestyle. 2-4 slides.

# RÈGLES
- Choisis le style selon l'IMAGE + niche + prix (sauf style imposé par l'utilisateur).
- Le Hook crée une tension/curiosité immédiate (jamais une description plate).
- Pour CHAQUE slide, précise le TYPE DE PHOTO À PRENDRE (cadrage, fond, angle, ce qu'on voit).
- FRANÇAIS PUR. Concret et actionnable.

# ⬇️⬇️⬇️ ZONE ÉDITABLE 1 — HOOKS GAGNANTS (à enrichir par le product owner) ⬇️⬇️⬇️
# Ajoute ici des patterns de hooks qui convertissent (par niche), formules, exemples réels.
# Exemples de départ :
# - « Les N signes que … (et personne ne te l'a dit) »
# - « Pourquoi ton/ta … [problème] (et la solution) »
# - « Arrête de … si tu veux … »
# ⬆️⬆️⬆️ FIN ZONE ÉDITABLE 1 ⬆️⬆️⬆️

# ⬇️⬇️⬇️ ZONE ÉDITABLE 2 — IDÉES DE SLIDES / ANGLES GAGNANTS (à enrichir) ⬇️⬇️⬇️
# Ajoute ici des structures de carrousels qui marchent, angles par niche, exemples de CTA.
# ⬆️⬆️⬆️ FIN ZONE ÉDITABLE 2 ⬆️⬆️⬆️
"""

_STRATEGY_OUTPUT = """# TA TÂCHE (ÉTAPE 1/2 — STRATÉGIE)
Analyse l'image + les infos et renvoie UNIQUEMENT ce JSON (rien d'autre) :
{
  "type_slide": {
    "style": "quad_photo | fond_blanc | ia_cartoon",
    "label": "Nom lisible du style en français",
    "justification": "1-2 phrases : pourquoi ce style pour CE produit."
  },
  "hook": "Texte du hook de la 1ʳᵉ slide (court, percutant).",
  "titre_carrousel": "Titre principal du carrousel.",
  "titre_variantes": ["variante 1", "variante 2"],
  "detected_niche": "Niche détectée."
}
"""

_CONTENT_OUTPUT = """# TA TÂCHE (ÉTAPE 2/2 — CONTENU)
On a déjà choisi la stratégie suivante :
- Style : {style} ({label})
- Hook (slide 1) : {hook}
- Titre du carrousel : {titre}
- Niche : {niche}

Produis maintenant le détail. Renvoie UNIQUEMENT ce JSON (rien d'autre) :
{{
  "slides": [
    {{
      "numero": 1,
      "type": "hook | value | cta",
      "texte": "Texte à afficher sur la slide.",
      "sous_texte": "Sous-texte optionnel (peut être vide).",
      "photo_a_prendre": "Photo PRÉCISE à shooter : cadrage, fond, angle, ce qu'on voit.",
      "emotion": "Émotion à transmettre.",
      "position_texte": "center | top | bottom"
    }}
  ],
  "cta": "Phrase de CTA de la dernière slide (vers le panier TikTok Shop).",
  "description_optimisee": "Description produit optimisée prête à coller (emojis, bénéfices ✨, CTA panier 🛒). 200-320 caractères.",
  "hashtags": ["2-3 tendances", "3-4 niche", "1-2 tiktokshop (max 8-10 total)"],
  "conseils_saves": ["Conseil 1 pour maximiser les sauvegardes.", "Conseil 2."]
}}
La slide 1 reprend le hook ci-dessus. La dernière slide est le CTA. Respecte le nb de slides typique du style.
"""


def _product_infos(product_name, price, currency, description, niche) -> str:
    infos = []
    if product_name: infos.append(f"- Nature / nom : {product_name}")
    if description:   infos.append(f"- Description : {description}")
    if price:         infos.append(f"- Prix : {price} {currency or 'EUR'}")
    if niche:         infos.append(f"- Niche : {niche}")
    return "Informations produit :\n" + "\n".join(infos) if infos else "Aucune info produit fournie."


# ════════════════════════════════════════════════════════════════════════════
# ÉTAPE 1 — STRATÉGIE (vision)
# ════════════════════════════════════════════════════════════════════════════
def generate_strategy(image_b64: str, product_name: Optional[str] = None,
                      price: Optional[str] = None, currency: str = "EUR",
                      description: Optional[str] = None, niche: Optional[str] = None,
                      preferred_style: Optional[str] = None) -> dict:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY manquant")
    blocks = [
        {"type": "text", "text": "Voici l'image du produit à analyser :"},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
        {"type": "text", "text": _product_infos(product_name, price, currency, description, niche)},
    ]
    if preferred_style and preferred_style != "auto":
        blocks.append({"type": "text", "text": f"⚠️ L'utilisateur IMPOSE le style « {preferred_style} »."})
    blocks.append({"type": "text", "text": PHOTO_SLIDE_KNOWLEDGE})
    blocks.append({"type": "text", "text": _STRATEGY_OUTPUT})
    try:
        raw = _mistral_call(api_key, "pixtral-12b-2409", blocks, timeout=60.0)
        data = _extract_json(raw)
        data["_fallback"] = False
        return data
    except Exception as e:
        print(f"photo_slide strategy error: {e}")
        return _mock_strategy()


# ════════════════════════════════════════════════════════════════════════════
# ÉTAPE 2 — CONTENU (texte rapide)
# ════════════════════════════════════════════════════════════════════════════
def generate_content(strategy: dict, product_name: Optional[str] = None,
                     price: Optional[str] = None, currency: str = "EUR",
                     description: Optional[str] = None, niche: Optional[str] = None) -> dict:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY manquant")
    st = strategy.get("type_slide") or {}
    task = _CONTENT_OUTPUT.format(
        style=st.get("style", "auto"), label=st.get("label", ""),
        hook=strategy.get("hook", ""), titre=strategy.get("titre_carrousel", ""),
        niche=strategy.get("detected_niche") or niche or "non précisée",
    )
    prompt = (PHOTO_SLIDE_KNOWLEDGE + "\n\n"
              + _product_infos(product_name, price, currency, description, niche) + "\n\n"
              + task)
    try:
        raw = _mistral_call(api_key, "mistral-small-latest", prompt, timeout=45.0)
        return _extract_json(raw)
    except Exception as e:
        print(f"photo_slide content error: {e}")
        return _mock_content()


# ════════════════════════════════════════════════════════════════════════════
# Génération complète (one-shot) — gardée pour compat / fallback non-streamé
# ════════════════════════════════════════════════════════════════════════════
def generate_photo_slide(image_b64: str, product_name: Optional[str] = None,
                         price: Optional[str] = None, currency: str = "EUR",
                         description: Optional[str] = None, niche: Optional[str] = None,
                         preferred_style: Optional[str] = None) -> dict:
    strat = generate_strategy(image_b64, product_name, price, currency, description, niche, preferred_style)
    content = generate_content(strat, product_name, price, currency, description, niche)
    return {**strat, **content}


# ════════════════════════════════════════════════════════════════════════════
# Mocks (filets de sécurité si l'IA échoue — l'UI ne casse jamais)
# ════════════════════════════════════════════════════════════════════════════
def _mock_strategy() -> dict:
    return {
        "_fallback": True,
        "type_slide": {"style": "fond_blanc", "label": "Fond Blanc (minimaliste premium)",
                       "justification": "Style épuré idéal pour lister des bénéfices et générer des saves."},
        "hook": "3 signes que ta routine est foirée (et la solution)",
        "titre_carrousel": "3 signes que ta routine cheveux est foirée (et la solution)",
        "titre_variantes": ["Pourquoi tes cheveux cassent (personne ne te le dit)",
                            "Le secret cosméto que tout le monde ignore"],
        "detected_niche": "Cosmétique",
    }


def _mock_content() -> dict:
    return {
        "slides": [
            {"numero": 1, "type": "hook", "texte": "3 signes que tes cheveux te lâchent",
             "sous_texte": "(et personne ne t'a expliqué pourquoi)",
             "photo_a_prendre": "Produit centré sur fond blanc impeccable, texte en haut, typo soignée.",
             "emotion": "Curiosité + tension", "position_texte": "top"},
            {"numero": 2, "type": "value", "texte": "Signe #1 : casse à la racine",
             "sous_texte": "Manque d'hydratation profonde",
             "photo_a_prendre": "Gros plan produit, ingrédients clés mis en avant.",
             "emotion": "Reconnaissance du problème", "position_texte": "center"},
            {"numero": 3, "type": "cta", "texte": "La solution ? Ce sérum.",
             "sous_texte": "Lien dans le panier jaune 🛒",
             "photo_a_prendre": "Produit en majesté + prix visible, ambiance premium.",
             "emotion": "Action immédiate", "position_texte": "bottom"},
        ],
        "cta": "Disponible maintenant dans le panier jaune 🛒 — stock limité.",
        "description_optimisee": ("Tu cherches LE produit qui change tout ?\n\n3 signes que ta routine doit "
                                  "changer 👇\n✨ Casse à la racine\n✨ Cuir chevelu irrité\n✨ Cheveux ternes\n\n"
                                  "La solution dans le panier jaune 🛒"),
        "hashtags": ["tiktokshop", "beautytips", "cheveux", "routinecheveux", "soincapillaire", "cosmetique"],
        "conseils_saves": ["Format liste = forte probabilité de sauvegarde.",
                           "Style fond blanc = épuré, facile à relire.",
                           "Numérotation claire incite à revenir au carrousel."],
    }
