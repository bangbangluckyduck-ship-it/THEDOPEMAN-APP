from __future__ import annotations
import base64
import json
import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Optional


# ════════════════════════════════════════════════════════════════════════════
# MOMENTUM SAISONNIER — Calcul déterministe du timing stratégique
# ════════════════════════════════════════════════════════════════════════════
# Mapping mot-clé produit → mois de pic de vente (1=Jan ... 12=Dec).
# Utilisé par get_seasonality_momentum() pour produire un statut stratégique
# (Inception / Pic / Déclin / Hors-Saison / Evergreen) injecté dans le prompt
# de synthèse Mistral. Permet à l'IA de baser ses conseils de publication
# sur un signal DÉTERMINISTE plutôt que sur sa propre estimation calendaire.
PEAK_SEASONS: dict[str, list[int]] = {
    # ─── Beauté / Soleil / Été ─────────────────────────────────────────────
    "solaire":       [6, 7, 8],
    "maillot":       [6, 7, 8],
    "bronzage":      [6, 7, 8],
    "plage":         [6, 7, 8],
    "lunettes":      [6, 7, 8],
    "piscine":       [6, 7, 8],
    "autobronzant":  [5, 6, 7],
    "ventilateur":   [6, 7, 8],

    # ─── Q4 / Cadeaux / Fin d'année ────────────────────────────────────────
    "jouet":         [11, 12],
    "cadeau":        [11, 12],
    "noel":          [11, 12],
    "noël":          [11, 12],
    "fete":          [11, 12],
    "fête":          [11, 12],
    "avent":         [10, 11],
    "deco":          [11, 12],
    "déco":          [11, 12],

    # ─── Fitness / Résolutions / Bikini body ───────────────────────────────
    "fitness":       [1, 5, 6],
    "sport":         [1, 5, 6],
    "minceur":       [1, 5, 6],
    "musculation":   [1, 5, 6],
    "proteine":      [1, 5, 6],
    "protéine":      [1, 5, 6],
    "yoga":          [1, 5, 6],

    # ─── Saint-Valentin ────────────────────────────────────────────────────
    "bijou":         [2],
    "amour":         [2],
    "couple":        [2],
    "rose":          [2],
    "parfum":        [2, 5, 11, 12],   # ajouté Fête des Mères + fêtes
    "lingerie":      [2],

    # ─── Rentrée scolaire / bureau ─────────────────────────────────────────
    "ecole":         [8, 9],
    "école":         [8, 9],
    "bureau":        [8, 9],
    "organisation":  [8, 9],
    "rentree":       [8, 9],
    "rentrée":       [8, 9],
    "fourniture":    [8, 9],
    "cartable":      [8, 9],

    # ─── Hiver / Confort / Cocooning ───────────────────────────────────────
    "doudoune":      [11, 12, 1],
    "chauffage":     [11, 12, 1, 2],
    "humidificateur":[11, 12, 1, 2],
    "couverture":    [11, 12, 1],
    "echarpe":       [11, 12, 1],
    "écharpe":       [11, 12, 1],
    "bouillotte":    [11, 12, 1],
}


def get_seasonality_momentum(product_hint: str) -> str:
    """
    Calcul déterministe du momentum saisonnier d'un produit.

    Compare le mois courant au(x) mois de pic listé(s) dans PEAK_SEASONS
    pour un mot-clé produit, et retourne un statut stratégique actionnable.

    Args:
        product_hint: Nom du produit (issu de la détection vision ou saisi user).
                      Insensible à la casse, peut contenir plusieurs mots.

    Returns:
        Une string descriptive parmi :
          - "Phase d'Inception (Idéal)" — pic dans 1-2 mois
          - "Pic de Saison (Chaud)"     — on est en plein pic
          - "Fin de Tendance (Déclin)"  — pic vient de passer (1-2 mois après)
          - "Hors-Saison (Risqué)"      — pic loin (>2 mois dans tous les sens)
          - "Produit Evergreen"         — aucun mot-clé saisonnier détecté
    """
    if not product_hint or not isinstance(product_hint, str):
        return "Produit Evergreen (Ventes stables toute l'année, pas de pic majeur détecté)."

    hint_lower = product_hint.lower()
    current_month = datetime.now().month

    # Trouve toutes les correspondances mot-clé → liste des mois de pic
    matched_peak_months: list[int] = []
    matched_keywords: list[str] = []
    for keyword, peaks in PEAK_SEASONS.items():
        if keyword in hint_lower:
            matched_peak_months.extend(peaks)
            matched_keywords.append(keyword)

    if not matched_peak_months:
        return "Produit Evergreen (Ventes stables toute l'année, pas de pic majeur détecté)."

    # Calcul de la distance circulaire (12 mois bouclés) entre mois courant
    # et chaque pic. Distance signée : positive = pic à venir, négative = passé.
    def signed_circular_distance(now: int, peak: int) -> int:
        forward = (peak - now) % 12          # 0..11 mois à attendre
        backward = (now - peak) % 12          # 0..11 mois écoulés depuis pic
        if forward <= backward:
            return forward                    # pic encore à venir (ou aujourd'hui)
        return -backward                      # pic vient de passer

    distances = [signed_circular_distance(current_month, p) for p in matched_peak_months]
    # On garde la distance dont la valeur absolue est minimale (pic le plus proche)
    closest = min(distances, key=lambda d: abs(d))
    matched_str = ", ".join(sorted(set(matched_keywords))[:3])

    if closest == 0:
        return (
            f"Pic de Saison (Chaud) : Nous sommes en plein pic. "
            f"Scaler les budgets immédiatement, la conversion est maximale. "
            f"[mot-clé détecté : {matched_str}]"
        )
    if 1 <= closest <= 2:
        return (
            f"Phase d'Inception (Idéal) : Le pic est dans {closest} mois. "
            f"C'est le moment parfait pour tester les créas à bas coût. "
            f"[mot-clé détecté : {matched_str}]"
        )
    if -2 <= closest <= -1:
        return (
            f"Fin de Tendance (Déclin) : Le pic vient de passer (il y a {abs(closest)} mois). "
            f"Écouler les stocks, réduire les coûts d'acquisition. "
            f"[mot-clé détecté : {matched_str}]"
        )
    return (
        f"Hors-Saison (Risqué) : Produit totalement hors saison "
        f"(prochain pic dans {abs(closest)} mois). "
        f"Coût d'acquisition potentiellement très élevé. "
        f"[mot-clé détecté : {matched_str}]"
    )


# ════════════════════════════════════════════════════════════════════════════
# CALENDRIER ÉVÉNEMENTIEL + SAISONNALITÉ (timing, gros impact sur conversion)
# ════════════════════════════════════════════════════════════════════════════

# Événements clés TikTok Shop FR/EU (jour/mois, types de produits boostés)
EVENEMENTS_CALENDAIRE = [
    # (label, mois, jour, [catégories/keywords boostés], jours_avant_pic)
    ("Saint-Valentin",        2,  14, ["bijou", "parfum", "lingerie", "fleur", "chocolat", "couple"],         21),
    ("Pâques",                4,  20, ["chocolat", "déco", "enfant"],                                         14),
    ("Fête des Mères",        5,  26, ["bijou", "parfum", "beauté", "cadeau", "fleur"],                       21),
    ("Fête des Pères",        6,  16, ["montre", "tech", "alcool", "gadget", "outil"],                        21),
    ("Vacances été",          7,   1, ["plage", "maillot", "lunettes", "solaire", "voyage", "valise"],        45),
    ("Rentrée scolaire",      8,  25, ["fourniture", "sac", "mode", "ordinateur", "tech"],                    21),
    ("Halloween",            10,  31, ["déguisement", "déco", "maquillage", "bonbon"],                        30),
    ("Black Friday",         11,  29, ["tech", "électronique", "mode", "beauté", "cadeau"],                   14),
    ("Cyber Monday",         12,   2, ["tech", "abonnement"],                                                 14),
    ("Calendrier de l'avent",10,  20, ["calendrier", "avent", "cadeau", "beauté", "chocolat"],                15),
    ("Noël",                 12,  25, ["cadeau", "déco", "tech", "bijou", "enfant", "jouet"],                 28),
    ("Soldes hiver",          1,   8, ["mode", "chaussure"],                                                   7),
    ("Soldes été",            6,  25, ["mode", "chaussure"],                                                   7),
    ("French Days printemps", 4,   1, ["tech", "électroménager", "mode"],                                      7),
    ("French Days automne",   9,  27, ["tech", "électroménager", "mode"],                                      7),
]

# Saisonnalité par mots-clés produit (mois où ça performe / mois creux)
SAISONNALITE_KEYWORDS = {
    # Été
    "lunettes": {"peak": [4, 5, 6, 7, 8], "creux": [11, 12, 1, 2]},
    "solaire": {"peak": [5, 6, 7, 8], "creux": [11, 12, 1]},
    "maillot": {"peak": [4, 5, 6, 7], "creux": [10, 11, 12, 1, 2]},
    "piscine": {"peak": [4, 5, 6, 7], "creux": [10, 11, 12, 1, 2]},
    "plage": {"peak": [4, 5, 6, 7], "creux": [11, 12, 1, 2]},
    "ventilateur": {"peak": [5, 6, 7, 8], "creux": [11, 12, 1, 2]},
    "climatiseur": {"peak": [5, 6, 7, 8], "creux": [11, 12, 1]},
    "glacière": {"peak": [4, 5, 6, 7, 8], "creux": [11, 12, 1, 2]},
    # Hiver
    "doudoune": {"peak": [10, 11, 12, 1, 2], "creux": [5, 6, 7, 8]},
    "manteau": {"peak": [10, 11, 12, 1, 2], "creux": [6, 7, 8]},
    "écharpe": {"peak": [10, 11, 12, 1, 2], "creux": [6, 7, 8]},
    "chauffage": {"peak": [10, 11, 12, 1, 2], "creux": [5, 6, 7, 8]},
    "humidificateur": {"peak": [10, 11, 12, 1, 2], "creux": [6, 7, 8]},
    "couverture": {"peak": [10, 11, 12, 1], "creux": [6, 7, 8]},
    "bouillotte": {"peak": [10, 11, 12, 1, 2], "creux": [5, 6, 7, 8]},
    # Saisonnier événementiel
    "calendrier de l'avent": {"peak": [10, 11], "creux": [1, 2, 3, 4, 5, 6, 7]},
    "halloween": {"peak": [9, 10], "creux": [1, 2, 3, 4, 5, 6, 7, 8]},
    "noël": {"peak": [11, 12], "creux": [1, 2, 3, 4, 5, 6, 7, 8]},
    "sapin": {"peak": [11, 12], "creux": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
    # Evergreen avec petites variations
    "parfum": {"peak": [2, 5, 11, 12], "creux": []},
    "bijou": {"peak": [2, 5, 11, 12], "creux": []},
}


def _saison_actuelle(mois: int) -> str:
    if mois in (12, 1, 2): return "hiver"
    if mois in (3, 4, 5): return "printemps"
    if mois in (6, 7, 8): return "été"
    return "automne"


def _evenements_proches(today: date, max_days: int = 60) -> list:
    """Retourne les événements dans les `max_days` prochains jours, triés par proximité."""
    results = []
    for label, m, d, keywords, lead_days in EVENEMENTS_CALENDAIRE:
        # Construit la date de l'événement cette année; si passé, prend l'année prochaine
        try:
            ev_date = date(today.year, m, d)
        except ValueError:
            continue
        if ev_date < today:
            ev_date = date(today.year + 1, m, d)
        delta = (ev_date - today).days
        if 0 <= delta <= max_days:
            results.append({
                "label": label,
                "date": ev_date.isoformat(),
                "jours_avant": delta,
                "keywords_boostes": keywords,
                "fenetre_publication_avant_pic_jours": lead_days,
                "dans_fenetre_optimale": delta <= lead_days,
            })
    return sorted(results, key=lambda x: x["jours_avant"])


def _get_calendar_context(today: Optional[date] = None) -> dict:
    """Contexte temporel injecté dans le prompt synthèse."""
    today = today or date.today()
    mois = today.month
    return {
        "date_actuelle": today.isoformat(),
        "mois_actuel": mois,
        "mois_actuel_nom": ["janvier","février","mars","avril","mai","juin",
                            "juillet","août","septembre","octobre","novembre","décembre"][mois-1],
        "saison_actuelle": _saison_actuelle(mois),
        "evenements_60j": _evenements_proches(today, max_days=60),
    }


def _saisonnalite_pour_produit(produit: str, mois: int) -> dict:
    """Détecte si le produit est en pic/creux/neutre selon mois actuel."""
    if not produit:
        return {"statut": "inconnu", "score": 50, "raison": "produit non identifié"}
    p = produit.lower()
    for kw, data in SAISONNALITE_KEYWORDS.items():
        if kw in p:
            if mois in data["peak"]:
                return {
                    "statut": "pic",
                    "score": 95,
                    "raison": f"« {kw} » est en pleine saison ({_saison_actuelle(mois)})",
                    "keyword_detecte": kw,
                }
            if mois in data["creux"]:
                return {
                    "statut": "creux",
                    "score": 15,
                    "raison": f"« {kw} » est à contre-saison ({_saison_actuelle(mois)} = saison défavorable)",
                    "keyword_detecte": kw,
                }
            return {
                "statut": "neutre",
                "score": 60,
                "raison": f"« {kw} » ni en pic ni en creux ce mois-ci",
                "keyword_detecte": kw,
            }
    return {"statut": "evergreen", "score": 70, "raison": "Produit sans saisonnalité forte détectée"}


def _format_calendar_for_prompt(cal_ctx: dict, saison_produit: dict) -> str:
    lines = [
        "\n================================================================================",
        "CONTEXTE TEMPOREL ACTUEL (très important pour évaluer le timing du contenu)",
        "================================================================================",
        f"Date de l'analyse : {cal_ctx['date_actuelle']}",
        f"Mois actuel : {cal_ctx['mois_actuel_nom']} (saison : {cal_ctx['saison_actuelle']})",
        f"",
        f"SAISONNALITÉ DU PRODUIT ANALYSÉ :",
        f"  Statut : {saison_produit['statut'].upper()} | Score saison : {saison_produit['score']}/100",
        f"  Raison : {saison_produit['raison']}",
    ]
    evs = cal_ctx.get("evenements_60j", [])
    if evs:
        lines.append("\nÉVÉNEMENTS COMMERCIAUX DANS LES 60 PROCHAINS JOURS :")
        for ev in evs[:6]:
            in_window = "✅ DANS LA FENÊTRE OPTIMALE" if ev["dans_fenetre_optimale"] else "⏰ trop tôt pour push max"
            lines.append(
                f"  - {ev['label']} dans {ev['jours_avant']}j ({ev['date']}) | {in_window}"
                f" | boost catégories: {', '.join(ev['keywords_boostes'][:4])}"
            )
        lines.append("\nSi le produit analysé correspond à une catégorie boostée par un événement proche, "
                     "et que tu es dans la fenêtre optimale de publication, le score timing doit être élevé. "
                     "Sinon, score moyen ou bas selon distance/non-correspondance.")
    else:
        lines.append("\nAucun événement commercial majeur dans les 60 prochains jours.")
    lines.append("\nINSTRUCTIONS POUR LE BLOC contexte_temporel DU JSON :")
    lines.append("  - score_timing /100 = synthèse saisonnalité + événements + cycle")
    lines.append("  - cycle_tendance ∈ {early, peak, late, dead} basé sur l'écosystème TikTok actuel")
    lines.append("  - warning_timing : message court ⚠️/🔥/✅ visible en haut du diagnostic UI")
    lines.append("  - fenetre_publication : nombre de jours optimaux pour publier maintenant (-1 si pas la saison)")
    return "\n".join(lines)


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


def analyze_visual(frames_b64: List[str], product: Optional[str] = None, price: Optional[str] = None) -> dict:
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
    if price:
        content.append({"type": "text", "text": f"\n💶 PRIX INDIQUÉ par l'utilisateur : {price}. Considère-le comme le prix de référence du produit (ne le remets pas en cause même s'il n'est pas visible à l'écran)."})

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

🆕 9️⃣ CONTEXTE TEMPOREL /100 (CRITIQUE — peut tout changer)
Évalue le TIMING de cette publication :
- Saisonnalité : le produit est-il en pic, creux ou neutre selon la date actuelle ?
- Événement commercial proche : Saint-Valentin/Noël/Black Friday/etc. dans <60j qui boost ce type de produit ?
- Cycle de tendance : produit en émergence (early), au pic (peak), en chute (late) ou mort (dead) ?
- Fenêtre d'opportunité : combien de jours avant qu'il soit trop tard ?
- Warning : alerte courte affichée en haut de l'analyse si timing critique
Score 90-100 : timing parfait (pic saison + événement proche)
Score 70-89 : bon timing
Score 40-69 : timing neutre / evergreen
Score 0-39 : à contre-saison ou tendance morte (déconseillé de publier maintenant)

RETOUR JSON OBLIGATOIRE (STRUCTURE EXACTE) :
{"contexte_temporel": {"score_timing": <0-100>, "score_saison": <0-100>, "statut_saison": "<pic|peak|neutre|creux|evergreen>", "evenement_booster": {"label": "<nom événement ou null>", "jours_avant": <int ou null>, "dans_fenetre_optimale": <true/false>, "boost_applicable": <true/false>}, "cycle_tendance": "<early|peak|late|dead>", "fenetre_publication": {"jours_recommandes": <int>, "moment_optimal": "<ex: 'publier dans les 14 prochains jours' ou 'attendre mars-avril'>"}, "warning_timing": "<🔥 TIMING OPTIMAL / ✅ TIMING OK / ⚠️ TIMING DÉFAVORABLE / ❌ CONTRE-SAISON>", "message_warning": "<2 phrases concrètes>", "recommandation_publication": "<conseil court>"}, "analyse_8_dimensions": {"hook": {"score": <0-100>, "categorie": "<💰ARGENT|❌ERREUR|🎯OPPORTUNITÉ|⚡SIMPLICITÉ|🚀RÉSULTAT|😤FRUSTRATION|🤯CHOC|🔬RÉVÉLATION>", "feedback": "<>"}, "retention": {"score": <0-100>, "boucles_ouvertes": <0-10>, "feedback": "<>"}, "mecanismes_vente": {"score": <0-100>, "biais_principal": "<>", "nb_biais": <1-4>, "type_vente": "<>", "feedback": "<>"}, "positionnement": {"score": <0-100>, "role": "<>", "accessibilite": <1-10>, "credibilite": <1-10>, "relatable": "<oui/non>", "feedback": "<>"}, "format_visuel": {"score": <0-100>, "supports_utilises": ["<>"], "variation_montage": "<lent/moyen/rapide>", "feedback": "<>"}, "emotion_dominante": {"score": <0-100>, "emotion": "<>", "intensite": <1-10>, "transitions_efficaces": ["<>"], "feedback": "<>"}, "conversion_shop": {"score": <0-100>, "cta_visibles": <0-3>, "cta_implicites": <0-3>, "ce_que_vend": "<>", "engagements": {"commentaires": "<oui/non>", "sauvegardes": "<oui/non>", "partage": "<oui/non>"}, "feedback": "<>"}, "algorithme": {"score": <0-100>, "signaux_forts": ["<>"], "moments_cles": ["<>"], "potentiel_push": "<faible/moyen/fort>", "feedback": "<>"}, "score_persuasion_global": <0-100>}, "scores_legacy": {"accroche": {"note": <0-10>, "commentaire": "<>"}, "discours": {"note": <0-10>, "commentaire": "<>"}, "qualite_visuelle": {"note": <0-10>, "commentaire": "<>"}, "visibilite_produit": {"note": <0-10>, "commentaire": "<>"}, "call_to_action": {"note": <0-10>, "commentaire": "<>"}, "energie_dynamisme": {"note": <0-10>, "commentaire": "<>"}, "credibilite_confiance": {"note": <0-10>, "commentaire": "<>"}}, "detection": {"produit": "<nom>", "categorie_marche": "<UNE SEULE valeur parmi : beaute|mode|tech|fitness|sante|maison|autre>", "prix_estime": "<prix EUR ou non détecté>", "prix_rentable": <true/false>, "hook_type": "<>", "hook_force": <0-10>, "confiance_detection": <0.6-1.0>}, "viral_potential": {"score": <0-100>, "facteur_prix": "<très bas <15€|bon 15-40€|élevé 40-100€|premium 100€+>", "explication": "<2-3 lignes>"}, "structure_vente": {"accroche": {"present": <true/false>, "score": <0-10>, "hook_type": "<>", "feedback": "<>"}, "probleme": {"present": <true/false>, "score": <0-10>, "problem_stated": "<>", "clarity": <0-10>, "feedback": "<>"}, "solution": {"present": <true/false>, "score": <0-10>, "how_solved": "<>", "product_link": "<yes/no>", "feedback": "<>"}, "produit": {"present": <true/false>, "score": <0-10>, "shown_adequately": "<yes/no/partially>", "demo_quality": "<none/basic/good/excellent>", "feedback": "<>"}, "cta": {"present": <true/false>, "score": <0-10>, "cta_type": "<>", "clarity": <0-10>, "persuasion": "<faible/moyen/fort>", "feedback": "<>"}, "ordre_naturel": <true/false>, "transitions": "<fluides/abruptes/absentes>", "score_structure": <0-100>}, "score_global": <0-100>, "points_forts": ["<1>", "<2>", "<3>"], "points_ameliorer": ["<1>", "<2>", "<3>"], "recommendations_hooks": {"hook_type_propose": "<>", "raison": "<1-2 phrases>", "exemples_concrets": ["<>", "<>", "<>"]}, "plan_reproduction": {"hook_similaire": {"structure": "<>", "variables": "<>", "exemple": "<>"}, "mecanique_montage": {"rythme": "<>", "transitions": "<>", "elements_visuels": ["<>"]}, "cta_optimise": {"type": "<direct/implicite/emotionnel>", "placement": "<debut/milieu/fin>", "formulation": "<>"}, "angle_shop": {"produit": "<>", "storytelling": "<>", "emotion": "<>"}}, "conseils_concrets": ["<1>", "<2>", "<3>", "<4>"], "ameliorations_prioritaires": [{"rang": 1, "action": "<>", "impact": "<>"}, {"rang": 2, "action": "<>", "impact": "<>"}, {"rang": 3, "action": "<>", "impact": "<>"}], "verdict": "<3-4 phrases langage probabiliste>", "disclaimer_realisme": "Analyse décortique persuasion + signaux algo. TikTok surprend — mauvaises vidéos vendent bien, excellentes floppent. Repère stratégique, pas certitude."}"""


# ════════════════════════════════════════════════════════════════════════════
# EXIGENCES DE QUALITÉ (Phase 2) — appliquées à tous les feedbacks/conseils.
# N'ajoute AUCUNE clé JSON : muscle uniquement le CONTENU des champs existants.
# Placé en fin de prompt (haute récence) pour maximiser l'effet.
# ════════════════════════════════════════════════════════════════════════════
QUALITY_DIRECTIVES = """

════════════════════════════════════════════════════════════════════════════════
EXIGENCES DE QUALITÉ — RESPECTE-LES POUR CHAQUE "feedback" / "commentaire" / "conseil"
════════════════════════════════════════════════════════════════════════════════
1. SPÉCIFIQUE À CETTE VIDÉO : interdiction formelle de conseils génériques applicables
   à n'importe quelle vidéo ("améliore ton accroche", "ajoute un CTA"…). Chaque remarque
   s'appuie sur un élément CONCRET réellement vu (vision) ou entendu (transcript).
2. CITE LE TRANSCRIPT : pour juger hook / rétention / discours / conversion, cite la
   phrase EXACTE entre guillemets « … » sur laquelle tu te bases. Si transcript absent,
   dis-le explicitement et appuie-toi sur la description visuelle.
3. ACTIONNABLE + EXEMPLE PRÊT À L'EMPLOI : chaque "points_ameliorer", "conseils_concrets"
   et "ameliorations_prioritaires" dit QUOI changer, COMMENT, et donne un exemple RÉEL
   reformulé prêt à dire face caméra (ex : réécris concrètement le hook en 1 phrase).
4. ANCRE PRODUIT & PRIX : relie tes conseils au produit détecté et à son prix — l'angle
   de vente et le potentiel viral dépendent directement du prix.
5. JUSTIFIE LES SCORES : un score bas DOIT pointer un manque précis ; un score haut une
   force précise. Pas de score "moyen par défaut" non argumenté.
6. exemples_concrets / formulation / script : du texte RÉEL prêt à l'emploi, jamais des
   descriptions abstraites ("fais un hook accrocheur" est INTERDIT).
7. Reste probabiliste ("semble", "tend à") mais PRÉCIS et utile. Zéro remplissage.
"""


# ════════════════════════════════════════════════════════════════════════════
# Modèle de synthèse — configurable via env (défaut inchangé : mistral-small).
# Pour un gain de qualité, définir SYNTHESIS_MODEL=mistral-medium-latest (ou large)
# sur Render — aucun redéploiement de code nécessaire.
# ════════════════════════════════════════════════════════════════════════════
def _synthesis_model() -> str:
    return os.getenv("SYNTHESIS_MODEL", "mistral-small-latest")


# ════════════════════════════════════════════════════════════════════════════
# PROMPT PREMIUM DYNAMIQUE — réservé aux plans Gold / Agency (+ beta / admin)
# Concaténé au prompt de synthèse UNIQUEMENT pour ces tiers. Le contrôle du tier
# est fait 100% côté serveur (token JWT / Supabase) ; jamais via le frontend.
# ════════════════════════════════════════════════════════════════════════════
PREMIUM_STRATEGY_TIERS = {"gold", "agency", "beta", "admin"}

PREMIUM_PROMPT_BLOCK = """

████████████████████████████████████████████████████████████████████████████████
█  INSTRUCTION PREMIUM (Génération de revenus) — RÉSERVÉ PLANS GOLD / AGENCY
████████████████████████████████████████████████████████████████████████████████

En plus de l'analyse ci-dessus, tu dois identifier formellement le produit vendu ou mis en avant. Ensuite, dresse le profil psychologique du meilleur public cible (Persona) pour l'acheter. Enfin, rédige un script TikTok clé en main (Hook de 0-3s, Démonstration organique, Call-to-Action vers le TikTok Shop) hautement optimisé pour convertir cette audience précise. Structure cette réponse sous le titre exact '👑 Stratégie de Conversion (Premium)'.

⚠️ CONTRAINTE DE FORMAT : tu produis du JSON UNIQUEMENT. Tu DOIS donc ajouter au JSON final une clé supplémentaire `strategie_conversion_premium` avec EXACTEMENT cette structure :
"strategie_conversion_premium": {
  "titre": "👑 Stratégie de Conversion (Premium)",
  "produit_identifie": "<nom précis du produit vendu / mis en avant>",
  "persona": {
    "profil": "<âge, genre, situation de vie, niveau de revenu typique de l'acheteur idéal>",
    "psychologie": "<motivations profondes, douleurs et désirs qui déclenchent l'achat>",
    "declencheurs_achat": ["<déclencheur 1>", "<déclencheur 2>", "<déclencheur 3>"]
  },
  "script_tiktok": {
    "hook_0_3s": "<phrase d'accroche exacte à dire face caméra, 0-3s>",
    "demonstration_organique": "<déroulé de la démonstration produit, naturelle et non publicitaire>",
    "call_to_action": "<CTA exact et incitatif vers le TikTok Shop>"
  }
}
"""


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
    user_tier: str = "free",
    price: Optional[str] = None,
) -> dict:
    """
    Synthèse text-only via mistral-small : combine vision + transcript + marché.
    Bcp + rapide que pixtral car pas d'images à traiter (8-15s vs 30-60s).

    `user_tier` est résolu côté serveur (token JWT / Supabase). Pour les plans
    Gold / Agency (+ beta / admin), on concatène le bloc PREMIUM qui génère la
    section "👑 Stratégie de Conversion (Premium)" (persona + script de vente).
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise Exception("MISTRAL_API_KEY missing")

    # base_prompt : instructions d'analyse standard (tous les plans)
    base_prompt = SYNTHESIS_PROMPT
    # Le bloc premium (Gold / Agency / beta / admin) sera ajouté À LA FIN du prompt
    # (recency) pour maximiser la fiabilité d'émission de la clé JSON par le modèle.
    is_premium = (user_tier or "free").lower() in PREMIUM_STRATEGY_TIERS

    parts = [base_prompt]

    # 🆕 Contexte temporel (calendrier + saisonnalité) — calculé côté serveur, fiable
    cal_ctx = _get_calendar_context()
    detected_product_name = visual_result.get("produit") if isinstance(visual_result, dict) else None
    saison_produit = _saisonnalite_pour_produit(
        detected_product_name or (product or ""),
        cal_ctx["mois_actuel"],
    )
    parts.append(_format_calendar_for_prompt(cal_ctx, saison_produit))

    # 🆕 MOMENTUM SAISONNIER — Statut stratégique déterministe (priorité au produit
    # saisi par l'utilisateur, sinon retombe sur la détection vision).
    product_hint_for_momentum = (product or "").strip() or (detected_product_name or "")
    momentum_status = get_seasonality_momentum(product_hint_for_momentum)
    parts.append("\n\n████████████████████████████████████████████████████████████████████████████████")
    parts.append("█  CONTEXTE TEMPOREL & COMMERCIAL — MOMENTUM SAISONNIER (PRIORITÉ ABSOLUE)")
    parts.append("████████████████████████████████████████████████████████████████████████████████")
    parts.append("")
    parts.append("Le système a calculé de manière DÉTERMINISTE le momentum saisonnier du produit")
    parts.append(f"analysé (« {product_hint_for_momentum or 'produit inconnu'} »).")
    parts.append("")
    parts.append("👉 STATUT MOMENTUM (à utiliser tel quel — c'est une donnée FACTUELLE) :")
    parts.append(f"   ➤ {momentum_status}")
    parts.append("")
    parts.append("RÈGLES OBLIGATOIRES :")
    parts.append("  1. Tu DOIS baser ta recommandation de publication sur ce statut momentum exact.")
    parts.append("  2. Tu DOIS reprendre la formule du statut (Inception / Pic / Déclin / Hors-Saison /")
    parts.append("     Evergreen) dans ton bloc contexte_temporel.recommandation_publication.")
    parts.append("  3. Tu NE DOIS PAS contredire ce statut : il est calculé sur la base du mois courant")
    parts.append(f"     ({cal_ctx['mois_actuel_nom']}) et de la saisonnalité réelle du produit.")
    parts.append("  4. Si le statut indique 'Hors-Saison' ou 'Déclin', tu DOIS le refléter dans le")
    parts.append("     score_timing (≤ 40) et le warning_timing (⚠️ ou ❌).")
    parts.append("  5. Si le statut indique 'Pic de Saison' ou 'Phase d'Inception', tu DOIS le")
    parts.append("     refléter dans le score_timing (≥ 80) et le warning_timing (🔥 ou ✅).")
    parts.append("  6. 'Evergreen' = score_timing neutre (50-70), pas de pression temporelle.")
    parts.append("")
    parts.append("Ce momentum prime sur ton intuition calendaire — c'est la SOURCE DE VÉRITÉ.")
    parts.append("████████████████████████████████████████████████████████████████████████████████")

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

    if price:
        parts.append(
            f"\n\n💶 PRIX INDIQUÉ PAR L'UTILISATEUR : {price}. "
            "Considère ce prix comme la donnée de référence (detection.prix_estime) du produit "
            "et base toute l'analyse prix / potentiel de conversion dessus, même s'il n'apparaît pas à l'écran."
        )

    if market_context:
        parts.append(_format_market_context(market_context))

    parts.append(_HOOKS_CONTEXT)

    # Phase 2 : exigences de qualité (spécificité, citations transcript, actionnable).
    # Ancrage produit explicite pour des conseils contextualisés.
    _prod_label = (product or "").strip() or (detected_product_name or "le produit analysé")
    parts.append(f"\n🎯 Produit de référence pour tes conseils : « {_prod_label} ».")
    parts.append(QUALITY_DIRECTIVES)

    # Bloc PREMIUM en TOUT DERNIER (recency) → le modèle lit l'instruction juste
    # avant de répondre, ce qui fiabilise l'ajout de la clé strategie_conversion_premium.
    if is_premium:
        parts.append(PREMIUM_PROMPT_BLOCK)

    full_prompt = "\n".join(parts)

    raw = _mistral_call(
        api_key,
        _synthesis_model(),   # text-only, configurable via env SYNTHESIS_MODEL
        full_prompt,
        # medium/large sont plus lents que small → marge généreuse pour éviter
        # "read operation timed out". Configurable via SYNTHESIS_TIMEOUT.
        timeout=float(os.getenv("SYNTHESIS_TIMEOUT", "120")),
    )
    try:
        parsed = _extract_json(raw)
    except Exception:
        return {"error": "Impossible de parser la réponse IA", "raw": raw[:1000]}

    # Injecte le momentum déterministe dans le résultat final (source de vérité,
    # même si l'IA l'a reformulé ou ignoré dans son JSON).
    ct = parsed.setdefault("contexte_temporel", {})
    ct["momentum_status"] = momentum_status
    ct["momentum_product_hint"] = product_hint_for_momentum

    # Sécurité : la stratégie premium n'est conservée que pour les plans habilités.
    # (Si un modèle renvoyait le bloc sans qu'on l'ait demandé, on le supprime.)
    if not is_premium:
        parsed.pop("strategie_conversion_premium", None)

    return _post_process(parsed, market_context, visual_result, cal_ctx, saison_produit, manual_price=price)


# ════════════════════════════════════════════════════════════════════════════
# POST-PROCESSING (calculs prix/conversion côté serveur, plus fiable que IA)
# ════════════════════════════════════════════════════════════════════════════
def _post_process(
    parsed: dict,
    market_context: Optional[dict],
    visual_result: dict,
    cal_ctx: Optional[dict] = None,
    saison_produit: Optional[dict] = None,
    manual_price: Optional[str] = None,
) -> dict:
    """Applique la logique business prix/conversion + injection des données marché + timing."""
    # Prix saisi manuellement par l'utilisateur → fait autorité sur la détection IA.
    if manual_price and str(manual_price).strip():
        parsed.setdefault("detection", {})["prix_estime"] = str(manual_price).strip()
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
        pc = parsed.setdefault("prix_conversion", {})
        pc["montant"] = prix_num
        pc["categorie"] = cat
        pc["prix_identifie"] = True
        pc.setdefault("potentiel_conversion", {}).update({
            "niveau": niveau,
            "temps_attendre": delai,
            "confiance_prechampion": champion,
        })
        pc["conseil_prix"] = conseil
    else:
        # Prix NON identifié → ne PAS auto-bucketer, l'analyse conversion est juste "non évaluable"
        pc = parsed.setdefault("prix_conversion", {})
        pc["montant"] = None
        pc["categorie"] = "non identifié"
        pc["prix_identifie"] = False
        pc["evaluation_conversion_impossible"] = True
        pc.setdefault("potentiel_conversion", {}).update({
            "niveau": "non évaluable",
            "temps_attendre": None,
            "confiance_prechampion": False,
        })
        pc["conseil_prix"] = (
            "💰 Prix non identifié dans la vidéo — l'analyse de conversion ne peut "
            "pas être chiffrée avec fiabilité. Ajoute le prix manuellement (champ "
            "« produit ») pour débloquer le diagnostic complet de potentiel de vente. "
            "En attendant, l'analyse couvre uniquement la qualité du contenu vidéo."
        )

    # Injecter les données marché si dispo
    if market_context:
        parsed["donnees_marche"] = {
            "top_products": market_context.get("top_products", [])[:5],
            "trending": market_context.get("trending", [])[:5],
            "top_creators": market_context.get("top_creators", [])[:3],
        }

    # 🆕 Enrichir / garantir contexte_temporel avec les valeurs calculées serveur
    if cal_ctx and saison_produit:
        ct = parsed.setdefault("contexte_temporel", {})
        # Toujours écraser avec les vraies valeurs calculées côté serveur (fiables)
        ct["date_analyse"] = cal_ctx["date_actuelle"]
        ct["mois_actuel"] = cal_ctx["mois_actuel_nom"]
        ct["saison_actuelle"] = cal_ctx["saison_actuelle"]
        ct["score_saison"] = saison_produit["score"]
        ct["statut_saison"] = saison_produit["statut"]
        ct["saison_raison"] = saison_produit["raison"]
        ct["evenements_proches"] = cal_ctx.get("evenements_60j", [])[:5]

        # Score timing fallback si l'IA n'a pas répondu correctement
        if not isinstance(ct.get("score_timing"), (int, float)):
            ct["score_timing"] = saison_produit["score"]

        # Détecter automatiquement l'événement booster le plus proche
        produit_lower = (visual_result.get("produit") or "").lower()
        evt_match = None
        for ev in cal_ctx.get("evenements_60j", []):
            if any(kw in produit_lower for kw in ev["keywords_boostes"]):
                evt_match = ev
                break
        if evt_match and not ct.get("evenement_booster", {}).get("label"):
            ct["evenement_booster"] = {
                "label": evt_match["label"],
                "jours_avant": evt_match["jours_avant"],
                "dans_fenetre_optimale": evt_match["dans_fenetre_optimale"],
                "boost_applicable": True,
            }
        elif not ct.get("evenement_booster"):
            ct["evenement_booster"] = {
                "label": None, "jours_avant": None,
                "dans_fenetre_optimale": False, "boost_applicable": False,
            }

        # Warning automatique cohérent avec le score
        if not ct.get("warning_timing"):
            if ct["score_timing"] >= 85:
                ct["warning_timing"] = "🔥 TIMING OPTIMAL"
            elif ct["score_timing"] >= 60:
                ct["warning_timing"] = "✅ TIMING OK"
            elif ct["score_timing"] >= 30:
                ct["warning_timing"] = "⚠️ TIMING DÉFAVORABLE"
            else:
                ct["warning_timing"] = "❌ CONTRE-SAISON"

        if not ct.get("message_warning"):
            if saison_produit["statut"] == "creux":
                ct["message_warning"] = (
                    f"Le produit cible une période à l'opposé du moment actuel "
                    f"({cal_ctx['saison_actuelle']}). Publier maintenant aura un impact très faible. "
                    f"Attends la bonne saison pour scaler efficacement."
                )
            elif evt_match and evt_match["dans_fenetre_optimale"]:
                ct["message_warning"] = (
                    f"Tu publies à {evt_match['jours_avant']} jours de « {evt_match['label']} » "
                    f"— c'est la fenêtre optimale pour ce type de produit. Push maximal recommandé."
                )
            elif saison_produit["statut"] == "pic":
                ct["message_warning"] = (
                    f"Le produit est en pleine saison ({cal_ctx['saison_actuelle']}). "
                    f"Bonne fenêtre pour publier — la demande naturelle est élevée."
                )
            else:
                ct["message_warning"] = "Pas de signal temporel fort. Le contenu peut être publié toute l'année."

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
    user_tier: str = "free",
) -> dict:
    """
    Compat : exécute vision puis synthèse en séquence (utile pour tests/fallback).
    Pour le vrai parallélisme, utiliser analyze_visual() et synthesize_analysis()
    directement avec asyncio.gather() depuis main.py.
    """
    visual = analyze_visual(frames_b64, product)
    return synthesize_analysis(visual, transcript, market_context, product, user_tier)


# ════════════════════════════════════════════════════════════════════════════
# MÉTA-SYNTHÈSE MULTI-VIDÉOS — patterns gagnants / perdants (coaching personnel)
#
# Principe : l'analyse multi-lien porte sur les vidéos de l'utilisateur. On croise
# les N analyses pour faire émerger ce qui REVIENT (récurrences), côté forces
# (patterns gagnants à reproduire) ET côté faiblesses (patterns qui plombent
# potentiellement l'algo TikTok Shop, à corriger).
#
# Aujourd'hui : raisonnement basé sur les scores des 8 dimensions déjà calculés.
# Demain (connexion compte TikTok) : chaque vidéo portera un champ `performance`
# (ventes/vues réelles) qui pondèrera les patterns → corrélation data-driven.
# ════════════════════════════════════════════════════════════════════════════
BATCH_PATTERNS_PROMPT = """Tu es un coach expert TikTok Shop. On te donne l'analyse de PLUSIEURS vidéos d'UN MÊME créateur (au format JSON compact : scores des 8 dimensions, hook, produit, forces/faiblesses, et éventuellement des stats réelles de ventes/vues).

Ta mission : faire émerger les PATTERNS RÉCURRENTS de ce créateur, pas analyser chaque vidéo isolément.

RÈGLES DE RAISONNEMENT :
- Un "pattern" = un trait qui REVIENT sur plusieurs vidéos (≥2). Ignore ce qui n'apparaît qu'une fois.
- PATTERNS GAGNANTS = récurrences associées à des scores élevés (et, si dispo, à de vraies ventes). À reproduire.
- PATTERNS PERDANTS = récurrences associées à des scores faibles / signaux faibles pour l'algo TikTok Shop (hook mou, pas de CTA, rétention basse, conversion shop faible…). À corriger en priorité.
- Si `stats_reelles_disponibles` est true, PRIORISE la corrélation avec les ventes réelles plutôt que les scores.
- Langage probabiliste ("tend à", "semble"), français, concret et actionnable. Tutoie le créateur.

RETOUR JSON UNIQUEMENT, structure exacte :
{
  "nb_videos": <int>,
  "base_analyse": "<'scores d'analyse' ou 'ventes réelles + scores'>",
  "patterns_gagnants": [
    {"pattern": "<ce qui revient et marche>", "occurrences": <int>, "preuve": "<dimensions/scores qui le soutiennent>", "conseil": "<comment le réutiliser/amplifier>"}
  ],
  "patterns_perdants": [
    {"pattern": "<ce qui revient et plombe>", "occurrences": <int>, "risque_algo": "<pourquoi ça nuit à la portée/conversion TikTok Shop>", "correction": "<action concrète>"}
  ],
  "recette_personnelle": "<2-3 phrases : LA formule gagnante de ce créateur, à garder>",
  "priorite_coaching": "<l'action n°1 à corriger maintenant pour le plus d'impact>"
}"""


def _summarize_analysis_for_batch(analysis: dict, index: int, performance: Optional[dict] = None) -> dict:
    """Résumé compact d'une analyse pour la méta-synthèse (limite la taille du prompt)."""
    dims = analysis.get("analyse_8_dimensions") or {}
    detection = analysis.get("detection") or {}

    def _score(key: str):
        d = dims.get(key)
        return d.get("score") if isinstance(d, dict) else None

    summary = {
        "video": index + 1,
        "produit": detection.get("produit"),
        "hook_type": detection.get("hook_type"),
        "score_global": analysis.get("score_global"),
        "scores": {
            "hook": _score("hook"),
            "retention": _score("retention"),
            "mecanismes_vente": _score("mecanismes_vente"),
            "positionnement": _score("positionnement"),
            "format_visuel": _score("format_visuel"),
            "emotion": _score("emotion_dominante"),
            "conversion_shop": _score("conversion_shop"),
            "algorithme": _score("algorithme"),
        },
        "points_forts": (analysis.get("points_forts") or [])[:3],
        "points_ameliorer": (analysis.get("points_ameliorer") or [])[:3],
    }
    # Tuyauterie future : stats réelles TikTok (ventes/vues). None tant que non connecté.
    if performance:
        summary["performance"] = performance
    return summary


def synthesize_batch_patterns(analyses: List[dict], performances: Optional[List[Optional[dict]]] = None) -> dict:
    """
    Croise N analyses d'un même créateur → patterns gagnants + patterns perdants.
    `performances` : liste optionnelle alignée sur `analyses` (stats réelles futures).
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise Exception("MISTRAL_API_KEY missing")

    summaries = []
    for i, a in enumerate(analyses):
        perf = performances[i] if (performances and i < len(performances)) else None
        summaries.append(_summarize_analysis_for_batch(a or {}, i, perf))

    has_perf = any(s.get("performance") for s in summaries)
    payload = json.dumps(
        {"videos": summaries, "stats_reelles_disponibles": has_perf},
        ensure_ascii=False,
    )
    prompt = BATCH_PATTERNS_PROMPT + "\n\nDONNÉES À ANALYSER :\n" + payload

    raw = _mistral_call(api_key, "mistral-small-latest", prompt, timeout=60.0)
    try:
        result = _extract_json(raw)
    except Exception:
        result = {
            "nb_videos": len(summaries),
            "base_analyse": "ventes réelles + scores" if has_perf else "scores d'analyse",
            "patterns_gagnants": [],
            "patterns_perdants": [],
            "recette_personnelle": "Synthèse indisponible pour ce lot.",
            "priorite_coaching": "",
        }
    result["nb_videos"] = len(summaries)
    result["stats_reelles"] = has_perf
    return result
