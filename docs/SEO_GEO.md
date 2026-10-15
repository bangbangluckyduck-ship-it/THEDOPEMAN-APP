# Moteur de contenu SEO & GEO — mode d'emploi

> Mis en place le 15/10/2026 à partir du brief « Qeerah — Brief SEO & GEO ».
> Objectif : un canal d'acquisition passif (Google + citations par les IA) qui
> tourne pendant que le démarchage est en pause.

---

## 1. Ce qui est en place

| Brief | État | Où |
|---|---|---|
| Blog sur le domaine principal (`/blog`, `/blog/[slug]`) | ✅ | `main.py`, `blog_articles.py` |
| Rendu HTML côté serveur (lisible sans JS par Google et les crawlers IA) | ✅ construit une fois au démarrage | `blog_articles.construire()` |
| Gabarit d'article unique : 1 seul H1, chapô-réponse, sommaire ancré, H2 en questions, FAQ, CTA, articles liés, sources | ✅ | `templates/blog_article.html` |
| Title ≤ 60, description ≤ 155, canonique, Open Graph, Twitter | ✅ vérifiés automatiquement | `blog_articles.controler()` |
| **Huit langues** (fr, en, en-ie, pt-br, es, es-mx, it, de), un slug par marché, hreflang réciproques | ✅ | `content/blog/<id>/<langue>.html` |
| Schema.org : Article + BreadcrumbList + FAQPage par article, Organization (accueil + À propos, même `@id`), ItemList sur `/blog` | ✅ | |
| Sitemap XML auto (toutes les langues, avec `lastmod`) | ✅ | `/sitemap.xml` |
| robots.txt (crawlers IA autorisés) + llms.txt (liste les guides automatiquement) | ✅ | `/robots.txt`, `/llms.txt` |
| Maillage interne (articles liés + liens `guide:` dans le texte) | ✅ | |
| Core Web Vitals : pas d'image, pas de police externe, CSS inline minimal, scripts en `defer` | ✅ | |
| Tests (checklist, langues, hreflang, sitemap, liens) dans la CI | ✅ | `test_blog_articles.py` |
| **Google Search Console** : soumettre `https://www.qeerah.com/sitemap.xml` | ⬜ **à faire par toi** | search.google.com/search-console |
| **Suivi des positions** sur les requêtes cibles | ⬜ **à faire par toi** | Search Console › Performances, filtrer par page |
| **Présence externe** (Reddit, annuaires SaaS, comparatifs) | ⬜ **à faire par toi** | cf. §5 |

---

## 2. Publier un article (workflow récurrent)

1. **Choisir la requête** dans le backlog (§4), la plus haute non faite.
2. **Demander à Claude Code**, par exemple :

   > Écris le guide « *quel produit choisir pour vendre sur TikTok Shop* » en suivant
   > docs/SEO_GEO.md : dossier `content/blog/choisir-produit/`, les six langues
   > rédigées, chiffres sourcés uniquement (aucun chiffre inventé ; un exemple
   > fictif doit être signalé comme tel), CTA vers la fonctionnalité Qeerah la plus
   > proche, liens vers 2 guides existants. Puis lance `test_blog_articles.py`.

3. **Relire le français** (c'est la version de référence) et vérifier les chiffres
   contre les sources.
4. **Lancer les tests** : `venv\Scripts\python.exe test_blog_articles.py` → tout doit être `ok`.
5. **Déployer** (push → Render). Le sitemap, `/blog`, `llms.txt` et les hreflang
   se mettent à jour seuls.
6. **Search Console** : « Inspection de l'URL » sur la version française → « Demander une indexation ».
7. **Cocher la requête** dans le backlog (§4).

Rythme visé : 1 à 2 articles par créneau libre.

---

## 3. Format d'un article

```
content/blog/<id>/
  article.json      métadonnées communes + par langue
  fr.html           corps (fragment HTML, SANS <h1>)
  en.html  pt-br.html  es.html  it.html  de.html
```

`en-ie` et `es-mx` réutilisent automatiquement `en` et `es` (URL et hreflang propres).

### article.json

```json
{
  "requete": "requête cible française",
  "intention": "transactionnelle | mixte | informationnelle | comparative",
  "publie": "2026-10-15",
  "maj": "2026-10-15",
  "lecture_min": 7,
  "cta": "analyse",                    // clef de blog_articles.CTA
  "lies": ["id-guide-1", "id-guide-2"],// 1 à 2 guides existants
  "brouillon": false,                  // true = non publié
  "sources": [{"titre": "…", "url": "…"}],
  "langues": {
    "fr": {
      "slug": "requete-cible-en-tirets",
      "titre": "≤ 60 caractères, requête incluse",
      "h1": "Le titre affiché, contient la requête",
      "description": "70 à 155 caractères, incitative",
      "categorie": "📊 MÉTHODE",
      "chapo": "LA réponse directe à la question, en 2-3 phrases. C'est la phrase que les IA extraient.",
      "faq": [{"q": "Question ?", "r": "Réponse autonome, citable telle quelle."}]
    },
    "en": { … }, "pt-br": { … }, "es": { … }, "it": { … }, "de": { … }
  }
}
```

### Corps (`fr.html`, etc.)

- **Pas de `<h1>`** : le gabarit le pose à partir de `h1`.
- Chaque section : `<h2 id="ancre">Titre sous forme de question ?</h2>` — l'`id` alimente le sommaire. 3 minimum.
- Lien vers un autre guide : `<a href="guide:<id>">…</a>` (résolu dans la bonne langue).
- Lien vers une page du site : chemin **français** (`/pricing`, `/analyser-une-video-tiktok-shop`) — préfixé automatiquement pour les autres langues.
- Blocs disponibles : `<div class="tableau"><table>…</table></div>`, `<div class="encadre">`, `<div class="exemple">` (pour les exemples chiffrés fictifs, toujours signalés comme tels).
- 800 à 1 700 mots en français (vérifié).

### Règles de contenu (GEO)

- **Réponse dans le chapô**, en une phrase nette.
- **H2 en questions**, listes, tableaux : facile à citer tel quel.
- **Chiffres sourcés uniquement**, avec le lien dans le texte. Jamais de chiffre inventé ;
  un exemple de calcul avec des chiffres fictifs est autorisé s'il est annoncé comme tel.
- **« Qeerah » écrit de la même façon partout**, et décrit de la même façon : outil
  d'analyse de vidéos TikTok Shop par IA.
- **Pas de cannibalisation** : vérifier qu'aucune page existante ne vise déjà la requête
  (cf. pages d'atterrissage `/analyser-une-video-tiktok-shop`,
  `/pourquoi-ma-video-tiktok-shop-ne-fait-pas-de-vues`,
  `/produits-qui-vendent-tiktok-shop-france`). Si oui, choisir un angle distinct et lier
  les deux pages.

### Ajouter un appel à l'action

Les CTA vivent dans `blog_articles.CTA` (titre, texte, bouton × 6 langues + chemin).
Ajouter une clef (ex. `"scripts"` → `/scripts`) avant de l'utiliser dans un `article.json`.

---

## 4. Backlog des requêtes

Légende : ✅ publié · ⬜ à faire · ⚠️ à arbitrer (risque de doublon avec une page existante)

### Lot 1 (brief, Partie 2)

| | Requête cible | Angle | Intention | Guide |
|---|---|---|---|---|
| ✅ | analyser ses vidéos TikTok Shop | Lire ses propres stats comme un entonnoir (distinct de la page `/analyser-une-video-tiktok-shop`, qui décortique n'importe quelle vidéo) | Transactionnelle | `analyser-ses-videos` |
| ✅ | comment analyser ses hooks TikTok Shop | Mesurer, décortiquer en 4 couches, 6 types, exemple chiffré | Transactionnelle | `analyser-ses-hooks` |
| ✅ | améliorer ses résultats TikTok Shop | Les 5 leviers et l'ordre pour les travailler | Mixte | `ameliorer-resultats` |
| ⚠️ | pourquoi mes vidéos TikTok Shop ne vendent pas | Diagnostic vues sans ventes. Proche de `/pourquoi-ma-video-tiktok-shop-ne-fait-pas-de-vues` (qui traite des **vues**) : angle « ventes » uniquement, lier les deux | Informationnelle | |
| ⬜ | réussir sur TikTok Shop en affiliation | Guide complet débutant | Informationnelle | |
| ⬜ | meilleurs outils d'analyse TikTok Shop | Comparatif honnête où Qeerah figure (critères, prix publics, limites de chacun) | Comparative | |
| ⬜ | combien gagnent les créateurs TikTok Shop | Données de marché **sourcées**. Ne jamais segmenter les revenus par nombre d'abonnés : sur TikTok Shop, les ventes dépendent des vidéos et des produits, pas de la taille du compte (cf. §6) | Informationnelle | |

### Créateurs

| | Requête |
|---|---|
| ⬜ | quel produit choisir pour vendre sur TikTok Shop |
| ⬜ | combien de vidéos par jour pour percer sur TikTok Shop |
| ⬜ | comment être accepté dans le programme d'affiliation TikTok Shop |
| ⚠️ | pourquoi j'ai des vues mais pas de ventes sur TikTok Shop (fusionner avec « ne vendent pas ») |
| ⚠️ | comment trouver des produits qui se vendent sur TikTok Shop (proche de `/produits-qui-vendent-tiktok-shop-france`) |
| ⬜ | comment écrire un script de vidéo TikTok Shop *(ajout — CTA vers `/scripts`)* |
| ⬜ | exemples de hooks TikTok Shop par catégorie *(ajout)* |
| ⬜ | faire un carrousel photo TikTok Shop qui vend *(ajout — CTA vers `/carousel`)* |
| ⬜ | vidéo ou live : que choisir sur TikTok Shop *(ajout)* |
| ⬜ | quelle commission en affiliation TikTok Shop selon la catégorie *(ajout)* |

### Marques

| | Requête |
|---|---|
| ⬜ | comment lancer sa boutique TikTok Shop |
| ⬜ | comment recruter des créateurs affiliés sur TikTok Shop |
| ⬜ | quelle commission proposer aux affiliés TikTok Shop |
| ⬜ | comment gérer les échantillons produits pour les créateurs |
| ⬜ | comment mesurer le ROI d'une campagne TikTok Shop |
| ⬜ | comment briefer un créateur TikTok Shop *(ajout)* |

### Agences

| | Requête |
|---|---|
| ⬜ | comment gérer plusieurs créateurs TikTok Shop |
| ⬜ | quels KPI suivre pour un client TikTok Shop |
| ⬜ | comment scaler une campagne d'affiliation TikTok Shop |
| ⬜ | comment facturer une prestation TikTok Shop |
| ⬜ | modèle de reporting mensuel TikTok Shop pour un client *(ajout)* |

---

## 5. Présence externe (GEO) — à faire hors du site

Les IA recommandent ce qui est cité **ailleurs**. Par ordre d'effort/impact :

1. **Annuaires SaaS** : Product Hunt, G2, Capterra, SaaSHub, AlternativeTo, There's An AI For That, Futurepedia — fiche avec la même description d'une phrase partout.
2. **Listes « meilleurs outils TikTok Shop »** : contacter les auteurs des articles qui sortent en tête sur cette requête (FR et EN) pour être ajouté.
3. **Reddit** (r/TikTokShop, r/TikTokshopsellers, r/Affiliatemarketing) : répondre utilement avec la méthode des guides ; lien seulement quand il répond à la question.
4. **Profils Qeerah** cohérents (TikTok, LinkedIn de Dope Ventures) : même nom, même phrase de présentation que `llms.txt`.

Phrase de présentation à réutiliser telle quelle :
> Qeerah est un outil d'analyse de vidéos TikTok Shop par IA : il explique pourquoi une vidéo vend — accroche, rétention, déclencheurs psychologiques, appel à l'action — et quoi reproduire.

---

## 6. Points relevés pendant la mise en place

- ✅ **Corrigé le 16/10/2026** (phrase et source Branvas retirées en FR, EN et dans les
  traductions). Pour mémoire, l'article `/blog/expansion-mondiale-tiktok-shop` (et sa FAQ, son
  JSON-LD et la version anglaise) attribue à Branvas « le créateur médian gagne environ
  200 $/mois ». Vérifié le 15/10/2026, la page Branvas ne donne pas de médiane — seulement
  des fourchettes par palier d'abonnés, une grille sans valeur : sur TikTok Shop, les revenus
  ne dépendent pas du nombre d'abonnés (une vidéo est poussée par l'algorithme à des
  non-abonnés, un petit compte peut vendre plus qu'un gros). Branvas est donc à retirer comme
  source, et la phrase à supprimer : c'est exactement le type de chiffre que les IA reprennent.
- **Règle éditoriale** : aucun guide ne présente le nombre d'abonnés comme un facteur de
  revenus ou un prérequis pour vendre.
- Les pages d'atterrissage existantes restent en place ; les guides pointent vers elles.
