# Autonomous Execution Proof: first benchmark

## Objective

Prove whether Aether performs operational work after intake—not merely accepts applications—using one versioned workflow and auditable task-level evidence.

**First technical proof:** run one synthetic J&K small food-business journey end-to-end in the existing controlled environment. This is a software test, not proof of live-government impact. The jurisdiction, exact business profile and legally applicable approvals remain to be validated.

## Build for autonomy from day one

The workflow engine must own the case from intake to verified outcome. Tasks should execute automatically by default when all of these are true: the rule is authoritative and current, the action is within the tenant's granted permissions, the connector is approved, the operation is idempotent or safely recoverable, and success can be verified. If any condition fails, Aether must block or route the task to a named exception queue rather than pretend it completed.

Do not treat a generated note, a queued request, an HTTP 200, or a successful submission as a verified government outcome. A result counts as verified only when an authoritative source or approved test double confirms the expected state.

## Automated end-to-end proof

The repository now includes `backend/tests/test_end_to_end_employee_workflow.py`. It exercises a fictional restaurant-onboarding case through citizen intake, internal employee tasks, an explicit human-authority pause, simulated approvals, final case completion, event checks, and persisted audit-chain verification. It intentionally excludes JusticeOS/judicial workflows.

Verified on candidate commit `20d28f2a1799056357c27ec111943b038c3e868b`: [Aether MVP CI](https://github.com/amirmohd4/Aether/actions/runs/38686985214) passed, including the backend suite (**137 passed**), frontend build, autonomy benchmark tests, public feedback asset checks, and live public-demo smoke test. The end-to-end test is synthetic software verification only; it is not evidence of live-government integration or measured staff-time savings.

Run the focused test from the repository root:

```bash
cd backend
PYTHONPATH=.:.. pytest -q tests/test_end_to_end_employee_workflow.py
```

## What to run next

1. Extend the existing end-to-end test with fault injection: missing documents, conflicting data, duplicate delivery, timeout/outage, and stale rule version.
2. Verify each injected fault causes a safe retry, recoverable blocked state, or clearly owned human exception. It must never invent an inspection, decision, payment, certificate, or external state change.
3. Reconcile the final case state against the synthetic system of record and retain the event/audit export.
4. Record a manual baseline separately using observed cases or a department-approved time study. Measure staff minutes and handoffs; do not invent baseline numbers.
5. Repeat in an authorised sandbox or shadow pilot only after written permission and data/security review.

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
