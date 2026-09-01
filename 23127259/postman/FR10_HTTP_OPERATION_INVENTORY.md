# FR-10 HTTP Operation Inventory & Architecture (Execution-Ready)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Formal Executable Test Cases:** `46` (41 AI-Derived + 5 Human Extensions)
- **Authentication Helpers:** `3`
- **Order Creation & Prerequisite State Helpers:** `14`

---

## 1. Request-Definition vs Runtime-HTTP Model

| Metric | Count | Description |
|---|:---:|---|
| **Formal Test Cases** | **`46`** | Authoritative audited & extended test suite (`41` AI-derived + `5` Human extensions) |
| **Authentication Helpers** | **`3`** | Top-level setup requests (`POST /api/auth/login` for Admin, User A, User B) |
| **Order Creation & Prerequisite State Helpers** | **`14`** | Dynamic API-level order fixture setup requests in Folder 00 |
| **Collection Request Definitions** | **`77`** | Total standalone HTTP request items in the Postman collection (17 setup + 60 formal steps) |
| **Script-Triggered HTTP Calls (`pm.sendRequest`)** | **`36`** | Dynamic persistence verification GET queries executed inside test scripts for atomic cases |
| **Expected Total Runtime HTTP Operations** | **`113`** | Total network calls executed during a full automated Newman collection run |

---

## 2. Comprehensive Formal Case HTTP Operations Table

| Formal ID | Order Variable Consumed | Initial State | Setup Calls | Action Calls | Verify Calls | Total Runtime HTTP Calls |
|---|---|---|:---:|:---:|:---:|:---:|
| **`FR10-AI-001`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-002`** | `orderConfirmedId`| `confirmed` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-003`** | `orderShippingId` | `shipping` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-004`** | `orderId` | `pending` | In Folder 00 | 3 (`PUT /status` x3) | 1 (`GET /orders/:id`) | **4** |
| **`FR10-AI-005`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-006`** | `orderConfirmedId`| `confirmed` | In Folder 00 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-007`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-008`** | `orderConfirmedId`| `confirmed` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-009`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-010`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-011`** | `orderConfirmedId`| `confirmed` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-013`** | `orderConfirmedId`| `confirmed` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-014`** | `orderShippingId` | `shipping` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-015`** | `orderShippingId` | `shipping` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-016`** | `orderShippingId` | `shipping` | In Folder 00 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-017`** | `orderDeliveredId`| `delivered` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-018`** | `orderDeliveredId`| `delivered` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-019`** | `orderDeliveredId`| `delivered` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-020`** | `orderDeliveredId`| `delivered` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-021`** | `orderCanceledId` | `canceled` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-022`** | `orderCanceledId` | `canceled` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-023`** | `orderCanceledId` | `canceled` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-024`** | `orderCanceledId` | `canceled` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-025`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-026`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-027`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-028`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-029`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-030`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-031`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-032`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-033`** | `orderAId` | `pending` | In Folder 00 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-034`** | `orderConfirmedId`| `confirmed` | In Folder 00 | 1 (`PUT /cancel`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-035`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-036`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-037`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-038`** | `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-039`** | Synthetic `999999`| Non-Existent | N/A | 1 (`PUT /status`) | 0 (Non-existent) | **1** |
| **`FR10-AI-040`** | Synthetic `not-an-id`| Malformed | N/A | 1 (`PUT /status`) | 0 (Malformed ID) | **1** |
| **`FR10-AI-041`** | `orderId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 1 (`GET /orders/:id`) | **2** |
| **`FR10-AI-042`** | Synthetic SQLi | Malicious | N/A | 1 (`PUT /status`) | 0 (SQLi probe) | **1** |
| **`FR10-HUM-001`**| `orderId` | `pending` | In Folder 00 | 2 (`PUT /status` x2) | 2 (`GET /orders/:id` x2) | **4** |
| **`FR10-HUM-002`**| `orderAId`, `orderBId`| 2x `pending`| In Folder 00 | 1 (`PUT /status`) | 2 (`GET /orders/:id` x2) | **3** |
| **`FR10-HUM-003`**| `orderId` | `pending` | In Folder 00 | 4 (`PUT` x4) | 2 (`GET /orders/:id` x2) | **6** |
| **`FR10-HUM-004`**| `orderConfirmedId`| `confirmed` | In Folder 00 | 1 (`PUT /status`) | 0 (Exploratory) | **1** |
| **`FR10-HUM-005`**| `orderPendingId` | `pending` | In Folder 00 | 1 (`PUT /status`) | 0 (Exploratory) | **1** |
| **Setup Helpers** | N/A | Setup | 17 (3 Auth + 14 Fixture Setup) | 0 | 0 | **17** |
| **TOTALS** | — | — | **17 Setup Calls** | **52 Action Calls** | **44 Verify Calls** | **113 Operations** |
