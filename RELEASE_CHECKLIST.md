# Aether GovOS MVP Release Checklist

## Software gate
- [x] Release-line backend compile/tests are green for the latest main commit.
- [x] Latest frontend typecheck/build is green.
- [x] All three Aether CI workflows pass on the current release line.
- [x] Case persistence and task checkpoint recovery tests pass.
- [x] API key tenant/scopes/revocation tests pass.
- [x] Document upload/download/hash integrity tests pass.
- [x] Notification and payment idempotency tests pass.
- [x] Durable worker case leases are implemented and tested.
- [x] Marketplace exposes all 34 MVP services as sandbox contracts.
- [x] Production execution fail-closes when live connectors/rules are absent.
- [x] Human authority and cross-tenant/department/jurisdiction authorization tests pass.

## Supabase gate
- [x] Latest Aether hardening migrations are applied to the connected project.
- [x] RLS is enabled on the exposed legacy application tables.
- [x] RLS is enabled on the `aether_internal` execution tables.
- [x] Browser roles are denied access to the private execution schema.
- [x] `public.aether_memberships` is server-controlled.
- [x] No critical Supabase security-advisor RLS finding remains.
- [x] Storage bucket `aether-documents` is private.

## Render gate
- [x] Render service points to the Aether GitHub main branch and final backend URL.
- [x] `/health` is configured as the Render health check.
- [x] `AETHER_ENABLE_LEGACY_API=false`.
- [x] Staging remains bounded to synthetic/non-authoritative execution.
- [x] Embedded durable worker runtime is deployed with exponential database-failure backoff.
- [ ] **Database authentication:** the Render service's existing database credential currently fails authentication against the Supabase pooler. The pooler hostname is reachable; the remaining issue is the database credential itself.

## Netlify gate
- [x] `VITE_API_URL` points to the Render backend.
- [x] `VITE_REQUIRE_AUTH=true`.
- [x] SPA fallback is active.
- [x] Published deploy corresponds to the current release line.

## Legal/connectivity gate
Aether's controlled MVP deliberately does not manufacture government authority.
- [ ] Each live government connector has written authorization and valid credentials.
- [ ] Each production service has authoritative, effective-dated rules.
- [ ] Required human/physical decision boundaries are confirmed by the responsible authority.
- [ ] Any statutory e-signature/certificate integration is legally valid and certified.

## Final controlled-MVP smoke test
After Render database authentication is corrected, run:

    AETHER_API_URL=https://aether-backend-9laf.onrender.com python scripts/release_smoke_test.py

Then execute:
- one controlled restaurant case;
- one generic service case;
- one document-upload/resume case;
- one human-approval case;
- audit-chain verification after each.

## Controlled MVP declaration
The software is ready for controlled/sandbox release once the Render database credential is corrected and the final deployed smoke tests pass.

This must remain distinct from live government production.

## Production-only prerequisites
Do not bypass these through feature flags:
- authorized government connector credentials and endpoint contracts;
- authoritative, effective-dated rules for every exposed service/jurisdiction;
- certified statutory e-signature/certificate/issuance integrations where legally required;
- production OCR, notification and payment provider configuration;
- full tenant/department/jurisdiction penetration testing;
- production load/chaos testing;
- final rollback validation.
