"""
🤝 Programme d'affiliation — logique métier.

Parcours :
  1. Un user connecté candidate  → apply()  → statut 'pending'.
  2. L'admin approuve/crée        → approve()/create() → statut 'approved' + code.
  3. Le lien qeerah.com/?ref=CODE attribue les inscriptions (attribute_signup).
  4. L'affilié voit son lien + son nombre d'inscrits (get_for_user).

Toutes les fonctions prennent le client supabase (service_role) en paramètre —
la table `affiliates` est verrouillée en RLS (aucun accès via la clé anon).
"""
from __future__ import annotations

import secrets
import string
from datetime import datetime, timezone
from typing import Optional

STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"
STATUS_DISABLED = "disabled"

_ALPHABET = string.ascii_lowercase + string.digits  # code lisible, sans ambiguïté maj/min
_CODE_LEN = 8


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _gen_code(supabase) -> str:
    """Code court unique (retry en cas de collision, très improbable)."""
    for _ in range(6):
        code = "".join(secrets.choice(_ALPHABET) for _ in range(_CODE_LEN))
        try:
            r = supabase.table("affiliates").select("id").eq("code", code).execute()
            if not r.data:
                return code
        except Exception:
            return code  # best-effort : on renvoie le code, l'unicité DB reste garante
    return code


def get_by_email(supabase, email: str) -> Optional[dict]:
    if not supabase or not email:
        return None
    try:
        r = supabase.table("affiliates").select("*").eq("email", email.lower().strip()).execute()
        return r.data[0] if r.data else None
    except Exception:
        return None


def get_by_code(supabase, code: str) -> Optional[dict]:
    if not supabase or not code:
        return None
    try:
        r = supabase.table("affiliates").select("*").eq("code", code).execute()
        return r.data[0] if r.data else None
    except Exception:
        return None


def count_signups(supabase, code: str) -> int:
    """Nombre d'inscriptions attribuées à ce code (users.referred_by = code)."""
    if not supabase or not code:
        return 0
    try:
        r = supabase.table("users").select("email", count="exact").eq("referred_by", code).execute()
        if getattr(r, "count", None) is not None:
            return int(r.count)
        return len(r.data or [])
    except Exception:
        return 0


def apply(supabase, email: str) -> dict:
    """Candidature d'un user connecté. Idempotent : renvoie la ligne existante
    si déjà candidat/affilié, sinon crée une demande 'pending'."""
    email = (email or "").lower().strip()
    if not supabase or not email:
        return {"ok": False, "error": "unavailable"}
    existing = get_by_email(supabase, email)
    if existing:
        return {"ok": True, "affiliate": existing, "already": True}
    try:
        r = supabase.table("affiliates").insert({
            "email": email,
            "status": STATUS_PENDING,
            "created_at": _now(),
        }).execute()
        return {"ok": True, "affiliate": (r.data or [{}])[0], "already": False}
    except Exception as e:
        print(f"affiliates.apply error: {e}")
        return {"ok": False, "error": "insert_failed"}


def set_status(supabase, email: str, status: str) -> dict:
    """Change le statut. Passer à 'approved' génère un code s'il n'y en a pas."""
    email = (email or "").lower().strip()
    if status not in (STATUS_PENDING, STATUS_APPROVED, STATUS_REJECTED, STATUS_DISABLED):
        return {"ok": False, "error": "bad_status"}
    aff = get_by_email(supabase, email)
    if not aff:
        return {"ok": False, "error": "not_found"}
    data: dict = {"status": status}
    if status == STATUS_APPROVED:
        if not aff.get("code"):
            data["code"] = _gen_code(supabase)
        if not aff.get("approved_at"):
            data["approved_at"] = _now()
    try:
        supabase.table("affiliates").update(data).eq("email", email).execute()
        return {"ok": True, "affiliate": {**aff, **data}}
    except Exception as e:
        print(f"affiliates.set_status error: {e}")
        return {"ok": False, "error": "update_failed"}


def create_approved(supabase, email: str) -> dict:
    """Admin crée un affilié directement (déjà approuvé + code)."""
    email = (email or "").lower().strip()
    if not supabase or not email or "@" not in email:
        return {"ok": False, "error": "bad_email"}
    if get_by_email(supabase, email):
        return set_status(supabase, email, STATUS_APPROVED)
    try:
        supabase.table("affiliates").insert({
            "email": email,
            "status": STATUS_APPROVED,
            "code": _gen_code(supabase),
            "created_at": _now(),
            "approved_at": _now(),
        }).execute()
        return {"ok": True, "affiliate": get_by_email(supabase, email)}
    except Exception as e:
        print(f"affiliates.create_approved error: {e}")
        return {"ok": False, "error": "insert_failed"}


def list_all(supabase) -> list[dict]:
    """Tous les affiliés + leur nombre d'inscrits (pour l'admin)."""
    if not supabase:
        return []
    try:
        r = supabase.table("affiliates").select("*").order("created_at", desc=True).execute()
        rows = r.data or []
    except Exception:
        return []
    for row in rows:
        row["signups"] = count_signups(supabase, row.get("code")) if row.get("code") else 0
    return rows


def attribute_signup(supabase, new_email: str, ref_code: str) -> bool:
    """À l'inscription : rattache le nouveau user à un code d'affilié APPROUVÉ.
    No-op si code inconnu/non approuvé ou auto-parrainage. À n'appeler qu'à la
    création du compte (jamais d'écrasement d'une attribution existante)."""
    new_email = (new_email or "").lower().strip()
    ref_code = (ref_code or "").strip()
    if not supabase or not new_email or not ref_code:
        return False
    aff = get_by_code(supabase, ref_code)
    if not aff or aff.get("status") != STATUS_APPROVED:
        return False
    if aff.get("email", "").lower() == new_email:   # pas d'auto-parrainage
        return False
    try:
        supabase.table("users").update({"referred_by": ref_code}).eq("email", new_email).execute()
        return True
    except Exception as e:
        print(f"affiliates.attribute_signup error: {e}")
        return False


def get_for_user(supabase, email: str, base_url: str) -> dict:
    """État d'affiliation pour l'espace client. base_url ex: https://qeerah.com"""
    aff = get_by_email(supabase, email)
    if not aff:
        return {"is_affiliate": False, "status": None}
    code = aff.get("code")
    link = f"{base_url.rstrip('/')}/?ref={code}" if code else None
    return {
        "is_affiliate": True,
        "status": aff.get("status"),
        "code": code,
        "link": link,
        "signups": count_signups(supabase, code) if code else 0,
    }
