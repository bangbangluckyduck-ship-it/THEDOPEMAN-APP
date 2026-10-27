"""Tests de l'aperçu rapide (visiteur sans compte) — 27/10/2026.

Ce qui doit rester vrai :
  • l'aperçu ne garde que ce que le visiteur voit, et refuse une réponse sans
    score ni verdict (l'appelant retombe alors sur le rapport complet) ;
  • le rapport complet reprend MOT POUR MOT l'aperçu déjà montré : rien ne
    change sous les yeux du visiteur après son inscription ;
  • le rattachement répond 202 tant que le rapport se rédige, le rend dès qu'il
    est prêt, et « expirée » s'il a échoué ou s'est perdu dans un redémarrage.

Aucune base, aucune clé d'IA : Supabase et les modèles sont simulés.
Lancement :  venv/bin/python -m pytest test_apercu.py -v
"""
from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime, timedelta, timezone

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

import pytest
from fastapi.testclient import TestClient

import ai_providers
import analyzer
import main
import mission
from auth import create_access_token

client = TestClient(main.app)

APERCU_BRUT = {
    "score_global": 80,
    "verdict": "La démonstration porte la vente.",
    "point_fort": "Accroche par la frustration",
    "point_a_ameliorer": "Aucun appel à l'action",
    "action_prioritaire": "Dis ton appel à l'action à 0:08, juste après la démonstration",
    "detection": {"produit": "Gourde", "prix_estime": "19€", "hook_type": "frustration", "hook_force": 8},
}


@pytest.fixture
def apercu(monkeypatch):
    monkeypatch.setattr(ai_providers, "text_complete", lambda *a, **k: json.dumps(APERCU_BRUT))
    return analyzer.synthesize_apercu({"produit": "Gourde"}, "transcript", lang="fr")


# ── Aperçu ─────────────────────────────────────────────────────────────────
def test_apercu_au_format_du_rapport(apercu):
    assert apercu["score_global"] == 80
    assert apercu["points_forts"] == ["Accroche par la frustration"]
    assert apercu["points_ameliorer"] == ["Aucun appel à l'action"]
    assert apercu["ameliorations_prioritaires"][0]["action"].startswith("Dis ton appel")
    p = main._partiel_anonyme({**apercu, "source": "url", "source_url": "u"}, "a" * 32)
    assert p["score_global"] == 80 and p["apercu_action"] == "Dis ton appel à l'action à 0:08,…"
    assert p["detection"]["produit"] == "Gourde"


def test_apercu_sans_score_refuse(monkeypatch):
    monkeypatch.setattr(ai_providers, "text_complete",
                        lambda *a, **k: json.dumps({**APERCU_BRUT, "score_global": None}))
    with pytest.raises(ValueError):
        analyzer.synthesize_apercu({}, None)


def test_apercu_le_prix_saisi_fait_autorite(monkeypatch):
    monkeypatch.setattr(ai_providers, "text_complete", lambda *a, **k: json.dumps(APERCU_BRUT))
    assert analyzer.synthesize_apercu({}, None, price="24,90 €")["detection"]["prix_estime"] == "24,90 €"


def test_apercu_lit_le_meme_prompt_que_le_rapport(monkeypatch):
    vus = []
    monkeypatch.setattr(ai_providers, "text_complete", lambda p, **k: vus.append(p) or json.dumps(APERCU_BRUT))
    analyzer.synthesize_apercu({"produit": "Gourde"}, "transcript", lang="fr")
    corps, *_ = analyzer._prompt_synthese({"produit": "Gourde"}, "transcript", None, None, None, None)
    assert vus[0].startswith(corps) and "APERÇU" in vus[0]


# ── Le rapport complet reprend l'aperçu ────────────────────────────────────
def test_le_rapport_reprend_l_apercu(apercu):
    rapport = {
        "score_global": 72, "verdict": "Autre verdict",
        "points_forts": ["Accroche directe", "Démo claire", "Prix visible"],
        "points_ameliorer": ["CTA tardif", "Aucun appel à l'action", "Fin abrupte"],
        "ameliorations_prioritaires": [{"rang": 1, "action": "Autre", "impact": "+ de clics"},
                                       {"rang": 2, "action": "Deux"}],
        "detection": {"produit": "Bouteille", "categorie_marche": "maison"},
    }
    analyzer._appliquer_imposes(rapport, apercu)
    assert rapport["score_global"] == 80 and rapport["verdict"] == APERCU_BRUT["verdict"]
    assert rapport["points_forts"] == ["Accroche par la frustration", "Démo claire", "Prix visible"]
    # recopiée plus bas par le modèle : pas de doublon
    assert rapport["points_ameliorer"] == ["Aucun appel à l'action", "Fin abrupte"]
    assert rapport["ameliorations_prioritaires"][0] == {
        "rang": 1, "action": APERCU_BRUT["action_prioritaire"], "impact": "+ de clics"}
    assert rapport["ameliorations_prioritaires"][1]["action"] == "Deux"
    assert rapport["detection"]["produit"] == "Gourde" and rapport["detection"]["categorie_marche"] == "maison"


def test_la_consigne_contient_l_apercu(apercu):
    bloc = analyzer._bloc_imposes(apercu)
    assert "MOT POUR MOT" in bloc and APERCU_BRUT["verdict"] in bloc and '"score_global": 80' in bloc


# ── Rattachement d'un rapport en rédaction ─────────────────────────────────
class _Requete:
    def __init__(self, base, cle=None, maj=None):
        self.base, self.cle, self.maj = base, cle, maj

    def select(self, *_a):
        return self

    def limit(self, _n):
        return self

    def eq(self, _col, val):
        self.cle = val
        return self

    def update(self, maj):
        self.maj = maj
        return self

    def upsert(self, ligne):
        self.base.lignes[ligne["cache_key"]] = dict(ligne)
        return self

    def execute(self):
        ligne = self.base.lignes.get(self.cle)
        if self.maj is not None and ligne:
            ligne.update(self.maj)
        return type("R", (), {"data": [ligne] if ligne else []})()


class FausseBase:
    def __init__(self):
        self.lignes = {}

    def table(self, _nom):
        return _Requete(self)


@pytest.fixture
def base(monkeypatch):
    b = FausseBase()
    monkeypatch.setattr(main, "supabase_client", b)
    monkeypatch.setattr(main, "_persist_sync_analysis", lambda *a, **k: None)
    monkeypatch.setattr(mission, "marquer", lambda *a, **k: None)
    monkeypatch.setattr(main, "usage_info", lambda u: {})
    monkeypatch.setenv("RATTACHER_ATTENTE_S", "0")
    return b


def _rattacher(anon_id):
    jeton = create_access_token("essai@example.com")
    return client.post("/api/analyse-anonyme/rattacher", json={"anon_id": anon_id},
                       headers={"Authorization": "Bearer " + jeton})


def _ligne(base, payload, il_y_a=timedelta(0)):
    anon_id = "c" * 32
    maintenant = datetime.now(timezone.utc)
    base.lignes[main._ANON_PREFIXE + anon_id] = {
        "cache_key": main._ANON_PREFIXE + anon_id,
        "payload": {"source": "url", "source_url": "u", "rattache_a": None,
                    "cree_le": (maintenant - il_y_a).isoformat(), **payload},
        "expires_at": (maintenant + timedelta(hours=40)).isoformat()}
    return anon_id


def test_rapport_en_redaction_202(base):
    assert _rattacher(_ligne(base, {"result": None, "en_cours": True})).status_code == 202


def test_rapport_perdu_dans_un_redemarrage_404(base):
    anon_id = _ligne(base, {"result": None, "en_cours": True}, il_y_a=timedelta(minutes=10))
    assert _rattacher(anon_id).status_code == 404


def test_rapport_en_echec_404(base):
    assert _rattacher(_ligne(base, {"result": None, "en_cours": False, "erreur": "x"})).status_code == 404


def test_rapport_pret_rendu_en_entier(base):
    r = _rattacher(_ligne(base, {"result": {"score_global": 80, "verdict": "V"}, "en_cours": False}))
    assert r.status_code == 200 and r.json()["score_global"] == 80 and r.json()["rattachee"] is True


def test_le_rapport_en_fond_est_depose(base, apercu, monkeypatch):
    anon_id = main._stocker_anonyme(None, source="url", source_url="u")
    assert base.lignes[main._ANON_PREFIXE + anon_id]["payload"]["en_cours"] is True
    recu = {}

    def faux_rapport(*a, imposes=None):
        recu["imposes"] = imposes
        return {"score_global": 80, "verdict": "V"}

    async def fausse_fin(result, **_k):
        return {**result, "fini": True}

    monkeypatch.setattr(main, "synthesize_analysis", faux_rapport)
    monkeypatch.setattr(main, "_finaliser_analyse_url", fausse_fin)
    ctx = dict(visual_result={}, transcript=None, market_context=None, product=None, tier="free",
               price=None, user_role=None, lang="fr", url="u", performance=None, cache_key=None,
               analysis_start=0.0, user={"valid": False})
    asyncio.run(main._terminer_rapport_anonyme(anon_id, apercu, **ctx))
    payload = base.lignes[main._ANON_PREFIXE + anon_id]["payload"]
    assert recu["imposes"] is apercu
    assert payload["en_cours"] is False and payload["result"]["fini"] is True


def test_le_rapport_en_fond_en_echec_est_signale(base, apercu, monkeypatch):
    anon_id = main._stocker_anonyme(None, source="url", source_url="u")

    def en_panne(*a, **k):
        raise RuntimeError("Claude indisponible")

    monkeypatch.setattr(main, "synthesize_analysis", en_panne)
    ctx = dict(visual_result={}, transcript=None, market_context=None, product=None, tier="free",
               price=None, user_role=None, lang="fr", url="u", performance=None, cache_key=None,
               analysis_start=0.0, user={"valid": False})
    asyncio.run(main._terminer_rapport_anonyme(anon_id, apercu, **ctx))
    payload = base.lignes[main._ANON_PREFIXE + anon_id]["payload"]
    assert payload["en_cours"] is False and "Claude indisponible" in payload["erreur"]
    assert _rattacher(anon_id).status_code == 404
