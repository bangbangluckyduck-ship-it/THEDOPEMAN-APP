-- ════════════════════════════════════════════════════════════════════════
-- REFONTE TARIFAIRE — offre unique « Qeerah Pro » + essai gratuit 7 jours
--
--   • Qeerah Pro : 29,99 €/mois ou 299 €/an → 100 analyses par cycle mensuel
--   • Essai gratuit : 7 jours après inscription, accès complet, 10 analyses
--
-- STRICTEMENT ADDITIVE — aucun DROP, aucune suppression de données.
-- Les tables monthly_usage / daily_usage restent en place et intactes : elles
-- conservent l'historique d'usage et servent de repli si cette migration devait
-- être annulée (cf. bloc ROLLBACK en fin de fichier).
--
-- Idempotente : peut être rejouée sans effet de bord.
-- ════════════════════════════════════════════════════════════════════════

-- ── 1) Colonnes sur users ────────────────────────────────────────────────
-- trial_ends_at         : fin de l'essai gratuit (NULL = pas d'essai en cours)
-- current_period_start  : début du cycle de facturation Stripe (ancre du quota)
-- current_period_end    : fin du cycle Stripe (annuel = +1 an, pas le sous-cycle
--                         mensuel du quota, qui est dérivé de l'ancre côté code)
ALTER TABLE users ADD COLUMN IF NOT EXISTS trial_ends_at        TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN IF NOT EXISTS current_period_start TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN IF NOT EXISTS current_period_end   TIMESTAMPTZ;

-- ── 2) Backfill de l'essai pour les comptes DÉJÀ inscrits ────────────────
-- Volontairement calé sur now() + 7 jours, PAS sur created_at + 7 jours :
-- ancrer sur la date d'inscription couperait instantanément l'accès de tous les
-- comptes existants au moment où la migration passe. Chacun garde donc une
-- semaine pleine à compter de la bascule.
UPDATE users
   SET trial_ends_at = now() + INTERVAL '7 days'
 WHERE trial_ends_at IS NULL
   AND COALESCE(tier, 'free') = 'free';

-- ── 3) Consommation d'analyses par cycle de facturation ──────────────────
-- Une ligne par (utilisateur, cycle). Le cycle courant est déterminé par le
-- code (analysis_quota.py) à partir de l'ancre Stripe ; le reset se fait « à la
-- lecture » (nouvelle ligne au changement de cycle), sans cron — même approche
-- que credits.py. Les lignes des cycles passés sont conservées : elles forment
-- l'historique de consommation, et rien ne les purge.
CREATE TABLE IF NOT EXISTS analysis_quota_periods (
    id            BIGSERIAL PRIMARY KEY,
    user_id       UUID        NOT NULL,
    period_start  TIMESTAMPTZ NOT NULL,
    period_end    TIMESTAMPTZ NOT NULL,
    count         INTEGER     NOT NULL DEFAULT 0,
    limit_value   INTEGER,                        -- plafond appliqué (100 ou 10) — trace historique
    kind          TEXT,                           -- 'subscription' | 'trial'
    created_at    TIMESTAMPTZ DEFAULT now(),
    updated_at    TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, period_start)
);

CREATE INDEX IF NOT EXISTS idx_analysis_quota_user_period
    ON analysis_quota_periods (user_id, period_start DESC);

-- ── 4) Verrouillage RLS ──────────────────────────────────────────────────
-- Même régime que users / monthly_usage (cf. migration lockdown) : la table
-- contient de la donnée de consommation rattachée à un compte, elle ne doit pas
-- être lisible via la clé anon, qui est publique par conception. Le backend y
-- accède avec service_role, qui bypasse RLS.
ALTER TABLE analysis_quota_periods ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE pol RECORD;
BEGIN
  FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = 'analysis_quota_periods'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON analysis_quota_periods', pol.policyname);
  END LOOP;
  CREATE POLICY analysis_quota_periods_deny_direct_access
      ON analysis_quota_periods FOR ALL USING (false) WITH CHECK (false);
END $$;

-- ── 5) Vérifications ─────────────────────────────────────────────────────
-- a) Les 3 colonnes existent bien sur users
SELECT column_name, data_type
  FROM information_schema.columns
 WHERE table_name = 'users'
   AND column_name IN ('trial_ends_at', 'current_period_start', 'current_period_end')
 ORDER BY column_name;

-- b) La policy de refus est en place (doit renvoyer 1 ligne, qual = false)
SELECT tablename, policyname, qual
  FROM pg_policies
 WHERE tablename = 'analysis_quota_periods';

-- c) Combien de comptes ont reçu un essai
SELECT count(*) AS comptes_en_essai
  FROM users
 WHERE trial_ends_at IS NOT NULL AND trial_ends_at > now();


-- ════════════════════════════════════════════════════════════════════════
-- ROLLBACK (à n'exécuter que pour revenir en arrière)
--
-- Aucune donnée existante n'ayant été modifiée ni supprimée par cette
-- migration, l'annuler consiste à retirer ce qu'elle a ajouté. Le quota
-- repart alors sur monthly_usage, resté intact.
--
--   DROP TABLE IF EXISTS analysis_quota_periods;
--   ALTER TABLE users DROP COLUMN IF EXISTS trial_ends_at;
--   ALTER TABLE users DROP COLUMN IF EXISTS current_period_start;
--   ALTER TABLE users DROP COLUMN IF EXISTS current_period_end;
--
-- Note : le DROP TABLE supprime l'historique de consommation par cycle. Pour
-- le conserver, renommer plutôt la table :
--   ALTER TABLE analysis_quota_periods RENAME TO analysis_quota_periods_backup;
-- ════════════════════════════════════════════════════════════════════════
