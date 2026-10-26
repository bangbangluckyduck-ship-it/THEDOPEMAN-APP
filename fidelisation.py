"""Garder les abonnés — paiement en retard, pause plutôt que résiliation, raisons.

## Paiement échoué
Stripe relance automatiquement (réglage « Smart Retries » du tableau de bord).
Pendant ces relances, l'abonné GARDE son accès : le tier expirait jusqu'ici à la
fin de la période payée (users.tier_expiry), si bien qu'un échec de carte coupait
l'accès dès le lendemain, alors que Stripe n'avait pas fini de réessayer. On
repousse donc l'échéance jusqu'à la prochaine tentative ; c'est
`customer.subscription.deleted`, à la fin des relances, qui ferme l'accès
(auth.revoke_by_customer, inchangé). Un bandeau dans l'app invite à mettre la
carte à jour (portail Stripe).

## Pause d'un mois
Stripe `pause_collection` (behavior « void ») avec une date de reprise. La
période déjà payée reste due jusqu'au bout ; ensuite aucune facture n'est émise,
l'échéance du tier passe et l'accès se ferme de lui-même ; à la date de reprise,
Stripe recommence à facturer et `invoice.paid` rouvre l'accès. L'app affiche
« en pause jusqu'au … » avec « Reprendre maintenant ».

## Résiliation
Deux clics au maximum : « Résilier » ouvre une fenêtre (pause / continuer /
annuler) ; « Continuer la résiliation » ouvre le portail Stripe. La question sur
la raison est facultative, dans la même fenêtre — jamais une étape de plus.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import stripe

RAISONS = ("trop_cher", "pas_assez_utilise", "il_manque", "autre")
DUREE_PAUSE = timedelta(days=30)


def _maintenant() -> datetime:
    return datetime.now(timezone.utc)


def _date(ts) -> datetime | None:
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc) if ts else None
    except (TypeError, ValueError):
        return None


def _maj(supabase, email: str, champs: dict) -> bool:
    """Mise à jour best-effort : colonnes absentes (migration) → False, sans lever."""
    if not supabase or not email:
        return False
    try:
        supabase.table("users").update(champs).eq("email", email.lower()).execute()
        return True
    except Exception as e:
        print(f"[fidelisation] mise à jour {sorted(champs)} pour {email} : {e}")
        return False


def _email_du_client(obj: dict) -> str:
    email = (obj.get("customer_email") or "").strip().lower()
    if not email and obj.get("customer"):
        try:
            email = (stripe.Customer.retrieve(obj["customer"]).get("email") or "").strip().lower()
        except Exception:
            email = ""
    return email


# ── Webhooks ───────────────────────────────────────────────────────────────
def paiement_echoue(supabase, invoice: dict) -> str:
    """invoice.payment_failed : bandeau + accès gardé jusqu'à la prochaine relance."""
    email = _email_du_client(invoice)
    if not email:
        return ""
    champs = {"paiement_en_retard_depuis": _maintenant().isoformat()}
    prochaine = _date(invoice.get("next_payment_attempt"))
    if prochaine:
        # Un jour de marge après la tentative : le webhook de réussite a le temps
        # d'arriver avant que l'échéance ne coupe l'accès.
        champs_expiry = {"tier_expiry": (prochaine + timedelta(days=1)).date().isoformat()}
        _maj(supabase, email, champs_expiry)
    # Ne réécrit pas la date du premier échec si elle existe déjà.
    try:
        r = supabase.table("users").select("paiement_en_retard_depuis").eq("email", email).limit(1).execute()
        if (r.data or [{}])[0].get("paiement_en_retard_depuis"):
            return email
    except Exception:
        pass
    _maj(supabase, email, champs)
    return email


def paiement_regle(supabase, email: str) -> None:
    """invoice.paid : plus de retard."""
    _maj(supabase, email, {"paiement_en_retard_depuis": None})


def abonnement_modifie(supabase, sub: dict) -> str:
    """customer.subscription.updated : statut de paiement et pause, quelle que soit
    leur origine (l'app, le portail Stripe, le tableau de bord)."""
    email = _email_du_client(sub)
    if not email:
        return ""
    statut = sub.get("status")
    if statut in ("past_due", "unpaid"):
        pass   # le bandeau est posé par invoice.payment_failed (date du 1er échec)
    elif statut == "active":
        _maj(supabase, email, {"paiement_en_retard_depuis": None})
    pause = sub.get("pause_collection") or {}
    fin = _date(pause.get("resumes_at")) if pause else None
    _maj(supabase, email, {"pause_fin": fin.isoformat() if fin else None})
    return email


# ── État pour l'app ────────────────────────────────────────────────────────
def etat(supabase, email: str) -> dict:
    """{paiement_en_retard, pause_fin, hebdo} — valeurs neutres si indisponible."""
    out = {"paiement_en_retard": False, "pause_fin": None, "hebdo": True}
    if not supabase or not email:
        return out
    try:
        r = (supabase.table("users").select("paiement_en_retard_depuis,pause_fin,hebdo_opt_out")
             .eq("email", email.lower()).limit(1).execute())
        u = (r.data or [{}])[0]
    except Exception:
        return out
    fin = u.get("pause_fin")
    try:
        fin_dt = datetime.fromisoformat(str(fin).replace("Z", "+00:00")) if fin else None
    except ValueError:
        fin_dt = None
    out["paiement_en_retard"] = bool(u.get("paiement_en_retard_depuis"))
    out["pause_fin"] = fin_dt.isoformat() if fin_dt and fin_dt > _maintenant() else None
    out["hebdo"] = not u.get("hebdo_opt_out")
    return out


# ── Actions de l'abonné ────────────────────────────────────────────────────
def _abonnement(supabase, email: str) -> str | None:
    """Abonnement Stripe du compte. Repli sur Stripe lui-même : quand l'échéance
    passe pendant une pause, supabase_client.get_user_tier repasse le compte en
    « free » et efface subscription_id — la reprise doit pourtant le retrouver."""
    try:
        r = supabase.table("users").select("subscription_id").eq("email", email.lower()).limit(1).execute()
        sub_id = (r.data or [{}])[0].get("subscription_id")
        if sub_id:
            return sub_id
    except Exception:
        pass
    try:
        for client in stripe.Customer.list(email=email.lower(), limit=3).get("data", []):
            for sub in stripe.Subscription.list(customer=client["id"], status="all", limit=5).get("data", []):
                if sub.get("status") in ("active", "trialing", "past_due") or sub.get("pause_collection"):
                    return sub["id"]
    except Exception as e:
        print(f"[fidelisation] recherche d'abonnement Stripe ({email}) : {e}")
    return None


def mettre_en_pause(supabase, email: str) -> dict:
    """Pause de facturation d'un mois, à partir de la fin de la période payée."""
    sub_id = _abonnement(supabase, email)
    if not sub_id or not stripe.api_key:
        return {"ok": False, "detail": "Aucun abonnement actif trouvé."}
    try:
        sub = stripe.Subscription.retrieve(sub_id)
        debut = _date(sub.get("current_period_end")) or _maintenant()
        reprise = debut + DUREE_PAUSE
        stripe.Subscription.modify(sub_id, pause_collection={
            "behavior": "void", "resumes_at": int(reprise.timestamp())})
    except stripe.error.StripeError as e:
        return {"ok": False, "detail": str(e.user_message or e)}
    _maj(supabase, email, {"pause_fin": reprise.isoformat()})
    return {"ok": True, "pause_fin": reprise.isoformat(), "acces_jusqu_au": debut.isoformat()}


def reprendre(supabase, email: str) -> dict:
    sub_id = _abonnement(supabase, email)
    if not sub_id or not stripe.api_key:
        return {"ok": False, "detail": "Aucun abonnement trouvé."}
    try:
        stripe.Subscription.modify(sub_id, pause_collection="")
    except stripe.error.StripeError as e:
        return {"ok": False, "detail": str(e.user_message or e)}
    _maj(supabase, email, {"pause_fin": None})
    return {"ok": True}


def enregistrer_raison(supabase, email: str, raison: str, detail: str | None = None) -> bool:
    if raison not in RAISONS or not supabase:
        return False
    try:
        supabase.table("cancel_feedback").insert({
            "email": email.lower(), "raison": raison,
            "detail": (detail or "").strip()[:500] or None,
        }).execute()
        return True
    except Exception as e:
        print(f"[fidelisation] raison non enregistrée ({email}) : {e}")
        return False


def preference_hebdo(supabase, email: str, actif: bool) -> bool:
    return _maj(supabase, email, {"hebdo_opt_out": not actif})
