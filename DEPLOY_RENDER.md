# Aether GovOS — Render Deployment and Controlled Staging

Aether's controlled MVP uses the existing Supabase project for persistence, Auth and private document storage; Render for the FastAPI execution API; and Netlify for the React Command Center.

## Deployment boundary

- Keep `main` release-only. Do not merge PR #11 until the staging gates pass.
- Use `aether-mvp-build` as the release-candidate source for staging.
- Keep government connectors disabled. The first release is a synthetic/sandbox GovOS, not a live government filing or approval service.
- Do not create a paid Render resource for the MVP. The current blueprint uses one Free web service with an embedded worker thread; do not create a separate background worker service.
- The Render Free plan may suspend idle services and is not a guarantee of always-on background processing. Clearly disclose that limitation in a controlled demo.

## Render web service

Use the existing Aether backend Docker configuration:

- Runtime: Docker
- Dockerfile: `backend/Dockerfile`
- Health check: `/health`
- Port: `8081`
- Embedded worker: `AETHER_EMBED_WORKER=true`
- Worker interval: `AETHER_WORKER_INTERVAL_SECONDS=5`
- Worker startup delay: `AETHER_WORKER_STARTUP_DELAY_SECONDS=8`

The embedded worker is deliberately selected to avoid requiring another Render service. It runs alongside the API process and processes durable cases/notification outbox work when the Free web instance is awake.

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

The readiness endpoint now rejects a staging/production database connection using the wrong database role. Do not use the Supabase postgres superuser as the Aether application's runtime identity.

## Netlify frontend

Build the React frontend from the same release candidate branch and set:

- `VITE_API_URL`: matching staging Render API base URL.
- `VITE_SUPABASE_URL`: existing Supabase project URL.
- `VITE_SUPABASE_ANON_KEY`: Supabase publishable/anon key only.
- `VITE_REQUIRE_AUTH=true`.

The current `netlify.toml` values point at the existing public backend and must be changed for a separate staging deployment. A publishable/anon key may be public; service-role keys, database passwords and encryption keys must never be in frontend variables.

## Release verification

1. Confirm `/health` returns HTTP 200.
2. Confirm `/ready` returns HTTP 200, database is ready, and the expected least-privilege role is valid.
3. Confirm the authenticated `/api/aether/v2/release/readiness` response reports `ready_for_controlled_mvp=true`.
4. Confirm connector mode is synthetic and legacy APIs are quarantined.
5. Create a read-only Aether API key with the required `cases:read` scope and store it as the GitHub Actions secret `AETHER_STAGING_API_KEY`.
6. Run GitHub Actions → **Aether Staging Release Smoke** on branch `aether-mvp-build`. Supply the staging API and frontend URLs.
7. The workflow checks API health/readiness, frontend response, service catalog, marketplace, connector catalog, rule readiness, India department/journey endpoints and controlled-MVP release readiness.

If `AETHER_STAGING_API_KEY` is absent, authenticated product/release checks are skipped and the workflow emits a warning. That run is not final launch approval.

## Rollback

Before any public cutover, record the currently live Render and Netlify commits. Roll back the backend and frontend to the known-good pair if smoke checks fail. Keep already-applied backward-compatible Supabase migrations in place; never roll back the database schema blindly.

## Production government integrations

Do not switch to production mode or enable real connectors merely because the application is healthy. Each live service separately requires written authority, approved endpoints/credentials, authoritative effective-dated rules, sandbox certification, human/statutory approval boundaries and reconciliation against the government's system of record.
