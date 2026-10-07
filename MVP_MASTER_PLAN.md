# Aether — Master MVP Build Plan

## Product target

Aether is a Government Operating System / execution layer. The MVP must support one shared execution backbone for citizens, businesses, banks/NBFCs, developers/real-estate, insurers, enterprises, and government officers.

Core promise:

Objective → understand → discover requirements → create case → build government work graph → execute independent work in parallel → verify/reconcile → handle exceptions → request authorised human action only where required → resume → final outcome → evidence/audit.

## Release rule

Development work stays on `aether-mvp-build`. `main` is the release branch.

The controlled MVP release is now on `main`, with the Supabase schema hardened and the Netlify frontend published from the release commit.

## Current status — CTO estimate

Overall whole-MVP software completion: **~90% for the controlled MVP / sandbox release**.

This is a directional engineering estimate, not a project-management measurement.

The software backbone is release-candidate complete for controlled/sandbox operation: objective understanding, requirements, 34-service catalog, cross-department graphs, dependency-aware parallel execution, durable queue/checkpoints/leases, evidence and document vault, OCR adapter, audit, RBAC, API keys, payments, notifications, analytics, marketplace, worker runtime and the unified Command Center are implemented.

## Deployed release status

- GitHub release commit: `25db222db97f153fad5731bd51dc2dc168d8fcdf` plus subsequent release-configuration commits.
- GitHub backend/frontend automated checks on the release line have passed.
- Supabase project is active and hardened; required Aether migrations are applied.
- Netlify site `aether-govos` is published from the current release commit.
- Render web service has a known-good live deployment, while the latest release deployment is currently waiting in Render's deployment queue. Do not treat the queued deployment as validated until it starts and becomes healthy.
- The Render blueprint now declares `/health` as the health check and includes the Supabase pooler host override for both the web and worker definitions.
- A separate Render worker is defined in `render.yaml`, but the connected Render workspace currently exposes only the web service. Worker provisioning/live execution is therefore the remaining infrastructure validation item.

## Strongly built

- Shared case/execution domain
- 34-service shared registry
- Requirements gate and source provenance
- Government Ontology model
- Work Graph model
- Dependency-aware execution and parallel digital tasks
- Human/statutory and physical-action boundaries
- Retry policy, stable task idempotency and queue semantics
- Execution event ledger
- Durable PostgreSQL/SQLite persistence
- Synthetic Government Environment
- Evidence verification and reconciliation
- Durable case listing, resume and incremental document submission
- Private tenant usage metering
- Authorized HTTP connector contract
- Server-controlled membership/RBAC boundary with department/jurisdiction scoping
- Tamper-evident audit hash chain and integrity verification
- Document upload, hashing, private storage, extraction, encryption and OCR adapter
- Notification outbox and idempotency
- Payment ledger and provider adapters
- Operator analytics and 34-service marketplace
- Standalone worker runtime with durable case leases
- Unified Aether Command Center
- CI definitions for backend tests and frontend build/typecheck
- Supabase RLS/security hardening for the controlled MVP

## Partially built

- Broad service catalog: all 34 identities share the execution backbone, but domain-specific legal graphs are deeper for selected MVP verticals.
- Government rules: provenance/version readiness exists, but production-authoritative effective-dated rule coverage is not complete across every jurisdiction/service.
- Connector framework: synthetic execution and an authorized REST adapter exist; live government connector certification/access remains external.
- Document intelligence: production OCR/vision provider configuration remains external.
- Persistence: durable recovery exists; full event-sourced replay is future scale hardening.
- Notifications/payments: provider contracts and credentials remain external.
- Frontend: unified Command Center is the primary MVP surface; older service-specific screens remain for compatibility.

## Remaining MVP release-validation work

1. Get the latest Render deployment out of the current queue and verify the web service becomes healthy.
2. Validate live worker execution against Supabase using the exact configured connection details.
3. Run the final deployed smoke test across the Netlify frontend and Render API.
4. Verify role/tenant/department/jurisdiction boundaries against the deployed stack.

## Production / scale extensions

These are not being manufactured as completed MVP features:
1. Authorized live government connectors and endpoint certifications
2. Authoritative versioned effective-dated rule packs for production jurisdictions
3. Certified statutory signatures, certificates and issuance integrations
4. Production OCR/vision provider contracts and credentials
5. Production notification delivery and payment processor credentials
6. Distributed event-sourced replay and large-scale worker orchestration
7. Full production load/chaos testing
8. Retirement of legacy modules after dependency proof

## Legacy-code policy

Do not delete legacy modules merely because a V2 equivalent exists.

A legacy file is deleted only when:
- no production route imports it,
- no V2 path depends on it,
- its data model has a V2 replacement,
- its behavior is covered by tests,
- and the replacement is confirmed in the unified MVP flow.

## Final release gate

Before declaring the controlled MVP fully deployed:
- application boots cleanly in the release container;
- complete automated test suite passes;
- core customer journeys pass end-to-end;
- persistence/restart recovery passes;
- connector idempotency passes;
- Supabase migrations and RLS/security posture are verified;
- Render deployment succeeds and health check passes;
- worker execution succeeds;
- Netlify deployment matches the release commit;
- deployed smoke-test APIs and UI pass;
- rollback path remains available.
