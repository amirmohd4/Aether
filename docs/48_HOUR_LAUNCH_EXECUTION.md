# Aether controlled MVP — 48-hour launch execution

Last updated: 2026-11-14

## Release target

Target a controlled public synthetic MVP release by 2026-11-16. This is a release target, not a claim that every gate has passed.

## Product scope in this release candidate

The hardened development branch contains the shared Aether execution backbone: objective understanding, a 34-service registry, requirement discovery, dependency-aware work graphs, durable queue/checkpoints/retries, evidence and document handling, audit/reconciliation, tenant membership/RBAC, operator and officer workflows, notification/payment foundations, developer marketplace foundations, and India administrative-intelligence discovery.

The public experience adds an interactive synthetic journey studio with routine, missing-evidence, human-review, retry and adverse/conflict scenarios; a research-preview explainer; and a structured feedback form. The studio is explicitly client-side simulation. The authenticated Command Center remains the product surface for real Aether case execution in the controlled environment.

## Non-negotiable boundaries

- No official government application is submitted by the synthetic studio.
- No protected government records are accessed.
- No Aether-generated statutory approval, rejection, certificate, permit or benefit is represented as official.
- No real identity or confidential documents are requested in the public demo.
- Live integrations remain disabled unless the relevant authority, publisher permissions, credentials and technical tests are in place.
- Service templates and jurisdiction labels are indicative until verified against current official sources.

## 48-hour execution gates

### Gate A — frontend and user journey
- [ ] Netlify deploy preview builds from the exact hardened branch head.
- [ ] Research preview, interactive studio, Command Center, Delivery Ops and India admin surfaces render without runtime errors.
- [ ] Test all five synthetic scenarios and reset behaviour.
- [ ] Test feedback handoff, validation and successful Netlify Forms submission.
- [ ] Test mobile and desktop layouts and keyboard navigation.

### Gate B — backend and data safety
- [ ] Deploy the exact hardened commit to an isolated staging API.
- [ ] /health and /ready pass; /ready confirms the least-privilege aether_runtime role.
- [ ] Authenticated release-readiness endpoint reports controlled-MVP readiness.
- [ ] Supabase Auth, private document storage upload/read, encryption and deletion/retention controls are verified.
- [ ] Tenant isolation, role, scope and jurisdiction-denial tests pass against deployed staging.
- [ ] Durable worker, idempotency, retry and restart recovery are verified against staging data.

### Gate C — operational release
- [ ] Exact frontend/backend commit pairing is recorded.
- [ ] Rollback target and procedure are tested.
- [ ] Privacy notice, synthetic-only disclosures, terms/contact route and counsel review are completed.
- [ ] No production branch merge or public-beta claim before Gates A–C are evidenced.

## Current known blockers

As of 2026-11-14, the latest hardened branch's frontend and backend CI passed, but its staging smoke job was skipped because staging URLs/API configuration were absent. Render production still runs an older backend commit. The Supabase runtime role exists, but the deployed Render connection has not been proven to use it. The current public research-preview deployment is a separate, older branch and must not be mistaken for the hardened product release.

## Release decision

A public synthetic research preview may be released once Gate A passes and the public privacy/safety boundary is confirmed. The authenticated, database-backed controlled MVP must remain no-go until Gate B and Gate C pass. Do not silently downgrade the latter gates or describe an unverified staging deployment as complete.
