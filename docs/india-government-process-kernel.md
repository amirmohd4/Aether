# Aether India Government Process Kernel

## Purpose

Aether should sit above existing government departments and systems, not replace them. This document defines the operating model Aether should use to turn a citizen/business objective into the actual government work that occurs after submission.

The National Portal of India currently presents 13,994 online services, including 1,100+ central-government services and 12,894+ state-government services, across 18 information categories. Its current service taxonomy includes Agriculture/Rural/Environment, Benefits/Social Development, Business/Self-employed, Citizenship/Visa/Passports, Driving/Transport, Education/Learning, Governance/Planning, Health/Wellness, Housing/Local Services, Infrastructure/Industries, Jobs, Justice/Law/Grievances, Money/Taxes, Science/IT/Communication, Travel/Tourism, Welfare of Families and Youth/Sports/Culture. The older National Government Services Portal reported 13,698 services before its May 2026 migration notice. This scale means Aether should not hard-code one workflow for every service; it needs a reusable process kernel plus jurisdiction-specific service profiles.

UMANG already provides a one-stop interface for major services. Aether's differentiation must therefore be execution of the underlying government work, not another service directory.

Sources:
- https://www.india.gov.in/
- https://www.india.gov.in/services
- https://services.india.gov.in/service/detail/
- https://negd.gov.in/our_projects/umang/

## Universal post-submission lifecycle

Most application-driven services can be modeled as:

1. Receive and acknowledge
2. Register / diarize / create case file
3. Determine jurisdiction and competent authority
4. Assign to section / official
5. Completeness and document scrutiny
6. Identity / entity / KYC validation
7. Record lookup and cross-system verification
8. Deficiency / clarification / query cycle
9. Technical or substantive scrutiny
10. Inter-department consultation / NOC
11. Inspection / field verification when required
12. Prepare note / recommendation / agenda
13. Statutory decision
14. Calculate demand / fee / dues / security
15. Verify payment
16. Generate order / certificate / licence / approval
17. Digitally sign / register / update master record
18. Dispatch / notify / publish
19. Post-decision compliance / renewal / monitoring
20. Appeal / grievance / audit / retention

Stages can be skipped, repeated or executed in parallel.

## Employee work atoms

Across departments, employees repeatedly perform:

- open/diarize a case and confirm the correct office;
- classify and route the case;
- compare application against checklist;
- inspect uploaded documents;
- extract facts and enter them into departmental systems/forms;
- search existing records;
- reconcile names, addresses, IDs, parcels, registrations, tax numbers and references;
- raise deficiency/shortfall queries;
- compare resubmissions;
- draft office notes, scrutiny notes and correspondence;
- request reports from other sections/departments;
- chase pending reports;
- schedule inspections and appointments;
- consolidate inspection/report comments;
- calculate fees, dues, penalties and balances;
- verify payment;
- prepare decision/certificate/order packets;
- update records and notify the applicant;
- monitor pending cases, appeals, renewals and compliance;
- prepare audit/evidence files.

These work atoms are the deeper employee-automation moat for Aether.

## Service archetypes

### 1. Certificate / record issuance

Examples: birth, death, domicile, income, caste/community, nationality, surviving-member.

Typical path:
application -> acknowledgement -> completeness -> local/record verification -> report -> competent officer scrutiny -> issue.

Delhi's domicile flow shows dealing-assistant document checks, acknowledgement, verification, Tehsildar scrutiny/recommendation, SDM approval and certificate issue. Delhi income-certificate guidance uses local enquiry before issue.

Sources:
- https://revenue.delhi.gov.in/sites/default/files/revenue/rti-files/46-3.pdf
- https://revenue.delhi.gov.in/revenue/income-certificate-0

Aether: automate intake, checklist, extraction, record matching, enquiry packets, deficiency notices, SLA tracking, certificate preparation and notification. Human: statutory verification/finding and approval.

### 2. Mutation / land-record change

Typical path:
application -> jurisdiction -> notice/proclamation -> Patwari report -> statements/objections -> document/record matching -> sanction or referral -> record update -> appeal.

Delhi Revenue describes Patwari record maintenance and mutation initiation. Its mutation procedure includes proclamation, Patwari report, statements, document matching, sanction where no objection and referral to Revenue Assistant/SDM where objections arise.

Source:
- https://dmsouth.delhi.gov.in/services-offered/

Aether: property/entity normalization, record lookup, notice generation, objection-window tracking, report requests, contradiction detection, appeal tracking and file preparation. Human: contested-right findings, hearings and statutory orders.

### 3. Property registration

Typical path:
deed/data preparation -> online scrutiny -> Sub-Registrar verification -> approve/reject/resubmit -> stamp duty/registration payment -> appointment -> physical presentation/identity/biometric as applicable -> registration -> registered document.

Odisha's official flow states that the Sub-Registrar can approve/reject/resubmit, payment follows approval, an appointment is fixed and original documents are presented at the office.

Source:
- https://www.igrodisha.gov.in/Property.aspx

Aether: deed-data extraction, party validation, fee calculation from authoritative rules, appointment coordination, pre-registration packet and post-registration reconciliation. Human: mandatory physical and registrar acts.

### 4. Municipal trade licence

Typical path:
application -> document scrutiny -> inspection where required -> health/technical review -> higher approval -> demand/fee -> payment -> licence.

BBMP documents multiple verification/forwarding levels. MCGM documents document verification, correction/re-upload, fire NOC for hazardous products, approval, demand, payment and certificate generation.

Sources:
- https://site.bbmp.gov.in/departmentwebsites/BBMPIT/OTLS.html
- https://portal.mcgm.gov.in/irj/portal/anonymous/qlChecklistITLp

Aether: form preparation, document review, premises/property reconciliation, inspection scheduling, NOC coordination, demand and payment reconciliation, renewal watch. Human: inspection and statutory approval.

### 5. Building / development permission

Typical path:
submit plans -> fee -> screening -> technical plan examination -> site inspection -> title/dues/revenue checks -> NOCs/conditions -> committee/authority -> demand -> payment -> compliance -> digitally signed approval.

Rajasthan's published flow includes Assistant Town Planner plan examination, Junior Engineer inspection, account dues, revenue title verification, Building Plan Committee approval, demand, applicable NOCs/conditions and final digital approval. MCD currently exposes online status, joint inspection and digital sanction/occupancy outputs.

Sources:
- https://www.lsg.urban.rajasthan.gov.in/content/dam/raj/udh/lsgs/lsg-jaipur/pdf/stp%20cell/Appling%20processer%20%20of%20buliding%20plan%20approval.pdf
- https://eodb.mcd.gov.in/

Aether: plan/document extraction, zoning checks, title/dues lookup, NOC dependency graph, inspection packets, committee agenda, demand, payment and conditions tracker. Human: site inspection and statutory planning decision.

### 6. Fire NOC

Typical path:
application -> clerk scrutiny -> defect loop -> fire verifier -> physical inspection -> report/photos -> approving authority/committee -> NOC.

Haryana's official process explicitly describes clerk scrutiny, correction/re-upload, fire-officer inspection/report and approval. Surat describes plan scrutiny, fire-officer recommendation and site inspection.

Sources:
- https://www.ulbharyana.gov.in/WebCMS/Start/10572
- https://www.suratmunicipal.gov.in/Departments/TownDevelopmentHowDoIFireNOC

Aether: checklist, evidence extraction, correction notices, inspection scheduling, inspection packet, report ingestion, recommendation packet, fees and renewal monitoring. Human: physical safety inspection and statutory certification.

### 7. Factory / labour licensing

Typical path:
application -> scrutiny -> inspection/site verification -> labour/fire/environment/premises evidence -> recommendation -> higher review -> approval/licence.

West Bengal's SOP describes official scrutiny/visit/recommendation, higher-level review and final approval/rectification. Assam describes multi-stage site appraisal, plan approval and registration/licensing.

Sources:
- https://factories.wb.gov.in/main/user_manual_registration
- https://ciflabour.assam.gov.in/portlet-innerpage/registration-licencing-for-non-hazardous-factory

Aether: multi-department evidence matrix, risk/category preparation, inspection scheduling, discrepancy handling, recommendation-note drafting, SLA monitoring and licence packet. Human: inspection and statutory decision.

### 8. Food-business licensing

FoSCoS is the pan-India FSSAI licensing/registration platform and supports tracking, inspection checklists and alerts; it integrates with other food-safety systems.

Source:
- https://foscos.fssai.gov.in/about-flrs

Aether: classify business, map documents/products, validate premises, manage deficiencies, schedule/prepare inspections, monitor compliance/renewal/returns. Human: official inspection, sampling and adjudication.

### 9. Environment / pollution consent

Typical path:
project classification -> application -> fee -> scrutiny -> technical/environmental review -> inspection if required -> consent/authorization -> conditions -> monitoring/renewal.

Government service descriptions show online submission and regulatory assessment; pollution rules permit officials to inspect premises and seek plans/specifications/additional information.

Sources:
- https://services.india.gov.in/service/detail/consent-to-operate-cto-from-punjab-pollution-control-board-in-punjab-1
- https://v1.wii.gov.in/airpollution_rules_1

Aether: category/rule lookup, evidence matrix, consent-history retrieval, deficiency cycle, inspection scheduling, condition tracking and renewal. Human: regulatory determination, inspection, sampling and adjudication.

### 10. Transport

Vehicle registration can be highly digital: manufacturer vehicle parameters, Aadhaar eKYC, taxes/fees and links to insurers, financiers, FASTag, HSRP providers and RTOs.

Source:
- https://services.india.gov.in/service/detail/apply-for-vehicle-registration-1

Driving-licence workflows add a physical test boundary.

Aether: data ingestion, reconciliation, duplicate checks, fee/tax calculation, appointment/test preparation, exception handling and status orchestration. Human: physical tests/inspection and licensing decision.

### 11. Passport

PSKs/POPSKs handle front-end functions while Passport Offices handle back-end processing including printing, dispatch, police liaison and review of police reports.

Sources:
- https://www.passportindia.gov.in/psp/FaqWhereToApply
- https://www.passportindia.gov.in/AppOnlineProject/pdf/rti_Trivandrum.pdf

Aether: document preparation, appointment management, police-verification coordination, adverse-report routing, dispatch monitoring. Human: biometric capture, granting decision and police findings.

### 12. Company incorporation

MCA states that name reservation/incorporation processing at the Central Reservation Centre is faceless and randomized and that resubmissions are normally not handled by the same official.

Source:
- https://mca.gov.in/content/mca/global/en/home.html

Aether: entity data assembly, signatory/DSC checklist, form preparation, consistency checks, resubmission diff and downstream registration coordination. Human: statutory registrar action.

### 13. Tax and regulatory processing

The Income Tax portal combines e-filing with centralized processing, intimations, rectification, refunds, worklists and demand-management facilities; PAN verification is also available to authorized external agencies.

Sources:
- https://www.incometax.gov.in/iec/foportal/
- https://www.incometax.gov.in/iec/foportal/help/all-topics/e-filing-services/verify-your-pan

Aether: validation, record matching, discrepancy detection, notice/response preparation, deadline tracking, demand/payment reconciliation and audit evidence. Human: assessment, adjudication and statutory determinations.

### 14. Social security claims

EPFO provides online member/employer services and currently notes additional verification and validation during claim/service processing. Its documented online transfer workflow includes employer verification followed by central processing.

Sources:
- https://unifiedportal-mem.epfindia.gov.in/
- https://www.epfindia.gov.in/site_docs/PDFs/Circulars/Y2013-2014/IS_OTCP_RelBetaVersion_12573.pdf

Aether: claim intake, record retrieval, employer follow-up, discrepancy comparison, queue control, settlement reconciliation and notifications. Human: statutory/field exceptions.

### 15. Scholarships / benefits / subsidies

Typical path:
application -> institute/local verification -> district/state/department verification -> eligibility/sanction -> DBT/payment -> reconciliation -> renewal/monitoring.

For NMMSS 2026-27, Ministry of Education describes Level-1 verification by the Institute Nodal Officer and Level-2 by the District Nodal Officer, with disbursement through PFMS/DBT.

Source:
- https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2295776

Aether: application validation, eligibility evidence matrix, routing, duplicate/fraud signals, bank validation, reminder engine, sanction packet, payment reconciliation and renewal watch. Human: exception handling and sanction decision when required.

### 16. Grievances

CPGRAMS connects central ministries/departments and States with role-based access, unique IDs, status tracking, reminders/clarification and appeal after unsatisfactory disposal.

Source:
- https://www.pgportal.gov.in/

Aether: classification, jurisdiction routing, similar-case retrieval, evidence collection, SLA/reminders, response drafting, escalation and closure evidence. Human: substantive redress decision.

### 17. RTI

RTI Online shows statuses such as forwarded to CPIO, transferred to another public authority and disposed; one request can generate multiple numbers when forwarded to multiple CPIOs, and supporting documents can be requested.

Source:
- https://rtionline.gov.in/faq.php

Aether: subject/jurisdiction routing, transfer preparation, record-search packets, deadline watch, supporting-document requests, response drafting and appeal tracking. Human: CPIO disclosure/exemption decisions.

### 18. Public procurement

The Department of Expenditure procurement manual describes technical and financial evaluation stages, comparative statements, tender committees for applicable procurements and recording reasons/decisions.

Source:
- https://doe.gov.in/files/circulars_document/MfPoNCS_2025.pdf

Aether: procurement file creation, compliance matrices, bid-document comparison, clarification consolidation, workpapers, comparative statements, committee agenda, contract packet, milestone/payment reconciliation. Human: evaluation judgment, committee decision, award and delegated financial authority.

## Core work-atom catalog

Aether should implement reusable operations:

REGISTER_CASE
CLASSIFY_CASE
ROUTE_CASE
ASSIGN_OFFICER
CHECK_COMPLETENESS
EXTRACT_DOCUMENT_FACTS
COMPARE_DOCUMENTS
VERIFY_IDENTITY
LOOKUP_RECORD
RECONCILE_RECORDS
DETECT_DUPLICATE
CHECK_ELIGIBILITY
CALCULATE_FEE
CHECK_DUES
PREPARE_DEFICIENCY
PREPARE_QUERY
INGEST_RESPONSE
COMPARE_RESUBMISSION
REQUEST_INTERDEPARTMENT_REPORT
CONSOLIDATE_COMMENTS
SCHEDULE_APPOINTMENT
SCHEDULE_INSPECTION
PREPARE_INSPECTION_PACKET
INGEST_INSPECTION_REPORT
PREPARE_RECOMMENDATION
PREPARE_COMMITTEE_AGENDA
PREPARE_DECISION_BRIEF
PREPARE_DEMAND
RECONCILE_PAYMENT
PREPARE_CERTIFICATE
PREPARE_ORDER
DIGITAL_SIGNATURE_HANDOFF
UPDATE_RECORD
DISPATCH_NOTIFICATION
START_SLA_WATCH
ESCALATE_SLA_RISK
PREPARE_HANDOFF
PREPARE_AUDIT_PACKET
CLOSE_CASE
START_RENEWAL_WATCH
START_APPEAL_TRACK
POST_DECISION_COMPLIANCE

## Automation boundary

Fully automatable with an authorized connector:
routing, extraction, record lookup, deterministic checks, duplicate checks, fee calculations, payment reconciliation, polling, reminders, SLA clocks, notifications, record sync, file assembly and audit packets.

Automatable preparation but human action/signature:
deficiency notices, official correspondence, inspection scheduling, inspection packets, recommendations, committee agendas, decision briefs, draft licences/certificates/orders and hearing packets.

Human statutory authority:
approvals/rejections requiring delegated authority, adjudication, hearings, legal findings, discretionary exceptions, official inspection findings, sanctions/penalties and judicial decisions.

Physical boundaries:
biometrics, mandatory physical appearance, driving tests, site inspection, physical measurement/sampling and witness/signature acts when legally required.

Aether should orchestrate these boundaries and resume the case automatically afterward.

## The deeper architecture

Objective
-> service/obligation identification
-> jurisdiction + competent authority
-> authoritative effective-dated rule pack
-> process archetype
-> evidence requirements
-> work atoms
-> connector actions
-> human/physical boundaries
-> parallel execution
-> exception/query loops
-> replanning
-> decision handoff
-> outcome + record update
-> renewal/compliance watch

The moat is not the service list. It is the ability to execute the same administrative work atoms across thousands of different services while changing only the rules, forms, authorities, evidence, timelines, routing and connectors.

## Next engineering target

The existing six-task administrative lane is a good foundation but is too generic. It should become a dynamic employee-work graph that can generate:

1. automatic assignment and workload routing;
2. verified auto-filled departmental forms;
3. a deficiency engine that explains exactly what failed and how to fix it;
4. query-response preparation with evidence citations;
5. resubmission diff and selective replanning;
6. inter-department request/response coordination;
7. inspection scheduling and inspection packets;
8. one-page statutory decision briefs;
9. fee/dues/demand and receipt reconciliation;
10. SLA prediction and escalation;
11. post-decision record update and notifications;
12. renewal/compliance scheduling.

Every prepared action should retain provenance. Every statutory act should remain attributable to the authorized officer. Production should fail closed when a required live connector or authoritative effective-dated rule is unavailable.
