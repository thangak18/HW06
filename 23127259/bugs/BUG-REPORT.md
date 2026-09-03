# HW06 Master Defect & Bug Tracking Report

- **Student:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`
- **Last Updated:** 2026-09-01 20:34:26+07:00

---

## 1. Feature FR-02: Login & Account Lockout (Pool A)

### 1.1 Confirmed Formal Specification / Contract Defects (3 Issues Filed)

#### 1. BUG-FR02-001: Sensitive Password Exposure in Successful Login Response
- **Severity:** **HIGH** (Information Disclosure / Sensitive Data Exposure)
- **Specification Basis:** `api_specification.md` §2.1 & [ADDITIONAL-SEC] (Response Data Sanitization / OWASP API3:2023)
- **Related Test Case:** `FR02-AI-028`
- **GitHub Issue:** [thangak18/HW06#1](https://github.com/thangak18/HW06/issues/1)
- **Screenshot Evidence:** [`screenshots/FR02/BUG-FR02-001-login-password-exposure.png`](screenshots/FR02/BUG-FR02-001-login-password-exposure.png)
- **Newman Evidence:** `23127259/newman/fr02/FR02-run-03.json` (`FR02-AI-028` assertion failure)
- **Reproduction Text:** [`evidence/FR02/BUG-FR02-001-reproduction.txt`](evidence/FR02/BUG-FR02-001-reproduction.txt)
- **Description:** A successful `POST /api/login` response exposes the user's plaintext password inside the `user` profile object (`user.password`), violating response sanitization and credential confidentiality.

---

#### 2. BUG-FR02-002: Account Remains Locked Beyond Documented 30-Second Lockout Duration
- **Severity:** **HIGH** (Denial of Service / Core Business Logic Violation)
- **Specification Basis:** EShop SRS §2 [FR-02] (Normative 30-Second Temporary Lockout)
- **Related Test Case:** `FR02-AI-021` (and `FR02-AI-024`)
- **GitHub Issue:** [thangak18/HW06#2](https://github.com/thangak18/HW06/issues/2)
- **Screenshot Evidence:** [`screenshots/FR02/BUG-FR02-002-lock-after-30s.png`](screenshots/FR02/BUG-FR02-002-lock-after-30s.png)
- **Newman Evidence:** `23127259/newman/fr02/FR02-run-03.json` (`FR02-AI-021` assertion failure)
- **Reproduction Text:** [`evidence/FR02/BUG-FR02-002-reproduction.txt`](evidence/FR02/BUG-FR02-002-reproduction.txt) (Elapsed time: 36.03s)
- **Description:** After entering the locked state upon 3 consecutive failures, the SUT fails to automatically unlock the account after 30 seconds. Submitting valid credentials at T = 36s continues to return HTTP 403 Forbidden indefinitely.

---

#### 3. BUG-FR02-003: Correct Login Rejected After Two Consecutive Failed Attempts
- **Severity:** **HIGH** (Authentication Flaw / Premature Account Lockout)
- **Specification Basis:** EShop SRS §2 [FR-02] (Consecutive Failure Reset at N=2 Pre-Lockout Boundary)
- **Related Test Case:** `FR02-HUM-003` (Student Human Extension)
- **GitHub Issue:** [thangak18/HW06#3](https://github.com/thangak18/HW06/issues/3)
- **Screenshot Evidence:** [`screenshots/FR02/BUG-FR02-003-correct-login-at-n2.png`](screenshots/FR02/BUG-FR02-003-correct-login-at-n2.png)
- **Newman Evidence:** `23127259/newman/fr02/FR02-run-03.json` (`FR02-HUM-003` assertion failure)
- **Reproduction Text:** [`evidence/FR02/BUG-FR02-003-reproduction.txt`](evidence/FR02/BUG-FR02-003-reproduction.txt)
- **Description:** When an account has 2 prior failed logins (N=2), submitting CORRECT credentials on the 3rd attempt causes the SUT to trigger lockout and return HTTP 403 Forbidden instead of logging in and resetting the failure sequence.

---

### 1.2 Exploratory / Robustness Observations (Not Filed as Spec Bugs)

#### OBS-FR02-001: Unhandled HTTP 500 on Non-Documented Form-Encoded Login Request
- **Severity:** **MEDIUM** (Robustness / Unhandled Exception)
- **Oracle Type:** Exploratory / Transport Robustness
- **Related Test Case:** `FR02-HUM-005`
- **GitHub Issue:** *Not Filed (Excluded per spec bug triage policy)*
- **Evidence Reference:** [`evidence/FR02/OBS-FR02-001-observation.txt`](evidence/FR02/OBS-FR02-001-observation.txt)
- **Description:** Sending `Content-Type: application/x-www-form-urlencoded` causes an unhandled 500 Internal Server Error in the backend middleware parser. Retained as an exploratory robustness finding.
