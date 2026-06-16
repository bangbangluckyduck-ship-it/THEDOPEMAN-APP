-- ════════════════════════════════════════════════════════════════════════════
-- Emails d'incitation Free → payant (déclencheur quota + relance J+3) + désinscription
-- À exécuter dans Supabase → SQL Editor.
-- ════════════════════════════════════════════════════════════════════════════

-- Désinscription marketing (RGPD) : si TRUE, on n'envoie plus d'email promotionnel.
ALTER TABLE users ADD COLUMN IF NOT EXISTS marketing_opt_out BOOLEAN DEFAULT FALSE;

-- Mois (YYYY-MM) du dernier email "quota atteint" envoyé → 1 envoi max par mois.
ALTER TABLE users ADD COLUMN IF NOT EXISTS upsell_quota_email_month TEXT;

-- Relance J+3 déjà envoyée (une seule fois par compte).
ALTER TABLE users ADD COLUMN IF NOT EXISTS upsell_j3_sent BOOLEAN DEFAULT FALSE;

-- Sécurité : la relance J+3 a besoin d'une date de création. Si la colonne n'existe
-- pas encore, on l'ajoute (par défaut = maintenant pour les lignes existantes).
ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();

-- Index pour la requête quotidienne de relance (Free récents).
CREATE INDEX IF NOT EXISTS idx_users_free_created ON users (tier, created_at)
  WHERE tier = 'free';
