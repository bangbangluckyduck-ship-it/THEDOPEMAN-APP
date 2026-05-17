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


PROMPT = """Tu es un expert en marketing TikTok Shop avec 8 ans d'expérience en conversion et ventes directes.

IMPORTANT — NUANCE ET HUMILITÉ:
Sois nuancé dans tes analyses. On peut toujours se tromper.
Des vidéos "mauvaises" vendent très bien, des "excellentes" floppent. L'algo TikTok est imprévisible.
Utilise du langage probabiliste ("semble", "laisse penser", "tend à", "probablement") — jamais affirmatif.

Analyse cette vidéo TikTok Shop.

RÈGLES STRICTES:
1. Rédige UNIQUEMENT en français pur, zéro anglicisme
2. Retourne UNIQUEMENT un JSON valide parsable
3. Pas de texte avant ou après le JSON

================================================================================
PHASE 1: ANALYSE QUALITÉ (7 CRITÈRES)
================================================================================

Score chaque critère sur 10:
1. "accroche" → Force des 3 premières secondes
2. "discours" → Clarté message + argumentation + structure vente
3. "qualite_visuelle" → Éclairage, cadrage, stabilité
4. "visibilite_produit" → Produit bien montré? Gros plans? Angles?
5. "call_to_action" → Appel à l'action présent, clair, persuasif
6. "energie_dynamisme" → Rythme, énergie créateur, engagement
7. "credibilite_confiance" → Authenticité, preuves sociales

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
PHASE 6: ANALYSE STRUCTURE DE VENTE (NOUVEAU)
================================================================================

La vidéo DOIT suivre ce flux naturel pour convertir:
1. ACCROCHE (0-5sec) → Capture l'attention immédiatement
2. PROBLÈME (5-20sec) → Identifie un point de douleur spécifique
3. SOLUTION (20-45sec) → Montre comment le produit résout
4. PRODUIT (45-60sec) → Démonstration/présentation du produit
5. CTA (60+sec) → Appel à l'action clair et persuasif

ÉVALUE CHAQUE ÉTAPE:

Pour ACCROCHE: present (true/false), score (0-10), hook_type (type détecté), feedback (est-ce percutant?)
Pour PROBLÈME: present (true/false), score (0-10), problem_stated (le problème identifié), clarity (0-10), feedback (clair et relatable?)
Pour SOLUTION: present (true/false), score (0-10), how_solved (comment le produit résout), product_link (yes/no), feedback (crédible et spécifique?)
Pour PRODUIT: present (true/false), score (0-10), shown_adequately (yes/no/partially), demo_quality (none/basic/good/excellent), feedback (angles suffisants?)
Pour CTA: present (true/false), score (0-10), cta_type (type identifié), clarity (0-10), persuasion (faible/moyen/fort), feedback (arrive au bon moment?)

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
  "structure_vente": {
    "accroche": {
      "present": <true/false>,
      "score": <0-10>,
      "hook_type": "<type détecté>",
      "feedback": "<est-ce percutant?>"
    },
    "probleme": {
      "present": <true/false>,
      "score": <0-10>,
      "problem_stated": "<le problème identifié>",
      "clarity": <0-10>,
      "feedback": "<est-ce clair et relatable?>"
    },
    "solution": {
      "present": <true/false>,
      "score": <0-10>,
      "how_solved": "<comment le produit résout>",
      "product_link": "<yes/no>",
      "feedback": "<la solution est-elle crédible?>"
    },
    "produit": {
      "present": <true/false>,
      "score": <0-10>,
      "shown_adequately": "<yes/no/partially>",
      "demo_quality": "<none/basic/good/excellent>",
      "feedback": "<angles suffisants? Démonstration claire?>"
    },
    "cta": {
      "present": <true/false>,
      "score": <0-10>,
      "cta_type": "<type identifié>",
      "clarity": <0-10>,
      "persuasion": "<faible/moyen/fort>",
      "feedback": "<le CTA arrive au bon moment?>"
    },
    "ordre_naturel": <true/false>,
    "transitions": "<fluides/abruptes/absentes>",
    "etapes_presentes": ["accroche", "probleme", "solution", "produit", "cta"],
    "etapes_manquantes": [],
    "etapes_faibles": [],
    "score_structure": <0-100>
  },
  "score_global": <0-100>,
  "points_forts": ["<1>", "<2>", "<3>", "<4>"],
  "points_ameliorer": ["<1>", "<2>", "<3>"],
  "recommendations_hooks": {
    "hook_type_propose": "<meilleur type>",
    "raison": "<pourquoi (1-2 phrases)>",
    "exemples_concrets": ["<exemple 1>", "<exemple 2>", "<exemple 3>"]
  },
  "prix_conversion": {
    "montant": <prix en EUR ou null>,
    "categorie": "<economique | moyen | premium>",
    "potentiel_conversion": {
      "niveau": "<rapide | moyen | lent>",
      "description": "<texte nuancé basé sur prix + score vidéo>",
      "temps_attendre": "<j7 | j30>",
      "confiance_prechampion": <true/false>
    },
    "conseil_prix": "<conseil contextuel et nuancé sur le timing d'évaluation>"
  },
  "conseils_concrets": ["<1>", "<2>", "<3>", "<4>"],
  "ameliorations_structure": [
    "<conseil 1 sur l'ordre/flux>",
    "<conseil 2 sur étapes manquantes>",
    "<conseil 3 sur transitions>"
  ],
  "disclaimer_realisme": "Cette analyse est un guide, pas une certitude. L'algo TikTok surprend toujours : des vidéos considérées mauvaises vendent bien, des excellentes floppent. Utilise ces données comme repère, pas comme vérité absolue.",
  "verdict": "<Résumé réaliste 3-4 phrases avec langage probabiliste : potentiel apparent? Point faible principal? Priorité? Refaire ou tester?>"
}

IMPORTANT: JSON uniquement, pas de markdown, français pur, langage probabiliste."""


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
        timeout=85.0,
    )

    if not response.is_success:
        raise Exception(f"OpenRouter error {response.status_code}: {response.text[:300]}")

    raw = response.json()["choices"][0]["message"]["content"]

    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            parsed = json.loads(match.group())

            # Extraire les champs structure au niveau racine
            if "structure_vente" in parsed:
                sv = parsed["structure_vente"]
                parsed["structure_score"]   = sv.get("score_structure", 0)
                parsed["etapes_manquantes"] = sv.get("etapes_manquantes", [])
                parsed["etapes_faibles"]    = sv.get("etapes_faibles", [])

            # Logique humanisée prix/conversion (côté serveur, plus fiable qu'IA)
            prix_str = parsed.get("detection", {}).get("prix_estime", "") or ""
            score    = parsed.get("score_global", 0) or 0

            # Extraire la valeur numérique du prix
            prix_num = 0.0
            prix_match = re.search(r"(\d+(?:[.,]\d+)?)", str(prix_str))
            if prix_match:
                prix_num = float(prix_match.group(1).replace(",", "."))

            # Calcul du conseil nuancé
            if prix_num > 0:
                if prix_num <= 40:
                    cat = "economique"
                    if score >= 70:
                        conseil = (f"Potentiel de conversion rapide probable à {prix_str}. "
                                   "La gamme de prix semble favorable et la vidéo laisse penser "
                                   "à de bons résultats. À confirmer sur J3/J7 — l'algo reste imprévisible.")
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
                                   "J7 ne sera probablement pas représentatif — attends J+30 pour tirer une conclusion.")
                        niveau, delai, champion = "moyen", "j30", False
                    elif score >= 60:
                        conseil = (f"Potentiel modéré. À {prix_str}, les premiers jours peuvent être trompeurs. "
                                   "Attends J+30 avant de conclure sur les performances.")
                        niveau, delai, champion = "moyen", "j30", False
                    else:
                        conseil = (f"Potentiel limité. Prix moyen + vidéo moyenne = combinaison difficile. "
                                   "Peu probable mais l'algo peut surprendre. Reste vigilant si ça décolle en J3.")
                        niveau, delai, champion = "lent", "j30", False

                else:  # prix > 100
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
                cat     = "inconnu"
                conseil = ("Prix non détecté — impossible d'évaluer le potentiel de conversion avec précision. "
                           "Analyse la vidéo sur J7 pour les produits < 40€, J30 pour les autres.")
                niveau, delai, champion = "inconnu", "j7", False

            # Injecter dans le résultat (remplace ou complète ce que l'IA a mis)
            pc = parsed.setdefault("prix_conversion", {})
            pc["montant"]   = prix_num if prix_num > 0 else None
            pc["categorie"] = cat
            pc.setdefault("potentiel_conversion", {}).update({
                "niveau":               niveau,
                "temps_attendre":       delai,
                "confiance_prechampion": champion,
            })
            pc["conseil_prix"] = conseil

            return parsed
        except json.JSONDecodeError:
            pass

    return {"error": "Impossible de parser la réponse IA", "raw": raw}
