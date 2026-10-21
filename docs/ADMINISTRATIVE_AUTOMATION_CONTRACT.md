# Administrative Automation Contract

## What is automated now

The planner converts deterministic delivery-risk findings and unresolved dependency handoffs into proposed, deduplicated administrative actions. Each action includes a stable idempotency key, department, priority, evidence checklist, source finding/task and whether a human decision is required.

## What is not automated yet

The planner intentionally does not enqueue or execute actions. A production queue must first verify tenant access, allowed action types, accountable owner, source-backed rules, connector capability, idempotency support, and whether the action crosses a statutory or financial authority boundary.

## Safe path to execution

1. Create proposal and stable idempotency key.
2. Apply tenant/policy authorization and check duplicate active work.
3. Assign accountable owner and SLA from a versioned policy.
4. For internal administrative preparation, enqueue a durable task.
5. For external submissions, require a configured connector, source-backed requirements, explicit authorization and idempotency support.
6. For statutory, physical, contractual or financial decisions, pause for the authorized human.
7. Persist each attempt and correlation ID; reconcile the provider's source-of-truth status.
8. Notify only on meaningful changes, failures, required human action or verified completion.
