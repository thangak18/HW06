# Interaction Log: INT-018

- **Interaction ID:** INT-018
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 20:03:37+07:00
- **Project Stage:** Phase 1C.1 – FR-02 Student-Selected Human Extension Finalization
- **Transcript Reference:** `transcript_full.jsonl` (Prompt: Step 644, Output: Step 661)

---

## 1. Submitted Prompt

```text
/Speckit /Speckit We are starting:

PHASE 1C.1 – FR-02 STUDENT-SELECTED HUMAN EXTENSION FINALIZATION

The student has reviewed the FR-02 post-audit gap analysis and has now
APPROVED the following five extension directions as the final Human extension
suite.

IMPORTANT PROVENANCE NOTE:

These directions were finalized by the student after reviewing an AI-assisted
coverage-gap analysis.

Do NOT falsely claim that no AI assistance was involved.

Use wording such as:

"Student-selected and finalized after AI-assisted gap analysis."

Do NOT describe them as:
"entirely independently invented without AI."

However, these cases are separate from the original AI-generated inventory
FR02-AI-001..037 and must use FR02-HUM identifiers.

==================================================
1. AUDIT INTERACTION NUMBERING
==================================================

Previous interaction:

INT-017
FR-02 Human Extension Gap Analysis

Current interaction:

INT-018

First backfill the COMPLETE exact AI output for INT-017 from the completed
Antigravity transcript.

Locate the actual:
- USER_INPUT for INT-017
- corresponding PLANNER_RESPONSE

Do not guess transcript steps.

Then create:

23127259/ai/interactions/INT-018-fr02-human-extension-finalization.md

Record:
- actual Tool
- actual Model
- actual Date
- actual Local Time
- timezone UTC+07:00
- Stage:
  FR-02 Student-Selected Human Extension Finalization
- THIS COMPLETE PROMPT verbatim

Append THIS complete prompt to:

23127259/ai/prompts/AI_PROMPT_LOG.md

Update:

23127259/ai/AI_AUDIT_REPORT.md

For INT-018 Exact AI Output use:

PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES

until this interaction actually completes.

==================================================
2. PRESERVE RAW AI GENERATION
==================================================

DO NOT modify:

23127259/testcases/FR02_AI_DRAFT.md

Verify SHA-256 remains:

b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c

Also preserve:

23127259/ai/TC_AUDIT_FR02.md

Do not change previously recorded Human Audit verdicts.

==================================================
3. FINAL STUDENT-SELECTION SET
==================================================

The student approves the following five directions.

--------------------------------------------------
HUMAN EXTENSION 1
--------------------------------------------------

Source Gap:
G-02

Direction:
HTTP Method Enforcement for /api/login

Student rationale:
The documented login operation uses POST. The original AI suite tested only
POST and never checked whether unsupported HTTP methods can accidentally invoke
authentication behavior.

Test objective:
Verify that /api/login cannot successfully authenticate a user when invoked
through an HTTP method that is not documented for the login operation.

Oracle discipline:
Do NOT automatically require HTTP 405 unless api_specification.md explicitly
requires it.

Minimum specification-safe oracle:

- unsupported method invocation must NOT result in successful authentication
- no usable authentication JWT/session should be created through an
  unsupported method

If the exact status is unspecified:
mark it NOT SPECIFIED.

--------------------------------------------------
HUMAN EXTENSION 2
--------------------------------------------------

Source Gap:
G-05

Direction:
Additional SQL Injection Vector Beyond Original AI Payloads

Student rationale:
The original AI suite tested only simple classic SQL injection strings.
A single payload does not provide broad behavioral confidence against SQL
injection attempts.

Test objective:
Use a meaningfully different SQL-injection-style input pattern and verify that
it cannot bypass authentication or obtain an unauthorized authenticated
session.

IMPORTANT:
Do NOT simply copy the exact payload already used by:
FR02-AI-025
FR02-AI-026

Choose a distinct behavioral probe.

Oracle discipline:

- no authentication bypass
- no unauthorized usable JWT
- classify as SEC-05 PARTIAL BLACK-BOX EVIDENCE
- do NOT claim this proves all queries are parameterized

--------------------------------------------------
HUMAN EXTENSION 3
--------------------------------------------------

Source Gap:
CUSTOM-G-09

Gap Name:
Successful Login Reset at N=2 Boundary

Student rationale:
The AI suite tested counter reset after one failed login, but did not directly
exercise the more critical threshold-adjacent state where the account already
has two consecutive failed logins before a successful authentication occurs.

Test objective:
Verify that a successful authentication occurring after exactly two
consecutive failures resets the failure sequence before the N=3 lockout
threshold can be reached.

Important coverage distinction:

This must be meaningfully different from:
FR02-AI-022
FR02-AI-023

Those sequences begin their reset verification after one initial failed login.

This Human case must specifically exercise the N=2 pre-lockout boundary.

Use externally observable behavior rather than undocumented internal
login_attempts response fields.

--------------------------------------------------
HUMAN EXTENSION 4
--------------------------------------------------

Source Gap:
CUSTOM-G-10

Gap Name:
Account Lockout Isolation Between Different Users

Student rationale:
The AI suite tested lockout behavior on one dedicated account but never
verified that one user's lock state does not incorrectly affect another
independent account.

Test objective:
Verify that placing Account A into the temporary locked state does not prevent
a different valid Account B from authenticating normally.

Oracle discipline:

- lockout must remain associated with the affected account
- Account B valid authentication must continue to follow normal FR-02 behavior
- do not inspect internal counters as the primary oracle
- use externally observable authentication results

Use two dedicated test accounts so this case is isolated and reproducible.

--------------------------------------------------
HUMAN EXTENSION 5
--------------------------------------------------

Source Gap:
G-08

Direction:
Non-JSON Content-Type Request Contract

Student rationale:
The original AI suite assumed application/json for normal authentication and
tested malformed JSON, but did not test credentials supplied using an
undocumented request encoding.

Test objective:
Verify that using a non-documented Content-Type cannot accidentally bypass the
documented authentication contract or create an authenticated session.

Oracle discipline:

The specification may NOT define whether the server must return:
400
415
401
or another error.

Therefore do NOT invent an exact status unless documented.

Minimum safe assertion:

- non-documented request encoding must not create an unintended authenticated
  session
- exact parser/Content-Type behavior may remain SPEC-UNDEFINED

Treat this as:
EXPLORATORY / API CONTRACT

rather than claiming a formal MIME requirement if none exists.

==================================================
4. ASSIGN FORMAL HUMAN TEST IDS
==================================================

Create exactly:

FR02-HUM-001
FR02-HUM-002
FR02-HUM-003
FR02-HUM-004
FR02-HUM-005

Mapping:

FR02-HUM-001 = G-02 HTTP Method Enforcement
FR02-HUM-002 = G-05 Additional SQLi Vector
FR02-HUM-003 = CUSTOM-G-09 Reset at N=2 Boundary
FR02-HUM-004 = CUSTOM-G-10 Account Lockout Isolation
FR02-HUM-005 = G-08 Non-JSON Content-Type Contract

Do not generate a sixth case.

==================================================
5. CREATE FINAL HUMAN TEST CASE ARTIFACT
==================================================

Create:

23127259/testcases/FR02_HUMAN_TEST_CASES.md

Use:

# FR-02 Student-Selected Human Extension Test Cases

Include provenance statement:

"These extension directions were selected and finalized by the student after
reviewing the completed AI-generated suite, Human Audit results, and an
AI-assisted coverage-gap analysis. They are intentionally separated from the
raw AI-generated FR02-AI inventory."

For EACH Human test case include:

- Test Case ID
- Title
- Source Gap
- Student Rationale
- Why Existing AI Suite Missed This
- Technique
- Requirement / Spec Basis
- Preconditions
- Request Method / Sequence
- Endpoint
- Headers
- Test Data
- Steps
- Expected HTTP Status
- Expected Semantic Result
- State Before
- State After
- Oracle Confidence
- Spec Limitations
- Postman Implementation Notes

==================================================
6. REQUIREMENT DISCIPLINE
==================================================

For each Human case distinguish:

SPECIFICATION-BACKED
PARTIALLY SPECIFICATION-BACKED
EXPLORATORY

Do not convert an exploratory behavior into a fake formal requirement.

Expected classifications should be considered carefully:

FR02-HUM-001:
API contract / method enforcement.
Exact error status may be unspecified.

FR02-HUM-002:
Security behavioral probe.
SEC-05 PARTIAL black-box evidence.

FR02-HUM-003:
Strong specification-backed state-transition test.

FR02-HUM-004:
Strong account-isolation / state-security test if account-specific lockout is
supported by FR-02 semantics.

FR02-HUM-005:
Exploratory/API-contract behavior if MIME rejection is undocumented.

Do not fabricate requirement references.

==================================================
7. CHECK DISTINCTNESS AGAINST AI CASES
==================================================

Before finalizing compare each Human test against all usable AI-derived cases.

Create:

## Human-vs-AI Distinctness Matrix

| Human ID | Closest AI Case(s) | What Is New | Duplicate? |
|---|---|---|---|

Expected result:
all five must be meaningfully distinct.

Special attention:

FR02-HUM-002 must not merely repeat AI-025/026.

FR02-HUM-003 must not duplicate AI-022/023:
its distinguishing boundary is SUCCESS AFTER TWO CONSECUTIVE FAILURES.

FR02-HUM-004 must test cross-account isolation, absent from AI suite.

==================================================
8. UPDATE HUMAN EXTENSION DESIGN WORKSPACE
==================================================

Update:

23127259/testcases/FR02_HUMAN_EXTENSION_DESIGN.md

Replace the five blank Human slots with the five student-approved selections.

Preserve:

- selected gap
- rationale
- test objective
- formal assigned HUM ID

Add:

Design Status:
STUDENT SELECTED / FINALIZED

Do not delete the original gap analysis section.

==================================================
9. ACCOUNTING
==================================================

Create/update an FR-02 suite accounting section:

Raw AI-generated:
37

Raw AI rejected during Human Audit:
2

Usable AI-derived after corrections:
35

Human extension:
5

Final executable candidate suite:
40

Use wording carefully:

37 RAW AI-GENERATED
not 35 raw AI-generated.

The correct accounting is:

37 raw AI outputs
→ Human Audit
→ 35 usable AI-derived
+ 5 Human extensions
= 40 final executable candidate cases

==================================================
10. DO NOT IMPLEMENT POSTMAN YET
==================================================

This interaction finalizes TEST DESIGN only.

DO NOT:

- execute SUT
- execute Postman
- execute Newman
- generate fake execution evidence
- confirm bugs
- create GitHub Issues
- implement the collection yet
- modify EShop source

Postman implementation is the NEXT phase.

==================================================
11. QUALITY CHECK
==================================================

Before completing verify:

- exactly 5 FR02-HUM cases
- all IDs unique
- all cases distinct from usable AI cases
- HUM-003 uses N=2 before successful reset
- HUM-004 uses two independent accounts
- HUM-002 uses a different SQLi vector from AI cases
- no invented exact HTTP statuses
- exploratory cases clearly marked
- raw AI file hash unchanged
- Human Audit file unchanged
- total executable candidate cases = 40

==================================================
12. GIT COMMIT
==================================================

If all five Human cases are finalized:

stage only relevant Human-extension and audit-log artifacts.

Commit:

test(23127259): add human-designed FR-02 extension cases

Include:

23127259/testcases/FR02_HUMAN_EXTENSION_DESIGN.md
23127259/testcases/FR02_HUMAN_TEST_CASES.md
23127259/ai/AI_AUDIT_REPORT.md
23127259/ai/prompts/AI_PROMPT_LOG.md
23127259/ai/interactions/INT-017*
23127259/ai/interactions/INT-018*

Do NOT include unrelated artifacts.

Push:

origin/thang/hw06-implementation

Do NOT merge to main.

==================================================
13. END REPORT
==================================================

Return:

# Phase 1C.1 Completion Report

## Audit Evidence
- INT-017 output backfilled
- INT-018 prompt stored
- INT-018 output pending

## Human Extensions

| HUM ID | Gap | Technique | Oracle Classification | Distinct From AI? |
|---|---|---|---|---|

## Accounting
- raw AI generated: 37
- rejected raw AI: 2
- usable AI-derived: 35
- Human extensions: 5
- final executable candidate suite: 40

## Integrity
- raw AI SHA-256
- Human Audit unchanged

## Git
- commit SHA
- push result
- git status

Then STOP.

Next phase:

PHASE 1D – FR-02 POSTMAN COLLECTION IMPLEMENTATION
```

---

## 2. Exact AI Output

```markdown
# Phase 1C.1 Completion Report

---

## 1. Audit Evidence
- **INT-017 Output Backfilled:** **YES** — Exact output (Step 643, 5,913 bytes) backfilled into [`INT-017-fr02-human-extension-gap-analysis.md`](INT-017-fr02-human-extension-gap-analysis.md).
- **INT-018 Prompt Stored:** **YES (Verbatim)** in [`INT-018-fr02-human-extension-finalization.md`](INT-018-fr02-human-extension-finalization.md) and [`AI_PROMPT_LOG.md`](../prompts/AI_PROMPT_LOG.md) (167,042 bytes).
- **INT-018 Output Status:** `PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES`.

---

## 2. Finalized Human Extension Test Suite (`FR02-HUM-001` .. `FR02-HUM-005`)

The 5 student-selected Human extension test cases have been authored and recorded in [FR02_HUMAN_TEST_CASES.md](../../testcases/FR02_HUMAN_TEST_CASES.md):

| Human ID | Source Gap | Test Title | Technique | Oracle Classification | Distinct From AI Cases? |
|:---:|:---:|---|---|:---:|:---:|
| `FR02-HUM-001` | `G-02` | HTTP Verb / Method Enforcement Rejection on Login Route (`GET`) | API Contract / Method Enforcement | `PARTIALLY SPEC-BACKED` / `API CONTRACT` | **YES** (All AI cases used `POST`; verb dispatching was omitted) |
| `FR02-HUM-002` | `G-05` | Advanced SQL Injection Multi-Vector Resilience Probe (Comment Vector `admin'--`) | Security / Behavioral Injection Probe | `PARTIALLY SPEC-BACKED` / `SEC-05 PROBE` | **YES** (Tests comment truncation delimiter vs simple `' OR '1'='1`) |
| `FR02-HUM-003` | `CUSTOM-G-09` | Consecutive Failure Counter Reset at $N=2$ Pre-Lockout Boundary via Successful Login | State Transition / Boundary Reset | `SPECIFICATION-BACKED` | **YES** (Tests reset specifically at critical $(N-1)$ boundary vs $N=1$) |
| `FR02-HUM-004` | `CUSTOM-G-10` | Account Lockout State Isolation Between Independent User Accounts | Security / State Isolation Testing | `SPECIFICATION-BACKED` | **YES** (Multi-tenant principal isolation absent from AI suite) |
| `FR02-HUM-005` | `G-08` | Non-JSON Content-Type Request Contract Handling (`x-www-form-urlencoded`) | Exploratory / API Contract | `EXPLORATORY` / `API CONTRACT` | **YES** (Tests valid credentials via non-JSON encoding) |

---

## 3. Suite Accounting & Inventory Consolidation

$$\begin{aligned}
\text{Raw AI-Generated Test Cases} &= \mathbf{37} \\
\text{Raw AI Rejected during Human Audit} &= \mathbf{2} \quad (\text{Duplicates: } \text{FR02-AI-016}, \text{FR02-AI-017}) \\
\text{Usable AI-Derived Cases post-Audit} &= \mathbf{35} \quad (16\text{ VALID} + 19\text{ INCOMPLETE with corrections}) \\
\text{Student-Designed Human Extensions} &= \mathbf{5} \quad (\text{FR02-HUM-001} .. \text{FR02-HUM-005}) \\
\hline
\mathbf{\text{Total Final Executable Candidate Suite}} &= \mathbf{40\text{ Test Cases}}
\end{aligned}$$

*(Meets and satisfies the assignment requirement of $\ge 35\text{ AI} + \ge 5\text{ Human} = \ge 40\text{ total test cases per feature}$).*

---

## 4. Test Artifact Cryptographic & Audit Integrity
- **Raw AI Draft Hash:** `b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c` *(Unchanged & preserved in [`testcases/FR02_AI_DRAFT.md`](../../testcases/FR02_AI_DRAFT.md))*.
- **Human Audit Worksheet:** [TC_AUDIT_FR02.md](../TC_AUDIT_FR02.md) *(Preserved with 100% student verdicts)*.
- **Design Workspace:** [FR02_HUMAN_EXTENSION_DESIGN.md](../../testcases/FR02_HUMAN_EXTENSION_DESIGN.md) *(Updated with finalized selections)*.

---

## 5. Git Commit & Push Verification
- **Commit Message:** `test(23127259): add human-designed FR-02 extension cases`
- **Commit SHA:** [`1634d8f`](https://github.com/thangak18/HW06/commit/1634d8f)
- **Branch:** `thang/hw06-implementation` (Pushed to `origin`, working tree clean).

```text
On branch thang/hw06-implementation
Your branch is up to date with 'origin/thang/hw06-implementation'.

nothing to commit, working tree clean
```

---

Execution is stopped here. Ready to proceed to **PHASE 1D – FR-02 POSTMAN COLLECTION IMPLEMENTATION**.
```

---

## 3. Human Evaluation & Outcome

- **Verdict:** VALID. Recorded 5 student-selected Human extension test cases (`FR02-HUM-001` .. `FR02-HUM-005`) in `FR02_HUMAN_TEST_CASES.md` and updated `FR02_HUMAN_EXTENSION_DESIGN.md`. Total candidate suite reached 40 executable cases. Committed as `1634d8f`.
- **Status:** EXACT OUTPUT AVAILABLE.
