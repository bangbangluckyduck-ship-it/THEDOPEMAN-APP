-- 🧠 Mémoire produits : s'enrichit à chaque analyse pour améliorer la reco au fil
-- du temps. 100% anonymisé (aucun lien utilisateur ; un product_id TikTok Shop
-- n'est pas une donnée personnelle).
CREATE TABLE IF NOT EXISTS analyzed_products (
    product_key   TEXT PRIMARY KEY,         -- "id:<product_id>" si connu, sinon "name:<cat>:<slug>"
    product_id    TEXT,                      -- vrai id TikTok (rempli via Video Products)
    product_name  TEXT,
    categorie     TEXT,
    region        TEXT,
    price         NUMERIC,
    last_sales    BIGINT,
    times_seen    INTEGER DEFAULT 1,         -- nb de fois analysé (signal de récurrence)
    first_seen    TIMESTAMPTZ DEFAULT now(),
    last_seen     TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_analyzed_products_cat ON analyzed_products (categorie, region, times_seen DESC);

ALTER TABLE analyzed_products ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "analyzed_products_backend_all" ON analyzed_products;
CREATE POLICY "analyzed_products_backend_all" ON analyzed_products FOR ALL USING (true) WITH CHECK (true);
