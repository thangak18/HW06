# FR-02 SUT Bug Candidates & Triage Catalog

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`
- **Execution Run Reference:** `FR02-run-03`

---

## 1. Specification Oracle Invariant & Triage Principles

> [!IMPORTANT]
> **Oracle Preservation Invariant:**
> No audited oracle was weakened to make the SUT pass.
>
> The executable suite contains:
> - **Specification-backed assertions** (grounded in normative SRS §2 FR-02 and `api_specification.md`)
> - **Partially specification-backed security assertions** (grounded in standard API data sanitization and SEC guidelines)
> - **Exploratory / engineering robustness assertions** (grounded in HTTP/parser robustness)
>
> Only failures with an explicit specification-backed oracle are eligible for formal specification bug filing.

---

## 2. Summary of Triaged Defect Candidates

| Candidate ID | Defect Title | Severity | Relevant Test Case | Oracle Basis | Final Triage Status |
|---|---|:---:|:---:|---|:---:|
| **`BUG-FR02-001`** | Plaintext Password Disclosed in Login Response JSON | **HIGH** | `FR02-AI-028` | API Contract Specification + [ADDITIONAL-SEC] | **CONFIRMED SPEC BUG** (Ready to File) |
| **`BUG-FR02-002`** | Account Remains Locked Beyond Documented 30-Second Lockout Duration | **HIGH** | `FR02-AI-021` | SRS §2 FR-02 (Normative Specification) | **CONFIRMED SPEC BUG** (Ready to File) |
| **`BUG-FR02-003`** | Premature Account Lockout on Valid Login Attempt at N=2 Boundary | **HIGH** | `FR02-HUM-003` | SRS §2 FR-02 (Normative Specification) | **CONFIRMED SPEC BUG** (Ready to File) |
| **`OBS-FR02-001`** | Unhandled HTTP 500 on Non-Documented Form-Encoded Login Request | **MEDIUM** | `FR02-HUM-005` | Exploratory / Transport Robustness | **EXPLORATORY OBSERVATION** (Not eligible for spec bug) |

---

## 3. Detailed Triaged Defect Reports

### BUG-FR02-001: Plaintext Password Disclosed in Successful Login Response
- **Candidate ID:** `BUG-FR02-001`
- **Test ID:** `FR02-AI-028`
- **Severity:** **HIGH** (Information Disclosure / Sensitive Data Exposure)
- **Oracle Basis:** `api_specification.md` specifies `user` profile attributes (`id`, `name`, `email`, `role`) and does not document password. Disclosing plaintext passwords violates fundamental response data sanitization principles.
- **Observed Behavior:** `POST /api/login` returns HTTP 200 with `"password": "User1234!"` inside `response.user`.
- **Status:** **CONFIRMED SPEC/CONTRACT DEFECT**. Issue draft: [`issues/BUG-FR02-001.md`](issues/BUG-FR02-001.md).

---

### BUG-FR02-002: Account Remains Locked Beyond Documented 30-Second Lockout Duration
- **Candidate ID:** `BUG-FR02-002`
- **Test ID:** `FR02-AI-021` (and `FR02-AI-024`)
- **Severity:** **HIGH** (Denial of Service / Core Business Logic Violation)
- **Oracle Basis:** SRS §2 FR-02: "If consecutive failed attempts >= 3, temporarily lock account for 30 seconds. After 30 seconds, the account must automatically unlock and accept authentication."
- **Observed Behavior:** Submitting valid credentials after waiting 36 seconds ($> 30	ext{s}$) continues returning HTTP 403 Forbidden (`{"error": "Tài khoản đã bị khóa. Vui lòng thử lại sau."}`).
- **Status:** **CONFIRMED SPEC DEFECT**. Issue draft: [`issues/BUG-FR02-002.md`](issues/BUG-FR02-002.md).

---

### BUG-FR02-003: Premature Account Lockout on Valid Login Attempt at N=2 Boundary
- **Candidate ID:** `BUG-FR02-003`
- **Test ID:** `FR02-HUM-003` (Student Human Extension)
- **Severity:** **HIGH** (Authentication Flaw / Premature Account Denial)
- **Oracle Basis:** SRS §2 FR-02: Lockout threshold is 3 CONSECUTIVE failed login attempts. Submitting correct credentials on request #3 after 2 prior failures ($N=2$) must succeed (HTTP 200 + JWT) and reset consecutive failure progression.
- **Observed Behavior:** SUT locks the account on the 3rd attempt even when valid credentials are submitted.
- **Status:** **CONFIRMED SPEC DEFECT**. Issue draft: [`issues/BUG-FR02-003.md`](issues/BUG-FR02-003.md).

---

### OBS-FR02-001: Unhandled HTTP 500 on Non-Documented Form-Encoded Login Request
- **Candidate ID:** `OBS-FR02-001` (formerly candidate BUG-FR02-004)
- **Test ID:** `FR02-HUM-005` (Student Human Extension)
- **Severity:** **MEDIUM** (Robustness / Parser Error)
- **Oracle Basis:** Exploratory / Transport Robustness. `api_specification.md` specifies JSON communication (`application/json`) but does not explicitly define mandatory status codes for form-encoded payloads.
- **Observed Behavior:** `POST /api/login` with `Content-Type: application/x-www-form-urlencoded` causes an unhandled 500 Internal Server Error.
- **Status:** **DOWNGRADED TO EXPLORATORY OBSERVATION** (Not eligible for formal spec-backed GitHub bug issue by default). Evidence preserved in [`evidence/FR02/OBS-FR02-001-observation.txt`](evidence/FR02/OBS-FR02-001-observation.txt).
