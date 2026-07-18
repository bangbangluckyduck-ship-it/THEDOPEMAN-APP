"""
GÉNÉRATEUR MULTI-ANGLES — pour UN produit, produit 3 à 5 scripts prêts à tourner,
chacun dans une FORMULE DIFFÉRENTE (A→H), anti-répétition.

C'est l'outil « TEMPLATE_scripts_master » du décodage : donne un produit → reçois
plusieurs angles. Il matérialise la stratégie n°1 des top comptes (recycler un
produit gagnant sous plusieurs angles pour gagner la loterie algo par le VOLUME).

Déterministe là où c'est possible (choix de formules biaisé par product_intel),
génératif pour la rédaction (ai_providers.text_complete). Jamais bloquant.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

import ai_providers
import product_intel


# ── Chargé une fois : formules + playbook FR depuis la base de connaissances ──
def _load_kb() -> dict:
    try:
        return json.loads((Path(__file__).parent / "hooks_db.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


_KB = _load_kb()

# Formules recommandées par catégorie produit (biais déterministe, aligné corpus).
_FORMULAS_BY_CATEGORY: dict[str, list[str]] = {
    "anxiogene_securite": ["G_educatif_securite", "F_skit_dialogue", "A_confessionnel", "E_demo_solution", "D_deal_frontal"],
    "astuce_maline":      ["H_astuce_hack", "E_demo_solution", "F_skit_dialogue", "C_curiosite", "D_deal_frontal"],
    "satisfaisant_demo":  ["A_confessionnel", "E_demo_solution", "C_curiosite", "B_comparatif", "D_deal_frontal"],
    "prix_waouh_marque":  ["F_skit_dialogue", "A_confessionnel", "D_deal_frontal", "B_comparatif", "C_curiosite"],
    "utile_quotidien":    ["F_skit_dialogue", "C_curiosite", "E_demo_solution", "D_deal_frontal", "A_confessionnel"],
    "generique":          ["A_confessionnel", "F_skit_dialogue", "E_demo_solution", "D_deal_frontal", "C_curiosite"],
}


def _extract_json(raw: str) -> Optional[dict]:
    """Extrait le premier objet JSON valide d'une réponse LLM (tolérant au bruit)."""
    if not raw:
        return None
    # Retire d'éventuelles clôtures markdown ```json ... ```
    raw = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except Exception:
        pass
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(raw[start:end + 1])
        except Exception:
            return None
    return None


def _build_prompt(product: str, price: Optional[str], intel: dict,
                  formulas: list[str], n: int, market_fr: bool,
                  user_role: Optional[str]) -> str:
    sf = _KB.get("script_formulas", {})
    formula_lines = []
    for fid in formulas:
        desc = sf.get(fid)
        if desc:
            formula_lines.append(f"- {fid} : {desc}")
    invariants = sf.get("invariants_adn", [])
    playbook = _KB.get("fr_deals_playbook", {})

    fr_block = ""
    if market_fr:
        fr_block = (
            "\nMARCHÉ FR — applique :\n"
            f"- Durée : {playbook.get('duree_optimale_s', '25-40 s')}\n"
            f"- Rituel deal : {playbook.get('rituel_deal', '')}\n"
            f"- Boosters possibles : {' ; '.join(playbook.get('boosters_conversion', [])[:4])}\n"
        )

    role_block = ""
    if user_role == "affilie":
        role_block = "\nRÔLE : affilié → conversion immédiate, ton direct, clic impulsif.\n"
    elif user_role == "vendeur":
        role_block = "\nRÔLE : vendeur de sa marque → valeur + confiance, éviter le sur-hype.\n"

    return f"""Tu es scénariste TikTok Shop expert. Génère EXACTEMENT {n} scripts DIFFÉRENTS pour UN SEUL produit, chacun dans une FORMULE distincte. FRANÇAIS. JSON UNIQUEMENT.

PRODUIT : « {product} »
PRIX : {price or 'non précisé'}
POTENTIEL PRODUIT (déterministe) : {intel['potential_score']}/100 — {intel['category_label']} — saturation {intel['saturation_risk']}.

FORMULES À UTILISER (une par script, jamais deux fois la même) :
{chr(10).join(formula_lines)}

INVARIANTS D'ADN À RESPECTER dans CHAQUE script :
{chr(10).join('- ' + i for i in invariants)}
{fr_block}{role_block}
RÈGLES DE RÉDACTION (strictes) :
- Chaque `script` est un texte RÉEL prêt à dire face caméra (jamais une description abstraite).
- Aucune salutation, aucun emoji. Commence direct par le hook. 12 mots max par phrase.
- Le prix/deal est la CHUTE (sauf formule D_deal_frontal qui ouvre dessus).
- Rareté/urgence UNIQUEMENT en sortie et SEULEMENT si c'est vrai (jamais de fausse urgence).
- Pour F_skit_dialogue : écris en répliques préfixées « — » (2 personnages).
- CONFORMITÉ : rappelle (champ mention_pub) qu'une vidéo qui vend doit afficher la mention
  publicitaire (« Publicité »/« Collaboration commerciale ») ; n'invente ni faux prix ni fausse promo.

RETOURNE CE JSON EXACT :
{{"produit": "{product}", "potentiel_produit": {intel['potential_score']},
  "mention_pub": "<1 phrase : rappel d'afficher la mention publicitaire + de ne garder que des allégations/prix véridiques>",
  "scripts": [
    {{"formule": "<id formule ex A_confessionnel>", "angle": "<résumé de l'angle en 4-6 mots>",
      "hook_0_3s": "<phrase d'accroche exacte, 0-3s>",
      "script": "<script complet prêt à dire, avec balises de montage [entre crochets], textes écran en minuscules>",
      "cta": "<CTA final exact>", "duree_estimee_s": <int 20-45>,
      "why_it_works": "<1 phrase : pourquoi cet angle pour CE produit>"}}
  ]}}
Génère {n} entrées dans `scripts`, chacune une formule différente de la liste ci-dessus."""


def generate_multi_angle_scripts(
    product: str,
    price: Optional[str] = None,
    market: str = "fr",
    user_role: Optional[str] = None,
    n: int = 5,
    timeout: float = 60.0,
) -> dict:
    """Génère n scripts multi-angles pour un produit.

    Retour : {"ok": bool, "produit": str, "potentiel_produit": int,
              "mention_pub": str, "scripts": [...], "error"?: str}
    """
    product = (product or "").strip()
    if not product:
        return {"ok": False, "error": "Nom de produit requis.", "scripts": []}
    if not ai_providers.any_ai_key():
        return {"ok": False, "error": "Aucune clé IA configurée.", "scripts": []}

    n = max(3, min(5, int(n or 5)))
    market_fr = (market or "fr").lower().startswith("fr")
    user_role = (user_role or "").strip().lower() or None
    if user_role not in ("affilie", "vendeur"):
        user_role = None

    intel = product_intel.score_product(product, price)
    formulas = _FORMULAS_BY_CATEGORY.get(intel["category_id"], _FORMULAS_BY_CATEGORY["generique"])[:n]

    prompt = _build_prompt(product, price, intel, formulas, n, market_fr, user_role)

    try:
        raw = ai_providers.text_complete(prompt, timeout=timeout, max_tokens=4096, temperature=0.7)
    except Exception as e:
        return {"ok": False, "error": f"Échec génération : {e}", "scripts": []}

    parsed = _extract_json(raw)
    if not parsed or not isinstance(parsed.get("scripts"), list) or not parsed["scripts"]:
        return {"ok": False, "error": "Réponse IA non exploitable.", "scripts": [], "raw": (raw or "")[:500]}

    # Anti-répétition défensive : dédoublonne par formule.
    seen: set[str] = set()
    unique = []
    for s in parsed["scripts"]:
        fid = str(s.get("formule", "")).strip() or f"angle_{len(unique)}"
        if fid in seen:
            continue
        seen.add(fid)
        unique.append(s)

    return {
        "ok": True,
        "produit": parsed.get("produit", product),
        "potentiel_produit": intel["potential_score"],
        "categorie_produit": intel["category_label"],
        "mention_pub": parsed.get("mention_pub", ""),
        "scripts": unique,
    }
