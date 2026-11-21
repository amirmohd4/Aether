# Aether Release Readiness

Last checked: 2026-11-21.

## Release decision

**NO-GO for public production launch. CONDITIONAL GO for a tightly controlled synthetic pilot once browser acceptance, deployed write-path tests, operational ownership and privacy/terms are completed.**

The current candidate is `aether-mvp-build` at `66393d61509b3df201a248c9c1ae29eb6ed066b6`. PR [#11](https://github.com/amirmohd4/Aether/pull/11) promotes this candidate to `main`; it remains open and unmerged. The candidate contains 88 commits relative to `main` and changes 58 files. Production must not be updated by an unreviewed merge simply because CI is green.

Aether's initial release is a synthetic government research/pilot environment. It does not submit official government applications, access private government records, issue certificates, or make statutory decisions. Live integrations require written authorization, approved credentials/endpoints, authoritative effective-dated rules, certification where required, and system-of-record reconciliation.

## Current verified state

### Repository and CI

- Candidate: `aether-mvp-build`, commit `66393d61509b3df201a248c9c1ae29eb6ed066b6`.
- Aether MVP CI: passed on the current candidate; backend and frontend jobs succeeded.
- Aether MVP Tests: passed on the current candidate; **154 backend tests passed**.
- Aether MVP Frontend: passed on the current candidate.
- Aether Staging Release Smoke: passed on the current PR candidate, but remains a read-only smoke.
- Aether Staging Release Smoke: passed on PR #11 merge ref `41cde4f43f4dfe3ef7a85d16c2363840a39034e2`.
- Netlify candidate deploy preview #11: `ready` for candidate commit `66393d61509b3df201a248c9c1ae29eb6ed066b6`; preview is configured for the authenticated staging API (`VITE_REQUIRE_AUTH=true`).
- The authenticated smoke used a read-only API key. It passed eight read/readiness product checks: service catalog, marketplace, connector catalog, rule readiness, India admin overview, departments, journey templates and release readiness. Public health/readiness/root checks also returned HTTP 200.
- The smoke asserted `/ready` reports database ready and `database_role_valid=true`.
- The candidate Netlify preview is now configured to use `https://aether-staging.onrender.com` and require Supabase authentication; the staging CORS allowlist was updated to include preview #11, and that Render redeploy completed successfully. This wiring has not yet been tested in a real browser. Staging still runs the older `integration-check/public-preview-into-hardened` commit, not the candidate backend.
- The smoke did not create a case, upload/retrieve a document, approve/reject a human task, or verify a full user journey.

### Supabase

The connected project is `aether`, ref `lekudqjewxxunqjuqayi`, status `ACTIVE_HEALTHY`.

Fresh database inspection on 2026-11-21 confirmed:
- Ten applied migrations.
- Thirteen public application tables and ten `aether_internal` tables.
- RLS enabled on all 23 application tables.
- `aether_runtime` exists, can log in, is not a superuser, and cannot create databases or roles.
- `aether-documents` exists and is private; its bucket limit is now 15 MiB and its MIME allowlist matches the application upload allowlist (PDF, plain text, CSV, JSON, JPEG, PNG and DOCX).
- The `aether_runtime` database role has `rolbypassrls=false`; browser roles have no broad direct access to application records.
- Security Advisor returned no lints. Performance Advisor reported 38 unused-index informational findings; these were not changed because usage may be low on the current staging project.
- Cross-tenant admin access was found in candidate code and fixed: `admin` is now tenant-scoped for both case detail access and case listing. New tests cover cross-tenant denial, tenant-scoped admin listing and tenantless-admin denial; the 154-test suite passed.

These checks do not prove the deployed application can perform private storage operations, encryption, or tenant-scoped document access.

### Render

Three services are present:

- `aether-staging`: separate staging service, branch `integration-check/public-preview-into-hardened`; latest observed live deploy commit `a8b4b8eb9c85b82fd84fac05de6dc28dac33cf25`. Candidate and staging branches have diverged: candidate is 24 commits ahead and 17 behind the deployed branch. Do not switch the service branch until all 17 staging-only commits and candidate changes are reconciled.
- `aether-backend`: production backend still deploys from `main`, latest observed live commit `f64148aad10a5f8f586efde0cefe7a817fe6d996`. It has not been promoted to the candidate.
- `aether-public-demo`: public demo service on its separate older branch.

The staging worker logs show periodic ticks with `processed=0` and zero notification activity in the sampled window. This proves the worker loop is running, not that a durable task was processed, retried, recovered or delivered.

The Render connector does not expose environment-variable values. The database identity was indirectly verified by the successful staging `/ready` check, but the deployed Auth, storage service credentials, encryption key, worker behavior and other environment settings have not all been proven.

### Netlify

- Candidate preview #11 is marked `ready` for `66393d61509b3df201a248c9c1ae29eb6ed066b6`: [open preview](https://deploy-preview-11--aether-govos.netlify.app/).
- The production Netlify site's current published deploy remains the older deploy; the candidate preview is not production.
- The current preview's browser login and API wiring have not been tested in a real browser.

## Remaining release gates

1. **Candidate browser acceptance:** test preview #11 on mobile/desktop; login/signup, session persistence, tenant selection, sign-out, navigation, forms, uploads, error states and API wiring.
2. **Deployed write-path E2E:** use a dedicated staging test account to create a synthetic case, submit evidence, upload/read a private document, resume execution, complete officer approval/rejection, inspect notifications and verify audit integrity.
3. **Authorization/security:** unit-level candidate tests now prove tenant-admin isolation and officer department/jurisdiction filtering; still test these controls against deployed Supabase Auth and staging data, plus API key scope/expiry/revocation, file abuse limits and secret exposure.
4. **Storage/encryption:** prove deployed Supabase Storage upload/read/delete using server-only credentials; verify encrypted extracted text at rest and tenant-specific access.
5. **Worker/reliability:** create durable synthetic work and prove processing, bounded retries, lease expiry, restart recovery and notification outbox delivery. Ticks alone are insufficient.
6. **Availability:** test cold start, health monitoring, backup/restore, rollback and bounded load. Current Render services are on Free plans; cold starts/suspension make them unsuitable for an availability guarantee. No paid upgrade has been authorized.
7. **Legal/privacy/compliance:** publish reviewed privacy notice, terms, retention/deletion and consent language; identify legal entity, controller/processor roles and support/incident contacts; obtain qualified review of applicable Indian requirements and pilot institution approval.
8. **Pilot operations:** define one workflow/jurisdiction, invited users, owner/support owner, data boundaries, success metrics, incident process and exit criteria.

## Required deployment boundary

Do not repoint production Render service `aether-backend` or publish the candidate Netlify build as production until the release gates pass. Keep production `main` unchanged until the candidate's complete diff is reviewed and the release owner approves the exact deployment.

Keep `AETHER_ENABLE_PRODUCTION_CONNECTORS=false`. Do not use real citizen documents or claim official government authority in a synthetic pilot.

## Go/no-go

- **Internal development:** GO.
- **Controlled synthetic staging:** GO for supervised technical testing; read-only staging smoke has passed.
- **Invited synthetic pilot:** conditional; complete browser acceptance, write-path E2E, operational ownership and privacy/terms first.
- **Public production:** NO-GO.
- **Live government execution:** NO-GO until authorization, credentials, authoritative rules, certification and reconciliation are independently satisfied.
