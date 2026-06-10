"""
📸 Carousel Creator (Photo Slide Coach v4) — assemble le résultat complet.

Mode A (prompts) : réutilise photo_slide (pixtral) → plan stratégique + textes.
Mode B (images)  : plan + génération des 4 slides (image_gen, routage intelligent)
                   + conseils pour les slides 5-7 (photos perso à prendre).
"""
from __future__ import annotations

from typing import Optional

import photo_slide
import image_gen


def _next_slides_advice(product_name: str, niche: Optional[str]) -> list:
    """Conseils pour les slides 5-7 (photos réelles à shooter par l'utilisateur)."""
    p = product_name or "ton produit"
    return [
        {"slide_number": 5, "type": "lifestyle", "title": "Photo Lifestyle",
         "photo_advice": f"Montre {p} en situation réelle (matin, dans la routine).",
         "technical_tips": ["Lumière naturelle (fenêtre)", "Produit + main qui l'utilise", "Arrière-plan flou"],
         "text_overlay": "Sa routine au quotidien", "purpose": "Crée la projection mentale."},
        {"slide_number": 6, "type": "detail", "title": "Photo Détail",
         "photo_advice": f"Gros plan sur un détail clé de {p} (texture, ingrédient, finition).",
         "technical_tips": ["Macro / très près", "Fond neutre", "Mise au point nette sur le détail"],
         "text_overlay": "Le détail qui change tout", "purpose": "Renforce la crédibilité."},
        {"slide_number": 7, "type": "cta", "title": "Photo CTA",
         "photo_advice": f"{p} bien présenté + indication vers le panier.",
         "technical_tips": ["Produit centré", "Espace pour le texte", "Flèche/main vers le bas"],
         "text_overlay": "Dispo dans le panier jaune 🛒", "purpose": "Pousse à l'action."},
    ]


def _music() -> dict:
    return {"type": "Cinematic inspirant", "tempo_bpm": "80-100",
            "trending_examples": ["placeholder 1", "placeholder 2", "placeholder 3"]}


def generate_carousel(image_b64: Optional[str], mode: str = "prompts",
                      style: Optional[str] = None, provider: str = "auto",
                      product_name: Optional[str] = None, description: Optional[str] = None,
                      price: Optional[str] = None, currency: str = "EUR",
                      niche: Optional[str] = None, user_idea: Optional[str] = None,
                      product_image_url: Optional[str] = None, avoid: Optional[str] = None) -> dict:
    """Génère le carrousel complet (Mode A ou B). user_idea = idée libre de l'utilisateur
    (intégrée au plan/visuels) ; l'optimisation TikTok Shop reste notre valeur ajoutée.
    product_image_url = image OFFICIELLE TikTok Shop (KeyAPI) → identification + fidélité.
    avoid = hooks/titres/descriptions déjà générés → jamais réutilisés (créativité forcée)."""
    # 1) Plan stratégique + textes (réutilise Photo Slide / pixtral)
    desc_plan = description or ""
    if user_idea:
        desc_plan = (desc_plan + f" | Idée de l'utilisateur à intégrer : {user_idea}").strip(" |")
    plan = photo_slide.generate_photo_slide(
        image_b64, product_name, price, currency, desc_plan, niche,
        preferred_style=style if style and style != "auto" else None,
        image_url=product_image_url, avoid=avoid)

    ts = plan.get("type_slide") or {}
    # Le CHOIX EXPLICITE de l'utilisateur PRIME (sinon pixtral pouvait renvoyer fond_blanc
    # et écraser un choix « cartoon »). Sinon, recommandation de pixtral.
    user_style = style if (style and style != "auto") else None
    chosen_style = user_style or ts.get("style") or "fond_blanc"
    result = {
        "mode": mode,
        "strategy": {
            "chosen_style": chosen_style,
            "recommended_style": chosen_style,
            "style_label": ts.get("label"),
            "justification": ts.get("justification"),
            "detected_niche": plan.get("detected_niche") or niche,
            "probleme_principal": plan.get("probleme_principal"),
            "biais_psychologique": plan.get("biais_psychologique"),
        },
        "hook": plan.get("hook"),
        "carousel_title": plan.get("titre_carrousel"),
        "title_variants": plan.get("titre_variantes") or [],
        "slides_plan": plan.get("slides") or [],
        "cta": plan.get("cta"),
        "description": plan.get("description_optimisee"),
        "hashtags": plan.get("hashtags") or [],
        "music_suggestions": _music(),
        "save_optimization_tips": plan.get("conseils_saves") or [],
        "_fallback": plan.get("_fallback", False),
        "_plan_error": plan.get("_plan_error"),
    }

    # 2) Mode B : images IA (slides 1-4) + conseils slides 5-7
    if mode == "images":
        images = image_gen.generate_slide_images(
            product_name or "", chosen_style, provider, niche,
            description=description, product_image_b64=image_b64, user_idea=user_idea,
            product_image_url=product_image_url,
            problem=plan.get("probleme_principal"),
            slide1_visual=plan.get("slide1_visuel"))
        result["ai_generated_images"] = images
        result["next_slides_advice"] = _next_slides_advice(product_name, niche)
        result["images_mock"] = all(im.get("mock") for im in images) if images else True
        result["ai_used"] = provider
        # Diagnostic : si une image a échoué, on remonte la dernière erreur AIML.
        if any(im.get("mock") for im in (images or [])):
            result["_image_error"] = image_gen.last_error()

    return result
