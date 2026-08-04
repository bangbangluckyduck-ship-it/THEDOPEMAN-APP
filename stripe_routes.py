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
from auth import set_user_tier, get_customer_id, revoke_by_customer, get_user_from_request

router = APIRouter(tags=["stripe"])


def _session_email(request: Request) -> str:
    """E-mail de la session, ou chaîne vide si le visiteur n'est pas connecté.

    Ne lève jamais : un jeton absent ou expiré vaut « pas connecté », c'est à
    l'appelant de décider si cela bloque. Sert à ne JAMAIS faire confiance à un
    e-mail fourni dans le corps de la requête quand une session existe.
    """
    try:
        user = get_user_from_request(request)
        return (user.get("email") or "").lower().strip() if user.get("valid") else ""
    except Exception:
        return ""

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

    # ── Suivi publicitaire TikTok ────────────────────────────────────────
    # Renseignés par static/qeerah-tiktok.js UNIQUEMENT si le visiteur a
    # accordé la finalité « publicité ». Recopiés dans les métadonnées Stripe
    # pour que le webhook puisse envoyer CompletePayment à TikTok : c'est le
    # seul endroit qui sait qu'un paiement a réellement abouti.
    # Sans tt_consent="1", le webhook n'envoie rien.
    tt_consent:  Optional[str] = None
    tt_event_id: Optional[str] = None   # identifiant de dédoublonnage navigateur ↔ serveur
    tt_ttp:      Optional[str] = None   # cookie _ttp posé par le pixel
    tt_ttclid:   Optional[str] = None   # identifiant de clic publicitaire
    tt_url:      Optional[str] = None   # page d'où part le paiement


def _tiktok_metadata(body: CheckoutRequest, request: Request) -> dict:
    """Métadonnées Stripe portant le contexte publicitaire TikTok.

    Renvoie un dictionnaire VIDE tant que le visiteur n'a pas accordé la
    finalité publicité : sans consentement, aucune donnée ne doit être stockée
    ni, plus tard, transmise à TikTok.

    L'adresse IP et le user-agent viennent d'ICI et pas du webhook : le webhook
    est appelé par Stripe, son IP est celle de Stripe. Ils améliorent la mise en
    correspondance côté TikTok — sans eux, seuls l'empreinte de l'e-mail et le
    cookie _ttp permettent de rattacher la conversion à une publicité.

    Stripe plafonne chaque valeur de métadonnée à 500 caractères : on tronque.
    """
    if (body.tt_consent or "") != "1":
        return {}

    entetes = request.headers
    ip = (entetes.get("x-forwarded-for", "").split(",")[0].strip()
          or (request.client.host if request.client else ""))

    donnees = {
        "tt_consent":  "1",
        "tt_event_id": body.tt_event_id or "",
        "tt_ttp":      body.tt_ttp or "",
        "tt_ttclid":   body.tt_ttclid or "",
        "tt_url":      body.tt_url or "",
        "tt_ua":       entetes.get("user-agent", ""),
        "tt_ip":       ip,
    }
    return {k: v[:500] for k, v in donnees.items() if v}


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
        # Retour vers /app, pas vers la page d'accueil : l'accueil est la page de
        # VENTE, elle ne charge pas app_v3.js et ne sait donc pas traiter
        # `checkout=success`. Un client qui venait de payer revoyait l'argumentaire
        # commercial avec un paramètre orphelin dans l'URL, sans confirmation.
        "success_url":  f"{base}/app?checkout=success&session_id={{CHECKOUT_SESSION_ID}}",
        "cancel_url":   f"{base}/pricing?checkout=cancel",
        "metadata":     {"plan": plan, "billing": billing, **_tiktok_metadata(body, request)},
        # ── Facturation entreprise ────────────────────────────────────────
        # Sans ces deux options, la facture d'abonnement générée par Stripe ne
        # portait que l'e-mail : ni raison sociale, ni adresse, ni n° de TVA —
        # donc inexploitable par la comptabilité d'une société.
        "billing_address_collection": "required",
        "tax_id_collection": {"enabled": True},
    }
    # ⚠️ MENTION TVA — action à faire dans le Dashboard Stripe, pas ici.
    # INVOICE_FOOTER (« TVA non applicable, article 293 B du CGI ») n'est appliqué
    # qu'aux paiements uniques, via `invoice_creation.invoice_data.footer`. L'API
    # Checkout n'expose AUCUN équivalent pour un abonnement : `subscription_data` ne
    # porte pas de pied de page. Les factures d'abonnement — le produit principal —
    # sortent donc sans la mention obligatoire en franchise en base.
    # → Renseigner le pied de page par défaut dans Stripe → Paramètres → Facturation
    #   → Modèle de facture. Cela couvre les deux modes d'un seul coup.

    # L'e-mail de la session prime TOUJOURS sur celui du corps de requête : un
    # visiteur connecté ne peut pas ouvrir un paiement au nom d'un autre compte,
    # et l'adresse facturée est forcément celle qui recevra l'abonnement.
    # `client_reference_id` rattache la session Stripe au compte : si l'acheteur
    # saisit malgré tout une autre adresse, le webhook sait à qui créditer.
    buyer_email = _session_email(request) or (body.email or "")
    if buyer_email:
        params["customer_email"] = buyer_email
        params["client_reference_id"] = buyer_email

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
        "success_url":  f"{base}/app?credits=success&session_id={{CHECKOUT_SESSION_ID}}",
        "cancel_url":   f"{base}/credits?credits=cancel",
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
    # Même règle que pour l'abonnement : la session prime sur le corps de requête.
    buyer_email = _session_email(request) or (body.email or "")
    if buyer_email:
        params["customer_email"] = buyer_email
        params["client_reference_id"] = buyer_email

    try:
        session = stripe.checkout.Session.create(**params)
    except stripe.error.StripeError as e:
        raise HTTPException(500, detail=str(e.user_message or e))
    return {"url": session.url}


# ── CUSTOMER PORTAL ───────────────────────────────────────────

@router.post("/customer-portal")
async def customer_portal(request: Request):
    """Redirige l'abonné vers le portail Stripe (gérer/annuler l'abonnement).

    ⚠️ SÉCURITÉ : l'identité vient EXCLUSIVEMENT de la session. Cette route lisait
    auparavant `email` / `customer_id` dans le corps de la requête, sans jamais
    vérifier de jeton — n'importe qui pouvait donc obtenir une URL de portail au nom
    d'un autre abonné (factures, adresse de facturation, moyen de paiement, et
    résiliation de l'abonnement) en connaissant simplement son adresse e-mail.
    Le corps de la requête est désormais entièrement ignoré.
    """
    # L'authentification est vérifiée AVANT l'état de configuration : un appelant
    # anonyme ne doit rien apprendre sur le paramétrage du service.
    email = _session_email(request)
    if not email:
        raise HTTPException(401, "Connecte-toi pour gérer ton abonnement.")

    if not stripe.api_key:
        raise HTTPException(503, "Stripe non configuré.")

    customer_id = get_customer_id(email)
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
#
# (supprimé) Ce module exposait un SECOND handler de webhook sur `POST /webhook`
# — le routeur n'ayant pas de préfixe, il était servi à la racine du domaine.
# Ce n'était pas celui branché côté Stripe (c'est `/api/v1/stripe/webhook`, dans
# main.py), mais il restait joignable et contenait un repli dangereux : sans
# STRIPE_WEBHOOK_SECRET, il traitait le payload SANS vérifier la signature et
# accordait le tier « pro » à l'adresse e-mail indiquée dans le corps.
#
# Un seul handler de webhook désormais, celui qui reçoit réellement les
# événements : main.py → `@app.post("/api/v1/stripe/webhook")`.
