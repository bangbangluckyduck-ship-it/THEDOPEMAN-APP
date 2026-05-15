from __future__ import annotations
import base64
import json
import os
import re
from typing import List, Optional


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


PROMPT = """Tu es un expert en marketing TikTok Shop avec 5 ans d'expérience à optimiser des vidéos de vente.

Analyse cette vidéo TikTok Shop (frames extraites{transcript_note}).

Évalue chaque critère sur 10 et retourne UNIQUEMENT un JSON valide, sans texte avant ou après :

{{
  "scores": {{
    "accroche": {{
      "note": <0-10>,
      "commentaire": "<analyse des premières secondes : est-ce que ça accroche immédiatement ?>"
    }},
    "discours": {{
      "note": <0-10>,
      "commentaire": "<clarté du message, argumentation, fluidité, structure de vente>"
    }},
    "qualite_visuelle": {{
      "note": <0-10>,
      "commentaire": "<éclairage, cadrage, stabilité, résolution, esthétique>"
    }},
    "visibilite_produit": {{
      "note": <0-10>,
      "commentaire": "<mise en valeur du produit, angles montrés, gros plans, démonstration>"
    }},
    "call_to_action": {{
      "note": <0-10>,
      "commentaire": "<présence, clarté et efficacité du CTA>"
    }},
    "energie_dynamisme": {{
      "note": <0-10>,
      "commentaire": "<rythme, énergie du créateur, engagement émotionnel>"
    }},
    "credibilite_confiance": {{
      "note": <0-10>,
      "commentaire": "<authenticité, professionnalisme, preuves sociales, confiance dégagée>"
    }}
  }},
  "score_global": <0-100>,
  "points_forts": ["<point fort 1>", "<point fort 2>", "<point fort 3>"],
  "points_ameliorer": ["<problème 1>", "<problème 2>", "<problème 3>"],
  "conseils_concrets": ["<conseil précis 1>", "<conseil 2>", "<conseil 3>", "<conseil 4>"],
  "verdict": "<résumé en 2-3 phrases du potentiel commercial et ce qu'il faut changer en priorité>"
}}"""


def analyze_video(frames_b64: List[str], transcript: Optional[str] = None) -> dict:
    import httpx

    api_key = os.getenv("GOOGLE_API_KEY")
    transcript_note = " + transcription audio" if transcript else ""

    parts = []
    for i, frame in enumerate(frames_b64):
        label = "🎯 Accroche (début)" if i == 0 else f"Frame {i+1}"
        parts.append({"text": label})
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": frame}})

    if transcript:
        parts.append({"text": f"\n\nTranscription audio :\n{transcript}"})

    parts.append({"text": PROMPT.format(transcript_note=transcript_note)})

    response = httpx.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent",
        params={"key": api_key},
        json={"contents": [{"parts": parts}]},
        timeout=30.0,
    )

    if not response.is_success:
        raise Exception(f"Gemini API error {response.status_code}: {response.text[:300]}")

    data = response.json()
    raw = data["candidates"][0]["content"]["parts"][0]["text"]

    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {"error": "Impossible de parser la réponse IA", "raw": raw}
