-- ✍️ Générateur de scripts multi-angles — compteur dédié (quota séparé des analyses).
-- Modèle aligné sur photo_slide_generations : les free ont 3 générations/mois,
-- les Pro/Gold/Agency sont illimités. Le comptage se fait sur cette table (par mois
-- calendaire, par email), et N'ENTAME PAS le quota d'analyses vidéo.

CREATE TABLE IF NOT EXISTS script_generations (
    id            BIGSERIAL PRIMARY KEY,
    email         TEXT,
    created_at    TIMESTAMPTZ DEFAULT now(),
    product_name  TEXT,
    price         TEXT,
    user_role     TEXT,                 -- 'affilie' | 'vendeur' | null
    tier          TEXT,                 -- tier de l'utilisateur au moment de la génération
    n_scripts     INTEGER DEFAULT 0     -- nombre de scripts renvoyés
);
CREATE INDEX IF NOT EXISTS idx_scriptgen_email ON script_generations (email, created_at DESC);
ALTER TABLE script_generations ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "scriptgen_backend_all" ON script_generations;
CREATE POLICY "scriptgen_backend_all" ON script_generations FOR ALL USING (true) WITH CHECK (true);
