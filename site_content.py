"""
📄 Source de vérité UNIQUE du contenu du site.

Toute valeur affichée à plusieurs endroits — promesse d'essai, prix, quotas,
liens sociaux, chiffres de la section preuve — vit ici et nulle part ailleurs.
Les gabarits y accèdent par le contexte Jinja (cf. main.py : _render).

RÈGLE : si une chaîne apparaît sur deux pages, elle doit venir d'ici. Une valeur
codée en dur dans un gabarit est un bug, pas un raccourci — c'est ce qui a
produit sept formulations différentes de la même promesse d'essai.

Les prix ne sont PAS redéfinis ici : ils viennent de feature_flags, déjà source
de vérité côté facturation. Les dupliquer recréerait exactement le problème que
ce fichier existe pour supprimer.
"""
from __future__ import annotations

import feature_flags as _ff

# ── L'ESSAI GRATUIT ───────────────────────────────────────────────────────
# Formulation unique, validée. Interdiction d'en écrire une variante ailleurs.
TRIAL_OFFER = "7 jours d'accès complet, sans carte bancaire"
TRIAL_OFFER_SHORT = "7 jours offerts"
TRIAL_DAYS = _ff.TRIAL_DAYS               # 7
TRIAL_ANALYSES = _ff.TRIAL_ANALYSES       # 10

# Nombre d'essais offerts sur chaque fonctionnalité consommant des crédits
# (Studio d'accroches, Coach carrousel) pendant l'essai.
TRIAL_FREE_USES = 3

# Formulation complète, à utiliser là où le détail doit être explicite (page
# tarifs, CGV). La promesse courte ne détaille pas les plafonds : les deux
# doivent rester cohérentes avec l'article 4 des CGV.
TRIAL_OFFER_FULL = (
    f"{TRIAL_DAYS} jours d'accès complet, sans carte bancaire — "
    f"{TRIAL_ANALYSES} analyses de vidéos et {TRIAL_FREE_USES} essais "
    f"sur chaque outil de création"
)

# ── L'OFFRE ───────────────────────────────────────────────────────────────
PLAN_NAME = "Qeerah Pro"
PRICE_MONTH = _ff.PRO_MONTHLY_PRICE                    # 29.99
PRICE_YEAR = _ff.PRO_YEARLY_PRICE                      # 299.0
PRICE_YEAR_MONTHLY = round(PRICE_YEAR / 12, 2)         # 24.92
PRICE_MONTH_YEARLY = round(PRICE_MONTH * 12, 2)        # 359.88
VAT_NOTICE = _ff.VAT_NOTICE

# Économie de l'annuel — CALCULÉE, jamais écrite en dur (cf. lot 2.5 : le site
# annonçait « 2 mois offerts » d'un côté et 359,88 € de l'autre, deux chiffres
# incompatibles).
SAVING_YEAR = round(PRICE_MONTH_YEARLY - PRICE_YEAR, 2)              # 60.88
SAVING_YEAR_PERCENT = round(SAVING_YEAR / PRICE_MONTH_YEARLY * 100)  # 17

# ── QUOTAS INCLUS ─────────────────────────────────────────────────────────
ANALYSES_PER_MONTH = _ff.PRO_ANALYSES_PER_MONTH        # 100

# ⚠️ À CONFIRMER : valeurs reprises de credits.PLAN_CREDITS["pro"], calibrées
# pour l'ancienne grille tarifaire. Ne pas afficher avant validation.
CREDITS_PER_MONTH = 30
CREDITS_PER_CAROUSEL = 10
CAROUSELS_PER_MONTH = CREDITS_PER_MONTH // CREDITS_PER_CAROUSEL      # 3

# ── SECTION PREUVE ────────────────────────────────────────────────────────
# Valeurs inchangées sur décision d'Aimeric. Écrites côté serveur : l'animation
# de comptage se superpose ensuite, elle ne part plus de zéro.
STATS = [
    {"value": 1000, "prefix": "+", "label": "top vidéos analysées"},
    {"value": 31,   "prefix": "+", "label": "leviers de vente décodés"},
    {"value": 10,   "prefix": "+", "label": "créateurs TikTok Shop FR"},
    {"value": 6,    "prefix": "+", "label": "marchés analysés"},
]

# ── DIMENSIONS D'ANALYSE ──────────────────────────────────────────────────
# Sept, et non huit : le site en annonçait huit et n'en listait que sept.
# Décision d'Aimeric : on annonce le nombre réel.
ANALYSIS_DIMENSIONS = [
    "Accroche", "Rétention", "Vente", "Émotion",
    "Conversion", "Algorithme", "Score global",
]
ANALYSIS_DIMENSIONS_COUNT = len(ANALYSIS_DIMENSIONS)                 # 7
ANALYSIS_DIMENSIONS_TEXT = ", ".join(ANALYSIS_DIMENSIONS)

# ── LIENS ─────────────────────────────────────────────────────────────────
SOCIAL = {
    "tiktok": "https://www.tiktok.com/@qeerah.app",
}
# L'ancien pseudonyme contenait la marque « tiktokshop », à l'origine d'une
# plainte. Aucune occurrence ne doit subsister dans le dépôt.

CONTACT_EMAIL = "contact@qeerah.com"
# Domaine réellement servi par Render : qeerah.com redirige en 308 vers www.
# Une balise canonical doit désigner l'URL finale, pas une URL redirigée.
SITE_URL = "https://www.qeerah.com"

# ── ÉDITEUR (mentions légales) ────────────────────────────────────────────
# Repris des CGV, donc déjà vérifié. Les champs vides sont à fournir : ils ne
# seront jamais inventés.
COMPANY = {
    "name": "DOPE VENTURES",
    "legal_form": "SASU",
    "capital": "100 €",
    "rcs": "RCS Paris 106 482 508",
    "siren": "106 482 508",
    # SIRET du siège, relevé sur l'annuaire officiel des entreprises
    # (recherche-entreprises.api.gouv.fr) : adresse, forme juridique et code
    # activité concordent avec les CGV.
    "siret": "106 482 508 00012",
    "address": "47 rue Vivienne, 75002 Paris, France",
    "president": "Aimeric Bourgon",
    "publication_director": "Aimeric Bourgon",
    "activity_code": "62.01Z",
    "vat_notice": VAT_NOTICE,
    # Hébergeur — obligatoire (LCEN art. 6). Relevé sur les conditions
    # d'utilisation de Render : le préambule identifie « Render Services, Inc. »
    # comme éditeur du service, et 525 Brannan Street est l'adresse postale
    # qu'ils y publient.
    "host": {
        "name": "Render Services, Inc.",
        "address": "525 Brannan Street, Suite 300, San Francisco, CA 94107, États-Unis",
        "url": "https://render.com",
    },
    "mediator": {
        "name": "CM2C — Centre de Médiation de la Consommation de Conciliateurs de Justice",
        "address": "14 rue Saint Jean, 75017 Paris",
        "url": "https://www.cm2c.net",
    },
}

# ── PREUVE SOCIALE ────────────────────────────────────────────────────────
# Aucun témoignage rédigé n'existe à ce jour : la section reste masquée, y
# compris son lien de navigation. Un conteneur vide nuit plus que son absence.
TESTIMONIALS_ENABLED = False


def context() -> dict:
    """Contexte injecté dans tous les gabarits."""
    return {
        "TRIAL_OFFER": TRIAL_OFFER,
        "TRIAL_OFFER_SHORT": TRIAL_OFFER_SHORT,
        "TRIAL_OFFER_FULL": TRIAL_OFFER_FULL,
        "TRIAL_DAYS": TRIAL_DAYS,
        "TRIAL_ANALYSES": TRIAL_ANALYSES,
        "TRIAL_FREE_USES": TRIAL_FREE_USES,

        "PLAN_NAME": PLAN_NAME,
        "PRICE_MONTH": PRICE_MONTH,
        "PRICE_YEAR": PRICE_YEAR,
        "PRICE_YEAR_MONTHLY": PRICE_YEAR_MONTHLY,
        "PRICE_MONTH_YEARLY": PRICE_MONTH_YEARLY,
        "SAVING_YEAR": SAVING_YEAR,
        "SAVING_YEAR_PERCENT": SAVING_YEAR_PERCENT,
        "VAT_NOTICE": VAT_NOTICE,

        "ANALYSES_PER_MONTH": ANALYSES_PER_MONTH,
        "CREDITS_PER_MONTH": CREDITS_PER_MONTH,
        "CAROUSELS_PER_MONTH": CAROUSELS_PER_MONTH,
        "CREDITS_PER_CAROUSEL": CREDITS_PER_CAROUSEL,

        "STATS": STATS,
        "ANALYSIS_DIMENSIONS": ANALYSIS_DIMENSIONS,
        "ANALYSIS_DIMENSIONS_COUNT": ANALYSIS_DIMENSIONS_COUNT,
        "ANALYSIS_DIMENSIONS_TEXT": ANALYSIS_DIMENSIONS_TEXT,

        "SOCIAL": SOCIAL,
        "CONTACT_EMAIL": CONTACT_EMAIL,
        "SITE_URL": SITE_URL,
        "COMPANY": COMPANY,
        "TESTIMONIALS_ENABLED": TESTIMONIALS_ENABLED,

        # Formatage français des montants : 29.99 → « 29,99 »
        "eur": lambda v: (f"{v:.2f}".rstrip("0").rstrip(".") if v == int(v)
                          else f"{v:.2f}").replace(".", ","),
    }
