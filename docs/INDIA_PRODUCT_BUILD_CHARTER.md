# Aether India — Product Build Charter

## Product decision

Aether is an India-first AI Government Execution Platform. It is not a replacement front-end for government portals and not a generic chatbot. It is an administrative intelligence and execution system that understands an outcome, maps applicable services and authorities, assembles evidence, coordinates work across systems and people, manages exceptions, and reconciles completion against the relevant government system of record.

## Who it serves

- Citizens and households
- MSMEs, startups and large businesses
- Developers, contractors and infrastructure operators
- Banks, NBFCs and insurers performing consent-based due diligence
- Government officers and departments
- Developers and technology partners through APIs

## Product architecture

1. **National Administrative Ontology** — government levels, departments, authorities, jurisdictions, service families, laws, documents, applications, cases and outcomes.
2. **Effective-dated Rules & Evidence Registry** — source URL, issuing authority, jurisdiction, publication date, effective period, applicability predicates, document requirements, notified service timeline, designated officer, appeal route and verification history.
3. **Intent-to-Outcome Planner** — converts natural-language objectives into a case plan, asks for missing facts and explains why each step may apply.
4. **Dependency Graph Engine** — typed relationships: statutory prerequisite, conditional prerequisite, evidence dependency, operational dependency, parallel work, human decision and physical inspection. Every statutory edge must carry a source and effective date.
5. **Case & Work Orchestrator** — idempotent work items, parallel execution, deadlines, retries, escalations, resumable cases and cross-department handoffs.
6. **Evidence & Document Intelligence** — extraction, validation, deduplication, provenance, consent, purpose limitation, retention and reusable evidence references.
7. **Connector Fabric** — API-first adapters, approved portal automation only where explicitly permitted, human-assisted tasks and synthetic sandbox adapters.
8. **Authority & Governance Layer** — least privilege, tenant/department/jurisdiction isolation, separation of duties, human statutory decisions, immutable audit and grievance/appeal handoffs.
9. **Outcome Reconciliation** — do not call a case complete merely because a connector returned success; reconcile with the authority's system of record and retain official evidence.
10. **Developer & Partner Platform** — scoped API keys, SDKs, webhooks, service catalog, connector certification and partner marketplace.
11. **Operations Intelligence** — service-level bottlenecks, repeat document requests, rejection reasons, workload, exception patterns and policy-change impact.

## India-wide operating model

Central ministries and agencies, State/UT departments, district administrations, urban and rural local bodies, statutory regulators, utilities, courts and public-sector institutions must be represented as separate authority types. A department label alone is insufficient to identify the competent authority. Each service instance is resolved using country, State/UT, district, local body, subject facts and the effective date.

## Replacement strategy

Aether should replace a legacy module only when it can prove functional coverage, legal authority, data migration, interoperability, security, auditability, uptime, accessibility, disaster recovery, procurement approval and a safe rollback. Otherwise Aether orchestrates the existing system through an authorized connector. Replacement is a technical and procurement decision, not a marketing claim.

## First deep journeys

1. Hotel / hospitality establishment.
2. Manufacturing unit establishment.
3. Real-estate development.
4. Contractor project delivery and milestone compliance.
5. Bank property due diligence (consent-based and evidence-limited).

These are journey templates for planning and discovery, not universal legal checklists. Every State/UT and local authority variant requires official source validation.

## Public beta boundaries

- Clearly label synthetic and illustrative workflows.
- Never issue or imitate official certificates, approvals, receipts or government identity.
- Never submit to a government system without an authorized connector, user consent and applicable legal authority.
- Do not infer statutory eligibility from generic AI knowledge.
- Keep personal data minimized, purpose-limited and tenant-isolated.
- Preserve human decisions, inspections, hearings and statutory discretion.

## Release gates

A public controlled beta requires: current branch CI green; frontend/backend smoke test; authentication and tenant-isolation tests; data retention and deletion controls; security review; accessibility review; realistic synthetic scenarios; clear disclosures; incident response; privacy notice and terms. A production government deployment additionally requires written authorization, approved credentials/endpoints, source-backed effective-dated rules, provider contracts, security testing and system-of-record reconciliation.

## Build sequence

1. Integrate the Administrative Intelligence read APIs and seed taxonomy.
2. Add a source-backed rule-pack schema and review workflow.
3. Add graph validation and conditional dependency evaluation.
4. Deepen one journey end-to-end without claiming statutory completion.
5. Add India jurisdiction packs and source verification workflow.
6. Certify connectors one authority at a time.
7. Add role-specific public and officer workspaces after workflow reliability is proven.
