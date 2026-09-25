"""Tests de la séquence e-mail d'essai (essai_emails.py) et de la mission.

Aucune base ni clé requise : une fausse table Supabase en mémoire suffit.
Ce qui doit rester vrai :
  • chaque e-mail tombe dans sa fenêtre de jours (J2 / J5 / J7) ;
  • J2 / J5 poussent la PROCHAINE étape non faite, et se taisent si la mission
    est accomplie ; seul J7 parle de l'offre, après le bilan ;
  • mode simulation par défaut : rien ne part sans ESSAI_EMAILS_ACTIFS=1 ;
  • désinscrits et adresses de test exclus ; jamais deux fois la même étape.

Lancement :  venv/bin/python -m pytest test_essai_emails.py -v
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime, timedelta, timezone

os.environ.setdefault("APP_SIGNING_SECRET", "secret-de-test-non-production")

import essai_emails
import mission

MAINTENANT = datetime(2026, 9, 25, 9, 0, tzinfo=timezone.utc)


# ── Fausse base ────────────────────────────────────────────────────────────
class _Req:
    def __init__(self, db, table):
        self.db, self.table, self.filtres, self._upsert = db, table, [], None

    def select(self, *_a, **_k): return self
    def order(self, *_a, **_k): return self
    def limit(self, *_a, **_k): return self
    def eq(self, col, val): self.filtres.append(lambda r: r.get(col) == val); return self
    def gte(self, col, val): self.filtres.append(lambda r: (r.get(col) or "") >= val); return self
    def upsert(self, row): self._upsert = row; return self

    def execute(self):
        lignes = self.db.setdefault(self.table, [])
        if self._upsert is not None:
            lignes.append(self._upsert)
            return type("R", (), {"data": [self._upsert]})()
        data = [r for r in lignes if all(f(r) for f in self.filtres)]
        return type("R", (), {"data": sorted(data, key=lambda r: r.get("created_at", ""))})()


class FauxSupabase:
    def __init__(self, **tables): self.db = {k: list(v) for k, v in tables.items()}
    def table(self, nom): return _Req(self.db, nom)


def _user(email, jours_depuis_debut, **extra):
    fin = MAINTENANT - timedelta(days=jours_depuis_debut) + timedelta(days=7)
    return {"email": email, "tier": "free", "trial_ends_at": fin.isoformat(), **extra}


def _run(sb, actif=False, envoyes=None):
    os.environ["ESSAI_EMAILS_ACTIFS"] = "1" if actif else ""
    import email_service as es

    async def faux_send(to, sujet, html):
        if envoyes is not None: envoyes.append((to, sujet, html))
        return True
    es.email_service._send = faux_send
    return asyncio.run(essai_emails.run(sb, maintenant=MAINTENANT))


# ── Fenêtres ───────────────────────────────────────────────────────────────
def test_fenetres_de_jours():
    def due(jours):
        fin = MAINTENANT - timedelta(days=jours) + timedelta(days=7)
        return essai_emails.etape_due(fin, MAINTENANT)
    assert due(1) is None
    assert due(2.5) == "j2"
    assert due(3.5) == "j2"
    assert due(4.5) is None
    assert due(5.2) == "j5"
    assert due(6.5) == "j7"      # veille de la fin
    assert due(7.5) == "j7"      # juste après la fin
    assert due(9) is None


# ── Mission ────────────────────────────────────────────────────────────────
def test_mission_deduite_des_tables():
    sb = FauxSupabase(
        analysis_jobs=[{"email": "a@qeerah.fr", "status": "done", "created_at": "2026-09-20T10:00:00+00:00"},
                       {"email": "a@qeerah.fr", "status": "done", "created_at": "2026-09-24T10:00:00+00:00"}],
        script_generations=[{"email": "a@qeerah.fr", "created_at": "2026-09-21T10:00:00+00:00"}],
        user_favorites=[{"email": "a@qeerah.fr", "item_type": "script", "created_at": "2026-09-22T10:00:00+00:00"}],
    )
    e = mission.etat(sb, "a@qeerah.fr")
    assert [x["fait"] for x in e["etapes"]] == [True, True, True, True]
    assert e["prochaine"] is None
    # Une analyse AVANT le script gardé ne valide pas l'étape 4.
    sb.db["analysis_jobs"].pop()
    assert mission.etat(sb, "a@qeerah.fr")["prochaine"] == 4


# ── Contenus ───────────────────────────────────────────────────────────────
def test_j2_pousse_la_prochaine_etape_sans_parler_de_prix():
    etat = {"prochaine": 2, "terminees": 1, "bilan": {}}
    objet, _titre, corps = essai_emails.contenu("j2", etat, "https://www.qeerah.com")
    assert "ton produit" in objet.lower()
    assert "/scripts?mission=2" in corps
    assert "€" not in corps and "Qeerah Pro" not in corps


def test_j5_se_tait_si_mission_accomplie():
    assert essai_emails.contenu("j5", {"prochaine": None, "terminees": 4}, "https://x") is None


def test_j7_bilan_puis_offre():
    etat = {"bilan": {"videos_decryptees": 3, "generations_scripts": 1, "scripts_gardes": 1}}
    objet, _t, corps = essai_emails.contenu("j7", etat, "https://www.qeerah.com")
    assert objet == "Ton essai en chiffres"
    assert corps.index("vidéos décryptées") < corps.index("Passer à Qeerah Pro")


def test_aucun_mot_interdit():
    for etape, etat in (("j2", {"prochaine": 1, "terminees": 0}), ("j5", {"prochaine": 3, "terminees": 2}),
                        ("j7", {"bilan": {"videos_decryptees": 1}})):
        _o, _t, corps = essai_emails.contenu(etape, etat, "https://x")
        bas = corps.lower()
        for mot in ("l'ia", "booster", "propulse", "vitesse supérieure", "profite", "vous "):
            assert mot not in bas, (etape, mot)


# ── Passage quotidien ──────────────────────────────────────────────────────
def test_simulation_par_defaut_rien_ne_part():
    sb = FauxSupabase(users=[_user("a@qeerah.fr", 2.5)])
    envoyes = []
    r = _run(sb, actif=False, envoyes=envoyes)
    assert r["simulation"] is True and r["sent"] == 0 and envoyes == []
    assert r["par_etape"] == {"j2": 1}
    assert not sb.db.get("market_cache")          # rien de marqué en simulation


def test_envoi_reel_exclusions_et_pas_de_doublon():
    sb = FauxSupabase(users=[
        _user("a@qeerah.fr", 2.5),
        _user("desinscrit@qeerah.fr", 2.5, marketing_opt_out=True),
        _user("bot-1@example.com", 2.5),
    ])
    envoyes = []
    r = _run(sb, actif=True, envoyes=envoyes)
    assert [e[0] for e in envoyes] == ["a@qeerah.fr"]
    assert r["sent"] == 1
    assert "/unsubscribe?e=" in envoyes[0][2]     # lien de désinscription signé
    # Second passage le même jour : déjà envoyé → rien.
    envoyes.clear()
    r2 = _run(sb, actif=True, envoyes=envoyes)
    assert envoyes == [] and r2["sent"] == 0
