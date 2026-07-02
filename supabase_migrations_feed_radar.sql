-- Feed Radar — vidéos enrichies (≥ view_threshold_used vues, thumbnail oEmbed
-- officiel TikTok, GMV estimé par calcul, tendance créateur).
--
-- GMV et tendance sont au niveau CRÉATEUR (pas vidéo) : les endpoints KeyAPI
-- vidéo→produit et vidéo→trend renvoient systématiquement vide en pratique
-- (testé sur 10 vidéos réelles, y compris shop-taguées) — cf. mémoire projet.
-- gmv_estimated est donc un CALCUL (vues × CTOR × prix moyen produits du
-- créateur), jamais une donnée API brute : toujours affiché "GMV estimé".

CREATE TABLE IF NOT EXISTS feed_radar_videos (
    id                      BIGSERIAL PRIMARY KEY,
    video_id                TEXT NOT NULL UNIQUE,
    video_url               TEXT NOT NULL,              -- share_url public, requis pour oEmbed
    creator_unique_id       TEXT,
    creator_nickname        TEXT,
    region                  TEXT,
    views                   BIGINT DEFAULT 0,
    likes                   BIGINT DEFAULT 0,
    comments                BIGINT DEFAULT 0,
    shares                  BIGINT DEFAULT 0,

    oembed_thumbnail_url    TEXT,
    oembed_html             TEXT,
    oembed_author_name      TEXT,
    oembed_fetched_at       TIMESTAMPTZ,

    trend_snapshot          JSONB DEFAULT '[]'::jsonb,   -- série GMV/ventes 30j du CRÉATEUR (sparkline)

    gmv_estimated           NUMERIC,                      -- vues * ctor_used * avg_product_price
    gmv_estimation_method   TEXT DEFAULT 'calculated_ctor',
    ctor_used               NUMERIC,                       -- taux assumé pour ce calcul (traçabilité)
    avg_product_price       NUMERIC,                       -- prix moyen assumé pour ce calcul (traçabilité)

    ai_score                NUMERIC,
    ai_analysis             JSONB,

    view_threshold_used     BIGINT NOT NULL,
    collected_at            TIMESTAMPTZ DEFAULT now(),
    updated_at              TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_feed_radar_views     ON feed_radar_videos (views DESC);
CREATE INDEX IF NOT EXISTS idx_feed_radar_gmv       ON feed_radar_videos (gmv_estimated DESC NULLS LAST);
CREATE INDEX IF NOT EXISTS idx_feed_radar_score     ON feed_radar_videos (ai_score DESC NULLS LAST);
CREATE INDEX IF NOT EXISTS idx_feed_radar_region    ON feed_radar_videos (region);
CREATE INDEX IF NOT EXISTS idx_feed_radar_collected ON feed_radar_videos (collected_at DESC);

ALTER TABLE feed_radar_videos ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "feed_radar_videos_backend_all" ON feed_radar_videos;
CREATE POLICY "feed_radar_videos_backend_all" ON feed_radar_videos FOR ALL USING (true) WITH CHECK (true);
