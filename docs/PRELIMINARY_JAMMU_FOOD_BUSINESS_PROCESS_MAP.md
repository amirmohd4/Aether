# Preliminary Process Discovery: Small Food Business in Jammu

**Status:** research draft; not an authoritative legal checklist, not production rules, and not evidence that all listed approvals apply to every business.

## Why we are mapping this before coding

The official Jammu Municipal Corporation (JMC) website already provides an online NOC/licence system. Its official 26 March 2021 announcement says its online services include online application, department receipt, document/fee verification, officer escalation, status tracking, online payment and digitally signed outputs. FSSAI operates FoSCoS for food-business licensing/registration and application tracking. J&K also has a Single Window System and NSWS lists approvals for J&K.

This means Aether must not duplicate a portal. The unresolved question is whether a business-opening journey across these systems has coordination gaps that an authorised execution layer can reduce.

## Official sources checked

1. JMC online NOC/licence form: https://www.jmc.jk.gov.in/NOCForm.aspx
2. JMC official release on online e-services (26 March 2021): https://www.jmc.jk.gov.in/newsdetail.aspx?id=389
3. JMC e-governance portal: https://www.jmc.jk.gov.in/
4. J&K Single Window System: https://singlewindow.jk.gov.in/
5. NSWS J&K approvals and Know Your Approvals: https://www.nsws.gov.in/portal/jammukashmir
6. FSSAI FoSCoS apply/renew/track: https://foscos.fssai.gov.in/
7. FSSAI food-business services and guidance: https://www.fssai.gov.in/business

## Preliminary journey map

| Stage | What is established from official sources | What remains unverified |
|---|---|---|
| 1. Describe the business | NSWS offers a Know Your Approvals route; FoSCoS asks for business/location details and provides eligibility and document guidance. | Whether these tools identify the complete approval path for the exact JMC location and business profile. |
| 2. Determine food-safety registration/licence | FoSCoS provides new application, renewal, modification, eligibility, documents, fee information, application processing guidance and tracking. | Exact category, documents, fee, inspection path and current rules for the proposed business; these depend on current official eligibility and must be verified. |
| 3. Determine municipal NOC/licence needs | JMC provides an online NOC/licence system; its form asks for personal details, establishment name, location, licence/NOC type and selected attachments. | Which specific JMC approval applies to the selected business, current checklist, fee, timeline, responsible unit and status/response semantics. |
| 4. Check other approvals | NSWS and J&K Single Window provide approval discovery. | Whether any additional authority is legally relevant based on premises, cooking/fuel, building use, seating/capacity, employment, signage, waste, alcohol, or other facts. Do not presume any is required. |
| 5. Prepare evidence | JMC form exposes attachment fields including land documents, neighbour NOC, newspaper cutting, state subject and approved/site plan for some selectable NOC/licence paths. FoSCoS publishes separate food-business document guidance. | Whether documents overlap; whether either authority lawfully accepts evidence from the other system; whether reuse is technically possible. |
| 6. Submit and process | JMC says applications, document/fee verification, escalation, status and digitally signed outputs are available for its online services. FoSCoS supports applications and tracking. | Whether the systems expose authorised APIs or sandbox access; whether case identifiers, statuses, missing-document requests and decision events can be exchanged. |
| 7. Resolve exceptions | JMC's announcement describes escalation to another dealing officer. FoSCoS publishes applicant guidance and grievance/escalation routes. | Real frequency and causes of delays, repeated requests, unowned cross-system handoffs, and time spent chasing status. Requires case records/interviews with permission. |
| 8. Verify final outcome | Official systems provide status and official outputs within their own scope. | A lawful, reliable method for Aether to reconcile the final state from each system without impersonation or unauthorised access. |

## Candidate Aether value — hypotheses to test, not claims

- One objective and a source-backed plan showing only approvals that apply to this business profile.
- A common case view that links separate application references and deadlines, where permitted.
- Evidence reuse only where the receiving authority accepts it and the data-sharing basis is lawful.
- Cross-system dependency tracking and exception follow-up without bypassing officials or statutory decisions.
- Final reconciliation against each authoritative system of record.
- A reusable connector/rule-pack pattern that lowers the cost of adding the next workflow.

## Required discovery before any implementation

1. Fix a specific business profile (for example, a small restaurant/café), premises and municipal jurisdiction. The path cannot be authoritative without these facts.
2. Review the live official JMC form's selectable licence/NOC types and retrieve the current checklist/fee/timeline for the relevant type.
3. Verify FoSCoS category, eligibility, documents, fees and processing rules against current official materials and effective dates.
4. Use NSWS and the J&K Single Window to identify possible additional approvals; independently verify applicability from primary rules.
5. Speak with applicants or authorised advisers and, if access is possible, JMC/FSSAI/process owners. Collect dated examples of repeated evidence, stalled handoffs and actual time-to-outcome. Do not infer local pain from global survey statistics.
6. Establish baseline measures: elapsed time, applicant minutes, repeat submissions, calls/visits, staff minutes, handoffs, exception reasons and outcome.
7. Determine whether an authorised sandbox/API exists. If not, use a transparent shadow-mode study with lawful sample data; never scrape protected data, bypass controls, or submit real applications without written authority.

## Pilot go/no-go criteria

Proceed only if the evidence confirms all of the following:

- a material cross-system problem exists despite current portals;
- a named institutional sponsor and operational owner can be engaged;
- authoritative, current rules can be sourced and reviewed;
- a lawful integration or shadow-mode path exists;
- a baseline can be measured and the final outcome independently verified;
- the pilot can improve applicant or staff effort without creating unauthorised actions;
- the same execution kernel can be reused for another workflow at lower deployment cost.

If existing systems already coordinate the full journey effectively, reject this candidate rather than forcing Aether into it.
