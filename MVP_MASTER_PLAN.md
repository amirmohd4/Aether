# Aether — Master MVP Build Plan

## Product target

Aether is a Government Operating System / execution layer. The controlled MVP supports one shared execution backbone for citizens, businesses, banks/NBFCs, developers/real-estate, insurers, enterprises and government officers.

Core promise:

Objective → understand → discover requirements → create case → build government work graph → execute independent digital work in parallel → verify/reconcile → handle exceptions → request authorised human action only where required → resume → outcome → evidence/audit.

## Controlled-MVP status

**Core software scope: IMPLEMENTED. Controlled-beta launch gate: NOT YET VERIFIED.**

The repository contains the planned controlled-MVP software capabilities and a passing development-branch CI baseline. However, a successful code build is not proof that the current release candidate is deployed or operating end to end. As of 2026-11-13, the existing Supabase Free project has been restored and its schema/RLS/private bucket are verified, but Render still deploys older commits from separate branches. Deployed environment configuration, live readiness, staging E2E, worker execution and rollback are not yet verified.

This is a software-scope status for synthetic/sandbox workflows, not a public-launch approval or a claim of live government authority. The current go/no-go decision is maintained in `docs/RELEASE_READINESS.md`.

## Completed product backbone

- Objective understanding with ranked service candidates and ambiguity stop
- Requirements discovery with source provenance/authority status
- 34-service shared registry and marketplace
- Government ontology
- Dependency-aware work graphs and parallel task execution
- Durable queue, retries, idempotency, checkpoints and case leases
- Durable case/document/notification/payment/event persistence
- Evidence verification, reconciliation, exceptions and critical-path visibility
- Human/statutory and physical-action boundaries
- Synthetic Government Environment
- Tamper-evident audit hash chain and integrity verification
- Supabase Auth integration
- Server-controlled memberships, tenant/RBAC/department/jurisdiction authorization
- Scoped developer API keys with expiry/revocation
- Server-side document storage, hashing, extraction, encryption and OCR adapter
- Notification outbox with delivery/retry/idempotency support
- Payment ledger with idempotent provider adapters
- Operator analytics
- Unified Aether Command Center
- Worker runtime with durable leases and notification dispatch
- Render deployment with managed-Postgres migration discipline and database-ready worker
- Vercel frontend deployment and SPA fallback
- Supabase RLS/security hardening
- Automated backend/frontend CI and deployed smoke testing

## Deployment validation history (re-verify before launch)

### GitHub
The integrated development release candidate has passing backend tests, frontend lint/build and combined CI. Always re-run and verify workflows on the exact release commit before merge.

### Supabase
The existing Free project was restored to ACTIVE_HEALTHY on 2026-11-13. Live database inspection confirmed ten applied migrations, 13 public application tables, ten internal execution tables, RLS enabled across those application tables, a restricted `aether_runtime` role, a private `aether-documents` bucket and no Security/Health Advisor lints. These database checks do not prove the deployed Render backend has working credentials or that its auth/storage operations succeed.

The runtime database role has only the access needed by the Aether server/worker and does not require database/schema creation privileges.

### Render and frontend
Historical deployment checks in this document are stale until repeated against the current release. The connected Render workspace currently has:
- `aether-backend` on `main`, latest recorded live commit `f64148aad10a5f8f586efde0cefe7a817fe6d996` (2026-10-15).
- `aether-public-demo` on `launch/public-research-preview`, latest recorded live commit `eb148e6dc6866ea0a5214b01d9f908a89d94a264` (2026-10-29).
- No separate `aether-worker` service, despite its declaration in `render.yaml`.
- Current release-candidate branch is not deployed to either service. No fresh health/readiness, worker-tick or staging E2E evidence is available.

The repository contains frontend deployment configuration, but the currently active frontend provider, deployment commit and frontend/backend pairing must be independently verified.

## Controlled-MVP boundaries

The controlled MVP intentionally uses deterministic synthetic government integrations. It does not issue official government decisions/documents and does not represent live government authority.

The 34-service catalog shares a common execution backbone. Some services have deeper domain-specific workflow templates than others; this is a deliberate controlled-MVP scope choice, not a silent claim that every jurisdiction has fully modeled legal procedures.

## Production / scale work after MVP

These remain external authorization, provider or scale prerequisites:

1. Authorized live government connectors and endpoint certifications
2. Authoritative, versioned, effective-dated rule packs for each launch service/jurisdiction
3. Certified statutory signature, certificate and issuance integrations
4. Production OCR/vision provider contracts and credentials
5. Production notification delivery and payment processor contracts/credentials
6. Full tenant/department/jurisdiction penetration testing
7. Production load/chaos testing
8. Distributed event-sourced replay and large-scale worker orchestration
9. Legacy-module retirement after dependency proof

These must not be simulated as completed.

## Legacy-code policy

Do not delete legacy modules merely because a V2 equivalent exists.

A legacy file is deleted only when:
- no production route imports it,
- no V2 path depends on it,
- its data model has a V2 replacement,
- its behavior is covered by tests,
- and the replacement is confirmed in the unified MVP flow.

## Next product phase

See `REAL_GOVERNMENT_ACTIVATION.md` for the production activation workflow. The next phase is authorized real-world integration, not more controlled-MVP scaffolding:
- onboard the first government sandbox/certified connector;
- load authoritative rule packs;
- configure production providers;
- execute security/load validation;
- then promote the controlled deployment posture toward real production.
