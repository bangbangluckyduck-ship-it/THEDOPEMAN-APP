-- ════════════════════════════════════════════════════════════════════════
-- NOTIFICATIONS — abonnements Web Push (PWA)
-- ════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS push_subscriptions (
  id          BIGSERIAL PRIMARY KEY,
  email       TEXT,                         -- null si visiteur anonyme
  endpoint    TEXT UNIQUE NOT NULL,
  p256dh      TEXT NOT NULL,
  auth        TEXT NOT NULL,
  is_admin    BOOLEAN DEFAULT FALSE,        -- pour les alertes réservées à l'admin
  user_agent  TEXT,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  last_seen   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_push_email ON push_subscriptions (email);
CREATE INDEX IF NOT EXISTS idx_push_admin ON push_subscriptions (is_admin) WHERE is_admin = TRUE;
