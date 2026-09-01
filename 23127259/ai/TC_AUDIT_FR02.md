# FR-02 Human Test-Case Audit

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Raw AI Generation Inventory:** `FR02-AI-001` .. `FR02-AI-037` (37 cases)
- **Raw AI Generation Hash:** `b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c`
- **Audit Completion Status:** **100% COMPLETE (37 / 37 cases audited by student)**

---

## 1. Audit Policy & Student Governance

Every raw AI-generated test case must receive a formal **STUDENT verdict**:
- **`VALID`**: The test case correctly implements authoritative specification rules without flawed assumptions.
- **`INVALID`**: The test case is logically flawed, contradicts specification, or represents an unneeded duplicate.
- **`INCOMPLETE`**: The test case has valid intent but requires specific corrections/refinements to its oracle or data.

For each test case, the human auditor records:
1. **Raw AI Case ID & Title**
2. **Specification / Oracle Basis**
3. **Student Verdict** (`VALID` / `INVALID` / `INCOMPLETE`)
4. **Student Reasoning** (Technical explanation for the verdict)
5. **Student Correction** (Modifications applied if `INCOMPLETE`)
6. **Final Disposition** (`ACCEPTED AS IS`, `REJECTED`, or `ACCEPTED WITH CORRECTIONS`)
7. **Decision Time** (Timestamp of student verdict)

---

## 2. Master Test-Case Audit Table (100% Audited)

| AI Case ID | Raw Title | Oracle Basis | Student Verdict | Student Reasoning | Student Correction | Final Disposition | Decision Time |
|---|---|---|:---:|---|---|:---:|:---:|
| `FR02-AI-001` | Valid User Login with Registered Credentials | 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2] | **`VALID`** | The case matches the documented successful login contract. The API specification defines POST /api/login with valid credentials as HTTP 200 and returns a JWT token together with user information. The test is a valid baseline positive authentication case. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:46:24 |
| `FR02-AI-002` | Valid Admin Login with Registered Admin Credentials | 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2] | **`VALID`** | A registered admin account is still authenticated through the same POST /api/login endpoint. The expected 200 response, JWT issuance, and returned user information are consistent with the login contract. Verifying that the returned user information preserves role="admin" is reasonable for the seeded admin account. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:46:24 |
| `FR02-AI-003` | Login Rejection on Registered Email with Incorrect Password | 📋 [SRS §2 FR-02] | **`VALID`** | FR-02 explicitly requires failed authentication for incorrect credentials, a generic error that does not disclose whether the email or password was wrong, and an increment of exactly one failed attempt. This case correctly represents the first failed attempt while the account remains unlocked. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:46:24 |
| `FR02-AI-004` | Login Rejection on Unregistered Syntactically Valid Email | 📋 [SRS §2 FR-02] | **`VALID`** | An unregistered email must not authenticate, and FR-02 requires authentication errors not to reveal whether the email or password was incorrect. Comparing this response semantics with the wrong-password case is therefore consistent with the anti-enumeration requirement. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:46:24 |
| `FR02-AI-005` | Login Rejection on Malformed Email Syntax Missing At-Symbol | 📋 [SRS §2 FR-02] | **`INCOMPLETE`** | Using a malformed email is a useful negative/domain-partition test, but the SRS/API specification does not explicitly define email-format validation or require a particular validation error for an address missing "@". The reliable oracle is only that authentication must not succeed; the exact status and validation behavior are unspecified. | Keep the test input, but remove the claim that malformed-email rejection is a mandatory syntax-validation rule. Expected result should be: authentication must not succeed and no JWT must be issued; exact HTTP status and validation message are NOT SPECIFIED. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:46:24 |
| `FR02-AI-006` | Login Rejection on Empty String Email Field | 📋 [SRS §2 FR-02] | **`INCOMPLETE`** | Empty email is a meaningful negative input, but the specification does not explicitly define how an empty string is validated or whether it is rejected by request validation versus normal authentication processing. The current note overstates this as a mandatory field constraint. | Keep email="" as the test input. Assert only that the request must not produce successful authentication or a JWT. Mark exact status, validation message, and processing path as NOT SPECIFIED. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:46:24 |
| `FR02-AI-007` | Login Rejection on Missing Email Property in Request Body | 🗂️ [API-SPEC §1.2] | **`INCOMPLETE`** | The API contract documents email and password as login request fields, so testing a missing email property is useful. However, the specification does not clearly define the exact error schema/status or whether the server must classify it specifically as an "invalid/incomplete payload". | Keep the missing-email test. Expected semantic result should be authentication must not succeed and no JWT should be issued. Leave exact HTTP status and error-message structure as NOT SPECIFIED unless api_specification.md explicitly defines them. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:46:24 |
| `FR02-AI-008` | Login Rejection on Null Email Value in Request Body | 🗂️ [API-SPEC §1.2] | **`INCOMPLETE`** | Null email is a useful robustness and type-domain test, but null-handling behavior is not explicitly specified by FR-02. The assertion that the server must not return 500 is good engineering practice, but it is not a clearly stated FR-02 business oracle. | Retain email=null as an exploratory negative test. Assert that authentication must not succeed; mark exact status, null validation behavior, error schema, and state effects as NOT SPECIFIED. Treat the no-500 expectation as an engineering robustness expectation rather than a formal FR-02 oracle. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:46:24 |
| `FR02-AI-009` | Login Rejection on Whitespace-Only Email Input | 📋 [SRS §2 FR-02] | **`INCOMPLETE`** | Whitespace-only email is a useful domain-partition input, but the specification does not define whitespace trimming, normalization, or a non-blank validation rule for login email. Therefore the test currently implies a validation requirement that is not documented. | Keep the whitespace-only input as exploratory/domain coverage. Assert only that it must not result in successful authentication for the tested account. Do not require trimming or a specific blank-field error; exact behavior remains SPEC-UNDEFINED. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:46:24 |
| `FR02-AI-010` | Login Rejection on Empty String Password Field | 📋 [SRS §2 FR-02] | **`INCOMPLETE`** | Empty password is a meaningful negative input and must not authenticate the registered account, but the specification does not define whether an empty password is rejected during request validation or processed as a failed credential attempt. The current State After is therefore ambiguous and not deterministic. | Keep password="" and assert authentication failure with no JWT. Set exact HTTP status to NOT SPECIFIED unless documented. Set State After / failure-counter effect to NOT SPECIFIED rather than "FAILURE_SEQUENCE_ACTIVE or unchanged". | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:46:24 |
| `FR02-AI-011` | Login Rejection on Missing Password Property in Request Body | 🗂️ [API-SPEC §1.2] | **`INCOMPLETE`** | Omitting the password field is a useful negative request-domain case, but the specification does not define the exact HTTP status, validation message, or whether the request is rejected before authentication processing. The current state-after alternatives are therefore not deterministic. | Keep the missing-password input. Assert only that authentication must not succeed and no JWT must be issued. Mark exact HTTP status, error schema, and failure-counter/state effect as NOT SPECIFIED. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:51:24 |
| `FR02-AI-012` | Login Rejection on Null Password Value in Request Body | 🗂️ [API-SPEC §1.2] | **`INCOMPLETE`** | A null password is a useful robustness/type-domain test, but the SRS/API specification does not explicitly define null handling. The no-500 expectation is an engineering robustness expectation rather than a formal FR-02 business oracle, and the state-after behavior is unspecified. | Keep password=null as an exploratory negative input. Assert authentication non-success and no JWT. Mark exact status, null-validation behavior, error schema, and counter/state effect as NOT SPECIFIED. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:51:24 |
| `FR02-AI-013` | Consecutive Failure Progression at Boundary N=2 (Remains Unlocked) | 📋 [SRS §2 FR-02] | **`VALID`** | FR-02 explicitly locks the account after 3 or more consecutive failed logins. Therefore after the second consecutive failure the account must still remain unlocked. This is a valid N-1 boundary-value test. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:51:24 |
| `FR02-AI-014` | Consecutive Failure Threshold at Boundary N=3 (Account Transitions to Locked) | 📋 [SRS §2 FR-02] | **`VALID`** | FR-02 explicitly defines the lockout threshold at 3 consecutive failed logins. This case correctly verifies the N=3 boundary and transition into the temporary LOCKED state while correctly leaving the exact HTTP status of request #3 unspecified. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:51:24 |
| `FR02-AI-015` | First Consecutive Failed Login Attempt (Normal to Failure Sequence Active, Not Locked) | 📋 [SRS §2 FR-02] | **`VALID`** | This case verifies the first observable transition in the failure sequence. Since the lockout threshold is 3 consecutive failures, the account must remain unlocked after failure #1 and accept subsequent authentication attempts. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:51:24 |
| `FR02-AI-016` | Second Consecutive Failed Login Attempt (Progression in Failure Sequence, Remains Unlocked) | 📋 [SRS §2 FR-02] | **`INVALID`** | This case is semantically duplicate of FR02-AI-013. Both use the same precondition of exactly one prior failure, submit the second wrong password, and assert that the account remains unlocked with two consecutive failures. A different technique label does not create a distinct executable scenario. | Remove from the final deduplicated executable suite or retain only as raw AI-audit evidence. Use FR02-AI-013 as the canonical N=2 case. | `REJECTED (DUPLICATE OF FR02-AI-013)` | 2026-09-01 19:51:24 |
| `FR02-AI-017` | Third Consecutive Failed Login Attempt (Transitions Account into Locked State) | 📋 [SRS §2 FR-02] | **`INVALID`** | This case is semantically duplicate of FR02-AI-014. Both start after two consecutive failures, submit the third wrong password, and assert transition to LOCKED while leaving the exact response status unspecified. | Remove from the final deduplicated executable suite or retain only as raw AI-audit evidence. Use FR02-AI-014 as the canonical N=3 lockout-threshold case. | `REJECTED (DUPLICATE OF FR02-AI-014)` | 2026-09-01 19:51:24 |
| `FR02-AI-018` | Login Rejection on Subsequent Request During Active Lockout Window (Wrong Credentials) | 📋 [SRS §2 FR-02] | **`INCOMPLETE`** | FR-02 supports the core assertion that a request made during the active 30-second lockout window must be rejected and the account remains locked. However, the case additionally requires no stack traces/internal-variable disclosure, which is broader than the primary lockout oracle and is not clearly defined as part of this specific FR-02 behavior. | Keep the active-lock wrong-credentials scenario. Assert temporary-lock rejection, no successful authentication, and LOCKED state. Leave exact status unspecified. Treat stack-trace/debug-data non-disclosure separately as an additional security/robustness assertion unless explicitly supported by the specification. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:51:24 |
| `FR02-AI-019` | Login Rejection on Subsequent Request During Active Lockout Window (Correct Credentials Do Not Bypass Lock) | 📋 [SRS §2 FR-02] | **`VALID`** | An account in an active temporary lockout state must not authenticate before the 30-second window expires. Therefore even correct credentials cannot bypass the lock, and a successful JWT must not be issued. The case correctly leaves the exact 4xx status unspecified. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:51:24 |
| `FR02-AI-020` | Lockout Duration Timing Boundary Check Prior to Expiration (T=25s in 30s Window) | 📋 [SRS §2 FR-02] | **`VALID`** | FR-02 explicitly defines a 30-second lockout duration. Testing at T+25s gives a safely pre-expiration boundary point, so the account must still be locked and valid credentials must not authenticate. The case correctly avoids asserting an undocumented exact 4xx status. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:51:24 |
| `FR02-AI-021` | Lockout Duration Expiration Boundary Check After 30s Window (T=32s Auto-Unlock) | 📋 [SRS §2 FR-02] | **`VALID`** | FR-02 explicitly defines a temporary lockout duration of 30 seconds. At T+32s the lockout interval has expired, so submitting valid credentials must be processed normally and successful authentication should return the documented 200 response and JWT. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:54:34 |
| `FR02-AI-022` | Successful Authentication Resets Consecutive Failure Progression | 📋 [SRS §2 FR-02] | **`VALID`** | FR-02 explicitly states that a successful login resets the consecutive failed-login counter to 0. The wrong -> success -> wrong sequence correctly verifies that the failure after success belongs to a new consecutive-failure sequence and must not prematurely lock the account. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:54:34 |
| `FR02-AI-023` | Consecutive Failure Semantics Verification (Non-Consecutive Failures Do Not Trigger Lockout) | 📋 [SRS §2 FR-02] | **`VALID`** | The lockout rule is based on consecutive failed logins. Because a successful authentication resets the failure sequence, the sequence wrong -> success -> wrong -> wrong contains only two consecutive failures after the reset and therefore must not trigger lockout. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:54:34 |
| `FR02-AI-024` | Post-Lockout Expiration Account Usability and Failure Sequence Reset | 📋 [SRS §2 FR-02] | **`VALID`** | Although lock expiry by itself does not necessarily specify the internal counter state, this test's precondition explicitly includes a successful login after the 30-second lockout has expired. FR-02 explicitly states that successful authentication resets the failure counter to 0. Therefore the following wrong password is correctly treated as the first failure of a fresh sequence. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:54:34 |
| `FR02-AI-025` | SQL Injection Behavioral Probe in Email Field | 📋 [SRS §9 SEC-05] | **`INCOMPLETE`** | The SQL injection payload is a relevant SEC-05 behavioral probe and unauthorized authentication must not occur. However, black-box rejection of one payload cannot prove that the implementation uses parameterized queries as required by SEC-05. The assertions that the response must never be 500 and must never expose SQL errors are also broader engineering/security expectations rather than the complete SEC-05 oracle. | Keep the SQLi email probe and assert that the payload must not bypass authentication or create an unauthorized session. Classify the result as PARTIAL BLACK-BOX EVIDENCE for SEC-05. Do not claim that a passing result proves parameterized queries; supplement with source/DB verification where permitted. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:54:34 |
| `FR02-AI-026` | SQL Injection Behavioral Probe in Password Field | 📋 [SRS §9 SEC-05] | **`INCOMPLETE`** | The password-field SQL injection probe is relevant to SEC-05, but its black-box result only demonstrates behavioral resistance to the selected payload. It cannot establish that all database queries are parameterized, and the no-500/no-database-error assertions are not sufficient proof of SEC-05 compliance. | Retain the password SQLi probe and assert no authentication bypass or unauthorized token issuance. Keep SEC-05 classification as PARTIAL BLACK-BOX EVIDENCE and document that parameterization requires supplemental implementation verification. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:54:34 |
| `FR02-AI-027` | Cross-Response Generic Credential Error Equivalence (Anti-Enumeration) | 📋 [SRS §2 FR-02] ("không để lộ chi tiết nguyên nhân") | **`VALID`** | FR-02 explicitly requires authentication errors not to disclose whether the email or password was incorrect. Comparing the registered-email/wrong-password response against the unregistered-email response is a direct observable test of this non-disclosure requirement. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:54:34 |
| `FR02-AI-028` | Sensitive Credential Exposure Probe in Successful Login Response | 📋 [SRS §9 SEC-01] & Clean Credential Handling | **`INCOMPLETE`** | Checking that the successful login response does not expose a plaintext password is a valuable additional security test, but it is not equivalent to SEC-01. SEC-01 specifically requires passwords not to be stored in plaintext, which cannot be proven merely by inspecting the login response. | Retain the response-sanitization assertion as [ADDITIONAL-SEC] Sensitive Data Exposure. Remove SEC-01 compliance as the primary oracle. State separately that SEC-01 storage-at-rest compliance requires supplemental database/source verification. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:54:34 |
| `FR02-AI-029` | Token Omission Assertion on Failed Authentication | 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2] | **`INCOMPLETE`** | Failed authentication must not provide a usable authenticated session or JWT, so the security objective is valid. However, the specification does not necessarily require the literal token property to be completely absent rather than null or otherwise non-usable. The raw case therefore overspecifies the exact error-response schema. | Change the oracle to: failed authentication must not issue any usable authentication token or authorization capability. Do not require a specific token-field omission/null representation unless api_specification.md explicitly defines it. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:54:34 |
| `FR02-AI-030` | SEC-02 Supporting Token Usability Verification on Protected Endpoint | 📋 [SRS §9 SEC-02] & 📋 [SRS §2 FR-02] | **`VALID`** | FR-02 issues the JWT and the specification states that the returned token is used as Authorization: Bearer <token> on subsequent authenticated APIs. Using one documented protected endpoint to verify that the issued token is usable is a legitimate supporting/indirect FR-02 integration test. The case correctly identifies that SEC-02 enforcement primarily belongs to the downstream protected endpoint. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:54:34 |
| `FR02-AI-031` | SEC-02 Supporting Tampered Signature Rejection on Protected Endpoint | 📋 [SRS §9 SEC-02] & 📋 [SRS §2 FR-02] | **`VALID`** | SEC-02 requires security-sensitive APIs to accept only a valid JWT. A token whose payload/signature has been tampered with is no longer valid, so a documented protected endpoint must reject it. This is acceptable as supporting/indirect FR-02 integration coverage because FR-02 is the token issuer and the protected endpoint is the token consumer. | NONE | `ACCEPTED AS IS` | 2026-09-01 19:56:42 |
| `FR02-AI-032` | Successful Login Response Schema and Data Type Contract | 🗂️ [API-SPEC §1.2] & 📋 [SRS §2 FR-02] | **`INCOMPLETE`** | Validating the successful login response structure is appropriate and the documented contract supports the presence of a token and user information. However, the raw AI case over-specifies several details such as a strictly limited top-level structure, a positive integer ID, exact role enumeration, and a three-part encoded JWT unless all of those are explicitly normative in api_specification.md. | Retain schema validation for fields and types explicitly documented by API-SPEC. Remove or mark as PARTIAL any constraints that are inferred from examples or JWT conventions rather than explicitly specified. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:56:42 |
| `FR02-AI-033` | Invalid Credentials Error Response Schema and Structure Contract | 🗂️ [API-SPEC §1.2] & 📋 [SRS §2 FR-02] | **`INCOMPLETE`** | Validating the generic error response for invalid credentials is appropriate, but the specification does not necessarily mandate the exact error property name or require literal absence of both token and user fields. The important behavior is generic authentication failure with no usable authenticated session/token. | Keep the generic error-contract check. Do not require a particular error key or exact omission representation unless explicitly documented. Assert that authentication fails and no usable authentication token is issued. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:56:42 |
| `FR02-AI-034` | Locked-Account Error Response Contract and Internal Non-Disclosure | 📋 [SRS §2 FR-02] ("thông báo tạm khóa... không để lộ chi tiết") | **`INCOMPLETE`** | FR-02 supports a temporary-lockout notification and non-disclosure of sensitive authentication details. However, the raw case expands this into specific prohibitions on stack, SQL, lockout_until, attempts, and other internal fields that are not individually defined by the FR-02 contract. | Retain the temporary-lockout error response and generic non-disclosure assertion. Leave exact status and field name unspecified, and treat stack trace/database/internal-variable leakage checks as additional security/robustness assertions rather than the formal FR-02 oracle. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:56:42 |
| `FR02-AI-035` | Syntactically Malformed JSON Request Body Transport Contract | 🗂️ [API-SPEC §1.2] & Transport Robustness | **`INCOMPLETE`** | Malformed JSON is a useful transport/parser robustness case, but malformed JSON handling is not explicitly defined by the FR-02 business specification. Therefore requiring a particular 4xx class response, forbidding 500, or requiring a structured JSON parser error is broader than the documented FR-02 oracle. | Retain this as an exploratory transport robustness test. Assert only that malformed input must not result in successful authentication or issuance of a usable JWT. Treat exact status, parser error schema, and no-500 behavior as engineering expectations unless separately documented. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:56:42 |
| `FR02-AI-036` | Response Content-Type Header Contract Across Status Codes | 🗂️ [API-SPEC §1.2] | **`INCOMPLETE`** | Checking Content-Type is useful API-contract validation, but the raw test marks application/json as an EXPLICIT requirement based largely on REST convention. Unless api_specification.md explicitly requires this response header, the assertion is inferred rather than a specification-backed FR-02 oracle. | Keep Content-Type validation only as a PARTIAL or exploratory API-contract check unless the exact JSON response Content-Type is explicitly documented. Do not classify it as EXPLICIT solely because the API uses JSON. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:56:42 |
| `FR02-AI-037` | Extraneous Request Body Properties Ingestion Contract | 🗂️ [API-SPEC §1.2] & Schema Robustness | **`INCOMPLETE`** | Supplying unexpected fields such as role="admin" is a valuable parameter-injection and privilege-escalation probe. However, the login specification does not define whether unknown fields must be rejected or ignored. Therefore the HTTP 200-versus-400 behavior is SPEC-UNDEFINED. The useful security assertion is only that client-supplied login fields must not elevate the authenticated user's actual role. | Retain the test as an exploratory/additional-security parameter-injection case. Do not require either silent ignoring or HTTP 400. Assert only that the supplied role field cannot alter the authenticated account's real authorization role. | `ACCEPTED WITH CORRECTIONS` | 2026-09-01 19:56:42 |

---

## 3. Human Review Batch 1 – FR02-AI-001 .. FR02-AI-010 (COMPLETED)

---

### FR02-AI-001 – Valid User Login with Registered Credentials

- **Raw Technique:** Equivalence Partitioning (EP-EM-01 + EP-PW-01)
- **Raw AI Expected Result:** Status ``HTTP 200 OK``; Response: JSON object containing:
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2]
  - *Clause:* API Spec §1.2 documents POST /api/login returning HTTP 200 with JWT token and user profile object.
- **Specification Ambiguity:** NONE IDENTIFIED

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** The case matches the documented successful login contract. The API specification defines POST /api/login with valid credentials as HTTP 200 and returns a JWT token together with user information. The test is a valid baseline positive authentication case.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

### FR02-AI-002 – Valid Admin Login with Registered Admin Credentials

- **Raw Technique:** Equivalence Partitioning (EP-EM-01 + EP-PW-01)
- **Raw AI Expected Result:** Status ``HTTP 200 OK``; Response: JSON object containing non-empty JWT `token` and `user` object with `role: "admin"`.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2]
  - *Clause:* API Spec §1.2 documents login for all registered accounts including admin users.
- **Specification Ambiguity:** NONE IDENTIFIED

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** A registered admin account is still authenticated through the same POST /api/login endpoint. The expected 200 response, JWT issuance, and returned user information are consistent with the login contract. Verifying that the returned user information preserves role="admin" is reasonable for the seeded admin account.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

### FR02-AI-003 – Login Rejection on Registered Email with Incorrect Password

- **Raw Technique:** Equivalence Partitioning (EP-EM-01 + EP-PW-02)
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized` (or 4xx generic error)`; Response: Generic error message (e.g. `"Invalid email or password"`) without disclosing whether email or password was the cause.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02 mandates failure message for incorrect password without disclosing which credential failed.
- **Specification Ambiguity:** NONE IDENTIFIED

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** FR-02 explicitly requires failed authentication for incorrect credentials, a generic error that does not disclose whether the email or password was wrong, and an increment of exactly one failed attempt. This case correctly represents the first failed attempt while the account remains unlocked.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

### FR02-AI-004 – Login Rejection on Unregistered Syntactically Valid Email

- **Raw Technique:** Equivalence Partitioning (EP-EM-02 + EP-PW-01)
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized` (or 4xx generic error)`; Response: Generic error message identical to wrong-password response (prevents account enumeration).
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02 mandates generic error message for invalid credentials to prevent user enumeration.
- **Specification Ambiguity:** NONE IDENTIFIED

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** An unregistered email must not authenticate, and FR-02 requires authentication errors not to reveal whether the email or password was incorrect. Comparing this response semantics with the wrong-password case is therefore consistent with the anti-enumeration requirement.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

### FR02-AI-005 – Login Rejection on Malformed Email Syntax Missing At-Symbol

- **Raw Technique:** Equivalence Partitioning / Negative (EP-EM-03 + EP-PW-01)
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 400 Bad Request or 401 Unauthorized)`; Response: Error response; authentication must strictly not succeed.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02 requires valid email format; rejection is required. Exact 4xx code (400 vs 401) is not specified.
- **Specification Ambiguity:** Exact HTTP status code (400 Bad Request vs 401 Unauthorized) is NOT SPECIFIED in API spec.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Using a malformed email is a useful negative/domain-partition test, but the SRS/API specification does not explicitly define email-format validation or require a particular validation error for an address missing "@". The reliable oracle is only that authentication must not succeed; the exact status and validation behavior are unspecified.
- **Correction:** Keep the test input, but remove the claim that malformed-email rejection is a mandatory syntax-validation rule. Expected result should be: authentication must not succeed and no JWT must be issued; exact HTTP status and validation message are NOT SPECIFIED.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

### FR02-AI-006 – Login Rejection on Empty String Email Field

- **Raw Technique:** Equivalence Partitioning / Negative (EP-EM-04 + EP-PW-01)
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 400 or 401)`; Response: Error response; authentication must strictly not succeed.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* Email is logically mandatory. Empty string must not authenticate. Exact 4xx code is not specified.
- **Specification Ambiguity:** Exact HTTP status code for empty input is NOT SPECIFIED in API spec.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Empty email is a meaningful negative input, but the specification does not explicitly define how an empty string is validated or whether it is rejected by request validation versus normal authentication processing. The current note overstates this as a mandatory field constraint.
- **Correction:** Keep email="" as the test input. Assert only that the request must not produce successful authentication or a JWT. Mark exact status, validation message, and processing path as NOT SPECIFIED.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

### FR02-AI-007 – Login Rejection on Missing Email Property in Request Body

- **Raw Technique:** Equivalence Partitioning / Negative (EP-EM-05 + EP-PW-01)
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 400 or 401)`; Response: Error response indicating invalid/incomplete payload; authentication must not succeed.
- **Relevant Specification Evidence:**
  - *Source:* 🗂️ [API-SPEC §1.2]
  - *Clause:* Payload schema requires email property. Omitting email must fail authentication.
- **Specification Ambiguity:** Exact HTTP status code for missing schema property is NOT SPECIFIED in API spec.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** The API contract documents email and password as login request fields, so testing a missing email property is useful. However, the specification does not clearly define the exact error schema/status or whether the server must classify it specifically as an "invalid/incomplete payload".
- **Correction:** Keep the missing-email test. Expected semantic result should be authentication must not succeed and no JWT should be issued. Leave exact HTTP status and error-message structure as NOT SPECIFIED unless api_specification.md explicitly defines them.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

### FR02-AI-008 – Login Rejection on Null Email Value in Request Body

- **Raw Technique:** Equivalence Partitioning / Negative (EP-EM-06 + EP-PW-01)
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 400 or 401)`; Response: Error response; server must not crash or return unhandled 500 error.
- **Relevant Specification Evidence:**
  - *Source:* 🗂️ [API-SPEC §1.2]
  - *Clause:* Null JSON value must not cause unhandled 500 error or authenticate. Rejection is required.
- **Specification Ambiguity:** Exact HTTP status code for null input is NOT SPECIFIED in API spec.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Null email is a useful robustness and type-domain test, but null-handling behavior is not explicitly specified by FR-02. The assertion that the server must not return 500 is good engineering practice, but it is not a clearly stated FR-02 business oracle.
- **Correction:** Retain email=null as an exploratory negative test. Assert that authentication must not succeed; mark exact status, null validation behavior, error schema, and state effects as NOT SPECIFIED. Treat the no-500 expectation as an engineering robustness expectation rather than a formal FR-02 oracle.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

### FR02-AI-009 – Login Rejection on Whitespace-Only Email Input

- **Raw Technique:** Equivalence Partitioning / Negative (EP-EM-07 + EP-PW-01)
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 400 or 401)`; Response: Rejection notice; authentication must not succeed.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* Whitespace-only email must not authenticate as a valid registered user.
- **Specification Ambiguity:** Whether whitespace is trimmed prior to validation is SPEC-UNDEFINED.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Whitespace-only email is a useful domain-partition input, but the specification does not define whitespace trimming, normalization, or a non-blank validation rule for login email. Therefore the test currently implies a validation requirement that is not documented.
- **Correction:** Keep the whitespace-only input as exploratory/domain coverage. Assert only that it must not result in successful authentication for the tested account. Do not require trimming or a specific blank-field error; exact behavior remains SPEC-UNDEFINED.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

### FR02-AI-010 – Login Rejection on Empty String Password Field

- **Raw Technique:** Equivalence Partitioning / Negative (EP-EM-01 + EP-PW-03)
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 400 or 401)`; Response: Rejection notice; authentication must not succeed.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* Password is logically mandatory. Empty password must not authenticate.
- **Specification Ambiguity:** Exact HTTP status code (400 vs 401) for empty password is NOT SPECIFIED in API spec.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Empty password is a meaningful negative input and must not authenticate the registered account, but the specification does not define whether an empty password is rejected during request validation or processed as a failed credential attempt. The current State After is therefore ambiguous and not deterministic.
- **Correction:** Keep password="" and assert authentication failure with no JWT. Set exact HTTP status to NOT SPECIFIED unless documented. Set State After / failure-counter effect to NOT SPECIFIED rather than "FAILURE_SEQUENCE_ACTIVE or unchanged".
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:46:24`

---

## 4. Human Review Batch 2 – FR02-AI-011 .. FR02-AI-020 (COMPLETED)

---

### FR02-AI-011 – Login Rejection on Missing Password Property in Request Body

- **Raw Technique:** Equivalence Partitioning / Negative (EP-EM-01 + EP-PW-04)
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 400 or 401)`; Response: Error response; authentication must strictly not succeed.
- **Relevant Specification Evidence:**
  - *Source:* 🗂️ [API-SPEC §1.2]
  - *Clause:* API Spec §1.2 defines login schema requiring password property.
- **Specification Ambiguity:** Exact HTTP status code for missing password key is NOT SPECIFIED (400 vs 401).

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Omitting the password field is a useful negative request-domain case, but the specification does not define the exact HTTP status, validation message, or whether the request is rejected before authentication processing. The current state-after alternatives are therefore not deterministic.
- **Correction:** Keep the missing-password input. Assert only that authentication must not succeed and no JWT must be issued. Mark exact HTTP status, error schema, and failure-counter/state effect as NOT SPECIFIED.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

### FR02-AI-012 – Login Rejection on Null Password Value in Request Body

- **Raw Technique:** Equivalence Partitioning / Negative (EP-EM-01 + EP-PW-05)
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 400 or 401)`; Response: Error response; server must not crash or return unhandled 500 error.
- **Relevant Specification Evidence:**
  - *Source:* 🗂️ [API-SPEC §1.2]
  - *Clause:* Type safety constraint: null password must not authenticate.
- **Specification Ambiguity:** Exact 4xx status code and error message structure are NOT SPECIFIED.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** A null password is a useful robustness/type-domain test, but the SRS/API specification does not explicitly define null handling. The no-500 expectation is an engineering robustness expectation rather than a formal FR-02 business oracle, and the state-after behavior is unspecified.
- **Correction:** Keep password=null as an exploratory negative input. Assert authentication non-success and no JWT. Mark exact status, null-validation behavior, error schema, and counter/state effect as NOT SPECIFIED.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

### FR02-AI-013 – Consecutive Failure Progression at Boundary N=2 (Remains Unlocked)

- **Raw Technique:** Boundary Value Analysis (BVA $N=2$)
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized` (or 4xx generic credential error)`; Response: Generic credential failure message; account must **remain UNLOCKED** (subsequent login attempts still processed).
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Lockout triggers after 3 consecutive failures. At N=2, account must remain UNLOCKED.
- **Specification Ambiguity:** Whether attempt #2 response body contains a remaining attempts indicator is SPEC-UNDEFINED.

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** FR-02 explicitly locks the account after 3 or more consecutive failed logins. Therefore after the second consecutive failure the account must still remain unlocked. This is a valid N-1 boundary-value test.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

### FR02-AI-014 – Consecutive Failure Threshold at Boundary N=3 (Account Transitions to Locked)

- **Raw Technique:** Boundary Value Analysis (BVA $N=3$)
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` on request #3 (HTTP 401 or HTTP 403)`; Response: Authentication rejected; account state **transitions to LOCKED**. Any subsequent request during the 30-second lockout window must be rejected with a temporary lockout notice.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Account locks after 3 consecutive failed attempts.
- **Specification Ambiguity:** Exact HTTP status code on 3rd failing request (401 vs 403) is NOT SPECIFIED in SRS.

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** FR-02 explicitly defines the lockout threshold at 3 consecutive failed logins. This case correctly verifies the N=3 boundary and transition into the temporary LOCKED state while correctly leaving the exact HTTP status of request #3 unspecified.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

### FR02-AI-015 – First Consecutive Failed Login Attempt (Normal to Failure Sequence Active, Not Locked)

- **Raw Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized` (or 4xx generic credential error)`; Response: Generic error message (e.g. `"Invalid email or password"`); account must **remain UNLOCKED** and immediately accept subsequent login attempts for credential evaluation.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: 1st consecutive failed attempt initiates failure sequence; account remains UNLOCKED.
- **Specification Ambiguity:** NONE IDENTIFIED

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** This case verifies the first observable transition in the failure sequence. Since the lockout threshold is 3 consecutive failures, the account must remain unlocked after failure #1 and accept subsequent authentication attempts.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

### FR02-AI-016 – Second Consecutive Failed Login Attempt (Progression in Failure Sequence, Remains Unlocked)

- **Raw Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized` (or 4xx generic credential error)`; Response: Generic credential error message; account must **remain UNLOCKED**.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: 2nd consecutive failed attempt accumulates count; account remains UNLOCKED.
- **Specification Ambiguity:** Duplicate of FR02-AI-013 (BVA N=2 vs State Transition N=2).

#### Human Decision:
- **Verdict:** `INVALID`
- **Reasoning:** This case is semantically duplicate of FR02-AI-013. Both use the same precondition of exactly one prior failure, submit the second wrong password, and assert that the account remains unlocked with two consecutive failures. A different technique label does not create a distinct executable scenario.
- **Correction:** Remove from the final deduplicated executable suite or retain only as raw AI-audit evidence. Use FR02-AI-013 as the canonical N=2 case.
- **Final Disposition:** `REJECTED (DUPLICATE OF FR02-AI-013)`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

### FR02-AI-017 – Third Consecutive Failed Login Attempt (Transitions Account into Locked State)

- **Raw Technique:** STATE TRANSITION / BVA
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` on request #3 (HTTP 401 or HTTP 403)`; Response: Authentication rejected; account state **transitions to LOCKED**. Any subsequent request during the 30-second lockout window must be rejected with a temporary lockout notice.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: 3rd consecutive failed attempt transitions account state into LOCKED.
- **Specification Ambiguity:** Duplicate of FR02-AI-014 (BVA N=3 vs State Transition N=3).

#### Human Decision:
- **Verdict:** `INVALID`
- **Reasoning:** This case is semantically duplicate of FR02-AI-014. Both start after two consecutive failures, submit the third wrong password, and assert transition to LOCKED while leaving the exact response status unspecified.
- **Correction:** Remove from the final deduplicated executable suite or retain only as raw AI-audit evidence. Use FR02-AI-014 as the canonical N=3 lockout-threshold case.
- **Final Disposition:** `REJECTED (DUPLICATE OF FR02-AI-014)`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

### FR02-AI-018 – Login Rejection on Subsequent Request During Active Lockout Window (Wrong Credentials)

- **Raw Technique:** STATE TRANSITION / NEGATIVE
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 403 Forbidden / 429 Too Many Requests / 4xx)`; Response: Error notice indicating account is temporarily locked without disclosing internal variables or stack traces.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Active lockout rejects requests for 30 seconds. Wrong password while locked must be rejected.
- **Specification Ambiguity:** Exact status code (401 vs 403) and distinct lockout error message format.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** FR-02 supports the core assertion that a request made during the active 30-second lockout window must be rejected and the account remains locked. However, the case additionally requires no stack traces/internal-variable disclosure, which is broader than the primary lockout oracle and is not clearly defined as part of this specific FR-02 behavior.
- **Correction:** Keep the active-lock wrong-credentials scenario. Assert temporary-lock rejection, no successful authentication, and LOCKED state. Leave exact status unspecified. Treat stack-trace/debug-data non-disclosure separately as an additional security/robustness assertion unless explicitly supported by the specification.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

### FR02-AI-019 – Login Rejection on Subsequent Request During Active Lockout Window (Correct Credentials Do Not Bypass Lock)

- **Raw Technique:** STATE TRANSITION / NEGATIVE / SECURITY
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 403 Forbidden / 429 / 4xx)`; Response: Error notice indicating account is temporarily locked; authentication must strictly NOT succeed and NO JWT token must be issued.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Correct credentials submitted during active lockout window must NOT bypass lock.
- **Specification Ambiguity:** Exact status code (401 vs 403) and distinct lockout error message format.

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** An account in an active temporary lockout state must not authenticate before the 30-second window expires. Therefore even correct credentials cannot bypass the lock, and a successful JWT must not be issued. The case correctly leaves the exact 4xx status unspecified.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

### FR02-AI-020 – Lockout Duration Timing Boundary Check Prior to Expiration (T=25s in 30s Window)

- **Raw Technique:** BVA / STATE TRANSITION
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 403 / 429 / 4xx)`; Response: Rejection with temporary lockout notice; authentication must not succeed.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Lockout duration is 30 seconds. At T=25s (< 30s), account must remain locked.
- **Specification Ambiguity:** Timing precision in asynchronous server runtime.

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** FR-02 explicitly defines a 30-second lockout duration. Testing at T+25s gives a safely pre-expiration boundary point, so the account must still be locked and valid credentials must not authenticate. The case correctly avoids asserting an undocumented exact 4xx status.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:51:24`

---

## 5. Human Review Batch 3 – FR02-AI-021 .. FR02-AI-030 (COMPLETED)

---

### FR02-AI-021 – Lockout Duration Expiration Boundary Check After 30s Window (T=32s Auto-Unlock)

- **Raw Technique:** BVA / STATE TRANSITION
- **Raw AI Expected Result:** Status ``HTTP 200 OK``; Response: Successful login response returning valid JWT `token` and `user` object.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Lockout duration is 30 seconds. After 30 seconds have elapsed (T=32s), the account must automatically unlock and accept authentication.
- **Specification Ambiguity:** Timing accuracy of server background expiration vs lazy request-time evaluation.

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** FR-02 explicitly defines a temporary lockout duration of 30 seconds. At T+32s the lockout interval has expired, so submitting valid credentials must be processed normally and successful authentication should return the documented 200 response and JWT.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

### FR02-AI-022 – Successful Authentication Resets Consecutive Failure Progression

- **Raw Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Raw AI Expected Result:** Status `- Step 1: `HTTP 401 Unauthorized``; Response: At Step 3, account must **remain UNLOCKED** (treated as 1st failure of a new sequence, not 2nd cumulative failure).
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Successful authentication resets consecutive failed login counter to zero.
- **Specification Ambiguity:** NONE IDENTIFIED

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** FR-02 explicitly states that a successful login resets the consecutive failed-login counter to 0. The wrong -> success -> wrong sequence correctly verifies that the failure after success belongs to a new consecutive-failure sequence and must not prematurely lock the account.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

### FR02-AI-023 – Consecutive Failure Semantics Verification (Non-Consecutive Failures Do Not Trigger Lockout)

- **Raw Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Raw AI Expected Result:** Status `- Step 1: `HTTP 401 Unauthorized``; Response: At Step 4, total lifetime failures in session is 3, but consecutive failures in active sequence is only 2. Account must **remain UNLOCKED**.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Lockout applies to *consecutive* failed attempts. An interleaved successful login prevents lockout progression on subsequent failure.
- **Specification Ambiguity:** NONE IDENTIFIED

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** The lockout rule is based on consecutive failed logins. Because a successful authentication resets the failure sequence, the sequence wrong -> success -> wrong -> wrong contains only two consecutive failures after the reset and therefore must not trigger lockout.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

### FR02-AI-024 – Post-Lockout Expiration Account Usability and Failure Sequence Reset

- **Raw Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized``; Response: Generic credential error; account must **remain UNLOCKED** (behaving as attempt=1 of a fresh lifecycle).
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: After lockout expiration, account is fully unlocked. Post-lockout failure progression starts fresh.
- **Specification Ambiguity:** Reset is deterministic following the post-expiration successful login.

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** Although lock expiry by itself does not necessarily specify the internal counter state, this test's precondition explicitly includes a successful login after the 30-second lockout has expired. FR-02 explicitly states that successful authentication resets the failure counter to 0. Therefore the following wrong password is correctly treated as the first failure of a fresh sequence.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

### FR02-AI-025 – SQL Injection Behavioral Probe in Email Field

- **Raw Technique:** INJECTION PROBE / SECURITY (SEC-05)
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized` (or 4xx generic error; strictly NOT 200 OK, NOT 500 Internal Server Error)`; Response: N/A
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §9 SEC-05]
  - *Clause:* SRS §9 SEC-05: Database queries must use parameterized queries. Injection strings in email must not bypass auth.
- **Specification Ambiguity:** Black-box probe provides PARTIAL evidence; full SEC-05 compliance requires source verification.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** The SQL injection payload is a relevant SEC-05 behavioral probe and unauthorized authentication must not occur. However, black-box rejection of one payload cannot prove that the implementation uses parameterized queries as required by SEC-05. The assertions that the response must never be 500 and must never expose SQL errors are also broader engineering/security expectations rather than the complete SEC-05 oracle.
- **Correction:** Keep the SQLi email probe and assert that the payload must not bypass authentication or create an unauthorized session. Classify the result as PARTIAL BLACK-BOX EVIDENCE for SEC-05. Do not claim that a passing result proves parameterized queries; supplement with source/DB verification where permitted.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

### FR02-AI-026 – SQL Injection Behavioral Probe in Password Field

- **Raw Technique:** INJECTION PROBE / SECURITY (SEC-05)
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized` (or 4xx generic error; strictly NOT 200 OK, NOT 500)`; Response: N/A
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §9 SEC-05]
  - *Clause:* SRS §9 SEC-05: Parameterized queries prevent SQL injection in password field.
- **Specification Ambiguity:** Black-box probe provides PARTIAL evidence; full SEC-05 compliance requires source verification.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** The password-field SQL injection probe is relevant to SEC-05, but its black-box result only demonstrates behavioral resistance to the selected payload. It cannot establish that all database queries are parameterized, and the no-500/no-database-error assertions are not sufficient proof of SEC-05 compliance.
- **Correction:** Retain the password SQLi probe and assert no authentication bypass or unauthorized token issuance. Keep SEC-05 classification as PARTIAL BLACK-BOX EVIDENCE and document that parameterization requires supplemental implementation verification.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

### FR02-AI-027 – Cross-Response Generic Credential Error Equivalence (Anti-Enumeration)

- **Raw Technique:** INFORMATION DISCLOSURE / SECURITY
- **Raw AI Expected Result:** Status `- Step 1: `HTTP 401 Unauthorized` (or 4xx)`; Response: N/A
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Failed logins must return generic error not revealing whether email or password failed.
- **Specification Ambiguity:** NONE IDENTIFIED

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** FR-02 explicitly requires authentication errors not to disclose whether the email or password was incorrect. Comparing the registered-email/wrong-password response against the unregistered-email response is a direct observable test of this non-disclosure requirement.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

### FR02-AI-028 – Sensitive Credential Exposure Probe in Successful Login Response

- **Raw Technique:** SECURITY / SENSITIVE DATA EXPOSURE
- **Raw AI Expected Result:** Status ``HTTP 200 OK``; Response: N/A
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §9 SEC-01] & [ADDITIONAL-SEC]
  - *Clause:* Response sanitization: login response must not include plaintext password in user object.
- **Specification Ambiguity:** Response sanitization is transport-level; SEC-01 mandates hashing at rest in DB.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Checking that the successful login response does not expose a plaintext password is a valuable additional security test, but it is not equivalent to SEC-01. SEC-01 specifically requires passwords not to be stored in plaintext, which cannot be proven merely by inspecting the login response.
- **Correction:** Retain the response-sanitization assertion as [ADDITIONAL-SEC] Sensitive Data Exposure. Remove SEC-01 compliance as the primary oracle. State separately that SEC-01 storage-at-rest compliance requires supplemental database/source verification.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

### FR02-AI-029 – Token Omission Assertion on Failed Authentication

- **Raw Technique:** SECURITY / AUTHENTICATION
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized` (or 4xx)`; Response: N/A
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2]
  - *Clause:* API Spec §1.2: Token is returned only on HTTP 200 success. Failed requests (4xx) must omit token property.
- **Specification Ambiguity:** Oracle should assert token non-usability without overspecifying error body structure.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Failed authentication must not provide a usable authenticated session or JWT, so the security objective is valid. However, the specification does not necessarily require the literal token property to be completely absent rather than null or otherwise non-usable. The raw case therefore overspecifies the exact error-response schema.
- **Correction:** Change the oracle to: failed authentication must not issue any usable authentication token or authorization capability. Do not require a specific token-field omission/null representation unless api_specification.md explicitly defines it.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

### FR02-AI-030 – SEC-02 Supporting Token Usability Verification on Protected Endpoint

- **Raw Technique:** SECURITY / AUTHENTICATION / SEQUENCE TESTING
- **Raw AI Expected Result:** Status `- Step 1: `HTTP 200 OK``; Response: N/A
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §9 SEC-02] & 🗂️ [API-SPEC §1.2]
  - *Clause:* SEC-02: Valid JWT issued by login must successfully authenticate on protected endpoint (GET /api/orders/my-orders).
- **Specification Ambiguity:** Cross-feature endpoint dependency (probes JWT token validity on downstream order API).

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** FR-02 issues the JWT and the specification states that the returned token is used as Authorization: Bearer <token> on subsequent authenticated APIs. Using one documented protected endpoint to verify that the issued token is usable is a legitimate supporting/indirect FR-02 integration test. The case correctly identifies that SEC-02 enforcement primarily belongs to the downstream protected endpoint.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:54:34`

---

## 6. Human Review Batch 4 – FR02-AI-031 .. FR02-AI-037 (COMPLETED)

---

### FR02-AI-031 – SEC-02 Supporting Tampered Signature Rejection on Protected Endpoint

- **Raw Technique:** SECURITY / SIGNATURE INTEGRITY / SEQUENCE TESTING
- **Raw AI Expected Result:** Status `- Step 1: `HTTP 200 OK``; Response: N/A
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §9 SEC-02] & 🗂️ [API-SPEC §1.2]
  - *Clause:* SEC-02: Tampered JWT signature must be rejected on protected endpoint (GET /api/orders/my-orders) with 401 Unauthorized.
- **Specification Ambiguity:** Probes JWT signature validation on downstream endpoint.

#### Human Decision:
- **Verdict:** `VALID`
- **Reasoning:** SEC-02 requires security-sensitive APIs to accept only a valid JWT. A token whose payload/signature has been tampered with is no longer valid, so a documented protected endpoint must reject it. This is acceptable as supporting/indirect FR-02 integration coverage because FR-02 is the token issuer and the protected endpoint is the token consumer.
- **Correction:** NONE
- **Final Disposition:** `ACCEPTED AS IS`
- **Decision Timestamp:** `2026-09-01 19:56:42`

---

### FR02-AI-032 – Successful Login Response Schema and Data Type Contract

- **Raw Technique:** SCHEMA VALIDATION / API CONTRACT
- **Raw AI Expected Result:** Status ``HTTP 200 OK``; Response: Top-level JSON object strictly containing documented contract attributes.
- **Relevant Specification Evidence:**
  - *Source:* 🗂️ [API-SPEC §1.2]
  - *Clause:* API Spec §1.2 documents 200 OK success response schema containing token string and user profile object.
- **Specification Ambiguity:** NONE IDENTIFIED

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Validating the successful login response structure is appropriate and the documented contract supports the presence of a token and user information. However, the raw AI case over-specifies several details such as a strictly limited top-level structure, a positive integer ID, exact role enumeration, and a three-part encoded JWT unless all of those are explicitly normative in api_specification.md.
- **Correction:** Retain schema validation for fields and types explicitly documented by API-SPEC. Remove or mark as PARTIAL any constraints that are inferred from examples or JWT conventions rather than explicitly specified.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:56:42`

---

### FR02-AI-033 – Invalid Credentials Error Response Schema and Structure Contract

- **Raw Technique:** SCHEMA VALIDATION / ERROR CONTRACT
- **Raw AI Expected Result:** Status ``HTTP 401 Unauthorized` (or 4xx error)`; Response: Valid JSON error object.
- **Relevant Specification Evidence:**
  - *Source:* 🗂️ [API-SPEC §1.2]
  - *Clause:* API Spec §1.2 documents 401 error response returning error message string.
- **Specification Ambiguity:** Whether error response contains additional metadata fields is SPEC-UNDEFINED.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Validating the generic error response for invalid credentials is appropriate, but the specification does not necessarily mandate the exact error property name or require literal absence of both token and user fields. The important behavior is generic authentication failure with no usable authenticated session/token.
- **Correction:** Keep the generic error-contract check. Do not require a particular error key or exact omission representation unless explicitly documented. Assert that authentication fails and no usable authentication token is issued.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:56:42`

---

### FR02-AI-034 – Locked-Account Error Response Contract and Internal Non-Disclosure

- **Raw Technique:** SCHEMA VALIDATION / ERROR CONTRACT
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 403 Forbidden / 429 / 4xx)`; Response: Valid JSON error object informing of temporary lockout.
- **Relevant Specification Evidence:**
  - *Source:* 📋 [SRS §2 FR-02]
  - *Clause:* SRS §2 FR-02: Lockout error response must not disclose internal debug variables or stack traces.
- **Specification Ambiguity:** Exact error schema and status code (401 vs 403) are NOT SPECIFIED in SRS.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** FR-02 supports a temporary-lockout notification and non-disclosure of sensitive authentication details. However, the raw case expands this into specific prohibitions on stack, SQL, lockout_until, attempts, and other internal fields that are not individually defined by the FR-02 contract.
- **Correction:** Retain the temporary-lockout error response and generic non-disclosure assertion. Leave exact status and field name unspecified, and treat stack trace/database/internal-variable leakage checks as additional security/robustness assertions rather than the formal FR-02 oracle.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:56:42`

---

### FR02-AI-035 – Syntactically Malformed JSON Request Body Transport Contract

- **Raw Technique:** NEGATIVE CONTRACT / PARSER RESILIENCE
- **Raw AI Expected Result:** Status ``NOT SPECIFIED` (HTTP 400 Bad Request or 4xx; strictly NOT 200 OK, NOT 500 Internal Server Error)`; Response: Client error response; server parser must handle malformed JSON cleanly without unhandled runtime crash or HTML stack trace leakage.
- **Relevant Specification Evidence:**
  - *Source:* 🗂️ [API-SPEC §1.2]
  - *Clause:* Syntactically malformed JSON body must be rejected (4xx) without unhandled 500 error.
- **Specification Ambiguity:** Exact 4xx status (400 vs 422) is NOT SPECIFIED.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Malformed JSON is a useful transport/parser robustness case, but malformed JSON handling is not explicitly defined by the FR-02 business specification. Therefore requiring a particular 4xx class response, forbidding 500, or requiring a structured JSON parser error is broader than the documented FR-02 oracle.
- **Correction:** Retain this as an exploratory transport robustness test. Assert only that malformed input must not result in successful authentication or issuance of a usable JWT. Treat exact status, parser error schema, and no-500 behavior as engineering expectations unless separately documented.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:56:42`

---

### FR02-AI-036 – Response Content-Type Header Contract Across Status Codes

- **Raw Technique:** API CONTRACT / HEADER VALIDATION
- **Raw AI Expected Result:** Status `- Step 1: `HTTP 200 OK``; Response: - Both Step 1 and Step 2 HTTP responses must include the header `Content-Type: application/json` (or `application/json; charset=utf-8`).
- **Relevant Specification Evidence:**
  - *Source:* 🗂️ [API-SPEC §1.2]
  - *Clause:* API Spec §1.2 defines JSON API contracts across all endpoints.
- **Specification Ambiguity:** Whether explicit Content-Type: application/json header assertion is mandatory on errors is SPEC-UNDEFINED.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Checking Content-Type is useful API-contract validation, but the raw test marks application/json as an EXPLICIT requirement based largely on REST convention. Unless api_specification.md explicitly requires this response header, the assertion is inferred rather than a specification-backed FR-02 oracle.
- **Correction:** Keep Content-Type validation only as a PARTIAL or exploratory API-contract check unless the exact JSON response Content-Type is explicitly documented. Do not classify it as EXPLICIT solely because the API uses JSON.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:56:42`

---

### FR02-AI-037 – Extraneous Request Body Properties Ingestion Contract

- **Raw Technique:** API CONTRACT / EXPLORATORY SCHEMA
- **Raw AI Expected Result:** Status ``HTTP 200 OK` (or 400 if strict schema validation is enforced)`; Response: If login succeeds, the issued JWT and `user` object must reflect the actual database role (`"user"`), and injected extraneous fields must be ignored.
- **Relevant Specification Evidence:**
  - *Source:* 🗂️ [API-SPEC §1.2] & [SRS §9 SEC-06]
  - *Clause:* Extraneous request body fields (e.g., injected 'role': 'admin') must not escalate user privilege or cause unhandled error.
- **Specification Ambiguity:** Whether extraneous fields are rejected with 400 or silently ignored during auth is SPEC-UNDEFINED.

#### Human Decision:
- **Verdict:** `INCOMPLETE`
- **Reasoning:** Supplying unexpected fields such as role="admin" is a valuable parameter-injection and privilege-escalation probe. However, the login specification does not define whether unknown fields must be rejected or ignored. Therefore the HTTP 200-versus-400 behavior is SPEC-UNDEFINED. The useful security assertion is only that client-supplied login fields must not elevate the authenticated user's actual role.
- **Correction:** Retain the test as an exploratory/additional-security parameter-injection case. Do not require either silent ignoring or HTTP 400. Assert only that the supplied role field cannot alter the authenticated account's real authorization role.
- **Final Disposition:** `ACCEPTED WITH CORRECTIONS`
- **Decision Timestamp:** `2026-09-01 19:56:42`

---

## 7. Human Audit Summary & Final Accounting

### Overall Verdict Distribution
- **Total Raw AI Cases Audited:** 37
- **`VALID` (Accepted As Is):** 16 cases (43.2%)
  - `FR02-AI-001`, `FR02-AI-002`, `FR02-AI-003`, `FR02-AI-004`, `FR02-AI-013`, `FR02-AI-014`, `FR02-AI-015`, `FR02-AI-019`, `FR02-AI-020`, `FR02-AI-021`, `FR02-AI-022`, `FR02-AI-023`, `FR02-AI-024`, `FR02-AI-027`, `FR02-AI-030`, `FR02-AI-031`
- **`INVALID` (Rejected as Redundant Duplicates):** 2 cases (5.4%)
  - `FR02-AI-016` (Duplicate of `FR02-AI-013`)
  - `FR02-AI-017` (Duplicate of `FR02-AI-014`)
- **`INCOMPLETE` (Accepted With Corrections):** 19 cases (51.4%)
  - `FR02-AI-005`, `FR02-AI-006`, `FR02-AI-007`, `FR02-AI-008`, `FR02-AI-009`, `FR02-AI-010`, `FR02-AI-011`, `FR02-AI-012`, `FR02-AI-018`, `FR02-AI-025`, `FR02-AI-026`, `FR02-AI-028`, `FR02-AI-029`, `FR02-AI-032`, `FR02-AI-033`, `FR02-AI-034`, `FR02-AI-035`, `FR02-AI-036`, `FR02-AI-037`

### Net Executable AI Inventory Post-Audit
- **Accepted Executable AI Cases:** 35 cases (16 `VALID` + 19 `INCOMPLETE with corrections`)
- **Meets Mandatory HW06 Threshold:** $\ge 35$ AI test cases $ightarrow$ **100% Satisfied**.
