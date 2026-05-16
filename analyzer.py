from __future__ import annotations
import base64
import json
import os
import re
from pathlib import Path
from typing import List, Optional


def _load_hooks_context() -> str:
    """Charge la base de données des accroches et retourne un résumé condensé pour le prompt."""
    try:
        db_path = Path(__file__).parent / "hooks_db.json"
        db = json.loads(db_path.read_text(encoding="utf-8"))

        lines = ["\n================================================================================",
                 "BASE DE DONNÉES ACCROCHES (utilise ces données pour tes recommandations)",
                 "================================================================================"]

        lines.append("\nPERFORMANCE DES TYPES D'ACCROCHE (score = taux de conversion moyen):")
        for cat in sorted(db["categories"], key=lambda c: c["performance_score"], reverse=True):
            warn = f" ⚠️ {cat['warning']}" if cat.get("warning") else ""
            lines.append(f"- {cat['nom']} (score {cat['performance_score']:.0%}): {cat['description']}{warn}")
            lines.append(f"  Exemples: {' | '.join(cat['examples'][:3])}")

        lines.append("\nRECOMMANDATIONS PAR CATÉGORIE PRODUIT:")
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


PROMPT = """Tu es un expert en marketing TikTok Shop avec 8 ans d'expérience en conversion.

RÈGLES STRICTES:
1. Rédige UNIQUEMENT en français pur (zéro anglicisme dans les textes générés)
2. Retourne UNIQUEMENT un JSON valide parsable
3. Pas de texte avant ou après le JSON
4. Tous les scores sur 10 (sauf score_global sur 100)

================================================================================
PHASE 1: ANALYSE QUALITÉ (7 CRITÈRES)
================================================================================

Évalue chaque critère sur 10 avec un commentaire court et pertinent.

================================================================================
PHASE 2: DÉTECTION AUTOMATIQUE
================================================================================

A) PRODUIT VENDU: nom exact ou "non détecté"
B) PRIX: prix exact en EUR si visible, sinon "non détecté". prix_rentable = true si 15-40€
C) TYPE D'ACCROCHE (1 seule catégorie):
   - "Controverse douce" → cadrage contre-intuitif ("n'achète pas")
   - "Urgence tarifaire" → stock/promo limité
   - "Réponse commentaire" → "vous me demandez"
   - "Curiosité" → "tu ne savais pas", "personne ne sait"
   - "Peur" → "tu risques de", "attention au piège"
   - "Témoignage" → before/after, preuve sociale
   - "Cas d'usage" → "voici comment l'utiliser"
   - "Tendance" → suit une tendance du moment
   - "Autre"
D) FORCE DE L'ACCROCHE (0-10)

================================================================================
PHASE 3: POTENTIEL VIRAL (0-100)
================================================================================

Basé sur: force de l'accroche, qualité visuelle, prix du produit, énergie.
Fournis un score, le facteur prix et une explication de 2-3 lignes.

================================================================================
PHASE 4: SCORE GLOBAL (0-100)
================================================================================

Moyenne pondérée: qualité vidéo 40% + potentiel viral 40% + force accroche 20%

================================================================================
PHASE 5: RECOMMANDATIONS D'ACCROCHES
================================================================================

Pour le produit détecté et le type d'accroche utilisé:
1. Propose le MEILLEUR type d'accroche pour ce produit
2. Explique POURQUOI en 1-2 phrases
3. Donne 3 EXEMPLES EXACTS réutilisables directement

================================================================================
RETOUR JSON (STRUCTURE EXACTE)
================================================================================

{
  "scores": {
    "accroche": {"note": <0-10>, "commentaire": "<...>"},
    "discours": {"note": <0-10>, "commentaire": "<...>"},
    "qualite_visuelle": {"note": <0-10>, "commentaire": "<...>"},
    "visibilite_produit": {"note": <0-10>, "commentaire": "<...>"},
    "call_to_action": {"note": <0-10>, "commentaire": "<...>"},
    "energie_dynamisme": {"note": <0-10>, "commentaire": "<...>"},
    "credibilite_confiance": {"note": <0-10>, "commentaire": "<...>"}
  },
  "detection": {
    "produit": "<nom ou non détecté>",
    "prix_estime": "<prix EUR ou non détecté>",
    "prix_rentable": <true/false>,
    "hook_type": "<catégorie>",
    "hook_force": <0-10>,
    "confiance_detection": <0.6-1.0>
  },
  "viral_potential": {
    "score": <0-100>,
    "facteur_prix": "<très bas <15€ | bon 15-40€ | élevé 40-100€ | premium 100€+>",
    "explication": "<2-3 lignes>"
  },
  "score_global": <0-100>,
  "points_forts": ["<1>", "<2>", "<3>", "<4>"],
  "points_ameliorer": ["<1>", "<2>", "<3>"],
  "recommendations_hooks": {
    "hook_type_propose": "<meilleur type>",
    "raison": "<pourquoi (1-2 phrases)>",
    "exemples_concrets": ["<exemple 1>", "<exemple 2>", "<exemple 3>"]
  },
  "conseils_concrets": ["<1>", "<2>", "<3>", "<4>"],
  "verdict": "<Résumé 3-4 phrases: potentiel viral? Problème principal? Priorité? Refaire ou publier?>"
}

IMPORTANT: JSON uniquement, pas de markdown, français pur, sois direct et applicable."""


def analyze_video(frames_b64: List[str], transcript: Optional[str] = None) -> dict:
    import httpx

    api_key = os.getenv("MISTRAL_API_KEY")

    content = []
    for i, frame in enumerate(frames_b64):
        label = "Accroche (début)" if i == 0 else f"Image {i+1}"
        content.append({"type": "text", "text": label})
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{frame}"},
        })

    if transcript:
        content.append({"type": "text", "text": f"\n\nTranscription audio :\n{transcript}"})

    content.append({"type": "text", "text": PROMPT + _HOOKS_CONTEXT})

    response = httpx.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "pixtral-12b-2409",
            "messages": [{"role": "user", "content": content}],
        },
        timeout=30.0,
    )

    if not response.is_success:
        raise Exception(f"OpenRouter error {response.status_code}: {response.text[:300]}")

    raw = response.json()["choices"][0]["message"]["content"]

    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {"error": "Impossible de parser la réponse IA", "raw": raw}
