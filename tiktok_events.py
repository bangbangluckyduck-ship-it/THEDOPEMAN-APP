"""
Événements TikTok côté SERVEUR — API Events (Events API 2.0).

Pourquoi côté serveur et pas dans le navigateur : après un paiement, le client
revient de Stripe sur /app. Un événement émis à ce moment-là serait perdu dès
qu'un bloqueur de publicités, un mode privé ou une fermeture d'onglet s'en mêle
— soit une part significative des conversions, précisément celles qu'on paie le
plus cher à acquérir. Le webhook Stripe, lui, est le SEUL endroit où l'on sait
avec certitude qu'un paiement a réussi.

DÉDOUBLONNAGE : chaque événement porte un `event_id`. TikTok considère deux
envois de même (event_name, event_id) comme UNE conversion pendant 48 h.
L'identifiant est fabriqué par le navigateur avant la redirection vers Stripe
(cf. static/qeerah-tiktok.js → checkoutContext()) et voyage dans les métadonnées
de la session Stripe. Le jour où le pixel enverrait aussi CompletePayment, les
deux se recouvriraient sans double comptage. Il rend aussi les REDISTRIBUTIONS
de webhook par Stripe inoffensives.

CONSENTEMENT : rien n'est envoyé si le navigateur n'a pas transmis
`tt_consent=1` au moment du checkout. Un envoi serveur ne sort pas du champ du
RGPD : transmettre l'empreinte de l'e-mail d'un client à une régie publicitaire
est un traitement à finalité publicitaire, qui exige le même consentement que le
pixel. Conséquence assumée : les conversions des visiteurs qui refusent ne
remontent pas dans TikTok Ads.

DONNÉES PERSONNELLES : l'e-mail n'est JAMAIS transmis en clair. TikTok exige une
empreinte SHA-256 de l'adresse normalisée (minuscules, sans espaces).

Variables d'environnement :
  TIKTOK_PIXEL_ID              — identifiant du pixel (même valeur que le navigateur)
  TIKTOK_EVENTS_ACCESS_TOKEN   — jeton « Events API » généré dans TikTok Events Manager
  TIKTOK_EVENTS_TEST_CODE      — optionnel : code de test, à RETIRER en production
                                 (les événements marqués test ne comptent pas
                                 dans les rapports)
"""
from __future__ import annotations

import hashlib
import os
import time

import httpx

API_URL = "https://business-api.tiktok.com/open_api/v1.3/event/track/"

PIXEL_ID = os.getenv("TIKTOK_PIXEL_ID", "").strip()
ACCESS_TOKEN = os.getenv("TIKTOK_EVENTS_ACCESS_TOKEN", "").strip()
TEST_EVENT_CODE = os.getenv("TIKTOK_EVENTS_TEST_CODE", "").strip()

TIMEOUT = 8.0


def _sha256(valeur: str) -> str:
    return hashlib.sha256(valeur.encode("utf-8")).hexdigest()


def _hash_email(email: str) -> str:
    """Empreinte de l'e-mail au format attendu par TikTok : minuscules, sans
    espaces autour, SHA-256 hexadécimal. Une adresse mal normalisée produit une
    empreinte différente de celle calculée par TikTok → aucune correspondance,
    donc une conversion non attribuée et silencieusement perdue."""
    email = (email or "").strip().lower()
    return _sha256(email) if email else ""


def est_configure() -> bool:
    return bool(PIXEL_ID and ACCESS_TOKEN)


async def envoyer_evenement(
    nom: str,
    event_id: str,
    *,
    email: str = "",
    url: str = "",
    ttp: str = "",
    ttclid: str = "",
    ip: str = "",
    user_agent: str = "",
    value: float | None = None,
    currency: str = "EUR",
    contents: list | None = None,
    event_time: int | None = None,
) -> bool:
    """Envoie un événement à TikTok. Best-effort : renvoie False et trace, mais
    ne lève jamais — un incident chez TikTok ne doit pas faire échouer le
    webhook Stripe (Stripe rejouerait alors le paiement en boucle)."""
    if not est_configure():
        print("[tiktok_events] non configuré (TIKTOK_PIXEL_ID / "
              "TIKTOK_EVENTS_ACCESS_TOKEN absents) — événement non envoyé.")
        return False

    utilisateur: dict = {}
    empreinte = _hash_email(email)
    if empreinte:
        utilisateur["email"] = empreinte
    if ttp:
        utilisateur["ttp"] = ttp
    if ttclid:
        utilisateur["ttclid"] = ttclid
    if ip:
        utilisateur["ip"] = ip
    if user_agent:
        utilisateur["user_agent"] = user_agent

    proprietes: dict = {"currency": currency}
    if value is not None:
        proprietes["value"] = value
    if contents:
        proprietes["contents"] = contents

    evenement: dict = {
        "event": nom,
        "event_time": int(event_time or time.time()),
        "event_id": event_id,
        "user": utilisateur,
        "properties": proprietes,
    }
    if url:
        evenement["page"] = {"url": url}

    charge: dict = {
        "event_source": "web",
        "event_source_id": PIXEL_ID,
        "data": [evenement],
    }
    if TEST_EVENT_CODE:
        charge["test_event_code"] = TEST_EVENT_CODE

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            reponse = await client.post(
                API_URL,
                json=charge,
                headers={
                    "Access-Token": ACCESS_TOKEN,
                    "Content-Type": "application/json",
                },
            )
        corps = reponse.json()
        # ⚠️ TikTok répond HTTP 200 même en cas d'erreur métier : le verdict est
        # dans `code` (0 = succès). Se fier au statut HTTP ferait passer un jeton
        # invalide ou un pixel inconnu pour un envoi réussi.
        if reponse.status_code == 200 and corps.get("code") == 0:
            print(f"[tiktok_events] {nom} envoyé (event_id={event_id})")
            return True
        print(f"[tiktok_events] {nom} REFUSÉ par TikTok "
              f"(http={reponse.status_code}, code={corps.get('code')}, "
              f"message={corps.get('message')})")
        return False
    except Exception as e:
        print(f"[tiktok_events] {nom} non envoyé ({type(e).__name__}: {e})")
        return False


async def envoyer_complete_payment(
    *,
    event_id: str,
    email: str,
    value: float,
    currency: str = "EUR",
    url: str = "",
    ttp: str = "",
    ttclid: str = "",
    ip: str = "",
    user_agent: str = "",
    content_id: str = "qeerah_pro",
) -> bool:
    """Conversion d'abonnement payé."""
    return await envoyer_evenement(
        "CompletePayment",
        event_id,
        email=email,
        url=url,
        ttp=ttp,
        ttclid=ttclid,
        ip=ip,
        user_agent=user_agent,
        value=value,
        currency=currency,
        contents=[{
            "content_id": content_id,
            "content_type": "product",
            "content_name": "Qeerah Pro",
            "quantity": 1,
            "price": value,
        }],
    )
