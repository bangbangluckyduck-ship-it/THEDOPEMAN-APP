-- Quota journalier de la Recherche de profil TikTok (Pro = 10/jour, Gold+ = illimité).
-- Indépendant de monthly_usage/daily_usage (câblés sur l'analyse vidéo, cf. auth.py).

CREATE TABLE IF NOT EXISTS recherche_search_usage (
    id          BIGSERIAL PRIMARY KEY,
    user_id     UUID NOT NULL,
    day         TEXT NOT NULL,               -- 'YYYY-MM-DD' UTC, même format que daily_usage
    count       INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, day)
);

CREATE INDEX IF NOT EXISTS idx_recherche_usage_user_day ON recherche_search_usage (user_id, day);

ALTER TABLE recherche_search_usage ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "recherche_search_usage_backend_all" ON recherche_search_usage;
CREATE POLICY "recherche_search_usage_backend_all" ON recherche_search_usage FOR ALL USING (true) WITH CHECK (true);
