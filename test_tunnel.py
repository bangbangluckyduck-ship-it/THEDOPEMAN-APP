"""Tests du tunnel de vente — analyse sans compte, inscription, retour Google.

Aucune base, aucune clé d'IA : on vérifie ce qui ne doit jamais casser.
  • un visiteur sans compte ne reçoit QUE le score, le verdict, une force, une
    faiblesse et le début de la première action — rien d'autre ne quitte le
    serveur ;
  • le rattachement exige un compte et refuse un identifiant mal formé ;
  • le retour de Google ne peut viser qu'une page du site (pas de redirection
    ouverte), et l'ancien comportement (/app) reste le défaut.

Lancement :  venv/bin/python -m pytest test_tunnel.py -v
"""
from __future__ import annotations

import os

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

from fastapi.testclient import TestClient

import google_oauth
import main
from auth import create_access_token

client = TestClient(main.app)

RAPPORT = {
    "score_global": 72,
    "verdict": "La démonstration porte la vente.",
    "points_forts": ["Accroche directe", "Démo claire", "Prix visible"],
    "points_ameliorer": ["CTA tardif", "Son faible", "Fin abrupte"],
    "ameliorations_prioritaires": [{"rang": 1, "action": "Dis ton appel à l'action à 0:08, juste après la démonstration", "impact": "+ de clics"}],
    "recommendations_hooks": {"exemples_concrets": ["Accroche secrète 1", "Accroche secrète 2"]},
    "analyse_8_dimensions": {"hook": {"score": 80, "feedback": "Retour détaillé secret"}},
    "detection": {"produit": "Gourde", "prix_estime": "19€", "hook_type": "question", "hook_force": 7,
                  "categorie_marche": "maison"},
    "transcript": "Transcription complète secrète",
    "source": "url", "source_url": "https://www.tiktok.com/@a/video/1",
}


# ── Résultat partiel ───────────────────────────────────────────────────────
def test_le_partiel_ne_contient_que_le_promis():
    p = main._partiel_anonyme(RAPPORT, "a" * 32)
    assert p["partiel"] is True and p["usage"] == {"tracked": False}
    assert p["score_global"] == 72 and p["verdict"] == RAPPORT["verdict"]
    assert p["points_forts"] == ["Accroche directe"]
    assert p["points_ameliorer"] == ["CTA tardif"]
    assert p["apercu_action"] == "Dis ton appel à l'action à 0:08,…"
    texte = repr(p)
    for secret in ("secrète", "secret", "+ de clics", "Démo claire", "Son faible", "maison"):
        assert secret not in texte, secret


def test_le_partiel_tient_sans_stockage():
    # Sans Supabase, pas d'identifiant : le lien reste rattachable par le cache.
    sauve = main.supabase_client
    main.supabase_client = None
    try:
        p = main._reponse_anonyme(RAPPORT, source="url", source_url=RAPPORT["source_url"])
    finally:
        main.supabase_client = sauve
    assert p["anon_id"] is None and p["source_url"] == RAPPORT["source_url"]


def test_debut_de_phrase():
    assert main._debut_de_phrase("") == ""
    assert main._debut_de_phrase("Un deux trois") == "Un…"
    assert main._debut_de_phrase("un deux trois quatre cinq six sept huit") == "un deux trois quatre cinq six sept…"


# ── Rattachement ───────────────────────────────────────────────────────────
def test_rattacher_exige_un_compte():
    r = client.post("/api/analyse-anonyme/rattacher", json={"anon_id": "a" * 32})
    assert r.status_code == 401


def test_rattacher_refuse_un_identifiant_mal_forme():
    jeton = create_access_token("essai@example.com")
    r = client.post("/api/analyse-anonyme/rattacher", json={"anon_id": "../../users"},
                    headers={"Authorization": "Bearer " + jeton})
    assert r.status_code == 404


# ── Retour de Google ───────────────────────────────────────────────────────
def test_le_retour_google_reste_sur_le_site():
    for mauvais in ("//evil.com", "https://evil.com", "/\\evil.com", "/app#x", "javascript:alert(1)", ""):
        assert google_oauth.suite_du_state(google_oauth.make_state(mauvais)) is None, mauvais
    bon = "/en?rattacher=" + "b" * 32
    assert google_oauth.suite_du_state(google_oauth.make_state(bon)) == bon


def test_le_state_sans_suite_reste_valide():
    s = google_oauth.make_state()
    assert google_oauth.verify_state(s) and google_oauth.suite_du_state(s) is None


def test_un_state_falsifie_ne_donne_aucune_suite():
    s = google_oauth.make_state("/en")
    payload, sig = s.rsplit(".", 1)
    assert google_oauth.suite_du_state(payload + ".0" + sig[1:]) is None


# ── Liens des e-mails ──────────────────────────────────────────────────────
def test_le_clic_d_un_email_reste_sur_le_site():
    for mauvais in ("https://evil.com", "//evil.com", "/\evil.com"):
        r = client.get("/e/j7", params={"r": mauvais}, follow_redirects=False)
        assert r.status_code == 302 and r.headers["location"] == "/app", mauvais
    r = client.get("/e/h24", params={"r": "/app?mission=2"}, follow_redirects=False)
    assert r.headers["location"] == "/app?mission=2"


def test_un_lien_de_paiement_mal_signe_mene_aux_tarifs():
    r = client.get("/abonnement/payer", params={"e": "a@b.fr", "s": "faux"}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/pricing"
