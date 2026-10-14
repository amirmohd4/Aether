# Aether launch readiness — 16 October 2026

**Decision at this checkpoint: NOT YET CLEARED for a broad public sandbox launch.** A research/demo preview and expert outreach are appropriate; the updated web experience must be deployed and smoke-tested before it is advertised as a usable beta.

This is an evidence-based checkpoint, not a claim that the whole product is production-ready.

## Verified

- The latest inspected feature branch is `pilot/jk-cross-agency-execution`; PR [#9](https://github.com/amirmohd4/Aether/pull/9) remains open and draft. Do not merge it to the release branch without final review.
- GitHub Actions passed on commit `bc43aa31d1ecb921ea9c45b5a184aba97c007153` for frontend, MVP CI, and backend tests. Later commits add the public feedback pages, visible feedback links, and branding metadata; CI for those later commits must be checked before release.
- The currently published Netlify deploy is [`6ac6804b9630c700081688cf`](https://6ac6804b9630c700081688cf--aether-govos.netlify.app), from `main` commit `ea264bef84095e8bb128cfabb3e88abc78ff8f60`, published 7 October 2026. It is older than the feature branch and is **not proof that the new feedback experience is live**.
- Netlify form processing is now enabled for the site. A static form at `public/feedback.html` and a confirmation page at `public/feedback-thanks.html` have been added on the feature branch. The form must be registered by a deploy and a real test submission must be confirmed before launch. Do not assume enabling form processing alone makes the form live.
- The React command center now links to feedback in both the signed-out and signed-in views. The HTML page title and description now use Aether branding instead of the previous placeholder title.
- Supabase project `aether` is active/healthy. Ten `aether_internal` tables and the listed `public` tables have RLS enabled. Internal tables have policies scoped to `aether_runtime`; legacy tables have deny-browser policies for `anon` and `authenticated`; memberships permit authenticated users to read their own membership. The Supabase security advisor returned no lints at the time checked.
- Supabase performance advisor reported 38 unused-index notices. These are informational; do not drop indexes before understanding workload and query patterns.
- The synthetic test suite and launch copy explicitly distinguish simulation from live government execution. No measured real-world savings, live government integration, paying customer, or institutional sponsor has been established.

## Required before announcing a usable public sandbox

1. Check that CI passes on the exact final branch head after the feedback and metadata commits.
2. Verify the correct Render workspace and inspect the backend service, deploy state, environment configuration (without exposing secrets), health endpoint, and logs. Do not deploy into an unconfirmed workspace.
3. Publish the updated frontend to a controlled preview or explicitly approved release deploy; obtain the actual URL from the platform rather than guessing a branch URL.
4. Test the deployed home page, sign-in/unauthenticated view, synthetic workflow, failure/rejection behavior, feedback page, feedback submission, confirmation page, mobile layout, and error handling.
5. Confirm the feedback form is registered in Netlify and the test submission is visible to the intended owner; set up submission notifications and retention/access ownership.
6. Run backend release smoke tests against the deployed environment. Confirm production remains fail-closed and live connectors remain disabled.
7. Review auth, tenant/role boundaries, CORS, rate limiting/abuse handling, logs, secrets, privacy wording, incident contact, rollback and backups.
8. Reconcile the release branch with the reviewed candidate and verify the final deploy points to the exact intended commit. Do not publish social launch copy before these checks pass.

## Safe public claims

Aether is a prototype execution/orchestration layer for complex workflows. The current demo uses simulated government systems and synthetic data. It does not submit real government applications, access protected government records, issue official decisions or certificates, or prove real-world time savings.

## Still outside this launch

- Authorised live government integrations, contracts and credentials
- Effective-dated authoritative rule packs and certified statutory signature/issuance paths
- Production provider credentials for OCR, notifications and payments
- Independently measured pilot outcomes and customer willingness-to-pay evidence
- Broad service-by-service mapping and systematic stakeholder interviews

## Links

- [Repository](https://github.com/amirmohd4/Aether)
- [Draft PR #9](https://github.com/amirmohd4/Aether/pull/9)
- [Public beta launch kit](https://github.com/amirmohd4/Aether/blob/pilot/jk-cross-agency-execution/docs/PUBLIC_BETA_LAUNCH_KIT.md)
- [Global institutional problem evidence](https://github.com/amirmohd4/Aether/blob/pilot/jk-cross-agency-execution/docs/GLOBAL_PROBLEM_EVIDENCE.md)
