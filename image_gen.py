"""
🎨 Génération d'images IA (Photo Slide Coach v4 — Mode B).

Abstraction multi-fournisseurs. Tant qu'aucune clé n'est configurée (REPLICATE_API_TOKEN
…), on renvoie un MOCK (placeholder) → l'UI/funnel se construit et se teste sans coût.
Dès qu'une clé est posée, on branche le vrai appel (Replicate : FLUX / Ideogram).

⚠️ ZONE ÉDITABLE : le prompt image (PHOTO_SLIDE_IMG_PROMPT) est prévu pour être
enrichi par le PO (style des slides gagnants).
"""
from __future__ import annotations

import os
import time
from typing import Optional

import httpx

# Fournisseurs proposés à l'utilisateur (label + coût en crédits + prix one-time €).
IMAGE_PROVIDERS = {
    "gemini":   {"label": "Gemini Imagen 4", "credits": 8,  "price": 7.99,  "recommended": True,  "model": None},
    "dalle3":   {"label": "DALL-E 3",        "credits": 10, "price": 9.99,  "model": None},
    "ideogram": {"label": "Ideogram v3",     "credits": 12, "price": 11.99, "model": "ideogram-ai/ideogram-v3-turbo"},
    "flux":     {"label": "FLUX.1 Pro",      "credits": 10, "price": 9.99,  "model": "black-forest-labs/flux-1.1-pro"},
    "multi":    {"label": "Multi-IA (toutes)", "credits": 30, "price": 24.99, "model": None},
}

# ⬇️⬇️⬇️ ZONE ÉDITABLE — STYLE DES SLIDES IA (à enrichir par le PO) ⬇️⬇️⬇️
PHOTO_SLIDE_IMG_PROMPT = (
    "Vertical 9:16 TikTok Shop carousel slide, {style}, premium e-commerce look, "
    "clean composition, space for text overlay, high detail, product: {product}. "
    "Phase: {phase}."
)
# ⬆️⬆️⬆️ FIN ZONE ÉDITABLE ⬆️⬆️⬆️


def provider_credits(provider: str) -> int:
    return IMAGE_PROVIDERS.get(provider, {}).get("credits", 10)


def provider_price(provider: str) -> float:
    return IMAGE_PROVIDERS.get(provider, {}).get("price", 9.99)


def has_image_key() -> bool:
    return bool(os.getenv("REPLICATE_API_TOKEN") or os.getenv("OPENAI_API_KEY")
                or os.getenv("FAL_KEY"))


def _mock_image(phase: str, idx: int) -> dict:
    return {
        "url": None,                 # pas d'URL réelle tant qu'il n'y a pas de clé
        "mock": True,
        "phase": phase,
        "slide": idx,
        "note": "Aperçu démo — branche une clé image (REPLICATE_API_TOKEN) pour générer en réel.",
    }


def _replicate_run(model: str, prompt: str, timeout: float = 60.0) -> Optional[str]:
    """Lance une prédiction Replicate et renvoie l'URL de l'image (ou None)."""
    token = os.getenv("REPLICATE_API_TOKEN")
    if not token or not model:
        return None
    try:
        with httpx.Client(timeout=timeout) as c:
            r = c.post(
                f"https://api.replicate.com/v1/models/{model}/predictions",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                         "Prefer": "wait"},
                json={"input": {"prompt": prompt, "aspect_ratio": "9:16"}},
            )
            data = r.json()
            out = data.get("output")
            if isinstance(out, list) and out:
                return out[0]
            if isinstance(out, str):
                return out
    except Exception as e:
        print(f"replicate run error: {e}")
    return None


def generate_slide_images(product_name: str, style: str, provider: str = "flux",
                          phases: Optional[list] = None) -> list:
    """Génère les 4 slides (Hook/Value/Value/CTA). Mock si pas de clé."""
    phases = phases or ["Hook", "Value", "Value", "CTA"]
    model = IMAGE_PROVIDERS.get(provider, {}).get("model")
    images = []
    for i, phase in enumerate(phases, start=1):
        if not has_image_key() or not model:
            images.append(_mock_image(phase, i))
            continue
        prompt = PHOTO_SLIDE_IMG_PROMPT.format(style=style or "clean studio", product=product_name or "the product", phase=phase)
        url = _replicate_run(model, prompt)
        images.append({"url": url, "mock": url is None, "phase": phase, "slide": i})
    return images
