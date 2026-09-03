# Interaction Log: INT-007

- **Interaction ID:** INT-007
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 18:56:52+07:00
- **Project Stage:** Phase 1A.3 – FR-02 Lockout State-Transition Test Generation

---

## 1. Submitted Prompt

```text
/Speckit We are continuing with:

PHASE 1A.3 – FR-02 LOCKOUT STATE-TRANSITION TEST GENERATION

This is the THIRD FR-02 AI-generation interaction.

Current FR-02 AI inventory:
FR02-AI-001 .. FR02-AI-014
Cumulative count: 14

This stage generates ONLY state-transition and lockout-lifecycle cases.

Do NOT:
- generate the complete remaining suite
- generate dedicated security cases
- generate schema-only cases
- generate Human-designed extension cases
- audit VALID / INVALID / INCOMPLETE
- execute Postman/Newman
- run the SUT
- inspect server.js/database.js as oracle
- confirm implementation defects
- generate FR-10 or FR-14 material
- commit yet

==================================================
1. AUTHORITATIVE INPUT
==================================================

Read:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md
23127259/testcases/FR02_AI_DRAFT.md

Also use the authoritative:
- EShop SRS / README requirements
- api_specification.md

Formal expected behavior must come ONLY from:
[SRS]
[API-SPEC]

Ignore all known implementation observations when setting expected results.

==================================================
2. FIRST CORRECT ONE COVERAGE GAP
==================================================

The previous Stage 1A.2 was instructed to distinguish:

N=1
N=2
N=3
N>3 / request while locked

but only explicit cases for N=2 and N=3 were generated.

Therefore this stage MUST include an explicit case for:

FR02-AI-015:
First consecutive failed login attempt.

Specification-derived oracle:
- authentication fails
- account must NOT yet be in locked state
- subsequent login attempt must still be accepted for credential evaluation

Do not depend on reading an undocumented internal login_attempts field.

==================================================
3. FR-02 SPECIFICATION STATE MODEL
==================================================

Use the specification-derived lifecycle only:

NORMAL
  |
  | failed login #1
  v
FAILURE_SEQUENCE_ACTIVE
  |
  | failed login #2
  v
FAILURE_SEQUENCE_ACTIVE
  |
  | failed login #3
  v
LOCKED
  |
  | 30-second lock period expires
  v
LOCK_EXPIRED / AUTHENTICATION_ALLOWED

Successful authentication before lockout:
- resets consecutive-failure progression to zero

Successful authentication after lock expiry:
- must restore the account to a clean usable authentication state according
  to the specification.

IMPORTANT:

Do not model the source-code +2 anomaly.

Do not model a 3-minute lock.

Those are implementation observations, not test oracle.

==================================================
4. GENERATION TARGET
==================================================

Generate approximately 8–10 UNIQUE AI-generated test cases.

Continue IDs sequentially beginning:

FR02-AI-015

Expected end range should be approximately:

FR02-AI-022 .. FR02-AI-024

Do not pad the count.

Every test must exercise a distinct state-transition behavior.

==================================================
5. REQUIRED STATE SCENARIOS
==================================================

Cover at minimum:

A. Failure progression

1. First failed attempt:
   NORMAL -> FAILURE_SEQUENCE_ACTIVE
   Not locked.

2. Second consecutive failed attempt:
   Still not locked.

3. Third consecutive failed attempt:
   Account enters LOCKED state.

Important:
If exact HTTP status returned by the THIRD request itself is not explicitly
specified:
Expected HTTP Status = NOT SPECIFIED
Expected state after request = LOCKED

B. Request while locked

Test a subsequent login request during the lock window.

Include both:

- wrong credentials while locked
- correct credentials while locked

Expected semantic behavior:
authentication must be rejected while lock is active.

Do not assume correct password bypasses lockout.

Use documented locked response status only if explicitly available.

C. Lock duration boundary

Specification duration:
30 seconds.

Design state tests around:

- clearly before expiry, e.g. T+25s
- clearly after expiry, e.g. T+32s

Do NOT depend on exact scheduler precision at exactly 30.000 seconds.

If you discuss T=30s itself, label exact millisecond behavior:
IMPLEMENTATION/TIMING TOLERANCE – NOT SUITABLE AS STRICT BLACK-BOX ORACLE.

D. Successful-login reset

Generate a case:

wrong login
-> then successful login
-> subsequent wrong login must behave as the FIRST failure of a new
   consecutive-failure sequence.

Do not inspect login_attempts internally.

Validate externally through observable lockout behavior.

E. Consecutive-failure semantics

Generate a case showing failures must be consecutive.

Example conceptual sequence:

wrong
-> success
-> wrong
-> wrong

The two failures after the success must not be treated as failure #3 from the
earlier sequence.

Expected behavior must come from the SRS reset-on-success rule.

F. Post-lock-expiry usability

After lockout expires:
- a valid credential attempt should be processed normally
- account should not remain permanently inaccessible

If the specification does NOT explicitly define whether the failure counter is
reset automatically merely by time expiry, do NOT invent that internal state.

Test only externally observable behavior.

==================================================
6. TEST CASE FORMAT
==================================================

Append each generated case to:

23127259/testcases/FR02_AI_DRAFT.md

Use the same format as Stage 1A.2.

Every case must include:

- Test Case ID
- Title
- Technique
- Requirement reference
- Preconditions
- Request method
- Endpoint
- Headers
- Exact sequence of requests/actions
- State Before
- Expected HTTP Status per step where specified
- Expected semantic response
- State After
- Oracle Confidence
- Notes

Technique should be one or more of:

STATE TRANSITION
BVA
SEQUENCE TESTING
NEGATIVE

==================================================
7. STATE-INDEPENDENCE RULE
==================================================

These are design-level test cases.

Each formal test case should declare a deterministic precondition.

Examples:

Precondition:
Dedicated lockout test account exists and is currently unlocked with no active
consecutive-failure sequence.

Do not assume one formal test case happens to inherit the correct state from a
previous unrelated case.

When later implementing Postman:
setup/reset will be designed explicitly.

Do NOT implement that setup now.

==================================================
8. STATUS-CODE DISCIPLINE
==================================================

Do not invent exact statuses.

For each step:

If SRS/API-SPEC explicitly gives status:
use it.

If only semantic behavior is specified:
write:

Expected HTTP Status: NOT SPECIFIED
Expected semantic behavior: <spec-derived behavior>

Especially preserve this rule for:
- the third failed request itself
- timing transition behavior where exact response status is undocumented

==================================================
9. HUMAN-CASE INTEGRITY
==================================================

Do NOT create any:

FR02-HUM-xxx

The final human-designed extension cases will be chosen only AFTER:
1. >=35 AI-generated cases exist
2. Human Audit is complete
3. actual remaining coverage gaps are identified

Ideas previously suggested by AI in planning documents are not automatically
eligible as final Human cases.

==================================================
10. DO NOT AUDIT
==================================================

This is still AI GENERATION.

Do not classify cases:
VALID
INVALID
INCOMPLETE

The student will do that later.

You may use Oracle Confidence:

EXPLICIT
PARTIAL
SPEC-UNDEFINED

==================================================
11. UPDATE STAGE SUMMARY
==================================================

Update the summary table at the top of:

23127259/testcases/FR02_AI_DRAFT.md

It should contain:

| Stage | ID Range | Generated Count |
|---|---|---:|
| 1A.2 Domain/BVA | FR02-AI-001..014 | 14 |
| 1A.3 State/Lockout | FR02-AI-015..XXX | N |

Then show cumulative total.

Do not renumber existing cases.

==================================================
12. AI AUDIT LOG
==================================================

Determine the next real interaction ID.

Expected:
INT-007

Create:

23127259/ai/interactions/INT-007-fr02-lockout-state-generation.md

Record truthfully:
- Interaction ID
- AI Tool
- Model
- real date/time
- Stage:
  FR-02 Stage 3 – Lockout State-Transition Generation
- Exact prompt
- Full AI output

Update:

23127259/ai/AI_AUDIT_REPORT.md

Do not fabricate any metadata.

==================================================
13. QUALITY CHECK
==================================================

Before finishing verify:

- FR02-AI-015 explicitly covers failure #1
- failure #1 does not lock account
- failure #2 does not lock account
- failure #3 transitions account into LOCKED state
- exact response of failure #3 is not invented if unspecified
- correct credentials while locked do not bypass lock
- before-expiry and after-expiry behavior are distinguished
- reset-on-success sequence is covered
- consecutive-failure semantics are covered
- no implementation anomaly is used as expected behavior
- no Human cases generated
- no duplicate semantics with FR02-AI-001..014
- only FR-02 appears

==================================================
14. GIT POLICY
==================================================

Do NOT commit.

The FR-02 AI-generation commit occurs after all FR-02 generation stages and
deduplication are complete.

At the end report:

1. Interaction ID
2. IDs generated in this stage
3. Generated count
4. State scenarios covered
5. Oracle-confidence breakdown
6. Any SPEC-UNDEFINED state questions
7. Cumulative FR-02 AI count
8. Remaining number needed to reach >=35
9. git status

Then STOP.

Next stage:

PHASE 1A.4 – FR-02 SECURITY TEST GENERATION
```

---

## 2. AI Output Summary

- Generated **10 unique state-transition test cases** (`FR02-AI-015` through `FR02-AI-024`) appended to `23127259/testcases/FR02_AI_DRAFT.md`:
  - `FR02-AI-015`: 1st consecutive failed attempt ($N=1$) $\rightarrow$ state becomes `FAILURE_SEQUENCE_ACTIVE`, not locked (`EXPLICIT`).
  - `FR02-AI-016`: 2nd consecutive failed attempt ($N=2$) $\rightarrow$ remains unlocked (`EXPLICIT`).
  - `FR02-AI-017`: 3rd consecutive failed attempt ($N=3$) $\rightarrow$ transitions to `LOCKED` (`PARTIAL`).
  - `FR02-AI-018`: Subsequent request during active lock with incorrect credentials $\rightarrow$ rejected with lockout notice (`PARTIAL`).
  - `FR02-AI-019`: Subsequent request during active lock with **CORRECT** credentials $\rightarrow$ rejected, no bypass (`EXPLICIT`).
  - `FR02-AI-020`: Timing boundary check at $T=25\text{s}$ before 30s expiry $\rightarrow$ still locked (`PARTIAL`).
  - `FR02-AI-021`: Timing boundary check at $T=32\text{s}$ after 30s expiry $\rightarrow$ unlocked, authenticates successfully (`EXPLICIT`).
  - `FR02-AI-022`: Successful login resets failure progression (fail $\rightarrow$ success $\rightarrow$ fail remains unlocked) (`EXPLICIT`).
  - `FR02-AI-023`: Non-consecutive failure sequence (fail $\rightarrow$ success $\rightarrow$ fail $\rightarrow$ fail remains unlocked) (`EXPLICIT`).
  - `FR02-AI-024`: Post-lockout expiration full lifecycle recovery and failure sequence reset (`EXPLICIT`).
- Cumulative AI test case count reached **24 / 35 test cases**.

---

## 3. Human Evaluation & Next Steps

- **Verdict:** VALID for Stage 1A.3 state-transition and lockout lifecycle coverage.
- **Next Stage:** Phase 1A.4 – Security & Schema Test Generation (`FR02-AI-025` through `FR02-AI-035`).
