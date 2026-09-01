# Raw AI-Generated Test Cases: FR-10 (Order Status / State Machine)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Primary APIs:** `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel`, `GET /api/orders/:id`
- **Authoritative Standard:** EShop SRS Section 4.10, api_specification.md, HW06 Requirements

---

## 1. Generation Inventory & Stage Tracking

| ID Range | Generation Stage | Batch Count | Cumulative Raw AI Count | Status |
|---|---|---:|---:|:---:|
| `FR10-AI-001` – `FR10-AI-012` | Batch 1: Core Valid Forward Transitions, Valid Cancellations & Skip Transitions | 12 | 12 | **GENERATED** |
| `FR10-AI-013` – `FR10-AI-022` | Batch 2: Backward Regressions, Terminal Immutability & User Cancel | 10 | 22 | Pending Phase 2A.3 |
| `FR10-AI-023` – `FR10-AI-030` | Batch 3: Authentication (`SEC-02`), RBAC (`SEC-03`) & Ownership | 8 | 30 | Pending Phase 2A.4 |
| `FR10-AI-031` – `FR10-AI-040` | Batch 4: Status Domain, Order ID Boundaries & Schema/SEC-05 | 10 | 40 | Pending Phase 2A.5 |

---

## 2. Raw AI Test Cases (Batch 1: Core State Transitions)

---

### FR10-AI-001 – Valid Admin Forward Transition: Pending to Confirmed

- **Test Case ID:** `FR10-AI-001`
- **Title:** Valid Admin Transition from `pending` to `confirmed`
- **Technique:** State Transition Testing (Valid Forward Edge)
- **Requirement:** SRS FR-10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Fresh order created via setup helper in `pending` state; admin credentials available.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT in `Authorization: Bearer <adminToken>`
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "confirmed"
  }
  ```
- **Action / Sequence:**
  1. Helper creates order $\rightarrow$ state is `pending`.
  2. Admin sends `PUT /api/admin/orders/:id/status` with `status: "confirmed"`.
  3. Query `GET /api/orders/:id` to verify persisted state.
- **Expected HTTP Status:** `200 OK` (if documented)
- **Expected Semantic Result:** Order successfully advances from `pending` to `confirmed`.
- **Expected State After:** `confirmed`
- **Persistence Verification Plan:** Send `GET /api/orders/:id` with admin/user token; assert `response.order.status === "confirmed"`.
- **Oracle Confidence:** HIGH
- **Notes:** Baseline valid fulfillment transition per SRS FR-10.

---

### FR10-AI-002 – Valid Admin Forward Transition: Confirmed to Shipping

- **Test Case ID:** `FR10-AI-002`
- **Title:** Valid Admin Transition from `confirmed` to `shipping`
- **Technique:** State Transition Testing (Valid Forward Edge)
- **Requirement:** SRS FR-10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order created and confirmed by admin $\rightarrow$ state is `confirmed`.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT in `Authorization: Bearer <adminToken>`
- **State Before:** `confirmed`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "shipping"
  }
  ```
- **Action / Sequence:**
  1. Setup advances order to `confirmed`.
  2. Admin sends `PUT /api/admin/orders/:id/status` with `status: "shipping"`.
  3. Query `GET /api/orders/:id` to verify persisted state.
- **Expected HTTP Status:** `200 OK` (if documented)
- **Expected Semantic Result:** Order successfully transitions from `confirmed` to `shipping`.
- **Expected State After:** `shipping`
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "shipping"`.
- **Oracle Confidence:** HIGH
- **Notes:** Standard merchant dispatch workflow.

---

### FR10-AI-003 – Valid Admin Forward Transition: Shipping to Delivered

- **Test Case ID:** `FR10-AI-003`
- **Title:** Valid Admin Transition from `shipping` to `delivered`
- **Technique:** State Transition Testing (Valid Terminal Edge)
- **Requirement:** SRS FR-10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order advanced through `pending` $\rightarrow$ `confirmed` $\rightarrow$ `shipping`.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT in `Authorization: Bearer <adminToken>`
- **State Before:** `shipping`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "delivered"
  }
  ```
- **Action / Sequence:**
  1. Setup advances order to `shipping`.
  2. Admin sends `PUT /api/admin/orders/:id/status` with `status: "delivered"`.
  3. Query `GET /api/orders/:id` to verify persisted state.
- **Expected HTTP Status:** `200 OK` (if documented)
- **Expected Semantic Result:** Order successfully reaches terminal `delivered` status.
- **Expected State After:** `delivered`
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "delivered"`.
- **Oracle Confidence:** HIGH
- **Notes:** Moves order into permanent terminal fulfillment state.

---

### FR10-AI-004 – Complete Happy-Path Order Lifecycle Continuity Sequence

- **Test Case ID:** `FR10-AI-004`
- **Title:** End-to-End Sequential Progression (`pending` $\rightarrow$ `confirmed` $\rightarrow$ `shipping` $\rightarrow$ `delivered`)
- **Technique:** Multi-Step State Sequence Testing
- **Requirement:** SRS FR-10, SRS Section 4.10 Lifecycle Continuum
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Customer places order (`pending`); Admin credentials active.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT
- **State Before:** `pending`
- **Request Method:** `PUT` (Sequential Chaining)
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:** `{ "status": "confirmed" }` $\rightarrow$ `{ "status": "shipping" }` $\rightarrow$ `{ "status": "delivered" }`
- **Action / Sequence:**
  1. Helper creates fresh order (`pending`).
  2. Admin transitions `pending` $\rightarrow$ `confirmed` (verify 200 & state).
  3. Admin transitions `confirmed` $\rightarrow$ `shipping` (verify 200 & state).
  4. Admin transitions `shipping` $\rightarrow$ `delivered` (verify 200 & state).
  5. Final `GET /api/orders/:id` asserts `delivered`.
- **Expected HTTP Status:** `200 OK` on all transitions
- **Expected Semantic Result:** Complete linear progression succeeds uninterrupted across all intermediate milestones.
- **Expected State After:** `delivered`
- **Persistence Verification Plan:** Multi-stage `GET /api/orders/:id` queries after each transition validating exact sequential state persistence.
- **Oracle Confidence:** HIGH
- **Notes:** Validates full lifecycle continuity on a single order entity.

---

### FR10-AI-005 – Valid Customer Self-Cancellation on Pending Order

- **Test Case ID:** `FR10-AI-005`
- **Title:** Customer Cancels Own `pending` Order via `PUT /api/orders/:id/cancel`
- **Technique:** State Transition Testing (Customer Cancellation)
- **Requirement:** SRS Section 4.10 (Pending Order Cancellation by User)
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Customer $U_1$ has placed an order in `pending` state.
- **Actor:** Order Owner Customer ($U_1$, `role = 'user'`)
- **Authentication Context:** Valid customer JWT (`userToken`)
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/orders/:id/cancel`
- **Headers:** `Authorization: Bearer <userToken>`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:** Empty `{}`
- **Action / Sequence:**
  1. Customer $U_1$ places order $\rightarrow$ state is `pending`.
  2. Customer $U_1$ sends `PUT /api/orders/:id/cancel`.
  3. Query `GET /api/orders/:id` to verify state.
- **Expected HTTP Status:** `200 OK` (if documented)
- **Expected Semantic Result:** Order is successfully canceled by customer; transitions to `canceled`.
- **Expected State After:** `canceled`
- **Persistence Verification Plan:** Send `GET /api/orders/:id` with $U_1$ token; assert `response.order.status === "canceled"`.
- **Oracle Confidence:** HIGH
- **Notes:** Standard customer self-service cancellation on unreviewed order.

---

### FR10-AI-006 – Valid Admin Cancellation on Pending Order

- **Test Case ID:** `FR10-AI-006`
- **Title:** Administrator Cancels `pending` Order via Admin Status Endpoint
- **Technique:** State Transition Testing (Admin Cancellation)
- **Requirement:** SRS Section 4.10 (Pending Order Cancellation by Admin)
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Fresh order created in `pending` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "canceled"
  }
  ```
- **Action / Sequence:**
  1. Setup creates order in `pending` state.
  2. Admin sends `PUT /api/admin/orders/:id/status` with `status: "canceled"`.
  3. Query `GET /api/orders/:id` to verify state.
- **Expected HTTP Status:** `200 OK` (if documented)
- **Expected Semantic Result:** Order is successfully canceled by administrator; transitions to `canceled`.
- **Expected State After:** `canceled`
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "canceled"`.
- **Oracle Confidence:** HIGH
- **Notes:** Merchant rejects/cancels pending order.

---

### FR10-AI-007 – Valid Customer Self-Cancellation on Confirmed Order

- **Test Case ID:** `FR10-AI-007`
- **Title:** Customer Cancels Own `confirmed` Order Prior to Shipment
- **Technique:** State Transition Testing (Customer Pre-Shipment Cancellation)
- **Requirement:** SRS Section 4.10 (User cancellation allowed while status is `confirmed`)
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order placed by customer $U_1$ and advanced to `confirmed` by admin setup.
- **Actor:** Order Owner Customer ($U_1$, `role = 'user'`)
- **Authentication Context:** Valid customer JWT (`userToken`)
- **State Before:** `confirmed`
- **Request Method:** `PUT`
- **Endpoint:** `/api/orders/:id/cancel`
- **Headers:** `Authorization: Bearer <userToken>`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:** Empty `{}`
- **Action / Sequence:**
  1. Helper creates order $\rightarrow$ admin transitions to `confirmed`.
  2. Customer $U_1$ sends `PUT /api/orders/:id/cancel`.
  3. Query `GET /api/orders/:id` to verify state.
- **Expected HTTP Status:** `200 OK` (if documented)
- **Expected Semantic Result:** Customer successfully cancels order in `confirmed` status before carrier dispatch.
- **Expected State After:** `canceled`
- **Persistence Verification Plan:** Send `GET /api/orders/:id` with $U_1$ token; assert `response.order.status === "canceled"`.
- **Oracle Confidence:** HIGH
- **Notes:** SRS Section 4.10 explicitly specifies that user cancellation is permitted while status is `confirmed`.

---

### FR10-AI-008 – Valid Admin Cancellation on Confirmed Order

- **Test Case ID:** `FR10-AI-008`
- **Title:** Administrator Cancels `confirmed` Order Prior to Shipment
- **Technique:** State Transition Testing (Admin Pre-Shipment Cancellation)
- **Requirement:** SRS Section 4.10 (Admin cancellation allowed while status is `confirmed`)
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order placed and advanced to `confirmed` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `confirmed`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "canceled"
  }
  ```
- **Action / Sequence:**
  1. Setup creates order and advances to `confirmed`.
  2. Admin sends `PUT /api/admin/orders/:id/status` with `status: "canceled"`.
  3. Query `GET /api/orders/:id` to verify state.
- **Expected HTTP Status:** `200 OK` (if documented)
- **Expected Semantic Result:** Administrator successfully voids confirmed order prior to carrier dispatch.
- **Expected State After:** `canceled`
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "canceled"`.
- **Oracle Confidence:** HIGH
- **Notes:** Merchant cancels order during packaging/pre-shipment phase.

---

### FR10-AI-009 – Invalid Forward Skip Transition: Pending Directly to Shipping

- **Test Case ID:** `FR10-AI-009`
- **Title:** Illegal Forward State Skip: `pending` Directly to `shipping`
- **Technique:** Negative State Transition Testing (Illegal Intermediate State Skip)
- **Requirement:** SRS FR-10, FSM Integrity Rules
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Fresh order created in `pending` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "shipping"
  }
  ```
- **Action / Sequence:**
  1. Setup creates order in `pending` state.
  2. Admin attempts to transition `pending` directly to `shipping`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Transition rejected; intermediate `confirmed` state cannot be bypassed.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Prevents skipping required merchant review and confirmation.

---

### FR10-AI-010 – Invalid Forward Skip Transition: Pending Directly to Delivered

- **Test Case ID:** `FR10-AI-010`
- **Title:** Illegal Forward State Skip: `pending` Directly to `delivered`
- **Technique:** Negative State Transition Testing (Multi-Stage State Skip)
- **Requirement:** SRS FR-10, FSM Integrity Rules
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Fresh order created in `pending` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "delivered"
  }
  ```
- **Action / Sequence:**
  1. Setup creates order in `pending` state.
  2. Admin attempts to transition `pending` directly to `delivered`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Transition rejected; order cannot bypass both `confirmed` and `shipping` stages.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** High-risk bypass probe preventing instantaneous fulfillment of unverified orders.

---

### FR10-AI-011 – Invalid Forward Skip Transition: Confirmed Directly to Delivered

- **Test Case ID:** `FR10-AI-011`
- **Title:** Illegal Forward State Skip: `confirmed` Directly to `delivered`
- **Technique:** Negative State Transition Testing (Intermediate Dispatch Skip)
- **Requirement:** SRS FR-10, FSM Integrity Rules
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order advanced to `confirmed` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `confirmed`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "delivered"
  }
  ```
- **Action / Sequence:**
  1. Setup advances order to `confirmed`.
  2. Admin attempts to transition `confirmed` directly to `delivered`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Transition rejected; intermediate `shipping` (transit) state cannot be bypassed.
- **Expected State After:** `confirmed` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "confirmed"`.
- **Oracle Confidence:** HIGH
- **Notes:** Ensures goods must pass through carrier transit before marking fulfilled.

---

### FR10-AI-012 – Invalid Forward Skip Attempt by Normal Customer Token

- **Test Case ID:** `FR10-AI-012`
- **Title:** Unauthorized Customer Forward Skip Attempt (`pending` $\rightarrow$ `shipping`)
- **Technique:** Negative State Transition + RBAC Boundary Testing
- **Requirement:** SRS FR-10, SRS FR-12, SEC-03
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order in `pending` state; customer token active.
- **Actor:** Normal Customer (`role = 'user'`)
- **Authentication Context:** Valid customer JWT (`userToken`)
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <userToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "shipping"
  }
  ```
- **Action / Sequence:**
  1. Setup creates order in `pending` state.
  2. Customer attempts to send `PUT /api/admin/orders/:id/status` with `status: "shipping"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `403 Forbidden` under `SEC-03` or `400 Bad Request`)
- **Expected Semantic Result:** Request rejected due to unauthorized role and illegal state transition; order status remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Evaluates combined state-skipping and RBAC privilege boundary under SEC-03.
