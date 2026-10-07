# Aether — Real Government Production Activation Plan

## 1. Is this required for the MVP?

No for the controlled/sandbox MVP.

Aether's current MVP is intentionally non-authoritative: it proves the execution architecture end-to-end using deterministic synthetic government systems. Live government production is a separate activation phase.

It becomes required when Aether is expected to:
- read or write real government records;
- submit real applications to government systems;
- retrieve authoritative citizen/business/property data;
- make or transmit legally binding decisions/documents;
- operate for real citizens, banks, businesses or government departments in production.

Do not unlock live execution merely by setting a feature flag.

## 2. The first production pilot

Do not integrate all 34 services at once.

Choose:
- one department;
- one jurisdiction;
- one high-value service;
- one government system/API path;
- one clearly defined pilot outcome.

The first connector should be narrow enough that the government authority can certify the data fields, request/response contract, permissions and operational owner.

## 3. What we need from the government

For the selected service, obtain a written integration packet containing:

### Authority
- department/organization owner;
- authorized technical and business contact;
- written authorization for Aether to integrate;
- approved purpose/use case;
- approved environments (sandbox and production);
- approved data categories and retention rules.

### Technical contract
- base URL(s) and environment separation;
- authentication mechanism and credential process;
- API/OpenAPI documentation;
- request/response schemas;
- status and error semantics;
- rate limits, timeouts and retry rules;
- webhook/polling contract if asynchronous;
- maintenance/contact/escalation process;
- certificate/mTLS/IP allow-list requirements if applicable.

### Legal/statutory boundary
- which steps Aether may automate;
- which steps require an officer;
- which steps require a physical act;
- who is legally responsible for each final decision;
- whether e-signature, certificate issuance or other certified services are required.

## 4. Where we should look first

### API Setu / government API marketplaces

API Setu is an official MeitY platform for discovering and integrating government APIs. Access to an API is subject to the relevant use case and provider approval; credentials/permissions are issued through the approved onboarding/subscription flow.

Use it to:
1. search for the required government API;
2. identify whether sandbox access exists;
3. register Aether as an authorized consumer where applicable;
4. obtain provider approval;
5. receive credentials and API documentation;
6. integrate against the sandbox first.

### Government department systems

If the required service is not exposed through API Setu, the department/NIC/state e-governance owner may provide a direct integration, secure gateway, service-bus interface, or another approved mechanism.

Aether must use only the mechanism explicitly authorized by the system owner.

## 5. What we need for rules

For every production service/jurisdiction, build a versioned rule pack from authoritative government material.

Required metadata:
- rule-pack ID and version;
- jurisdiction;
- authority status;
- source document/title;
- source URL or controlled document reference;
- verification date;
- effective date;
- rule IDs;
- service binding;
- conditions, required inputs/documents and boundary conditions.

The Aether release gate must reject a production pack that is missing authoritative provenance or effective dates.

Never invent a legal rule, effective date, fee, SLA, document requirement or approval condition.

## 6. Connector activation sequence

### Phase A — sandbox
1. Register/authorize Aether.
2. Receive sandbox credentials.
3. Map the government's schema to Aether's canonical connector contract.
4. Implement the adapter behind the existing connector registry.
5. Add contract tests using official sandbox responses.
6. Verify authentication, retries, idempotency and asynchronous status handling.
7. Verify audit events and evidence mapping.

### Phase B — rule activation
1. Load the authoritative rule pack.
2. Validate source/effective-date completeness.
3. Run rule regression tests.
4. Confirm human/statutory boundaries with the authority.
5. Obtain business/department acceptance.

### Phase C — security and operational acceptance
1. Secrets remain server-side.
2. Confirm tenant/department/jurisdiction authorization.
3. Validate encryption, document handling and retention.
4. Run security testing.
5. Run load/timeout/retry/duplicate-request tests.
6. Validate monitoring, incident response and rollback.

### Phase D — controlled production rollout
1. Start with a very small approved cohort.
2. Keep live execution behind an explicit production authorization/configuration boundary.
3. Compare Aether outcomes against the government system of record.
4. Monitor errors, latency, reconciliation and human escalations.
5. Expand only after the authority signs off on the pilot results.

## 7. Statutory integrations

Where a process requires legally valid signing, certificate issuance or another regulated trust service, use the government's approved provider/mechanism.

Aether should orchestrate the step and preserve evidence, but must not pretend that an internal Aether result is an official certificate, signature or government decision.

## 8. Provider activation

Separate contracts/credentials may be required for:
- OCR/vision;
- email/SMS/notification delivery;
- payments;
- e-signature/certificate services.

Provider adapters should remain server-side, credentialed, observable and idempotent.

## 9. Production go/no-go checklist

A service can move from controlled to live only when all are true:

- [ ] Written government authorization
- [ ] Approved technical endpoint/contract
- [ ] Valid production credentials
- [ ] Sandbox certification completed
- [ ] Authoritative rule pack loaded
- [ ] Effective dates verified
- [ ] Human/statutory boundaries approved
- [ ] Required statutory provider certified/approved
- [ ] Security validation completed
- [ ] Load/chaos/timeout/retry validation completed
- [ ] Monitoring and incident owner assigned
- [ ] Rollback tested
- [ ] Government/department UAT sign-off recorded

## 10. What Aether engineering already provides

The existing MVP already provides the platform layer for this activation:

Objective → requirements → case → work graph → queue → connector → evidence → verification/reconciliation → human/statutory pause → resume → outcome → audit.

Therefore the next engineering work is adapter implementation and certification against actual authorized government contracts, not a rewrite of the core engine.

## 11. First target recommendation

For the first real-world pilot, use one J&K service where the department can provide a clear technical owner, sandbox, authoritative rules and measurable outcome.

Do not start with a multi-department mega-integration. Prove one certified workflow completely, then reuse the connector/rule/audit pattern for the next services.
