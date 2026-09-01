# FR-02 SUT Bug Candidates Catalog

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`
- **Execution Run Reference:** `FR02-run-03`

---

## 1. Executive Bug Summary

During formal Newman execution of the 40-case FR-02 test suite against the EShop SUT, **4 genuine defect candidates** were uncovered. Each defect violates explicit specification clauses in SRS §2 FR-02, SEC requirements, or standard HTTP/REST API contracts.

| Bug ID | Title | Severity | Relevant Test Case | Specification Reference | Root Cause Category |
|---|---|:---:|:---:|---|---|
| **`BUG-FR02-001`** | Plaintext Password Exposure in Login Response JSON | **CRITICAL** | `FR02-AI-028` | ADDITIONAL-SEC / OWASP API3 | Information Disclosure / Response Sanitization |
| **`BUG-FR02-002`** | Permanent Account Lockout (Failure to Auto-Unlock at T > 30s) | **HIGH** | `FR02-AI-021` | SRS §2 FR-02 | State Machine / Lock Expiration Logic |
| **`BUG-FR02-003`** | Premature Lockout on Valid Login Attempt at N=2 Boundary | **HIGH** | `FR02-HUM-003` | SRS §2 FR-02 | Attempt Counter Order of Operations |
| **`BUG-FR02-004`** | Unhandled Server Crash (HTTP 500) on Form-Encoded Request Body | **MEDIUM** | `FR02-HUM-005` | API-SPEC §1.2 | Transport Parsing / Body Middleware Exception |

---

## 2. Detailed Bug Reports

### BUG-FR02-001: Plaintext Password Exposure in Login Response Profile
- **Bug ID:** `BUG-FR02-001`
- **Test ID:** `FR02-AI-028`
- **Severity:** **CRITICAL** (CWE-200: Exposure of Sensitive Information, OWASP API3:2023 Broken Object Property Level Authorization)
- **Specification Oracle:**
  > "A successful login response must return a JWT token and user profile object. The user profile MUST NEVER disclose the plaintext password or password hash."
- **Observed Behavior:**
  Sending a valid `POST /api/login` returns HTTP 200 with the full user record containing `"password": "User1234!"` in plaintext inside `response.user`.
- **Payload / Reproduction:**
  ```http
  POST /api/login HTTP/1.1
  Host: localhost:3000
  Content-Type: application/json

  {
    "email": "user_123456@eshop.com",
    "password": "User1234!"
  }
  ```
- **Actual Response:**
  ```json
  {
    "message": "Login successful",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 24,
      "name": "Regular User",
      "email": "user_123456@eshop.com",
      "password": "User1234!",
      "role": "user",
      "login_attempts": 0,
      "locked_until": null
    }
  }
  ```

---

### BUG-FR02-002: Permanent Account Lockout (Failure to Auto-Unlock after 30-Second Duration)
- **Bug ID:** `BUG-FR02-002`
- **Test ID:** `FR02-AI-021` (and `FR02-AI-024`)
- **Severity:** **HIGH** (Denial of Service / Core Business Logic Violation)
- **Specification Oracle:**
  > [SRS §2 FR-02]: "If consecutive failed attempts >= 3, the account is temporarily locked for 30 seconds. After 30 seconds, the account must automatically unlock and permit authentication with valid credentials."
- **Observed Behavior:**
  After 3 failed login attempts, the account is locked. When valid credentials are submitted after waiting $\ge 32$ seconds (e.g. 35s), the server continues to return HTTP 403 Forbidden (`{"error": "Tài khoản đã bị khóa. Vui lòng thử lại sau."}`) indefinitely. The account never unlocks without manual database intervention.
- **Payload / Reproduction:**
  1. Send 3 incorrect password requests to `lockout_user@eshop.com` $ightarrow$ Account locks on 3rd attempt.
  2. Wait 35 seconds ($T > 30	ext{s}$).
  3. Send `POST /api/login` with valid password $ightarrow$ Returns HTTP 403 instead of HTTP 200 + JWT.

---

### BUG-FR02-003: Premature Lockout on Valid Login Attempt at N=2 Boundary
- **Bug ID:** `BUG-FR02-003`
- **Test ID:** `FR02-HUM-003` (Student Human Extension)
- **Severity:** **HIGH** (Authentication Flaw / Premature Account Denial)
- **Specification Oracle:**
  > [SRS §2 FR-02]: "Lockout threshold is 3 CONSECUTIVE failed login attempts. An account with 2 prior failed attempts ($N=2$) must remain unlocked. If the user submits valid credentials on the 3rd attempt, login must succeed (HTTP 200 + JWT) and reset the failure counter to 0."
- **Observed Behavior:**
  When an account has 2 prior failed logins ($N=2$), submitting CORRECT credentials on the 3rd attempt causes the SUT to trigger lockout and return HTTP 403 Forbidden instead of authenticating!
- **Root Cause:**
  The SUT increments the attempt counter or checks `login_attempts >= 2` *before* authenticating the submitted password, treating the 3rd request as a lock-triggering failure regardless of password validity.

---

### BUG-FR02-004: Unhandled Server Crash (HTTP 500) on Form-Encoded Request Body
- **Bug ID:** `BUG-FR02-004`
- **Test ID:** `FR02-HUM-005` (Student Human Extension)
- **Severity:** **MEDIUM** (Robustness / Unhandled Exception)
- **Specification Oracle:**
  > [API-SPEC §1.2]: "API endpoints communicate via JSON (`application/json`). Requests with invalid or unsupported encoding must be rejected gracefully with a 4xx client error (e.g. 400 Bad Request or 415 Unsupported Media Type) without server crashes."
- **Observed Behavior:**
  Submitting `POST /api/login` with `Content-Type: application/x-www-form-urlencoded` and URL-encoded body `email=user%40eshop.com&password=User1234!` causes an unhandled exception in the backend resulting in **HTTP 500 Internal Server Error**.
- **Payload / Reproduction:**
  ```http
  POST /api/login HTTP/1.1
  Host: localhost:3000
  Content-Type: application/x-www-form-urlencoded

  email=user%40eshop.com&password=User1234!
  ```
- **Actual Response:** `HTTP/1.1 500 Internal Server Error` with HTML error stack.
