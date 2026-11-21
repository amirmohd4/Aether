# Aether GovOS MVP Release Checklist

Last verified: 2026-11-21. This checklist records current evidence, not historical assertions. A checked item must have reproducible evidence from the current release candidate or deployed target.

## Product scope — implemented in the development candidate

- [x] Objective understanding with ranked service candidates and clarification stops.
- [x] Requirements discovery with provenance and authority-status distinction.
- [x] Shared national service catalogue; 61 core service-family definitions plus extended India-wide taxonomy and reusable process graphs.
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
- [x] India administrative intelligence taxonomy and illustrative cross-department journeys.
- [x] Backend/frontend CI and release-readiness endpoint.

These are implemented capabilities. They are not proof that every deployed user journey or external provider integration is production-ready.

## Code and CI — verified

- [x] Backend test suite passed on the promoted candidate.
- [x] Frontend typecheck and production build passed on the promoted candidate.
- [x] Aether MVP CI and backend tests passed on candidate commit `1de9e95386684043a933f73e18e4c6104f74a506` (158 backend tests), including tenant-admin cross-tenant denial and tenant-scoped admin listing.
- [x] Aether MVP Tests passed on that candidate.
- [x] Aether MVP Frontend passed on that candidate; the later authenticated-preview configuration commit also passed frontend lint/build.
- [x] Aether Staging Release Smoke completed successfully on PR #11 merge ref `41cde4f43f4dfe3ef7a85d16c2363840a39034e2`.
- [x] Staging smoke observed HTTP 200 for health, readiness and root; readiness asserted database role validity.
- [x] Authenticated staging smoke passed service catalog, marketplace, connector catalog, rule readiness, India admin overview, department catalog, journey templates and release-readiness checks.
- [x] Netlify deploy preview #11 reached `ready` for candidate commit `1de9e95386684043a933f73e18e4c6104f74a506`.

**Scope limitation:** the staging smoke uses a read-only API key and performs read/readiness checks. It does not create a case, upload/read a document, perform an officer decision, or prove a full citizen-to-officer journey. The candidate preview configuration now points to authenticated `aether-staging` and sets `VITE_REQUIRE_AUTH=true`; the staging CORS allowlist was updated to include preview #11 and redeployed successfully. This configuration has not yet been exercised in a real browser, and staging still runs the older integration branch rather than the candidate backend.

## Supabase — verified at database level

- [x] Existing project `aether` (`lekudqjewxxunqjuqayi`) reports `ACTIVE_HEALTHY`.
- [x] Twelve migrations are recorded as applied, including admin action queue and document bucket limit migrations.
- [x] Thirteen public application tables and twelve internal execution tables are present.
- [x] RLS is enabled on all 25 application tables; the two admin queue tables grant access only to `aether_runtime` and deny browser-role SELECT.
- [x] Dedicated `aether_runtime` role exists and is non-superuser, cannot create roles or databases, and can log in.
- [x] `aether-documents` bucket exists and is private.
- [x] Bucket-level upload restrictions set to 15 MiB and the application's approved MIME allowlist.
- [x] Admin action/work-item schema migration applied with RLS and least-privilege runtime grants.
- [x] Candidate readiness endpoint checks both admin queue tables and server-enforced storage limits.
- [x] Supabase Security and Health Advisors returned no lints.

- [ ] Prove the deployed staging process can upload, retrieve and delete a test document through its configured server-side credentials.
- [ ] Verify encryption-at-rest behavior for extracted document text with the deployed encryption key.
- [ ] Verify tenant-scoped document access and cross-tenant denial end-to-end.

Database-level configuration does not by itself prove the deployed application's storage credentials or user authorization behavior.

## Render, runtime and availability

- [x] A separate `aether-staging` Render service exists and is active.
- [x] Staging service now runs reconciled candidate commit `a07df14e03cf4d38c1c169400ea699accd49ebe8` from `integration-check/public-preview-into-hardened` after PR #28 merged.
- [x] Post-deploy staging release smoke passed `/health`, `/ready`, root and eight authenticated read-only product/release checks; `/ready` asserted `database_role_valid=true` and release readiness asserted `ready_for_controlled_mvp=true` with no controlled blockers.
- [ ] Confirm deployed environment-variable names/configuration without exposing values; verify encryption, Supabase Auth, storage and worker settings.
- [ ] Prove worker dispatch processes a synthetic durable task, not merely that the polling loop emits ticks.
- [ ] Prove retries, lease expiry, restart recovery and notification outbox delivery.
- [ ] Demonstrate a rollback to a known-good backend/frontend pair.
- [ ] Decide whether Free-tier cold starts and service suspension are acceptable for the pilot; disclose the availability limitation or approve a paid plan explicitly.
- [ ] Run a bounded load and failure test before expanding the pilot.

The current staging service is not the production backend. PR #11 remains unmerged and PR #20 was closed as superseded by PR #11. Production Render service `aether-backend` still deploys from `main` at the older commit `f64148aad10a5f8f586efde0cefe7a817fe6d996`. Do not repoint it as a shortcut.

## Frontend and browser acceptance — outstanding

- [x] Candidate Netlify preview #11 is deployed and marked ready.
- [ ] Test preview #11 in a real browser on desktop and mobile.
- [ ] Verify signup/login, session persistence, tenant selection and sign-out with a dedicated pilot account.
- [ ] Verify every primary navigation route, CTA, form validation, upload progress and error state.
- [ ] Verify candidate frontend calls the intended staging API; current smoke only checked a different preview's HTML response.
- [ ] Inspect built browser assets and network requests to confirm no server secret is exposed. Public Supabase publishable/anon keys are expected; service-role keys, DB passwords and encryption keys are prohibited.
- [ ] Complete keyboard, screen-reader, contrast and responsive accessibility checks.
- [ ] Verify feedback form submission and support contact path.

## End-to-end product and security — outstanding

- [ ] Citizen/business objective-to-case workflow completes against the deployed candidate in synthetic mode.
- [ ] Missing-evidence flow, document upload, final-document resume and task graph are verified against deployed storage.
- [ ] Officer/operator queue, human approval/rejection, exceptions and notifications complete end-to-end.
- [ ] Audit chain verifies after a complete deployed case.
- [x] Candidate unit tests deny cross-tenant tenant-admin case access, limit admin case listing to the active tenant and fail closed on missing officer department/jurisdiction scope.
- [ ] Deployed tenant isolation, cross-tenant denial, role, department and jurisdiction boundaries pass adversarial staging tests.
- [ ] API-key scope denial, expiry and revocation are tested against the deployed service.
- [ ] File size, MIME, signature, malformed-file and upload abuse limits are tested.
- [ ] CORS, rate limits, security headers, error handling and monitoring are checked on the actual candidate frontend/backend pair.
- [ ] Backup and restore are tested; incident ownership and escalation are assigned.

## Legal, privacy and government authority boundary

- [x] Controlled MVP defaults to synthetic government systems.
- [x] Product responses distinguish internal execution from official government outcomes.
- [x] Live government connectors remain disabled by default.
- [ ] Publish and review accurate privacy notice, terms, retention/deletion policy and pilot consent.
- [ ] Confirm the operating legal entity, data-controller/processor roles, support contact and incident contact.
- [ ] Complete a data-flow and personal-data minimization review before accepting real citizen documents.
- [ ] Confirm applicable Indian privacy, cybersecurity, accessibility, records-retention and procurement obligations with qualified counsel and the pilot institution.
- [ ] Obtain written authorization for every live government connector and approved endpoint/credential.
- [ ] Validate authoritative, effective-dated rules for every service and launch jurisdiction.
- [ ] Obtain required certification for statutory signature, certificate and issuance integrations.
- [ ] Prove system-of-record reconciliation for every activated connector.

A synthetic pilot is not an official government service and must not imply statutory approval, certificate issuance, government affiliation or access to government records.

## Pilot and release decision

- [ ] Name a pilot owner and operational support owner.
- [ ] Select one administrative workflow, one jurisdiction and a small set of invited users.
- [ ] Use synthetic or explicitly consented test data only until privacy/legal controls are approved.
- [ ] Define success metrics: completion rate, time to complete, missing-evidence rate, manual intervention rate, error rate and user-reported issues.
- [ ] Run a supervised pilot and close all critical/high-severity findings.
- [ ] Obtain explicit pilot institution approval before real operational data is processed.
- [ ] Review PR #11 and production deployment plan only after the above controlled-pilot gates pass.

**Current decision: NO-GO for public production launch. CONDITIONAL GO for a tightly controlled synthetic pilot after browser acceptance, deployed write-path tests, operational ownership and privacy/terms are completed.**

Do not merge PR #11 into `main` or claim live government execution on the strength of CI and read-only smoke checks alone. Keep live connectors disabled.