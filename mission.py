"""Mission d'essai — 4 étapes qui mènent de « je comprends » à « je publie ».

  1. Décrypte une vidéo qui vend           → ≥ 1 analyse
  2. Et pour ton produit ?                 → ≥ 1 génération de scripts
  3. Prépare ta prochaine vidéo            → ≥ 1 script gardé (favori « script »)
  4. Reviens décrypter ta vidéo publiée    → 1 analyse APRÈS le script gardé

L'état est DÉDUIT des tables existantes (analysis_jobs, script_generations,
user_favorites) : aucune migration, rien à tenir à jour à la main, et la même
source sert l'app (GET /api/mission) et les e-mails d'essai (essai_emails.py).
"""
from __future__ import annotations


def _dates(supabase, table: str, email: str, extra: dict | None = None,
           limit: int = 500) -> list[str]:
    """Dates de création (ISO, triées) des lignes d'un compte. [] si indisponible."""
    if not supabase:
        return []
    try:
        q = supabase.table(table).select("created_at").eq("email", email)
        for col, val in (extra or {}).items():
            q = q.eq(col, val)
        r = q.order("created_at", desc=False).limit(limit).execute()
        return [row["created_at"] for row in (r.data or []) if row.get("created_at")]
    except Exception as e:
        print(f"[mission] {table}: {e}")
        return []


def etat(supabase, email: str) -> dict:
    """État de la mission d'un compte + bilan chiffré (fin d'essai)."""
    analyses = _dates(supabase, "analysis_jobs", email, {"status": "done"})
    scripts = _dates(supabase, "script_generations", email)
    gardes = _dates(supabase, "user_favorites", email, {"item_type": "script"})

    premier_garde = gardes[0] if gardes else None
    # Les dates ISO de Supabase sont comparables en tant que chaînes (même format).
    apres_script = [d for d in analyses if premier_garde and d > premier_garde]

    etapes = [
        {"id": 1, "fait": len(analyses) >= 1},
        {"id": 2, "fait": len(scripts) >= 1},
        {"id": 3, "fait": len(gardes) >= 1},
        {"id": 4, "fait": len(apres_script) >= 1},
    ]
    prochaine = next((e["id"] for e in etapes if not e["fait"]), None)
    return {
        "etapes": etapes,
        "terminees": sum(1 for e in etapes if e["fait"]),
        "prochaine": prochaine,          # None = mission accomplie
        "bilan": {
            "videos_decryptees": len(analyses),
            "generations_scripts": len(scripts),
            "scripts_gardes": len(gardes),
        },
    }
