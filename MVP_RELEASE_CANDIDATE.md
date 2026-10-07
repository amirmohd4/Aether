# Aether GovOS — Controlled MVP Release Candidate

## Verdict

The repository is a release candidate for a controlled/sandbox Aether GovOS MVP. The software path from real-world objective to executable, auditable government workflow is implemented across the shared 34-service catalog.

This is not a declaration of live government authority.

## Included in this release candidate

- Objective understanding with ranked candidates and clarification stop
- Requirement discovery with source provenance and an explicit authority-status distinction
- 34-service shared registry with customer eligibility and reusable process graphs
- Government ontology and dependency-aware work graph
- Parallel task execution with stable idempotency keys and bounded retries
- Durable task queue, task checkpoints and restart recovery
- Durable case leases for worker coordination
- Evidence verification, reconciliation, exception/risk handling and critical-path state
- Explicit human/statutory and physical-action boundaries
- Server-controlled tenant membership, RBAC and jurisdiction/department filtering
- Tenant-scoped developer API keys with scopes, expiry and revocation
- Private server-side document storage with SHA-256 integrity verification
- Native text/PDF extraction plus external OCR adapter
- Encrypted extracted document text when AETHER_ENCRYPTION_KEY is configured
- Notification outbox with idempotency, dispatch leases and bounded retries
- Idempotent payment ledger with replaceable external provider adapter
- Usage metering and operator analytics
- Sandbox developer marketplace catalog
- Unified Command Center with guided intake, actual file upload, payment, notification and authority surfaces
- Durable worker process for Render
- Production fail-closed controls and release-readiness endpoint
- Supabase RLS/legacy-browser lockdown migrations
- Backend/frontend CI and release smoke test

## Controlled MVP operating mode

Use:

    AETHER_ENV=staging
    AETHER_AUTH_MODE=supabase
    AETHER_ENABLE_LEGACY_API=false
    AETHER_ENABLE_PRODUCTION_CONNECTORS=false

This intentionally keeps the government environment synthetic.

## Production blockers

Production cannot be honestly declared complete until the environment has external dependencies that the repository cannot fabricate:

1. Authorized live government connector credentials, contracts and certification
2. Authoritative, effective-dated rule packs for each exposed jurisdiction/service
3. Certified statutory signature/certificate/issuance integrations where required
4. Production OCR, notification and payment provider contracts/credentials
5. Final Supabase RLS/security-advisor verification in the deployed project
6. Final Render and Netlify smoke tests plus rollback validation

## Release discipline

Development remains on aether-mvp-build. The release branch is main.

Do not enable live connectors or bypass the production fail-closed checks just to make a demo appear production-ready.