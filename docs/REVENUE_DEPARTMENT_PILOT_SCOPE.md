# Revenue Department Pilot Scope

## Product decision

The first Aether pilot is a **Revenue Department service hub**, not a developer-only workflow. Developers are one supported customer type; citizens, landowners, businesses, banks and other permitted applicants must be supported where a service applies to them.

The current shared service registry now contains 61 total MVP services, including **30 Revenue Department service entries**. These are service-family definitions for intent recognition and workflow routing. They are not a claim that every service is legally available in every State/UT or that all 30 have a verified production process pack.

## Revenue service families in the MVP registry

### Land records and extracts
- Certified land record / Fard / Record of Rights
- Jamabandi / Record of Rights extract
- Khasra Girdawari / crop inspection record
- Aks Masavi / Latha map extract
- Tatima Shajra / subdivision map extract
- Chulah / Chowkidari record extract
- Land passbook / property card
- Certified mutation copy

### Mutation, ownership and land administration
- Land/property mutation
- Inheritance / succession mutation
- Mutation attestation
- Land partition
- Land demarcation / boundary survey
- Land record correction / rectification
- Land possession certificate / report
- Land lien marking / cancellation
- Land conversion / change of land use
- State land lease / allotment application
- Government land encroachment complaint
- Land acquisition / compensation claim

### Certificates and citizen services
- Domicile / residence certificate
- Income certificate
- Caste / category certificate
- Reserved category certificate
- Dependent certificate
- Legal heir / surviving member certificate
- Property / land holding certificate

### Case, business and relief workflows
- Revenue court / Tehsil case status
- Land / crop damage assessment and relief claim
- Title verification for developers, businesses, banks and insurers

The service catalog should accept local synonyms and terms (for example Fard, Intikal, Warasat, Jamabandi, Girdawari, Aks Masavi, Latha and Tatima Shajra). Aether should ask clarifying questions when the service, parcel or jurisdiction is ambiguous.

## Department boundary

Some journeys cross into Registration, Municipal, Planning, Forest, Environment, Agriculture, Disaster Management or other departments. Aether may coordinate those dependencies, but must identify the actual responsible authority and must not label another department's statutory approval as a Revenue Department decision.

Property registration, stamp duty, encumbrance records and construction approvals may be related to a Revenue journey but their competent authority and legal process must be established for the selected jurisdiction.

## Jurisdiction and legal accuracy

Service availability, responsible officer, forms, evidence, fee, statutory deadline, appeal authority and workflow differ by State/UT and sometimes by district. Do not infer these from a generic India-wide catalog.

Aether's jurisdiction process registry requires a process profile with an authority, source URL, effective date and verification date before marking a workflow ready for jurisdiction-specific execution. Until such a profile is verified:
- show the service as catalogued but jurisdiction rules as unverified;
- do not invent document lists, fees, deadlines or officer powers;
- do not submit an application or represent a simulated result as an official outcome;
- keep human statutory decisions and physical field verification with the competent authority.

## Jammu & Kashmir reference sources reviewed

These sources demonstrate the breadth of Revenue services in J&K and are references for catalog design, not authority to apply J&K rules to Ladakh or another jurisdiction:

- District Jammu Revenue Department functions and land-record types: https://jammu.nic.in/department-of-revenue/
- District Budgam Revenue online services (Fard, Aks Masavi/Latha, mutation attestation/copy, demarcation, Girdawari, Jamabandi, encumbrance, Chulah/Chowkidari, change of land use, land passbook): https://budgam.nic.in/revenue-online-services/
- District Rajouri Revenue citizen services: https://rajouri.nic.in/revenue/
- District Samba Revenue services, designated officers and timelines: https://samba.gov.in/revenue-deptt/
- J&K Jansugam Legal Heir service detail: https://jansugam.jk.gov.in/getServiceDesc.html?serviceId=18240009

## Next implementation sequence

1. Confirm the first pilot jurisdiction (State/UT and district). Ladakh and Jammu & Kashmir must be treated as separate jurisdictions.
2. Build and verify the jurisdiction-specific service inventory from the competent administration's current official service list, laws, forms, service guarantees and appeal structure.
3. Create source-backed process profiles for each included service, with effective dates and named authorities.
4. Build a reusable intake schema for applicant identity, parcel identifiers (district, tehsil, village, khasra, khata/khewat as applicable), co-owners, purpose and supporting evidence.
5. Add service-specific evidence checklists, validation, duplicate detection, case tracking, grievance/appeal paths and officer queues.
6. Run synthetic end-to-end tests for every service family before inviting pilot users.
7. Keep external government submissions and official record updates disabled until written authorization and supported integrations exist.

## Free-infrastructure constraint

The pilot remains on the existing free tiers. Do not upgrade Render, Netlify or Supabase plans or incur paid usage without explicit user approval. Design for cold starts, quotas, restarts and limited worker availability; disclose these limitations rather than promising production-grade uptime.
