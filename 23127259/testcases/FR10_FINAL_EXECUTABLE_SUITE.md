# FR-10 Final Executable Test Suite Specification

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Status:** **FINAL EXECUTABLE SPECIFICATION (POST-HUMAN AUDIT & EXTENSION)**
- **Total Formal Executable Test Cases:** `46` (41 Usable AI-Derived Cases + 5 Human Extension Cases)
- **Rejected Raw AI Cases:** `1` (`FR10-AI-012` excluded from execution suite)

---

## 1. Executive Suite Summary & Composition

This document defines the authoritative, finalized **46-case executable test suite** for feature **FR-10 (Order Status & State Machine)**. It integrates:
1. **41 Audited & Corrected AI-Derived Test Cases:** Derived from the frozen raw draft (`FR10_AI_DRAFT.md`), audited by the student in `TC_AUDIT_FR10.md`, and refined with disciplined non-normative oracles for `FR10-AI-033`, `FR10-AI-034`, and `FR10-AI-040` in `FR10_HUMAN_AUDIT_CORRECTIONS.md`.
2. **5 Student-Selected Human Extension Test Cases:** Selected and finalized by the student in `FR10_HUMAN_TEST_CASES.md` (`FR10-HUM-001` .. `FR10-HUM-005`) addressing state-machine continuity (`G-04`), multi-entity isolation (`G-05`), downstream fulfillment (`G-07`), same-state self-loop (`G-01`), and media type robustness (`G-08`).
3. **Formal Exclusion of `FR10-AI-012`:** The raw AI case combining customer authorization failure with an invalid forward skip transition is formally rejected and omitted from this executable suite.

---

## 2. Test Suite Classification & Oracle Discipline

- **`SPECIFICATION-BACKED` (41 Cases):** Directly verifiable against explicit SRS rules, state transition matrices, and security invariants (`SEC-02`, `SEC-03`, `SEC-05`).
- **`PARTIALLY SPECIFICATION-BACKED` (3 Cases):** `FR10-AI-033`, `FR10-AI-034` (business authorization/ownership), and `FR10-AI-040` (input robustness). Assert safe non-success and non-mutation without enforcing unstated status codes.
- **`EXPLORATORY / API CONTRACT` (2 Cases):** `FR10-HUM-004` (same-state update) and `FR10-HUM-005` (non-JSON transport). Non-normative oracles designed to observe server behavior and guard against state corruption.

---

## 3. Formal Executable Test Cases Inventory

### FR10-AI-001 – Valid Forward Transition: Admin Confirms Pending Order (pending -> confirmed)
- **Formal Test ID:** `FR10-AI-001`
- **Folder:** `01 – Valid Forward & Lifecycle Transitions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** State Transition Testing / Happy Path
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `200 OK`
- **Expected State After:** `confirmed`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `confirmed`.
- **Description & Objective:** Verify Admin can transition an order from pending to confirmed.

---
### FR10-AI-002 – Valid Forward Transition: Admin Dispatches Confirmed Order (confirmed -> shipping)
- **Formal Test ID:** `FR10-AI-002`
- **Folder:** `01 – Valid Forward & Lifecycle Transitions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** State Transition Testing / Happy Path
- **Actor:** Admin
- **State Before:** `confirmed`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "shipping"}`
- **Expected HTTP Status:** `200 OK`
- **Expected State After:** `shipping`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `shipping`.
- **Description & Objective:** Verify Admin can transition an order from confirmed to shipping.

---
### FR10-AI-003 – Valid Forward Transition: Admin Delivers Shipping Order (shipping -> delivered)
- **Formal Test ID:** `FR10-AI-003`
- **Folder:** `01 – Valid Forward & Lifecycle Transitions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** State Transition Testing / Happy Path / Terminal Transition
- **Actor:** Admin
- **State Before:** `shipping`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "delivered"}`
- **Expected HTTP Status:** `200 OK`
- **Expected State After:** `delivered`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `delivered`.
- **Description & Objective:** Verify Admin can transition an in-transit order to terminal delivered state.

---
### FR10-AI-004 – End-to-End Complete Linear Lifecycle Flow (pending -> confirmed -> shipping -> delivered)
- **Formal Test ID:** `FR10-AI-004`
- **Folder:** `01 – Valid Forward & Lifecycle Transitions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** End-to-End Lifecycle Sequence / Integration
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "delivered"}`
- **Expected HTTP Status:** `200 OK across all steps`
- **Expected State After:** `delivered`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `delivered`.
- **Description & Objective:** Verify full linear 4-stage progression on a single continuous order entity.

---
### FR10-AI-005 – Valid Customer Self-Service Cancellation on Pending Order (pending -> canceled)
- **Formal Test ID:** `FR10-AI-005`
- **Folder:** `02 – Order Cancellation Pathways`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** State Transition Testing / Customer Self-Service
- **Actor:** Owner Customer (User A)
- **State Before:** `pending`
- **Target Route:** `PUT /api/orders/{{orderId}}/cancel`
- **Request Body:** `{}`
- **Expected HTTP Status:** `200 OK`
- **Expected State After:** `canceled`
- **Persistence Verification:** Authorized `User A / Admin` query verifies order state is `canceled`.
- **Description & Objective:** Verify owner customer can cancel a pending order.

---
### FR10-AI-006 – Valid Customer Self-Service Cancellation on Confirmed Order (confirmed -> canceled)
- **Formal Test ID:** `FR10-AI-006`
- **Folder:** `02 – Order Cancellation Pathways`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** State Transition Testing / Pre-Shipment Cancellation
- **Actor:** Owner Customer (User A)
- **State Before:** `confirmed`
- **Target Route:** `PUT /api/orders/{{orderId}}/cancel`
- **Request Body:** `{}`
- **Expected HTTP Status:** `200 OK`
- **Expected State After:** `canceled`
- **Persistence Verification:** Authorized `User A / Admin` query verifies order state is `canceled`.
- **Description & Objective:** Verify owner customer can cancel a confirmed pre-shipment order.

---
### FR10-AI-007 – Valid Admin Status Cancellation on Pending Order (pending -> canceled)
- **Formal Test ID:** `FR10-AI-007`
- **Folder:** `02 – Order Cancellation Pathways`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** State Transition Testing / Administrative Control
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "canceled"}`
- **Expected HTTP Status:** `200 OK`
- **Expected State After:** `canceled`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `canceled`.
- **Description & Objective:** Verify Admin can cancel a pending order via status mutation endpoint.

---
### FR10-AI-008 – Valid Admin Status Cancellation on Confirmed Order (confirmed -> canceled)
- **Formal Test ID:** `FR10-AI-008`
- **Folder:** `02 – Order Cancellation Pathways`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** State Transition Testing / Administrative Control
- **Actor:** Admin
- **State Before:** `confirmed`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "canceled"}`
- **Expected HTTP Status:** `200 OK`
- **Expected State After:** `canceled`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `canceled`.
- **Description & Objective:** Verify Admin can cancel a confirmed order via status mutation endpoint.

---
### FR10-AI-009 – Invalid Forward Skip: Admin Attempts Direct Transition pending -> shipping
- **Formal Test ID:** `FR10-AI-009`
- **Folder:** `03 – Invalid Forward Skips & Backward Regressions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Negative State Transition / Forward Skip Boundary
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "shipping"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify direct forward skip bypassing confirmed is rejected and state remains pending.

---
### FR10-AI-010 – Invalid Forward Skip: Admin Attempts Direct Transition pending -> delivered
- **Formal Test ID:** `FR10-AI-010`
- **Folder:** `03 – Invalid Forward Skips & Backward Regressions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Negative State Transition / Multi-Stage Forward Skip
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "delivered"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify direct forward skip from pending to delivered is rejected.

---
### FR10-AI-011 – Invalid Forward Skip: Admin Attempts Direct Transition confirmed -> delivered
- **Formal Test ID:** `FR10-AI-011`
- **Folder:** `03 – Invalid Forward Skips & Backward Regressions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Negative State Transition / Skip Shipping Boundary
- **Actor:** Admin
- **State Before:** `confirmed`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "delivered"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `confirmed`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `confirmed`.
- **Description & Objective:** Verify direct forward skip bypassing shipping is rejected and state remains confirmed.

---
### FR10-AI-013 – Invalid Backward Regression: Admin Attempts confirmed -> pending
- **Formal Test ID:** `FR10-AI-013`
- **Folder:** `03 – Invalid Forward Skips & Backward Regressions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Negative State Transition / Backward Regression
- **Actor:** Admin
- **State Before:** `confirmed`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "pending"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `confirmed`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `confirmed`.
- **Description & Objective:** Verify backward regression from confirmed to pending is prohibited.

---
### FR10-AI-014 – Invalid Backward Regression: Admin Attempts shipping -> confirmed
- **Formal Test ID:** `FR10-AI-014`
- **Folder:** `03 – Invalid Forward Skips & Backward Regressions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Negative State Transition / Backward Regression
- **Actor:** Admin
- **State Before:** `shipping`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `shipping`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `shipping`.
- **Description & Objective:** Verify backward regression from shipping to confirmed is prohibited.

---
### FR10-AI-015 – Invalid Backward Regression: Admin Attempts shipping -> pending
- **Formal Test ID:** `FR10-AI-015`
- **Folder:** `03 – Invalid Forward Skips & Backward Regressions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Negative State Transition / Multi-Stage Backward Regression
- **Actor:** Admin
- **State Before:** `shipping`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "pending"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `shipping`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `shipping`.
- **Description & Objective:** Verify multi-stage backward regression from shipping to pending is prohibited.

---
### FR10-AI-016 – Invalid Customer Cancellation on In-Transit Order (shipping -> canceled rejected)
- **Formal Test ID:** `FR10-AI-016`
- **Folder:** `03 – Invalid Forward Skips & Backward Regressions`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Negative State Transition / In-Transit Lockout
- **Actor:** Owner Customer (User A)
- **State Before:** `shipping`
- **Target Route:** `PUT /api/orders/{{orderId}}/cancel`
- **Request Body:** `{}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `shipping`
- **Persistence Verification:** Authorized `User A / Admin` query verifies order state is `shipping`.
- **Description & Objective:** Verify customer cannot cancel an order that has entered shipping status.

---
### FR10-AI-017 – Terminal State Immutability: Prohibit Mutation delivered -> pending
- **Formal Test ID:** `FR10-AI-017`
- **Folder:** `04 – Terminal-State Immutability`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Terminal State Immutability Testing
- **Actor:** Admin
- **State Before:** `delivered`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "pending"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `delivered`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `delivered`.
- **Description & Objective:** Verify delivered order cannot transition to pending.

---
### FR10-AI-018 – Terminal State Immutability: Prohibit Mutation delivered -> confirmed
- **Formal Test ID:** `FR10-AI-018`
- **Folder:** `04 – Terminal-State Immutability`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Terminal State Immutability Testing
- **Actor:** Admin
- **State Before:** `delivered`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `delivered`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `delivered`.
- **Description & Objective:** Verify delivered order cannot transition to confirmed.

---
### FR10-AI-019 – Terminal State Immutability: Prohibit Mutation delivered -> shipping
- **Formal Test ID:** `FR10-AI-019`
- **Folder:** `04 – Terminal-State Immutability`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Terminal State Immutability Testing
- **Actor:** Admin
- **State Before:** `delivered`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "shipping"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `delivered`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `delivered`.
- **Description & Objective:** Verify delivered order cannot transition to shipping.

---
### FR10-AI-020 – Terminal State Immutability: Prohibit Mutation delivered -> canceled
- **Formal Test ID:** `FR10-AI-020`
- **Folder:** `04 – Terminal-State Immutability`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Terminal State Immutability Testing
- **Actor:** Admin
- **State Before:** `delivered`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "canceled"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `delivered`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `delivered`.
- **Description & Objective:** Verify delivered order cannot be canceled.

---
### FR10-AI-021 – Terminal State Immutability: Prohibit Mutation canceled -> pending
- **Formal Test ID:** `FR10-AI-021`
- **Folder:** `04 – Terminal-State Immutability`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Terminal State Immutability Testing
- **Actor:** Admin
- **State Before:** `canceled`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "pending"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `canceled`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `canceled`.
- **Description & Objective:** Verify canceled order cannot be revived to pending.

---
### FR10-AI-022 – Terminal State Immutability: Prohibit Mutation canceled -> confirmed
- **Formal Test ID:** `FR10-AI-022`
- **Folder:** `04 – Terminal-State Immutability`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Terminal State Immutability Testing
- **Actor:** Admin
- **State Before:** `canceled`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `canceled`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `canceled`.
- **Description & Objective:** Verify canceled order cannot transition to confirmed.

---
### FR10-AI-023 – Terminal State Immutability: Prohibit Mutation canceled -> shipping
- **Formal Test ID:** `FR10-AI-023`
- **Folder:** `04 – Terminal-State Immutability`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Terminal State Immutability Testing
- **Actor:** Admin
- **State Before:** `canceled`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "shipping"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `canceled`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `canceled`.
- **Description & Objective:** Verify canceled order cannot transition to shipping.

---
### FR10-AI-024 – Terminal State Immutability: Prohibit Mutation canceled -> delivered
- **Formal Test ID:** `FR10-AI-024`
- **Folder:** `04 – Terminal-State Immutability`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Terminal State Immutability Testing
- **Actor:** Admin
- **State Before:** `canceled`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "delivered"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `canceled`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `canceled`.
- **Description & Objective:** Verify canceled order cannot transition to delivered.

---
### FR10-AI-025 – SEC-02 Authentication Boundary: Admin Status Mutation Without Authorization Header
- **Formal Test ID:** `FR10-AI-025`
- **Folder:** `05 – SEC-02 Authentication Invariants`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Security / Authentication Header Absence
- **Actor:** Unauthenticated Client
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `401 Unauthorized`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify unauthenticated request to admin status endpoint is rejected with 401.

---
### FR10-AI-026 – SEC-02 Authentication Boundary: Admin Status Mutation With Malformed Bearer Token
- **Formal Test ID:** `FR10-AI-026`
- **Folder:** `05 – SEC-02 Authentication Invariants`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Security / Malformed Token
- **Actor:** Unauthenticated Client
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `401 Unauthorized`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify request with invalid signature/malformed JWT is rejected with 401.

---
### FR10-AI-027 – SEC-02 Authentication Boundary: Admin Status Mutation With Expired Bearer Token
- **Formal Test ID:** `FR10-AI-027`
- **Folder:** `05 – SEC-02 Authentication Invariants`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Security / Expired Token
- **Actor:** Unauthenticated Client
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `401 Unauthorized`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify request with expired JWT is rejected with 401.

---
### FR10-AI-028 – SEC-02 Authentication Boundary: Customer Cancellation Without Authorization Header
- **Formal Test ID:** `FR10-AI-028`
- **Folder:** `05 – SEC-02 Authentication Invariants`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Security / Authentication Header Absence
- **Actor:** Unauthenticated Client
- **State Before:** `pending`
- **Target Route:** `PUT /api/orders/{{orderId}}/cancel`
- **Request Body:** `{}`
- **Expected HTTP Status:** `401 Unauthorized`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `User A / Admin` query verifies order state is `pending`.
- **Description & Objective:** Verify unauthenticated cancel request is rejected with 401.

---
### FR10-AI-029 – SEC-02 Authentication Boundary: Customer Cancellation With Malformed Bearer Token
- **Formal Test ID:** `FR10-AI-029`
- **Folder:** `05 – SEC-02 Authentication Invariants`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Security / Malformed Token
- **Actor:** Unauthenticated Client
- **State Before:** `pending`
- **Target Route:** `PUT /api/orders/{{orderId}}/cancel`
- **Request Body:** `{}`
- **Expected HTTP Status:** `401 Unauthorized`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `User A / Admin` query verifies order state is `pending`.
- **Description & Objective:** Verify malformed JWT cancel request is rejected with 401.

---
### FR10-AI-030 – SEC-03 RBAC Boundary: Normal Customer Token Targeting Admin Status Mutation Endpoint
- **Formal Test ID:** `FR10-AI-030`
- **Folder:** `06 – SEC-03 Role-Based Access Control (RBAC)`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Security / RBAC Privilege Escalation Guard
- **Actor:** Customer (User A)
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `403 Forbidden / 4xx`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify normal customer cannot access admin status update route.

---
### FR10-AI-031 – SEC-03 RBAC Boundary: Admin Token Targeting Customer Cancellation Endpoint
- **Formal Test ID:** `FR10-AI-031`
- **Folder:** `06 – SEC-03 Role-Based Access Control (RBAC)`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Security / Role Boundary Probe
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/orders/{{orderId}}/cancel`
- **Request Body:** `{}`
- **Expected HTTP Status:** `403 Forbidden / 4xx / Safe Rejection`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify Admin token on customer cancel route is handled safely without unauthorized cross-route mutation.

---
### FR10-AI-032 – SEC-03 RBAC Boundary: Non-Admin Role Token Targeting Admin Status Mutation Endpoint
- **Formal Test ID:** `FR10-AI-032`
- **Folder:** `06 – SEC-03 Role-Based Access Control (RBAC)`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Security / Unknown Role RBAC Rejection
- **Actor:** Guest / Non-Admin Role
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `403 Forbidden / 4xx`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify unprivileged non-admin token cannot update order status.

---
### FR10-AI-033 – Cross-User Ownership: Customer B Probes Cancellation on Customer A's Pending Order
- **Formal Test ID:** `FR10-AI-033`
- **Folder:** `07 – Cross-User Ownership & Partial Authorization`
- **Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION`
- **Technique:** Authorization / Multi-Tenant Isolation / Cross-User Probe
- **Actor:** Customer B (Non-Owner)
- **State Before:** `pending`
- **Target Route:** `PUT /api/orders/{{orderAId}}/cancel`
- **Request Body:** `{}`
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED (e.g. 403/404)`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Customer A / Admin` query verifies order state is `pending`.
- **Description & Objective:** Verify Customer B cannot cancel Customer A's pending order; state verified by Customer A/Admin.

---
### FR10-AI-034 – Cross-User Ownership: Customer B Probes Cancellation on Customer A's Confirmed Order
- **Formal Test ID:** `FR10-AI-034`
- **Folder:** `07 – Cross-User Ownership & Partial Authorization`
- **Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION`
- **Technique:** Authorization / Multi-Tenant Isolation / Cross-User Probe
- **Actor:** Customer B (Non-Owner)
- **State Before:** `confirmed`
- **Target Route:** `PUT /api/orders/{{orderAId}}/cancel`
- **Request Body:** `{}`
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED (e.g. 403/404)`
- **Expected State After:** `confirmed`
- **Persistence Verification:** Authorized `Customer A / Admin` query verifies order state is `confirmed`.
- **Description & Objective:** Verify Customer B cannot cancel Customer A's confirmed order; state verified by Customer A/Admin.

---
### FR10-AI-035 – Input Domain: Admin Status Mutation With Undocumented Enum ('processing')
- **Formal Test ID:** `FR10-AI-035`
- **Folder:** `08 – Status Enum & Order-ID Input Domain`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Equivalence Partitioning / Invalid Enum Domain
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "processing"}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify status value outside the 5 documented lifecycle states is rejected.

---
### FR10-AI-036 – Input Domain: Admin Status Mutation With Missing Mandatory 'status' Body Property
- **Formal Test ID:** `FR10-AI-036`
- **Folder:** `08 – Status Enum & Order-ID Input Domain`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Schema Validation / Missing Mandatory Key
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify payload missing status key is rejected with 400 Bad Request.

---
### FR10-AI-037 – Input Domain: Admin Status Mutation With Explicit Null Status Property
- **Formal Test ID:** `FR10-AI-037`
- **Folder:** `08 – Status Enum & Order-ID Input Domain`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Schema Validation / Null Value Rejection
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": null}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify null status property is rejected with 400 Bad Request.

---
### FR10-AI-038 – Input Domain: Admin Status Mutation With Numeric Status Type ({'status': 123})
- **Formal Test ID:** `FR10-AI-038`
- **Folder:** `08 – Status Enum & Order-ID Input Domain`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Schema Validation / Type Mismatch Rejection
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": 123}`
- **Expected HTTP Status:** `400 Bad Request / 4xx Error`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `pending`.
- **Description & Objective:** Verify numeric status type is rejected with 400 Bad Request.

---
### FR10-AI-039 – Input Domain: Admin Status Mutation on Well-Formed Non-Existent Order ID (:id = 999999)
- **Formal Test ID:** `FR10-AI-039`
- **Folder:** `08 – Status Enum & Order-ID Input Domain`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Boundary Testing / Non-Existent Resource Identification
- **Actor:** Admin
- **State Before:** `N/A`
- **Target Route:** `PUT /api/admin/orders/999999/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `404 Not Found`
- **Expected State After:** `N/A`
- **Persistence Verification:** Authorized `N/A` query verifies order state is `N/A`.
- **Description & Objective:** Verify mutation on non-existent order ID returns 404 without side-effects.

---
### FR10-AI-040 – Input Domain: Admin Status Mutation on Malformed Non-Numeric Order ID (:id = 'not-an-id')
- **Formal Test ID:** `FR10-AI-040`
- **Folder:** `08 – Status Enum & Order-ID Input Domain`
- **Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED / INPUT ROBUSTNESS`
- **Technique:** Robustness Testing / Identifier Syntax Probe
- **Actor:** Admin
- **State Before:** `N/A`
- **Target Route:** `PUT /api/admin/orders/not-an-id/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED (e.g. 400/404)`
- **Expected State After:** `N/A`
- **Persistence Verification:** Authorized `N/A` query verifies order state is `N/A`.
- **Description & Objective:** Verify malformed non-numeric identifier is safely rejected without server crash (500) or unintended mutation.

---
### FR10-AI-041 – Persistence & Consistency: Read-After-Write State Verification and Response Schema Consistency
- **Formal Test ID:** `FR10-AI-041`
- **Folder:** `09 – Response Schema, Persistence & SEC-05`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Consistency Testing / Read-After-Write / Schema Conformance
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `200 OK (Consistent in PUT response and subsequent GET)`
- **Expected State After:** `confirmed`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `confirmed`.
- **Description & Objective:** Multi-request consistency case verifying response payload matches subsequent authorized GET query.

---
### FR10-AI-042 – SEC-05 Injection Defense: Black-Box SQL Injection Probe on Status Path Parameter
- **Formal Test ID:** `FR10-AI-042`
- **Folder:** `09 – Response Schema, Persistence & SEC-05`
- **Oracle Classification:** `SPECIFICATION-BACKED`
- **Technique:** Security / SQL Injection Robustness
- **Actor:** Admin
- **State Before:** `N/A`
- **Target Route:** `PUT /api/admin/orders/1' OR '1'='1/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `400 / 404 (Safely rejected, no SQL syntax leak, no 500 crash)`
- **Expected State After:** `N/A`
- **Persistence Verification:** Authorized `Admin` query verifies order state is `N/A`.
- **Description & Objective:** Verify SQL injection string in path parameter is safely rejected without syntax leakage or mass updates.

---
### FR10-HUM-001 – State Machine Continuity & Recovery: Legal Admin Confirmation Following Rejected Illegal Skip
- **Formal Test ID:** `FR10-HUM-001`
- **Folder:** `10 – Human-Designed Extension Cases`
- **Oracle Classification:** `SPECIFICATION-BACKED / STATE-MACHINE CONTINUITY`
- **Technique:** State Transition Testing / Error Recovery Sequence / Multi-Operation Continuity
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "shipping"}`
- **Expected HTTP Status:** `Step 1: Rejected (4xx); Step 3: 200 OK`
- **Expected State After:** `confirmed`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `confirmed`.
- **Description & Objective:** Multi-step recovery: attempt illegal pending->shipping (rejected), verify pending, then legal pending->confirmed (succeeds).

---
### FR10-HUM-002 – Multi-Entity State Isolation: Transitioning Order A Leaves Independent Order B Untouched
- **Formal Test ID:** `FR10-HUM-002`
- **Folder:** `10 – Human-Designed Extension Cases`
- **Oracle Classification:** `SPECIFICATION-BACKED / ENTITY-STATE ISOLATION`
- **Technique:** Multi-Entity Boundary Testing / Database Isolation / Side-Effect Absence
- **Actor:** Admin
- **State Before:** `Order A: pending, Order B: pending`
- **Target Route:** `PUT /api/admin/orders/{{orderAId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `200 OK on Order A; Order B remains pending`
- **Expected State After:** `Order A: confirmed, Order B: pending`
- **Persistence Verification:** Authorized `Admin` query verifies order state is `Order A: confirmed, Order B: pending`.
- **Description & Objective:** Mutates Order A to confirmed; queries both orders to prove Order A is confirmed and Order B is pending.

---
### FR10-HUM-003 – Downstream Fulfillment Continuity: Legitimate Admin Completion Following Barred Customer Cancellation
- **Formal Test ID:** `FR10-HUM-003`
- **Folder:** `10 – Human-Designed Extension Cases`
- **Oracle Classification:** `SPECIFICATION-BACKED / LIFECYCLE CONTINUITY`
- **Technique:** End-to-End Business Flow / Lifecycle Continuity / Negative Action Recovery
- **Actor:** User A (Cancel) / Admin (Deliver)
- **State Before:** `shipping`
- **Target Route:** `PUT /api/orders/{{orderId}}/cancel`
- **Request Body:** `{}`
- **Expected HTTP Status:** `Customer Cancel: Rejected (4xx); Admin Deliver: 200 OK`
- **Expected State After:** `delivered`
- **Persistence Verification:** Authorized `Admin / User A` query verifies order state is `delivered`.
- **Description & Objective:** Owner customer cancellation during shipping is rejected; subsequent Admin transition shipping->delivered succeeds.

---
### FR10-HUM-004 – Exploratory Same-State Self-Loop Probe: Admin Submits Redundant Mutation (confirmed -> confirmed)
- **Formal Test ID:** `FR10-HUM-004`
- **Folder:** `10 – Human-Designed Extension Cases`
- **Oracle Classification:** `EXPLORATORY / API CONTRACT`
- **Technique:** Exploratory Testing / FSM Self-Loop Analysis / API Idempotency
- **Actor:** Admin
- **State Before:** `confirmed`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `{"status": "confirmed"}`
- **Expected HTTP Status:** `OBSERVATIONAL (Accepts 200 OK idempotent success OR 4xx rejection; state remains confirmed)`
- **Expected State After:** `confirmed`
- **Persistence Verification:** Authorized `Admin` query verifies order state is `confirmed`.
- **Description & Objective:** Probes same-state self-loop update semantics; non-normative oracle; verifies state remains confirmed.

---
### FR10-HUM-005 – Exploratory Request Encoding Robustness: Admin Submits Mutation with Content-Type: text/plain
- **Formal Test ID:** `FR10-HUM-005`
- **Folder:** `10 – Human-Designed Extension Cases`
- **Oracle Classification:** `EXPLORATORY / API CONTRACT`
- **Technique:** Robustness Testing / Media Type Validation / Content Negotiation Boundary
- **Actor:** Admin
- **State Before:** `pending`
- **Target Route:** `PUT /api/admin/orders/{{orderId}}/status`
- **Request Body:** `"{\"status\":\"confirmed\"}"`
- **Expected HTTP Status:** `OBSERVATIONAL (Accepts 400/415 rejection, graceful parse 200, or safe error; non-normative oracle)`
- **Expected State After:** `pending`
- **Persistence Verification:** Authorized `Admin` query verifies order state is `pending`.
- **Description & Objective:** Probes non-JSON media type negotiation to detect unhandled 500 crashes; observational oracle.

---
## 4. Excluded Test Cases Log

### FR10-AI-012 (REJECTED – NOT MATERIALIZED)
- **Raw AI ID:** `FR10-AI-012`
- **Reason for Exclusion:** Confounded failure dimensions (normal customer role + invalid forward skip `pending -> shipping`). Violates single-variable isolation.
- **Disposition:** Retained in `FR10_AI_DRAFT.md` as raw audit evidence; strictly excluded from this 46-case executable suite.
