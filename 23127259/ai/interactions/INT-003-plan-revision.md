# Interaction Log: INT-003

- **Interaction ID:** INT-003
- **Tool:** Antigravity IDE Assistant
- **Model:** Claude Sonnet 4.6
- **Date & Time:** 2026-09-01 16:15:00+07:00
- **Purpose / Stage:** Implementation Plan Revision (SEC Mappings & Specification Oracle Separation)

---

## 1. Submitted Prompt
```text
/Speckit Review and REVISE the HW06 plan you just produced.

PLAN REVISION ONLY.
DO NOT implement anything.
DO NOT create files.
DO NOT modify the repository.
DO NOT create Postman collections.
DO NOT create test cases yet.
DO NOT commit or push.

Your previous plan has several issues that must be corrected before implementation.

==================================================
1. CRITICAL: FIX SEC-01 THROUGH SEC-07
==================================================

You mapped the Security Requirements incorrectly.

Use the authoritative EShop SRS definitions exactly:

SEC-01:
Passwords must not be stored in plaintext.

SEC-02:
Security-sensitive APIs must require a valid JWT token.

SEC-03:
Admin APIs must verify role='admin' in the token, not merely token existence.

SEC-04:
User-controlled data displayed in the UI must be escaped correctly and must
not be inserted through unsafe innerHTML usage.

SEC-05:
Database queries must use parameterized queries rather than direct string
concatenation.

SEC-06:
The profile-update API must not allow a client to change the role field.

SEC-07:
Password-reset OTP must have sufficient entropy (minimum 6 digits), expire,
and become invalid after use.

Audit EVERY SEC reference in the previous plan and correct it.

Examples:
- missing admin role check on category/order admin API -> SEC-03
- missing JWT on a protected endpoint -> SEC-02
- parameterized SQL -> SEC-05
- plaintext password storage -> SEC-01

Do NOT label:
- IDOR as SEC-04
- rate limiting as SEC-06
- data exposure as SEC-05
because those mappings are incorrect.

Security issues may still be tested even when they do not correspond exactly
to an SEC ID, but label them separately as:
"Additional security test / business authorization test".

==================================================
2. SEPARATE SPECIFICATION FROM IMPLEMENTATION
==================================================

The previous plan inspected server.js/database.js and effectively revealed
intentional defects before test generation.

Revise the methodology.

The primary test oracle must come from:

1. HW06 PDF
2. EShop SRS / README requirements
3. api_specification.md

NOT from server.js implementation behavior.

New methodology:

SPECIFICATION
    ->
AI-generated test design
    ->
Human audit against specification
    ->
Human-added tests
    ->
Freeze expected results
    ->
Execute against SUT
    ->
Observe discrepancies
    ->
Report genuine bugs
    ->
Only THEN inspect server.js/database.js to explain root cause if useful.

Source-code inspection may identify CANDIDATE defects during planning, but
those candidates MUST NOT be treated as confirmed bugs until reproduced
through real API execution.

In the revised plan, move source-derived implementation anomalies into a
section:

"Known implementation observations — NOT YET CONFIRMED BY EXECUTION"

Do not let those observations determine the expected result.

==================================================
3. FIX FR-14 TEST ORACLES
==================================================

Do NOT call behavior a defect unless supported by a requirement.

FR-14 explicitly requires:
- Admin category management
- category name is mandatory/non-empty
- admin access requirements are inherited from FR-12
- api_specification.md exposes GET/POST/PUT/DELETE category endpoints

Therefore strong spec-backed tests include:
- empty category name
- missing category name
- JWT enforcement where required
- admin-role enforcement on modifying endpoints
- CRUD endpoint behavior/schema

However:

A. DUPLICATE CATEGORY NAME
There is no explicit requirement stating category names must be unique.

Therefore:
- it may be an exploratory test
- acceptance of duplicates MUST NOT automatically be reported as a bug

B. ORPHAN PRODUCTS
There is no explicit referential-integrity requirement stating what must happen
to products when their category is deleted.

Therefore:
- exploratory only
- do not declare a bug without a requirement oracle

C. XSS PAYLOAD
SEC-04 requires safe escaping when user-controlled content is DISPLAYED ON UI.

Returning a raw "<script>..." string in JSON is not by itself proof of an XSS
bug.

For HW06 backend API tests:
- such payload may be used as a security probe
- do not call raw JSON reflection an XSS vulnerability unless the consuming UI
  renders it unsafely and real execution evidence proves this.

Revise all FR-14 test counts and human-added cases accordingly.

==================================================
4. FIX FR-02 SECURITY INTERPRETATION
==================================================

The successful login implementation appears to return the complete user row,
including password.

Treat this as:
- a sensitive-data exposure candidate
- potentially related evidence that plaintext password handling is unsafe

BUT:
SEC-01 specifically states that passwords must NOT BE STORED in plaintext.

Do not incorrectly map response exposure to SEC-05.

Distinguish:
A. password storage violation -> SEC-01
B. password appearing in API response -> additional sensitive-data exposure
   defect

Also avoid making direct database inspection a normal API test-case oracle.

==================================================
5. FIX FR-10 SECURITY INTERPRETATION
==================================================

For FR-10:

- invalid/final-state transitions -> FR-10 business-rule testing
- admin endpoint accessible to regular user -> SEC-03
- protected endpoint accessible without JWT -> SEC-02
- accessing another user's order -> authorization / ownership / IDOR-style test

Do not map IDOR to SEC-04.

Keep:
- canceled -> delivered
- shipping user-cancel
- normal user calling admin transition
- unauthenticated order access

as HIGH-VALUE candidate tests, but mark implementation outcomes as:
"candidate observation until reproduced via real execution."

==================================================
6. FR-14 SCOPE AMBIGUITY
==================================================

Do not state as fact that "three APIs" unquestionably means three features.

Document the exact evidence:

HW06 asks for:
- one API implementing a feature from Pool A
- one API implementing a feature from Pool B
- one API implementing a feature from Pool C
- consult api_specification.md for endpoints behind the selected feature

FR-14 is Category Management CRUD.

api_specification.md exposes:
- GET /api/categories
- POST /api/categories
- PUT /api/categories/:id
- DELETE /api/categories/:id

The SRS text explicitly mentions Add/View/Delete, while the API specification
also exposes PUT Update.

Recommended scope:
include all four category endpoints for complete FR-14/API-spec coverage.

Label this as a defensible SCOPE DECISION, not as an explicit PDF statement.

==================================================
7. REMOVE INVENTED MANDATORY REQUIREMENTS
==================================================

The previous plan added some engineering targets that are NOT assignment
requirements.

Correct them:

- "minimum 6 AI interactions per API" -> engineering recommendation only
- "at least 2 bugs" -> REMOVE as a mandatory requirement
- specific Postman features as mandatory -> distinguish recommendations from PDF
- exact number of Git commits -> engineering recommendation

The PDF requires reporting genuine bugs that are found.
Do not create a bug-count quota.

Continue to recommend multiple focused AI interactions, but label them [ENG].

==================================================
8. AI AUDIT VS TEST-CASE AUDIT
==================================================

Do not conflate these two audits.

AI Audit Report:
For each AI interaction record:
- AI tool
- date/time
- exact prompt
- AI output

Human test-case audit:
For EACH AI-generated test case classify:
- VALID
- INVALID
- INCOMPLETE
with rationale and correction.

They are related but not the same artifact.

Make this distinction explicit in the revised plan.

==================================================
9. AGENT SKILL DIAGRAM WORDING
==================================================

Correct the phrase "must be hand-drawn."

The assignment says the diagram must be SELF-DRAWN:
the student makes the design decisions and produces the diagram;
any diagramming tool is acceptable;
the final diagram must not be AI-generated.

Therefore:
- draw.io / Excalidraw / manually authored Mermaid are acceptable as applicable
- do not have AI generate the final diagram and claim it as self-drawn
- it does NOT literally have to be drawn with pen and paper

==================================================
10. CI/CD PASS/FAIL STRATEGY
==================================================

Reconsider the previous suggestion:

"Passing run = only happy-path folders."

The assignment wording asks for:
- one sample commit whose pipeline run shows all API test cases passing
- another sample commit whose pipeline run shows one test case failing

Do not silently reinterpret "all API test cases" as only a happy-path subset.

Design a defensible CI demonstration strategy.

Clearly distinguish:
A. full regression execution results against the buggy SUT
B. assignment-required CI demonstration run
C. intentionally failing CI demonstration

Do NOT change legitimate test expected results merely to force a green build.

If there is unavoidable ambiguity because the SUT intentionally contains
defects, flag it as a point to confirm with the TA rather than inventing an
interpretation.

==================================================
11. STATEFUL EXECUTION
==================================================

Keep the useful observation that restarting the backend resets the SQLite DB.

However, design automated tests so that each state-sensitive scenario is as
independent and deterministic as reasonably possible.

For FR-10:
- create fresh orders for independent transition scenarios
- do not reuse one order across incompatible transition tests
- setup must create the exact initial state required

For FR-02:
- use a dedicated lockout account
- avoid locking the primary user used by other suites

For FR-14:
- generate unique temporary category names for tests that require isolation
- clean only records created by the current test

==================================================
12. REVISE THE BUG-CANDIDATE TABLE
==================================================

Classify candidates into:

A. Strong specification-backed candidates
Examples:
- FR-02 attempt increment mismatch
- FR-02 lockout duration mismatch
- FR-10 canceled -> delivered
- FR-10 user cancel while shipping
- FR-10 admin transition missing role check
- protected order endpoint missing JWT where applicable
- FR-14 modifying category with normal user
- FR-14 empty/missing category name accepted

B. Additional security candidates
- password exposed in login response
- cross-user order access

C. Exploratory observations, NOT automatically bugs
- duplicate category names
- orphan categories/products
- raw XSS-like strings returned in JSON
- unspecified maximum lengths

All bugs remain UNCONFIRMED until reproduced by real execution.

==================================================
13. FINAL OUTPUT
==================================================

Return a corrected version:

# HW06 Revised Implementation Plan – FR-02 / FR-10 / FR-14

Preserve the strong parts of the original plan:
- traceability
- Postman architecture
- test-count planning
- state-transition matrix
- repository organization
- branch strategy
- commit roadmap
- CI/CD
- submission artifact map
- risk register
- definition of done

But correct all issues above.

At the end add:

## Changes From Previous Plan

with a table containing:
- previous issue
- correction
- reason
- source (PDF / SRS / API Spec / ENG)

Then STOP.

DO NOT IMPLEMENT ANYTHING.
```

---

## 2. AI Output Summary
- Re-mapped SEC-01..07 strictly to EShop SRS Section 9 definitions.
- Established primary test oracles from specification and moved source code observations to unconfirmed candidate section.
- Separated AI Audit Report (per interaction) from Test Case Audits (per generated case).
- Formulated 3-scenario CI/CD strategy.

---

## 3. Human Evaluation & Outcome
- **Review Finding:** Substantially improved and aligned with academic standards. Identified minor details to adjust: `confirmed->canceled` transition in FR-10 matrix and strict test accounting ($\ge 120$ total).
- **Action:** Finalized in INT-004.
