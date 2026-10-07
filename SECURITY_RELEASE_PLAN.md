# Supabase Security Release Plan

## Current finding

Supabase's security advisor currently reports RLS disabled on 14 tables:
- public.citizens
- public.api_keys
- public.properties
- public.certificates
- public.workflow_states
- public.fraud_detection_logs
- public.trade_licenses
- public.building_permits
- public.water_connections
- public.birth_certificates
- public.death_certificates
- public.medical_licenses
- aether_internal.aether_v2_cases
- aether_internal.aether_v2_execution_events

This is a release blocker for production because exposed tables without RLS can be reachable by anon/authenticated clients.

## Do not apply yet

The remediation below is intentionally not executed on the connected Supabase project. Enabling RLS without matching policies can block legitimate application access, while generic authenticated-can-read-everything policies would create an authorization vulnerability.

## Required authorization model

Aether should use:
1. Supabase Auth identity via auth.uid().
2. Aether tenant/membership records stored in server-controlled data, not user-editable user metadata.
3. Roles such as citizen, business, bank, developer, insurer, officer, department_admin, admin.
4. Explicit object ownership or tenant predicates for every exposed row.
5. Backend/service-role access only for privileged government connectors and internal workers.
6. No service-role or secret credentials in the browser.

## Internal V2 policy shape

Before enabling RLS on aether_internal tables, add:
- owner_user_id uuid to aether_v2_cases
- tenant_id uuid to aether_v2_cases
- matching tenant_id to execution events and queue
- a server-controlled membership table mapping auth.uid() to tenant and role

Then use policies conceptually equivalent to:

    CREATE POLICY "case members can read their tenant cases"
    ON aether_internal.aether_v2_cases
    FOR SELECT TO authenticated
    USING (
      tenant_id = (
        SELECT tenant_id
        FROM public.aether_memberships
        WHERE user_id = (SELECT auth.uid())
          AND status = 'active'
      )
    );

    CREATE POLICY "case owners can create cases"
    ON aether_internal.aether_v2_cases
    FOR INSERT TO authenticated
    WITH CHECK (
      owner_user_id = (SELECT auth.uid())
      AND tenant_id = (
        SELECT tenant_id
        FROM public.aether_memberships
        WHERE user_id = (SELECT auth.uid())
          AND status = 'active'
      )
    );

The exact policy set must be finalized after the membership table and case ownership columns are migrated.

## Legacy public tables

The existing legacy tables should not receive broad authenticated read/write policies. For tables no longer used directly by the MVP UI, the safest interim policy is deny-by-default while backend access is migrated behind the Aether API.

Example pattern:

    ALTER TABLE public.<legacy_table> ENABLE ROW LEVEL SECURITY;

    CREATE POLICY "<legacy_table> deny public client access"
    ON public.<legacy_table>
    FOR ALL TO anon, authenticated
    USING (false)
    WITH CHECK (false);

Only tables that genuinely need direct client access should receive narrower ownership/tenant policies.

## Release gate

Production deployment must not proceed until:
- RLS is enabled on all exposed data tables.
- Every table has a deliberate policy set.
- API/service credentials are server-side only.
- Authenticated users cannot read another tenant's case or evidence.
- Officers can only access cases authorized for their department and jurisdiction.
- Sensitive tables such as api_keys remain inaccessible from the browser.
- RLS tests cover SELECT, INSERT, UPDATE, and DELETE behavior.
- Supabase security advisor returns no critical RLS findings.