# Aether Release Readiness

Last checked: 2026-11-13 18:00 UTC

## Current decision

**NO-GO for public launch until a deployed staging run passes.** The core GovOS software scope remains unchanged and is implemented in the development branch. The latest reviewed release-candidate code passed backend tests, frontend typecheck/build and combined CI. Supabase is restored and its schema/security posture has been checked. New release gates now verify the actual private document bucket and require the least-privilege database role.

The remaining critical work is deployment configuration and end-to-end proof: Render still runs older commits from older branches; the runtime database role/password and Supabase service credentials are not exposed for verification; no staging URLs/API key are configured in GitHub; and the new staging smoke job therefore skipped. Do not merge PR #11 into `main` yet.

Aether's first release is the existing India-first AI Government Execution Platform / GovOS, operating against synthetic government systems. It must not claim official government filing, approval or certificate issuance.

## Verified repository and code

- Repository: `amirmohd4/Aether`.
- Development branch: `aether-mvp-build`.
- Reviewed release-candidate commit: `d0f9c4502f811bfd16cd122216ee8b60fae0f9d8`.
- PR #11 targets `main`, remains open and unmerged. Keep it unmerged until staging and rollback gates pass.
- Product scope is unchanged: objective understanding, requirements discovery, shared service catalog, cross-department process/work graphs, dependency-aware execution, evidence/document handling, human authority boundaries, audit/reconciliation, operator/developer surfaces and India administrative intelligence.
- The India module contains an India-wide discovery taxonomy, three illustrative cross-department journey templates, authenticated read APIs and a frontend explorer. These are planning aids, not exhaustive statutory checklists.
- On code commit `d0f9c4502f811bfd16cd122216ee8b60fae0f9d8`, all core CI passed:
  - Aether MVP Tests: Python compilation and complete backend pytest suite passed.
  - Aether MVP CI: backend tests and frontend typecheck/build passed.
  - Aether MVP Frontend: TypeScript check and Vite production build passed.
  - Administrative action worker workflow passed.
- Added regression tests for explicit worker configuration, private storage readiness and database runtime-role enforcement.
- `/ready` now rejects a staging/production connection unless `current_user` matches `AETHER_DATABASE_EXPECTED_ROLE`.
- `/api/aether/v2/release/readiness` now checks that the real Supabase Storage bucket exists and is private, rather than trusting environment-variable presence; it also requires explicit embedded-worker or worker-command configuration.
- `render.yaml` now specifies one Free backend web service with an embedded worker, rather than creating a separate worker service. This avoids a second Render resource for the controlled MVP.
- Authenticated smoke coverage now includes service catalog, marketplace, connectors, rule readiness, India admin overview/departments/journeys and controlled release readiness.

## Supabase — verified

- Existing project: `aether`, ref `lekudqjewxxunqjuqayi`.
- Organization plan: `free` / `tier_free`; no replacement project or upgrade was created.
- Project status: `ACTIVE_HEALTHY`.
- Ten migrations recorded as applied.
- Thirteen public application tables and ten `aether_internal` execution tables.
- RLS enabled on all 23 application tables.
- Dedicated `aether_runtime` role exists as a non-superuser login role.
- Browser roles have no access to internal execution tables; runtime role has required internal access.
- `aether-documents` exists and is private (`public=false`).
- Supabase Security and Health Advisors returned no lints.
- Performance Advisor reported 39 informational unused-index findings. No indexes were removed without workload evidence.
- Database inspection through the Supabase administration connection does not prove Render uses the `aether_runtime` role. The deployed backend must pass the new `/ready` role check.

## Render — release deployment outstanding

- `aether-backend` is Free, deploys from `main`, and latest recorded live deployment is `f64148aad10a5f8f586efde0cefe7a817fe6d996` (2026-10-15). It is not running the current release candidate.
- `aether-public-demo` is Free, deploys from `launch/public-research-preview`, and latest recorded live deployment is `eb148e6dc6866ea0a5214b01d9f908a89d94a264` (2026-10-29).
- The backend service uses `/health` as its Render health check. `/ready` is the database/role readiness gate.
- No separate worker service exists in the connected Render workspace. The updated blueprint uses the embedded worker to avoid creating another service. Its actual ticks still need to be verified after deployment.
- Render service-detail responses do not expose environment-variable values. The following deployed values are therefore not independently verified: `DATABASE_URL`, `AETHER_DATABASE_PASSWORD`, `AETHER_DATABASE_ROLE_OVERRIDE`, `AETHER_DATABASE_EXPECTED_ROLE`, Supabase service-role key, encryption key, auth mode and CORS.
- The runbook now documents the least-privilege `aether_runtime` role configuration. Render must receive the matching database-role password as a secret; never commit it.
- Direct public endpoint checks were inaccessible from the current environment. Render logs/events previously returned no application entries; this is not proof of runtime health.

## Staging smoke automation

- Added `.github/workflows/aether-staging-smoke.yml`.
- It runs on pushes to `aether-mvp-build` and accepts explicit API/frontend URLs for manual dispatch once available.
- It checks `/health`, `/ready` (including the expected database role), root API and frontend HTML, then runs authenticated product/release smoke checks.
- The latest workflow run completed with the `staging-not-configured` notice job; the actual `staging-smoke` job was skipped because staging URLs are not configured.
- Required GitHub repository variables: `AETHER_STAGING_API_URL`, `AETHER_STAGING_FRONTEND_URL`.
- Required GitHub repository secret for authenticated coverage: `AETHER_STAGING_API_KEY` (read-only Aether API key with `cases:read` scope).
- The smoke run is not evidence of a successful staging deployment until those values are set and the staging-smoke job itself completes.

## Frontend

- Frontend TypeScript check and Vite production build passed in CI.
- Current `netlify.toml` points at the existing backend URL and existing Supabase project.
- The deployed frontend/backend pair is not verified to use the current release candidate. A staging frontend must use the staging API URL and public Supabase publishable key.
- No service-role key, database password or encryption key may be placed in frontend assets.

## Go/no-go gates

- [x] Existing Supabase Free project restored to ACTIVE_HEALTHY.
- [x] Ten migrations, 13 public tables, ten internal tables, RLS, runtime role and private bucket verified.
- [x] Core backend tests, frontend lint/build and combined CI passed on reviewed release-candidate code.
- [x] Readiness checks hardened for private storage, explicit worker configuration and least-privilege database role.
- [x] Staging deployment runbook and automated smoke workflow added.
- [ ] Configure the `aether_runtime` password in Supabase and matching Render secret; verify deployed `/ready` returns HTTP 200 with `database_role_valid=true`.
- [ ] Deploy the reviewed release candidate to an isolated staging API and matching frontend without replacing the current production service.
- [ ] Configure GitHub staging URL variables and authenticated smoke secret; run the actual staging-smoke job.
- [ ] Verify deployed Supabase Auth, private document upload/read, encryption and tenant isolation.
- [ ] Verify embedded worker ticks, durable case recovery, retries and notification outbox.
- [ ] Run complete citizen/business and officer/operator journeys end to end in synthetic mode.
- [ ] Verify monitoring, CORS, rate limits, security headers, privacy disclosures, accessibility and support ownership.
- [ ] Demonstrate rollback to a known-good backend/frontend pair.
- [ ] Only then review and merge PR #11 to `main`.

## Release policy

Do not merge PR #11, switch to production mode or enable live government connectors merely because CI passes. First configure and deploy staging, verify the least-privilege database identity and private storage, run authenticated end-to-end smoke tests, prove worker behavior and rollback. The initial release remains a synthetic/sandbox GovOS; each live government connector requires written authorization, approved credentials/endpoints, authoritative effective-dated rules, certification and system-of-record reconciliation.
