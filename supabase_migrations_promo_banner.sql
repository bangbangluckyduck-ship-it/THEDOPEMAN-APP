-- ════════════════════════════════════════════════════════════════════════
-- BANDEAU PROMOTIONNEL — piloté depuis /dope-admin
--
-- Une seule ligne (singleton, id = 1). L'échéance `ends_at` est la source de
-- vérité : le bandeau disparaît de lui-même quand elle est passée, sans
-- intervention. Le décompte affiché est donc réel et identique pour tous les
-- visiteurs — il ne redémarre pas par session.
--
-- Additive, idempotente, réversible (DROP TABLE promo_banner).
-- ════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS promo_banner (
    id          SMALLINT PRIMARY KEY DEFAULT 1,
    active      BOOLEAN     NOT NULL DEFAULT false,
    message     TEXT,                     -- ex. « -20 % sur Qeerah Pro »
    code        TEXT,                     -- code promo Stripe à saisir au paiement
    cta_label   TEXT,                     -- ex. « En profiter »
    cta_url     TEXT DEFAULT '/pricing',
    ends_at     TIMESTAMPTZ,              -- échéance réelle ; NULL = pas de décompte
    updated_at  TIMESTAMPTZ DEFAULT now(),
    CONSTRAINT promo_banner_singleton CHECK (id = 1)
);

INSERT INTO promo_banner (id, active, message, code, cta_label, cta_url)
VALUES (1, false, '', '', 'En profiter', '/pricing')
ON CONFLICT (id) DO NOTHING;

-- Lecture publique nécessaire ? NON : le bandeau est servi par le backend via
-- /api/promo (service_role). La table reste donc fermée à la clé anon, comme
-- users et analysis_quota_periods.
ALTER TABLE promo_banner ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE pol RECORD;
BEGIN
  FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = 'promo_banner'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON promo_banner', pol.policyname);
  END LOOP;
  CREATE POLICY promo_banner_deny_direct_access
      ON promo_banner FOR ALL USING (false) WITH CHECK (false);
END $$;

-- Vérification : 1 ligne, 1 policy de refus
SELECT (SELECT count(*) FROM promo_banner)                                   AS lignes,
       (SELECT count(*) FROM pg_policies
          WHERE tablename = 'promo_banner' AND qual = 'false')               AS verrouillee;
