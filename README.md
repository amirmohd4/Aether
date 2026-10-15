# Aether GovOS

Aether GovOS is an early-stage government-workflow orchestration prototype. It explores how an outcome-first interface could map requirements, coordinate permitted digital tasks, recover from exceptions, verify results, and stop at legally required human actions. The public research preview uses synthetic systems only.

**Product hypothesis:** Aether could coordinate the work between a service request and its eventual official outcome, while the responsible authority remains the system of record and decision-maker.

## Public research preview

- **[Open the interactive synthetic preview](https://deploy-preview-10--aether-govos.netlify.app/)**
- [Share feedback](https://deploy-preview-10--aether-govos.netlify.app/feedback.html)
- [Launch-readiness checklist](docs/launch-readiness-checklist.md)
- [Global mock-preview plan](docs/global-mock-preview-plan.md)

Use fictional values only. The preview demonstrates workflow patterns; it does not contact government systems, submit official applications, issue records, or make legal decisions. Feedback submissions are registered by Netlify Forms, but end-to-end delivery has not yet been verified.

## Current MVP

- 32 public mock services in the user-facing service catalogue
- Objective understanding with ranked service candidates
- Requirement discovery with jurisdiction/source provenance
- Reusable cross-department work graphs
- Parallel dependency-aware execution
- Synthetic Government Environment with deterministic responses
- Document inspection and evidence extraction
- Verification, reconciliation, exceptions and risk findings
- Human authority and physical-action boundaries
- Durable PostgreSQL/SQLite case, queue, checkpoint, document, notification, payment and event persistence
- Resumable cases and incremental document submission
- Tamper-evident execution audit chain
- Server-controlled tenant membership and role boundaries
- Private usage metering for case/outcome billing foundations
- Opt-in authorized REST connectors for real integrations
- Unified Aether Command Center with guided document intake, document upload/hash ledger and role-aware officer authority queue
- Backend and frontend CI workflows
- Production security headers/readiness endpoint and legacy API quarantine
- Standalone resumable worker runtime with durable case leases and notification outbox dispatch
- Developer API marketplace catalog and tenant-scoped API keys
- Controlled-MVP release readiness endpoint and expanded post-deployment smoke test

The controlled MVP uses a deterministic synthetic government environment. It does not issue official government decisions/documents and does not represent live government authority.

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
Document storage uses Supabase Storage when configured with the server-only service-role key; otherwise it uses a local development store. Extracted document text is encrypted at rest when AETHER_ENCRYPTION_KEY is configured. OCR can be connected through AETHER_OCR_BASE_URL/AETHER_OCR_TOKEN.

## Deployment policy

Public research-preview changes stay on `launch/public-research-preview`; `main` remains release-only. Do not merge or publish a production release until the current readiness checklist is satisfied and the release is explicitly approved.

Do not deploy every small change. Before release, run the complete test/security/persistence gate. Then merge the final MVP to main, apply Supabase migrations, deploy the Render backend, publish the final Netlify frontend, run smoke tests, and keep a rollback path.

See MVP_MASTER_PLAN.md and SECURITY_RELEASE_PLAN.md for the release gate.

## Truthful MVP status

The repository contains a working controlled/sandbox prototype, but it is **not yet approved as launch-ready**. The public preview still requires final deployed-preview checks, a verified feedback-form submission, manual scenario/accessibility checks, and review of outstanding dependency/security findings. Production government execution remains fail-closed until authorised live connectors, authoritative effective-dated rules, statutory signature/issuance integrations, provider credentials, and deployed Supabase/Render/Netlify security validation are in place.



## Controlled public research sandbox

The deploy-preview context is wired to a separate Render service, `aether-public-demo`, rather than the authenticated production backend. It is a synthetic-only sandbox: production government connectors and legacy APIs are disabled; requests are rate-limited and body-size capped; file uploads and API-key management are disabled; and anonymous demo cases are partitioned by a random browser session identifier. The service uses local SQLite storage on a free Render instance, so demo data is temporary and can be lost on restart or redeploy.

**Never enter real names, contact details, identity numbers, confidential records, or actual documents.** Use fictional values only. Human steps and payment records are simulated; they do not issue official decisions or move money. The production Netlify context keeps authentication required and points to the separately configured backend.

## Autonomy measurement and release gate

The benchmark tool reports only values present in a supplied CSV; blank impact measurements remain unknown. It does not claim live validation or real-world savings without measured and independently checked data.

```bash
python -m unittest tools.test_autonomy_benchmark -v
python -m unittest tools.test_public_feedback_form -v
python tools/autonomy_benchmark.py path/to/measured-task-export.csv
```

See [Autonomous Execution Proof](docs/AUTONOMOUS_EXECUTION_PROOF.md) for the CSV schema, metrics, and the necessary-but-not-sufficient release gate.
