-- ════════════════════════════════════════════════════════════════════════
-- AFFILIATION — PHASE 2 : COMMISSIONS
-- À exécuter dans Supabase → SQL Editor, APRÈS supabase_migrations_affiliates.sql.
--
-- Règles (décidées le 16/10/2026) :
--   • commission = % de CHAQUE facture Stripe payée par un client parrainé
--     (première souscription, renouvellements, packs de crédits) ;
--   • à vie : tant que le client paie, l'affilié touche ;
--   • taux par défaut selon le type (créateur / agence), réglable par affilié ;
--   • payable 30 jours après le paiement (laisse passer remboursements/litiges).
--
-- Une ligne de affiliate_commissions = une facture payée. `stripe_invoice_id`
-- est UNIQUE : Stripe relivre ses webhooks, la même facture ne compte qu'une fois.
-- ════════════════════════════════════════════════════════════════════════

-- 1) Affiliés : type et nom affiché. `commission_rate` existait déjà (réservé) :
--    il devient le taux PERSONNALISÉ en %, NULL = taux par défaut du type.
ALTER TABLE affiliates ADD COLUMN IF NOT EXISTS type TEXT NOT NULL DEFAULT 'createur';  -- createur | agence
ALTER TABLE affiliates ADD COLUMN IF NOT EXISTS name TEXT;

-- 2) Commissions
CREATE TABLE IF NOT EXISTS affiliate_commissions (
    id                 BIGSERIAL PRIMARY KEY,
    affiliate_code     TEXT NOT NULL,
    customer_email     TEXT NOT NULL,             -- le client parrainé qui a payé
    stripe_invoice_id  TEXT UNIQUE NOT NULL,
    stripe_charge_id   TEXT,                      -- pour retrouver la ligne sur remboursement
    stripe_payment_intent TEXT,
    amount_cents       INTEGER NOT NULL,          -- montant payé par le client
    currency           TEXT NOT NULL DEFAULT 'eur',
    rate               NUMERIC NOT NULL,          -- taux appliqué, figé au moment du paiement
    commission_cents   INTEGER NOT NULL,          -- ramené à 0 si remboursé avant versement
    refunded_cents     INTEGER NOT NULL DEFAULT 0,
    status             TEXT NOT NULL DEFAULT 'pending',  -- pending | paid | cancelled
    invoice_paid_at    TIMESTAMPTZ NOT NULL,
    payable_at         TIMESTAMPTZ NOT NULL,      -- invoice_paid_at + 30 jours
    paid_out_at        TIMESTAMPTZ,               -- date à laquelle TU as versé l'affilié
    note               TEXT,                      -- ex. « ajustement remboursement »
    created_at         TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_aff_comm_code   ON affiliate_commissions (affiliate_code);
CREATE INDEX IF NOT EXISTS idx_aff_comm_charge ON affiliate_commissions (stripe_charge_id);
CREATE INDEX IF NOT EXISTS idx_aff_comm_pi     ON affiliate_commissions (stripe_payment_intent);

-- Même verrou que `affiliates` : accès uniquement par le backend (service_role).
ALTER TABLE affiliate_commissions ENABLE ROW LEVEL SECURITY;
DO $$
DECLARE pol RECORD;
BEGIN
  FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = 'affiliate_commissions'
  LOOP EXECUTE format('DROP POLICY IF EXISTS %I ON affiliate_commissions', pol.policyname); END LOOP;
END $$;
CREATE POLICY "affiliate_commissions_deny_direct_access" ON affiliate_commissions
    FOR ALL USING (false) WITH CHECK (false);

-- Vérif
SELECT column_name FROM information_schema.columns WHERE table_name = 'affiliates' ORDER BY ordinal_position;
SELECT tablename, policyname FROM pg_policies WHERE tablename = 'affiliate_commissions';
