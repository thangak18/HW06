# FR-02 AI-Generated Test Case Draft

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Cumulative Generation Target:** $\ge 35\text{ AI-generated test cases}$ (across Stages 1A.2, 1A.3, 1A.4, 1A.5)

---

## Generation Summary Tracker

| Stage | Sub-Suite Description | ID Range | Generated Count | Status |
|:---:|---|:---:|---:|:---:|
| **Stage 1A.2** | Domain Partitions & Boundary Cases | `FR02-AI-001` .. `FR02-AI-014` | 14 | **GENERATED** |
| **Stage 1A.3** | Lockout State Machine & Timing | `FR02-AI-015` .. `FR02-AI-024` | 10 | **GENERATED** |
| **Stage 1A.4** | Security Probes & Token Usability | `FR02-AI-025` .. `FR02-AI-031` | 7 | **GENERATED** |
| **Stage 1A.5** | Schema Validation & Error Contracts | `FR02-AI-032` .. `FR02-AI-037` | 6 | **GENERATED** |
| **TOTAL** | **Full AI-Generated Inventory** | `FR02-AI-001` .. `FR02-AI-037` | **37** | **Complete ($\ge 35$ Target Reached)** |

---

## Stage 1A.2 – Domain and Boundary Cases

### TC-FR02-AI-001: Valid User Login with Registered Credentials
- **Test Case ID:** `FR02-AI-001`
- **Title:** Valid User Login with Registered Credentials
- **Technique:** Equivalence Partitioning (EP-EM-01 + EP-PW-01)
- **Requirement:** 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2]
- **Preconditions:** User `test@eshop.com` is registered with password `Test1234!` and account is in `NORMAL` state (unlocked, attempts=0).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com",
    "password": "Test1234!"
  }
  ```
- **State Before:** `NORMAL`
- **Action:** Send login request with matching valid credentials.
- **Expected HTTP Status:** `HTTP 200 OK`
- **Expected Response:** JSON object containing:
  - `token`: non-empty JWT string
  - `user`: object with user profile details (`id`, `name`, `email`, `role`)
  - `message`: string indicating login success
- **State After:** `NORMAL` (attempts=0)
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Baseline positive authentication scenario.

---

### TC-FR02-AI-002: Valid Admin Login with Registered Admin Credentials
- **Test Case ID:** `FR02-AI-002`
- **Title:** Valid Admin Login with Registered Admin Credentials
- **Technique:** Equivalence Partitioning (EP-EM-01 + EP-PW-01)
- **Requirement:** 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2]
- **Preconditions:** Admin `admin@eshop.com` is registered with password `Admin123!` and account is unlocked.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "admin@eshop.com",
    "password": "Admin123!"
  }
  ```
- **State Before:** `NORMAL`
- **Action:** Send login request with admin credentials.
- **Expected HTTP Status:** `HTTP 200 OK`
- **Expected Response:** JSON object containing non-empty JWT `token` and `user` object with `role: "admin"`.
- **State After:** `NORMAL`
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Admin authentication path generating admin-scoped JWT.

---

### TC-FR02-AI-003: Login Rejection on Registered Email with Incorrect Password
- **Test Case ID:** `FR02-AI-003`
- **Title:** Login Rejection on Registered Email with Incorrect Password
- **Technique:** Equivalence Partitioning (EP-EM-01 + EP-PW-02)
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `test@eshop.com` exists and is unlocked (attempts=0).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com",
    "password": "WrongPassword999!"
  }
  ```
- **State Before:** `NORMAL` (attempts=0)
- **Action:** Submit incorrect password for registered user.
- **Expected HTTP Status:** `HTTP 401 Unauthorized` (or 4xx generic error)
- **Expected Response:** Generic error message (e.g. `"Invalid email or password"`) without disclosing whether email or password was the cause.
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (attempts=1, unlocked)
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Verifies failure counter increment and generic error non-disclosure.

---

### TC-FR02-AI-004: Login Rejection on Unregistered Syntactically Valid Email
- **Test Case ID:** `FR02-AI-004`
- **Title:** Login Rejection on Unregistered Syntactically Valid Email
- **Technique:** Equivalence Partitioning (EP-EM-02 + EP-PW-01)
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Email `nonexistent_user_999@eshop.com` is not registered in the system.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "nonexistent_user_999@eshop.com",
    "password": "Password123!"
  }
  ```
- **State Before:** N/A (non-existent account)
- **Action:** Attempt login with unregistered email.
- **Expected HTTP Status:** `HTTP 401 Unauthorized` (or 4xx generic error)
- **Expected Response:** Generic error message identical to wrong-password response (prevents account enumeration).
- **State After:** N/A
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Anti-enumeration oracle test.

---

### TC-FR02-AI-005: Login Rejection on Malformed Email Syntax Missing At-Symbol
- **Test Case ID:** `FR02-AI-005`
- **Title:** Login Rejection on Malformed Email Syntax Missing At-Symbol
- **Technique:** Equivalence Partitioning / Negative (EP-EM-03 + EP-PW-01)
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** None.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "invalidemailformat.eshop.com",
    "password": "Password123!"
  }
  ```
- **State Before:** N/A
- **Action:** Submit malformed email string lacking `@` delimiter.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 400 Bad Request or 401 Unauthorized)
- **Expected Response:** Error response; authentication must strictly not succeed.
- **State After:** N/A
- **Oracle Confidence:** `PARTIAL`
- **Notes:** Exact 4xx code is unspecified in API spec; rejection is mandatory.

---

### TC-FR02-AI-006: Login Rejection on Empty String Email Field
- **Test Case ID:** `FR02-AI-006`
- **Title:** Login Rejection on Empty String Email Field
- **Technique:** Equivalence Partitioning / Negative (EP-EM-04 + EP-PW-01)
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** None.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "",
    "password": "Password123!"
  }
  ```
- **State Before:** N/A
- **Action:** Submit login request with empty string email.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 400 or 401)
- **Expected Response:** Error response; authentication must strictly not succeed.
- **State After:** N/A
- **Oracle Confidence:** `PARTIAL`
- **Notes:** Mandatory field constraint verification.

---

### TC-FR02-AI-007: Login Rejection on Missing Email Property in Request Body
- **Test Case ID:** `FR02-AI-007`
- **Title:** Login Rejection on Missing Email Property in Request Body
- **Technique:** Equivalence Partitioning / Negative (EP-EM-05 + EP-PW-01)
- **Requirement:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** None.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "password": "Password123!"
  }
  ```
- **State Before:** N/A
- **Action:** Send JSON payload omitting `email` key entirely.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 400 or 401)
- **Expected Response:** Error response indicating invalid/incomplete payload; authentication must not succeed.
- **State After:** N/A
- **Oracle Confidence:** `PARTIAL`
- **Notes:** Payload structure validation.

---

### TC-FR02-AI-008: Login Rejection on Null Email Value in Request Body
- **Test Case ID:** `FR02-AI-008`
- **Title:** Login Rejection on Null Email Value in Request Body
- **Technique:** Equivalence Partitioning / Negative (EP-EM-06 + EP-PW-01)
- **Requirement:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** None.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": null,
    "password": "Password123!"
  }
  ```
- **State Before:** N/A
- **Action:** Submit `null` value for email.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 400 or 401)
- **Expected Response:** Error response; server must not crash or return unhandled 500 error.
- **State After:** N/A
- **Oracle Confidence:** `PARTIAL`
- **Notes:** Type safety and null pointer handling.

---

### TC-FR02-AI-009: Login Rejection on Whitespace-Only Email Input
- **Test Case ID:** `FR02-AI-009`
- **Title:** Login Rejection on Whitespace-Only Email Input
- **Technique:** Equivalence Partitioning / Negative (EP-EM-07 + EP-PW-01)
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** None.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "   ",
    "password": "Password123!"
  }
  ```
- **State Before:** N/A
- **Action:** Submit whitespace-only string in email field.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 400 or 401)
- **Expected Response:** Rejection notice; authentication must not succeed.
- **State After:** N/A
- **Oracle Confidence:** `PARTIAL`
- **Notes:** Whitespace sanitization / non-blank constraint.

---

### TC-FR02-AI-010: Login Rejection on Empty String Password Field
- **Test Case ID:** `FR02-AI-010`
- **Title:** Login Rejection on Empty String Password Field
- **Technique:** Equivalence Partitioning / Negative (EP-EM-01 + EP-PW-03)
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** User `test@eshop.com` exists.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com",
    "password": ""
  }
  ```
- **State Before:** `NORMAL`
- **Action:** Submit login with empty string password.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 400 or 401)
- **Expected Response:** Rejection notice; authentication must not succeed.
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (or unchanged if rejected by pre-validation)
- **Oracle Confidence:** `PARTIAL`
- **Notes:** Mandatory password constraint.

---

### TC-FR02-AI-011: Login Rejection on Missing Password Property in Request Body
- **Test Case ID:** `FR02-AI-011`
- **Title:** Login Rejection on Missing Password Property in Request Body
- **Technique:** Equivalence Partitioning / Negative (EP-EM-01 + EP-PW-04)
- **Requirement:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** User `test@eshop.com` exists.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com"
  }
  ```
- **State Before:** `NORMAL`
- **Action:** Submit JSON payload omitting `password` key.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 400 or 401)
- **Expected Response:** Error response; authentication must strictly not succeed.
- **State After:** `NORMAL` (or `FAILURE_SEQUENCE_ACTIVE`)
- **Oracle Confidence:** `PARTIAL`
- **Notes:** Incomplete request payload schema validation.

---

### TC-FR02-AI-012: Login Rejection on Null Password Value in Request Body
- **Test Case ID:** `FR02-AI-012`
- **Title:** Login Rejection on Null Password Value in Request Body
- **Technique:** Equivalence Partitioning / Negative (EP-EM-01 + EP-PW-05)
- **Requirement:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** User `test@eshop.com` exists.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com",
    "password": null
  }
  ```
- **State Before:** `NORMAL`
- **Action:** Submit `null` password value.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 400 or 401)
- **Expected Response:** Error response; server must not crash or return unhandled 500 error.
- **State After:** `NORMAL` (or `FAILURE_SEQUENCE_ACTIVE`)
- **Oracle Confidence:** `PARTIAL`
- **Notes:** Type safety validation for password field.

---

### TC-FR02-AI-013: Consecutive Failure Progression at Boundary N=2 (Remains Unlocked)
- **Test Case ID:** `FR02-AI-013`
- **Title:** Consecutive Failure Progression at Boundary N=2 (Remains Unlocked)
- **Technique:** Boundary Value Analysis (BVA $N=2$)
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test user `lockout-test@eshop.com` has experienced exactly 1 prior failed login (attempts=1, state is `FAILURE_SEQUENCE_ACTIVE`).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "WrongPasswordAttempt2!"
  }
  ```
- **State Before:** `FAILURE_SEQUENCE_ACTIVE` (attempts=1, unlocked)
- **Action:** Submit 2nd consecutive incorrect password.
- **Expected HTTP Status:** `HTTP 401 Unauthorized` (or 4xx generic credential error)
- **Expected Response:** Generic credential failure message; account must **remain UNLOCKED** (subsequent login attempts still processed).
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (attempts=2, unlocked)
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Tests $(N-1)$ boundary just below the lockout threshold $N=3$.

---

### TC-FR02-AI-014: Consecutive Failure Threshold at Boundary N=3 (Account Transitions to Locked)
- **Test Case ID:** `FR02-AI-014`
- **Title:** Consecutive Failure Threshold at Boundary N=3 (Account Transitions to Locked)
- **Technique:** Boundary Value Analysis (BVA $N=3$)
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test user `lockout-test@eshop.com` has experienced exactly 2 prior failed logins (attempts=2, state is `FAILURE_SEQUENCE_ACTIVE`).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "WrongPasswordAttempt3!"
  }
  ```
- **State Before:** `FAILURE_SEQUENCE_ACTIVE` (attempts=2, unlocked)
- **Action:** Submit 3rd consecutive incorrect password.
- **Expected HTTP Status:** `NOT SPECIFIED` on request #3 (HTTP 401 or HTTP 403)
- **Expected Response:** Authentication rejected; account state **transitions to LOCKED**. Any subsequent request during the 30-second lockout window must be rejected with a temporary lockout notice.
- **State After:** `LOCKED` (temporary 30-second lockout active)
- **Oracle Confidence:** `PARTIAL` (State transition is EXPLICIT; exact HTTP code of request #3 is NOT SPECIFIED)
- **Notes:** Tests threshold boundary $N=3$.

---

## Stage 1A.3 – Lockout State Machine & Timing

### TC-FR02-AI-015: First Consecutive Failed Login Attempt (Normal to Failure Sequence Active, Not Locked)
- **Test Case ID:** `FR02-AI-015`
- **Title:** First Consecutive Failed Login Attempt (Normal to Failure Sequence Active, Not Locked)
- **Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` exists in `NORMAL` baseline state (attempts=0, unlocked).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "WrongPasswordAttempt1!"
  }
  ```
- **State Before:** `NORMAL` (attempts=0, unlocked)
- **Action:** Submit 1st incorrect password on baseline account.
- **Expected HTTP Status:** `HTTP 401 Unauthorized` (or 4xx generic credential error)
- **Expected Response:** Generic error message (e.g. `"Invalid email or password"`); account must **remain UNLOCKED** and immediately accept subsequent login attempts for credential evaluation.
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (attempts=1, unlocked)
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Fixes Stage 1A.2 coverage gap by explicitly asserting non-locked state on initial failure ($N=1$).

---

### TC-FR02-AI-016: Second Consecutive Failed Login Attempt (Progression in Failure Sequence, Remains Unlocked)
- **Test Case ID:** `FR02-AI-016`
- **Title:** Second Consecutive Failed Login Attempt (Progression in Failure Sequence, Remains Unlocked)
- **Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` has experienced exactly 1 prior failed login (state: `FAILURE_SEQUENCE_ACTIVE`, attempts=1).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "WrongPasswordAttempt2!"
  }
  ```
- **State Before:** `FAILURE_SEQUENCE_ACTIVE` (attempts=1, unlocked)
- **Action:** Submit 2nd consecutive incorrect password.
- **Expected HTTP Status:** `HTTP 401 Unauthorized` (or 4xx generic credential error)
- **Expected Response:** Generic credential error message; account must **remain UNLOCKED**.
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (attempts=2, unlocked)
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Validates state progression from attempt 1 to attempt 2 without premature lock.

---

### TC-FR02-AI-017: Third Consecutive Failed Login Attempt (Transitions Account into Locked State)
- **Test Case ID:** `FR02-AI-017`
- **Title:** Third Consecutive Failed Login Attempt (Transitions Account into Locked State)
- **Technique:** STATE TRANSITION / BVA
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` has experienced exactly 2 prior failed logins (state: `FAILURE_SEQUENCE_ACTIVE`, attempts=2).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "WrongPasswordAttempt3!"
  }
  ```
- **State Before:** `FAILURE_SEQUENCE_ACTIVE` (attempts=2, unlocked)
- **Action:** Submit 3rd consecutive incorrect password.
- **Expected HTTP Status:** `NOT SPECIFIED` on request #3 (HTTP 401 or HTTP 403)
- **Expected Response:** Authentication rejected; account state **transitions to LOCKED**. Any subsequent request during the 30-second lockout window must be rejected with a temporary lockout notice.
- **State After:** `LOCKED` (temporary 30-second lockout active)
- **Oracle Confidence:** `PARTIAL` (State transition is EXPLICIT; exact HTTP code of request #3 is NOT SPECIFIED)
- **Notes:** Threshold state transition test ($N=3$).

---

### TC-FR02-AI-018: Login Rejection on Subsequent Request During Active Lockout Window (Wrong Credentials)
- **Test Case ID:** `FR02-AI-018`
- **Title:** Login Rejection on Subsequent Request During Active Lockout Window (Wrong Credentials)
- **Technique:** STATE TRANSITION / NEGATIVE
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` has triggered lockout ($N=3$ consecutive failures) and is currently within the active 30-second lockout window ($T < 30\text{s}$).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "AnyWrongPassword!"
  }
  ```
- **State Before:** `LOCKED` (active lockout window)
- **Action:** Submit login request with incorrect credentials during active lockout.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 403 Forbidden / 429 Too Many Requests / 4xx)
- **Expected Response:** Error notice indicating account is temporarily locked without disclosing internal variables or stack traces.
- **State After:** `LOCKED` (lockout remains active until 30s elapsed)
- **Oracle Confidence:** `PARTIAL`
- **Notes:** Verifies active lockout defense against continued brute-force attempts.

---

### TC-FR02-AI-019: Login Rejection on Subsequent Request During Active Lockout Window (Correct Credentials Do Not Bypass Lock)
- **Test Case ID:** `FR02-AI-019`
- **Title:** Login Rejection on Subsequent Request During Active Lockout Window (Correct Credentials Do Not Bypass Lock)
- **Technique:** STATE TRANSITION / NEGATIVE / SECURITY
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` has triggered lockout ($N=3$ consecutive failures) and is currently within the active 30-second lockout window ($T < 30\text{s}$). Registered password is `LockoutPass123!`.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "LockoutPass123!"
  }
  ```
- **State Before:** `LOCKED` (active lockout window)
- **Action:** Submit login request with the **CORRECT** password while account is locked.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 403 Forbidden / 429 / 4xx)
- **Expected Response:** Error notice indicating account is temporarily locked; authentication must strictly NOT succeed and NO JWT token must be issued.
- **State After:** `LOCKED`
- **Oracle Confidence:** `EXPLICIT` (Semantic rule that locked account cannot authenticate is explicit)
- **Notes:** Critical security test verifying correct credentials cannot bypass an active lockout state.

---

### TC-FR02-AI-020: Lockout Duration Timing Boundary Check Prior to Expiration (T=25s in 30s Window)
- **Test Case ID:** `FR02-AI-020`
- **Title:** Lockout Duration Timing Boundary Check Prior to Expiration (T=25s in 30s Window)
- **Technique:** BVA / STATE TRANSITION
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` entered `LOCKED` state at $T_0$. Exactly 25 seconds have elapsed ($T_0 + 25\text{s} < T_0 + 30\text{s}$).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "LockoutPass123!"
  }
  ```
- **State Before:** `LOCKED` (active, remaining duration $\approx 5\text{s}$)
- **Action:** Attempt login at $T+25\text{s}$ before the 30-second duration expires.
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 403 / 429 / 4xx)
- **Expected Response:** Rejection with temporary lockout notice; authentication must not succeed.
- **State After:** `LOCKED`
- **Oracle Confidence:** `PARTIAL`
- **Notes:** BVA before-expiry boundary check ($T < 30\text{s}$).

---

### TC-FR02-AI-021: Lockout Duration Expiration Boundary Check After 30s Window (T=32s Auto-Unlock)
- **Test Case ID:** `FR02-AI-021`
- **Title:** Lockout Duration Expiration Boundary Check After 30s Window (T=32s Auto-Unlock)
- **Technique:** BVA / STATE TRANSITION
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` entered `LOCKED` state at $T_0$. More than 30 seconds have elapsed ($T_0 + 32\text{s} > T_0 + 30\text{s}$).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "LockoutPass123!"
  }
  ```
- **State Before:** `LOCK_EXPIRED`
- **Action:** Submit login with valid credentials at $T+32\text{s}$ after the 30-second duration has elapsed.
- **Expected HTTP Status:** `HTTP 200 OK`
- **Expected Response:** Successful login response returning valid JWT `token` and `user` object.
- **State After:** `NORMAL` (account unlocked and authenticated)
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** BVA after-expiry boundary check ($T > 30\text{s}$) verifying automatic unlock.

---

### TC-FR02-AI-022: Successful Authentication Resets Consecutive Failure Progression
- **Test Case ID:** `FR02-AI-022`
- **Title:** Successful Authentication Resets Consecutive Failure Progression
- **Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` in `NORMAL` state.
- **Action Sequence:**
  1. Step 1: Submit 1 wrong password $\rightarrow$ State transitions to `FAILURE_SEQUENCE_ACTIVE` (attempts=1).
  2. Step 2: Submit correct password $\rightarrow$ Returns HTTP 200 OK; State resets to `NORMAL` (attempts=0).
  3. Step 3: Submit 1 wrong password $\rightarrow$ State transitions to `FAILURE_SEQUENCE_ACTIVE` (attempts=1 of new sequence).
- **Expected HTTP Status:**
  - Step 1: `HTTP 401 Unauthorized`
  - Step 2: `HTTP 200 OK`
  - Step 3: `HTTP 401 Unauthorized`
- **Expected Response:** At Step 3, account must **remain UNLOCKED** (treated as 1st failure of a new sequence, not 2nd cumulative failure).
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (attempts=1, unlocked)
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Verifies SRS requirement that successful login resets the consecutive failure counter to 0.

---

### TC-FR02-AI-023: Consecutive Failure Semantics Verification (Non-Consecutive Failures Do Not Trigger Lockout)
- **Test Case ID:** `FR02-AI-023`
- **Title:** Consecutive Failure Semantics Verification (Non-Consecutive Failures Do Not Trigger Lockout)
- **Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` in `NORMAL` state.
- **Action Sequence:**
  1. Step 1: Submit 1 wrong password (Failure #1) $\rightarrow$ 401.
  2. Step 2: Submit correct password (Reset) $\rightarrow$ 200 OK.
  3. Step 3: Submit 1 wrong password (New Sequence Failure #1) $\rightarrow$ 401.
  4. Step 4: Submit 2nd wrong password (New Sequence Failure #2) $\rightarrow$ 401.
- **Expected HTTP Status:**
  - Step 1: `HTTP 401 Unauthorized`
  - Step 2: `HTTP 200 OK`
  - Step 3: `HTTP 401 Unauthorized`
  - Step 4: `HTTP 401 Unauthorized`
- **Expected Response:** At Step 4, total lifetime failures in session is 3, but consecutive failures in active sequence is only 2. Account must **remain UNLOCKED**.
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (attempts=2, unlocked)
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Strictly tests the "consecutive" requirement ("từ 3 lần trở lên liên tiếp").

---

### TC-FR02-AI-024: Post-Lockout Expiration Account Usability and Failure Sequence Reset
- **Test Case ID:** `FR02-AI-024`
- **Title:** Post-Lockout Expiration Account Usability and Failure Sequence Reset
- **Technique:** STATE TRANSITION / SEQUENCE TESTING
- **Requirement:** 📋 [SRS §2 FR-02]
- **Preconditions:** Account `lockout-test@eshop.com` underwent full lockout ($N=3$), waited 32s until lock expired, and performed 1 successful login (200 OK).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "WrongPasswordPostUnlock1!"
  }
  ```
- **State Before:** `NORMAL` (restored post-unlock)
- **Action:** Submit 1 incorrect password after full lockout-unlock-login lifecycle.
- **Expected HTTP Status:** `HTTP 401 Unauthorized`
- **Expected Response:** Generic credential error; account must **remain UNLOCKED** (behaving as attempt=1 of a fresh lifecycle).
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (attempts=1, unlocked)
- **Oracle Confidence:** `EXPLICIT`
- **Notes:** Verifies full account recovery and absence of residual lockout states after complete lifecycle.

---

## Stage 1A.4 – Security Probes

### TC-FR02-AI-025: SQL Injection Behavioral Probe in Email Field
- **Test Case ID:** `FR02-AI-025`
- **Title:** SQL Injection Behavioral Probe in Email Field
- **Technique:** INJECTION PROBE / SECURITY (SEC-05)
- **Security Classification:** `SEC-05 – PARTIAL BLACK-BOX EVIDENCE`
- **Requirement:** 📋 [SRS §9 SEC-05]
- **Preconditions:** None.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "admin@eshop.com' OR '1'='1",
    "password": "ArbitraryPassword!"
  }
  ```
- **State Before:** N/A
- **Action:** Submit classic SQL injection authentication-bypass string in the email field.
- **Expected HTTP Status:** `HTTP 401 Unauthorized` (or 4xx generic error; strictly NOT 200 OK, NOT 500 Internal Server Error)
- **Expected Semantic Result:** Authentication strictly rejected; no unauthorized access granted.
- **Expected Security Result:** Payload treated safely as literal data; no SQL syntax error leaked in response.
- **State After:** Unchanged / No unauthorized session established
- **Oracle Confidence:** `PARTIAL`
- **Black-Box Limitation:** Rejection of an injection payload provides behavioral resistance evidence only; it does not definitively prove parameterized queries are implemented at rest (full proof requires DB/source verification).
- **Notes:** SEC-05 behavioral injection resistance test.

---

### TC-FR02-AI-026: SQL Injection Behavioral Probe in Password Field
- **Test Case ID:** `FR02-AI-026`
- **Title:** SQL Injection Behavioral Probe in Password Field
- **Technique:** INJECTION PROBE / SECURITY (SEC-05)
- **Security Classification:** `SEC-05 – PARTIAL BLACK-BOX EVIDENCE`
- **Requirement:** 📋 [SRS §9 SEC-05]
- **Preconditions:** Registered user `admin@eshop.com` exists.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "admin@eshop.com",
    "password": "' OR 1=1 --"
  }
  ```
- **State Before:** N/A
- **Action:** Submit SQL injection comment/tautology string in the password field for a known user.
- **Expected HTTP Status:** `HTTP 401 Unauthorized` (or 4xx generic error; strictly NOT 200 OK, NOT 500)
- **Expected Semantic Result:** Authentication strictly rejected; no password bypass occurs.
- **Expected Security Result:** Password string treated as literal value; no database error exposure.
- **State After:** Unchanged / No unauthorized session established
- **Oracle Confidence:** `PARTIAL`
- **Black-Box Limitation:** Behavioral rejection does not prove parameterized queries are used.
- **Notes:** SEC-05 behavioral injection resistance test.

---

### TC-FR02-AI-027: Cross-Response Generic Credential Error Equivalence (Anti-Enumeration)
- **Test Case ID:** `FR02-AI-027`
- **Title:** Cross-Response Generic Credential Error Equivalence (Anti-Enumeration)
- **Technique:** INFORMATION DISCLOSURE / SECURITY
- **Security Classification:** `[ADDITIONAL-SEC] / SRS FR-02 Information Disclosure Defense`
- **Requirement:** 📋 [SRS §2 FR-02] ("không để lộ chi tiết nguyên nhân")
- **Preconditions:** User `test@eshop.com` exists; user `nonexistent_audit_user@eshop.com` does not exist.
- **Action Sequence:**
  1. Step 1: Submit Request A with registered email + wrong password:
     `{"email": "test@eshop.com", "password": "WrongPassword999!"}`
  2. Step 2: Submit Request B with unregistered email + arbitrary password:
     `{"email": "nonexistent_audit_user@eshop.com", "password": "ArbitraryPassword999!"}`
- **Expected HTTP Status:**
  - Step 1: `HTTP 401 Unauthorized` (or 4xx)
  - Step 2: `HTTP 401 Unauthorized` (or 4xx)
- **Expected Semantic Result:** Both requests return HTTP 4xx errors.
- **Expected Security Result:** The response body error message of Request A and Request B must be **identical / semantically indistinguishable** (e.g. both return `"Invalid email or password"`), preventing attackers from enumerating valid account emails.
- **State Before:** Step 1: `NORMAL`
- **State After:** Step 1: `FAILURE_SEQUENCE_ACTIVE` (attempts=1); Step 2: N/A
- **Oracle Confidence:** `EXPLICIT`
- **Black-Box Limitation:** Directly testable and verifiable via black-box API comparison.
- **Notes:** Distinct from individual EP rejection tests (FR02-AI-003 and 004); specifically evaluates cross-response equivalence.

---

### TC-FR02-AI-028: Sensitive Credential Exposure Probe in Successful Login Response
- **Test Case ID:** `FR02-AI-028`
- **Title:** Sensitive Credential Exposure Probe in Successful Login Response
- **Technique:** SECURITY / SENSITIVE DATA EXPOSURE
- **Security Classification:** `[ADDITIONAL-SEC] Sensitive Data Exposure in Response / SEC-01 Probe`
- **Requirement:** 📋 [SRS §9 SEC-01] & Clean Credential Handling
- **Preconditions:** Registered user `test@eshop.com` with password `Test1234!` exists.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com",
    "password": "Test1234!"
  }
  ```
- **State Before:** `NORMAL`
- **Action:** Submit valid credentials to obtain successful authentication response.
- **Expected HTTP Status:** `HTTP 200 OK`
- **Expected Semantic Result:** Successful login returning JWT `token` and `user` profile object.
- **Expected Security Result:** The `response.user` object must **NOT expose the password field** (`response.user.password` must be `undefined` or omitted). Plaintext password must never be reflected in response payloads.
- **State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL`
- **Black-Box Limitation:** Absence of a password field in API JSON response provides transport-level sanitization evidence; it does NOT definitively prove password hashing at rest (SEC-01 full proof requires DB inspection).
- **Notes:** Sensitive data exclusion assertion.

---

### TC-FR02-AI-029: Token Omission Assertion on Failed Authentication
- **Test Case ID:** `FR02-AI-029`
- **Title:** Token Omission Assertion on Failed Authentication
- **Technique:** SECURITY / AUTHENTICATION
- **Security Classification:** `[ADDITIONAL-SEC] Authentication Token Isolation`
- **Requirement:** 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com",
    "password": "IncorrectPassword123!"
  }
  ```
- **State Before:** `NORMAL`
- **Action:** Submit failed authentication request.
- **Expected HTTP Status:** `HTTP 401 Unauthorized` (or 4xx)
- **Expected Semantic Result:** Authentication rejected with generic error.
- **Expected Security Result:** The response body must **strictly NOT contain a `token` field** (or `token` must be `undefined`/null). No session or authorization capability is conferred upon failed authentication.
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (attempts=1, unlocked)
- **Oracle Confidence:** `EXPLICIT`
- **Black-Box Limitation:** Fully testable via response payload inspection.
- **Notes:** Security integrity assertion on error payloads.

---

### TC-FR02-AI-030: SEC-02 Supporting Token Usability Verification on Protected Endpoint
- **Test Case ID:** `FR02-AI-030`
- **Title:** SEC-02 Supporting Token Usability Verification on Protected Endpoint
- **Technique:** SECURITY / AUTHENTICATION / SEQUENCE TESTING
- **Security Classification:** `SEC-02 SUPPORTING / INDIRECT FR-02 TEST`
- **Requirement:** 📋 [SRS §9 SEC-02] & 📋 [SRS §2 FR-02]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Action Sequence:**
  1. Step 1: Submit valid login (`POST /api/login`) $\rightarrow$ Capture returned JWT string as `userToken`.
  2. Step 2: Call protected endpoint `GET /api/orders/my-orders` with header `Authorization: Bearer <userToken>`.
- **Expected HTTP Status:**
  - Step 1: `HTTP 200 OK`
  - Step 2: `HTTP 200 OK`
- **Expected Semantic Result:** Valid token issued by FR-02 is accepted by protected endpoint.
- **Expected Security Result:** Protected endpoint successfully validates the JWT signature and payload issued by `POST /api/login`, granting access to the authenticated user's resources.
- **State Before:** Step 1: `NORMAL`
- **State After:** Step 1: `NORMAL`
- **Oracle Confidence:** `PARTIAL`
- **Black-Box Limitation:** SEC-02 enforcement belongs primarily to the protected endpoint (`GET /api/orders/my-orders`), while FR-02 functions as the token issuer.
- **Notes:** Downstream authentication dependency verification.

---

### TC-FR02-AI-031: SEC-02 Supporting Tampered Signature Rejection on Protected Endpoint
- **Test Case ID:** `FR02-AI-031`
- **Title:** SEC-02 Supporting Tampered Signature Rejection on Protected Endpoint
- **Technique:** SECURITY / SIGNATURE INTEGRITY / SEQUENCE TESTING
- **Security Classification:** `SEC-02 SUPPORTING / INDIRECT FR-02 TEST`
- **Requirement:** 📋 [SRS §9 SEC-02] & 📋 [SRS §2 FR-02]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Action Sequence:**
  1. Step 1: Submit valid login (`POST /api/login`) $\rightarrow$ Capture returned JWT.
  2. Step 2: Tamper with the JWT payload/signature (e.g. modify payload role or append invalid signature characters).
  3. Step 3: Call protected endpoint `GET /api/orders/my-orders` with header `Authorization: Bearer <tamperedToken>`.
- **Expected HTTP Status:**
  - Step 1: `HTTP 200 OK`
  - Step 3: `HTTP 401 Unauthorized` (or 403 Forbidden)
- **Expected Semantic Result:** Tampered token is rejected.
- **Expected Security Result:** Protected endpoint detects invalid/tampered cryptographic signature on the token issued by FR-02 and denies access.
- **State Before:** Step 1: `NORMAL`
- **State After:** Step 1: `NORMAL`
- **Oracle Confidence:** `EXPLICIT`
- **Black-Box Limitation:** Verifies JWT cryptographic integrity verification on downstream consumer.
- **Notes:** SEC-02 token integrity probe.

---

## Stage 1A.5 – Schema Validation and Error Contracts

### TC-FR02-AI-032: Successful Login Response Schema and Data Type Contract
- **Test Case ID:** `FR02-AI-032`
- **Title:** Successful Login Response Schema and Data Type Contract
- **Technique:** SCHEMA VALIDATION / API CONTRACT
- **Requirement:** 🗂️ [API-SPEC §1.2] & 📋 [SRS §2 FR-02]
- **Preconditions:** Active registered user `test@eshop.com` with password `Test1234!` exists.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com",
    "password": "Test1234!"
  }
  ```
- **Expected HTTP Status:** `HTTP 200 OK`
- **Expected Response Contract:** Top-level JSON object strictly containing documented contract attributes.
- **Required Fields:**
  - `token`: Required
  - `user`: Required
  - `message`: Optional / Documented string
- **Field Types:**
  - `token`: `string` (non-empty 3-part base64 encoded JWT)
  - `user`: `object` containing:
    - `user.id`: `number` / `integer` (positive)
    - `user.name`: `string`
    - `user.email`: `string` matching `"test@eshop.com"`
    - `user.role`: `string` (`"user"` or `"admin"`)
- **Fields That Must Not Indicate Successful Authentication:** N/A (Success response)
- **Oracle Confidence:** `EXPLICIT`
- **Specification Limitations:** `api_specification.md` Section 1.2 provides explicit example structure for success response.
- **Notes:** Distinct from behavioral test FR02-AI-001 by asserting full schema type definitions on all returned attributes.

---

### TC-FR02-AI-033: Invalid Credentials Error Response Schema and Structure Contract
- **Test Case ID:** `FR02-AI-033`
- **Title:** Invalid Credentials Error Response Schema and Structure Contract
- **Technique:** SCHEMA VALIDATION / ERROR CONTRACT
- **Requirement:** 🗂️ [API-SPEC §1.2] & 📋 [SRS §2 FR-02]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com",
    "password": "WrongPasswordForSchema123!"
  }
  ```
- **Expected HTTP Status:** `HTTP 401 Unauthorized` (or 4xx error)
- **Expected Response Contract:** Valid JSON error object.
- **Required Fields:**
  - Top-level error description string (e.g. `error` or `message` property).
- **Field Types:**
  - `error` / `message`: `string` (non-empty human-readable generic error message).
- **Fields That Must Not Indicate Successful Authentication:**
  - `token` must strictly NOT exist or be null.
  - `user` must strictly NOT exist.
- **Oracle Confidence:** `EXPLICIT`
- **Specification Limitations:** API specification provides error description; exact error key name (`error` vs `message`) is evaluated flexibly across standard REST conventions.
- **Notes:** Validates error payload structure and complete absence of auth session tokens.

---

### TC-FR02-AI-034: Locked-Account Error Response Contract and Internal Non-Disclosure
- **Test Case ID:** `FR02-AI-034`
- **Title:** Locked-Account Error Response Contract and Internal Non-Disclosure
- **Technique:** SCHEMA VALIDATION / ERROR CONTRACT
- **Requirement:** 📋 [SRS §2 FR-02] ("thông báo tạm khóa... không để lộ chi tiết")
- **Preconditions:** Dedicated test account `lockout-test@eshop.com` is in `LOCKED` state.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "lockout-test@eshop.com",
    "password": "LockoutPass123!"
  }
  ```
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 403 Forbidden / 429 / 4xx)
- **Expected Response Contract:** Valid JSON error object informing of temporary lockout.
- **Required Fields:**
  - Error message property indicating temporary lockout status.
- **Field Types:**
  - Error description property: `string`.
- **Fields That Must Not Indicate Successful Authentication:**
  - `token` and `user` must strictly NOT exist.
  - Internal debug properties (e.g. `stack`, `sql`, `lockout_until` raw epoch, `attempts` counter) must NOT be leaked.
- **Oracle Confidence:** `PARTIAL`
- **Specification Limitations:** Exact status code and field name are unspecified in SRS; non-disclosure and error structure are specification-backed.
- **Notes:** Focuses on response structure and sanitization of internal server attributes during lockout.

---

### TC-FR02-AI-035: Syntactically Malformed JSON Request Body Transport Contract
- **Test Case ID:** `FR02-AI-035`
- **Title:** Syntactically Malformed JSON Request Body Transport Contract
- **Technique:** NEGATIVE CONTRACT / PARSER RESILIENCE
- **Requirement:** 🗂️ [API-SPEC §1.2] & Transport Robustness
- **Preconditions:** None.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```text
  { "email": "test@eshop.com", "password": 
  ```
  *(Truncated / broken JSON syntax lacking closing value and brace)*
- **Expected HTTP Status:** `NOT SPECIFIED` (HTTP 400 Bad Request or 4xx; strictly NOT 200 OK, NOT 500 Internal Server Error)
- **Expected Response Contract:** Client error response; server parser must handle malformed JSON cleanly without unhandled runtime crash or HTML stack trace leakage.
- **Required Fields:** `NOT SPECIFIED`
- **Field Types:** Structured JSON error object (or standard HTTP 4xx body).
- **Fields That Must Not Indicate Successful Authentication:**
  - `token` and `user` must strictly NOT exist.
- **Oracle Confidence:** `PARTIAL`
- **Specification Limitations:** Transport parser error codes are not explicitly documented in the business API spec.
- **Notes:** Distinguishes HTTP parser resilience from business authentication logic.

---

### TC-FR02-AI-036: Response Content-Type Header Contract Across Status Codes
- **Test Case ID:** `FR02-AI-036`
- **Title:** Response Content-Type Header Contract Across Status Codes
- **Technique:** API CONTRACT / HEADER VALIDATION
- **Requirement:** 🗂️ [API-SPEC §1.2]
- **Preconditions:** Registered user `test@eshop.com` exists.
- **Action Sequence:**
  1. Step 1: Send valid login request (`POST /api/login`).
  2. Step 2: Send invalid login request (`POST /api/login`).
- **Expected HTTP Status:**
  - Step 1: `HTTP 200 OK`
  - Step 2: `HTTP 401 Unauthorized` (or 4xx)
- **Expected Response Contract:**
  - Both Step 1 and Step 2 HTTP responses must include the header `Content-Type: application/json` (or `application/json; charset=utf-8`).
- **Required Fields:** N/A (Header contract)
- **Field Types:** Header value: `string` containing `application/json`.
- **Fields That Must Not Indicate Successful Authentication:** N/A
- **Oracle Confidence:** `EXPLICIT`
- **Specification Limitations:** Standard REST JSON contract documented across `api_specification.md`.
- **Notes:** Validates consistent HTTP MIME type header delivery.

---

### TC-FR02-AI-037: Extraneous Request Body Properties Ingestion Contract
- **Test Case ID:** `FR02-AI-037`
- **Title:** Extraneous Request Body Properties Ingestion Contract
- **Technique:** API CONTRACT / EXPLORATORY SCHEMA
- **Requirement:** 🗂️ [API-SPEC §1.2] & Schema Robustness
- **Preconditions:** Registered standard user `test@eshop.com` exists (role is `"user"`).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Request Body:**
  ```json
  {
    "email": "test@eshop.com",
    "password": "Test1234!",
    "unrecognized_field": "exploratory_payload",
    "role": "admin"
  }
  ```
- **Expected HTTP Status:** `HTTP 200 OK` (or 400 if strict schema validation is enforced)
- **Expected Response Contract:** If login succeeds, the issued JWT and `user` object must reflect the actual database role (`"user"`), and injected extraneous fields must be ignored.
- **Required Fields:** Standard success fields (`token`, `user`).
- **Field Types:** Standard login success schema.
- **Fields That Must Not Indicate Successful Authentication:**
  - `user.role` must NOT be elevated to `"admin"`.
- **Oracle Confidence:** `PARTIAL`
- **Specification Limitations:** API specification does not mandate whether extraneous fields are rejected with 400 or silently ignored; privilege non-escalation is mandatory.
- **Notes:** Evaluates schema parser tolerance and parameter injection resistance.
