# Aether One-Stop Developer and Contractor Execution Plan

## Product objective

Aether is not merely a directory of services or a document submission portal. It is an outcome execution layer that coordinates the work before, during, and after an application across a developer's or contractor's lifecycle. The product should remove avoidable data re-entry, document chasing, status chasing, manual routing, deadline misses, reconciliation and repetitive administrative work.

"Instant" means instant intake validation, dependency discovery, evidence reuse, routing, task creation, status visibility and safe execution of operations that have authorized integrations. It must never mean inventing an official result or bypassing an authority's review or a physical inspection.

## User journeys

### Developer / project owner: idea to operational project
1. Capture project type, parcel/location, jurisdiction, intended use, ownership/lease context, scale and target dates.
2. Build a versioned requirements checklist using official, effective-dated sources; mark unknown rules explicitly.
3. Create a dependency graph across land/title, planning/zoning, building, fire, environment, utilities, taxes, procurement, financing, inspections and completion.
4. Request only missing evidence; reuse previously verified evidence when the issuer, subject, validity, permissions and purpose match.
5. Run independent checks in parallel where dependencies allow.
6. Track each external request with correlation ID, submitted payload hash, provider status, last verified time and next poll/retry time.
7. Reconcile conflicts across records and route exceptions to the right authorized reviewer.
8. Produce a completion pack with decisions, receipts, outstanding conditions and evidence provenance.

### Contractor / EPC: tender to accepted work and payment claim
1. Import tender documents and amendments; record source/version and bid deadline.
2. Extract eligibility criteria, bid security, mandatory attachments, submission format, clarifications and addenda.
3. Run a readiness gate with source-linked evidence and an explicit unresolved-items list.
4. Compare BOQ, specifications, drawings and change orders by version; show diffs and cost/schedule exposure for human approval.
5. Track worker/site compliance evidence and expiry without treating upload as official validation.
6. Connect work packages, measurements, milestone acceptance, invoices and contractually required claim evidence.
7. Assemble the payment claim pack and route it to the contractual reviewer; track queries, resubmissions and verified payment status.
8. Keep a dispute/evidence timeline with communication and change history.

### Software developer / integrator: sandbox to reliable workflow
1. Discover versioned APIs and schemas.
2. Use synthetic fixtures with deterministic outcomes and test failures.
3. Authenticate with tenant-scoped credentials and least-privilege scopes.
4. Submit idempotent requests; track correlation IDs and signed webhook events.
5. Reconcile callbacks against polled status, safely retry transient failures and send permanent failures to an exception queue.
6. Inspect traces, rate limits, connector health, audit events and versioned error contracts.

## Shared platform primitives

- **Case / outcome record:** objective, tenant, owner, jurisdiction, target outcome and lifecycle status.
- **Dependency graph:** task dependencies, department, owner, evidence requirements, SLA clock and escalation policy.
- **Evidence passport:** issuer, subject, type, issue/expiry dates, source URI, checksum, verification level, purpose and access policy.
- **Connector contract:** capability, jurisdiction, authentication, allowed operations, idempotency, status lookup, rate limits, retries and source-of-truth semantics.
- **Work queue:** durable task claim, lease, attempts, idempotency key, backoff, dead-letter handling and recovery.
- **Event ledger:** append-only event history with actor, timestamp, correlation ID, before/after references and integrity verification.
- **Human authority boundary:** approval/signature, statutory decisions, physical inspections, engineering certifications, bid submission and money movement are gated by explicit authorization.
- **Outcome verifier:** independently reconcile receipt/reference/status/evidence; never equate a successful HTTP response with a completed real-world outcome.

## Cross-department orchestration rules

1. Resolve jurisdiction and project type before applying requirements.
2. Use parallel execution only for independent tasks; enforce dependency edges for prerequisites.
3. Assign one accountable owner and a next action to every open handoff.
4. Preserve source and timestamp for each rule and status.
5. Deduplicate requests only when idempotency semantics and payload identity permit it.
6. Retry only safe transient failures; do not blindly retry payments, filings, submissions or other non-idempotent operations.
7. Escalate stale external status by SLA and route to the correct department without losing history.
8. Reconcile contradictory records; do not silently choose the convenient result.
9. Notify only on meaningful state changes, required action, approaching deadlines or verified outcomes.
10. Track employee touches and citizen/contractor touches so manual-handoff reduction is measurable.

## Automation backlog (priority order)

### P0 — needed for a credible controlled MVP
- Persisted case and task state across restart.
- Tenant isolation and permission tests on every read/write endpoint.
- Reusable evidence metadata and expiry checks.
- Case-level dependency/handoff view with owner and next action.
- Deadline scheduler with timezone-aware dates and deduplicated notifications.
- Connector contract and synthetic test fixtures for success, pending, query, timeout, conflict, rejection and recovery.
- Source-backed requirement records with jurisdiction, effective date, source URL and last-verified timestamp.
- Complete end-to-end tests for developer readiness and contractor tender-to-payment.

### P1 — measurable admin-work reduction
- Tender pack ingestion and source-linked checklist.
- Version comparison for addenda, BOQ, specifications and change orders.
- Payment evidence pack and query-response workflow.
- Cross-agency status polling, webhook intake and reconciliation.
- Expiry/deadline radar with escalation and assignment.
- Reusable evidence passport and permissioned sharing.
- Department inbox with workload, aging, SLA and reassignment controls.

### P2 — higher leverage intelligence
- Predictive schedule/cost risk only after adequate historical data and measured calibration.
- Workflow recommendation from prior resolved cases, with explainable evidence and human override.
- Connector health-based routing and safe fallback.
- Portfolio analytics for recurring bottlenecks and duplicate evidence requests.
- Developer SDK, webhook replay tools and observability portal.

## Current implementation slice

The branch adds a deterministic advisory risk engine and a new authenticated API surface:
- GET /api/aether/v2/delivery-playbooks
- GET /api/aether/v2/cases/{case_id}/delivery-intelligence

The case endpoint composes budget/schedule/permit/payment risk findings with recorded task dependencies and cross-department handoffs. It reads existing case state; it does not mutate official records or claim live authority integration.

## Verification and release gates

- Run backend tests and type/lint checks in CI.
- Test demo, API-key and Supabase authorization modes; verify cross-tenant and cross-department access is denied.
- Verify case/task state survives process restart.
- Test idempotency and concurrent execution.
- Confirm all synthetic results are visibly labelled and no mock connector is presented as live.
- Validate source-backed requirements for each enabled jurisdiction and service.
- Measure baseline and outcomes: intake-to-ready time, missing-document rejection rate, manual handoffs per case, staff minutes per case, time to complete payment pack, overdue task rate, false-positive risk rate, connector failure/recovery and verified completion rate.
- Keep production rollout blocked until real connector authorization, security review, monitoring, incident recovery and rollback are demonstrated.

## Product integrity

Do not advertise "instant approvals" or "all services automated" without evidence. Aether can make coordination, checks, preparation and routine digital exchanges faster; statutory decisions, disputed records, physical actions and money movement remain subject to the responsible authority and applicable controls.
