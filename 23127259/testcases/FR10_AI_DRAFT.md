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
| `FR10-AI-013` – `FR10-AI-024` | Batch 2: Backward Regressions, Terminal Immutability & User In-Transit Cancel | 12 | 24 | **GENERATED** |
| `FR10-AI-025` – `FR10-AI-034` | Batch 3: Authentication (`SEC-02`), RBAC (`SEC-03`) & Ownership Boundaries | 10 | 34 | **GENERATED** |
| `FR10-AI-035` – `FR10-AI-042` | Batch 4: Status Domain, Order ID Boundaries, Schema/Persistence & SEC-05 Probe | 8 | 42 | **GENERATED (42 RAW CASES PENDING HUMAN AUDIT - FROZEN)** |

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

---

## 4. Raw AI Test Cases (Batch 3: Authentication, RBAC & Ownership Boundaries)

---

### FR10-AI-025 – SEC-02: Missing Authorization Header on Valid Admin Status Transition

- **Test Case ID:** `FR10-AI-025`
- **Title:** Missing Authorization Header on Valid Admin Status Transition (`pending` $\rightarrow$ `confirmed`)
- **Technique:** Security / Authentication Testing (SEC-02 Missing Credential)
- **Requirement:** SEC-02 Authentication Standard, SRS FR-10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / SEC-02 AUTHENTICATION`
- **Preconditions:** Fresh order created via helper setup in `pending` state.
- **Actor:** Unauthenticated Client (`Anonymous`)
- **Authentication Context:** None (Missing `Authorization` header)
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "confirmed"
  }
  ```
- **Action / Sequence:**
  1. Helper creates order $\rightarrow$ state is `pending`.
  2. Unauthenticated client sends `PUT /api/admin/orders/:id/status` with `status: "confirmed"` without `Authorization` header.
  3. Query `GET /api/orders/:id` using admin token to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `401 Unauthorized`)
- **Expected Semantic Result:** Request rejected due to missing authentication; order status remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` using admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Evaluates SEC-02 authentication enforcement on the admin status route while keeping the transition otherwise valid.

---

### FR10-AI-026 – SEC-02: Malformed Authorization Header on Valid Admin Status Transition

- **Test Case ID:** `FR10-AI-026`
- **Title:** Malformed Authorization Header on Valid Admin Transition (`pending` $\rightarrow$ `confirmed`)
- **Technique:** Security / Authentication Testing (SEC-02 Header Syntax)
- **Requirement:** SEC-02 Authentication Standard, SRS FR-10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / SEC-02 AUTHENTICATION`
- **Preconditions:** Fresh order created in `pending` state.
- **Actor:** Unauthenticated Client / Malformed Token Client
- **Authentication Context:** Malformed Bearer header: `Authorization: InvalidBearerFormat`
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: InvalidBearerFormat`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "confirmed"
  }
  ```
- **Action / Sequence:**
  1. Setup creates order in `pending` state.
  2. Client sends `PUT /api/admin/orders/:id/status` with malformed `Authorization` header.
  3. Query `GET /api/orders/:id` via admin token to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `401 Unauthorized` or `400 Bad Request`)
- **Expected Semantic Result:** Request rejected due to malformed authentication header scheme; order status remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` using admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Tests header parsing resilience under SEC-02.

---

### FR10-AI-027 – SEC-02: Syntactically Invalid / Random JWT on Valid Admin Transition

- **Test Case ID:** `FR10-AI-027`
- **Title:** Syntactically Invalid / Random JWT on Valid Admin Transition (`pending` $\rightarrow$ `confirmed`)
- **Technique:** Security / Authentication Testing (SEC-02 Token Verification)
- **Requirement:** SEC-02 Authentication Standard, SRS FR-10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / SEC-02 AUTHENTICATION`
- **Preconditions:** Fresh order created in `pending` state.
- **Actor:** Unauthenticated Attacker
- **Authentication Context:** Random pseudo-token `Authorization: Bearer invalid.token.garbage12345`
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer invalid.token.garbage12345`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "confirmed"
  }
  ```
- **Action / Sequence:**
  1. Setup creates order in `pending` state.
  2. Attacker sends `PUT /api/admin/orders/:id/status` with garbage token.
  3. Query `GET /api/orders/:id` via admin token to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `401 Unauthorized`)
- **Expected Semantic Result:** Request rejected due to invalid token signature/format; order status remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` using admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Verifies rejection of unverified arbitrary JWT strings.

---

### FR10-AI-028 – SEC-02: Cryptographically Tampered JWT on Valid Admin Transition

- **Test Case ID:** `FR10-AI-028`
- **Title:** Cryptographically Tampered JWT on Valid Admin Transition (`pending` $\rightarrow$ `confirmed`)
- **Technique:** Security / Integrity Testing (SEC-02 Cryptographic Signature Verification)
- **Requirement:** SEC-02 Authentication Standard, SRS FR-10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / SEC-02 AUTHENTICATION`
- **Preconditions:** Fresh order created in `pending` state; genuine JWT captured and signature/payload bits altered.
- **Actor:** Attacker attempting signature forgery / payload tampering
- **Authentication Context:** Tampered JWT `Authorization: Bearer {{tamperedAdminToken}}`
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer {{tamperedAdminToken}}`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  ```json
  {
    "status": "confirmed"
  }
  ```
- **Action / Sequence:**
  1. Setup creates order in `pending` state.
  2. Attacker sends `PUT /api/admin/orders/:id/status` with tampered token.
  3. Query `GET /api/orders/:id` via admin token to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `401 Unauthorized`)
- **Expected Semantic Result:** Request rejected due to cryptographic signature mismatch; order status remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` using legitimate admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Provides behavioral SEC-02 evidence that tampered tokens fail authentication.

---

### FR10-AI-029 – SEC-02: Missing Authorization Header on Customer Cancellation Endpoint

- **Test Case ID:** `FR10-AI-029`
- **Title:** Missing Authorization Header on Customer Cancellation Endpoint (`PUT /api/orders/:id/cancel`)
- **Technique:** Security / Authentication Testing (SEC-02 Endpoint Gate)
- **Requirement:** SEC-02 Authentication Standard, SRS Section 4.10, API-SPEC `PUT /api/orders/:id/cancel`
- **Oracle Classification:** `SPECIFICATION-BACKED / SEC-02 AUTHENTICATION`
- **Preconditions:** Order created in `pending` state for customer $U_1$.
- **Actor:** Unauthenticated Client (`Anonymous`)
- **Authentication Context:** None (Missing `Authorization` header)
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/orders/:id/cancel`
- **Headers:** `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:** Empty `{}`
- **Action / Sequence:**
  1. Setup creates order for customer $U_1$ in `pending` state.
  2. Unauthenticated client sends `PUT /api/orders/:id/cancel` without `Authorization` header.
  3. Query `GET /api/orders/:id` via customer $U_1$ token to verify state remained `pending`.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `401 Unauthorized`)
- **Expected Semantic Result:** Request rejected because cancellation requires authenticated user context; order status remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` with $U_1$ token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Verifies authentication gate on customer-facing cancellation route.

---

### FR10-AI-030 – SEC-03: Normal Customer Role Attempting Valid Admin Transition

- **Test Case ID:** `FR10-AI-030`
- **Title:** Normal Customer Role Attempting Valid Admin Transition (`pending` $\rightarrow$ `confirmed`)
- **Technique:** Role-Based Access Control / RBAC Boundary Testing (SEC-03)
- **Requirement:** SEC-03 Authorization Standard, SRS FR-10, SRS FR-12, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / SEC-03 BEHAVIORAL AUTHORIZATION`
- **Preconditions:** Order created in `pending` state; customer token active for normal user.
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
    "status": "confirmed"
  }
  ```
- **Action / Sequence:**
  1. Helper creates order in `pending` state.
  2. Normal customer attempts `PUT /api/admin/orders/:id/status` with `status: "confirmed"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `403 Forbidden`)
- **Expected Semantic Result:** Request rejected due to insufficient privileges (`role = 'user'`); transition from `pending` to `confirmed` is reserved for admins.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` with admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Evaluates SEC-03 RBAC boundary on otherwise-valid state transition.

---

### FR10-AI-031 – SEC-03: Normal Customer Role Attempting Admin Cancellation Route

- **Test Case ID:** `FR10-AI-031`
- **Title:** Normal Customer Role Attempting Admin Cancellation Route (`pending` $\rightarrow$ `canceled`)
- **Technique:** Role-Based Access Control / RBAC Boundary Testing (SEC-03)
- **Requirement:** SEC-03 Authorization Standard, SRS Section 4.10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / SEC-03 BEHAVIORAL AUTHORIZATION`
- **Preconditions:** Order created in `pending` state; normal customer token active.
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
    "status": "canceled"
  }
  ```
- **Action / Sequence:**
  1. Helper creates order in `pending` state.
  2. Normal customer attempts to cancel via admin route `PUT /api/admin/orders/:id/status` with `status: "canceled"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `403 Forbidden`)
- **Expected Semantic Result:** Request rejected because the admin status endpoint requires administrator role regardless of whether the target state is cancellation.
- **Expected State After:** `pending`
- **Persistence Verification Plan:** Send `GET /api/orders/:id` with admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Verifies normal user cannot bypass route-level RBAC by invoking valid state values on admin endpoints.

---

### FR10-AI-032 – SEC-03: Normal Customer Role Attempting Admin Transit Dispatch

- **Test Case ID:** `FR10-AI-032`
- **Title:** Normal Customer Role Attempting Admin Transit Dispatch (`confirmed` $\rightarrow$ `shipping`)
- **Technique:** Role-Based Access Control / RBAC Boundary Testing (SEC-03 Post-Confirmation)
- **Requirement:** SEC-03 Authorization Standard, SRS FR-10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / SEC-03 BEHAVIORAL AUTHORIZATION`
- **Preconditions:** Order created and transitioned to `confirmed` by admin setup.
- **Actor:** Normal Customer (`role = 'user'`)
- **Authentication Context:** Valid customer JWT (`userToken`)
- **State Before:** `confirmed`
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
  1. Helper advances order to `confirmed`.
  2. Normal customer attempts `PUT /api/admin/orders/:id/status` with `status: "shipping"`.
  3. Query `GET /api/orders/:id` to verify state remained `confirmed`.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `403 Forbidden`)
- **Expected Semantic Result:** Request rejected due to non-admin role; order state remains confirmed.
- **Expected State After:** `confirmed` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` with admin token; assert `response.order.status === "confirmed"`.
- **Oracle Confidence:** HIGH
- **Notes:** Validates that SEC-03 RBAC restrictions continue to hold across all downstream order states.

---

### FR10-AI-033 – Cross-User Ownership Boundary: Customer B Cancelling Customer A's Pending Order

- **Test Case ID:** `FR10-AI-033`
- **Title:** Cross-User Ownership Boundary: Customer B Cancelling Customer A's `pending` Order
- **Technique:** Authorization & Data Isolation Testing (Cross-Tenant Ownership Boundary)
- **Requirement:** SRS Section 4.10, Business Authorization Discipline
- **Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED / OWNERSHIP BOUNDARY`
- **Preconditions:** Customer $U_A$ creates order in `pending` state; Customer $U_B$ is a distinct registered customer with valid token.
- **Actor:** Unrelated Authenticated Customer ($U_B$, `role = 'user'`)
- **Authentication Context:** Valid customer JWT of User B (`userBToken`)
- **State Before:** `pending` (owned by $U_A$)
- **Request Method:** `PUT`
- **Endpoint:** `/api/orders/:id/cancel`
- **Headers:** `Authorization: Bearer <userBToken>`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderAId}}`
- **Request Body:** Empty `{}`
- **Action / Sequence:**
  1. Setup creates order for User A $\rightarrow$ state is `pending`.
  2. User B sends `PUT /api/orders/{{orderAId}}/cancel` using User B's auth token.
  3. Query `GET /api/orders/{{orderAId}}` using User A / Admin token to verify state remained `pending`.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `403 Forbidden` or `404 Not Found`)
- **Expected Semantic Result:** Cancellation rejected; authenticated customer cannot cancel an order belonging to a different customer.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/{{orderAId}}` with $U_A$ / Admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Clean ownership isolation test with valid token, valid user role, and cancellable order state.

---

### FR10-AI-034 – Cross-User Ownership Boundary: Customer B Cancelling Customer A's Confirmed Order

- **Test Case ID:** `FR10-AI-034`
- **Title:** Cross-User Ownership Boundary: Customer B Cancelling Customer A's `confirmed` Order
- **Technique:** Authorization & Data Isolation Testing (Cross-Tenant Ownership Boundary)
- **Requirement:** SRS Section 4.10, Business Authorization Discipline
- **Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED / OWNERSHIP BOUNDARY`
- **Preconditions:** Customer $U_A$'s order is advanced to `confirmed` state; Customer $U_B$ has valid token.
- **Actor:** Unrelated Authenticated Customer ($U_B$, `role = 'user'`)
- **Authentication Context:** Valid customer JWT of User B (`userBToken`)
- **State Before:** `confirmed` (owned by $U_A$)
- **Request Method:** `PUT`
- **Endpoint:** `/api/orders/:id/cancel`
- **Headers:** `Authorization: Bearer <userBToken>`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderAId}}`
- **Request Body:** Empty `{}`
- **Action / Sequence:**
  1. Setup creates order for User A and transitions to `confirmed`.
  2. User B sends `PUT /api/orders/{{orderAId}}/cancel` using User B's auth token.
  3. Query `GET /api/orders/{{orderAId}}` using User A / Admin token to verify state remained `confirmed`.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `403 Forbidden` or `404 Not Found`)
- **Expected Semantic Result:** Cancellation rejected; User B cannot cancel User A's confirmed order prior to shipping.
- **Expected State After:** `confirmed` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/{{orderAId}}` with $U_A$ / Admin token; assert `response.order.status === "confirmed"`.
- **Oracle Confidence:** HIGH
- **Notes:** Evaluates ownership boundary in the second cancellable lifecycle state.

---

## 5. Raw AI Test Cases (Batch 4: Input Domain, Order ID Boundaries, Schema/Persistence & SEC-05)

---

### FR10-AI-035 – Status Domain: Undocumented Status Enum Value

- **Test Case ID:** `FR10-AI-035`
- **Title:** Undocumented Status Enum Value (`status: "processing"`)
- **Technique:** Equivalence Partitioning / Domain Boundary Testing (Invalid Status Enum)
- **Requirement:** SRS Section 4.10, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / DOMAIN VALIDATION`
- **Preconditions:** Fresh order in `pending` state; admin credentials active.
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
    "status": "processing"
  }
  ```
- **Action / Sequence:**
  1. Helper creates order $\rightarrow$ state is `pending`.
  2. Admin sends `PUT /api/admin/orders/:id/status` with `status: "processing"`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Status mutation rejected because `"processing"` is not one of the five documented states (`pending`, `confirmed`, `shipping`, `delivered`, `canceled`); order state remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` using admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Evaluates status enumeration validation on admin status route.

---

### FR10-AI-036 – Status Domain: Missing Required Status Property in Request Body

- **Test Case ID:** `FR10-AI-036`
- **Title:** Missing Required `status` Property in Mutation Body
- **Technique:** Schema / Required Property Validation
- **Requirement:** API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / SCHEMA VALIDATION`
- **Preconditions:** Fresh order in `pending` state; admin credentials active.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `pending`
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:** `{}`
- **Action / Sequence:**
  1. Helper creates order $\rightarrow$ state is `pending`.
  2. Admin sends `PUT /api/admin/orders/:id/status` with empty JSON body `{}`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Request rejected due to missing mandatory `status` property; order state remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` using admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Verifies required schema properties are strictly enforced.

---

### FR10-AI-037 – Status Domain: Null Status Value in Mutation Body

- **Test Case ID:** `FR10-AI-037`
- **Title:** Null `status` Value in Mutation Body
- **Technique:** Boundary Value Analysis / Null Value Handling
- **Requirement:** API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / INPUT VALIDATION`
- **Preconditions:** Fresh order in `pending` state; admin credentials active.
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
    "status": null
  }
  ```
- **Action / Sequence:**
  1. Helper creates order $\rightarrow$ state is `pending`.
  2. Admin sends `PUT /api/admin/orders/:id/status` with `status: null`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Request rejected; null values are invalid for the required status string field; order state remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` using admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Validates null rejection on state mutation route.

---

### FR10-AI-038 – Status Domain: Wrong JSON Type for Status Field

- **Test Case ID:** `FR10-AI-038`
- **Title:** Non-String JSON Type for `status` Field (`status: 123`)
- **Technique:** Data Type / Schema Robustness Testing
- **Requirement:** API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED / INPUT CONTRACT`
- **Preconditions:** Fresh order in `pending` state; admin credentials active.
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
    "status": 123
  }
  ```
- **Action / Sequence:**
  1. Helper creates order $\rightarrow$ state is `pending`.
  2. Admin sends `PUT /api/admin/orders/:id/status` with numeric status `123`.
  3. Query `GET /api/orders/:id` to verify state was NOT altered.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `400 Bad Request` or `422 Unprocessable Entity`)
- **Expected Semantic Result:** Request rejected due to data type mismatch; status field requires a string value; order state remains unchanged.
- **Expected State After:** `pending` (State remains UNCHANGED)
- **Persistence Verification Plan:** Send `GET /api/orders/:id` using admin token; assert `response.order.status === "pending"`.
- **Oracle Confidence:** HIGH
- **Notes:** Evaluates type safety and prevents unexpected numeric parsing or coercion.

---

### FR10-AI-039 – Order ID Partitions: Well-Formed Non-Existing Order ID

- **Test Case ID:** `FR10-AI-039`
- **Title:** Well-Formed Non-Existing Order ID (`:id = 999999`)
- **Technique:** Equivalence Partitioning (Non-Existent Resource ID)
- **Requirement:** API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / RESOURCE RESOLUTION`
- **Preconditions:** Admin credentials active; order ID `999999` is confirmed non-existent in database.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** Non-existent order target
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = 999999`
- **Request Body:**
  ```json
  {
    "status": "confirmed"
  }
  ```
- **Action / Sequence:**
  1. Admin sends `PUT /api/admin/orders/999999/status` with `status: "confirmed"`.
  2. Verify error response is returned and no side effects occur on other existing orders.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `404 Not Found`)
- **Expected Semantic Result:** Request rejected because the target order ID does not exist; no database record is created or mutated.
- **Expected State After:** Resource remains non-existent
- **Persistence Verification Plan:** Assert failure response; query existing orders to verify no unintended order mutations occurred.
- **Oracle Confidence:** HIGH
- **Notes:** Evaluates resource existence validation on state mutation route.

---

### FR10-AI-040 – Order ID Partitions: Malformed / Non-Numeric Order ID Path Parameter

- **Test Case ID:** `FR10-AI-040`
- **Title:** Malformed Non-Numeric Order ID Path Parameter (`:id = "not-an-id"`)
- **Technique:** Path Parameter Format / Boundary Testing
- **Requirement:** API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SPECIFICATION-BACKED / PARAMETER VALIDATION`
- **Preconditions:** Admin credentials active.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** N/A (Invalid path parameter syntax)
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = not-an-id`
- **Request Body:**
  ```json
  {
    "status": "confirmed"
  }
  ```
- **Action / Sequence:**
  1. Admin sends `PUT /api/admin/orders/not-an-id/status` with `status: "confirmed"`.
  2. Verify error response and assert no order state alteration.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `400 Bad Request` or `404 Not Found`)
- **Expected Semantic Result:** Request rejected due to malformed path parameter format; no order is selected or modified.
- **Expected State After:** N/A (No order mutated)
- **Persistence Verification Plan:** Assert failure response; verify existing orders remain unaltered.
- **Oracle Confidence:** HIGH
- **Notes:** Validates route parsing when non-integer strings are passed as path IDs without SQL injection payload.

---

### FR10-AI-041 – Response + Persistence Consistency on Valid Transition

- **Test Case ID:** `FR10-AI-041`
- **Title:** Valid Transition Response Schema and Persisted-State Consistency
- **Technique:** Response Schema & State Persistence Consistency Testing
- **Requirement:** API-SPEC `PUT /api/admin/orders/:id/status`, `GET /api/orders/:id`, SRS Section 4.10
- **Oracle Classification:** `SPECIFICATION-BACKED / RESPONSE CONTRACT & PERSISTENCE`
- **Preconditions:** Fresh order created in `pending` state; admin credentials active.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** `pending`
- **Request Method:** `PUT` (followed by `GET`)
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
  3. Validate mutation response body matches documented contract schema.
  4. Perform follow-up `GET /api/orders/:id` to assert persisted status consistency.
- **Expected HTTP Status:** `200 OK` (if documented)
- **Expected Semantic Result:**
  - **Mutation Response:** Confirms successful transition and returns documented order response attributes.
  - **Persisted State:** Subsequent `GET /api/orders/:id` returns `status: "confirmed"`.
- **Expected State After:** `confirmed`
- **Persistence Verification Plan:** Send `GET /api/orders/:id` with admin/user token; assert `response.order.status === "confirmed"`.
- **Oracle Confidence:** HIGH
- **Notes:** Isolates response schema conformance and verifies immediate read-after-write consistency on valid state transitions.

---

### FR10-AI-042 – SEC-05: Partial Black-Box Behavioral SQL Injection Probe in Order ID Path Parameter

- **Test Case ID:** `FR10-AI-042`
- **Title:** SEC-05 SQL Injection Behavioral Probe in Order ID Path Parameter
- **Technique:** Security / Injection Testing (SEC-05 Black-Box Parameter Probe)
- **Requirement:** SEC-05 SQL Injection Standard, API-SPEC `PUT /api/admin/orders/:id/status`
- **Oracle Classification:** `SEC-05 / PARTIAL BLACK-BOX BEHAVIORAL EVIDENCE`
- **Preconditions:** Multiple orders exist in database; admin credentials active.
- **Actor:** Attacker attempting SQL Injection via Path Parameter
- **Authentication Context:** Valid admin JWT (`adminToken`)
- **State Before:** Baseline existing database orders
- **Request Method:** `PUT`
- **Endpoint:** `/api/admin/orders/:id/status`
- **Headers:** `Authorization: Bearer <adminToken>`, `Content-Type: application/json`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = 1%27%20OR%20%271%27=%271` (URL-encoded `1' OR '1'='1`)
- **Request Body:**
  ```json
  {
    "status": "delivered"
  }
  ```
- **Action / Sequence:**
  1. Attacker sends `PUT /api/admin/orders/1%27%20OR%20%271%27=%271/status` with `status: "delivered"`.
  2. Verify injection string does NOT execute raw SQL or cause bulk / unauthorized order state mutation.
  3. Query existing orders to confirm no unauthorized mass state changes occurred.
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. `400 Bad Request` or `404 Not Found`)
- **Expected Semantic Result:** Injection attempt is neutralized; query is treated safely without executing injected SQL syntax; no unintended orders are updated.
- **Expected State After:** All database orders retain their original, unmutated states.
- **Persistence Verification Plan:** Query existing orders via `GET /api/orders/:id`; assert no unintended orders transitioned to `delivered`.
- **Oracle Confidence:** MEDIUM-HIGH (Black-box behavioral probe; provides behavioral evidence without claiming internal code proof).
- **Notes:** Behavioral SEC-05 black-box validation probe targeting path parameter routing and database query boundary.
