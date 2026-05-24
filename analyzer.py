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


PROMPT = """Tu es un expert en psychologie de persuasion, neurosciences appliquées au contenu viral,
et stratégie TikTok Shop avec 8+ ans d'expérience en conversion directe.

Ton analyse DÉPASSE la simple description. Tu décortiques la vidéo comme un SYSTÈME DE PERSUASION.

IMPORTANT — NUANCE ET HUMILITÉ:
Sois nuancé. Des vidéos "mauvaises" vendent bien, des "excellentes" floppent. L'algo TikTok est imprévisible.
Utilise du langage probabiliste ("semble", "laisse penser", "tend à", "probablement") — jamais affirmatif.

RÈGLES STRICTES:
1. Rédige UNIQUEMENT en français pur, zéro anglicisme
2. Retourne UNIQUEMENT un JSON valide et parsable
3. Pas de texte avant ou après le JSON

================================================================================
FRAMEWORK D'ANALYSE — 8 DIMENSIONS DE PERSUASION
================================================================================

1. HOOK ANALYSIS (0-3 secondes) /100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analyse le MÉCANISME D'INTERRUPTION de scroll:
- Type d'interruption: visuelle / verbale / émotionnelle / curiosité
- Promesse implicite ou explicite
- Tension psychologique créée
- Catégorie du hook: 💰ARGENT | ❌ERREUR | 🎯OPPORTUNITÉ | ⚡SIMPLICITÉ | 🚀RÉSULTAT | 😤FRUSTRATION | 🤯CHOC | 🔬RÉVÉLATION

Évalue:
- Rapidité d'entrée dans le sujet (en secondes)
- Densité d'information dans les 3 premières secondes
- Niveau de stimulation visuelle (1-10)
- Présence d'un élément perturbateur

Score Hook /100:
- 90-100: Stop-scroll immédiat + promesse irrésistible
- 70-89: Très accrocheur, légère friction
- 50-69: Correct mais améliorable
- <50: Faible, risque de scroll

2. STRUCTURE DE RÉTENTION /100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analyse comment la vidéo MAINTIENT l'attention:
- Fréquence de changements de plans (toutes les X secondes)
- Éléments de stimulation: transitions, zooms, mouvements caméra
- Variations de ton vocal, texte à l'écran, effets sonores
- Boucles ouvertes (Open Loops): "attends de voir...", questions en suspens, teasings
- Progression par étapes, cliffhangers internes

Score Rétention /100:
- 90-100: Impossible de partir, boucles ouvertes maîtrisées
- 70-89: Très bonne rétention, quelques baisses
- 50-69: Rétention moyenne, risque de drop
- <50: Vidéo trop linéaire, scroll prévisible

3. MÉCANISMES DE VENTE (Biais Psychologiques) /100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Identifie les biais exploités:
- 🎓 AUTORITÉ: Expert reconnu, certifications, expertise
- 👥 PREUVE SOCIALE: Témoignages, "tout le monde l'utilise", données chiffrées
- ⏳ RARETÉ/URGENCE: Stock limité, édition limitée, "avant que ça parte"
- 💸 ACCESSIBILITÉ: Prix justifié, "moins cher que..."
- 🧩 SIMPLICITÉ: "Il suffit de...", démonstration en 1 geste
- 🔥 FOMO: "Ne fais pas comme ceux qui ratent..."
- ✅ VALIDATION SOCIALE: "Tu mérites", "les vrais [profession]"
- 🌟 ASPIRATION: Lifestyle, identité désirée
- 🔄 TRANSFORMATION: Avant/Après, réussite personnelle

Mécanisme principal détecté: [1 seul]
Nombre de biais combinés: [1-4]

Type de vente:
- 🎯 DIRECTE: "Achète maintenant"
- 🎭 INDIRECTE: Démo qui suscite envie
- 💝 ÉMOTIONNELLE: Connexion d'abord
- 📚 ÉDUCATIVE: Apprend puis recommande
- 🌅 ASPIRATIONNELLE: Style de vie
- 📖 STORYTELLING: Histoire inclut le produit

Score Vente /100:
- 90-100: Multiple biais combinés intelligemment
- 70-89: 2-3 biais bien exploités
- 50-69: 1 biais évident, manque de profondeur
- <50: Vente trop directe ou insuffisante

4. POSITIONNEMENT CRÉATEUR /100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quel rôle adopte le créateur?
- 👨‍🏫 EXPERT: Maîtrise technique apparente
- 🧙 MENTOR: Guide bienveillant
- 🤝 AMI: Conversation naturelle, intimité
- 🎯 PREUVE VIVANTE: "J'ai testé, voici le résultat"
- 🧪 EXPÉRIMENTATEUR: Curiosité partagée
- 🏃 OUTSIDER: "Voici ce qu'on te cache"
- 👤 PERSONNE COMME TOI: Relatable, accessible

Mesure:
- Accessibilité perçue (1-10)
- Crédibilité (1-10)
- Distance émotionnelle (proche vs distant)
- "Moi aussi je peux le faire": OUI/NON

Score Positionnement /100:
- 90-100: Positionnement clair + connexion immédiate
- 70-89: Bon positionnement, légère friction
- 50-69: Positionnement flou
- <50: Viewer ne se projette pas

5. FORMAT VISUEL /100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Évalue les supports visuels:
- 📋 Tableaux/Carnets: Effet "cours privé"
- 📱 Écrans: Effet "preuve digitale"
- ✏️ Sous-titres/Texte: Captions dynamiques, emojis
- 🎬 Montage: Cuts, zooms, transitions
- 👋 Gestuelle: Mains expressives, body language, regard caméra
- 🎯 Objets Physiques: Produit bien montré, démonstration

Comment les supports:
- Augmentent la crédibilité (preuve visuelle)
- Améliorent la compréhension
- Augmentent le watch time (variation)
- Créent un effet "cours privé"

Score Format /100:
- 90-100: Supports parfaitement intégrés et impactants
- 70-89: Bons supports, manque de variété
- 50-69: Format basique
- <50: Présentation amateur

6. ÉMOTION DOMINANTE /100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Identifie l'ÉMOTION PRINCIPALE exploitée:
- 🌟 ESPOIR: "C'est possible pour toi aussi"
- 😤 FRUSTRATION: "Tu en as marre de... voici la solution"
- 🎯 AMBITION: "Tu mérites le meilleur"
- 😰 PEUR: "Ne fais pas l'erreur que..."
- 😍 ENVIE: "Imagine si tu avais..."
- 🤔 CURIOSITÉ: "Le secret que personne ne dit"
- ⚡ URGENCE: "Il faut agir maintenant"
- ✅ VALIDATION: "Tu as raison de vouloir..."

Mesure:
- Intensité émotionnelle (1-10)
- Fréquence des stimuli émotionnels
- Rapidité de connexion (en secondes)
- Cohérence émotionnelle (début à fin)

Transitions émotionnelles efficaces:
- Frustration → Espoir = très efficace
- Curiosité → Satisfaction = bonne boucle
- Peur → Solution = conversion forte

Score Émotion /100:
- 90-100: Émotion forte, claire, parfaitement exploitée
- 70-89: Émotion identifiable et impactante
- 50-69: Émotion présente mais diluée
- <50: Vidéo trop neutre

7. CONVERSION TIKTOK SHOP /100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Identifie les CTAs:
- VISIBLES: "Lien dans le panier", "Clique sur le sac", "Achète avant fin du stock"
- IMPLICITES: Démonstration qui suscite envie
- ÉMOTIONNELS: "Tu mérites", "Offre-toi"

Ce que vend vraiment la vidéo:
- 📦 PRODUIT (bien matériel)
- 🌅 MODE DE VIE (identité associée)
- 💼 OPPORTUNITÉ (gain potentiel)
- 👤 IDENTITÉ (devenir quelqu'un)
- 🔄 TRANSFORMATION (état → meilleur état)

Mécanismes d'engagement:
- Push vers commentaires: OUI/NON
- Push vers sauvegardes: OUI/NON
- Push vers partage: OUI/NON
- Push vers suivi: OUI/NON
- Push vers revisite: OUI/NON

Score Conversion /100:
- 90-100: CTAs multiples, fluides, irrésistibles
- 70-89: CTAs clairs et bien placés
- 50-69: CTA présent mais faible
- <50: CTA absent ou maladroit

8. ALGORITHME TIKTOK /100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pourquoi l'algorithme pousse cette vidéo:

Signaux POSITIFS:
- ⏱️ Vitesse de rétention: Hook fort, pas de "trou mort"
- 💎 Densité de valeur: Beaucoup d'info, pas de remplissage
- 🔁 Structure addictive: Boucles ouvertes, promesses de fin
- 🎁 Micro récompenses: Petites révélations régulières
- 📖 Tension narrative: Conflit, question en suspens, résolution
- 💬 Commentaires provoqués: Question, opinion, erreur intentionnelle
- 🔄 Partage: Utile, émotionnel, tag-friendly

Moments clés:
- 🎯 REWATCH: Info dense, à revoir
- 💬 COMMENTAIRES: Créent de la discussion
- 💾 SAUVEGARDES: Info à garder
- 📤 PARTAGE: Section à passer à d'autres

Score Algorithme /100:
- 90-100: Optimisé pour tous les signaux TikTok
- 70-89: Plusieurs signaux forts
- 50-69: Signaux basiques présents
- <50: Algo ne pushera pas

================================================================================
ANALYSE STRUCTURELLE DE VENTE (LEGACY — À INCLURE AUSSI)
================================================================================

Flux naturel optimal:
1. ACCROCHE (0-5s) → Capture l'attention
2. PROBLÈME (5-20s) → Identifie point de douleur
3. SOLUTION (20-45s) → Montre comment le produit résout
4. PRODUIT (45-60s) → Démonstration/présentation
5. CTA (60+s) → Appel à l'action clair

================================================================================
RETOUR JSON (STRUCTURE COMPLÈTE)
================================================================================

{
  "analyse_8_dimensions": {
    "hook": {"score": <0-100>, "categorie": "<type>", "feedback": "<...>"},
    "retention": {"score": <0-100>, "boucles_ouvertes": <0-10>, "feedback": "<...>"},
    "mecanismes_vente": {"score": <0-100>, "biais_principal": "<nom>", "nb_biais": <1-4>, "type_vente": "<type>", "feedback": "<...>"},
    "positionnement": {"score": <0-100>, "role": "<type>", "accessibilite": <1-10>, "credibilite": <1-10>, "relatable": "<oui/non>", "feedback": "<...>"},
    "format_visuel": {"score": <0-100>, "supports_utilises": ["<...>"], "variation_montage": "<lent/moyen/rapide>", "feedback": "<...>"},
    "emotion_dominante": {"score": <0-100>, "emotion": "<type>", "intensite": <1-10>, "transitions_efficaces": ["<...>"], "feedback": "<...>"},
    "conversion_shop": {"score": <0-100>, "cta_visibles": <0-3>, "cta_implicites": <0-3>, "ce_que_vend": "<type>", "engagements": {"commentaires": "<oui/non>", "sauvegardes": "<oui/non>", "partage": "<oui/non>"}, "feedback": "<...>"},
    "algorithme": {"score": <0-100>, "signaux_forts": ["<...>"], "moments_cles": ["<...>"], "potentiel_push": "<faible/moyen/fort>", "feedback": "<...>"},
    "score_persuasion_global": <0-100>
  },
  "scores_legacy": {
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
    "accroche": {"present": <true/false>, "score": <0-10>, "hook_type": "<type>", "feedback": "<...>"},
    "probleme": {"present": <true/false>, "score": <0-10>, "problem_stated": "<...>", "clarity": <0-10>, "feedback": "<...>"},
    "solution": {"present": <true/false>, "score": <0-10>, "how_solved": "<...>", "product_link": "<yes/no>", "feedback": "<...>"},
    "produit": {"present": <true/false>, "score": <0-10>, "shown_adequately": "<yes/no/partially>", "demo_quality": "<none/basic/good/excellent>", "feedback": "<...>"},
    "cta": {"present": <true/false>, "score": <0-10>, "cta_type": "<type>", "clarity": <0-10>, "persuasion": "<faible/moyen/fort>", "feedback": "<...>"},
    "ordre_naturel": <true/false>,
    "transitions": "<fluides/abruptes/absentes>",
    "score_structure": <0-100>
  },
  "score_global": <0-100>,
  "points_forts": ["<1>", "<2>", "<3>"],
  "points_ameliorer": ["<1>", "<2>", "<3>"],
  "recommendations_hooks": {
    "hook_type_propose": "<meilleur type>",
    "raison": "<pourquoi (1-2 phrases)>",
    "exemples_concrets": ["<exemple 1>", "<exemple 2>", "<exemple 3>"]
  },
  "plan_reproduction": {
    "hook_similaire": {"structure": "<détail>", "variables": "<à adapter>", "exemple": "<pour ton produit>"},
    "mecanique_montage": {"rythme": "<X cuts par Y sec>", "transitions": "<types>", "elements_visuels": ["<...>"]},
    "cta_optimise": {"type": "<direct/implicite/emotionnel>", "placement": "<debut/milieu/fin>", "formulation": "<exemple>"},
    "angle_shop": {"produit": "<recommandation>", "storytelling": "<framework>", "emotion": "<laquelle>"}
  },
  "conseils_concrets": ["<1>", "<2>", "<3>", "<4>"],
  "ameliorations_prioritaires": [
    {"rang": 1, "action": "<...", "impact": "<..>"},
    {"rang": 2, "action": "<...", "impact": "<..>"},
    {"rang": 3, "action": "<...", "impact": "<..>"}
  ],
  "verdict": "<Résumé réaliste 3-4 phrases avec langage probabiliste : potentiel apparent? Point faible? Priorité? Refaire ou tester?>",
  "disclaimer_realisme": "Cette analyse décortique les mécanismes de persuasion et les signaux algorithme. L'algo TikTok surprend toujours — des vidéos considérées mauvaises vendent bien, des excellentes floppent. Utilise comme repère stratégique, pas comme certitude."
}

IMPORTANT: JSON uniquement, pas de markdown, français pur, langage probabiliste."""


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


def analyze_video(frames_b64: List[str], transcript: Optional[str] = None, market_context: Optional[dict] = None) -> dict:
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
