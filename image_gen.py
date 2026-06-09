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
    """Modèle d'IMAGE-TO-IMAGE (img2img) pour REPRODUIRE FIDÈLEMENT le produit uploadé.
    Meilleur choix : blackforestlabs/flux-2-pro-edit (FLUX.2 Pro Edit, meilleur 2026).
    Configurable via env IMAGE_EDIT_MODEL."""
    return os.getenv("IMAGE_EDIT_MODEL", "blackforestlabs/flux-2-pro-edit")


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
_COMMON = "Vertical 9:16 aspect ratio, TikTok Shop carousel slide, no watermark, no logo, NO TEXT, NO WORDS, NO LABELS on the image."


def _build_prompt(slide_idx: int, phase: str, style: Optional[str], product_name: Optional[str],
                  description: Optional[str], niche: Optional[str], user_idea: Optional[str] = None) -> str:
    idea = f" Creative direction from user: {user_idea}." if user_idea else ""
    style = (style or "").lower()
    sdesc = STYLE_DESC.get(style, _DEFAULT_STYLE_DESC)
    prod = product_name or "the product"
    topic = niche or "everyday life"

    if slide_idx == 1:
        # SLIDE 1 (Hook) : JUSTE la SITUATION du PROBLÈME, zéro produit, zéro texte.
        # PAS dramatique (visages à bout). Subtil, contextuel, relatable.
        if style == "quad_photo":
            return (f"{_COMMON} Composition: a 2x2 grid of four distinct panels. {sdesc}. Each panel shows "
                    f"a RELATABLE SITUATION where someone experiences a problem related to {topic} that needs solving. "
                    f"NOT dramatic faces, NOT distressed. Just natural, everyday situations showing the PROBLEM IN ACTION. "
                    f"IMPORTANT: do NOT show any product. Photoreal, relatable, subtle, natural.{idea}")
        cartoon = "stylized cartoon/anime" if style == "ia_cartoon" else "photoreal, cinematic"
        return (f"{_COMMON} A RELATABLE SITUATION where someone experiences a problem related to {topic} that needs solving. "
                f"Show the PROBLEM IN CONTEXT (not abstract, not dramatic faces). {sdesc}. "
                f"IMPORTANT: do NOT show any product. {cartoon}, natural, relatable, stop-scroll, no text.{idea}")

    # SLIDES 2-4 : le PRODUIT fidèlement reproduit selon l'étape du PROCESS de vente.
    desc = f" ({description})" if description else ""
    ph = phase.lower()

    if "solution" in ph:
        # SLIDE 2 (Solution) : Produit EN SITUATION (EN UTILISATION, pas juste tenu). Fidèle + précis.
        # Exemple lampe: tenue vers le visage/caméra pour éclairer. Exemple huile: appliquée sur la peau. Pas de collage.
        extra = f"The {prod} is ACTIVELY BEING USED by a person — not just held, but IN ACTION solving the problem. " \
                f"Show how it's REALLY USED (placement, application, interaction). Faithfully reproduce {prod} with all details. " \
                f"Natural integration, no collage effect. {sdesc}. Realistic, relatable, reassuring."
    elif "cta" in ph:
        # SLIDE 4 (CTA) : Produit en action, vibe d'appel à l'action / panier.
        extra = f"The {prod} in ACTION, ready-to-buy mood. Hero shot, product centered and prominent. {sdesc}. " \
                f"Inspiring, action-oriented, CTA-ready. Faithfully reproduce {prod} with all brand details."
    else:
        # SLIDE 3 (Produit) : Produit seul, RESPECT le style. Clean, product photography.
        extra = f"Showcase {prod} ALONE, clean and premium. Product-centered, highlight key features/benefits. " \
                f"{sdesc}. Faithfully reproduce {prod} with all details (logos, text, colors, brand elements). " \
                f"MUST respect the chosen style ({style or 'default'})."

    # Directives clés : fidélité produit + RESPECT STYLE + zéro texte.
    style_enforcement = f"MANDATORY: Use the EXACT visual style requested: {sdesc}" if style and style != "auto" else ""
    return (f"{_COMMON} {style_enforcement} Faithfully reproduce the product: {prod}{desc}. {extra}{idea} "
            f"Reproduce faithfully the uploaded product with all details (colors, logos, text, finish). No collage effect. No text on image.")


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

    # Payload MINIMAL : vertical 9:16 demandé dans le prompt.
    base = {"model": model, "prompt": prompt}
    if image_ref:
        # Image-to-Image (img2img) : passe l'image source (base64 ou URL) au champ "image_urls" (ARRAY).
        # AIML accepte data:image/jpeg;base64,... ou URLs publiques.
        payload = {**base, "image_urls": [image_ref], "image_size": "landscape_16_9"}
        url = _call(payload)
        if url:
            return url
        # Fallback txt2img si img2img échoue (le modèle peut ne pas supporter img2img).
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
        # LOGIQUE D'IMAGE :
        # Slide 1 (Hook) : JAMAIS l'image du produit → txt2img du PROBLÈME uniquement.
        # Slides 2+ : image-to-image avec le produit uploadé → reproduit FIDÈLEMENT le produit.
        if i >= 2 and image_ref:
            # Image-to-image : passe l'image uploadée + prompt spécifique (Solution/Produit/CTA)
            url = _aiml_generate(edit_model(), prompt, image_ref=image_ref)
            model = edit_model()
        else:
            # Slide 1 OU pas d'image uploadée : txt2img normal (pas de référence image)
            url = _aiml_generate(model, prompt, image_ref=None)
        images.append({"url": url, "mock": url is None, "phase": phase, "slide": i,
                       "model": model, "need": need, "no_product": i == 1})
    return images
