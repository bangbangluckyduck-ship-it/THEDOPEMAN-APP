-- 🎯 Mission d'essai v2 — « Fais ton premier diagnostic en 60 secondes » (lot 1).
--
-- Une ligne par compte : la date de chaque étape et le résumé des deux vidéos
-- comparées (vidéo qui vend / vidéo de l'utilisateur). Suit l'utilisateur sur
-- tous ses appareils et sert aux e-mails d'essai (lot 3).
--
-- Sans cette table, l'app reste utilisable : mission.py déduit alors l'état des
-- analyses et des générations existantes, sans le comparatif.
--
-- À jouer une fois dans Supabase → SQL Editor. Rejouable sans risque.

CREATE TABLE IF NOT EXISTS trial_mission (
    email         TEXT PRIMARY KEY,
    etape1_at     TIMESTAMPTZ,          -- une vidéo qui vend analysée (accueil compris)
    etape2_at     TIMESTAMPTZ,          -- SA dernière vidéo analysée
    etape3_at     TIMESTAMPTZ,          -- accroches générées pour son produit
    termine_at    TIMESTAMPTZ,          -- les trois étapes faites
    ref_resume    JSONB,                -- résumé de la vidéo qui vend (score, accroche, CTA, dimensions)
    perso_resume  JSONB,                -- résumé de sa vidéo
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Accès réservé au serveur : la clé service contourne RLS, la clé publique est
-- refusée (même verrou que `users`, cf. supabase_migrations_lockdown_sensitive_tables.sql).
ALTER TABLE trial_mission ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "trial_mission_deny_direct_access" ON trial_mission;
CREATE POLICY "trial_mission_deny_direct_access" ON trial_mission FOR ALL USING (false) WITH CHECK (false);
