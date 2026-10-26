-- ✉️ E-mails d'essai v2 (lot 3) — journal des envois et langue de l'utilisateur.
--
-- email_log : une ligne par e-mail envoyé (ou simulé). La contrainte d'unicité
-- (email, cle) garantit qu'une même personne ne reçoit jamais deux fois le même
-- e-mail, même si deux passages du cron se chevauchent.
--
-- users.lang : langue choisie à l'inscription (fr, en, pt-br, es, es-mx, it, de),
-- pour écrire les e-mails dans la langue de l'utilisateur. Absente = français.
--
-- Sans cette migration, la séquence fonctionne quand même : le journal retombe
-- sur market_cache (comme avant) et les e-mails partent en français.
--
-- À jouer une fois dans Supabase → SQL Editor. Rejouable sans risque.

CREATE TABLE IF NOT EXISTS email_log (
    id          BIGSERIAL PRIMARY KEY,
    email       TEXT NOT NULL,
    cle         TEXT NOT NULL,           -- bienvenue, h24, j3_radar, j3_creation, j6, j7, j10, hebdo:2026-W44…
    statut      TEXT NOT NULL,           -- envoye | simule
    envoye_le   TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (email, cle)
);
CREATE INDEX IF NOT EXISTS idx_email_log_envoye ON email_log (envoye_le DESC);

ALTER TABLE email_log ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "email_log_deny_direct_access" ON email_log;
CREATE POLICY "email_log_deny_direct_access" ON email_log FOR ALL USING (false) WITH CHECK (false);

ALTER TABLE users ADD COLUMN IF NOT EXISTS lang TEXT;
