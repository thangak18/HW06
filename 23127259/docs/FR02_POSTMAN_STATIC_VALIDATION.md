# FR-02 Postman Collection Static Validation Report

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`
- **Collection File:** `postman/collections/FR02_Login_Account_Lockout.postman_collection.json`
- **Environment File:** `postman/environments/FR02-local.postman_environment.json`

> [!IMPORTANT]
> **Execution Gate Statement:**
> **NO SUT EXECUTION WAS PERFORMED IN THIS PHASE.**
> This report documents non-execution static validation results including JSON schema validity, request-to-testcase mapping completeness, duplicate exclusion, and header enforcement.

---

## 1. Static Validation Metric Summary

| Validation Check | Expected Criterion | Observed Value | Status |
|---|---|:---:|:---:|
| **Collection JSON Syntax** | Well-formed JSON | Valid (Parses without error) | **PASS** |
| **Environment JSON Syntax** | Well-formed JSON | Valid (Parses without error) | **PASS** |
| **Total Postman Requests** | 44 (40 formal + 4 setup) | 44 requests | **PASS** |
| **Helper Setup Requests** | 4 setup helpers | 4 helpers | **PASS** |
| **Formal Test Case Requests** | Exactly 40 executable cases | 40 formal cases | **PASS** |
| **AI-Derived Mapped Cases** | Exactly 35 cases | 35 cases | **PASS** |
| **Human Extension Mapped Cases** | Exactly 5 cases (`FR02-HUM-001..005`) | 5 cases | **PASS** |
| **Unique Formal Testcase IDs** | 40 unique IDs (0 duplicates) | 40 unique IDs | **PASS** |
| **Exclusion of `FR02-AI-016`** | Absent from executable collection | Absent (`has_016 = False`) | **PASS** |
| **Exclusion of `FR02-AI-017`** | Absent from executable collection | Absent (`has_017 = False`) | **PASS** |
| **`X-Student-Id` Enforcement** | Injected on all requests via Pre-request | Enforced (Collection-level + Headers) | **PASS** |
| **Hardcoded Live JWTs** | Zero hardcoded JWT tokens in JSON | 0 tokens (Uses `{{userToken}}`) | **PASS** |
| **SUT Execution Performed** | None (Static check only) | **NO EXECUTION PERFORMED** | **PASS** |

---

## 2. Folder-by-Folder Structural Breakdown

| Folder Name | Helper Requests | Formal Test Cases | Mapped Testcase IDs |
|---|:---:|:---:|---|
| `00 – Setup Helpers` | 4 | 0 | `HELPER-001` .. `HELPER-004` (Excluded from test suite count) |
| `01 – Positive Authentication` | 0 | 2 | `FR02-AI-001`, `FR02-AI-002` |
| `02 – Domain and Negative Inputs` | 0 | 10 | `FR02-AI-003` .. `FR02-AI-012` |
| `03 – Lockout Boundary and State Progression` | 0 | 10 | `FR02-AI-013` .. `FR02-AI-015`, `FR02-AI-018` .. `FR02-AI-024` |
| `04 – Security and Token Integrity` | 0 | 7 | `FR02-AI-025` .. `FR02-AI-031` |
| `05 – Schema and Contract Validation` | 0 | 6 | `FR02-AI-032` .. `FR02-AI-037` |
| `06 – Human Extensions` | 0 | 5 | `FR02-HUM-001` .. `FR02-HUM-005` |
| **TOTAL** | **4** | **40** | **40 Unique Executable Test Cases** |
