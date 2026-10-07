-- Legacy schema lockdown for the Aether MVP.
-- The current MVP UI uses the V2 execution API; legacy tables are therefore
-- server-only until each one is migrated to the new case/tenant model.
--
-- RLS is deny-by-default for browser roles. Backend connections using the
-- database/service role are unaffected by RLS.

DO $$
DECLARE
  table_name text;
BEGIN
  FOREACH table_name IN ARRAY ARRAY[
    'citizens',
    'api_keys',
    'properties',
    'certificates',
    'workflow_states',
    'fraud_detection_logs',
    'trade_licenses',
    'building_permits',
    'water_connections',
    'birth_certificates',
    'death_certificates',
    'medical_licenses'
  ]
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_name);

    EXECUTE format(
      'DROP POLICY IF EXISTS "%s deny browser access" ON public.%I',
      table_name,
      table_name
    );

    EXECUTE format(
      'CREATE POLICY "%s deny browser access" ON public.%I
       FOR ALL TO anon, authenticated
       USING (false)
       WITH CHECK (false)',
      table_name,
      table_name
    );

    EXECUTE format('REVOKE ALL ON TABLE public.%I FROM anon, authenticated', table_name);
  END LOOP;
END
$$;
