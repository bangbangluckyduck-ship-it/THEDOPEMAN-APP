"""
🎨 Génération d'images IA (Photo Slide Coach v4 — Mode B) via AGRÉGATEUR (AIML API).

UNE seule clé (AIMLAPI_KEY) → accès à FLUX, DALL-E, Ideogram, Imagen, SD…
🤖 ROUTAGE INTELLIGENT : notre IA choisit le MEILLEUR modèle selon le besoin de
l'image (texte net, réalisme produit, anime/cartoon, premium, artistique) — l'utilisateur
n'a pas à choisir (mode « auto »). Les choix explicites restent possibles.

Tant qu'aucune clé n'est posée → MOCK (le funnel se construit/teste sans coût).
"""
from __future__ import annotations

import os
from typing import Optional

import httpx

AIML_BASE = "https://api.aimlapi.com/v1"

# ── Modèles AIML par BESOIN (IDs à confirmer/ajuster dans la doc AIML) ───────────
# ⬇️ ZONE ÉDITABLE — mapping besoin → meilleur modèle (qualité PROD) ⬇️
_PROD_MODEL_BY_NEED = {
    "text":     "ideogram/V_3",          # texte net dans l'image (Quad Photo, overlays)
    "realism":  "flux-pro/v1.1",         # photoréalisme produit (Fond Blanc, hero shot)
    "anime":    "flux/dev",              # anime / cartoon / stylisé (IA Cartoon)
    "artistic": "dall-e-3",              # créatif / artistique
    "premium":  "imagen-3",              # rendu premium / luxe
}
# ⬆️ FIN ZONE ÉDITABLE ⬆️

# 💸 Mode TEST économique : tout sur FLUX schnell (~0,008 €/image) pour valider à
# moindre coût. Bascule en qualité PROD avec env IMAGE_QUALITY=prod (sans redéploiement).
_TEST_MODEL = "flux/schnell"
_PROVIDER_NEED = {"flux": "realism", "ideogram": "text", "dalle3": "artistic", "imagen": "premium"}


def _is_prod_quality() -> bool:
    return os.getenv("IMAGE_QUALITY", "test").lower() == "prod"


def need_model(need: str) -> str:
    if not _is_prod_quality():
        return _TEST_MODEL
    return _PROD_MODEL_BY_NEED.get(need, _PROD_MODEL_BY_NEED["realism"])


# Compat (certains affichages lisent MODEL_BY_NEED) → reflète le mode courant.
MODEL_BY_NEED = {k: need_model(k) for k in _PROD_MODEL_BY_NEED}

# Choix explicites proposés à l'utilisateur (label + coût crédits + prix one-time €).
# "auto" = routage intelligent (recommandé).
IMAGE_PROVIDERS = {
    "auto":     {"label": "Auto (meilleure IA selon l'image)", "credits": 8,  "price": 7.99, "recommended": True, "model": None},
    "flux":     {"label": "FLUX (réalisme)",   "credits": 10, "price": 9.99,  "model": MODEL_BY_NEED["realism"]},
    "ideogram": {"label": "Ideogram (texte)",  "credits": 12, "price": 11.99, "model": MODEL_BY_NEED["text"]},
    "dalle3":   {"label": "DALL-E 3 (créatif)", "credits": 10, "price": 9.99, "model": MODEL_BY_NEED["artistic"]},
    "imagen":   {"label": "Imagen (premium)",  "credits": 8,  "price": 7.99,  "model": MODEL_BY_NEED["premium"]},
    "multi":    {"label": "Multi-IA (compare 3)", "credits": 30, "price": 24.99, "model": None},
}

# ⬇️ ZONE ÉDITABLE — description des styles (rendu visuel) ⬇️
STYLE_DESC = {
    "fond_blanc": "clean minimalist studio shot on a pure white seamless background, soft shadows, premium e-commerce product photography, sharp focus",
    "quad_photo": "clean bright product photography, high detail",
    "ia_cartoon": "stylized 3D cartoon / anime illustration, vibrant colors, Pixar-like, expressive",
}
_DEFAULT_STYLE_DESC = "clean professional product photography, premium look"
# ⬆️ FIN ZONE ÉDITABLE ⬆️

# ── RÈGLES IMPÉRATIVES de génération (par slide) ────────────────────────────────
# Slide 1 (Hook) : le PRODUIT N'APPARAÎT JAMAIS → visuel d'un PROBLÈME que le produit
#   résout (+ Quad = grille 2x2 de 4 problèmes/douleurs). Slides 2+ : produit FIDÈLE.
_COMMON = "Vertical 9:16 aspect ratio, TikTok Shop carousel slide, large empty area for bold text overlay, no watermark, no logo."


def _build_prompt(slide_idx: int, phase: str, style: Optional[str], product_name: Optional[str],
                  description: Optional[str], niche: Optional[str]) -> str:
    style = (style or "").lower()
    sdesc = STYLE_DESC.get(style, _DEFAULT_STYLE_DESC)
    prod = product_name or "the product"
    topic = niche or "everyday life"

    if slide_idx == 1:
        # HOOK : aucun produit, on montre un PROBLÈME / une douleur.
        if style == "quad_photo":
            return (f"{_COMMON} Composition: a 2x2 grid of four distinct panels. Each panel "
                    f"illustrates a different problem, frustration or pain point related to {topic} "
                    f"that a solution would fix. IMPORTANT: do NOT show any product. People/situations "
                    f"only. Photoreal, relatable, emotional.")
        cartoon = "stylized cartoon/anime" if style == "ia_cartoon" else "photoreal, cinematic"
        return (f"{_COMMON} A single strong HOOK image showing a relatable PROBLEM / frustration / pain "
                f"related to {topic}. IMPORTANT: do NOT show any product. {cartoon}, emotional, stop-scroll.")

    # SLIDES 2+ : le PRODUIT fidèlement reproduit dans le style choisi.
    desc = f" ({description})" if description else ""
    if phase.lower() == "cta":
        extra = "Hero shot, product centered and prominent, inviting, call-to-action vibe."
    else:
        extra = "Product clearly visible and faithfully rendered, in context."
    return (f"{_COMMON} Faithfully reproduce the product: {prod}{desc}. {sdesc}. {extra}")


def provider_credits(provider: str) -> int:
    return IMAGE_PROVIDERS.get(provider, {}).get("credits", 10)


def provider_price(provider: str) -> float:
    return IMAGE_PROVIDERS.get(provider, {}).get("price", 9.99)


def has_image_key() -> bool:
    return bool(os.getenv("AIMLAPI_KEY"))


def pick_need(style: Optional[str], niche: Optional[str], phase: Optional[str] = None) -> str:
    """🤖 Choisit le BESOIN d'image (→ meilleur modèle) selon le style/niche."""
    s = (style or "").lower()
    n = (niche or "").lower()
    if any(k in s for k in ("quad", "texte", "liste", "text")):
        return "text"                      # besoin de texte net → Ideogram
    if any(k in s for k in ("cartoon", "anime", "ia", "illustration", "dessin")):
        return "anime"
    if any(k in s for k in ("premium", "luxe", "luxury")) or "cosm" in n or "beaut" in n:
        return "premium"
    if any(k in s for k in ("artistique", "creatif", "créatif", "fun")):
        return "artistic"
    return "realism"                       # défaut : photoréalisme produit (FLUX)


def model_for(provider: str, style: Optional[str], niche: Optional[str], phase: Optional[str] = None) -> str:
    """Modèle AIML à utiliser : routage intelligent en mode auto, sinon le choix explicite.
    En mode test (IMAGE_QUALITY != prod), tout est routé sur FLUX schnell (économie)."""
    if provider in (None, "", "auto"):
        need = pick_need(style, niche, phase)
    else:
        need = _PROVIDER_NEED.get(provider, "realism")
    return need_model(need)


def _aiml_generate(model: str, prompt: str, image_ref: Optional[str] = None,
                   timeout: float = 90.0) -> Optional[str]:
    """Appel AIML API (compatible OpenAI images). image_ref = data URI produit (img2img,
    pour fidélité). Si l'appel échoue avec la réf, retente en text-only."""
    key = os.getenv("AIMLAPI_KEY")
    if not key or not model:
        return None

    def _call(payload):
        try:
            with httpx.Client(timeout=timeout) as c:
                r = c.post(f"{AIML_BASE}/images/generations",
                           headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                           json=payload)
            if not r.is_success:
                print(f"AIML {r.status_code}: {r.text[:200]}")
                return None
            data = r.json()
            items = data.get("data") or data.get("images") or []
            if items and isinstance(items, list):
                first = items[0]
                if isinstance(first, dict):
                    return first.get("url") or first.get("image_url") or first.get("b64_json")
                if isinstance(first, str):
                    return first
        except Exception as e:
            print(f"AIML generate error: {e}")
        return None

    base = {"model": model, "prompt": prompt, "size": "1024x1792"}
    if image_ref:
        # Tentative img2img (référence produit) → fallback text-only si non supporté.
        url = _call({**base, "image_url": image_ref})
        if url:
            return url
    return _call(base)


def _mock_image(phase: str, idx: int, need: str) -> dict:
    return {"url": None, "mock": True, "phase": phase, "slide": idx, "need": need,
            "note": "Aperçu démo — pose AIMLAPI_KEY sur Render pour générer en réel."}


def generate_slide_images(product_name: str, style: str, provider: str = "auto",
                          niche: Optional[str] = None, phases: Optional[list] = None,
                          description: Optional[str] = None, product_image_b64: Optional[str] = None) -> list:
    """Génère les 4 slides avec règles impératives :
       - slide 1 (Hook) : aucun produit → problème (+ Quad = grille 2x2).
       - slides 2+ : produit fidèle (référence img2img si dispo).
    Routage intelligent du modèle. Mock si pas de clé."""
    phases = phases or ["Hook", "Value", "Value", "CTA"]
    image_ref = None
    if product_image_b64:
        image_ref = "data:image/jpeg;base64," + product_image_b64
    images = []
    for i, phase in enumerate(phases, start=1):
        need = pick_need(style, niche, phase)
        model = model_for(provider, style, niche, phase)
        prompt = _build_prompt(i, phase, style, product_name, description, niche)
        if not has_image_key():
            images.append({**_mock_image(phase, i, need), "prompt": prompt})
            continue
        # Slide 1 = pas de produit → on n'envoie PAS la référence. Slides 2+ → référence.
        ref = image_ref if i >= 2 else None
        url = _aiml_generate(model, prompt, image_ref=ref)
        images.append({"url": url, "mock": url is None, "phase": phase, "slide": i,
                       "model": model, "need": need, "no_product": i == 1})
    return images
