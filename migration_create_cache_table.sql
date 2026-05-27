-- Migration: Create video_analyses_cache table
-- Date: 2026-05-27
-- Purpose: Cache video analysis results for performance optimization

-- Create table
CREATE TABLE IF NOT EXISTS video_analyses_cache (
    id BIGSERIAL PRIMARY KEY,
    video_url TEXT UNIQUE NOT NULL,
    video_id TEXT NOT NULL,
    analysis_data JSONB NOT NULL,
    product_id TEXT,
    ai_model_used TEXT DEFAULT 'mistral',
    analysis_duration_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    view_count INTEGER DEFAULT 1,

    -- Constraints
    CONSTRAINT check_ttl CHECK (expires_at > created_at),
    CONSTRAINT check_view_count CHECK (view_count >= 0),
    CONSTRAINT check_duration CHECK (analysis_duration_ms > 0)
);

-- Create indices for performance
CREATE INDEX IF NOT EXISTS idx_video_url ON video_analyses_cache(video_url);
CREATE INDEX IF NOT EXISTS idx_video_id ON video_analyses_cache(video_id);
CREATE INDEX IF NOT EXISTS idx_expires_at ON video_analyses_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_view_count ON video_analyses_cache(view_count DESC);
CREATE INDEX IF NOT EXISTS idx_created_at ON video_analyses_cache(created_at DESC);

-- Enable RLS
ALTER TABLE video_analyses_cache ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Allow service role (backend) full access
-- This allows the backend to read/write cache entries
CREATE POLICY "cache_backend_access" ON video_analyses_cache
    FOR ALL USING (
        -- Service role bypass (always true for backend)
        auth.jwt() ->> 'role' = 'service_role'
        OR current_setting('request.jwt.claims')::jsonb ->> 'role' = 'service_role'
    );

-- RLS Policy: Deny all other access by default
-- This prevents direct client access to cache
CREATE POLICY "cache_deny_direct_access" ON video_analyses_cache
    FOR ALL USING (FALSE);

-- Create function to automatically update updated_at
CREATE OR REPLACE FUNCTION update_cache_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for updated_at
CREATE TRIGGER cache_update_timestamp
    BEFORE UPDATE ON video_analyses_cache
    FOR EACH ROW
    EXECUTE FUNCTION update_cache_updated_at();

-- Create function for daily cleanup (removes expired entries with low view count)
CREATE OR REPLACE FUNCTION cleanup_expired_cache()
RETURNS void AS $$
BEGIN
    DELETE FROM video_analyses_cache
    WHERE expires_at < NOW() AND view_count < 2;
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup job (runs daily at 3 AM UTC)
-- Note: Requires pg_cron extension. If not available, run cleanup manually or use application scheduler
SELECT cron.schedule(
    'cleanup_video_cache_daily',
    '0 3 * * *',
    'SELECT cleanup_expired_cache()'
) ON CONFLICT (jobname) DO NOTHING;
