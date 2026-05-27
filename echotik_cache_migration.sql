-- Créer table pour cache vidéos virales (24h)
CREATE TABLE IF NOT EXISTS viral_videos_cache (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category TEXT NOT NULL,
  videos JSONB NOT NULL,
  cached_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '24 hours',
  UNIQUE(category)
);

-- Index pour recherche rapide par catégorie et expiration
CREATE INDEX IF NOT EXISTS idx_viral_category ON viral_videos_cache(category);
CREATE INDEX IF NOT EXISTS idx_viral_expires ON viral_videos_cache(expires_at);

-- RLS Policies
ALTER TABLE viral_videos_cache ENABLE ROW LEVEL SECURITY;

-- Permettre lecture publique (cache)
CREATE POLICY "viral_videos_public_read" ON viral_videos_cache
  FOR SELECT USING (true);

-- Permettre écriture au service backend uniquement
CREATE POLICY "viral_videos_service_write" ON viral_videos_cache
  FOR INSERT WITH CHECK (true);

CREATE POLICY "viral_videos_service_update" ON viral_videos_cache
  FOR UPDATE USING (true);
