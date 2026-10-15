"""Tests du programme d'affiliation : attribution, commissions, remboursements,
versements.

POURQUOI CE FICHIER EXISTE — c'est de l'argent. Une commission calculée deux
fois (webhook relivré), versée sur une facture remboursée, ou attribuée au
mauvais affilié ne casse rien de visible : elle se paie, c'est tout.

Pas de base réelle : `FauxSupabase` imite la poignée d'appels du client
Supabase utilisés par affiliates.py.

Lancement :
    venv/bin/python test_affiliates.py
    (ou python -m pytest test_affiliates.py)
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

import affiliates as aff


# ── Faux client Supabase ─────────────────────────────────────────────────────
class _Res:
    def __init__(self, data):
        self.data = data
        self.count = len(data)


class _Requete:
    def __init__(self, base, table):
        self.base, self.table, self.filtres, self.op, self.valeurs = base, table, [], "select", None

    def select(self, *_a, **_k):
        self.op = "select"; return self

    def insert(self, valeurs):
        self.op, self.valeurs = "insert", valeurs; return self

    def update(self, valeurs):
        self.op, self.valeurs = "update", valeurs; return self

    def eq(self, c, v):
        self.filtres.append(lambda r: r.get(c) == v); return self

    def neq(self, c, v):
        self.filtres.append(lambda r: r.get(c) not in (v, None)); return self

    def like(self, c, motif):
        p = motif.rstrip("%")
        self.filtres.append(lambda r: str(r.get(c) or "").startswith(p)); return self

    def in_(self, c, vs):
        self.filtres.append(lambda r: r.get(c) in vs); return self

    def order(self, *_a, **_k):
        return self

    def execute(self):
        lignes = self.base.setdefault(self.table, [])
        if self.op == "insert":
            ligne = {"id": len(lignes) + 1, **self.valeurs}
            lignes.append(ligne)
            return _Res([ligne])
        cibles = [r for r in lignes if all(f(r) for f in self.filtres)]
        if self.op == "update":
            for r in cibles:
                r.update(self.valeurs)
        return _Res([dict(r) for r in cibles])


class FauxSupabase:
    def __init__(self):
        self.base: dict = {}

    def table(self, nom):
        return _Requete(self.base, nom)


def _monde(type_="createur", rate=None, status="approved"):
    sb = FauxSupabase()
    sb.base["affiliates"] = [{"id": 1, "email": "agence@ex.com", "code": "abcd1234",
                              "status": status, "type": type_, "commission_rate": rate}]
    sb.base["users"] = [
        {"email": "client@ex.com", "referred_by": "abcd1234", "tier": "pro",
         "subscription_id": "sub_1", "tier_expiry": "2999-01-01"},
        {"email": "inconnu@ex.com", "referred_by": None, "tier": "pro", "subscription_id": "sub_2"},
        {"email": "agence@ex.com", "referred_by": "abcd1234", "tier": "pro", "subscription_id": "sub_3"},
    ]
    return sb


def _facture(id_="in_1", montant=2999, jours=0, charge="ch_1"):
    paye = datetime.now(timezone.utc) - timedelta(days=jours)
    return {"id": id_, "amount_paid": montant, "currency": "eur", "charge": charge,
            "payment_intent": "pi_" + id_, "status_transitions": {"paid_at": int(paye.timestamp())}}


# ── Calcul ───────────────────────────────────────────────────────────────────
def test_taux_par_defaut_selon_le_type():
    assert aff.taux_effectif({"type": "createur"}) == 25.0
    assert aff.taux_effectif({"type": "agence"}) == 20.0
    assert aff.taux_effectif({}) == 25.0


def test_un_taux_personnalise_prime():
    assert aff.taux_effectif({"type": "agence", "commission_rate": 25}) == 25.0
    assert aff.taux_effectif({"type": "agence", "commission_rate": 0}) == 0.0


def test_commission_arrondie_au_centime():
    assert aff.calculer_commission(2999, 20) == 600       # 599,8 → 6,00 €
    assert aff.calculer_commission(29900, 30) == 8970
    assert aff.calculer_commission(2999, 12.5) == 375     # 374,875 → 3,75 €
    assert aff.calculer_commission(0, 20) == 0


def test_une_facture_a_zero_ne_cree_rien():
    """Facture d'essai ou 100 % remisée : rien à commissionner."""
    assert aff.ligne_commission(_facture(montant=0), {"code": "x"}, "c@ex.com") is None


def test_payable_trente_jours_apres_le_paiement():
    l = aff.ligne_commission(_facture(), {"code": "x", "type": "createur"}, "c@ex.com")
    ecart = datetime.fromisoformat(l["payable_at"]) - datetime.fromisoformat(l["invoice_paid_at"])
    assert ecart == timedelta(days=aff.DELAI_VALIDATION_JOURS)


def test_releve():
    maintenant = datetime.now(timezone.utc)
    passe, futur = (maintenant - timedelta(days=1)).isoformat(), (maintenant + timedelta(days=5)).isoformat()
    lignes = [
        {"amount_cents": 2999, "commission_cents": 600, "status": "pending", "payable_at": futur},
        {"amount_cents": 2999, "commission_cents": 600, "status": "pending", "payable_at": passe},
        {"amount_cents": 2999, "commission_cents": 600, "status": "paid", "payable_at": passe},
        {"amount_cents": 2999, "commission_cents": 0, "status": "cancelled", "payable_at": passe},
        {"amount_cents": 0, "commission_cents": -300, "status": "pending", "payable_at": passe},
    ]
    r = aff.releve(lignes, maintenant)
    assert r["en_attente"] == 600
    assert r["a_verser"] == 300          # 600 validés − 300 d'ajustement de remboursement
    assert r["verse"] == 600
    assert r["paiements"] == 3


# ── Attribution ──────────────────────────────────────────────────────────────
def test_attribution_ne_remplace_jamais_un_affilie_existant():
    sb = _monde()
    sb.base["affiliates"].append({"id": 2, "email": "autre@ex.com", "code": "zzzz9999", "status": "approved"})
    assert aff.attribute_signup(sb, "client@ex.com", "zzzz9999") is False
    assert sb.base["users"][0]["referred_by"] == "abcd1234"


def test_attribution_d_un_client_non_rattache():
    sb = _monde()
    assert aff.attribute_signup(sb, "inconnu@ex.com", "ABCD1234") is True   # casse ignorée
    assert sb.base["users"][1]["referred_by"] == "abcd1234"


def test_pas_d_attribution_a_un_affilie_desactive():
    sb = _monde(status="disabled")
    assert aff.attribute_signup(sb, "inconnu@ex.com", "abcd1234") is False


# ── Commissions ──────────────────────────────────────────────────────────────
def test_paiement_d_un_client_parraine():
    sb = _monde(type_="agence")
    l = aff.record_invoice(sb, _facture(montant=29900), "client@ex.com")
    assert l["commission_cents"] == 5980 and l["rate"] == 20.0
    assert len(sb.base["affiliate_commissions"]) == 1


def test_webhook_relivre_ne_compte_qu_une_fois():
    sb = _monde()
    aff.record_invoice(sb, _facture(), "client@ex.com")
    aff.record_invoice(sb, _facture(), "client@ex.com")
    assert len(sb.base["affiliate_commissions"]) == 1


def test_chaque_renouvellement_compte():
    """« À vie » : chaque facture payée génère sa commission."""
    sb = _monde()
    for i in range(3):
        aff.record_invoice(sb, _facture(id_=f"in_{i}"), "client@ex.com")
    assert len(sb.base["affiliate_commissions"]) == 3


def test_client_non_parraine_ne_cree_rien():
    sb = _monde()
    assert aff.record_invoice(sb, _facture(), "inconnu@ex.com") is None


def test_affilie_desactive_ne_touche_plus_rien():
    sb = _monde(status="disabled")
    assert aff.record_invoice(sb, _facture(), "client@ex.com") is None


def test_pas_de_commission_sur_ses_propres_paiements():
    sb = _monde()
    assert aff.record_invoice(sb, _facture(), "agence@ex.com") is None


def test_le_taux_est_fige_au_moment_du_paiement():
    sb = _monde()
    aff.record_invoice(sb, _facture(id_="in_a"), "client@ex.com")
    sb.base["affiliates"][0]["commission_rate"] = 50
    aff.record_invoice(sb, _facture(id_="in_b"), "client@ex.com")
    taux = [l["rate"] for l in sb.base["affiliate_commissions"]]
    assert taux == [25.0, 50.0]


# ── Remboursements ───────────────────────────────────────────────────────────
def test_remboursement_total_avant_versement_annule():
    sb = _monde()
    aff.record_invoice(sb, _facture(), "client@ex.com")
    aff.handle_refund(sb, {"id": "ch_1", "amount": 2999, "amount_refunded": 2999})
    l = sb.base["affiliate_commissions"][0]
    assert l["status"] == "cancelled" and l["commission_cents"] == 0


def test_remboursement_partiel_avant_versement_reduit():
    sb = _monde()
    aff.record_invoice(sb, _facture(montant=3000), "client@ex.com")
    aff.handle_refund(sb, {"id": "ch_1", "amount": 3000, "amount_refunded": 1500})
    l = sb.base["affiliate_commissions"][0]
    assert l["status"] == "pending" and l["commission_cents"] == 375


def test_remboursement_apres_versement_cree_un_ajustement_negatif():
    sb = _monde()
    aff.record_invoice(sb, _facture(montant=3000), "client@ex.com")
    sb.base["affiliate_commissions"][0]["status"] = "paid"
    aff.handle_refund(sb, {"id": "ch_1", "amount": 3000, "amount_refunded": 3000})
    aff.handle_refund(sb, {"id": "ch_1", "amount": 3000, "amount_refunded": 3000})  # relivré
    ajusts = [l for l in sb.base["affiliate_commissions"] if l["amount_cents"] == 0]
    assert len(ajusts) == 1 and ajusts[0]["commission_cents"] == -750


def test_remboursement_retrouve_par_payment_intent():
    """API Stripe récente : la facture n'a pas de `charge`, seulement le PI."""
    sb = _monde()
    aff.record_invoice(sb, _facture(charge=None), "client@ex.com")
    n = aff.handle_refund(sb, {"id": "ch_x", "payment_intent": "pi_in_1", "amount": 2999, "amount_refunded": 2999})
    assert n == 1


# ── Versements ───────────────────────────────────────────────────────────────
def test_marquer_verse_ne_touche_que_le_valide():
    sb = _monde()
    aff.record_invoice(sb, _facture(id_="vieux", jours=40), "client@ex.com")
    aff.record_invoice(sb, _facture(id_="recent", jours=2), "client@ex.com")
    res = aff.mark_paid(sb, "abcd1234")
    assert res["ok"] and res["total_cents"] == 750 and res["count"] == 1
    statuts = {l["stripe_invoice_id"]: l["status"] for l in sb.base["affiliate_commissions"]}
    assert statuts == {"vieux": "paid", "recent": "pending"}


def test_rien_a_verser():
    sb = _monde()
    aff.record_invoice(sb, _facture(jours=2), "client@ex.com")
    assert aff.mark_paid(sb, "abcd1234")["ok"] is False


def test_abonnes_actifs():
    users = [
        {"tier": "pro", "subscription_id": "s", "tier_expiry": "2999-01-01"},
        {"tier": "pro", "subscription_id": "s", "tier_expiry": "2000-01-01"},   # expiré
        {"tier": "free", "subscription_id": "s"},                               # résilié
        {"tier": "pro", "subscription_id": None},                               # accordé à la main
    ]
    assert aff._abonnes_actifs(users) == 1


# ── Capture du lien ──────────────────────────────────────────────────────────
def test_le_lien_marche_sur_toutes_les_pages():
    from fastapi.testclient import TestClient
    import main
    client = TestClient(main.app)
    for page in ("/pricing", "/blog/analyser-ses-hooks-tiktok-shop", "/analyser-une-video-tiktok-shop"):
        r = client.get(page + "?ref=ABCD1234")
        assert "qeerah_ref=abcd1234" in r.headers.get("set-cookie", ""), page
    assert "qeerah_ref" not in client.get("/pricing?ref=<script>").headers.get("set-cookie", "")


def test_le_code_voyage_dans_la_facture():
    import main
    assert main._ref_de_facture({"subscription_details": {"metadata": {"ref": "abcd1234"}}}) == "abcd1234"
    assert main._ref_de_facture({"parent": {"subscription_details": {"metadata": {"ref": "x1y2z3w4"}}}}) == "x1y2z3w4"
    assert main._ref_de_facture({}) == ""


if __name__ == "__main__":
    tests = [(n, o) for n, o in sorted(globals().items())
             if n.startswith("test_") and callable(o)]
    reussis, echoues = 0, []
    for nom, fn in tests:
        try:
            fn()
            print(f"  ok    {nom}")
            reussis += 1
        except Exception as e:
            print(f"  ÉCHEC {nom}\n        {e!r}")
            echoues.append(nom)

    print(f"\n{reussis}/{len(tests)} tests passent.")
    if echoues:
        print("Échecs : " + ", ".join(echoues))
    raise SystemExit(1 if echoues else 0)
