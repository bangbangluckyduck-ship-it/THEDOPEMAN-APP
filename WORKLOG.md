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

## 🎯 CAHIER DES CHARGES — Données marché / créateurs [VALIDÉ 2/6/2026]

> Remplaçant de l'ancienne intégration KeyAPI (supprimée). À NE PAS recoder tant que
> la source de données (KeyAPI ou autre) n'a pas été confirmée comme exposant
> réellement les champs ci-dessous (liens + visuels réels).

**But** : intelligence **marché / concurrents** — l'œil sur LES AUTRES (≠ API officielle TikTok = SON propre compte). Les deux sont complémentaires.

**Cœur de la fonctionnalité = LES CRÉATEURS** : donner aux abonnés Gold un accès aux **créateurs qui performent le mieux dans le monde**, **ce qu'ils font** (leur contenu / vidéos) et **ce qu'ils vendent** (leurs produits).

**Doit afficher (données 100% réelles, par catégorie) :**
1. **Top créateurs mondiaux** qui cartonnent → **lien direct vers leur profil** + vraie photo de profil.
2. **Leur contenu** : les **vraies vidéos gagnantes** → **lien direct vers la bonne vidéo** + vraie miniature.
3. **Ce qu'ils vendent** : les **produits** → **lien direct vers la fiche produit TikTok** + vraie image produit.

**Règle qualité (échec passé à ne pas reproduire) :**
- ❌ Interdit : faux liens (URLs de recherche), faux créateurs déduits des produits, vidéos bidon, thumbnails qui ne correspondent pas.
- ✅ Obligatoire : uniquement des données réelles de l'API, liens directs réels (créateur / vidéo / produit), visuels exacts. Donnée absente → on ne l'affiche pas (jamais inventer).

**Accès (gating) :**
- **Gold & Agency** : accès complet.
- **Plans inférieurs (free/pro)** : affichage **partiel + reste flouté** (teasing → upsell Gold).

**Prochaine étape avant tout code** : confirmer que la source (KeyAPI ou alternative) expose bien créateurs + leurs vidéos + leurs produits avec liens directs et visuels réels. Sinon → changer de source.

### ✅ KeyAPI VALIDÉ (audit 2/6, base https://api.keyapi.ai, header `Authorization: Bearer <KEYAPI_TOKEN>`)
Chaîne créateur-centric confirmée (endpoint debug admin `/api/_debug/keyapi` — À RETIRER après build) :

1. **Top créateurs** : `GET /v1/tiktok/influencer/ranking/analytics`
   params requis : `date` (yyyy-MM-dd, 1er du mois si mensuel), `region` (US), `rank_type` (1=jour,2=semaine,3=mois), `influencer_rank_field` (1=followers,2=ventes), `page_num` (1), `page_size` (≤10).
   → champs : `avatar`, `nick_name`, `unique_id` (handle), `user_id`, `total_followers_history_cnt`, `total_sale_history_cnt`, `total_sale_gmv_history_amt`, `most_category_id`, `region`.
   → **lien profil** = `https://www.tiktok.com/@{unique_id}`

2. **Vidéos d'un créateur** : `GET /v1/tiktok/influencer/videos`
   param requis : **`unique_id`** (PAS user_id) + `page_num`, `page_size`.
   → `data.aweme_list[]` : `aweme_id`, `desc`, `share_url` (lien direct), `video.cover.url_list[0]` / `origin_cover` (miniature), `statistics.{play_count,digg_count,comment_count,share_count,collect_count}`.

3. **Produits d'un créateur** : `GET /v1/tiktok/influencer/products/analytics`
   param : **`user_id`** + `page_num`, `page_size`.
   → `cover_url` (JSON string array → parser), `product_id`, `product_name`, `spu_avg_price`, `total_sale_cnt`, `total_sale_gmv_amt`.

⚠️ Les URLs d'images/vidéos TikTok sont **signées avec expiration** (`x-expires`) → les récupérer à la volée (pas de cache long). Lien fiche produit à confirmer (format `shop.tiktok.com/view/product/{product_id}` non vérifié).

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

## 💳 KeyAPI — état (2/6 soir)
- Feature « Créateurs Gagnants » + reco marché auto **codées, déployées, validées** sur la vraie chaîne (ranking → videos → products/analytics).
- ⚠️ **Essai gratuit 7j terminé → 0 crédit.** Décision : **abonnement KeyAPI payant** (option choisie). Dès recharge, la feature remarche telle quelle (aucun re-dev).
- Sans crédit : les endpoints renvoient 402 → l'UI dégrade proprement (vide), pas de plantage.
- Le **cache Supabase** (24h créateurs/catégorie, 12h détail) limite la conso → activer la table `market_cache` (SQL fourni) pour économiser le quota.
- 🔧 Endpoint debug `/api/_debug/keyapi` = consomme du quota → **à retirer** une fois le multi-pays fini.

## 🌍 Multi-pays — CONFIRMÉ FONCTIONNEL (2026-07-02)
Objectif : Top créateurs par **pays** (mensuel ≈ 30j), localisé selon la langue de l'app — l'utilisateur voit d'abord son pays puis les autres marchés (US, UK, BR…).
- ✅ **FR CONFIRMÉ COUVERT** — re-testé en direct le 02/07/2026, 9 créateurs FR remontés (ex: @hannaholala, 2M abonnés). Le "FR = 0 créateur" plus haut était dû au quota KeyAPI épuisé au moment du test, pas à une absence de données — ne pas re-douter cette couverture sans re-tester.
- 9 régions confirmées utilisables : US, GB, BR, DE, FR, ES, IT, ID, MY (= `MARKET_COUNTRIES` dans `static/app_v3.js`, réutilisé par `FEED_RADAR_REGIONS` dans `feed_radar.py`).
- Codé : Feed Radar boucle sur ces 9 régions à chaque collecte cron ; chaque utilisateur voit les vidéos de sa région (détectée via `_userRegion()` côté frontend).

## 🐛 Bugs marché restants
- **Lien produit** : `shop.tiktok.com/view/product/{id}` ne redirige pas (peut-être géo-bloqué FR). À tester `www.tiktok.com/view/product/{id}` dans le navigateur (sans quota). Endpoint `insights/product/detail` = payant (402), inutilisable.
- **Miniatures vidéo** : étaient en `.heic` (KO Chrome) → fix `.heic→.jpeg` + `<img onerror>` déployé (à reconfirmer en prod).

## 🆕 Endpoints KeyAPI « realtime » (branchés, à tester au 1er paiement)
Schéma validé sur exemples KeyAPI réels (2026-06). Tout est gated Gold/Agency + caché 7j.
- **Fix lien produit** : `_clean_product` passe de `shop.tiktok.com` → `www.tiktok.com/view/product/{id}`
  (confirmé par `share_deep_link` de `detail_new_app`). C'était la cause des liens qui ne redirigeaient pas.
- **`detail_new_app`** → `market_creators.get_product_detail(product_id, region)` :
  navigue `data.data.goda_protocol.data.global.product_info_resp.products[0]` → titre, image
  (`product_base.images[].url_list[0]`), prix (`price.real_price/original_price`), `sold_count`,
  note (`product_detail_review`), vendeur, **VRAIE URL** (`share_info.share_deep_link`, on garde le nu).
  Endpoint : `GET /api/market/product/{product_id}` (Gold/Agency only).
- **`product/search`** → `market_creators.search_products(keyword, region)` :
  parse `data.body.sections[].items[].data.raw_data` (string JSON Lynx) → `view_object.commonLogParams.cardLog`
  (title_text, show_price, currency, rate, volume) + `dynamicData.cover` + `baseLog.seller_name`.
  Endpoint : `GET /api/market/products/search?keyword=&region=` (Gold full / free-pro preview[:2]).
  Front : `renderSimilarProducts(d)` dans les résultats d'analyse (« 🛍️ Produits similaires en tendance »).
- ⚠️ **À CONFIRMER au 1er test payant** : (1) noms exacts des params (`keyword`/`region`/`product_id`) ;
  (2) coût crédits « realtime » (peut être > endpoints influencer) ; (3) `product/search` est géolocalisé
  → forcer `region` selon langue app sinon prix en devise locale (test a renvoyé MY/VN en RM).
- `photo-search` / `photo-search/page` : non branchés (reco par image, à évaluer plus tard).

## 🎯 Métriques produit par période (à valider AU PAIEMENT, NE PAS coder à l'aveugle)
Catalogue KeyAPI complet reçu (2026-06). Le user veut sur un produit : **commandes 7j/28j, CTR,
nb de créateurs ayant posté une vidéo (période), nb d'add-to-cart**. Ces métriques ne sont PAS dans
`detail_new_app` (qui ne donne que `sold_count` cumulé) → elles sont dans la famille **« (Analytics) »
+ « Intelligence »** (= données Affiliate Center, visibles par tous les créateurs, donc scrapables).
Mapping le plus probable :
- **Commandes 7j/28j** → `Product Detail (Analytics)` + `Product Trends (Analytics)` (séries par période).
- **CTR + add-to-cart** → `Top Product Insights Detail` (Intelligence / Affiliate Center).
- **Nb créateurs ayant posté une vidéo (période)** → `Product Creators (Analytics)`.
- Bonus pipeline : `Get Product ID from Share Link` (lien → product_id), `Product Videos (Analytics)`.
PLAN AU PAIEMENT (3 appels test, puis le user colle les réponses → je construis les parseurs sur le vrai schéma) :
  1. `Product Detail (Analytics)` sur un product_id connu → champs période (order_cnt_7d, ctr…).
  2. `Product Creators (Analytics)` → confirme « nb créateurs / période ».
  3. `Top Product Insights Detail` → confirme CTR + add-to-cart.
⚠️ Discipline : on a déjà été piégés à deviner les schémas KeyAPI → AUCUN code avant d'avoir la vraie réponse JSON.

## 📸 Photo Slide Coach (livré — MVP, GOLD/AGENCY)
Onglet `📸 Photo Slide` (à droite de Créateurs Gagnants). Upload image produit + nature/prix/description
→ IA vision **pixtral-12b** → plan carrousel : type de slide (3 styles), Hook slide 1, titre carrousel
(+variantes), description optimisée, plan slide par slide AVEC type de photo à prendre, CTA dernière slide,
hashtags, conseils saves. Boutons « Copier » partout.
- **`photo_slide.py`** : `PHOTO_SLIDE_SYSTEM_PROMPT` (directives + 3 styles) avec **2 ZONES ÉDITABLES**
  balisées (`⬇️ ZONE ÉDITABLE 1 — HOOKS GAGNANTS`, `ZONE ÉDITABLE 2 — IDÉES DE SLIDES`) pour que le PO
  enrichisse l'IA sans toucher au code. `generate_photo_slide()` → pixtral, fallback mock si échec (`_fallback`).
- **`main.py`** : `POST /api/photo-slide/generate` (Form: image b64 + champs), gated `_MARKET_PREMIUM_TIERS`,
  exécuté en executor, timeout 90s. Image ÉPHÉMÈRE (base64 → IA, pas de stockage).
- **Front** : onglet `tab-photoslide`, gate non-premium → pricing, upload drag&drop (`_psHandleFile`),
  `generatePhotoSlide()` + `renderPhotoSlideResult()`. tier via `window.__userInfo`.
- **Différé (phase 2)** : export PDF/image, historique (table `photo_slide_generations`), partage AGENCY,
  suggestions musique, quotas/mois. Stripe reste désactivé → upsell pointe vers pricing.
- **Streaming SSE en 2 étapes (affichage au fur et à mesure)** :
  `generate_strategy()` (pixtral, ~15-25s) → event `strategy` (type slide + hook + titre + niche) affiché
  AVANT la suite ; puis `generate_content()` (mistral-small rapide) → event `content` (slides + photo à
  prendre + CTA + description + hashtags + saves). Events : progress/strategy/content/complete/error.
  Front : `generatePhotoSlide()` lit le flux (reader/TextDecoder), rendu progressif via `renderPhotoSlideResult(data, partial)`.
- **Minuteur visuel** sous le loader (`⏱️ Xs · estimation ~20-40s`) + « ✍️ Rédaction des slides… » pendant l'étape 2.
- Accès : GOLD/AGENCY/BETA/ADMIN (gate back honore tier OU `is_admin` ; front attend `window.__userInfoPromise`).

## 🗓️ ROADMAP AVANT LE 23 JUIN 2026 (demandé par le PO 2026-06-07)
Objectifs « go prod » à boucler avant le 23/06 :
1. [ ] **Google Analytics côté admin** — intégrer GA (mesure trafic/usage) visible dans le back-office admin.
2. [ ] **Emails fonctionnels** (3 types) :
       - regénération mot de passe (existe partiellement via SendGrid `email_service.py` → à valider en prod)
       - **mail de bienvenue** (à câbler à l'inscription)
       - **mail de validation du plan** (à câbler à l'achat/upgrade)
       ⚠️ Dépendance délivrabilité : clé `SENDGRID_API_KEY` prod + auth domaine (SPF/DKIM) + blocage Hostinger
       MailChannels [PSFD] à lever. Sans ça, aucun mail ne part.
3. [ ] **Modifier le mot de passe utilisateur manuellement** (admin → reset/définir le mdp d'un user).
       Base existe (`admin reset-user-password`) → exposer proprement dans le back-office.
4. [ ] **Stripe en PROD** : société créée → `CHECKOUT_ENABLED=true`, clés live, produits/prix, webhook secret,
       customer portal. ⚠️ Aujourd'hui checkout DÉSACTIVÉ tant que la société n'existe pas.
5. [ ] **Nouvelle fonctionnalité** (le PO doit la décrire) — à spécifier.

### Points à NE PAS oublier (flagués par l'assistant)
- [ ] **Webhook Stripe en double à réconcilier** (`main.py` + `stripe_routes.py`) — à régler avant prod paiement.
- [ ] **Pages légales** à compléter si paiement live (CGV, politique de remboursement, mentions Stripe).
- [ ] **Photo Slide** : le PO doit fournir ses **hooks/slides gagnants** → injecter dans les 2 ZONES ÉDITABLES de `photo_slide.py`.
- [ ] **RGPD** : mémoire produits (`analyzed_products`) + `analyzed_insights` anonymisés → vérifier mention politique de confidentialité.
- [ ] (Optionnel) Retirer les endpoints debug admin (`keyapi-selftest`, `analyzed-products`, `video-products` test) avant prod publique — GARDÉS pour l'instant (décision PO).
- [ ] (Différé/PAUSE) TikTok Display API prod (démo + review + clés) — hors scope 23/06 sauf décision.
- [ ] (PAUSE confirmée 2026-06-07) Bouton **audience** = onglet Mon compte → « 📊 Statistiques d'audience »
      (démographie abonnés via provider Business). Code complet, jamais testé en réel (besoin app Business
      approuvée + compte créateur connecté). Hors scope 23/06.

## 📋 Pistes / TODO
- [ ] Tester le bouton **audience (business)** en réel → ajuster `TIKTOK_BIZ_FIELDS` si la démographie ne s'affiche pas.
- [ ] **Repartir de zéro sur les « données marché »** (remplaçant de KeyAPI) — direction à définir.
- [ ] Si Display réactivé : enregistrer la vidéo démo (sandbox) → soumettre review → basculer clés prod.
- [ ] Module croisement **contenu↔perfs réelles** (Display `video.list` + analyse Mistral + agrégat anonymisé) — en attente d'approbation Display.
- [ ] (Backlog ancien) Webhook Stripe en double à réconcilier (`main.py` + `stripe_routes.py`).
- [ ] (User) Ticket Hostinger MailChannels [PSFD] (blocage email).
