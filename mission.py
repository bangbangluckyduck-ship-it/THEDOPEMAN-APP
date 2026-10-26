"""Mission d'essai — « Fais ton premier diagnostic en 60 secondes ».

  1. Analyse une vidéo qui vend        → une première analyse (accueil compris)
  2. Analyse TA dernière vidéo         → une analyse lancée depuis la mission
  3. Génère 3 accroches pour ton produit → une génération sur /scripts

Dès que les étapes 1 et 2 sont faites, la mission compare les deux vidéos
(score, force de l'accroche, moment de l'appel à l'action, 2 ou 3 écarts) : c'est
le déclic « je n'avais pas vu ça ». Le comparatif est CALCULÉ à partir des deux
analyses déjà produites — aucun appel d'IA supplémentaire.

## Stockage
La table `trial_mission` (supabase_migrations_mission_v2.sql) garde, par compte,
la date de chaque étape et un résumé des deux vidéos à comparer. Elle suit
l'utilisateur sur tous ses appareils et sert aux e-mails d'essai.

Sans la table (migration pas encore jouée), la mission reste utilisable : son état
est alors DÉDUIT des tables existantes (analyses terminées, générations de
scripts), comme avant — seul le comparatif manque.

⚠️ La colonne e-mail de `analysis_jobs` s'appelle `user_email`. L'ancienne
version interrogeait `email` : la requête échouait en silence, l'étape « analyse »
n'était jamais validée et le bilan de fin d'essai comptait toujours 0 vidéo.
"""
from __future__ import annotations

from datetime import datetime, timezone

ETAPES = (1, 2, 3)
TABLE = "trial_mission"

# Dimensions comparées, dans l'ordre d'affichage. Les libellés sont traduits par
# l'interface (clefs `dim_<dimension>`), pas ici.
DIMENSIONS = ("hook", "retention", "mecanismes_vente", "positionnement",
              "format_visuel", "emotion_dominante", "conversion_shop", "algorithme")

# Écart minimal (points sur 100) pour qu'une dimension compte comme une différence.
ECART_MIN = 10


def _maintenant() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Lecture des données existantes ────────────────────────────────────────
def _compter(supabase, table: str, colonne: str, email: str, extra: dict | None = None) -> int:
    """Nombre de lignes d'un compte. 0 si indisponible."""
    if not supabase:
        return 0
    try:
        q = supabase.table(table).select("id", count="exact").eq(colonne, email)
        for col, val in (extra or {}).items():
            q = q.eq(col, val)
        r = q.limit(1).execute()
        return int(r.count or 0)
    except Exception as e:
        print(f"[mission] comptage {table} : {e}")
        return 0


def _premiere_analyse(supabase, email: str) -> dict | None:
    """Résultat de la première analyse terminée du compte (pour le comparatif)."""
    if not supabase:
        return None
    try:
        r = (supabase.table("analysis_jobs").select("result")
             .eq("user_email", email).eq("status", "done")
             .order("created_at", desc=False).limit(1).execute())
        rows = r.data or []
        return rows[0].get("result") if rows else None
    except Exception as e:
        print(f"[mission] première analyse : {e}")
        return None


def _ligne(supabase, email: str) -> tuple[bool, dict | None]:
    """(table disponible, ligne du compte ou None)."""
    if not supabase:
        return False, None
    try:
        r = supabase.table(TABLE).select("*").eq("email", email).limit(1).execute()
        rows = r.data or []
        return True, (rows[0] if rows else None)
    except Exception as e:
        print(f"[mission] {TABLE} indisponible : {e}")
        return False, None


# ── Résumé d'une analyse et comparatif ───────────────────────────────────
def _nombre(v):
    try:
        return round(float(v))
    except (TypeError, ValueError):
        return None


def _cta_seconde(result: dict):
    """Seconde de l'appel à l'action (audio prioritaire, puis visuel), ou None."""
    for cle in ("cta_audio", "cta_visuel"):
        bloc = result.get(cle) or {}
        if isinstance(bloc, dict) and bloc.get("present") is not False:
            s = _nombre(bloc.get("timestamp_seconds"))
            if s is not None and s >= 0:
                return s
    return None


def resume(result: dict | None) -> dict | None:
    """Ce qu'il faut garder d'une analyse pour la comparer, sans tout stocker."""
    if not isinstance(result, dict):
        return None
    score = _nombre(result.get("score_global"))
    if score is None:
        return None
    det = result.get("detection") or {}
    dims, feedback = {}, {}
    for cle, bloc in (result.get("analyse_8_dimensions") or {}).items():
        if cle in DIMENSIONS and isinstance(bloc, dict):
            s = _nombre(bloc.get("score"))
            if s is not None:
                dims[cle] = s
            if bloc.get("feedback"):
                feedback[cle] = str(bloc["feedback"])[:240]
    return {
        "score": score,
        "hook_force": _nombre(det.get("hook_force")),
        "hook_type": det.get("hook_type") or None,
        "cta_s": _cta_seconde(result),
        "produit": det.get("produit") or None,
        "prix": det.get("prix_estime") or None,
        "url": result.get("source_url") or None,
        "dims": dims,
        "feedback": feedback,
    }


def comparatif(ref: dict | None, perso: dict | None) -> dict | None:
    """Vidéo qui vend vs vidéo de l'utilisateur : chiffres + 2 ou 3 écarts clés."""
    if not ref or not perso:
        return None
    communes = [d for d in DIMENSIONS if d in ref.get("dims", {}) and d in perso.get("dims", {})]
    ecarts = sorted(communes, key=lambda d: perso["dims"][d] - ref["dims"][d])
    differences = [
        {"dimension": d, "ref": ref["dims"][d], "perso": perso["dims"][d],
         "pourquoi": (ref.get("feedback") or {}).get(d)}
        for d in ecarts if ref["dims"][d] - perso["dims"][d] >= ECART_MIN
    ][:3]
    garder = ("score", "hook_force", "hook_type", "cta_s", "produit", "url")
    return {
        "ref": {k: ref.get(k) for k in garder},
        "perso": {k: perso.get(k) for k in garder},
        "differences": differences,
    }


# ── État de la mission ────────────────────────────────────────────────────
def etat(supabase, email: str) -> dict:
    """État de la mission d'un compte, comparatif et bilan chiffré."""
    email = (email or "").strip().lower()
    disponible, ligne = _ligne(supabase, email)
    ligne = ligne or {}
    analyses = _compter(supabase, "analysis_jobs", "user_email", email, {"status": "done"})
    generations = _compter(supabase, "script_generations", "email", email)

    fait = {
        1: bool(ligne.get("etape1_at")) or analyses >= 1,
        # Sans la table, impossible de savoir quelle analyse est la sienne : on
        # retombe sur « une deuxième analyse », l'approximation la moins fausse.
        2: bool(ligne.get("etape2_at")) or (not disponible and analyses >= 2),
        3: bool(ligne.get("etape3_at")) or generations >= 1,
    }
    etapes = [{"id": i, "fait": fait[i]} for i in ETAPES]
    prochaine = next((i for i in ETAPES if not fait[i]), None)

    comp = None
    if fait[1] and fait[2]:
        ref = ligne.get("ref_resume") or resume(_premiere_analyse(supabase, email))
        comp = comparatif(ref, ligne.get("perso_resume"))

    return {
        "etapes": etapes,
        "terminees": sum(1 for i in ETAPES if fait[i]),
        "total": len(ETAPES),
        "prochaine": prochaine,                 # None = mission accomplie
        "terminee": prochaine is None,
        # Produit détecté sur la vidéo qui vend : préremplit l'étape 3.
        "produit": ((ligne.get("perso_resume") or {}).get("produit")
                    or (ligne.get("ref_resume") or {}).get("produit")),
        "comparatif": comp,
        "bilan": bilan(supabase, email),
    }


def marquer(supabase, email: str, etape: int, resultat: dict | None = None) -> dict:
    """Valide une étape (sans jamais réécrire une date déjà posée).

    `resultat` : l'analyse qui valide l'étape 1 ou 2, résumée pour le comparatif.
    Une étape 2 demandée alors que l'étape 1 n'est pas faite valide l'étape 1 :
    la première vidéo analysée sert toujours de référence.
    Renvoie {"ok": bool, "nouvelle": bool, "etape": int, "terminee": bool}.
    """
    email = (email or "").strip().lower()
    if etape not in ETAPES or not email or not supabase:
        return {"ok": False, "nouvelle": False, "etape": etape, "terminee": False}
    disponible, ligne = _ligne(supabase, email)
    if not disponible:
        return {"ok": False, "nouvelle": False, "etape": etape, "terminee": False}
    ligne = ligne or {}

    if etape == 2 and not ligne.get("etape1_at"):
        etape = 1
    maj: dict = {}
    if not ligne.get(f"etape{etape}_at"):
        maj[f"etape{etape}_at"] = _maintenant()
    r = resume(resultat)
    if etape == 1 and r and not ligne.get("ref_resume"):
        maj["ref_resume"] = r
    if etape == 2 and r and not ligne.get("perso_resume"):
        maj["perso_resume"] = r

    dates = {i: ligne.get(f"etape{i}_at") or maj.get(f"etape{i}_at") for i in ETAPES}
    terminee = all(dates.values())
    if terminee and not ligne.get("termine_at"):
        maj["termine_at"] = _maintenant()
    nouvelle = f"etape{etape}_at" in maj
    if not maj:
        return {"ok": True, "nouvelle": False, "etape": etape, "terminee": terminee}
    try:
        maj["updated_at"] = _maintenant()
        if ligne:
            supabase.table(TABLE).update(maj).eq("email", email).execute()
        else:
            supabase.table(TABLE).insert({"email": email, **maj}).execute()
    except Exception as e:
        print(f"[mission] marquer étape {etape} ({email}) : {e}")
        return {"ok": False, "nouvelle": False, "etape": etape, "terminee": False}
    import entonnoir
    if nouvelle:
        entonnoir.enregistrer(supabase, f"mission_etape_{etape}", email=email)
    if "termine_at" in maj:
        entonnoir.enregistrer(supabase, "mission_terminee", email=email)
    return {"ok": True, "nouvelle": nouvelle, "etape": etape, "terminee": terminee}


# ── Bilan (fin d'essai, e-mails J6/J7) ───────────────────────────────────
def bilan(supabase, email: str) -> dict:
    """Ce que le compte a réellement fait. Une valeur absente = aucune donnée.

    - videos   : analyses terminées
    - leviers  : leviers de vente identifiés (somme des `nb_biais` des analyses)
    - accroches: accroches générées sur /scripts (somme des `n_scripts`)
    - meilleur : meilleure note obtenue par une vidéo, sur 100
    """
    email = (email or "").strip().lower()
    out: dict = {}
    if not supabase or not email:
        return out
    try:
        r = (supabase.table("analysis_jobs")
             .select("score:result->score_global,"
                     "biais:result->analyse_8_dimensions->mecanismes_vente->nb_biais")
             .eq("user_email", email).eq("status", "done").limit(500).execute())
        rows = r.data or []
        if rows:
            out["videos"] = len(rows)
            scores = [s for s in (_nombre(x.get("score")) for x in rows) if s is not None]
            if scores:
                out["meilleur"] = max(scores)
            leviers = sum(b for b in (_nombre(x.get("biais")) for x in rows) if b)
            if leviers:
                out["leviers"] = leviers
    except Exception as e:
        print(f"[mission] bilan analyses : {e}")
    try:
        r = (supabase.table("script_generations").select("n_scripts")
             .eq("email", email).limit(500).execute())
        accroches = sum(int(x.get("n_scripts") or 0) for x in (r.data or []))
        if accroches:
            out["accroches"] = accroches
    except Exception as e:
        print(f"[mission] bilan scripts : {e}")
    return out
