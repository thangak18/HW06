# FR-02 Human-Designed Extension Workspace

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

---

## 1. Purpose & Student Governance

The purpose of this workspace is to identify specification-relevant testing dimensions and coverage gaps not fully addressed by the **35 usable AI-derived test cases** (`FR02-AI-001` .. `FR02-AI-037`, excluding rejected duplicates `FR02-AI-016` and `FR02-AI-017`).

> [!NOTE]
> **Provenance Statement:**
> These extension directions were selected and finalized by the student after reviewing the completed AI-generated suite, Human Audit results, and an AI-assisted coverage-gap analysis. They are intentionally separated from the raw AI-generated `FR02-AI` inventory.

---

## 2. Existing Post-Audit Coverage Matrix

The following matrix reflects the 35 usable AI-derived test cases following the completed student Human Audit:

| Requirement / Dimension | Existing Usable AI Cases | Coverage Level | Evidence / Spec Basis |
|---|---|:---:|---|
| **Successful User Authentication** | `FR02-AI-001` | `COVERED` | 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2] (200 OK + JWT + profile) |
| **Successful Admin Authentication** | `FR02-AI-002` | `COVERED` | 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2] (200 OK + admin JWT) |
| **Invalid Password on Registered Email** | `FR02-AI-003` | `COVERED` | 📋 [SRS §2 FR-02] (Generic error + 1st failure increment) |
| **Unregistered Syntactically Valid Email** | `FR02-AI-004` | `COVERED` | 📋 [SRS §2 FR-02] (Generic error anti-enumeration) |
| **Email Domain Partitions (Malformed/Empty/Whitespace)** | `FR02-AI-005`, `FR02-AI-006`, `FR02-AI-009` | `COVERED` | 📋 [SRS §2 FR-02] (Authentication non-success assertions) |
| **Missing / Null Email Payload Fields** | `FR02-AI-007`, `FR02-AI-008` | `COVERED` | 🗂️ [API-SPEC §1.2] (Transport / Schema robustness) |
| **Password Domain Partitions (Empty/Missing/Null)** | `FR02-AI-010`, `FR02-AI-011`, `FR02-AI-012` | `COVERED` | 📋 [SRS §2 FR-02] & 🗂️ [API-SPEC §1.2] (Auth non-success) |
| **Failure Progression: N=1** | `FR02-AI-015` | `COVERED` | 📋 [SRS §2 FR-02] (Counter increment, remains unlocked) |
| **Failure Progression: Boundary N=2** | `FR02-AI-013` | `COVERED` | 📋 [SRS §2 FR-02] (Boundary N-1, remains unlocked) |
| **Lockout Threshold: Boundary N=3** | `FR02-AI-014` | `COVERED` | 📋 [SRS §2 FR-02] (Transition to LOCKED state) |
| **Active Lockout Window Rejection (Wrong Credentials)** | `FR02-AI-018` | `COVERED` | 📋 [SRS §2 FR-02] (Temporary lock rejection) |
| **Active Lockout Window Rejection (Valid Credentials)** | `FR02-AI-019` | `COVERED` | 📋 [SRS §2 FR-02] (Valid credentials cannot bypass lock) |
| **Lockout Duration Timing: Pre-Expiry (T=25s)** | `FR02-AI-020` | `COVERED` | 📋 [SRS §2 FR-02] (Account remains locked at T < 30s) |
| **Lockout Duration Timing: Post-Expiry (T=32s)** | `FR02-AI-021` | `COVERED` | 📋 [SRS §2 FR-02] (Automatic unlock after 30s window) |
| **Successful-Login Reset Rule** | `FR02-AI-022` | `COVERED` | 📋 [SRS §2 FR-02] (Valid login resets failure counter to 0) |
| **Consecutive-Failure Semantics** | `FR02-AI-023` | `COVERED` | 📋 [SRS §2 FR-02] (Interleaved success prevents lockout) |
| **Post-Lockout Expiration Usability & Reset** | `FR02-AI-024` | `COVERED` | 📋 [SRS §2 FR-02] (Post-unlock login resets counter) |
| **SQL Injection Behavioral Probes (Email/Password)** | `FR02-AI-025`, `FR02-AI-026` | `PARTIALLY COVERED` | 📋 [SRS §9 SEC-05] (Probes show behavioral resistance; does not prove DB parameterization) |
| **Account Enumeration / Error Text Equivalence** | `FR02-AI-027` | `COVERED` | 📋 [SRS §2 FR-02] (Cross-response generic error equality) |
| **Sensitive Data Response Sanitization** | `FR02-AI-028` | `COVERED` | `[ADDITIONAL-SEC]` (Password omitted from JSON response) |
| **SEC-01 Password Storage at Rest** | None | `PARTIALLY COVERED` | 📋 [SRS §9 SEC-01] (Black-box API cannot directly inspect DB hash representation) |
| **Token Absence / Non-Usability on Failure** | `FR02-AI-029` | `COVERED` | 📋 [SRS §2 FR-02] (No usable session issued on 4xx) |
| **Downstream JWT Usability & Tamper Resistance** | `FR02-AI-030`, `FR02-AI-031` | `COVERED` | 📋 [SRS §9 SEC-02] (Indirect token verification on protected route) |
| **Success / Generic Error JSON Schema Contracts** | `FR02-AI-032`, `FR02-AI-033` | `COVERED` | 🗂️ [API-SPEC §1.2] (Type and field structural assertions) |
| **Lockout Error Structure & Non-Disclosure** | `FR02-AI-034` | `COVERED` | 📋 [SRS §2 FR-02] (Lockout response without internal leakage) |
| **Malformed JSON & Transport Contracts** | `FR02-AI-035`, `FR02-AI-036`, `FR02-AI-037` | `COVERED` | 🗂️ [API-SPEC §1.2] (Parser resilience, headers, extra fields) |

---

## 3. Candidate Coverage Gaps for Student Review

### A. Specification-Backed Coverage Gaps

#### Gap G-01: Email Case-Insensitive Normalization
- **Requirement / Dimension:** Email Input Normalization
- **Current Coverage:** `NOT COVERED`
- **Specification Basis:** 📋 [SRS §2 FR-02] & RFC 5321 standard practices.
- **Why Existing AI Cases Do Not Fully Cover It:** AI generated domain partitions for format, whitespace, empty, and null strings, but all positive/negative authentication cases used strictly lowercase emails (`user@eshop.com`). Login behavior when uppercase or mixed-case email characters are submitted is unrepresented.
- **Student Design Status:** `RESERVED / NOT SELECTED FOR BATCH 1C`

#### Gap G-02: HTTP Method & Route Enforcement on Login Endpoint
- **Requirement / Dimension:** HTTP Verb Dispatching (`GET`, `PUT`, `DELETE` on `/api/login`)
- **Current Coverage:** `NOT COVERED`
- **Specification Basis:** 🗂️ [API-SPEC §1.2] explicitly specifies `POST /api/login`.
- **Why Existing AI Cases Do Not Fully Cover It:** All 37 AI test cases exclusively invoked `POST`. The behavior of the login route when non-POST methods are dispatched was completely omitted.
- **Student Design Status:** **`STUDENT SELECTED / FINALIZED` $ightarrow$ `FR02-HUM-001`**

#### Gap G-03: Lockout Boundary Timing Edge Condition ($T=30.0	ext{s}$)
- **Requirement / Dimension:** Lockout Duration Boundary Precision
- **Current Coverage:** `PARTIALLY COVERED`
- **Specification Basis:** 📋 [SRS §2 FR-02] mandates a 30-second lockout duration.
- **Why Existing AI Cases Do Not Fully Cover It:** AI generated $T=25	ext{s}$ (`FR02-AI-020`) and $T=32	ext{s}$ (`FR02-AI-021`), which comfortably bracket the 30-second window. The immediate boundary behavior right around the expiration point was not probed.
- **Student Design Status:** `RESERVED`

#### Gap G-04: SEC-01 Password Storage at Rest Verification Boundary
- **Requirement / Dimension:** SEC-01 Database Password Hashing
- **Current Coverage:** `PARTIALLY COVERED`
- **Specification Basis:** 📋 [SRS §9 SEC-01] mandates that passwords must not be stored in plaintext.
- **Why Existing AI Cases Do Not Fully Cover It:** AI test `FR02-AI-028` inspected only the HTTP response JSON. Black-box API tests cannot inspect the database table directly; storage-at-rest compliance requires supplemental database/source verification.
- **Student Design Status:** `RESERVED`

#### Gap G-05: SEC-05 Multi-Vector Parameterized Query Injection Probes
- **Requirement / Dimension:** SEC-05 Parameterized Query Behavioral Resistance
- **Current Coverage:** `PARTIALLY COVERED`
- **Specification Basis:** 📋 [SRS §9 SEC-05] mandates parameterized queries for all database interactions.
- **Why Existing AI Cases Do Not Fully Cover It:** AI generated single-quote tautology payloads (`' OR '1'='1`). More sophisticated SQL injection vectors (e.g. comment-truncation delimiters `admin'--`) were not explored.
- **Student Design Status:** **`STUDENT SELECTED / FINALIZED` $ightarrow$ `FR02-HUM-002`**

#### Custom Gap CUSTOM-G-09: Successful Login Reset at N=2 Pre-Lockout Boundary
- **Requirement / Dimension:** Reset Rule at Critical $(N-1)$ Boundary
- **Current Coverage:** `NOT COVERED`
- **Specification Basis:** 📋 [SRS §2 FR-02] (Successful login resets consecutive failure counter to 0).
- **Why Existing AI Cases Do Not Fully Cover It:** AI tested reset after $N=1$ (`FR02-AI-022`), but omitted the critical threshold-adjacent state where the account already has two consecutive failures before reset.
- **Student Design Status:** **`STUDENT SELECTED / FINALIZED` $ightarrow$ `FR02-HUM-003`**

#### Custom Gap CUSTOM-G-10: Account Lockout State Isolation Between Independent Users
- **Requirement / Dimension:** Multi-User Lockout Isolation
- **Current Coverage:** `NOT COVERED`
- **Specification Basis:** 📋 [SRS §2 FR-02] (Lockout applies to the specific account experiencing consecutive failed logins).
- **Why Existing AI Cases Do Not Fully Cover It:** AI suite tested lockout behavior exclusively on a single dedicated account without verifying cross-account lock isolation.
- **Student Design Status:** **`STUDENT SELECTED / FINALIZED` $ightarrow$ `FR02-HUM-004`**

---

### B. Exploratory / Engineering Opportunities

#### Gap G-06: Concurrency & Race Condition on Consecutive Failure Accumulation
- **Requirement / Dimension:** Concurrent Request Synchronization
- **Current Coverage:** `NOT COVERED`
- **Specification Basis:** 📋 [SRS §2 FR-02] (consecutive failure progression).
- **Why Existing AI Cases Do Not Fully Cover It:** AI generated purely sequential single-request test cases. Near-simultaneous login requests on the same account to test failure counter race conditions were omitted.
- **Student Design Status:** `RESERVED`

#### Gap G-07: Payload Size / Large Input Resilience
- **Requirement / Dimension:** Transport Robustness & Buffer Handling
- **Current Coverage:** `NOT COVERED`
- **Specification Basis:** 🗂️ [API-SPEC §1.2] (JSON payload handling).
- **Why Existing AI Cases Do Not Fully Cover It:** AI tested short strings and standard inputs; extremely large payload bodies were not generated.
- **Student Design Status:** `RESERVED`

#### Gap G-08: Content-Type Header Negotiation Variants (`application/x-www-form-urlencoded`)
- **Requirement / Dimension:** MIME Type Handling
- **Current Coverage:** `PARTIALLY COVERED`
- **Specification Basis:** 🗂️ [API-SPEC §1.2] requires JSON communication.
- **Why Existing AI Cases Do Not Fully Cover It:** AI tested malformed JSON syntax but did not test sending valid credentials formatted as form-urlencoded data to verify strict Content-Type enforcement.
- **Student Design Status:** **`STUDENT SELECTED / FINALIZED` $ightarrow$ `FR02-HUM-005`**

---

## 4. Student-Selected Human Extensions (Finalized Selections)

### HUMAN SLOT 1 $ightarrow$ `FR02-HUM-001`
- **Assigned ID:** `FR02-HUM-001`
- **Selected Gap ID:** `G-02` (HTTP Method Enforcement on `/api/login`)
- **Why I selected this gap:** The documented login operation uses POST. The original AI suite tested only POST and never checked whether unsupported HTTP methods can accidentally invoke authentication behavior.
- **My Test Objective:** Verify that `/api/login` cannot successfully authenticate a user when invoked through an HTTP method (`GET`) that is not documented for the login operation.
- **My Test Data:** Method: `GET`, URL: `/api/login`
- **My Preconditions:** Registered user exists in database.
- **My Steps:** Dispatch an HTTP `GET` request to `/api/login`.
- **My Expected Result:** Status `4xx` (404/405; NOT SPECIFIED); authentication logic does not execute, no JWT token issued.
- **Why AI missed this:** AI generated tests exclusively using the documented HTTP verb and omitted negative method dispatching.
- **Design Status:** `STUDENT SELECTED / FINALIZED`

---

### HUMAN SLOT 2 $ightarrow$ `FR02-HUM-002`
- **Assigned ID:** `FR02-HUM-002`
- **Selected Gap ID:** `G-05` (SEC-05 Multi-Vector Injection Probes)
- **Why I selected this gap:** The original AI suite tested only simple classic SQL injection strings (`' OR '1'='1`). A single payload does not provide broad behavioral confidence against SQL injection attempts.
- **My Test Objective:** Use a meaningfully different SQL-injection-style input pattern (comment delimiter `admin@eshop.com'--`) and verify that it cannot bypass authentication or obtain an unauthorized authenticated session.
- **My Test Data:** `{"email": "admin@eshop.com'--", "password": "arbitrary_incorrect_password"}`
- **My Preconditions:** Admin account exists.
- **My Steps:** Submit login payload with comment-truncation vector in email field.
- **My Expected Result:** Status `4xx`; authentication fails, no admin JWT issued, no database error disclosure.
- **Why AI missed this:** AI generated standard tautological payloads without exploring alternative syntactic delimiters.
- **Design Status:** `STUDENT SELECTED / FINALIZED`

---

### HUMAN SLOT 3 $ightarrow$ `FR02-HUM-003`
- **Assigned ID:** `FR02-HUM-003`
- **Selected Gap ID:** `CUSTOM-G-09` (Successful Login Reset at N=2 Boundary)
- **Why I selected this gap:** The AI suite tested counter reset after one failed login, but did not directly exercise the more critical threshold-adjacent state where the account already has two consecutive failed logins before a successful authentication occurs.
- **My Test Objective:** Verify that a successful authentication occurring after exactly two consecutive failures resets the failure sequence before the N=3 lockout threshold can be reached.
- **My Test Data:** Sequence: 2 wrong logins $ightarrow$ 1 valid login $ightarrow$ 1 wrong login on dedicated test account `human_reset@eshop.com`.
- **My Preconditions:** Dedicated test account `human_reset@eshop.com` in `NORMAL` state.
- **My Steps:** Execute 2 wrong logins, 1 valid login, and 1 wrong login.
- **My Expected Result:** 3rd request succeeds (200 OK + JWT); 4th request fails but account remains UNLOCKED (does not trigger lockout).
- **Why AI missed this:** AI suite tested reset starting only from $N=1$ and omitted the $(N-1)$ critical boundary state.
- **Design Status:** `STUDENT SELECTED / FINALIZED`

---

### HUMAN SLOT 4 $ightarrow$ `FR02-HUM-004`
- **Assigned ID:** `FR02-HUM-004`
- **Selected Gap ID:** `CUSTOM-G-10` (Account Lockout Isolation Between Different Users)
- **Why I selected this gap:** The AI suite tested lockout behavior on one dedicated account but never verified that one user's lock state does not incorrectly affect another independent account.
- **My Test Objective:** Verify that placing Account A into the temporary locked state does not prevent a different valid Account B from authenticating normally.
- **My Test Data:** Account A (`lock_victim@eshop.com`, locked via 3 failures) and Account B (`isolated_user@eshop.com`, valid credentials).
- **My Preconditions:** Two distinct valid accounts exist in `NORMAL` state.
- **My Steps:** Trigger lockout on Account A (3 failures); confirm Account A is locked; submit valid credentials for Account B.
- **My Expected Result:** Account A is rejected with lockout error; Account B authenticates successfully (200 OK + JWT).
- **Why AI missed this:** AI generation focused on single-user lifecycle progression and omitted multi-principal isolation.
- **Design Status:** `STUDENT SELECTED / FINALIZED`

---

### HUMAN SLOT 5 $ightarrow$ `FR02-HUM-005`
- **Assigned ID:** `FR02-HUM-005`
- **Selected Gap ID:** `G-08` (Non-JSON Content-Type Request Contract)
- **Why I selected this gap:** The original AI suite assumed application/json for normal authentication and tested malformed JSON, but did not test credentials supplied using an undocumented request encoding.
- **My Test Objective:** Verify that using a non-documented Content-Type (`application/x-www-form-urlencoded`) cannot accidentally bypass the documented authentication contract or create an authenticated session.
- **My Test Data:** `email=test%40eshop.com&password=Test1234!` sent with `Content-Type: application/x-www-form-urlencoded`.
- **My Preconditions:** Registered user exists.
- **My Steps:** Submit valid credentials formatted as form-urlencoded string.
- **Expected Result:** Status `4xx` (NOT SPECIFIED); server must not create an unintended authenticated session or return a valid JWT.
- **Why AI missed this:** AI adhered strictly to documented JSON payloads and omitted non-JSON transport encoding boundaries.
- **Design Status:** `STUDENT SELECTED / FINALIZED`
