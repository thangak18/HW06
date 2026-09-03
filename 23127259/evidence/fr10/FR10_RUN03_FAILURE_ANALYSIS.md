# FR-10 Run 03 Failure Analysis Report

- **Execution Context:** Phase 2D.1D.4 – Controlled Canonical Newman Run 03
- **Tested Deployment:** `http://localhost:3000` (Student ID: `23127259`)
- **Raw Evidence:** `evidence/fr10/newman/FR10-run03.json`
- **Total Executed Cases:** 46
- **Total Normative Failures:** 6 (`FR10-AI-016`, `FR10-AI-024`, `FR10-AI-030`, `FR10-AI-031`, `FR10-AI-032`, `FR10-HUM-003`)
- **Total Blocked / Harness Errors:** 0

---

## 1. Candidate Defect Summary Table

| Candidate Cluster ID | Target Formal Case IDs | Category | Severity | Confirmation Status |
|---|---|---|:---:|:---:|
| **`CANDIDATE-FR10-FSM-01`** | `FR10-AI-016`, `FR10-HUM-003` | Lifecycle / In-Transit State Machine Violation | **HIGH** | `RETAIN FOR TARGETED CONFIRMATION` |
| **`CANDIDATE-FR10-FSM-02`** | `FR10-AI-024` | Lifecycle / Terminal State Immutability Violation | **HIGH** | `RETAIN FOR TARGETED CONFIRMATION` |
| **`CANDIDATE-SEC03-01`** | `FR10-AI-030`, `FR10-AI-031`, `FR10-AI-032` | Security / Privilege Escalation / RBAC Bypass | **CRITICAL** | `RETAIN FOR TARGETED CONFIRMATION` |
| **`CANDIDATE-SEC02-01`** | `AI-025..029` | Security / Authentication Boundary | N/A | **DROPPED** (All 5 SEC-02 cases passed safely) |

---

## 2. Detailed Normative Failure Records

### Failure Record 01: `FR10-AI-016`
- **Formal ID:** `FR10-AI-016`
- **Candidate Cluster:** `CANDIDATE-FR10-FSM-01`
- **Fixture Variable:** `order_FR10_AI_016`
- **Setup Result:** PASS (Fresh checkout order created -> Admin advanced to `confirmed` -> Admin advanced to `shipping`)
- **Initial State:** `shipping`
- **Actor:** Customer (Order Owner, User A)
- **Role:** `role = 'user'`
- **Target Endpoint:** `PUT /api/orders/{{order_FR10_AI_016}}/cancel`
- **Input Body:** `{}`
- **Observed HTTP Response:** `200 OK`
- **Persisted state observed via authorized API GET:** `'canceled'` (Retrieved via authorized `GET /api/orders/:id`)
- **Canonical Oracle:** Level 1 SRS Section 4.10 strictly prohibits customer self-service cancellation once the order is in `shipping`. Expected `4xx` Client Error rejection with persisted state remaining `'shipping'`.
- **Actual SUT Behavior:** SUT accepted the cancellation request with HTTP 200 and mutated the order status from `shipping` to `canceled`.
- **Classification:** **FAIL – NORMATIVE ORACLE VIOLATION**
- **Downstream Contamination:** NONE (Dedicated fixture isolated to `FR10-AI-016`).

---

### Failure Record 02: `FR10-AI-024`
- **Formal ID:** `FR10-AI-024`
- **Candidate Cluster:** `CANDIDATE-FR10-FSM-02`
- **Fixture Variable:** `order_FR10_AI_024`
- **Setup Result:** PASS (Fresh checkout order created -> Admin transitioned to `canceled`)
- **Initial State:** `canceled` (Terminal State)
- **Actor:** System Administrator (Admin)
- **Role:** `role = 'admin'`
- **Target Endpoint:** `PUT /api/admin/orders/{{order_FR10_AI_024}}/status`
- **Input Body:** `{"status": "delivered"}`
- **Observed HTTP Response:** `200 OK`
- **Persisted state observed via authorized API GET:** `'delivered'` (Retrieved via authorized `GET /api/orders/:id`)
- **Canonical Oracle:** Level 1 SRS Section 4.10 & Level 2 FSM state chart specify that `canceled` is an immutable terminal sink state. Expected `4xx` Client Error rejection with persisted state remaining `'canceled'`.
- **Actual SUT Behavior:** SUT accepted the status update from terminal `canceled` to `delivered` with HTTP 200 and mutated the persisted database record.
- **Classification:** **FAIL – NORMATIVE ORACLE VIOLATION**
- **Downstream Contamination:** NONE (Dedicated fixture isolated to `FR10-AI-024`).

---

### Failure Record 03: `FR10-AI-030`
- **Formal ID:** `FR10-AI-030`
- **Candidate Cluster:** `CANDIDATE-SEC03-01`
- **Fixture Variable:** `order_FR10_AI_030`
- **Setup Result:** PASS (Fresh checkout order created in `pending` state)
- **Initial State:** `pending`
- **Actor:** Normal Customer (User A)
- **Role:** `role = 'user'`
- **Target Endpoint:** `PUT /api/admin/orders/{{order_FR10_AI_030}}/status`
- **Input Body:** `{"status": "confirmed"}`
- **Authentication:** `Bearer {{userAToken}}`
- **Observed HTTP Response:** `200 OK`
- **Persisted state observed via authorized API GET:** `'confirmed'` (Retrieved via authorized `GET /api/orders/:id`)
- **Canonical Oracle:** Level 1 SRS Section 4 / Assignment Notes RBAC mandates that `/api/admin/*` routes strictly require `role = 'admin'`. Normal customer tokens must be rejected with `403 Forbidden` / `4xx` and zero state mutation (`pending`).
- **Actual SUT Behavior:** SUT failed to enforce role authorization on Admin mutation route, executing status update `pending -> confirmed` on behalf of a regular customer.
- **Classification:** **FAIL – NORMATIVE ORACLE VIOLATION**
- **Downstream Contamination:** NONE (Dedicated fixture isolated to `FR10-AI-030`).

---

### Failure Record 04: `FR10-AI-031`
- **Formal ID:** `FR10-AI-031`
- **Candidate Cluster:** `CANDIDATE-SEC03-01`
- **Fixture Variable:** `order_FR10_AI_031`
- **Setup Result:** PASS (Fresh checkout order created in `pending` state)
- **Initial State:** `pending`
- **Actor:** Normal Customer (User A)
- **Role:** `role = 'user'`
- **Target Endpoint:** `PUT /api/admin/orders/{{order_FR10_AI_031}}/status`
- **Input Body:** `{"status": "canceled"}`
- **Authentication:** `Bearer {{userAToken}}`
- **Observed HTTP Response:** `200 OK`
- **Persisted state observed via authorized API GET:** `'canceled'` (Retrieved via authorized `GET /api/orders/:id`)
- **Canonical Oracle:** Level 1 RBAC policy prohibits regular customers from invoking `/api/admin/*`. Expected `403 Forbidden` / `4xx` with order state remaining `'pending'`.
- **Actual SUT Behavior:** SUT accepted customer token on Admin cancellation route with HTTP 200 and mutated order state to `canceled`.
- **Classification:** **FAIL – NORMATIVE ORACLE VIOLATION**
- **Downstream Contamination:** NONE (Dedicated fixture isolated to `FR10-AI-031`).

---

### Failure Record 05: `FR10-AI-032`
- **Formal ID:** `FR10-AI-032`
- **Candidate Cluster:** `CANDIDATE-SEC03-01`
- **Fixture Variable:** `order_FR10_AI_032`
- **Setup Result:** PASS (Fresh checkout order created -> Admin legitimately advanced to `confirmed`)
- **Initial State:** `confirmed`
- **Actor:** Normal Customer (User A)
- **Role:** `role = 'user'`
- **Target Endpoint:** `PUT /api/admin/orders/{{order_FR10_AI_032}}/status`
- **Input Body:** `{"status": "shipping"}`
- **Authentication:** `Bearer {{userAToken}}`
- **Observed HTTP Response:** `200 OK`
- **Persisted state observed via authorized API GET:** `'shipping'` (Retrieved via authorized `GET /api/orders/:id`)
- **Canonical Oracle:** Level 1 RBAC policy prohibits regular customers from invoking `/api/admin/*`. Expected `403 Forbidden` / `4xx` with order state remaining `'confirmed'`.
- **Actual SUT Behavior:** SUT accepted customer token on Admin dispatch route with HTTP 200 and mutated order state from `confirmed` to `shipping`.
- **Classification:** **FAIL – NORMATIVE ORACLE VIOLATION**
- **Downstream Contamination:** NONE (Dedicated fixture isolated to `FR10-AI-032`).

---

### Failure Record 06: `FR10-HUM-003`
- **Formal ID:** `FR10-HUM-003`
- **Candidate Cluster:** `CANDIDATE-FR10-FSM-01`
- **Fixture Variable:** `order_FR10_HUM_003`
- **Setup Result:** PASS (Multi-stage sequence: Checkout -> Admin confirmed -> Admin shipping)
- **Initial State:** `shipping`
- **Actor:** Customer (Order Owner, User A)
- **Role:** `role = 'user'`
- **Target Endpoint:** `PUT /api/orders/{{order_FR10_HUM_003}}/cancel`
- **Input Body:** `{}`
- **Observed HTTP Response:** `200 OK`
- **Persisted state observed via authorized API GET:** `'canceled'`
- **Canonical Oracle:** Level 1 SRS Section 4.10 prohibits customer cancellation during transit. Expected `4xx` rejection with order remaining in `shipping`.
- **Actual SUT Behavior:** Customer cancellation was accepted (HTTP 200), corrupting the downstream multi-stage sequence assertion.
- **Classification:** **FAIL – NORMATIVE ORACLE VIOLATION**
- **Downstream Contamination:** NONE (Dedicated fixture isolated to `FR10-HUM-003`).

---

## 3. Exploratory Robustness Observations

### Observation 01: `FR10-HUM-004` (Same-State Transition Probe)
- **Target Endpoint:** `PUT /api/admin/orders/{{order_FR10_HUM_004}}/status` body `{"status":"confirmed"}` on already `confirmed` order.
- **Observed Response:** `400 Bad Request`
- **Persisted State:** `'confirmed'`
- **Verdict:** **EXPLORATORY OBSERVATION** (Clean rejection, database invariant preserved).

### Observation 02: `FR10-HUM-005` (Non-JSON Media Type Probe)
- **Target Endpoint:** `PUT /api/admin/orders/{{order_FR10_HUM_005}}/status` with `Content-Type: text/plain` and payload `status=confirmed`.
- **Observed Response:** `500 Internal Server Error`
- **Persisted State:** `'pending'`
- **Verdict:** **EXPLORATORY OBSERVATION**
- **Formal Note:** HTTP 500 observed; persisted order did not enter an invalid lifecycle state. This remains an exploratory robustness observation and is NOT automatically a normative FR-10 defect.
