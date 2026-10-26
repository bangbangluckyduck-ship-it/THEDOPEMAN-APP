"""Tests de la fidélisation (fidelisation.py, hebdo.py) — sans base ni Stripe.

Ce qui doit rester vrai :
  • un paiement échoué garde l'accès jusqu'à la prochaine relance Stripe et
    pose le bandeau ; un paiement réglé l'enlève ;
  • la pause d'un mois part de la fin de la période payée ;
  • la raison de départ est facultative et limitée aux choix proposés ;
  • l'e-mail hebdo : abonnés et anciens essais seulement, un seul lien, aucun
    « pourquoi » inventé, mode test par défaut, désinscription de l'hebdo seul.

Lancement :  venv/bin/python -m pytest test_fidelisation.py -v
"""
from __future__ import annotations

import asyncio
import os
import re
from datetime import datetime, timedelta, timezone

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

import fidelisation
import hebdo

MAINTENANT = datetime(2026, 10, 26, 8, 0, tzinfo=timezone.utc)


class _Req:
    def __init__(self, base, table):
        self.base, self.table, self.filtres, self._maj, self._ins = base, table, [], None, None

    def select(self, *_a, **_k): return self
    def order(self, *_a, **_k): return self
    def limit(self, *_a, **_k): return self
    def or_(self, *_a, **_k): return self
    def eq(self, col, val): self.filtres.append(lambda r: r.get(col) == val); return self
    def gte(self, col, val): self.filtres.append(lambda r: (r.get(col) or "") >= val); return self
    def update(self, champs): self._maj = champs; return self
    def insert(self, ligne): self._ins = ligne; return self
    def upsert(self, ligne): self._ins = ligne; return self

    def execute(self):
        lignes = self.base.db.setdefault(self.table, [])
        if self._ins is not None:
            lignes.append(dict(self._ins))
            return type("R", (), {"data": [self._ins]})()
        data = [r for r in lignes if all(f(r) for f in self.filtres)]
        if self._maj is not None:
            for r in data:
                r.update(self._maj)
        return type("R", (), {"data": data})()


class FauxSupabase:
    def __init__(self, **tables): self.db = {k: [dict(r) for r in v] for k, v in tables.items()}
    def table(self, nom): return _Req(self, nom)


# ── Paiement échoué ────────────────────────────────────────────────────────
def test_paiement_echoue_garde_l_acces_et_pose_le_bandeau():
    sb = FauxSupabase(users=[{"email": "a@qeerah.fr", "tier": "pro", "tier_expiry": "2026-10-26"}])
    relance = int((MAINTENANT + timedelta(days=3)).timestamp())
    assert fidelisation.paiement_echoue(sb, {"customer_email": "A@qeerah.fr", "next_payment_attempt": relance})
    u = sb.db["users"][0]
    assert u["tier_expiry"] == (MAINTENANT + timedelta(days=4)).date().isoformat()
    assert u["paiement_en_retard_depuis"]
    assert fidelisation.etat(sb, "a@qeerah.fr")["paiement_en_retard"] is True
    fidelisation.paiement_regle(sb, "a@qeerah.fr")
    assert fidelisation.etat(sb, "a@qeerah.fr")["paiement_en_retard"] is False


def test_abonnement_modifie_synchronise_la_pause():
    sb = FauxSupabase(users=[{"email": "a@qeerah.fr"}])
    fin = int((datetime.now(timezone.utc) + timedelta(days=20)).timestamp())
    fidelisation.abonnement_modifie(sb, {"customer_email": "a@qeerah.fr", "status": "active",
                                         "pause_collection": {"behavior": "void", "resumes_at": fin}})
    assert fidelisation.etat(sb, "a@qeerah.fr")["pause_fin"]
    fidelisation.abonnement_modifie(sb, {"customer_email": "a@qeerah.fr", "status": "active", "pause_collection": None})
    assert fidelisation.etat(sb, "a@qeerah.fr")["pause_fin"] is None


def test_pause_un_mois_apres_la_periode_payee(monkeypatch):
    fin_periode = int((MAINTENANT + timedelta(days=12)).timestamp())
    appels = {}
    monkeypatch.setattr(fidelisation.stripe, "api_key", "sk_test_x")
    monkeypatch.setattr(fidelisation.stripe.Subscription, "retrieve",
                        lambda sid: {"id": sid, "current_period_end": fin_periode})
    monkeypatch.setattr(fidelisation.stripe.Subscription, "modify",
                        lambda sid, **k: appels.update(k))
    sb = FauxSupabase(users=[{"email": "a@qeerah.fr", "subscription_id": "sub_1"}])
    r = fidelisation.mettre_en_pause(sb, "a@qeerah.fr")
    assert r["ok"] and appels["pause_collection"]["behavior"] == "void"
    assert appels["pause_collection"]["resumes_at"] == fin_periode + 30 * 86400


def test_raison_facultative_et_bornee():
    sb = FauxSupabase()
    assert fidelisation.enregistrer_raison(sb, "a@qeerah.fr", "trop_cher")
    assert not fidelisation.enregistrer_raison(sb, "a@qeerah.fr", "<script>")
    assert sb.db["cancel_feedback"] == [{"email": "a@qeerah.fr", "raison": "trop_cher", "detail": None}]


# ── E-mail hebdo ───────────────────────────────────────────────────────────
VIDEOS = [{"video_url": "https://www.tiktok.com/@a/video/1", "oembed_author_name": "a", "views": 1200000,
           "region": "FR", "collected_at": (MAINTENANT - timedelta(days=2)).isoformat()},
          {"video_url": "https://www.tiktok.com/@b/video/2", "oembed_author_name": "b", "views": 900000,
           "region": "FR", "collected_at": (MAINTENANT - timedelta(days=3)).isoformat()}]


def test_hebdo_un_seul_lien_et_pas_de_pourquoi_invente():
    videos = [dict(v, pourquoi=None) for v in VIDEOS]
    videos[0]["pourquoi"] = "La démonstration commence dès la première seconde."
    objet, corps = hebdo.contenu(videos, "fr", True, "https://www.qeerah.com/e/hebdo")
    assert objet == "ce qui vend cette semaine"
    assert len(re.findall(r"<a href=", corps)) == 1
    assert "Pourquoi elle vend : La démonstration" in corps
    assert "Analyse-la pour voir pourquoi elle vend." in corps


def test_hebdo_destinataires_et_mode_test():
    sb = FauxSupabase(
        users=[{"email": "abonne@qeerah.fr", "tier": "pro"},
               {"email": "ancien@qeerah.fr", "tier": "free", "trial_ends_at": (MAINTENANT - timedelta(days=10)).isoformat()},
               {"email": "essai@qeerah.fr", "tier": "free", "trial_ends_at": (MAINTENANT + timedelta(days=3)).isoformat()},
               {"email": "coupe@qeerah.fr", "tier": "pro", "hebdo_opt_out": True}],
        feed_radar_videos=VIDEOS)
    comptes = {u["email"]: u["abonne"] for u in hebdo._destinataires(sb, MAINTENANT)}
    assert comptes == {"abonne@qeerah.fr": True, "ancien@qeerah.fr": False, "coupe@qeerah.fr": True}

    os.environ.pop("HEBDO_ACTIF", None)
    envoyes = []
    import email_service as es

    async def faux_send(to, sujet, html):
        envoyes.append(to)
        return True
    es.email_service._send = faux_send
    r = asyncio.run(hebdo.run(sb, maintenant=MAINTENANT))
    assert r["simulation"] and not envoyes          # mode test : rien ne part

    os.environ["HEBDO_ACTIF"] = "1"
    try:
        asyncio.run(hebdo.run(sb, maintenant=MAINTENANT))
        asyncio.run(hebdo.run(sb, maintenant=MAINTENANT))   # même semaine : pas de doublon
    finally:
        os.environ.pop("HEBDO_ACTIF", None)
    assert sorted(envoyes) == ["abonne@qeerah.fr", "ancien@qeerah.fr"]


def test_desinscription_de_l_hebdo_seul():
    from fastapi.testclient import TestClient
    import main
    from auth import make_unsubscribe_token
    sb = FauxSupabase(users=[{"email": "a@qeerah.fr"}])
    sauve = main.supabase_client
    main.supabase_client = sb
    try:
        r = TestClient(main.app).get("/unsubscribe", params={
            "e": "a@qeerah.fr", "s": make_unsubscribe_token("a@qeerah.fr"), "type": "hebdo"})
    finally:
        main.supabase_client = sauve
    assert "plus l'e-mail de la semaine" in r.text
    assert sb.db["users"][0] == {"email": "a@qeerah.fr", "hebdo_opt_out": True}
