-- 📸 Photo Slide Coach v4 — funnel homepage + anonyme + pay-as-you-go (Stripe différé)
-- Réutilise user_credits / credit_purchases (migration crédits déjà passée).

-- 1) Générations des VISITEURS ANONYMES (tracking IP/cookie, 1 essai gratuit).
CREATE TABLE IF NOT EXISTS anonymous_generations (
    id                   BIGSERIAL PRIMARY KEY,
    ip_hash              TEXT,
    cookie_id            TEXT,
    created_at           TIMESTAMPTZ DEFAULT now(),
    generation_mode      TEXT,                 -- 'prompts' | 'images'
    generation_data      JSONB,
    product_name         TEXT,
    email_captured       TEXT,
    converted_user_email TEXT,                 -- si le visiteur crée un compte
    stripe_payment_id    TEXT,
    payment_amount       NUMERIC
);
CREATE INDEX IF NOT EXISTS idx_anon_gen_ipcookie ON anonymous_generations (ip_hash, cookie_id, created_at DESC);
ALTER TABLE anonymous_generations ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_gen_backend_all" ON anonymous_generations;
CREATE POLICY "anon_gen_backend_all" ON anonymous_generations FOR ALL USING (true) WITH CHECK (true);

-- 2) Générations des UTILISATEURS connectés (historique Photo Slide v4).
CREATE TABLE IF NOT EXISTS photo_slide_generations (
    id                  BIGSERIAL PRIMARY KEY,
    email               TEXT,
    created_at          TIMESTAMPTZ DEFAULT now(),
    generation_mode     TEXT,                  -- 'prompts' | 'images'
    chosen_style        TEXT,
    chosen_ai           TEXT,
    product_name        TEXT,
    product_description TEXT,
    product_price       NUMERIC,
    niche               TEXT,
    generated_data      JSONB,                 -- plan + images + conseils slides 5-7
    credits_used        INTEGER DEFAULT 0,
    payment_method      TEXT,                  -- 'subscription_credits' | 'purchased_credits' | 'one_time' | 'free'
    is_saved            BOOLEAN DEFAULT false
);
CREATE INDEX IF NOT EXISTS idx_psg_email ON photo_slide_generations (email, created_at DESC);
ALTER TABLE photo_slide_generations ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "psg_backend_all" ON photo_slide_generations;
CREATE POLICY "psg_backend_all" ON photo_slide_generations FOR ALL USING (true) WITH CHECK (true);

-- 3) Achats one-time (génération unique / pack), visiteur OU connecté. Stripe différé.
CREATE TABLE IF NOT EXISTS one_time_purchases (
    id                BIGSERIAL PRIMARY KEY,
    ip_hash           TEXT,
    email             TEXT,
    product_type      TEXT,                    -- 'single_generation' | 'credit_pack'
    amount_paid       NUMERIC,
    currency          TEXT DEFAULT 'EUR',
    stripe_payment_id TEXT,
    generation_id     BIGINT,
    status            TEXT DEFAULT 'pending',  -- 'pending' | 'paid' | 'failed'
    created_at        TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_otp_email ON one_time_purchases (email, created_at DESC);
ALTER TABLE one_time_purchases ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "otp_backend_all" ON one_time_purchases;
CREATE POLICY "otp_backend_all" ON one_time_purchases FOR ALL USING (true) WITH CHECK (true);
