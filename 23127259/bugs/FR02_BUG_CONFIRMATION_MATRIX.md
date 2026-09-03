# FR-02 SUT Bug Confirmation & Triage Matrix

- **Feature Under Test:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

---

## 1. Master Bug Confirmation Matrix

| Candidate ID | Defect Title | Related Test | Oracle Type | Independent Repro Status | Final Classification | Severity | GitHub Issue Eligible? |
|:---:|---|:---:|---|:---:|---|:---:|:---:|
| **`BUG-FR02-001`** | Plaintext Password Exposure in Login Response JSON | `FR02-AI-028` | API Contract Specification + [ADDITIONAL-SEC] | **CONFIRMED** | Sensitive Data Exposure / Login Response Contract Violation | **HIGH** | **YES (Ready to File)** |
| **`BUG-FR02-002`** | Account Remains Locked Beyond Documented 30-Second Lockout Duration | `FR02-AI-021` | SRS §2 FR-02 (Normative Specification) | **CONFIRMED** | Core Specification Defect (State Machine / Lock Expiration) | **HIGH** | **YES (Ready to File)** |
| **`BUG-FR02-003`** | Premature Account Lockout on Valid Login Attempt at N=2 Boundary | `FR02-HUM-003` | SRS §2 FR-02 (Normative Specification) | **CONFIRMED** | Core Specification Defect (State Machine / Consecutive Counter Logic) | **HIGH** | **YES (Ready to File)** |
| **`OBS-FR02-001`** | Unhandled HTTP 500 on Non-Documented Form-Encoded Login Request | `FR02-HUM-005` | Exploratory / Transport Robustness | **REPRODUCED (OBSERVATION)** | Exploratory / Robustness Observation | **MEDIUM** | **NO (Downgraded - Not eligible as spec bug)** |

---

## 2. Summary of Triage Findings

| Classification Category | Count | IDs |
|---|:---:|---|
| **Confirmed Specification / API Contract Bugs** | **3** | `BUG-FR02-001`, `BUG-FR02-002`, `BUG-FR02-003` |
| **Exploratory Robustness Observations** | **1** | `OBS-FR02-001` |
| **Test Harness Failures (in Final Run 03)** | **0** | None (All 7 harness issues resolved in REP-001..007) |
| **Not Reproduced / Intermittent** | **0** | None (All findings 100% deterministically reproduced) |
| **Total Defect Candidates Triaged** | **4** | |
