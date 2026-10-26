"""Tests de la séquence e-mail d'essai v2 (essai_emails.py).

Aucune base ni clé requise : une fausse table Supabase en mémoire suffit.
Ce qui doit rester vrai :
  • chaque e-mail tombe dans sa fenêtre (heures depuis le début de l'essai) ;
  • +24 h se tait si SA vidéo est déjà analysée ; jour 3 dépend de la mission ;
  • une idée, UN lien (+ désinscription), objet en minuscules, sans « gratuit /
    offre / exclusif » ni « ! », signé « Aimeric — Qeerah », dans la langue du compte ;
  • le bilan n'affiche que des données réelles ;
  • MODE TEST par défaut : rien ne part, rien n'est marqué ;
  • abonnés, désinscrits et adresses de test exclus ; jamais deux fois le même.

Lancement :  venv/bin/python -m pytest test_essai_emails.py -v
"""
from __future__ import annotations

import asyncio
import os
import re
from datetime import datetime, timedelta, timezone

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")

import essai_emails

MAINTENANT = datetime(2026, 10, 26, 9, 0, tzinfo=timezone.utc)
LIENS = {k: "https://www.qeerah.com/e/x" for k in
         ("bienvenue", "h24", "j3_radar", "j3_feed", "j3_creation", "j6", "j7", "j10")}


# ── Fausse base ────────────────────────────────────────────────────────────
class _Req:
    def __init__(self, base, table):
        self.base, self.table, self.filtres = base, table, []
        self._ecriture = None

    def select(self, *_a, **_k): return self
    def order(self, *_a, **_k): return self
    def limit(self, *_a, **_k): return self
    def or_(self, *_a, **_k): return self
    def eq(self, col, val): self.filtres.append(lambda r: r.get(col) == val); return self
    def gte(self, col, val): self.filtres.append(lambda r: (r.get(col) or "") >= val); return self
    def insert(self, row): self._ecriture = row; return self
    def upsert(self, row): self._ecriture = row; return self

    def execute(self):
        lignes = self.base.db.setdefault(self.table, [])
        if self._ecriture is not None:
            lignes.append(dict(self._ecriture))
            return type("R", (), {"data": [self._ecriture], "count": None})()
        data = [r for r in lignes if all(f(r) for f in self.filtres)]
        return type("R", (), {"data": data, "count": len(data)})()


class FauxSupabase:
    def __init__(self, **tables): self.db = {k: list(v) for k, v in tables.items()}
    def table(self, nom): return _Req(self, nom)


def _user(email, heures_depuis_debut, **extra):
    fin = MAINTENANT - timedelta(hours=heures_depuis_debut) + timedelta(days=7)
    return {"email": email, "tier": "free", "trial_ends_at": fin.isoformat(), **extra}


def _run(sb, actif=False, envoyes=None):
    os.environ["ESSAI_EMAILS_ACTIFS"] = "1" if actif else "0"
    import email_service as es

    async def faux_send(to, sujet, html):
        if envoyes is not None:
            envoyes.append((to, sujet, html))
        return True
    es.email_service._send = faux_send
    return asyncio.run(essai_emails.run(sb, maintenant=MAINTENANT))


# ── Fenêtres ───────────────────────────────────────────────────────────────
def test_fenetres():
    def moment(h):
        fin = MAINTENANT - timedelta(hours=h) + timedelta(days=7)
        return essai_emails.moment_du(fin, MAINTENANT)
    assert moment(1) == "bienvenue"
    assert moment(30) == "h24"
    assert moment(60) is None
    assert moment(80) == "j3"
    assert moment(150) == "j6"
    assert moment(170) == "j7"       # juste après la fin de l'essai
    assert moment(220) == "j10"
    assert moment(250) is None       # ensuite, plus rien


def test_choix_selon_la_mission():
    pas_fait = {"etapes": [{"id": 2, "fait": False}], "terminee": False}
    fait = {"etapes": [{"id": 2, "fait": True}], "terminee": True}
    assert essai_emails.choisir("h24", pas_fait) == "h24"
    assert essai_emails.choisir("h24", fait) is None
    assert essai_emails.choisir("j3", pas_fait) == "j3_radar"
    assert essai_emails.choisir("j3", fait) == "j3_creation"


# ── Règles d'écriture ──────────────────────────────────────────────────────
ETAT = {"prochaine": 2, "terminee": False,
        "bilan": {"videos": 8, "leviers": 14, "accroches": 9, "meilleur": 74}}
VIDEO = {"video_url": "https://www.tiktok.com/@a/video/1", "oembed_author_name": "a", "views": 28403956}


def test_regles_d_ecriture_dans_toutes_les_langues():
    interdits = ("gratuit", "offre", "exclusif", "free", "offer", "exclusive", "grátis",
                 "gratis", "oferta", "kostenlos", "angebot", "l'ia", "notre ia", "booster")
    for lang in ("fr", "en", "pt-br", "es", "es-mx", "it", "de"):
        for cle in ("bienvenue", "h24", "j3_radar", "j3_feed", "j3_creation", "j6", "j7", "j10"):
            objet, _titre, corps = essai_emails.contenu(cle, ETAT, lang, LIENS, VIDEO)
            assert objet == objet.lower(), (lang, cle, objet)
            assert "!" not in objet and "!" not in corps, (lang, cle)
            texte = (objet + " " + corps).lower()
            for mot in interdits:
                assert mot not in texte, (lang, cle, mot)
            assert len(re.findall(r"<a href=", corps)) == 1, (lang, cle)
            assert "Aimeric — Qeerah" in corps


def test_le_bilan_n_affiche_que_le_reel():
    assert essai_emails.phrase_bilan({"videos": 8, "leviers": 14, "accroches": 9, "meilleur": 74}, "fr") == (
        "Pendant ton essai, tu as analysé 8 vidéos, identifié 14 leviers de vente et généré 9 accroches. "
        "Ta meilleure vidéo : 74/100.")
    assert essai_emails.phrase_bilan({"videos": 1}, "fr") == "Pendant ton essai, tu as analysé 1 vidéo."
    assert essai_emails.phrase_bilan({}, "fr") == ""
    _o, _t, corps = essai_emails.contenu("j7", {"bilan": {}}, "fr", LIENS)
    assert "Pendant ton essai" not in corps and "Qeerah Pro" in corps


def test_sans_video_du_pays_le_jour_3_renvoie_au_feed_radar():
    objet, _t, _c = essai_emails.contenu("j3_radar", ETAT, "fr", LIENS, None)
    assert objet == "ce qui vend en ce moment"
    assert essai_emails.chemin("j3_feed", ETAT) == "/app?onglet=feedradar"


def test_les_liens_menent_a_l_action():
    assert essai_emails.chemin("bienvenue", ETAT) == "/app?mission=2"
    assert essai_emails.chemin("h24", ETAT) == "/app?mission=2"
    assert essai_emails.chemin("j3_radar", ETAT, VIDEO).startswith("/app?analyser=https%3A%2F%2F")
    assert essai_emails.chemin("j7", ETAT) == "/abonnement/payer"
    lien = essai_emails.lien_suivi("https://www.qeerah.com", "j7", "/abonnement/payer", "a@b.fr")
    assert lien.startswith("https://www.qeerah.com/e/j7?r=%2Fabonnement%2Fpayer%3Fe%3Da%2540b.fr%26s%3D")


# ── Passage horaire ────────────────────────────────────────────────────────
def test_mode_test_par_defaut():
    os.environ.pop("ESSAI_EMAILS_ACTIFS", None)
    assert essai_emails.actif() is False


def test_mode_test_rien_ne_part_rien_n_est_marque():
    sb = FauxSupabase(users=[_user("a@qeerah.fr", 30)])
    envoyes = []
    r = _run(sb, actif=False, envoyes=envoyes)
    assert r["simulation"] and not envoyes
    assert not sb.db.get("email_log")


def test_envoi_reel_puis_jamais_deux_fois():
    sb = FauxSupabase(users=[_user("a@qeerah.fr", 30, lang="de")])
    envoyes = []
    _run(sb, actif=True, envoyes=envoyes)
    assert len(envoyes) == 1 and envoyes[0][1] == "wo deine zuschauer abspringen"
    assert sb.db["email_log"][0]["cle"] == "h24"
    _run(sb, actif=True, envoyes=envoyes)
    assert len(envoyes) == 1


def test_exclusions():
    sb = FauxSupabase(users=[
        _user("desinscrit@qeerah.fr", 30, marketing_opt_out=True),
        {**_user("abonne@qeerah.fr", 30), "tier": "pro"},
        _user("bot@example.com", 30),
    ])
    envoyes = []
    _run(sb, actif=True, envoyes=envoyes)
    assert not envoyes
