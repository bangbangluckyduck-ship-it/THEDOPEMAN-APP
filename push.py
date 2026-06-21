from __future__ import annotations

"""
Web Push (PWA) — abonnements + envoi via VAPID.

Tout est défensif : si `pywebpush` n'est pas installé ou si les clés VAPID ne
sont pas configurées, les fonctions renvoient simplement 0/False sans casser
le reste de l'app. Les abonnements expirés (404/410) sont purgés à l'envoi.
"""

import os
import json

VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY", "").strip()
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY", "").strip()
VAPID_SUBJECT = os.getenv("VAPID_SUBJECT", "mailto:contact@qeerah.com").strip()


def is_configured() -> bool:
    return bool(VAPID_PUBLIC_KEY and VAPID_PRIVATE_KEY)


# ── Abonnements (DB) ──────────────────────────────────────────────────────
def save_subscription(supabase, sub: dict, email: str | None, is_admin: bool, user_agent: str | None) -> bool:
    if not supabase:
        return False
    keys = sub.get("keys") or {}
    endpoint = sub.get("endpoint")
    if not endpoint or not keys.get("p256dh") or not keys.get("auth"):
        return False
    try:
        supabase.table("push_subscriptions").upsert({
            "endpoint": endpoint,
            "p256dh": keys["p256dh"],
            "auth": keys["auth"],
            "email": (email or None),
            "is_admin": bool(is_admin),
            "user_agent": (user_agent or "")[:300],
        }, on_conflict="endpoint").execute()
        return True
    except Exception as e:
        print(f"[push] save error: {e}")
        return False


def remove_subscription(supabase, endpoint: str) -> None:
    if not supabase or not endpoint:
        return
    try:
        supabase.table("push_subscriptions").delete().eq("endpoint", endpoint).execute()
    except Exception as e:
        print(f"[push] remove error: {e}")


# ── Envoi ─────────────────────────────────────────────────────────────────
def _send_one(supabase, row: dict, payload: dict) -> bool:
    """Envoie à un abonnement ; purge si expiré (404/410)."""
    try:
        from pywebpush import webpush, WebPushException
    except Exception as e:
        print(f"[push] pywebpush indisponible: {e}")
        return False
    info = {"endpoint": row["endpoint"], "keys": {"p256dh": row["p256dh"], "auth": row["auth"]}}
    try:
        webpush(
            subscription_info=info,
            data=json.dumps(payload),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_SUBJECT},
            timeout=10,
        )
        return True
    except WebPushException as e:
        status = getattr(getattr(e, "response", None), "status_code", None)
        if status in (404, 410):
            remove_subscription(supabase, row.get("endpoint"))
        else:
            print(f"[push] send error ({status}): {e}")
        return False
    except Exception as e:
        print(f"[push] send error: {e}")
        return False


def _broadcast(supabase, rows: list, payload: dict) -> int:
    sent = 0
    for row in rows or []:
        if _send_one(supabase, row, payload):
            sent += 1
    return sent


def send_to_all(supabase, payload: dict) -> int:
    """Notif à tous les abonnés (ex: nouveauté)."""
    if not (is_configured() and supabase):
        return 0
    try:
        rows = supabase.table("push_subscriptions").select("*").execute().data or []
    except Exception as e:
        print(f"[push] list error: {e}")
        return 0
    return _broadcast(supabase, rows, payload)


def send_to_admins(supabase, payload: dict) -> int:
    """Alerte réservée aux abonnements admin (te prévenir toi)."""
    if not (is_configured() and supabase):
        return 0
    try:
        rows = supabase.table("push_subscriptions").select("*").eq("is_admin", True).execute().data or []
    except Exception as e:
        print(f"[push] admin list error: {e}")
        return 0
    return _broadcast(supabase, rows, payload)


def send_to_email(supabase, email: str, payload: dict) -> int:
    """Notif à tous les appareils d'un utilisateur donné."""
    if not (is_configured() and supabase and email):
        return 0
    try:
        rows = supabase.table("push_subscriptions").select("*").eq("email", email).execute().data or []
    except Exception as e:
        print(f"[push] email list error: {e}")
        return 0
    return _broadcast(supabase, rows, payload)
