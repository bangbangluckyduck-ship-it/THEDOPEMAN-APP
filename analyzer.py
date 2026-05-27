from __future__ import annotations
import base64
import json
import os
import re
from pathlib import Path
from typing import List, Optional


# ════════════════════════════════════════════════════════════════════════════
# HOOKS DB CONTEXT (chargé une fois au démarrage, injecté côté synthèse)
# ════════════════════════════════════════════════════════════════════════════
def _load_hooks_context() -> str:
    try:
        db_path = Path(__file__).parent / "hooks_db.json"
        db = json.loads(db_path.read_text(encoding="utf-8"))

        lines = ["\n================================================================================",
                 "BASE DE DONNÉES ACCROCHES (utilise pour tes recommandations)",
                 "================================================================================"]

        lines.append("\nPERFORMANCE TYPES D'ACCROCHE (score = conversion):")
        for cat in sorted(db["categories"], key=lambda c: c["performance_score"], reverse=True):
            warn = f" ⚠️ {cat['warning']}" if cat.get("warning") else ""
            lines.append(f"- {cat['nom']} (score {cat['performance_score']:.0%}): {cat['description']}{warn}")
            lines.append(f"  Exemples: {' | '.join(cat['examples'][:3])}")

        lines.append("\nRECOS PAR CATÉGORIE PRODUIT:")
        for key, cat in db["product_categories"].items():
            hooks = ", ".join(cat["recommended_hooks"])
            lines.append(f"- {key} ({', '.join(cat['names'][:4])}…): meilleurs types → {hooks}. {cat['notes']}")

        lines.append("\nFACTEURS PRIX:")
        for key, pf in db["price_factors"].items():
            lines.append(f"- {pf['range']}€: multiplicateur viral ×{pf['viral_multiplier']} — {pf['note']}")

        return "\n".join(lines)
    except Exception:
        return ""


_HOOKS_CONTEXT = _load_hooks_context()


# ════════════════════════════════════════════════════════════════════════════
# TRANSCRIPTION (AssemblyAI nano - ~5-15s)
# ════════════════════════════════════════════════════════════════════════════
def transcribe_audio(audio_path: str) -> Optional[str]:
    """Transcribe audio using AssemblyAI (nano model = fastest)."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        return None
    try:
        import assemblyai as aai
        aai.settings.api_key = api_key
        config = aai.TranscriptionConfig(
            language_code="fr",
            speech_model=aai.SpeechModel.nano,
        )
        result = aai.Transcriber().transcribe(audio_path, config=config)
        if result.status == aai.TranscriptStatus.error:
            return None
        return result.text
    except Exception:
        return None


# ════════════════════════════════════════════════════════════════════════════
# ÉTAPE 1 : VISION (Mistral Pixtral — frames uniquement, prompt minimal, rapide)
# ════════════════════════════════════════════════════════════════════════════
VISION_PROMPT = """Tu es expert vision pour TikTok Shop. Tu DOIS regarder les images et retourner UNIQUEMENT du JSON valide en français.

Analyse rapide des frames extraites de la vidéo TikTok :

1. PRODUIT : décris ce que tu vois (forme, couleur, texture, contexte d'usage). Identifie le PRODUIT PRINCIPAL.
2. CONFIANCE détection (0.6 à 1.0) :
   - 0.95-1.0 : visible plusieurs plans, sans ambiguïté
   - 0.85-0.94 : clair mais 1 plan
   - 0.75-0.84 : probable, doutes mineurs
   - 0.65-0.74 : incertain
3. QUALITÉ VISUELLE (0-100) : lumière, cadrage, netteté, esthétique
4. FORMAT VISUEL (0-100) : variation des plans, montage (lent/moyen/rapide), supports utilisés (📋tableaux, 📱écrans, ✏️texte, 🎬cuts, 👋gestuelle, 🎯objets)
5. HOOK VISUEL (0-100) : la 1ère frame est-elle stop-scroll ? Stimulation visuelle 1-10.
6. PRIX VISIBLE : si tu vois un prix à l'écran (€, $, USD, EUR), note-le.

RETOUR JSON UNIQUEMENT, structure exacte :
{
  "description_visuelle": "<2 phrases décrivant ce que tu vois>",
  "produit": "<nom du produit principal>",
  "confiance_detection": <0.6-1.0>,
  "prix_visible": "<valeur si visible, sinon 'non visible'>",
  "qualite_visuelle_score": <0-100>,
  "format_visuel_score": <0-100>,
  "format_visuel_supports": ["<>"],
  "format_visuel_rythme": "<lent/moyen/rapide>",
  "hook_visuel_score": <0-100>,
  "stimulation_visuelle": <1-10>,
  "elements_visuels_remarquables": ["<>", "<>"]
}"""


def _mistral_call(api_key: str, model: str, content_or_messages, timeout: float = 60.0) -> str:
    """Generic Mistral chat completion call. content_or_messages can be a list of content blocks or full messages."""
    import httpx
    if isinstance(content_or_messages, list) and content_or_messages and isinstance(content_or_messages[0], dict) and "role" in content_or_messages[0]:
        messages = content_or_messages
    else:
        messages = [{"role": "user", "content": content_or_messages}]

    response = httpx.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
        },
        timeout=timeout,
    )
    if not response.is_success:
        raise Exception(f"Mistral error {response.status_code}: {response.text[:300]}")
    return response.json()["choices"][0]["message"]["content"]


def _extract_json(raw: str) -> dict:
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        raise ValueError("No JSON in response")
    return json.loads(match.group())


def analyze_visual(frames_b64: List[str], product: Optional[str] = None) -> dict:
    """
    Vision pass : Mistral Pixtral analyse SEULEMENT les frames.
    Prompt minimal → réponse JSON courte → 10-15s au lieu de 60-90s.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise Exception("MISTRAL_API_KEY missing")

    content = []
    for i, frame in enumerate(frames_b64):
        label = "Accroche (1ère image)" if i == 0 else f"Image {i+1}"
        content.append({"type": "text", "text": label})
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{frame}"},
        })

    if product:
        content.append({"type": "text", "text": f"\n🎯 PRODUIT INDIQUÉ par l'utilisateur : {product}. Utilise pour valider ta détection."})

    content.append({"type": "text", "text": VISION_PROMPT})

    raw = _mistral_call(api_key, "pixtral-12b-2409", content, timeout=45.0)
    try:
        return _extract_json(raw)
    except Exception:
        return {
            "description_visuelle": "Analyse visuelle indisponible",
            "produit": product or "non détecté",
            "confiance_detection": 0.6,
            "qualite_visuelle_score": 50,
            "format_visuel_score": 50,
            "hook_visuel_score": 50,
        }


# ════════════════════════════════════════════════════════════════════════════
# ÉTAPE 2 : SYNTHÈSE (Mistral small / text-only — combine vision + transcript)
# ════════════════════════════════════════════════════════════════════════════
SYNTHESIS_PROMPT = """Tu es expert TikTok Shop & psychologie persuasion. Tu reçois UNE analyse visuelle déjà faite + un transcript audio + contexte marché. Tu dois produire le JSON FINAL complet d'analyse. Langage probabiliste ("semble", "tend à"). FRANÇAIS PUR. JSON UNIQUEMENT.

INSTRUCTIONS :
- Réutilise les scores visuels fournis (qualite_visuelle, format_visuel, hook_visuel) — NE LES RECALCULE PAS, recopie-les
- Évalue les 5 dimensions textuelles à partir du transcript : rétention, mécanismes vente, positionnement, émotion, conversion shop, algorithme
- Identifie le produit (utilise vision + transcript)
- Score global = moyenne pondérée

DIMENSIONS À NOTER :
1️⃣ HOOK /100 (utilise hook_visuel_score + analyse transcript des 5 premiers mots)
2️⃣ RÉTENTION /100 — boucles ouvertes, cliffhangers, progression
3️⃣ MÉCANISMES VENTE /100 — biais (🎓autorité, 👥preuve sociale, ⏳rareté, 💸accessibilité, 🔥FOMO, ✅validation, 🌟aspiration, 🔄transformation), type vente (🎯directe/🎭indirecte/💝émotionnelle/📚éducative/🌅aspirationnelle/📖storytelling)
4️⃣ POSITIONNEMENT /100 — rôle (👨‍🏫expert, 🧙mentor, 🤝ami, 🎯preuve vivante, 🧪expérimentateur, 🏃outsider), accessibilité 1-10, crédibilité 1-10
5️⃣ FORMAT VISUEL /100 — copie format_visuel_score de la vision
6️⃣ ÉMOTION /100 — 🌟espoir, 😤frustration, 🎯ambition, 😰peur, 😍envie, 🤔curiosité, ⚡urgence, ✅validation
7️⃣ CONVERSION SHOP /100 — CTAs visibles/implicites, ce qu'on vend vraiment
8️⃣ ALGORITHME /100 — signaux rétention/partage/commentaires/sauvegarde

FLUX VENTE STRUCTURE : 1.Accroche(0-5s) → 2.Problème(5-20s) → 3.Solution(20-45s) → 4.Produit(45-60s) → 5.CTA(60+s)

RETOUR JSON OBLIGATOIRE (STRUCTURE EXACTE) :
{"analyse_8_dimensions": {"hook": {"score": <0-100>, "categorie": "<💰ARGENT|❌ERREUR|🎯OPPORTUNITÉ|⚡SIMPLICITÉ|🚀RÉSULTAT|😤FRUSTRATION|🤯CHOC|🔬RÉVÉLATION>", "feedback": "<>"}, "retention": {"score": <0-100>, "boucles_ouvertes": <0-10>, "feedback": "<>"}, "mecanismes_vente": {"score": <0-100>, "biais_principal": "<>", "nb_biais": <1-4>, "type_vente": "<>", "feedback": "<>"}, "positionnement": {"score": <0-100>, "role": "<>", "accessibilite": <1-10>, "credibilite": <1-10>, "relatable": "<oui/non>", "feedback": "<>"}, "format_visuel": {"score": <0-100>, "supports_utilises": ["<>"], "variation_montage": "<lent/moyen/rapide>", "feedback": "<>"}, "emotion_dominante": {"score": <0-100>, "emotion": "<>", "intensite": <1-10>, "transitions_efficaces": ["<>"], "feedback": "<>"}, "conversion_shop": {"score": <0-100>, "cta_visibles": <0-3>, "cta_implicites": <0-3>, "ce_que_vend": "<>", "engagements": {"commentaires": "<oui/non>", "sauvegardes": "<oui/non>", "partage": "<oui/non>"}, "feedback": "<>"}, "algorithme": {"score": <0-100>, "signaux_forts": ["<>"], "moments_cles": ["<>"], "potentiel_push": "<faible/moyen/fort>", "feedback": "<>"}, "score_persuasion_global": <0-100>}, "scores_legacy": {"accroche": {"note": <0-10>, "commentaire": "<>"}, "discours": {"note": <0-10>, "commentaire": "<>"}, "qualite_visuelle": {"note": <0-10>, "commentaire": "<>"}, "visibilite_produit": {"note": <0-10>, "commentaire": "<>"}, "call_to_action": {"note": <0-10>, "commentaire": "<>"}, "energie_dynamisme": {"note": <0-10>, "commentaire": "<>"}, "credibilite_confiance": {"note": <0-10>, "commentaire": "<>"}}, "detection": {"produit": "<nom>", "prix_estime": "<prix EUR ou non détecté>", "prix_rentable": <true/false>, "hook_type": "<>", "hook_force": <0-10>, "confiance_detection": <0.6-1.0>}, "viral_potential": {"score": <0-100>, "facteur_prix": "<très bas <15€|bon 15-40€|élevé 40-100€|premium 100€+>", "explication": "<2-3 lignes>"}, "structure_vente": {"accroche": {"present": <true/false>, "score": <0-10>, "hook_type": "<>", "feedback": "<>"}, "probleme": {"present": <true/false>, "score": <0-10>, "problem_stated": "<>", "clarity": <0-10>, "feedback": "<>"}, "solution": {"present": <true/false>, "score": <0-10>, "how_solved": "<>", "product_link": "<yes/no>", "feedback": "<>"}, "produit": {"present": <true/false>, "score": <0-10>, "shown_adequately": "<yes/no/partially>", "demo_quality": "<none/basic/good/excellent>", "feedback": "<>"}, "cta": {"present": <true/false>, "score": <0-10>, "cta_type": "<>", "clarity": <0-10>, "persuasion": "<faible/moyen/fort>", "feedback": "<>"}, "ordre_naturel": <true/false>, "transitions": "<fluides/abruptes/absentes>", "score_structure": <0-100>}, "score_global": <0-100>, "points_forts": ["<1>", "<2>", "<3>"], "points_ameliorer": ["<1>", "<2>", "<3>"], "recommendations_hooks": {"hook_type_propose": "<>", "raison": "<1-2 phrases>", "exemples_concrets": ["<>", "<>", "<>"]}, "plan_reproduction": {"hook_similaire": {"structure": "<>", "variables": "<>", "exemple": "<>"}, "mecanique_montage": {"rythme": "<>", "transitions": "<>", "elements_visuels": ["<>"]}, "cta_optimise": {"type": "<direct/implicite/emotionnel>", "placement": "<debut/milieu/fin>", "formulation": "<>"}, "angle_shop": {"produit": "<>", "storytelling": "<>", "emotion": "<>"}}, "conseils_concrets": ["<1>", "<2>", "<3>", "<4>"], "ameliorations_prioritaires": [{"rang": 1, "action": "<>", "impact": "<>"}, {"rang": 2, "action": "<>", "impact": "<>"}, {"rang": 3, "action": "<>", "impact": "<>"}], "verdict": "<3-4 phrases langage probabiliste>", "disclaimer_realisme": "Analyse décortique persuasion + signaux algo. TikTok surprend — mauvaises vidéos vendent bien, excellentes floppent. Repère stratégique, pas certitude."}"""


def _format_market_context(market: dict) -> str:
    try:
        lines = ["\n================================================================================",
                 "DONNÉES MARCHÉ TEMPS RÉEL (TikTok Shop FR)",
                 "================================================================================"]
        top = market.get("top_products", [])
        if top:
            lines.append("\nTOP PRODUITS EN VENTE:")
            for p in top[:5]:
                name = p.get('title') or p.get('name', '?')
                lines.append(f"- {name} — {p.get('sold_count', p.get('sales', '?'))} ventes | {p.get('category', '?')}")
        trending = market.get("trending", [])
        if trending:
            lines.append("\nPRODUITS TRENDING:")
            for p in trending[:5]:
                name = p.get('title') or p.get('name', '?')
                lines.append(f"- {name} — {p.get('growth_percent', p.get('trend_momentum', '?'))}")
        return "\n".join(lines)
    except Exception:
        return ""


def synthesize_analysis(
    visual_result: dict,
    transcript: Optional[str],
    market_context: Optional[dict] = None,
    product: Optional[str] = None,
) -> dict:
    """
    Synthèse text-only via mistral-small : combine vision + transcript + marché.
    Bcp + rapide que pixtral car pas d'images à traiter (8-15s vs 30-60s).
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise Exception("MISTRAL_API_KEY missing")

    parts = [SYNTHESIS_PROMPT]

    parts.append("\n\n================================================================================")
    parts.append("ANALYSE VISUELLE DÉJÀ EFFECTUÉE (réutilise ces scores tel quel) :")
    parts.append("================================================================================")
    parts.append(json.dumps(visual_result, ensure_ascii=False, indent=2))

    if transcript and transcript.strip():
        parts.append("\n\n================================================================================")
        parts.append("TRANSCRIPT AUDIO DE LA VIDÉO :")
        parts.append("================================================================================")
        parts.append(transcript)
    else:
        parts.append("\n\nNOTE : pas de transcript audio disponible (vidéo muette ou audio absent). Base ton analyse uniquement sur la vision.")

    if product:
        parts.append(f"\n\n🎯 PRODUIT INDIQUÉ PAR L'UTILISATEUR : {product}")

    if market_context:
        parts.append(_format_market_context(market_context))

    parts.append(_HOOKS_CONTEXT)

    full_prompt = "\n".join(parts)

    raw = _mistral_call(
        api_key,
        "mistral-small-latest",   # text-only, ~3x plus rapide que pixtral
        full_prompt,
        timeout=70.0,
    )
    try:
        parsed = _extract_json(raw)
    except Exception:
        return {"error": "Impossible de parser la réponse IA", "raw": raw[:1000]}

    return _post_process(parsed, market_context, visual_result)


# ════════════════════════════════════════════════════════════════════════════
# POST-PROCESSING (calculs prix/conversion côté serveur, plus fiable que IA)
# ════════════════════════════════════════════════════════════════════════════
def _post_process(parsed: dict, market_context: Optional[dict], visual_result: dict) -> dict:
    """Applique la logique business prix/conversion + injection des données marché."""
    # Extraire structure_vente au top level
    if "structure_vente" in parsed:
        sv = parsed["structure_vente"]
        parsed["structure_score"] = sv.get("score_structure", 0)
        parsed["etapes_manquantes"] = sv.get("etapes_manquantes", [])
        parsed["etapes_faibles"] = sv.get("etapes_faibles", [])

    # Score global - calculer si manquant
    score = parsed.get("score_global")
    if not score or score == 0:
        scores_list = []
        if "scores" in parsed:
            for v in parsed["scores"].values():
                if isinstance(v, dict) and "note" in v:
                    scores_list.append(v["note"] * 10)
        if "analyse_8_dimensions" in parsed:
            for v in parsed["analyse_8_dimensions"].values():
                if isinstance(v, dict) and "score" in v:
                    scores_list.append(v["score"])
        if "viral_potential" in parsed and isinstance(parsed["viral_potential"], dict):
            if "score" in parsed["viral_potential"]:
                scores_list.append(parsed["viral_potential"]["score"])
        if scores_list:
            score = round(sum(scores_list) / len(scores_list))
            parsed["score_global"] = score
        else:
            score = 0

    # Prix → conseil conversion
    prix_str = parsed.get("detection", {}).get("prix_estime", "") or ""
    prix_num = 0.0
    prix_match = re.search(r"(\d+(?:[.,]\d+)?)", str(prix_str))
    if prix_match:
        prix_num = float(prix_match.group(1).replace(",", "."))

    if prix_num > 0:
        if prix_num <= 40:
            cat = "economique"
            if score >= 70:
                conseil = (f"Potentiel de conversion rapide probable à {prix_str}. "
                           "La gamme de prix semble favorable et la vidéo laisse penser à de bons résultats. "
                           "À confirmer sur J3/J7 — l'algo reste imprévisible.")
                niveau, delai, champion = "rapide", "j7", False
            else:
                conseil = (f"Potentiel de conversion limité malgré le prix accessible ({prix_str}). "
                           "Une vidéo moins convaincante réduit les chances, même à bas prix. "
                           "Teste quand même sur J3 — TikTok peut surprendre.")
                niveau, delai, champion = "moyen", "j7", False
        elif prix_num <= 100:
            cat = "moyen"
            if score >= 75:
                conseil = (f"Bon potentiel apparent, mais à {prix_str} la conversion tend à être lente. "
                           "J7 ne sera probablement pas représentatif — attends J+30 pour conclure.")
                niveau, delai, champion = "moyen", "j30", False
            elif score >= 60:
                conseil = (f"Potentiel modéré. À {prix_str}, les premiers jours peuvent être trompeurs. "
                           "Attends J+30 avant de conclure sur les performances.")
                niveau, delai, champion = "moyen", "j30", False
            else:
                conseil = (f"Potentiel limité. Prix moyen + vidéo moyenne = combinaison difficile. "
                           "Peu probable mais l'algo peut surprendre. Reste vigilant si ça décolle en J3.")
                niveau, delai, champion = "lent", "j30", False
        else:  # > 100
            cat = "premium"
            if score >= 90:
                conseil = (f"Potentiel fort malgré le prix premium ({prix_str}). "
                           "La structure et l'accroche semblent solides, ce qui peut compenser le prix élevé. "
                           "Reste prudent — même une excellente vidéo ne garantit rien.")
                niveau, delai, champion = "moyen", "j30", True
            elif score >= 75:
                conseil = (f"Potentiel modéré. À {prix_str}, la conversion sera très lente. "
                           "Attends absolument J+30 — J7 ne veut rien dire à ce niveau de prix.")
                niveau, delai, champion = "lent", "j30", False
            else:
                conseil = (f"Potentiel faible. Prix premium + vidéo moyenne = combinaison difficile. "
                           "J+30 sera décisif, mais les attentes doivent rester modérées.")
                niveau, delai, champion = "lent", "j30", False
    else:
        cat = "inconnu"
        conseil = ("Prix non détecté — impossible d'évaluer le potentiel de conversion avec précision. "
                   "Analyse la vidéo sur J7 pour les produits < 40€, J30 pour les autres.")
        niveau, delai, champion = "inconnu", "j7", False

    pc = parsed.setdefault("prix_conversion", {})
    pc["montant"] = prix_num if prix_num > 0 else None
    pc["categorie"] = cat
    pc.setdefault("potentiel_conversion", {}).update({
        "niveau": niveau,
        "temps_attendre": delai,
        "confiance_prechampion": champion,
    })
    pc["conseil_prix"] = conseil

    # Injecter les données marché si dispo
    if market_context:
        parsed["donnees_marche"] = {
            "top_products": market_context.get("top_products", [])[:5],
            "trending": market_context.get("trending", [])[:5],
            "top_creators": market_context.get("top_creators", [])[:3],
        }

    # Expose visual_result en debug (optionnel)
    parsed["_visual_pass"] = {
        "produit": visual_result.get("produit"),
        "confiance": visual_result.get("confiance_detection"),
        "description": visual_result.get("description_visuelle"),
    }

    return parsed


# ════════════════════════════════════════════════════════════════════════════
# BACKWARD COMPAT : ancienne fonction monolithique (fallback)
# ════════════════════════════════════════════════════════════════════════════
def analyze_video(
    frames_b64: List[str],
    transcript: Optional[str] = None,
    market_context: Optional[dict] = None,
    product: Optional[str] = None,
) -> dict:
    """
    Compat : exécute vision puis synthèse en séquence (utile pour tests/fallback).
    Pour le vrai parallélisme, utiliser analyze_visual() et synthesize_analysis()
    directement avec asyncio.gather() depuis main.py.
    """
    visual = analyze_visual(frames_b64, product)
    return synthesize_analysis(visual, transcript, market_context, product)
