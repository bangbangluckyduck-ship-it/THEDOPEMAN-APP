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

# Dernière erreur AIML rencontrée (pour diagnostic via /api/_admin/image-selftest).
_LAST_ERROR: Optional[str] = None


def last_error() -> Optional[str]:
    return _LAST_ERROR

# ── Modèles AIML par BESOIN (IDs à confirmer/ajuster dans la doc AIML) ───────────
# ⬇️ ZONE ÉDITABLE — mapping besoin → meilleur modèle (qualité PROD) ⬇️
_PROD_MODEL_BY_NEED = {
    "text":     "recraft-v3",                  # texte/design net (Quad Photo, overlays)
    "realism":  "flux-pro/v1.1",               # photoréalisme produit (Fond Blanc, hero shot)
    "anime":    "flux/dev",                    # anime / cartoon / stylisé (IA Cartoon)
    "artistic": "dall-e-3",                    # créatif / artistique
    "premium":  "imagen-4.0-generate-001",     # rendu premium / luxe
}
# ⬆️ FIN ZONE ÉDITABLE ⬆️

# 💸 Mode TEST économique : txt2img « auto » sur FLUX schnell (~0,008 €/image).
# Bascule qualité PROD via env IMAGE_QUALITY=prod (sans redéploiement).
_TEST_MODEL = "flux/schnell"

# Choix EXPLICITE d'IA (utilise le vrai modèle, même en mode test, pour pouvoir comparer).
PROVIDER_MODEL = {
    "flux":       "flux-pro/v1.1",
    "nanobanana": "google/gemini-2.5-flash-image",
    "recraft":    "recraft-v3",
    "dalle3":     "dall-e-3",
    "imagen":     "imagen-4.0-generate-001",
}


def _is_prod_quality() -> bool:
    return os.getenv("IMAGE_QUALITY", "test").lower() == "prod"


def need_model(need: str) -> str:
    if not _is_prod_quality():
        return _TEST_MODEL
    return _PROD_MODEL_BY_NEED.get(need, _PROD_MODEL_BY_NEED["realism"])


def edit_model() -> str:
    """Modèle d'ÉDITION d'image (conserve le produit à partir de la photo uploadée).
    txt2img (schnell) ne peut pas reproduire le produit → on utilise un modèle img2img
    / subject-preserving (FLUX Kontext). Configurable via env IMAGE_EDIT_MODEL."""
    return os.getenv("IMAGE_EDIT_MODEL", "google/gemini-2.5-flash-image-edit")


# Compat (certains affichages lisent MODEL_BY_NEED) → reflète le mode courant.
MODEL_BY_NEED = {k: need_model(k) for k in _PROD_MODEL_BY_NEED}

# Choix explicites proposés à l'utilisateur (label + coût crédits + prix one-time €).
# "auto" = routage intelligent (recommandé).
IMAGE_PROVIDERS = {
    "auto":       {"label": "Auto (meilleure IA)",   "credits": 8,  "price": 7.99, "recommended": True},
    "nanobanana": {"label": "Nano Banana (fidèle)",  "credits": 8,  "price": 7.99},
    "flux":       {"label": "FLUX (réalisme)",       "credits": 10, "price": 9.99},
    "imagen":     {"label": "Imagen (premium)",      "credits": 8,  "price": 7.99},
    "dalle3":     {"label": "DALL-E 3 (créatif)",    "credits": 10, "price": 9.99},
    "recraft":    {"label": "Recraft (texte/design)", "credits": 10, "price": 9.99},
    "multi":      {"label": "Multi-IA (compare 3)",  "credits": 30, "price": 24.99},
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
                  description: Optional[str], niche: Optional[str], user_idea: Optional[str] = None) -> str:
    idea = f" Creative direction from user: {user_idea}." if user_idea else ""
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
                    f"only. Photoreal, relatable, emotional.{idea}")
        cartoon = "stylized cartoon/anime" if style == "ia_cartoon" else "photoreal, cinematic"
        return (f"{_COMMON} A single strong HOOK image showing a relatable PROBLEM / frustration / pain "
                f"related to {topic}. IMPORTANT: do NOT show any product. {cartoon}, emotional, stop-scroll.{idea}")

    # SLIDES 2+ : le PRODUIT fidèlement reproduit, selon l'étape du PROCESS de vente.
    desc = f" ({description})" if description else ""
    ph = phase.lower()
    if "cta" in ph:
        extra = "CTA slide: hero shot, product centered and prominent, inviting, points toward the cart."
    elif "solution" in ph:
        extra = "SOLUTION slide: present the product as the answer to the problem, reassuring."
    else:  # Produit
        extra = "PRODUCT slide: showcase the product, highlight its key benefit/feature."
    # Directive clé pour la fidélité produit (testé sur Gemini/ChatGPT — marche)
    return (f"{_COMMON} Faithfully reproduce the product: {prod}{desc}. {sdesc}. {extra}{idea} Reproduce faithfully the uploaded product.")


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
    if provider and provider != "auto" and provider in PROVIDER_MODEL:
        return PROVIDER_MODEL[provider]      # choix explicite → vrai modèle (même en test)
    need = pick_need(style, niche, phase)
    return need_model(need)


def _aiml_generate(model: str, prompt: str, image_ref: Optional[str] = None,
                   timeout: float = 90.0) -> Optional[str]:
    """Appel AIML API (compatible OpenAI images). image_ref = data URI produit (img2img,
    pour fidélité). Si l'appel échoue avec la réf, retente en text-only."""
    key = os.getenv("AIMLAPI_KEY")
    if not key or not model:
        return None

    global _LAST_ERROR

    def _call(payload):
        global _LAST_ERROR
        try:
            with httpx.Client(timeout=timeout) as c:
                r = c.post(f"{AIML_BASE}/images/generations",
                           headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                           json=payload)
            if not r.is_success:
                _LAST_ERROR = f"{r.status_code} (model={payload.get('model')}): {r.text[:300]}"
                print(f"AIML {_LAST_ERROR}")
                return None
            data = r.json()
            items = data.get("data") or data.get("images") or []
            if items and isinstance(items, list):
                first = items[0]
                if isinstance(first, dict):
                    return first.get("url") or first.get("image_url") or first.get("b64_json")
                if isinstance(first, str):
                    return first
            _LAST_ERROR = f"réponse sans image (model={payload.get('model')}): {str(data)[:200]}"
        except Exception as e:
            _LAST_ERROR = f"exception (model={payload.get('model')}): {e}"
            print(f"AIML generate error: {e}")
        return None

    # Payload MINIMAL (la taille varie selon les modèles AIML → on laisse le défaut
    # pour éviter les refus). Vertical 9:16 demandé dans le prompt.
    base = {"model": model, "prompt": prompt}
    if image_ref:
        # Édition / img2img : on teste plusieurs noms de champ d'image selon le modèle.
        for field in ("image_url", "image_urls", "image", "reference_image_url"):
            payload = {**base, field: ([image_ref] if field == "image_urls" else image_ref)}
            url = _call(payload)
            if url:
                return url
    return _call(base)


def list_models() -> dict:
    """Liste les modèles dispo de la clé AIML (pour récupérer les IDs exacts)."""
    key = os.getenv("AIMLAPI_KEY")
    if not key:
        return {"error": "AIMLAPI_KEY absente"}
    try:
        with httpx.Client(timeout=20.0) as c:
            r = c.get(f"{AIML_BASE}/models", headers={"Authorization": f"Bearer {key}"})
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def _mock_image(phase: str, idx: int, need: str) -> dict:
    return {"url": None, "mock": True, "phase": phase, "slide": idx, "need": need,
            "note": "Aperçu démo — pose AIMLAPI_KEY sur Render pour générer en réel."}


def generate_slide_images(product_name: str, style: str, provider: str = "auto",
                          niche: Optional[str] = None, phases: Optional[list] = None,
                          description: Optional[str] = None, product_image_b64: Optional[str] = None,
                          user_idea: Optional[str] = None) -> list:
    """Génère les 4 slides avec règles impératives :
       - slide 1 (Hook) : aucun produit → problème (+ Quad = grille 2x2).
       - slides 2+ : produit fidèle (référence img2img si dispo).
    Routage intelligent du modèle. Mock si pas de clé."""
    # 4 slides générées = process de vente : Accroche(sans produit) → Solution → Produit → CTA.
    phases = phases or ["Accroche", "Solution", "Produit", "CTA"]
    image_ref = None
    if product_image_b64:
        image_ref = "data:image/jpeg;base64," + product_image_b64
    images = []
    for i, phase in enumerate(phases, start=1):
        need = pick_need(style, niche, phase)
        model = model_for(provider, style, niche, phase)
        prompt = _build_prompt(i, phase, style, product_name, description, niche, user_idea)
        if not has_image_key():
            images.append({**_mock_image(phase, i, need), "prompt": prompt})
            continue
        # Slide 1 = pas de produit (txt2img). Slides 2+ avec photo → modèle d'ÉDITION
        # (conserve le produit). Sans photo → txt2img normal.
        if i >= 2 and image_ref:
            url = _aiml_generate(edit_model(), prompt, image_ref=image_ref)
            model = edit_model()
        else:
            url = _aiml_generate(model, prompt, image_ref=None)
        images.append({"url": url, "mock": url is None, "phase": phase, "slide": i,
                       "model": model, "need": need, "no_product": i == 1})
    return images
