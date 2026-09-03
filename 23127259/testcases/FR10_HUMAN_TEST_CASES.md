# FR-10 Human-Designed Extension Test Cases Specification

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Suite Type:** Human Extension Test Suite ($\ge 5$ cases)
- **Total Cases:** `5` (`FR10-HUM-001` .. `FR10-HUM-005`)
- **Provenance:** Student-selected and finalized Human Extension cases after AI-assisted coverage-gap analysis.

---

### FR10-HUM-001
- **Test Case ID:** `FR10-HUM-001`
- **Human Selection Source:** Gap `G-04` (State-Machine Continuity & Recovery After Rejected Mutation)
- **Provenance:** Student-selected and finalized Human Extension case after AI-assisted coverage-gap analysis.
- **Title:** State Machine Continuity & Recovery: Legal Admin Confirmation (`pending` $\rightarrow$ `confirmed`) Following Rejected Illegal Forward Skip (`pending` $\rightarrow$ `shipping`)
- **Technique:** State Transition Testing / Error Recovery Sequence / Multi-Operation Continuity
- **Requirement / Gap:** SRS Section 4.10, FR-10 State Machine Invariants, Gap `G-04`
- **Oracle Classification:** `SPECIFICATION-BACKED / STATE-MACHINE CONTINUITY`
- **Why AI Coverage Missed This:** AI generation focused on single-request atomic checks; `FR10-AI-009` verified only that `pending -> shipping` is rejected, leaving unverified whether the order entity or state-machine worker was corrupted or locked by the failed attempt.
- **Why Distinct From Existing AI Cases:** Unlike `FR10-AI-009` (isolated rejection) or `FR10-AI-001` (isolated transition), this multi-step test executes an illegal attempt, verifies non-mutation, and immediately tests transactional recovery via a subsequent valid lifecycle transition.
- **Preconditions:** SUT is running; authenticated Admin credentials and User credentials available; fresh order created in `pending` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** `Authorization: Bearer {{adminToken}}`
- **State Before:** `pending`
- **Request Method:** Step 1: `PUT`, Step 2: `GET`, Step 3: `PUT`, Step 4: `GET`
- **Endpoint:** `PUT /api/admin/orders/:id/status`, `GET /api/orders/:id`
- **Headers:** `Content-Type: application/json`, `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}` (Valid numeric order ID)
- **Request Body:**
  - Step 1 (Illegal Skip): `{"status": "shipping"}`
  - Step 3 (Valid Transition): `{"status": "confirmed"}`
- **Action / Sequence:**
  1. Create a fresh test order in `pending` state (`orderId`).
  2. Send `PUT /api/admin/orders/{{orderId}}/status` with `{"status": "shipping"}`.
  3. Verify illegal mutation is rejected (non-success client error).
  4. Send `GET /api/orders/{{orderId}}` to confirm order remains `pending`.
  5. Send `PUT /api/admin/orders/{{orderId}}/status` with `{"status": "confirmed"}`.
  6. Verify mutation succeeds (HTTP 200).
  7. Send `GET /api/orders/{{orderId}}` to verify persisted state is `confirmed`.
- **Expected HTTP Status:**
  - Step 2 (Illegal skip): `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. 400 Bad Request)
  - Step 4 (Read query): `200 OK`
  - Step 5 (Legal confirmation): `200 OK`
  - Step 7 (Read query): `200 OK`
- **Expected Semantic Result:** Illegal transition is rejected without modifying state; order remains fully operational and transitions cleanly to `confirmed` upon valid Admin request.
- **Expected State After:** `confirmed`
- **Persistence Verification:** Step 7 query returns `{"status": "confirmed"}` for `{{orderId}}`.
- **Bug Reporting Limitation:** If Step 2 succeeds or modifies state, file as illegal transition bug; if Step 5 fails after Step 2 rejection, file as state machine lock/corruption bug.
- **Notes:** Mandatory anti-cheat header `X-Student-Id: 23127259` present on all requests.

---

### FR10-HUM-002
- **Test Case ID:** `FR10-HUM-002`
- **Human Selection Source:** Gap `G-05` (Multi-Entity State Isolation)
- **Provenance:** Student-selected and finalized Human Extension case after AI-assisted coverage-gap analysis.
- **Title:** Multi-Entity State Isolation: Transitioning Order A (`pending` $\rightarrow$ `confirmed`) Leaves Independent Order B Strictly in `pending` State
- **Technique:** Multi-Entity Boundary Testing / Database Isolation / Side-Effect Absence Verification
- **Requirement / Gap:** SRS Section 4.10, Relational Entity Independence, Gap `G-05`
- **Oracle Classification:** `SPECIFICATION-BACKED / ENTITY-STATE ISOLATION`
- **Why AI Coverage Missed This:** AI generation evaluated transitions on single order entities in isolation, leaving unverified whether SQL `UPDATE` queries omitted `WHERE id = :id` filters or caused unintended bulk state updates.
- **Why Distinct From Existing AI Cases:** Distinct from all AI cases because it establishes two concurrently existing entities in identical initial states and proves that mutation targeting Entity A has zero side-effects on Entity B.
- **Preconditions:** SUT is running; authenticated Admin credentials available; two distinct orders (`orderAId`, `orderBId`) created in `pending` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** `Authorization: Bearer {{adminToken}}`
- **State Before:** Order A: `pending`, Order B: `pending`
- **Request Method:** Step 1: `PUT`, Step 2: `GET`, Step 3: `GET`
- **Endpoint:** `PUT /api/admin/orders/:id/status`, `GET /api/orders/:id`
- **Headers:** `Content-Type: application/json`, `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Path Parameters:** Step 1 & 2: `:id = {{orderAId}}`, Step 3: `:id = {{orderBId}}`
- **Request Body:** Step 1 (Mutate Order A only): `{"status": "confirmed"}`
- **Action / Sequence:**
  1. Create Order A in `pending` (`orderAId`).
  2. Create Order B in `pending` (`orderBId`).
  3. Send `PUT /api/admin/orders/{{orderAId}}/status` with `{"status": "confirmed"}`.
  4. Verify Order A mutation response returns `status = 'confirmed'`.
  5. Send `GET /api/orders/{{orderAId}}` and verify persisted state is `confirmed`.
  6. Send `GET /api/orders/{{orderBId}}` and verify persisted state remains `pending`.
- **Expected HTTP Status:**
  - Step 3 (Mutate Order A): `200 OK`
  - Step 5 (Read Order A): `200 OK`
  - Step 6 (Read Order B): `200 OK`
- **Expected Semantic Result:** Order A transitions to `confirmed`; Order B is strictly unaffected and remains in `pending` state.
- **Expected State After:** Order A: `confirmed`, Order B: `pending`
- **Persistence Verification:** Independent `GET` queries confirm Order A is `confirmed` and Order B is `pending`.
- **Bug Reporting Limitation:** If Order B status changes to `confirmed` after Step 3, file as critical multi-entity bulk mutation defect.
- **Notes:** Tests external entity isolation without making speculative claims about internal DB isolation levels.

---

### FR10-HUM-003
- **Test Case ID:** `FR10-HUM-003`
- **Human Selection Source:** Gap `G-07` (Lifecycle Continues After Barred Customer Cancellation)
- **Provenance:** Student-selected and finalized Human Extension case after AI-assisted coverage-gap analysis.
- **Title:** Downstream Fulfillment Continuity: Legitimate Admin Completion (`shipping` $\rightarrow$ `delivered`) Following Barred In-Transit Customer Cancellation
- **Technique:** End-to-End Business Flow / Lifecycle Continuity / Negative Action Recovery
- **Requirement / Gap:** SRS Section 4.10, Fulfillment Completion Rules, Gap `G-07`
- **Oracle Classification:** `SPECIFICATION-BACKED / LIFECYCLE CONTINUITY`
- **Why AI Coverage Missed This:** `FR10-AI-016` tested only the isolated rejection of customer cancellation during shipping; no AI case verified that subsequent legitimate fulfillment to terminal `delivered` remained fully operational after the customer's rejected action.
- **Why Distinct From Existing AI Cases:** Combines negative customer authorization boundary with downstream fulfillment completion on a single continuous entity flow.
- **Preconditions:** SUT running; authenticated Customer and Admin credentials available; order created by Customer.
- **Actor:** Step 1-3: Admin, Step 4: Owner Customer, Step 7: Admin
- **Authentication Context:** Steps 1-3 & 7: `Authorization: Bearer {{adminToken}}`, Step 4: `Authorization: Bearer {{userToken}}`
- **State Before:** `pending`
- **Request Method:** Step 1: `PUT`, Step 2: `PUT`, Step 3: `PUT`, Step 4: `GET`, Step 5: `PUT`, Step 6: `GET`
- **Endpoint:** `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel`, `GET /api/orders/:id`
- **Headers:** `Content-Type: application/json`, `X-Student-Id: 23127259`, appropriate `Authorization` header per step
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:**
  - Step 1 (Confirm): `{"status": "confirmed"}`
  - Step 2 (Dispatch): `{"status": "shipping"}`
  - Step 3 (Customer Cancel): `{}` (Cancel endpoint)
  - Step 5 (Deliver): `{"status": "delivered"}`
- **Action / Sequence:**
  1. Admin transitions order: `pending` $\rightarrow$ `confirmed`.
  2. Admin transitions order: `confirmed` $\rightarrow$ `shipping`.
  3. Owner Customer attempts `PUT /api/orders/{{orderId}}/cancel`.
  4. Verify customer cancellation is rejected (non-success).
  5. Query `GET /api/orders/{{orderId}}` to confirm state remains `shipping`.
  6. Admin sends `PUT /api/admin/orders/{{orderId}}/status` with `{"status": "delivered"}`.
  7. Verify Admin fulfillment succeeds (`200 OK`).
  8. Query `GET /api/orders/{{orderId}}` to confirm final terminal state is `delivered`.
- **Expected HTTP Status:**
  - Step 1 & 2 (Admin transitions): `200 OK`
  - Step 3 (Customer cancel attempt): `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (e.g. 400 or 403)
  - Step 5 (Query in-transit): `200 OK`
  - Step 6 (Admin deliver): `200 OK`
  - Step 8 (Query delivered): `200 OK`
- **Expected Semantic Result:** Customer cancellation during shipping is rejected; order state remains `shipping`; subsequent Admin delivery succeeds and terminates fulfillment cleanly.
- **Expected State After:** `delivered`
- **Persistence Verification:** Step 8 query confirms persisted state is `delivered`.
- **Bug Reporting Limitation:** If Step 3 cancels the in-transit order, report unauthorized cancellation bug; if Step 6 fails after Step 3 rejection, report fulfillment blocker bug.
- **Notes:** Models realistic customer-service dispute flow where attempted user cancellation must not break warehouse delivery completion.

---

### FR10-HUM-004
- **Test Case ID:** `FR10-HUM-004`
- **Human Selection Source:** Gap `G-01` (Same-State / Idempotent Mutation Probe)
- **Provenance:** Student-selected and finalized Human Extension case after AI-assisted coverage-gap analysis.
- **Title:** Exploratory Same-State Self-Loop Probe: Admin Submits Redundant Mutation (`confirmed` $\rightarrow$ `confirmed`)
- **Technique:** Exploratory Testing / FSM Self-Loop Analysis / API Idempotency Probe
- **Requirement / Gap:** SRS Section 4.10 (Spec-Undefined Same-State Behavior), Gap `G-01`
- **Oracle Classification:** `EXPLORATORY / API CONTRACT`
- **Why AI Coverage Missed This:** AI generation strictly tested transitions between distinct state pairs ($S_i \neq S_j$); self-loop mutations ($S_i \rightarrow S_i$) were omitted.
- **Why Distinct From Existing AI Cases:** Sole test in the suite evaluating same-state update semantics on the Admin mutation route.
- **Preconditions:** SUT running; authenticated Admin credentials available; test order in `confirmed` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** `Authorization: Bearer {{adminToken}}`
- **State Before:** `confirmed`
- **Request Method:** Step 1: `PUT`, Step 2: `GET`
- **Endpoint:** `PUT /api/admin/orders/:id/status`, `GET /api/orders/:id`
- **Headers:** `Content-Type: application/json`, `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:** `{"status": "confirmed"}`
- **Action / Sequence:**
  1. Establish order in `confirmed` state.
  2. Send `PUT /api/admin/orders/{{orderId}}/status` with `{"status": "confirmed"}`.
  3. Observe server response (either HTTP 200 no-op or 4xx error).
  4. Send `GET /api/orders/{{orderId}}` to verify persisted state remains `confirmed`.
- **Expected HTTP Status:** `OBSERVATIONAL – NOT NORMATIVELY SPECIFIED` (Accepts 200 OK idempotent success OR 4xx rejection).
- **Expected Semantic Result:** Server either treats redundant transition as idempotent success or rejects it safely; under all circumstances, the order remains in `confirmed` state and is not corrupted.
- **Expected State After:** `confirmed`
- **Persistence Verification:** Step 4 read query confirms persisted state is `confirmed`.
- **Bug Reporting Limitation:** **NON-NORMATIVE ORACLE.** Same-state behavior is SPEC-UNDEFINED. Do NOT file a formal FR-10 bug whether the server responds with 200 or 400, provided the order remains in `confirmed` state.
- **Notes:** Recorded strictly as an exploratory finding for API contract characterization.

---

### FR10-HUM-005
- **Test Case ID:** `FR10-HUM-005`
- **Human Selection Source:** Gap `G-08` (Non-JSON Content-Type Robustness)
- **Provenance:** Student-selected and finalized Human Extension case after AI-assisted coverage-gap analysis.
- **Title:** Exploratory Request Encoding Robustness: Admin Submits Mutation Payload with `Content-Type: text/plain`
- **Technique:** Robustness Testing / Media Type Validation / Content Negotiation Boundary
- **Requirement / Gap:** API Specification Request Encoding Invariants, Gap `G-08`
- **Oracle Classification:** `EXPLORATORY / API CONTRACT`
- **Why AI Coverage Missed This:** AI generation tested input domains and schema keys within valid `application/json` formatting only; non-standard header encodings were unexamined.
- **Why Distinct From Existing AI Cases:** Uniquely isolates HTTP header media-type negotiation on status mutation endpoints to detect unhandled server crashes (HTTP 500).
- **Preconditions:** SUT running; authenticated Admin credentials available; test order in `pending` state.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** `Authorization: Bearer {{adminToken}}`
- **State Before:** `pending`
- **Request Method:** Step 1: `PUT`, Step 2: `GET`
- **Endpoint:** `PUT /api/admin/orders/:id/status`, `GET /api/orders/:id`
- **Headers:** `Content-Type: text/plain`, `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Path Parameters:** `:id = {{orderId}}`
- **Request Body:** `{"status":"confirmed"}` (Raw text body string)
- **Action / Sequence:**
  1. Establish order in `pending` state.
  2. Send `PUT /api/admin/orders/{{orderId}}/status` with `Content-Type: text/plain` and raw body string `{"status":"confirmed"}`.
  3. Observe server response handling.
  4. Send `GET /api/orders/{{orderId}}` to verify persisted state remains `pending` (or cleanly updated if parser auto-detects JSON).
- **Expected HTTP Status:** `OBSERVATIONAL – NOT NORMATIVELY SPECIFIED` (Server may reject with 400/415 or gracefully parse as 200).
- **Expected Semantic Result:** Malformed media transport is handled without unhandled 500 crash or database corruption; state remains predictable.
- **Expected State After:** `pending` (or `confirmed` if server accepts text/plain JSON).
- **Persistence Verification:** Step 4 read query verifies order is intact and uncorrupted.
- **Bug Reporting Limitation:** **NON-NORMATIVE ORACLE.** If server returns HTTP 500, record as an exploratory robustness finding / observation rather than a formal FR-10 specification bug.
- **Notes:** Tests server robustness against non-conforming API clients.
