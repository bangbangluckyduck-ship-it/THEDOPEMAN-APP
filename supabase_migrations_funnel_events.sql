-- 📈 Mesure du tunnel (lot 6) — événements anonymes, avec langue.
--
-- Une ligne = un événement du tunnel : visite de l'accueil, analyse sans compte,
-- résultat affiché, clic « débloquer », inscription (detail = google | email),
-- étapes de mission, essai arrivé à terme, paiement (detail = mensuel | annuel),
-- paiement échoué, pause, résiliation, e-mail envoyé / cliqué (detail = clé).
--
-- AUCUNE donnée personnelle : ni e-mail, ni IP, ni identifiant de compte —
-- mesure d'audience exemptée de consentement, indépendante du bandeau cookies.
-- Requêtes prêtes à l'emploi : docs/README_ENTONNOIR.md.
--
-- Sans cette table, les événements retombent dans visitor_logs (sans langue).
-- À jouer une fois dans Supabase → SQL Editor. Rejouable sans risque.

CREATE TABLE IF NOT EXISTS funnel_events (
    id          BIGSERIAL PRIMARY KEY,
    evenement   TEXT NOT NULL,
    lang        TEXT,                    -- fr, en, en-ie, pt-br, es, es-mx, it, de (ou null)
    detail      TEXT,                    -- 40 caractères max, jamais une donnée personnelle
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_funnel_events_evt_date ON funnel_events (evenement, created_at DESC);

ALTER TABLE funnel_events ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "funnel_events_deny_direct_access" ON funnel_events;
CREATE POLICY "funnel_events_deny_direct_access" ON funnel_events FOR ALL USING (false) WITH CHECK (false);
