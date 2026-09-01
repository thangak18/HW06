# Interaction Log: INT-008

- **Interaction ID:** INT-008
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 18:59:26+07:00
- **Project Stage:** Phase 1A.4 – FR-02 Security Test Generation

---

## 1. Submitted Prompt

```text
/Speckit We are continuing with:

PHASE 1A.4 – FR-02 SECURITY TEST CASE GENERATION

This is the FOURTH FR-02 AI-generation interaction.

Current FR-02 AI inventory:

FR02-AI-001 .. FR02-AI-024
Cumulative AI-generated count: 24

This stage generates ONLY security-focused FR-02 test cases.

DO NOT:
- generate schema-only cases
- generate general malformed/error cases already covered
- generate Human-designed extension cases
- audit VALID / INVALID / INCOMPLETE
- execute Postman or Newman
- run the SUT
- confirm candidate bugs
- inspect server.js/database.js as the expected-result oracle
- generate FR-10 or FR-14 tests
- commit yet

==================================================
1. PRESERVE PRIOR AI OUTPUT
==================================================

Do NOT silently correct or rewrite previously generated cases
FR02-AI-001..024.

This is important for the later Human Audit.

In particular, some previous AI cases may contain questionable assumptions,
for example internal failure-counter state after lock expiry.

Leave them exactly as generated.

The student will later classify every case as:

VALID
INVALID
INCOMPLETE

and correct them during the Human Audit phase.

==================================================
2. AUTHORITATIVE INPUT
==================================================

Read:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md
23127259/testcases/FR02_AI_DRAFT.md
23127259/docs/SECURITY_APPLICABILITY.md

Also consult authoritative:

- EShop SRS / README requirements
- api_specification.md

Expected results must come only from:

[SRS]
[API-SPEC]

Do NOT derive the oracle from:
- server.js
- database.js
- OBS-xx implementation observations
- known candidate bugs

==================================================
3. SECURITY REQUIREMENT DISCIPLINE
==================================================

Use these authoritative security requirements:

SEC-01:
Passwords must not be stored in plaintext.

SEC-02:
Security-sensitive APIs must require a valid JWT.

SEC-03:
Admin APIs must verify role='admin'.

SEC-04:
User-controlled UI-rendered data must be safely escaped.

SEC-05:
Database queries must use parameterized queries.

SEC-06:
Profile update must not permit client-side role modification.

SEC-07:
Password-reset OTP must have sufficient entropy, expiry, and single-use.

For FR-02:

SEC-01:
PARTIAL black-box coverage.

SEC-02:
INDIRECT / AUTHENTICATION DEPENDENCY.
POST /api/login issues the JWT; it does not itself require JWT.

SEC-05:
PARTIAL black-box behavioral coverage through injection probes.

SEC-03:
NOT directly applicable to POST /api/login.

SEC-04:
UI scoped, not a core login API test.

SEC-06:
NOT applicable to selected FR-02 endpoint.

SEC-07:
Belongs to password-reset / FR-03, not FR-02.

Do NOT force SEC-03/04/06/07 cases into FR-02 just to increase count.

==================================================
4. GENERATION TARGET
==================================================

Generate approximately 7–8 UNIQUE security-focused AI cases.

Continue IDs sequentially from:

FR02-AI-025

Expected end range:

approximately FR02-AI-031 or FR02-AI-032.

Do not pad count.

Each case must have a distinct security objective.

==================================================
5. REQUIRED SECURITY DIMENSIONS
==================================================

Cover the following where specification-supported.

--------------------------------------------------
A. SEC-05 – SQL Injection Behavioral Probes
--------------------------------------------------

Generate:

1. SQL injection-like payload in email
2. SQL injection-like payload in password

Examples may include classic authentication-bypass strings.

Expected behavior:

- payload must not cause unauthorized authentication
- authentication must not succeed unless valid credentials are genuinely
  supplied

Label:

SEC-05 – PARTIAL BLACK-BOX EVIDENCE

Do NOT claim that failure of an injection attack proves that parameterized
queries are implemented.

--------------------------------------------------
B. Credential Enumeration / Error Disclosure
--------------------------------------------------

Generate a security case comparing:

A:
registered email + incorrect password

versus

B:
unregistered syntactically valid email + arbitrary password

Security objective:

the response must not reveal which credential element is incorrect or whether
the email exists, where the SRS explicitly requires generic credential-error
behavior.

This must be distinct from FR02-AI-003 and FR02-AI-004:

Those cases test authentication rejection individually.

This new case tests CROSS-RESPONSE SECURITY EQUIVALENCE / INFORMATION
DISCLOSURE.

Do not create a semantic duplicate.

--------------------------------------------------
C. Sensitive Data Exposure
--------------------------------------------------

Generate a successful-login security case asserting that sensitive credential
material should not be exposed in the API response where supported by the
security requirements.

Separate clearly:

SEC-01:
password storage at rest — PARTIAL / not fully provable via API

from

[ADDITIONAL-SEC]:
plaintext password or credential material appearing in the API response.

Do not claim response-field absence alone proves SEC-01 compliance.

--------------------------------------------------
D. Token Issuance on Authentication Failure
--------------------------------------------------

Generate a case asserting:

invalid credentials must NOT result in successful authentication and must NOT
issue a usable authentication token.

This security assertion must be distinct from merely checking HTTP 401.

If exact error schema is unspecified, do not invent fields.

--------------------------------------------------
E. Token Issuance During Active Lock
--------------------------------------------------

Generate a security case:

account is in LOCKED state
-> submit correct credentials during active lock

Security objective:

lockout must not be bypassed
and no successful authenticated session/token should be issued.

Avoid duplicating FR02-AI-019 by making the security assertion focus
specifically on authentication/token issuance rather than only state
transition.

If this would still be semantically duplicate after review, do NOT create it;
choose another distinct security dimension.

--------------------------------------------------
F. SEC-02 Supporting Token-Usability Probe
--------------------------------------------------

At most one or two supporting cases may verify that a JWT returned by
successful login functions as the authentication credential expected by a
documented protected endpoint.

Clearly label:

SEC-02 SUPPORTING / INDIRECT FR-02 TEST

Possible conceptual flow:

1. POST /api/login with valid credentials
2. capture returned JWT
3. call one documented protected endpoint using:
   Authorization: Bearer <token>
4. authenticated request should be accepted if all other preconditions are met

Optionally contrast with a tampered token.

However:

- do not turn this stage into testing another feature
- do not create a large downstream endpoint suite
- choose the simplest documented protected endpoint available
- document that SEC-02 enforcement belongs primarily to the protected
  endpoint, while FR-02 provides the token

==================================================
6. DO NOT CREATE UNSUPPORTED SECURITY REQUIREMENTS
==================================================

Do NOT generate cases merely because they are common security practices if the
assignment/SRS does not define an oracle.

Examples requiring caution:

- JWT expiration
- refresh tokens
- token revocation
- MFA
- IP-based throttling
- CAPTCHA
- arbitrary password maximum length
- account lock based on IP

If useful, these may later appear as exploratory observations, but they must
not become specification-backed expected failures.

==================================================
7. TEST CASE FORMAT
==================================================

Append cases to:

23127259/testcases/FR02_AI_DRAFT.md

Use the existing format.

Every test must contain:

- Test Case ID
- Title
- Technique
- Security classification
- Requirement reference
- Preconditions
- Request Method
- Endpoint
- Headers
- Exact request data / request sequence
- Expected HTTP Status only when specified
- Expected semantic result
- Expected security result
- State Before
- State After if relevant
- Oracle Confidence
- Black-box limitation
- Notes

Technique may include:

SECURITY
NEGATIVE
INJECTION PROBE
INFORMATION DISCLOSURE
AUTHENTICATION
SEQUENCE TESTING

==================================================
8. ORACLE CONFIDENCE
==================================================

Use:

EXPLICIT
PARTIAL
SPEC-UNDEFINED

Examples:

SQL injection probe:
PARTIAL
because behavioral resistance does not prove parameterized implementation.

Sensitive response field:
PARTIAL unless explicit response exclusion is specified.

Generic wrong-email / wrong-password behavior:
EXPLICIT if SRS explicitly requires non-disclosure.

Downstream JWT usability:
PARTIAL / INDIRECT where appropriate.

==================================================
9. DUPLICATION RULE
==================================================

Before adding each case compare against:

FR02-AI-001..024.

Do NOT add a case if its only difference is wording.

Examples:

FR02-AI-003 already verifies wrong-password rejection.

A new security test is acceptable only if it adds a different assertion,
such as comparing its error message against the unregistered-email response.

FR02-AI-019 already tests correct password during lockout.

Do not duplicate it unless the new test has a genuinely separate security
assertion not already represented.

==================================================
10. HUMAN-CASE INTEGRITY
==================================================

Do NOT create:

FR02-HUM-xxx

Actual Human-designed extension cases are selected only after:

1. >=35 AI-generated cases are complete
2. Human Audit is completed
3. real coverage gaps are identified

Prior AI planning suggestions do NOT count as Human cases.

==================================================
11. UPDATE SUMMARY
==================================================

Update the summary at the top of:

23127259/testcases/FR02_AI_DRAFT.md

Maintain:

| Stage | ID Range | Generated Count |
|---|---|---:|
| 1A.2 Domain/BVA | FR02-AI-001..014 | 14 |
| 1A.3 State/Lockout | FR02-AI-015..024 | 10 |
| 1A.4 Security | FR02-AI-025..XXX | N |

Show cumulative total.

Do not renumber old cases.

==================================================
12. AI AUDIT LOGGING
==================================================

Determine the next real interaction ID.

Expected:
INT-008

Create:

23127259/ai/interactions/INT-008-fr02-security-generation.md

Record truthfully:

- Interaction ID
- AI Tool
- Model
- actual date/time
- Stage:
  FR-02 Stage 4 – Security Test Generation
- Exact prompt
- Full AI output

Update:

23127259/ai/AI_AUDIT_REPORT.md

Do not fabricate metadata.

==================================================
13. QUALITY GATE
==================================================

Before finishing verify:

- only FR-02 security tests were generated
- no FR02-HUM IDs exist
- no source-derived implementation behavior became expected behavior
- SEC mappings are correct
- SEC-01 limitation is documented
- SEC-05 limitation is documented
- credential enumeration test is cross-response, not duplicate rejection
- no unnecessary SEC-03/04/06/07 cases created
- no JWT expiry requirement invented
- cases are semantically distinct from FR02-AI-001..024

==================================================
14. GIT POLICY
==================================================

Do NOT commit.

At the end report:

1. Interaction ID
2. IDs generated
3. Generated count
4. Security dimensions covered
5. SEC requirement mapping
6. Additional-security dimensions
7. Oracle-confidence breakdown
8. Cases intentionally NOT generated due to lack of requirement
9. Cumulative FR-02 AI count
10. Remaining cases needed to reach >=35
11. git status

Then STOP.

Next stage:

PHASE 1A.5 – FR-02 SCHEMA AND ERROR-CONTRACT TEST GENERATION
```

---

## 2. AI Output Summary

- Generated **7 unique security test cases** (`FR02-AI-025` through `FR02-AI-031`) appended to `23127259/testcases/FR02_AI_DRAFT.md`:
  - `FR02-AI-025`: SQL injection behavioral probe in email field (`SEC-05 PARTIAL`)
  - `FR02-AI-026`: SQL injection behavioral probe in password field (`SEC-05 PARTIAL`)
  - `FR02-AI-027`: Cross-response generic credential error equivalence to prevent user enumeration (`[ADDITIONAL-SEC] / SRS FR-02`)
  - `FR02-AI-028`: Sensitive credential exposure probe in successful login response (`[ADDITIONAL-SEC] / SEC-01 PROBE`)
  - `FR02-AI-029`: Token omission assertion on failed authentication (`[ADDITIONAL-SEC]`)
  - `FR02-AI-030`: SEC-02 supporting valid token usability verification on `GET /api/orders/my-orders` (`SEC-02 INDIRECT`)
  - `FR02-AI-031`: SEC-02 supporting tampered signature rejection on protected endpoint (`SEC-02 INDIRECT`)
- Updated summary tracker table: **31 / 35 cumulative test cases** generated.

---

## 3. Human Evaluation & Next Steps

- **Verdict:** VALID for Stage 1A.4 security test coverage.
- **Next Stage:** Phase 1A.5 – Schema Validation & Error-Contract Test Generation (`FR02-AI-032` through `FR02-AI-035`).
