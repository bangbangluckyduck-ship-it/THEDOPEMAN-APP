"""Signature des sessions (audit sécurité du 2026-11-12, point S2).

- APP_SIGNING_SECRET est obligatoire : plus de repli sur la clé publique Supabase.
- L'ancien format de jeton v1 (sans horodatage, donc sans expiration) est refusé.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import importlib
import os
import sys

import pytest

SECRET = "secret-de-test-non-production-assez-long-pour-32"


def _charger_auth(monkeypatch, **env):
    for k in ("APP_SIGNING_SECRET", "SUPABASE_ANON_KEY"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    sys.modules.pop("auth", None)
    return importlib.import_module("auth")


def test_refuse_de_demarrer_sans_secret_dedie(monkeypatch):
    # Avant : la clé anon (publique) servait de repli et l'app démarrait quand même.
    with pytest.raises(RuntimeError, match="APP_SIGNING_SECRET"):
        _charger_auth(monkeypatch, SUPABASE_ANON_KEY="cle-anon-publique")


def test_refuse_un_secret_egal_a_la_cle_publique(monkeypatch):
    with pytest.raises(RuntimeError, match="SUPABASE_ANON_KEY"):
        _charger_auth(monkeypatch, APP_SIGNING_SECRET="meme-valeur", SUPABASE_ANON_KEY="meme-valeur")


def test_session_v2_valide(monkeypatch):
    auth = _charger_auth(monkeypatch, APP_SIGNING_SECRET=SECRET)
    jeton = auth.create_access_token("client@exemple.fr")
    assert auth.verify_access_token(jeton) == "client@exemple.fr"


def test_jeton_signe_avec_la_cle_anon_refuse(monkeypatch):
    auth = _charger_auth(monkeypatch, APP_SIGNING_SECRET=SECRET, SUPABASE_ANON_KEY="cle-anon-publique")
    # Un attaquant qui connaît la clé anon forge un jeton v2 pour l'admin :
    ts = "9999999999"
    email = "admin@exemple.fr"
    sig = hmac.new(b"cle-anon-publique", f"{email}|{ts}".encode(), hashlib.sha256).hexdigest()
    jeton = f"{base64.b64encode(email.encode()).decode()}.{ts}.{sig}"
    assert auth.verify_access_token(jeton) is None


def test_ancien_jeton_v1_refuse_meme_bien_signe(monkeypatch):
    auth = _charger_auth(monkeypatch, APP_SIGNING_SECRET=SECRET)
    email = "client@exemple.fr"
    sig = hmac.new(SECRET.encode(), email.encode(), hashlib.sha256).hexdigest()
    jeton_v1 = f"{base64.b64encode(email.encode()).decode()}.{sig}"
    assert auth.verify_access_token(jeton_v1) is None


@pytest.fixture(autouse=True, scope="module")
def _restaurer_auth():
    # Les autres fichiers de test importent auth avec leur propre secret : on repart propre.
    yield
    sys.modules.pop("auth", None)
    os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
