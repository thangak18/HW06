# FR-10 Newman Run 01 Execution Summary

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature Under Test:** FR-10 – Order Status & State Machine (Pool B)
- **Execution Date:** 2026-09-01
- **Commit Under Test:** `aef0ef7`
- **Target SUT:** `http://localhost:3000` (Node/Express backend)
- **Run Verdict:** **`HARNESS_REPAIR_REQUIRED`**

---

## 1. Execution Command & Environment

```bash
npx newman run /Volumes/Thang/HW06/HW06/23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json \
  -e /Volumes/Thang/HW06/HW06/23127259/postman/environments/FR10-local.postman_environment.json \
  -r cli,json,htmlextra \
  --reporter-json-export /Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01.json \
  --reporter-htmlextra-export /Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01.html | tee /Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01-cli.txt
```

- **Newman Version:** `6.2.2`
- **Exit Code:** `1` (due to assertion failures caused by unpopulated setup tokens)
- **Runtime Duration:** `1.57s` (Started: `1788278202237`, Completed: `1788278203804`)

---

## 2. Quantitative Operation & Assertion Metrics

| Metric Category | Total Executions | Passed | Failed / Errors | Notes |
|---|:---:|:---:|:---:|---|
| **Iterations** | `1` | `1` | `0` | Single controlled baseline run |
| **Collection Request Items** | `139` | `139` | `0` | 4 setup helpers + 135 formal step items |
| **Script-Triggered Requests** | `36` | `36` | `0` | Handled via `pm.sendRequest` in test scripts |
| **Total HTTP Requests Sent** | **`175`** | `175` | `0` | Zero network connection/timeout errors |
| **Prerequest & Test Scripts** | `322` | `322` | `0` | Header injection and token extraction executed |
| **Assertions Evaluated** | **`175`** | **`45`** | **`130`** | 130 failed due to unauthenticated setup requests |

---

## 3. Formal Case Reconciliation

- **Formal Executable Test Cases:** **`46`** (41 AI + 5 HUM; AI-012 excluded)
- **PASS:** `2` (Pre-auth / Unauthenticated SEC-02 negative probes that expected 401)
- **BLOCKED – HARNESS/SETUP:** `42`
- **EXPLORATORY OBSERVATION:** `2` (`FR10-HUM-004`, `FR10-HUM-005`)
- **FAIL – EXPECTED ORACLE VIOLATION:** `0` (Zero genuine SUT bugs confirmed in Run 01)

---

## 4. Security & Exploratory Case Observations

1. **SEC-02 Authentication Invariants (`FR10-AI-025..029`):**
   - Unauthenticated probes correctly observed HTTP 401 rejection.
2. **SEC-03 RBAC Probes (`FR10-AI-030..032`):**
   - Blocked by lack of setup tokens; to be formally evaluated in Run 02 once tokens propagate.
3. **Cross-User Ownership Probes (`FR10-AI-033..034`):**
   - Blocked by lack of setup tokens.
4. **SEC-05 Injection Defense (`FR10-AI-042`):**
   - Blocked by setup.
5. **Human Extensions (`FR10-HUM-001..005`):**
   - Step definitions successfully executed; order mutations blocked by missing setup tokens.

---

## 5. Next Action Recommendation

- **Verdict:** **`HARNESS_REPAIR_REQUIRED`**
- **Required Repair:** Update the 3 login helper request URLs in Folder 00 from `/api/auth/login` to `/api/login` so that JWT bearer tokens are cleanly extracted into `adminToken`, `userAToken`, and `userBToken`.
- **Protocol Discipline:** Run 01 is preserved verbatim. The harness repair and subsequent execution will occur in Phase 2D.1C / Run 02 in a dedicated follow-up interaction.
