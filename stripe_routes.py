"""
Routes Stripe — Checkout, Customer Portal, Webhooks.

Variables d'environnement Render à configurer :
  STRIPE_SECRET_KEY              sk_live_...
  STRIPE_PUBLISHABLE_KEY         pk_live_...
  STRIPE_WEBHOOK_SECRET          whsec_...

  QEERAH PRO — offre unique (2 prix, à créer sur Stripe) :
  STRIPE_PRICE_QEERAH_PRO_MONTH  price_...   (29,99 €/mois)
  STRIPE_PRICE_QEERAH_PRO_YEAR   price_...   (299 €/an, 2 mois offerts)

  ⚠️ Noms VOLONTAIREMENT nouveaux. Réutiliser STRIPE_PRICE_PRO / _YEAR aurait
  fait vendre les anciens tarifs (12,99 € / 129,90 €) en silence tant que
  Render n'aurait pas été mis à jour. Ici, une variable absente = erreur
  explicite au checkout, jamais un repli sur un prix périmé.

  PACKS DE CRÉDITS (paiement one-time, PAS des abonnements — cf. credits.py) :
  STRIPE_PRICE_CREDITS_DECOUVERTE  price_...   (9 €   → 150 crédits)
  STRIPE_PRICE_CREDITS_STANDARD    price_...   (15 €  → 300 crédits)
  STRIPE_PRICE_CREDITS_PRO         price_...   (49 €  → 1200 crédits)
  STRIPE_PRICE_CREDITS_AGENCY      price_...   (129 € → 3300 crédits)
"""
from __future__ import annotations
import os
import stripe
from typing import Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from auth import set_user_tier, get_customer_id, revoke_by_customer

router = APIRouter(tags=["stripe"])

# Mention portée au pied des factures. En franchise en base de TVA, l'article
# 293 B du CGI impose de l'indiquer. Réglable via STRIPE_INVOICE_FOOTER : le
# régime change si le seuil de franchise est franchi, et le libellé doit alors
# être adapté sans redéploiement. Variable vidée = aucune mention.
INVOICE_FOOTER = os.getenv(
    "STRIPE_INVOICE_FOOTER",
    "TVA non applicable, article 293 B du CGI",
).strip()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

# Offre unique « Qeerah Pro » — 29,99 €/mois ou 299 €/an.
_QEERAH_PRO = {
    "month": os.getenv("STRIPE_PRICE_QEERAH_PRO_MONTH", ""),
    "year":  os.getenv("STRIPE_PRICE_QEERAH_PRO_YEAR", ""),
}


def get_price_id(plan: str, billing: str = "month") -> str:
    """Retourne le price_id Stripe de l'offre unique.

    Aucun repli sur un autre prix : si la variable d'environnement n'est pas
    posée, on renvoie une chaîne vide et l'appelant lève une 400 explicite.
    Un repli silencieux risquerait de vendre un tarif archivé."""
    if plan != "pro":
        return ""
    b = "year" if (billing or "month").lower().startswith("year") else "month"
    return _QEERAH_PRO.get(b, "")


PLAN_NAMES = {
    "pro": "Qeerah Pro — 29,99 €/mois (299 €/an)",
}


# ── CHECKOUT ──────────────────────────────────────────────────

class CheckoutRequest(BaseModel):
    plan:    Optional[str] = "pro"     # seule valeur acceptée : "pro"
    email:   Optional[str] = None
    billing: Optional[str] = "month"   # "month" | "year"


@router.post("/create-checkout-session")
async def create_checkout_session(body: CheckoutRequest, request: Request):
    """Crée une session Stripe Checkout et retourne l'URL de paiement."""
    if not stripe.api_key:
        raise HTTPException(503, detail="Stripe non configuré (STRIPE_SECRET_KEY manquant).")

    plan = (body.plan or "pro").lower()
    if plan != "pro":
        # gold / agency / ltd ne sont plus vendus. Refus explicite plutôt que
        # silencieux : un ancien bouton oublié quelque part doit se voir.
        raise HTTPException(
            400,
            detail="Une seule offre est disponible : Qeerah Pro.",
        )

    billing = "year" if (body.billing or "month").lower().startswith("year") else "month"
    price_id = get_price_id(plan, billing)
    if not price_id:
        var = "STRIPE_PRICE_QEERAH_PRO_YEAR" if billing == "year" else "STRIPE_PRICE_QEERAH_PRO_MONTH"
        raise HTTPException(
            400,
            detail=f"Offre indisponible : {var} n'est pas configurée.",
        )

    base = str(request.base_url).rstrip("/")

    params: dict = {
        "mode":         "subscription",
        "line_items":   [{"price": price_id, "quantity": 1}],
        "success_url":  f"{base}/?checkout=success&session_id={{CHECKOUT_SESSION_ID}}",
        "cancel_url":   f"{base}/?checkout=cancel",
        "metadata":     {"plan": plan, "billing": billing},
        # ── Facturation entreprise ────────────────────────────────────────
        # Sans ces deux options, la facture d'abonnement générée par Stripe ne
        # portait que l'e-mail : ni raison sociale, ni adresse, ni n° de TVA —
        # donc inexploitable par la comptabilité d'une société.
        "billing_address_collection": "required",
        "tax_id_collection": {"enabled": True},
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
        # ── Facturation entreprise ────────────────────────────────────────
        # En mode 'payment', Stripe n'émet AUCUNE facture par défaut : l'acheteur
        # ne recevait qu'un reçu de paiement, impossible à passer en comptabilité.
        # invoice_creation génère une vraie facture PDF ; customer_creation
        # garantit qu'un client Stripe existe pour la rattacher.
        # Le pied de page porte la mention d'exonération de TVA, obligatoire en
        # franchise en base. Libellé réglable sans redéploiement (le régime peut
        # changer si le seuil est franchi) ; vider la variable pour l'ôter.
        "invoice_creation": {
            "enabled": True,
            "invoice_data": {"footer": INVOICE_FOOTER} if INVOICE_FOOTER else {},
        },
        "customer_creation": "always",
        "billing_address_collection": "required",
        "tax_id_collection": {"enabled": True},
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
