# Brief — Choix du meilleur fournisseur de données TikTok Shop pour Qeerah

> **But de ce document** : servir de cahier des charges autonome pour qu'une
> session Claude (ou un dev) puisse évaluer et choisir la meilleure API de
> données TikTok Shop, sans avoir besoin du contexte de la conversation
> d'origine. Tout ce qu'il faut savoir est ici : ce qu'on veut récupérer, ce
> que le fournisseur actuel (KeyAPI) fait et NE fait pas, les critères de
> sélection, et un protocole de test avec des comptes réels comme étalon.
>
> Rédigé le 2026-07-03 après investigation live approfondie de KeyAPI.

---

## 1. Contexte produit

**Qeerah** (qeerah.com, société DOPE VENTURES) est un SaaS d'aide aux créateurs
et vendeurs **TikTok Shop**. Public cible principal : créateurs / affiliés
**francophones** (marché France) + marchés internationaux. Trois features
dépendent d'une API de données TikTok Shop tierce :

1. **Recherche de profil** — l'utilisateur tape un `@handle` TikTok → doit voir
   son **GMV réel des 30 derniers jours** + ses meilleures ventes / vitrine.
   (Type Kalodata.) Fonctionne pour N'IMPORTE quel handle, pas seulement les
   comptes classés.
2. **Créateurs Gagnants** — classement des meilleurs créateurs/vendeurs par
   marché et par catégorie, avec leur GMV, leurs produits, leurs vidéos.
3. **Feed Radar** — feed des vidéos TikTok Shop virales du moment, avec GMV
   estimé par vidéo, tendance du créateur, thumbnail.

**Le besoin nº1, non négociable : la FRAÎCHEUR (données à J-1) et la
COUVERTURE DES CRÉATEURS FRANÇAIS DOMESTIQUES.** C'est précisément là que le
fournisseur actuel (KeyAPI) échoue (voir §4).

---

## 2. Données à récupérer (cahier des charges fonctionnel)

Par ordre de priorité pour Qeerah :

### 2.1 — CRITIQUE : GMV par créateur (fenêtre glissante 30j + série quotidienne)
- Entrée : un `@handle` OU un identifiant créateur.
- Sortie attendue : GMV total sur 30 jours glissants + série jour par jour
  (pour sparkline), **frais jusqu'à J-1**.
- **Doit marcher pour un créateur/affilié français lambda**, pas seulement les
  tops classés ni les vendeurs cross-border.
- Doit être le GMV **attribué au créateur** (ce que SES vidéos/lives ont généré),
  pas le GMV global du produit tous vendeurs confondus.

### 2.2 — Résolution de profil
- `@handle` → identifiant interne + profil : nickname, avatar, followers,
  nb de vidéos, bio. Gérer proprement un handle inexistant.

### 2.3 — Produits d'un créateur (vitrine)
- Liste des produits qu'un créateur met en avant, idéalement **avec une date de
  publication / mise en avant** (pour trier par récence — KeyAPI ne l'a pas).
- Par produit : nom, image, prix, ventes, GMV. Idéalement le GMV **attribué à
  ce créateur** pour ce produit (pas le GMV global du produit).

### 2.4 — Classements créateurs par marché/catégorie
- Top créateurs par région (9 marchés visés, cf. §3) et par catégorie, triables
  par ventes/GMV. **Doit distinguer / permettre de filtrer les vrais créateurs
  du marché local** (ex : vrais créateurs FR) vs les vendeurs cross-border.
- Granularité temporelle : jour / semaine / mois.

### 2.5 — Classements produits par marché/catégorie
- Top produits qui se vendent, par région/catégorie : nom, image, prix, ventes,
  GMV, **vraie URL produit** (pas juste un ID).

### 2.6 — Données par vidéo (pour Feed Radar)
- Découverte des vidéos virales TikTok Shop + par vidéo : vues, likes,
  commentaires, partages, thumbnail, URL.
- **IDÉAL (KeyAPI ne l'a pas) : GMV attribué PAR VIDÉO** et le **produit taggé
  dans la vidéo**. Aujourd'hui on est obligés d'ESTIMER le GMV vidéo par calcul
  (vues × CTOR × prix moyen) faute d'attribution réelle — une API qui donne le
  GMV réel par vidéo serait un game-changer pour cette feature.

### 2.7 — Recherche produit + fiche produit
- Recherche de produits par mot-clé, par région. Fiche produit : titre, image,
  prix, ventes, note, vraie URL d'achat.

---

## 3. Marchés (régions) à couvrir

Actuellement 9 marchés, **FR en priorité absolue** (cœur de cible) :
`FR, US, GB, BR, DE, ES, IT, ID, MY`.

Un bon fournisseur couvre au minimum ces 9, avec **le TikTok Shop domestique
français inclus dans la couverture GMV** (le point de blocage KeyAPI).

---

## 4. État des lieux KeyAPI (`https://api.keyapi.ai`) — ce qui marche et ce qui bloque

Fournisseur actuel. Token via env `KEYAPI_TOKEN`. Modèle à crédits (~20 000
crédits/mois dans notre offre). Endpoints intégrés dans `market_creators.py`.

### 4.1 — Ce qui MARCHE chez KeyAPI
- `/v1/tiktok/influencer/detail?unique_id=` → handle → uid + profil. ✅
  (handle inexistant = HTTP 200 avec body `"unique_id is invalid"`, pas un 404).
- `/v1/tiktok/influencer/ranking/analytics` → classements créateurs par région.
  Params : `date`, `region`, `rank_type` (1=jour, 2=semaine, 3=mois),
  `influencer_rank_field` (1=followers, 2=ventes ; 3+ = erreur 400),
  `category_id`, pagination `page_num`/`page_size` (max 10). ✅
- `/v1/tiktok/influencer/trends/analytics?user_id=&start_date=&end_date=` →
  série GMV/ventes QUOTIDIENNE par créateur (page_size max 10 → pagination).
  **SEULE source d'un GMV daté.** Marche BIEN pour les comptes couverts. ✅/⚠️
- `/v1/tiktok/influencer/products/analytics?user_id=` → produits de la vitrine
  d'un créateur (ordre natif = ordre vitrine). ✅ MAIS voir limites §4.2.
- `/v1/tiktok/influencer/videos?unique_id=` → vidéos d'un créateur (aweme_list
  avec create_time, stats, cover, share_url). ✅
- `/v1/tiktok/product/ranking/analytics`, `/v1/tiktok/realtime/product/search`,
  `/v1/tiktok/realtime/product/detail_new_app` → produits + vraie URL. ✅
  (detail_new_app renvoie parfois 500 sur des produits FR.)
- **Fraîcheur** : J-1 pour les comptes couverts (testé le 03/07 : vendeurs
  cross-border frais jusqu'au 02/07).

### 4.2 — Ce qui BLOQUE chez KeyAPI (limites PROUVÉES en live 2026-07-03)

**🔴 BLOQUANT Nº1 — Pas de GMV pour les créateurs français domestiques.**
C'est LA raison de ce brief. Testé exhaustivement :
- Scan de 150 comptes du classement FR → 50 vrais créateurs francophones
  (lang=fr) identifiés. **Les 50 ont un GMV à ZÉRO sur TOUS les jours récents**
  (ex. testés jour par jour du 19/06 au 01/07 : 0 partout), alors que KeyAPI
  renvoie bien leurs jours et leurs métriques sociales (vues/abonnés fraîches).
- En parallèle, les vendeurs **cross-border** (asiatiques qui vendent sur le
  marché FR : @hannaholala, @mrdealsdaily) ont un GMV réel et frais à J-1.
- **Interprétation** : le GMV de KeyAPI est spécifique à certains marchés ; le
  **TikTok Shop domestique français n'est PAS couvert**. Les cross-border ont du
  GMV car leur marché d'origine (SEA…) l'est. Testé sous tous les angles
  (rank_field, rank_type jour/semaine/mois, 15 pages de profondeur, lookup par
  handle direct) : les créateurs FR domestiques sont uniformément à 0.
- Cas concret : @thedopeman99 (compte d'Aimeric, vend réellement) → GMV KeyAPI
  gelé au 24/05 puis 0, alors qu'il confirme vendre. @gerald.atk pareil, gelé au
  22/05. Deux comptes FR qui se figent à ~2 jours d'écart = coupure systémique,
  pas un arrêt réel des ventes.

**🔴 GMV par créateur = seulement la cohorte "couverte", pas tout le monde.**
`trends/analytics` renvoie 0 pour les comptes hors couverture (dont FR
domestique). La feature Recherche promet "n'importe quel handle" mais ne délivre
un vrai GMV que pour les comptes couverts (surtout cross-border + tops classés).

**🔴 Aucune attribution GMV par VIDÉO.**
`/v1/tiktok/video/products/analytics` et `/v1/tiktok/video/trends/analytics`
renvoient VIDE (testé sur 10 vraies vidéos). Les tags produit DANS les objets
vidéo (`products_info`, `right_products`, `bottom_products`) sont TOUJOURS
VIDES. `anchors` ne contient que des effets/filtres, pas les produits shop.
→ Impossible de relier une vidéo à son produit ni d'avoir son GMV réel. On est
forcés d'estimer (vues × CTOR 0.04% × prix moyen).

**🟠 GMV produit = GLOBAL, pas la part du créateur.**
`total_sale_gmv_amt` de `products/analytics` est le GMV du produit TOUS vendeurs
confondus (ex : "598k$" sur @thedopeman99 incluait 216k$ d'un produit à 1 seule
vidéo ; @hannaholala sommait à 3,55M$ pour ~211k$/30j réels). Le champ
d'attribution `total_video_sale_gmv_amt` est à 0 partout. → On ne peut pas
montrer le GMV lifetime réel d'un créateur.

**🟠 Aucune date de publication produit.**
`products/analytics` n'a aucun champ date ; params de tri (`sort_field`,
`order`, `product_rank_field`) IGNORÉS. → Impossible de trier les produits d'un
créateur par récence (on garde l'ordre natif de la vitrine comme proxy).

**🟠 Historique limité à ~6-7 mois.**
`trends/analytics` ne renvoie rien au-delà (~J-210+ = 0 ligne).

**🟠 Classement "region=FR" ≠ créateurs français.**
`region=FR` = vendeurs sur le MARCHÉ français, dominé par des cross-border
(vietnamiens, portugais, indonésiens…). Pas de filtre "nationalité créateur".

---

## 5. Critères de sélection d'un nouveau fournisseur (checklist)

Un bon candidat doit cocher, par ordre d'importance :

1. **✅ GMV frais (J-1) pour les créateurs FRANÇAIS domestiques** — le test qui
   élimine KeyAPI. NON négociable.
2. **✅ GMV par créateur pour un handle arbitraire** (pas seulement les tops
   classés) — fenêtre 30j glissante + série quotidienne.
3. **✅ Couverture des 9 marchés** (FR, US, GB, BR, DE, ES, IT, ID, MY), FR en
   priorité.
4. **✅ Attribution GMV correcte** : la part du créateur, distincte du GMV global
   produit.
5. **⭐ GMV / produit attribué PAR VIDÉO** (bonus fort — débloque Feed Radar en
   données réelles au lieu d'estimations).
6. **✅ Classements créateurs & produits** par marché/catégorie, granularité
   jour/semaine/mois, avec possibilité de cibler les créateurs locaux.
7. **✅ Fiche produit avec vraie URL d'achat + images.**
8. **✅ Date de publication / mise en avant produit** (bonus : tri par récence).
9. **✅ Historique > 6-7 mois** (bonus).
10. **Pragmatique** : API REST documentée, tarif/crédits raisonnables, rate
    limits vivables, stabilité (peu de 500), auth simple par token.

---

## 6. Fournisseurs candidats à évaluer

- **Kalodata** (PRIORITÉ — a manifestement la donnée FR domestique fraîche ;
  vérifier s'ils exposent une API publique/entreprise et son tarif).
- **FastMoss** — data TikTok Shop créateurs/produits, réputé large couverture.
- **Shoplus** — analytics TikTok Shop multi-marchés.
- **EchoTik** — data créateurs/produits/vidéos TikTok Shop (à ne pas confondre
  avec le host `echosell` des images KeyAPI).
- **Pipiads / TikRank / Sortlist-like** — à cribler selon la checklist §5.
- **KeyAPI** (actuel) — à garder comme fallback pour ce qu'il fait bien
  (cross-border, classements, produits) si on adopte un second fournisseur juste
  pour le GMV FR domestique.

Question clé à poser à chaque fournisseur (ou à tester) : **"Renvoyez-vous le
GMV quotidien à J-1 d'un créateur/affilié TikTok Shop FRANÇAIS domestique
donné ?"** — avec les comptes de test du §7.

---

## 7. Protocole de test (étalon avec comptes réels)

Pour valider N'IMPORTE quelle API candidate, tester ces handles et comparer aux
résultats connus KeyAPI (03/07/2026). Un bon fournisseur doit donner du GMV
récent et non nul là où KeyAPI donne 0.

| Handle | Type | Résultat KeyAPI (référence) | Attendu d'un bon fournisseur |
|---|---|---|---|
| `@thedopeman99` | Affilié FR (compte d'Aimeric, vend réellement) | GMV gelé au 24/05 puis 0 | GMV réel récent > 0 |
| `@gerald.atk` | Affilié FR | GMV gelé au 22/05 | GMV réel récent > 0 |
| `@monhijabpascher` | Créatrice FR (lang=fr) | 0 sur tous les jours récents | GMV réel > 0 |
| `@khadija__lifestyle` | Créatrice FR | 0 sur tous les jours récents | GMV réel > 0 |
| `@delicesbysm` | Créatrice FR | 0 sur tous les jours récents | GMV réel > 0 |
| `@marine__mkdm` | Créatrice FR | 0 sur tous les jours récents | GMV réel > 0 |
| `@hannaholala` | Cross-border (VN→FR) | GMV frais à J-1 (~211k$/30j) | GMV frais (contrôle positif) |
| `@mrdealsdaily` | Cross-border (→FR) | GMV frais à J-1 | GMV frais (contrôle positif) |

**Critère de succès** : le fournisseur renvoie un GMV quotidien récent (< 7
jours) et cohérent pour au moins les 6 comptes FR, là où KeyAPI renvoie 0.

Vérifier aussi : couverture des 9 marchés, présence de l'attribution GMV/vidéo,
tarif au volume, rate limits.

---

## 8. Où c'est branché dans le code (pour l'intégration)

- Toute la couche KeyAPI est isolée dans **`market_creators.py`** (`_get()` =
  client HTTP avec circuit-breaker sur quota). Un nouveau fournisseur se
  branche là, idéalement derrière la même interface de fonctions
  (`get_influencer_profile`, `get_creator_gmv_30d`, `get_creator_best_sellers`,
  `get_top_creators`, `get_top_products`, etc.) pour ne pas toucher aux routes.
- Feed Radar : **`feed_radar.py`** (importe `market_creators`).
- Les features consommatrices : routes `/api/recherche/profile`,
  `/api/market/*`, `/api/feed-radar*` dans `main.py`.
- Stratégie recommandée si on ajoute un 2e fournisseur : router par besoin —
  GMV créateur FR domestique → nouveau fournisseur ; classements/produits/
  cross-border → garder KeyAPI tant qu'il fait le job.
