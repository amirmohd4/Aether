# Aether Release Readiness

Last checked: 2026-11-13 (live connector verification during release review)

## Current decision

**NO-GO — NOT READY for public launch or production government deployment.** The software repository contains a substantial sandbox MVP and the India administrative-intelligence increment. The exact integrated development commit passed the three recorded GitHub Actions workflows. However, the Supabase restore is still starting and the database is not yet accessible; the Render services are deployed from older branches/commits; and end-to-end staging, security, worker and rollback evidence is outstanding.

Aether must be described as a synthetic/sandbox workflow platform unless and until a specific government connector is authorized, source-backed, tested and reconciled against the authority's system of record. Internal task completion is not an official government outcome.

## Verified repository state

- Repository: `amirmohd4/Aether`.
- Development branch: `aether-mvp-build`.
- Integrated release-candidate commit at review start: `8ca80a57534fcac1aba7741f86bd00c86c3cee04`.
- Pull request #11 targets `main`, remains open and unmerged. Do not merge until the deployment and release gates below pass.
- The India administrative-intelligence increment is integrated into the development branch. It includes an India-wide discovery taxonomy, three illustrative cross-department journey templates, authenticated read APIs, and a frontend explorer.
- At the exact integrated commit above, the following GitHub Actions workflows completed successfully: Aether MVP Tests, Aether MVP CI (backend and frontend), and Aether MVP Frontend.
- The README describes the controlled MVP as a deterministic synthetic government environment. It does not issue official government decisions/documents.

## Live environment findings

1. **Supabase — RESTORE IN PROGRESS / DATABASE BLOCKER.**
   - Existing project `aether`, ref `lekudqjewxxunqjuqayi`, organization `zylrieqcwisauplfxmjh`.
   - Organization API confirms plan `free` / `tier_free`.
   - Restore action returned success. Subsequent project status is `COMING_UP`, not `ACTIVE_HEALTHY`.
   - Database table listing returned "Database is possibly not accessible at the moment". Migration listing returned an empty list; because the database is still starting, this is not sufficient evidence that the schema is empty or healthy.
   - Security/performance/health advisor calls returned no lints, but they are not a substitute for a successful database connection and schema/RLS verification.
   - No new project or plan upgrade was performed. Keep the existing project on Free; stop if any paid upgrade or charge is required.

2. **Render — deployment branch mismatch.**
   - `aether-backend` is on the Free plan, deploys from `main`, and its latest recorded live deployment is commit `f64148aad10a5f8f586efde0cefe7a817fe6d996` from 2026-10-15. It is not running the current development release candidate.
   - `aether-public-demo` is on the Free plan, deploys from `launch/public-research-preview`, and its latest recorded live deployment is commit `eb148e6dc6866ea0a5214b01d9f908a89d94a264` from 2026-10-29.
   - The public demo service has no configured Render health-check path. The backend has `/health`.
   - Render returned no application logs in the previously checked 24-hour window. Deployment status alone does not prove end-to-end application health.
   - Direct public endpoint verification was not available during this review.

3. **Worker deployment gap.**
   - The repository's `render.yaml` declares both a web service and a separate `aether-worker` service.
   - The connected Render workspace currently lists only `aether-backend` and `aether-public-demo`; no separate `aether-worker` service is present.
   - The backend blueprint also has an embedded worker configuration. The actual deployed environment and whether a worker is running must be verified before relying on scheduled/queued execution. Do not create a new paid service; any Free-plan-compatible architecture must be validated first.

4. **Frontend and secrets.**
   - The README requires the frontend to use the intended API URL and auth mode, with server secrets kept out of frontend assets.
   - Render service configuration and deployment branch do not establish that the frontend is deployed from the same release commit or configured correctly. Inspect environment-variable names/values securely and verify the deployed frontend/backend pairing before launch. Never print or commit secret values.

5. **Live government integrations.**
   - No connector may be treated as authorized without written authority, approved endpoint/credentials, authoritative effective-dated rules, sandbox certification and reconciliation against the government's system of record.
   - The department taxonomy and journey templates are discovery/planning aids, not exhaustive or universal statutory checklists.

## Go/no-go gates

- [ ] Supabase reports active/healthy; database connectivity succeeds.
- [ ] Existing schema, migration history, auth configuration, RLS policies, storage bucket/access policies and backup/recovery are verified. Do not infer these from stale documentation.
- [ ] Render backend is deployed from an approved release commit; health and readiness endpoints pass.
- [ ] Frontend is deployed from the same release candidate and configured to the intended backend/auth mode; no server secrets are present in browser assets.
- [ ] Worker execution is verified, or asynchronous execution is disabled and disclosed. Avoid creating a paid service.
- [ ] Latest backend tests, combined CI, frontend lint and frontend build pass on the exact release commit.
- [ ] Tenant isolation, authentication, authorization, document encryption, retention/deletion and audit controls are tested in staging.
- [ ] End-to-end staging scenarios cover intake, evidence, tenant isolation, queue/retry recovery, human approval, audit trail, exception handling and outcome reconciliation.
- [ ] Rate limits, CORS, security headers, error handling and operational monitoring are checked against deployed configuration.
- [ ] Rollback procedure and a known-good deployment are verified.
- [ ] Privacy notice, terms, accessibility, incident response and support ownership are ready.
- [ ] Every live government service independently passes legal authorization, source verification, connector certification and system-of-record reconciliation.

## Release policy

Do not merge to `main`, deploy publicly or announce production readiness merely because CI passes. First resolve the Supabase startup/database dependency, align the deployment branch, verify staging end to end, and confirm rollback. A controlled synthetic demo may be shared only if its environment is isolated, its runtime is verified, and it is clearly labelled synthetic. Never present it as an official government workflow or outcome.
