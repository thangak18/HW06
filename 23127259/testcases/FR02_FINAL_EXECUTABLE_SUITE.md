# FR-02 Final Executable Test Suite Specification

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

> [!IMPORTANT]
> **Authoritative Implementation Source:**
> This document is the authoritative specification for all executable Postman requests. It incorporates the audited outcomes of all 37 raw AI test cases and 5 student-selected Human extensions. Rejected duplicates (`FR02-AI-016`, `FR02-AI-017`) are explicitly excluded.

---

## 1. Suite Accounting Summary

| Source | Raw Considered | Rejected / Deduplicated | Net Executable Cases |
|---|---:|---:|---:|
| **AI-Generated Artifacts** | 37 | 2 (`FR02-AI-016`, `FR02-AI-017`) | **35** |
| **Student-Selected Human Extensions** | 5 | 0 | **5** |
| **TOTAL** | **42** | **2** | **40** |

---

## 2. Excluded Raw Cases Log

- **`FR02-AI-016` (Duplicate of `FR02-AI-013`):** Evaluated consecutive failure $N=2$ using BVA vs State Transition labels. Excluded from executable execution to prevent redundant test steps; canonical $N=2$ test is executed via `FR02-AI-013`.
- **`FR02-AI-017` (Duplicate of `FR02-AI-014`):** Evaluated lockout threshold $N=3$. Excluded from executable execution; canonical $N=3$ threshold test is executed via `FR02-AI-014`.

---

## 3. Executable Test Case Specifications (40 Cases)

### TC-FR02-AI-001: Valid User Login with Registered Credentials

- **Test Case ID:** `FR02-AI-001`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Valid User Login with Registered Credentials
- **Technique:** Equivalence Partitioning (EP-EM-01 + EP-PW-01)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2]
- **Preconditions:** User `test@eshop.com` is registered with password `Test1234!` and account is in `NORMAL` state (unlocked, attempts=0).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 200 OK``
- **Expected Semantic Result:** JSON object containing:
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** The case matches the documented successful login contract. The API specification defines POST /api/login with valid credentials as HTTP 200 and returns a JWT token together with user information. The test is a valid baseline positive authentication case.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-002: Valid Admin Login with Registered Admin Credentials

- **Test Case ID:** `FR02-AI-002`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Valid Admin Login with Registered Admin Credentials
- **Technique:** Equivalence Partitioning (EP-EM-01 + EP-PW-01)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2]
- **Preconditions:** Admin `admin@eshop.com` is registered with password `Admin123!` and account is unlocked.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 200 OK``
- **Expected Semantic Result:** JSON object containing non-empty JWT `token` and `user` object with `role: "admin"`.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** A registered admin account is still authenticated through the same POST /api/login endpoint. The expected 200 response, JWT issuance, and returned user information are consistent with the login contract. Verifying that the returned user information preserves role="admin" is reasonable for the seeded admin account.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-003: Login Rejection on Registered Email with Incorrect Password

- **Test Case ID:** `FR02-AI-003`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Login Rejection on Registered Email with Incorrect Password
- **Technique:** Equivalence Partitioning (EP-EM-01 + EP-PW-02)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `test@eshop.com` exists and is unlocked (attempts=0).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 401 Unauthorized` (or 4xx generic error)`
- **Expected Semantic Result:** Generic error message (e.g. `"Invalid email or password"`) without disclosing whether email or password was the cause.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** FR-02 explicitly requires failed authentication for incorrect credentials, a generic error that does not disclose whether the email or password was wrong, and an increment of exactly one failed attempt. This case correctly represents the first failed attempt while the account remains unlocked.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-004: Login Rejection on Unregistered Syntactically Valid Email

- **Test Case ID:** `FR02-AI-004`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Login Rejection on Unregistered Syntactically Valid Email
- **Technique:** Equivalence Partitioning (EP-EM-02 + EP-PW-01)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Email `nonexistent_user_999@eshop.com` is not registered in the system.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 401 Unauthorized` (or 4xx generic error)`
- **Expected Semantic Result:** Generic error message identical to wrong-password response (prevents account enumeration).
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** An unregistered email must not authenticate, and FR-02 requires authentication errors not to reveal whether the email or password was incorrect. Comparing this response semantics with the wrong-password case is therefore consistent with the anti-enumeration requirement.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-005: Login Rejection on Malformed Email Syntax Missing At-Symbol

- **Test Case ID:** `FR02-AI-005`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Login Rejection on Malformed Email Syntax Missing At-Symbol
- **Technique:** Equivalence Partitioning / Negative (EP-EM-03 + EP-PW-01)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** None.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `4xx (NOT SPECIFIED in API Spec; e.g. 400 Bad Request or 401 Unauthorized)`
- **Expected Semantic Result:** Error response; authentication must strictly not succeed.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL / SPEC-UNDEFINED`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Keep the test input, but remove the claim that malformed-email rejection is a mandatory syntax-validation rule. Expected result should be: authentication must not succeed and no JWT must be issued; exact HTTP status and validation message are NOT SPECIFIED.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-006: Login Rejection on Empty String Email Field

- **Test Case ID:** `FR02-AI-006`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Login Rejection on Empty String Email Field
- **Technique:** Equivalence Partitioning / Negative (EP-EM-04 + EP-PW-01)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** None.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `4xx (NOT SPECIFIED in API Spec; e.g. 400 Bad Request or 401 Unauthorized)`
- **Expected Semantic Result:** Error response; authentication must strictly not succeed.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL / SPEC-UNDEFINED`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Keep email="" as the test input. Assert only that the request must not produce successful authentication or a JWT. Mark exact status, validation message, and processing path as NOT SPECIFIED.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-007: Login Rejection on Missing Email Property in Request Body

- **Test Case ID:** `FR02-AI-007`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Login Rejection on Missing Email Property in Request Body
- **Technique:** Equivalence Partitioning / Negative (EP-EM-05 + EP-PW-01)
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** None.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `4xx (NOT SPECIFIED in API Spec; e.g. 400 Bad Request or 401 Unauthorized)`
- **Expected Semantic Result:** Error response indicating invalid/incomplete payload; authentication must not succeed.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL / SPEC-UNDEFINED`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Keep the missing-email test. Expected semantic result should be authentication must not succeed and no JWT should be issued. Leave exact HTTP status and error-message structure as NOT SPECIFIED unless api_specification.md explicitly defines them.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-008: Login Rejection on Null Email Value in Request Body

- **Test Case ID:** `FR02-AI-008`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Login Rejection on Null Email Value in Request Body
- **Technique:** Equivalence Partitioning / Negative (EP-EM-06 + EP-PW-01)
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** None.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `4xx (NOT SPECIFIED in API Spec; e.g. 400 Bad Request or 401 Unauthorized)`
- **Expected Semantic Result:** Error response; server must not crash or return unhandled 500 error.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL / SPEC-UNDEFINED`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Retain email=null as an exploratory negative test. Assert that authentication must not succeed; mark exact status, null validation behavior, error schema, and state effects as NOT SPECIFIED. Treat the no-500 expectation as an engineering robustness expectation rather than a formal FR-02 oracle.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-009: Login Rejection on Whitespace-Only Email Input

- **Test Case ID:** `FR02-AI-009`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Login Rejection on Whitespace-Only Email Input
- **Technique:** Equivalence Partitioning / Negative (EP-EM-07 + EP-PW-01)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** None.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``NOT SPECIFIED` (HTTP 400 or 401)`
- **Expected Semantic Result:** Rejection notice; authentication must not succeed.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``PARTIAL``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Keep the whitespace-only input as exploratory/domain coverage. Assert only that it must not result in successful authentication for the tested account. Do not require trimming or a specific blank-field error; exact behavior remains SPEC-UNDEFINED.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-010: Login Rejection on Empty String Password Field

- **Test Case ID:** `FR02-AI-010`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Login Rejection on Empty String Password Field
- **Technique:** Equivalence Partitioning / Negative (EP-EM-01 + EP-PW-03)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** User `test@eshop.com` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `4xx (NOT SPECIFIED in API Spec; e.g. 400 Bad Request or 401 Unauthorized)`
- **Expected Semantic Result:** Rejection notice; authentication must not succeed.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL / SPEC-UNDEFINED`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Keep password="" and assert authentication failure with no JWT. Set exact HTTP status to NOT SPECIFIED unless documented. Set State After / failure-counter effect to NOT SPECIFIED rather than "FAILURE_SEQUENCE_ACTIVE or unchanged".
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-011: Login Rejection on Missing Password Property in Request Body

- **Test Case ID:** `FR02-AI-011`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Login Rejection on Missing Password Property in Request Body
- **Technique:** Equivalence Partitioning / Negative (EP-EM-01 + EP-PW-04)
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** User `test@eshop.com` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `4xx (NOT SPECIFIED in API Spec; e.g. 400 Bad Request or 401 Unauthorized)`
- **Expected Semantic Result:** Error response; authentication must strictly not succeed.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL / SPEC-UNDEFINED`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Keep the missing-password input. Assert only that authentication must not succeed and no JWT must be issued. Mark exact HTTP status, error schema, and failure-counter/state effect as NOT SPECIFIED.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-012: Login Rejection on Null Password Value in Request Body

- **Test Case ID:** `FR02-AI-012`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Login Rejection on Null Password Value in Request Body
- **Technique:** Equivalence Partitioning / Negative (EP-EM-01 + EP-PW-05)
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** User `test@eshop.com` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `4xx (NOT SPECIFIED in API Spec; e.g. 400 Bad Request or 401 Unauthorized)`
- **Expected Semantic Result:** Error response; server must not crash or return unhandled 500 error.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL / SPEC-UNDEFINED`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Keep password=null as an exploratory negative input. Assert authentication non-success and no JWT. Mark exact status, null-validation behavior, error schema, and counter/state effect as NOT SPECIFIED.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-013: Consecutive Failure Progression at Boundary N=2 (Remains Unlocked)

- **Test Case ID:** `FR02-AI-013`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Consecutive Failure Progression at Boundary N=2 (Remains Unlocked)
- **Technique:** Boundary Value Analysis (BVA $N=2$)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test user `lockout-test@eshop.com` has experienced exactly 1 prior failed login (attempts=1, state is `FAILURE_SEQUENCE_ACTIVE`).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 401 Unauthorized` (or 4xx generic credential error)`
- **Expected Semantic Result:** Generic credential failure message; account must **remain UNLOCKED** (subsequent login attempts still processed).
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** FR-02 explicitly locks the account after 3 or more consecutive failed logins. Therefore after the second consecutive failure the account must still remain unlocked. This is a valid N-1 boundary-value test.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-014: Consecutive Failure Threshold at Boundary N=3 (Account Transitions to Locked)

- **Test Case ID:** `FR02-AI-014`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Consecutive Failure Threshold at Boundary N=3 (Account Transitions to Locked)
- **Technique:** Boundary Value Analysis (BVA $N=3$)
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test user `lockout-test@eshop.com` has experienced exactly 2 prior failed logins (attempts=2, state is `FAILURE_SEQUENCE_ACTIVE`).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``NOT SPECIFIED` on request #3 (HTTP 401 or HTTP 403)`
- **Expected Semantic Result:** Authentication rejected; account state **transitions to LOCKED**. Any subsequent request during the 30-second lockout window must be rejected with a temporary lockout notice.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``PARTIAL` (State transition is EXPLICIT; exact HTTP code of request #3 is NOT SPECIFIED)`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** FR-02 explicitly defines the lockout threshold at 3 consecutive failed logins. This case correctly verifies the N=3 boundary and transition into the temporary LOCKED state while correctly leaving the exact HTTP status of request #3 unspecified.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-015: First Consecutive Failed Login Attempt (Normal to Failure Sequence Active, Not Locked)

- **Test Case ID:** `FR02-AI-015`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** First Consecutive Failed Login Attempt (Normal to Failure Sequence Active, Not Locked)
- **Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` exists in `NORMAL` baseline state (attempts=0, unlocked).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 401 Unauthorized` (or 4xx generic credential error)`
- **Expected Semantic Result:** Generic error message (e.g. `"Invalid email or password"`); account must **remain UNLOCKED** and immediately accept subsequent login attempts for credential evaluation.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** This case verifies the first observable transition in the failure sequence. Since the lockout threshold is 3 consecutive failures, the account must remain unlocked after failure #1 and accept subsequent authentication attempts.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-018: Login Rejection on Subsequent Request During Active Lockout Window (Wrong Credentials)

- **Test Case ID:** `FR02-AI-018`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Login Rejection on Subsequent Request During Active Lockout Window (Wrong Credentials)
- **Technique:** STATE TRANSITION / NEGATIVE
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` has triggered lockout ($N=3$ consecutive failures) and is currently within the active 30-second lockout window ($T < 30\text{s}$).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``NOT SPECIFIED` (HTTP 403 Forbidden / 429 Too Many Requests / 4xx)`
- **Expected Semantic Result:** Error notice indicating account is temporarily locked without disclosing internal variables or stack traces.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``PARTIAL``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Keep the active-lock wrong-credentials scenario. Assert temporary-lock rejection, no successful authentication, and LOCKED state. Leave exact status unspecified. Treat stack-trace/debug-data non-disclosure separately as an additional security/robustness assertion unless explicitly supported by the specification.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-019: Login Rejection on Subsequent Request During Active Lockout Window (Correct Credentials Do Not Bypass Lock)

- **Test Case ID:** `FR02-AI-019`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Login Rejection on Subsequent Request During Active Lockout Window (Correct Credentials Do Not Bypass Lock)
- **Technique:** STATE TRANSITION / NEGATIVE / SECURITY
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` has triggered lockout ($N=3$ consecutive failures) and is currently within the active 30-second lockout window ($T < 30\text{s}$). Registered password is `LockoutPass123!`.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``NOT SPECIFIED` (HTTP 403 Forbidden / 429 / 4xx)`
- **Expected Semantic Result:** Error notice indicating account is temporarily locked; authentication must strictly NOT succeed and NO JWT token must be issued.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT` (Semantic rule that locked account cannot authenticate is explicit)`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** An account in an active temporary lockout state must not authenticate before the 30-second window expires. Therefore even correct credentials cannot bypass the lock, and a successful JWT must not be issued. The case correctly leaves the exact 4xx status unspecified.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-020: Lockout Duration Timing Boundary Check Prior to Expiration (T=25s in 30s Window)

- **Test Case ID:** `FR02-AI-020`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Lockout Duration Timing Boundary Check Prior to Expiration (T=25s in 30s Window)
- **Technique:** BVA / STATE TRANSITION
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` entered `LOCKED` state at $T_0$. Exactly 25 seconds have elapsed ($T_0 + 25\text{s} < T_0 + 30\text{s}$).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``NOT SPECIFIED` (HTTP 403 / 429 / 4xx)`
- **Expected Semantic Result:** Rejection with temporary lockout notice; authentication must not succeed.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``PARTIAL``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** FR-02 explicitly defines a 30-second lockout duration. Testing at T+25s gives a safely pre-expiration boundary point, so the account must still be locked and valid credentials must not authenticate. The case correctly avoids asserting an undocumented exact 4xx status.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-021: Lockout Duration Expiration Boundary Check After 30s Window (T=32s Auto-Unlock)

- **Test Case ID:** `FR02-AI-021`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Lockout Duration Expiration Boundary Check After 30s Window (T=32s Auto-Unlock)
- **Technique:** BVA / STATE TRANSITION
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` entered `LOCKED` state at $T_0$. More than 30 seconds have elapsed ($T_0 + 32\text{s} > T_0 + 30\text{s}$).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 200 OK``
- **Expected Semantic Result:** Successful login response returning valid JWT `token` and `user` object.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** FR-02 explicitly defines a temporary lockout duration of 30 seconds. At T+32s the lockout interval has expired, so submitting valid credentials must be processed normally and successful authentication should return the documented 200 response and JWT.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-022: Successful Authentication Resets Consecutive Failure Progression

- **Test Case ID:** `FR02-AI-022`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Successful Authentication Resets Consecutive Failure Progression
- **Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` in `NORMAL` state.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `- Step 1: `HTTP 401 Unauthorized``
- **Expected Semantic Result:** At Step 3, account must **remain UNLOCKED** (treated as 1st failure of a new sequence, not 2nd cumulative failure).
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** FR-02 explicitly states that a successful login resets the consecutive failed-login counter to 0. The wrong -> success -> wrong sequence correctly verifies that the failure after success belongs to a new consecutive-failure sequence and must not prematurely lock the account.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-023: Consecutive Failure Semantics Verification (Non-Consecutive Failures Do Not Trigger Lockout)

- **Test Case ID:** `FR02-AI-023`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Consecutive Failure Semantics Verification (Non-Consecutive Failures Do Not Trigger Lockout)
- **Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` in `NORMAL` state.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `- Step 1: `HTTP 401 Unauthorized``
- **Expected Semantic Result:** At Step 4, total lifetime failures in session is 3, but consecutive failures in active sequence is only 2. Account must **remain UNLOCKED**.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** The lockout rule is based on consecutive failed logins. Because a successful authentication resets the failure sequence, the sequence wrong -> success -> wrong -> wrong contains only two consecutive failures after the reset and therefore must not trigger lockout.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-024: Post-Lockout Expiration Account Usability and Failure Sequence Reset

- **Test Case ID:** `FR02-AI-024`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Post-Lockout Expiration Account Usability and Failure Sequence Reset
- **Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` underwent full lockout ($N=3$), waited 32s until lock expired, and performed 1 successful login (200 OK).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 401 Unauthorized``
- **Expected Semantic Result:** Generic credential error; account must **remain UNLOCKED** (behaving as attempt=1 of a fresh lifecycle).
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Although lock expiry by itself does not necessarily specify the internal counter state, this test's precondition explicitly includes a successful login after the 30-second lockout has expired. FR-02 explicitly states that successful authentication resets the failure counter to 0. Therefore the following wrong password is correctly treated as the first failure of a fresh sequence.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-025: SQL Injection Behavioral Probe in Email Field

- **Test Case ID:** `FR02-AI-025`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** SQL Injection Behavioral Probe in Email Field
- **Technique:** INJECTION PROBE / SECURITY (SEC-05)
- **Requirement / Oracle Basis:** 📋 [SRS §9 SEC-05]
- **Preconditions:** None.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 401 Unauthorized` (or 4xx generic error; strictly NOT 200 OK, NOT 500 Internal Server Error)`
- **Expected Semantic Result:** JSON response
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL BLACK-BOX EVIDENCE (SEC-05)`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Keep the SQLi email probe and assert that the payload must not bypass authentication or create an unauthorized session. Classify the result as PARTIAL BLACK-BOX EVIDENCE for SEC-05. Do not claim that a passing result proves parameterized queries; supplement with source/DB verification where permitted.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-026: SQL Injection Behavioral Probe in Password Field

- **Test Case ID:** `FR02-AI-026`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** SQL Injection Behavioral Probe in Password Field
- **Technique:** INJECTION PROBE / SECURITY (SEC-05)
- **Requirement / Oracle Basis:** 📋 [SRS §9 SEC-05]
- **Preconditions:** Registered user `admin@eshop.com` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 401 Unauthorized` (or 4xx generic error; strictly NOT 200 OK, NOT 500)`
- **Expected Semantic Result:** JSON response
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL BLACK-BOX EVIDENCE (SEC-05)`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Retain the password SQLi probe and assert no authentication bypass or unauthorized token issuance. Keep SEC-05 classification as PARTIAL BLACK-BOX EVIDENCE and document that parameterization requires supplemental implementation verification.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-027: Cross-Response Generic Credential Error Equivalence (Anti-Enumeration)

- **Test Case ID:** `FR02-AI-027`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** Cross-Response Generic Credential Error Equivalence (Anti-Enumeration)
- **Technique:** INFORMATION DISCLOSURE / SECURITY
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02] ("không để lộ chi tiết nguyên nhân")
- **Preconditions:** User `test@eshop.com` exists; user `nonexistent_audit_user@eshop.com` does not exist.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `- Step 1: `HTTP 401 Unauthorized` (or 4xx)`
- **Expected Semantic Result:** JSON response
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** FR-02 explicitly requires authentication errors not to disclose whether the email or password was incorrect. Comparing the registered-email/wrong-password response against the unregistered-email response is a direct observable test of this non-disclosure requirement.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-028: Sensitive Credential Exposure Probe in Successful Login Response

- **Test Case ID:** `FR02-AI-028`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Sensitive Credential Exposure Probe in Successful Login Response
- **Technique:** SECURITY / SENSITIVE DATA EXPOSURE
- **Requirement / Oracle Basis:** 📋 [SRS §9 SEC-01] & Clean Credential Handling
- **Preconditions:** Registered user `test@eshop.com` with password `Test1234!` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 200 OK``
- **Expected Semantic Result:** JSON response
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `ADDITIONAL-SEC (Response Sanitization)`
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Retain the response-sanitization assertion as [ADDITIONAL-SEC] Sensitive Data Exposure. Remove SEC-01 compliance as the primary oracle. State separately that SEC-01 storage-at-rest compliance requires supplemental database/source verification.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-029: Token Omission Assertion on Failed Authentication

- **Test Case ID:** `FR02-AI-029`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Token Omission Assertion on Failed Authentication
- **Technique:** SECURITY / AUTHENTICATION
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 401 Unauthorized` (or 4xx)`
- **Expected Semantic Result:** JSON response
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** Change the oracle to: failed authentication must not issue any usable authentication token or authorization capability. Do not require a specific token-field omission/null representation unless api_specification.md explicitly defines it.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-030: SEC-02 Supporting Token Usability Verification on Protected Endpoint

- **Test Case ID:** `FR02-AI-030`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** SEC-02 Supporting Token Usability Verification on Protected Endpoint
- **Technique:** SECURITY / AUTHENTICATION / SEQUENCE TESTING
- **Requirement / Oracle Basis:** 📋 [SRS §9 SEC-02] & 📋 [SRS §2 FR-02]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `- Step 1: `HTTP 200 OK``
- **Expected Semantic Result:** JSON response
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``PARTIAL``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** FR-02 issues the JWT and the specification states that the returned token is used as Authorization: Bearer <token> on subsequent authenticated APIs. Using one documented protected endpoint to verify that the issued token is usable is a legitimate supporting/indirect FR-02 integration test. The case correctly identifies that SEC-02 enforcement primarily belongs to the downstream protected endpoint.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-031: SEC-02 Supporting Tampered Signature Rejection on Protected Endpoint

- **Test Case ID:** `FR02-AI-031`
- **Source:** `AI-derived`
- **Audit Status:** `VALID`
- **Title:** SEC-02 Supporting Tampered Signature Rejection on Protected Endpoint
- **Technique:** SECURITY / SIGNATURE INTEGRITY / SEQUENCE TESTING
- **Requirement / Oracle Basis:** 📋 [SRS §9 SEC-02] & 📋 [SRS §2 FR-02]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `- Step 1: `HTTP 200 OK``
- **Expected Semantic Result:** JSON response
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** None
- **Human Audit Rationale / Corrections:** SEC-02 requires security-sensitive APIs to accept only a valid JWT. A token whose payload/signature has been tampered with is no longer valid, so a documented protected endpoint must reject it. This is acceptable as supporting/indirect FR-02 integration coverage because FR-02 is the token issuer and the protected endpoint is the token consumer.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-032: Successful Login Response Schema and Data Type Contract

- **Test Case ID:** `FR02-AI-032`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Successful Login Response Schema and Data Type Contract
- **Technique:** SCHEMA VALIDATION / API CONTRACT
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2] & 📋 [SRS §2 FR-02]
- **Preconditions:** Active registered user `test@eshop.com` with password `Test1234!` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 200 OK``
- **Expected Semantic Result:** Top-level JSON object strictly containing documented contract attributes.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** `api_specification.md` Section 1.2 provides explicit example structure for success response.
- **Human Audit Rationale / Corrections:** Retain schema validation for fields and types explicitly documented by API-SPEC. Remove or mark as PARTIAL any constraints that are inferred from examples or JWT conventions rather than explicitly specified.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-033: Invalid Credentials Error Response Schema and Structure Contract

- **Test Case ID:** `FR02-AI-033`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Invalid Credentials Error Response Schema and Structure Contract
- **Technique:** SCHEMA VALIDATION / ERROR CONTRACT
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2] & 📋 [SRS §2 FR-02]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 401 Unauthorized` (or 4xx error)`
- **Expected Semantic Result:** Valid JSON error object.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** API specification provides error description; exact error key name (`error` vs `message`) is evaluated flexibly across standard REST conventions.
- **Human Audit Rationale / Corrections:** Keep the generic error-contract check. Do not require a particular error key or exact omission representation unless explicitly documented. Assert that authentication fails and no usable authentication token is issued.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-034: Locked-Account Error Response Contract and Internal Non-Disclosure

- **Test Case ID:** `FR02-AI-034`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Locked-Account Error Response Contract and Internal Non-Disclosure
- **Technique:** SCHEMA VALIDATION / ERROR CONTRACT
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02] ("thông báo tạm khóa... không để lộ chi tiết")
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` is in `LOCKED` state.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``NOT SPECIFIED` (HTTP 403 Forbidden / 429 / 4xx)`
- **Expected Semantic Result:** Valid JSON error object informing of temporary lockout.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``PARTIAL``
- **Specification Limitations:** Exact status code and field name are unspecified in SRS; non-disclosure and error structure are specification-backed.
- **Human Audit Rationale / Corrections:** Retain the temporary-lockout error response and generic non-disclosure assertion. Leave exact status and field name unspecified, and treat stack trace/database/internal-variable leakage checks as additional security/robustness assertions rather than the formal FR-02 oracle.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-035: Syntactically Malformed JSON Request Body Transport Contract

- **Test Case ID:** `FR02-AI-035`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Syntactically Malformed JSON Request Body Transport Contract
- **Technique:** NEGATIVE CONTRACT / PARSER RESILIENCE
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2] & Transport Robustness
- **Preconditions:** None.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``NOT SPECIFIED` (HTTP 400 Bad Request or 4xx; strictly NOT 200 OK, NOT 500 Internal Server Error)`
- **Expected Semantic Result:** Client error response; server parser must handle malformed JSON cleanly without unhandled runtime crash or HTML stack trace leakage.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``PARTIAL``
- **Specification Limitations:** Transport parser error codes are not explicitly documented in the business API spec.
- **Human Audit Rationale / Corrections:** Retain this as an exploratory transport robustness test. Assert only that malformed input must not result in successful authentication or issuance of a usable JWT. Treat exact status, parser error schema, and no-500 behavior as engineering expectations unless separately documented.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-036: Response Content-Type Header Contract Across Status Codes

- **Test Case ID:** `FR02-AI-036`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Response Content-Type Header Contract Across Status Codes
- **Technique:** API CONTRACT / HEADER VALIDATION
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** `- Step 1: `HTTP 200 OK``
- **Expected Semantic Result:** - Both Step 1 and Step 2 HTTP responses must include the header `Content-Type: application/json` (or `application/json; charset=utf-8`).
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``EXPLICIT``
- **Specification Limitations:** Standard REST JSON contract documented across `api_specification.md`.
- **Human Audit Rationale / Corrections:** Keep Content-Type validation only as a PARTIAL or exploratory API-contract check unless the exact JSON response Content-Type is explicitly documented. Do not classify it as EXPLICIT solely because the API uses JSON.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-AI-037: Extraneous Request Body Properties Ingestion Contract

- **Test Case ID:** `FR02-AI-037`
- **Source:** `AI-derived`
- **Audit Status:** `CORRECTED FROM INCOMPLETE`
- **Title:** Extraneous Request Body Properties Ingestion Contract
- **Technique:** API CONTRACT / EXPLORATORY SCHEMA
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2] & Schema Robustness
- **Preconditions:** Registered standard user `test@eshop.com` exists (role is `"user"`).
- **Setup Requirements:** N/A
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** POST /api/login
- **Expected HTTP Status:** ``HTTP 200 OK` (or 400 if strict schema validation is enforced)`
- **Expected Semantic Result:** If login succeeds, the issued JWT and `user` object must reflect the actual database role (`"user"`), and injected extraneous fields must be ignored.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** ``PARTIAL``
- **Specification Limitations:** API specification does not mandate whether extraneous fields are rejected with 400 or silently ignored; privilege non-escalation is mandatory.
- **Human Audit Rationale / Corrections:** Retain the test as an exploratory/additional-security parameter-injection case. Do not require either silent ignoring or HTTP 400. Assert only that the supplied role field cannot alter the authenticated account's real authorization role.
- **Postman Assertion Plan:** Assert response

---

### TC-FR02-HUM-001: HTTP Verb / Method Enforcement Rejection on Login Route

- **Test Case ID:** `FR02-HUM-001`
- **Source:** `Human Extension`
- **Audit Status:** `HUMAN EXTENSION`
- **Title:** HTTP Verb / Method Enforcement Rejection on Login Route
- **Technique:** API CONTRACT / METHOD ENFORCEMENT
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2] (Specifies POST /api/login)
- **Preconditions:** Registered user exists.
- **Setup Requirements:** None required.
- **Request Method / Sequence:** `GET`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** Dispatch HTTP GET to /api/login.
- **Expected HTTP Status:** `4xx (404 Not Found or 405 Method Not Allowed; NOT SPECIFIED in API Spec)`
- **Expected Semantic Result:** Authentication logic does not execute, no JWT token issued.
- **Expected State After:** `NORMAL (Unchanged)`
- **Oracle Confidence:** `PARTIAL (API Contract)`
- **Specification Limitations:** Exact status code is not explicitly defined in api_specification.md.
- **Human Audit Rationale / Corrections:** Student-selected to test unsupported HTTP method enforcement on the login route.
- **Postman Assertion Plan:** Send GET request; assert status is 4xx, code is not 200, and response body contains no token.

---

### TC-FR02-HUM-002: Advanced SQL Injection Multi-Vector Resilience Probe (Comment & Stacked Vector)

- **Test Case ID:** `FR02-HUM-002`
- **Source:** `Human Extension`
- **Audit Status:** `HUMAN EXTENSION`
- **Title:** Advanced SQL Injection Multi-Vector Resilience Probe (Comment & Stacked Vector)
- **Technique:** SECURITY / BEHAVIORAL INJECTION PROBE
- **Requirement / Oracle Basis:** 📋 [SRS §9 SEC-05] (Parameterized queries required)
- **Preconditions:** Admin account exists in database.
- **Setup Requirements:** None required.
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** Submit login payload with comment-truncation vector in email field (admin@eshop.com'--).
- **Expected HTTP Status:** `4xx (400 Bad Request or 401 Unauthorized; NOT SPECIFIED)`
- **Expected Semantic Result:** Authentication fails; no unauthorized JWT issued, no database error disclosure.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL BLACK-BOX EVIDENCE (SEC-05)`
- **Specification Limitations:** Black-box testing cannot prove parameterized queries across all backend paths.
- **Human Audit Rationale / Corrections:** Student-selected to probe multi-character comment truncation SQL injection vectors.
- **Postman Assertion Plan:** Send POST with payload; assert status is 4xx, token is undefined, and no SQL exception traces exist.

---

### TC-FR02-HUM-003: Consecutive Failure Counter Reset at N=2 Pre-Lockout Boundary via Successful Login

- **Test Case ID:** `FR02-HUM-003`
- **Source:** `Human Extension`
- **Audit Status:** `HUMAN EXTENSION`
- **Title:** Consecutive Failure Counter Reset at N=2 Pre-Lockout Boundary via Successful Login
- **Technique:** STATE TRANSITION / BOUNDARY RESET TESTING
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02] (Successful login resets consecutive failure counter to 0)
- **Preconditions:** Dedicated account reset_fr02@eshop.com in NORMAL state.
- **Setup Requirements:** Provision fresh reset account via setup helper.
- **Request Method / Sequence:** `POST (Sequence: 2 Wrong -> 1 Valid -> 1 Wrong)`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** Execute 2 failed logins, 1 valid login, and 1 failed login.
- **Expected HTTP Status:** `Sequence: 4xx, 4xx, 200 OK, 4xx`
- **Expected Semantic Result:** Valid login on attempt 3 succeeds (200 OK + JWT) and resets counter; attempt 4 fails but does NOT trigger lockout.
- **Expected State After:** `FAILURE_SEQUENCE_ACTIVE (Count = 1, NOT LOCKED)`
- **Oracle Confidence:** `EXPLICIT`
- **Specification Limitations:** Verified via externally observable authentication states without internal DB counter inspection.
- **Human Audit Rationale / Corrections:** Student-selected to test counter reset specifically at the critical (N-1) pre-lockout boundary.
- **Postman Assertion Plan:** Execute sequence; assert attempt 3 returns 200 OK + JWT and attempt 4 fails without lockout.

---

### TC-FR02-HUM-004: Account Lockout State Isolation Between Independent User Accounts

- **Test Case ID:** `FR02-HUM-004`
- **Source:** `Human Extension`
- **Audit Status:** `HUMAN EXTENSION`
- **Title:** Account Lockout State Isolation Between Independent User Accounts
- **Technique:** SECURITY / STATE ISOLATION TESTING
- **Requirement / Oracle Basis:** 📋 [SRS §2 FR-02] (Lockout applies to the specific account experiencing failures)
- **Preconditions:** Account A (victim_fr02@eshop.com) and Account B (isolated_fr02@eshop.com) exist in NORMAL state.
- **Setup Requirements:** Provision Account A and Account B via setup helper.
- **Request Method / Sequence:** `POST (Sequence: 3 Failures on A -> 1 Valid on B)`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** Trigger lockout on Account A (3 failures); immediately submit valid credentials for Account B.
- **Expected HTTP Status:** `Account A: 4xx (Lockout error), Account B: 200 OK`
- **Expected Semantic Result:** Account A is locked for 30s; Account B authenticates normally without being affected by Account A's lockout.
- **Expected State After:** `Account A: LOCKED, Account B: NORMAL`
- **Oracle Confidence:** `PARTIALLY SPECIFICATION-BACKED / STATE ISOLATION`
- **Specification Limitations:** Cross-account state isolation is inferred from per-user authentication architecture.
- **Human Audit Rationale / Corrections:** Student-selected to verify that lockout state is strictly isolated per account.
- **Postman Assertion Plan:** Assert Account A receives lockout error on 4th request; assert Account B receives 200 OK with valid JWT.

---

### TC-FR02-HUM-005: Non-JSON Content-Type Request Contract Handling (application/x-www-form-urlencoded)

- **Test Case ID:** `FR02-HUM-005`
- **Source:** `Human Extension`
- **Audit Status:** `HUMAN EXTENSION`
- **Title:** Non-JSON Content-Type Request Contract Handling (application/x-www-form-urlencoded)
- **Technique:** EXPLORATORY / API CONTRACT
- **Requirement / Oracle Basis:** 🗂️ [API-SPEC §1.2] (Documents JSON API communication)
- **Preconditions:** Registered user exists.
- **Setup Requirements:** None required.
- **Request Method / Sequence:** `POST`
- **Endpoint:** `/api/login`
- **Request / Action Sequence:** Submit valid credentials formatted as form-urlencoded string with Content-Type: application/x-www-form-urlencoded.
- **Expected HTTP Status:** `4xx (400 Bad Request, 415 Unsupported Media Type, or 401 Unauthorized; NOT SPECIFIED)`
- **Expected Semantic Result:** Server must not create an unintended authenticated session or crash with unhandled 500 error.
- **Expected State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL (Exploratory / API Contract)`
- **Specification Limitations:** Exact status code for non-JSON MIME is not specified in API spec.
- **Human Audit Rationale / Corrections:** Student-selected to test transport contract when non-JSON Content-Type is supplied.
- **Postman Assertion Plan:** Send urlencoded request; assert status is 4xx and server does not return 500.
