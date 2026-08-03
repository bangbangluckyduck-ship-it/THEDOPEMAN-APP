"""État de fraîcheur et de complétude des données marché.

Répond à trois questions, pour chacun des écrans qui dépendent du fournisseur
de données : **est-ce à jour, est-ce récent, est-ce complet ?**

⚠️ Ce script ne consomme AUCUN crédit KeyAPI : il ne lit que Supabase. Il est
donc utilisable même quota épuisé — c'est justement à ce moment-là qu'on a le
plus besoin de savoir ce qu'on a en réserve.

    python3 diagnostic_donnees.py

Variables nécessaires : SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY.
"""
from __future__ import annotations

import collections
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

U = (os.getenv("SUPABASE_URL") or "").rstrip("/")
SK = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or ""
MAINTENANT = datetime.now(timezone.utc)


def _lire(chemin: str, compter: bool = False):
    entetes = {"apikey": SK, "Authorization": "Bearer " + SK, "Accept": "application/json"}
    if compter:
        entetes["Prefer"] = "count=exact"
    req = urllib.request.Request(U + "/rest/v1/" + chemin, headers=entetes)
    with urllib.request.urlopen(req, timeout=30) as rep:
        return json.loads(rep.read() or b"[]"), rep.headers.get("Content-Range")


def _compter(table: str, filtre: str = "") -> int:
    """Compte EXACTEMENT, côté serveur.

    ⚠️ Indispensable : PostgREST plafonne une réponse à 1 000 lignes quel que
    soit le `limit` demandé. Compter sur les lignes rapatriées donnait donc des
    pourcentages faux dès que la table dépasse ce seuil — ce qui est déjà le cas
    de feed_radar_videos.
    """
    q = f"{table}?select=id&limit=1" + (f"&{filtre}" if filtre else "")
    try:
        _, plage = _lire(q, compter=True)
        return int((plage or "0/0").split("/")[-1])
    except Exception:
        q = q.replace("select=id", "select=*")
        _, plage = _lire(q, compter=True)
        return int((plage or "0/0").split("/")[-1])


def _depuis(jours: int) -> str:
    """Filtre PostgREST « collecté depuis moins de N jours », URL-encodé.
    Le `+` du décalage horaire ISO doit être encodé, sinon PostgREST renvoie 400."""
    from datetime import timedelta
    d = MAINTENANT - timedelta(days=jours)
    return "collected_at=gte." + urllib.parse.quote(d.isoformat())


def _date(valeur):
    """Analyse un horodatage Supabase, de façon tolérante.

    ⚠️ `datetime.fromisoformat` n'accepte, avant Python 3.11, QUE 3 ou 6 chiffres
    de fraction de seconde. Supabase en renvoie parfois 5 — la date était alors
    jugée illisible alors qu'elle était parfaitement valide. On normalise la
    fraction avant d'analyser, et on retombe sur une lecture sans fraction.
    """
    if not valeur:
        return None
    txt = str(valeur).replace("Z", "+00:00")
    normalise = re.sub(r"\.(\d+)", lambda m: "." + m.group(1)[:6].ljust(6, "0"), txt)
    for essai in (normalise, re.sub(r"\.\d+", "", txt)):
        try:
            d = datetime.fromisoformat(essai)
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return None


def _age(valeur) -> str:
    d = _date(valeur)
    if not d:
        return "date illisible"
    h = (MAINTENANT - d).total_seconds() / 3600
    if h < 48:
        return f"il y a {h:.0f} h"
    return f"il y a {h/24:.0f} jours"


def _barre(part: float, largeur: int = 24) -> str:
    plein = int(round(part * largeur))
    return "█" * plein + "·" * (largeur - plein)


def _titre(texte: str) -> None:
    print(f"\n{'═' * 66}\n{texte}\n{'═' * 66}")


# ── Feed Radar ────────────────────────────────────────────────────────────
def feed_radar() -> None:
    _titre("FEED RADAR")
    lignes, plage = _lire(
        "feed_radar_videos?select=region,collected_at,updated_at,gmv_source,"
        "gmv_real,video_products,oembed_thumbnail_url,views&limit=5000", compter=True)
    total = plage.split("/")[-1] if plage else len(lignes)
    if not lignes:
        print("  Table vide — aucune collecte n'a jamais abouti.")
        return

    total = _compter("feed_radar_videos")
    print(f"  {total} vidéos en base")
    recentes = _lire("feed_radar_videos?select=collected_at,region"
                     "&order=collected_at.desc&limit=1")[0]
    if recentes:
        print(f"  Dernière collecte : {_age(recentes[0]['collected_at'])}"
              f"  ({recentes[0]['collected_at'][:16].replace('T', ' ')} UTC)")

    # Fraîcheur : une vidéo collectée il y a plus d'une semaine est un fond de
    # catalogue, pas une tendance. C'est LA métrique qui compte pour un « radar ».
    print("\n  Fraîcheur (comptage exact) :")
    for jours, libelle in [(1, "moins de 24 h"), (7, "moins d'une semaine"),
                           (15, "moins de 15 jours"), (30, "moins d'un mois")]:
        n = _compter("feed_radar_videos", _depuis(jours))
        alerte = "  ⚠️" if jours == 7 and n == 0 else ""
        print(f"    {libelle:22} {n:>5} / {total}  {_barre(n/total)}{alerte}")

    print("\n  Couverture par région (fraîches = moins de 15 jours) :")
    for reg in sorted({l.get("region") for l in lignes if l.get("region")}):
        n = _compter("feed_radar_videos", f"region=eq.{reg}")
        f = _compter("feed_radar_videos", f"region=eq.{reg}&{_depuis(15)}")
        marque = "  ← audience cœur de cible" if reg == "FR" else ""
        print(f"    {reg:4} {n:>5} vidéos   dont {f:>4} fraîches{marque}")

    # Complétude : ce qui manque rend une carte inutilisable côté utilisateur.
    print("\n  Complétude :")
    for libelle, filtre in [
        ("avec un produit taggé", "video_products=not.is.null"),
        ("avec une vignette", "oembed_thumbnail_url=not.is.null"),
        ("avec un GMV réel (pas estimé)", "gmv_source=eq.real_attribution"),
        ("avec un GMV réel non nul", "gmv_real=gt.0"),
    ]:
        n = _compter("feed_radar_videos", filtre)
        print(f"    {libelle:32} {n:>5}/{total}  {_barre(n/total)} {n/total:>5.0%}")


# ── Créateurs Gagnants et Recherche ───────────────────────────────────────
def cache_marche() -> None:
    _titre("CRÉATEURS GAGNANTS · RECHERCHE · MARCHÉ  (cache partagé)")
    lignes, plage = _lire("market_cache?select=cache_key,expires_at,created_at&limit=5000",
                          compter=True)
    total = plage.split("/")[-1] if plage else len(lignes)
    if not lignes:
        print("  Cache vide — le premier écran ouvert consommera des crédits.")
        return
    print(f"  {total} entrées en cache\n")

    # Le préfixe de clé dit à quel écran l'entrée appartient.
    familles = collections.Counter()
    for l in lignes:
        cle = l.get("cache_key") or ""
        morceaux = cle.split(":")
        familles[":".join(morceaux[:2]) if len(morceaux) > 1 else cle] += 1

    # ⚠️ Le schéma de clés a changé au fil des versions (« v2: », « v3: », puis
    # sans préfixe). Le code actuel écrit des clés SANS préfixe de version
    # (`creators::`, `catov::`, `catmom::`, `recherche::`…). Les entrées portant
    # un ancien préfixe ne seront donc plus JAMAIS relues : elles occupent la
    # table sans servir à rien, et elles gonflent trompeusement le total.
    vivantes = [l for l in lignes
                if not (l.get("cache_key") or "").startswith(("v1:", "v2:", "v3:"))]
    mortes = len(lignes) - len(vivantes)

    print("  Entrées LISIBLES par le code actuel :")
    if not vivantes:
        print("    aucune — le premier écran ouvert consommera des crédits.")
    for fam, n in collections.Counter(
            (l.get("cache_key") or "").split(":")[0] for l in vivantes).most_common(12):
        lot = [l for l in vivantes if (l.get("cache_key") or "").startswith(fam + ":")]
        dates = [d for d in (_date(l.get("created_at")) for l in lot) if d]
        print(f"    {fam:22} {n:>4} entrées · dernière {_age(max(dates).isoformat()) if dates else '?'}")

    if mortes:
        print(f"\n  {mortes} entrées d'un ANCIEN schéma de clés (v1/v2/v3) :")
        print("    plus jamais relues par le code actuel — elles ne protègent donc")
        print("    plus rien et peuvent être purgées sans conséquence.")

    print("\n  ⓘ Une entrée périmée reste servie plutôt que d'afficher un écran vide")
    print("    (cache quasi permanent). Elle n'est rafraîchie qu'au bouton dédié.")


# ── Produits mémorisés ────────────────────────────────────────────────────
def produits() -> None:
    _titre("MÉMOIRE PRODUITS  (alimentée par les analyses, sans KeyAPI)")
    try:
        lignes, plage = _lire("analyzed_products?select=last_seen,region&limit=2000",
                              compter=True)
    except Exception as e:
        print("  table indisponible :", e)
        return
    if not lignes:
        print("  Vide.")
        return
    dates = [d for d in (_date(l.get("last_seen")) for l in lignes) if d]
    print(f"  {plage.split('/')[-1] if plage else len(lignes)} produits mémorisés")
    if dates:
        print(f"  Dernier vu : {_age(max(dates).isoformat())}")


def main() -> int:
    if not U or not SK:
        print("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY manquants.")
        return 1
    print(f"Diagnostic des données — {MAINTENANT:%d/%m/%Y %H:%M} UTC")
    print("Lecture seule, aucun crédit fournisseur consommé.")
    for section in (feed_radar, cache_marche, produits):
        try:
            section()
        except Exception as e:
            print(f"\n  ⚠️ {section.__name__} : {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
