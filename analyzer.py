from __future__ import annotations
import json
import os
import re
from typing import List, Optional

import anthropic

PROMPT = """Tu es un expert en marketing TikTok Shop avec 5 ans d'expérience à optimiser des vidéos de vente.

Analyse cette vidéo TikTok Shop (frames extraites{transcript_note}).

Évalue chaque critère sur 10 et retourne UNIQUEMENT un JSON valide, sans texte avant ou après :

{{
  "scores": {{
    "accroche": {{
      "note": <0-10>,
      "commentaire": "<analyse des 3 premières secondes : est-ce que ça accroche immédiatement ?>"
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
  "points_forts": ["<ce qui fonctionne très bien 1>", "<point fort 2>", "<point fort 3>"],
  "points_ameliorer": ["<problème prioritaire 1>", "<problème 2>", "<problème 3>"],
  "conseils_concrets": [
    "<conseil actionnable très précis 1>",
    "<conseil 2>",
    "<conseil 3>",
    "<conseil 4>"
  ],
  "verdict": "<résumé en 2-3 phrases du potentiel commercial de cette vidéo et ce qu'il faut changer en priorité>"
}}"""


def transcribe_audio(audio_path: str) -> Optional[str]:
    """Try faster-whisper then openai-whisper. Returns None if neither available."""
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_path, language="fr")
        return " ".join(seg.text for seg in segments).strip()
    except ImportError:
        pass

    try:
        import whisper
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path, language="fr")
        return result["text"].strip()
    except ImportError:
        pass

    return None


def analyze_video(frames_b64: List[str], transcript: Optional[str] = None) -> dict:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    content: list = []

    for i, frame in enumerate(frames_b64):
        label = "🎯 Début (accroche)" if i < 3 else ("📢 Fin (CTA)" if i >= len(frames_b64) - 2 else f"Frame {i+1}")
        content.append({"type": "text", "text": f"**{label}**"})
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": frame},
        })

    transcript_note = ""
    if transcript:
        content.append({"type": "text", "text": f"\n\n**Transcription audio :**\n{transcript}"})
        transcript_note = " + transcription audio"

    content.append({"type": "text", "text": PROMPT.format(transcript_note=transcript_note)})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": content}],
    )

    raw = response.content[0].text
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        return json.loads(match.group())

    return {"error": "Impossible de parser la réponse IA", "raw": raw}
