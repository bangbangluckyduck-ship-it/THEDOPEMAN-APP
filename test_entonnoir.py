"""Tests de l'entonnoir de conversion (entonnoir.py + POST /api/evt).

Ce qui doit rester vrai :
  • le navigateur ne peut envoyer QUE la visite et les clics — analyses,
    inscriptions, étapes de mission et paiements sont réservés au serveur ;
  • une IP ne peut pas gonfler les compteurs à volonté (plafond) ;
  • rien d'identifiant n'est stocké : ni IP, ni e-mail — l'événement, la
    langue et un détail court (méthode, mensuel/annuel, clé d'e-mail) ;
  • sans la table funnel_events, repli sur visitor_logs ; l'historique sous
    les anciens noms reste compté ;
  • le taux de passage se calcule sur la marche précédente.

Lancement :  venv/bin/python -m pytest test_entonnoir.py -v
"""
from __future__ import annotations

import os

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

from fastapi.testclient import TestClient

import entonnoir
import main


class _Req:
    def __init__(self, base, table):
        self.base, self.table, self.filtres, self.ligne, self.compter = base, table, [], None, False

    def insert(self, ligne): self.ligne = ligne; return self
    def select(self, *_a, count=None): self.compter = count == "exact"; return self
    def eq(self, col, val): self.filtres.append(lambda r: r.get(col) == val); return self
    def gte(self, col, val): self.filtres.append(lambda r: r.get(col, "") >= val); return self
    def limit(self, *_a): return self

    def execute(self):
        if self.table in self.base.absentes:
            raise RuntimeError(f'relation "{self.table}" does not exist')
        lignes = self.base.db.setdefault(self.table, [])
        if self.ligne is not None:
            # created_at : valeur par défaut que la base pose sur funnel_events.
            extra = {"created_at": "2099-01-01T00:00:00+00:00"} if self.table == "funnel_events" else {}
            lignes.append({**self.ligne, **extra})
            return type("R", (), {"data": [self.ligne], "count": None})()
        data = [r for r in lignes if all(f(r) for f in self.filtres)]
        return type("R", (), {"data": data, "count": len(data)})()


class FauxSupabase:
    def __init__(self, absentes=(), **tables):
        self.db = {k: list(v) for k, v in tables.items()}
        self.absentes = set(absentes)

    def table(self, nom): return _Req(self, nom)


def test_rien_d_identifiant_n_est_stocke():
    sb = FauxSupabase(users=[{"email": "a@qeerah.fr", "lang": "de"}])
    entonnoir.enregistrer(sb, "inscription", detail="google", email="a@qeerah.fr")
    ligne = sb.db["funnel_events"][0]
    assert {k: ligne[k] for k in ("evenement", "lang", "detail")} == {
        "evenement": "inscription", "lang": "de", "detail": "google"}
    assert "a@qeerah.fr" not in repr(ligne)


def test_langue_inconnue_ignoree_et_repli_sans_table():
    sb = FauxSupabase(absentes={"funnel_events"})
    assert entonnoir.enregistrer(sb, "visite_accueil", lang="xx")
    assert set(sb.db["visitor_logs"][0]) == {"page", "timestamp"}
    assert sb.db["visitor_logs"][0]["page"] == "evt:visite_accueil"


def test_taux_de_passage_et_historique_sous_les_anciens_noms():
    sb = FauxSupabase(visitor_logs=[{"page": "evt:accueil_vue", "timestamp": "2099-01-01"}] * 150)
    for cle, n in (("visite_accueil", 50), ("analyse_anonyme_lancee", 50), ("resultat_affiche", 40),
                   ("clic_debloquer", 20), ("inscription", 6)):
        for _ in range(n):
            entonnoir.enregistrer(sb, cle)
    t = {m["cle"]: m for m in entonnoir.tableau(sb, 30)["marches"]}
    assert t["visite_accueil"]["total"] == 200 and t["visite_accueil"]["taux"] is None
    assert t["analyse_anonyme_lancee"]["taux"] == 25.0
    assert t["inscription"]["taux"] == 30.0
    assert t["inscription"]["depuis_debut"] == 3.0
    assert t["abonnement"]["total"] == 0 and t["abonnement"]["taux"] is None


def test_le_serveur_seul_compte_ce_qui_est_certain():
    for cle in ("inscription", "abonnement", "analyse_anonyme_lancee", "resultat_affiche",
                "mission_etape_1", "checkout_ouvert", "paiement_echoue"):
        assert cle not in entonnoir.DEPUIS_NAVIGATEUR
    cles = [c for c, _ in entonnoir.ETAPES] + [c for c, _ in entonnoir.ANNEXES]
    assert entonnoir.DEPUIS_NAVIGATEUR <= set(cles)


def test_route_evt_liste_blanche_langue_et_plafond():
    client = TestClient(main.app)
    main._EVT_PAR_IP.clear()
    assert client.post("/api/evt", json={"e": "inscription"}).status_code == 400
    assert client.post("/api/evt", json={"e": "n_importe_quoi"}).status_code == 400
    assert client.post("/api/evt", json={"e": "cta_clic", "l": "pt-br"}).status_code == 200
    assert client.post("/api/evt", json={"e": "accueil_vue"}).status_code == 200   # ancien script
    codes = [client.post("/api/evt", json={"e": "cta_clic"}).status_code for _ in range(main._EVT_MAX + 5)]
    assert 429 in codes
    main._EVT_PAR_IP.clear()
