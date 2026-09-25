"""Tests de l'entonnoir de conversion (entonnoir.py + POST /api/evt).

Ce qui doit rester vrai :
  • le navigateur ne peut envoyer QUE les événements de la liste blanche —
    compte créé et abonnement sont réservés au serveur ;
  • une IP ne peut pas gonfler les compteurs à volonté (plafond) ;
  • rien d'identifiant n'est stocké : ni IP, ni e-mail, seulement l'étape ;
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
    def __init__(self, db):
        self.db, self.filtres, self.ligne, self.compter = db, [], None, False

    def insert(self, ligne): self.ligne = ligne; return self
    def select(self, *_a, count=None): self.compter = count == "exact"; return self
    def eq(self, col, val): self.filtres.append(lambda r: r.get(col) == val); return self
    def gte(self, col, val): self.filtres.append(lambda r: r.get(col, "") >= val); return self
    def limit(self, *_a): return self

    def execute(self):
        if self.ligne is not None:
            self.db.append(self.ligne)
            return type("R", (), {"data": [self.ligne], "count": None})()
        n = sum(1 for r in self.db if all(f(r) for f in self.filtres))
        return type("R", (), {"data": [], "count": n})()


class FauxSupabase:
    def __init__(self): self.lignes = []
    def table(self, _nom): return _Req(self.lignes)


def test_rien_d_identifiant_n_est_stocke():
    sb = FauxSupabase()
    entonnoir.enregistrer(sb, "cta_clic")
    assert set(sb.lignes[0]) == {"page", "timestamp"}
    assert sb.lignes[0]["page"] == "evt:cta_clic"


def test_taux_de_passage():
    sb = FauxSupabase()
    for cle, n in (("accueil_vue", 200), ("cta_clic", 50), ("analyse_lancee", 40),
                   ("analyse_terminee", 30), ("compte_cree", 6)):
        for _ in range(n):
            entonnoir.enregistrer(sb, cle)
    t = {m["cle"]: m for m in entonnoir.tableau(sb, 30)["marches"]}
    assert t["accueil_vue"]["taux"] is None                # première marche
    assert t["cta_clic"]["taux"] == 25.0
    assert t["compte_cree"]["taux"] == 20.0
    assert t["compte_cree"]["depuis_debut"] == 3.0
    assert t["abonnement"]["total"] == 0 and t["abonnement"]["taux"] is None  # rien avant → pas de taux


def test_le_serveur_seul_compte_inscription_et_paiement():
    assert "compte_cree" not in entonnoir.DEPUIS_NAVIGATEUR
    assert "abonnement" not in entonnoir.DEPUIS_NAVIGATEUR
    cles = [c for c, _ in entonnoir.ETAPES] + [c for c, _ in entonnoir.ANNEXES]
    assert entonnoir.DEPUIS_NAVIGATEUR <= set(cles)


def test_route_evt_liste_blanche_et_plafond():
    client = TestClient(main.app)
    main._EVT_PAR_IP.clear()
    assert client.post("/api/evt", json={"e": "compte_cree"}).status_code == 400
    assert client.post("/api/evt", json={"e": "n_importe_quoi"}).status_code == 400
    assert client.post("/api/evt", json={"e": "cta_clic"}).status_code == 200
    codes = [client.post("/api/evt", json={"e": "cta_clic"}).status_code for _ in range(main._EVT_MAX + 5)]
    assert 429 in codes
    main._EVT_PAR_IP.clear()
