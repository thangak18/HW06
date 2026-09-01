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
| `FR10-AI-013` – `FR10-AI-024` | Batch 2: Backward Regressions, Terminal Immutability & User In-Transit Cancel | 12 | 24 | **GENERATED (24 RAW CASES PENDING HUMAN AUDIT)** |
| `FR10-AI-025` – `FR10-AI-032` | Batch 3: Authentication (`SEC-02`), RBAC (`SEC-03`) & Ownership | 8 | 32 | Pending Phase 2A.4 |
| `FR10-AI-033` – `FR10-AI-040` | Batch 4: Status Domain, Order ID Boundaries & Schema/SEC-05 | 8 | 40 | Pending Phase 2A.5 |

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
- **Notes:** [PENDING HUMAN AUDIT – MULTIPLE FAILURE DIMENSIONS] Combines unauthorized role with illegal skip transition.

---

## 3. Raw AI Test Cases (Batch 2: Backward Regressions, Terminal States & User In-Transit Cancel)

---

### FR10-AI-013 – Invalid Backward State Regression: Confirmed to Pending

- **Test Case ID:** `FR10-AI-013`
- **Title:** Illegal Backward Regression: `confirmed` to `pending`
- **Technique:** Negative State Transition Testing (Backward Regression)
- **Requirement:** SRS FR-10, FSM Progression Rules
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order created and advanced to `confirmed` state via helper setup.
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
    "status": "pending"
  }
  ```
- **Action / Sequence:**
  1. Helper creates order $\rightarrow$ transitions to `confirmed`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "pending"`.
  3. Query `GET /api/orders/:id` to verify state was NOT regressed.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Backward transition rejected; confirmed order cannot revert to pending review.
- **Expected State After:** `confirmed` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "confirmed"`.
- **Oracle Confidence:** HIGH
- **Notes:** Pure backward state transition probe using valid admin authentication.

---

### FR10-AI-014 – Invalid Backward State Regression: Shipping to Confirmed

- **Test Case ID:** `FR10-AI-014`
- **Title:** Illegal Backward Regression: `shipping` to `confirmed`
- **Technique:** Negative State Transition Testing (Backward Regression)
- **Requirement:** SRS FR-10, FSM Progression Rules
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order advanced through `pending` $\rightarrow$ `confirmed` $\rightarrow$ `shipping`.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `shipping`
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
  1. Helper creates and advances order to `shipping`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "confirmed"`.
  3. Query `GET /api/orders/:id` to verify state was NOT regressed.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Backward transition rejected; in-transit order cannot regress to pre-shipment stage.
- **Expected State After:** `shipping` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "shipping"`.
- **Oracle Confidence:** HIGH
- **Notes:** Verifies in-transit dispatch cannot be undone via status update API.

---

### FR10-AI-015 – Invalid Backward State Regression: Shipping to Pending

- **Test Case ID:** `FR10-AI-015`
- **Title:** Illegal Backward Multi-Stage Regression: `shipping` to `pending`
- **Technique:** Negative State Transition Testing (Multi-Stage Backward Regression)
- **Requirement:** SRS FR-10, FSM Progression Rules
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order advanced through `pending` $\rightarrow$ `confirmed` $\rightarrow$ `shipping`.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `shipping`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "pending"
  }
  ```
- **Action / Sequence:**
  1. Helper creates and advances order to `shipping`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "pending"`.
  3. Query `GET /api/orders/:id` to verify state was NOT regressed.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Multi-stage regression rejected; dispatched order cannot revert to initial placement state.
- **Expected State After:** `shipping` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "shipping"`.
- **Oracle Confidence:** HIGH
- **Notes:** Ensures strict forward-only lifecycle progression.

---

### FR10-AI-016 – Customer Prohibited In-Transit Cancellation Attempt

- **Test Case ID:** `FR10-AI-016`
- **Title:** Customer Prohibited Cancellation of In-Transit Order (`shipping` $\rightarrow$ `canceled`)
- **Technique:** Negative Business Rule & State Testing
- **Requirement:** SRS Section 4.10 (User cannot cancel when status is `shipping`)
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order placed by customer $U_1$ and advanced through `confirmed` to `shipping` by admin setup.
- **Actor:** Order Owner Customer ($U_1$, `role = 'user'`)
- **Authentication Context:** Valid customer JWT (`userToken`)
- **State Before:** `shipping`
- **Request Method:** `PUT`
- **Endpoint:** `/api/orders/:id/cancel`
- **Headers:** `Authorization: Bearer <userToken>`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:** Empty `{}`
- **Action / Sequence:**
  1. Helper creates order for $U_1$ $\rightarrow$ admin advances order to `shipping`.
  2. Customer $U_1$ attempts to call `PUT /api/orders/:id/cancel`.
  3. Query `GET /api/orders/:id` to verify order status remained `shipping`.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `409 Conflict`)
- **Expected Semantic Result:** Cancellation rejected; customer is barred from cancelling orders that have already shipped.
- **Expected State After:** `shipping` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` with $U_1$ token; assert `response.order.status === "shipping"`.
- **Oracle Confidence:** HIGH
- **Notes:** Directly tests the explicit SRS Section 4.10 rule: "When an order is shipping, User cannot cancel it".

---

### FR10-AI-017 – Invalid Terminal State Mutation: Delivered to Pending

- **Test Case ID:** `FR10-AI-017`
- **Title:** Illegal Terminal State Mutation: `delivered` to `pending`
- **Technique:** Terminal State Immutability Testing
- **Requirement:** SRS FR-10, FSM Terminal State Invariant
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order fulfilled through lifecycle to `delivered` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `delivered`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "pending"
  }
  ```
- **Action / Sequence:**
  1. Helper advances order to `delivered`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "pending"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Mutation rejected; completed order in terminal state is permanently immutable.
- **Expected State After:** `delivered` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "delivered"`.
- **Oracle Confidence:** HIGH
- **Notes:** Tests immutability of terminal `delivered` state.

---

### FR10-AI-018 – Invalid Terminal State Mutation: Delivered to Confirmed

- **Test Case ID:** `FR10-AI-018`
- **Title:** Illegal Terminal State Mutation: `delivered` to `confirmed`
- **Technique:** Terminal State Immutability Testing
- **Requirement:** SRS FR-10, FSM Terminal State Invariant
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order fulfilled through lifecycle to `delivered` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `delivered`
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
  1. Helper advances order to `delivered`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "confirmed"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Mutation rejected; fulfilled order cannot be reverted to pre-shipment confirmation.
- **Expected State After:** `delivered` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "delivered"`.
- **Oracle Confidence:** HIGH
- **Notes:** Prevents resurrecting fulfilled orders into active processing pipelines.

---

### FR10-AI-019 – Invalid Terminal State Mutation: Delivered to Shipping

- **Test Case ID:** `FR10-AI-019`
- **Title:** Illegal Terminal State Mutation: `delivered` to `shipping`
- **Technique:** Terminal State Immutability Testing
- **Requirement:** SRS FR-10, FSM Terminal State Invariant
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order fulfilled through lifecycle to `delivered` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `delivered`
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
  1. Helper advances order to `delivered`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "shipping"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Mutation rejected; delivered package cannot revert to in-transit status.
- **Expected State After:** `delivered` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "delivered"`.
- **Oracle Confidence:** HIGH
- **Notes:** Tests terminal boundary between fulfillment and transit.

---

### FR10-AI-020 – Invalid Terminal State Mutation: Delivered to Canceled

- **Test Case ID:** `FR10-AI-020`
- **Title:** Illegal Terminal State Mutation: `delivered` to `canceled`
- **Technique:** Terminal State Immutability Testing
- **Requirement:** SRS FR-10, FSM Terminal State Invariant
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order fulfilled through lifecycle to `delivered` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `delivered`
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
  1. Helper advances order to `delivered`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "canceled"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Mutation rejected; completed order cannot be canceled after delivery fulfillment.
- **Expected State After:** `delivered` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "delivered"`.
- **Oracle Confidence:** HIGH
- **Notes:** Critical business invariant: delivered commercial transactions cannot be voided as cancellations.

---

### FR10-AI-021 – Invalid Terminal State Mutation: Canceled to Pending

- **Test Case ID:** `FR10-AI-021`
- **Title:** Illegal Terminal State Mutation: `canceled` to `pending`
- **Technique:** Terminal State Immutability Testing (Resurrection Prevention)
- **Requirement:** SRS FR-10, FSM Terminal State Invariant
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order placed and canceled $\rightarrow$ state is `canceled`.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `canceled`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "pending"
  }
  ```
- **Action / Sequence:**
  1. Helper creates and cancels order $\rightarrow$ state is `canceled`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "pending"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Mutation rejected; voided/canceled order cannot be resurrected into pending review.
- **Expected State After:** `canceled` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "canceled"`.
- **Oracle Confidence:** HIGH
- **Notes:** Prevents resurrecting aborted transactions.

---

### FR10-AI-022 – Invalid Terminal State Mutation: Canceled to Confirmed

- **Test Case ID:** `FR10-AI-022`
- **Title:** Illegal Terminal State Mutation: `canceled` to `confirmed`
- **Technique:** Terminal State Immutability Testing (Resurrection Prevention)
- **Requirement:** SRS FR-10, FSM Terminal State Invariant
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order placed and canceled $\rightarrow$ state is `canceled`.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `canceled`
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
  1. Helper creates and cancels order $\rightarrow$ state is `canceled`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "confirmed"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Mutation rejected; canceled order cannot be confirmed for fulfillment.
- **Expected State After:** `canceled` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "canceled"`.
- **Oracle Confidence:** HIGH
- **Notes:** Prevents confirming previously voided orders.

---

### FR10-AI-023 – Invalid Terminal State Mutation: Canceled to Shipping

- **Test Case ID:** `FR10-AI-023`
- **Title:** Illegal Terminal State Mutation: `canceled` to `shipping`
- **Technique:** Terminal State Immutability Testing (Resurrection Prevention)
- **Requirement:** SRS FR-10, FSM Terminal State Invariant
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order placed and canceled $\rightarrow$ state is `canceled`.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `canceled`
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
  1. Helper creates and cancels order $\rightarrow$ state is `canceled`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "shipping"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Mutation rejected; canceled order cannot be dispatched to carrier.
- **Expected State After:** `canceled` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "canceled"`.
- **Oracle Confidence:** HIGH
- **Notes:** Prevents accidental dispatch of canceled items.

---

### FR10-AI-024 – Invalid Terminal State Mutation: Canceled to Delivered

- **Test Case ID:** `FR10-AI-024`
- **Title:** Illegal Terminal State Mutation: `canceled` to `delivered`
- **Technique:** Terminal State Immutability Testing (Terminal-to-Terminal Mutation)
- **Requirement:** SRS FR-10, FSM Terminal State Invariant
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Preconditions:** Order placed and canceled $\rightarrow$ state is `canceled`.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `canceled`
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
  1. Helper creates and cancels order $\rightarrow$ state is `canceled`.
  2. Admin attempts to send `PUT /api/admin/orders/:id/status` with `status: "delivered"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `NOT SPECIFIED – ERROR / NON-SUCCESS` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Mutation rejected; canceled order cannot transition directly to delivered.
- **Expected State After:** `canceled` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id`; assert `response.order.status === "canceled"`.
- **Oracle Confidence:** HIGH
- **Notes:** High-risk probe verifying terminal-to-terminal cross-mutation prevention.
