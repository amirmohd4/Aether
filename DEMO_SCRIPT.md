# Aether GovOS — Controlled MVP Demo Script

**Audience:** Government stakeholders, developers, partners, investors  
**Positioning:** Aether is a government execution layer. The controlled MVP demonstrates end-to-end orchestration against deterministic synthetic government systems. It does not issue official government decisions or documents.

---

## 0:00–0:20 — The Problem

**Visual:** Aether Command Center.

**Voiceover:**
“Aether starts with a real-world government objective instead of forcing a user to understand which department, form, or sequence comes next. It turns that objective into a governed workflow.”

**On-screen:**
- Objective understanding
- Requirements discovery
- Cross-department orchestration
- Evidence and audit
- Human/statutory boundary

---

## 0:20–0:45 — Understand the Objective

**Actions:**
1. Enter a natural-language service objective.
2. Show ranked service candidates.
3. Show clarification when the request is genuinely ambiguous.
4. Select the resolved service.

**Voiceover:**
“Aether identifies the likely service, exposes alternatives when relevant, and stops for clarification instead of guessing when ambiguity matters.”

---

## 0:45–1:10 — Discover Requirements

**Actions:**
1. Open the requirements view.
2. Show required inputs and documents.
3. Show jurisdiction and rule-source provenance.
4. Upload a required document from the guided intake flow.

**Voiceover:**
“Requirements are discovered with jurisdiction and rule provenance. Documents are validated, stored privately, hashed for integrity, and linked back to the case.”

**Important:** Demonstration data is synthetic. Do not present sandbox rules as live legal authority.

---

## 1:10–1:40 — Build and Execute the Work Graph

**Actions:**
1. Start the case.
2. Show the generated work graph.
3. Show dependency-aware tasks entering the durable queue.
4. Show independent work executing in parallel.
5. Show checkpoints and case state.

**Voiceover:**
“The case engine turns the service into a dependency-aware work graph. Independent digital work can run in parallel, while durable queues, leases, retries, idempotency and checkpoints make execution resumable.”

---

## 1:40–2:00 — Verify Evidence

**Actions:**
1. Open task/evidence status.
2. Show verification and reconciliation results.
3. Show an exception or missing-evidence state.
4. Resolve the evidence gap.

**Voiceover:**
“Aether does not treat a response as truth merely because a connector returned it. Results are verified, reconciled and surfaced as evidence, exceptions, and risk findings.”

---

## 2:00–2:20 — Human and Statutory Boundary

**Actions:**
1. Navigate to the officer authority queue.
2. Show a task paused for a human decision.
3. Approve or reject with an officer role.
4. Resume the case.

**Voiceover:**
“When law or institutional authority requires a person, physical act, or statutory decision, Aether stops. The authorized officer acts, the decision is recorded, and the workflow resumes.”

---

## 2:20–2:40 — Outcome, Audit and Notifications

**Actions:**
1. Show the completed case outcome in the Command Center.
2. Open the audit chain.
3. Show notification/outbox state.
4. Show usage/payment records where configured.

**Voiceover:**
“The final state includes the outcome, supporting evidence, event history and tamper-evident audit chain. Operational events are durable rather than dependent on a single browser session.”

---

## 2:40–3:00 — Developer and Marketplace Surface

**Actions:**
1. Open the API Marketplace.
2. Show the 34 controlled MVP service contracts.
3. Show tenant-scoped API key controls.
4. Show connector and rule-pack readiness.

**Voiceover:**
“For developers and institutional partners, Aether exposes a shared service catalog and tenant-scoped API access. Real connectors and authoritative rule packs are explicitly configured rather than implied.”

---

## 3:00 — Closing

**Voiceover:**
“The controlled Aether MVP is an execution and orchestration layer: objective to requirements, case to work graph, execution to evidence, human authority to outcome, and every step auditable. Live government execution is intentionally fail-closed until the responsible authority provides authorized endpoints, credentials, authoritative rules, and any required statutory integrations.”

**Closing screen:**
- Aether GovOS
- Controlled MVP
- Government execution layer
- Live authority requires authorized external integrations

---

## Claims we must not make in the controlled MVP demo

Do not describe synthetic data as live government data.

Do not claim that official government certificates, registrations, approvals, or statutory decisions are issued by Aether.

Do not claim “fully automated” for workflows containing human or statutory boundaries.

Do not claim arbitrary state/country coverage without an installed, source-backed and authorized rule/connector configuration.

Do not quote unsupported historical metrics such as property counts, connector counts, API prices, or response times.

---

## Recording Checklist

- Backend/API is healthy.
- Frontend is built from the current release branch.
- Use a test tenant and synthetic data.
- Demonstrate an actual case from intake through pause/resume.
- Show the audit result.
- Show the human authority queue.
- Show the service marketplace.
- Clearly label sandbox/controlled behavior.
