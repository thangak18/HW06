# FR-02 Student-Selected Human Extension Test Cases

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

> [!NOTE]
> **Provenance Statement:**
> These extension directions were selected and finalized by the student after reviewing the completed AI-generated suite, Human Audit results, and an AI-assisted coverage-gap analysis. They are intentionally separated from the raw AI-generated `FR02-AI` inventory and assigned formal `FR02-HUM` identifiers.

---

## 1. Suite Accounting & Summary

- **Raw AI-Generated Test Cases:** 37
- **Raw AI Rejected During Human Audit:** 2 (`FR02-AI-016`, `FR02-AI-017` as redundant duplicates)
- **Usable AI-Derived Cases Post-Audit:** 35 (16 `VALID` + 19 `INCOMPLETE with corrections`)
- **Student-Designed Human Extension Cases:** 5 (`FR02-HUM-001` .. `FR02-HUM-005`)
- **Total Final Executable Candidate Suite:** **40 Test Cases**

---

## 2. Human-vs-AI Distinctness Matrix

| Human ID | Title | Closest AI Case(s) | Key Technical Innovation / What Is New | Duplicate Status |
|---|---|---|---|:---:|
| `FR02-HUM-001` | HTTP Verb / Method Enforcement Rejection | None (All AI cases used `POST`) | Evaluates route handler robustness when non-documented HTTP verbs (`GET`) are dispatched. | **DISTINCT** |
| `FR02-HUM-002` | Advanced SQL Injection Multi-Vector Resilience Probe | `FR02-AI-025`, `FR02-AI-026` (Simple tautology `' OR '1'='1`) | Uses a distinct comment-truncation vector (`admin@eshop.com'--`) probing multi-character SQL syntax resilience. | **DISTINCT** |
| `FR02-HUM-003` | Consecutive Failure Counter Reset at N=2 Pre-Lockout Boundary | `FR02-AI-022` (Reset after $N=1$), `FR02-AI-023` | Tests successful login reset specifically at the critical $(N-1)$ threshold-adjacent state ($N=2$) before lockout. | **DISTINCT** |
| `FR02-HUM-004` | Account Lockout State Isolation Between Independent User Accounts | `FR02-AI-018`, `FR02-AI-019` (Single-account lockout) | Uses two independent accounts to verify that Account A's lockout state does not block Account B's authentication. | **DISTINCT** |
| `FR02-HUM-005` | Non-JSON Content-Type Request Contract Handling | `FR02-AI-035` (Malformed JSON syntax), `FR02-AI-036` | Tests valid credentials supplied via unsupported `application/x-www-form-urlencoded` MIME encoding. | **DISTINCT** |

---

## 3. Detailed Human Test Case Specifications

### TC-FR02-HUM-001: HTTP Verb / Method Enforcement Rejection on Login Route
- **Test Case ID:** `FR02-HUM-001`
- **Title:** HTTP Verb / Method Enforcement Rejection on Login Route
- **Source Gap:** `G-02` (HTTP Method Enforcement on `/api/login`)
- **Student Rationale:** The documented login operation strictly specifies `POST /api/login`. The original AI suite tested only `POST` and never verified whether unsupported HTTP methods (`GET`, `PUT`, `DELETE`) on the login route cannot accidentally invoke authentication logic or expose internal endpoints.
- **Why Existing AI Suite Missed This:** AI generation assumed standard REST POST method bindings and focused entirely on request body variation, neglecting HTTP verb dispatching boundaries.
- **Technique:** API CONTRACT / METHOD ENFORCEMENT
- **Requirement / Spec Basis:** 🗂️ [API-SPEC §1.2] (Specifies `POST /api/login`)
- **Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED` / `API CONTRACT`
- **Preconditions:** Registered user exists.
- **Request Method / Sequence:** `GET /api/login`
- **Endpoint:** `/api/login`
- **Headers:**
  - `X-Student-Id: 23127259`
- **Test Data:** Empty body / No payload
- **Steps:** Send an HTTP `GET` request to `/api/login`.
- **Expected HTTP Status:** `HTTP 404 Not Found` or `HTTP 405 Method Not Allowed` (Exact status is NOT SPECIFIED in API Spec).
- **Expected Semantic Result:** The server must NOT execute authentication logic, must NOT authenticate the user, and must NOT issue a valid JWT token.
- **State Before:** `NORMAL`
- **State After:** `NORMAL` (Failure counter is unchanged).
- **Oracle Confidence:** `PARTIAL`
- **Spec Limitations:** Exact HTTP error status for unsupported verbs on login is not explicitly defined in `api_specification.md`; assertion relies on non-authentication.
- **Postman Implementation Notes:** Configure a `GET` request to `{{baseUrl}}/api/login`. Assert status code is 4xx (404/405), response body does not contain `token`, and `pm.response.code` is not 200.

---

### TC-FR02-HUM-002: Advanced SQL Injection Multi-Vector Resilience Probe (Comment & Stacked Vector)
- **Test Case ID:** `FR02-HUM-002`
- **Title:** Advanced SQL Injection Multi-Vector Resilience Probe (Comment & Stacked Vector)
- **Source Gap:** `G-05` (SEC-05 Multi-Vector Injection Probes)
- **Student Rationale:** The original AI suite tested only simple `' OR '1'='1` tautology payloads. A single payload does not provide broad behavioral confidence against SQL injection attempts. Testing a distinct comment-truncation payload (`admin@eshop.com'--`) verifies parser resilience against multi-character injection patterns.
- **Why Existing AI Suite Missed This:** AI generated generic SQLi probes on email and password using the same tautological template without exploring alternative syntactic delimiters.
- **Technique:** SECURITY / BEHAVIORAL INJECTION PROBE
- **Requirement / Spec Basis:** 📋 [SRS §9 SEC-05] (Database queries must use parameterized queries)
- **Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED` / `SECURITY PROBE` (`SEC-05 PARTIAL BLACK-BOX EVIDENCE`)
- **Preconditions:** Seeded database with standard admin account (`admin@eshop.com`).
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Test Data:**
  ```json
  {
    "email": "admin@eshop.com'--",
    "password": "arbitrary_incorrect_password"
  }
  ```
- **Steps:** Submit login payload with comment-truncation vector in email field.
- **Expected HTTP Status:** `4xx` (`400 Bad Request` or `401 Unauthorized`; exact code is NOT SPECIFIED).
- **Expected Semantic Result:** Authentication must fail; the server must not bypass password verification, must not issue an administrative or user JWT, and must not disclose database error traces.
- **State Before:** `NORMAL`
- **State After:** `NORMAL` (or failure counter increments; does not bypass auth).
- **Oracle Confidence:** `PARTIAL`
- **Spec Limitations:** Black-box rejection provides behavioral resistance evidence only; proving parameterized queries across all backend paths requires source verification.
- **Postman Implementation Notes:** Assert `pm.response.code` is 4xx, `response.token` is undefined, and response body does not contain database error strings (`sqlite3`, `syntax error`, `ORA-`, `SQLSTATE`).

---

### TC-FR02-HUM-003: Consecutive Failure Counter Reset at N=2 Pre-Lockout Boundary via Successful Login
- **Test Case ID:** `FR02-HUM-003`
- **Title:** Consecutive Failure Counter Reset at N=2 Pre-Lockout Boundary via Successful Login
- **Source Gap:** `CUSTOM-G-09` (Successful Login Reset at N=2 Boundary)
- **Student Rationale:** The AI suite tested counter reset after one failed login (`FR02-AI-022`), but did not directly exercise the more critical threshold-adjacent state where the account already has two consecutive failed logins ($N=2$) before a successful authentication occurs.
- **Why Existing AI Suite Missed This:** AI generation created reset tests starting from $N=1$ and did not explore the $(N-1)$ critical boundary state immediately preceding lockout.
- **Technique:** STATE TRANSITION / BOUNDARY RESET TESTING
- **Requirement / Spec Basis:** 📋 [SRS §2 FR-02] (Successful authentication resets consecutive failed login counter to 0)
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Dedicated test account `human_reset@eshop.com` exists in `NORMAL` state.
- **Request Method / Sequence:**
  1. `POST /api/login` with wrong password (Attempt 1 $ightarrow$ Counter = 1, `NORMAL / FAILURE_SEQUENCE_ACTIVE`).
  2. `POST /api/login` with wrong password (Attempt 2 $ightarrow$ Counter = 2, $N=2$ Boundary, `UNLOCKED`).
  3. `POST /api/login` with correct password (Attempt 3 $ightarrow$ Authenticates successfully, returns 200 OK + JWT, **Resets Counter to 0**).
  4. `POST /api/login` with wrong password (Attempt 4 $ightarrow$ 1st failure of new sequence $ightarrow$ **Account must remain UNLOCKED**).
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Steps:** Execute steps 1 through 4 sequentially.
- **Expected HTTP Status:** Step 1: `4xx`, Step 2: `4xx`, Step 3: `200 OK`, Step 4: `4xx`.
- **Expected Semantic Result:** On Step 3, login succeeds with valid JWT. On Step 4, the single failure does NOT trigger lockout (account remains unlocked and accepts further logins).
- **State Before:** `NORMAL`
- **State After:** `FAILURE_SEQUENCE_ACTIVE` (Count = 1, NOT LOCKED).
- **Oracle Confidence:** `EXPLICIT`
- **Spec Limitations:** Tested purely via externally observable authentication states without relying on internal database counter inspection.
- **Postman Implementation Notes:** In collection runner, execute sequentially. After step 4, verify a valid login request succeeds, confirming the account is unlocked.

---

### TC-FR02-HUM-004: Account Lockout State Isolation Between Independent User Accounts
- **Test Case ID:** `FR02-HUM-004`
- **Title:** Account Lockout State Isolation Between Independent User Accounts
- **Source Gap:** `CUSTOM-G-10` (Account Lockout Isolation Between Different Users)
- **Student Rationale:** The AI suite tested lockout behavior on one dedicated account but never verified that one user's lock state does not incorrectly affect another independent account. Cross-account lock isolation is essential to ensure a denial-of-service against one account cannot impact other users.
- **Why Existing AI Suite Missed This:** AI generation focused on single-user lifecycle progression and omitted multi-principal isolation scenarios.
- **Technique:** SECURITY / STATE ISOLATION TESTING
- **Requirement / Spec Basis:** 📋 [SRS §2 FR-02] (Lockout applies to the specific account experiencing consecutive failed logins)
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Two distinct valid accounts exist: Account A (`lock_victim@eshop.com`) and Account B (`isolated_user@eshop.com`). Both start in `NORMAL` state.
- **Request Method / Sequence:**
  1. Send 3 consecutive failing logins to Account A (`POST /api/login`, wrong password $	imes 3$).
  2. Confirm Account A is in active `LOCKED` state (Attempt 4 to Account A is rejected with lockout message).
  3. Immediately send valid login for Account B (`POST /api/login`, correct credentials).
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127259`
- **Steps:** Execute steps 1, 2, and 3 sequentially.
- **Expected HTTP Status:** Step 1: `4xx` $	imes 3$, Step 2: `4xx` (Lockout rejection), Step 3: `200 OK`.
- **Expected Semantic Result:** Account A is successfully locked for 30 seconds. Account B is completely unaffected by Account A's lockout and successfully authenticates, receiving HTTP 200, a valid JWT, and Account B's user profile.
- **State Before:** Account A: `NORMAL`, Account B: `NORMAL`.
- **State After:** Account A: `LOCKED`, Account B: `NORMAL`.
- **Oracle Confidence:** `EXPLICIT`
- **Spec Limitations:** None; multi-tenant account isolation is fundamental to per-user authentication state models.
- **Postman Implementation Notes:** Assert Account A receives lockout error on request 4, while Account B receives `responseCode.code === 200` with non-empty `token` and `user.email === 'isolated_user@eshop.com'`.

---

### TC-FR02-HUM-005: Non-JSON Content-Type Request Contract Handling (`application/x-www-form-urlencoded`)
- **Test Case ID:** `FR02-HUM-005`
- **Title:** Non-JSON Content-Type Request Contract Handling (`application/x-www-form-urlencoded`)
- **Source Gap:** `G-08` (Content-Type MIME Negotiation Variants)
- **Student Rationale:** The original AI suite assumed `application/json` for normal authentication and tested malformed JSON, but did not test credentials supplied using an undocumented request encoding like `application/x-www-form-urlencoded`.
- **Why Existing AI Suite Missed This:** AI generation adhered strictly to documented JSON payloads and omitted non-JSON transport encoding boundaries.
- **Technique:** EXPLORATORY / API CONTRACT
- **Requirement / Spec Basis:** 🗂️ [API-SPEC §1.2] (Documents JSON API communication)
- **Oracle Classification:** `EXPLORATORY` / `API CONTRACT`
- **Preconditions:** Registered user exists.
- **Request Method:** `POST`
- **Endpoint:** `/api/login`
- **Headers:**
  - `Content-Type: application/x-www-form-urlencoded`
  - `X-Student-Id: 23127259`
- **Test Data:** `email=test%40eshop.com&password=Test1234!` (URL-encoded body string)
- **Steps:** Submit valid credentials formatted as urlencoded form data with `Content-Type: application/x-www-form-urlencoded`.
- **Expected HTTP Status:** `4xx` (`400 Bad Request`, `415 Unsupported Media Type`, or `401 Unauthorized`; exact code is NOT SPECIFIED).
- **Expected Semantic Result:** The server must NOT create an unintended authenticated session or return a valid authentication token unless form-encoding is formally supported. If unparsed, it must fail gracefully without unhandled 500 error.
- **State Before:** `NORMAL`
- **State After:** `NORMAL`
- **Oracle Confidence:** `PARTIAL`
- **Spec Limitations:** Exact status code (400 vs 415 vs 401) is not defined in `api_specification.md`; the reliable assertion is absence of an authenticated session.
- **Postman Implementation Notes:** In Postman, set body type to `x-www-form-urlencoded`. Assert response code is 4xx, and server does not return 500.
