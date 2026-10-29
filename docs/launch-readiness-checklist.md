# Aether GovOS — Launch Readiness Checklist

**Branch:** `launch/public-research-preview`  
**Release type:** Public research preview only  
**Last reviewed:** 2026-10-29  
**Current rule:** Do not merge to the production branch, activate live connectors, or claim official service delivery until the relevant gates below are met.

## Confirmed in repository / CI

- [x] One canonical user-facing catalogue contains 32 non-judicial service templates.
- [x] The public command centre defaults to a global mock context rather than a state or city.
- [x] The command centre includes a 32-template synthetic studio; the public research page now explains the end-to-end vision with a guided cross-team example and selectable routine, missing-evidence, system-failure, human-review, and evidence-conflict scenarios.
- [x] Mock journey steps are tailored by service family; jurisdiction-specific templates are labelled.
- [x] Synthetic-only disclaimers state that no official application, record, approval, or certificate is created.
- [x] Legacy national-ID intake has been replaced with a fictional demo reference.
- [x] Legacy results no longer claim a real application was approved or a document was downloaded.
- [x] Release-candidate checks passed for backend tests, frontend type-check/build, autonomy benchmark, public-launch asset tests, and npm audit. The live public-demo smoke test passed after commit `66c5ed8` deployed, validating synthetic case creation/read, cross-session isolation, upload blocking, API-key blocking, and CORS for the active preview origin.

## Required before announcing the research preview

- [x] Verify the latest Netlify deploy preview is ready and serves the expected branch commit. Current preview: https://deploy-preview-10--aether-govos.netlify.app/research-preview.html (confirmed ready for commit `9f79c85`).
- [ ] Manually exercise all five scenarios on representative identity, property, business, welfare/tax, and permit templates.
- [x] Confirm the feedback form is registered with Netlify Forms on the current preview deployment; submission count remains zero, so delivery is not yet proven.
- [ ] Send one controlled test feedback submission and verify it appears in the correct form; then remove test data if appropriate.
- [ ] Check mobile layout, keyboard access, form validation, and error states.
- [ ] Review all public copy for unsupported claims about instant processing, universal availability, official approval, and measured savings.
- [x] Patch the identified frontend dependency advisories; `npm audit` reports zero known vulnerabilities, and CI now fails on moderate-or-higher npm advisories.
- [x] Confirm the preview points to the separate `aether-public-demo` Render service; the live smoke test confirms a public-demo tenant namespace, cross-session case isolation, and blocked real-file uploads/API-key management. Live government connectors remain disabled.

## Required before any live government pilot

- [ ] Written authorisation from the relevant system owner.
- [ ] Official API/sandbox contract, credentials, purpose limitation, and operation allowlist.
- [ ] Jurisdiction-specific rules sourced, versioned, reviewed, and dated.
- [ ] Security, privacy, retention, incident response, tenant isolation, audit, rollback, and kill-switch reviews.
- [ ] Human-authority and physical-action boundaries accepted by the responsible authority.
- [ ] Baseline metrics, support ownership, pilot cohort, success criteria, and exit plan agreed.

## Current boundary

The public research preview is live at https://deploy-preview-10--aether-govos.netlify.app/research-preview.html; the interactive workspace is at https://deploy-preview-10--aether-govos.netlify.app/. This is a synthetic research instrument, not a live GovOS deployment. The feedback form is registered but has zero recorded submissions, so actual capture is still unverified. A passing build and smoke test do not prove that all service workflows are legally accurate, that a government system is connected, or that real-world savings have occurred. Do not remove the remaining gates to meet a launch date.
