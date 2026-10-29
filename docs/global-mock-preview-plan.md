# Aether GovOS — Global Mock Preview & Pilot Plan

**Status:** Working research-preview plan; not an approved government proposal or a live integration.  
**Scope:** Global product preview using jurisdiction-neutral mock workflows; live integrations are added only for explicitly authorised jurisdictions and systems.  
**Operating mode today:** Synthetic/mock government data only.  
**Excluded:** Judicial/JusticeOS workflows, production citizen data, unauthorised scraping or portal automation, autonomous statutory decisions.

## Executive recommendation

Build and demonstrate one complete, low-risk service journey in Aether's Synthetic Government Environment before requesting live access. Prefer a read-only application-status lookup or document-verification workflow **only if** a department confirms an appropriate authorised interface exists. Do not assume that a public portal has an API or that public accessibility grants permission to automate it.

The MVP should prove that Aether can coordinate a case, preserve evidence provenance, execute permitted digital tasks, recover from transient failures, stop at a human-authority boundary, and produce an auditable final status.

## 1. Global preview hypothesis

> For a narrowly scoped public-service workflow, Aether can reduce repeated data entry and manual status-chasing while preserving the department's authority, existing system of record, security requirements, and auditability.

This is a hypothesis to test—not a claim of measured savings.

## 2. Mock-first workflow

1. **Intake:** A test user selects the service and supplies synthetic reference data.
2. **Validate:** Aether checks required fields and flags missing/invalid inputs.
3. **Build case graph:** Aether creates explicit tasks, dependencies, owners, timeouts, and allowed operations.
4. **Execute permitted tasks:** A mock connector returns deterministic success, pending, not-found, validation-error, and temporary-failure responses.
5. **Recover safely:** Retry only retryable operations; use idempotency keys to prevent duplicate submissions; route ambiguous outcomes to review.
6. **Human boundary:** Statutory decisions, physical inspection, and other reserved actions stop for an authorised officer. Mock mode must never imply that a synthetic approval is legally valid.
7. **Verify:** Aether reconciles the mock system response with the expected outcome and records the evidence reference.
8. **Notify and close:** The case timeline shows completed, pending, failed, and human-review tasks; the audit record captures what happened and why.

## 3. Required mock scenarios

- Happy path: all permitted tasks succeed.
- Missing document or invalid input: request correction without losing the case.
- Pending application: show pending state and poll only within the mock contract.
- Not found / mismatched reference: do not infer or fabricate a match.
- Rate limit / timeout / temporary outage: bounded retry with backoff.
- Unknown submission result: reconcile before retrying to avoid duplicate side effects.
- Connector returns an operation outside its allowlist: fail closed.
- Human decision or physical inspection required: pause and create a review task.
- Tenant/user access violation: deny and audit.
- Audit persistence failure: fail safely; never report an unrecorded operation as completed.
- Resume after worker restart: continue from durable state without duplicate side effects.

## 4. Mock data contract

All synthetic records must be visibly marked SYNTHETIC — NOT AN OFFICIAL RECORD in the UI and API responses. Use fictional names, identifiers, addresses, application references, document hashes, and timestamps. Never seed real personal data or reuse real credentials.

Each fixture should define:
- scenario ID and synthetic case ID;
- request and expected response;
- operation allowlist;
- expected task graph and state transitions;
- retry/idempotency expectations;
- expected audit events;
- expected user-facing result;
- assertions that no live external endpoint was contacted.

Mock connectors should be selected explicitly by environment/configuration. Production startup must reject demo sessions, mock credentials, synthetic government endpoints, and missing/empty operation allowlists.

## 5. Live-integration gate (jurisdiction-specific, never hard-coded globally)

No live connector is activated until all of the following are recorded and reviewed:

- named department/system owner and accountable operational contact;
- written authorization and approved purpose;
- approved environment, API documentation, credentials and network requirements;
- data minimisation, retention, access, incident and deletion rules;
- confirmed request/response contract, rate limits, status semantics and retry rules;
- written definition of which actions Aether may perform and which require an officer;
- versioned service rules with authoritative source, effective date and review date;
- contract tests against the authorised sandbox;
- security review, tenant isolation tests, audit verification and rollback/kill switch;
- agreed pilot measures, support process, and exit criteria.

If no approved API/sandbox exists, keep the integration mocked and ask the system owner for the sanctioned access route. Do not bypass access controls or automate a portal without permission.

## 6. Pilot measurement plan

Capture a baseline first, then compare the same measures during a controlled pilot:

| Measure | Definition |
|---|---|
| End-to-end elapsed time | Intake to verified result, with paused/waiting time separately reported |
| Citizen effort | Number of repeated fields, document resubmissions, and status-chasing contacts |
| Staff effort | Active staff minutes per case, excluding elapsed waiting time |
| First-pass completeness | Cases accepted for processing without a correction request |
| Automation rate | Permitted digital tasks completed without staff intervention / all eligible digital tasks |
| Exception rate | Cases requiring manual intervention, grouped by reason |
| Reliability | Retry success, duplicate-side-effect count, and unresolved connector errors |
| Safety | Unauthorized operations, tenant-boundary failures, missing audit events, and false completion reports |

Targets should be agreed with the pilot partner after baseline collection. Do not publish savings claims without measured, attributable results.

## 7. Responsibilities

**Aether team:** orchestration, mock scenarios, connector contract, audit, observability, tests, security documentation, operator runbook and pilot metrics.

**Department/system owner:** authoritative process and rule validation, access approval, interface documentation, credentials, permitted operations, human decision boundaries, operational support and acceptance criteria.

**Pilot sponsor:** scope, participating staff, baseline collection, user consent/notice where applicable, evaluation and go/no-go decision.

## 8. Immediate engineering acceptance criteria

- A single demo service can run end-to-end with deterministic fixtures.
- Every task has a visible state, dependency, operation and outcome.
- Failures and retries are reproducible in tests.
- Human-authority tasks cannot be silently auto-completed.
- Synthetic data is clearly labelled at every user-facing boundary.
- Audit events can be traced from intake to final case state.
- No test uses live government credentials or production personal data.
- CI covers happy path, exception path, authorization, tenant isolation, idempotency, resume/restart, and audit integrity.
- The demo UI clearly distinguishes simulated status from official status.

## 9. Global preview and live-integration decision gates

1. **Mock demonstration:** internal engineering acceptance.
2. **Process validation:** a knowledgeable service owner confirms the workflow and statutory boundaries.
3. **Sandbox:** written permission and official technical contract received.
4. **Controlled live pilot:** security/legal approval, defined cohort, support plan, rollback and success measures.
5. **Production:** only after pilot evaluation, operational ownership, monitoring, incident response and explicit release approval.

## Official discovery starting points

- India: API Setu — https://apisetu.gov.in/ and policy — https://www.apisetu.gov.in/api-policy
- Other countries: use the relevant national, state/provincial, regional or municipal digital-government API catalogues and the owning department's approved integration process.

These are discovery starting points, not proof that a specific service API is available or that Aether has access. Every live connector must be configured for a documented jurisdiction, system owner, approved purpose and explicit operation allowlist. Keep jurisdiction rules and credentials outside the global core.

## Current public preview implementation

The public research-preview branch contains a client-side mock studio driven by the canonical 32-service shortcut catalogue. It supports five user-selectable scenarios: routine path, missing evidence, authority/human review, retry after a synthetic transient failure, and an adverse evidence/rule-conflict path. Workflow stages are selected by service family (for example, property, permits, identity/records, welfare/tax, and business services).

The mock studio uses fictional checklist items and generates a synthetic reference locally. It does not submit a case to a government endpoint, validate actual jurisdictional rules, or create an official record. India-specific reference templates are labelled separately from configurable workflow patterns. The legacy country/service selector uses the same canonical catalogue; it does not claim all 32 templates are legally available in every country.

The static feedback form is registered with Netlify Forms, but a successful end-to-end submission has not yet been verified. Treat the feedback path as configured, not proven, until a controlled test submission is received and confirmed.

Before public promotion, verify the deployed preview renders the latest branch commit, manually exercise all five scenario modes on representative templates, confirm the form receives a test submission, and recheck mobile accessibility, privacy copy, and error states. A passing build alone does not satisfy these checks.

## Current truth

A mock-first pilot can prove Aether's software behaviour, orchestration, safety boundaries, recoverability and user experience. It cannot prove that a government API exists, that a department has authorised access, that official rules are correct, or that operational time/cost savings have occurred. Those require separate validation.
