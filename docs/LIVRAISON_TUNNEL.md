# Tunnel de vente — livraison (26/10/2026)

Branche `feat/tunnel-vente`, un commit par lot. 173 tests passent en local (dont
40 nouveaux) ; la CI les lance désormais à chaque poussée. Rien n'est en ligne :
la branche n'est ni poussée ni fusionnée.

**Limite importante** : ce poste n'a ni base Supabase ni clés Stripe. Les
migrations ne sont donc **pas appliquées** (fichiers SQL ci-dessous), et ni
Checkout, ni le retour Google, ni l'envoi réel d'un e-mail n'ont pu être joués de
bout en bout. Tout le reste a été vérifié par les tests et à l'écran en 375 px.
Le code fonctionne sans les migrations (replis prévus) : on peut déployer avant
de les jouer.

## 1. Ce qui est fait, lot par lot

### Lot 1 — Mission guidée (`0941263`)
- Carte « Fais ton premier diagnostic en 60 secondes » : vidéo qui vend → TA
  dernière vidéo → 3 accroches pour ton produit (`/scripts`, prérempli avec le
  produit détecté). Un bouton par étape, qui mène directement à l'action.
- Comparatif côte à côte (score, force de l'accroche, moment du CTA, 2 ou 3
  écarts), calculé à partir des deux analyses : aucun appel d'IA en plus.
- Mission terminée : félicitations, puis carte réduite vers le Feed Radar.
- Progression dans la table `trial_mission` (suit l'utilisateur partout).
- **Bug corrigé** : l'ancienne mission lisait `analysis_jobs.email` au lieu de
  `user_email` → l'étape « analyse » n'était jamais validée, le bilan de fin
  d'essai et les e-mails comptaient toujours 0 vidéo.
- Règle d'essai unique « 7 jours, 10 analyses, tous les outils. Sans carte
  bancaire. » (accueil, fenêtres de connexion, tarifs, app), compteur discret
  « Essai : J-4 · 6 analyses restantes », message clair à la limite d'un outil.

### Lot 2 — Verrou et inscription en un clic (`b9cd77e`)
- Le visiteur sans compte ne reçoit plus que le score, le verdict, une force,
  une faiblesse et le début de sa première action. **Avant, le serveur envoyait
  tout** et la page se contentait de masquer.
- Le rapport complet est gardé 48 h et rattaché au compte juste après
  l'inscription (e-mail ou Google), sur la même page, et valide l'étape 1 —
  y compris pour un fichier (perdu à l'inscription avant).
- Fenêtre d'inscription : Google d'abord, puis e-mail + mot de passe, rien de
  plus. Google revient sur la page d'origine, dans la bonne langue.
- **Bug corrigé** : `/app` renvoyait tout visiteur sans session vers l'accueil
  (la boucle décrite dans la mission) — et un retour Google sur `/app` y perdait
  son jeton. `/app` montre maintenant « Commence ton essai gratuit », la
  connexion en dessous, le mot de passe oublié sur place.

### Lot 3 — E-mails d'essai (`9f6c272`)
- Fournisseur : **aucun nouveau** (Resend et SMTP Hostinger déjà branchés).
- Bienvenue, +24 h, jour 3 (vidéo du Feed Radar de son pays, ou passage à la
  création si la mission est faite), jour 6, jour 7 (bilan + paiement direct),
  jour 10, puis plus rien. 7 langues. Journal anti-doublon, arrêt à
  l'abonnement, désinscription respectée.
- Bienvenue désormais envoyée aussi après une inscription Google (il n'y en
  avait aucune).
- **Mode test par défaut** : rien ne part. Textes français à relire :
  [`docs/emails-essai-fr.md`](emails-essai-fr.md).

### Lot 4 — Fin d'essai, offre, paiement (`477d912`)
- Bilan réel (vidéos, leviers, accroches, meilleure note), lignes vides masquées,
  « Continue avec Qeerah Pro » → Stripe Checkout directement.
- Plus de « une seule offre / rien n'est verrouillé / pas de palier ». Pro et
  Agency (sur devis) côte à côte sur `/pricing`, l'accueil et `/pricing/compare` ;
  recharges en option dès 9 €.
- `/pricing` : « 100 analyses par mois », mensuel par défaut (l'annuel affiche
  24,92 €/mois), bouton selon la situation (visiteur → essai + « S'abonner
  directement » ; essai → Checkout ; abonné → son espace).
- `/pricing/compare` et `/temoignages` écrits côté serveur (vides sans
  JavaScript avant). Colonnes Essai / Pro / Agency, uniquement des
  fonctionnalités présentes dans le code.
- Preuve sociale : « +10 créateurs » masqué, « marchés analysés » = la liste
  affichée (7), témoignages visibles à partir de 3 avis publiés.

### Lot 5 — Garder les abonnés (`33df42b`)
- Paiement échoué : bandeau « mets ta carte à jour » (portail Stripe). **Bug
  corrigé** : l'accès était coupé dès le lendemain de la fin de période, alors
  que Stripe relançait encore ; il est maintenant gardé jusqu'à la fin des
  relances.
- « Résilier » → fenêtre : pause 1 mois (vraie pause de facturation Stripe,
  reprise datée, « Reprendre maintenant »), continuer la résiliation (portail,
  2 clics en tout), annuler. Raison facultative enregistrée.
- E-mail hebdo « Ce qui vend cette semaine dans ton pays » : 3 vidéos du Feed
  Radar, le pourquoi tiré d'une analyse existante (jamais inventé), un lien.
  Abonnés et anciens essais. Désinscription de l'hebdo seul + réglage dans
  l'onglet Compte. Mode test par défaut.

### Lot 6 — Mesure (`cc9f158`)
- Table `funnel_events` (événement, langue, détail, sans donnée personnelle).
  Le serveur compte ce dont il est certain ; le navigateur seulement la visite et
  les clics. Requêtes prêtes : [`docs/README_ENTONNOIR.md`](README_ENTONNOIR.md).

## 2. Migrations SQL à jouer (Supabase → SQL Editor), dans cet ordre

1. `supabase_migrations_mission_v2.sql` — table `trial_mission`
2. `supabase_migrations_emails_essai_v2.sql` — table `email_log`, colonne `users.lang`
3. `supabase_migrations_fidelisation.sql` — colonnes `hebdo_opt_out`,
   `paiement_en_retard_depuis`, `pause_fin`, table `cancel_feedback`
4. `supabase_migrations_funnel_events.sql` — table `funnel_events`

Toutes rejouables sans risque, accès refusé à la clé publique (comme `users`).

## 3. Actions manuelles

### Render
- **⚠️ La séquence d'e-mails d'essai est désormais en mode test par défaut.**
  L'ancienne séquence J2/J5/J7 ne part plus tant que `ESSAI_EMAILS_ACTIFS=1`
  n'est pas posé. L'e-mail de bienvenue historique, lui, continue de partir.
- Après relecture des textes : `ESSAI_EMAILS_ACTIFS=1` sur le **service web**
  (bienvenue à l'inscription) **et** sur le cron « upsell-j3 ».
- Cron « upsell-j3 » : passer le planning à `0 * * * *` (chaque heure).
- Nouveau cron « hebdo » : `python3 cron_hebdo.py`, `0 8 * * 1`, mêmes variables
  que « upsell-j3 » ; `HEBDO_ACTIF=1` une fois les textes validés.
- Vérifier la valeur de `FEED_RADAR_REGIONS` : l'e-mail du jour 3 et l'hebdo ne
  montrent que des vidéos du pays de l'utilisateur ; sans données pour son pays,
  le jour 3 renvoie au Feed Radar et l'hebdo ne part pas.

### Stripe (d'abord en mode test)
- Webhook `/api/v1/stripe/webhook` : **ajouter** `customer.subscription.updated`
  et vérifier `invoice.payment_failed` (en plus de `checkout.session.completed`,
  `invoice.paid`, `customer.subscription.deleted`, `charge.refunded`).
- Paramètres → Facturation → Récupération des revenus : relances automatiques
  (Smart Retries), puis **annuler l'abonnement** à la fin des relances (c'est ce
  qui ferme l'accès) ; activer les e-mails Stripe « paiement échoué » et « carte
  bientôt expirée ».
- Portail client : mise à jour du moyen de paiement, factures, résiliation
  (en fin de période conseillée). Inutile d'y activer la pause : l'app la gère
  par l'API, une seconde pause côté portail créerait deux comportements.
- Pied de facture « TVA non applicable, article 293 B du CGI » (déjà signalé
  dans le code : à poser dans le modèle de facture).
- Test de bout en bout en mode test : carte `4242 4242 4242 4242` (paiement),
  `4000 0000 0000 0341` (s'enregistre puis échoue au prélèvement → bandeau).

### E-mails (délivrabilité)
- Domaine d'envoi : enregistrements **SPF** et **DKIM** fournis par Resend (ou
  par Hostinger si l'envoi passe en SMTP), plus un enregistrement **DMARC**.
  `EMAIL_FROM` doit être sur ce domaine vérifié.

### À relire / valider
- Textes des e-mails d'essai : [`docs/emails-essai-fr.md`](emails-essai-fr.md).
- Textes de l'hebdo : dans `hebdo.py` (`TEXTES["fr"]`).

## 4. `TODO DOPE:` — à trancher

1. **Offre Agency** : contenu exact (rien n'est listé, aucune fonctionnalité
   inventée). La colonne Agency du comparatif reprend l'ancien tableau : à confirmer.
2. **FAQ et données structurées de l'accueil** : gardent l'ancienne formulation
   de l'essai (« 7 jours d'accès complet… ») car le référencement les lit.
   Aligner sur la règle unique ?
3. **« plus de 10 créateurs TikTok Shop FR confirmés »** : le chiffre est masqué
   dans les statistiques, mais la phrase au-dessus le dit encore. La garder ?
4. **« 7 marchés analysés »** : confirmer les 7 pays du corpus d'analyse.
5. **« 30 crédits IA par mois »** affichés sur `/pricing` : marqués « à
   confirmer » dans le code depuis l'ancienne grille.
6. **« Structures gagnantes »** : servies seulement aux anciens niveaux gold /
   agency / beta, pas à Pro (retirées du comparatif). Les ouvrir à Pro ?
7. **Mention « Tes données vidéo restent TOUJOURS en local »** (bandeau cookies
   de l'app, bandeau de confiance « restent EN LOCAL, jamais envoyées », note de
   confidentialité) : **fausse**. Rien changé, comme demandé :
   - fichier, essai et abonnés : la vidéo **entière** est envoyée au serveur
     (`/analyze`, `/api/jobs/create-upload`) puis à Gemini ;
   - fichier, ancien chemin : 6 images et l'audio partent au serveur puis aux
     fournisseurs d'IA ;
   - lien : le serveur télécharge la vidéo et l'envoie à Gemini ;
   - vrai : les fichiers temporaires sont supprimés après l'analyse ; le
     résultat (texte) est conservé dans « Mes analyses » et le cache.
8. **Témoignages** : 2 publiés → la section reste masquée jusqu'au 3e.
9. **Prix hors zone euro**, incohérences relevées (aucun prix créé) :
   - l'accueil affiche un ordre de grandeur en US$, £, R$, MX$ (taux fixes dans
     `homepage_i18n.FX`, à rafraîchir) ; `/pricing` n'affiche que des euros ;
   - la mention fiscale diffère : neutre sur l'accueil hors UE (« prélevé en
     euros »), explication de la franchise française sur `/pricing` ;
   - en ES / IT / DE, l'accueil dit « IVA / MwSt. incl. » alors que la TVA ne
     s'applique pas (293 B) — équivalent de « TTC », mais ambigu.
10. **Pages encore en français seulement** (avant ce travail aussi) :
    `/scripts`, `/carousel`, `/temoignages`, la page de désinscription.

## 5. Captures mobiles (375 px)

Dans [`docs/captures-tunnel/`](captures-tunnel/) :
`01-resultat-partiel` · `02-fenetre-inscription` · `02b-porte-entree-app` ·
`03-carte-mission` · `04-comparatif-mission` · `05-bilan-fin-essai` ·
`06a-tarifs-haut` · `06b-tarifs-offres` · `07-comparatif-tarifs-de` ·
`08-resiliation-et-paiement`.

Les captures de la mission, du comparatif et du bilan utilisent des données
simulées (pas de base sur ce poste) ; la mise en page est celle du code livré.
