-- 🔁 Fidélisation (lot 5) — e-mail hebdo, paiement en retard, pause, raisons de départ.
--
-- users.hebdo_opt_out            : l'abonné ne veut plus de l'e-mail hebdo
--                                  (« Ce qui vend cette semaine »). Indépendant
--                                  de marketing_opt_out, qui coupe tout.
-- users.paiement_en_retard_depuis : premier échec de paiement non résolu (null =
--                                  à jour). Affiche le bandeau « mets ta carte à
--                                  jour » dans l'app.
-- users.pause_fin                : fin de la pause d'un mois (Stripe
--                                  pause_collection.resumes_at). Null = pas de pause.
-- cancel_feedback                : réponse facultative avant une résiliation.
--
-- Sans cette migration : l'e-mail hebdo respecte marketing_opt_out, le bandeau
-- et la pause ne s'affichent pas, la raison n'est pas enregistrée — rien ne casse.
--
-- À jouer une fois dans Supabase → SQL Editor. Rejouable sans risque.

ALTER TABLE users ADD COLUMN IF NOT EXISTS hebdo_opt_out BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS paiement_en_retard_depuis TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN IF NOT EXISTS pause_fin TIMESTAMPTZ;

CREATE TABLE IF NOT EXISTS cancel_feedback (
    id          BIGSERIAL PRIMARY KEY,
    email       TEXT NOT NULL,
    raison      TEXT NOT NULL,          -- trop_cher | pas_assez_utilise | il_manque | autre
    detail      TEXT,                   -- texte libre facultatif (« autre », « il manque… »)
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_cancel_feedback_date ON cancel_feedback (created_at DESC);

ALTER TABLE cancel_feedback ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "cancel_feedback_deny_direct_access" ON cancel_feedback;
CREATE POLICY "cancel_feedback_deny_direct_access" ON cancel_feedback FOR ALL USING (false) WITH CHECK (false);
