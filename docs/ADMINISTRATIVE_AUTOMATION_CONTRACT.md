# Administrative Automation Contract

## What is automated in the controlled MVP

The planner converts deterministic delivery-risk findings and unresolved dependency handoffs into proposed, deduplicated actions. A tenant-bound enqueue endpoint persists allowlisted internal follow-up actions with stable idempotency keys. Sensitive follow-up actions enter an approval state and require a different authorized reviewer. An authenticated worker claims queued records with a lease, retries failures with backoff, reclaims expired leases, and creates a separate durable work-item record. Dispatch is marked verified only after that work item is reloaded and checked against its tenant and case.

Department administrators can assign work items. Authorized staff can complete them with a completion note; evidence document IDs, when supplied, must belong to the same case and tenant. Where an action requires evidence, at least one case document is mandatory. Completion verification covers internal record integrity and evidence references, not whether an external authority accepted the result.

## Explicit non-automation boundary

The worker allowlist contains internal follow-up tasks only. It does not file forms, submit bids, change permit/legal status, certify construction, approve contractual entitlement, or release money. Those require official integrations, source-of-truth reconciliation, least-privilege connector credentials and the appropriate authorized decision-maker. A durable internal work item is not an official outcome.

## Runtime requirements still needed before production

- Set AETHER_AUTOMATION_WORKER_TOKEN in the backend runtime.
- Set GitHub repository secrets AETHER_AUTOMATION_WORKER_URL (HTTPS base URL of the deployed API) and AETHER_AUTOMATION_WORKER_TOKEN (same high-entropy token).
- Ensure production uses PostgreSQL and the expected DATABASE_URL; verify schema creation/migrations and backup/recovery policy.
- Configure tenant membership, role assignments, CORS, secrets rotation and monitoring.
- Run a staging end-to-end exercise for queue, approval, dispatch, lease recovery, assignment, completion and evidence rejection before enabling production traffic.

## Execution flow

1. Recompute the proposal from the current case state; reject stale proposals.
2. Verify case access and tenant binding.
3. Persist an idempotent queue record; duplicate requests return the existing record.
4. Require second-person review for actions marked as requiring a human decision.
5. The authenticated worker claims work with a lease and bounded retries.
6. Atomically create a durable internal work item and mark dispatch verified only after reloading the work item.
7. Assign the work item to an authorized staff identity.
8. Complete the work item with a note and case-scoped evidence references where required.
9. Preserve a clear distinction between internal completion and verified official outcomes.
