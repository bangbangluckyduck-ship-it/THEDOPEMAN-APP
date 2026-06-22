"""
Routes Stripe — Checkout, Customer Portal, Webhooks.

Variables d'environnement Render à configurer :
  STRIPE_SECRET_KEY              sk_live_...
  STRIPE_PUBLISHABLE_KEY         pk_live_...
  STRIPE_WEBHOOK_SECRET          whsec_...

  PRO — montée progressive (créer 3 prix sur Stripe) :
  STRIPE_PRICE_PRO_999           price_...   (9,99 €/mois  — 31/07 → 19/08)
  STRIPE_PRICE_PRO_999_YEAR      price_...   (99,90 €/an)
  STRIPE_PRICE_PRO_1199          price_...   (11,99 €/mois — 20/08 → 15/09)
  STRIPE_PRICE_PRO_1199_YEAR     price_...   (119,90 €/an)
  STRIPE_PRICE_PRO               price_...   (12,99 €/mois — 16/09+)
  STRIPE_PRICE_PRO_YEAR          price_...   (129,90 €/an)

  GOLD — prix de lancement puis prix normal :
  STRIPE_PRICE_GOLD_LAUNCH       price_...   (79 €/mois   — 16/09 → 14/10)
  STRIPE_PRICE_GOLD_LAUNCH_YEAR  price_...   (790 €/an)
  STRIPE_PRICE_GOLD              price_...   (99 €/mois   — 15/10+)
  STRIPE_PRICE_GOLD_YEAR         price_...   (990 €/an)

  AGENCY :
  STRIPE_PRICE_AGENCY            price_...   (299 €/mois)
  STRIPE_PRICE_AGENCY_YEAR       price_...   (2990 €/an)
"""
from __future__ import annotations
import os
from datetime import date as _date
import stripe
from typing import Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from auth import set_user_tier, get_customer_id, revoke_by_customer

router = APIRouter(tags=["stripe"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

# Dates de transition tarifaire
_PRO_999_END    = _date(2026, 8, 20)   # PRO passe à 11,99 €
_PRO_1199_END   = _date(2026, 9, 16)   # PRO passe à 12,99 €
_GOLD_PROMO_END = _date(2026, 10, 15)  # GOLD passe à 99 €

# Prix PRO progressifs
_PRO_999  = {"month": os.getenv("STRIPE_PRICE_PRO_999", ""),  "year": os.getenv("STRIPE_PRICE_PRO_999_YEAR", "")}
_PRO_1199 = {"month": os.getenv("STRIPE_PRICE_PRO_1199", ""), "year": os.getenv("STRIPE_PRICE_PRO_1199_YEAR", "")}
_PRO      = {"month": os.getenv("STRIPE_PRICE_PRO", ""),      "year": os.getenv("STRIPE_PRICE_PRO_YEAR", "")}

# Prix GOLD lancement puis normal
_GOLD_LAUNCH = {"month": os.getenv("STRIPE_PRICE_GOLD_LAUNCH", ""),      "year": os.getenv("STRIPE_PRICE_GOLD_LAUNCH_YEAR", "")}
_GOLD        = {"month": os.getenv("STRIPE_PRICE_GOLD", ""),              "year": os.getenv("STRIPE_PRICE_GOLD_YEAR", "")}

# AGENCY (prix fixe)
_AGENCY = {"month": os.getenv("STRIPE_PRICE_AGENCY", ""), "year": os.getenv("STRIPE_PRICE_AGENCY_YEAR", "")}


def get_price_id(plan: str, billing: str = "month") -> str:
    """Retourne le price_id Stripe selon le plan, la période et la date du jour."""
    b = "year" if (billing or "month").lower().startswith("year") else "month"
    today = _date.today()

    if plan == "pro":
        if today < _PRO_999_END:
            return _PRO_999[b]
        elif today < _PRO_1199_END:
            return _PRO_1199[b]
        else:
            return _PRO[b]
    elif plan == "gold":
        return _GOLD_LAUNCH[b] if today < _GOLD_PROMO_END else _GOLD[b]
    elif plan == "agency":
        return _AGENCY[b]
    return ""


PLAN_NAMES = {
    "pro":    "PRO — 12,99 €/mois (129,90 €/an)",
    "gold":   "GOLD — 99 €/mois (990 €/an)",
    "agency": "AGENCY — 299 €/mois (2990 €/an)",
}


# ── CHECKOUT ──────────────────────────────────────────────────

class CheckoutRequest(BaseModel):
    plan:    str                  # "pro" | "gold" | "agency"
    email:   Optional[str] = None
    billing: Optional[str] = "month"   # "month" | "year"


@router.post("/create-checkout-session")
async def create_checkout_session(body: CheckoutRequest, request: Request):
    """Crée une session Stripe Checkout et retourne l'URL de paiement."""
    if not stripe.api_key:
        raise HTTPException(503, detail="Stripe non configuré (STRIPE_SECRET_KEY manquant).")

    billing = "year" if (body.billing or "month").lower().startswith("year") else "month"
    price_id = get_price_id(body.plan, billing)
    if not price_id:
        suffix = "_YEAR" if billing == "year" else ""
        raise HTTPException(
            400,
            detail=f"Plan '{body.plan}' ({billing}) inconnu ou STRIPE_PRICE_{body.plan.upper()}{suffix} non configuré.",
        )

    base = str(request.base_url).rstrip("/")

    try:
        params: dict = {
            "mode":         "subscription",
            "line_items":   [{"price": price_id, "quantity": 1}],
            "success_url":  f"{base}/?checkout=success&session_id={{CHECKOUT_SESSION_ID}}",
            "cancel_url":   f"{base}/?checkout=cancel",
            "metadata":     {"plan": body.plan, "billing": billing},
            "allow_promotion_codes": True,
        }
        if body.email:
            params["customer_email"] = body.email

        session = stripe.checkout.Session.create(**params)
        return {"url": session.url}

    except stripe.error.StripeError as e:
        raise HTTPException(500, detail=str(e.user_message or e))


# ── CUSTOMER PORTAL ───────────────────────────────────────────

@router.post("/customer-portal")
async def customer_portal(request: Request):
    """Redirige l'abonné vers le portail Stripe (gérer/annuler l'abonnement)."""
    if not stripe.api_key:
        raise HTTPException(503, "Stripe non configuré.")

    data = await request.json()
    email = data.get("email") or ""
    customer_id = data.get("customer_id") or get_customer_id(email)

    if not customer_id:
        raise HTTPException(400, "Aucun abonnement trouvé pour ce compte.")

    base = str(request.base_url).rstrip("/")
    try:
        portal = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=f"{base}/",
        )
        return {"url": portal.url}
    except stripe.error.StripeError as e:
        raise HTTPException(500, detail=str(e.user_message or e))


# ── WEBHOOK ───────────────────────────────────────────────────

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Webhook Stripe — écoute les événements d'abonnement.
    Configure l'URL dans Stripe Dashboard → Webhooks :
      https://tts-analyzer.onrender.com/webhook
    Événements à activer :
      checkout.session.completed
      customer.subscription.deleted
      invoice.payment_failed
    """
    payload    = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    secret     = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    if not secret:
        # Mode dev sans webhook secret : traite quand même (à sécuriser en prod)
        import json
        try:
            event = {"type": "unknown", "data": {"object": {}}}
            event = json.loads(payload)
        except Exception:
            raise HTTPException(400, "Payload invalide")
    else:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, secret)
        except ValueError:
            raise HTTPException(400, "Payload invalide")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(400, "Signature invalide")

    etype = event.get("type", "")
    obj   = event.get("data", {}).get("object", {})

    # ── Paiement réussi → activer le tier ──
    if etype == "checkout.session.completed":
        plan     = (obj.get("metadata") or {}).get("plan", "pro")
        email    = (obj.get("customer_details") or {}).get("email")
        cust_id  = obj.get("customer")
        sub_id   = obj.get("subscription")
        if email:
            set_user_tier(email, plan, customer_id=cust_id, subscription_id=sub_id)

    # ── Abonnement annulé / expiré → downgrade free ──
    elif etype == "customer.subscription.deleted":
        cust_id = obj.get("customer")
        if cust_id:
            revoke_by_customer(cust_id)

    # ── Paiement échoué → log (pas de downgrade immédiat, Stripe réessaie) ──
    elif etype == "invoice.payment_failed":
        email   = (obj.get("customer_email") or "").strip()
        cust_id = obj.get("customer")
        # TODO phase 2 : envoyer un email de relance

    return {"ok": True}
