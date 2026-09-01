# Interaction Log: INT-020

- **Interaction ID:** INT-020
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 20:11:35+07:00
- **Project Stage:** Phase 1D.1 – FR-02 Controlled Postman/Newman Execution and Result Triage
- **Transcript Reference:** `transcript_full.jsonl` (Prompt: Step 714, Output: Pending backfill)

---

## 1. Submitted Prompt

```text
/Speckit /Speckit We are starting:

PHASE 1D.1 – FR-02 CONTROLLED POSTMAN/NEWMAN EXECUTION AND RESULT TRIAGE

Current state:

FR-02 final executable suite:
40 formal test cases

Breakdown:
- 35 usable AI-derived cases
- 5 Student-selected/finalized Human Extensions
- 4 setup/helper requests not counted as test cases

Postman collection:
23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json

Environment:
23127259/postman/environments/FR02-local.postman_environment.json

Previous implementation commit:
bfa9b92

IMPORTANT:

This is the FIRST FORMAL EXECUTION phase for FR-02.

We will now:
1. backfill INT-019
2. verify the test harness
3. start/verify the SUT
4. run controlled Newman execution
5. preserve genuine raw output
6. distinguish:
   - PASS
   - SPEC FAILURE / BUG CANDIDATE
   - TEST HARNESS FAILURE
   - SPEC-UNDEFINED / EXPLORATORY OBSERVATION
7. repair ONLY test harness defects if necessary
8. rerun after harness repair
9. create genuine Newman evidence

DO NOT:
- modify EShop SUT source
- change a specification oracle merely to make a failing test pass
- fabricate pass/fail results
- fabricate screenshots
- call every failed assertion a product bug
- create GitHub Issues before triage is complete
- merge to main
- start FR-10 or FR-14

==================================================
1. AI AUDIT NUMBERING
==================================================

Previous interaction:
INT-019
FR-02 Final Executable Suite + Postman Implementation

Current interaction:
INT-020

First recover the COMPLETE exact output for INT-019 from the completed
Antigravity transcript.

Find the real:
- USER_INPUT
- corresponding PLANNER_RESPONSE

Do not guess step numbers.

Update:
23127259/ai/interactions/INT-019-fr02-postman-implementation.md

Then create:
23127259/ai/interactions/INT-020-fr02-controlled-execution.md

Record:
- actual Tool
- actual Model
- actual Date
- actual Local Time
- timezone UTC+07:00
- Stage:
  FR-02 Controlled Postman/Newman Execution
- THIS COMPLETE PROMPT verbatim

Append this exact prompt to:
23127259/ai/prompts/AI_PROMPT_LOG.md

Update:
23127259/ai/AI_AUDIT_REPORT.md

For INT-020 Exact AI Output initially use:
PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES

Do not fabricate the current output before it exists.

==================================================
2. VERIFY RAW AND AUDITED ARTIFACT INTEGRITY
==================================================

Verify:

shasum -a 256 23127259/testcases/FR02_AI_DRAFT.md

Expected:
b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c

Do not modify:
23127259/testcases/FR02_AI_DRAFT.md
23127259/ai/TC_AUDIT_FR02.md

Also verify the executable suite still contains:
40 formal executable cases.

If raw hash changed unexpectedly:
STOP.

==================================================
3. PRE-EXECUTION COLLECTION INSPECTION
==================================================

Before making ANY HTTP request, inspect:

23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json
23127259/postman/environments/FR02-local.postman_environment.json
23127259/testcases/FR02_EXECUTION_TRACEABILITY.md
23127259/docs/FR02_POSTMAN_STATE_STRATEGY.md

Verify:

- collection JSON parses
- 40 unique formal testcase IDs exist
- FR02-AI-016 absent
- FR02-AI-017 absent
- exactly 5 FR02-HUM IDs
- helpers clearly labelled as helpers
- no live JWT hardcoded
- all formal requests receive X-Student-Id
- baseUrl resolves to http://localhost:3000
- stateful sequences are actually implemented as sequences rather than only
  single isolated requests with comments
- corrected INCOMPLETE cases use the audited oracle rather than raw oracle

If a static implementation defect is found:
repair the TEST HARNESS before execution.

Document the repair.

Do not change specification expectations.

==================================================
4. IDEMPOTENT SETUP CHECK
==================================================

The collection uses documented POST /api/register setup helpers.

Before full execution, inspect whether setup is repeatable.

The same collection may be executed multiple times.

Therefore setup helpers must tolerate:
- account already exists
or
- dynamically create uniquely named dedicated accounts

Do not treat "email already registered" during setup as an SUT bug.

Preferred approach:
use dynamic per-run suffixes where appropriate, for example a timestamp or
run ID stored as a collection/environment variable.

However:
preserve stable credentials where specific seeded user/admin fixtures are
required.

Document exactly which accounts are:
- seeded fixtures
- dynamically generated test accounts

Do not modify SUT DB directly as normal setup.

==================================================
5. STATEFUL ACCOUNT ISOLATION CHECK
==================================================

Confirm that one test does not unintentionally poison another test.

At minimum distinguish accounts for:
- basic positive login
- generic negative-domain cases
- N=1/N=2/N=3 lockout progression
- active-lock scenarios
- timing scenarios
- reset-after-success scenarios
- Human N=2 reset case
- Human cross-account isolation case

If multiple test IDs intentionally share one sequence:
document the execution dependency explicitly.

Do not depend on an undocumented `login_attempts` API response.

Use externally observable state only.

==================================================
6. VERIFY SUT AVAILABILITY
==================================================

Use the known SUT location:

/Volumes/Thang/eshop-sut/backend

Check:
- whether port 3000 is already listening
- whether an EShop backend process is already running

If a healthy correct SUT process is already running:
reuse it.

If not:
start the SUT using the legitimate project command / node server.js as
appropriate.

Do not modify the SUT source.

Record:
- startup command
- PID if available
- hostname
- port
- startup time

==================================================
7. EXECUTION PRE-FLIGHT
==================================================

Perform only a minimal pre-flight before the full suite:

- verify the API host responds
- verify one harmless documented endpoint or setup helper works
- verify X-Student-Id is actually sent
- verify environment variables resolve

Do not use pre-flight to decide whether specification failures should be
ignored.

If pre-flight reveals a HARNESS problem:
fix harness, document, then proceed.

If pre-flight reveals a likely SUT defect:
do not modify SUT.
Proceed carefully to formal evidence collection where possible.

==================================================
8. FIRST FORMAL NEWMAN RUN
==================================================

Create an evidence directory if needed:

23127259/newman/fr02/

Run the COMPLETE formal collection using Newman.

Use the real collection and environment.

Generate at minimum:
- CLI output
- machine-readable JSON report
- HTML report using htmlextra if installed

Suggested artifact names:

23127259/newman/fr02/FR02-run-01-console.txt
23127259/newman/fr02/FR02-run-01.json
23127259/newman/fr02/FR02-run-01.html

Use an actual command equivalent to:

newman run <collection> \
  -e <environment> \
  -r cli,json,htmlextra \
  --reporter-json-export <json-path> \
  --reporter-htmlextra-export <html-path>

Use actual installed reporter syntax.

Capture stdout/stderr honestly.

Do not fabricate files if Newman fails before generating them.

==================================================
9. DO NOT AUTO-CALL FAILURES BUGS
==================================================

After run 01, classify every failed formal case into exactly one category:

A. SPEC FAILURE / BUG CANDIDATE

Criteria:
- expected result is supported by SRS/API-SPEC or accepted Human Audit oracle
- harness executed correctly
- test precondition was valid
- actual result contradicts expected behavior

B. TEST HARNESS FAILURE

Examples:
- wrong variable
- invalid setup sequence
- test account unintentionally locked by previous case
- bad Postman script
- wrong request body encoding created by our collection
- helper registration collision
- timeout caused by test harness logic
- stale token variable

This is NOT an SUT bug.

C. SPEC-UNDEFINED / EXPLORATORY OBSERVATION

Examples:
- MIME behavior where exact response is undefined
- exact error key
- exact Content-Type where audit downgraded oracle
- undocumented parser behavior

Do not mark as product failure unless a supported invariant is violated.

D. PASS

Expectation and actual behavior align.

==================================================
10. CREATE EXECUTION TRIAGE ARTIFACT
==================================================

Create:

23127259/newman/fr02/FR02_RUN01_TRIAGE.md

Use:

| Test ID | Result | Actual | Expected Oracle | Classification | Evidence | Action |
|---|---|---|---|---|---|---|

Classification:
PASS
BUG CANDIDATE
TEST HARNESS FAILURE
SPEC-UNDEFINED OBSERVATION

Every failed Newman assertion must appear in this table.

==================================================
11. HARNESS REPAIR POLICY
==================================================

If Run 01 contains TEST HARNESS FAILURE:

you MAY fix:
- Postman request configuration
- scripts
- environment variables
- setup helpers
- request sequencing
- waits
- dynamic test data

You MUST NOT:
- alter SRS/API expected behavior
- loosen a valid assertion because the SUT failed it
- edit server.js
- edit database.js
- modify SUT implementation

For every harness repair create:

23127259/newman/fr02/FR02_HARNESS_REPAIRS.md

Columns:

| Repair ID | Test IDs Affected | Problem | Root Cause | Harness Change | Oracle Changed? |
|---|---|---|---|---|---|

Oracle Changed? must be:
NO

unless the Human Audit itself contained a clerical implementation mismatch,
in which case STOP and report before changing it.

==================================================
12. SECOND CONTROLLED RUN IF HARNESS WAS REPAIRED
==================================================

If any harness repair was necessary:

run the full collection again.

Artifacts:

FR02-run-02-console.txt
FR02-run-02.json
FR02-run-02.html

Create:
FR02_RUN02_TRIAGE.md

Run 02 becomes the primary execution result after legitimate harness repair.

Preserve Run 01.

Never overwrite raw Run 01 evidence.

If no harness repair was required:
Run 01 remains the primary formal execution.

==================================================
13. TIMING TEST SAFETY
==================================================

FR02 includes real 30-second lockout tests.

Do not shorten the lockout oracle merely to save execution time.

Measure actual elapsed time where practical.

For before-expiry:
use the implemented safe pre-expiry point.

For after-expiry:
use the implemented safe post-expiry point.

If runtime scheduling causes ambiguous timing:
classify as HARNESS/TIMING issue and rerun with safer bracketing.

Do not classify timing jitter as product bug without reliable evidence.

==================================================
14. SECURITY TEST INTERPRETATION
==================================================

For SEC-05 black-box tests:

Passing means:
SQLi behavioral bypass not observed for tested payload.

It does NOT mean:
parameterized queries proven.

For SEC-01 response-sanitization test:

Passing means:
plaintext password not exposed in tested response.

It does NOT prove:
password storage at rest is hashed.

Keep these distinctions in execution reporting.

==================================================
15. BUG CANDIDATE CONSOLIDATION
==================================================

After primary run, create:

23127259/bugs/FR02_BUG_CANDIDATES.md

Include ONLY genuine specification-backed mismatches.

For each:

- Candidate ID
- Related Test Case
- Requirement
- Expected
- Actual
- Reproduction Preconditions
- Reproduction Steps
- Severity Estimate
- Newman Evidence Reference
- Status: CANDIDATE – NOT YET FILED

Do not create GitHub Issues in this phase yet.

Do not include:
- harness failures
- exploratory mismatches
- spec-undefined differences

==================================================
16. EXECUTION SUMMARY
==================================================

Create:

23127259/newman/fr02/FR02_EXECUTION_SUMMARY.md

Report:

- total executable cases: 40
- passed
- bug-candidate failures
- harness failures before repair
- exploratory observations
- final primary run
- helpers executed
- total assertions
- Newman version
- Node version
- hostname/base URL
- X-Student-Id
- execution timestamp

Do not hide failures.

==================================================
17. EVIDENCE INTEGRITY
==================================================

Never hand-edit Newman JSON/HTML to alter results.

You may redact a runtime JWT/token VALUE if it is accidentally embedded in a
text artifact before committing.

Use:
[REDACTED_RUNTIME_JWT]

Do not falsify surrounding evidence.

Inspect reports before commit for:
- tokens
- passwords if sensitive
- API keys
- secrets

Seed/demo fixture passwords may be documented only if they are intentionally
public test fixtures.

==================================================
18. SCREENSHOT POLICY
==================================================

HW06 requires screenshots for genuine bugs.

Do NOT fabricate screenshots.

In this phase:
if genuine bug candidates exist, identify exactly which real evidence screen
should later be captured manually from:
- Postman
or
- Newman output

You may create a screenshot checklist:

23127259/bugs/FR02_SCREENSHOT_CHECKLIST.md

but do not synthesize images.

==================================================
19. POSTMAN FEATURES UPDATE
==================================================

Update:

23127259/docs/POSTMAN_FEATURES_FR02.md

Only now mark features actually used.

You may now mark:
- Collections
- Folders
- Environment Variables
- Pre-request Scripts
- Tests
- Data-driven Runner if actually executed
- Newman if actually executed

Do not mark:
- Monitor
- Mock Server
- CI/CD

unless truly performed.

==================================================
20. EXECUTION COMMIT
==================================================

Do NOT use a commit message implying all tests pass unless they actually do.

Use neutral commit:

test(23127259): execute FR-02 API test suite

Include:
- actual Newman reports
- raw console logs
- execution summary
- triage
- harness repair log if applicable
- bug candidate report if applicable
- updated collection/environment if harness fixes were made
- POSTMAN_FEATURES_FR02.md
- INT-019 completed audit backfill
- INT-020 interaction evidence
- AI_AUDIT_REPORT.md
- AI_PROMPT_LOG.md

Do NOT include:
- fake screenshot
- fabricated bug evidence

Push:
origin/thang/hw06-implementation

Do NOT merge to main.

==================================================
21. END REPORT
==================================================

Return:

# Phase 1D.1 Completion Report

## AI Audit
- INT-019 output backfilled
- INT-020 prompt stored
- INT-020 output pending

## SUT
- startup/reuse status
- base URL
- process/port status

## Pre-flight
- result
- harness fixes before formal run

## Formal Execution
- Run 01 command
- Run 01 total testcases
- Run 01 assertions
- Run 01 passes
- Run 01 failures

## Triage
- PASS count
- BUG CANDIDATE count
- TEST HARNESS FAILURE count
- SPEC-UNDEFINED OBSERVATION count

## Harness Repair
- repairs performed
- oracle changes: MUST be NO
- Run 02 required? YES/NO

## Primary Final Run
- run identifier
- total formal testcases
- passed
- specification-backed failed cases
- exploratory observations

## Bug Candidates
For each:
- candidate ID
- testcase
- requirement
- expected
- actual

## Evidence
- console log
- JSON report
- HTML report
- summary path
- triage path

## Security
- runtime tokens redacted?
- hardcoded secret leakage?

## Git
- commit SHA
- push result
- git status

Then STOP.

DO NOT CREATE GITHUB ISSUES YET.

Next phase:

PHASE 1D.2 – FR-02 BUG CONFIRMATION, EVIDENCE, AND GITHUB ISSUE FILING
```

---

## 2. Exact AI Output

```markdown
PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES
```

---

## 3. Human Evaluation & Outcome

- **Verdict:** In progress. Executing controlled Newman run for FR-02, performing result triage, identifying specification bug candidates vs harness defects, and logging genuine execution reports.
- **Status:** EXACT PROMPT STORED; OUTPUT PENDING BACKFILL.
