# Aether Administrative Workflow Research Register

**Updated:** 16 October 2026  
**Purpose:** Convert market research into a traceable list of workflows to validate.  
**Status:** Discovery hypotheses. No workflow below is marked as customer-validated or live-integrated.  
**Rule:** An official report can evidence a documented issue; it does not by itself establish current prevalence, buyer budget or willingness to pay.

## Prioritised discovery candidates

| ID | Sector / workflow | End-to-end lifecycle to map | Main friction hypothesis | Existing alternatives to inspect | Likely economic buyer | Aether wedge | Evidence / confidence | Key disconfirmation question |
|---|---|---|---|---|---|---|---|---|
| EDU-01 | Education — scholarship case and exception resolution | Application → institution verification → eligibility checks → district/state review → payment handoff → reconciliation → grievance | Incomplete files, repeated verification, opaque pending state, payment-status chasing | Scholarship portals, institution MIS, treasury/payment systems, spreadsheets, email, CSC/operator help | Education department/programme owner; possibly a programme implementation partner | Detect missing evidence early; track each authorised dependency; route exceptions; reconcile status to authoritative payment evidence | **Documented historical issue, current scope unvalidated.** CAG Report No. 36 of 2025 records delays in selected jurisdictions/cases | Which current scheme and jurisdiction has a measurable backlog and an authorised test route? Which steps cause the delay? |
| EDU-02 | Education — teacher/staff service lifecycle | Sanctioned post → recruitment/joining → service record → posting/transfer/deputation → leave/pay fixation/promotion → grievance/retirement | Multiple staff-service requests and records spread across administrative levels; repeated manual compilation | Shala Darpan or state HRMS, eOffice, payroll, spreadsheets and paper records | Directorate / department / district administration | One case graph across HR, finance and school records; evidence pack; lawful rule checks; employee-facing status | **Workflow existence documented.** NIC's Integrated Shala Darpan page lists several employee services; operational pain and procurement unknown | What portion of work is still manual despite existing HRMS? Can Aether integrate with the authoritative HR and payroll systems? |
| EDU-03 | Education — school grants and utilisation | Budget allocation → school plan → approval → procurement → invoice → utilisation certificate → audit | Fragmented evidence and late reporting may delay reconciliation and audit response | Finance systems, school MIS, procurement systems, spreadsheets and email | Department finance/programme owner | Evidence-linked grant graph, reconciliation, deadline monitoring, anomaly flags and audit packet | **Hypothesis** supported by known grant/accountability workflow; needs scheme-specific official sources | Are delays caused by process/software, late funds, procurement restrictions or capacity constraints outside Aether's control? |
| EDU-04 | Education — school infrastructure / maintenance | School request → inspection → estimate → sanction → procurement/work order → completion evidence → payment/closure | Schools, education officers, public works and finance may need to coordinate across systems | Asset registers, public works systems, eOffice, email, spreadsheets | Education infrastructure directorate / public works sponsor | Cross-department work graph with evidence and blocker attribution | **Hypothesis**; validate local process and whether a single owner can sponsor | Is the workflow repeatable enough across schools and does the buyer control the relevant systems? |
| GOV-01 | Public administration — grievance resolution | Intake → classification → department assignment → evidence request → investigation → action → response → satisfaction/reopen | Formal disposal can differ from meaningful resolution; recurring root causes may be poorly surfaced | CPGRAMS/state grievance portals, ticketing systems, email and call centres | Department grievance owner / DARPG or state equivalent | Cross-system case coordination, root-cause categories, reopened-case loop and verified resolution | **Official committee signal.** 161st Parliamentary Committee report (March 2026) recommends root-cause analysis and attention to reopened/unresolved cases | Which department has data access and authority to test actual resolution quality rather than closure counts? |
| GOV-02 | Public administration — interdepartmental file / approval | Receipt → scrutiny → case note → technical/finance/legal review → delegated decision → issue/dispatch → record | Digital files can still leave dependencies and follow-up spread across separate systems | eOffice, departmental case systems, email and registers | Secretary/department operations or digital-transformation sponsor | Process graph over existing eOffice and line-of-business systems; dependency/SLA analytics | **Digitisation already exists.** DARPG's public eOffice post reports high e-file and e-receipt digitisation | What work remains outside eOffice, and is a cross-system orchestration layer permitted? |
| GOV-03 | Government procurement and works — contractor bill readiness | Tender → award → agreement → work order → measurement → certification → running bill → deductions → payment → final settlement | Incomplete evidence, reconciliation and unclear blocker ownership can add rework and delay | eProcurement portals, finance/works systems, spreadsheets, document repositories and consultants | Contractor CFO/operations; government works department or implementation partner | Bill preflight, contract-linked evidence, milestone dependency map, exception and payment-status reconciliation | **Audit signals exist.** CAG public works audit records delay-attribution and contract-control issues in a specific state context | Will contractors pay for this if official portals and consultants already handle submission? Can actual bill status be read lawfully? |
| GOV-04 | Government procurement — tender qualification and bid pack | Tender discovery → eligibility interpretation → evidence collection → bid pack → submission → clarification → award | Tender requirements are dense, deadlines unforgiving and evidence reused across bids | eProcurement portals, tender aggregators, consultants, shared drives and spreadsheets | Contractor owner / tendering team | Tender-to-checklist compiler, reusable evidence passport, deadline/dependency tracking and pack validation | **Strong workflow plausibility; commercial demand unvalidated** | Which segments submit enough bids to justify software, and which actions must remain human-reviewed? |
| FIN-01 | Bank / NBFC — loan-file completeness | Application → consent → evidence collection → KYC/business checks → financial data → collateral checks → underwriting handoff → conditions → disbursement | Missing/inconsistent evidence creates manual query loops between LOS, providers and operations | LOS/LMS, core banking, bureau services, KYC providers, document systems and internal queues | COO / lending operations / transformation / technology | Orchestrate authorised evidence and exception work across existing LOS/LMS; provide source-linked file completeness | **Established software categories; exact unmet gap unvalidated.** RBI AI-risk guidance signals governance expectations | Which step has enough measurable manual work that incumbents cannot solve it cheaply? What API/data rights are available? |
| FIN-02 | Insurance — claim evidence and query coordination | Claim intake → policy checks → evidence → query → specialist review → authorised decision → settlement → grievance | Repeated queries and fragmented parties can prolong handling | Claims management, TPA platforms, provider portals, document systems | Claims operations leader / TPA | Coordinate evidence and query loops across authorised parties; reconcile final status | **Workflow established; pain and budget unvalidated** | Can Aether improve turnaround without changing the insurer's claims decision or duplicating TPA capability? |
| PROP-01 | Developer — permit dependency management | Project profile → jurisdictional applicability → land/title evidence → plans → NOCs → fees → inspection → correction → completion/occupancy | Several authorities and consultants may have separate requirements, queues and status mechanisms | Building approval portals, project-management tools, architects, lawyers, compliance consultants | Developer COO / project director / compliance lead | Project-level permit graph, evidence reuse, dependency critical path and authoritative status tracking | **Multi-authority model plausible; jurisdiction-specific requirements essential** | Which project types have the most costly coordination pain and an accessible authorised integration path? |
| BIZ-01 | MSME / industrial compliance | Entity profile → licence applicability → documents → applications → inspections → renewals → evidence retention | Multiple licences and renewals may be tracked across consultants and calendars | Accountants/company secretaries, compliance SaaS, ERP, spreadsheets and government portals | Owner/CFO/compliance head | Continuous obligation graph and evidence-linked renewal execution | **Hypothesis**; current provider pricing and buyer spend need collection | Is the main pain software, expert advice, rule ambiguity, or lack of official responsiveness? |
| PART-01 | Professional firms / system integrators — multi-client case operations | Client onboarding → authority/consent → case checklist → filing prep → status → query → closure | Staff repeatedly perform similar admin tasks across client portfolios | Practice-management software, CRM, email, spreadsheets and client portals | Practice leader / systems integrator | Multi-tenant workflow engine, reusable templates, case audit and client status views | **Hypothesis**; distribution potential depends on partner interviews | Will partners resell Aether or perceive it as a threat to billable service work? |

## Initial scoring framework

Score each candidate 1–5 after evidence is collected. Do not fill scores from intuition alone.

| Criterion | Weight | Evidence required |
|---|---:|---|
| Frequency and repeat volume | 15% | Case volume per month/year and recurring nature |
| Cost of delay/rework | 15% | Measured staff time, resubmissions, financing/project cost or SLA breaches |
| Buyer and budget clarity | 15% | Named budget owner, budget line or comparable procurement |
| Reachable design partner | 15% | Named organisation and willing process owner |
| Integration and data permission | 15% | Official API/sandbox or written authorised path |
| Repeatability across customers | 10% | Shared process despite jurisdiction differences |
| Implementation feasibility | 10% | Technical scope, security requirements and delivery time |
| Legal / safety risk (inverse score) | 5% | Clear rules and manageable consequence of error |

**Hard gates:** no live production data/action without written authority; no pilot without a named sponsor and baseline; no automation that bypasses statutory authority; no claim of savings without verified measurement.

## Minimum research record for every candidate

Create one record per actual workflow, not one per broad sector:

- Workflow ID, service name, jurisdiction, agency and source date.
- Official process source, rules/sections, effective date and confidence.
- Applicant eligibility and precise outcome.
- Step-by-step task graph, roles, hand-offs and approval authority.
- Forms, evidence, fees, SLA, status definitions and final system of record.
- Current software, APIs, vendors, consultants, manual workarounds and procurement evidence.
- Stakeholder quote or documented finding, exact source URL/date and role.
- Pain evidence, frequency, cost, affected population and counterevidence.
- Buyer, budget holder, security owner and procurement route.
- Allowed automated operations, required human actions and physical tasks.
- Integration access, data permissions, retention and security constraints.
- Pilot baseline, acceptance criteria, failure modes and decision.
- Status label: **desk-research signal / official evidence / stakeholder-confirmed / baseline-measured / pilot-verified**.

## Next research collection targets

1. Collect current scheme-specific manuals and application checklists for one scholarship workflow, one teacher-service workflow and one school grant workflow.
2. Collect a sample of recent public works tenders, contract conditions, running-bill forms, measurement/certification templates and payment status procedures.
3. Map one bank's SME or retail loan process using public vendor material and interviews; distinguish LOS features from cross-system work that remains manual.
4. Map one insurer/TPA claim workflow and identify which participant owns the administrative bottleneck.
5. Collect procurement tenders/contracts for relevant software categories and record actual disclosed prices only where available.
6. Review public posts and comments from officials, professional bodies, industry associations, vendors and users. Log date, role, claim, workflow, supporting evidence and whether it is a personal opinion or an official position.
7. Ask every interviewee to walk through a recent case from start to finish and identify the last three manual hand-offs, the most common rework reason, the authoritative completion signal, and who would approve spending on a solution.

## Source links

- e-Kranti / integrated services and workflow automation: https://www.pmindia.gov.in/en/news_updates/approach-and-key-components-of-e-kranti-national-e-governance-plan-2-0/
- NeSDA Way Forward, December 2025: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2217323&lang=1&reg=3
- Parliamentary Committee report on grievances and AI-enabled service delivery (March 2026): https://sansad.in/getFile/document/h_Press_releasefile/18/216/891P_2026_3_12.pdf?source=rajyasabha
- Integrated Shala Darpan: https://www.nic.gov.in/project/integrated-shala-darpan/
- Education Demand for Grants 2026–27: https://prsindia.org/budgets/parliament/demand-for-grants-2026-27-analysis-education
- CAG scholarship audit: https://cag.gov.in/webroot/uploads/download_audit_report/2025/Report-No.-36-of-2025_Civil_English_03-02-2026-signed-069ca36644bcd89.99772695.pdf
- CAG public works audit: https://cag.gov.in/uploads/download_audit_report/2025/Report-no.-02-MP-English-CAR---26-04-2025-1-0689480fd53fbd0.42233161.pdf
- India AI Governance Guidelines: https://www.pib.gov.in/PressNoteDetails.aspx?ModuleId=3&NoteId=157370&lang=1&reg=+3
- API Setu: https://apisetu.gov.in/
- DARPG eOffice LinkedIn post: https://www.linkedin.com/posts/department-of-administrative-reforms-and-public-grievances-government-of-india_year-end-review-2025-strengthening-digital-activity-7411396850597068800-ll6S
- DARPG e-Jagriti/process re-engineering LinkedIn post: https://www.linkedin.com/posts/department-of-administrative-reforms-and-public-grievances-government-of-india_negw-digitalgovernance-citizencentricservices-activity-7496536211113721856-D5HJ
- DARPG CPGRAMS AI chatbot LinkedIn post: https://www.linkedin.com/posts/department-of-administrative-reforms-and-public-grievances-government-of-india_cpgrams-aichatbot-goodgovernance-activity-7466085881452412928-v0Vs

## Decision rule

Do not choose the first vertical because it is easiest to demo or because it appears large. Choose it when the evidence identifies a recurring, expensive, reachable workflow; a buyer with budget; a safe authorised execution path; and a result that can be verified. The first product should be narrow in the workflow and broad in the reusable core.
