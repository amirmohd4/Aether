# Aether GovOS — Launch Readiness Checklist

**Branch:** `launch/public-research-preview`  
**Release type:** Public research preview only  
**Last reviewed:** 2026-10-15  
**Current rule:** Do not merge to the production branch, activate live connectors, or claim official service delivery until the relevant gates below are met.

## Confirmed in repository / CI

- [x] One canonical user-facing catalogue contains 32 non-judicial service templates.
- [x] The public command centre defaults to a global mock context rather than a state or city.
- [x] A client-side mock studio exposes routine, missing-evidence, human-review, retry, and adverse-path scenarios.
- [x] Mock journey steps are tailored by service family; jurisdiction-specific templates are labelled.
- [x] Synthetic-only disclaimers state that no official application, record, approval, or certificate is created.
- [x] Legacy national-ID intake has been replaced with a fictional demo reference.
- [x] Legacy results no longer claim a real application was approved or a document was downloaded.
- [x] Latest branch CI passed: 144 backend tests, frontend type-check/build, live synthetic-sandbox smoke test, public-launch asset tests, and the npm audit gate.

## Required before announcing the research preview

- [x] Verify the latest Netlify deploy is ready and serves the expected PR commit. Current verified preview: https://deploy-preview-10--aether-govos.netlify.app
- [ ] Manually exercise all five scenarios on representative identity, property, business, welfare/tax, and permit templates.
- [x] Confirm the feedback form is registered with Netlify Forms on the current preview deployment; submission count remains zero, so delivery is not yet proven.
- [ ] Send one controlled test feedback submission and verify it appears in the correct form; then remove test data if appropriate.
- [ ] Check mobile layout, keyboard access, form validation, and error states.
- [ ] Review all public copy for unsupported claims about instant processing, universal availability, official approval, and measured savings.
- [x] Patch the identified frontend dependency advisories; `npm audit` reports zero known vulnerabilities, and CI now fails on moderate-or-higher npm advisories.
- [ ] Confirm the preview backend is isolated from production data and credentials.

## Required before any live government pilot

- [ ] Written authorisation from the relevant system owner.
- [ ] Official API/sandbox contract, credentials, purpose limitation, and operation allowlist.
- [ ] Jurisdiction-specific rules sourced, versioned, reviewed, and dated.
- [ ] Security, privacy, retention, incident response, tenant isolation, audit, rollback, and kill-switch reviews.
- [ ] Human-authority and physical-action boundaries accepted by the responsible authority.
- [ ] Baseline metrics, support ownership, pilot cohort, success criteria, and exit plan agreed.

## Current boundary

The public mock studio is a synthetic research instrument, not a live GovOS deployment. A passing build proves code can compile; it does not prove that all service workflows are legally accurate, that feedback is reaching the team, that a government system is connected, or that real-world savings have occurred. Do not remove these gates to meet a launch date.
