# FR-10 Human Audit Correction Manifest & Executable Derivatives

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Raw AI Draft Status:** Frozen & Immutable (`23127259/testcases/FR10_AI_DRAFT.md`)
- **Total Raw Cases:** `42`
- **Usable AI-Derived Cases:** `41` (38 Valid As-Is + 3 Corrected Derivatives)
- **Rejected Raw Cases:** `1` (`FR10-AI-012`)

---

## 1. Overview & Purpose

This manifest documents the authoritative **Human Audit Corrections** for the AI-generated FR-10 test suite. In compliance with HW06 integrity standards:
1. `FR10_AI_DRAFT.md` is strictly **immutable** and preserves the raw AI generation history.
2. Corrected executable interpretations are documented here and will govern the creation of the final Postman collection and Newman test harness.
3. Cases flagged as `INCOMPLETE` during Human Audit are refined with disciplined oracles, while invalid/confounded cases (`FR10-AI-012`) are formally excluded from the final execution suite.

---

## 2. Corrected Executable Derivatives

### FR10-AI-033 – Cross-User Ownership Cancellation on Pending Order
- **Raw AI ID:** `FR10-AI-033`
- **Human Verdict:** `INCOMPLETE`
- **Original AI Risk:** The raw case assumed that cross-user cancellation restrictions are an explicit, normative FR-10 requirement and asserted a strict conventional HTTP 403 status code. In the authoritative EShop SRS, the feature is phrased as *"When an order is pending, User can cancel it"*, which implies customer self-service ownership rather than providing an explicit multi-tenant access-control matrix.
- **Corrected Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION`
- **Corrected Execution Invariants:**
  - **Caller:** Authenticated Customer B with valid token (`userBToken`, `role = 'user'`).
  - **Target:** Order created and owned by Customer A (`orderAId`) in legitimate cancellable `pending` state.
  - **Request:** `PUT /api/orders/{{orderAId}}/cancel`.
  - **Isolated Dimension:** Mismatched resource ownership (Caller ID $\neq$ Resource Owner ID).
- **Corrected Expected Semantic Result:** The cancellation request must be rejected. Customer B must not have authority to cancel Customer A's order. The order state for Customer A's order must remain `pending`.
- **Corrected HTTP-Status Discipline:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED`. Any standard client error (e.g. `403 Forbidden`, `404 Not Found`, or generic 4xx error) is accepted as compliant behavioral enforcement. No specific status code is mandated.
- **Corrected Persistence Oracle:** After the mutation request, an authorized query (`GET /api/orders/{{orderAId}}` using Customer A's token or Admin token) must prove that the order state remains `pending`. (Do not use unauthorized Customer B's read query as persistence proof).
- **Bug-Reporting Limitation:** If the SUT allows Customer B to cancel Customer A's order, this must be reported as a potential business authorization / ownership anomaly requiring requirement confirmation, rather than claiming violation of an explicit named FR-10 requirement clause.
- **Executable in Final Suite:** **YES**

---

### FR10-AI-034 – Cross-User Ownership Cancellation on Confirmed Order
- **Raw AI ID:** `FR10-AI-034`
- **Human Verdict:** `INCOMPLETE`
- **Original AI Risk:** Same specification-strength limitation as AI-033, exercised on the `confirmed` lifecycle state. Raw draft asserted strict conventional 403.
- **Corrected Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION`
- **Corrected Execution Invariants:**
  - **Caller:** Authenticated Customer B (`userBToken`, `role = 'user'`).
  - **Target:** Order created and owned by Customer A (`orderAId`) in legitimate cancellable `confirmed` state.
  - **Request:** `PUT /api/orders/{{orderAId}}/cancel`.
  - **Isolated Dimension:** Mismatched resource ownership on pre-shipment confirmed order.
- **Corrected Expected Semantic Result:** The mutation request must be rejected. Customer B must not cancel Customer A's confirmed order. Order state must remain `confirmed`.
- **Corrected HTTP-Status Discipline:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED` (Any 4xx error code accepted).
- **Corrected Persistence Oracle:** Authorized query by Customer A or Admin confirms order state is unchanged at `confirmed`.
- **Bug-Reporting Limitation:** Report unexpected mutation conservatively as an ownership / authorization finding.
- **Executable in Final Suite:** **YES**

---

### FR10-AI-040 – Malformed Non-Numeric Order ID Path Parameter
- **Raw AI ID:** `FR10-AI-040`
- **Human Verdict:** `INCOMPLETE`
- **Original AI Risk:** The raw draft asserted that `:id` path parameter has a strict numeric format constraint and expected an exact HTTP 400 Bad Request. However, the authoritative API contract (`api_specification.md`) defines the route shape as `/api/admin/orders/:id/status` without establishing an explicit regex or schema type constraint for the path parameter. Inferring numeric format solely because the underlying relational database uses integer primary keys would turn an implementation detail into the oracle.
- **Corrected Oracle Classification:** `PARTIALLY SPECIFICATION-BACKED / INPUT ROBUSTNESS`
- **Corrected Execution Invariants:**
  - **Caller:** System Administrator (`role = 'admin'`, valid `adminToken`).
  - **Target Route:** `PUT /api/admin/orders/not-an-id/status`.
  - **Payload:** `{"status": "confirmed"}`.
  - **Isolated Dimension:** Malformed string identifier probe in path parameter.
- **Corrected Expected Semantic Result:** The request must be safely rejected without crashing the SUT (no unhandled 500 error) and must not cause unintended lookup or mutation of any existing order in the database.
- **Corrected HTTP-Status Discipline:** `ERROR / NON-SUCCESS – EXACT CODE NOT SPECIFIED`. Standard non-success responses (e.g. `400 Bad Request`, `404 Not Found`, or other 4xx errors) are acceptable runtime handling.
- **Corrected Persistence Oracle:** Baseline database orders are queried before and after to verify zero accidental side-effects.
- **Bug-Reporting Limitation:** If the SUT responds with 404 instead of 400, this is compliant robustness handling and must not be filed as a specification bug.
- **Executable in Final Suite:** **YES**

---

## 3. Rejected Raw Cases Excluded from Executable Suite

### FR10-AI-012 – Unauthorized Customer Forward Skip (`pending` $\rightarrow$ `shipping`)
- **Raw AI ID:** `FR10-AI-012`
- **Human Verdict:** `INVALID`
- **Disposition:** **REJECTED – DO NOT MATERIALIZE INTO FINAL EXECUTABLE SUITE**
- **Reason for Rejection:**
  1. **Confounded Failure Dimensions:** The request combines two independent invalid dimensions:
     - Actor role is normal customer (`role = 'user'`) targeting an Admin-only route (`/api/admin/orders/:id/status`).
     - Requested transition is an illegal multi-state forward skip (`pending` $\rightarrow$ `shipping`), bypassing `confirmed`.
  2. **Ambiguous Causality:** When the SUT rejects the request, a black-box test cannot determine whether failure was caused by RBAC enforcement (`SEC-03`) or state machine transition validation (`FR-10 FSM`).
  3. **Redundancy Upon Isolation:**
     - If corrected to use an Admin token, it becomes an exact duplicate of `FR10-AI-009`.
     - If corrected to use a legal transition edge, it overlaps `FR10-AI-030`.
  4. **Audit Disposition:** Preserved in `FR10_AI_DRAFT.md` as historical raw generation evidence, but omitted from the final 41-case executable test suite.
- **Executable in Final Suite:** **NO**

---

## 4. Final Suite Accounting Summary

| Category | Count | IDs |
|---|:---:|---|
| **Raw AI Generated** | `42` | `FR10-AI-001` .. `FR10-AI-042` |
| **Valid As-Is** | `38` | `FR10-AI-001`..`011`, `FR10-AI-013`..`032`, `FR10-AI-035`..`039`, `FR10-AI-041`..`042` |
| **Corrected Derivatives** | `3` | `FR10-AI-033`, `FR10-AI-034`, `FR10-AI-040` |
| **Rejected from Suite** | `1` | `FR10-AI-012` |
| **Total Usable Executable AI Cases** | **`41`** | Satisfies assignment requirement ($\ge 35$) |
