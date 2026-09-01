# FR-10 Requirement & State-Machine Analysis

**Feature ID:** FR-10 – Order Status & State Machine (Pool B)  
**Student Name:** Nguyễn Tấn Thắng  
**Student ID:** `23127259`  
**Authoritative Standards:** EShop SRS Section 4.10, api_specification.md, HW06 Assignment Requirements  
**Analysis Date:** September 1, 2026

---

## 1. Feature Scope

FR-10 governs the lifecycle, progression, validation, and authorization boundaries of customer orders within the EShop system. The order subsystem functions as a discrete finite state machine (FSM) transitioning across documented commercial milestones—from order placement through confirmation, dispatch, fulfillment, or cancellation.

Testing FR-10 requires verifying:
1. Strict sequential forward progression of order states.
2. Rigid enforcement of terminal/immutable states (`delivered`, `canceled`).
3. Role-Based Access Control (RBAC) separating customer self-service actions from administrative fulfillment actions.
4. Ownership boundaries preventing cross-tenant / IDOR status tampering.
5. Robust input validation and schema conformance on all state-mutating endpoints.

---

## 2. API Surface

The normative API surface participating in FR-10 state transitions and verification comprises:

| HTTP Method | Endpoint | Primary Role in FR-10 | Auth / Header Requirement | Documented Expected Roles |
|---|---|---|---|---|
| `PUT` | `/api/admin/orders/:id/status` (or `PUT /api/orders/:id/status`) | **Primary State Transition Endpoint:** Mutates the order status field to a new target state. | `Bearer <JWT>`, `X-Student-Id` | `admin` (for fulfillment transitions); `user` (for self-cancellation where routed) |
| `POST` | `/api/orders/:id/cancel` (or `PUT /api/orders/:id/cancel`) | **User Self-Cancellation Endpoint:** Dedicated customer endpoint to cancel eligible orders. | `Bearer <JWT>`, `X-Student-Id` | `user` (order owner) / `admin` |
| `GET` | `/api/orders/:id` | **Direct State Query & Verification Oracle:** Retrieves full order details including persisted status. | `Bearer <JWT>`, `X-Student-Id` | `user` (owner) / `admin` |
| `GET` | `/api/orders/my-orders` (or `GET /api/orders`) | **List Orders State Query:** Downstream query of user order list. | `Bearer <JWT>`, `X-Student-Id` | `user` |
| `POST` | `/api/orders` (or `/api/checkout`) | **Precondition Fixture Generator:** Places new orders in initial `pending` state. | `Bearer <JWT>`, `X-Student-Id` | `user` |

---

## 3. Actors and Authorization

FR-10 distinguishes five operational actor contexts:

1. **Unauthenticated Client (`ANON`):** Request without `Authorization` header or with invalid/tampered token. Must be rejected on all mutating endpoints (`HTTP 401 Unauthorized`) per `SEC-02`.
2. **Authenticated Order Owner (`USER-OWNER`):** Authenticated customer who placed the order. Permitted to view order and cancel orders in `pending` or `confirmed` status. Prohibited from executing fulfillment transitions (`confirmed`, `shipping`, `delivered`).
3. **Authenticated Non-Owner Customer (`USER-NON-OWNER`):** Authenticated customer who did NOT place the targeted order. Prohibited from viewing or modifying the order (IDOR / Horizontal Privilege boundary).
4. **Authenticated System Administrator (`ADMIN`):** Authenticated user possessing `role = 'admin'`. Authorized to advance fulfillment transitions (`pending -> confirmed -> shipping -> delivered`) and cancel un-shipped orders.
5. **Tampered/Forged Role Client (`ATTACKER-ROLE-FORGED`):** Token containing forged client-side claims (e.g. `role: admin` with invalid signature or modified payload). Must be rejected under `SEC-03`.

---

## 4. Authoritative State Set

According to EShop SRS Section 4.10 and `api_specification.md`, the authoritative set of order states consists of exactly five (5) string enum values:

```
[ pending ] ──(Admin)──> [ confirmed ] ──(Admin)──> [ shipping ] ──(Admin)──> [ delivered ] (Terminal)
     │                         │
  (User/Admin)              (User/Admin)
     │                         │
     v                         v
[ canceled ] (Terminal) <──────┘
```

1. **`pending` (Initial State):** Default state upon successful order creation / checkout. Awaiting merchant confirmation.
2. **`confirmed` (Intermediate State):** Merchant has reviewed and accepted the order. Ready for packaging/dispatch.
3. **`shipping` (Transit State):** Order has been dispatched to carrier and is currently in transit.
4. **`delivered` (Terminal State):** Customer has received goods. Fulfillment complete. State is permanently immutable.
5. **`canceled` (Terminal State):** Order voided/aborted by customer or merchant prior to dispatch. State is permanently immutable.

---

## 5. State Transition Matrix

The table below defines the formal specification-backed validity of every possible $(S_{current}, S_{target})$ combination:

| # | Current State ($S_{from}$) | Target State ($S_{to}$) | Permitted Actor | Allowed? | Oracle Classification | Normative Specification Rationale |
|---|---|---|---|:---:|---|---|
| **T01** | `pending` | `confirmed` | `admin` | **YES** | `SPECIFICATION-BACKED` | Merchant confirms new order for processing. |
| **T02** | `pending` | `canceled` | `user` (owner), `admin` | **YES** | `SPECIFICATION-BACKED` | Customer or merchant cancels order before confirmation. |
| **T03** | `pending` | `shipping` | None | **NO** | `SPECIFICATION-BACKED` | Illegal skip transition (`confirmed` skipped). |
| **T04** | `pending` | `delivered` | None | **NO** | `SPECIFICATION-BACKED` | Illegal skip transition (`confirmed`, `shipping` skipped). |
| **T05** | `pending` | `pending` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent transition. API may reject with 4xx or return 200 NOP. |
| **T06** | `confirmed` | `shipping` | `admin` | **YES** | `SPECIFICATION-BACKED` | Merchant dispatches confirmed package to carrier. |
| **T07** | `confirmed` | `canceled` | `user` (owner), `admin` | **YES** | `SPECIFICATION-BACKED` | Cancellation permitted while package has not yet shipped. |
| **T08** | `confirmed` | `pending` | None | **NO** | `SPECIFICATION-BACKED` | Illegal backward transition. |
| **T09** | `confirmed` | `delivered` | None | **NO** | `SPECIFICATION-BACKED` | Illegal skip transition (`shipping` skipped). |
| **T10** | `confirmed` | `confirmed` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent transition. |
| **T11** | `shipping` | `delivered` | `admin` | **YES** | `SPECIFICATION-BACKED` | Carrier/merchant confirms delivery completion. |
| **T12** | `shipping` | `canceled` | None (User explicitly blocked) | **NO** | `SPECIFICATION-BACKED` | SRS explicitly states user cannot cancel while shipping; admin cancellation is non-normative. |
| **T13** | `shipping` | `pending` | None | **NO** | `SPECIFICATION-BACKED` | Illegal backward transition. |
| **T14** | `shipping` | `confirmed` | None | **NO** | `SPECIFICATION-BACKED` | Illegal backward transition. |
| **T15** | `shipping` | `shipping` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent transition. |
| **T16** | `delivered` | `pending` | None | **NO** | `SPECIFICATION-BACKED` | Terminal state violation. |
| **T17** | `delivered` | `confirmed` | None | **NO** | `SPECIFICATION-BACKED` | Terminal state violation. |
| **T18** | `delivered` | `shipping` | None | **NO** | `SPECIFICATION-BACKED` | Terminal state violation. |
| **T19** | `delivered` | `canceled` | None | **NO** | `SPECIFICATION-BACKED` | Terminal state violation (cannot cancel delivered order). |
| **T20** | `delivered` | `delivered` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent on terminal state. |
| **T21** | `canceled` | `pending` | None | **NO** | `SPECIFICATION-BACKED` | Terminal state violation (cannot resurrect canceled order). |
| **T22** | `canceled` | `confirmed` | None | **NO** | `SPECIFICATION-BACKED` | Terminal state violation. |
| **T23** | `canceled` | `shipping` | None | **NO** | `SPECIFICATION-BACKED` | Terminal state violation. |
| **T24** | `canceled` | `delivered` | None | **NO** | `SPECIFICATION-BACKED` | Terminal state violation. |
| **T25** | `canceled` | `canceled` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent on terminal state. |

---

## 6. Invalid Transition Classes

Invalid state mutations are grouped into five rigorous testable classes:

1. **Class A: Forward Skip Transitions (`SKIP`):**
   - Attempting to skip required intermediate states (e.g. `pending -> shipping`, `pending -> delivered`, `confirmed -> delivered`).
   - Expected behavior: Rejection with `4xx Client Error` (`400 Bad Request` or `422 Unprocessable Entity`); persisted state must remain unchanged.
2. **Class B: Backward Regression Transitions (`REGRESS`):**
   - Attempting to regress order progress (e.g. `shipping -> confirmed`, `confirmed -> pending`, `delivered -> shipping`).
   - Expected behavior: Rejection with `4xx Client Error`; persisted state must remain unchanged.
3. **Class C: Post-Terminal Mutation Transitions (`TERMINAL_MUTATION`):**
   - Attempting any status change on an order already in `delivered` or `canceled`.
   - Expected behavior: Rejection with `4xx Client Error`; persisted state must remain permanently immutable.
4. **Class D: Unauthorized Role Transitions (`RBAC_VIOLATION`):**
   - Normal customer attempting admin-only fulfillment transitions (`pending -> confirmed`, `confirmed -> shipping`, `shipping -> delivered`).
   - Expected behavior: Rejection with `403 Forbidden` under `SEC-03`.
5. **Class E: Unauthorized In-Transit Cancellation (`SHIPPING_CANCEL_VIOLATION`):**
   - Customer attempting to cancel an order currently in `shipping` status.
   - Expected behavior: Rejection with `4xx Client Error` (`400 Bad Request` or `403 Forbidden`).

---

## 7. Status Input Partitions

Equivalence partitioning on the `status` payload field (`{ "status": <value> }`):

| Partition ID | Input Value / Type | Partition Category | Validity | Oracle Classification | Expected Semantic Handling |
|---|---|---|:---:|---|---|
| `EP-STAT-01` | `"confirmed"` | Valid forward enum | Valid | `SPECIFICATION-BACKED` | State advanced if valid actor and current state. |
| `EP-STAT-02` | `"shipping"` | Valid forward enum | Valid | `SPECIFICATION-BACKED` | State advanced if valid actor and current state. |
| `EP-STAT-03` | `"delivered"` | Valid forward enum | Valid | `SPECIFICATION-BACKED` | State advanced if valid actor and current state. |
| `EP-STAT-04` | `"canceled"` | Valid cancellation enum | Valid | `SPECIFICATION-BACKED` | Order canceled if in `pending` or `confirmed`. |
| `EP-STAT-05` | `"unknown_status"`, `"refunded"`, `"processing"` | Undocumented enum | Invalid | `SPECIFICATION-BACKED` | Rejection with `400 Bad Request` / `422`. |
| `EP-STAT-06` | `""` (Empty string) | Empty value | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with `400 Bad Request`. |
| `EP-STAT-07` | Missing `status` key `{}` | Missing required key | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with `400 Bad Request`. |
| `EP-STAT-08` | `null` | Null JSON value | Invalid | `EXPLORATORY / ENGINEERING` | Rejection without HTTP 500 server crash. |
| `EP-STAT-09` | `"   "` (Whitespace string) | Whitespace-only string | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with `400 Bad Request`. |
| `EP-STAT-10` | `"CONFIRMED"`, `"Pending"`, `"SHIPPING"` | Case variation | Invalid / Spec-Undefined | `SPEC-UNDEFINED` | Rejection or exact case matching required. |
| `EP-STAT-11` | `123`, `true` | Numeric / Boolean type | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with 4xx type mismatch. |
| `EP-STAT-12` | `{"nested": "confirmed"}` | Object type | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with 4xx type mismatch. |
| `EP-STAT-13` | `["confirmed"]` | Array type | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with 4xx type mismatch. |
| `EP-STAT-14` | String $> 1000\text{ chars}$ | Excessive length buffer | Invalid | `EXPLORATORY / ENGINEERING` | Rejection without buffer overflow / 500. |

---

## 8. Order ID Partitions

Equivalence partitioning on the `:id` path parameter (`/api/orders/:id/status`):

| Partition ID | Input Value / Format | Partition Category | Validity | Oracle Classification | Expected Semantic Handling |
|---|---|---|:---:|---|---|
| `EP-ID-01` | Valid existing order ID (e.g. `1`, `42`) | Valid numeric ID | Valid | `SPECIFICATION-BACKED` | Process status transition on targeted order. |
| `EP-ID-02` | Non-existent positive integer (e.g. `999999`) | Non-existent entity | Invalid | `SPECIFICATION-BACKED` | Rejection with `404 Not Found`. |
| `EP-ID-03` | `0` (Zero) | Non-positive boundary | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with `400 Bad Request` or `404 Not Found`. |
| `EP-ID-04` | `-1`, `-99` | Negative integer | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with `400 Bad Request` or `404 Not Found`. |
| `EP-ID-05` | `"abc"`, `"xyz"` | Non-numeric string | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with `400 Bad Request` or `404 Not Found`. |
| `EP-ID-06` | `1.5`, `3.14` | Decimal / Float string | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with `400 Bad Request` or `404 Not Found`. |
| `EP-ID-07` | `99999999999999999999` | BigInt / Integer overflow | Invalid | `EXPLORATORY / ENGINEERING` | Rejection without 500 server crash. |
| `EP-ID-08` | Special characters / SQL injection probe (`1' OR '1'='1`) | Malicious path string | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with `400 Bad Request` or `404 Not Found` under `SEC-05`. |

---

## 9. Authentication / Authorization Partitions

Evaluation of incoming request security context under `SEC-02` and `SEC-03`:

| Auth Partition ID | Token / Header State | Target Action | Expected Status | Security Standard |
|---|---|---|:---:|---|
| `EP-AUTH-01` | Missing `Authorization` header | Any state transition | `401 Unauthorized` | `SEC-02` (Mandatory JWT) |
| `EP-AUTH-02` | Malformed header (e.g. `Bearer`, `Basic xyz`) | Any state transition | `401 Unauthorized` | `SEC-02` (Malformed token) |
| `EP-AUTH-03` | Invalid signature / corrupted JWT string | Any state transition | `401 Unauthorized` | `SEC-02` (Signature mismatch) |
| `EP-AUTH-04` | Valid customer JWT (`role: 'user'`) | Admin transition (`confirmed`, `shipping`, `delivered`) | `403 Forbidden` | `SEC-03` (RBAC role check) |
| `EP-AUTH-05` | Valid customer JWT (`role: 'user'`) | Self-cancellation on own `pending` order | `200 OK` | `FR-10` / `SEC-02` |
| `EP-AUTH-06` | Valid admin JWT (`role: 'admin'`) | Admin fulfillment transitions | `200 OK` | `FR-10` / `SEC-03` |

---

## 10. Ownership Analysis (Cross-Tenant / IDOR)

The relationship between order ownership and customer access boundaries:

- **Customer Self-Service Boundary:** A normal authenticated user ($U_1$) is authorized to interact only with orders placed by $U_1$.
- **Horizontal Tampering (IDOR):** If user $U_1$ attempts to cancel or modify an order belonging to user $U_2$, the API must reject the operation.
- **Oracle Classification:** `SPECIFICATION-BACKED` (per SRS FR-10 and FR-11: customer views and modifies only own orders).
- **Expected Rejection Status:** `403 Forbidden` or `404 Not Found` (to avoid leaking order existence).
- **Admin Privilege:** Administrators operate globally across all customer orders and are exempt from single-user ownership restrictions.

---

## 11. Security Applicability Matrix

| Security Requirement | Applicability to FR-10 | Testing Approach | Verification Limit & Boundary |
|---|:---:|---|---|
| **SEC-01** (Passwords at Rest) | **N/A** | Not applicable to order status operations. | No password payloads are processed in FR-10. |
| **SEC-02** (Valid JWT on Sensitive APIs) | **DIRECTLY APPLICABLE (FULL)** | Submit requests with missing, malformed, invalid, and tampered JWTs to status endpoints. | Black-box API tests provide complete verification of 401 rejection behavior. |
| **SEC-03** (Admin Role Verification) | **DIRECTLY APPLICABLE (FULL)** | Submit customer tokens (`role: 'user'`) and forged tokens to admin fulfillment transitions. | Validates behavioral RBAC rejection (HTTP 403); internal code review verifies claims processing. |
| **SEC-04** (UI XSS Escaping) | **N/A** | UI-scoped rendering rule. | API reflects raw status strings in JSON; does not prove UI DOM safety. |
| **SEC-05** (Parameterized Queries) | **PARTIALLY APPLICABLE** | Submit SQL injection strings in `:id` path parameter and `status` JSON body. | Behavioral resilience (no SQL syntax leakage/crash) provides partial evidence; DB inspection confirms query parameterization. |
| **SEC-06** (Profile Role Tampering) | **N/A** | Scoped to profile management (FR-04). | Not applicable to order status transitions. |
| **SEC-07** (OTP Entropy & Expiry) | **N/A** | Scoped to password reset (FR-03). | Not applicable to order state transitions. |

---

## 12. Response / Schema Oracle

From `api_specification.md`, the documented contract for successful status mutations and error responses:

### 12.1 Successful Transition Response Contract
- **Expected HTTP Status:** `200 OK`
- **Content-Type:** `application/json`
- **Documented Top-Level Fields:**
  - `message`: String describing successful update (e.g. `"Order status updated successfully"`).
  - `order` (or updated order object):
    - `id`: Positive integer matching the requested `:id`.
    - `status`: String matching the newly updated target state enum.

### 12.2 Error Response Contract
- **Expected HTTP Status:** `400 Bad Request` (invalid input / illegal transition), `401 Unauthorized` (auth failure), `403 Forbidden` (RBAC violation), `404 Not Found` (non-existent order).
- **Documented Top-Level Fields:**
  - `message`: Descriptive error string without leaking internal stack traces, database schema details, or raw server internals.

---

## 13. Sequence Testing Dimensions

Because order lifecycle testing requires stateful multi-request sequences, test design must enforce structured chaining:

1. **Happy-Path Fulfillment Lifecycle Sequence:**
   $$\text{POST /api/orders (pending)} \xrightarrow{\text{Admin}} \text{confirmed} \xrightarrow{\text{Admin}} \text{shipping} \xrightarrow{\text{Admin}} \text{delivered (Terminal)}$$
2. **Early Cancellation Sequence (from Pending):**
   $$\text{POST /api/orders (pending)} \xrightarrow{\text{User/Admin}} \text{canceled (Terminal)} \xrightarrow{\text{Admin Attempt}} \text{Rejection (4xx)}$$
3. **Mid-Stream Cancellation Sequence (from Confirmed):**
   $$\text{POST /api/orders (pending)} \xrightarrow{\text{Admin}} \text{confirmed} \xrightarrow{\text{User/Admin}} \text{canceled (Terminal)} \xrightarrow{\text{Admin Attempt}} \text{Rejection (4xx)}$$
4. **Disallowed In-Transit Cancellation Sequence:**
   $$\text{POST /api/orders (pending)} \xrightarrow{\text{Admin}} \text{confirmed} \xrightarrow{\text{Admin}} \text{shipping} \xrightarrow{\text{User Cancel Attempt}} \text{Rejection (4xx)} \rightarrow \text{State Remains shipping}$$
5. **Post-Delivered Immutability Sequence:**
   $$\text{Fulfill to delivered} \xrightarrow{\text{Attempt cancel / regress}} \text{Rejection (4xx)} \rightarrow \text{State Remains delivered}$$

---

## 14. State Isolation / Fixture Requirements

To ensure 100% deterministic test execution and prevent state contamination across test cases:
1. **Dynamic Setup Helpers:** Test runs must dynamically create fresh order fixtures (`POST /api/orders`) for each autonomous test case or sequence.
2. **Independent Order IDs:** Every test case operates on its own dedicated `orderId` variable; no test case mutates an order used by another test case.
3. **Distinct Test Accounts:** Separate dynamic customer credentials (`userOwner`, `userNonOwner`) and admin credentials (`adminUser`) provisioned per run.

---

## 15. Persistence Verification Strategy

To satisfy the HW06 requirement for authoritative state verification:
- **Two-Tier Oracle Model:**
  1. **Tier 1 (Response Body Oracle):** Assert that the mutating endpoint returns HTTP 200 and indicates the new status in the JSON response payload.
  2. **Tier 2 (Persistence State Oracle):** Follow every mutating request with an independent `GET /api/orders/:id` query to verify that the status has been persisted in the underlying database and is externally observable.
- For negative test cases (rejected transitions), the Tier 2 query must confirm that the order status remains strictly unchanged at its prior valid state.

---

## 16. Specification Gaps / Ambiguities (`SPEC-UNDEFINED`)

The following behavioral aspects are not explicitly defined in `api_specification.md` and are classified as `SPEC-UNDEFINED` (exploratory / robustness targets):

1. **Idempotent Status Updates:** Whether sending `PUT /api/orders/:id/status` with `status: "confirmed"` when the order is already `confirmed` returns HTTP 200 (NOP) or HTTP 400 (Invalid transition).
2. **Admin Cancellation While In-Transit:** Whether an administrator is permitted to cancel an order in `shipping` status (e.g. for lost parcel workflows) or if cancellation is globally barred once shipped.
3. **Exact Error Response Schema:** Specific sub-error codes, localized strings, or error array wrappers are not standardized in `api_specification.md`.
4. **Case Sensitivity Handling:** Whether status strings are strictly lower-case or case-insensitive.

---

## 17. Risk Hypotheses

High-priority risk failure modes to probe during test generation and execution:

- **RISK-FR10-01 (State Skipping):** Backend allows direct transition from `pending` to `delivered` or `shipping` without required intermediate confirmation.
- **RISK-FR10-02 (Backward State Regression):** Backend allows orders to move backward from `delivered` or `shipping` back to `pending`.
- **RISK-FR10-03 (Terminal State Mutability):** Backend permits status mutations on orders already marked `canceled` or `delivered`.
- **RISK-FR10-04 (RBAC Bypass / Privilege Escalation):** Normal customer tokens can successfully trigger admin fulfillment transitions (`confirmed`, `shipping`, `delivered`).
- **RISK-FR10-05 (Horizontal Privilege Escalation / IDOR):** Customer can cancel or view orders belonging to another user.
- **RISK-FR10-06 (In-Transit Cancellation Bypass):** Customer can cancel an order that has already transitioned to `shipping`.
- **RISK-FR10-07 (State / Response Desynchronization):** API returns HTTP 200 claiming status updated, but subsequent `GET /api/orders/:id` reveals persisted state did not change.

---

## 18. Target Distribution for AI Test Generation (Phase 2A.2)

To ensure comprehensive coverage and allow for rigorous Human Audit filtering while comfortably exceeding the assignment target ($\ge 35$ usable AI-derived cases), Phase 2A.2 will target **38 raw AI-generated test cases** across the following categories:

| Category # | Category Description | Target Case Count | Target Test Case ID Range |
|:---:|---|:---:|---|
| **Cat 1** | **Valid Forward State Transitions (Admin Lifecycle)** | 4 | `FR10-AI-001` – `FR10-AI-004` |
| **Cat 2** | **Valid Cancellation Transitions (Customer & Admin)** | 4 | `FR10-AI-005` – `FR10-AI-008` |
| **Cat 3** | **Invalid Forward Skip Transitions** | 4 | `FR10-AI-009` – `FR10-AI-012` |
| **Cat 4** | **Invalid Backward State Regressions** | 5 | `FR10-AI-013` – `FR10-AI-017` |
| **Cat 5** | **Terminal State Immutability Probes (`delivered`, `canceled`)** | 5 | `FR10-AI-018` – `FR10-AI-022` |
| **Cat 6** | **Authentication & JWT Validation (`SEC-02`)** | 4 | `FR10-AI-023` – `FR10-AI-026` |
| **Cat 7** | **RBAC & Privilege Escalation Probes (`SEC-03`)** | 4 | `FR10-AI-027` – `FR10-AI-030` |
| **Cat 8** | **Status Payload Input Domain & Boundaries** | 4 | `FR10-AI-031` – `FR10-AI-034` |
| **Cat 9** | **Order ID Path Parameter Partitions & Boundaries** | 4 | `FR10-AI-035` – `FR10-AI-038` |
| **Total** | **Raw AI Generation Target** | **38** | `FR10-AI-001` – `FR10-AI-038` |
