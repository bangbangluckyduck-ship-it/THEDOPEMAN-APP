-- ════════════════════════════════════════════════════════════════════════
-- PROGRAMME D'AFFILIATION Qeerah
-- • Un user candidate depuis son espace → statut 'pending'.
-- • L'admin (/dope-admin) crée directement OU approuve → statut 'approved'
--   + un code d'affiliation unique.
-- • Le lien qeerah.com/?ref=CODE attribue les inscriptions (users.referred_by).
-- • L'affilié voit son lien + le nombre d'inscrits dans son espace client.
--
-- Sécurité : table verrouillée (RLS deny anon/authenticated). Le backend y
-- accède via supabase_service (service_role, bypasse RLS). Cf. le verrouillage
-- des tables sensibles (supabase_migrations_lockdown_sensitive_tables.sql).
-- ════════════════════════════════════════════════════════════════════════

-- 1) Table des affiliés
CREATE TABLE IF NOT EXISTS affiliates (
    id               BIGSERIAL PRIMARY KEY,
    email            TEXT UNIQUE NOT NULL,          -- compte de l'affilié
    code             TEXT UNIQUE,                   -- attribué à l'approbation
    status           TEXT NOT NULL DEFAULT 'pending', -- pending|approved|rejected|disabled
    commission_rate  NUMERIC,                       -- réservé (payouts, phase 2) — non utilisé au lancement
    created_at       TIMESTAMPTZ DEFAULT now(),
    approved_at      TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_affiliates_code ON affiliates (code);

ALTER TABLE affiliates ENABLE ROW LEVEL SECURITY;
DO $$
DECLARE pol RECORD;
BEGIN
  FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = 'affiliates'
  LOOP EXECUTE format('DROP POLICY IF EXISTS %I ON affiliates', pol.policyname); END LOOP;
END $$;
CREATE POLICY "affiliates_deny_direct_access" ON affiliates
    FOR ALL USING (false) WITH CHECK (false);

-- 2) Attribution des inscriptions : code de l'affilié qui a amené le user.
--    (Colonne posée sur la table users existante, déjà verrouillée en RLS.)
ALTER TABLE users ADD COLUMN IF NOT EXISTS referred_by TEXT;
CREATE INDEX IF NOT EXISTS idx_users_referred_by ON users (referred_by);

-- Vérif : la table affiliates doit avoir 1 policy "USING (false)".
SELECT tablename, policyname, qual FROM pg_policies WHERE tablename = 'affiliates';
