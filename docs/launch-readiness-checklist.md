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
- [x] Frontend type-check/build and backend test/CI workflows passed on the reviewed commits (check the latest branch runs before release).

## Required before announcing the research preview

- [ ] Verify the latest Netlify deploy is ready and serves the expected PR commit.
- [ ] Manually exercise all five scenarios on representative identity, property, business, welfare/tax, and permit templates.
- [ ] Confirm the feedback form is detected by Netlify Forms after a deploy with form detection enabled.
- [ ] Send one controlled test feedback submission and verify it appears in the correct form; then remove test data if appropriate.
- [ ] Check mobile layout, keyboard access, form validation, and error states.
- [ ] Review all public copy for unsupported claims about instant processing, universal availability, official approval, and measured savings.
- [ ] Review dependency/security alerts and decide how to address unresolved high-severity findings.
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
