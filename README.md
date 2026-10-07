# Aether GovOS

Aether is a government execution layer. It takes a real-world objective, understands the requested service, discovers requirements, builds a cross-department work graph, executes independent digital work in parallel, verifies results, stops at legally required human actions, and resumes until the outcome is complete.

**Core product:** Aether automates the work between a government application and the government decision/outcome.

## Current MVP

- 34 services in the shared service registry
- Objective understanding with ranked service candidates
- Requirement discovery with jurisdiction/source provenance
- Reusable cross-department work graphs
- Parallel dependency-aware execution
- Synthetic Government Environment with deterministic responses
- Document inspection and evidence extraction
- Verification, reconciliation, exceptions and risk findings
- Human authority and physical-action boundaries
- Durable PostgreSQL/SQLite case, queue and event persistence
- Resumable cases and incremental document submission
- Tamper-evident execution audit chain
- Server-controlled tenant membership and role boundaries
- Private usage metering for case/outcome billing foundations
- Opt-in authorized REST connectors for real integrations
- Unified Aether Command Center
- Backend and frontend CI workflows

The synthetic government system is a demo environment. It does not issue official government documents and it does not represent live government connectivity.

## Architecture

```text
Objective
  ↓
Objective Understanding
  ↓
Requirements + Rule Evidence
  ↓
Case Engine
  ↓
Government Ontology / Work Graph
  ↓
Dependency + Queue Engine
  ↓
Department Workers / Connectors
  ↓
Observe → Verify → Reconcile
  ↓
Human Authority / Physical Action
  ↓
Outcome + Evidence + Audit
  ↓
Usage / Measurement
```

The government remains the system of record. Aether is the intelligence, orchestration and execution layer.

## Local development

### Frontend

```bash
npm ci
npm run dev
```

Environment:

```env
VITE_API_URL=http://localhost:8081
VITE_REQUIRE_AUTH=false
```

### Backend

```bash
cd backend
pip install -r requirements.txt
AETHER_ENV=development AETHER_AUTH_MODE=none uvicorn main:app --host 0.0.0.0 --port 8081
```

Use SQLite locally unless DATABASE_URL is explicitly set.

## Release configuration

```env
AETHER_ENV=production
AETHER_AUTH_MODE=supabase
DATABASE_URL=<server-side database URL>
SUPABASE_URL=<server-side Supabase URL>
SUPABASE_SERVICE_ROLE_KEY=<server-side only>
VITE_API_URL=<public Render backend URL>
VITE_REQUIRE_AUTH=true
AETHER_ENABLE_PRODUCTION_CONNECTORS=false
```

Production authentication fails closed when authentication is not configured.

Real government connectors are enabled only by explicit server-side configuration. Credentials must never be placed in frontend code.

## Deployment policy

During MVP construction, development work stays on aether-mvp-build and main is release-only.

Do not deploy every small change. Before release, run the complete test/security/persistence gate. Then merge the final MVP to main, apply Supabase migrations, deploy the Render backend, publish the final Netlify frontend, run smoke tests, and keep a rollback path.

See MVP_MASTER_PLAN.md and SECURITY_RELEASE_PLAN.md for the release gate.

## Truthful MVP status

This repository is not yet a production government integration. Real government access, service certification, production document storage/OCR, broad legal-rule coverage, distributed worker operations, payments/fees, notifications, marketplace and full production E2E testing are still release work.

