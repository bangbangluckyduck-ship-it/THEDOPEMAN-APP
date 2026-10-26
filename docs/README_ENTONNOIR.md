# Mesurer le tunnel de vente

Les événements du tunnel sont dans la table `funnel_events` (migration
`supabase_migrations_funnel_events.sql`). Une ligne = un événement : son nom, la
langue du visiteur ou du compte, un détail court, l'heure. **Aucune donnée
personnelle** (ni e-mail, ni IP, ni identifiant) : c'est une mesure d'audience
exemptée de consentement, indépendante du bandeau cookies.

On compte des **événements**, pas des personnes : la visite et le clic « Analyser »
sont dédoublonnés par onglet, le reste est compté côté serveur une seule fois
(une inscription, une étape de mission, un paiement).

## Les événements

| Événement | Compté par | Détail |
|---|---|---|
| `visite_accueil` | navigateur (une fois par onglet) | — |
| `analyse_anonyme_lancee` | serveur | `lien` ou `fichier` |
| `resultat_affiche` | serveur (résultat partiel servi) | `url` ou `upload` |
| `clic_debloquer` | navigateur | — |
| `inscription` | serveur | `email` ou `google` |
| `mission_etape_1` · `_2` · `_3` | serveur (première validation) | — |
| `mission_terminee` | serveur (les 3 étapes) | — |
| `essai_expire` | serveur (cron horaire, une fois par compte) | — |
| `checkout_ouvert` | serveur (session Stripe créée) | `mensuel` ou `annuel` |
| `abonnement` | serveur (webhook Stripe) | `mensuel` ou `annuel` |
| `paiement_echoue` · `pause` · `resiliation` | serveur | — |
| `email_envoye` · `email_clique` | serveur | clé de l'e-mail (`h24`, `j7`, `hebdo`…) |
| `cta_clic` · `feedradar_decrypter` | navigateur | — |

La langue vient de la page (accueil en 8 langues), du choix fait à l'inscription
(`users.lang`) ou est vide quand on ne la connaît pas (`inconnue` ci-dessous).

Avant la migration, les événements étaient dans `visitor_logs` (`page = 'evt:…'`,
sans langue, anciens noms) : l'admin (`/dope-admin`) additionne les deux, les
requêtes ci-dessous ne lisent que `funnel_events`.

## Le tunnel, par semaine et par langue

À coller dans Supabase → SQL Editor.

```sql
-- Visiteurs → analyses → inscriptions → missions terminées → abonnés,
-- par semaine (lundi) et par langue, avec le taux de passage entre chaque marche.
WITH evt AS (
  SELECT date_trunc('week', created_at)::date AS semaine,
         COALESCE(lang, 'inconnue')           AS langue,
         evenement
  FROM funnel_events
  WHERE created_at >= now() - interval '12 weeks'
),
marches AS (
  SELECT semaine, langue,
         COUNT(*) FILTER (WHERE evenement = 'visite_accueil')         AS visiteurs,
         COUNT(*) FILTER (WHERE evenement = 'analyse_anonyme_lancee') AS analyses,
         COUNT(*) FILTER (WHERE evenement = 'inscription')            AS inscriptions,
         COUNT(*) FILTER (WHERE evenement = 'mission_terminee')       AS missions_terminees,
         COUNT(*) FILTER (WHERE evenement = 'abonnement')             AS abonnes
  FROM evt
  GROUP BY semaine, langue
)
SELECT semaine,
       langue,
       visiteurs,
       analyses,
       ROUND(100.0 * analyses           / NULLIF(visiteurs, 0), 1)          AS "visiteurs → analyses %",
       inscriptions,
       ROUND(100.0 * inscriptions       / NULLIF(analyses, 0), 1)           AS "analyses → inscriptions %",
       missions_terminees,
       ROUND(100.0 * missions_terminees / NULLIF(inscriptions, 0), 1)       AS "inscriptions → missions %",
       abonnes,
       ROUND(100.0 * abonnes            / NULLIF(missions_terminees, 0), 1) AS "missions → abonnés %",
       ROUND(100.0 * abonnes            / NULLIF(visiteurs, 0), 2)          AS "visiteurs → abonnés %"
FROM marches
ORDER BY semaine DESC, visiteurs DESC;
```

**À lire avec deux précautions.** Une marche peut dépasser la précédente : un
visiteur peut s'inscrire sans avoir analysé de vidéo, ou s'abonner sans finir sa
mission — un taux au-dessus de 100 % n'est pas une erreur. Et un abonnement payé
cette semaine vient souvent d'une inscription des semaines précédentes : pour
juger une semaine, regarde la tendance sur plusieurs semaines.

## Le détail du tunnel (toutes les marches, 30 derniers jours)

```sql
SELECT evenement,
       COUNT(*)                                        AS total,
       COUNT(*) FILTER (WHERE detail = 'google')       AS via_google,
       COUNT(*) FILTER (WHERE detail = 'email')        AS via_email,
       COUNT(*) FILTER (WHERE detail = 'annuel')       AS annuels
FROM funnel_events
WHERE created_at >= now() - interval '30 days'
GROUP BY evenement
ORDER BY total DESC;
```

## Les e-mails : envoyés, cliqués

```sql
SELECT detail AS email,
       COUNT(*) FILTER (WHERE evenement = 'email_envoye') AS envoyes,
       COUNT(*) FILTER (WHERE evenement = 'email_clique') AS cliques,
       ROUND(100.0 * COUNT(*) FILTER (WHERE evenement = 'email_clique')
             / NULLIF(COUNT(*) FILTER (WHERE evenement = 'email_envoye'), 0), 1) AS "taux de clic %"
FROM funnel_events
WHERE evenement IN ('email_envoye', 'email_clique')
  AND created_at >= now() - interval '30 days'
GROUP BY detail
ORDER BY envoyes DESC;
```

## Les départs

```sql
-- Paiements échoués, pauses, résiliations par semaine.
SELECT date_trunc('week', created_at)::date AS semaine,
       COUNT(*) FILTER (WHERE evenement = 'paiement_echoue') AS paiements_echoues,
       COUNT(*) FILTER (WHERE evenement = 'pause')           AS pauses,
       COUNT(*) FILTER (WHERE evenement = 'resiliation')     AS resiliations
FROM funnel_events
WHERE created_at >= now() - interval '12 weeks'
GROUP BY 1 ORDER BY 1 DESC;

-- Pourquoi ils partent (réponses facultatives avant la résiliation).
SELECT raison, COUNT(*) AS reponses, MAX(created_at) AS derniere
FROM cancel_feedback
GROUP BY raison ORDER BY reponses DESC;
```
