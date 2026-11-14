# Public MVP and Government-Authorization Boundaries

## Purpose

Aether is an India-first AI Government Execution Platform. The public MVP may demonstrate end-to-end government-process orchestration without claiming to be a government service or exercising government authority.

This document is a product and release-control baseline, not a legal opinion. Obtain India-qualified legal review before public launch and before any production personal-data processing or government integration.

## Public synthetic MVP: permitted product posture

The public MVP may let citizens, businesses, developers, and invited officers:

- Describe a goal and receive an indicative process plan.
- Discover departments, services, and publicly available requirements.
- View cross-department dependencies and indicative timelines.
- Use synthetic document fixtures and fictional identities for the public demo; real user documents are disabled from the public demo path until privacy, retention, deletion, and security controls have passed review.
- Create tasks, evidence records, reminders, and progress views within Aether.
- Experience simulated citizen, business, operator, and officer journeys using synthetic identities and records.
- Use developer documentation and sandbox APIs that do not connect to protected government systems.

All department maps, process templates, checklists, and timelines must be labelled indicative unless verified against current, effective-dated official sources. Cite the source, jurisdiction, retrieval date, and effective date where available. Do not imply that a discovery template is an official or exhaustive statutory checklist.

## Prohibited without specific authority and technical approval

Aether must not, without the relevant authority, credentials, permissions, and approvals:

- Submit, amend, withdraw, or track a real application by using a protected government integration.
- Access non-public citizen, business, identity, tax, land, health, banking, or other restricted records.
- Use another person's credentials, automate around access controls, scrape restricted portals, or bypass CAPTCHA, rate limits, or authentication.
- Issue, certify, approve, reject, or represent itself as granting a government licence, certificate, benefit, permit, or statutory decision.
- Display synthetic workflow completion as an official filing, acknowledgement, approval, or government outcome.
- Use government logos, seals, branding, or language that implies endorsement or affiliation without permission.

A user's consent alone does not replace the API publisher's approval, government authorization, or platform terms where those are required.

## Required user-facing disclosure

Display clearly on onboarding, relevant workflow screens, and completion screens:

> Aether is an independent software platform and is not a government website or department. Unless a workflow explicitly identifies an authorized live integration, this experience uses public information and/or simulated data. Aether cannot issue government approvals or certificates. A sandbox completion does not submit an application to, or create an official record with, any government authority.

For each workflow, identify whether it is:
1. Public-information guidance;
2. User-managed preparation;
3. Synthetic sandbox execution; or
4. Authorized live integration.

Never blur these modes.

## Data and privacy controls for public MVP

- Public demo default: use only fictional identities, synthetic business records, generated sample documents, and simulated acknowledgements. Do not invite public users to upload real personal or confidential records.
- Do not ask for Aadhaar, PAN, bank credentials, health records, or other sensitive/high-risk documents merely to demonstrate the product.
- Before accepting real user documents in any controlled pilot, provide a clear privacy notice, purpose, data categories, retention period, deletion/contact route, and consent flow appropriate to the data and feature.
- Use private storage, encryption, tenant isolation, least-privilege access, audit logs, and tested deletion/retention controls.
- Do not use customer documents to train models unless a separate, explicit, legally reviewed opt-in supports that use.
- Keep demo/test data segregated from any production data.
- Review the staged commencement dates of the Digital Personal Data Protection Act, 2023 and Rules, 2025 with counsel; do not assume all provisions commenced on the notification date.

## Government data and API integrations

For every proposed integration, maintain an approval record containing:

- Government department / API publisher and system owner;
- Exact API, data fields, purposes, user population, and jurisdiction;
- API publisher terms, written approval, credentials, and permitted use case;
- User-consent and authentication design where applicable;
- Security assessment, data-flow diagram, retention/deletion, incident handling, and audit requirements;
- Sandbox certification and production go-live approval;
- Reconciliation method against the authority's system of record;
- Named owner, support route, SLA, rate limits, and revocation/rollback plan.

For API Setu, follow its current terms, API-specific documentation, subscription and publisher-approval process. Availability in a directory is not blanket permission to consume an API. Use only valid credentials and approved use cases.

## Release gates

### Gate A — Public synthetic MVP

May proceed after engineering, privacy, security, and legal review confirms:
- No protected government integration is active;
- Synthetic and live modes are technically separated;
- Disclosures are visible and accurate;
- Public information is sourced and clearly labelled;
- User data handling is minimized, secured, and documented;
- Support, incident response, deletion, and rollback procedures are tested.

### Gate B — One authorized live integration

Requires all Gate A controls plus written authority from the relevant department/API publisher, API-specific credentials and terms, user-consent design where applicable, security testing, sandbox certification, production approval, and system-of-record reconciliation.

### Gate C — Government-wide deployment

Requires separate agreements and approvals for each participating authority and jurisdiction, plus procurement, hosting, security, audit, accessibility, operational, and support requirements applicable to that deployment. Approval from one department must not be treated as approval from another.

## Sources to re-check before each integration

- API Setu Terms of Use: https://docs.apisetu.gov.in/document-central/terms-of-use/
- API Setu consumer/API flow: https://docs.apisetu.gov.in/document-central/explore-apisetu/Overview.html
- Digital Personal Data Protection Act, 2023: https://www.indiacode.nic.in/bitstream/123456789/22037/1/a2023-22.pdf
- DPDP commencement notification, G.S.R. 843(E), 13 November 2025: https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf
- DPDP Rules, 2025: https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf
