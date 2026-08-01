"""
📊 Quota d'analyses — offre unique « Qeerah Pro ».

  • Abonné      : 100 analyses par cycle MENSUEL, aligné sur la facturation Stripe
  • Essai       : 7 jours après inscription, accès complet, 10 analyses
  • Essai expiré: 0 analyse (les analyses passées restent consultables)

Pourquoi ce module remplace check_quota()/monthly_usage (auth.py) sur l'analyse
vidéo : l'ancien compteur travaillait sur le MOIS CALENDAIRE. Un abonné du 20 du
mois voyait donc son quota remis à zéro 10 jours après son paiement. Ici, la
période est ancrée sur `current_period_start` renvoyé par Stripe.

Cas de l'abonnement ANNUEL : Stripe ne fournit qu'un cycle d'un an. Le quota,
lui, reste de 100 par mois — sinon un abonné annuel serait plafonné à 100
analyses pour toute l'année. On dérive donc une fenêtre mensuelle glissante à
partir de la date anniversaire (cf. _monthly_window).

Reset « à la lecture », sans cron : au changement de fenêtre, une nouvelle ligne
est créée dans analysis_quota_periods. Les lignes précédentes sont conservées
(historique de consommation).

Comportement en cas de panne Supabase : FAIL-OPEN (on laisse passer). C'est le
choix déjà fait partout ailleurs dans le code (credits.py, recherche_quota.py) ;
bloquer toutes les analyses parce que la base de comptage est indisponible
coûterait plus cher qu'un dépassement ponctuel.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple

from fastapi import HTTPException

from supabase_client import supabase_service as supabase, _get_user_id

# ── Plafonds ──────────────────────────────────────────────────────────────
PRO_PERIOD_LIMIT = 100      # analyses par cycle mensuel (Qeerah Pro)
TRIAL_LIMIT      = 10       # analyses pendant l'essai gratuit
TRIAL_DAYS       = 7

# Tiers considérés comme abonnés. gold/agency/beta ne sont plus souscriptibles
# (refonte tarifaire) mais restent traités comme des abonnés : des comptes
# historiques peuvent encore les porter, et il n'est pas question de les couper.
_SUBSCRIBED_TIERS = {"pro", "gold", "agency", "beta"}
_UNLIMITED_TIERS  = {"admin"}

_FR_MONTHS = {
    1: "janvier", 2: "février", 3: "mars", 4: "avril", 5: "mai", 6: "juin",
    7: "juillet", 8: "août", 9: "septembre", 10: "octobre", 11: "novembre",
    12: "décembre",
}


# ── Utilitaires date ──────────────────────────────────────────────────────

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_dt(s) -> Optional[datetime]:
    if not s:
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _add_months(d: datetime, n: int) -> datetime:
    """Ajoute n mois en conservant le jour quand c'est possible.

    Gère les fins de mois : une ancre au 31 janvier donne le 28 février (ou le
    29 en année bissextile), puis le 31 mars — le jour d'ancrage n'est jamais
    perdu, il est seulement rogné le temps d'un mois court.
    """
    total = d.month - 1 + n
    year = d.year + total // 12
    month = total % 12 + 1
    # Dernier jour du mois cible
    if month == 12:
        last = 31
    else:
        last = (datetime(year, month + 1, 1, tzinfo=d.tzinfo) - timedelta(days=1)).day
    return d.replace(year=year, month=month, day=min(d.day, last))


def _monthly_window(anchor: datetime, now: datetime) -> Tuple[datetime, datetime]:
    """Fenêtre mensuelle courante [début, fin) à partir d'une date d'ancrage.

    Mensuel  : l'ancre est le début du cycle Stripe, la fenêtre coïncide avec lui.
    Annuel   : l'ancre est la date de souscription ; on avance de mois en mois
               jusqu'à encadrer `now`. Un abonné du 15 mars voit donc son quota
               repartir le 15 de chaque mois, toute l'année.
    """
    if now < anchor:
        return anchor, _add_months(anchor, 1)

    # Estimation directe du nombre de mois écoulés, puis ajustement (±1) pour
    # absorber les décalages de fin de mois. Évite une boucle sur 12 itérations.
    k = (now.year - anchor.year) * 12 + (now.month - anchor.month)
    start = _add_months(anchor, k)
    if start > now:
        k -= 1
        start = _add_months(anchor, k)
    end = _add_months(anchor, k + 1)
    while end <= now:            # filet de sécurité (dates limites)
        k += 1
        start, end = _add_months(anchor, k), _add_months(anchor, k + 1)
    return start, end


def format_fr(d: Optional[datetime]) -> str:
    """« 9 août 2026 » — pour les messages utilisateur."""
    if not d:
        return ""
    return f"{d.day} {_FR_MONTHS.get(d.month, d.month)} {d.year}"


# ── Lecture du compte ─────────────────────────────────────────────────────

def _user_row(email: str) -> dict:
    if not supabase or not email:
        return {}
    try:
        r = supabase.table("users").select(
            "id,tier,trial_ends_at,current_period_start,current_period_end,created_at"
        ).eq("email", email).execute()
        return (r.data or [{}])[0]
    except Exception as e:
        print(f"analysis_quota._user_row error: {e}")
        return {}


def resolve_period(email: str, tier: str) -> dict:
    """Détermine la période de quota applicable.

    Renvoie {kind, start, end, limit} où kind vaut :
      'unlimited'     → admin, aucun plafond
      'subscription'  → abonné, fenêtre mensuelle ancrée sur Stripe
      'trial'         → essai gratuit en cours
      'expired'       → essai terminé, pas d'abonnement → 0 analyse
    """
    tier = (tier or "free").lower()
    now = _now()

    if tier in _UNLIMITED_TIERS:
        return {"kind": "unlimited", "start": None, "end": None, "limit": None}

    row = _user_row(email)

    if tier in _SUBSCRIBED_TIERS:
        anchor = _parse_dt(row.get("current_period_start"))
        if not anchor:
            # Abonné sans bornes Stripe connues (webhook pas encore passé, ou
            # compte historique) : on ancre sur la date de création du compte
            # plutôt que sur le 1er du mois — pas de quota offert en double.
            anchor = _parse_dt(row.get("created_at")) or now
        start, end = _monthly_window(anchor, now)
        return {"kind": "subscription", "start": start, "end": end,
                "limit": PRO_PERIOD_LIMIT}

    trial_end = _parse_dt(row.get("trial_ends_at"))
    if trial_end and now < trial_end:
        return {"kind": "trial", "start": trial_end - timedelta(days=TRIAL_DAYS),
                "end": trial_end, "limit": TRIAL_LIMIT}

    return {"kind": "expired", "start": None, "end": trial_end, "limit": 0}


# ── Compteur ──────────────────────────────────────────────────────────────

def _count(user_id: str, start: datetime) -> int:
    if not supabase or not user_id or not start:
        return 0
    try:
        r = supabase.table("analysis_quota_periods").select("count") \
            .eq("user_id", user_id).eq("period_start", start.isoformat()).execute()
        return (r.data[0].get("count") or 0) if r.data else 0
    except Exception as e:
        print(f"analysis_quota._count error: {e}")
        return 0


def get_state(email: str, tier: str) -> dict:
    """État complet du quota, pour l'API et l'affichage tableau de bord."""
    period = resolve_period(email, tier)
    limit = period["limit"]

    if period["kind"] == "unlimited":
        return {"kind": "unlimited", "used": 0, "limit": None, "remaining": None,
                "reset_at": None, "reset_label": "", "blocked": False}

    used = _count(_get_user_id(email), period["start"]) if period["start"] else 0
    remaining = max(0, (limit or 0) - used)
    return {
        "kind":        period["kind"],
        "used":        used,
        "limit":       limit,
        "remaining":   remaining,
        "reset_at":    period["end"].isoformat() if period["end"] else None,
        "reset_label": format_fr(period["end"]),
        "blocked":     remaining <= 0,
    }


def check(user: dict) -> None:
    """Lève une HTTPException si l'utilisateur ne peut pas lancer d'analyse.

    429 → quota du cycle épuisé (message avec la date de réinitialisation)
    402 → essai terminé, aucun abonnement actif
    """
    if not user or not user.get("valid"):
        return
    if user.get("is_admin"):
        return

    tier = (user.get("tier") or "free").lower()
    state = get_state(user["email"], tier)

    if state["kind"] == "unlimited" or not state["blocked"]:
        return

    if state["kind"] == "expired":
        raise HTTPException(
            status_code=402,
            detail="Ton essai gratuit est terminé. Abonne-toi à Qeerah Pro pour "
                   "continuer à analyser tes vidéos — tes analyses précédentes "
                   "restent consultables.",
        )

    if state["kind"] == "trial":
        raise HTTPException(
            status_code=429,
            detail=f"Tu as utilisé les {TRIAL_LIMIT} analyses de ton essai gratuit. "
                   "Abonne-toi à Qeerah Pro pour 100 analyses par mois.",
        )

    raise HTTPException(
        status_code=429,
        detail=f"Quota mensuel atteint ({state['limit']} analyses) — "
               f"réinitialisation le {state['reset_label']}.",
    )


def increment(email: str, tier: str) -> int:
    """Incrémente le compteur du cycle courant. À n'appeler QUE sur une analyse
    réellement aboutie — jamais sur une erreur API, jamais sur un cache-hit."""
    if not supabase or not email:
        return 0

    period = resolve_period(email, tier)
    if period["kind"] == "unlimited" or not period["start"]:
        return 0

    user_id = _get_user_id(email)
    if not user_id:
        return 0

    start_iso = period["start"].isoformat()
    now_iso = _now().isoformat()
    try:
        existing = supabase.table("analysis_quota_periods").select("id,count") \
            .eq("user_id", user_id).eq("period_start", start_iso).execute()
        if existing.data:
            new_count = (existing.data[0].get("count") or 0) + 1
            supabase.table("analysis_quota_periods").update(
                {"count": new_count, "updated_at": now_iso}
            ).eq("id", existing.data[0]["id"]).execute()
            return new_count

        supabase.table("analysis_quota_periods").insert({
            "user_id":      user_id,
            "period_start": start_iso,
            "period_end":   period["end"].isoformat(),
            "count":        1,
            "limit_value":  period["limit"],
            "kind":         period["kind"],
        }).execute()
        return 1
    except Exception as e:
        print(f"analysis_quota.increment error: {e}")
        return 0


# ── Cycle de facturation (appelé par le webhook Stripe) ───────────────────

def set_billing_period(email: str, start: Optional[datetime],
                       end: Optional[datetime]) -> None:
    """Enregistre les bornes du cycle Stripe sur le compte.

    Appelé sur checkout.session.completed ET sur invoice.paid : c'est ce qui
    fait repartir le quota au renouvellement. Le compteur n'est pas remis à
    zéro ici — le changement de fenêtre suffit, puisque le comptage est indexé
    par period_start (nouvelle fenêtre = nouvelle ligne à 0).
    """
    if not supabase or not email or not start:
        return
    try:
        supabase.table("users").update({
            "current_period_start": start.isoformat(),
            "current_period_end":   end.isoformat() if end else None,
        }).eq("email", email.lower().strip()).execute()
    except Exception as e:
        print(f"analysis_quota.set_billing_period error: {e}")


def start_trial(email: str) -> None:
    """Démarre l'essai de 7 jours à l'inscription. Ne fait rien si un essai a
    déjà été posé : re-créer un compte ne doit pas rallonger l'essai."""
    if not supabase or not email:
        return
    try:
        email = email.lower().strip()
        r = supabase.table("users").select("trial_ends_at").eq("email", email).execute()
        if r.data and r.data[0].get("trial_ends_at"):
            return
        supabase.table("users").update(
            {"trial_ends_at": (_now() + timedelta(days=TRIAL_DAYS)).isoformat()}
        ).eq("email", email).execute()
    except Exception as e:
        print(f"analysis_quota.start_trial error: {e}")
