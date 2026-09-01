# FR-10 HTTP Operation Inventory & Architecture

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Formal Executable Test Cases:** `46` (41 AI-Derived + 5 Human Extensions)
- **Authentication Helpers:** `3`

---

## 1. Request-Definition vs Runtime-HTTP Model

| Metric | Count | Description |
|---|:---:|---|
| **Formal Test Cases** | **`46`** | Authoritative audited & extended test suite (`41` AI-derived + `5` Human extensions) |
| **Authentication Helpers** | **`3`** | Top-level setup requests (Admin Login, User A Login, User B Login) |
| **Collection Request Definitions** | **`63`** | Total standalone HTTP request items in the Postman collection |
| **Script-Triggered HTTP Calls (`pm.sendRequest`)** | **`36`** | Dynamic persistence verification GET queries executed inside test scripts for atomic cases |
| **Expected Total Runtime HTTP Operations** | **`99`** | Total network calls executed during a full automated Newman collection run |

---

## 2. Comprehensive Formal Case HTTP Operations Table

| Formal ID | Collection Request Definitions | Script-Triggered HTTP Calls | Setup Calls | Action Calls | Verify Calls | Expected Runtime HTTP Calls |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **`FR10-AI-001`** | 1 (`[FR10-AI-001]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-002`** | 1 (`[FR10-AI-002]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-003`** | 1 (`[FR10-AI-003]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-004`** | 4 (Step 1, Step 2, Step 3, Verify) | 0 | 0 | 3 (`PUT /status` x3) | 1 (`GET /orders/:id`) | **4** |
| **`FR10-AI-005`** | 1 (`[FR10-AI-005]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-006`** | 1 (`[FR10-AI-006]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-007`** | 1 (`[FR10-AI-007]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-008`** | 1 (`[FR10-AI-008]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-009`** | 1 (`[FR10-AI-009]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-010`** | 1 (`[FR10-AI-010]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-011`** | 1 (`[FR10-AI-011]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-013`** | 1 (`[FR10-AI-013]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-014`** | 1 (`[FR10-AI-014]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-015`** | 1 (`[FR10-AI-015]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-016`** | 1 (`[FR10-AI-016]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-017`** | 1 (`[FR10-AI-017]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-018`** | 1 (`[FR10-AI-018]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-019`** | 1 (`[FR10-AI-019]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-020`** | 1 (`[FR10-AI-020]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-021`** | 1 (`[FR10-AI-021]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-022`** | 1 (`[FR10-AI-022]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-023`** | 1 (`[FR10-AI-023]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-024`** | 1 (`[FR10-AI-024]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-025`** | 1 (`[FR10-AI-025]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-026`** | 1 (`[FR10-AI-026]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-027`** | 1 (`[FR10-AI-027]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-028`** | 1 (`[FR10-AI-028]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-029`** | 1 (`[FR10-AI-029]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-030`** | 1 (`[FR10-AI-030]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-031`** | 1 (`[FR10-AI-031]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-032`** | 1 (`[FR10-AI-032]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-033`** | 1 (`[FR10-AI-033]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-034`** | 1 (`[FR10-AI-034]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-035`** | 1 (`[FR10-AI-035]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-036`** | 1 (`[FR10-AI-036]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-037`** | 1 (`[FR10-AI-037]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-038`** | 1 (`[FR10-AI-038]`) | 1 (`pm.sendRequest GET`) | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-039`** | 1 (`[FR10-AI-039]`) | 0 | 0 | 1 (`PUT /status`) | 0 (Non-existent) | **1** |
| **`FR10-AI-040`** | 1 (`[FR10-AI-040]`) | 0 | 0 | 1 (`PUT /status`) | 0 (Malformed ID) | **1** |
| **`FR10-AI-041`** | 2 (Action, Verify) | 0 | 0 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-042`** | 1 (`[FR10-AI-042]`) | 0 | 0 | 1 (`PUT /status`) | 0 (SQLi probe) | **1** |
| **`FR10-HUM-001`**| 4 (Action 1, Verify 1, Action 2, Verify 2) | 0 | 0 | 2 (`PUT /status` x2) | 2 (`GET /orders/:id` x2) | **4** |
| **`FR10-HUM-002`**| 3 (Action, Verify A, Verify B) | 0 | 0 | 1 (`PUT /status`) | 2 (`GET /orders/:id` x2) | **3** |
| **`FR10-HUM-003`**| 6 (Action 1, Action 2, Action 3, Verify 1, Action 4, Verify 2) | 0 | 0 | 4 (`PUT` x4) | 2 (`GET /orders/:id` x2) | **6** |
| **`FR10-HUM-004`**| 1 (`[FR10-HUM-004]`) | 0 | 0 | 1 (`PUT /status`) | 0 (Exploratory) | **1** |
| **`FR10-HUM-005`**| 1 (`[FR10-HUM-005]`) | 0 | 0 | 1 (`PUT /status`) | 0 (Exploratory) | **1** |
| **Setup Helpers** | 3 (Admin, User A, User B Login) | 0 | 3 (`POST /login` x3) | 0 | 0 | **3** |
| **TOTALS** | **63 Definitions** | **36 Script Calls** | **3 Calls** | **52 Calls** | **44 Calls** | **99 Operations** |

---

## 3. Explanatory Reconciliation of Counts

1. **46 Formal Test Cases:** Exactly 46 formal business/security test cases are audited and specified.
2. **63 Collection Request Definitions:** 3 authentication helpers + 41 atomic single-request formal items + 19 multi-step sub-request items (e.g. AI-004: 4 items, AI-041: 2 items, HUM-001: 4 items, HUM-002: 3 items, HUM-003: 6 items).
3. **36 Script-Triggered HTTP Calls:** Embedded `pm.sendRequest` persistence queries executing inside test scripts for isolated atomic cases. Every script-triggered request explicitly carries `X-Student-Id: {{studentId}}` and the appropriate `Authorization: Bearer {{token}}`.
4. **99 Total Expected Runtime Operations:** 63 standalone request executions + 36 internal script-level verification requests = 99 HTTP operations executed across the network.
