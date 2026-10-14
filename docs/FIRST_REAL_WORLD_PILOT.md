# First Real-World Pilot: J&K Cross-Agency Business Setup

## Decision

Stop expanding the service catalogue and stop adding general-purpose features until this pilot is validated.

**Pilot hypothesis:** Aether can reduce applicant effort, staff coordination effort, and end-to-end uncertainty for one narrowly scoped business-opening journey by coordinating authorised work across existing systems.

**Candidate journey:** opening a small food-service business in one Jammu & Kashmir jurisdiction. This is a hypothesis to validate, not a claim that every business needs the same approvals. The exact location, business profile, applicable approvals, and pilot sponsor must be confirmed before the workflow is treated as authoritative.

## Why this is the first candidate

- OECD's *Smart Regulations, Strong Business* research reports that in 60% of surveyed countries businesses say they must submit the same documents more than once in licensing/permitting; business organisations in only 13% say permit processes and timelines are coordinated across authorities; and business organisations in 67% report untimely decisions. These are country-level survey findings, not shares of all individual applications.
- Jammu & Kashmir has an existing Single Window System, and the National Single Window System lists J&K approvals and a "Know Your Approvals" route.
- FSSAI already operates FoSCoS for food-business licensing/registration and tracking. Aether must complement these systems, not duplicate their application portals.
- Aether's current controlled MVP uses synthetic government systems. It is not authorised to submit live applications or issue official decisions.

## Sources to verify during discovery

1. OECD, *Smart Regulations, Strong Business* (2025): https://www.oecd.org/en/publications/smart-regulations-strong-business_93d38770-en/full-report/diagnostic-drivers-of-regulatory-burden-and-complexity_7296019b.html
2. J&K Single Window System: https://singlewindow.jk.gov.in/
3. NSWS J&K approvals: https://www.nsws.gov.in/portal/jammukashmir
4. FSSAI FoSCoS: https://foscos.fssai.gov.in/
5. Aether real-government activation gate: https://github.com/amirmohd4/Aether/blob/main/REAL_GOVERNMENT_ACTIVATION.md

## Phase 1 — map the real process before coding

For one clearly defined business profile and location:

- Collect current official service pages, applicable acts/rules/orders, forms, fee schedules, required-document lists, published timelines, inspection conditions, appeal/grievance routes, and official status-tracking paths.
- Identify every potentially relevant authority and system; do not assume all approvals apply.
- Record each step's trigger, input, authoritative source, owner, dependency, allowed automation, human/statutory decision boundary, output, failure path, and effective date.
- Distinguish statutory deadlines from service targets and estimates.
- Interview applicants/agents, frontline processors, department/IT owners, and a potential budget owner. Record dated findings and separate observations from assumptions.
- Establish a baseline for elapsed time, applicant follow-ups/repeat submissions, staff minutes, handoffs, exceptions, and case outcomes.

**Gate 1:** no workflow is called production-ready until each mandatory requirement has an authoritative source, jurisdiction, effective date, and reviewer.

## Phase 2 — prove value in shadow/sandbox mode

Use the existing Aether execution kernel. Do not add a new platform layer unless a tested gap requires it.

- Turn the validated process into a versioned rule pack and dependency-aware work graph.
- Use official sandbox APIs or explicitly authorised test interfaces only.
- If no authorised interface exists, run a transparent shadow workflow with lawful sample/test data; do not scrape, bypass access controls, or impersonate users.
- Test incomplete evidence, conflicting data, changed rules, duplicate requests, timeouts, unavailable systems, overdue handoffs, required inspections, human approval, recovery and audit reconciliation.
- Compare Aether's case state with the authoritative system of record wherever a permitted test integration exists.

**Gate 2:** the complete cycle works, critical errors fail safely, every consequential action is authorised and auditable, and final outcomes are verified—not inferred from a successful submission.

## Phase 3 — authorised pilot

Before live operation obtain written authority, a named departmental/business owner, approved purpose and data scope, API contract and credentials, rule-pack sign-off, security/privacy review, incident owner, rollback plan, and UAT acceptance. Keep live execution fail-closed until every production gate in REAL_GOVERNMENT_ACTIVATION.md is satisfied.

Start with a small approved cohort. Never represent Aether output as an official licence, certificate, or decision.

## Success metrics

Set targets only after collecting a baseline.

- Median and 90th-percentile end-to-end completion time.
- Applicant time, repeat document submissions, calls/visits, and status-chasing.
- Staff minutes per case and number of manual handoffs.
- First-time-right application completeness.
- Unowned/overdue handoffs and exception resolution time.
- Verified outcome rate and safe recovery from outages/duplicate requests.
- Unauthorised consequential actions: **zero**.
- Implementation/support cost per case and cost/time to deploy the next workflow.
- Named buyer, budget route, and evidence of willingness to pay.

## 30-day immediate work

**Days 1–5:** choose the exact local body/district and business profile; collect official rules and portal paths; list candidate approvals without assuming applicability.

**Days 6–12:** map the current-state process and evidence provenance; identify unknowns, owners, status mechanisms, and where a lawful sandbox or pilot permission might be obtained.

**Days 13–20:** interview 8–12 stakeholders if access permits; collect real examples of delays/rework and establish a baseline plan. Do not claim interviews or baseline data until completed.

**Days 21–30:** produce a reviewed process map, source-backed rule-pack draft, connector feasibility matrix, threat/data-boundary assessment, pilot sponsor plan, and go/no-go recommendation.

## Decision rule

Proceed to a live pilot only if there is (1) a meaningful measurable pain, (2) a named institutional sponsor/buyer, (3) authoritative current rules, (4) a lawful integration path, (5) baseline data, and (6) a credible way to verify outcomes. Otherwise keep the work in shadow mode or choose a better-supported workflow.

## Product boundary

This work continues the original Aether GovOS goal:

**Objective → plan → authorised execution → cross-system coordination → exception resolution → verified outcome.**

The product differentiator is reliable, reusable execution across existing systems—not another directory, chatbot, or portal.
