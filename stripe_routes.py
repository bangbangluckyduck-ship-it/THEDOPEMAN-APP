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

  PACKS DE CRÉDITS (paiement one-time, PAS des abonnements — cf. credits.py) :
  STRIPE_PRICE_CREDITS_DECOUVERTE  price_...   (9 €   → 150 crédits)
  STRIPE_PRICE_CREDITS_STANDARD    price_...   (15 €  → 300 crédits)
  STRIPE_PRICE_CREDITS_PRO         price_...   (49 €  → 1200 crédits)
  STRIPE_PRICE_CREDITS_AGENCY      price_...   (129 € → 3300 crédits)
"""
from __future__ import annotations
import os
from datetime import date as _date
import stripe
from typing import Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from auth import set_user_tier, get_customer_id, revoke_by_customer
from feature_flags import is_enabled

router = APIRouter(tags=["stripe"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

# Lancement progressif par PALIERS DE PRIX (roadmap feature_flags.py) :
# PRO 9,99€ → 11,99€ → 12,99€ ; GOLD 79€ (launch) → 99€ (normal).
_PRO_999    = {"month": os.getenv("STRIPE_PRICE_PRO_999", ""),         "year": os.getenv("STRIPE_PRICE_PRO_999_YEAR", "")}
_PRO_1199   = {"month": os.getenv("STRIPE_PRICE_PRO_1199", ""),        "year": os.getenv("STRIPE_PRICE_PRO_1199_YEAR", "")}
_PRO        = {"month": os.getenv("STRIPE_PRICE_PRO", ""),             "year": os.getenv("STRIPE_PRICE_PRO_YEAR", "")}
_GOLD_LAUNCH = {"month": os.getenv("STRIPE_PRICE_GOLD_LAUNCH", ""),    "year": os.getenv("STRIPE_PRICE_GOLD_LAUNCH_YEAR", "")}
_GOLD       = {"month": os.getenv("STRIPE_PRICE_GOLD", ""),            "year": os.getenv("STRIPE_PRICE_GOLD_YEAR", "")}
_AGENCY     = {"month": os.getenv("STRIPE_PRICE_AGENCY", ""),          "year": os.getenv("STRIPE_PRICE_AGENCY_YEAR", "")}


def get_price_id(plan: str, billing: str = "month") -> str:
    """Retourne le price_id Stripe selon le plan, la période (mois/an) et le
    palier de prix en vigueur aujourd'hui (roadmap feature_flags.py)."""
    b = "year" if (billing or "month").lower().startswith("year") else "month"

    if plan == "pro":
        if is_enabled("pro_price_12_99"):
            tier = _PRO
        elif is_enabled("pro_price_11_99"):
            tier = _PRO_1199
        else:
            tier = _PRO_999
        # Filet de sécurité : si le palier courant n'a pas de price_id configuré,
        # on retombe sur le prix final (toujours censé être configuré).
        return tier.get(b, "") or _PRO.get(b, "")

    if plan == "gold":
        tier = _GOLD if is_enabled("gold_price_normal") else _GOLD_LAUNCH
        return tier.get(b, "") or _GOLD.get(b, "")

    if plan == "agency":
        return _AGENCY.get(b, "")

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

    params: dict = {
        "mode":         "subscription",
        "line_items":   [{"price": price_id, "quantity": 1}],
        "success_url":  f"{base}/?checkout=success&session_id={{CHECKOUT_SESSION_ID}}",
        "cancel_url":   f"{base}/?checkout=cancel",
        "metadata":     {"plan": body.plan, "billing": billing},
    }
    if body.email:
        params["customer_email"] = body.email

    # Promo de lancement (variante B) : si STRIPE_LAUNCH_COUPON est défini, la remise
    # est appliquée AUTOMATIQUEMENT (le client ne tape rien). Sinon, on autorise la
    # saisie d'un code promo. Stripe interdit d'avoir les deux à la fois.
    coupon = os.getenv("STRIPE_LAUNCH_COUPON", "").strip()
    if coupon:
        params["discounts"] = [{"coupon": coupon}]
    else:
        params["allow_promotion_codes"] = True

    try:
        session = stripe.checkout.Session.create(**params)
    except stripe.error.StripeError as e:
        # Coupon expiré/invalide → on ne bloque JAMAIS le paiement : on retente au
        # plein tarif (avec saisie de code promo possible).
        if params.get("discounts"):
            params.pop("discounts", None)
            params["allow_promotion_codes"] = True
            try:
                session = stripe.checkout.Session.create(**params)
            except stripe.error.StripeError as e2:
                raise HTTPException(500, detail=str(e2.user_message or e2))
        else:
            raise HTTPException(500, detail=str(e.user_message or e))
    return {"url": session.url}


# ── PACKS DE CRÉDITS (paiement one-time) ───────────────────────
_CREDIT_PACK_PRICE_ENV = {
    "decouverte": "STRIPE_PRICE_CREDITS_DECOUVERTE",
    "standard":   "STRIPE_PRICE_CREDITS_STANDARD",
    "pro":        "STRIPE_PRICE_CREDITS_PRO",
    "agency":     "STRIPE_PRICE_CREDITS_AGENCY",
}


class CreditsCheckoutRequest(BaseModel):
    pack:  str                    # "decouverte" | "standard" | "pro" | "agency"
    email: Optional[str] = None


@router.post("/create-credits-checkout-session")
async def create_credits_checkout_session(body: CreditsCheckoutRequest, request: Request):
    """Crée une session Stripe Checkout pour un pack de crédits — paiement
    UNIQUE (mode='payment'), jamais un abonnement. Le webhook crédite le
    compte via credits.add_purchase() sur checkout.session.completed
    (metadata.type == 'credit_pack')."""
    if not stripe.api_key:
        raise HTTPException(503, detail="Stripe non configuré (STRIPE_SECRET_KEY manquant).")

    import credits as credits_mod
    pack_info = credits_mod.CREDIT_PACKS.get(body.pack)
    if not pack_info:
        raise HTTPException(400, detail=f"Pack '{body.pack}' inconnu.")

    env_var = _CREDIT_PACK_PRICE_ENV.get(body.pack, "")
    price_id = os.getenv(env_var, "") if env_var else ""
    if not price_id:
        raise HTTPException(
            400,
            detail=f"Pack '{body.pack}' : {env_var} non configuré.",
        )

    base = str(request.base_url).rstrip("/")
    params: dict = {
        "mode":         "payment",
        "line_items":   [{"price": price_id, "quantity": 1}],
        "success_url":  f"{base}/?credits=success&session_id={{CHECKOUT_SESSION_ID}}",
        "cancel_url":   f"{base}/?credits=cancel",
        "metadata":     {"type": "credit_pack", "pack": body.pack},
    }
    if body.email:
        params["customer_email"] = body.email

    try:
        session = stripe.checkout.Session.create(**params)
    except stripe.error.StripeError as e:
        raise HTTPException(500, detail=str(e.user_message or e))
    return {"url": session.url}


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
