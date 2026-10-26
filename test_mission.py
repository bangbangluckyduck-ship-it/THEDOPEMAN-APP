"""Tests de la mission d'essai v2 (mission.py) — aucune base requise.

Ce qui doit rester vrai :
  • l'étape « analyse » se lit sur `analysis_jobs.user_email` (l'ancienne version
    lisait une colonne `email` inexistante : l'étape n'était jamais validée) ;
  • l'étape 2 n'est validée que par une analyse signalée comme SA vidéo ;
  • une étape 2 demandée avant l'étape 1 valide l'étape 1 ;
  • les dates déjà posées ne sont jamais réécrites ;
  • le comparatif sort 2 ou 3 écarts réels, sans appel d'IA ;
  • le bilan n'affiche que des données réelles ;
  • sans la table `trial_mission`, la mission retombe sur les tables existantes.

Lancement :  venv/bin/python -m pytest test_mission.py -v
"""
from __future__ import annotations

import mission

EMAIL = "a@qeerah.fr"


# ── Fausse base ────────────────────────────────────────────────────────────
class _Req:
    def __init__(self, base, table):
        self.base, self.table, self.filtres = base, table, []
        self._insert = self._update = None
        self._count = False

    def select(self, *_a, count=None, **_k):
        self._count = count == "exact"
        return self

    def order(self, *_a, **_k): return self
    def limit(self, *_a, **_k): return self
    def eq(self, col, val): self.filtres.append(lambda r: r.get(col) == val); return self
    def insert(self, row): self._insert = row; return self
    def update(self, row): self._update = row; return self

    def execute(self):
        if self.table in self.base.absentes:
            raise RuntimeError(f'relation "{self.table}" does not exist')
        lignes = self.base.db.setdefault(self.table, [])
        if self._insert is not None:
            lignes.append(dict(self._insert))
            return type("R", (), {"data": [self._insert], "count": None})()
        data = [r for r in lignes if all(f(r) for f in self.filtres)]
        if self._update is not None:
            for r in data:
                r.update(self._update)
        return type("R", (), {"data": data, "count": len(data) if self._count else None})()


class FauxSupabase:
    def __init__(self, absentes=(), **tables):
        self.db = {k: [dict(r) for r in v] for k, v in tables.items()}
        self.absentes = set(absentes)

    def table(self, nom): return _Req(self, nom)


def _analyse(score, **dims):
    return {
        "score_global": score,
        "detection": {"produit": "Gourde isotherme", "hook_force": 7, "hook_type": "question"},
        "cta_audio": {"present": True, "timestamp_seconds": 8},
        "analyse_8_dimensions": {k: {"score": v, "feedback": f"Pourquoi {k}"} for k, v in dims.items()},
        "analyse_8_dimensions_extra": None,
    }


REF = _analyse(84, hook=90, retention=80, conversion_shop=85, emotion_dominante=60)
PERSO = _analyse(52, hook=55, retention=62, conversion_shop=50, emotion_dominante=75)


# ── Lecture de l'état ──────────────────────────────────────────────────────
def test_lit_la_colonne_user_email_des_analyses():
    sb = FauxSupabase(analysis_jobs=[{"id": 1, "user_email": EMAIL, "status": "done"}])
    e = mission.etat(sb, EMAIL)
    assert [x["fait"] for x in e["etapes"]] == [True, False, False]
    assert e["prochaine"] == 2 and e["total"] == 3


def test_sans_table_la_mission_retombe_sur_les_tables_existantes():
    sb = FauxSupabase(absentes={"trial_mission"},
                      analysis_jobs=[{"id": i, "user_email": EMAIL, "status": "done"} for i in (1, 2)],
                      script_generations=[{"id": 1, "email": EMAIL, "n_scripts": 3}])
    e = mission.etat(sb, EMAIL)
    assert e["terminee"] and e["comparatif"] is None


def test_une_deuxieme_analyse_ne_suffit_pas_avec_la_table():
    sb = FauxSupabase(trial_mission=[],
                      analysis_jobs=[{"id": i, "user_email": EMAIL, "status": "done"} for i in (1, 2)])
    assert mission.etat(sb, EMAIL)["prochaine"] == 2


# ── Validation des étapes ──────────────────────────────────────────────────
def test_etape_2_avant_etape_1_valide_l_etape_1():
    sb = FauxSupabase(trial_mission=[])
    r = mission.marquer(sb, EMAIL, 2, REF)
    assert r["ok"] and r["etape"] == 1 and r["nouvelle"]
    ligne = sb.db["trial_mission"][0]
    assert ligne["etape1_at"] and not ligne.get("etape2_at")
    assert ligne["ref_resume"]["score"] == 84


def test_les_dates_ne_sont_jamais_reecrites():
    sb = FauxSupabase(trial_mission=[])
    mission.marquer(sb, EMAIL, 1, REF)
    avant = sb.db["trial_mission"][0]["etape1_at"]
    r = mission.marquer(sb, EMAIL, 1, PERSO)
    assert not r["nouvelle"]
    ligne = sb.db["trial_mission"][0]
    assert ligne["etape1_at"] == avant and ligne["ref_resume"]["score"] == 84


def test_parcours_complet_puis_comparatif():
    sb = FauxSupabase(trial_mission=[])
    mission.marquer(sb, EMAIL, 1, REF)
    mission.marquer(sb, EMAIL, 2, PERSO)
    r = mission.marquer(sb, EMAIL, 3)
    assert r["terminee"] and sb.db["trial_mission"][0]["termine_at"]

    e = mission.etat(sb, EMAIL)
    assert e["terminee"] and e["produit"] == "Gourde isotherme"
    c = e["comparatif"]
    assert c["ref"]["score"] == 84 and c["perso"]["score"] == 52
    assert c["ref"]["cta_s"] == 8
    # Écarts triés du plus grand au plus petit ; l'émotion, meilleure chez lui,
    # n'en fait pas partie.
    assert [d["dimension"] for d in c["differences"]] == ["hook", "conversion_shop", "retention"]
    assert c["differences"][0]["pourquoi"] == "Pourquoi hook"


def test_comparatif_sans_ecart():
    c = mission.comparatif(mission.resume(PERSO), mission.resume(PERSO))
    assert c["differences"] == []


def test_resume_ignore_une_analyse_sans_score():
    assert mission.resume({"verdict": "…"}) is None
    assert mission.resume(None) is None


# ── Bilan ──────────────────────────────────────────────────────────────────
def test_bilan_ne_garde_que_les_donnees_reelles():
    sb = FauxSupabase(
        analysis_jobs=[{"user_email": EMAIL, "status": "done", "score": 74, "biais": 3},
                       {"user_email": EMAIL, "status": "done", "score": 61, "biais": 2}],
        script_generations=[{"email": EMAIL, "n_scripts": 3}, {"email": EMAIL, "n_scripts": 5}],
    )
    assert mission.bilan(sb, EMAIL) == {"videos": 2, "meilleur": 74, "leviers": 5, "accroches": 8}
    assert mission.bilan(FauxSupabase(), EMAIL) == {}
