-- Cache des données marché KeyAPI (créateurs / vidéos / produits)
-- Optionnel : sans cette table, l'app marche quand même (juste sans cache → plus d'appels KeyAPI).
CREATE TABLE IF NOT EXISTS market_cache (
    cache_key   TEXT PRIMARY KEY,
    payload     JSONB,
    expires_at  TIMESTAMPTZ,
    created_at  TIMESTAMPTZ DEFAULT now()
);
ALTER TABLE market_cache ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "market_cache_backend_all" ON market_cache;
CREATE POLICY "market_cache_backend_all" ON market_cache FOR ALL USING (true) WITH CHECK (true);
