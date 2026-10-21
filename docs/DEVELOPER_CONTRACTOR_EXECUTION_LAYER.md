# Aether Developer + Contractor Execution Layer

## Product thesis

Do not build another project-management dashboard. Aether should reduce the work required to move a project from intent to verified delivery across government, commercial, and financial systems. Existing tools record tasks; Aether should connect dependencies, evidence, accountable owners, and externally verifiable outcomes.

## Target users and high-cost failures

### Developers / real-estate operators
- Parcel/title and encumbrance checks are fragmented and often repeated across lenders, counsel, surveyors, and authorities.
- Approval requirements vary by jurisdiction and project type; stale checklists create rework.
- A permit or utility dependency can invalidate an otherwise credible schedule.
- Teams repeatedly re-upload the same evidence to banks, insurers, authorities, and partners.
- Project finance, drawdowns, escrow conditions, and milestone evidence are disconnected from delivery status.

### Contractors / EPC / subcontractors
- Tender eligibility, bid deadlines, addenda, bid bonds, and mandatory attachments are easy to miss.
- BOQ, scope, drawing revisions, and change orders drift across versions.
- Labour, safety, insurance, tax, and site-access evidence expires or is submitted late.
- Measurement books, milestone acceptance, invoices, and payment claims lack a single evidence trail.
- A dependency gets stuck because the owner, next action, or required proof is unclear.
- Progress reports hide uncertainty by presenting stale dates as facts.

## Product capabilities (sequenced)

1. **Outcome intake** — user states a goal; Aether identifies jurisdiction, project type, asset, contract, desired outcome, and missing context. Ambiguity must stop execution, not be guessed away.
2. **Evidence passport** — reusable, permissioned evidence references with issuer, subject, issue/expiry dates, source, hash, verification state, and reuse permissions. Avoid unnecessary duplication of sensitive files.
3. **Dependency graph** — link permits, land/title, design approvals, utility connections, procurement, labour compliance, inspections, finance conditions, milestones, and payment claims. Every edge has provenance and an owner.
4. **Deadline and expiry radar** — deterministic alerts for bid deadlines, document expiry, permit expiry, insurance renewal, milestone due dates, and payment due dates. Use explicit time zones and auditable source dates.
5. **Cost/schedule early warning** — compare baseline, commitments, forecast, contingency, planned finish, and forecast finish. Every warning shows inputs and calculation; missing data is unknown, never green.
6. **Tender readiness workspace** — parse tender pack/addenda, extract mandatory eligibility/evidence/deadlines, flag contradictions and missing documents, and produce a source-linked checklist. Human review remains mandatory for legal interpretation and bid submission.
7. **Change-order intelligence** — compare versioned BOQ/scope/drawings and identify changed quantities, dependencies, and cost/schedule exposure. Show diffs and source versions; never silently approve variation.
8. **Payment evidence pack** — assemble contract milestone, measured work, acceptance, invoice, tax/compliance evidence, approvals, and dispute status into a traceable claim package. Never promise payment or infer contractual entitlement.
9. **Developer API control plane** — versioned APIs, per-tenant keys/scopes, idempotency, sandbox fixtures, signed webhooks, request traces, replay-safe retries, quotas, and connector health.
10. **Recovery assistant** — when an external dependency fails, classify failure, preserve evidence, retry only idempotent operations, suggest permitted next steps, and route statutory decisions to authorized humans.

## Initial engineering slice

backend/aether_core/delivery_intelligence.py adds a pure, deterministic, advisory risk assessor for supplied budget, commitments, forecast, schedule dates, permits, milestones, dependencies, and payment-claim evidence. It returns stable finding codes, severity, supporting evidence needed, and explicit limitations. It does not call external systems and does not claim legal or construction compliance.

## Required next integration steps

- Add typed request/response models and a tenant-authorized API route; never expose another tenant's project.
- Persist project baseline and snapshots with provenance, timestamps, actor, source, and schema version.
- Add jurisdictional rules only from verified official sources with effective dates and source citations.
- Connect this engine to Aether case/work-graph tasks; emit findings as case events and link evidence references.
- Add frontend playbooks for tender readiness, permit readiness, payment evidence, and project risk.
- Add tests for date boundaries, decimal precision, malformed inputs, access control, idempotency, persistence/restart, and adversarial payloads.
- Run the repository's backend test suite and frontend typecheck before calling the feature integrated.
- Keep all live authority actions disabled until authorized credentials, provider contracts, and validation are in place.

## Success metrics

Measure against a baseline rather than claim improvements without evidence:
- time from intake to a complete, source-backed evidence pack;
- preventable rejection rate for incomplete submissions;
- days from milestone acceptance to a complete payment claim;
- number of duplicate document requests;
- stale/expired evidence detected before submission;
- schedule and cost warning precision (false-positive and missed-risk rates);
- connector success, retry, and recovery rates;
- human minutes saved per completed outcome.

## Non-negotiable safeguards

- No fabricated official statuses, title ownership, lien clearance, permit approval, engineering sign-off, or payment entitlement.
- Every risk finding exposes its inputs and limitations.
- No automatic bid submission, statutory filing, engineering sign-off, or payment release without explicit authorization and required human controls.
- Missing data is an explicit unknown state.
- Evidence and project data are tenant-scoped; secrets remain server-side.
