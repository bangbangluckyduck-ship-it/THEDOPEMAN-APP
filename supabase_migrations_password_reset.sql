-- Supabase Migration: Create password_reset_tokens table
-- Run this in your Supabase SQL editor to set up password reset functionality

CREATE TABLE IF NOT EXISTS password_reset_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL,
  reset_token TEXT NOT NULL,
  token_type TEXT NOT NULL CHECK (token_type IN ('temporary_password', 'magic_link')),
  new_password TEXT,  -- Hash bcrypt du nouveau mot de passe (si type='temporary_password')
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  used BOOLEAN DEFAULT FALSE,
  ip_address TEXT,

  CONSTRAINT fk_email FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
);

-- Indices pour optimiser les requêtes
CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_email ON password_reset_tokens(email);
CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_created ON password_reset_tokens(created_at);
CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_expires ON password_reset_tokens(expires_at);
CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_used ON password_reset_tokens(used);

-- Politique de sécurité RLS (optionnel mais recommandé)
ALTER TABLE password_reset_tokens ENABLE ROW LEVEL SECURITY;

-- Allow reads only for verification (no direct user access, backend only)
CREATE POLICY "password_reset_backend_only" ON password_reset_tokens
  FOR SELECT
  USING (FALSE);  -- Aucun accès direct

-- Nettoyer les tokens expiréés (créer une fonction pour maintenance périodique)
-- Cette fonction peut être appelée manuellement ou via cron
CREATE OR REPLACE FUNCTION cleanup_expired_reset_tokens()
RETURNS void AS $$
BEGIN
  DELETE FROM password_reset_tokens
  WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;
