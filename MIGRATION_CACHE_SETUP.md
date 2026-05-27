# Cache System Setup Guide

## Step 1: Create Cache Table in Supabase

1. Go to [Supabase Dashboard](https://supabase.com)
2. Select your project
3. Go to **SQL Editor** → **New Query**
4. Copy and paste the SQL below
5. Click **RUN**

```sql
-- Create video_analyses_cache table
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
```

## Step 2: Enable RLS (Row Level Security)

In SQL Editor, run:

```sql
-- Enable RLS
ALTER TABLE video_analyses_cache ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "cache_service_role_access" ON video_analyses_cache
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "cache_deny_public" ON video_analyses_cache
    FOR ALL USING (FALSE);
```

## Step 3: Create Helper Functions

In SQL Editor, run:

```sql
-- Create function to update timestamp
CREATE OR REPLACE FUNCTION update_cache_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
DROP TRIGGER IF EXISTS cache_update_timestamp ON video_analyses_cache;
CREATE TRIGGER cache_update_timestamp
    BEFORE UPDATE ON video_analyses_cache
    FOR EACH ROW
    EXECUTE FUNCTION update_cache_updated_at();
```

## Verification

Run this query to verify the table was created:

```sql
SELECT * FROM information_schema.tables 
WHERE table_name = 'video_analyses_cache';
```

You should see 1 row returned.

## What This Does

- **video_analyses_cache table**: Stores cached video analysis results
- **Indices**: Speed up lookups by URL, video_id, expiration time, and popularity
- **RLS Policies**: Only backend (service role) can access the cache
- **Auto-update trigger**: Automatically updates the `updated_at` timestamp

## Cache Features

- **Auto-expiration**: Results expire after 30/60/90 days based on popularity
- **View tracking**: Counts how many times a cached result is used
- **Performance**: SSE streaming displays cached results in <1 second
- **Smart cleanup**: Low-view expired entries are cleaned up daily

## Backend Integration

The Python backend (`cache_manager.py`) handles:
- Checking cache before analysis
- Saving analysis results to cache
- Updating view counts
- Statistics reporting

No additional configuration needed - just run the SQL above!

---

**Status**: Ready to implement
**Next**: Restart your FastAPI server and test the `/api/analyze/stream` endpoint
