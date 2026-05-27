-- ════════════════════════════════════════════════════════════════
-- ANALYTICS TABLE - Supabase Migration
-- ════════════════════════════════════════════════════════════════

-- Table pour tracker les visiteurs par jour
CREATE TABLE IF NOT EXISTS daily_visitor_stats (
  id BIGSERIAL PRIMARY KEY,
  date DATE NOT NULL UNIQUE,
  visitor_count INTEGER DEFAULT 1,
  unique_visitors INTEGER DEFAULT 0,
  analysis_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table pour tracker les visits individuelles (optionnel mais utile pour analytics avancées)
CREATE TABLE IF NOT EXISTS visitor_logs (
  id BIGSERIAL PRIMARY KEY,
  page TEXT NOT NULL,
  ip_hash TEXT,
  user_agent_hash TEXT,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  user_email TEXT
);

-- Index pour performance
CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_visitor_stats(date DESC);
CREATE INDEX IF NOT EXISTS idx_visitor_logs_timestamp ON visitor_logs(timestamp DESC);

-- Politique RLS
ALTER TABLE daily_visitor_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE visitor_logs ENABLE ROW LEVEL SECURITY;

-- Permettre au backend (service role) de modifier les stats
CREATE POLICY "allow_service_role_stats" ON daily_visitor_stats
  FOR ALL USING (true);

CREATE POLICY "allow_service_role_logs" ON visitor_logs
  FOR ALL USING (true);

-- Table pour la configuration des analytiques (pour les admins)
CREATE TABLE IF NOT EXISTS analytics_config (
  id BIGSERIAL PRIMARY KEY,
  key TEXT UNIQUE NOT NULL,
  value TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO analytics_config (key, value) VALUES
  ('tracking_enabled', 'true'),
  ('daily_summary_enabled', 'true'),
  ('analytics_password', 'admin123')
ON CONFLICT (key) DO NOTHING;
