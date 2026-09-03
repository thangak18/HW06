# FR-10 HTTP Operation Inventory & Architecture (Per-Case Isolated)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Formal Executable Test Cases:** `46` (41 AI-Derived + 5 Human Extensions)

---

## 1. Request-Definition vs Runtime-HTTP Model

| Metric | Count | Description |
|---|:---:|---|
| **Formal Test Cases** | **`46`** | Authoritative audited & extended test suite (`41` AI-derived + `5` Human extensions) |
| **Authentication Helpers** | **`3`** | Top-level setup requests (`POST /api/auth/login` for Admin, User A, User B in Folder 00) |
| **Order Creation Setup Requests** | **`44`** | Co-located `POST /api/checkout` fixture creation requests (1 per real-order case; 2 for HUM-002) |
| **Prerequisite State Setup Calls** | **`31`** | Admin / User transitions establishing `confirmed`, `shipping`, `delivered`, `canceled` preconditions |
| **Formal Action / Verify Requests** | **`60`** | Standalone request items in collection folders 01..10 |
| **Total Collection Request Definitions** | **`138`** | Total standalone HTTP request items in the Postman collection |
| **Script-Triggered HTTP Calls (`pm.sendRequest`)** | **`36`** | Dynamic persistence verification GET queries executed inside atomic test scripts |
| **Expected Total Runtime HTTP Operations** | **`174`** | Total network calls executed during a full automated Newman collection run |

---

## 2. Accounting Summary
- Every real-order formal test case establishes its own fresh, isolated order fixture.
- Total HTTP operations: 3 auth helpers + 44 checkout creation calls + 31 prerequisite transition calls + 60 formal step items + 36 script-level persistence GETs = **174 total operations**.
- Formal Test Case count remains strictly **46**.
