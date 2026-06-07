"""
🎬 AI Video Prompt Studio — génère des prompts text-to-video optimisés TikTok Shop
(Sora 2, Veo 3, Runway, Kling, Pika, Hailuo) via Mistral pixtral (vision : lit
l'image produit).

⚠️ ZONES ÉDITABLES : les blocs balisés « ⬇️ ZONE ÉDITABLE … » sont prévus pour que
le PO enrichisse l'IA (patterns par niveau, spécificités par plateforme) sans
toucher au code.

RÈGLE D'UNICITÉ : un prompt n'est JAMAIS généré deux fois à l'identique (structure
ok, détails toujours différents) — assurée par un seed de variation + température.
"""
from __future__ import annotations

import json
import os
import random
from typing import Optional

import httpx

from analyzer import _extract_json

PLATFORM_LABELS = {
    "sora2": "Sora 2 (OpenAI)", "veo3": "Veo 3 (Google)", "runway": "Runway Gen-4",
    "kling": "Kling AI 2.0", "pika": "Pika Labs 2.0", "hailuo": "Hailuo AI",
    "all": "Toutes les plateformes",
}

AI_VIDEO_PROMPT_SYSTEM = """Tu es un expert en création de PROMPTS vidéo IA (text-to-video) optimisés pour TikTok Shop.
Tu génères un prompt prêt à coller dans l'outil cible. FRANÇAIS PUR. JSON UNIQUEMENT.

# ⚠️ RÈGLE D'UNICITÉ ABSOLUE
Tu ne dois JAMAIS produire deux fois le même prompt. La STRUCTURE peut être identique,
mais TOUS les détails concrets (scènes, décor, lumière, mouvements de caméra, plans,
formulations du hook/CTA, ambiance, objets) doivent être DIFFÉRENTS à chaque génération.
Le « seed de variation » fourni t'oblige à proposer une déclinaison inédite. Interdiction
de recopier une formulation déjà classique : sois créatif et spécifique à CE produit.

# PLATEFORMES
- Sora 2 / Veo 3 : cinématique ultra-réaliste, prompts descriptifs riches.
- Runway Gen-4 : standard, prompts structurés.
- Kling 2.0 / Pika 2.0 / Hailuo : prompts concis, mouvements clairs.
- « all » : propose un prompt adapté, en notant les variantes par plateforme dans variants.

# SPÉCIFICITÉS TIKTOK SHOP
- Format VERTICAL 9:16. Hook stop-scroll dans les 3 premières secondes. Produit visible.
- Durée optimale 15-30s. PAS de claims interdits (santé miracle, médical, "guérit").
- Conforme aux guidelines (pas de marques tierces, pas de contenu trompeur).

# NIVEAUX (durée + usage)
- 1 Simple (3-5s) : B-roll, hook visuel, transition.
- 2 Intermédiaire (5-10s) : démo produit, avant/après.
- 3 Complexe (10-20s) : mini-pub narrative.
- 4 Vidéo TTS complète (15-30s) : vidéo finale prête à publier.
- 5 Multi-clips (30-60s) : 3-5 prompts liés (séquence).

# ⬇️⬇️⬇️ ZONE ÉDITABLE 1 — PATTERNS GAGNANTS PAR NIVEAU (à enrichir par le PO) ⬇️⬇️⬇️
# Ajoute ici des structures de prompts qui marchent, par niveau.
# ⬆️⬆️⬆️ FIN ZONE ÉDITABLE 1 ⬆️⬆️⬆️

# ⬇️⬇️⬇️ ZONE ÉDITABLE 2 — SPÉCIFICITÉS / ASTUCES PAR PLATEFORME (à enrichir) ⬇️⬇️⬇️
# Ex : Sora aime les descriptions de lumière ; Kling préfère les verbes de mouvement…
# ⬆️⬆️⬆️ FIN ZONE ÉDITABLE 2 ⬆️⬆️⬆️

# FORMAT DE RÉPONSE — JSON STRICT
{
  "main_prompt": "Le prompt complet prêt à coller dans l'outil cible.",
  "negative_prompt": "Ce qu'il faut éviter (watermarks, distorsions, texte parasite…).",
  "technical_settings": {"resolution": "1080x1920", "frame_rate": "30fps", "duration": "<ex 25s>", "aspect_ratio": "9:16"},
  "post_production_text": {"hook": "<texte 0-3s>", "middle": "<texte central>", "cta": "<CTA panier jaune>"},
  "music_suggestions": {"type": "<style>", "tempo_bpm": "<ex 90-110>", "trending_examples": ["placeholder 1", "placeholder 2"]},
  "tiktok_shop_compliance": {"status": "passed | warnings", "checks": ["✓ ...", "✓ ..."]},
  "export_steps": ["1. ...", "2. ...", "3. ..."],
  "variants": [{"name": "<angle>", "prompt": "<prompt alternatif COMPLET et DIFFÉRENT>"}],
  "why_it_works": ["<raison 1>", "<raison 2>", "<raison 3>"]
}
Fournis 3 variants minimum, chacun réellement différent (angles distincts).
"""


def _call_pixtral(content: list, timeout: float = 70.0) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY manquant")
    resp = httpx.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "pixtral-12b-2409",
            "messages": [{"role": "user", "content": content}],
            "temperature": 0.9,                 # diversité → unicité
            "random_seed": random.randint(1, 2_000_000_000),
        },
        timeout=timeout,
    )
    if not resp.is_success:
        raise RuntimeError(f"Mistral error {resp.status_code}: {resp.text[:200]}")
    return resp.json()["choices"][0]["message"]["content"]


def generate_video_prompt(image_b64: Optional[str], level: int, platform: str,
                          product_name: Optional[str] = None, description: Optional[str] = None,
                          price: Optional[str] = None, currency: str = "EUR",
                          niche: Optional[str] = None, visual_style: Optional[str] = None,
                          mood: Optional[str] = None, emotion_target: Optional[str] = None,
                          color_tone: Optional[str] = None) -> dict:
    """Génère un plan de prompt vidéo IA. Fallback mock si l'IA échoue (_fallback)."""
    blocks: list = []
    if image_b64:
        blocks.append({"type": "text", "text": "Image du produit à mettre en scène :"})
        blocks.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}})

    infos = [f"- Niveau demandé : {level}", f"- Plateforme cible : {PLATFORM_LABELS.get(platform, platform)}"]
    if product_name: infos.append(f"- Produit : {product_name}")
    if description:  infos.append(f"- Description : {description}")
    if price:        infos.append(f"- Prix : {price} {currency or 'EUR'}")
    if niche:        infos.append(f"- Niche : {niche}")
    style = [x for x in [visual_style, mood, emotion_target, color_tone] if x]
    if style:        infos.append(f"- Style/ambiance : {', '.join(style)}")
    blocks.append({"type": "text", "text": "\n".join(infos)})

    seed = random.randint(100000, 999999)
    blocks.append({"type": "text", "text": f"🎲 Seed de variation : {seed} — produis une déclinaison INÉDITE (jamais vue), détails tous différents."})
    blocks.append({"type": "text", "text": AI_VIDEO_PROMPT_SYSTEM})

    try:
        raw = _call_pixtral(blocks, timeout=70.0)
        data = _extract_json(raw)
        data["_fallback"] = False
        data["platform"] = platform
        data["level"] = level
        return data
    except Exception as e:
        print(f"video_prompt generate error: {e}")
        return _mock_result(level, platform, product_name)


def _mock_result(level: int, platform: str, product_name: Optional[str]) -> dict:
    return {
        "_fallback": True,
        "level": level, "platform": platform,
        "main_prompt": ("Vertical 9:16 cinematic video, 25s. Gros plan produit posé sur une surface "
                        "minérale sombre, lumière dorée rasante, légère fumée. Caméra : slow push-in. "
                        f"Mise en valeur premium de « {product_name or 'le produit'} »."),
        "negative_prompt": "No watermark, no text overlay, no distortion, no extra fingers, no logo tiers.",
        "technical_settings": {"resolution": "1080x1920", "frame_rate": "30fps", "duration": "25s", "aspect_ratio": "9:16"},
        "post_production_text": {"hook": "Le détail que personne ne remarque…", "middle": "Qualité premium, résultat visible.", "cta": "Dispo dans le panier jaune 🛒"},
        "music_suggestions": {"type": "Cinematic inspirant", "tempo_bpm": "90-110", "trending_examples": ["placeholder 1", "placeholder 2"]},
        "tiktok_shop_compliance": {"status": "passed", "checks": ["✓ Pas de claims médicaux", "✓ Format vertical", "✓ Durée optimale"]},
        "export_steps": ["1. Génère dans l'outil IA", "2. Importe dans CapCut", "3. Ajoute textes + musique", "4. Ajoute le bouton produit", "5. Publie"],
        "variants": [{"name": "Plus lifestyle", "prompt": "…"}, {"name": "Plus storytelling", "prompt": "…"}, {"name": "Plus comparatif", "prompt": "…"}],
        "why_it_works": ["Hook curiosité = stop-scroll", "Hero shot = désir", "CTA subtil = conversion"],
    }
