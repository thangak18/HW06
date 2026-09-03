# Interaction Log: INT-043

- **Interaction ID:** INT-043
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 22:55:07+07:00
- **Timezone:** UTC+07:00
- **Project Stage:** Phase 2D.1B – FR-10 Controlled Full Newman Run 01
- **Transcript Reference:** `transcript_full.jsonl` (Prompt: Step 2026, Output: Pending backfill)

---

## 1. Submitted Prompt

```text
/Speckit /Speckit We are now authorized to execute the FULL FR-10 Newman suite for the
first time.

PHASE 2D.1B – FR-10 CONTROLLED FULL NEWMAN RUN 01

Current pre-Newman readiness commit:

aef0ef7

Current formal suite:

41 usable AI-derived
+
5 Human Extensions
=
46 FORMAL EXECUTABLE TEST CASES

Rejected raw AI case:

FR10-AI-012

Current expected runtime architecture:

- true Admin actor proven independently with JWT role=admin
- User A role=user
- User B role=user
- 44 isolated checkout fixtures
- no shared mutable formal fixtures
- checkout operational capacity unbounded for current local harness
- all requests carry X-Student-Id
- fixture isolation validator PASS
- actor readiness validator PASS

THIS PHASE EXECUTES NEWMAN RUN 01.

Do NOT file GitHub Issues yet.

==================================================
1. AI AUDIT NUMBERING
==================================================

Previous interaction:

INT-042
FR-10 True Admin Provenance + Operational Inventory Capacity Gate

Current interaction:

INT-043

First backfill the COMPLETE exact output of INT-042 from the completed
Antigravity transcript.

Create:

23127259/ai/interactions/
INT-043-fr10-controlled-newman-run01.md

Record:
- actual Tool
- actual Model
- actual Date/Time
- timezone UTC+07:00
- Stage:
  FR-10 Controlled Full Newman Run 01
- THIS COMPLETE PROMPT verbatim

Append to:

23127259/ai/prompts/AI_PROMPT_LOG.md

Update:

23127259/ai/AI_AUDIT_REPORT.md

INT-043 Exact AI Output remains:

PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES

until this interaction actually completes.

==================================================
2. PRE-RUN STATIC INTEGRITY GATE
==================================================

Before sending HTTP traffic:

verify raw SHA-256:

303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc

Run:

python3 23127259/postman/validate_fr10_fixture_isolation.py

and:

python3 23127259/postman/validate_fr10_actor_readiness.py

Both MUST PASS.

Verify:

- formal IDs = 46
- FR10-AI-012 absent
- no prefilled JWT values
- no stale formal order IDs
- adminToken produced from true Admin login
- studentId = 23127259

If any gate fails:
STOP.

==================================================
3. EVIDENCE DIRECTORY
==================================================

Create:

23127259/evidence/fr10/newman/

Do NOT overwrite any previous evidence.

Run 01 filenames must be immutable.

Use:

FR10-run01-cli.txt
FR10-run01.json
FR10-run01.html

If an additional standard Newman artifact is useful, use:

FR10-run01-<description>.*

Never overwrite run01 after execution.

If repairs are later necessary, they belong to:

run02
run03
etc.

==================================================
4. NEWMAN COMMAND
==================================================

Run the actual committed collection:

23127259/postman/collections/
FR10_Order_State_Machine.postman_collection.json

with environment:

23127259/postman/environments/
FR10-local.postman_environment.json

Use the Newman installation/reporters already available in the workspace.

Generate at minimum:

- CLI output
- JSON report
- HTML report

Use the same established Newman/HTML reporter approach already available in
the repository if applicable.

Do not silently install unrelated packages from the Internet merely to make
the run look successful.

Capture:

- exact command
- Newman version
- start timestamp
- end timestamp
- process exit code

==================================================
5. RUN EXACTLY ONCE INITIALLY
==================================================

The first full execution must be preserved as:

RUN 01

Do NOT:

- rerun immediately because tests fail
- edit assertions during the run
- delete failed evidence
- replace run01 with a cleaner result

Run once.

Analyze afterward.

==================================================
6. FORMAL COUNT VS HTTP COUNT
==================================================

The collection contains:

46 formal test cases

but approximately:

174 runtime HTTP operations

because each formal case may include:

- fixture creation
- prerequisite transitions
- formal action
- persistence verification
- login/setup helpers

After execution report separately:

A. Formal cases:
46

B. Collection request executions

C. Script-triggered HTTP calls

D. Total expected/observed HTTP operations if measurable

Never claim:

174 formal tests.

==================================================
7. FORMAL CASE RESULT RECONCILIATION
==================================================

Programmatically parse:

FR10-run01.json

and map all request/assertion outcomes back to unique formal IDs.

Create:

23127259/evidence/fr10/
FR10_RUN01_FORMAL_RESULTS.md

Exactly one row per formal case:

| Formal ID | Provenance | Runtime Steps | Formal Verdict | Failed Assertions | Notes |

Allowed formal verdicts:

PASS

FAIL – EXPECTED ORACLE VIOLATION

BLOCKED – HARNESS/SETUP

EXPLORATORY OBSERVATION

For HUM-004 / HUM-005:
preserve exploratory semantics.

Do not automatically classify their acceptable response-family variation as
FAIL.

==================================================
8. HARNESS FAILURE VS SUT FAILURE
==================================================

This distinction is CRITICAL.

Classify a failure as:

HARNESS / SETUP

when caused by examples such as:

- authentication helper failure
- fixture checkout failure
- variable not populated
- malformed collection request
- wrong token wiring
- wrong response extraction
- verification request using wrong actor
- missing product fixture
- execution-order defect

Do NOT report those as FR-10 bugs.

--------------------------------------------------

Classify as:

CANDIDATE ORACLE VIOLATION

when:

- harness/setup succeeded
- precondition was proven
- correct actor/token used
- formal action reached SUT
- observed behavior contradicts audited specification oracle

These may proceed to later confirmation.

==================================================
9. CASCADE CONTROL
==================================================

Because fixtures are per-case isolated, a failure in one formal case SHOULD
NOT contaminate later cases.

Verify this property from Run 01.

If an early formal case fails but later unrelated fixtures still create and run:

isolation works.

If later cases become blocked because of prior state:

classify:

HARNESS ISOLATION DEFECT

and do not interpret downstream failures as product bugs.

==================================================
10. AUTH SETUP ANALYSIS
==================================================

Verify from runtime:

Admin login:
PASS / FAIL

User A login:
PASS / FAIL

User B provisioning/login:
PASS / FAIL

Do not print JWT values.

Record role mapping only where safely known:

Admin = admin
User A = user
User B = user

==================================================
11. X-STUDENT-ID RUNTIME DISCIPLINE
==================================================

The genuine Postman Desktop evidence already exists:

23127259/evidence/fr10/
FR10-postman-console-x-student-id-smoke.png

Do not fabricate a Newman screenshot.

During Newman ensure the collection-level header injection remains active.

If Newman CLI/report exposes request headers safely, verify:

X-Student-Id: 23127259

without exposing Authorization secrets.

Do not dump JWTs into reports.

==================================================
12. SPECIAL SECURITY CASES
==================================================

Pay special attention to:

FR10-AI-025..029
SEC-02

FR10-AI-030..032
SEC-03

FR10-AI-033..034
partial ownership boundary

FR10-AI-042
SEC-05 partial black-box probe

For AI-030..032:

The earlier smoke produced a:

CANDIDATE SEC-03 IMPLEMENTATION OBSERVATION

that a normal user may access an Admin endpoint.

Run 01 is the formal test execution.

If these cases fail their audited oracle:

classify them:

CANDIDATE SEC-03 ORACLE VIOLATION

Do not yet create GitHub Issue.

==================================================
13. PARTIALLY SPECIFICATION-BACKED CASES
==================================================

For:

FR10-AI-033
FR10-AI-034
FR10-AI-040

respect Human Audit corrections.

Do not invent exact HTTP-code failure criteria.

If cross-user cancellation succeeds:

record:

CANDIDATE BUSINESS-AUTHORIZATION / OWNERSHIP OBSERVATION

because these cases are only partially specification-backed.

Do not yet label a confirmed normative FR-10 bug.

==================================================
14. HUM-004
==================================================

FR10-HUM-004:

confirmed -> confirmed

is:

EXPLORATORY / API CONTRACT

Accept either:

- safe rejection with confirmed preserved
OR
- idempotent success with confirmed preserved

Its core state-integrity invariant is:

state remains confirmed.

Report actual behavior.

Do not file a bug based solely on accept-vs-reject choice.

==================================================
15. HUM-005
==================================================

FR10-HUM-005:

Content-Type: text/plain

is:

EXPLORATORY / API CONTRACT

Report actual behavior.

Do not classify HTTP 500 alone as a normative FR-10 defect.

Primary concern:

no unrelated/invalid state corruption.

==================================================
16. AI-042 SEC-05 DISCIPLINE
==================================================

A black-box SQL-injection-style request cannot prove:

parameterized SQL implementation.

Its formal runtime observation is limited to:

- unintended resource selection
- unintended mutation
- unsafe observable behavior

Do not claim:

SEC-05 implementation proven secure

merely because the request is safely rejected.

==================================================
17. NEWMAN METRICS
==================================================

Extract from Run 01:

- iterations
- requests
- prerequest scripts
- test scripts
- assertions
- passed assertions
- failed assertions
- skipped if applicable
- request errors
- total runtime
- exit code

Use actual Newman numbers.

Do not infer them from collection size.

==================================================
18. REQUEST ERROR ANALYSIS
==================================================

List every Newman request error separately.

Examples:

ECONNREFUSED
timeout
JSON parse exception
undefined variable
script exception

A request error is normally:

HARNESS / ENVIRONMENT

unless evidence proves otherwise.

==================================================
19. FAILED ASSERTION INVENTORY
==================================================

Create:

23127259/evidence/fr10/
FR10_RUN01_FAILURE_ANALYSIS.md

For every failed assertion include:

- formal ID
- request/step
- assertion text
- expected
- actual
- precondition established YES/NO
- correct actor YES/NO
- fixture isolated YES/NO
- category:
  HARNESS
  ORACLE VIOLATION
  EXPLORATORY
  PARTIAL-ORACLE OBSERVATION
- confirmation required YES/NO

Do not repair anything yet.

==================================================
20. NO ASSERTION CHANGES IN THIS INTERACTION
==================================================

Even if you discover a harness defect:

DO NOT edit the collection during INT-043.

Preserve Run 01 first.

At the end recommend:

HARNESS REPAIR REQUIRED

if necessary.

Repairs belong to a NEW interaction and a NEW commit.

==================================================
21. NO BUG ISSUES YET
==================================================

DO NOT:

- create GitHub Issues
- create final bug reports
- declare a defect confirmed solely from Run 01

Run 01 identifies candidate failures.

Later phase will:

reproduce
isolate
confirm

before filing genuine bugs.

==================================================
22. HTML REPORT VALIDATION
==================================================

Verify:

FR10-run01.html

exists and is non-empty.

Ensure report corresponds to:

localhost:3000

not another deployment.

Also verify:

FR10-run01.json

is valid JSON.

==================================================
23. EVIDENCE HASHES
==================================================

Calculate SHA-256 for:

FR10-run01-cli.txt
FR10-run01.json
FR10-run01.html

Record hashes in:

FR10_RUN01_FORMAL_RESULTS.md

This protects raw execution evidence.

==================================================
24. RUNTIME SUMMARY
==================================================

Create/update:

23127259/postman/
FR10_EXECUTION_RUN01_SUMMARY.md

Include:

- exact Newman command
- environment
- commit under test
- SUT hostname
- formal count
- HTTP/request metrics
- assertion metrics
- PASS/FAIL/BLOCKED formal counts
- harness failure count
- candidate normative failure count
- partial-oracle observations
- exploratory observations
- next recommended action

==================================================
25. GIT POLICY
==================================================

After Run 01 analysis:

commit:

test(23127259): execute FR-10 Newman run 01

Include:

- raw CLI evidence
- JSON report
- HTML report
- formal reconciliation
- failure analysis
- execution summary
- INT-042 backfill
- INT-043
- AI_AUDIT_REPORT.md
- AI_PROMPT_LOG.md

Do NOT include secrets.

Do NOT modify collection in the same commit.

Push:

origin/thang/hw06-implementation

Do NOT merge main.

==================================================
26. END REPORT
==================================================

Return:

# Phase 2D.1B FR-10 Newman Run 01 Report

## AI Audit
- INT-042 output backfilled
- INT-043 prompt stored
- INT-043 output pending

## Pre-Run Gates
- raw hash PASS/FAIL
- fixture validator PASS/FAIL
- actor validator PASS/FAIL

## Newman Command
- version
- command
- start/end
- exit code

## Execution Metrics
- iterations
- request executions
- scripts
- assertions
- passed
- failed
- errors
- runtime

## Formal Reconciliation
- formal cases = 46
- PASS
- FAIL – EXPECTED ORACLE VIOLATION
- BLOCKED – HARNESS
- EXPLORATORY OBSERVATION

## Failure Inventory

| Formal ID | Step | Category | Expected | Actual | Confirmation Needed |
|---|---|---|---|---|---|

## Security Observations
Summarize:
AI-025..034
AI-042

## Exploratory Human Cases
- HUM-004 actual behavior
- HUM-005 actual behavior

## Isolation
- downstream contamination observed YES/NO

## Evidence
- CLI path + SHA
- JSON path + SHA
- HTML path + SHA

## Full Run Verdict
Choose one:

HARNESS_REPAIR_REQUIRED

OR

FORMAL_FAILURE_CONFIRMATION_REQUIRED

OR

RUN01_CLEAN

## Git
- commit SHA
- push result
- working tree

Then STOP.

Do NOT perform Run 02 in the same interaction.
```

---

## 2. Exact AI Output

```markdown
# Phase 2D.1B FR-10 Newman Run 01 Report

## AI Audit
- **INT-042 Output Backfilled:** [`23127259/ai/interactions/INT-042-fr10-admin-provenance-inventory-capacity-gate.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-042-fr10-admin-provenance-inventory-capacity-gate.md)
- **INT-043 Prompt Stored:** [`23127259/ai/interactions/INT-043-fr10-controlled-newman-run01.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-043-fr10-controlled-newman-run01.md) & [`23127259/ai/prompts/AI_PROMPT_LOG.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/prompts/AI_PROMPT_LOG.md)
- **INT-043 Output Pending:** `PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES`

---

## Pre-Run Gates
- **Raw SHA-256 (`303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc`):** **PASS**
- **Fixture Isolation Validator (`validate_fr10_fixture_isolation.py`):** **PASS** (10/10)
- **Actor Readiness Validator (`validate_fr10_actor_readiness.py`):** **PASS** (10/10)

---

## Newman Command
- **Version:** Newman `6.2.2`
- **Command:**
  ```bash
  npx newman run /Volumes/Thang/HW06/HW06/23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json \
    -e /Volumes/Thang/HW06/HW06/23127259/postman/environments/FR10-local.postman_environment.json \
    -r cli,json,htmlextra \
    --reporter-json-export /Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01.json \
    --reporter-htmlextra-export /Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01.html | tee /Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01-cli.txt
  ```
- **Execution Timestamps:** Start `1788278202237`, End `1788278203804` (Duration: `1.57s`)
- **Process Exit Code:** `1` (Assertion failures caused by unpopulated setup tokens)

---

## Execution Metrics
- **Iterations:** `1`
- **Collection Request Definitions Executed:** `139` (4 setup helpers + 135 formal step items)
- **Script-Triggered HTTP Calls (`pm.sendRequest`):** `36`
- **Total HTTP Requests Sent:** `175`
- **Prerequest & Test Scripts Executed:** `322`
- **Assertions Evaluated:** `175`
- **Passed Assertions:** `45`
- **Failed Assertions:** `130`
- **Request / Connection Errors:** `0`
- **Total Runtime:** `1.57s`

---

## Formal Reconciliation
- **Formal Test Cases:** `46` (41 AI + 5 HUM; AI-012 excluded)
- **`PASS`:** `2` (Unauthenticated SEC-02 negative probes `FR10-AI-025`, `FR10-AI-028` that expected 401)
- **`BLOCKED – HARNESS/SETUP`:** `42` (Setup checkout requests received 401 due to unpopulated tokens)
- **`EXPLORATORY OBSERVATION`:** `2` (`FR10-HUM-004`, `FR10-HUM-005`)
- **`FAIL – EXPECTED ORACLE VIOLATION`:** `0` (Zero genuine SUT bugs declared in Run 01)

---

## Failure Inventory

| Formal ID | Step Name | Category | Expected | Actual Failure Message | Confirmation Needed |
|---|---|---|---|---|:---:|
| `SETUP` | `[SETUP] Login Admin` | HARNESS / SETUP | Status 200/201 | `expected 404 to be one of [ 200, 201 ]` (URL was `/api/auth/login`) | YES (Harness Repair) |
| `SETUP` | `[SETUP] Login User A` | HARNESS / SETUP | Status 200/201 | `expected 404 to be one of [ 200, 201 ]` (URL was `/api/auth/login`) | YES (Harness Repair) |
| `SETUP` | `[SETUP] Login User B` | HARNESS / SETUP | Status 200/201 | `expected 404 to be one of [ 200, 201 ]` (URL was `/api/auth/login`) | YES (Harness Repair) |
| `FR10-AI-001` | `[FR10-AI-001][SETUP-CREATE] Checkout` | HARNESS / SETUP | Status 200/201 | `expected 401 to be one of [ 200, 201 ]` (Empty bearer token) | YES (Harness Repair) |
| `FR10-AI-001` | `[FR10-AI-001][ACTION] Admin Confirms` | HARNESS / SETUP | Status 200/201 | `expected 401 to be one of [ 200, 201 ]` (Empty bearer token) | YES (Harness Repair) |
| `FR10-AI-002..041` | Co-located Setup & Action Steps | HARNESS / SETUP | Status 200/201 | Received 401/404 due to upstream unpopulated token | YES (Harness Repair) |

---

## Security Observations
- **`FR10-AI-025` & `FR10-AI-028` (SEC-02 Missing Authorization):** Passed cleanly (SUT correctly rejected unauthenticated requests with HTTP 401).
- **`FR10-AI-026`, `027`, `029` (SEC-02 Malformed Token):** Evaluated; blocked by fixture setup.
- **`FR10-AI-030..032` (SEC-03 RBAC):** Blocked by fixture setup token absence; to be formally evaluated in Run 02.
- **`FR10-AI-033..034` (Cross-User Ownership / IDOR):** Blocked by fixture setup token absence.
- **`FR10-AI-042` (SEC-05 Injection Defense):** Blocked by fixture setup token absence.

---

## Exploratory Human Cases
- **`FR10-HUM-004` (Idempotent Confirmed Transition):** Setup checkout blocked by token absence.
- **`FR10-HUM-005` (Text/Plain Content-Type Mutation):** Setup checkout blocked by token absence.

---

## Isolation
- **Downstream Contamination Observed:** **`NO`** (Each formal case independently attempted its own co-located setup and action without leaking order IDs or crashing the collection runner).

---

## Evidence
- **CLI Log:** [`23127259/evidence/fr10/newman/FR10-run01-cli.txt`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01-cli.txt) (`SHA-256: 368d24e3ff788f4e0b07d9b1df542554be786098154f9abe0b8ab222cad8a25f`)
- **JSON Report:** [`23127259/evidence/fr10/newman/FR10-run01.json`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01.json) (`SHA-256: d893515103fffbcc5cd4e8ad31981464893f42c43ceb07a0c6daff1760969d67`)
- **HTML Interactive Report:** [`23127259/evidence/fr10/newman/FR10-run01.html`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01.html) (`SHA-256: 569c8c2e0111075fb82dc10e1fb553be9e45bee0a04d78d586544b08c40ec6a4`)

---

## Full Run Verdict
### **`HARNESS_REPAIR_REQUIRED`**

### Root Cause & Required Fix for Run 02:
- **Root Cause:** In Folder `00 – Setup / Authentication Helpers`, the 3 login requests (`[SETUP] Login Admin`, `[SETUP] Login User A`, `[SETUP] Login User B`) targeted `/api/auth/login` (which returned 404) instead of the active SUT route `/api/login`. As a result, tokens were not extracted into environment variables, causing downstream checkouts to fail with 401.
- **Protocol Adherence:** Run 01 evidence is preserved verbatim without alteration. The collection fix will be applied in Phase 2D.1C for Run 02.

---

## Git
- **Commit SHA:** [`1bf476a`](https://github.com/thangak18/HW06/commit/1bf476a) (`test(23127259): execute FR-10 Newman run 01`)
- **Push Result:** Pushed to `origin/thang/hw06-implementation`
- **Working Tree:** Clean
```

---

## 3. Human Evaluation & Outcome

- **Verdict:** COMPLETED. Phase 2D.1B executed Newman Run 01 across 46 formal test cases (175 total runtime HTTP requests). Result: 130 assertion failures caused by harness auth route mismatch in Folder 00 (`/api/auth/login` returned 404, preventing token extraction). Classified as `HARNESS_REPAIR_REQUIRED`. Transitioning to Phase 2D.1C for reconciliation correction and harness repair.
- **Status:** COMPLETED & COMMITTED (`1bf476a`).

