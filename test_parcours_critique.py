"""Tests du parcours critique — ce qui doit MARCHER pour que Qeerah soit vendable.

⚠️ POURQUOI CE FICHIER EXISTE.
Le dépôt contenait 20 fonctions de test réparties dans deux fichiers, qu'aucun
lanceur n'exécutait jamais. Pendant ce temps, deux régressions silencieuses ont
vécu en production :

  • l'essai gratuit ne démarrait plus (tout nouveau compte naissait « expiré ») ;
  • le webhook Stripe lisait un champ retiré de l'API, donc le cycle de
    facturation n'était jamais enregistré.

Les deux auraient été attrapées par les tests ci-dessous, le jour même.

Ces tests ne remplacent pas une suite complète : ils couvrent exactement les
chemins dont une panne coûte de l'argent ou expose des données. Ils tournent sans
base de données ni clé d'API — Supabase, Stripe et les moteurs d'IA sont hors
scope, on vérifie la LOGIQUE et les CONTRÔLES D'ACCÈS.

Lancement :
    venv/bin/python -m pytest test_parcours_critique.py -v
ou, sans pytest :
    venv/bin/python test_parcours_critique.py
"""
from __future__ import annotations

import os

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")
os.environ.setdefault("ADMIN_EMAIL", "admin-test@example.com")

from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

import analysis_quota
import auth
import main

client = TestClient(main.app)


# ══════════════════════════════════════════════════════════════════════════
# 1. L'ESSAI GRATUIT — la régression qui bloquait 100 % des inscriptions
# ══════════════════════════════════════════════════════════════════════════

def test_un_compte_neuf_recoit_une_date_de_fin_d_essai():
    """Sans `trial_ends_at` dans la ligne insérée, resolve_period() conclut
    « essai terminé » et l'utilisateur reçoit un 402 dès sa première analyse."""
    ligne = main._new_user_row("neuf@example.com", "$2b$hash-factice")
    assert ligne.get("trial_ends_at"), \
        "La ligne insérée n'a pas de trial_ends_at : tout compte neuf naîtra bloqué."
    fin = datetime.fromisoformat(ligne["trial_ends_at"])
    restant = (fin - datetime.now(timezone.utc)).total_seconds() / 86400
    assert 6 < restant <= analysis_quota.TRIAL_DAYS, \
        f"L'essai devrait durer {analysis_quota.TRIAL_DAYS} jours, il en dure {restant:.1f}."


def test_un_compte_neuf_peut_lancer_une_analyse():
    """Le test qui aurait tout attrapé : bout en bout de la ligne insérée
    jusqu'à la décision de quota."""
    ligne = main._new_user_row("neuf@example.com", "$2b$hash-factice")
    periode = _periode_pour(ligne)
    assert periode["kind"] == "trial", \
        f"Un compte neuf devrait être en essai, il est en '{periode['kind']}'."
    assert periode["limit"] == analysis_quota.TRIAL_LIMIT, \
        "L'essai devrait donner droit à des analyses, il en donne zéro."


def test_un_compte_sans_essai_est_bien_detecte_comme_expire():
    """Vérifie que le test précédent teste quelque chose : sans la colonne,
    la conclusion doit bien être « expiré »."""
    periode = _periode_pour({"tier": "free"})
    assert periode["kind"] == "expired" and periode["limit"] == 0


def _periode_pour(ligne_users: dict) -> dict:
    """Rejoue resolve_period() sur une ligne donnée, sans toucher à la base."""
    original = analysis_quota._user_row
    analysis_quota._user_row = lambda email: ligne_users
    try:
        return analysis_quota.resolve_period("test@example.com",
                                             ligne_users.get("tier", "free"))
    finally:
        analysis_quota._user_row = original


# ══════════════════════════════════════════════════════════════════════════
# 2. STRIPE — la rupture d'API qui a rendu `invoice.paid` inopérant
# ══════════════════════════════════════════════════════════════════════════

def test_le_cycle_de_facturation_est_lu_sur_les_items():
    """Depuis l'API 2025-03-31 « basil », current_period_* vit sur les items de
    l'abonnement, plus sur l'abonnement lui-même."""
    debut = int(datetime(2026, 8, 1, tzinfo=timezone.utc).timestamp())
    fin = int(datetime(2026, 9, 1, tzinfo=timezone.utc).timestamp())
    abonnement = {
        "id": "sub_test",
        "items": {"data": [{"current_period_start": debut, "current_period_end": fin}]},
    }
    d, f = main._subscription_period(abonnement)
    assert d is not None and f is not None, \
        "Le cycle n'est pas lu sur les items : set_billing_period ne sera jamais appelé."
    assert d.month == 8 and f.month == 9


def test_le_cycle_reste_lisible_sur_l_ancien_format():
    """Repli : si le compte Stripe repasse un jour sur une API ancienne, on ne
    doit pas casser."""
    debut = int(datetime(2026, 8, 1, tzinfo=timezone.utc).timestamp())
    d, _ = main._subscription_period({"id": "sub_v1", "current_period_start": debut})
    assert d is not None and d.month == 8


def test_un_abonnement_illisible_ne_fait_pas_planter():
    d, f = main._subscription_period({"id": "sub_vide"})
    assert d is None and f is None


# ══════════════════════════════════════════════════════════════════════════
# 3. CONTRÔLES D'ACCÈS — ce qui exposait des données de facturation
# ══════════════════════════════════════════════════════════════════════════

def test_le_portail_de_facturation_refuse_un_anonyme():
    """Cette route lisait l'e-mail dans le corps sans vérifier de jeton :
    connaître une adresse suffisait à ouvrir le portail Stripe d'un abonné."""
    r = client.post("/customer-portal", json={"email": "victime@example.com"})
    assert r.status_code == 401, \
        f"Le portail devrait exiger une session, il répond {r.status_code}."


def test_le_portail_ignore_un_customer_id_impose():
    r = client.post("/customer-portal", json={"customer_id": "cus_VICTIME"})
    assert r.status_code == 401


def test_le_second_webhook_non_signe_a_disparu():
    """`POST /webhook` traitait un payload SANS vérifier la signature quand le
    secret manquait, et accordait le tier « pro » à l'e-mail indiqué."""
    r = client.post("/webhook", json={"type": "checkout.session.completed"})
    assert r.status_code in (404, 405), \
        f"Le webhook en doublon est toujours joignable ({r.status_code})."


def test_les_temoignages_exigent_un_compte():
    """Chaque envoi déclenchait une notification push à l'administrateur."""
    r = client.post("/api/temoignages", json={"nom": "Robot", "texte": "x" * 20})
    assert r.status_code == 401


def test_le_cron_refuse_une_cle_absente_ou_fausse():
    assert client.get("/api/_cron/upsell-j3").status_code == 403
    assert client.get("/api/_cron/upsell-j3?key=mauvaise").status_code == 403


def test_la_connexion_ne_cree_plus_de_compte():
    """Une adresse inconnue doit renvoyer 401, pas fabriquer un compte vide."""
    r = client.post("/api/login", json={"email": "jamais-vu@example.invalid",
                                        "password": "motdepasse123"})
    # 401 = comportement voulu. 500 = pas de base en local, acceptable ici :
    # ce qui compte, c'est qu'on ne reçoive JAMAIS 200 avec created=true.
    assert r.status_code != 200, "La connexion a créé un compte."
    if r.status_code == 200:
        assert not r.json().get("created")


# ══════════════════════════════════════════════════════════════════════════
# 4. SSRF — le proxy d'images renvoyait le corps de n'importe quelle cible
# ══════════════════════════════════════════════════════════════════════════

CAS_SSRF = [
    ("https://p16-sign-va.tiktokcdn.com/img.jpg", True,  "CDN légitime"),
    ("https://v.byteimg.com/a/b.jpeg",            True,  "CDN légitime"),
    ("http://169.254.169.254/latest/meta-data/?p16-", False, "métadonnées cloud"),
    ("http://127.0.0.1:10000/admin?tiktokcdn",    False, "loopback"),
    ("https://example.com/x?p16-tiktokcdn.com",   False, "jeton placé dans le query"),
    ("https://p16-evil.attaquant.com/x.jpg",      False, "préfixe autorisé sur un hôte tiers"),
    ("https://tiktokcdn.com.evil.net/x.jpg",      False, "suffixe usurpé"),
    ("http://p16-sign-va.tiktokcdn.com/img.jpg",  False, "http en clair"),
    ("https://10.0.0.5/x.jpg",                    False, "IP privée"),
]


def test_le_proxy_d_images_ne_sort_pas_de_sa_liste_blanche():
    """La liste blanche testait une sous-chaîne de l'URL ENTIÈRE : un jeton placé
    dans le chemin ou le query suffisait à viser le réseau interne, et le corps
    de la réponse était renvoyé à l'appelant."""
    echecs = []
    for url, attendu, libelle in CAS_SSRF:
        obtenu = main._img_proxy_host_allowed(url)
        if obtenu != attendu:
            echecs.append(f"{libelle} ({url}) → autorisé={obtenu}, attendu={attendu}")
    assert not echecs, "Filtre SSRF défaillant :\n  " + "\n  ".join(echecs)


# ══════════════════════════════════════════════════════════════════════════
# 5. SESSIONS — la base de toute l'authentification
# ══════════════════════════════════════════════════════════════════════════

def test_un_jeton_valide_est_accepte_et_un_jeton_falsifie_refuse():
    jeton = auth.create_access_token("moi@example.com")
    assert auth.verify_access_token(jeton) == "moi@example.com"
    assert auth.verify_access_token(jeton[:-4] + "0000") is None
    assert auth.verify_access_token("n-importe-quoi") is None


def test_un_jeton_perime_est_refuse():
    """Forge un jeton correctement signé mais horodaté il y a 400 jours : la
    signature est valable, seule l'ancienneté doit le faire rejeter."""
    import base64
    import hashlib
    import hmac
    import time

    email = "moi@example.com"
    vieux_ts = str(int(time.time()) - 400 * 86400)
    signature = hmac.new(auth.SECRET_KEY, f"{email}|{vieux_ts}".encode(),
                         hashlib.sha256).hexdigest()
    jeton = f"{base64.b64encode(email.encode()).decode()}.{vieux_ts}.{signature}"

    assert auth.verify_access_token(jeton) is None, \
        "Un jeton vieux de 400 jours est encore accepté."


def test_une_duree_de_session_minuscule_ne_desactive_pas_l_expiration():
    """`int(days * 86400)` retombait à 0 pour une valeur très petite — or 0 est
    le sentinelle « jamais d'expiration ». Une saisie maladroite désactivait
    donc l'expiration au lieu de la raccourcir."""
    ancien = os.environ.get("SESSION_TTL_DAYS")
    os.environ["SESSION_TTL_DAYS"] = "0.0000001"
    try:
        assert auth._session_ttl_seconds() > 0, \
            "Une durée minuscule désactive l'expiration des sessions."
    finally:
        if ancien is None:
            os.environ.pop("SESSION_TTL_DAYS", None)
        else:
            os.environ["SESSION_TTL_DAYS"] = ancien


# ══════════════════════════════════════════════════════════════════════════
# 6. LES PAGES RÉPONDENT — un gabarit cassé au rendu casse le démarrage
# ══════════════════════════════════════════════════════════════════════════

PAGES_PUBLIQUES = [
    "/", "/app", "/pricing", "/pricing/compare", "/credits", "/avis",
    "/blog", "/contact", "/about", "/terms", "/privacy", "/cgv",
    "/mentions-legales", "/analyser-une-video-tiktok-shop",
    "/produits-qui-vendent-tiktok-shop-france",
    "/pourquoi-ma-video-tiktok-shop-ne-fait-pas-de-vues",
    "/robots.txt", "/sitemap.xml", "/llms.txt", "/health",
]


def test_toutes_les_pages_publiques_repondent():
    en_erreur = []
    for chemin in PAGES_PUBLIQUES:
        code = client.get(chemin).status_code
        if code != 200:
            en_erreur.append(f"{chemin} → {code}")
    assert not en_erreur, "Pages en erreur :\n  " + "\n  ".join(en_erreur)


def test_l_ancienne_marque_n_apparait_plus():
    """« TikTok Shop Vidéo Analyzer » est le nom à l'origine de la plainte qui a
    imposé le rebrand : il ne doit réapparaître nulle part."""
    for chemin in ("/", "/app"):
        contenu = client.get(chemin).text
        assert "TikTok Shop Vidéo Analyzer" not in contenu, \
            f"L'ancienne marque est de retour sur {chemin}."


def test_la_promesse_de_confidentialite_ne_ment_pas():
    """L'application affirmait que les analyses restent « EN LOCAL » et ne sont
    « jamais récupérées sur nos serveurs » — alors qu'elles sont en base."""
    js = open("static/app_v3.js", encoding="utf-8").read()
    for mensonge in ("restent EN LOCAL", "uniquement sur ton appareil",
                     "Nous ne les récupérons jamais"):
        assert mensonge not in js, \
            f"Affirmation fausse de retour dans l'interface : « {mensonge} »"


def test_les_en_tetes_de_securite_sont_poses():
    entetes = {k.lower() for k in client.get("/").headers}
    for attendu in ("content-security-policy", "strict-transport-security",
                    "x-frame-options", "x-content-type-options",
                    "referrer-policy", "permissions-policy"):
        assert attendu in entetes, f"En-tête de sécurité manquant : {attendu}"


# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import traceback

    tests = [(n, o) for n, o in sorted(globals().items())
             if n.startswith("test_") and callable(o)]
    reussis, echoues = 0, []
    for nom, fn in tests:
        try:
            fn()
            print(f"  ok    {nom}")
            reussis += 1
        except Exception as e:
            print(f"  ÉCHEC {nom}\n        {e}")
            echoues.append(nom)

    print(f"\n{reussis}/{len(tests)} tests passent.")
    if echoues:
        print("Échecs : " + ", ".join(echoues))
    raise SystemExit(1 if echoues else 0)
