# Aether GovOS — Render Deployment and Controlled Staging

Aether's controlled MVP uses the existing Supabase project for persistence, Auth and private document storage; Render for the FastAPI execution API; and Netlify for the React Command Center.

## Deployment boundary

- The active candidate is PR [#20](https://github.com/amirmohd4/Aether/pull/20), branch `integration-check/public-preview-into-hardened`. Keep it in draft and do not merge until the release gates in `docs/RELEASE_READINESS.md` pass.
- Keep `main` release-only. Existing Render services still run older branches/commits; do not treat them as staging for PR #20.
- Keep government connectors disabled. The first release is a synthetic/sandbox GovOS, not a live government filing or approval service.
- Do not create paid infrastructure for the MVP. The candidate blueprint uses one Free web service with an embedded worker; do not create a separate background worker service unless the architecture and cost are explicitly reviewed.
- Render Free services may suspend while idle. They are not a guarantee of always-on background processing; disclose this limitation in demos.

## Render web service

Use the existing Aether backend Docker configuration:

- Runtime: Docker
- Dockerfile: `backend/Dockerfile`
- Health check: `/health`
- Port: `8081`
- Embedded worker: `AETHER_EMBED_WORKER=true`
- Worker interval: `AETHER_WORKER_INTERVAL_SECONDS=5`
- Worker startup delay: `AETHER_WORKER_STARTUP_DELAY_SECONDS=8`

The embedded worker runs alongside the API process and processes durable cases/notification-outbox work when the Free web instance is awake. A log line showing worker ticks is not proof that real work items are processed successfully.

## Required server-side environment

Set these in Render's environment settings. Never copy server secrets into Netlify or browser assets.

| Variable | Value / purpose |
|---|---|
| `AETHER_ENV` | `staging` |
| `AETHER_AUTH_MODE` | `supabase` |
| `AETHER_ENABLE_LEGACY_API` | `false` |
| `AETHER_ENABLE_PRODUCTION_CONNECTORS` | `false` |
| `AETHER_EMBED_WORKER` | `true` |
| `AETHER_WORKER_INTERVAL_SECONDS` | `5` |
| `AETHER_WORKER_STARTUP_DELAY_SECONDS` | `8` |
| `AETHER_DATABASE_ROLE_OVERRIDE` | `aether_runtime` |
| `AETHER_DATABASE_EXPECTED_ROLE` | `aether_runtime` |
| `AETHER_DATABASE_PASSWORD` | Secret password assigned to the Supabase `aether_runtime` role |
| `DATABASE_URL` | PostgreSQL pooler URL for the existing Supabase project; retain the correct pooler port and database name |
| `AETHER_DATABASE_HOST_OVERRIDE` | Existing project's Supabase pooler host in `ap-northeast-1` |
| `SUPABASE_URL` | Existing Supabase project URL |
| `SUPABASE_ANON_KEY` | Supabase publishable/anon key, server-side for Auth validation |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-only Supabase service-role key |
| `AETHER_ENCRYPTION_KEY` | Valid Fernet key, unique to this environment |
| `AETHER_DOCUMENT_BUCKET` | `aether-documents` |
| `AETHER_CORS_ORIGINS` | Exact staging frontend origin |
| `PORT` | `8081` |

### Database least-privilege setup

The existing Supabase migrations create the login role `aether_runtime`; the role password is intentionally not committed to Git.

1. In the Supabase SQL editor, assign a strong unique password to the role using your password manager:
   `ALTER ROLE aether_runtime WITH PASSWORD '<your-strong-unique-password>';`
2. Store that same password as the Render secret `AETHER_DATABASE_PASSWORD`.
3. Keep `AETHER_DATABASE_ROLE_OVERRIDE=aether_runtime` and `AETHER_DATABASE_EXPECTED_ROLE=aether_runtime`.
4. Set `DATABASE_URL` to the project's Supabase PostgreSQL pooler endpoint and correct pooler port. The application applies the configured host, role and password overrides.
5. Verify the deployed `/ready` response. It must return HTTP 200 and `database_role_valid: true`.

The readiness endpoint rejects a staging/production database connection using the wrong database role. Do not use the Supabase postgres superuser as the Aether application's runtime identity.

## Netlify frontend

Build the React frontend from the same release candidate and set:

- `VITE_API_URL`: matching staging Render API base URL.
- `VITE_SUPABASE_URL`: existing Supabase project URL.
- `VITE_SUPABASE_ANON_KEY`: Supabase publishable/anon key only.
- `VITE_REQUIRE_AUTH=true` for the authenticated staging environment.

The current `netlify.toml` has separate production and deploy-preview API settings. Confirm the preview's API target and matching backend CORS allowlist before claiming the deployed frontend/backend pair works. A publishable/anon key may be public; service-role keys, database passwords and encryption keys must never be in frontend variables.

## Staging verification

1. Deploy the candidate to an isolated staging API and matching frontend. Do not repoint the existing production or public-demo service, and do not use a shared production database for test writes.
2. Confirm API `/health` returns HTTP 200.
3. Confirm `/ready` returns HTTP 200, database is ready, and `database_role_valid=true`.
4. Confirm authenticated `/api/aether/v2/release/readiness` reports `ready_for_controlled_mvp=true`.
5. Confirm connector mode is synthetic and legacy APIs are quarantined.
6. Set GitHub repository variables `AETHER_STAGING_API_URL` and `AETHER_STAGING_FRONTEND_URL`.
7. Create a read-only Aether API key with `cases:read` scope and store it as GitHub Actions secret `AETHER_STAGING_API_KEY`.
8. Run `.github/workflows/aether-staging-smoke.yml`. A skipped job or a notice-only run is not a passing staging test.
9. Exercise document upload/read, tenant isolation, worker dispatch/recovery/retries, feedback submission and full synthetic citizen/business plus operator journeys.
10. Record monitoring, privacy/accessibility checks and a successful rollback rehearsal.

If `AETHER_STAGING_API_KEY` is absent, authenticated product/release checks are not completed. That run is not final launch approval.

## Rollback

Before any public cutover, record the currently live Render and Netlify commits. Roll back the backend and frontend to the known-good pair if smoke checks fail. Keep already-applied backward-compatible Supabase migrations in place; never roll back the database schema blindly.

## Production government integrations

Do not switch to production mode or enable real connectors merely because the application is healthy. Each live service separately requires written authority, approved endpoints/credentials, authoritative effective-dated rules, sandbox certification, human/statutory approval boundaries and reconciliation against the government's system of record.
