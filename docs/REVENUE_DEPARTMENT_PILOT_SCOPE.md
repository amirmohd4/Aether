# Aether National Product Scope

## Product decision

Aether is a national, multi-department Government OS. Its product scope is not restricted to one department, State/UT, district, user type or service category.

The national service directory is intended to cover Central, State/UT, district, municipal and local government services. The shared platform provides objective understanding, service discovery, case management, document intake, workflow orchestration, notifications, payments where authorized, evidence verification, human review, audit and developer APIs.

The current core registry contains 61 service-family definitions and the extended India service taxonomy contains additional service families. These are discovery and routing definitions, not proof that every service is currently available, legally verified or executable in every jurisdiction.

## National coverage model

Aether should cover departments and public authorities across:

- Revenue, land administration and registration
- Municipal administration and local bodies
- Planning, housing and urban development
- Transport and road authorities
- Health, food safety and drug control
- Education, skills and employment
- Agriculture, rural development and animal husbandry
- Labour and social security
- Social welfare, pensions and public distribution
- Taxation, corporate affairs and MSME
- Police, justice, legal services and grievance redressal
- Environment, forests, mines and disaster management
- Electricity, water, sanitation and public utilities
- Procurement and other public services

This list is a taxonomy, not a claim that all departments have production integrations.

## Location and jurisdiction resolution

The intake experience must ask for the location to which the requested service applies. Depending on the service, that can be the applicant's residence, property/parcel, business premises, place of activity, registered office or another legally relevant location.

Applicant residence must not automatically be treated as the controlling jurisdiction. For example, a person may live in one State and apply for a land-record service concerning property in another State.

Resolution order:

1. Understand the requested service and the subject of the application.
2. Identify which location legally controls that service.
3. Collect the minimum required location fields (country, State/UT, district, and lower-level geography where required).
4. Resolve the most specific verified process profile available for that service and jurisdiction.
5. Apply only rules effective on the requested/application date.
6. Display the selected jurisdiction, responsible authority, source, effective date and last verification date.
7. Ask the user to correct or clarify ambiguous locations.
8. If no verified profile exists, label the process as unverified and do not invent requirements, fees, statutory timelines, appeal routes or officer powers.

Profiles must be versioned and source-backed. A valid process profile should identify its service, jurisdiction, authority, official source URL, effective date, verification date, requirements, process steps and authority boundaries. Expired, conflicting or incomplete profiles must not be silently treated as current.

## Department boundaries and cross-government journeys

Aether may coordinate dependencies across departments, but must preserve the legal identity of each competent authority. It must not present one department's action as another department's statutory decision. Statutory approvals, signatures, inspections and adjudications remain with authorized officials unless a formally authorized integration explicitly permits another action.

## Service coverage and truthful claims

Every service-family entry must have a clear coverage status:
- Catalogued: the service can be discovered and routed at a family level.
- Jurisdiction profile missing: local process details are not verified.
- Profile incomplete: some official source, authority, date or process information is missing.
- Verified process: the current jurisdiction profile has been checked against authoritative sources.
- Sandbox executable: Aether can demonstrate the workflow using synthetic systems.
- Live integration authorized: the competent authority has authorized the connector and credentials.
- Live outcome verified: a result has been reconciled with the official system of record.

Do not describe a catalogued service as live or available for statutory submission.

## Launch strategy

The public MVP can launch as a national discovery and controlled workflow-orchestration product if the interface clearly labels sandbox behavior, jurisdiction coverage and limitations. It must not claim national statutory execution, universal service coverage or government endorsement.

Before any real applications or operational personal data are processed, Aether needs the relevant institutional authorization, verified jurisdiction rule packs, privacy and retention controls, secure operational support, and approved government connectors.

## Free infrastructure constraint

Continue on existing free tiers. Do not upgrade Render, Netlify or Supabase or incur paid usage without explicit approval. Disclose cold starts, quotas, storage limits, worker constraints and availability limitations.
