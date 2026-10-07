# Aether MVP — Release Deployment

Deployment is intentionally a single coordinated release, not a per-change workflow.

## Before release

The aether-mvp-build branch must pass backend compile/tests, frontend lint/build, persistence/recovery, queue lease/idempotency, authentication/RBAC/tenant isolation, Supabase RLS/security review, connector contract tests, core customer journeys, and release smoke tests.

Do not merge to main until these are green.

## Supabase

Apply the migrations in supabase/migrations/.

Verify migration success, RLS on exposed tables, no public access to internal execution tables, membership policies, no sensitive secrets in browser configuration, and no unresolved critical Supabase security findings.

## Render

The connected Render backend service is aether-backend. It uses backend/Dockerfile and the main branch for release.

Required server-side configuration:

```env
AETHER_ENV=production
AETHER_AUTH_MODE=supabase
DATABASE_URL=<server-side database URL>
SUPABASE_URL=<server-side Supabase URL>
SUPABASE_SERVICE_ROLE_KEY=<server-side only>
AETHER_ENABLE_PRODUCTION_CONNECTORS=false
```

Enable real connectors only after their authorization, endpoint, authentication and idempotency behavior have been verified.

After deployment, verify GET /health, GET /api/aether/v2/services, GET /api/aether/v2/connectors and GET /api/aether/v2/rules, then run a controlled end-to-end case and verify persistence, audit integrity and human-authority behavior.

## Netlify

The connected Netlify site is aether-govos.

Set:

```env
VITE_API_URL=<public Render backend URL>
VITE_REQUIRE_AUTH=true
```

Publish the build generated from the final release commit only.

## Rollback

Stop further deployment, restore the previous application commit, preserve compatible data migrations, inspect Supabase migration compatibility before any rollback, and re-run health and smoke tests.

## Hard rule

Do not describe the demo as live government connectivity or claim that it issues official government documents unless the relevant government system has actually authorized and completed that integration.

