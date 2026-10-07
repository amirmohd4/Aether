# Aether GovOS MVP Release Checklist

## Software gate
- [ ] Latest `aether-mvp-build` branch has green backend compile/tests.
- [ ] Latest frontend typecheck/build is green.
- [ ] CI/security workflow is green for the exact release commit.
- [ ] Case persistence and task checkpoint recovery pass.
- [ ] API key tenant/scopes/revocation tests pass.
- [ ] Document upload/download/hash integrity tests pass.
- [ ] Notification and payment idempotency tests pass.
- [ ] Human authority and cross-tenant/department/jurisdiction authorization tests pass.

## Supabase gate
- [ ] Apply the latest idempotent Aether hardening migration.
- [ ] Verify RLS enabled on all exposed legacy tables.
- [ ] Verify RLS enabled on all `aether_internal` execution tables.
- [ ] Verify browser roles cannot read/write the private execution schema.
- [ ] Verify `public.aether_memberships` only exposes each user's own membership.
- [ ] Verify no critical security advisor findings remain.
- [ ] Verify storage bucket `aether-documents` is private.

## Render gate
- [ ] Configure `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and server-only `SUPABASE_SERVICE_ROLE_KEY`.
- [ ] Configure `AETHER_ENCRYPTION_KEY` as a 128/192/256-bit URL-safe base64 key.
- [ ] Keep `AETHER_ENABLE_LEGACY_API=false`.
- [ ] Staging/MVP: keep synthetic connectors explicitly enabled by environment intent.
- [ ] Production: set `AETHER_ENV=production` only after live connectors and authoritative rules are verified.
- [ ] Verify `/health` and `/ready`.

## Netlify gate
- [ ] `VITE_API_URL` points to the final Render backend.
- [ ] `VITE_REQUIRE_AUTH=true` for authenticated MVP/workspace use.
- [ ] SPA fallback is active.
- [ ] Published deploy corresponds to the release commit.

## Legal/connectivity gate
Aether's software cannot manufacture government authority. Before live production execution:
- [ ] Each government connector has written authorization and valid credentials.
- [ ] Each target service has authoritative, effective-dated rules.
- [ ] Required human/physical decision boundaries are confirmed by the responsible authority.
- [ ] Any statutory e-signature/certificate integration is legally valid and certified.

## Smoke test
Run:

    AETHER_API_URL=https://<render-host> python scripts/release_smoke_test.py

Then execute one controlled restaurant case, one generic service case, one document-upload/resume case, and one human-approval case. Verify the audit chain after each.