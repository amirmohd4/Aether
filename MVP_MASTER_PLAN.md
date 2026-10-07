# Aether — Master MVP Build Plan

## Product target

Aether is a Government Operating System / execution layer. The MVP must support one shared execution backbone for citizens, businesses, banks/NBFCs, developers/real-estate, insurers, enterprises, and government officers.

Core promise:

Objective → understand → discover requirements → create case → build government work graph → execute independent work in parallel → verify/reconcile → handle exceptions → request authorised human action only where required → resume → final outcome → evidence/audit.

## Release rule

Do not deploy production changes during MVP construction.

Development branch: `aether-mvp-build`

`main` is treated as the release branch. The final MVP is merged to `main` only after the release checklist is green. That merge is the coordinated trigger for Render and the connected Netlify flow. Supabase schema/migrations are applied only as part of the final release process.

## Current status — CTO estimate

Overall whole-MVP software completion: **~85% for the controlled MVP / sandbox release**.

This remains a directional engineering estimate, not a project-management measurement. The software is now release-candidate complete for controlled/sandbox operation: objective understanding, requirements, 34-service catalog, cross-department graphs, parallel execution, durable queue/checkpoints/case leases, evidence and document vault, OCR adapter, audit, RBAC, API keys, payments, notifications, analytics, marketplace, worker runtime and unified Command Center are implemented.

This is a directional engineering estimate, not a measured project-management percentage.

### Strongly built
- Shared case/execution domain
- Service Registry with 32+ service identities
- Requirements gate
- Source provenance fields for verified rules
- Government Ontology model
- Work Graph model
- Dependency-aware execution
- Parallel digital task execution
- Human/physical authority boundaries
- Retry policy
- Stable task idempotency keys
- Execution event ledger
- Durable case/event repository design
- Supabase private persistence schema
- Synthetic Government Environment
- Restaurant and commercial-project execution templates
- Existing broad frontend/service surfaces from the earlier product
- Existing backend service-specific models/connectors that can be reused while migrating
- Objective understanding with ranked candidates and ambiguity stop
- Reusable process graphs across the MVP service catalog
- Explicit connector operation metadata on executable tasks
- Evidence-aware reconciliation and decision-package workers
- Durable case listing, resume, and incremental document submission
- Private tenant usage metering with idempotent case/outcome events
- Opt-in authorized HTTP connector contract for production integrations
- Server-controlled membership/RBAC boundary with department/jurisdiction scoping
- Tamper-evident audit hash chain and integrity verification endpoint
- CI definitions for backend tests and frontend typecheck/build
- Legacy browser-data lockdown migration with deny-by-default RLS

### Partially built
- Broad service catalog → all 34 identities have a shared executable baseline; domain-specific legal graphs remain limited to the MVP verticals
- Government rules → provenance/version readiness exists for a narrow verified slice, not broad jurisdiction/service coverage
- Connector framework → synthetic execution plus an opt-in authorized REST adapter exist; live government connector certification/access remains external work
- Document intelligence → server-side file upload, hashing, private storage, native text/PDF extraction, encrypted extracted text and an external OCR adapter exist; production OCR/vision provider configuration remains external
- Persistence → durable cases, queues, checkpoints, case leases, events and recovery exist; fully event-sourced replay remains future hardening
- Notifications/payments → durable idempotent ledgers, notification outbox and provider adapters exist; external delivery/payment credentials are not bundled
- Frontend → unified Command Center, guided intake, document upload, payments, notifications, marketplace visibility, role-aware authority queue and recent-case recovery exist; legacy service screens remain for compatibility

### Controlled-MVP completion state

The remaining blockers are external production prerequisites: authorized live government connectivity, authoritative effective-dated rules, certified statutory signature/issuance integrations, and final deployed environment/security validation. Those cannot be truthfully manufactured in code.

### Production / scale extensions (not missing controlled-MVP software)

1. Authorized live government connectors and endpoint certifications — external dependency
2. Authoritative, versioned, effective-dated rule packs for each production jurisdiction/service — external/legal-data dependency
3. Certified statutory signatures, certificates and issuance integrations — external authority dependency
4. Production OCR/vision provider credentials and service-level integration — external provider dependency
5. Production notification delivery providers and credentials — external provider dependency
6. Production payment processor contracts/credentials — external provider dependency
7. Deployed Supabase RLS/security-advisor verification — deployment gate
8. Distributed event-sourced replay and large-scale worker orchestration — scale hardening
9. Full production load/chaos testing — release validation
10. Retirement of legacy modules after dependency proof — cleanup/maintenance

The controlled MVP intentionally keeps synthetic government connectors and non-authoritative baseline service metadata behind explicit boundaries. These are not silently promoted to legal/production authority.

## Legacy-code policy

Do **not** delete legacy modules merely because a V2 equivalent exists.

A legacy file is deleted only when:
- no production route imports it,
- no V2 path depends on it,
- its data model has a V2 replacement,
- its behavior is covered by tests,
- and the replacement is confirmed in the unified MVP flow.

Obvious generated/cache artifacts can be removed during cleanup after dependency review.

## Current legacy areas observed

The repository still contains:
- `backend/models/*` service-specific models
- `backend/services/*` older service/business logic
- `backend/connectors/*` older connector implementations
- `backend/govstack/*` earlier government-stack modules
- `src/components/*` many service-specific frontend surfaces
- multiple deployment/configuration documents and historical artifacts

These are **not yet fully removed** because existing routes still reference parts of them.

## Remaining blockers before production declaration (external)
1. Connect at least one real government integration per intended launch journey using authorized credentials and sandbox/certification access.
2. Populate authoritative, versioned, effective-dated rules for every service/jurisdiction being exposed; do not treat baseline metadata as law.
3. Configure production OCR/document storage, notification and payment providers.
4. Run the full Supabase RLS/security review against the deployed database and verify no browser role can reach private execution tables.
5. Run the release smoke test against the final Render URL and final Netlify site.
6. Retire or explicitly quarantine remaining legacy APIs/modules after dependency review.

## Final release gate

Before merging MVP to `main`:
- application boots cleanly in the release container
- complete automated test suite passes
- core customer journeys pass end-to-end
- persistence/restart recovery passes
- connector idempotency passes
- security review/RLS plan is resolved
- production secrets/configuration verified
- Supabase migrations verified
- Render deployment succeeds and health check passes
- Netlify deployment succeeds and published build matches release commit
- smoke-test APIs and UI
- only then declare MVP deployed
