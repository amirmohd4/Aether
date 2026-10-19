# Workflow Dossier EDU-01 — Scholarship Application to Verified Payment

**Research cut-off:** 17 October 2026  
**Status:** Desk-research dossier; not a validated live process map.  
**Initial focus:** India; scheme and state/UT must be specified before operational use.  
**Why this workflow:** Education is a long-term Aether vertical, and a CAG audit documents historical scholarship processing and payment delays, including Jammu & Kashmir. The dossier demonstrates how to investigate a service without assuming that every delay is a software problem.

## 1. Outcome

An eligible student receives the correct scholarship amount within the applicable scheme timeline, with a traceable eligibility decision, verified application, authorised sanction, successful payment and a clear grievance route.

Aether must not assume eligibility, make an adverse decision, or treat “submitted” or “sanctioned” as equivalent to “paid.”

## 2. Evidence and what it actually establishes

CAG Report No. 36 of 2025 reports that, in the audited data, 29.88 lakh post-matric scholarship beneficiaries across 14 States/UTs received payments with delays ranging from 1 to 89 months. It lists several causes, including defective applications and district-office delays in Gujarat and Jammu & Kashmir, administrative verification delays in Delhi, time-consuming checking/payment in Gujarat, and delayed release/non-availability of funds in some jurisdictions. It also notes that the Ministry had prescribed timelines in scheme guideline revisions and that delays persisted in the audited period.

Source: https://cag.gov.in/uploads/download_audit_report/2025/Report-No.-36-of-2025_Civil_English_03-02-2026-signed-069ca36644bcd89.99772695.pdf

**Interpretation:** There are multiple distinct bottlenecks. Aether may reduce defects, queue invisibility, hand-off delay and reconciliation work. It cannot create funds that have not been released, change scheme eligibility rules, or guarantee a payment date outside the responsible agency's control. The report is historical audit evidence, not proof of current performance in every scheme.

## 3. Likely end-to-end workflow to verify against a selected scheme

The exact steps, authorities, dates, portals and eligibility rules vary. Confirm each step from current scheme guidelines, the current portal, state/UT orders and programme officials.

1. **Scheme and academic-year setup**
   - Responsible department publishes scheme rules, eligibility, income/academic conditions, deadlines, documents, verification levels and sanction/funding process.
   - Aether research task: version the scheme rules by academic year, jurisdiction, effective date and source; do not reuse a stale rule pack.
2. **Student/institution application**
   - Student or authorised institution user submits the application through the relevant scholarship portal or assisted-service channel.
   - Inputs may include identity, enrolment, course, institution, category, income, bank/payment details and supporting evidence, depending on scheme.
   - Aether opportunity: guided intake, plain-language checklist, OCR/extraction and completeness checks before submission.
3. **Institution verification**
   - Institution verifies enrolment and other institution-controlled facts, then forwards, corrects or returns the application under the scheme rules.
   - Aether opportunity: detect missing fields, mismatched identifiers and overdue institution actions; prepare a reasoned query rather than a generic “defective” status.
4. **Department / district verification**
   - Authorised officials check eligibility evidence and required records; exceptions may be referred to another office or department.
   - Aether opportunity: assemble source-linked evidence, route by jurisdiction, track queue age, record exact return reasons and prevent duplicate work.
5. **Eligibility and sanction**
   - The competent programme/department authority applies the current rules and budget/sanction process.
   - Aether opportunity: prepare a decision-ready case file and deterministic rule-check results, identify unresolved conflicts, and log the authorised decision.
   - Boundary: only the authorised decision-maker can take a reserved eligibility/sanction decision.
6. **Fund availability and payment instruction**
   - Sanctioned cases proceed through the applicable fund-release, payment-file and treasury/bank processes.
   - Aether opportunity: reconcile counts and amounts between approved lists, payment instructions and acknowledgements; identify whether a case is awaiting verification, sanction, fund release or payment processing.
   - Boundary: Aether cannot solve an unavailable budget allocation or release funds without authority.
7. **Payment status reconciliation**
   - Payment result may be successful, pending, rejected, returned or otherwise unresolved, according to the payment rail's status vocabulary.
   - Aether opportunity: reconcile the authoritative payment response, classify the exception, route corrected details to an authorised operator and retry only when safe and permitted.
8. **Student notification and grievance**
   - Student receives an understandable status and, where needed, a request for correction or a legitimate grievance/appeal route.
   - Aether opportunity: multilingual, accessible notifications; precise pending reason; next required action; deadline; escalation and reopening loop.
9. **Closure and audit**
   - Case closes only when authoritative evidence supports the final state and the scheme's closure criteria are met.
   - Aether opportunity: produce a traceable record of rule version, evidence, decisions, payment reconciliation and actions.

## 4. Who does what today? To verify locally

| Actor | Likely responsibility | Evidence needed in field research |
|---|---|---|
| Student / guardian | Supplies application and correct evidence; responds to queries | Current scheme form, portal journey, common defect notices |
| School/college/institution verifier | Confirms institution-controlled facts and forwards/returns application | Official user manual, role permissions, queue reports |
| District / designated verification officer | Checks assigned applications and exceptions | Scheme-specific rules, office instructions, actual case walk-through |
| State/department programme team | Applies scheme rules, manages sanctions and programme oversight | Guidelines, order, workflow screen, exception reports |
| Finance / treasury / payment operator | Handles authorised financial stages and reconciles outcomes | Payment flow, status vocabulary, file formats, responsibility split |
| Bank/payment rail | Processes the authorised payment instruction and returns status | Official integration contract, acknowledgement/status codes |
| Grievance/appeal officer | Handles disputes, corrections and escalations | Official grievance route, service timelines, reopen process |

This role map is a hypothesis until confirmed for the chosen scheme. Do not assume the same official or system handles all stages.

## 5. Existing software and process to inventory

- National Scholarship Portal or the relevant state/UT/department scholarship portal, where applicable.
- Institution MIS and verification screens.
- State/department workflow or eOffice where used for exceptions and correspondence.
- Beneficiary/identity verification and permitted source-record services.
- Treasury, fund-release, DBT/payment and bank acknowledgement systems as applicable.
- Email, spreadsheets, downloadable lists, calls and physical file movement that occur outside the main portal.
- Helpdesk, Common Service Centre or institution assistance used by applicants.

Do not claim that a particular scheme uses all of these. Record exact system name, owner, user roles, data fields, supported APIs, access conditions, status semantics and official manuals.

## 6. Aether design for this workflow

**User promise:** “Know what is missing, who must act next, and whether the scholarship was actually paid—without repeated calls or visits to discover the status.”

- Pre-submit defect prevention: checklist and cross-field validation from the current official scheme pack.
- Evidence passport: provenance, purpose, consent/legal basis, freshness and reuse constraints.
- Work graph: application → institution check → district/department check → sanction → funds/payment → reconciliation → notification.
- Queue intelligence: distinguish work waiting for an official, missing applicant evidence, a system failure and unavailable funds.
- Exception-specific communication: explain exactly what is wrong and who can correct it.
- Safe automation: prepare and route tasks, invoke authorised interfaces, track acknowledgements and retry idempotently.
- Human decision boundary: eligibility, sanction, dispute and any reserved statutory action remain with the authorised official.
- Outcome proof: “paid” only when supported by authoritative payment evidence; otherwise show the precise confirmed state.
- Analytics: first-pass completeness, median/p90 time per stage, queue age, rework rate, percentage paid within timeline, exception categories and reopened cases.

## 7. Pilot baseline and acceptance measures

Collect at least a representative baseline over a defined period, including ordinary and exception cases.

- Application volume by scheme, academic year, district and institution.
- Percentage incomplete at first submission and top defect reasons.
- Median/p90 time at institution, district, department, sanction and payment stages.
- Staff minutes and number of manual touches per case.
- Percentage returned/reopened and number of repeat evidence requests.
- Sanction-to-payment time, returned-payment rate and reconciliation time.
- Applicant calls/visits or helpdesk contacts per case, if reliably recorded.
- Wrong-status rate and false “completed” rate.
- Access/security incidents and unauthorised record exposure (target zero).

**Pilot success requires:** a named programme owner; current official rule sources; a lawful data-access agreement; a sandbox or approved test environment; measurable baseline; no autonomous adverse decisions; and evidence that Aether improves a selected metric without worsening eligibility errors or excluding applicants.

## 8. Unknowns blocking production

- Which specific scheme and jurisdiction will be selected?
- What are the current official guidelines, deadlines, defect codes and appeals process?
- Which system is the authoritative record at each stage?
- What is the current live backlog and where does it accumulate?
- Can the programme share de-identified or synthetic test cases?
- Which APIs or approved integrations exist, and who can authorise access?
- Are delays currently dominated by defects, verification capacity, budget/fund release, payment issues or another cause?
- Who owns the budget and can sponsor a paid pilot?

## 9. Sources

- CAG Report No. 36 of 2025: https://cag.gov.in/uploads/download_audit_report/2025/Report-No.-36-of-2025_Civil_English_03-02-2026-signed-069ca36644bcd89.99772695.pdf
- NIC Integrated Shala Darpan (education administration and scholarship capabilities): https://www.nic.gov.in/project/integrated-shala-darpan/
- DARPG NeSDA Way Forward April 2026 report: https://darpg.gov.in/sites/default/files/NeSDA_WF_Apr2026_Report.pdf
