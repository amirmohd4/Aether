# Aether GovOS MVP Release Checklist

Last verified: 2026-11-13. This checklist records current evidence, not historical assertions. A checked item must have reproducible evidence from the current release candidate or deployed target.

## Product scope — implemented in the development branch

- [x] Objective understanding with ranked service candidates and clarification stops.
- [x] Requirements discovery with provenance and authority-status distinction.
- [x] Shared 34-service registry and reusable process graphs.
- [x] Dependency-aware work graphs and parallel task execution.
- [x] Deterministic synthetic government environment.
- [x] Evidence verification, reconciliation, exception/risk handling and critical-path state.
- [x] Explicit human/statutory and physical-action boundaries.
- [x] Server-controlled tenant membership, RBAC and jurisdiction/department filtering.
- [x] Tenant-scoped API keys, scopes, expiry and revocation.
- [x] Private server-side document storage adapter, SHA-256 integrity and extraction.
- [x] Encrypted extracted document text when configured.
- [x] Durable queue, checkpoints, leases, retries and notification outbox.
- [x] Idempotent payment ledger and replaceable provider adapter.
- [x] Usage metering and operator analytics.
- [x] Sandbox developer marketplace.
- [x] Unified Command Center with guided intake, uploads, payments, notifications and officer authority queue.
- [x] India administrative intelligence: discovery taxonomy, illustrative cross-department journeys, authenticated APIs and frontend explorer.
- [x] Backend/frontend CI and release-readiness endpoint.

## Code validation

- [x] Backend compile and complete pytest suite passed on code commit `d0f9c4502f811bfd16cd122216ee8b60fae0f9d8`.
- [x] Frontend TypeScript check and production build passed on that code commit.
- [x] Combined backend/frontend CI passed on that code commit.
- [x] Administrative action worker workflow passed on that code commit.
- [x] Subsequent release-readiness documentation commit changes no application source; core CI passed on the application-code head.

## Supabase — verified

- [x] Existing project restored to ACTIVE_HEALTHY.
- [x] Organization remains on Free plan; no replacement project or upgrade was created.
- [x] Ten migrations recorded as applied.
- [x] Thirteen public application tables and ten internal execution tables present.
- [x] RLS enabled on all 23 application tables.
- [x] Dedicated non-superuser `aether_runtime` role exists.
- [x] Browser roles have no access to internal execution tables; runtime role has required access.
- [x] `aether-documents` storage bucket exists and is private.
- [x] Supabase Security and Health Advisors returned no lints.
- [ ] Deployed Render backend successfully connects using its configured runtime database identity.
- [ ] Deployed backend completes Supabase Auth and private document upload/read tests.

## Render and worker — outstanding

- [ ] Approved release candidate is deployed to an isolated staging API.
- [ ] Staging `/health` returns HTTP 200.
- [ ] Staging `/ready` returns HTTP 200 and confirms database readiness.
- [ ] Authenticated `/api/aether/v2/release/readiness` approves controlled MVP.
- [ ] Backend environment variables are verified without exposing secret values.
- [ ] Embedded worker is proven to process durable work and notification outbox, or asynchronous work is disabled and disclosed.
- [ ] Worker retry/recovery behavior is verified against the restored Supabase database.
- [ ] No paid Render resource is created without explicit cost approval.

## Frontend — outstanding

- [ ] Staging frontend is deployed from the same release candidate.
- [ ] `VITE_API_URL` points to the matching staging API.
- [ ] `VITE_REQUIRE_AUTH=true` and Supabase Auth login/signup work.
- [ ] Tenant selection, session persistence and sign-out work.
- [ ] No service-role key, database password or other server secret appears in browser assets.
- [ ] SPA fallback and all core Command Center surfaces work in the deployed browser.

## End-to-end and security — outstanding

- [ ] Citizen/business objective-to-case workflow completes in synthetic mode.
- [ ] Department/operator work queues, human approvals and exceptions work.
- [ ] Evidence upload, retrieval, hash integrity and encryption are verified.
- [ ] Tenant isolation, cross-tenant denial, role and jurisdiction checks pass in staging.
- [ ] Queue idempotency, bounded retries, lease expiry and restart recovery pass.
- [ ] Audit trail and outcome reconciliation are verified.
- [ ] CORS, rate limits, security headers, error handling and monitoring are checked.
- [ ] Rollback to a known-good backend and frontend deployment is demonstrated.
- [ ] Privacy notice, terms, accessibility, incident response and support ownership are ready.

## Release automation

- [x] Authenticated release smoke script checks health, readiness, service catalog, marketplace, connectors, rules and controlled-MVP readiness.
- [x] Authenticated smoke coverage includes India administrative-intelligence overview, departments and journeys.
- [x] Staging smoke workflow supports release-branch pushes, GitHub URL variables and manual URL inputs.
- [ ] Configure GitHub variables `AETHER_STAGING_API_URL` and `AETHER_STAGING_FRONTEND_URL`.
- [ ] Configure GitHub secret `AETHER_STAGING_API_KEY` for authenticated staging smoke.
- [ ] Run the actual staging-smoke job; latest workflow run skipped it because staging URLs are not configured.

## Legal and government integration boundary

- [x] Controlled MVP defaults to synthetic government systems.
- [x] Product responses distinguish internal execution from official government outcomes.
- [ ] Each live connector has written authorization, approved credentials/endpoints and sandbox certification.
- [ ] Each exposed production service has authoritative, effective-dated rules and jurisdiction-specific prerequisites.
- [ ] Statutory signature, certificate and issuance integrations are certified where legally required.
- [ ] Government system-of-record reconciliation is proven for every activated connector.

## Release decision

**Current status: NOT READY FOR PUBLIC LAUNCH.**

The product scope and development code are implemented, and Supabase has been restored and checked. The next release milestone is a controlled synthetic beta, not live government production. Do not merge PR #11 into `main` until the Render, frontend, end-to-end, security and rollback items above have evidence. Never bypass the legal/authority gates to make a demo appear live.
