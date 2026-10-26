# E-mails d'essai — textes à relire (français)

Signés « Aimeric — Qeerah ». Un seul bouton par e-mail, plus le lien de désinscription en pied :
« Tu reçois cet e-mail parce que tu as un compte Qeerah. Ne plus recevoir ces e-mails. »

**Rien ne part tant que `ESSAI_EMAILS_ACTIFS=1` n'est pas posé sur Render** : en attendant, chaque e-mail est écrit en entier dans les journaux du cron.

Exemple de bilan utilisé (jours 6 et 7) : 8 vidéos, 14 leviers, 9 accroches, meilleure note 74/100. Seules les lignes où il y a une donnée réelle apparaissent ; sans aucune donnée, une variante sans bilan part à la place (indiquée ci-dessous).

## À l'inscription (toujours)

**Objet :** ton compte qeerah est prêt

> Salut,
> Ton compte est prêt. Ta mission tient en 3 étapes et te montre, en quelques minutes, ce qui sépare ta vidéo d'une vidéo qui vend.
> Prochaine étape : analyse une vidéo qui vend.
> Aimeric — Qeerah

**Bouton :** Continuer ma mission → /app?mission=<prochaine étape> (champ ou outil déjà ouvert)

## +24 h, s'il n'a pas analysé SA vidéo

**Objet :** où tes spectateurs décrochent

> Salut,
> Analyse ta dernière vidéo : tu vas voir à quelle seconde les gens décrochent, et ce qui la sépare d'une vidéo qui vend.
> Aimeric — Qeerah

**Bouton :** Analyser ma dernière vidéo → /app?mission=2 (champ du lien ouvert)

## Jour 3, mission non terminée (vidéo du Feed Radar de son pays)

**Objet :** une vidéo qui vend en ce moment

> Salut,
> Cette vidéo de @lestrouvaillesdecaro vend en ce moment (28 403 956 vues).
> Analyse-la : tu vas comprendre pourquoi elle marche, et ce que tu peux reproduire dans la tienne.
> Aimeric — Qeerah

**Bouton :** Analyser cette vidéo → /app?analyser=<lien de la vidéo> (analyse préremplie)

## Jour 3, mission non terminée, aucune vidéo collectée dans son pays

**Objet :** ce qui vend en ce moment

> Salut,
> Ouvre le Feed Radar, choisis une vidéo qui vend en ce moment et analyse-la : tu vas comprendre pourquoi elle marche, et ce que tu peux reproduire dans la tienne.
> Aimeric — Qeerah

**Bouton :** Voir ce qui vend → /app?onglet=feedradar

## Jour 3, mission terminée

**Objet :** de l'analyse à ta prochaine vidéo

> Salut,
> Tu as terminé ta mission : tu sais ce qui sépare ta vidéo d'une vidéo qui vend.
> Prochaine étape : en faire ta prochaine vidéo. Prends un produit, génère plusieurs angles, et teste deux accroches différentes cette semaine.
> Aimeric — Qeerah

**Bouton :** Écrire mes prochaines accroches → /scripts

## Jour 6, essai actif, non abonné

**Objet :** ton essai se termine demain

> Salut,
> Pendant ton essai, tu as analysé 8 vidéos, identifié 14 leviers de vente et généré 9 accroches. Ta meilleure vidéo : 74/100.
> Ton essai se termine demain. Tes analyses restent accessibles ensuite.
> Aimeric — Qeerah

**Bouton :** Ouvrir mon espace → /app

*Variante sans aucune donnée :*

> Ton essai se termine demain. Il te reste le temps d'analyser une vidéo qui vend, puis la tienne.

## Jour 7, essai expiré, non abonné

**Objet :** ton essai en chiffres

> Salut,
> Pendant ton essai, tu as analysé 8 vidéos, identifié 14 leviers de vente et généré 9 accroches. Ta meilleure vidéo : 74/100.
> Ton essai est terminé. Pour continuer à comprendre ce qui vend chaque mois, continue avec Qeerah Pro : 29,99 € par mois, sans engagement.
> Aimeric — Qeerah

**Bouton :** Continuer avec Qeerah Pro → Stripe Checkout direct (lien signé, e-mail prérempli)

*Variante sans aucune donnée :*

> Ton essai est terminé. Avec Qeerah Pro, tu comprends chaque mois pourquoi les vidéos TikTok Shop vendent, et quoi reproduire dans les tiennes : 29,99 € par mois, sans engagement.

## Jour 10, toujours pas abonné (dernier e-mail)

**Objet :** une dernière chose

> Salut,
> C'est mon dernier message à ce sujet. Si tu veux reprendre là où tu t'es arrêté, ton compte et tes analyses t'attendent.
> Aimeric — Qeerah

**Bouton :** Reprendre avec Qeerah Pro → Stripe Checkout direct (lien signé, e-mail prérempli)
