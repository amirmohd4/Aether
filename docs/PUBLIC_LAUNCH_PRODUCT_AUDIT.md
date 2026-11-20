# Aether Public Launch — Product Experience Audit

**Audit date:** 2026-11-20  
**Audited candidate:** `integration-check/public-preview-into-hardened` at `ca26c524b2860f268448ce80dc6488c668f9e499`  
**Audit branch:** `public-launch/product-experience-audit`  
**Purpose:** Establish the first evidence-based product workstream for the public Aether GovOS launch. This is a source-code audit, not a claim that deployed browser journeys have been tested.

## Executive verdict

Aether has substantial backend orchestration and domain UI foundations, but the current frontend composition is not yet a coherent public-facing Government OS experience. The immediate next step is to make the public entry experience and the core objective-to-workflow journey coherent, truthful, and demonstrably functional before adding more surface area.

The public launch can operate without live government integrations. It must clearly separate:
- Aether actions that actually execute inside the platform;
- public information and requirements whose provenance/status is disclosed;
- simulated government responses; and
- steps that require a real external authority or system.

## Evidence-backed findings

### P0 — Public app composition does not currently expose a clear product journey

- `src/App.tsx` renders `PublicMvpNotice`, `GlobalMockStudio`, `AetherCommandCenter`, `DeliveryOpsConsole`, and `IndiaAdminIntelligence` sequentially.
- `src/App.tsx` does not import or render `GlobalLanding`.
- The repository contains `src/pages/GlobalLanding.tsx`, but it is not the application entry point in the inspected composition.
- The result is a long stacked collection of tools rather than a deliberate public landing → choose persona/objective → guided workflow → workspace journey.
- `AetherCommandCenter` is a large, dense application surface (78 KB source file) and needs role- and task-oriented navigation rather than being exposed as one undifferentiated page.

**Required action:** Design and implement a single public application shell with clear entry points for citizen, business, bank/financial institution, developer, and government officer. Route each persona into a coherent workspace. Preserve the existing execution engine; do not replace it with a static marketing page.

### P0 — The current mock studio is a client-side scenario simulator, not the real workflow engine

Evidence in `src/components/GlobalMockStudio.tsx`:
- `runSimulation()` generates a `SIM-...` reference in the browser.
- It constructs scenario steps from local helper functions and React state.
- Its UI explicitly says no government connector is called and no real application is created.
- The workflow templates are illustrative; the jurisdiction label does not verify local law or service availability.
- It presents five scenarios: routine, missing evidence, human review, retry, and adverse/evidence conflict.

**Required action:** Retain this as an explicitly labeled preview/sandbox scenario tool, but make the primary product journey use the actual Aether V2 backend case, requirements, work graph, task, evidence, and audit APIs. A demo must not make client-generated simulation references look like persisted Aether cases.

### P0 — Feedback is not submitted from the mock studio

Evidence in `src/components/GlobalMockStudio.tsx`:
- The feedback UI says feedback is not sent automatically.
- `copyFeedback()` copies text to the clipboard.
- `openFeedbackForm()` stores a draft in browser `sessionStorage` and navigates to `/feedback.html`.
- This component alone does not prove that the feedback form persists a submission or that the team receives it.

**Required action:** Verify the deployed feedback endpoint/form end-to-end and add a durable, privacy-conscious feedback store or a clearly disclosed external intake. Show a real submission confirmation only after the server/provider accepts it.

### P1 — Claims and service counts need product-wide truth review

- `src/components/GlobalHero.tsx` contains claims including “195 UN Member States Ready”, “15+ Governments Active”, “< 3 mins Average Processing”, and “99.99% Sovereign Uptime”. No evidence for these metrics was found in the inspected source or release evidence.
- `GlobalHero.tsx` is not currently rendered by `src/App.tsx`, but must not be wired into the public entry point with these claims unchanged.
- `GlobalMockStudio.tsx` describes 32 templates in its UI copy, while repository release documents describe a 34-service registry. The user-facing count needs to be derived from the actual catalog and consistently explained.
- The repository's `README.md` correctly describes the controlled MVP as synthetic and non-authoritative.

**Required action:** Remove unsupported metrics and universal coverage claims. Display only measured, reproducible product capabilities and distinguish registered service families from jurisdiction-verified live services.

### P1 — Public and authenticated surfaces need a deliberate access model

- `AuthContext` uses `VITE_REQUIRE_AUTH` to determine whether authentication is required.
- The Command Center, Delivery Ops Console, and India Admin Intelligence have different auth-aware behavior.
- `DeliveryOpsConsole` returns no UI when authentication is required but there is no session.
- The current top-level composition does not establish clear public-preview versus signed-in workspace navigation.

**Required action:** Define which capabilities are public, which require sign-in, and which require an officer/developer role. Test those boundaries in the browser and enforce authorization on the backend; hiding a frontend component is not an access-control mechanism.

### P1 — Document and workflow claims need deployed end-to-end proof

- The backend has a server-side document adapter with private Supabase Storage support, content validation, SHA-256 hashing, and extracted-text handling.
- The repository contains tests for encryption and document validation.
- These facts do not prove the deployed Render service can upload, retrieve, and authorize access to documents using the configured Supabase credentials.
- Backend CI passed, but CI tests do not prove a real deployed multi-tenant workflow.

**Required action:** Run staging tests for upload → metadata persistence → authorized read → hash verification → cross-tenant denial, using synthetic documents and two disposable test tenants.

## Product target for the public launch

The first public release should demonstrate the real Aether product loop:

1. User selects a persona and describes an objective in natural language.
2. Aether identifies the likely service and asks for missing/ambiguous context.
3. Aether shows candidate departments/services, jurisdiction scope, and provenance/authority status.
4. Aether creates a persisted case using the V2 backend.
5. Aether builds and displays the dependency-aware work graph, parallelizable tasks, blockers, and human/statutory boundaries.
6. User uploads synthetic or voluntarily supplied documents with clear privacy guidance; Aether validates and securely stores them.
7. Aether tracks task progress, evidence, exceptions, user actions, and next best actions.
8. Officer/operator workspace supports review, assignment, evidence requests, and internal decisions with role checks.
9. Aether records audit history and distinguishes internal completion from external official acceptance.
10. User can submit feedback and receive a genuine confirmation.

For steps requiring an external government portal, the product should prepare the handoff, tell the user exactly what remains external, let the user record an acknowledgement/reference, and continue tracking. It must never fabricate submission, government acceptance, or statutory outcome.

## Implementation order

### Workstream 1 — Public product shell and truthful entry point
- Build coherent public landing and navigation around the existing product.
- Add persona entry points and a single natural-language objective start.
- Remove unsupported metrics and claims.
- Separate public preview, signed-in workspace, officer tools, and developer tools.
- Do not discard or rewrite working backend capabilities.

### Workstream 2 — Real end-to-end citizen/business workflow
- Connect the main user journey to V2 APIs rather than the client-only mock simulator.
- Persist the case and show requirements, jurisdiction/provenance, work graph, tasks, blockers, evidence, audit, and next actions.
- Use a synthetic mode indicator and accurate official-outcome provenance throughout.

### Workstream 3 — Officer/operator and developer experiences
- Make role-specific workspaces discoverable and usable.
- Verify tenant, role, department, and jurisdiction restrictions server-side.
- Keep sandbox API contracts clearly distinct from live connectors.

### Workstream 4 — Feedback and public-launch operations
- Verify real feedback persistence and acknowledgement.
- Add privacy notice, terms, support/contact ownership, incident/reporting path, accessibility checks, analytics with data minimization, and abuse/rate-limit controls.
- Verify rollback and production monitoring.

### Workstream 5 — Staging acceptance
- Test real worker processing/retry/restart recovery.
- Test private document upload/read/hash/encryption and cross-tenant denial.
- Run end-to-end journeys for citizen/business and officer/operator.
- Test feedback submission and rollback.
- Only then approve the controlled public preview.

## Explicit non-goals for this public preview

- No unauthorized government API access or scraping of protected systems.
- No claim that Aether submits official applications or receives official outcomes without an authorized connector.
- No fabricated legal requirements, fees, SLAs, coverage, performance or uptime statistics.
- No real sensitive citizen documents in demos or synthetic test fixtures.
- No production connector enablement by feature flag alone.

## Release decision

**Current decision: NOT YET APPROVED FOR PUBLIC LAUNCH.**

The authenticated staging smoke and CI are positive evidence, but the public product journey is not yet coherent or fully verified. The highest-leverage next step is Workstream 1 followed immediately by Workstream 2—not another broad infrastructure expansion and not premature live government integration.

This audit is based on the repository files listed above and the inspected release candidate. Items requiring browser, provider, or live staging execution are explicitly marked as requiring verification rather than assumed complete.
