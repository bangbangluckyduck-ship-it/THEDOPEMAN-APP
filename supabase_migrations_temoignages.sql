-- ════════════════════════════════════════════════════════════════════════
-- FEATURE 2 — Témoignages beta testeurs (collecte hybride + validation admin)
-- ════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS temoignages (
  id               BIGSERIAL PRIMARY KEY,
  nom              TEXT NOT NULL,
  texte            TEXT NOT NULL,
  lien_tiktok      TEXT,
  photo_url        TEXT,
  metrique         TEXT,                       -- ex: "+12% de complétion"
  note             INT,                        -- note optionnelle 1-5
  statut           TEXT NOT NULL DEFAULT 'en_attente',  -- en_attente | publie | masque
  mis_en_avant     BOOLEAN DEFAULT FALSE,
  date_soumission  TIMESTAMPTZ DEFAULT NOW(),
  date_publication TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_temoignages_statut ON temoignages (statut, mis_en_avant, date_publication DESC);

-- Anti-spam de la relance email : 1 seul envoi par compte
ALTER TABLE users ADD COLUMN IF NOT EXISTS testimonial_email_sent BOOLEAN DEFAULT FALSE;
