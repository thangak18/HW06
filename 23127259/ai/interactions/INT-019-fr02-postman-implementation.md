# Interaction Log: INT-019

- **Interaction ID:** INT-019
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 20:06:50+07:00
- **Project Stage:** Phase 1D.0 – FR-02 Final Executable Suite Materialization & Postman Collection Implementation
- **Transcript Reference:** `transcript_full.jsonl` (Prompt: Step 662, Output: Step 713)

---

## 1. Submitted Prompt

```text
/Speckit /Speckit We are starting:

PHASE 1D.0 – FR-02 FINAL EXECUTABLE SUITE MATERIALIZATION AND POSTMAN COLLECTION IMPLEMENTATION

Current completed state:

Raw AI-generated cases:
37

Human Audit:
37 / 37 complete

Audit result:
- VALID: 16
- INCOMPLETE WITH CORRECTIONS: 19
- INVALID DUPLICATES: 2

Usable AI-derived cases:
35

Human Extension cases:
5

Final executable candidate count:
40

Previous Human Extension commit:
1634d8f

IMPORTANT:

This phase converts the audited design into the ACTUAL executable FR-02
specification and Postman collection.

DO NOT EXECUTE THE TESTS YET.

DO NOT:
- start formal SUT execution
- run Collection Runner
- run Newman
- generate HTML reports
- confirm bugs
- create GitHub Issues
- fabricate execution results
- modify the EShop SUT
- merge to main

==================================================
1. AI AUDIT NUMBERING
==================================================

Previous interaction:

INT-018
FR-02 Human Extension Finalization

Current interaction:

INT-019

First backfill the COMPLETE exact AI output of INT-018 from the completed
Antigravity transcript.

Find the actual USER_INPUT and corresponding PLANNER_RESPONSE.
Do not guess transcript indices.

Then create:

23127259/ai/interactions/INT-019-fr02-postman-implementation.md

Record:
- actual Tool
- actual Model
- actual Date/Time
- timezone UTC+07:00
- Stage:
  FR-02 Final Executable Suite + Postman Implementation
- THIS COMPLETE PROMPT verbatim

Append the same full prompt to:

23127259/ai/prompts/AI_PROMPT_LOG.md

Update:

23127259/ai/AI_AUDIT_REPORT.md

For INT-019 Exact AI Output use:

PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES

until this interaction completes.

==================================================
2. FIX HUMAN EXTENSION PROVENANCE WORDING
==================================================

Review:

23127259/testcases/FR02_HUMAN_TEST_CASES.md
23127259/testcases/FR02_HUMAN_EXTENSION_DESIGN.md

Do NOT claim the five extension cases were independently produced with zero AI
assistance.

Use transparent wording:

"Student-selected and finalized Human Extension cases after AI-assisted
coverage-gap analysis."

or equivalent.

Keep them separate from the raw AI-generated FR02-AI inventory.

Also verify FR02-HUM-004 classification.

If the SRS explicitly establishes account-specific lockout semantics:
SPECIFICATION-BACKED is acceptable.

If isolation between two distinct accounts is inferred rather than explicit:
use:

PARTIALLY SPECIFICATION-BACKED / STATE ISOLATION

Do not invent a stronger oracle than the SRS provides.

==================================================
3. PRESERVE RAW AI EVIDENCE
==================================================

DO NOT MODIFY:

23127259/testcases/FR02_AI_DRAFT.md

Verify SHA-256 remains:

b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c

Do NOT modify historical Human Audit verdicts in:

23127259/ai/TC_AUDIT_FR02.md

==================================================
4. CREATE THE FINAL EXECUTABLE TEST SPECIFICATION
==================================================

Create:

23127259/testcases/FR02_FINAL_EXECUTABLE_SUITE.md

This file is the authoritative implementation source for Postman.

IMPORTANT:

Do NOT copy raw INCOMPLETE AI cases unchanged.

For every usable AI-derived case:

VALID
→ use the audited case as accepted.

INCOMPLETE
→ apply the EXACT correction recorded in TC_AUDIT_FR02.md.

INVALID
→ exclude from executable suite.

Therefore explicitly exclude:

FR02-AI-016
FR02-AI-017

but preserve references showing they remain in raw evidence.

==================================================
5. FINAL SUITE ACCOUNTING
==================================================

The final executable specification must contain exactly:

35 usable AI-derived cases
+
5 Human Extension cases
=
40 executable candidate cases

Use IDs:

AI-derived:
35 accepted IDs from FR02-AI inventory, excluding 016 and 017.

Human:
FR02-HUM-001 .. FR02-HUM-005

Create summary:

| Source | Raw | Rejected | Executable |
|---|---:|---:|---:|
| AI Generated | 37 | 2 | 35 |
| Human Extension | 5 | 0 | 5 |
| TOTAL | 42 artifacts considered | 2 rejected | 40 executable |

Do NOT say only 35 cases were AI-generated.

Correct wording:

37 raw AI-generated
35 usable AI-derived after Human Audit
5 Human Extension
40 executable

==================================================
6. FINAL EXECUTABLE CASE FORMAT
==================================================

For each of the 40 cases include:

- Test Case ID
- Source:
  AI-derived / Human Extension
- Audit Status:
  VALID / CORRECTED FROM INCOMPLETE / HUMAN EXTENSION
- Title
- Technique
- Requirement / Oracle Basis
- Preconditions
- Setup Requirements
- Request Method
- Endpoint
- Headers
- Request Body
- Request / Action Sequence
- Expected HTTP Status
- Expected Semantic Result
- Expected State
- Oracle Confidence
- Spec Limitation
- Postman Assertion Plan

CRITICAL:

For corrected INCOMPLETE cases:
use the HUMAN AUDIT correction, not the raw AI oracle.

Example discipline:

If audit correction says exact HTTP status is NOT SPECIFIED:
do NOT assert a fixed 400/401 in Postman.

If audit correction says:
"authentication must not succeed"
then implement an assertion around non-success / no usable token rather than an
invented exact response.

==================================================
7. CREATE TRACEABILITY MATRIX
==================================================

Create:

23127259/testcases/FR02_EXECUTION_TRACEABILITY.md

Columns:

| Executable ID | Source | Requirement | Technique | Audit Origin | Postman Folder | Request Name | State Dependency | Oracle Type |
|---|---|---|---|---|---|---|---|---|

Every one of the 40 executable cases must map to a Postman request/folder.

No orphan cases.

No Postman request should be counted as a test case unless mapped here.

Setup/helper requests are allowed but must be labelled:

HELPER – NOT COUNTED AS TEST CASE

==================================================
8. INSPECT API SPEC BEFORE BUILDING SETUP
==================================================

Read the authoritative API specification and determine what documented
mechanisms exist for deterministic test setup.

Stateful FR-02 tests require controlled account state.

Do NOT assume undocumented reset endpoints.

Preferred strategy order:

A. documented registration endpoint to create fresh dedicated users
B. documented API mechanism that returns a known clean state
C. isolated seeded accounts plus explicit waiting where unavoidable

Do NOT:
- edit DB directly as normal Postman setup unless explicitly justified
- modify SUT source
- invent a reset endpoint

If a documented registration endpoint is used as setup:

label requests:

HELPER – SETUP ONLY – NOT FR-02 TEST CASE

The helper does not count toward the 40 FR-02 tests.

==================================================
9. STATE ISOLATION STRATEGY
==================================================

Create:

23127259/docs/FR02_POSTMAN_STATE_STRATEGY.md

Document how Postman execution will prevent tests from interfering with each
other.

Cover:

- ordinary valid-login account
- admin-login account
- negative credential account
- lockout account(s)
- N=1 / N=2 / N=3 state setup
- active-lock tests
- timing tests
- reset-on-success tests
- Human cross-account isolation test
- repeated Newman runs

Avoid dependence on undocumented `login_attempts` response fields.

Primary state oracle must remain externally observable.

==================================================
10. TIMING TEST DESIGN
==================================================

FR02-AI-020 and FR02-AI-021 involve the documented 30-second lock duration.

Do not use a strict exactly-30.000-second assertion.

Implement deterministic timing such as:

before-expiry:
a safely lower time such as ~25s if that is the audited case

after-expiry:
a safely higher time such as ~32s

However:

Do NOT execute waits in this phase.

Implement the script/flow only.

Document expected Newman runtime impact.

==================================================
11. POSTMAN ENVIRONMENT
==================================================

Create/update:

23127259/postman/environments/FR02-local.postman_environment.json

Use variables such as:

baseUrl = http://localhost:3000
studentId = 23127259

userEmail
userPassword

adminEmail
adminPassword

lockoutEmail
lockoutPassword

secondaryEmail
secondaryPassword

userToken

Do NOT commit secrets if credentials are sensitive.

If the SUT uses public seeded demo credentials:
document them as test fixtures.

Otherwise use placeholders / generated setup accounts.

Never commit a live JWT.

==================================================
12. X-STUDENT-ID – MANDATORY
==================================================

EVERY formal request must include:

X-Student-Id: 23127259

Prefer robust collection-level enforcement using a Pre-request Script such as
header upsert from:

{{studentId}}

but verify every generated request receives it.

Helper/setup requests should also include the header where the API accepts it.

Add a collection-level safety check to prevent accidental execution without the
studentId variable.

==================================================
13. BUILD POSTMAN COLLECTION
==================================================

Create:

23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json

Collection structure should be clear and mapped to the final suite.

Recommended folders:

00 – Setup Helpers
01 – Positive Authentication
02 – Domain and Negative Inputs
03 – Lockout Boundary and State
04 – Security
05 – Schema and Contract
06 – Human Extensions

Request names MUST begin with the mapped testcase ID for formal cases.

Example:

FR02-AI-001 – Valid User Login

Helper request example:

HELPER-001 – Create Fresh Lockout User

Do not assign FR02 test IDs to helpers.

==================================================
14. IMPLEMENT ALL 40 EXECUTABLE CASES
==================================================

Implement:

35 usable audited AI-derived cases
+
5 Human Extension cases

Do NOT implement rejected:

FR02-AI-016
FR02-AI-017

For every request/script:

- preserve audited oracle
- include X-Student-Id
- use variables
- avoid hardcoded live tokens
- add meaningful Postman `pm.test` assertions
- include comments indicating testcase ID and requirement

For cases with:

Expected HTTP Status = NOT SPECIFIED

DO NOT write:

pm.response.to.have.status(400)

or any single exact status assertion.

Instead assert only what the audited oracle supports.

Example concept:

pm.expect(pm.response.code).to.not.equal(200)

only if non-success is truly specification-backed.

Where even exact success/non-success transport classification is exploratory,
write appropriate non-destructive contract assertions and comments.

==================================================
15. SECURITY TEST ASSERTIONS
==================================================

For SEC-05 probes:

assert:
- no successful authentication bypass
- no usable unauthorized JWT

Do NOT state in test output:
"Parameterized queries confirmed"

Use wording:

"SQLi behavioral bypass not observed"

because black-box testing is partial evidence only.

For response password exposure:
classify as additional security response-sanitization evidence, not full
SEC-01 proof.

==================================================
16. SCHEMA CASE DISCIPLINE
==================================================

Do not use invented JSON Schema restrictions.

Only validate fields/types explicitly documented or accepted by Human Audit.

For corrected cases:

FR02-AI-032..037

carefully apply the Human Audit corrections.

Especially:

- do not over-assert strict top-level structure
- do not invent exact error-key names
- do not treat Content-Type as EXPLICIT if audit downgraded it
- keep extraneous-field behavior exploratory where required

==================================================
17. HUMAN CASE IMPLEMENTATION
==================================================

Implement:

FR02-HUM-001
HTTP method enforcement

FR02-HUM-002
different SQLi vector

FR02-HUM-003
successful reset specifically after N=2 consecutive failures

FR02-HUM-004
cross-account lockout isolation

FR02-HUM-005
non-JSON Content-Type contract

Use the finalized Human file as design source.

Do not silently alter their rationale.

==================================================
18. DATA-DRIVEN TESTING
==================================================

HW06 asks students to use reasonable Postman features.

If useful, create:

23127259/postman/data/fr02-domain-data.json

for suitable stateless domain cases.

Do NOT force all stateful cases into a data-driven runner if doing so harms
determinism.

Document which FR-02 cases are data-driven.

==================================================
19. POSTMAN FEATURES DOCUMENTATION
==================================================

Update/create:

23127259/docs/POSTMAN_FEATURES_FR02.md

Record features actually implemented at this stage, for example:

- collection
- folders
- environment variables
- collection variables
- Pre-request Scripts
- Test scripts
- data-driven requests where applicable

Do NOT claim:
- Monitor
- Mock Server
- Newman
- CI

as "used" yet unless they have actually been configured/executed.

Those belong to later phases.

==================================================
20. STATIC COLLECTION VALIDATION ONLY
==================================================

This phase may perform NON-EXECUTION validation such as:

- JSON parse validation
- Postman schema sanity check
- request count
- formal testcase mapping count
- duplicate request-name check
- X-Student-Id header/script presence
- traceability completeness

Do NOT send HTTP requests to SUT.

Do NOT execute Newman.

Do NOT produce pass/fail test results.

==================================================
21. REQUIRED STATIC CHECKS
==================================================

At minimum verify:

- collection JSON parses successfully
- exactly 40 formal testcase IDs mapped
- FR02-AI-016 absent from executable collection
- FR02-AI-017 absent from executable collection
- exactly 5 FR02-HUM IDs
- no duplicate formal testcase IDs
- every formal case has X-Student-Id enforcement
- no hardcoded live JWT
- no unsupported fixed statuses from corrected INCOMPLETE cases
- helper requests clearly excluded from count

Create:

23127259/docs/FR02_POSTMAN_STATIC_VALIDATION.md

Record static results only.

Explicitly state:

NO SUT EXECUTION PERFORMED IN THIS PHASE.

==================================================
22. DO NOT CREATE FAKE EVIDENCE
==================================================

Do NOT create:

- Newman HTML report
- pass/fail screenshot
- bug screenshot
- bug report
- GitHub Issue
- CI run
- Postman Runner screenshot

until actual execution occurs.

==================================================
23. GIT COMMIT
==================================================

If implementation and static validation are complete:

stage only relevant Phase 1D.0 artifacts.

Commit:

test(23127259): implement FR-02 Postman collection

Include relevant:

23127259/testcases/FR02_FINAL_EXECUTABLE_SUITE.md
23127259/testcases/FR02_EXECUTION_TRACEABILITY.md

23127259/docs/FR02_POSTMAN_STATE_STRATEGY.md
23127259/docs/POSTMAN_FEATURES_FR02.md
23127259/docs/FR02_POSTMAN_STATIC_VALIDATION.md

23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json
23127259/postman/environments/FR02-local.postman_environment.json
23127259/postman/data/fr02-domain-data.json
(if actually used)

plus audit artifacts:
INT-018
INT-019
AI_AUDIT_REPORT.md
AI_PROMPT_LOG.md

Do not include execution evidence.

Push:

origin/thang/hw06-implementation

Do NOT merge to main.

==================================================
24. END REPORT
==================================================

Return:

# Phase 1D.0 Completion Report

## AI Audit
- INT-018 output backfilled
- INT-019 prompt stored
- INT-019 output pending

## Final Executable Suite
- raw AI: 37
- rejected AI: 2
- usable AI-derived: 35
- Human Extensions: 5
- executable total: 40

## Postman Collection
- collection path
- folder structure
- helper request count
- formal testcase request count
- AI-derived mapped count
- Human mapped count

## Stateful Strategy
- setup mechanism selected
- lockout isolation mechanism
- repeatability strategy
- timing strategy

## Static Validation
- JSON valid
- 40 unique IDs mapped
- X-Student-Id coverage
- hardcoded JWT count
- rejected IDs absent
- execution performed: NO

## Provenance Corrections
- Human Extension wording
- FR02-HUM-004 oracle classification verification

## Git
- commit SHA
- push result
- git status

Then STOP.

DO NOT EXECUTE THE COLLECTION.

Next phase:

PHASE 1D.1 – FR-02 CONTROLLED POSTMAN/NEWMAN EXECUTION
```

---

## 2. Exact AI Output

```markdown
# Phase 1D.0 Completion Report

---

## 1. AI Audit Verification
- **INT-018 Output Backfilled:** **YES** — Exact output (Step 661, 4,239 bytes) backfilled into [`INT-018-fr02-human-extension-finalization.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-018-fr02-human-extension-finalization.md).
- **INT-019 Prompt Stored:** **YES (Verbatim)** in [`INT-019-fr02-postman-implementation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-019-fr02-postman-implementation.md) and [`AI_PROMPT_LOG.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/prompts/AI_PROMPT_LOG.md) (184,752 bytes).
- **INT-019 Output Status:** `PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES`.

---

## 2. Final Executable Suite Accounting

$$\begin{aligned}
\text{Raw AI-Generated Test Cases Considered} &= \mathbf{37} \\
\text{Raw AI Rejected During Human Audit} &= \mathbf{2} \quad (\text{Duplicates: } \text{FR02-AI-016}, \text{FR02-AI-017}) \\
\text{Usable AI-Derived Cases Post-Audit} &= \mathbf{35} \quad (16\text{ VALID} + 19\text{ INCOMPLETE with corrections applied}) \\
\text{Student-Selected Human Extensions} &= \mathbf{5} \quad (\text{FR02-HUM-001} .. \text{FR02-HUM-005}) \\
\hline
\mathbf{\text{Total Final Executable Candidate Suite}} &= \mathbf{40\text{ Test Cases}}
\end{aligned}$$

- **Authoritative Executable Suite Specification:** [FR02_FINAL_EXECUTABLE_SUITE.md](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_FINAL_EXECUTABLE_SUITE.md).
- **Full Traceability Matrix:** [FR02_EXECUTION_TRACEABILITY.md](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_EXECUTION_TRACEABILITY.md).

---

## 3. Postman Collection Architecture

- **Collection File:** [`23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json)
- **Environment File:** [`23127259/postman/environments/FR02-local.postman_environment.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/environments/FR02-local.postman_environment.json)
- **Domain Data File:** [`23127259/postman/data/fr02-domain-data.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/data/fr02-domain-data.json)
- **Features Documentation:** [POSTMAN_FEATURES_FR02.md](file:///Volumes/Thang/HW06/HW06/23127259/docs/POSTMAN_FEATURES_FR02.md)

### Folder Structure & Mapping:
| Folder | Helper Requests | Formal Test Requests | Mapped Test IDs |
|---|:---:|:---:|---|
| `00 – Setup Helpers` | 4 | 0 | `HELPER-001` .. `HELPER-004` (Excluded from test suite count) |
| `01 – Positive Authentication` | 0 | 2 | `FR02-AI-001`, `FR02-AI-002` |
| `02 – Domain and Negative Inputs` | 0 | 10 | `FR02-AI-003` .. `FR02-AI-012` |
| `03 – Lockout Boundary and State Progression` | 0 | 10 | `FR02-AI-013` .. `FR02-AI-015`, `FR02-AI-018` .. `FR02-AI-024` |
| `04 – Security and Token Integrity` | 0 | 7 | `FR02-AI-025` .. `FR02-AI-031` |
| `05 – Schema and Contract Validation` | 0 | 6 | `FR02-AI-032` .. `FR02-AI-037` |
| `06 – Human Extensions` | 0 | 5 | `FR02-HUM-001` .. `FR02-HUM-005` |
| **TOTAL** | **4** | **40** | **40 Unique Executable Test Cases** |

---

## 4. Stateful Isolation & Repeatability Strategy
Detailed in [FR02_POSTMAN_STATE_STRATEGY.md](file:///Volumes/Thang/HW06/HW06/23127259/docs/FR02_POSTMAN_STATE_STRATEGY.md):
1. **Account Segregation:** Distinct accounts allocated per test domain (`user@eshop.com`, `admin@eshop.com`, `user_domain@eshop.com`, `lockout_fr02@eshop.com`, `reset_fr02@eshop.com`, `victim_fr02@eshop.com`, `isolated_fr02@eshop.com`).
2. **Setup Mechanism:** Documented `POST /api/register` helper endpoints ensure dedicated test accounts exist prior to state progression tests.
3. **Timing Bracketing:** Deterministic timing delays safely bracket the 30-second lockout window ($T \approx 25\text{s}$ pre-expiry and $T \approx 32\text{s}$ post-expiry).
4. **Observable Oracles:** Assertions rely strictly on observable HTTP status codes, payloads, and subsequent request acceptance/rejection, without depending on internal DB columns.

---

## 5. Non-Execution Static Validation Summary
Detailed in [FR02_POSTMAN_STATIC_VALIDATION.md](file:///Volumes/Thang/HW06/HW06/23127259/docs/FR02_POSTMAN_STATIC_VALIDATION.md):
- **Collection & Environment JSON Syntax:** **PASS** (Valid JSON, verified by parser).
- **Total Mapped Test Cases:** **40** (Exactly 35 AI-derived + 5 Human extensions).
- **Duplicate Exclusion:** Confirmed `FR02-AI-016` (**Absent**) and `FR02-AI-017` (**Absent**).
- **`X-Student-Id` Header Enforcement:** **PASS** (Enforced on 100% of requests via collection-level pre-request script + header definitions).
- **Zero Hardcoded Secrets/JWTs:** **PASS** (Dynamic variables `{{userToken}}` and `{{adminToken}}` used exclusively).
- **SUT Execution Gate:** **NO SUT EXECUTION PERFORMED IN THIS PHASE.**

---

## 6. Provenance & Classification Refinements
- **Human Extension Provenance:** Verified in [FR02_HUMAN_TEST_CASES.md](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_HUMAN_TEST_CASES.md) and [FR02_HUMAN_EXTENSION_DESIGN.md](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_HUMAN_EXTENSION_DESIGN.md):
  > *"Student-selected and finalized Human Extension cases after AI-assisted coverage-gap analysis."*
- **`FR02-HUM-004` Oracle Classification:** Refined to `PARTIALLY SPECIFICATION-BACKED / STATE ISOLATION` (grounded in per-user authentication architecture without overstating explicit cross-account SRS wording).

---

## 7. Cryptographic & Git Commit Verification
- **Raw AI Draft SHA-256:** `b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c` *(Unchanged)*.
- **Commit Message:** `test(23127259): implement FR-02 Postman collection`
- **Commit SHA:** [`bfa9b92`](https://github.com/thangak18/HW06/commit/bfa9b92)
- **Branch:** `thang/hw06-implementation` (Pushed to `origin`, working tree clean).

```text
On branch thang/hw06-implementation
Your branch is up to date with 'origin/thang/hw06-implementation'.

nothing to commit, working tree clean
```

---

Execution is stopped here. Ready to proceed to **PHASE 1D.1 – FR-02 CONTROLLED POSTMAN/NEWMAN EXECUTION**.
```

---

## 3. Human Evaluation & Outcome

- **Verdict:** VALID. Materialized authoritative 40-case executable test specification (`FR02_FINAL_EXECUTABLE_SUITE.md`), traceability matrix (`FR02_EXECUTION_TRACEABILITY.md`), state strategy (`FR02_POSTMAN_STATE_STRATEGY.md`), Postman collection (`FR02_Login_Account_Lockout.postman_collection.json`), environment (`FR02-local.postman_environment.json`), and static validation report (`FR02_POSTMAN_STATIC_VALIDATION.md`). Zero SUT execution performed. Committed as `bfa9b92`.
- **Status:** EXACT OUTPUT AVAILABLE.
