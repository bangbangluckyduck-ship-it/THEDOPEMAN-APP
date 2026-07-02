-- ════════════════════════════════════════════════════════════════════════
-- VERROUILLAGE SÉCURITÉ — tables sensibles accessibles en lecture via la
-- clé anon (users, tiktok_tokens, password_reset_tokens confirmés lisibles
-- en direct le 2026-07-02 : emails, access_token TikTok, tokens de reset
-- mot de passe + hash bcrypt du nouveau mot de passe, tous exposés).
--
-- Le code backend a été migré pour utiliser supabase_service (clé
-- service_role, bypasse RLS) sur ces tables — ce verrouillage RLS ne casse
-- rien côté app, il retire uniquement l'accès direct via la clé anon.
--
-- Robuste aux noms de policies inconnus (certaines tables prédatent la
-- convention de migration de ce repo) : supprime TOUTES les policies
-- existantes sur chaque table avant de recréer un accès explicitement
-- refusé pour anon/authenticated.
-- ════════════════════════════════════════════════════════════════════════

DO $$
DECLARE
  pol RECORD;
  tbl TEXT;
BEGIN
  FOREACH tbl IN ARRAY ARRAY['users', 'tiktok_tokens', 'password_reset_tokens',
                              'monthly_usage', 'daily_usage', 'recherche_search_usage']
  LOOP
    -- Active RLS (idempotent si déjà activé)
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', tbl);

    -- Supprime toute policy existante sur cette table, quel que soit son nom
    FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = tbl
    LOOP
      EXECUTE format('DROP POLICY IF EXISTS %I ON %I', pol.policyname, tbl);
    END LOOP;

    -- Recrée un accès explicitement refusé (anon/authenticated). Le backend
    -- utilise service_role, qui bypasse RLS par nature — aucun impact sur l'app.
    EXECUTE format(
      'CREATE POLICY %I ON %I FOR ALL USING (false) WITH CHECK (false)',
      tbl || '_deny_direct_access', tbl
    );
  END LOOP;
END $$;

-- Vérification : doit renvoyer 1 policy "USING (false)" par table listée ci-dessus.
SELECT tablename, policyname, qual
FROM pg_policies
WHERE tablename IN ('users', 'tiktok_tokens', 'password_reset_tokens',
                     'monthly_usage', 'daily_usage', 'recherche_search_usage')
ORDER BY tablename;
