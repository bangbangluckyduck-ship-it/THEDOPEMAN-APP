# Proposition de découpage `main.py` / `analyzer.py` (point 10 de l'audit)

> Note volontaire : **le refactor n'a pas été appliqué** (risque élevé sur un fichier
> de 103 routes en prod). Voici un plan sûr et incrémental à exécuter quand tu auras
> le temps de tester route par route.

## Constat
- `main.py` ≈ 178 Ko, **103 routes** `@app.*` dans un seul fichier.
- `analyzer.py` ≈ 93 Ko (pipeline transcription + vision + synthèse).
- Le pattern `APIRouter` existe déjà et fonctionne : `admin_routes.py` et
  `stripe_routes.py` sont montés via `app.include_router(...)`. On réutilise
  **exactement** ce mécanisme → aucun changement d'URL, aucun import cassé.

## Découpage proposé de `main.py` (par domaine)

| Nouveau module        | Routes déplacées                                                  |
|-----------------------|-------------------------------------------------------------------|
| `auth_routes.py`      | `/api/register`, `/api/login`, `/api/forgot-password`, `/api/change-password`, `/api/user-info`, désinscription, OAuth TikTok (`/api/auth/tiktok/*`) |
| `analyze_routes.py`   | `/analyze`, `/analyze-url*`, `/api/analyze/stream`, `/api/jobs*`, batch-patterns |
| `market_routes.py`    | `/api/market/*`, `/api/market-data`, `/api/feed-radar*`           |
| `pages_routes.py`     | pages HTML publiques (`/`, `/pricing`, `/blog/*`, `/about`, `robots.txt`, `sitemap.xml`, …) |
| `credits_routes.py`   | `/api/credits/*`, `/api/plans/*`, `/api/carousel/*`, `/api/photo-slide/*` |
| `main.py` (reste)     | création de l'app, middlewares, `include_router(...)`, startup    |

Chaque module :
```python
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/login")   # <-- @app devient @router, l'URL ne change pas
async def login(...): ...
```
puis dans `main.py` : `app.include_router(auth_router)`.

## Méthode sûre (incrémentale, testable à chaque étape)
1. Extraire **un seul domaine à la fois** (commencer par `pages_routes.py`, le moins
   risqué : pas d'état, juste du HTML), tester, déployer.
2. Les dépendances partagées (helpers `verify_turnstile`, `track_visitor`, constantes
   `_HOMEPAGE_HTML`, semaphore d'analyse…) migrent dans un `deps.py` / `state.py`
   importé par les routers, pour éviter les imports circulaires.
3. Ne jamais renommer les fonctions de route ni les chemins pendant l'extraction :
   un déplacement pur, diff lisible, rollback trivial.

## `analyzer.py`
Découper par étape du pipeline (le fichier est déjà organisé en fonctions) :
- `analyzer/transcription.py` (`transcribe_audio`)
- `analyzer/vision.py` (`analyze_visual`)
- `analyzer/synthesis.py` (`synthesize_analysis`, `synthesize_batch_patterns`)
- `analyzer/__init__.py` ré-exporte tout → `from analyzer import analyze_video` continue
  de fonctionner sans toucher `main.py`.

Gain : lisibilité + tests unitaires par étape, **sans** changer l'API publique.
