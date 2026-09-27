"""Seul ADMIN_EMAIL est administrateur — un palier « admin » en base ne suffit pas.

Des comptes de test portant le palier « admin » avaient leur mot de passe publié
dans le dépôt (public) : la règle « tier == admin ⇒ administrateur » ouvrait
/dope-admin à n'importe qui. Ce test empêche qu'elle revienne.

Lancement :  venv/bin/python -m pytest test_securite_admin.py -v
"""
from __future__ import annotations

import os
import re

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

import auth


def test_palier_admin_seul_ne_suffit_pas():
    assert auth.is_admin({"valid": True, "email": "bot-admin@tts-test.com", "tier": "admin"}) is False


def test_admin_email_reste_administrateur():
    assert auth.is_admin({"valid": True, "email": "admin-test@example.com", "tier": "admin", "is_admin": True}) is True


def test_plus_aucune_verification_par_palier_dans_le_code():
    for fichier in ("auth.py", "main.py", "admin_routes.py"):
        code = open(fichier, encoding="utf-8").read()
        assert not re.search(r'tier"\)\s*==\s*"admin"', code), f"{fichier} : contrôle par palier « admin » réintroduit"


def test_aucun_mot_de_passe_de_robot_dans_le_depot():
    for fichier in ("setup_test_bots.py", "test_suite.py", "comprehensive_test_suite.py"):
        assert not re.search(r"Bot[A-Za-z]+Pass123!", open(fichier, encoding="utf-8").read()), fichier
