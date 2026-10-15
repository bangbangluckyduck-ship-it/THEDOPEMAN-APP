"""
🤝 Programme d'affiliation — logique métier.

Parcours :
  1. Un user connecté candidate  → apply()  → statut 'pending'.
  2. L'admin approuve/crée        → approve()/create() → statut 'approved' + code.
  3. Un lien qeerah.com/<n'importe quelle page>?ref=CODE pose un cookie 90 jours
     (middleware de main.py) ; il attribue le client à l'inscription
     (attribute_signup) ou, à défaut, au paiement (métadonnée Stripe `ref`).
  4. Chaque facture Stripe PAYÉE par un client parrainé crée une commission
     (record_invoice) ; un remboursement la réduit (handle_refund).
  5. L'affilié voit son lien, ses abonnés actifs et ses commissions
     (get_for_user) ; l'admin voit le relevé et marque les versements (mark_paid).

Règles de commission (décidées le 16/10/2026) :
  • % de chaque paiement, à vie, tant que le client paie ;
  • taux par défaut selon le type, réglable par affilié (DEFAULT_RATES) ;
  • payable DELAI_VALIDATION_JOURS après le paiement, pour laisser passer
    remboursements et litiges avant de verser quoi que ce soit.

Toutes les fonctions prennent le client supabase (service_role) en paramètre —
les tables sont verrouillées en RLS (aucun accès via la clé anon).
Le calcul lui-même (taux, montant, relevé) est fait par des fonctions pures,
testées sans base : test_affiliates.py.
"""
from __future__ import annotations

import secrets
import string
from datetime import date, datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"
STATUS_DISABLED = "disabled"

# ── Règles de commission ─────────────────────────────────────────────────────
TYPE_CREATEUR = "createur"
TYPE_AGENCE = "agence"
TYPES = (TYPE_CREATEUR, TYPE_AGENCE)
# Taux par défaut en % ; un taux personnalisé (affiliates.commission_rate) prime.
DEFAULT_RATES = {TYPE_CREATEUR: 25.0, TYPE_AGENCE: 20.0}
DELAI_VALIDATION_JOURS = 30

COMM_PENDING = "pending"      # en attente, ou payable si payable_at est passé
COMM_PAID = "paid"            # versé à l'affilié
COMM_CANCELLED = "cancelled"  # remboursé en totalité avant versement

# Tiers qui correspondent à un abonnement Stripe payant.
_TIERS_PAYANTS = ("pro", "gold", "agency")

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


def _reglages(type_: Optional[str], rate: Optional[float], name: Optional[str]) -> dict:
    """Champs type / taux / nom validés. Un taux vide = taux par défaut du type."""
    data: dict = {}
    if type_ is not None:
        if type_ not in TYPES:
            raise ValueError("bad_type")
        data["type"] = type_
    if rate is not None:
        if not 0 <= float(rate) <= 100:
            raise ValueError("bad_rate")
        data["commission_rate"] = float(rate)
    if name is not None:
        data["name"] = name.strip()[:120] or None
    return data


def create_approved(supabase, email: str, type_: str = TYPE_CREATEUR,
                    rate: Optional[float] = None, name: Optional[str] = None) -> dict:
    """Admin crée un affilié directement (déjà approuvé + code)."""
    email = (email or "").lower().strip()
    if not supabase or not email or "@" not in email:
        return {"ok": False, "error": "bad_email"}
    try:
        reglages = _reglages(type_, rate, name)
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    if get_by_email(supabase, email):
        res = set_status(supabase, email, STATUS_APPROVED)
        if res.get("ok") and reglages:
            return update_settings(supabase, email, type_, rate, name)
        return res
    try:
        supabase.table("affiliates").insert({
            "email": email,
            "status": STATUS_APPROVED,
            "code": _gen_code(supabase),
            "created_at": _now(),
            "approved_at": _now(),
            **reglages,
        }).execute()
        return {"ok": True, "affiliate": get_by_email(supabase, email)}
    except Exception as e:
        print(f"affiliates.create_approved error: {e}")
        return {"ok": False, "error": "insert_failed"}


def update_settings(supabase, email: str, type_: Optional[str] = None,
                    rate: Optional[float] = None, name: Optional[str] = None,
                    reset_rate: bool = False) -> dict:
    """Change le type, le taux personnalisé (ou le remet au défaut) et le nom.

    Un nouveau taux ne s'applique qu'aux paiements FUTURS : chaque commission
    garde le taux figé au moment de la facture (colonne `rate`)."""
    email = (email or "").lower().strip()
    try:
        data = _reglages(type_, rate, name)
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    if reset_rate:
        data["commission_rate"] = None
    if not data:
        return {"ok": False, "error": "nothing_to_update"}
    aff = get_by_email(supabase, email)
    if not aff:
        return {"ok": False, "error": "not_found"}
    try:
        supabase.table("affiliates").update(data).eq("email", email).execute()
        return {"ok": True, "affiliate": {**aff, **data}}
    except Exception as e:
        print(f"affiliates.update_settings error: {e}")
        return {"ok": False, "error": "update_failed"}


def attribute_signup(supabase, new_email: str, ref_code: str) -> bool:
    """Rattache un client à un code d'affilié APPROUVÉ.

    Appelée à la création du compte, et au paiement pour un client qui a payé
    sans s'être inscrit d'abord. Ne remplace JAMAIS une attribution existante :
    le premier affilié qui a amené le client le garde. No-op si code
    inconnu/non approuvé ou auto-parrainage."""
    new_email = (new_email or "").lower().strip()
    ref_code = (ref_code or "").strip().lower()
    if not supabase or not new_email or not ref_code:
        return False
    aff = get_by_code(supabase, ref_code)
    if not aff or aff.get("status") != STATUS_APPROVED:
        return False
    if aff.get("email", "").lower() == new_email:   # pas d'auto-parrainage
        return False
    try:
        r = supabase.table("users").select("referred_by").eq("email", new_email).execute()
        if r.data and r.data[0].get("referred_by"):
            return False
        supabase.table("users").update({"referred_by": ref_code}).eq("email", new_email).execute()
        return True
    except Exception as e:
        print(f"affiliates.attribute_signup error: {e}")
        return False


# ── Calcul (fonctions pures) ─────────────────────────────────────────────────
def taux_effectif(aff: dict) -> float:
    """Taux personnalisé s'il existe, sinon le taux par défaut du type."""
    perso = aff.get("commission_rate")
    if perso is not None and perso != "":
        return float(perso)
    return DEFAULT_RATES.get(aff.get("type") or TYPE_CREATEUR, DEFAULT_RATES[TYPE_CREATEUR])


def calculer_commission(montant_cents: int, taux: float) -> int:
    """Commission en centimes, arrondie au centime le plus proche (0,5 → haut)."""
    if montant_cents <= 0 or taux <= 0:
        return 0
    v = Decimal(int(montant_cents)) * Decimal(str(taux)) / Decimal(100)
    return int(v.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def _ts(v) -> datetime:
    """Horodatage Stripe (secondes epoch) → datetime UTC ; repli sur maintenant."""
    try:
        return datetime.fromtimestamp(int(v), tz=timezone.utc)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)


def ligne_commission(invoice: dict, aff: dict, customer_email: str) -> Optional[dict]:
    """Ligne à insérer pour une facture Stripe payée, ou None si rien à verser.

    `amount_paid` est ce que le client a réellement payé : remises et coupons
    déjà déduits, facture d'essai à 0 € ignorée."""
    montant = int(invoice.get("amount_paid") or 0)
    if montant <= 0 or not invoice.get("id"):
        return None
    taux = taux_effectif(aff)
    paye_le = _ts((invoice.get("status_transitions") or {}).get("paid_at") or invoice.get("created"))
    return {
        "affiliate_code": aff["code"],
        "customer_email": customer_email,
        "stripe_invoice_id": invoice["id"],
        "stripe_charge_id": invoice.get("charge") or None,
        "stripe_payment_intent": invoice.get("payment_intent") or None,
        "amount_cents": montant,
        "currency": (invoice.get("currency") or "eur").lower(),
        "rate": taux,
        "commission_cents": calculer_commission(montant, taux),
        "status": COMM_PENDING,
        "invoice_paid_at": paye_le.isoformat(),
        "payable_at": (paye_le + timedelta(days=DELAI_VALIDATION_JOURS)).isoformat(),
    }


def _dt(v) -> Optional[datetime]:
    if not v:
        return None
    if isinstance(v, datetime):
        return v
    try:
        return datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except ValueError:
        return None


def releve(lignes: "list[dict]", maintenant: Optional[datetime] = None) -> dict:
    """Totaux d'un affilié, en centimes.

    en_attente : payé par le client, encore dans les 30 jours de validation ;
    a_verser   : validé, pas encore versé — c'est ce que tu dois payer ;
    verse      : déjà versé.
    Les ajustements de remboursement (montants négatifs) se déduisent de a_verser."""
    maintenant = maintenant or datetime.now(timezone.utc)
    t = {"en_attente": 0, "a_verser": 0, "verse": 0, "paiements": 0, "chiffre_affaires": 0}
    for l in lignes:
        c = int(l.get("commission_cents") or 0)
        statut = l.get("status")
        if statut == COMM_CANCELLED:
            continue
        if int(l.get("amount_cents") or 0) > 0:
            t["paiements"] += 1
            t["chiffre_affaires"] += int(l["amount_cents"]) - int(l.get("refunded_cents") or 0)
        if statut == COMM_PAID:
            t["verse"] += c
        elif (_dt(l.get("payable_at")) or maintenant) <= maintenant:
            t["a_verser"] += c
        else:
            t["en_attente"] += c
    return t


# ── Paiements Stripe ─────────────────────────────────────────────────────────
def record_invoice(supabase, invoice: dict, customer_email: str) -> Optional[dict]:
    """Facture payée (webhook invoice.paid) → commission si le client est parrainé.

    Idempotent : `stripe_invoice_id` est unique, une relivraison du webhook ne
    crée pas de doublon. Ne lève jamais : le webhook ne doit pas échouer à
    cause de l'affiliation, sinon Stripe le rejouerait en boucle."""
    email = (customer_email or "").lower().strip()
    if not supabase or not email:
        return None
    try:
        u = supabase.table("users").select("referred_by").eq("email", email).execute()
        code = (u.data[0].get("referred_by") if u.data else None) or ""
        if not code:
            return None
        aff = get_by_code(supabase, code)
        # Un affilié désactivé ne touche plus rien sur les paiements à venir.
        if not aff or aff.get("status") != STATUS_APPROVED:
            return None
        if (aff.get("email") or "").lower() == email:
            return None
        ligne = ligne_commission(invoice, aff, email)
        if not ligne:
            return None
        deja = supabase.table("affiliate_commissions").select("id") \
            .eq("stripe_invoice_id", ligne["stripe_invoice_id"]).execute()
        if deja.data:
            return None
        supabase.table("affiliate_commissions").insert(ligne).execute()
        return ligne
    except Exception as e:
        print(f"affiliates.record_invoice error: {e}")
        return None


def handle_refund(supabase, charge: dict) -> int:
    """Remboursement (webhook charge.refunded) → réduit la commission liée.

    Pas encore versée : la commission est recalculée sur le montant non
    remboursé (annulée si remboursement total). Déjà versée : une ligne
    d'ajustement négative est ajoutée, déduite du prochain versement.
    Renvoie le nombre de commissions touchées."""
    if not supabase or not charge:
        return 0
    touchees = 0
    try:
        lignes = []
        if charge.get("id"):
            lignes = supabase.table("affiliate_commissions").select("*") \
                .eq("stripe_charge_id", charge["id"]).execute().data or []
        if not lignes and charge.get("payment_intent"):
            lignes = supabase.table("affiliate_commissions").select("*") \
                .eq("stripe_payment_intent", charge["payment_intent"]).execute().data or []
        rembourse = int(charge.get("amount_refunded") or 0)
        for l in lignes:
            if int(l.get("amount_cents") or 0) <= 0:
                continue                      # ligne d'ajustement elle-même
            montant = int(l["amount_cents"])
            rembourse_l = min(rembourse, montant)
            due = calculer_commission(montant - rembourse_l, float(l["rate"]))
            if l.get("status") == COMM_PAID:
                prefixe = f"{l['stripe_invoice_id']}:ajust:"
                ajusts = supabase.table("affiliate_commissions").select("commission_cents") \
                    .like("stripe_invoice_id", prefixe + "%").execute().data or []
                deja_compte = int(l["commission_cents"]) + sum(int(a["commission_cents"]) for a in ajusts)
                delta = due - deja_compte
                if delta >= 0:
                    continue
                maintenant = _now()
                supabase.table("affiliate_commissions").insert({
                    "affiliate_code": l["affiliate_code"],
                    "customer_email": l["customer_email"],
                    "stripe_invoice_id": f"{prefixe}{rembourse_l}",
                    "amount_cents": 0,
                    "currency": l.get("currency") or "eur",
                    "rate": l["rate"],
                    "commission_cents": delta,
                    "status": COMM_PENDING,
                    "invoice_paid_at": maintenant,
                    "payable_at": maintenant,
                    "note": "ajustement remboursement",
                }).execute()
            else:
                supabase.table("affiliate_commissions").update({
                    "commission_cents": due,
                    "refunded_cents": rembourse_l,
                    "status": COMM_CANCELLED if due == 0 else l.get("status") or COMM_PENDING,
                }).eq("id", l["id"]).execute()
            touchees += 1
    except Exception as e:
        print(f"affiliates.handle_refund error: {e}")
    return touchees


# ── Lectures ─────────────────────────────────────────────────────────────────
def _abonnes_actifs(users: "list[dict]") -> int:
    """Clients parrainés avec un abonnement Stripe en cours de validité."""
    aujourdhui = date.today().isoformat()
    n = 0
    for u in users:
        if u.get("tier") not in _TIERS_PAYANTS or not u.get("subscription_id"):
            continue
        exp = (u.get("tier_expiry") or "")[:10]
        if not exp or exp >= aujourdhui:
            n += 1
    return n


def _users_parraines(supabase, code: Optional[str] = None) -> "list[dict]":
    q = supabase.table("users").select("email,referred_by,tier,subscription_id,tier_expiry")
    q = q.eq("referred_by", code) if code else q.neq("referred_by", "")
    return q.execute().data or []


def _commissions(supabase, code: Optional[str] = None) -> "list[dict]":
    try:
        q = supabase.table("affiliate_commissions").select("*")
        if code:
            q = q.eq("affiliate_code", code)
        return q.order("invoice_paid_at", desc=True).execute().data or []
    except Exception as e:
        # Table absente tant que la migration n'a pas été passée : le reste
        # du programme d'affiliation doit continuer à fonctionner.
        print(f"affiliates._commissions : {e}")
        return []


def list_all(supabase) -> list[dict]:
    """Tous les affiliés + inscrits, abonnés actifs et relevé (pour l'admin).

    Trois requêtes au total, quel que soit le nombre d'affiliés."""
    if not supabase:
        return []
    try:
        r = supabase.table("affiliates").select("*").order("created_at", desc=True).execute()
        rows = r.data or []
    except Exception:
        return []
    try:
        users = _users_parraines(supabase)
    except Exception:
        users = []
    comms = _commissions(supabase)
    for row in rows:
        code = row.get("code")
        siens = [u for u in users if code and u.get("referred_by") == code]
        row["signups"] = len(siens)
        row["active_subscribers"] = _abonnes_actifs(siens)
        row["rate_effective"] = taux_effectif(row)
        row["releve"] = releve([c for c in comms if code and c.get("affiliate_code") == code])
    return rows


def statement(supabase, code: str) -> dict:
    """Relevé détaillé d'un affilié : totaux + dernières commissions."""
    lignes = _commissions(supabase, code)
    try:
        users = _users_parraines(supabase, code)
    except Exception:
        users = []
    return {
        "signups": len(users),
        "active_subscribers": _abonnes_actifs(users),
        "releve": releve(lignes),
        "commissions": lignes[:50],
    }


def mark_paid(supabase, code: str) -> dict:
    """Marque comme versées toutes les commissions validées (payable_at passé).

    À cliquer APRÈS avoir fait le virement à l'affilié. Renvoie le montant
    marqué, pour vérifier qu'il correspond au virement."""
    if not supabase or not code:
        return {"ok": False, "error": "unavailable"}
    maintenant = datetime.now(timezone.utc)
    lignes = [l for l in _commissions(supabase, code)
              if l.get("status") == COMM_PENDING and (_dt(l.get("payable_at")) or maintenant) <= maintenant]
    total = sum(int(l.get("commission_cents") or 0) for l in lignes)
    if total <= 0:
        return {"ok": False, "error": "nothing_payable", "total_cents": total}
    try:
        ids = [l["id"] for l in lignes]
        supabase.table("affiliate_commissions").update(
            {"status": COMM_PAID, "paid_out_at": maintenant.isoformat()}).in_("id", ids).execute()
        return {"ok": True, "total_cents": total, "count": len(ids)}
    except Exception as e:
        print(f"affiliates.mark_paid error: {e}")
        return {"ok": False, "error": "update_failed"}


def get_for_user(supabase, email: str, base_url: str) -> dict:
    """État d'affiliation pour l'espace client. base_url ex: https://qeerah.com"""
    aff = get_by_email(supabase, email)
    if not aff:
        return {"is_affiliate": False, "status": None}
    code = aff.get("code")
    link = f"{base_url.rstrip('/')}/?ref={code}" if code else None
    out = {
        "is_affiliate": True,
        "status": aff.get("status"),
        "type": aff.get("type") or TYPE_CREATEUR,
        "code": code,
        "link": link,
        "rate": taux_effectif(aff),
        "validation_days": DELAI_VALIDATION_JOURS,
        "signups": 0,
        "active_subscribers": 0,
        "releve": releve([]),
    }
    if code:
        st = statement(supabase, code)
        out.update({k: st[k] for k in ("signups", "active_subscribers", "releve")})
    return out
