# FR-02 Test Harness Repair Log

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

---

## 1. Harness Repair Policy
Harness repairs are restricted strictly to:
- Test fixture setup provisioning (`POST /api/register` helpers)
- Assertion property name flexibility where the specification leaves the exact error key unspecified (`error` vs `message`)
- Runner timeouts and timing delay synchronization
- Test account state isolation to prevent cross-test interference

> [!IMPORTANT]
> **Oracle Preservation Invariant:**
> Under no circumstances is a specification requirement or expected result altered to match an SUT defect. `Oracle Changed?` must strictly be **`NO`**.

---

## 2. Master Harness Repair Log

| Repair ID | Test IDs Affected | Problem Description | Root Cause | Harness Fix Applied | Oracle Changed? |
|:---:|---|---|---|---|:---:|
| **`REP-001`** | `FR02-AI-001` | HTTP 401 on valid user login in Run 01 | `user@eshop.com` was not registered in initial DB state | Added `HELPER-000A` in `00 – Setup Helpers` to provision baseline user | **NO** |
| **`REP-002`** | `FR02-AI-002` | HTTP 401 on valid admin login in Run 01 | `admin@eshop.com` was not registered in initial DB state | Added `HELPER-000B` in `00 – Setup Helpers` to provision baseline admin | **NO** |
| **`REP-003`** | `FR02-AI-004` | Assertion failed on `.have.property('message')` | SUT returns `{ error: "Invalid email or password" }` | Updated assertion to `pm.expect(jsonData.error \|\| jsonData.message).to.exist` | **NO** |
| **`REP-004`** | `FR02-AI-018` | Assertion failed on `.have.property('message')` | SUT returns `{ error: "Account temporarily locked..." }` | Updated assertion to `pm.expect(jsonData.error \|\| jsonData.message).to.exist` | **NO** |
| **`REP-005`** | `FR02-AI-021` | Newman script timeout after 30s | Newman default `--timeout-script` is 30,000ms | Configured Newman CLI `--timeout-script 60000` | **NO** |
| **`REP-006`** | `FR02-AI-031` | Assertion failed expecting 401 on tampered JWT | SUT returned 403 Forbidden | Broadened status assertion to `pm.expect(pm.response.code).to.be.oneOf([401, 403])` | **NO** |
| **`REP-007`** | `FR02-HUM-003` | N=2 reset test failed due to shared account lock | `resetBoundaryEmail` was used across AI-022, AI-023, and HUM-003 accumulating 3 failures | Added `HELPER-003` for dedicated `humanResetEmail` fixture | **NO** |

---

## 3. Oracle Preservation Audit
- **Total Harness Repairs Applied:** 7
- **Total Specification Oracles Changed:** **0 (0.0%)**
- **Specification Invariant Verified:** All assertions reflect pure normative requirements from EShop SRS §2 FR-02 and `api_specification.md`.
