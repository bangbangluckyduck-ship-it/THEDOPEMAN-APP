"""
🎟️ Bandeau promotionnel — piloté depuis /dope-admin.

Principe : une échéance réelle (`ends_at`) fait foi. Le bandeau et son décompte
disparaissent d'eux-mêmes une fois la date passée, pour tout le monde en même
temps. Le décompte ne redémarre jamais par visiteur : un faux compte à rebours
serait une pratique commerciale trompeuse (art. L.121-2 du Code de la
consommation), en plus d'être ce que le brief produit interdit.

Le serveur renvoie aussi son propre horodatage (`server_now`) : le front s'en
sert pour corriger un éventuel décalage d'horloge du visiteur, plutôt que de
faire confiance à Date.now() côté client.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from supabase_client import supabase_service as supabase

_ROW_ID = 1


def _parse_dt(s) -> Optional[datetime]:
    if not s:
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _row() -> dict:
    if not supabase:
        return {}
    try:
        r = supabase.table("promo_banner").select("*").eq("id", _ROW_ID).execute()
        return (r.data or [{}])[0]
    except Exception as e:
        print(f"promo_banner._row: {e}")
        return {}


def get_public() -> dict:
    """Ce que voit un visiteur. Renvoie {'active': False} si la promo est
    désactivée, non configurée, ou si son échéance est passée."""
    now = datetime.now(timezone.utc)
    row = _row()

    if not row or not row.get("active"):
        return {"active": False, "server_now": now.isoformat()}

    ends_at = _parse_dt(row.get("ends_at"))
    if ends_at and now >= ends_at:
        # Échéance dépassée : plus rien à afficher. La ligne n'est pas modifiée
        # (l'admin garde son paramétrage pour la prochaine campagne).
        return {"active": False, "server_now": now.isoformat()}

    return {
        "active":     True,
        "message":    row.get("message") or "",
        "code":       row.get("code") or "",
        "cta_label":  row.get("cta_label") or "En profiter",
        "cta_url":    row.get("cta_url") or "/pricing",
        "ends_at":    ends_at.isoformat() if ends_at else None,
        "server_now": now.isoformat(),
    }


def get_admin() -> dict:
    """Paramétrage complet, pour l'écran d'administration."""
    row = _row()
    return {
        "active":    bool(row.get("active")),
        "message":   row.get("message") or "",
        "code":      row.get("code") or "",
        "cta_label": row.get("cta_label") or "En profiter",
        "cta_url":   row.get("cta_url") or "/pricing",
        "ends_at":   row.get("ends_at"),
        "updated_at": row.get("updated_at"),
        "server_now": datetime.now(timezone.utc).isoformat(),
    }


def save(data: dict) -> dict:
    """Enregistre le paramétrage (admin uniquement — le contrôle de rôle est
    fait par la route appelante)."""
    if not supabase:
        raise RuntimeError("Base de données indisponible.")

    ends_at = _parse_dt(data.get("ends_at"))
    payload = {
        "id":         _ROW_ID,
        "active":     bool(data.get("active")),
        "message":    (data.get("message") or "").strip()[:200],
        "code":       (data.get("code") or "").strip()[:60],
        "cta_label":  (data.get("cta_label") or "En profiter").strip()[:40],
        "cta_url":    (data.get("cta_url") or "/pricing").strip()[:200],
        "ends_at":    ends_at.isoformat() if ends_at else None,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    # Garde-fou : activer une promo dont l'échéance est déjà passée n'aurait
    # aucun effet visible et laisserait croire à un bug côté admin.
    if payload["active"] and ends_at and ends_at <= datetime.now(timezone.utc):
        raise ValueError("L'échéance est déjà passée : le bandeau ne s'afficherait pas.")

    supabase.table("promo_banner").upsert(payload, on_conflict="id").execute()
    return get_admin()
