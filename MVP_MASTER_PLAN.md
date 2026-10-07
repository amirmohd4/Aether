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

Overall whole-MVP completion: **~48%**.

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
- Broad service catalog → all 34 identities now have a shared executable baseline; only a smaller number have evidence-backed domain-specific graphs
- Document intelligence → foundation exists, but production-grade extraction/validation is incomplete
- Government rules → provenance exists for a narrow verified slice, not broad jurisdiction/service coverage
- Connector framework → synthetic execution works and an opt-in REST adapter exists; real government connector certification/access is still incomplete
- Frontend → the unified Command Center now understands objectives, shows candidates, opens saved cases and resumes durable workflows; legacy service screens still exist and need retirement/migration
- Persistence → durable cases, queue leases, event ledger and resume APIs exist; full distributed replay semantics and operational worker service are still incomplete
- Error/recovery → retries exist, but distributed worker recovery is incomplete

### Major remaining build areas
1. Unified Objective/Understanding Engine
2. Complete Service Definition schema for every MVP service
3. Government Ontology expansion + entity resolution
4. Dynamic Work Graph generation from services/entities/rules
5. Durable worker queue, locking, leases, resumability and replay
6. Production connector abstraction with authorized API/portal/RPA adapters
7. Government rules/version/effective-date registry
8. Document extraction, validation, comparison and evidence packaging
9. Verification/reconciliation/risk/exception engine
10. Human Authority Console
11. Citizen/Business/Bank/Developer/Insurer/Enterprise workspaces
12. Developer/API gateway and authentication
13. Identity, tenancy, RBAC, secrets and security hardening
14. Payment/fee workflow
15. Notification/event delivery
16. Billing/usage metering for private customers
17. Marketplace foundations
18. Government service analytics and critical-path analytics
19. Unified frontend + backend integration
20. Full integration/E2E/security/load test suite
21. Cleanup of superseded legacy modules and artifacts
22. Final deployment, migration, smoke tests and rollback plan

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
