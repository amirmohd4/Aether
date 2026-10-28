# Aether CEO/CTO Execution Roadmap

**Version:** 1.0  
**Date:** 19 October 2026  
**Owner:** Aether leadership  
**Status:** Execution plan; commercial hypotheses are not yet customer-validated.  
**Scope:** Cross-industry Administrative Execution OS; India first, global architecture; education administration is a strategic long-term vertical. Judicial workflows remain out of scope.

## Executive decision

Build one reusable **Administrative Execution OS**, but launch through one narrow paid workflow. The first commercial wedge is **Aether Contractor Desk: tender qualification, evidence-pack preparation, contract obligation tracking, and running/final-bill readiness** for small and mid-sized contractors and the professional firms that serve them.

This is a deliberate beachhead, not the full company vision. It is comparatively reachable without waiting for a government procurement cycle or a bank's production integration/security approval. The first version can work from customer-provided documents and human-confirmed outputs, then add authorised integrations only when a buyer and supported access path justify them.

In parallel, maintain an education/public-administration discovery track, starting with a specific scholarship, staff-service, grant, or grievance workflow in one jurisdiction. Do not claim or attempt live government execution without the responsible institution's sponsorship, authoritative rules, access permissions and acceptance tests.

## Product definition

Aether is not another portal, chatbot, generic RPA script, or replacement for every system of record. It is the layer that:

1. Accepts a desired outcome or incoming case.
2. identifies the applicable process, jurisdiction, rules, evidence and authority boundaries;
3. compiles the work into a versioned dependency graph;
4. performs permitted digital tasks in parallel where safe;
5. records provenance, state changes, retries and exceptions;
6. routes only genuine decisions, inspections, consent or uncertain cases to a person;
7. resumes after a human or external system responds; and
8. verifies the result from authoritative evidence and reports what is complete, pending, blocked or failed.

**North-star promise:** “Give Aether the outcome. It coordinates every permitted step, keeps the case moving, proves what happened, and involves a person only when authority, judgment, physical work or uncertainty genuinely requires one.”

Maximum safe automation is the goal. Zero human involvement is not a credible universal promise: statutory approvals, professional judgment, physical inspections, consent, appeals and exceptional cases can require people.

## What exists today—and what it does not prove

The repository's controlled/sandbox MVP includes a shared service registry, objective/requirements intake, dependency-aware work graphs, queue/retry/checkpoint foundations, evidence and reconciliation patterns, role/tenant controls, audit, a command centre, and synthetic scenarios. The research-preview CI and smoke tests have passed on the documented branch.

That means the controlled software path is materially implemented; it does **not** prove that the production-domain deployment is healthy, that feedback delivery works, that real government systems are connected, that the workflows follow current law in every jurisdiction, or that a buyer will pay. The public preview is synthetic only. Keep production connectors disabled until the release gate is passed.

## Market-entry decision

### Beachhead: contractor operations

**Target buyer:** small and mid-sized works contractors, specialist tendering teams, and tender/contract administration firms that process enough bids and bills for repeat work to justify software.

**First paid job to be done:** “Tell me whether this tender/bill pack is complete, prepare the required evidence and drafts, track obligations and deadlines, and show me exactly what is missing before I submit or follow up.”

**Initial scope:**
- Ingest tender, contract, BOQ, measurement, invoice and supporting files supplied by the customer.
- Extract requirements and produce a source-linked checklist with page/section references.
- Reuse customer-approved business evidence with expiry and provenance controls.
- Flag missing, inconsistent, expired or conflicting information.
- Prepare a bid-document index and draft response pack for human review.
- Track contract milestones, securities, insurance, notices, measurement evidence and bill prerequisites.
- Reconcile customer-provided measurements, prior bills, deductions and invoice totals using deterministic calculations.
- Produce a bill-readiness report and a legitimate follow-up pack.
- Keep a case timeline and record whether each output is a draft, customer-confirmed, submitted, accepted, paid or independently verified.

**Do not promise in the first release:** guaranteed tender wins, official certification of work, guaranteed payment speed, automated legal interpretation without review, direct access to restricted portals, or proof of payment without authoritative evidence.

**Why this beachhead:** the workflow has repeated documents, deadline pressure, cash-flow consequences and a reachable private buyer. A useful first product can create value before live government integration. The main disconfirmation risk is that contractors may already be well served by consultants or may not pay enough; test this immediately instead of assuming demand.

### Parallel strategic track: education and government administration

Education remains a first-class long-term vertical, not a separate product. Select one specific, current workflow in one department and jurisdiction—for example, scholarship exception resolution, school-grant reconciliation, teacher/staff service requests, or school infrastructure work orders. First map the real process, existing MIS/HRMS/eOffice/treasury systems, applicable rules, decision rights, and measurable delay/rework. A government pilot requires a named sponsor and authorised access; public desk research alone is not enough.

### Why not start with a bank or insurer?

They remain high-value expansion markets, but production access involves sensitive data, incumbent LOS/LMS/claims platforms, security reviews, vendor onboarding and stronger validation requirements. Research their workflow gaps now; do not make them the first dependency for revenue unless an unusually accessible design partner appears.

## Roadmap and gates

Time ranges are targets for execution, not guarantees. Workstreams may overlap, but a later phase must not be declared complete until its exit criteria pass.

### Phase 0 — Baseline and launch safety (Days 1–5)

**Work**
- Re-check the current branch head, PR status, CI results and actual frontend/backend deployments.
- Re-run the user journey across intake, file upload, case graph, missing-evidence path, retry, human-review boundary, audit and outcome display.
- Confirm synthetic-only labels, safe fictional demo data, production connector flags, tenant boundaries, document access, error handling and feedback submission delivery.
- Confirm which service is authoritative for frontend hosting (Vercel is the intended official frontend; Render backend/worker; Supabase database/auth/storage). Netlify is redundant except for the existing research preview until migration/retirement is deliberately completed.
- Record every defect in a release checklist. Do not merge or deploy to production simply to make the roadmap look complete.

**Exit criteria**
- Reproducible test results and a deployment evidence record.
- No unresolved critical/high-risk tenant, auth, data exposure or unsafe execution defect.
- Clear distinction in product copy between synthetic demo, draft, submitted, accepted and verified outcome.

### Phase 1 — Workflow and buyer validation (Days 1–14)

**Work**
- Create a list of 30 target organisations across contractors and tender/contract administration firms; prioritise firms with repeat tenders, recurring bills and an identifiable operations owner.
- Conduct at least 12 structured discovery conversations and ask buyers to walk through a recent case using redacted documents. Do not ask only whether they like the idea.
- Measure current hours per bid/bill, number of manual handoffs, missing-document return rate, repeat queries, cost of outside help, volume per month and consequence of delay.
- Observe current tools: e-procurement portals, spreadsheets, accounting software, document folders, consultants, email and departmental works/finance systems.
- Test two offers: a narrowly scoped paid pilot and a recurring service. Record actual objections, current spend and who controls the budget.
- Build a workflow dossier with source links, step-by-step process, roles, exception cases, legal boundaries and integration feasibility.

**Exit criteria**
- At least 5 buyers confirm the problem with concrete recent examples.
- At least 3 provide a redacted sample pack or agree to a structured workflow review.
- At least 2 show a credible path to a paid pilot or provide a written expression of commercial intent.
- If these signals fail, change the workflow/segment before expanding the codebase.

### Phase 2 — Build the sellable Contractor Desk (Days 8–30)

**Build only what supports the first paid workflow**
- Customer workspace with cases, documents, deadlines, owners and status.
- Tender/contract document extraction with source citations to page/section and an explicit low-confidence state.
- Versioned tender/bill checklist templates with jurisdiction/department and effective date.
- Evidence passport: source, customer permission, document date, expiry, integrity hash and reuse restrictions.
- Deterministic reconciliation for supported numeric schedules; show formulas and source cells/pages.
- Exception queue: missing, inconsistent, expired, ambiguous, awaiting customer, awaiting authority.
- Draft generator for checklists, document indexes, clarification responses and follow-up letters.
- Human review and approval for external submissions or consequential outputs.
- Audit trail and exportable case report.
- Baseline-vs-Aether analytics: active staff minutes, elapsed time, rework, first-pass completeness and exception rates.
- Tenant-isolated data, secure uploads, retention/deletion controls and redaction guidance.

**Not in this phase**
- Building 100 new service templates.
- Replacing e-procurement or accounting platforms.
- Unauthorised portal automation or scraping.
- Fully autonomous statutory or financial decisions.
- Expensive integrations before a paying customer demonstrates need.

**Exit criteria**
- Test against a representative, redacted historical dataset with agreed acceptance criteria.
- Every extracted requirement links to evidence or is explicitly marked uncertain.
- Financial arithmetic is deterministic and tested; AI does not silently invent values.
- A reviewer can correct outputs and see the change history.
- A complete case can be exported with its evidence and audit record.

### Phase 3 — Paid, controlled pilot (Days 25–60)

**Offer**
- A 4–6 week pilot for one contractor's defined tender/bill workflow.
- Start with customer-supplied documents and draft/readiness outputs; customer retains submission and certification authority.
- Agree baseline metrics before starting and report results weekly.
- Charge a real pilot fee rather than treating free interest as proof of demand.

**Pricing experiment—not a market benchmark**
- Test a fixed pilot offer in the approximate range ₹25,000–₹1,50,000 depending on case volume, complexity and support.
- Quote only after confirming the scope; do not present this range as a verified prevailing market price.
- Test a recurring continuation offer based on active cases/volume, support and measurable value. Do not promise savings until measured.

**Pilot measures**
- Staff minutes per case and end-to-end elapsed time.
- First-pass completeness and missing-document detection.
- Number of manual handoffs and follow-ups.
- Extraction/reconciliation error rate.
- Percentage of cases completed without Aether-induced rework.
- User trust, weekly active usage and willingness to renew at a stated price.

**Exit criteria**
- Customer uses Aether on real, authorised cases.
- No material data/security incident or unreviewed consequential output.
- Measured improvement against the agreed baseline.
- Buyer signs a paid extension or gives a specific, evidence-backed reason not to renew.

### Phase 4 — Convert to recurring revenue and repeatability (Days 45–90)

**Work**
- Convert the pilot into a subscription or repeat-case contract.
- Standardise onboarding, security review, document retention, support, workflow configuration and pricing.
- Deliver a second customer using the same core, recording which features are reusable versus customer-specific.
- Build case-volume metering, tenant administration, usage reporting and a support runbook.
- Develop one approved integration only if customer value, permissions and economics justify it.
- Create a quantified case study only with customer permission and measured data.

**Exit criteria**
- At least 2 paying customers or one paying customer plus a signed, funded deployment plan with a clear date and buyer.
- Repeat onboarding is materially easier than the first deployment.
- Gross-margin model includes hosting, model/OCR costs, support and integration work.
- Renewal intent is based on demonstrated outcomes, not founder optimism.

### Parallel workstream — Education/public-sector validation (Days 1–90)

1. Choose one jurisdiction and one specific workflow; do not study “all education services” as one process.
2. Map current official rules, effective dates, forms, service timelines, system owners, human roles, exception paths and system-of-record evidence.
3. Identify current systems and where work still crosses portals, HRMS/MIS, eOffice, treasury/payment, spreadsheets and physical records.
4. Interview users/staff only with appropriate consent and confidentiality; seek a named department/programme sponsor.
5. Define a synthetic/offline prototype and a controlled pilot proposal.
6. Require written sponsorship, authorised data access, security/privacy review, acceptance criteria and an exit plan before live execution.
7. Measure actual resolution—not just formal closure—including reopened cases, elapsed time, staff effort and correct outcomes.

Do not wait for a government contract to validate the product, and do not imply that a public demo has official endorsement.

## Customer, buyer and value map

| Segment | Economic buyer | First valuable job | Existing alternatives to compare | Reason to buy | Main blocker |
|---|---|---|---|---|---|
| Works contractors | Owner, CFO, tender/operations head | Bid pack and bill-readiness workflow | Consultants, spreadsheets, e-procurement portal, accounting tools | Less manual preparation, fewer avoidable omissions, clearer obligations | Willingness to pay; existing consultants |
| Tender/contract admin firms | Practice owner / delivery lead | Process more client cases with the same team | Shared drives, templates, practice software | Higher case throughput and traceable quality | Change management; price |
| Banks/NBFCs | Lending operations / COO / transformation | Loan-file completeness and exception coordination | LOS/LMS, KYC/bureau providers, internal queues | Reduce query loops and manual case assembly | Security, vendor onboarding, data access |
| Insurers/TPAs | Claims operations leader | Evidence and query coordination | Claims platforms, TPA systems, provider portals | Fewer incomplete files and faster exception routing | Incumbent capability, medical/legal risk |
| Developers | COO / project director | Permit dependency tracking | Approval portals, project tools, consultants | Visibility across authorities and fewer missed prerequisites | Jurisdiction-specific rules, portal access |
| Education/public administration | Department/programme owner or authorised implementation partner | Scholarship, staff service, grant or grievance workflow | MIS/HRMS, eOffice, portals, treasury and manual coordination | Verified resolution and less rework | Procurement, authority, integration and data permissions |
| System integrators | Practice leader / delivery partner | Deliver cross-system workflows with reusable execution | Bespoke integration and RPA projects | Faster delivery and repeatable modules | Partner economics and differentiation |

## Product architecture order

Build and harden these layers in this order:

1. **Trust foundation:** identity, tenant isolation, permissions, secrets, audit, consent/legal basis, retention, kill switch.
2. **Process compiler:** typed workflow definitions, jurisdiction, effective dates, prerequisites, authority and proof of completion.
3. **Evidence passport:** source/provenance, extraction confidence, validation, expiry, permitted reuse and correction history.
4. **Execution runtime:** durable queues, idempotency, retries, checkpoints, timeout handling, reconciliation, replay and safe compensation.
5. **Connector/action fabric:** approved APIs and events first; RPA only where expressly permitted, stable and auditable; human task endpoints for inaccessible or reserved work.
6. **Role-aware workbench:** customer, operator, reviewer and authority views with a shared case state and appropriate permissions.
7. **Outcome verification:** distinguish draft, prepared, submitted, received, accepted, approved, issued, paid and independently verified.
8. **Operational intelligence:** time, cost, handoffs, rework, root causes, failure recovery and workflow improvement suggestions.
9. **Vertical packs:** contractor first; then the strongest validated adjacent workflow; education/public administration through its own approved rules pack.

Use language models for interpretation and drafting; deterministic code for calculations, permissions, state transitions and transaction controls. Every rule pack must have an authoritative source, effective date, jurisdiction, reviewer and test cases.

## Commercial discipline

- No claimed 70–80% likelihood of purchase without a representative buyer sample. Replace confidence claims with observed evidence: interview-to-sample rate, sample-to-pilot rate, pilot-to-paid conversion and renewal.
- A verbal compliment is not demand. A design partner, access to real redacted cases, a named budget owner and a paid pilot are stronger signals.
- Revenue is not profit. Track implementation labour, customer support, infrastructure, model/OCR, security, integration and sales costs.
- Avoid becoming a bespoke consulting shop. Customer-specific work must either be reusable, separately priced, or rejected.
- Do not charge citizens for ordinary access to public services as the default business model; institutional buyers should pay where feasible.

## Operating scorecard

Review weekly:
- qualified target accounts contacted and discovery sessions completed;
- cases/sample packs reviewed with permission;
- paid pilots proposed, signed and collected;
- time-to-first-value and weekly active customer users;
- median and p90 staff minutes and elapsed time per case;
- first-pass completeness, rework and exception rates;
- automation success and verified-outcome rates;
- AI extraction/reconciliation errors and unsafe-action blocks;
- support hours and gross margin per customer;
- renewals, referrals and reasons for lost deals.

## Release and safety gates

No live government/financial workflow is enabled until all relevant gates pass:
- written customer/department authorisation and data-processing terms;
- verified legal basis, jurisdiction and effective-dated rules;
- least-privilege connector credentials and documented API/portal permissions;
- security/privacy assessment and tenant-isolation tests;
- human approval gates for consequential or reserved actions;
- test cases for duplicate submissions, timeouts, partial failures and ambiguous outcomes;
- authoritative outcome verification and complete audit trail;
- operational monitoring, incident response, rollback/kill switch and customer support;
- user acceptance and a documented rollback/exit plan.

## Immediate next actions

1. Verify the latest branch, preview and intended Vercel/Render/Supabase deployment state; do not infer current health from historical CI.
2. Run the complete synthetic user journey and feedback-delivery check.
3. Build the 30-account contractor target list and interview script, then start discovery.
4. Use actual redacted tender/bill packs to validate extraction, source citations and deterministic reconciliation.
5. Ship only the minimum Contractor Desk capability needed for the first paid pilot.
6. In parallel, update one education workflow dossier from current authoritative sources and seek a named sponsor.
7. Report status using evidence: completed, blocked, not verified, or awaiting external authorisation.

## Decision rule

Aether expands when a workflow has all four:
1. a painful and recurring job supported by concrete case evidence;
2. an identified buyer and credible budget;
3. a legally and technically feasible execution path; and
4. a measurable outcome that can be verified.

If any is missing, research it before building more features.
