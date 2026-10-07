# Supabase Security Release Plan

## Current deployed security posture

The connected Aether Supabase project has been hardened for the controlled MVP release.

The legacy/public application tables identified during the release review now have Row Level Security enabled with deny-by-default browser access where direct client access is not required. A server-controlled `public.aether_memberships` table is used to resolve tenant and role membership.

The private execution schema also has RLS enabled. The internal `aether_internal` tables intentionally have no browser-facing policies because the Aether API/worker is the only access path; anon/authenticated browser roles do not receive privileges on these tables.

This is the correct controlled-MVP posture: private execution state stays server-side while the public application surface uses Aether API authorization.

## Required authorization model

Aether uses:
1. Supabase Auth identity for browser authentication.
2. Server-controlled tenant/membership records in `public.aether_memberships`.
3. Roles such as citizen, business, bank, developer, insurer, officer, department_admin and admin.
4. Server-side ownership, tenant, department and jurisdiction checks.
5. Backend/service-role access for privileged internal execution and government connectors.
6. No service-role or database secrets in frontend code.

## Verification completed

The deployed project was checked for:
- RLS enabled on the legacy application tables and internal execution tables.
- Private `aether-documents` storage bucket.
- Server-only access to internal execution tables.
- No critical Supabase security-advisor RLS findings.

Supabase may still report informational `rls_enabled_no_policy` notices for intentional internal tables. These are expected because browser roles are not granted access to those tables.

## Production gate still outstanding

The controlled MVP is not a claim of live government authority. Before any real production-government declaration, Aether still requires:
- authorized live government connectors and sandbox/certification access;
- authoritative effective-dated legal/rule data for each launch jurisdiction and service;
- certified statutory signature/issuance integrations;
- production OCR, notification and payment provider credentials;
- tenant/department/jurisdiction penetration testing;
- final production load/chaos testing.

Those are external authorization/integration prerequisites and must not be simulated as completed.
