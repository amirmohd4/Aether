# Autonomous Execution Proof: first benchmark

## Objective

Prove whether Aether performs operational work after intake—not merely accepts applications—using one versioned workflow and auditable task-level evidence.

**First technical proof:** run one synthetic J&K small food-business journey end-to-end in the existing controlled environment. This is a software test, not proof of live-government impact. The jurisdiction, exact business profile and legally applicable approvals remain to be validated.

## Build for autonomy from day one

The workflow engine must own the case from intake to verified outcome. Tasks should execute automatically by default when all of these are true: the rule is authoritative and current, the action is within the tenant's granted permissions, the connector is approved, the operation is idempotent or safely recoverable, and success can be verified. If any condition fails, Aether must block or route the task to a named exception queue rather than pretend it completed.

Do not treat a generated note, a queued request, an HTTP 200, or a successful submission as a verified government outcome. A result counts as verified only when an authoritative source or approved test double confirms the expected state.

## What to run now

1. Select one existing end-to-end workflow template already in the repo; do not add a new generic platform.
2. Create a synthetic test case with explicit tasks: intake, document completeness, rule/eligibility checks, fee/evidence reconciliation where applicable, authorised interdepartment requests, response tracking, exception recovery, and final outcome verification.
3. Run the case with no human intervention for all permitted routine tasks. Inject missing documents, conflicting data, duplicate delivery, timeout/outage, stale rule version, required inspection, and statutory approval.
4. Confirm every injected fault produces a safe retry, a recoverable blocked state, or a clearly owned human exception. It must never invent an inspection, decision, payment, certificate, or external state change.
5. Compare the case state with the synthetic system of record and retain the event/audit export.
6. Record a manual baseline separately: staff minutes and handoffs from observed cases or a department-approved time study. Do not invent baseline numbers.
7. Repeat with an authorised sandbox or shadow pilot only after written permission and data/security review.

## Metrics and definitions

Use `python tools/autonomy_benchmark.py <task-log.csv>` to aggregate a task-level CSV. The tool deliberately labels its results as unvalidated until the source evidence is independently checked.

- **Autonomous task rate:** tasks completed in automated mode with no manual intervention / all recorded tasks.
- **Automated task share:** tasks configured for automated execution / all recorded tasks. This alone is not a success metric.
- **Task completion rate:** completed tasks / all recorded tasks.
- **Staff minutes reduced:** measured baseline staff minutes minus measured Aether-run staff minutes.
- **Handoffs removed:** measured baseline handoffs minus actual handoffs.
- **Verified outcome rate:** cases with an authoritative verification / all cases.
- **Correct outcome rate:** cases with independently checked correct outcome / all cases.
- **Unauthorised actions:** must remain zero.

The CSV columns are: `case_id, task_id, execution_mode, task_status, manual_intervention, outcome_verified, outcome_correct, unauthorized_action, baseline_staff_minutes, actual_staff_minutes, baseline_handoffs, actual_handoffs`. One row per unique task; case-level measures repeat identically across that case's rows. Boolean values may be true/false or 1/0. Execution mode is automated, human, or mixed; task status is completed, failed, blocked, or pending.

## Pass/fail gates

**Technical gate:** every permitted synthetic task is executed or safely blocked; fault injection recovers correctly; duplicate actions do not duplicate effects; no unauthorised action occurs; all outcomes reconcile to the synthetic system of record; audit events identify the actor, task, permission, input/evidence, result and timestamp.

**Impact gate:** baseline and pilot cases are comparable; median/p90 elapsed time, applicant effort, staff minutes, repeat submissions, and handoffs improve; outcomes are not less accurate; a named institutional owner accepts the result.

**Live activation gate:** written authority, approved API/sandbox credentials, effective-dated rules reviewed by the responsible authority, security/privacy review, rollback/incident plan, and UAT sign-off. No bypassing access controls, scraping protected systems, or impersonating staff.

## Current honest status

The repository describes a deterministic synthetic government environment and an execution/orchestration foundation. This document does **not** claim the benchmark has been run, that any staff minutes have been saved, or that a real department has authorised Aether. The next proof requires running the workflow and publishing the actual test output and failures, not a slide deck.
