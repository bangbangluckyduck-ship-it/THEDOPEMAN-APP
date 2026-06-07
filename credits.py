"""
💎 Système de crédits — AI Video Prompt Studio.

- Crédits d'ABONNEMENT : le total dépend du plan (calculé serveur), reset le 1er du
  mois. Reset « à la lecture » (pas de cron) : si la date de reset est passée, on
  remet le compteur à 0.
- Crédits ACHETÉS : packs (validité 1 mois). Consommés APRÈS l'abonnement, par date
  d'expiration la plus proche. (Achat réel via Stripe = différé.)

Toutes les fonctions prennent le client supabase en paramètre (best-effort).
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Optional

# Crédits d'abonnement inclus par plan (par mois).
PLAN_CREDITS = {
    "free": 0,
    "pro": 10,
    "gold": 50,
    "agency": 200,
    "beta": 200,
    "admin": 99999,
}

# Coût d'une génération par niveau (1→5).
LEVEL_COST = {1: 1, 2: 2, 3: 3, 4: 5, 5: 10}

# Packs achetables (validité 1 mois). Prix indicatifs (Stripe à brancher).
CREDIT_PACKS = {
    "decouverte": {"label": "Pack Découverte", "credits": 20, "price": 9},
    "standard":   {"label": "Pack Standard", "credits": 50, "price": 19, "best": True},
    "pro":        {"label": "Pack Pro", "credits": 150, "price": 49},
    "agency":     {"label": "Pack Agency", "credits": 500, "price": 129},
}


def plan_total(tier: Optional[str]) -> int:
    return PLAN_CREDITS.get((tier or "free").lower(), 0)


def level_cost(level: int, platform: Optional[str] = None) -> int:
    base = LEVEL_COST.get(int(level), 1)
    if (platform or "").lower() == "all":   # « toutes plateformes » → +50%
        base = int(round(base * 1.5))
    return base


def _first_of_next_month(now: datetime) -> datetime:
    year, month = now.year, now.month
    if month == 12:
        return datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    return datetime(year, month + 1, 1, tzinfo=timezone.utc)


def _parse_dt(s) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def _ensure_subscription_fresh(supabase, email: str) -> int:
    """Lit (ou crée) la ligne user_credits et applique le reset mensuel à la lecture.
    Renvoie subscription_used à jour."""
    now = datetime.now(timezone.utc)
    used = 0
    reset_date = None
    try:
        r = supabase.table("user_credits").select("subscription_used,subscription_reset_date").eq("email", email).execute()
        if r.data:
            used = r.data[0].get("subscription_used") or 0
            reset_date = _parse_dt(r.data[0].get("subscription_reset_date"))
    except Exception:
        return 0

    need_write = False
    if reset_date is None:
        reset_date = _first_of_next_month(now)
        need_write = True
    elif now >= reset_date:
        used = 0
        reset_date = _first_of_next_month(now)
        need_write = True

    if need_write:
        try:
            supabase.table("user_credits").upsert({
                "email": email,
                "subscription_used": used,
                "subscription_reset_date": reset_date.isoformat(),
                "updated_at": now.isoformat(),
            }, on_conflict="email").execute()
        except Exception:
            pass
    return used


def _active_purchases(supabase, email: str) -> list:
    """Achats non expirés (et marque expirés ceux qui le sont)."""
    now = datetime.now(timezone.utc)
    try:
        r = supabase.table("credit_purchases").select(
            "id,credits_remaining,expires_at,is_expired,pack_name").eq("email", email).eq("is_expired", False).execute()
    except Exception:
        return []
    active = []
    for p in (r.data or []):
        exp = _parse_dt(p.get("expires_at"))
        if (p.get("credits_remaining") or 0) <= 0 or (exp and now >= exp):
            try:
                supabase.table("credit_purchases").update({"is_expired": True}).eq("id", p["id"]).execute()
            except Exception:
                pass
            continue
        active.append(p)
    active.sort(key=lambda p: _parse_dt(p.get("expires_at")) or now)  # expiration la + proche d'abord
    return active


def get_balance(supabase, email: str, tier: str) -> dict:
    """Solde complet : abonnement + achats. Calcul à la lecture (reset/expiration)."""
    total_sub = plan_total(tier)
    if not supabase or not email:
        return {"subscription": {"total": total_sub, "used": 0, "remaining": total_sub, "reset_date": None},
                "purchased": {"remaining": 0, "next_expiry": None}, "total_available": total_sub}

    used = _ensure_subscription_fresh(supabase, email)
    sub_remaining = max(0, total_sub - used)
    reset_date = None
    try:
        r = supabase.table("user_credits").select("subscription_reset_date").eq("email", email).execute()
        if r.data:
            reset_date = r.data[0].get("subscription_reset_date")
    except Exception:
        pass

    purchases = _active_purchases(supabase, email)
    purchased_remaining = sum(p.get("credits_remaining") or 0 for p in purchases)
    next_expiry = purchases[0].get("expires_at") if purchases else None

    return {
        "subscription": {"total": total_sub, "used": used, "remaining": sub_remaining, "reset_date": reset_date},
        "purchased": {"remaining": purchased_remaining, "next_expiry": next_expiry},
        "total_available": sub_remaining + purchased_remaining,
    }


def has_credits(supabase, email: str, tier: str, amount: int) -> bool:
    return get_balance(supabase, email, tier).get("total_available", 0) >= amount


def debit(supabase, email: str, tier: str, amount: int) -> bool:
    """Débite `amount` : abonnement d'abord, puis achats (expiration la + proche).
    Renvoie True si débité, False si solde insuffisant."""
    if amount <= 0:
        return True
    if not supabase or not email:
        return False
    bal = get_balance(supabase, email, tier)
    if bal["total_available"] < amount:
        return False

    now = datetime.now(timezone.utc).isoformat()
    remaining = amount

    # 1) Abonnement
    sub_remaining = bal["subscription"]["remaining"]
    take = min(remaining, sub_remaining)
    if take > 0:
        new_used = (bal["subscription"]["used"] or 0) + take
        try:
            supabase.table("user_credits").upsert(
                {"email": email, "subscription_used": new_used, "updated_at": now},
                on_conflict="email").execute()
        except Exception:
            return False
        remaining -= take

    # 2) Achats (FIFO par expiration)
    if remaining > 0:
        for p in _active_purchases(supabase, email):
            if remaining <= 0:
                break
            avail = p.get("credits_remaining") or 0
            t = min(remaining, avail)
            if t <= 0:
                continue
            try:
                supabase.table("credit_purchases").update(
                    {"credits_remaining": avail - t}).eq("id", p["id"]).execute()
            except Exception:
                continue
            remaining -= t

    return remaining <= 0
