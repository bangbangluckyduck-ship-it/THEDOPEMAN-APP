-- ════════════════════════════════════════════════════════════════════════
-- FEATURE 1 — Banque de Hooks (accroches) par catégorie de produit
-- Contenu curé en admin, gating d'accès par plan (FREE verrouillé).
-- ════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS hooks (
  id          BIGSERIAL PRIMARY KEY,
  texte       TEXT NOT NULL,
  categorie   TEXT NOT NULL,                       -- sante|beaute|mode|tech|fitness|maison|mobilier|food|autre
  url_video   TEXT,                                -- lien externe optionnel (TikTok, Drive…)
  type_acces  TEXT NOT NULL DEFAULT 'plan_minimum',-- 'tous' | 'plan_minimum' | 'plans_specifiques'
  plan_min    TEXT DEFAULT 'pro',                  -- utilisé si type_acces = plan_minimum
  plans_autorises JSONB DEFAULT '[]'::jsonb,       -- utilisé si type_acces = plans_specifiques (ex: ["gold","agency"])
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_hooks_categorie ON hooks (categorie);
CREATE INDEX IF NOT EXISTS idx_hooks_created   ON hooks (created_at DESC);
