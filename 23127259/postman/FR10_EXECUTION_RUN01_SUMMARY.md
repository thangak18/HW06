# FR-10 Newman Run 01 Execution Summary (Corrected)

> **RUN 01 DERIVED ANALYSIS CORRECTED AFTER HUMAN REVIEW**

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

## 3. Corrected Formal Case Reconciliation

- **Formal Executable Test Cases:** **`46`** (41 AI + 5 HUM; AI-012 excluded)
- **`PASS`:** `0` (Zero cases had verified preconditions)
- **`BLOCKED – HARNESS/SETUP`:** `46` (All cases blocked by setup auth failure)
- **`EXPLORATORY OBSERVATION`:** `0` (Exploratory cases HUM-004/005 blocked by setup)
- **`FAIL – EXPECTED ORACLE VIOLATION`:** `0` (Zero genuine SUT bugs declared in Run 01)

---

## 4. Next Action Recommendation

- **Verdict:** **`HARNESS_REPAIR_REQUIRED`**
- **Required Repair:** Update the 3 login helper request URLs in Folder 00 from `/api/auth/login` to `/api/login` so that JWT bearer tokens are cleanly extracted into `adminToken`, `userAToken`, and `userBToken`.
- **Protocol Discipline:** Run 01 raw evidence remains immutable. The harness repair and subsequent execution will occur in Phase 2D.1D (Newman Run 02).
