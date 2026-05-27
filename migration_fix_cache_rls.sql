-- Fix: video_analyses_cache RLS denying all writes from backend (anon key)
-- Date: 2026-05-27
--
-- Problem: existing policies require service_role JWT which is not present
-- when backend uses the SUPABASE anon key. Cache writes silently fail with
-- "new row violates row-level security policy".
--
-- Solution: drop restrictive policies, add a permissive one that allows
-- the backend (anon role) to read/write the cache. The cache holds only
-- non-sensitive analysis JSON so wider access is fine.

DROP POLICY IF EXISTS "cache_backend_access" ON video_analyses_cache;
DROP POLICY IF EXISTS "cache_deny_direct_access" ON video_analyses_cache;

-- Allow all backend operations (anon role used by FastAPI server)
CREATE POLICY "cache_allow_all_backend" ON video_analyses_cache
    FOR ALL
    USING (true)
    WITH CHECK (true);
