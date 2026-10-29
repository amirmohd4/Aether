# Aether GovOS

Aether GovOS is an early-stage government-workflow orchestration prototype. It explores how an outcome-first interface could map requirements, coordinate permitted digital tasks, recover from exceptions, verify results, and stop at legally required human actions. The public research preview uses synthetic systems only.

**Product thesis:** Aether is an Administrative Execution OS: a governed, cross-organisation execution layer that coordinates permitted work across systems, employees and departments, then verifies the outcome while preserving the authority of each system of record.

**Long-term scope:** the same core can support public administration, education departments, public works, contractors, banks, insurers, developers, MSMEs and system integrators through validated vertical workflow packs.

## Research and strategy

- [Market research and product strategy](docs/MARKET_RESEARCH_AND_PRODUCT_STRATEGY.md)
- [CEO/CTO execution roadmap](docs/CEO_CTO_EXECUTION_ROADMAP.md) — phased plan to validate the first paid workflow, launch a controlled contractor pilot, measure ROI, and expand into education/public administration
- [India administrative service atlas](docs/INDIA_ADMINISTRATIVE_SERVICE_ATLAS.md) — service families, current systems to investigate, workflows, buyer hypotheses, automation boundaries and official sources
- [Administrative workflow research register](docs/ADMINISTRATIVE_WORKFLOW_RESEARCH_REGISTER.md) — discovery hypotheses, disconfirmation questions and pilot gates
- [Education scholarship workflow dossier](docs/workflow-dossiers/EDU-01-scholarship-case.md) — application, verification, sanction, payment and exception handling
- [Contractor tender-to-payment workflow dossier](docs/workflow-dossiers/GOV-03-contractor-tender-to-payment.md) — tender, contract execution, bill readiness and payment reconciliation

These are desk-research assets, not validated live process maps or proof of customer demand. Every production workflow must be checked against current rules, the exact jurisdiction, the system of record and authorised access.

## Public research preview

- **[Open the interactive synthetic preview](https://deploy-preview-15--aether-govos.netlify.app/research-preview.html)**
- [Share feedback](https://deploy-preview-15--aether-govos.netlify.app/feedback.html)
- [Launch-readiness checklist](docs/launch-readiness-checklist.md)
- [Global mock-preview plan](docs/global-mock-preview-plan.md)

Use fictional values only. The preview demonstrates workflow patterns; it does not contact government systems, submit official applications, issue records, or make legal decisions. Feedback submissions are registered by Netlify Forms, but end-to-end delivery has not yet been verified.

## Product strategy

The platform is designed around an outcome-to-work compiler, versioned administrative process graph, evidence provenance, authorised connector/action fabric, durable execution and recovery, role-aware workbench, outcome verification, and measured operations analytics. The research strategy deliberately starts with a narrow paid workflow while preserving a cross-administration architecture. Education administration is a first-class long-term vertical, not a separate unrelated product.

See [Market Research and Product Strategy](docs/MARKET_RESEARCH_AND_PRODUCT_STRATEGY.md) for the source-backed market thesis, education workflows, vertical comparisons, autonomy policy, commercial model and 90-day research plan. Use the [Administrative Workflow Research Register](docs/ADMINISTRATIVE_WORKFLOW_RESEARCH_REGISTER.md) to track candidate workflows, buyer hypotheses, evidence strength, disconfirmation questions and pilot gates.

## Current MVP

- 32 public mock services in the user-facing service catalogue
- Objective understanding with ranked candidates
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
- Unified Aether Command Center with guided intake, document upload/hash ledger and role-aware officer authority queue
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
AETHER_ENV=staging
AETHER_AUTH_MODE=supabase
AETHER_ENABLE_LEGACY_API=false
AETHER_ENABLE_PRODUCTION_CONNECTORS=false
```

Do not enable live connectors or use real citizen data in the public research preview. Production release requires authorised integrations, verified rule packs, deployed security checks, and rollback validation.
