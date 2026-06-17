from __future__ import annotations

"""
🚦 Feature flags pilotés par DATE — colonne vertébrale du lancement échelonné.

Activation 100 % côté serveur (jamais de confiance dans le front). L'état est
CALCULÉ EN DIRECT à chaque requête à partir de la roadmap : pas de cron, pas de
table à maintenir, donc rien à oublier de flipper le jour J.

Roadmap (confirmée 2026-06-17) :
  • 31 juil. 2026  → lancement public : PRO visible (offre 9,99 €)
  • 20 août 2026   → PRO passe à 11,99 €
  • 16 sept. 2026  → PRO prix final 12,99 € + ouverture GOLD (79,99 €) & AGENCY (249 €)
  • 15 oct. 2026   → ouverture des LTD (199 / 299 / 499 €)

Surcharge manuelle possible pour tester / forcer un lancement anticipé :
  FF_PUBLIC_LAUNCH=on   FF_GOLD_AVAILABLE=on   FF_LTD_AVAILABLE=off  ...
(valeurs acceptées : on/1/true/yes  ou  off/0/false/no)
"""

import os
from datetime import date

# ── Dates de la roadmap ───────────────────────────────────────────────────
ROADMAP: dict[str, date] = {
    "public_launch":    date(2026, 7, 31),   # PRO visible publiquement
    "pro_price_11_99":  date(2026, 8, 20),   # PRO → 11,99 €
    "pro_price_12_99":  date(2026, 9, 16),   # PRO → 12,99 € (prix final)
    "gold_available":   date(2026, 9, 16),
    "agency_available": date(2026, 9, 16),
    "ltd_available":    date(2026, 10, 15),
}

# Prix de référence (l'« original » barré dans l'UI)
PRO_FINAL_PRICE = 12.99
GOLD_PROMO, GOLD_ORIGINAL = 79.99, 99.0
AGENCY_PROMO, AGENCY_ORIGINAL = 249.0, 299.0

_TRUE = {"on", "1", "true", "yes", "y"}
_FALSE = {"off", "0", "false", "no", "n"}

_FR_MONTHS = {
    1: "janvier", 2: "février", 3: "mars", 4: "avril", 5: "mai", 6: "juin",
    7: "juillet", 8: "août", 9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre",
}


def _env_override(flag: str):
    """Retourne True/False si FF_<FLAG> est défini, sinon None."""
    v = os.getenv("FF_" + flag.upper(), "").strip().lower()
    if v in _TRUE:
        return True
    if v in _FALSE:
        return False
    return None


def is_enabled(flag: str) -> bool:
    """Un flag est actif si la date du jour a atteint sa date d'activation
    (ou si une variable d'env le force)."""
    ov = _env_override(flag)
    if ov is not None:
        return ov
    d = ROADMAP.get(flag)
    return d is not None and date.today() >= d


def available_plans() -> dict:
    """Quels plans sont achetables aujourd'hui."""
    return {
        "free":   True,                          # toujours dispo
        "pro":    is_enabled("public_launch"),
        "gold":   is_enabled("gold_available"),
        "agency": is_enabled("agency_available"),
        "ltd":    is_enabled("ltd_available"),
    }


def current_prices() -> dict:
    """Prix en vigueur selon la date (PRO : 9,99 → 11,99 → 12,99)."""
    if is_enabled("pro_price_12_99"):
        pro = PRO_FINAL_PRICE
    elif is_enabled("pro_price_11_99"):
        pro = 11.99
    else:
        pro = 9.99
    return {
        "pro":    {"current": pro,          "original": PRO_FINAL_PRICE,
                   "promo": pro < PRO_FINAL_PRICE},
        "gold":   {"current": GOLD_PROMO,   "original": GOLD_ORIGINAL,   "promo": True},
        "agency": {"current": AGENCY_PROMO, "original": AGENCY_ORIGINAL, "promo": True},
    }


def _fmt(d: date) -> str:
    return f"{d.day} {_FR_MONTHS.get(d.month, d.month)} {d.year}"


def availability_dates() -> dict:
    """Dates lisibles pour l'UI (« 🔜 disponible le … »)."""
    return {
        "pro":    _fmt(ROADMAP["public_launch"]),
        "gold":   _fmt(ROADMAP["gold_available"]),
        "agency": _fmt(ROADMAP["agency_available"]),
        "ltd":    _fmt(ROADMAP["ltd_available"]),
    }


def snapshot() -> dict:
    """Vue complète (pour l'admin / le débogage)."""
    return {
        "today": date.today().isoformat(),
        "plans": available_plans(),
        "prices": current_prices(),
        "dates": availability_dates(),
        "flags": {k: is_enabled(k) for k in ROADMAP},
        "overrides": {k: _env_override(k) for k in ROADMAP if _env_override(k) is not None},
    }
