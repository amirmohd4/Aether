# Municipal Trade Licence Vertical Slice

## Scope

This is Aether's first dedicated municipal business-licensing workflow slice. The initial demonstration scenario is a fictional retail shop in Jammu district, Jammu and Kashmir. It is a product and engineering pilot, not a representation that Jammu Municipal Corporation has approved Aether or that this service is available for statutory submission through Aether.

## What the software now models

1. Applicant/entity identity and evidence intake.
2. Business-premises and occupancy evidence review.
3. Business activity and location classification.
4. A configurable screen for additional clearances. Fire, food-safety, labour, environmental and other dependencies must be determined from the current verified rule pack; they are not presumed mandatory.
5. Evidence and exception reconciliation.
6. An evidence-backed decision packet for the competent municipal authority.
7. An explicit human decision/signature checkpoint.
8. Official record synchronisation only through an authorised departmental connector.
9. Licence output/notification only after the official system confirms issuance.

## Rule and authority boundary

A source-backed Jammu & Kashmir profile is now loaded from the Housing & Urban Development Department circular dated 29-10-2022 and the JanSugam municipal-corporation commercial-establishment NOC listing. The circular reduces the core application evidence to two categories: identity proof and the applicable legal-occupancy/land document. For a firm/company, the application/authorization form must be signed by an authorized person. The JanSugam listing gives a 30-day service period, excluding government holidays. This does not yet establish the exact current designated officer, appellate authority, complete scrutiny sequence, fee schedule, or activity-specific conditions; those must be confirmed with the competent municipal authority before pilot activation.

A real pilot still requires the competent municipal authority to confirm:
- the exact service name, service owner and receiving office/portal;
- current rules, forms, eligibility, accepted evidence, fees and service timelines;
- the activity categories and conditional NOCs/inspections;
- officer roles, delegation, decision and signature authority;
- the accepted submission channel and official receipt/status mechanism;
- the conditions for official licence generation and record reconciliation.

## Release behaviour

- Synthetic preview: may exercise the workflow using fictional data and simulated authority actions. It must visibly state that no official application or licence is created.
- Controlled institutional pilot: only after written authority, verified rule pack, approved test credentials, security/privacy review and an agreed operating procedure.
- Live statutory service: only after an authorised connector, official acknowledgement reconciliation, authorised officer decisions, certificate validation, recovery/monitoring and operational acceptance are evidenced.

Production connectors remain disabled. Do not upload real identity or business documents into the public synthetic preview.

## Official sources checked

- J&K Housing & Urban Development Department circular HUD-PLANOCSS/34/2021-01 dated 29-10-2022: https://singlewindow.jk.gov.in/uploads/files/act_0434650001667037275.pdf
- JanSugam service 16810006, municipal-corporation commercial-establishment NOC (30 days; online/by-hand/kiosk): https://jansugam.jk.gov.in/getServiceDesc.html?serviceId=16810006
- Jammu Municipal Corporation online NOC/licence service directory: https://jmc.jk.gov.in/pddeservices.html
