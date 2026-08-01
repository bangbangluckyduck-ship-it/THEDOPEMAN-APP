from __future__ import annotations

"""
💰 Offre commerciale — source de vérité unique des prix affichés.

Une seule offre publique : **Qeerah Pro**, 29,99 €/mois ou 299 €/an.
Aucun palier intermédiaire, aucune offre agence publique, aucun prix barré,
aucun prix qui varie selon la date.

Ce module remplace l'ancien système de lancement échelonné (PRO 9,99 → 11,99 →
12,99 €, GOLD, AGENCY, LTD, roadmap datée). Les fonctions publiques sont
conservées — `available_plans()`, `current_prices()`, `is_enabled()`… — parce
que main.py et le front les consomment ; elles ne décrivent simplement plus
qu'une seule offre.

TVA : DOPE VENTURES est en franchise en base (art. 293 B du CGI). Les prix
affichés sont donc à la fois nets et TTC — c'est le montant réellement payé.
La mention légale est obligatoire partout où le prix apparaît.
"""

import os

# ── L'offre ───────────────────────────────────────────────────────────────
PRO_MONTHLY_PRICE = 29.99
PRO_YEARLY_PRICE  = 299.0

# Deux mois offerts : 299 € au lieu de 12 × 29,99 = 359,88 €.
PRO_YEARLY_MONTHS_FREE = 2

# Quota inclus, par cycle mensuel de facturation (cf. analysis_quota.py).
PRO_ANALYSES_PER_MONTH = 100

# Essai gratuit : 7 jours, accès complet, 10 analyses.
TRIAL_DAYS     = 7
TRIAL_ANALYSES = 10

VAT_NOTICE = "TVA non applicable, article 293 B du CGI"

_TRUE  = {"on", "1", "true", "yes", "y"}
_FALSE = {"off", "0", "false", "no", "n"}


def _env_override(flag: str):
    """Retourne True/False si FF_<FLAG> est défini, sinon None."""
    v = os.getenv("FF_" + flag.upper(), "").strip().lower()
    if v in _TRUE:
        return True
    if v in _FALSE:
        return False
    return None


def is_enabled(flag: str) -> bool:
    """Il n'y a plus de roadmap datée : l'offre Pro est ouverte en permanence,
    tout le reste est fermé. Une variable FF_<FLAG> permet encore de forcer un
    état ponctuellement (tests, coupure d'urgence de la souscription)."""
    ov = _env_override(flag)
    if ov is not None:
        return ov
    return flag in ("public_launch", "pro_available")


def available_plans() -> dict:
    """Ce qui est souscriptible aujourd'hui. `gold`/`agency`/`ltd` restent
    présents dans la réponse — le front les lit encore — mais toujours à False :
    ces plans ne sont plus vendus. Les comptes historiques qui les portent
    conservent leur accès (cf. analysis_quota._SUBSCRIBED_TIERS)."""
    return {
        "pro":    is_enabled("public_launch"),
        "free":   False,      # plus d'offre gratuite : un essai de 7 jours la remplace
        "gold":   False,
        "agency": False,      # sur devis uniquement, cf. page de comparaison
        "ltd":    False,
    }


def current_prices() -> dict:
    """Prix en vigueur. Ni `original` ni `promo` : les prix barrés sont proscrits."""
    return {
        "pro": {
            "month":        PRO_MONTHLY_PRICE,
            "year":         PRO_YEARLY_PRICE,
            "year_monthly": round(PRO_YEARLY_PRICE / 12, 2),   # ~24,92 €/mois
            "months_free":  PRO_YEARLY_MONTHS_FREE,
            "currency":     "EUR",
            "vat_notice":   VAT_NOTICE,
        }
    }


def offer_summary() -> dict:
    """Tout ce dont le front a besoin pour afficher l'offre, en un appel."""
    return {
        "name":     "Qeerah Pro",
        "prices":   current_prices()["pro"],
        "analyses": PRO_ANALYSES_PER_MONTH,
        "trial":    {"days": TRIAL_DAYS, "analyses": TRIAL_ANALYSES},
    }


def availability_dates() -> dict:
    """Conservée pour compatibilité : plus aucune ouverture n'est programmée."""
    return {"pro": "", "gold": "", "agency": "", "ltd": ""}


def snapshot() -> dict:
    """Vue complète (admin / débogage)."""
    return {
        "offer":     offer_summary(),
        "plans":     available_plans(),
        "prices":    current_prices(),
        "overrides": {k: _env_override(k)
                      for k in ("public_launch", "pro_available")
                      if _env_override(k) is not None},
    }
