-- Favoris utilisateur — sauvegarde de créateurs / produits / posts gagnants
-- repérés dans Créateurs Gagnants, Feed Radar, ou la fiche créateur.
--
-- payload = snapshot d'affichage (nom, image, url, prix…) pour pouvoir rendre
-- la carte Favoris sans re-taper les API KeyAPI. item_id = identifiant stable
-- (unique_id créateur / product_id / video_id). UNIQUE(email,type,id) → idempotent.
--
-- Additif et rétro-compatible : le code dégrade proprement si la table n'existe
-- pas encore (les endpoints /api/favorites renvoient une liste vide sans crash).

CREATE TABLE IF NOT EXISTS user_favorites (
    id          BIGSERIAL PRIMARY KEY,
    email       TEXT NOT NULL,
    item_type   TEXT NOT NULL,                 -- 'creator' | 'product' | 'video'
    item_id     TEXT NOT NULL,                 -- unique_id / product_id / video_id
    payload     JSONB DEFAULT '{}'::jsonb,     -- snapshot pour l'affichage
    created_at  TIMESTAMPTZ DEFAULT now(),
    UNIQUE (email, item_type, item_id)
);

CREATE INDEX IF NOT EXISTS idx_user_favorites_email
    ON user_favorites (email, created_at DESC);

ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "user_favorites_backend_all" ON user_favorites;
CREATE POLICY "user_favorites_backend_all" ON user_favorites FOR ALL USING (true) WITH CHECK (true);
