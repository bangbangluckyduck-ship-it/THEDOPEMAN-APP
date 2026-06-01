-- ════════════════════════════════════════════════════════════════════════════
-- Base de connaissances « structures gagnantes » (Gold / Agency)
-- ════════════════════════════════════════════════════════════════════════════
-- Données 100% ANONYMISÉES : aucune colonne ne contient d'email, d'IP ou d'id
-- utilisateur. On stocke uniquement l'insight agrégé d'une analyse vidéo pour
-- pouvoir proposer, sur une future analyse au score < 75, des accroches/scripts
-- ayant obtenu > 75 sur un produit similaire au même budget.
-- La table se remplit naturellement avec l'usage (aucun pré-remplissage).

CREATE TABLE IF NOT EXISTS analyzed_insights (
    id            BIGSERIAL PRIMARY KEY,
    category      TEXT        NOT NULL,           -- regroupement (beaute, tech, mode, ...)
    product       TEXT        NOT NULL,           -- nom produit détecté/saisi
    price         NUMERIC,                        -- prix EUR (nullable si inconnu)
    score_global  INTEGER     NOT NULL,           -- 0-100
    hook_type     TEXT,                           -- type d'accroche
    hook_examples JSONB       DEFAULT '[]'::jsonb,-- exemples d'accroches concrètes
    script        JSONB,                          -- script premium (hook/démo/CTA) si dispo
    verdict       TEXT,
    created_at    TIMESTAMPTZ DEFAULT now()
);

-- Index pour la requête de récupération (catégorie + score décroissant).
CREATE INDEX IF NOT EXISTS idx_analyzed_insights_cat_score
    ON analyzed_insights (category, score_global DESC);

CREATE INDEX IF NOT EXISTS idx_analyzed_insights_price
    ON analyzed_insights (price);

-- ── RLS ──────────────────────────────────────────────────────────────────────
-- Accès uniquement via le backend (clé service / anon utilisée serveur-side).
-- Aucun accès direct client : la donnée n'est jamais exposée individuellement,
-- elle ne sert qu'à alimenter les recommandations agrégées côté serveur.
ALTER TABLE analyzed_insights ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "analyzed_insights_backend_all" ON analyzed_insights;
CREATE POLICY "analyzed_insights_backend_all" ON analyzed_insights
    FOR ALL
    USING (true)
    WITH CHECK (true);
