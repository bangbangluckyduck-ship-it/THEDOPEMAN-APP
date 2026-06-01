-- ════════════════════════════════════════════════════════════════════════════
-- Tokens OAuth TikTok Shop (Partner API) — rattachés à l'utilisateur
-- ════════════════════════════════════════════════════════════════════════════
-- Stocke l'access_token / refresh_token obtenu après autorisation marchand.
-- 1 ligne par utilisateur (clé d'unicité : email).
-- Accès strictement backend (RLS) : les tokens ne sont JAMAIS exposés au client.

CREATE TABLE IF NOT EXISTS tiktok_tokens (
    id                        BIGSERIAL PRIMARY KEY,
    email                     TEXT        NOT NULL UNIQUE,
    open_id                   TEXT,                     -- identifiant marchand TikTok
    seller_name               TEXT,
    region                    TEXT,
    access_token              TEXT,
    refresh_token             TEXT,
    access_token_expires_at   BIGINT,                   -- epoch seconds
    refresh_token_expires_at  BIGINT,                   -- epoch seconds
    scope                     JSONB,
    updated_at                BIGINT,                   -- epoch seconds
    created_at                TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_tiktok_tokens_email ON tiktok_tokens (email);

-- ── RLS : accès backend uniquement ───────────────────────────────────────────
ALTER TABLE tiktok_tokens ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "tiktok_tokens_backend_all" ON tiktok_tokens;
CREATE POLICY "tiktok_tokens_backend_all" ON tiktok_tokens
    FOR ALL
    USING (true)
    WITH CHECK (true);
