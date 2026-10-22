# Aether Release Readiness

Last checked: 2026-10-22 (UTC)

## Current decision

**Controlled/sandbox MVP: code candidate; production release: blocked pending environment validation.**

The active development branch is `aether-mvp-build`. Pull request #11 targets `main` and remains open/unmerged. Production government actions remain fail-closed. Aether's synthetic scenarios and internal work-item completion are not official government outcomes.

## Verified repository state

- The backend test, backend CI, frontend CI, and administrative-worker workflows passed for commit `63dd2c7dc2de08f2c51b7324fe193b369a305614`.
- A separation-of-duties hardening change was added after that validated commit: enqueue now rejects a sensitive action when its requester and pre-approver are the same actor, with a regression test.
- The latest commit containing that change is `c218e9968fa88d07bd4a5b41ab096fe69594a58e`. Its CI checks must complete successfully before the new change is considered validated.
- A Vercel preview deployment was reported successful for one preview context; another Vercel deployment was still pending at the time of this check. Preview success does not establish production readiness.
- Netlify's `aether-govos` site reports a published deploy in the ready state. This does not verify the live backend/database dependency chain.

## Environment blockers

1. **Supabase:** the connected project `aether` (`lekudqjewxxunqjuqayi`) reports `INACTIVE`. Listing migrations timed out. Database readiness, auth, RLS, private document storage, and migrations therefore cannot currently be re-verified against the live project.
2. **Render:** service status and configuration have not been verified in this session because the Render connector requires explicit workspace selection. Do not infer that the backend is healthy from repository CI.
3. **Production Vercel status:** the latest recorded status for the `main` commit reports deployment rate-limited. A new preview deployment is not a substitute for a verified production deployment.
4. **Worker scheduling:** the worker workflow needs backend `AETHER_AUTOMATION_WORKER_TOKEN` and GitHub secrets `AETHER_AUTOMATION_WORKER_URL` plus matching `AETHER_AUTOMATION_WORKER_TOKEN`. GitHub scheduled workflows run only from the default branch, so a schedule defined only on the build branch is not an active recurring production scheduler.
5. **Live government integrations:** no production connector may be treated as authorized without written authority, approved endpoint/credentials, authoritative effective-dated rules, sandbox certification, and reconciliation against the government's system of record.

## Go/no-go gates

- [ ] Latest backend tests and backend CI pass for the current head.
- [ ] Latest frontend lint/build passes for the current head.
- [ ] Render workspace/service is confirmed; deployed backend health and readiness are checked.
- [ ] Supabase project is active; migration state, auth, RLS, and private storage are verified.
- [ ] Frontend points to the intended backend URL and auth mode; no server secrets are bundled into frontend assets.
- [ ] End-to-end staging test covers intake, document evidence, tenant isolation, queue/retry recovery, human approval, audit trail, and failure handling.
- [ ] Worker credentials and an actually active scheduler are verified, or the worker is explicitly disabled.
- [ ] Rollback procedure and a known-good deployment are verified.
- [ ] Any live government service separately passes its authorization and source-of-truth reconciliation gates.

## Release policy

Do not merge or deploy to production merely because CI passes. First resolve the environment blockers, verify staging, and confirm rollback. If a controlled demo is launched before government integrations are authorized, label it clearly as a synthetic sandbox and never represent its outputs as official records.
