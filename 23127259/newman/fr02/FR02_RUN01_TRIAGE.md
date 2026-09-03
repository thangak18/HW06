# FR-02 Newman Execution Run 01 Triage Report

- **Run ID:** `FR02-run-01`
- **Execution Date/Time:** 2026-09-01 20:13:00+07:00
- **Collection:** `23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json`
- **Environment:** `23127259/postman/environments/FR02-local.postman_environment.json`
- **Target SUT:** `http://localhost:3000`

---

## 1. Run 01 Failure Triage Table

| Test ID | Result | Actual Behavior | Expected Oracle | Classification | Evidence | Action |
|---|:---:|---|---|:---:|---|---|
| `FR02-AI-001` | **FAIL** | HTTP 401 `{"error": "Invalid email or password"}` | HTTP 200 OK + JWT token | **TEST HARNESS FAILURE** | `user@eshop.com` was not registered in setup helpers prior to execution. | Add `HELPER-000A` in setup folder to provision `user@eshop.com`. |
| `FR02-AI-002` | **FAIL** | HTTP 401 `{"error": "Invalid email or password"}` | HTTP 200 OK + admin JWT | **TEST HARNESS FAILURE** | `admin@eshop.com` was not registered in setup helpers prior to execution. | Add `HELPER-000B` in setup folder to provision `admin@eshop.com`. |
| `FR02-AI-004` | **FAIL** | Response contained `error: "Invalid email or password"` | Generic failure response | **TEST HARNESS FAILURE** | Test script asserted `jsonData.message` instead of `jsonData.error \|\| jsonData.message`. | Update assertion to accept `error` or `message` property. |
| `FR02-AI-018` | **FAIL** | Response contained `error: "Account temporarily locked..."` | Lockout failure response | **TEST HARNESS FAILURE** | Test script asserted `jsonData.message` instead of `jsonData.error \|\| jsonData.message`. | Update assertion to accept `error` or `message` property. |
| `FR02-AI-021` | **TIMEOUT** | Script execution timed out after 30000ms | 200 OK after 30s expiration | **TEST HARNESS FAILURE** | Newman default script timeout is 30s; 32s delay exceeded sandbox limit. | Pass `--script-timeout 60000` to Newman and use non-blocking timing loop. |

---

## 2. Summary of Run 01 Classifications
- **Total Executed Formal Requests (pre-timeout):** 22
- **Passes:** 17
- **Test Harness Failures:** 5
- **Bug Candidates Identified in Run 01:** 0 (All 5 failures were harness issues)
- **Specification Oracles Changed:** **NONE (0%)**
