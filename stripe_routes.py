"""
Routes Stripe — Checkout, Customer Portal, Webhooks.

Variables d'environnement Render à configurer :
  STRIPE_SECRET_KEY        sk_live_...  (ou sk_test_... en dev)
  STRIPE_PUBLISHABLE_KEY   pk_live_...
  STRIPE_WEBHOOK_SECRET    whsec_...
  STRIPE_PRICE_PRO         price_...    (9,99 €/mois)
  STRIPE_PRICE_GOLD        price_...    (99 €/mois)
  STRIPE_PRICE_AGENCY      price_...    (249 €/mois)
"""
from __future__ import annotations
import os
import stripe
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from auth import set_user_tier, get_customer_id, revoke_by_customer

router = APIRouter(tags=["stripe"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

# Price IDs — remplis dans Render une fois les prix créés dans le dashboard Stripe
PRICE_IDS: dict[str, str] = {
    "pro":    os.getenv("STRIPE_PRICE_PRO",    ""),
    "gold":   os.getenv("STRIPE_PRICE_GOLD",   ""),
    "agency": os.getenv("STRIPE_PRICE_AGENCY", ""),
}

PLAN_NAMES = {
    "pro":    "PRO — 9,99 €/mois",
    "gold":   "GOLD — 99 €/mois",
    "agency": "AGENCY — 249 €/mois",
}


# ── CHECKOUT ──────────────────────────────────────────────────

class CheckoutRequest(BaseModel):
    plan:  str            # "pro" | "gold" | "agency"
    email: str | None = None


@router.post("/create-checkout-session")
async def create_checkout_session(body: CheckoutRequest, request: Request):
    """Crée une session Stripe Checkout et retourne l'URL de paiement."""
    if not stripe.api_key:
        raise HTTPException(503, detail="Stripe non configuré (STRIPE_SECRET_KEY manquant).")

    price_id = PRICE_IDS.get(body.plan)
    if not price_id:
        raise HTTPException(
            400,
            detail=f"Plan '{body.plan}' inconnu ou STRIPE_PRICE_{body.plan.upper()} non configuré.",
        )

    base = str(request.base_url).rstrip("/")

    try:
        params: dict = {
            "mode":         "subscription",
            "line_items":   [{"price": price_id, "quantity": 1}],
            "success_url":  f"{base}/?checkout=success&session_id={{CHECKOUT_SESSION_ID}}",
            "cancel_url":   f"{base}/?checkout=cancel",
            "metadata":     {"plan": body.plan},
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
