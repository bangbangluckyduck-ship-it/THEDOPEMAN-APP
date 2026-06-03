# WORKLOG — TikTok Shop Analyzer

> Mémoire de travail. État au **2 juin 2026**. Repo : THEDOPEMAN-APP · prod sur Render → tiktokshop-analyzer.com

---

## 🧱 Stack
- **Backend** : FastAPI (`main.py`). HTML servi en strings préchargées (`_bust()` cache-busting via mtime + `_inject_turnstile()` + `_inject_tiktok_verification()`).
- **Frontend** : PWA vanilla JS (`static/app_v3.js`) + `templates/index.html` (app) / `homepage.html` / `dope_admin.html`.
- **IA** : Mistral — vision `pixtral-12b-2409` (`analyze_visual`) + synthèse `mistral-small-latest` (`synthesize_analysis`) dans `analyzer.py`.
- **Auth** : JWT HMAC (`auth.py`, `tts_token` en localStorage). Tier résolu **côté serveur** (TIER_CONFIG). Tiers : free, pro, gold, agency, beta, admin.
- **DB** : Supabase (`supabase_client.py`).
- **Stripe** : checkout **désactivé** (`CHECKOUT_ENABLED=false` dans app_v3.js) tant que société non créée. Webhook codé (`/api/v1/stripe/webhook` + `stripe_routes.py`).

---

## ✅ Fonctionnalités livrées (cette série de sessions)

### Analyse
- Slider horizontal (carousel scroll-snap) : chaque section = une slide, Coach IA en dernier, hauteur adaptée à l'écran (cap 74vh).
- Saisie **manuelle du prix** (champ `#price-input`) → fait autorité côté serveur (`_post_process` `manual_price`).
- Historique client-side (localStorage `dv_history`, dédup par signature `_sig`).
- Bloc premium « 👑 Stratégie de Conversion » (gold/agency/beta/admin) — `PREMIUM_PROMPT_BLOCK` ajouté en fin de prompt (recency). Jamais mis en cache.

### Base d'apprentissage « structures gagnantes » (Gold/Agency)
- `insights_store.py` : `save_insight()` (anonymisé) à chaque analyse + `get_winning_similar()` + `build_winning_payload()`.
- Si score < 75 ET tier ∈ {gold,agency,beta,admin} → slide « 🏆 Les structures qui ont mieux fonctionné » (accroches/scripts >75 sur produit similaire ±30% prix).
- Table Supabase **`analyzed_insights`** (anonymisée, RLS backend-only). Se remplit naturellement avec l'usage.
- Mention RGPD mise à jour (statistiques anonymisées).

### OAuth TikTok (2 providers) — `tiktok_oauth.py`
- **provider `display`** (Login Kit / Display API, developers.tiktok.com) : vidéos publiées + métriques réelles (`video.list`). Endpoints `open.tiktokapis.com`.
- **provider `business`** (Marketing API, business-api.tiktok.com, app ID `7646295731904446481`) : insights audience via `/business/get/`. **App déjà approuvée.**
- `state` signé HMAC (anti-CSRF, TTL 10 min) porte email + provider. Callback unique `/api/auth/tiktok/callback`.
- Routes : `/api/auth/tiktok/login?provider=`, `/callback`, `/status`, `/api/tiktok/me` (profil+vidéos), `/api/tiktok/insights` (audience).
- Frontend (onglet Mon compte) : 2 boutons (« Connecter mon compte TikTok » + « Connecter mes statistiques d'audience ») + affichage profil/vidéos/démographie.
- Table Supabase **`tiktok_tokens`** : 1 ligne par (email, provider). Migrations : `supabase_migrations_tiktok_tokens.sql` + `supabase_migrations_tiktok_provider.sql`.
- Pages légales publiques **`/conditions`** et **`/confidentialite`** (exigées par review TikTok + RGPD) — `templates/terms.html` / `privacy.html`.
- Vérif domaine TikTok : fichier de signature servi via env `TIKTOK_VERIFY_FILENAME`/`TIKTOK_VERIFY_CONTENT` (méthode « préfixe d'URL »). Domaine **vérifié**.

### Pages / divers
- Logo cliquable → home ; bouton retour → home (pas quitter l'app).
- PWA back-office (`/dope-admin`) avec icône distincte (logo.png).
- Dashboard admin KPI (`dope_admin.html` + `admin_routes.py`, sécurisé `_require_admin`).

---

## 🔌 État des intégrations TikTok
| Provider | App | Statut | Clés Render |
|---|---|---|---|
| **display** (vidéos) | developers.tiktok.com | ⏸️ **EN PAUSE** — testé OK en sandbox, **pas soumis/approuvé en prod**. Code conservé. | `TIKTOK_APP_ID` / `TIKTOK_APP_SECRET` |
| **business** (audience) | business-api.tiktok.com | ✅ App approuvée. À tester (clés + migration faites). | `TIKTOK_BIZ_APP_ID` / `TIKTOK_BIZ_APP_SECRET` |

> Décision (2/6) : **Display mis en pause**, code gardé. Cible = **créateurs** (d'où Display API, pas TikTok Shop Partner ni Business-only).

---

## 🗑️ KeyAPI — SUPPRIMÉ (commit e9c86bb)
- Raison : affichage de mauvaise qualité — l'app ne consommait qu'un endpoint produit (`/tiktok/product/list/analytics`) et **fabriquait** les « créateurs », « vidéos » et **tous les liens** (URLs de recherche bidon, thumbnails de produits sur des cartes créateur).
- Retiré : `keyapi_integration.py`, endpoints `/api/market-recommendations` `/api/viral-videos` `/api/product-recommendations`, helpers, onglet frontend « Tendances Gagnantes ».
- **Conservé** : Market Intelligence in-analyse (`renderMarketSection` / `donnees_marche`) qui vient du **scraper `TTS_SCRAPER_URL`** (`/api/coach-context`), PAS de KeyAPI.
- À faire éventuellement : retirer `KEYAPI_TOKEN` de Render, drop table `viral_videos_cache` (inutiles).

---

## 🔐 Contraintes permanentes
- Vérif du plan **100% serveur** (JWT/Supabase), jamais de confiance au frontend.
- **Aucun secret hardcodé** — tout via env.
- Stripe checkout **désactivé** (CHECKOUT_ENABLED=false).
- Bloc premium **jamais caché** (cache_manager strip `strategie_conversion_premium`).
- Données TikTok/insights : **anonymisées** pour l'apprentissage, consentement + RGPD.

---

## 🗄️ Tables Supabase utilisées
`users`, `monthly_usage`, `daily_usage`, `video_analyses_cache`, `daily_visitor_stats`, `visitor_logs`, `password_reset_tokens`, `analyzed_insights`, `tiktok_tokens`, (`viral_videos_cache` = obsolète KeyAPI).

---

## 📋 Pistes / TODO
- [ ] Tester le bouton **audience (business)** en réel → ajuster `TIKTOK_BIZ_FIELDS` si la démographie ne s'affiche pas.
- [ ] **Repartir de zéro sur les « données marché »** (remplaçant de KeyAPI) — direction à définir.
- [ ] Si Display réactivé : enregistrer la vidéo démo (sandbox) → soumettre review → basculer clés prod.
- [ ] Module croisement **contenu↔perfs réelles** (Display `video.list` + analyse Mistral + agrégat anonymisé) — en attente d'approbation Display.
- [ ] (Backlog ancien) Webhook Stripe en double à réconcilier (`main.py` + `stripe_routes.py`).
- [ ] (User) Ticket Hostinger MailChannels [PSFD] (blocage email).
