# Interaction Log: INT-021

- **Interaction ID:** INT-021
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 20:23:14+07:00
- **Project Stage:** Phase 1D.2 – FR-02 Execution Reconciliation and Bug Confirmation
- **Transcript Reference:** `transcript_full.jsonl` (Prompt: Step 817, Output: Pending backfill)

---

## 1. Submitted Prompt

```text
/Speckit /Speckit We are starting:

PHASE 1D.2 – FR-02 EXECUTION RECONCILIATION, BUG CONFIRMATION, AND ISSUE-READY EVIDENCE

Current primary execution:

Run 03
- 40 formal FR-02 test cases
- 67 / 71 assertions passed
- 4 failed assertions reported
- execution commit: 6af5080

IMPORTANT:

Do NOT immediately file all four previously reported bug candidates.

Before GitHub Issue creation we must correct classification and independently
confirm each specification-backed defect.

Current reported candidates:

BUG-FR02-001
Plaintext password exposure in login response

BUG-FR02-002
Account remains locked after >30 seconds

BUG-FR02-003
Correct login at N=2 boundary triggers lockout

BUG-FR02-004
HTTP 500 for x-www-form-urlencoded login body

This phase must:
1. backfill INT-020
2. reconcile execution coverage
3. verify exact oracle provenance
4. independently reproduce genuine bugs
5. downgrade exploratory findings where necessary
6. prepare issue-ready evidence
7. NOT modify the SUT

==================================================
1. AI AUDIT NUMBERING
==================================================

Previous interaction:
INT-020 – FR-02 Controlled Postman/Newman Execution

Current interaction:
INT-021

First locate and backfill the COMPLETE actual output for INT-020 from the
completed Antigravity transcript.

Do not guess transcript indices.

Then create:

23127259/ai/interactions/INT-021-fr02-bug-confirmation.md

Record:
- actual tool
- actual model
- actual date/time
- timezone UTC+07:00
- stage:
  FR-02 Execution Reconciliation and Bug Confirmation
- THIS COMPLETE PROMPT verbatim

Append this exact prompt to:

23127259/ai/prompts/AI_PROMPT_LOG.md

Update:

23127259/ai/AI_AUDIT_REPORT.md

For INT-021 output use PENDING until this interaction finishes.

==================================================
2. PRESERVE EXISTING EXECUTION EVIDENCE
==================================================

DO NOT modify or overwrite:

FR02-run-01*
FR02-run-02*
FR02-run-03*

Do not hand-edit Newman JSON/HTML results.

Do not modify:
FR02_AI_DRAFT.md
TC_AUDIT_FR02.md

Do not modify the EShop SUT.

==================================================
3. CORRECT EXECUTION REPORT LANGUAGE
==================================================

Review:

23127259/newman/fr02/FR02_EXECUTION_SUMMARY.md
23127259/bugs/FR02_BUG_CANDIDATES.md
23127259/newman/fr02/FR02_HARNESS_REPAIRS.md

Correct any statement equivalent to:

"All assertions strictly reflect normative specification requirements."

That is too strong.

Use:

"No audited oracle was weakened to make the SUT pass.

The executable suite contains:
- specification-backed assertions
- partially specification-backed security assertions
- exploratory / engineering assertions.

Only failures with an explicit specification-backed oracle are eligible for
formal specification bug filing."

Do not erase prior raw execution evidence.

==================================================
4. RECONCILE FORMAL TEST EXECUTION COUNT
==================================================

There is an accounting question:

Phase 1D.0 collection architecture reported:
8 helpers + 40 formal cases = 48 logical requests.

Run 03 reports:
56 requests executed.

Determine exactly why.

Inspect:
- collection structure
- Newman Run 03 JSON
- request names
- any request chaining / repeated sequence steps

Create:

23127259/newman/fr02/FR02_RUN03_EXECUTION_COVERAGE.md

Include:

| Formal Test ID | Executed? | Request/Sequence Count | Assertions | Final Result |
|---|---|---:|---:|---|

List ALL 40 formal IDs.

Also separately list helpers / sequence-support requests:

| Helper / Support Request | Count | Why Executed |
|---|---:|---|

Explain mathematically why Newman executed 56 requests.

Required gate:

40 / 40 formal testcase IDs must have execution evidence.

If fewer than 40 formal IDs actually executed:
STOP.
Do not proceed to bug filing.

==================================================
5. BUG-FR02-001 – RESPONSE PASSWORD EXPOSURE
==================================================

Re-evaluate the formal oracle.

Do NOT use:

SEC-01 password-storage-at-rest

as the primary black-box oracle.

Check api_specification.md success response contract.

Determine whether the documented `user` response includes only fields such as:

id
name
email
role

and does NOT document password.

Also use the Human Audit correction for FR02-AI-028.

Correct classification should be approximately:

Sensitive Data Exposure / Login Response Contract Violation
[ADDITIONAL-SEC]

not:

"SEC-01 hashing failure proven."

Independently reproduce using a fresh normal login request.

Capture:

- request
- HTTP status
- relevant response JSON
- presence of `user.password`
- redact unrelated JWT value as necessary

Create:

23127259/bugs/evidence/FR02/BUG-FR02-001-reproduction.txt

If plaintext password is reliably returned:
status = CONFIRMED.

If password is not returned:
status = NOT REPRODUCED.

Do not alter SUT.

Severity:
reassess using actual impact.
Do not automatically call CRITICAL merely because password appears.
Document severity rationale.

==================================================
6. BUG-FR02-002 – LOCKOUT DOES NOT EXPIRE
==================================================

This is potentially a direct SRS FR-02 defect.

Create a FRESH dedicated account.

Do not reuse a previously contaminated account.

Reproduction sequence:

- ensure account initially authenticates successfully
- generate exactly the required consecutive failed-login sequence
- confirm active lock
- wait safely beyond documented 30-second duration
- e.g. >=35 seconds to avoid scheduler/network jitter
- submit correct credentials

Use actual timestamps.

Capture:

T0:
lock activation time

T1:
post-expiration authentication time

Elapsed:
T1 - T0

Expected:
after documented temporary lock interval expires, authentication with correct
credentials is processed normally.

Actual:
record exact status/body.

Create:

23127259/bugs/evidence/FR02/BUG-FR02-002-reproduction.txt

If still locked well beyond 30 seconds:
CONFIRMED.

Do not infer "permanent forever" unless tested indefinitely.

Safer title if confirmed:

"Account remains locked beyond documented 30-second lockout duration"

rather than:
"Permanent account lockout"

unless permanence is actually demonstrated.

==================================================
7. BUG-FR02-003 – VALID LOGIN AT N=2 BOUNDARY
==================================================

This is potentially a strong FR-02 state-machine defect.

Create another FRESH dedicated account.

Required exact sequence:

1. baseline correct login succeeds
2. wrong password attempt #1
3. wrong password attempt #2
4. correct password attempt

Record each:
- timestamp
- HTTP status
- response semantics

Formal oracle:

After exactly two consecutive FAILED logins:
account is not yet locked.

A correct authentication attempt is not the third FAILED login.

Successful authentication should be allowed and should reset the consecutive
failure progression according to FR-02.

Do not inspect internal login_attempts as the primary oracle.

Create:

23127259/bugs/evidence/FR02/BUG-FR02-003-reproduction.txt

If step 4 is rejected specifically because the account is considered locked:
CONFIRMED.

If step 4 succeeds:
NOT REPRODUCED.

==================================================
8. BUG-FR02-004 MUST BE RECLASSIFIED BY DEFAULT
==================================================

FR02-HUM-005 was previously classified:

EXPLORATORY / API CONTRACT

because the specification does not define exact behavior for
application/x-www-form-urlencoded.

Therefore HTTP 500 on that request must NOT automatically be treated as a
specification-backed FR-02 bug.

Unless an explicit requirement is found requiring graceful rejection of this
MIME type:

rename/reclassify it as:

OBS-FR02-001
Unhandled HTTP 500 on non-documented form-encoded login request

Classification:
EXPLORATORY / ROBUSTNESS OBSERVATION

Status:
NOT ELIGIBLE FOR SPEC-BACKED FR-02 GITHUB BUG ISSUE

Preserve its evidence.

Do NOT delete the observation.

If a truly explicit specification requirement is found, quote the exact
requirement before retaining bug status.

==================================================
9. NO SOURCE-CODE ROOT CAUSE CLAIM YET
==================================================

Do not write definitive root causes such as:

"server.js increments attempts before validating password"

unless source inspection is performed AFTER runtime confirmation and clearly
labelled:

SUPPLEMENTAL ROOT-CAUSE INSPECTION

Runtime behavior proves the defect.
Source inspection may explain it.

Do not let implementation become the oracle.

==================================================
10. CREATE CONFIRMATION MATRIX
==================================================

Create:

23127259/bugs/FR02_BUG_CONFIRMATION_MATRIX.md

Columns:

| ID | Related Test | Oracle Type | Reproduced? | Final Classification | GitHub Issue Eligible? |
|---|---|---|---|---|---|

Expected possible outcomes:

BUG-FR02-001
Specification/API-contract + additional security
Eligible if reproduced and contract basis exists

BUG-FR02-002
Specification-backed FR-02
Eligible if reproduced

BUG-FR02-003
Specification-backed FR-02
Eligible if reproduced

OBS-FR02-001
Exploratory robustness
Not eligible as formal spec-backed issue by default

==================================================
11. ISSUE-READY BUG REPORTS
==================================================

For every CONFIRMED and eligible bug create:

23127259/bugs/issues/BUG-FR02-00X.md

Use:

# Title

## Requirement

## Related Test Case

## Environment

## Preconditions

## Reproduction Steps

## Expected Result

## Actual Result

## Reproducibility

## Severity

## Severity Rationale

## Newman Evidence

## Independent Reproduction Evidence

## Screenshot Required

## Status

CONFIRMED – READY TO FILE

Do not file GitHub Issue yet in this interaction.

==================================================
12. SCREENSHOT EVIDENCE PLAN
==================================================

HW06 requires screenshots for genuine bugs.

Update:

23127259/bugs/FR02_SCREENSHOT_CHECKLIST.md

For each confirmed eligible bug identify what the STUDENT should capture from
real execution.

Examples:

BUG-FR02-001:
Postman response showing `user.password`

BUG-FR02-002:
real request after >30s showing locked response, ideally with timestamp context

BUG-FR02-003:
sequence/evidence showing two wrong attempts followed by rejected correct login

Do not generate fake screenshots.

Do not synthesize images.

The student must capture genuine evidence.

==================================================
13. EXECUTION SUMMARY CORRECTION
==================================================

Update execution summary to distinguish:

Newman failed assertions
vs
formal confirmed bugs
vs
exploratory observations

For example:

Run 03 failed assertions: 4

After oracle-based triage:
- confirmed spec/API-contract bugs: N
- exploratory observations: N
- harness failures: 0

Do not equate:
failed assertion count = confirmed bug count.

==================================================
14. AUDIT SAFETY
==================================================

If independent reproduction contradicts Run 03:
preserve both.

Do not hide the discrepancy.

Document:
INTERMITTENT / NOT REPRODUCED

where appropriate.

==================================================
15. GIT POLICY
==================================================

After confirmation and corrected documentation:

commit:

test(23127259): confirm FR-02 API defects

Include:
- confirmation matrix
- genuine reproduction text evidence
- issue-ready Markdown drafts
- corrected execution summary
- coverage reconciliation
- exploratory observation evidence
- screenshot checklist
- INT-020 completed output
- INT-021 audit files
- AI_AUDIT_REPORT.md
- AI_PROMPT_LOG.md

Do not include fabricated screenshots.

Push:
origin/thang/hw06-implementation

Do NOT merge main.

Do NOT create GitHub issues yet.

==================================================
16. END REPORT
==================================================

Return:

# Phase 1D.2 Completion Report

## AI Audit
- INT-020 output backfilled
- INT-021 prompt stored
- INT-021 output pending

## Execution Coverage
- formal IDs executed: X / 40
- helper/support requests
- explanation for 56 total requests

## BUG-FR02-001
- oracle basis
- independent reproduction result
- final severity
- final classification
- GitHub issue eligible?

## BUG-FR02-002
- elapsed lockout test time
- reproduction result
- final classification
- GitHub issue eligible?

## BUG-FR02-003
- exact N=2 sequence
- reproduction result
- final classification
- GitHub issue eligible?

## OBS-FR02-001
- original test
- why exploratory
- preserved actual behavior
- issue eligible: NO unless explicit requirement found

## Final Triage

| Classification | Count |
|---|---:|
| Confirmed spec/API-contract bugs | N |
| Exploratory observations | N |
| Harness failures | 0 |
| Not reproduced | N |

## Evidence
List paths.

## Git
- commit SHA
- push result
- git status

Then STOP.

Next phase:

PHASE 1D.3 – FR-02 REAL SCREENSHOT EVIDENCE AND GITHUB ISSUE FILING
```

---

## 2. Exact AI Output

```markdown
PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES
```

---

## 3. Human Evaluation & Outcome

- **Verdict:** In progress. Reconciling 40-case execution coverage across 56 requests, independently reproducing defects, downgrading exploratory findings (OBS-FR02-001), generating confirmation matrix and issue-ready drafts.
- **Status:** EXACT PROMPT STORED; OUTPUT PENDING BACKFILL.
