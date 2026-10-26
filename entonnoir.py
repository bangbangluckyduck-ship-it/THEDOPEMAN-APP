"""Entonnoir de conversion — les marches du tunnel, comptées sans cookie.

  visite de l'accueil → analyse sans compte → résultat affiché → clic « débloquer »
  → inscription → mission 1, 2, 3 → abonnement

⚠️ POURQUOI CE MODULE EXISTE.
GA4 et le pixel TikTok ne comptent que les visiteurs qui ACCEPTENT les cookies :
une partie inconnue de l'entonnoir leur échappe, et le taux de passage entre deux
marches devient illisible. Ici on ne compte que des ÉVÉNEMENTS, anonymes :
  • aucun cookie, aucune adresse IP, aucun identifiant, aucun e-mail stocké ;
  • une ligne = « tel événement, telle langue, tel détail, à telle heure ».
C'est le cadre de la mesure d'audience exemptée de consentement (statistiques
agrégées, strictement internes) — à mentionner dans la politique de
confidentialité. Le bandeau cookies n'est donc pas concerné.

## Stockage
Table `funnel_events` (supabase_migrations_funnel_events.sql) : évènement,
langue, détail (méthode d'inscription, mensuel/annuel, clé d'e-mail…). Sans
elle, repli sur l'ancienne table `visitor_logs` (« evt:… », sans langue). Les
comptes de l'admin additionnent les deux : l'historique d'avant la migration
reste lisible. Requêtes prêtes à l'emploi : docs/README_ENTONNOIR.md.

## Qui envoie quoi
Le serveur enregistre ce dont il est CERTAIN (analyse sans compte, résultat
servi, inscription, étapes de mission, paiement, e-mails). Le navigateur
n'envoie que ce qu'il est seul à voir : la visite de l'accueil et les clics.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

PREFIXE = "evt:"
LANGUES = {"fr", "en", "en-ie", "pt-br", "es", "es-mx", "it", "de"}

# Le tunnel, dans l'ordre. (clef, libellé affiché dans l'admin)
ETAPES = [
    ("visite_accueil", "Visite de l'accueil"),
    ("analyse_anonyme_lancee", "Analyse lancée sans compte"),
    ("resultat_affiche", "Résultat partiel affiché"),
    ("clic_debloquer", "Clic « Débloquer mon décryptage »"),
    ("inscription", "Inscription"),
    ("mission_etape_1", "Mission 1 — vidéo qui vend analysée"),
    ("mission_etape_2", "Mission 2 — sa vidéo analysée"),
    ("mission_etape_3", "Mission 3 — accroches générées"),
    ("abonnement", "Abonnement payé"),
]

# Événements annexes, affichés sous le tunnel (pas une marche).
ANNEXES = [
    ("mission_terminee", "Mission terminée (3 étapes)"),
    ("essai_expire", "Essai arrivé à son terme"),
    ("checkout_ouvert", "Paiement Stripe ouvert"),
    ("paiement_echoue", "Paiement échoué"),
    ("pause", "Abonnement mis en pause"),
    ("resiliation", "Résiliation"),
    ("email_envoye", "E-mail envoyé"),
    ("email_clique", "Clic dans un e-mail"),
    ("cta_clic", "Clic « Analyser ma première vidéo »"),
    ("feedradar_decrypter", "Clic « Décrypter » sur le Feed Radar"),
]

# Ce que le NAVIGATEUR a le droit d'envoyer. Le reste n'est compté que côté
# serveur, là où il est certain.
DEPUIS_NAVIGATEUR = {"visite_accueil", "clic_debloquer", "cta_clic", "feedradar_decrypter"}

# Anciens noms (visitor_logs, avant le 26/10/2026) → nouveaux : l'historique
# reste compté sous le bon nom, et un navigateur qui sert encore l'ancien
# script ne perd rien.
ANCIENS_NOMS = {
    "accueil_vue": "visite_accueil",
    "analyse_lancee": "analyse_anonyme_lancee",
    "resultat_partiel": "resultat_affiche",
    "debloquer_clic": "clic_debloquer",
    "compte_cree": "inscription",
    "mission_1": "mission_etape_1",
    "mission_2": "mission_etape_2",
    "mission_3": "mission_etape_3",
}


def langue_du_compte(supabase, email: str | None) -> str | None:
    """Langue enregistrée d'un compte (users.lang) — lue, jamais stockée avec l'e-mail."""
    if not supabase or not email:
        return None
    try:
        r = supabase.table("users").select("lang").eq("email", email.lower()).limit(1).execute()
        return (r.data or [{}])[0].get("lang")
    except Exception:
        return None


def enregistrer(supabase, evenement: str, detail: str | None = None,
                lang: str | None = None, email: str | None = None) -> bool:
    """Ajoute un événement. Ne lève jamais : la mesure ne casse rien.

    `email` ne sert qu'à retrouver la langue du compte ; il n'est pas stocké.
    """
    if not supabase or not evenement:
        return False
    evenement = ANCIENS_NOMS.get(evenement, evenement)
    if lang is None and email:
        lang = langue_du_compte(supabase, email)
    lang = lang if lang in LANGUES else None
    try:
        supabase.table("funnel_events").insert({
            "evenement": evenement, "lang": lang,
            "detail": (str(detail)[:40] if detail else None),
        }).execute()
        return True
    except Exception:
        pass
    try:   # table pas encore créée : ancien stockage, sans langue ni détail
        supabase.table("visitor_logs").insert({
            "page": PREFIXE + evenement,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }).execute()
        return True
    except Exception as e:
        print(f"[entonnoir] {evenement} non enregistré : {e}")
        return False


def _compter(supabase, evenement: str, depuis: str) -> int | None:
    """Nouvelle table + historique (nouveau et ancien nom). None si tout échoue."""
    total, lu = 0, False
    try:
        r = (supabase.table("funnel_events").select("id", count="exact")
             .eq("evenement", evenement).gte("created_at", depuis).limit(1).execute())
        total += r.count or 0
        lu = True
    except Exception:
        pass
    noms = [evenement] + [ancien for ancien, nouveau in ANCIENS_NOMS.items() if nouveau == evenement]
    for nom in noms:
        try:
            r = (supabase.table("visitor_logs").select("id", count="exact")
                 .eq("page", PREFIXE + nom).gte("timestamp", depuis).limit(1).execute())
            total += r.count or 0
            lu = True
        except Exception as e:
            print(f"[entonnoir] comptage {nom} : {e}")
    return total if lu else None


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
