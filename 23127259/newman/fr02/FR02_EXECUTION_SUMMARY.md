# FR-02 Newman Automated Test Execution Summary

- **Feature Under Test:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`
- **Target Environment:** Local Node.js SUT (`http://localhost:3000`)
- **Execution Date:** 2026-09-01 20:19:00+07:00
- **Runner:** Newman v6.2.2 + `newman-reporter-htmlextra` v1.23.1

---

## 1. Specification Oracle Invariant & Triage Principles

> [!IMPORTANT]
> **Oracle Preservation Invariant:**
> No audited oracle was weakened to make the SUT pass.
>
> The executable suite contains:
> - **Specification-backed assertions**
> - **Partially specification-backed security assertions**
> - **Exploratory / engineering assertions**
>
> Only failures with an explicit specification-backed oracle are eligible for formal specification bug filing.

---

## 2. Test Suite Accounting & Inventory Overview

| Category | Postman Requests | Formal Test Cases | Description / Purpose |
|---|:---:|:---:|---|
| **00 – Setup Helpers** | 8 | *0 (Excluded)* | Deterministic provisioning of run-isolated test user accounts |
| **01 – Positive Authentication** | 2 | 2 | Baseline user and administrator login contracts |
| **02 – Domain and Negative Inputs** | 10 | 10 | Equivalence partitions, missing fields, malformed formats |
| **03 – Lockout Boundary & State Progression** | 10 | 10 | N=1..3 thresholds, active lockout rejections, timing windows |
| **04 – Security and Token Integrity** | 7 | 7 | SQLi probes, response sanitization, downstream JWT usability |
| **05 – Schema and Contract Validation** | 6 | 6 | Response structure, error schema, JSON parser resilience |
| **06 – Human Extensions** | 5 | 5 | Student-designed gap coverage (verb enforcement, N=2 boundary, isolation, form encoding) |
| **TOTAL** | **48 requests** | **40 Formal Cases** | **35 Usable AI-Derived + 5 Human Extensions** |

---

## 3. Multi-Run Execution Progression & Request Reconciliation

In Newman Run 03, **56 total HTTP requests** were dispatched to execute the 40 formal test cases and 8 setup helpers. This includes 12 requests generated across 4 multi-step sequential test cases (`FR02-AI-022`, `FR02-AI-023`, `FR02-HUM-003`, `FR02-HUM-004`) via `pm.sendRequest` pre-request chaining. Detailed reconciliation is documented in [`FR02_RUN03_EXECUTION_COVERAGE.md`](file:///Volumes/Thang/HW06/HW06/23127259/newman/fr02/FR02_RUN03_EXECUTION_COVERAGE.md).

### Run Comparison Table

| Metric | Run 01 (`FR02-run-01`) | Run 02 (`FR02-run-02`) | Run 03 (`FR02-run-03`) |
|---|:---:|:---:|:---:|
| **Total Requests Executed** | 22 (pre-timeout) | 56 | **56** |
| **Formal Test Cases Executed** | 17 / 40 | 40 / 40 | **40 / 40 (100.0%)** |
| **Total Assertions** | 38 | 70 | **71** |
| **Passed Assertions** | 32 | 64 | **67** |
| **Failed Assertions** | 6 (5 harness + timeout) | 6 (2 harness + 4 defects) | **4 (0 harness defects)** |
| **Assertion Pass Rate** | 84.2% | 91.4% | **94.4%** |
| **Run Duration** | Timeout @ 30s | 32.6s | **32.7s** |

---

## 4. Post-Execution Triage & Classification

```
Newman Run 03 Failed Assertions: 4
  |
  +--> Confirmed Specification / API Contract Bugs: 3
  |      - BUG-FR02-001 (FR02-AI-028): Plaintext Password Disclosed in Response
  |      - BUG-FR02-002 (FR02-AI-021): Account Remains Locked Beyond 30s Window
  |      - BUG-FR02-003 (FR02-HUM-003): Premature Lockout on Valid Login at N=2
  |
  +--> Exploratory / Robustness Observations: 1
  |      - OBS-FR02-001 (FR02-HUM-005): HTTP 500 on form-urlencoded (Not eligible for spec bug)
  |
  +--> Test Harness Failures: 0 (Clean test harness verified)
  +--> Not Reproduced: 0 (100% deterministic reproducibility)
```

---

## 5. Summary of Confirmed SUT Bug Candidates & Exploratory Findings

| Defect / Observation ID | Title | Severity | Oracle Basis | GitHub Issue Status |
|---|---|:---:|---|:---:|
| **`BUG-FR02-001`** | Plaintext Password Disclosed in Successful Login Response Profile | **HIGH** | API Contract + [ADDITIONAL-SEC] | **ELIGIBLE – READY TO FILE** |
| **`BUG-FR02-002`** | Account Remains Locked Beyond Documented 30-Second Lockout Duration | **HIGH** | SRS §2 FR-02 | **ELIGIBLE – READY TO FILE** |
| **`BUG-FR02-003`** | Premature Account Lockout on Valid Login Attempt at N=2 Boundary | **HIGH** | SRS §2 FR-02 | **ELIGIBLE – READY TO FILE** |
| **`OBS-FR02-001`** | Unhandled HTTP 500 on Non-Documented Form-Encoded Login Request | **MEDIUM** | Exploratory / Transport Robustness | **DOWNGRADED (Not eligible by default)** |

---

## 6. Execution Artifact References
- **Execution Coverage Reconciliation:** [`FR02_RUN03_EXECUTION_COVERAGE.md`](file:///Volumes/Thang/HW06/HW06/23127259/newman/fr02/FR02_RUN03_EXECUTION_COVERAGE.md)
- **Bug Confirmation Matrix:** [`../../bugs/FR02_BUG_CONFIRMATION_MATRIX.md`](file:///Volumes/Thang/HW06/HW06/23127259/bugs/FR02_BUG_CONFIRMATION_MATRIX.md)
- **Issue Drafts Directory:** [`../../bugs/issues/`](file:///Volumes/Thang/HW06/HW06/23127259/bugs/issues/)
- **Reproduction Evidence Directory:** [`../../bugs/evidence/FR02/`](file:///Volumes/Thang/HW06/HW06/23127259/bugs/evidence/FR02/)
- **Newman Console Output:** [`FR02-run-03-console.txt`](file:///Volumes/Thang/HW06/HW06/23127259/newman/fr02/FR02-run-03-console.txt)
- **Newman JSON Export:** [`FR02-run-03.json`](file:///Volumes/Thang/HW06/HW06/23127259/newman/fr02/FR02-run-03.json)
- **Newman HTML Report:** [`FR02-run-03.html`](file:///Volumes/Thang/HW06/HW06/23127259/newman/fr02/FR02-run-03.html)
