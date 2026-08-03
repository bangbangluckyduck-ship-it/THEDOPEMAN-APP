-- ════════════════════════════════════════════════════════════════════════
-- RATTRAPAGE — comptes créés sans essai gratuit
--
-- CONTEXTE
-- Les deux chemins de création de compte par e-mail (`/api/register` et la
-- branche « nouveau compte » de `/api/login`, seule réellement utilisée par le
-- front) inséraient la ligne `users` SANS la colonne `trial_ends_at`.
-- `analysis_quota.resolve_period()` lit un `trial_ends_at` NULL comme « essai
-- terminé » : ces comptes recevaient donc un 402 « Ton essai gratuit est
-- terminé » dès leur toute première analyse.
--
-- Seule l'inscription via Google échappait au défaut (elle passe par
-- `get_or_create_user()`, qui pose bien la date à la création de la ligne).
--
-- Le code est corrigé (main.py → `_new_user_row()`), mais les comptes déjà
-- créés restent bloqués : ce script les débloque.
--
-- STRICTEMENT ADDITIVE — aucun DROP, aucune donnée supprimée.
-- Idempotente : rejouable sans effet de bord (le WHERE exclut les comptes déjà
-- pourvus d'un essai).
-- ════════════════════════════════════════════════════════════════════════

-- ── 1) Qui est concerné ? (à lire AVANT d'appliquer) ────────────────────
-- Comptes gratuits sans aucune date de fin d'essai. Ce sont eux qui voient
-- « essai terminé » alors qu'ils n'ont jamais rien pu essayer.
SELECT count(*) AS comptes_bloques
  FROM users
 WHERE trial_ends_at IS NULL
   AND COALESCE(tier, 'free') = 'free';


-- ── 2) Le rattrapage ────────────────────────────────────────────────────
-- Calé sur `now() + 7 jours`, et NON sur `created_at + 7 jours` : ces personnes
-- n'ont jamais eu d'essai utilisable, leur en donner un déjà expiré ne
-- corrigerait rien. Chacune repart donc sur une semaine pleine.
--
-- Les abonnés payants sont exclus par le filtre sur `tier` : leur quota vient
-- du cycle de facturation, pas de l'essai.
UPDATE users
   SET trial_ends_at = now() + INTERVAL '7 days'
 WHERE trial_ends_at IS NULL
   AND COALESCE(tier, 'free') = 'free';


-- ── 3) Filet de sécurité en base ────────────────────────────────────────
-- Le correctif applicatif suffit, mais une valeur par défaut garantit qu'aucune
-- future porte d'entrée (nouveau point d'inscription, script d'import, insertion
-- manuelle depuis le dashboard Supabase) ne puisse recréer le même compte muet.
-- C'est la ceinture en plus des bretelles : le défaut venait précisément d'un
-- chemin d'insertion qui ignorait la colonne.
ALTER TABLE users
  ALTER COLUMN trial_ends_at SET DEFAULT (now() + INTERVAL '7 days');


-- ── 4) Vérifications ────────────────────────────────────────────────────
-- a) Plus aucun compte gratuit sans essai (doit renvoyer 0)
SELECT count(*) AS restants_sans_essai
  FROM users
 WHERE trial_ends_at IS NULL
   AND COALESCE(tier, 'free') = 'free';

-- b) La valeur par défaut est bien posée
SELECT column_name, column_default
  FROM information_schema.columns
 WHERE table_name = 'users'
   AND column_name = 'trial_ends_at';

-- c) Combien de comptes sont en essai ACTIF après rattrapage
SELECT count(*) AS comptes_en_essai_actif
  FROM users
 WHERE trial_ends_at IS NOT NULL
   AND trial_ends_at > now();


-- ════════════════════════════════════════════════════════════════════════
-- ROLLBACK (à n'exécuter que pour revenir en arrière)
--
--   ALTER TABLE users ALTER COLUMN trial_ends_at DROP DEFAULT;
--
-- L'UPDATE de l'étape 2 n'est volontairement PAS annulable : revenir en arrière
-- consisterait à remettre des comptes en « essai terminé » sans qu'ils aient
-- jamais pu essayer. Si c'était réellement voulu, cibler nominativement les
-- adresses concernées plutôt que d'inverser l'UPDATE en masse.
-- ════════════════════════════════════════════════════════════════════════
