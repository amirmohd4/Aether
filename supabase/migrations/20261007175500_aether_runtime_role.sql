-- Runtime identity for the Aether API/worker.
-- Password is intentionally managed as a Render secret, never stored in Git.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'aether_runtime') THEN
    CREATE ROLE aether_runtime LOGIN;
  END IF;
END
$$;

GRANT USAGE ON SCHEMA public TO aether_runtime;
GRANT USAGE ON SCHEMA aether_internal TO aether_runtime;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.aether_memberships TO aether_runtime;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA aether_internal TO aether_runtime;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA aether_internal TO aether_runtime;

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'aether_v2_api_keys',
    'aether_v2_case_leases',
    'aether_v2_cases',
    'aether_v2_documents',
    'aether_v2_execution_events',
    'aether_v2_notifications',
    'aether_v2_payments',
    'aether_v2_task_checkpoints',
    'aether_v2_task_queue',
    'aether_v2_usage'
  ]
  LOOP
    IF NOT EXISTS (
      SELECT 1
      FROM pg_policies
      WHERE schemaname = 'aether_internal'
        AND tablename = table_name
        AND policyname = 'aether_runtime_full_access'
    ) THEN
      EXECUTE format(
        'CREATE POLICY aether_runtime_full_access ON aether_internal.%I FOR ALL TO aether_runtime USING (true) WITH CHECK (true)',
        table_name
      );
    END IF;
  END LOOP;

  IF NOT EXISTS (
    SELECT 1
    FROM pg_policies
    WHERE schemaname = 'public'
      AND tablename = 'aether_memberships'
      AND policyname = 'aether_runtime_full_access'
  ) THEN
    CREATE POLICY aether_runtime_full_access
      ON public.aether_memberships
      FOR ALL TO aether_runtime
      USING (true)
      WITH CHECK (true);
  END IF;
END
$$;

DROP TABLE IF EXISTS aether_internal.aether_runtime_bootstrap;
