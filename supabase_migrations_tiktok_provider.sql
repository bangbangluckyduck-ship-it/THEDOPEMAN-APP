-- ════════════════════════════════════════════════════════════════════════════
-- Multi-provider TikTok : 1 ligne par (email, provider)
-- ════════════════════════════════════════════════════════════════════════════
-- provider = 'display'  (Login Kit / Display API — vidéos + perfs)
-- provider = 'business' (Marketing API — insights audience)
-- À exécuter sur une table tiktok_tokens existante (créée avec UNIQUE(email)).

ALTER TABLE tiktok_tokens
    ADD COLUMN IF NOT EXISTS provider TEXT NOT NULL DEFAULT 'display';

-- Supprime l'ancienne contrainte d'unicité sur email seul (si présente)
ALTER TABLE tiktok_tokens DROP CONSTRAINT IF EXISTS tiktok_tokens_email_key;

-- Nouvelle unicité : (email, provider)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'tiktok_tokens_email_provider_key'
    ) THEN
        ALTER TABLE tiktok_tokens
            ADD CONSTRAINT tiktok_tokens_email_provider_key UNIQUE (email, provider);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_tiktok_tokens_email_provider
    ON tiktok_tokens (email, provider);
