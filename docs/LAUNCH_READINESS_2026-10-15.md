# Aether launch readiness checkpoint — 15 October 2026

**Decision at this checkpoint: NO-GO for announcing a public beta as live. GO for continued preparation and carefully labelled research outreach.**

This is a factual checklist, not a claim that all release gates have passed. The current target is a controlled synthetic demo, not live government execution.

## Verified

- [x] PR #9 remains open and in draft; no production merge was performed.
- [x] Latest reviewed PR head before this checkpoint had all three GitHub Actions workflows green: MVP CI, MVP tests, and frontend CI. Every subsequent source commit must be rechecked on its exact SHA before release.
- [x] Supabase project `aether` reports `ACTIVE_HEALTHY`.
- [x] Supabase security advisor returned no security lints at the time checked.
- [x] The queried application and internal tables had row-level security enabled. This does not prove tenant-isolation correctness; runtime integration tests remain necessary.
- [x] Netlify Forms processing is enabled on the existing Aether site.
- [x] A privacy-conscious, no-file-upload feedback form and confirmation page have been added to the release branch.
- [x] The app links to the feedback route from signed-in and signed-out views.
- [x] Public copy consistently describes the government connector as synthetic and does not claim measured real-world savings.
- [x] Netlify has the Supabase project URL configured for production, branch deploys, and deploy previews.
- [ ] The publishable browser-key mutation was acknowledged by the Netlify connector but is not visible in the environment listing; treat frontend Supabase configuration as unverified until a build proves it is available. No service-role key was added to the frontend.

## Hard blockers before calling this a live public beta

- [ ] Deploy the exact reviewed branch/commit to a controlled preview or release candidate and record the resulting deployment URL and commit.
- [ ] Confirm the publishable Supabase client key is available to the build and the deployed app loads without a client-side configuration exception.
- [ ] Confirm the current build contains `/feedback.html` and the confirmation page.
- [ ] Submit one clearly labelled test response and verify it appears in Netlify Forms; then remove or mark the test response appropriately.
- [ ] Run the synthetic end-to-end workflow, missing-document stop, retry/recovery, idempotency, and statutory-rejection tests against the exact release commit.
- [ ] Verify the Render production configuration and health/readiness endpoint. Do not expose credentials in logs or public documentation.
- [ ] Verify browser authentication mode matches the backend. The frontend currently derives its login gate from `VITE_REQUIRE_AUTH`; if absent, it defaults to no UI gate, while the documented production backend mode requires authenticated access. Confirm the actual deployment setting and test both signed-out and authorised flows before exposing API-backed actions.
- [ ] Exercise tenant isolation and API authorization with two distinct test tenants; confirm one cannot read or mutate the other's cases.
- [ ] Check API error handling, rate limiting, request IDs, CORS, secrets, storage, retention, and rollback on the deployed environment.
- [ ] Confirm the launch landing page states the synthetic-demo limitation, provides the feedback path, and avoids claims of government endorsement or production readiness.
- [ ] Assign an incident/feedback owner and a way to disable the demo quickly.

## Current hosting facts

- Public Netlify site: https://aether-govos.netlify.app
- The last confirmed published deployment is from 7 October 2026 on `main`, commit `ea264bef84095e8bb128cfabb3e88abc78ff8f60`. It is stale relative to this release branch.
- Therefore, do not advertise `https://aether-govos.netlify.app/feedback.html` as working until the new deployment and a real form submission are verified.
- Netlify build config publishes Vite's `dist` directory and runs `npm ci && npm run build`.
- Baseline browser security headers have been added to the branch's `netlify.toml`; they are not live until that branch/config is deployed.
- Supabase project status: `ACTIVE_HEALTHY`; 10 migrations are recorded.
- Security advisor: no security lints returned at the time checked. Performance advisor surfaced informational unused-index findings; do not remove indexes without workload evidence.

## Public-launch posture

### Safe to share now
- The GitHub repository and architecture for technical review.
- The synthetic workflow and fault-recovery test approach, clearly labelled as a prototype.
- Requests for workflow discovery interviews that explicitly ask people not to share confidential or personal records.
- Prepared launch copy, after manual review.

### Not safe to claim yet
- That the new hosted demo is live and tested.
- That feedback collection works end-to-end.
- That live government services are integrated.
- That Aether issues official approvals or certificates.
- That time, staffing, cost, or error reductions have been measured.
- That a government institution endorses or sponsors Aether.

## Go/no-go rule

A public beta announcement is **GO** only after the exact deployed commit passes the checklist above and the feedback form is tested. Until then, use “prototype / research preview” language and link directly to GitHub. Social posting remains subject to the founder's final approval.
