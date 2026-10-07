# Aether GovOS MVP Release Checklist

## Controlled-MVP software gate
- [x] Release-line backend compile/tests are green on the final release line.
- [x] Frontend typecheck/build is green.
- [x] All Aether CI workflows pass on the final release line.
- [x] Deployed smoke workflow passes against the public Render API and Netlify frontend.
- [x] Case persistence and task checkpoint recovery tests pass.
- [x] API key tenant/scopes/revocation tests pass.
- [x] Document upload/download/hash integrity tests pass.
- [x] Notification and payment idempotency tests pass.
- [x] Durable worker case leases are implemented, tested and running.
- [x] Marketplace exposes all 34 MVP services as sandbox contracts.
- [x] Production execution fail-closes when live connectors/rules are absent.
- [x] Human authority and cross-tenant/department/jurisdiction authorization tests pass.

## Supabase gate
- [x] Aether persistence and operational migrations are applied.
- [x] Dedicated `aether_runtime` database role is configured for the deployed API/worker.
- [x] Runtime DDL is disabled on managed PostgreSQL; schema is migration-managed.
- [x] RLS is enabled on exposed legacy application tables.
- [x] RLS is enabled on the `aether_internal` execution tables.
- [x] The `aether_runtime` role has explicit server-only RLS policies for internal execution tables.
- [x] `public.aether_memberships` has explicit server-only runtime access while browser access remains owner-scoped.
- [x] Supabase security advisor returns no security lints.
- [x] Temporary database-credential bootstrap storage has been removed.
- [x] Storage bucket `aether-documents` is private.

## Render gate
- [x] Render service points to Aether main and the final backend URL.
- [x] `/health` is configured as the Render health check.
- [x] `/ready` now fails closed with HTTP 503 when the database is unavailable.
- [x] `AETHER_ENABLE_LEGACY_API=false`.
- [x] Staging remains bounded to synthetic/non-authoritative execution.
- [x] Embedded durable worker runtime is deployed with exponential database-failure backoff.
- [x] Render connects to Supabase successfully with the dedicated Aether runtime identity.
- [x] Worker ticks successfully against the deployed Supabase schema.

## Netlify gate
- [x] `VITE_API_URL` points to the Render backend.
- [x] `VITE_REQUIRE_AUTH=true`.
- [x] SPA fallback is active.
- [x] Published frontend returns HTTP 200 in deployed smoke testing.

## Final controlled-MVP smoke
The automated deployed smoke test verifies:
- Render `/health` responds 200;
- Render `/ready` reports database ready;
- Render root endpoint responds correctly;
- Netlify frontend responds 200 and contains valid HTML.

The broader authenticated smoke script also supports service catalog, marketplace, connectors, rules and release-readiness checks when an authorized bearer token or Aether API key is provided.

## Legal/connectivity boundary
The controlled MVP deliberately does not manufacture government authority.
- [ ] Each live government connector has written authorization and valid credentials.
- [ ] Each production service has authoritative, effective-dated rules.
- [ ] Required human/physical decision boundaries are confirmed by the responsible authority.
- [ ] Any statutory e-signature/certificate integration is legally valid and certified.

These are production-launch prerequisites, not missing controlled-MVP software.

## Production-only prerequisites
Do not bypass these through feature flags:
- authorized government connector credentials and endpoint contracts;
- authoritative, effective-dated rules for every exposed service/jurisdiction;
- certified statutory e-signature/certificate/issuance integrations where legally required;
- production OCR, notification and payment provider configuration;
- tenant/department/jurisdiction penetration testing;
- production load/chaos testing;
- final rollback validation.

## Controlled MVP declaration

**Controlled/sandbox MVP: COMPLETE.**

The Aether software backbone, persistent execution infrastructure, security boundary, worker runtime, unified Command Center, CI and deployed Render/Netlify path have passed the controlled release gate.

This declaration is intentionally distinct from live government production authority.
