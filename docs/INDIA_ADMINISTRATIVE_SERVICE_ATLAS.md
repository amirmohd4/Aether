# Aether India Administrative Service Atlas
**Research cut-off:** 17 October 2026  
**Status:** Desk-research baseline; workflow hypotheses require service-level validation.  
**Purpose:** Map what government offices do, what systems are already used, who depends on the work, where Aether could help, and what evidence is still missing.  
**Scope:** Central, state/UT and local administration in India; education is a first-class long-term vertical. Judicial workflows are excluded.

## 1. The decision this atlas supports

Aether should not try to replace every government portal or automate every official decision. Build a cross-organisation **Administrative Execution OS** that coordinates the whole workflow across existing systems, staff and organisations, performs permitted digital work, handles exceptions, and verifies the result against the authoritative system.

The unit of research is a **specific workflow in a specific jurisdiction**, not a ministry name or a generic service category. “Building permission in jurisdiction X for building type Y” is researchable; “real-estate approvals in India” is too broad.

## 2. What the evidence says about India's starting point

India already has substantial digital public-service infrastructure:

- DARPG's NeSDA Way Forward April 2026 report tracks unified portals and service coverage across States/UTs. The report's state/UT data is as of 30 April 2026. It demonstrates broad digitisation, but does not mean every backend step is integrated or fully automated. Source: https://darpg.gov.in/sites/default/files/NeSDA_WF_Apr2026_Report.pdf
- A PIB release on 29 April 2026 reported 25,209 e-services across States/UTs and more than 81% saturation of the 2,124 mandatory e-services tracked by the framework. Source: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2256516&lang=2&reg=48
- NIC describes eOffice eFile as a workflow-based system managing the lifecycle of official documents/DAK from receipt to disposal, and describes dashboards and tracking in related modules. Source: https://www.nic.gov.in/project/eoffice/
- ServicePlus describes regulatory, statutory, developmental and consumer-utility service families, configuration of service workflows, reports and integration with other e-government systems. Source: https://serviceonline.gov.in/configuread/
- API Setu exists to support safe, governed interoperability, but its own description identifies gaps including API availability, proprietary protocols, common data standards and governance. Access and use are subject to the API publisher's authentication, authorisation, consent and policy requirements. Source: https://apisetu.gov.in/aboutus
- The National Government Services Portal describes Jammu and Kashmir's Online Building Permission System as a fully online service. This is a reminder to investigate what the existing portal already does before proposing a duplicate. Source: https://services.india.gov.in/service/detail/apply-for-online-building-permission-jammu-and-kashmir
- NIC's Integrated Shala Darpan description lists education administration capabilities including staff records, leave, annual performance reporting, pay fixation, transfers/deputation, grievances, vacancies, school information and scholarships. Education is not a blank slate either. Source: https://www.nic.gov.in/project/integrated-shala-darpan/
- CAG Report No. 36 of 2025 records historical delays in selected scholarship cases, including application defects, district/department verification delays, time-consuming processing and funding delays. It reported 29.88 lakh post-matric scholarship beneficiaries in 14 States/UTs with delays of 1–89 months in the audited data; these findings are specific to the report's period and scope, not a claim about every current scheme. Source: https://cag.gov.in/uploads/download_audit_report/2025/Report-No.-36-of-2025_Civil_English_03-02-2026-signed-069ca36644bcd89.99772695.pdf
- The Department of Expenditure publishes a Manual for Procurement of Works, Second Edition 2025 and subsequent amendments, including an amendment dated 18 June 2026. Contractor workflows must be mapped against current procurement rules and amendments, not generic assumptions. Sources: https://doe.gov.in/en/manuals and https://doe.gov.in/en/circulars/amendment-manual-procurement-works-second-edition-2025

**Conclusion:** Aether's opportunity is not “government has no software.” It is the remaining work between portals, systems of record, people, evidence, dependencies and authoritative outcomes. This gap must be demonstrated workflow by workflow.

## 3. A common model of how administrative work happens

A typical case may pass through some, but not necessarily all, of these stages:

1. **Demand/intake:** application, letter, referral, grievance, tender, staff request or system event.
2. **Registration and routing:** diary/inward number, case ID, service/category and responsible unit.
3. **Applicability and completeness:** identify the correct jurisdiction, eligibility, documents, fees and rules.
4. **Evidence retrieval and verification:** validate source, identity, business/land/school/financial records and freshness.
5. **Case preparation:** caseworker reviews facts, performs calculations, drafts a note or recommendation, and records exceptions.
6. **Specialist checks:** technical, medical, legal, finance, audit, field inspection or another department as applicable.
7. **Authorised decision:** the designated official/committee accepts, rejects, sanctions, requests changes or records another permitted outcome.
8. **Execution:** issue an order/certificate, post a record, pay/disburse, create a work order or update a system of record.
9. **Notification and follow-up:** communicate status, request missing evidence, track deadlines and escalate under approved rules.
10. **Reconciliation and closure:** verify the authoritative state, reconcile payment/record/order, archive evidence and measure elapsed time/rework.
11. **Review/appeal/audit:** handle reopened cases, appeals, inspection findings, audit queries and retention obligations.

Not all services follow this sequence. Some are instant self-service; some require statutory review, physical inspection, public notice, payment, consultation or an appeal. The process pack must encode the actual service's rules and exceptions.

### Typical office roles

- Inward/diary or front-desk staff: register, classify and route.
- Dealing assistant/caseworker: check evidence, consult records, prepare file notes, request clarifications and track the case.
- Technical/specialist officer: validate professional/technical conditions or inspect.
- Accounts/finance: check budget, fees, deductions, sanction and payment records.
- Section head/manager: review, return, recommend or supervise.
- Competent authority: take a decision within delegated statutory/financial authority.
- Dispatch/records/IT staff: issue communication, update records, preserve the file and support the systems.

This is a role model, not a universal organisation chart. Aether should automate repeatable preparation and coordination but preserve the authority of the legally competent decision-maker.

## 4. Service and workflow atlas

The table below is a first-pass national map. Each row is a **workflow family** that must be decomposed into actual services, laws, forms, portals and jurisdiction-specific steps before production automation.

| Domain / department family | Representative workflows to inventory | Existing systems and methods to investigate | Main candidate pain (hypothesis, not universal fact) | Aether opportunity | Buyer / payer candidates | Hard boundaries |
|---|---|---|---|---|---|---|
| **1. General administration / eOffice** | Receipt/DAK; file movement; interdepartmental reference; note preparation; approval; dispatch; record retention | eOffice/eFile, departmental portals, email, registers, document repositories, spreadsheets | A file is digital but still waits on dependencies or another system; status and evidence are fragmented | Orchestrate tasks across eOffice and line-of-business systems; draft summaries; flag blockers; verify closure | Department, state IT agency, system integrator | No bypass of delegation, secrecy, retention or official decision authority |
| **2. Citizen certificates / e-District** | Birth/death, income, residence, caste/category, domicile, legal-heir or other locally provided certificates | State e-District/ServicePlus portals, municipal/registrar records, local registers, CSC/assisted-service channels | Missing documents, repeated verification, status ambiguity; varies by service | Preflight documents, reuse permitted evidence, route verification, notify applicant, verify issuance | State/UT department, district administration, e-governance agency | Eligibility and certificates depend on local law and authoritative records |
| **3. Revenue / land records** | Record-of-rights copies, mutation, land demarcation, ownership/encumbrance evidence, land-use changes, revenue certificates | State land-record systems, registration systems, e-District, maps, physical records, local revenue offices | Data mismatches, multi-office dependency, manual record checks | Link evidence and requests across systems, track mutation/objection/verification dependencies, prepare case packs | Revenue department; banks/developers may pay for their own permitted verification workflow | Do not infer legal title from an unverified copy; disputes, hearings and field measurement require authorised people |
| **4. Urban local bodies / municipal services** | Trade licences, property tax, water/sewer connections, building permission, completion/occupancy, complaints | Municipal portals (e.g. e-Nagar in some states), OBPS/building approval systems, billing systems, inspectors, email | Multiple permissions, unclear applicability, repeat document submission | Project/case dependency graph, fee and document preflight, inspection scheduling and result tracking | Municipal body/state urban department; developers/MSMEs for their own workflow | Zoning, inspections, statutory notice and final approval remain with competent authorities |
| **5. Education administration** | Scholarships; student transfers; admissions and records; teacher service book; leave; transfer/deputation; pay fixation; recruitment; school grants; infrastructure; grievance | Shala Darpan or state EMIS/HRMS, scholarship portals, treasury/payment systems, eOffice, spreadsheets, school records | Repeated verification and handoffs; late processing may stem from defective applications, staffing, budget release or portal schedules | Evidence-complete scholarship files; exception resolution; employee service lifecycle; school-grant reconciliation; cross-office infrastructure coordination | Education directorate/ministry, state IT agency, programme implementation partner | Do not infer eligibility or alter student/teacher records without authority; funding shortages cannot be solved by workflow automation alone |
| **6. Social welfare / benefits** | Pensions, disability/elderly benefits, housing schemes, ration/PDS, worker benefits, DBT and appeals | Scheme portals, beneficiary registries, Aadhaar-enabled or bank payment rails where authorised, local verification, CSCs, treasury | Eligibility checks, identity/record mismatch, verification queues, payment reconciliation | Detect missing evidence, route verification, reconcile sanctioned vs paid, identify stuck cases and notify | Welfare department/programme owner, state/central government, implementation agency | Sensitive personal data; consent/legal basis, exclusion-risk monitoring, human appeal and grievance path |
| **7. Health administration** | Facility registration, scheme empanelment, provider credentialing, public health procurement, claims/benefit administration, licences | Health portals, hospital information systems, insurer/TPA platforms, finance systems, paper records | Multi-party records, evidence queries, inconsistent coding, claim/payment status | Coordinate authorised evidence and query loops, reconcile records and hand off medical judgment | Health department, insurer/TPA, provider network, system integrator | Medical judgment, emergency care, patient privacy and coverage decisions require applicable safeguards |
| **8. Public works / infrastructure** | Project proposal; estimate; administrative/technical sanction; tender; work order; measurement book; running/final bill; completion; defect liability | eProcurement, departmental works software, finance/treasury, spreadsheets, signed measurement records, email | Dependencies across engineering, finance and contractor; bill evidence and status can be fragmented | Contract-to-payment graph, bill preflight, reconciliation, milestone/inspection evidence and blocker ownership | Works department, contractor, EPC firm, project-management company | No fabricated measurement/certificate; physical inspection and authorised certification remain human work |
| **9. Procurement / goods and services** | Procurement plan; tender; vendor registration; bid qualification; evaluation; purchase order; delivery/inspection; invoice; payment; debarment checks | GeM, CPPP/state eProcurement, ERP, finance systems, vendor portals, spreadsheets | Requirement ambiguity, bid-pack errors, duplicate entry, delivery-to-payment gaps | Tender-to-checklist compiler, vendor evidence passport, contract milestones, invoice reconciliation | Government procuring entity; vendors and contractors for their own internal work | Fair competition, conflict-of-interest rules, evaluation independence, audit trail and procurement rules |
| **10. Finance / treasury / grants** | Budget allocation; sanction; bill passing; grants; utilisation certificates; refunds; pension/payroll; payment reconciliation | IFMS/treasury, PFMS or scheme systems where applicable, ERP, bank rails, spreadsheets | Sanction, evidence and payment states can differ; reconciliation is laborious | Match sanction → bill → payment; flag discrepancies; assemble utilisation/audit packs; monitor deadlines | Finance department, grant programme owner, enterprise finance team | No unauthorised payments, sanctions or changes to financial records; dual control where required |
| **11. Tax / commercial tax** | Registration; returns; refunds; notices; assessments; replies; certificates | GST/common tax portals, accounting software, tax practitioner systems, document storage | Data collection, reconciliation and notice-response work | Gather authorised evidence, reconcile source data, prepare draft filings/replies and deadlines | MSMEs, tax/accounting firms, enterprises; public agency only through formal procurement | Tax advice and submissions require appropriate authorisation; tax authority decisions cannot be automated by Aether |
| **12. Corporate affairs / business registration** | Incorporation; director/company changes; annual filings; charges; certificates and record checks | MCA portal, company-secretarial software, accounting systems, professional firms | Repeated document packs and cross-checking among company records | Maintain obligation graph, prepare evidence pack, monitor due dates and reconcile filing acknowledgements | Companies, company secretaries, compliance firms, lenders | Legal declarations/signatures and professional certifications must remain properly authorised |
| **13. Labour / employment / social insurance** | Establishment registrations, PF/ESI processes, employee onboarding/exit, claims, inspections, returns | EPFO/ESIC portals, HRMS/payroll, accounting systems, consultant spreadsheets | Repeated employer/employee evidence and deadline coordination | Employee lifecycle workflow, discrepancy detection, evidence and renewal tracking | Employers, payroll providers, compliance firms | Sensitive employment/health data, statutory determinations and inspections |
| **14. Transport / road / vehicle** | Registration, permits, fitness, licences, tax, challans, fleet renewals, transfers | VAHAN/SARATHI and state systems, fleet software, transport office records | Fleet-scale expiries, multiple vehicle records and status follow-up | Fleet obligation graph, authorised status retrieval, renewal pack and expiry risk management | Fleet/logistics operators, dealers, insurers, transport agencies | Only authorised records access; physical fitness tests and licensing decisions stay with authorities |
| **15. Environment / pollution / industrial safety** | Consent to establish/operate; renewals; monitoring reports; inspection findings; environmental approvals | State Pollution Control Board portals, PARIVESH for relevant clearances, consultant tools, monitoring systems | Many permit conditions, evidence dates and renewal dependencies | Permit/condition graph, evidence tracking, alerting, inspection action closure | Industry, infrastructure developer, compliance consultants, relevant authority | Cannot substitute for actual monitoring, impact assessment or independent regulatory judgment |
| **16. Fire / food / local business licensing** | Licence applications and renewals; inspection; corrective action; certificate issuance | State/local portals, FSSAI FoSCoS for food-related work, inspection records, consultants | Document completeness and renewal/inspection coordination | Applicability and checklist engine, inspection follow-up, evidence tracking | Restaurants, retailers, factories, hospitals, hotels; local agencies via procurement | Do not certify safety or food compliance without prescribed checks and authority |
| **17. Utilities / energy / water** | New connection; load enhancement; meter/billing dispute; deposit/refund; street/utility permission | DISCOM/utility CRM and billing, work-order systems, contractor apps, municipal records | Field work and digital records not always synchronised | Coordinate application → site visit → estimate → payment → installation → meter/connection status | Utilities, developers, industrial/commercial customers | Field installation and safety checks require authorised staff; outages and physical constraints remain external |
| **18. Police / permits / local enforcement (non-judicial)** | Character/police verification where lawful; event permissions; lost-property reporting; licence verification | Departmental case systems, citizen portals, station registers, identity/record systems | Status and inter-office evidence can be difficult to coordinate | Document routing and status coordination for explicitly permitted non-investigative processes | Government agency via procurement; regulated employers for permitted checks | No surveillance expansion, unauthorised sensitive-data access, automated guilt/risk judgments or interference with investigations |
| **19. Grievance / public complaints / appeals** | Intake; classification; assignment; evidence request; investigation; action; response; satisfaction; reopening; root-cause analysis | CPGRAMS/state portals, departmental ticketing, email, call centres | Closure may not mean resolution; reopened and recurring issues need root-cause visibility | Cross-system case orchestration, evidence-backed resolution, recurring-cause detection, reopening loop | Department/agency, service operator, enterprise support teams | Preserve due process, appeal routes, privacy and independent review |
| **20. Government employee administration** | Recruitment; joining; service records; transfer/posting; leave; appraisal; promotion; training; payroll; pension; grievance | HRMS, eOffice/SPARROW, payroll, establishment registers and spreadsheets | Staff records and approval workflows may span units and finance | Employee service graph, rules-based completeness, status and hand-off tracking | Government HR/establishment directorate; enterprise HR teams | Employment decisions and sensitive records require lawful policy, authorised review and audit |
| **21. Banks / NBFCs** | Loan origination; KYC/evidence; bureau/financial data; collateral/title checks; underwriting; conditions precedent; disbursement | LOS/LMS, core banking, KYC and bureau providers, document systems, internal queues | Manual evidence and query loops across multiple vendors/systems | Orchestrate authorised evidence, identify discrepancies, build source-linked loan file, route exceptions | Bank/NBFC COO, lending operations, transformation/technology | No unauthorised data access, fabricated evidence, bypassed KYC or unapproved credit decisions |
| **22. Insurance / TPAs / healthcare providers** | Claim intake; policy and document checks; query loop; specialist review; settlement; grievance | Claims platforms, TPAs, hospital systems, provider portals, document systems | Repeated queries and fragmented parties can delay handling | Evidence completeness, query coordination, reconciliation and verified status | Insurer, TPA, provider network | Preserve medical/claims judgment, privacy, fair treatment and authorised decisions |
| **23. Developers / real estate** | Project applicability; land/title evidence; building plan; NOCs; fees; inspections; completion/occupancy; renewals | Building approval portals, project-management tools, architects/engineers, consultants | Different authorities and prerequisites create project-level dependency risk | Project permit graph with critical path, reusable evidence and authoritative status | Developer COO/project director, EPC/project-management firm | Requirements jurisdiction-specific; do not claim approval or legal title without authoritative evidence |
| **24. MSMEs / manufacturers / logistics** | Business setup; permits; renewals; employee compliance; vehicles; tax; environmental and utility work | ERP/accounting, compliance SaaS, consultants, spreadsheets, government portals | Multiple obligations and evidence dates are spread across systems and advisers | Continuous compliance graph and assisted execution | Owner/CFO/compliance head, industry association, payroll/accounting partner | Avoid pretending one national rule applies to all states or business types |
| **25. Professional firms / system integrators** | Multi-client onboarding, filing packs, status management, query handling and closure | CRM/practice management, email, spreadsheets, client portals | Repetitive administration across a portfolio of cases | Multi-tenant workflow templates, reusable evidence with permission, case status and audit | CA/CS/legal/compliance practice; SI and BPO providers | Preserve client authority, professional obligations and separation of tenant data |

## 5. Existing systems: how Aether should relate to them

Aether should classify each existing system rather than call everything a competitor:

- **System of record:** authoritative database for a certificate, loan, employee, payment, claim or approval. Aether should not silently replace it.
- **Portal / channel:** receives applications or displays status. Aether may prepare and coordinate work around it.
- **Workflow / case management:** routes tasks within a defined organisation or service. Aether must prove cross-system value beyond this.
- **ERP / core platform:** owns financial, HR, loan, claims or operational transactions. Integrate through authorised interfaces.
- **RPA / desktop automation:** operates a user interface. Use only when permitted and reliable; UI automation is fragile and must not evade access controls or terms.
- **Consultant / outsourcing / assisted-service channel:** supplies expertise, document preparation, representation or local access. Aether may augment rather than displace it.
- **API/data provider:** supplies a specific verification or transaction. Check consent, contract, API scope, rate limits, source quality and audit obligations.
- **Manual work:** paper registers, spreadsheets, calls, visits, email and messaging. Automate only after understanding why the workaround exists and whether the process is lawful and stable.

For every named vendor, capture the exact product, module, customer segment, capability, integration method, public price or contract evidence, and a counterargument for why the buyer might not need Aether. Do not use a vendor name as proof that a buyer will pay.

## 6. What should be automated, and what should not

### Automate by default where authorised and testable
- Intake classification and extraction, with confidence thresholds.
- Document completeness and consistency checks against effective-dated rules.
- Evidence collection/reuse where lawful, consented and purpose-limited.
- Calculations and reconciliation with deterministic tests.
- Draft notes, letters, checklists, case summaries and responses.
- Task creation, routing, reminders, deadlines, retries and escalation.
- Duplicate detection and safe idempotent submissions.
- Status tracking and reconciliation against authoritative records.
- Reporting, root-cause clustering and process-performance measurement.

### Use human approval or professional review where required
- Statutory decisions, sanctions, licensing, rejection and appeal outcomes.
- Credit/insurance/benefit decisions with legally or contractually reserved authority.
- Medical, engineering, legal or other professional judgments.
- High-impact exceptions, ambiguous rules, conflicting records and low-confidence evidence.
- Payments, signatures, declarations and actions requiring a named authorised person.
- Inspections, site measurements, safety checks and other physical tasks.

### Do not build
- An unrestricted “AI employee” with blanket credentials.
- A system that bypasses official portals, access controls or procurement rules.
- Silent auto-rejection of citizens or automated adverse decisions without the legally required process.
- A duplicate portal for services already delivered effectively without a proven cross-system gap.
- A workflow that claims success because it submitted a form rather than verifying the authoritative outcome.

## 7. Where to start: a disciplined wedge decision

Candidate workflows for field validation—not a final product commitment:

| Candidate | Why it merits study | First buyer hypothesis | Initial low-risk product slice | Critical validation |
|---|---|---|---|---|
| Contractor tender-to-bill readiness | Repeatable, document-heavy, links to bid success and cash flow | Contractor operations/CFO; later works department | Tender requirements → evidence checklist → bid pack validation; or contract-to-bill preflight | Does the buyer experience enough avoidable rework to pay? Can official status be accessed lawfully? |
| Education scholarship exception resolution | Official audit documents historical verification/payment delays and multiple hand-offs | Education programme owner / state IT agency | Detect defects, route exceptions, track sanctioned-to-paid reconciliation in a sandbox | What is the current scheme-specific bottleneck? Is there a sponsor and lawful data path? |
| Developer permit dependency management | Multi-authority project workflow can have high delay costs | Developer/project director | Jurisdiction-specific permit checklist and project dependency tracker | Can we model current rules accurately and access statuses? |
| Bank loan-file completeness | High-repeat institutional process and existing systems to integrate | Lending operations / COO | Evidence completeness and discrepancy workbench over a sandbox or authorised sample | What is the measurable gap versus LOS/KYC vendors? |
| Employee service workflow in education/public administration | Repeated leave, transfer, pay-fixation and service-record cases | Department HR/establishment owner | Case completeness, rule-versioned routing and status visibility | What remains outside existing HRMS/eOffice and who can sponsor integration? |

### Selection score (evidence only)

Score each workflow 1–5 with a linked source or interview note:

- Case frequency and repeat volume — 15%
- Cost of delay, staff time and rework — 15%
- Named budget owner and comparable spend — 15%
- Reachable design partner — 15%
- Legal access and integration path — 15%
- Repeatability across customers — 10%
- Delivery feasibility/security scope — 10%
- Manageable consequence of error (inverse risk) — 5%

**Hard gates:** no production data or live action without written authorisation; no claimed savings without a measured baseline; no pilot without a named process owner; no automation that bypasses statutory authority; no production rule pack without source, effective date, owner and review process.

## 8. Evidence and field-research plan

For each actual service, create a structured record containing:

1. Service name, ID, agency, jurisdiction, target user and outcome.
2. Legal basis, official rule/manual/circular, effective date and source URL.
3. Official application form, document checklist, fee, published service level and status definitions.
4. Step-by-step current process: applicant action, each employee role, each system, handoff, approval and final record.
5. Existing portal/system/vendor, exact capability, procurement/contract evidence and any public price.
6. Manual workarounds, repeat visits/calls, common defects, returned files, re-openings and exceptions.
7. Actual case volume, median and p90 time, staff minutes, touch count, first-pass completeness, rework and error rate.
8. Buyer, budget line, procurement route, security requirements, data controller and decision-maker.
9. Integration/API availability, test environment, permission, rate limits, audit and data-retention conditions.
10. Proposed Aether tasks, automation boundary, human checkpoint, verification evidence and rollback/recovery plan.
11. Baseline and pilot acceptance metrics, source of truth, counterevidence and reasons the opportunity may not exist.
12. Interview notes and quotes with date, role and consent; public posts are leads, not representative evidence.

### Source hierarchy

1. Current statute, regulation, official government order/circular, service rules and official manual.
2. Official service portal, form, charter, API documentation and system guidance.
3. CAG/Parliamentary Committee/department audit and official performance reports.
4. Procurement tenders, awarded contracts, budget documents and official vendor case studies.
5. Recorded interviews with the actual process owner, front-line employee, applicant and buyer.
6. Reputable reporting and stakeholder association statements.
7. Public social posts, forums and complaints as discovery leads only; verify independently.

### Research cadence and outputs

- **Stage 1 — Desk map:** service families, source links, current portals, existing systems and obvious exclusions.
- **Stage 2 — Deep process dossiers:** step-level workflow maps for selected services; role, document, rule, fee, SLA, handoff and exception.
- **Stage 3 — Market map:** incumbent vendors, consultants, procurement, pricing evidence, buyer roles and integration constraints.
- **Stage 4 — Field validation:** structured interviews, observed cases and measured baselines.
- **Stage 5 — Wedge score:** evidence-weighted ranking, counterevidence and explicit go/no-go.
- **Stage 6 — Pilot specification:** authorised data path, sandbox/connector plan, human boundaries, acceptance criteria, security and rollback.

This atlas is a baseline, not a claim that every Indian service has been individually mapped. The next unit of work is to turn the highest-ranked rows into jurisdiction-specific dossiers with official evidence and real operator interviews.

## 9. Reference sources

- DARPG NeSDA Way Forward April 2026 report: https://darpg.gov.in/sites/default/files/NeSDA_WF_Apr2026_Report.pdf
- PIB / DARPG 25,209 e-services report, 29 April 2026: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2256516&lang=2&reg=48
- NIC eOffice: https://www.nic.gov.in/project/eoffice/
- ServicePlus: https://serviceonline.gov.in/configuread/
- API Setu: https://apisetu.gov.in/aboutus
- NIC Integrated Shala Darpan: https://www.nic.gov.in/project/integrated-shala-darpan/
- CAG Report No. 36 of 2025: https://cag.gov.in/uploads/download_audit_report/2025/Report-No.-36-of-2025_Civil_English_03-02-2026-signed-069ca36644bcd89.99772695.pdf
- Department of Expenditure procurement manuals: https://doe.gov.in/en/manuals
- Department of Expenditure 2026 amendment to Works Manual: https://doe.gov.in/en/circulars/amendment-manual-procurement-works-second-edition-2025
- J&K Online Building Permission System service listing: https://services.india.gov.in/service/detail/apply-for-online-building-permission-jammu-and-kashmir
- API Setu API documentation: https://docs.apisetu.gov.in/document-central/explore-apisetu/Introduction.html

## 10. Decision record

**Product direction:** one cross-sector Administrative Execution OS with a shared execution/governance core and versioned vertical workflow packs.

**Not the product:** chatbot only, generic RPA only, portal replacement, or an unbounded agent with no human/legal controls.

**Research status:** initial public-source desk map completed; not exhaustive; no buyer willingness-to-pay percentage is justified yet.

**Next proof required:** one current workflow, a named buyer/process owner, a lawful integration/data path, measured baseline, and a controlled pilot showing verified outcome improvement.
