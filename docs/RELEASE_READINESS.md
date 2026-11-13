# Aether Release Readiness

Last checked: 2026-11-13 10:45 UTC

## Current decision

**NO-GO — NOT READY for public launch or production government deployment.** The repository contains a substantial sandbox MVP and a new India administrative-intelligence increment, but the live environment currently has a critical dependency blocker and the new increment is not merged or deployed.

Aether must be described as a synthetic/sandbox workflow platform unless and until a specific government connector is authorized, source-backed, tested and reconciled against the authority's system of record. Internal task completion is not an official government outcome.

## Verified repository state

- Default branch: `main`.
- The development branch `aether-mvp-build` is 60 commits ahead of `main` and has no divergence reported by GitHub compare. This means the existing MVP work is not yet in the default branch.
- The India administrative-intelligence branch `aether-india-admin-intelligence` is 13 commits ahead of `aether-mvp-build`.
- Pull request #17 targets `aether-mvp-build`, remains open and draft, and has not been merged.
- Latest feature-branch head checked: `73f89f33e043c83f5c3cc71db4c1bde62eb8ccba`.
- For that head, the dedicated backend test workflow completed successfully and the frontend lint/build workflow completed successfully. The combined CI backend job was still running at the time of this check; do not label all CI green until it completes.
- A Vercel preview URL was recorded for an earlier feature-branch commit. It has not been verified against the latest head and is not a production deployment.

## Live environment findings

1. **Supabase — BLOCKER.** The connected project named `aether` currently reports `INACTIVE`. Migration listing timed out and the database API reported that the database may not be accessible. The earlier October healthy-state report is stale and must not be used as current evidence. Do not attempt restoration without confirming the billing/compute implications.
2. **Render — service configuration found, runtime not proven.** The `aether-backend` web service is configured to deploy from `main` in Oregon; its latest recorded live deployment is from 2026-10-15 at commit `f64148aad10a5f8f586efde0cefe7a817fe6d996`. It does not contain the current development branch changes. The `aether-public-demo` service deploys from `launch/public-research-preview` in Singapore; its latest recorded live deployment is from 2026-10-29 at commit `eb148e6dc6866ea0a5214b01d9f908a89d94a264`. No Render application logs were returned for either service in the checked 24-hour window. A live deployment label alone does not prove application health.
3. **Branch-to-deployment gap.** Neither Render service is configured to deploy `aether-mvp-build` or `aether-india-admin-intelligence`. Do not claim the newly built administrative intelligence feature is live.
4. **Worker scheduling and credentials.** The scheduled worker requires the backend `AETHER_AUTOMATION_WORKER_TOKEN` and GitHub secrets `AETHER_AUTOMATION_WORKER_URL` plus matching `AETHER_AUTOMATION_WORKER_TOKEN`. GitHub scheduled workflows run only from the default branch; a workflow defined only on a non-default branch is not an active production scheduler. Actual worker execution must be verified.
5. **Live government integrations.** No connector may be treated as authorized without written authority, approved endpoint/credentials, authoritative effective-dated rules, sandbox certification and reconciliation against the government's system of record.

## Go/no-go gates

- [ ] Supabase project restored/active with billing implications understood; migrations, authentication, RLS and private storage re-verified.
- [ ] Render backend deployed from the approved release commit and health/readiness endpoints verified.
- [ ] Frontend deployed from the same release candidate and configured to the intended backend and auth mode; no server secrets in frontend assets.
- [ ] Latest backend tests, combined backend CI, frontend lint and frontend build pass on the exact release commit.
- [ ] Tenant-isolation, authentication, authorization, document encryption, retention/deletion and audit controls tested in staging.
- [ ] End-to-end staging scenarios cover intake, evidence, tenant isolation, queue/retry recovery, human approval, audit trail, exception handling and outcome reconciliation.
- [ ] Worker credentials and a live scheduler are verified, or worker execution is explicitly disabled and accurately disclosed.
- [ ] Rollback procedure and a known-good deployment are verified.
- [ ] Privacy notice, terms, accessibility, incident response and support ownership are ready.
- [ ] Every live government service independently passes legal authorization, source verification, connector certification and system-of-record reconciliation.

## Release policy

Do not merge to `main`, deploy publicly or announce production readiness merely because CI passes. First resolve the Supabase dependency, align the deployment branch, verify staging end to end, and confirm rollback. A controlled demo may be shared only if it is explicitly labelled synthetic and never presented as an official government workflow or outcome.
