# Aether — Master MVP Build Plan

## Product target

Aether is a Government Operating System / execution layer. The controlled MVP supports one shared execution backbone for citizens, businesses, banks/NBFCs, developers/real-estate, insurers, enterprises and government officers.

Core promise:

Objective → understand → discover requirements → create case → build government work graph → execute independent digital work in parallel → verify/reconcile → handle exceptions → request authorised human action only where required → resume → outcome → evidence/audit.

## Controlled-MVP status

**Controlled/sandbox MVP: COMPLETE.**

The planned controlled-MVP software and deployment gate are complete. Aether can run deterministic, non-authoritative government execution scenarios using the unified Command Center, persistent case/work-graph engine, worker runtime, private document storage, audit trail, RBAC and service marketplace.

This is a release status for the controlled/sandbox product, not a claim of live government authority.

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
- Netlify frontend deployment and SPA fallback
- Supabase RLS/security hardening
- Automated backend/frontend CI and deployed smoke testing

## Deployment validation completed

### GitHub
The final release line has passing backend tests, frontend build/typecheck and deployment smoke testing.

### Supabase
The connected Aether project has the required persistence/operational migrations applied, the private document bucket, RLS enabled on the exposed legacy and internal execution data, explicit server-only runtime policies, and no current security-advisor lints.

The runtime database role has only the access needed by the Aether server/worker and does not require database/schema creation privileges.

### Render
The Aether backend is live at the configured Render URL.

Verified:
- Docker release starts successfully
- `/health` returns HTTP 200
- `/ready` reports the database ready
- worker connects to Supabase successfully
- worker produces successful durable ticks
- managed PostgreSQL is migration-owned; runtime no longer attempts schema creation
- worker failure backoff protects the service from connection storms

### Netlify
The Aether Command Center is published at the configured Netlify site and returns successfully in deployed smoke testing.

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

The next phase is authorized real-world integration, not more controlled-MVP scaffolding:
- onboard the first government sandbox/certified connector;
- load authoritative rule packs;
- configure production providers;
- execute security/load validation;
- then promote the controlled deployment posture toward real production.
