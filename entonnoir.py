"""Entonnoir de conversion — les marches de l'escalier, comptées sans cookie.

  visiteur → clic sur l'appel à l'action → analyse lancée → analyse terminée
  → compte créé → mission 1…4 → abonnement

⚠️ POURQUOI CE MODULE EXISTE.
GA4 et le pixel TikTok ne comptent que les visiteurs qui ACCEPTENT les cookies :
une partie inconnue de l'entonnoir leur échappe, et le taux de passage entre deux
marches devient illisible. Ici on ne compte que des ÉVÉNEMENTS, anonymes :
  • aucun cookie, aucune adresse IP, aucun identifiant, aucun e-mail stocké ;
  • une ligne = « tel événement a eu lieu à telle heure », rien d'autre.
C'est le cadre de la mesure d'audience exemptée de consentement (statistiques
agrégées, strictement internes) — à mentionner dans la politique de
confidentialité.

Stockage : la table `visitor_logs`, déjà en place (append-only, page = « evt:… »).
Aucune migration. Compter des événements plutôt que des personnes est assumé :
les événements « vue » et « clic » sont dédoublonnés par onglet côté navigateur,
ce qui suffit à lire les taux de passage d'une semaine sur l'autre.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

PREFIXE = "evt:"

# L'escalier, dans l'ordre. (clef, libellé affiché dans l'admin)
ETAPES = [
    ("accueil_vue", "Vue de l'accueil"),
    ("cta_clic", "Clic sur « Analyser ma première vidéo »"),
    ("analyse_lancee", "Analyse lancée"),
    ("analyse_terminee", "Analyse terminée"),
    ("compte_cree", "Compte créé"),
    ("mission_1", "Mission 1 — vidéo qui vend décryptée"),
    ("mission_2", "Mission 2 — angles pour son produit"),
    ("mission_3", "Mission 3 — script gardé"),
    ("mission_4", "Mission 4 — sa vidéo décryptée"),
    ("abonnement", "Abonnement payé"),
]

# Événements annexes, affichés sous l'escalier (pas une marche).
ANNEXES = [
    ("resultat_partiel", "Résultat partiel vu (sans compte)"),
    ("debloquer_clic", "Clic « Voir tout mon décryptage »"),
    ("feedradar_decrypter", "Clic « Décrypter » sur le Feed Radar"),
]

# Ce que le NAVIGATEUR a le droit d'envoyer. Compte créé et abonnement ne sont
# comptés que côté serveur, là où ils sont certains (inscription, webhook Stripe).
DEPUIS_NAVIGATEUR = {
    "accueil_vue", "cta_clic", "analyse_lancee", "analyse_terminee",
    "mission_1", "mission_2", "mission_3", "mission_4",
    "resultat_partiel", "debloquer_clic", "feedradar_decrypter",
}


def enregistrer(supabase, evenement: str) -> bool:
    """Ajoute un événement. Ne lève jamais : la mesure ne casse rien."""
    if not supabase or not evenement:
        return False
    try:
        supabase.table("visitor_logs").insert({
            "page": PREFIXE + evenement,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }).execute()
        return True
    except Exception as e:
        print(f"[entonnoir] {evenement} non enregistré : {e}")
        return False


def _compter(supabase, evenement: str, depuis: str) -> int | None:
    try:
        r = (supabase.table("visitor_logs").select("id", count="exact")
             .eq("page", PREFIXE + evenement).gte("timestamp", depuis)
             .limit(1).execute())
        return r.count or 0
    except Exception as e:
        print(f"[entonnoir] comptage {evenement} : {e}")
        return None


def tableau(supabase, jours: int = 30) -> dict:
    """Les marches avec, pour chacune, le taux de passage depuis la précédente."""
    jours = max(1, min(int(jours or 30), 365))
    depuis = (datetime.now(timezone.utc) - timedelta(days=jours)).isoformat()

    marches, precedent = [], None
    for cle, libelle in ETAPES:
        total = _compter(supabase, cle, depuis)
        taux = (round(100 * total / precedent, 1)
                if total is not None and precedent else None)
        marches.append({"cle": cle, "libelle": libelle, "total": total, "taux": taux})
        precedent = total
    base = marches[0]["total"] or 0
    for m in marches:
        m["depuis_debut"] = round(100 * m["total"] / base, 2) if base and m["total"] is not None else None

    annexes = [{"cle": c, "libelle": l, "total": _compter(supabase, c, depuis)} for c, l in ANNEXES]
    return {"jours": jours, "depuis": depuis, "marches": marches, "annexes": annexes}
