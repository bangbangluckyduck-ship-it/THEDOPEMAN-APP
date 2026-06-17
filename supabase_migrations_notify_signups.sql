-- ════════════════════════════════════════════════════════════════════════
-- « 🔔 Me notifier » — capture d'emails pour les plans pas encore ouverts
-- (GOLD/AGENCY au 16 sept, LTD au 15 oct). Sert à la communication de lancement.
-- ════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS plan_notify_signups (
  id          BIGSERIAL PRIMARY KEY,
  email       TEXT NOT NULL,
  plan        TEXT NOT NULL,              -- 'pro' | 'gold' | 'agency' | 'ltd'
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  notified_at TIMESTAMPTZ,                -- rempli quand l'email de lancement est parti
  UNIQUE (email, plan)
);

CREATE INDEX IF NOT EXISTS idx_notify_plan ON plan_notify_signups (plan);
