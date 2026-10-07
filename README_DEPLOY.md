# Aether GovOS — MVP Deployment

## Release posture

The connected public MVP is a controlled execution demo. It uses Supabase-backed persistence and authentication plus deterministic synthetic government connectors. It must not be described as live government connectivity.

Do not enable live government connectors until written authorization, credentials, endpoint contracts, idempotency behavior, and jurisdiction-specific rule evidence have been verified.

## Supabase

Apply the latest Aether hardening migration in `supabase/migrations/20261008000000_aether_mvp_hardening.sql` to an approved environment.

After application, verify:
- RLS is enabled on all legacy public application tables.
- Browser roles have no privileges on `aether_internal` execution tables.
- `public.aether_memberships` only permits users to read their own membership.
- the `aether-documents` storage bucket is private.
- the Supabase security advisor has no critical RLS findings.

Do not apply RLS remediation to a production project without explicitly reviewing the resulting policies and access impact.

## Render — controlled MVP

The Render service uses `backend/Dockerfile`.

Recommended MVP environment:

```env
AETHER_ENV=staging
AETHER_AUTH_MODE=supabase
DATABASE_URL=<server-side database URL>
SUPABASE_URL=<server-side Supabase URL>
SUPABASE_ANON_KEY=<server-side publishable/anon key>
SUPABASE_SERVICE_ROLE_KEY=<server-side only>
AETHER_ENCRYPTION_KEY=<server-side URL-safe base64 key>
AETHER_ENABLE_LEGACY_API=false
AETHER_ENABLE_PRODUCTION_CONNECTORS=false
```

This mode keeps the MVP usable while preventing accidental live-government execution.

After deployment, run `GET /health`, `GET /ready`, `GET /api/aether/v2/release/readiness`, and `scripts/release_smoke_test.py`.

## Netlify — frontend

Build command: `npm run build`

Publish directory: `dist`

Environment:

```env
VITE_API_URL=<public Render backend URL>
VITE_REQUIRE_AUTH=true
```

The SPA fallback is defined in `netlify.toml`.

## Production transition

Move Render to `AETHER_ENV=production` only when:
- the Supabase hardening migration is verified;
- production secrets are configured;
- private document storage is available;
- live government connectors are authorized and configured;
- authoritative, effective-dated rules cover the services being exposed;
- human/physical authority boundaries are validated by the responsible authority.

Production startup and execution intentionally fail closed when these dependencies are absent.

## Rollback

Restore the prior application commit, preserve compatible database migrations, inspect migration compatibility before rollback, and rerun health/readiness/smoke tests.

## Hard rule

Do not claim that Aether issues official government certificates, approvals, or decisions unless the relevant authority has actually authorized and integrated that capability.