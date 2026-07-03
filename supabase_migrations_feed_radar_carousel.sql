-- Feed Radar — support des posts photo-carrousel TikTok (photo mode).
--
-- TikTok distingue les posts vidéo des posts photo-carrousel via image_post_info
-- dans l'API influencer/videos. On capture ce flag (market_creators._clean_video)
-- pour pouvoir mettre en avant, dans Feed Radar, les CARROUSELS à fortes vues —
-- exactement le format que l'utilisateur génère avec le créateur de carrousels.
--
-- Additif et rétro-compatible : colonnes nullable à défaut faux/0. Les lignes
-- déjà collectées resteront is_carousel = false jusqu'à la prochaine collecte
-- (run_feed_radar_collection les re-uppsert avec le flag renseigné).

ALTER TABLE feed_radar_videos
    ADD COLUMN IF NOT EXISTS is_carousel  BOOLEAN DEFAULT false,
    ADD COLUMN IF NOT EXISTS image_count  INTEGER DEFAULT 0;

-- Tri/filtre rapide « carrousels à fortes vues » (onglet Feed Radar).
CREATE INDEX IF NOT EXISTS idx_feed_radar_carousel_views
    ON feed_radar_videos (is_carousel, views DESC);
