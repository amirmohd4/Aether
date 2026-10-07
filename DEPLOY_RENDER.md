# Aether GovOS — Render Deployment

This repository deploys the Aether backend as a Render Docker web service and a separate durable worker. Supabase provides the production database/auth/storage boundary, and Netlify serves the frontend.

## Controlled MVP

Use the staging posture until live government integrations are explicitly authorized:

```env
AETHER_ENV=staging
AETHER_AUTH_MODE=supabase
AETHER_ENABLE_LEGACY_API=false
AETHER_ENABLE_PRODUCTION_CONNECTORS=false
DATABASE_URL=<Supabase/Postgres connection string>
SUPABASE_URL=<Supabase project URL>
SUPABASE_ANON_KEY=<server-side Supabase publishable/anon key>
SUPABASE_SERVICE_ROLE_KEY=<server-only service role key>
AETHER_ENCRYPTION_KEY=<Fernet key generated for this environment>
AETHER_DOCUMENT_BUCKET=aether-documents
```

The web service starts from `backend/Dockerfile`. The worker uses:

```
python backend/worker.py
```

The worker is responsible for durable case recovery and notification-outbox dispatch. Never run a second worker against the same production database without the durable case-lease mechanism enabled.

## Render services

Create two services from the repository:

1. Web service: Docker, `backend/Dockerfile`
2. Background worker: Docker, `backend/Dockerfile`, command `python backend/worker.py`

The included `render.yaml` contains the intended service definitions. Keep the backend and worker in the same region as the Supabase/Postgres endpoint where practical.

## Required environment

The web service and worker both need the server-side database and Supabase credentials. Never expose `SUPABASE_SERVICE_ROLE_KEY` or `AETHER_ENCRYPTION_KEY` to the frontend.

For notifications, configure an approved delivery adapter such as:

```env
AETHER_NOTIFICATION_WEBHOOK_URL=<approved webhook endpoint>
AETHER_NOTIFICATION_WEBHOOK_SECRET=<signing secret>
```

For live external payments, configure:

```env
AETHER_PAYMENT_PROVIDER_URL=<approved payment adapter>
AETHER_PAYMENT_PROVIDER_TOKEN=<server-only token>
```

For OCR beyond native text/PDF extraction:

```env
AETHER_OCR_BASE_URL=<approved OCR endpoint>
AETHER_OCR_TOKEN=<server-only token>
```

## Supabase release sequence

Apply the ordered SQL files under `supabase/migrations/`. The latest migrations are idempotent and include:

- private execution persistence;
- task checkpoints and durable case leases;
- encrypted-document metadata boundary;
- notification/payment/API-key ledgers;
- deny-by-default browser access to private execution tables;
- server-controlled tenant membership;
- legacy public-table browser lockdown.

After migration, verify the `aether-documents` storage bucket is private.

## Verification

After Render is live:

```bash
AETHER_API_URL=https://<render-host> python scripts/release_smoke_test.py
```

With Supabase authentication:

```bash
AETHER_API_URL=https://<render-host> \
AETHER_API_TOKEN=<short-lived-supabase-access-token> \
python scripts/release_smoke_test.py
```

The smoke test covers health, readiness, service catalog, marketplace, connector catalog, rule readiness and release readiness.

## Production transition

Do not switch `AETHER_ENV=production` merely because Render is healthy. Production execution is intentionally fail-closed until:

- authorized government connector credentials and endpoint contracts exist;
- authoritative, effective-dated rules cover the intended launch jurisdictions/services;
- legally valid human-signature/certificate integration is certified where required;
- production OCR/notification/payment providers are configured;
- Supabase RLS/security checks pass;
- the final Netlify frontend points at the final Render backend.

The synthetic government environment remains available for controlled demonstrations only.

## Rollback

Rollback the application to the previous known-good commit, leave already-applied compatible database migrations in place, verify schema compatibility, then rerun `/health`, `/ready` and the smoke test before reopening traffic.

## What not to do

Do not use the old mock-data deployment commands or treat synthetic connectors as real government connectivity. Do not place production secrets in frontend code. Do not claim Aether itself has statutory authority to issue government decisions.
