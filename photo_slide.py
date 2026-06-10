"""
📸 Photo Slide Coach (feature premium GOLD / AGENCY / BETA / ADMIN).

À partir d'une image produit + (nature, prix, description), l'IA propose un plan
de carrousel TikTok Shop optimisé. Génération en **2 étapes streamées** (SSE) :

  ÉTAPE 1 — STRATÉGIE (vision pixtral-12b, ~15-25s) :
    type de slide recommandé, Hook (1ʳᵉ image), titre carrousel (+variantes), niche.
  ÉTAPE 2 — CONTENU (texte mistral-small, rapide ~8-15s) :
    plan slide par slide AVEC type de photo à prendre, CTA, description optimisée,
    hashtags, conseils saves.

L'utilisateur voit donc la stratégie + le hook AVANT que tout soit fini.

⚠️ ZONES ÉDITABLES : les blocs entre « ⬇️ ZONE ÉDITABLE … » et « ⬆️ FIN ZONE ÉDITABLE »
   (dans PHOTO_SLIDE_KNOWLEDGE) sont prévus pour que le product owner enrichisse l'IA
   (hooks gagnants, patterns de slides) SANS toucher au reste du code.
"""
from __future__ import annotations

import os
import random
from typing import Optional

from analyzer import _extract_json
import ai_providers


def _variation_block(avoid: Optional[str] = None) -> str:
    """🎲 Force la CRÉATIVITÉ : seed de variation + interdiction de réutiliser ce qui a déjà
    été généré (hook / titre / description). Même principe que le Prompt Studio vidéo."""
    seed = random.randint(100000, 999999)
    txt = (f"\n\n🎲 Seed de variation : {seed} — produis une déclinaison INÉDITE : "
           "hook, titre, angle créatif et description TOUS différents d'une génération à l'autre. "
           "Bannis les formules clichées et déjà-vues. Sois réellement original.")
    if avoid:
        txt += ("\n🚫 DÉJÀ GÉNÉRÉ POUR CE PRODUIT — INTERDICTION ABSOLUE de réutiliser ou paraphraser "
                "ces hooks / titres / descriptions. Change radicalement d'angle :\n" + str(avoid)[:1000])
    return txt


# ════════════════════════════════════════════════════════════════════════════
# CONNAISSANCES PARTAGÉES (utilisées par les 2 étapes)
# ════════════════════════════════════════════════════════════════════════════
PHOTO_SLIDE_KNOWLEDGE = """Tu es un expert en stratégie de carrousels (« Photo Slides ») TikTok Shop.
Objectif d'un carrousel : maximiser le DWELL TIME (le swipe = signal algorithmique fort → « Pour Toi »),
inciter aux SAVES (format liste/fiche pratique = reach), et CONVERTIR vers le panier TikTok Shop.

# PROCESS DE VENTE OBLIGATOIRE (ordre impératif des slides)
ACCROCHE → PROBLÈME → SOLUTION → PRODUIT → CTA
- SLIDE 1 (ACCROCHE) : hook stop-scroll qui SOULÈVE LE PROBLÈME. ⚠️ LE PRODUIT N'APPARAÎT JAMAIS sur la slide 1.
- PROBLÈME : on enfonce la douleur / la frustration que vit le spectateur.
- SOLUTION : on présente comment c'est résolu (le produit entre en scène).
- PRODUIT : mise en valeur du produit (bénéfices, preuves, réassurance).
- CTA (dernière) : appel à l'action vers le panier jaune TikTok Shop, urgence + bénéfice clair.
Chaque étape du process doit apparaître dans le plan de slides, dans cet ordre.

# LES 3 STYLES DE SLIDES
## « quad_photo » — 4 photos divisées (grille 2x2)
4 quadrants (symptôme / problème / bénéfice / signe), texte centré. Idéal : listes de symptômes/signes,
bénéfices, top 4 caractéristiques, comparaisons. Niches : santé, beauté, fitness, éducation. 1 slide composite (parfois 2-3).
## « fond_blanc » — produit épuré + texte
Photo propre, fond blanc impeccable, typo soignée, minimaliste premium. Idéal : produit premium, listes
éducatives, conseils experts, listes de signes/erreurs. Niches : cosmétique premium, soins, conseils. 3-5 slides.
## « ia_cartoon » — personnage transformation (split screen)
Gauche : personnage avec problème (style IA/cartoon/anime, triste). Droite : transformé (heureux, bénéfices).
Idéal : avant/après, transformation, problème→solution, aspiration. Niches : fitness, cosmétique transformative,
compléments, lifestyle. 2-4 slides.

# RÈGLES
- Choisis le style selon l'IMAGE + niche + prix (sauf style imposé par l'utilisateur).
- Le Hook crée une tension/curiosité immédiate (jamais une description plate).
- Pour CHAQUE slide, précise le TYPE DE PHOTO À PRENDRE (cadrage, fond, angle, ce qu'on voit).
- FRANÇAIS PUR. Concret et actionnable.

# ⬇️⬇️⬇️ ZONE ÉDITABLE 1 — HOOKS GAGNANTS (à enrichir par le product owner) ⬇️⬇️⬇️
## RÈGLES HOOK (impératives)
1. INTERDIT « ce produit », « cet objet », « cette astuce », « ça ». Le hook nomme LA douleur exacte : « tes selfies jaunes à 23h », pas « tes photos sont moches ». TEST DE TRANSPLANTATION : si le hook colle tel quel à un autre produit, il est rejeté.
2. UN marqueur concret minimum par hook : heure (« à 16h »), durée (« en 8 secondes »), chiffre précis et impair (« 487 € », jamais « des centaines »), lieu ou geste vécu (« remettre ton jean sur ta peau encore humide »).
3. 12 mots MAX, lisible en 1,5 s. Tutoiement obligatoire. Pas de subordonnée. UNE douleur, UNE cible, UNE situation. Le mot le plus chargé (douleur, chiffre, interdit) en première ou dernière position.
4. BOUCLE OUVERTE obligatoire : seule la slide 2 peut la fermer. Test : « peut-on connaître la suite sans swiper ? » Si oui, réécrire.
5. INTERDIT le vocabulaire creux : « game changer », « révolutionnaire », « incroyable », « tu ne devineras jamais », « le secret que personne ne connaît », « hack ». Chaque adjectif doit être remplaçable par une preuve (chiffre, durée, comparaison), sinon supprimé.
6. Lecture de pensée : décrire un moment vécu précis (geste + heure + lieu) que le viewer reconnaît instantanément — « tu rallumes la lumière 3 fois avant chaque story » plutôt que « tes photos sont moches ».
7. Texte et image slide 1 : même scène, informations DIFFÉRENTES. Image = symptôme visible ; texte = promesse d'explication. La redondance mot à mot divise l'impact par deux.
8. Slide 1 : produit JAMAIS visible (ni flou, ni silhouette, ni packaging — il n'existe pas avant la slide PRODUIT). Jamais de visage dramatique, grimace ou mains sur la tête. La douleur est prouvée par un détail MATÉRIEL vérifiable dans le cadre.
9. UN seul biais dominant par hook, choisi AVANT d'écrire. Curiosité + peur + FOMO empilés = bruit.

## BIBLIOTHÈQUE DE BIAIS (formules + scène visuelle slide 1)
### 1. Curiosity gap
Formules : « La vraie raison de [symptôme précis + moment], ce n'est pas [coupable évident] » · « Personne ne te dit pourquoi [douleur] revient [fréquence/moment] » · « [Symptôme précis] ? Ce n'est pas [cause supposée]. »
Ex : « Ta peau tiraille à 16h ? Ce n'est pas ta crème. »
Visuel slide 1 : montrer l'INDICE, jamais la réponse — macro sur un avant-bras où une griffure laisse une trace blanche persistante, trois flacons de crème flous derrière : le symptôme contredit la cause supposée.
### 2. Contre-intuition (le coupable insoupçonné)
Formules : « Ce n'est pas toi le problème, c'est ton/ta [objet banal insoupçonné] » · « Arrête de [geste que tout le monde croit bon] : c'est ça qui [aggrave la douleur] » · « Plus tu [action logique], plus [résultat inverse précis] »
Ex : « Te tenir droit aggrave ton mal de dos. Vraiment. »
Visuel slide 1 : le geste « correct » qui ÉCHOUE — personne de dos assise très droite sur une chaise ergonomique, post-it « tiens-toi droit ! », une main glissée sur les lombaires.
### 3. Aversion à la perte
Formules : « Tu perds [chiffre précis] par [période] à cause de [habitude banale] » · « Chaque [geste quotidien] te vole [résultat précis] » · « Combien de [chose de valeur] tu as déjà gâchées à cause de [cause précise] ? »
Ex : « Tu perds 4h par mois à pleurer sur tes oignons »
Visuel slide 1 : rendre la perte COMPTABLE dans le cadre — 7 bouteilles d'eau entamées alignées derrière un laptop, ticket de caisse entouré au stylo.
### 4. Identification (« c'est moi »)
Formules : « POV : il est [heure précise] et tu [situation exacte] » · « Toi aussi tu [micro-geste un peu honteux] à chaque fois que [situation] ? » · « Si tu [détail vérifiable maintenant], lis ça »
Ex : « POV : il est 16h et tu n'as bu qu'un café depuis ce matin »
Visuel slide 1 : précision documentaire (« c'est MA table ») — gourde pleine intacte près du clavier, 3 tasses vides empilées, horloge d'écran à 16:42, mains sur clavier, zéro visage.
### 5. Preuve sociale + FOMO
Formules : « Pourquoi les [groupe précis] ont tous arrêté de [comportement courant] » · « [Nombre précis impair] [cible] ont compris ça avant toi » · « Pendant que tu [habitude pénible], les autres [résultat déjà obtenu] »
Ex : « 12 400 créatrices ont arrêté de supprimer leurs selfies ce mois-ci »
Visuel slide 1 : la demande sociale qui s'accumule, sans produit — convo de groupe avec 4 messages « mais c'est quoi ta lumière sur tes photos ?? », réactions emoji.
### 6. Autorité / secret d'initié
Formules : « Un(e) [métier crédible] m'a montré pourquoi [douleur précise] » · « [Métier] depuis [N] ans : voici ce que je vois chez 9 [cible] sur 10 » · « Ce que les [profession] font avant [résultat envié] et ne montrent jamais »
Ex : « Une kiné m'a montré pourquoi mon mal de nuque revient chaque dimanche »
Visuel slide 1 : autorité sans visage — mains d'un praticien en tunique sur les omoplates d'un patient de dos, poster anatomique entouré au marqueur rouge.
### 7. Récit interrompu (Zeigarnik)
Formules : « Il y a [durée], je [situation basse datée]. Puis j'ai compris un truc. » · « J'ai [action chiffrée] pendant [durée] avant de comprendre mon erreur » · « Jour 1 vs jour [N] : ce qui s'est passé entre les deux tient en une image »
Ex : « Il y a 3 mois, je cachais mes jambes même à 30 degrés »
Visuel slide 1 : figer le point bas ou le geste interrompu — jambes en jogging épais sur une serviette de plage en plein soleil, short plié jamais enfilé à côté.
# ⬆️⬆️⬆️ FIN ZONE ÉDITABLE 1 ⬆️⬆️⬆️

# ⬇️⬇️⬇️ ZONE ÉDITABLE 2 — IDÉES DE SLIDES / ANGLES GAGNANTS (à enrichir) ⬇️⬇️⬇️
# Ajoute ici des structures de carrousels qui marchent, angles par niche, exemples de CTA.
# ⬆️⬆️⬆️ FIN ZONE ÉDITABLE 2 ⬆️⬆️⬆️
"""

_STRATEGY_OUTPUT = """# TA TÂCHE (ÉTAPE 1/2 — STRATÉGIE)
Analyse l'image + les infos. D'ABORD identifie précisément le produit, puis LE problème
n°1 (douleur/désir concret et spécifique) qu'il résout pour son acheteur type.

⚠️ QUALITÉ HOOK — INTERDICTIONS ABSOLUES :
- Jamais « ce produit / cet objet / cette solution » dans un hook : nomme la douleur ou le résultat PRÉCIS.
- Jamais de formule creuse (« le problème que X résout », « découvre... », « tu vas adorer »).
- Le hook doit utiliser UN biais psychologique précis (curiosity gap, contre-intuition,
  identification « si tu... », chiffre précis, aversion à la perte) et donner envie de swiper.

Renvoie UNIQUEMENT ce JSON (rien d'autre) :
{
  "type_slide": {
    "style": "quad_photo | fond_blanc | ia_cartoon",
    "label": "Nom lisible du style en français",
    "justification": "1-2 phrases : pourquoi ce style pour CE produit."
  },
  "probleme_principal": "LE problème/désir n°1, concret et spécifique, que ce produit résout (ex: « selfies sombres et granuleux le soir », pas « mauvaise qualité photo »).",
  "biais_psychologique": "Le biais utilisé par le hook (curiosity_gap | contre_intuition | identification | chiffre | aversion_perte).",
  "hook": "Texte du hook slide 1 — court, percutant, SPÉCIFIQUE au problème ci-dessus.",
  "slide1_visuel": "Scène visuelle PRÉCISE de la slide 1 qui matérialise ce problème SANS montrer le produit : qui, fait quoi, où, quel détail rend le problème VISIBLE à l'image (ex: « jeune femme qui se filme au téléphone dans une chambre sombre le soir, son visage à l'écran du téléphone est sombre et granuleux, déception visible »). INTERDIT : visage dramatique générique, personne qui se tient la tête.",
  "titre_carrousel": "Titre principal du carrousel (spécifique, même exigence que le hook).",
  "titre_variantes": ["variante 1", "variante 2"],
  "detected_niche": "Niche détectée."
}
"""

_CONTENT_OUTPUT = """# TA TÂCHE (ÉTAPE 2/2 — CONTENU)
On a déjà choisi la stratégie suivante :
- Style : {style} ({label})
- Hook (slide 1) : {hook}
- Titre du carrousel : {titre}
- Niche : {niche}

Produis maintenant le détail. Renvoie UNIQUEMENT ce JSON (rien d'autre) :
{{
  "slides": [
    {{
      "numero": 1,
      "type": "hook | value | cta",
      "texte": "Texte à afficher sur la slide.",
      "sous_texte": "Sous-texte optionnel (peut être vide).",
      "photo_a_prendre": "Photo PRÉCISE à shooter : cadrage, fond, angle, ce qu'on voit.",
      "emotion": "Émotion à transmettre.",
      "position_texte": "center | top | bottom"
    }}
  ],
  "cta": "Phrase de CTA de la dernière slide (vers le panier TikTok Shop).",
  "description_optimisee": "Description produit optimisée prête à coller (emojis, bénéfices ✨, CTA panier 🛒). 200-320 caractères.",
  "hashtags": ["2-3 tendances", "3-4 niche", "1-2 tiktokshop (max 8-10 total)"],
  "conseils_saves": ["Conseil 1 pour maximiser les sauvegardes.", "Conseil 2."]
}}
La slide 1 reprend le hook ci-dessus. La dernière slide est le CTA. Respecte le nb de slides typique du style.
"""


def _product_infos(product_name, price, currency, description, niche) -> str:
    infos = []
    if product_name: infos.append(f"- Nature / nom : {product_name}")
    if description:   infos.append(f"- Description : {description}")
    if price:         infos.append(f"- Prix : {price} {currency or 'EUR'}")
    if niche:         infos.append(f"- Niche : {niche}")
    return "Informations produit :\n" + "\n".join(infos) if infos else "Aucune info produit fournie."


# ════════════════════════════════════════════════════════════════════════════
# ÉTAPE 1 — STRATÉGIE (vision)
# ════════════════════════════════════════════════════════════════════════════
def generate_strategy(image_b64: str, product_name: Optional[str] = None,
                      price: Optional[str] = None, currency: str = "EUR",
                      description: Optional[str] = None, niche: Optional[str] = None,
                      preferred_style: Optional[str] = None, image_url: Optional[str] = None,
                      avoid: Optional[str] = None) -> dict:
    if not ai_providers.any_ai_key():
        raise RuntimeError("Aucune clé IA configurée (MISTRAL / GEMINI / ANTHROPIC)")
    # Image officielle (URL KeyAPI) prioritaire pour l'identification, sinon photo uploadée
    # (base64), sinon AUCUNE image → stratégie texte-only à partir de nom/description/prix
    # (sans ce cas, on envoyait « base64,None » → pixtral plantait → mock générique).
    img_src = image_url or (f"data:image/jpeg;base64,{image_b64}" if image_b64 else None)
    blocks = []
    if img_src:
        blocks.append({"type": "text", "text": "Voici l'image du produit à analyser :"})
        blocks.append({"type": "image_url", "image_url": {"url": img_src}})
    else:
        blocks.append({"type": "text", "text": "Pas d'image disponible : base-toi UNIQUEMENT sur les "
                       "informations produit ci-dessous (nom, description, prix, niche) pour identifier "
                       "précisément le produit et son problème n°1."})
    blocks.append({"type": "text", "text": _product_infos(product_name, price, currency, description, niche)})
    if preferred_style and preferred_style != "auto":
        blocks.append({"type": "text", "text": f"⚠️ L'utilisateur IMPOSE le style « {preferred_style} »."})
    blocks.append({"type": "text", "text": PHOTO_SLIDE_KNOWLEDGE})
    blocks.append({"type": "text", "text": _variation_block(avoid)})
    blocks.append({"type": "text", "text": _STRATEGY_OUTPUT})
    try:
        raw = ai_providers.vision_complete(blocks, timeout=60.0)
        data = _extract_json(raw)
        data["_fallback"] = False
        return data
    except Exception as e:
        print(f"photo_slide strategy error: {e}")
        return _mock_strategy(product_name, str(e))


# ════════════════════════════════════════════════════════════════════════════
# ÉTAPE 2 — CONTENU (texte rapide)
# ════════════════════════════════════════════════════════════════════════════
def generate_content(strategy: dict, product_name: Optional[str] = None,
                     price: Optional[str] = None, currency: str = "EUR",
                     description: Optional[str] = None, niche: Optional[str] = None,
                     avoid: Optional[str] = None) -> dict:
    if not ai_providers.any_ai_key():
        raise RuntimeError("Aucune clé IA configurée (MISTRAL / GEMINI / ANTHROPIC)")
    st = strategy.get("type_slide") or {}
    task = _CONTENT_OUTPUT.format(
        style=st.get("style", "auto"), label=st.get("label", ""),
        hook=strategy.get("hook", ""), titre=strategy.get("titre_carrousel", ""),
        niche=strategy.get("detected_niche") or niche or "non précisée",
    )
    prompt = (PHOTO_SLIDE_KNOWLEDGE + "\n\n"
              + _product_infos(product_name, price, currency, description, niche) + "\n\n"
              + _variation_block(avoid) + "\n\n"
              + task)
    try:
        raw = ai_providers.text_complete(prompt, timeout=45.0)
        return _extract_json(raw)
    except Exception as e:
        print(f"photo_slide content error: {e}")
        return _mock_content(product_name)


# ════════════════════════════════════════════════════════════════════════════
# Génération complète (one-shot) — gardée pour compat / fallback non-streamé
# ════════════════════════════════════════════════════════════════════════════
def generate_photo_slide(image_b64: str, product_name: Optional[str] = None,
                         price: Optional[str] = None, currency: str = "EUR",
                         description: Optional[str] = None, niche: Optional[str] = None,
                         preferred_style: Optional[str] = None, image_url: Optional[str] = None,
                         avoid: Optional[str] = None) -> dict:
    strat = generate_strategy(image_b64, product_name, price, currency, description, niche,
                              preferred_style, image_url=image_url, avoid=avoid)
    content = generate_content(strat, product_name, price, currency, description, niche, avoid=avoid)
    return {**strat, **content}


# ════════════════════════════════════════════════════════════════════════════
# Mocks (filets de sécurité si l'IA échoue — l'UI ne casse jamais)
# ════════════════════════════════════════════════════════════════════════════
def _mock_strategy(product_name: Optional[str] = None, err: Optional[str] = None) -> dict:
    """Filet de sécurité GÉNÉRIQUE (jamais spécifique à un produit) si l'IA échoue.
    On remonte l'erreur (_plan_error) pour le diagnostic au lieu d'inventer un faux titre."""
    p = (product_name or "ce produit").strip()
    return {
        "_fallback": True,
        "_plan_error": err,
        "type_slide": {"style": "fond_blanc", "label": "Fond Blanc (minimaliste premium)",
                       "justification": "Style épuré idéal pour lister des bénéfices et générer des saves."},
        "probleme_principal": None,
        "biais_psychologique": "curiosity_gap",
        "hook": f"Personne ne t'a dit pourquoi ton {p} ne suffit pas (slide 3 = déclic)",
        "slide1_visuel": None,
        "titre_carrousel": f"Ce que 90% des gens ratent avant d'acheter un {p}",
        "titre_variantes": [f"{p} : l'erreur que tout le monde fait", f"Avant d'acheter un {p}, regarde ça"],
        "detected_niche": None,
    }


def _mock_content(product_name: Optional[str] = None) -> dict:
    p = (product_name or "ce produit").strip()
    return {
        "slides": [
            {"numero": 1, "type": "hook", "texte": "Tu galères encore avec ça ?",
             "sous_texte": "(le problème que personne ne règle vraiment)",
             "photo_a_prendre": "Visuel d'accroche qui illustre LE problème — sans montrer le produit.",
             "emotion": "Curiosité + tension", "position_texte": "top"},
            {"numero": 2, "type": "value", "texte": "La vraie cause",
             "sous_texte": "Ce que la plupart des gens ratent",
             "photo_a_prendre": "Mise en situation du problème, ambiance authentique.",
             "emotion": "Reconnaissance du problème", "position_texte": "center"},
            {"numero": 3, "type": "solution", "texte": f"La solution : {p}",
             "sous_texte": "Simple, rapide, efficace",
             "photo_a_prendre": f"{p} mis en valeur, fidèle au produit réel, fond propre.",
             "emotion": "Soulagement", "position_texte": "center"},
            {"numero": 4, "type": "cta", "texte": "Dispo dans le panier jaune 🛒",
             "sous_texte": "Stock limité",
             "photo_a_prendre": f"{p} bien présenté + prix visible, flèche vers le panier.",
             "emotion": "Action immédiate", "position_texte": "bottom"},
        ],
        "cta": "Disponible maintenant dans le panier jaune 🛒 — stock limité.",
        "description_optimisee": (f"Tu cherches LE produit qui change tout ?\n\nVoici pourquoi {p} fait le buzz 👇\n"
                                  "✨ Règle un vrai problème\n✨ Résultat rapide\n✨ Simple à utiliser\n\n"
                                  "La solution dans le panier jaune 🛒"),
        "hashtags": ["tiktokshop", "tiktokmademebuyit", "pourtoi", "fyp", "bonplan", "shopping"],
        "conseils_saves": ["Format liste = forte probabilité de sauvegarde.",
                           "Slide 1 = problème (jamais le produit) pour maximiser le stop-scroll.",
                           "Numérotation claire incite à revenir au carrousel."],
    }
