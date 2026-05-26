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


PROMPT = """Expert: psychologie persuasion, contenu viral, TikTok Shop. Analyse = SYSTÈME DE PERSUASION. Sois nuancé, langage probabiliste ("semble", "tend à", "probablement"). Retourne UNIQUEMENT du JSON valide, français pur.

1️⃣ HOOK (0-3s) /100 — 💰ARGENT | ❌ERREUR | 🎯OPPORTUNITÉ | ⚡SIMPLICITÉ | 🚀RÉSULTAT | 😤FRUSTRATION | 🤯CHOC | 🔬RÉVÉLATION
Évalue: type interruption (visuel/verbal/émotionnel/curiosité) | promesse implicite/explicite | rapidité entrée | densité info 3s | stimulation visuelle (1-10) | élément perturbateur
Score: 90-100 (stop-scroll immédiat) | 70-89 (très accrocheur) | 50-69 (correct) | <50 (faible)

2️⃣ RÉTENTION /100
Évalue: fréquence changements plans | transitions/zooms/mouvements | variations ton/texte/son | boucles ouvertes | progression étapes | cliffhangers
Score: 90-100 (impossible partir) | 70-89 (très bonne) | 50-69 (moyenne) | <50 (trop linéaire)

3️⃣ MÉCANISMES VENTE /100 — Biais: 🎓AUTORITÉ | 👥PREUVE SOCIALE | ⏳RARETÉ/URGENCE | 💸ACCESSIBILITÉ | 🧩SIMPLICITÉ | 🔥FOMO | ✅VALIDATION | 🌟ASPIRATION | 🔄TRANSFORMATION
Évalue: mécanisme principal (1) | nb biais (1-4) | type vente (🎯DIRECTE | 🎭INDIRECTE | 💝ÉMOTIONNELLE | 📚ÉDUCATIVE | 🌅ASPIRATIONNELLE | 📖STORYTELLING)
Score: 90-100 (multiples biais combinés) | 70-89 (2-3 biais) | 50-69 (1 biais) | <50 (trop direct)

4️⃣ POSITIONNEMENT /100 — Rôles: 👨‍🏫EXPERT | 🧙MENTOR | 🤝AMI | 🎯PREUVE VIVANTE | 🧪EXPÉRIMENTATEUR | 🏃OUTSIDER | 👤PERSONNE COMME TOI
Évalue: accessibilité (1-10) | crédibilité (1-10) | distance émotionnelle (proche/distant) | relatable (oui/non)
Score: 90-100 (clair + connexion) | 70-89 (bon, légère friction) | 50-69 (flou) | <50 (pas projection)

5️⃣ FORMAT VISUEL /100 — 📋Tableaux | 📱Écrans | ✏️Texte/Captions | 🎬Montage (cuts/zooms) | 👋Gestuelle | 🎯Objets physiques
Évalue: supports utilisés | comment augmentent crédibilité/compréhension/watch-time
Score: 90-100 (parfaitement intégrés) | 70-89 (bons, manque variété) | 50-69 (basique) | <50 (amateur)

6️⃣ ÉMOTION DOMINANTE /100 — 🌟ESPOIR | 😤FRUSTRATION | 🎯AMBITION | 😰PEUR | 😍ENVIE | 🤔CURIOSITÉ | ⚡URGENCE | ✅VALIDATION
Évalue: intensité (1-10) | fréquence stimuli | rapidité connexion | cohérence début-fin
Transitions efficaces: Frustration→Espoir (très efficace) | Curiosité→Satisfaction (bonne boucle) | Peur→Solution (conversion forte)
Score: 90-100 (forte, claire, exploitée) | 70-89 (identifiable, impactante) | 50-69 (présente, diluée) | <50 (neutre)

7️⃣ CONVERSION SHOP /100 — CTAs: VISIBLES | IMPLICITES | ÉMOTIONNELS. Vend: 📦PRODUIT | 🌅MODE DE VIE | 💼OPPORTUNITÉ | 👤IDENTITÉ | 🔄TRANSFORMATION
Évalue: CTAs (visibles, implicites) | ce que vend vraiment | pushes engagement (commentaires/sauvegardes/partage/suivi/revisite)
Score: 90-100 (multiples fluides) | 70-89 (clairs, bien placés) | 50-69 (présent, faible) | <50 (absent/maladroit)

8️⃣ ALGORITHME /100 — Signaux: ⏱️Rétention | 💎Densité valeur | 🔁Structure addictive | 🎁Micro-récompenses | 📖Tension narrative | 💬Commentaires | 🔄Partage. Moments: 🎯REWATCH | 💬COMMENTAIRES | 💾SAUVEGARDES | 📤PARTAGE
Score: 90-100 (tous signaux optimisés) | 70-89 (plusieurs forts) | 50-69 (basiques) | <50 (no push)

FLUX VENTE: 1.ACCROCHE(0-5s) → 2.PROBLÈME(5-20s) → 3.SOLUTION(20-45s) → 4.PRODUIT(45-60s) → 5.CTA(60+s)

🎯 IDENTIFICATION PRODUIT (CRITIQUE):
1. DÉCRIRE D'ABORD ce que tu VOIS dans CHAQUE image: formes, couleurs, textures, usage, contexte, actions
2. IDENTIFIER: "C'est clairement une [PRODUIT]" ou "Cela ressemble à un [PRODUIT] mais incertain"
3. CONFIANCE (0.6-1.0):
   - 0.95-1.0: Visible clairement, plusieurs plans, pas d'ambiguïté
   - 0.85-0.94: Clair mais un seul plan, ou léger détail flou
   - 0.75-0.84: Probable mais quelques doutes, image floue
   - 0.65-0.74: Incertain, ressemble à plusieurs produits
   - <0.65: Trop flou/ambigu
4. SI INCERTAIN: fournir 2-3 hypothèses avec % pour chacune
5. IGNORER les objets secondaires (main, décor) — focus PRODUIT PRINCIPAL

RETOUR JSON UNIQUEMENT:
{"analyse_8_dimensions": {"hook": {"score": <0-100>, "categorie": "<>", "feedback": "<>"}, "retention": {"score": <0-100>, "boucles_ouvertes": <0-10>, "feedback": "<>"}, "mecanismes_vente": {"score": <0-100>, "biais_principal": "<>", "nb_biais": <1-4>, "type_vente": "<>", "feedback": "<>"}, "positionnement": {"score": <0-100>, "role": "<>", "accessibilite": <1-10>, "credibilite": <1-10>, "relatable": "<oui/non>", "feedback": "<>"}, "format_visuel": {"score": <0-100>, "supports_utilises": ["<>"], "variation_montage": "<lent/moyen/rapide>", "feedback": "<>"}, "emotion_dominante": {"score": <0-100>, "emotion": "<>", "intensite": <1-10>, "transitions_efficaces": ["<>"], "feedback": "<>"}, "conversion_shop": {"score": <0-100>, "cta_visibles": <0-3>, "cta_implicites": <0-3>, "ce_que_vend": "<>", "engagements": {"commentaires": "<oui/non>", "sauvegardes": "<oui/non>", "partage": "<oui/non>"}, "feedback": "<>"}, "algorithme": {"score": <0-100>, "signaux_forts": ["<>"], "moments_cles": ["<>"], "potentiel_push": "<faible/moyen/fort>", "feedback": "<>"}, "score_persuasion_global": <0-100>}, "scores_legacy": {"accroche": {"note": <0-10>, "commentaire": "<>"}, "discours": {"note": <0-10>, "commentaire": "<>"}, "qualite_visuelle": {"note": <0-10>, "commentaire": "<>"}, "visibilite_produit": {"note": <0-10>, "commentaire": "<>"}, "call_to_action": {"note": <0-10>, "commentaire": "<>"}, "energie_dynamisme": {"note": <0-10>, "commentaire": "<>"}, "credibilite_confiance": {"note": <0-10>, "commentaire": "<>"}}, "detection": {"produit": "<nom ou non détecté>", "prix_estime": "<prix EUR ou non détecté>", "prix_rentable": <true/false>, "hook_type": "<>", "hook_force": <0-10>, "confiance_detection": <0.6-1.0>}, "viral_potential": {"score": <0-100>, "facteur_prix": "<très bas <15€ | bon 15-40€ | élevé 40-100€ | premium 100€+>", "explication": "<2-3 lignes>"}, "structure_vente": {"accroche": {"present": <true/false>, "score": <0-10>, "hook_type": "<>", "feedback": "<>"}, "probleme": {"present": <true/false>, "score": <0-10>, "problem_stated": "<>", "clarity": <0-10>, "feedback": "<>"}, "solution": {"present": <true/false>, "score": <0-10>, "how_solved": "<>", "product_link": "<yes/no>", "feedback": "<>"}, "produit": {"present": <true/false>, "score": <0-10>, "shown_adequately": "<yes/no/partially>", "demo_quality": "<none/basic/good/excellent>", "feedback": "<>"}, "cta": {"present": <true/false>, "score": <0-10>, "cta_type": "<>", "clarity": <0-10>, "persuasion": "<faible/moyen/fort>", "feedback": "<>"}, "ordre_naturel": <true/false>, "transitions": "<fluides/abruptes/absentes>", "score_structure": <0-100>}, "score_global": <0-100>, "points_forts": ["<1>", "<2>", "<3>"], "points_ameliorer": ["<1>", "<2>", "<3>"], "recommendations_hooks": {"hook_type_propose": "<>", "raison": "<1-2 phrases>", "exemples_concrets": ["<>", "<>", "<>"]}, "plan_reproduction": {"hook_similaire": {"structure": "<détail>", "variables": "<à adapter>", "exemple": "<>"}, "mecanique_montage": {"rythme": "<X cuts par Y sec>", "transitions": "<types>", "elements_visuels": ["<>"]}, "cta_optimise": {"type": "<direct/implicite/emotionnel>", "placement": "<debut/milieu/fin>", "formulation": "<>"}, "angle_shop": {"produit": "<>", "storytelling": "<>", "emotion": "<>"}}, "conseils_concrets": ["<1>", "<2>", "<3>", "<4>"], "ameliorations_prioritaires": [{"rang": 1, "action": "<>", "impact": "<>"}, {"rang": 2, "action": "<>", "impact": "<>"}, {"rang": 3, "action": "<>", "impact": "<>"}], "verdict": "<3-4 phrases langage probabiliste>", "disclaimer_realisme": "Analyse décortique persuasion + signaux algo. TikTok surprend — mauvaises vidéos vendent bien, excellentes floppent. Repère stratégique, pas certitude."}"""


def _format_market_context(market: dict) -> str:
    """Formate les données marché du scraper pour injection dans le prompt."""
    try:
        lines = ["\n================================================================================",
                 "DONNÉES MARCHÉ TEMPS RÉEL (TikTok Shop FR — dernières 6h)",
                 "================================================================================"]

        top = market.get("top_products", [])
        if top:
            lines.append("\nTOP PRODUITS EN VENTE (volume de ventes):")
            for p in top[:5]:
                lines.append(f"- {p.get('title','?')} — {p.get('sold_count','?')} ventes | {p.get('category','?')} | {p.get('current_price','?')}€")

        trending = market.get("trending", [])
        if trending:
            lines.append("\nPRODUITS TRENDING (croissance rapide):")
            for p in trending[:5]:
                lines.append(f"- {p.get('title','?')} — +{p.get('growth_percent','?')}% de ventes | {p.get('category','?')}")

        creators = market.get("top_creators", [])
        if creators:
            lines.append("\nCRÉATEURS SHOP FR LES PLUS ACTIFS:")
            for c in creators[:3]:
                lines.append(f"- @{c.get('handle','?')} ({c.get('followers','?')} followers) — spécialité: {c.get('primary_category','?')}")

        lines.append("\nUtilise ces données pour contextualiser ton analyse : le produit analysé est-il dans une catégorie tendance ? Son prix est-il compétitif par rapport aux top sellers ?")
        return "\n".join(lines)
    except Exception:
        return ""


def analyze_video(frames_b64: List[str], transcript: Optional[str] = None, market_context: Optional[dict] = None, product: Optional[str] = None) -> dict:
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

    if product:
        content.append({"type": "text", "text": f"\n🎯 PRODUIT À ANALYSER : {product}\nL'utilisateur spécifie que le produit analysé est : {product}. Utilise cette information pour affiner ton identification du produit, valider ou corriger ta détection automatique, et adapter tes conseils de coaching à ce contexte spécifique."})

    market_str = _format_market_context(market_context) if market_context else ""
    content.append({"type": "text", "text": PROMPT + _HOOKS_CONTEXT + market_str})

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
            score    = parsed.get("score_global")

            # Si Mistral n'a pas fourni score_global, le calculer à partir des autres scores
            if not score or score == 0:
                scores_list = []

                # Scores legacy (0-10, convert to 0-100)
                if "scores" in parsed:
                    for key, val in parsed["scores"].items():
                        if isinstance(val, dict) and "note" in val:
                            scores_list.append(val["note"] * 10)

                # Scores 8 dimensions (already 0-100)
                if "analyse_8_dimensions" in parsed:
                    for key, val in parsed["analyse_8_dimensions"].items():
                        if isinstance(val, dict) and "score" in val:
                            scores_list.append(val["score"])

                # Viral potential score
                if "viral_potential" in parsed:
                    vp = parsed["viral_potential"]
                    if isinstance(vp, dict) and "score" in vp:
                        scores_list.append(vp["score"])

                # Structure vente score
                if "structure_vente" in parsed:
                    sv = parsed["structure_vente"]
                    if isinstance(sv, dict) and "score_structure" in sv:
                        scores_list.append(sv["score_structure"])

                # Calculer la moyenne
                if scores_list:
                    score = round(sum(scores_list) / len(scores_list))
                    parsed["score_global"] = score
                    print(f"[ANALYZE] Calculated score_global={score} from {len(scores_list)} scores")
                else:
                    score = 0
                    print("[ANALYZE] Warning: Could not calculate score_global, set to 0")

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

            # Ajouter les données marché Echotik si disponibles
            if market_context:
                parsed["donnees_marche"] = {
                    "top_products": market_context.get("top_products", [])[:5],
                    "trending": market_context.get("trending", [])[:5],
                    "top_creators": market_context.get("top_creators", [])[:3],
                }

            return parsed
        except json.JSONDecodeError:
            pass

    return {"error": "Impossible de parser la réponse IA", "raw": raw}
