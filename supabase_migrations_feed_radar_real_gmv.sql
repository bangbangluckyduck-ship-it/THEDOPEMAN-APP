-- Feed Radar — GMV réel par vidéo (endpoint KeyAPI /video/detail/analytics corrigé mi-2026).
--
-- total_video_sale_gmv_amt renvoyait systématiquement 0 (cf. commentaires historiques dans
-- supabase_migrations_feed_radar.sql) — confirmé réparé en direct sur un compte FR réel
-- (@thedopeman99, GMV non-nul). On ajoute des colonnes DÉDIÉES plutôt que de réécrire
-- gmv_estimated : réel et estimé sont deux fiabilités différentes, elles ne doivent jamais
-- s'écraser silencieusement (permet d'auditer plus tard combien de lignes ont du réel).
--
-- Additif et rétro-compatible : colonnes nullable / à défaut sûr. gmv_source distingue
-- 'real_attribution' (donnée API brute, y compris un vrai 0) de 'calculated_ctor' (fallback,
-- cf. feed_radar.estimate_video_gmv). video_products = IDs produits tagués dans la vidéo,
-- toujours des STRINGS (jamais des entiers bruts — les IDs produit TikTok font ~19 chiffres,
-- au-delà de Number.MAX_SAFE_INTEGER côté navigateur).

ALTER TABLE feed_radar_videos
    ADD COLUMN IF NOT EXISTS gmv_real       NUMERIC,
    ADD COLUMN IF NOT EXISTS sales_real     BIGINT,
    ADD COLUMN IF NOT EXISTS gmv_source     TEXT DEFAULT 'calculated_ctor',
    ADD COLUMN IF NOT EXISTS video_products JSONB DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS is_ad          BOOLEAN DEFAULT false;

CREATE INDEX IF NOT EXISTS idx_feed_radar_gmv_real   ON feed_radar_videos (gmv_real DESC NULLS LAST);
CREATE INDEX IF NOT EXISTS idx_feed_radar_gmv_source ON feed_radar_videos (gmv_source);
