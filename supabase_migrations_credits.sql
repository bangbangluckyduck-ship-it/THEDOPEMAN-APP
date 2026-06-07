-- 💎 Système de crédits — AI Video Prompt Studio
-- Crédits d'abonnement (reset le 1er du mois, calcul à la lecture) + crédits achetés
-- (packs, validité 1 mois). Achat réel via Stripe DIFFÉRÉ (société pas créée).

-- 1) Crédits d'abonnement consommés (le TOTAL vient du plan, calculé serveur).
CREATE TABLE IF NOT EXISTS user_credits (
    email                    TEXT PRIMARY KEY,
    subscription_used        INTEGER DEFAULT 0,
    subscription_reset_date  TIMESTAMPTZ,          -- 1er du mois suivant (reset à la lecture)
    updated_at               TIMESTAMPTZ DEFAULT now()
);
ALTER TABLE user_credits ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "user_credits_backend_all" ON user_credits;
CREATE POLICY "user_credits_backend_all" ON user_credits FOR ALL USING (true) WITH CHECK (true);

-- 2) Packs de crédits achetés (validité 1 mois). Alimenté par Stripe (plus tard).
CREATE TABLE IF NOT EXISTS credit_purchases (
    id                 BIGSERIAL PRIMARY KEY,
    email              TEXT NOT NULL,
    pack_name          TEXT,
    credits_amount     INTEGER,
    credits_remaining  INTEGER,
    price_paid         NUMERIC,
    currency           TEXT DEFAULT 'EUR',
    stripe_payment_id  TEXT,
    purchased_at       TIMESTAMPTZ DEFAULT now(),
    expires_at         TIMESTAMPTZ,
    is_expired         BOOLEAN DEFAULT false
);
CREATE INDEX IF NOT EXISTS idx_credit_purchases_email ON credit_purchases (email, expires_at);
ALTER TABLE credit_purchases ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "credit_purchases_backend_all" ON credit_purchases;
CREATE POLICY "credit_purchases_backend_all" ON credit_purchases FOR ALL USING (true) WITH CHECK (true);

-- 3) Historique des générations de prompts vidéo.
CREATE TABLE IF NOT EXISTS video_prompt_generations (
    id                 BIGSERIAL PRIMARY KEY,
    email              TEXT,
    created_at         TIMESTAMPTZ DEFAULT now(),
    prompt_level       INTEGER,
    credits_used       INTEGER,
    ai_platform        TEXT,
    product_name       TEXT,
    niche              TEXT,
    generated_prompt   JSONB,
    is_saved           BOOLEAN DEFAULT false
);
CREATE INDEX IF NOT EXISTS idx_vpg_email ON video_prompt_generations (email, created_at DESC);
ALTER TABLE video_prompt_generations ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "vpg_backend_all" ON video_prompt_generations;
CREATE POLICY "vpg_backend_all" ON video_prompt_generations FOR ALL USING (true) WITH CHECK (true);
