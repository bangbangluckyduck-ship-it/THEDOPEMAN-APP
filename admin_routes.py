from __future__ import annotations

"""
Routes admin — accessibles uniquement à l'email ADMIN_EMAIL.
"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from auth import (
    get_user_from_request, is_admin,
    set_user_tier, _user_tiers, _monthly_usage, _daily_usage,
    TIER_CONFIG, usage_info,
)

router = APIRouter(prefix="/admin")


def _require_admin(request: Request) -> dict:
    user = get_user_from_request(request)
    if not is_admin(user):
        raise HTTPException(status_code=403, detail="Accès admin requis.")
    return user


# ── GET /admin/users ─────────────────────────────────────────
@router.get("/users")
async def list_users(request: Request):
    _require_admin(request)
    users = []

    # Try Supabase first, fallback to in-memory
    try:
        from supabase_client import get_all_users, SUPABASE_ENABLED
        if SUPABASE_ENABLED:
            supabase_users = get_all_users()
            for user_data in supabase_users:
                email = user_data["email"]
                tier = user_data.get("tier", "free")
                cfg = TIER_CONFIG.get(tier, TIER_CONFIG["free"])
                users.append({
                    "email": email,
                    "tier": tier,
                    "label": cfg["label"],
                    "expiry": user_data.get("expiry"),
                    "customer_id": None,  # Not stored in simple query
                })
            return {"ok": True, "count": len(users), "users": users}
    except Exception as e:
        print(f"Supabase error: {e}")
        pass

    # Fallback to in-memory (for backward compatibility)
    all_emails = set(_user_tiers.keys()) | set(_monthly_usage.keys()) | set(_daily_usage.keys())
    for email in sorted(all_emails):
        tier_data = _user_tiers.get(email, {})
        tier = tier_data.get("tier", "free")
        cfg  = TIER_CONFIG.get(tier, TIER_CONFIG["free"])
        users.append({
            "email":       email,
            "tier":        tier,
            "label":       cfg["label"],
            "customer_id": tier_data.get("customer_id"),
        })
    return {"ok": True, "count": len(users), "users": users}


# ── GET /admin/usage ─────────────────────────────────────────
# Usage réel des comptes : qui s'inscrit, et qui se sert vraiment de l'outil.
# LECTURE SEULE — cette vue n'écrit rien et ne modifie aucun compte.
#
# SOURCE DE VÉRITÉ : la table `analysis_jobs`, qui porte UNE LIGNE PAR ANALYSE
# (`user_email` + `created_at`), aussi bien pour les analyses asynchrones que
# pour les synchrones (main.py::_persist_sync_analysis). Les compteurs
# `analysis_quota_periods` / `monthly_usage` que lit /admin/stats sont, eux, des
# agrégats par période de facturation : ils donnent un total, jamais une date de
# dernière analyse ni un nombre de jours réellement actifs.
#
# TROIS LIMITES À GARDER EN TÊTE EN LISANT LE TABLEAU :
#  1. L'historisation démarre au 22/06/2026 (mise en service de la table). Un
#     compte antérieur affiche moins d'analyses qu'il n'en a réellement lancées.
#  2. Une analyse SYNCHRONE resservie depuis le cache n'est pas écrite
#     (_persist_sync_analysis ignore les résultats `from_cache`), alors que son
#     équivalent asynchrone l'est. Les totaux sont donc un plancher.
#  3. Les écritures sont best-effort : une panne Supabase perd la ligne sans
#     interrompre l'analyse.
# Ces trois points sont rappelés à l'écran, pour qu'un chiffre bas ne soit
# jamais lu comme « ce compte n'a rien fait » alors qu'il peut être incomplet.

_USAGE_PAGE_SIZE = 1000       # plafond de lignes par réponse PostgREST
_USAGE_MAX_ROWS  = 200_000    # garde-fou anti-boucle
_USAGE_DEPUIS    = "2026-06-22"   # 1re mise en service d'`analysis_jobs`

try:
    from zoneinfo import ZoneInfo
    _USAGE_TZ = ZoneInfo("Europe/Paris")
except Exception:             # base tzdata absente du conteneur
    _USAGE_TZ = timezone.utc


def _usage_parse_dt(value) -> Optional[datetime]:
    """Date Supabase → datetime aware. UTC par défaut si le fuseau est absent."""
    if not value:
        return None
    try:
        d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def _usage_fetch_all(supabase, table: str, columns: str) -> list[dict]:
    """Rapatrie TOUTES les lignes d'une table, par pages de 1000.

    Sans pagination, PostgREST tronque à 1000 lignes *sans erreur* : passé ce
    seuil, l'écran afficherait des totaux faux en silence — le pire des cas pour
    un tableau de pilotage. L'ordre sur `created_at` rend la pagination stable.
    """
    rows: list[dict] = []
    start = 0
    while start < _USAGE_MAX_ROWS:
        batch = (supabase.table(table).select(columns)
                 .order("created_at", desc=False)
                 .range(start, start + _USAGE_PAGE_SIZE - 1)
                 .execute()).data or []
        rows.extend(batch)
        if len(batch) < _USAGE_PAGE_SIZE:
            break
        start += _USAGE_PAGE_SIZE
    return rows


@router.get("/usage")
async def admin_usage(request: Request):
    """Un compte par ligne : inscription, statut, volume et régularité d'usage."""
    _require_admin(request)

    try:
        from supabase_client import supabase_service as supabase, SUPABASE_ENABLED
    except Exception:
        supabase, SUPABASE_ENABLED = None, False
    if not (SUPABASE_ENABLED and supabase):
        raise HTTPException(status_code=503, detail="Base de données indisponible.")

    # Mêmes exclusions que /admin/stats (bots @tts-test.com, comptes internes) :
    # deux écrans qui compteraient des populations différentes ne seraient pas
    # comparables, et l'écart passerait pour un bug.
    try:
        from main import _STATS_EXCLUDED_DOMAINS, _STATS_EXCLUDED_EMAILS
    except Exception:
        _STATS_EXCLUDED_DOMAINS, _STATS_EXCLUDED_EMAILS = [], []

    def _interne(email: str) -> bool:
        e = (email or "").lower()
        return (any(e.endswith("@" + d) for d in _STATS_EXCLUDED_DOMAINS)
                or e in _STATS_EXCLUDED_EMAILS)

    try:
        users = _usage_fetch_all(
            supabase, "users", "id,email,created_at,tier,trial_ends_at")
        jobs = _usage_fetch_all(
            supabase, "analysis_jobs", "user_email,created_at,status")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Lecture Supabase échouée : {e}")

    # ── Agrégation des analyses par compte ──────────────────────────────
    agg: dict[str, dict] = {}
    for j in jobs:
        email = (j.get("user_email") or "").lower().strip()
        if not email:
            continue
        d = _usage_parse_dt(j.get("created_at"))
        a = agg.setdefault(email, {"total": 0, "echecs": 0,
                                   "jours": set(), "derniere": None})
        a["total"] += 1
        if (j.get("status") or "") == "error":
            a["echecs"] += 1
        if d:
            # Jour civil français : une analyse lancée à 23 h 30 UTC appartient
            # au lendemain à Paris. Compter les jours en UTC scinderait une même
            # soirée d'usage en deux, et gonflerait la régularité apparente.
            a["jours"].add(d.astimezone(_USAGE_TZ).date().isoformat())
            if a["derniere"] is None or d > a["derniere"]:
                a["derniere"] = d

    # « Abonné » doit vouloir dire ici exactement ce qu'il veut dire dans le
    # moteur de quota : sinon l'écran annoncerait « essai expiré » à quelqu'un
    # que l'application laisse analyser (ou l'inverse).
    try:
        from analysis_quota import _SUBSCRIBED_TIERS, _UNLIMITED_TIERS
    except Exception:
        _SUBSCRIBED_TIERS = {"pro", "gold", "agency", "beta"}
        _UNLIMITED_TIERS = {"admin"}

    now = datetime.now(timezone.utc)
    comptes: list[dict] = []
    connus: set[str] = set()

    for u in users:
        email = (u.get("email") or "").lower().strip()
        if not email or _interne(email):
            continue
        connus.add(email)

        tier = (u.get("tier") or "free").lower()
        fin_essai = _usage_parse_dt(u.get("trial_ends_at"))
        if tier in _UNLIMITED_TIERS:
            statut = "admin"
        elif tier in _SUBSCRIBED_TIERS:
            statut = "abonne"
        elif fin_essai and now < fin_essai:
            statut = "essai"
        else:
            statut = "essai_expire"

        a = agg.get(email) or {}
        inscrit = _usage_parse_dt(u.get("created_at"))
        derniere = a.get("derniere")
        comptes.append({
            "email":            email,
            "user_id":          u.get("id"),
            "inscrit_le":       inscrit.isoformat() if inscrit else None,
            "statut":           statut,
            "tier":             tier,
            "essai_fin":        fin_essai.isoformat() if fin_essai else None,
            "analyses":         a.get("total", 0),
            "analyses_echec":   a.get("echecs", 0),
            "jours_actifs":     len(a.get("jours") or ()),
            "derniere_analyse": derniere.isoformat() if derniere else None,
        })

    # Ordre par défaut : les comptes qui se servent le plus de l'outil en tête.
    # Le tri interactif demandé (analyses / dernière analyse) se fait à l'écran,
    # sur ces mêmes lignes déjà chargées — pas de second aller-retour serveur.
    comptes.sort(key=lambda c: (c["analyses"], c["derniere_analyse"] or ""),
                 reverse=True)

    # Analyses rattachées à aucun compte listé (compte supprimé depuis, ou
    # e-mail interne exclu ci-dessus) : signalées pour expliquer un écart avec
    # le total affiché par /admin/stats plutôt que de le laisser inexpliqué.
    hors_comptes = sum(v["total"] for k, v in agg.items() if k not in connus)

    return {
        "ok": True,
        "count": len(comptes),
        "genere_le": now.isoformat(),
        "historisation_depuis": _USAGE_DEPUIS,
        "analyses_hors_comptes": hors_comptes,
        "comptes": comptes,
    }


# ── POST /admin/set-tier ─────────────────────────────────────
class SetTierBody(BaseModel):
    email: str
    tier:  str
    expiry: Optional[str] = None  # ISO date YYYY-MM-DD ou None pour pas d'expiration

@router.post("/set-tier")
async def set_tier(body: SetTierBody, request: Request):
    _require_admin(request)
    if body.tier not in TIER_CONFIG:
        raise HTTPException(status_code=400, detail=f"Tier invalide. Choix : {list(TIER_CONFIG.keys())}")
    set_user_tier(body.email.lower().strip(), body.tier, expiry=body.expiry)
    msg = f"{body.email} → {body.tier.upper()}"
    if body.expiry:
        msg += f" (expire le {body.expiry})"
    return {"ok": True, "email": body.email, "tier": body.tier, "expiry": body.expiry, "message": msg}


# ── POST /admin/grant-beta ───────────────────────────────────
class GrantBetaBody(BaseModel):
    email: str

@router.post("/grant-beta")
async def grant_beta(body: GrantBetaBody, request: Request):
    _require_admin(request)
    set_user_tier(body.email.lower().strip(), "beta")
    return {"ok": True, "email": body.email, "tier": "beta", "message": "Accès beta activé ✅"}


# ── DELETE /admin/revoke ─────────────────────────────────────
class RevokeBody(BaseModel):
    email: str

@router.post("/revoke")
async def revoke(body: RevokeBody, request: Request):
    _require_admin(request)
    set_user_tier(body.email.lower().strip(), "free")
    return {"ok": True, "email": body.email, "tier": "free", "message": "Accès révoqué → free"}


# ── POST /admin/reset-user-password ──────────────────────────
class ResetPasswordBody(BaseModel):
    email: str
    reset_type: str  # 'magic_link' or 'temporary_password'

@router.post("/reset-user-password")
async def reset_user_password(body: ResetPasswordBody, request: Request):
    """Admin reset user password with 2 options."""
    import bcrypt
    from supabase_client import supabase_service as supabase
    from password_reset import (
        generate_reset_token,
        generate_temporary_password,
        hash_token,
        create_password_reset_token,
    )
    from email_service import email_service

    _require_admin(request)

    email = body.email.lower().strip()
    reset_type = body.reset_type.lower()

    if reset_type not in ["magic_link", "temporary_password"]:
        raise HTTPException(status_code=400, detail="Type invalide: magic_link ou temporary_password")

    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")

    try:
        # Verify user exists
        user_exists = supabase.table("users").select("id").eq("email", email).execute()
        if not user_exists.data:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        if reset_type == "magic_link":
            # Token de reset RÉEL (celui renvoyé) → lien vers la page /reset-password.
            success, token_plaintext, _ = create_password_reset_token(email, "magic_link")
            if not success:
                raise HTTPException(status_code=500, detail="Erreur création token")

            import os
            from urllib.parse import quote as _q
            app_url = os.getenv("APP_PUBLIC_URL", "https://qeerah.com").rstrip("/")
            reset_link = f"{app_url}/reset-password?token={token_plaintext}&email={_q(email)}"
            email_sent = await email_service.send_magic_link_email(email, reset_link)

            if not email_sent:
                raise HTTPException(status_code=500, detail="Erreur envoi email")

            return {
                "ok": True,
                "email": email,
                "method": "magic_link",
                "message": "Lien de réinitialisation envoyé par email à l'utilisateur"
            }

        else:  # temporary_password
            # Generate temporary password
            temp_password = generate_temporary_password()
            password_hash = bcrypt.hashpw(temp_password.encode(), bcrypt.gensalt()).decode()

            # Admin = autorité → on APPLIQUE directement le MDP temporaire (utilisable de suite).
            supabase.table("users").update({"password": password_hash}).eq("email", email).execute()

            # Send email with temporary password
            email_sent = await email_service.send_temporary_password_email(email, temp_password)

            if not email_sent:
                raise HTTPException(status_code=500, detail="Erreur envoi email")

            return {
                "ok": True,
                "email": email,
                "method": "temporary_password",
                "temp_password": temp_password,  # Return to admin to communicate if needed
                "message": "Mot de passe temporaire généré et envoyé par email"
            }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Admin reset password error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ════════════════════════════════════════════════════════════════════
# FEATURE 1 — Banque de Hooks : CRUD admin
# ════════════════════════════════════════════════════════════════════
from typing import List


class HookBody(BaseModel):
    texte: str
    categorie: str
    url_video: Optional[str] = None
    type_acces: str = "plan_minimum"          # tous | plan_minimum | plans_specifiques
    plan_min: Optional[str] = "pro"
    plans_autorises: Optional[List[str]] = None


def _hook_record(body: HookBody) -> dict:
    return {
        "texte": (body.texte or "").strip(),
        "categorie": (body.categorie or "autre").strip().lower(),
        "url_video": (body.url_video or None) or None,
        "type_acces": (body.type_acces or "plan_minimum").strip().lower(),
        "plan_min": (body.plan_min or "pro").strip().lower(),
        "plans_autorises": [str(p).lower() for p in (body.plans_autorises or [])],
    }


@router.get("/hooks")
async def admin_list_hooks(request: Request, category: Optional[str] = None):
    _require_admin(request)
    from supabase_client import supabase_service as supabase
    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")
    q = supabase.table("hooks").select("*").order("created_at", desc=True)
    if category:
        q = q.eq("categorie", category.lower())
    rows = q.execute().data or []
    return {"ok": True, "count": len(rows), "hooks": rows}


@router.post("/hooks")
async def admin_create_hook(body: HookBody, request: Request):
    _require_admin(request)
    from supabase_client import supabase_service as supabase
    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")
    if not body.texte.strip():
        raise HTTPException(status_code=422, detail="Le texte du hook est obligatoire.")
    try:
        res = supabase.table("hooks").insert(_hook_record(body)).execute()
    except Exception as e:
        print(f"[admin hooks insert] {e}")
        raise HTTPException(status_code=500, detail=f"insert hooks: {e}")
    return {"ok": True, "hook": (res.data or [None])[0]}


@router.put("/hooks/{hook_id}")
async def admin_update_hook(hook_id: int, body: HookBody, request: Request):
    _require_admin(request)
    from supabase_client import supabase_service as supabase
    from datetime import datetime, timezone
    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")
    rec = _hook_record(body)
    rec["updated_at"] = datetime.now(timezone.utc).isoformat()
    supabase.table("hooks").update(rec).eq("id", hook_id).execute()
    return {"ok": True, "id": hook_id}


@router.delete("/hooks/{hook_id}")
async def admin_delete_hook(hook_id: int, request: Request):
    _require_admin(request)
    from supabase_client import supabase_service as supabase
    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")
    supabase.table("hooks").delete().eq("id", hook_id).execute()
    return {"ok": True, "id": hook_id}


# ════════════════════════════════════════════════════════════════════
# FEATURE 2 — Témoignages : CRUD admin (validation/publication)
# ════════════════════════════════════════════════════════════════════
class TemoignageBody(BaseModel):
    nom: str
    texte: str
    lien_tiktok: Optional[str] = None
    photo_url: Optional[str] = None
    metrique: Optional[str] = None
    note: Optional[int] = None
    statut: str = "en_attente"          # en_attente | publie | masque
    mis_en_avant: bool = False


@router.get("/temoignages")
async def admin_list_temoignages(request: Request, statut: Optional[str] = None):
    _require_admin(request)
    from supabase_client import supabase_service as supabase
    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")
    q = supabase.table("temoignages").select("*").order("date_soumission", desc=True)
    if statut:
        q = q.eq("statut", statut)
    return {"ok": True, "temoignages": q.execute().data or []}


@router.post("/temoignages")
async def admin_create_temoignage(body: TemoignageBody, request: Request):
    _require_admin(request)
    from supabase_client import supabase_service as supabase
    from datetime import datetime, timezone
    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")
    rec = body.model_dump()
    if rec.get("statut") == "publie":
        rec["date_publication"] = datetime.now(timezone.utc).isoformat()
    try:
        res = supabase.table("temoignages").insert(rec).execute()
    except Exception as e:
        print(f"[admin temoignages insert] {e}")
        raise HTTPException(status_code=500, detail=f"insert temoignages: {e}")
    return {"ok": True, "temoignage": (res.data or [None])[0]}


@router.put("/temoignages/{tid}")
async def admin_update_temoignage(tid: int, body: TemoignageBody, request: Request):
    _require_admin(request)
    from supabase_client import supabase_service as supabase
    from datetime import datetime, timezone
    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")
    rec = body.model_dump()
    # date_publication posée au passage en "publie" si pas déjà fixée
    if rec.get("statut") == "publie":
        existing = supabase.table("temoignages").select("date_publication").eq("id", tid).execute()
        if not (existing.data and existing.data[0].get("date_publication")):
            rec["date_publication"] = datetime.now(timezone.utc).isoformat()
    supabase.table("temoignages").update(rec).eq("id", tid).execute()
    return {"ok": True, "id": tid}


@router.delete("/temoignages/{tid}")
async def admin_delete_temoignage(tid: int, request: Request):
    _require_admin(request)
    from supabase_client import supabase_service as supabase
    if not supabase:
        raise HTTPException(status_code=500, detail="BD non disponible")
    supabase.table("temoignages").delete().eq("id", tid).execute()
    return {"ok": True, "id": tid}


# ════════════════════════════════════════════════════════════════════
# NOTIFICATIONS — broadcast push (nouveautés / relance manuelle)
# ════════════════════════════════════════════════════════════════════
class PushBroadcastBody(BaseModel):
    title: str
    body: str
    url: Optional[str] = "/app"


@router.post("/push/broadcast")
async def admin_push_broadcast(body: PushBroadcastBody, request: Request):
    _require_admin(request)
    import push
    from supabase_client import supabase_service as supabase
    if not push.is_configured():
        raise HTTPException(status_code=503, detail="Clés VAPID non configurées (variables d'env Render).")
    if not (body.title.strip() and body.body.strip()):
        raise HTTPException(status_code=422, detail="Titre et message requis.")
    sent = push.send_to_all(supabase, {"title": body.title.strip(), "body": body.body.strip(), "url": body.url or "/app"})
    return {"ok": True, "sent": sent}


@router.get("/push/stats")
async def admin_push_stats(request: Request):
    _require_admin(request)
    import push
    from supabase_client import supabase_service as supabase
    try:
        total = supabase.table("push_subscriptions").select("id", count="exact").execute().count or 0
    except Exception:
        total = 0
    return {"ok": True, "configured": push.is_configured(), "subscribers": total}


# ════════════════════════════════════════════════════════════════════
# RECHERCHE GMV — outil admin minimal (pas de cache, pas de quota).
# Version simplifiée de /api/recherche/profile côté user, juste pour une
# vérification ponctuelle du GMV d'un handle.
# ════════════════════════════════════════════════════════════════════
@router.get("/recherche-gmv")
async def admin_recherche_gmv(request: Request, handle: str):
    _require_admin(request)
    import market_creators
    handle_clean = (handle or "").lstrip("@").strip()
    if not handle_clean:
        raise HTTPException(status_code=422, detail="Handle requis.")
    try:
        result = await market_creators.get_creator_gmv_only(handle_clean)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Profil introuvable.")
    return {"ok": True, **result}


# ── PROGRAMME D'AFFILIATION ──────────────────────────────────
class AffiliateEmailBody(BaseModel):
    email: str

class AffiliateStatusBody(BaseModel):
    email: str
    status: str          # pending | approved | rejected | disabled


@router.get("/affiliates")
async def admin_list_affiliates(request: Request):
    _require_admin(request)
    import affiliates as aff
    from supabase_client import supabase_service
    return {"ok": True, "affiliates": aff.list_all(supabase_service)}


@router.post("/affiliates")
async def admin_create_affiliate(body: AffiliateEmailBody, request: Request):
    """Crée un affilié déjà approuvé (avec code) directement depuis l'admin."""
    _require_admin(request)
    import affiliates as aff
    from supabase_client import supabase_service
    res = aff.create_approved(supabase_service, body.email)
    if not res.get("ok"):
        raise HTTPException(status_code=400, detail=res.get("error", "Échec création."))
    return {"ok": True, "affiliate": res.get("affiliate")}


@router.post("/affiliates/status")
async def admin_set_affiliate_status(body: AffiliateStatusBody, request: Request):
    """Approuve (génère le code), rejette, désactive ou remet en attente un affilié."""
    _require_admin(request)
    import affiliates as aff
    from supabase_client import supabase_service
    res = aff.set_status(supabase_service, body.email, body.status)
    if not res.get("ok"):
        code = res.get("error", "")
        status = 404 if code == "not_found" else 400
        raise HTTPException(status_code=status, detail=code or "Échec.")
    return {"ok": True, "affiliate": res.get("affiliate")}


# ── BANDEAU PROMOTIONNEL ─────────────────────────────────────
class PromoBannerBody(BaseModel):
    active:    bool = False
    message:   Optional[str] = ""
    code:      Optional[str] = ""
    cta_label: Optional[str] = "En profiter"
    cta_url:   Optional[str] = "/pricing"
    ends_at:   Optional[str] = None      # ISO 8601, ex. "2026-08-15T23:59:00+02:00"


@router.get("/promo")
async def admin_get_promo(request: Request):
    """Paramétrage actuel du bandeau promotionnel."""
    _require_admin(request)
    import promo_banner
    return {"ok": True, "promo": promo_banner.get_admin()}


@router.post("/promo")
async def admin_save_promo(body: PromoBannerBody, request: Request):
    """Active, modifie ou désactive le bandeau promotionnel."""
    _require_admin(request)
    import promo_banner
    try:
        promo = promo_banner.save(body.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enregistrement impossible : {e}")
    return {"ok": True, "promo": promo}
