# Interaction Log: INT-009

- **Interaction ID:** INT-009
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 19:02:22+07:00
- **Project Stage:** Phase 1A.5 – FR-02 Response Schema and Error-Contract Test Generation

---

## 1. Submitted Prompt

```text
/Speckit We are continuing with:

PHASE 1A.5 – FR-02 RESPONSE SCHEMA AND ERROR-CONTRACT TEST GENERATION

This is the FIFTH FR-02 AI-generation interaction.

Current FR-02 AI inventory:

FR02-AI-001 .. FR02-AI-031
Cumulative AI-generated count: 31

This stage generates ONLY:

1. response-schema validation cases
2. documented success/error contract cases
3. response-type / structural assertions
4. any remaining API-contract case that is genuinely distinct

DO NOT:
- generate additional general domain tests already covered
- generate additional lockout state tests already covered
- generate a new dedicated security suite
- generate Human-designed cases
- audit VALID / INVALID / INCOMPLETE
- execute Postman/Newman
- run the SUT
- inspect server.js/database.js as oracle
- confirm bugs
- generate FR-10/FR-14 tests
- commit yet

==================================================
1. PRESERVE ALL EXISTING AI OUTPUT
==================================================

Do NOT rewrite, repair, renumber, or silently improve:

FR02-AI-001 .. FR02-AI-031

Even if some previous AI cases contain questionable assumptions or imperfect
security classification, preserve them for the later Human Audit.

Examples that must remain untouched:
- assumptions about internal post-lockout counter state
- SEC-01 classification nuances
- supporting downstream JWT tests

The later Human Audit is responsible for classifying each AI case as:
VALID / INVALID / INCOMPLETE.

==================================================
2. AUTHORITATIVE SOURCES
==================================================

Read:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md
23127259/testcases/FR02_AI_DRAFT.md
23127259/docs/SECURITY_APPLICABILITY.md

Also consult:

- EShop SRS / README requirements
- api_specification.md

Expected results must come ONLY from specification sources.

Do NOT use:
- server.js
- database.js
- known implementation observations
- candidate defect knowledge

as expected-result oracle.

==================================================
3. GENERATION TARGET
==================================================

Generate approximately:

5–7 UNIQUE AI-generated cases.

Continue sequentially from:

FR02-AI-032

Expected end range:
approximately FR02-AI-036 .. FR02-AI-038.

Quality is more important than stopping at exactly 35.

Do NOT pad the suite merely to increase count.

==================================================
4. SUCCESS RESPONSE CONTRACT
==================================================

Analyze the documented successful login response from api_specification.md.

Generate schema/contract cases only for fields explicitly documented.

Potential assertions may include:

- HTTP status if explicitly documented
- response is valid JSON
- top-level documented fields exist
- token exists
- token is a string if specified/inferable from contract
- user object exists if documented
- documented user fields have expected primitive/object types
- Content-Type if API contract provides enough basis

IMPORTANT:

Do not invent required fields that do not appear in api_specification.md.

If a particular property is shown only in an example but not normatively
required, label the oracle confidence appropriately.

==================================================
5. INVALID-CREDENTIAL ERROR CONTRACT
==================================================

Generate a schema/contract test for invalid credentials.

Focus on:

- documented HTTP status if explicit
- JSON response form
- documented error/message field
- absence of a success token
- generic credential error semantics

Avoid duplicating:

FR02-AI-003
FR02-AI-004
FR02-AI-027
FR02-AI-029

Those already test:
- wrong-password rejection
- unknown-email rejection
- cross-response equivalence
- no token on authentication failure

A new case is allowed only if its PRIMARY purpose is response-contract/schema
validation rather than authentication behavior.

==================================================
6. LOCKED-ACCOUNT ERROR CONTRACT
==================================================

If the API specification documents the locked-account response:

Generate one schema/contract case covering:

- response must be valid error JSON
- documented error/message field
- no successful token/session issued
- exact HTTP status only if explicitly documented

Do not duplicate state cases FR02-AI-017..021.

The new case should validate RESPONSE SHAPE, not lockout lifecycle.

If the exact locked response schema is NOT specified, write:

Oracle Confidence: PARTIAL / NOT SPECIFIED

and do not invent a schema.

==================================================
7. RESPONSE TYPE / STRUCTURE CASES
==================================================

Consider distinct contract checks such as:

A. Successful response is parseable JSON.

B. JWT/token field has the expected primitive type.

C. `user` is an object where documented.

D. Error responses use the documented error structure rather than returning
successful response structure.

E. Successful response does not accidentally match an error schema and vice
versa.

Only create cases that are meaningful and non-duplicative.

==================================================
8. CONTENT-TYPE DISCIPLINE
==================================================

If the specification explicitly requires or clearly defines JSON responses,
you may generate a Content-Type contract test.

If Content-Type is not explicitly specified:

do not claim an exact header value such as:
application/json; charset=utf-8

unless supported.

Use:
Oracle Confidence = PARTIAL

where appropriate.

==================================================
9. REQUEST ERROR-CONTRACT CASES
==================================================

Do NOT regenerate these already-covered semantic inputs:

- malformed email
- empty email
- missing email
- null email
- whitespace email
- empty password
- missing password
- null password

Those cases already exist.

However, you MAY generate at most one contract-focused case that takes one
representative malformed/missing request and checks:

"Does the API return a structurally valid documented error response?"

Only if this is genuinely distinct from the existing input-domain case.

If exact malformed-request response schema is undocumented:
do not invent it.

==================================================
10. JSON PARSING / MALFORMED JSON
==================================================

Review whether invalid JSON body has already been covered.

If NOT already represented in FR02-AI-001..031:

you may add a case for syntactically invalid JSON request body.

But carefully separate:

transport/parser behavior
from
FR-02 business authentication behavior.

If the SRS/API-SPEC does not define the exact status:

Expected HTTP Status: NOT SPECIFIED
Expected semantic result: request must not result in successful login
Oracle Confidence: PARTIAL

Do not assert arbitrary 400 unless documented.

==================================================
11. TEST CASE FORMAT
==================================================

Append to:

23127259/testcases/FR02_AI_DRAFT.md

Use the same detailed format as existing cases.

Every generated case must contain:

- Test Case ID
- Title
- Technique
- Requirement reference
- Preconditions
- Request Method
- Endpoint
- Headers
- Request Body / request sequence
- Expected HTTP Status
- Expected Response Contract
- Required Fields
- Field Types
- Fields That Must Not Indicate Successful Authentication
- Oracle Confidence
- Specification Limitations
- Notes

Technique should primarily be:

SCHEMA VALIDATION
API CONTRACT
NEGATIVE CONTRACT
RESPONSE VALIDATION

==================================================
12. DO NOT OVERSTATE JSON SCHEMA
==================================================

There is no permission to invent a formal JSON Schema if the specification
does not define one.

Examples:

If API spec says:

{
  "message": "...",
  "token": "...",
  "user": {...}
}

you may test documented shape and primitive/object types.

You may NOT invent:
- minLength
- regex
- additionalProperties=false
- undocumented nullable constraints
- exact timestamp formatting
- undocumented user object fields

Mark unspecified details accordingly.

==================================================
13. DUPLICATION CHECK
==================================================

Before adding every case compare it against:

FR02-AI-001 .. FR02-AI-031.

Do not generate a new test merely because it uses different wording.

Specifically avoid duplicates of:

FR02-AI-001 / 002
successful authentication

FR02-AI-003 / 004
credential rejection

FR02-AI-017..024
lockout behavior

FR02-AI-027
generic error equivalence

FR02-AI-028
sensitive response content

FR02-AI-029
token omitted on auth failure

FR02-AI-030 / 031
downstream JWT use

Schema cases must add new contract assertions.

==================================================
14. HUMAN-CASE INTEGRITY
==================================================

DO NOT generate any:

FR02-HUM-xxx

Actual human extension cases are selected only after:

1. AI generation is complete
2. every AI case has undergone Human Audit
3. actual uncovered gaps are identified

Previous AI planning suggestions are NOT automatically Human cases.

==================================================
15. UPDATE SUMMARY
==================================================

Update the summary table in:

23127259/testcases/FR02_AI_DRAFT.md

Expected structure:

| Stage | ID Range | Generated Count |
|---|---|---:|
| 1A.2 Domain/BVA | FR02-AI-001..014 | 14 |
| 1A.3 State/Lockout | FR02-AI-015..024 | 10 |
| 1A.4 Security | FR02-AI-025..031 | 7 |
| 1A.5 Schema/Error Contract | FR02-AI-032..XXX | N |

Show cumulative count.

Do NOT renumber previous cases.

==================================================
16. AI AUDIT LOGGING
==================================================

Determine the next real AI interaction ID.

Expected:
INT-009

Create:

23127259/ai/interactions/INT-009-fr02-schema-error-generation.md

Record truthfully:

- Interaction ID
- AI Tool
- Model
- actual date/time
- Stage:
  FR-02 Stage 5 – Schema and Error Contract Generation
- Exact prompt
- Full AI output

Update:

23127259/ai/AI_AUDIT_REPORT.md

Do not fabricate metadata.

==================================================
17. QUALITY GATE
==================================================

Before finishing verify:

- only FR-02 cases generated
- all IDs sequential from FR02-AI-032
- no Human IDs
- schema cases add distinct assertions
- no implementation-derived expected behavior
- no undocumented fields invented
- no arbitrary HTTP statuses invented
- malformed request exact status remains unspecified where appropriate
- previous AI cases remain unchanged
- total FR-02 AI count is now >=35

==================================================
18. GIT POLICY
==================================================

DO NOT COMMIT YET.

Even if cumulative count reaches >=35, generation is not frozen until the
next stage:

PHASE 1A.6 – FR-02 AI COVERAGE REVIEW, DEDUPLICATION, AND FREEZE

That stage will:

- check duplicate semantics
- check requirement coverage
- identify AI-generated gaps
- remove/merge duplicates if needed
- preserve evidence of removed cases
- ensure final AI-generated count remains >=35
- freeze the inventory
- then create the generation commit

At the end report:

1. Interaction ID
2. IDs generated
3. Generated count
4. Schema dimensions covered
5. Error-contract dimensions covered
6. Oracle confidence breakdown
7. SPEC-UNDEFINED contract details
8. Cumulative FR-02 AI count
9. Whether >=35 has been reached
10. git status

Then STOP.

Next stage:

PHASE 1A.6 – FR-02 AI COVERAGE REVIEW, DEDUPLICATION, AND FREEZE
```

---

## 2. AI Output Summary

- Generated **6 unique schema and error contract test cases** (`FR02-AI-032` through `FR02-AI-037`) appended to `23127259/testcases/FR02_AI_DRAFT.md`:
  - `FR02-AI-032`: Successful login response schema and data type contract (`EXPLICIT`)
  - `FR02-AI-033`: Invalid credentials error response schema and structure contract (`EXPLICIT`)
  - `FR02-AI-034`: Locked-account error response contract and internal non-disclosure (`PARTIAL`)
  - `FR02-AI-035`: Syntactically malformed JSON request body transport contract (`PARTIAL`)
  - `FR02-AI-036`: Response `Content-Type` header contract across status codes (`EXPLICIT`)
  - `FR02-AI-037`: Extraneous request body properties ingestion contract (`PARTIAL`)
- Cumulative AI test case inventory reached **37 / 35 test cases** (meeting and exceeding the $\ge 35$ AI generation threshold).

---

## 3. Human Evaluation & Next Steps

- **Verdict:** VALID for Stage 1A.5 schema and contract test coverage.
- **Next Stage:** Phase 1A.6 – FR-02 AI Coverage Review, Deduplication, and Generation Freeze.
