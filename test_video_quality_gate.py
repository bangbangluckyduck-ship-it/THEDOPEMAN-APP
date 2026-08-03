"""Tests du contrôle qualité des constats vidéo (analyzer._video_quality_issues).

Pourquoi ces tests existent : Claude ne voit jamais la vidéo. Il ne peut donc
pas remarquer qu'une timeline s'arrête à la 8e seconde d'un clip de 45, ni qu'un
timestamp tombe après la fin. Ce contrôle est le DERNIER endroit du pipeline où
une hallucination temporelle peut encore être vue — s'il se trompe, un rapport
faux part chez un client sans que rien ne le signale.

Deux risques symétriques, tous deux couverts ici :
  - laisser passer des constats faux → rapport inventé livré avec assurance ;
  - crier au loup sur une vidéo atypique (muette, plan fixe) → escalade inutile
    vers le modèle lent, donc la lenteur qu'on cherchait à éliminer.

Aucun appel réseau : le contrôle ne compare que des nombres entre eux.

    python3 test_video_quality_gate.py
"""
import sys

from analyzer import _video_quality_issues as gate


def constats(**overrides) -> dict:
    """Constats d'une analyse saine ; les cas de test n'en dévient qu'un aspect."""
    data = {
        "produit": "Sérum vitamine C",
        "confiance_detection": 0.95,
        "description_visuelle": "Plan serré salle de bain, lumière naturelle",
        "transcript": "Franchement ce sérum a changé ma peau, lien en bio",
        "qualite_visuelle_score": 72,
        "format_visuel_score": 80,
        "hook_visuel_score": 65,
        "cta_visuel": {"present": True, "description": "Lien en bio", "timestamp_seconds": 28},
        "cta_audio": {"present": True, "phrase": "lien en bio", "timestamp_seconds": 28},
        "rythme": "rapide",
        "duree_secondes": 30,
        "moderation": {"is_safe_visuel": True, "raison": None},
        "timeline_evenements": [
            {"timestamp_seconds": t, "evenement": "plan", "texte_ecran": None}
            for t in (0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30)
        ],
    }
    data.update(overrides)
    return data


def timeline(*timestamps):
    return [{"timestamp_seconds": t, "evenement": "plan", "texte_ecran": None} for t in timestamps]


# (libellé, constats, attendu) — attendu True = au moins une anomalie détectée.
CAS = [
    # — Ne doit RIEN signaler : sinon on escalade pour rien et on perd la vitesse.
    ("analyse saine", constats(), False),
    ("vidéo muette (aucun CTA audio annoncé)",
     constats(transcript="", cta_audio={"present": False, "phrase": None,
                                        "timestamp_seconds": None}), False),
    ("vidéo courte, timeline dense",
     constats(duree_secondes=7, timeline_evenements=timeline(0, 2, 4, 7)), False),
    ("confiance juste au-dessus du seuil", constats(confiance_detection=0.7), False),

    # — Doit signaler : constats invérifiables en aval.
    ("timeline absente", constats(timeline_evenements=[]), True),
    ("timeline qui s'arrête au début (8s sur 45s)",
     constats(duree_secondes=45, timeline_evenements=timeline(0, 3, 6, 8)), True),
    ("timestamp au-delà de la fin de la vidéo",
     constats(timeline_evenements=timeline(0, 10, 20, 55)), True),
    ("trou de 22s au milieu de la timeline",
     constats(timeline_evenements=timeline(0, 3, 25, 28, 30)), True),
    ("confiance de détection trop basse", constats(confiance_detection=0.4), True),
    ("CTA audio annoncé mais transcript vide", constats(transcript="   "), True),
    ("durée de vidéo non renseignée", constats(duree_secondes=0), True),
    ("timeline sans aucun timestamp exploitable",
     constats(timeline_evenements=[{"evenement": "plan"}]), True),

    # — Régression : le JSON que l'ancien code fabriquait en silence quand la
    #   réponse du modèle était illisible. Notes neutres, timeline vide, et
    #   surtout modération au vert sur une vidéo que personne n'avait regardée.
    #   Il partait tel quel chez le client. Il doit désormais être rejeté.
    ("analyse fabriquée de l'ancien repli silencieux",
     constats(confiance_detection=0.6, transcript="", duree_secondes=0,
              timeline_evenements=[], qualite_visuelle_score=50,
              format_visuel_score=50, hook_visuel_score=50,
              cta_visuel={"present": False}, cta_audio={"present": False}), True),
]


def main() -> int:
    echecs = 0
    for libelle, data, doit_signaler in CAS:
        anomalies = gate(data)
        ok = bool(anomalies) is doit_signaler
        echecs += not ok
        detail = " | ".join(anomalies) if anomalies else "aucune anomalie"
        print(f"{'✅' if ok else '❌'} {libelle:46s} → {detail}")

    total = len(CAS)
    if echecs:
        print(f"\n❌ {echecs}/{total} cas en échec")
        return 1
    print(f"\n✅ {total}/{total} cas passent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
