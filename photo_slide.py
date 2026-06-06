"""
📸 Photo Slide Coach (feature premium GOLD / AGENCY).

À partir d'une image produit + (nature, prix, description), l'IA vision
(Mistral pixtral-12b) propose un plan de carrousel TikTok Shop optimisé :
  • type de slide recommandé (parmi 3 styles)
  • Hook (texte de la 1ʳᵉ image)
  • titre du carrousel (+ variantes)
  • description produit optimisée
  • plan slide par slide AVEC le type de photo à prendre pour chacune
  • CTA de la dernière slide

⚠️ ZONES ÉDITABLES : les blocs entre les balises
   « ⬇️⬇️⬇️ ZONE ÉDITABLE … » et « ⬆️⬆️⬆️ FIN ZONE ÉDITABLE »
   sont prévus pour que le product owner enrichisse l'IA (hooks gagnants,
   patterns de slides, exemples par niche) SANS toucher au reste du code.
"""
from __future__ import annotations

import os
from typing import Optional

# On réutilise les utilitaires Mistral déjà éprouvés de l'analyzer.
from analyzer import _mistral_call, _extract_json


# ════════════════════════════════════════════════════════════════════════════
# PROMPT SYSTÈME — directives stratégiques (issues du cahier des charges)
# ════════════════════════════════════════════════════════════════════════════
PHOTO_SLIDE_SYSTEM_PROMPT = """Tu es un expert en stratégie de carrousels (« Photo Slides ») TikTok Shop.
À partir d'une IMAGE produit et de quelques infos, tu génères un plan de carrousel optimisé pour :
- Maximiser le DWELL TIME (le swipe entre slides = signal algorithmique fort, propulsion « Pour Toi »).
- Inciter aux SAVES (sauvegardes) : format liste/fiche pratique = signal de reach très fort.
- CONVERTIR vers le panier TikTok Shop.

FRANÇAIS PUR. Langage concret et actionnable. Tu réponds UNIQUEMENT en JSON valide.

# STRUCTURE UNIVERSELLE « HOOK → VALUE → CTA »
- SLIDE 1 (HOOK) : image choc ou problème accrocheur, stop-scroll immédiat, tension psychologique.
- SLIDES DU MILIEU (VALUE) : éducation, caractéristiques, réassurance/preuves, avant/après, bénéfices listés.
- DERNIÈRE SLIDE (CTA) : appel à l'action direct vers le panier TikTok Shop, urgence + bénéfice clair.

# LES 3 STYLES DE SLIDES À RECOMMANDER (tu en choisis UN, le plus adapté)

## Style « quad_photo » — 4 photos divisées (grille 2x2)
Image divisée en 4 quadrants (4 visuels : un symptôme / un problème / un bénéfice / un signe), texte
accrocheur centré. Idéal pour : listes de symptômes/signes, listes de bénéfices, top 4 caractéristiques,
comparaisons rapides. Niches : santé/bien-être, beauté, fitness, éducation produit.
Nb de slides : souvent 1 slide composite (parfois 2-3).

## Style « fond_blanc » — produit épuré + texte
Photo centrale très propre (dos ou profil), fond blanc impeccable, typo soignée, minimaliste premium.
Idéal pour : mise en avant produit premium, listes éducatives, conseils experts, listes de signes/erreurs.
Niches : cosmétique premium, soins capillaires, conseils experts, niches « éducation ».
Nb de slides : 3 à 5.

## Style « ia_cartoon » — personnage transformation (split screen)
Gauche : personnage avec problème (style IA/cartoon/anime, émotion triste/frustré). Droite : même
personnage transformé (heureux/confiant, bénéfices visibles). Idéal pour : avant/après, transformation,
problème→solution, aspiration, storytelling visuel rapide.
Niches : fitness/musculation, cosmétique transformative, compléments, bien-être/lifestyle.
Nb de slides : 2 à 4.

# RÈGLES DE GÉNÉRATION
- Analyse l'IMAGE + la nature/niche + le prix pour CHOISIR le meilleur style (sauf si l'utilisateur impose un style).
- Le Hook doit créer une tension ou une curiosité immédiate (pas une description plate du produit).
- Pour CHAQUE slide, précise le TYPE DE PHOTO À PRENDRE (cadrage, fond, angle, ce qu'on voit).
- La description optimisée : accroche + bénéfices listés (✨) + réassurance + CTA panier jaune 🛒. 200-320 caractères.
- Hashtags : 2-3 tendances généralistes + 3-4 niche + 1-2 TikTok Shop. Max 8-10.

# ⬇️⬇️⬇️ ZONE ÉDITABLE 1 — HOOKS GAGNANTS (à enrichir par le product owner) ⬇️⬇️⬇️
# Ajoute ici des patterns de hooks qui convertissent (par niche), des formules, des exemples réels.
# Exemples de départ :
# - « Les N signes que … (et personne ne te l'a dit) »
# - « Pourquoi ton/ta … [problème] (et la solution) »
# - « Arrête de … si tu veux … »
# ⬆️⬆️⬆️ FIN ZONE ÉDITABLE 1 ⬆️⬆️⬆️

# ⬇️⬇️⬇️ ZONE ÉDITABLE 2 — IDÉES DE SLIDES / ANGLES GAGNANTS (à enrichir) ⬇️⬇️⬇️
# Ajoute ici des structures de carrousels qui marchent, des angles par niche, des exemples de CTA.
# ⬆️⬆️⬆️ FIN ZONE ÉDITABLE 2 ⬆️⬆️⬆️

# FORMAT DE RÉPONSE — JSON STRICT, EXACTEMENT CETTE STRUCTURE
{
  "type_slide": {
    "style": "quad_photo | fond_blanc | ia_cartoon",
    "label": "Nom lisible du style en français",
    "justification": "1-2 phrases : pourquoi ce style pour CE produit."
  },
  "hook": "Texte du hook de la 1ʳᵉ slide (court, percutant).",
  "titre_carrousel": "Titre principal du carrousel.",
  "titre_variantes": ["variante 1", "variante 2"],
  "description_optimisee": "Description produit optimisée prête à coller (avec emojis, bénéfices, CTA).",
  "slides": [
    {
      "numero": 1,
      "type": "hook | value | cta",
      "texte": "Texte à afficher sur la slide.",
      "sous_texte": "Sous-texte optionnel (peut être vide).",
      "photo_a_prendre": "Description PRÉCISE de la photo à shooter : cadrage, fond, angle, ce qu'on voit.",
      "emotion": "Émotion à transmettre.",
      "position_texte": "center | top | bottom"
    }
  ],
  "cta": "Phrase de CTA de la dernière slide (vers le panier TikTok Shop).",
  "hashtags": ["hashtag1", "hashtag2"],
  "conseils_saves": ["Conseil 1 pour maximiser les sauvegardes.", "Conseil 2."]
}
"""


def _build_user_blocks(image_b64: str, product_name: Optional[str], price: Optional[str],
                       currency: str, description: Optional[str], niche: Optional[str],
                       preferred_style: Optional[str]) -> list:
    """Construit les blocs de contenu (image + consignes) pour pixtral."""
    blocks: list = [
        {"type": "text", "text": "Voici l'image du produit à analyser :"},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
    ]
    infos = []
    if product_name:
        infos.append(f"- Nature / nom du produit : {product_name}")
    if description:
        infos.append(f"- Description fournie : {description}")
    if price:
        infos.append(f"- Prix : {price} {currency or 'EUR'}")
    if niche:
        infos.append(f"- Niche / catégorie : {niche}")
    if infos:
        blocks.append({"type": "text", "text": "Informations produit :\n" + "\n".join(infos)})

    if preferred_style and preferred_style != "auto":
        blocks.append({"type": "text",
                       "text": f"⚠️ L'utilisateur IMPOSE le style « {preferred_style} ». Utilise CE style."})
    else:
        blocks.append({"type": "text", "text": "Choisis toi-même le meilleur style parmi les 3."})

    blocks.append({"type": "text", "text": PHOTO_SLIDE_SYSTEM_PROMPT})
    return blocks


def generate_photo_slide(image_b64: str, product_name: Optional[str] = None,
                         price: Optional[str] = None, currency: str = "EUR",
                         description: Optional[str] = None, niche: Optional[str] = None,
                         preferred_style: Optional[str] = None) -> dict:
    """Appelle pixtral et renvoie le plan de carrousel structuré (dict).

    En cas d'échec IA → renvoie un plan mock (cahier des charges) pour ne jamais
    casser l'UI, avec _fallback=True pour le signaler.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY manquant")

    content = _build_user_blocks(image_b64, product_name, price, currency,
                                 description, niche, preferred_style)
    try:
        raw = _mistral_call(api_key, "pixtral-12b-2409", content, timeout=60.0)
        data = _extract_json(raw)
        data["_fallback"] = False
        return data
    except Exception as e:
        print(f"photo_slide generate error: {e}")
        return _mock_result()


def _mock_result() -> dict:
    """Plan mock (issu du cahier des charges) — filet de sécurité si l'IA échoue."""
    return {
        "_fallback": True,
        "type_slide": {
            "style": "fond_blanc",
            "label": "Fond Blanc (minimaliste premium)",
            "justification": "Style épuré idéal pour lister des bénéfices et générer des sauvegardes.",
        },
        "hook": "3 signes que ta routine est foirée (et la solution)",
        "titre_carrousel": "3 signes que ta routine cheveux est foirée (et la solution)",
        "titre_variantes": [
            "Pourquoi tes cheveux cassent (personne ne te le dit)",
            "Le secret cosméto que tout le monde ignore",
        ],
        "description_optimisee": ("Tu cherches LE produit qui change tout ?\n\n3 signes que ta routine doit "
                                  "changer 👇\n✨ Casse à la racine\n✨ Cuir chevelu irrité\n✨ Cheveux ternes\n\n"
                                  "La solution dans le panier jaune 🛒"),
        "slides": [
            {"numero": 1, "type": "hook", "texte": "3 signes que tes cheveux te lâchent",
             "sous_texte": "(et personne ne t'a expliqué pourquoi)",
             "photo_a_prendre": "Produit centré sur fond blanc impeccable, texte en haut, typo soignée.",
             "emotion": "Curiosité + tension", "position_texte": "top"},
            {"numero": 2, "type": "value", "texte": "Signe #1 : casse à la racine",
             "sous_texte": "Manque d'hydratation profonde",
             "photo_a_prendre": "Gros plan produit, ingrédients clés mis en avant.",
             "emotion": "Reconnaissance du problème", "position_texte": "center"},
            {"numero": 3, "type": "value", "texte": "Signe #2 : cuir chevelu irrité",
             "sous_texte": "pH déséquilibré",
             "photo_a_prendre": "Détail produit + texte explicatif sur fond clair.",
             "emotion": "Validation + soulagement", "position_texte": "center"},
            {"numero": 4, "type": "cta", "texte": "La solution ? Ce sérum.",
             "sous_texte": "Lien dans le panier jaune 🛒",
             "photo_a_prendre": "Produit en majesté + prix visible, ambiance premium.",
             "emotion": "Action immédiate", "position_texte": "bottom"},
        ],
        "cta": "Disponible maintenant dans le panier jaune 🛒 — stock limité.",
        "hashtags": ["tiktokshop", "beautytips", "cheveux", "routinecheveux",
                     "soincapillaire", "cosmetique", "tipsbeaute"],
        "conseils_saves": [
            "Format liste = forte probabilité de sauvegarde.",
            "Style fond blanc = épuré, facile à relire.",
            "Numérotation claire incite à revenir au carrousel.",
        ],
    }
