# Aether — Master MVP Build Plan

## Product target

Aether is a Government Operating System / execution layer. The controlled MVP supports one shared execution backbone for citizens, businesses, banks/NBFCs, developers/real-estate, insurers, enterprises and government officers.

Core promise:

Objective → understand → discover requirements → create case → build government work graph → execute independent digital work in parallel → verify/reconcile → handle exceptions → request authorised human action only where required → resume → outcome → evidence/audit.

## Controlled-MVP status

**Controlled/sandbox software: implemented; research-preview CI and smoke checks: passing. Production release gate: NOT COMPLETE.**

The controlled software path can run deterministic, non-authoritative workflow scenarios through the unified Command Center, case/work-graph engine, worker runtime, document storage, audit trail, RBAC and service marketplace. The public research-preview branch has passing backend tests, frontend build checks, and synthetic-demo smoke tests. These checks do not by themselves verify the production-domain frontend, production Render/Supabase runtime, feedback delivery, rollback readiness, or any live government integration.

This status describes the controlled software and its preview checks—not production approval or live government authority.

## Completed product backbone

- Objective understanding with ranked service candidates and ambiguity stop
- Requirements discovery with source provenance/authority status
- 32-service non-judicial shared registry and marketplace
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
- Backend/worker deployment architecture with managed-Postgres migration discipline
- Netlify-hosted public research preview with a separate synthetic-only Render demo backend
- Supabase RLS/security hardening in the codebase and migration set
- Automated backend/frontend CI and synthetic-preview smoke tests

## Deployment validation completed

### GitHub
The current `launch/public-research-preview` head (`099d3e558bfa9224fc1fb6115a1a7d2d4b5582ac`) has passing backend tests, frontend build/typecheck, public-launch asset checks, autonomy benchmark, and synthetic public-demo smoke tests. The production-domain deployment and rollback gate are not certified by these preview checks.

### Production Supabase and Render
The production Supabase/Render state must be re-verified against the currently intended production project and service before release. Do not infer production health from a successful research-preview build or from the separate public-demo deployment. Confirm migrations, RLS/security-advisor findings, `/health`, `/ready`, database readiness, worker ticks, runtime permissions, and rollback behavior during the production release gate.

### Netlify and Render — current public research preview
The current public research preview is hosted on Netlify and uses a separate Render service (`aether-public-demo`) for synthetic-only backend requests. The public preview must not use production credentials or live government connectors. The Netlify production-domain deploy and the separate production Render/Supabase runtime must be verified independently before any production release; a ready deploy preview is not evidence that the production stack is approved or healthy.

## Controlled-MVP boundaries

The controlled MVP intentionally uses deterministic synthetic government integrations. It does not issue official government decisions/documents and does not represent live government authority.

The canonical user-facing catalog contains 32 non-judicial synthetic service templates and shares a common execution backbone. Some services have deeper domain-specific workflow templates than others; this is a deliberate controlled-MVP scope choice, not a claim that every jurisdiction has fully modeled legal procedures.

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
