# Aether Release Readiness

Last checked: 2026-11-13 12:55 UTC

## Current decision

**NO-GO for public launch or production deployment.** The integrated development release candidate passes all three GitHub Actions workflows, and the existing Supabase Free project has now returned to ACTIVE_HEALTHY. Its ten recorded migrations, application tables, RLS flags and private document bucket are visible again. The remaining blockers are deployed-version mismatch, unverified live runtime/configuration, staging end-to-end and rollback evidence, and incomplete operational/privacy launch sign-off.

Aether must be described as a synthetic/sandbox workflow platform unless and until a specific government connector is authorized, source-backed, tested and reconciled against the authority's system of record. Internal task completion is not an official government outcome.

## Verified repository state

- Repository: `amirmohd4/Aether`.
- Development branch: `aether-mvp-build`.
- Current reviewed head: `f6439b1f091d211027c58607876e1d3f57f3db2b`.
- Pull request #11 targets `main`, remains open and unmerged. Do not merge until deployment and release gates below pass.
- India administrative-intelligence increment is integrated: India-wide discovery taxonomy, three illustrative cross-department journey templates, authenticated read APIs and frontend explorer.
- On current head `f6439b1f091d211027c58607876e1d3f57f3db2b`, all three workflows completed successfully:
  - Aether MVP Tests: backend compile and pytest passed.
  - Aether MVP Frontend: TypeScript lint and Vite build passed.
  - Aether MVP CI: backend tests and frontend typecheck/build passed.
- README and product charter correctly constrain the MVP to synthetic workflows; no official government decisions/documents are issued.

## Supabase — restored and database-accessible

- Existing project: `aether`, ref `lekudqjewxxunqjuqayi`.
- Organization plan: `free` / `tier_free`. No new project or paid upgrade was created.
- Project API now reports `ACTIVE_HEALTHY` after restore.
- Supabase migration history reports 10 applied migrations.
- Database inspection confirms 13 public application tables and 10 `aether_internal` execution tables.
- RLS is enabled on all 13 public application tables and all 10 internal execution tables.
- The `aether_runtime` role exists. Internal execution tables have server-runtime-only policies; public legacy tables deny browser-role access; membership read policy is scoped to the authenticated user's own membership.
- The `aether-documents` bucket exists and is private (`public=false`).
- Supabase Security Advisor returned no security lints; Health Advisor returned no health lints.
- Performance Advisor returned 39 informational unused-index findings. Do not drop indexes without representative workload measurements; an idle/new database can naturally report unused indexes.
- These are database configuration checks, not proof that the deployed Render backend has the correct credentials or can authenticate and perform real document uploads.

## Render — deployment branch mismatch / runtime unverified

- `aether-backend` is on the Free plan, deploys from `main`, and its latest recorded live deployment is commit `f64148aad10a5f8f586efde0cefe7a817fe6d996` from 2026-10-15. It is not running the current development release candidate.
- `aether-public-demo` is on the Free plan, deploys from `launch/public-research-preview`, and its latest recorded live deployment is commit `eb148e6dc6866ea0a5214b01d9f908a89d94a264` from 2026-10-29.
- The public demo service has no configured Render health-check path; the backend has `/health`.
- Render returned no application logs or service events in the checked period. Direct public endpoint verification was not available. A `live` deployment label alone does not prove API health, database readiness or authentication.
- Do not merge PR #11 until a controlled staging deployment and its health/readiness endpoints are verified.

## Worker deployment gap

- Repository `render.yaml` declares a web service and a separate `aether-worker` service.
- The connected Render workspace lists only `aether-backend` and `aether-public-demo`; no separate `aether-worker` service is present.
- The backend blueprint supports embedded worker mode through `AETHER_EMBED_WORKER=true`, but the live service's environment and worker tick logs are not available for verification.
- Verify embedded worker execution or configure an existing Free-plan-compatible worker arrangement; do not create a paid service without explicit approval.

## Frontend, authentication and configuration

- Frontend code/build passes CI. Repository configuration uses the public Supabase publishable key; no service-role key should ever be exposed to browser assets.
- Render connector responses do not expose environment-variable values, so backend `DATABASE_URL`, `SUPABASE_URL`, publishable key, service-role key, encryption key, auth mode, CORS and worker settings are not independently verified here.
- The deployed frontend/backend pairing is not proven to use the same release candidate.
- `/ready` performs a database connection check and should return ready only when the deployed backend can reach PostgreSQL. `/release/readiness` must be checked in the actual staging environment.

## Go/no-go gates

- [x] Existing Supabase project restored to ACTIVE_HEALTHY on the Free plan.
- [x] Ten applied migrations, 13 public tables, 10 internal tables, RLS enabled on all application tables, runtime role and private document bucket verified.
- [x] Current development-head backend tests, frontend lint/build and combined CI passed.
- [ ] Render backend deployed from an approved release commit; `/health`, `/ready` and `/release/readiness` verified.
- [ ] Render environment variables and secret wiring verified without exposing secrets; database, Supabase Auth, encryption and storage operations tested from the deployed backend.
- [ ] Frontend deployed from the same release candidate and configured to the intended backend/auth mode; no server secrets in browser assets.
- [ ] Worker execution verified, or asynchronous execution disabled and accurately disclosed.
- [ ] Staging end-to-end scenarios cover intake, evidence upload/read, tenant isolation, queue/retry recovery, human approval, audit trail, exception handling and outcome reconciliation.
- [ ] Tenant isolation, authentication, authorization, document encryption, retention/deletion and audit controls tested.
- [ ] Rate limits, CORS, security headers, error handling and operational monitoring checked against deployed configuration.
- [ ] Rollback procedure and known-good deployment verified.
- [ ] Privacy notice, terms, accessibility, incident response and support ownership ready.
- [ ] Every live government service independently passes legal authorization, source verification, connector certification and system-of-record reconciliation.

## Release policy

Do not merge to `main`, deploy publicly or announce production readiness merely because CI passes. First align the deployment branch, verify the deployed backend can use the restored Free Supabase project, run staging end to end, confirm worker behavior and prove rollback. A controlled synthetic demo may be shared only if its environment is isolated, runtime is verified and it is clearly labelled synthetic. Never present it as an official government workflow or outcome.
