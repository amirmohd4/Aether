# Aether stakeholder pain-point research — October 2026

This note converts public evidence from government departments, parliamentary
committees, trade bodies, and current reporting into product requirements.
It is not a legal or policy opinion.

## 1. Approvals and NOCs still take too long

The Parliamentary Standing Committee on Commerce's 201st Report (7 August 2026)
said stakeholders continued to experience time-consuming approval and NOC
processes and recommended wider single-window digital clearance, delegation,
and time-bound/faceless delivery where feasible.

**Aether response:** treat a business/project objective as one cross-department
case, automatically build the approval dependency graph, prepare each
department handoff, monitor the clock, and surface only the exception or
statutory decision to staff.

Source:
https://www.pib.gov.in/PressReleasePage.aspx?PRID=2296240

## 2. Government already has e-office, but file movement itself needs analytics

DARPG's February 2025 Secretariat Reforms note directed departments to develop
e-Office analytics for file disposal, lateral movement and pendency, including
subject-specific delay analysis, and advised against proliferation of part-files.

**Aether response:** maintain one durable case identity and one evidence trail;
show dependency age, owner/department, rework, and next action; avoid spawning
separate administrative "part-files" for the same case.

Source:
https://darpg.gov.in/sites/default/files/SecReformsFeb2025.pdf

## 3. J&K has an explicit problem with unanswered communications

A J&K Department of Skill Development circular dated 2 March 2026 said repeated
reminders were not resolving several critical queries and instructed Heads of
Departments to meet timelines. Where a full reply requires data compilation or
field reports, it directed an interim response with the reason for delay and a
definitive timeline.

**Aether response:** generate interim progress replies automatically, preserve
the dependency, send the exact missing-data/field-report request, and escalate
only when the policy threshold is reached.

Source:
https://dsd.jk.gov.in/circular/CO%2002%20of%202026.Pdf

## 4. Citizen-facing portals can fail and create repeat visits

A June 2026 report on Ludhiana Sewa Kendras described recurring E-Sewa portal
slowness that produced backlogs and forced residents, including students and
parents, to make repeated visits. A separate June 2026 Pune report described
MahaOnline login failures and sluggishness leaving certificates pending during
admission and scholarship periods.

**Aether response:** make the case durable before submission, keep the verified
data/evidence in the case, make external submission resumable, and never ask
the user to recreate a completed packet just because a downstream portal
failed.

Sources:
https://timesofindia.indiatimes.com/city/ludhiana/queues-swell-at-sewa-kendras-as-server-slump-disrupts-services/articleshow/132001717.cms
https://timesofindia.indiatimes.com/city/pune/mahaonline-glitches-disrupt-rts-services-hit-students-during-admission-season/articleshow/131712047.cms

## 5. J&K already exposes the useful bottleneck dimensions we should automate around

The official J&K ServicePlus dashboard separates pending applications by
"Pending with Applicant" and "Pending with official", and further separates
cases within and beyond the Public Service Guarantee Act timeline. Its
September 2026 dashboard snapshot showed 391 services, 9.49 million total
applications, and 880k+ under process.

**Aether response:** classify every blocked case into applicant, departmental,
inter-departmental, field, connector, payment, or statutory-decision wait;
show exactly what is required to unblock it; and route the next action to the
right owner.

Source:
https://jansugam.jk.gov.in/databoard

## 6. Grievances should be routed, not bounced

DARPG's public-grievance guidelines say grievances should follow a
"whole-of-the-government" approach: a department should not simply close a
grievance because it does not pertain to that office; it should transfer it to
the right authority. The guidelines also note that additional documents can be
requested through CPGRAMS instead of closing the grievance for lack of them.

**Aether response:** route by subject/jurisdiction, preserve the case history,
request only missing evidence, and keep an auditable transfer chain.

Source:
https://www.darpg.gov.in/sites/default/files/Comprehensive%20guidelines_for_handling_the_Public_Grievances.pdf

## 7. Cross-system data visibility failures can delay benefits even after the process changes

FIEO's July 2026 feedback notice reported exporter problems with visibility of
Shipping Bills and Cargo Identification Numbers in DG Systems, contributing to
delays in export incentives and refunds. FIEO's September 2026 consultation
request specifically invited suggestions on delay, duplication, digitisation
and ICT improvements in customs clearance.

**Aether response:** add data-lineage and reconciliation as first-class work:
detect an "orphan" record, identify the last known system, preserve the
corresponding case packet, and automatically assemble the next escalation or
follow-up.

Sources:
https://fieo.org/en/view_section.php?id=0%2C2993%2C3011%2C3136&lang=0
https://fieo.org/en/events/uploads/uploads/uploads/directcontent/auth/events.php?dcd=14195&evetype=0&id=0%2C22&lang=0

## 8. High-volume portals need operational recovery, not only a helpdesk

MCA reported in February 2026 that its V3 portal handled about 3.84 crore
filings during 2021–2025. In FY2025-26 up to 31 January 2026, 3,16,877 helpdesk
tickets were raised; the ministry reported about 98% successful resolution.

**Aether response:** treat portal errors as recoverable workflow events:
capture the failed operation, keep the prepared data packet, retry according to
policy, and give the user a meaningful status rather than forcing another
submission.

Source:
https://www.pib.gov.in/PressReleasePage.aspx?PRID=2226017

## 9. Field staff workloads can become the bottleneck

A September 2026 report described Booth Level Officers in Delhi reporting very
long workdays while balancing election-roll field duties and their regular
responsibilities.

**Aether response:** where field verification is legally required, Aether
should prepare the visit packet, pre-validate the digital evidence, batch
low-risk/repeatable checks, surface only anomalies to the field worker, and
automatically feed the signed/authoritative field result back into the case.

Source:
https://www.hindustantimes.com/india-news/amid-new-ec-rules-delhi-blos-struggle-to-balance-exams-sir-duty-and-13-hour-work-days-101790641341400.html

## Product requirements derived from the evidence

1. One case identity across all departments.
2. One evidence packet, with provenance and deduplication.
3. "Ask once" data collection; reuse verified facts inside the case and offer
   reusable evidence for future cases only with explicit user authorization.
4. Automatic completeness checking before submission.
5. Automatic routing and ownership.
6. Inter-department request packets with durable follow-up.
7. Interim response generation when a reply depends on data or field work.
8. SLA countdown by responsible party, not just one overall timer.
9. Exception-aware automatic retry/replan without resetting completed work.
10. Cross-system reconciliation and orphan-record detection.
11. Operator cockpit focused on exceptions, statutory judgment and field work.
12. Mobile-first citizen experience with one clear next action.
13. Portal-failure recovery so citizens never repeat already completed work.
14. Full audit/evidence lineage for every automated action.
15. Explicit production connector permissions per department and operation.
