# Aether Release Readiness

Last checked: 2026-11-15

## Release decision

**NO-GO for a production GovOS launch.** The current candidate is suitable for continued controlled synthetic-preview validation, but it is not yet proven as a fully operational end-to-end release.

The active candidate is PR [#20](https://github.com/amirmohd4/Aether/pull/20), branch `integration-check/public-preview-into-hardened`, head commit `552ca35e48db859b178e61eb5c1c9ea44b7a1e53`. It remains an open draft and must not be merged until the release gates below pass.

Aether's first public experience must remain an independent synthetic research preview. It does not submit official government applications, access private government records, issue certificates, or make statutory decisions. Live integrations require written authorization, approved credentials/endpoints, authoritative effective-dated rules, certification, and system-of-record reconciliation.

## Candidate scope

The PR description records the intended candidate scope:
- 34-service registry, objective understanding, requirements discovery and jurisdiction-aware process planning.
- Cross-department work graphs, dependency-aware execution, retries, checkpoints, case recovery and reconciliation.
- Evidence/document workflows, private storage adapter, audit chain, tenant/RBAC controls and scoped API keys.
- Operator/officer workspaces, India administrative intelligence and developer marketplace foundations.
- Synthetic workflow studio, five demonstration scenarios, research-preview landing pages and feedback experience.

These are implementation claims and product scope, not proof that every journey has passed deployed end-to-end testing.

## Verified repository and CI

- Repository: `amirmohd4/Aether`.
- Candidate PR: [#20](https://github.com/amirmohd4/Aether/pull/20), open, draft, unmerged.
- Candidate head: `552ca35e48db859b178e61eb5c1c9ea44b7a1e53`.
- Base `main` head at PR creation: `f64148aad10a5f8f586efde0cefe7a817fe6d996`.
- Frontend CI passed: dependency install, TypeScript check and Vite build.
- Combined MVP CI passed: backend tests and frontend checks/build.
- MVP test workflow passed: Python compilation and backend pytest suite.
- The staging workflow did **not** run its staging-smoke job. The `staging-not-configured` notice job succeeded while `staging-smoke` was skipped. This is not a staging pass.
- Netlify deploy preview for PR #20 is marked ready at [deploy-preview-20](https://deploy-preview-20--aether-govos.netlify.app/), built from the candidate commit. A ready static deployment is not proof of successful API, auth, upload, or workflow journeys.
- Netlify feedback form `aether-feedback` is present with zero recorded submissions. Form submission and feedback processing have not been verified.

## Supabase — previously verified configuration

The existing project is `aether`, ref `lekudqjewxxunqjuqayi`, on the Free plan. The most recent recorded inspection found:
- Project status `ACTIVE_HEALTHY`.
- Ten applied migrations; 13 public application tables and ten `aether_internal` execution tables.
- RLS enabled on all 23 application tables.
- Dedicated non-superuser login role `aether_runtime`.
- Browser roles blocked from internal execution tables; runtime role has the required internal grants.
- Private `aether-documents` storage bucket.
- No Supabase Security or Health Advisor lints.
- 39 informational unused-index findings; no indexes were removed without workload evidence.

These database-administration checks do not prove that a deployed Render process authenticates as `aether_runtime`. The candidate's `/ready` check must pass against the deployed runtime.

## Render — current deployment boundary

Two existing Free services were inspected:
- `aether-backend` deploys from `main`; its service configuration was last updated 2026-10-15. It is not deployed from PR #20.
- `aether-public-demo` deploys from `launch/public-research-preview`; its service configuration was last updated 2026-10-29. It is not deployed from PR #20.

Recent application logs from `aether-public-demo` show embedded worker ticks every five seconds, with zero items processed and zero notifications delivered/failed in the sampled entries. This proves the worker loop is emitting ticks on that service; it does not prove candidate worker correctness, successful work execution, retries, recovery, or notification delivery.

Render service metadata does not expose environment-variable values. The deployed database URL/password, runtime role, Supabase service credentials, encryption key, auth mode and CORS configuration therefore remain unverified. The candidate backend has not been deployed to an isolated staging service.

Do not repoint either existing service to the candidate as a shortcut: the current services are not an isolated staging environment, and sharing the existing database would create an unsafe test boundary.

## Staging smoke automation

Workflow: `.github/workflows/aether-staging-smoke.yml`.

Required GitHub repository variables:
- `AETHER_STAGING_API_URL`
- `AETHER_STAGING_FRONTEND_URL`

Required GitHub Actions secret:
- `AETHER_STAGING_API_KEY` — a read-only Aether API key with the required `cases:read` scope.

The workflow verifies API `/health`, `/ready` (including `database_role_valid=true`), root API response, frontend response and authenticated product/release smoke checks. The latest candidate run skipped the actual staging job because the staging URLs are not configured. Do not describe that run as a passing smoke test.

## Go/no-go checklist

- [x] Candidate branch and PR #20 established; kept draft and unmerged.
- [x] Candidate backend tests, frontend typecheck/build and combined CI passed.
- [x] Netlify PR preview deployment reached `ready` for the candidate commit.
- [x] Existing Supabase Free project, schema, RLS, runtime role and private bucket previously inspected.
- [x] Public-demo service logs show embedded worker ticks; no work execution was demonstrated by the sampled logs.
- [ ] Set the `aether_runtime` password in Supabase and matching Render secret; verify candidate `/ready` returns HTTP 200 with `database_role_valid=true`.
- [ ] Deploy the candidate to an isolated staging API and matching frontend without replacing the existing services or sharing a production database.
- [ ] Configure staging URL variables and read-only API-key secret; run the actual staging-smoke job to completion.
- [ ] Verify Supabase Auth, private document upload/read, encryption and tenant isolation against staging.
- [ ] Exercise worker dispatch with synthetic work; verify processing, durable recovery, retries and notification outbox behavior.
- [ ] Complete synthetic citizen/business and officer/operator journeys against the deployed candidate.
- [ ] Verify preview-to-API CORS, security headers, rate limits, privacy disclosures, accessibility and feedback submission.
- [ ] Demonstrate rollback to a known-good backend/frontend pair.
- [ ] Only after all applicable gates pass, review PR #20 for merge to `main`.

## Release policy

Do not merge PR #20, promote the candidate to production, or enable live government connectors solely because CI or the Netlify build passes. Preserve the synthetic-only boundary and disclose Free-tier availability limits. Treat each government integration as a separate authorized, tested and reconciled release.
