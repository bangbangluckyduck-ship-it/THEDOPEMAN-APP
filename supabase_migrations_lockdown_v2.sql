-- ════════════════════════════════════════════════════════════════════════
-- VERROUILLAGE SÉCURITÉ v2 — politiques « ouvertes à tous » (audit 2026-11-12, S3)
--
-- Constat en base (pg_policies, 2026-11-12) : 16 tables ont des politiques
-- `FOR ALL TO public USING (true) [WITH CHECK (true)]`, et le rôle anon garde
-- le droit SELECT. Avec la clé anon, n'importe qui pouvait donc lire, modifier
-- ou supprimer crédits, achats, favoris, journaux de visite… via l'API REST.
--
-- Le backend utilise supabase_service (clé service_role, qui ignore RLS) :
-- vérifié dans les journaux Supabase (100 % des requêtes du serveur sur 24 h
-- en service_role). Seul insights_store.py utilisait encore le client anon ;
-- il passe à supabase_service dans le même changement. AUCUN impact attendu
-- côté app.
--
-- Même méthode que supabase_migrations_lockdown_sensitive_tables.sql, plus le
-- retrait des droits SQL (une politique RLS seule ne retire pas les GRANT).
-- Idempotent : peut être rejoué sans risque.
-- ════════════════════════════════════════════════════════════════════════

DO $$
DECLARE
  pol RECORD;
  tbl TEXT;
BEGIN
  FOREACH tbl IN ARRAY ARRAY[
    'analytics_config', 'analyzed_insights', 'analyzed_products',
    'anonymous_generations', 'credit_purchases', 'daily_visitor_stats',
    'feed_radar_videos', 'market_cache', 'one_time_purchases',
    'photo_slide_generations', 'script_generations', 'user_credits',
    'user_favorites', 'video_prompt_generations', 'viral_videos_cache',
    'visitor_logs'
  ]
  LOOP
    -- Table absente dans cet environnement : on passe (migration rejouable partout)
    IF to_regclass(format('public.%I', tbl)) IS NULL THEN
      RAISE NOTICE 'Table % absente, ignorée', tbl;
      CONTINUE;
    END IF;

    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', tbl);

    -- Supprime toutes les politiques existantes (toutes « USING (true) » au 2026-11-12)
    FOR pol IN SELECT policyname FROM pg_policies WHERE schemaname = 'public' AND tablename = tbl
    LOOP
      EXECUTE format('DROP POLICY IF EXISTS %I ON public.%I', pol.policyname, tbl);
    END LOOP;

    -- Accès direct explicitement refusé pour anon/authenticated
    EXECUTE format(
      'CREATE POLICY %I ON public.%I FOR ALL USING (false) WITH CHECK (false)',
      tbl || '_deny_direct_access', tbl
    );

    -- Retire aussi les droits SQL : la clé anon ne doit plus rien pouvoir faire ici
    EXECUTE format('REVOKE ALL ON public.%I FROM anon, authenticated', tbl);
  END LOOP;
END $$;

-- Vérification : 0 ligne attendue (plus aucune politique ouverte ni droit anon sur ces tables)
SELECT p.tablename, p.policyname, p.qual,
       has_table_privilege('anon', format('public.%I', p.tablename), 'SELECT') AS anon_select
FROM pg_policies p
WHERE p.schemaname = 'public'
  AND p.tablename IN ('analytics_config', 'analyzed_insights', 'analyzed_products',
    'anonymous_generations', 'credit_purchases', 'daily_visitor_stats',
    'feed_radar_videos', 'market_cache', 'one_time_purchases',
    'photo_slide_generations', 'script_generations', 'user_credits',
    'user_favorites', 'video_prompt_generations', 'viral_videos_cache', 'visitor_logs')
  AND (p.qual = 'true' OR p.with_check = 'true'
       OR has_table_privilege('anon', format('public.%I', p.tablename), 'SELECT'));
