# FR-10 Requirement & State-Machine Analysis

**Feature ID:** FR-10 – Order Status & State Machine (Pool B)  
**Student Name:** Nguyễn Tấn Thắng  
**Student ID:** `23127259`  
**Authoritative Standards:** EShop SRS Section 4.10, api_specification.md, HW06 Assignment Requirements  
**Analysis Date:** September 1, 2026 (Updated & Corrected in Phase 2A.2)

---

## 0. Human Review Corrections Before Generation

> [!NOTE]
> **Audit & Oracle Alignment Notice (Phase 2A.2 Gate):**  
> Following human review of the initial Phase 2A.1 analysis, the following normative corrections were applied before initiating test case generation:
> 1. **Exact Endpoint Disambiguation:** Removed ambiguous "OR" path alternatives. Locked primary admin status mutation to `PUT /api/admin/orders/:id/status` and customer self-cancellation to `PUT /api/orders/:id/cancel`. Clarified that `POST /api/orders` serves strictly as a test setup helper (FR-08 dependency), not the formal FR-10 API surface under test.
> 2. **Actor-Specific In-Transit Cancellation Semantics:** Disentangled `shipping -> canceled` into two separate cases: (a) User cancellation is explicitly barred by SRS (`Allowed = NO`, `SPECIFICATION-BACKED`); (b) Admin emergency cancellation in-transit is unmentioned in SRS/API-SPEC (`Allowed = SPEC-UNDEFINED`, `SPEC-UNDEFINED`).
> 3. **HTTP Status Code Discipline:** Removed assumptions of exact `401 Unauthorized` or `403 Forbidden` unless explicitly normative in `api_specification.md`. Used `Expected Semantic Result` with `Expected HTTP Status: NOT SPECIFIED – ERROR / NON-SUCCESS` (or `4xx Client Error`).
> 4. **Dedicated Ownership & Cross-Tenant Boundary Model:** Distinctly analyzed customer self-cancellation vs. cross-user cancellation (`PARTIAL / SPEC-UNDEFINED`) and own-order reading vs. cross-user order reading (`SPECIFICATION-BACKED / ADDITIONAL-SEC` per SRS FR-11).
> 5. **Two-Tier Persistence Oracle Enforcement:** Mandated that state transitions be verified not merely by the immediate PUT response body, but primarily through a follow-up query (`GET /api/orders/:id`).
> 6. **Multi-Interaction Raw Generation Target:** Expanded the generation plan to 40–42 raw AI cases across multiple staged interactions to ensure $>35$ usable cases after Human Audit filtering.

---

## 1. Feature Scope

FR-10 governs the lifecycle, state progression, authorization boundaries, and cancellation rules of customer orders in the EShop system. The order subsystem implements a discrete finite state machine (FSM) transitioning across documented commercial stages—from placement to merchant review, carrier transit, final fulfillment, or early cancellation.

Testing FR-10 requires verifying:
1. Strict sequential forward progression of order states without illegal state skipping.
2. Permanent immutability of terminal states (`delivered`, `canceled`).
3. Rigid Role-Based Access Control (RBAC) separating customer self-service actions from administrative fulfillment actions.
4. Ownership boundaries preventing cross-tenant / IDOR status tampering.
5. Robust input validation and schema conformance on all state-mutating endpoints.

---

## 2. API Surface & Exact Endpoints

The exact normative API surface participating in FR-10 state transitions and verification comprises:

| HTTP Method | Exact Endpoint Path | Participating Role in FR-10 | Mandatory Headers & Auth | Request Body Schema |
|---|---|---|---|---|
| `PUT` | `/api/admin/orders/:id/status` | **Primary Admin State Mutation API:** Advances order status along the fulfillment lifecycle (`confirmed`, `shipping`, `delivered`, `canceled`). | `Authorization: Bearer <token>`, `X-Student-Id` (Role: `admin`) | `{ "status": "<target_status>" }` |
| `PUT` | `/api/orders/:id/cancel` | **User Self-Cancellation API:** Allows customer to cancel their own un-shipped order. | `Authorization: Bearer <token>`, `X-Student-Id` (Role: `user`) | Empty body `{}` (or optional `{ "reason": "..." }`) |
| `GET` | `/api/orders/:id` | **Direct State Query & Verification Oracle:** Primary Tier 2 external persistence oracle. | `Authorization: Bearer <token>`, `X-Student-Id` | None |
| `GET` | `/api/orders/my-orders` | **List Orders State Query:** Supplemental verification of customer order list. | `Authorization: Bearer <token>`, `X-Student-Id` | None |
| `POST` | `/api/orders` (or `/api/checkout`) | **[HELPER / FR-08 DEPENDENCY]:** Fixture generator creating fresh test orders in initial `pending` state. | `Authorization: Bearer <token>`, `X-Student-Id` | Cart / Checkout payload |

---

## 3. Actors and Authorization Model

FR-10 distinguishes five operational actor contexts:

1. **Unauthenticated Client (`ANON`):** Request lacking `Authorization` header or presenting an invalid/tampered token. Expected Semantic Result: rejected; authentication required (`SEC-02`).
2. **Authenticated Order Owner (`USER-OWNER`):** Authenticated customer who placed the targeted order. Authorized for self-cancellation on un-shipped orders (`pending`, `confirmed`) via `PUT /api/orders/:id/cancel`. Unauthorized for fulfillment mutations via `PUT /api/admin/orders/:id/status`.
3. **Authenticated Non-Owner Customer (`USER-NON-OWNER`):** Authenticated customer who did NOT place the targeted order. Unauthorized to view or cancel the order (Horizontal Privilege / IDOR boundary).
4. **Authenticated System Administrator (`ADMIN`):** Authenticated user possessing verified `role = 'admin'`. Authorized to advance fulfillment transitions and perform administrative cancellations.
5. **Tampered / Client-Forged Role Client (`ATTACKER-FORGED`):** Token containing forged client claims without valid server signature. Expected Semantic Result: rejected under `SEC-03`.

---

## 4. Authoritative Order State Set

According to EShop SRS Section 4.10 and `api_specification.md`, the authoritative order state set comprises exactly five (5) discrete string enum values:

```
[ pending ] ──(Admin)──> [ confirmed ] ──(Admin)──> [ shipping ] ──(Admin)──> [ delivered ] (Terminal)
     │                         │
  (User/Admin)              (User/Admin)
     │                         │
     v                         v
[ canceled ] (Terminal) <──────┘
```

1. **`pending` (Initial State):** Default state immediately following order placement / checkout. Awaiting merchant confirmation.
2. **`confirmed` (Intermediate State):** Merchant has reviewed and accepted the order for processing.
3. **`shipping` (In-Transit State):** Order has been dispatched to carrier and is currently in transit.
4. **`delivered` (Terminal State):** Customer has received goods. Fulfillment is completed. State is permanently immutable.
5. **`canceled` (Terminal State):** Order has been voided/aborted prior to dispatch. State is permanently immutable.

---

## 5. Frozen State Transition Matrix

The table below defines the authoritative specification-backed validity of every possible $(S_{current}, S_{target})$ combination:

| # | Current State ($S_{from}$) | Target State ($S_{to}$) | Actor / Route | Allowed? | Oracle Classification | Normative Basis & Rationale |
|---|---|---|---|:---:|---|---|
| **T01** | `pending` | `confirmed` | `admin` via `PUT /api/admin/orders/:id/status` | **YES** | `SPECIFICATION-BACKED` | SRS FR-10: Merchant confirms new order. |
| **T02** | `pending` | `canceled` | `user` (owner) via `PUT /api/orders/:id/cancel` | **YES** | `SPECIFICATION-BACKED` | SRS FR-10: Customer cancels pending order. |
| **T03** | `pending` | `canceled` | `admin` via `PUT /api/admin/orders/:id/status` | **YES** | `SPECIFICATION-BACKED` | SRS FR-10: Merchant cancels pending order. |
| **T04** | `pending` | `shipping` | Any | **NO** | `SPECIFICATION-BACKED` | Illegal skip transition (`confirmed` skipped). |
| **T05** | `pending` | `delivered` | Any | **NO** | `SPECIFICATION-BACKED` | Illegal skip transition (`confirmed`, `shipping` skipped). |
| **T06** | `pending` | `pending` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent transition. |
| **T07** | `confirmed` | `shipping` | `admin` via `PUT /api/admin/orders/:id/status` | **YES** | `SPECIFICATION-BACKED` | SRS FR-10: Merchant dispatches package. |
| **T08** | `confirmed` | `canceled` | `user` (owner) via `PUT /api/orders/:id/cancel` | **YES** | `SPECIFICATION-BACKED` | SRS Section 4.10: Customer cancels before shipping. |
| **T09** | `confirmed` | `canceled` | `admin` via `PUT /api/admin/orders/:id/status` | **YES** | `SPECIFICATION-BACKED` | SRS Section 4.10: Merchant cancels before shipping. |
| **T10** | `confirmed` | `pending` | Any | **NO** | `SPECIFICATION-BACKED` | Illegal backward regression. |
| **T11** | `confirmed` | `delivered` | Any | **NO** | `SPECIFICATION-BACKED` | Illegal skip transition (`shipping` skipped). |
| **T12** | `confirmed` | `confirmed` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent transition. |
| **T13** | `shipping` | `delivered` | `admin` via `PUT /api/admin/orders/:id/status` | **YES** | `SPECIFICATION-BACKED` | SRS FR-10: Carrier/merchant completes delivery. |
| **T14** | `shipping` | `canceled` | `user` (owner) via `PUT /api/orders/:id/cancel` | **NO** | `SPECIFICATION-BACKED` | SRS Section 4.10 explicitly bars user cancel while shipping. |
| **T15** | `shipping` | `canceled` | `admin` via `PUT /api/admin/orders/:id/status` | **SPEC-UNDEFINED** | `SPEC-UNDEFINED` | Emergency in-transit admin cancel is unmentioned in SRS. |
| **T16** | `shipping` | `pending` | Any | **NO** | `SPECIFICATION-BACKED` | Illegal backward regression. |
| **T17** | `shipping` | `confirmed` | Any | **NO** | `SPECIFICATION-BACKED` | Illegal backward regression. |
| **T18** | `shipping` | `shipping` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent transition. |
| **T19** | `delivered` | Any other state | Any | **NO** | `SPECIFICATION-BACKED` | Terminal state immutability violation. |
| **T20** | `delivered` | `delivered` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent on terminal state. |
| **T21** | `canceled` | Any other state | Any | **NO** | `SPECIFICATION-BACKED` | Terminal state immutability violation. |
| **T22** | `canceled` | `canceled` | Any | **NO / NOP** | `SPEC-UNDEFINED` | Idempotent on terminal state. |

---

## 6. Invalid Transition Classes

Invalid state mutation attempts are categorized into five testable classes:

1. **Class A: Forward Skip Transitions (`SKIP`):**
   - Direct jumping across lifecycle stages (e.g. `pending -> shipping`, `pending -> delivered`, `confirmed -> delivered`).
   - Expected Semantic Result: Transition rejected; order status remains strictly unchanged.
2. **Class B: Backward Regression Transitions (`REGRESS`):**
   - Attempting to regress order progress (e.g. `shipping -> confirmed`, `confirmed -> pending`, `delivered -> shipping`).
   - Expected Semantic Result: Transition rejected; order status remains strictly unchanged.
3. **Class C: Post-Terminal Mutation Transitions (`TERMINAL_MUTATION`):**
   - Any status mutation attempt on an order already in `delivered` or `canceled`.
   - Expected Semantic Result: Transition rejected; terminal state remains permanently immutable.
4. **Class D: Unauthorized Role Transitions (`RBAC_VIOLATION`):**
   - Normal customer token attempting admin-only fulfillment transitions via `PUT /api/admin/orders/:id/status`.
   - Expected Semantic Result: Request rejected (`SEC-03`); order status unchanged.
5. **Class E: Unauthorized In-Transit Cancellation (`SHIPPING_CANCEL_VIOLATION`):**
   - Customer attempting to cancel an order currently in `shipping` status.
   - Expected Semantic Result: Request rejected (SRS Section 4.10); order status remains `shipping`.

---

## 7. Status Input Partitions

Equivalence partitioning on the `status` payload field (`{ "status": <value> }`):

| Partition ID | Input Value / Type | Partition Category | Validity | Oracle Classification | Expected Semantic Handling |
|---|---|---|:---:|---|---|
| `EP-STAT-01` | `"confirmed"` | Valid forward enum | Valid | `SPECIFICATION-BACKED` | State advanced if valid actor and current state. |
| `EP-STAT-02` | `"shipping"` | Valid forward enum | Valid | `SPECIFICATION-BACKED` | State advanced if valid actor and current state. |
| `EP-STAT-03` | `"delivered"` | Valid forward enum | Valid | `SPECIFICATION-BACKED` | State advanced if valid actor and current state. |
| `EP-STAT-04` | `"canceled"` | Valid cancellation enum | Valid | `SPECIFICATION-BACKED` | Order canceled if in `pending` or `confirmed`. |
| `EP-STAT-05` | `"unknown_status"`, `"refunded"`, `"processing"` | Undocumented enum | Invalid | `SPECIFICATION-BACKED` | Rejection with 4xx client error; status unchanged. |
| `EP-STAT-06` | `""` (Empty string) | Empty value | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with 4xx client error. |
| `EP-STAT-07` | Missing `status` key `{}` | Missing required key | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with 4xx client error. |
| `EP-STAT-08` | `null` | Null JSON value | Invalid | `EXPLORATORY / ENGINEERING` | Rejection without 500 server crash. |
| `EP-STAT-09` | `"   "` (Whitespace string) | Whitespace string | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with 4xx client error. |
| `EP-STAT-10` | `"CONFIRMED"`, `"Pending"`, `"SHIPPING"` | Case variation | Invalid / Spec-Undefined | `SPEC-UNDEFINED` | Rejection or exact lower-case match required. |
| `EP-STAT-11` | `123`, `true` | Numeric / Boolean type | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with 4xx type mismatch. |
| `EP-STAT-12` | `{"nested": "confirmed"}` | Object type | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with 4xx type mismatch. |
| `EP-STAT-13` | `["confirmed"]` | Array type | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with 4xx type mismatch. |
| `EP-STAT-14` | String $> 1000\text{ chars}$ | Excessive length buffer | Invalid | `EXPLORATORY / ENGINEERING` | Rejection without buffer overflow / 500 crash. |

---

## 8. Order ID Partitions

Equivalence partitioning on the `:id` path parameter (`/api/admin/orders/:id/status` and `/api/orders/:id/cancel`):

| Partition ID | Input Value / Format | Partition Category | Validity | Oracle Classification | Expected Semantic Handling |
|---|---|---|:---:|---|---|
| `EP-ID-01` | Valid existing order ID (e.g. `1`, `42`) | Valid numeric ID | Valid | `SPECIFICATION-BACKED` | Process transition on targeted order. |
| `EP-ID-02` | Non-existent positive integer (e.g. `999999`) | Non-existent entity | Invalid | `SPECIFICATION-BACKED` | Rejection with 4xx (e.g. 404 Not Found). |
| `EP-ID-03` | `0` (Zero) | Non-positive boundary | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with 4xx client error. |
| `EP-ID-04` | `-1`, `-99` | Negative integer | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with 4xx client error. |
| `EP-ID-05` | `"abc"`, `"xyz"` | Non-numeric string | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with 4xx client error. |
| `EP-ID-06` | `1.5`, `3.14` | Decimal / Float string | Invalid | `EXPLORATORY / ENGINEERING` | Rejection with 4xx client error. |
| `EP-ID-07` | `99999999999999999999` | Integer overflow | Invalid | `EXPLORATORY / ENGINEERING` | Rejection without 500 server crash. |
| `EP-ID-08` | SQL injection probe (`1' OR '1'='1`) | Malicious path string | Invalid | `PARTIALLY SPEC-BACKED` | Rejection with 4xx under `SEC-05`. |

---

## 9. Authentication & Authorization Partitions

Evaluation of request authentication context under `SEC-02` and `SEC-03`:

| Auth Partition ID | Token / Header State | Target Endpoint & Action | Expected Semantic Result | Expected HTTP Status | Security Standard |
|---|---|---|---|---|---|
| `EP-AUTH-01` | Missing `Authorization` header | Status mutation / Cancel | Rejected: Authentication required | `NOT SPECIFIED – ERROR / 4xx` | `SEC-02` (Mandatory JWT) |
| `EP-AUTH-02` | Malformed header (`Bearer`, `Basic xyz`) | Status mutation / Cancel | Rejected: Malformed token | `NOT SPECIFIED – ERROR / 4xx` | `SEC-02` (Malformed token) |
| `EP-AUTH-03` | Tampered signature / corrupted JWT | Status mutation / Cancel | Rejected: Invalid token | `NOT SPECIFIED – ERROR / 4xx` | `SEC-02` (Invalid signature) |
| `EP-AUTH-04` | Customer token (`role = 'user'`) | `PUT /api/admin/orders/:id/status` | Rejected: Insufficient privileges | `NOT SPECIFIED – ERROR / 4xx` | `SEC-03` (RBAC role check) |
| `EP-AUTH-05` | Customer token (`role = 'user'`) | `PUT /api/orders/:id/cancel` (own order) | Processed: Order canceled | `200 OK` (if documented) | `FR-10` / `SEC-02` |
| `EP-AUTH-06` | Admin token (`role = 'admin'`) | `PUT /api/admin/orders/:id/status` | Processed: Status updated | `200 OK` (if documented) | `FR-10` / `SEC-03` |

---

## 10. Dedicated Ownership & Cross-Tenant Access Model

The relationship between order ownership, privacy, and status mutations:

1. **Customer Self-Service Boundary (Own Order Cancellation):**
   - User $U_1$ cancelling $U_1$'s own `pending` or `confirmed` order via `PUT /api/orders/:id/cancel`.
   - Classification: `SPECIFICATION-BACKED` (SRS Section 4.10).
   - Expected Result: Order status successfully transitions to `canceled`.
2. **Horizontal Privilege Escalation (Cross-User Cancellation):**
   - User $U_1$ attempting to cancel an order belonging to user $U_2$ via `PUT /api/orders/:id/cancel`.
   - Classification: `PARTIAL / SPEC-UNDEFINED` (Business authorization boundary; SRS FR-10 does not explicitly specify status code for cross-user mutation).
   - Expected Semantic Result: Request rejected; $U_2$'s order remains unchanged.
3. **Customer Order Viewing (Own Order Query):**
   - User $U_1$ reading $U_1$'s own order via `GET /api/orders/:id`.
   - Classification: `SPECIFICATION-BACKED` (SRS FR-11).
   - Expected Result: Returns order details for $U_1$.
4. **Cross-User Order Reading (IDOR Privacy Violation):**
   - User $U_1$ attempting to read an order belonging to user $U_2$ via `GET /api/orders/:id`.
   - Classification: `SPECIFICATION-BACKED / ADDITIONAL-SEC` (SRS FR-11 explicitly mandates: *"users can only see their own orders"*).
   - Expected Semantic Result: Request rejected (e.g. 403 Forbidden or 404 Not Found); customer cannot inspect another customer's order.
5. **Administrative Authority:**
   - Admin users have global oversight and are exempt from single-user ownership boundaries.

---

## 11. Security Requirements Applicability Matrix

| Security ID | Standard Definition | Applicability to FR-10 | Verification Approach & Limits |
|:---:|---|:---:|---|
| **SEC-01** | Passwords must not be stored in plaintext. | **N/A** | Order state operations do not process password credentials. |
| **SEC-02** | Security-sensitive APIs must require a valid JWT. | **DIRECTLY APPLICABLE (FULL)** | Submit requests with missing, malformed, and tampered JWTs to status endpoints. Black-box API tests verify non-success rejection. |
| **SEC-03** | Admin APIs must verify `role = 'admin'` in the token. | **DIRECTLY APPLICABLE (FULL)** | Submit customer tokens (`role = 'user'`) to `PUT /api/admin/orders/:id/status`. Validates behavioral RBAC rejection. |
| **SEC-04** | User-controlled UI data must be escaped safely. | **N/A (UI-SCOPED)** | Returning raw status strings in JSON responses is standard API behavior. |
| **SEC-05** | Database queries must use parameterized queries. | **PARTIALLY APPLICABLE** | Submit SQL injection strings into `:id` path and `status` body. Evaluates behavioral injection resistance only; does not definitively prove parameterization technique. |
| **SEC-06** | Profile update must not allow client-side role change. | **N/A** | Scoped to profile management (`FR-04`). |
| **SEC-07** | Password-reset OTP entropy and expiry. | **N/A** | Scoped to password reset (`FR-03`). |

---

## 12. Response Body Oracle vs. Persistence State Oracle

To satisfy rigorous verification standards, FR-10 testing employs a strict **Two-Tier Oracle Model**:

### 12.1 Tier 1: Immediate Response Body Oracle
- Assert that mutating requests (`PUT /api/admin/orders/:id/status` and `PUT /api/orders/:id/cancel`) return an appropriate HTTP status code (e.g. `200 OK` for valid transitions, `4xx` error for invalid/unauthorized attempts).
- Validate top-level response attributes (e.g. `message`, `status`) where explicitly documented in `api_specification.md`.

### 12.2 Tier 2: External Persistence State Oracle
- Because an API could theoretically return HTTP 200 without writing to the database, or return an error after partially committing data, **every mutating request must be paired with an independent `GET /api/orders/:id` query**.
- For valid transitions: Verify that `response.order.status` equals the newly requested target state.
- For invalid/rejected transitions: Verify that `response.order.status` remains strictly unchanged at its prior valid state.

---

## 13. Sequence Testing Dimensions

Multi-request sequences required for deterministic lifecycle testing:

1. **Full Fulfillment Lifecycle Sequence:**
   $$\text{POST /api/orders (pending)} \xrightarrow{\text{Admin}} \text{confirmed} \xrightarrow{\text{Admin}} \text{shipping} \xrightarrow{\text{Admin}} \text{delivered (Terminal)}$$
2. **Early Cancellation Sequence (from Pending):**
   $$\text{POST /api/orders (pending)} \xrightarrow{\text{User/Admin}} \text{canceled (Terminal)} \xrightarrow{\text{Admin Attempt}} \text{Rejected} \rightarrow \text{State Remains canceled}$$
3. **Mid-Stream Cancellation Sequence (from Confirmed):**
   $$\text{POST /api/orders (pending)} \xrightarrow{\text{Admin}} \text{confirmed} \xrightarrow{\text{User/Admin}} \text{canceled (Terminal)} \xrightarrow{\text{Admin Attempt}} \text{Rejected} \rightarrow \text{State Remains canceled}$$
4. **Blocked In-Transit Cancellation Sequence:**
   $$\text{POST /api/orders (pending)} \xrightarrow{\text{Admin}} \text{confirmed} \xrightarrow{\text{Admin}} \text{shipping} \xrightarrow{\text{User Cancel Attempt}} \text{Rejected} \rightarrow \text{State Remains shipping}$$
5. **Post-Delivered Immutability Sequence:**
   $$\text{Fulfill to delivered} \xrightarrow{\text{Attempt cancel / regress}} \text{Rejected} \rightarrow \text{State Remains delivered}$$

---

## 14. State Isolation & Dynamic Fixture Strategy

To ensure 100% deterministic suite execution:
1. **No Shared Order IDs:** Every test case generates its own fresh order via setup helper requests (`POST /api/orders`).
2. **Isolated Dynamic Accounts:** Dynamic customer credentials (`userOwner`, `userNonOwner`) and admin credentials (`adminUser`) provisioned per run via `pm.environment.set()`.
3. **No SUT / DB Modification:** Test harness operates purely via public HTTP endpoints without touching database files or backend source code.

---

## 15. Specification Ambiguities (`SPEC-UNDEFINED`)

1. **Idempotent Updates:** Behavior of same-state transitions (e.g. `confirmed -> confirmed`) is not standardized in `api_specification.md` (HTTP 200 NOP vs. HTTP 400 rejection).
2. **Admin In-Transit Cancellation:** Whether an administrator is allowed emergency cancellation during `shipping` is not documented; conservatively treated as `SPEC-UNDEFINED`.
3. **Exact Error Response Schema:** Specific error codes and localized error message structures are unspecified.
4. **Case Sensitivity:** Whether status strings are strictly lower-case or case-insensitive is not defined.

---

## 16. Risk Hypotheses

- **RISK-FR10-01 (Illegal State Skipping):** Backend allows skipping intermediate states (e.g. `pending -> delivered`).
- **RISK-FR10-02 (Backward State Regression):** Backend allows moving backward (e.g. `shipping -> confirmed`).
- **RISK-FR10-03 (Terminal State Mutability):** Backend permits status mutations on orders in `canceled` or `delivered`.
- **RISK-FR10-04 (RBAC Bypass / SEC-03):** Normal customer tokens can trigger admin fulfillment transitions.
- **RISK-FR10-05 (Horizontal Privilege Escalation / IDOR):** Customer can cancel or view orders belonging to another user.
- **RISK-FR10-06 (In-Transit Cancellation Bypass):** Customer can cancel an order that has already shipped.
- **RISK-FR10-07 (Response / DB State Desynchronization):** API returns 200 claiming update, but subsequent GET reveals state was not persisted.

---

## 17. Multi-Interaction Raw AI Generation Plan (Targeting 40–42 Cases)

To provide comprehensive coverage across all testing dimensions and allow for rigorous Human Audit filtering, raw AI test cases will be generated across staged interactions:

| Batch / Interaction | Category Description | Target Count | Test Case ID Range | Status |
|---|---|:---:|---|:---:|
| **Batch 1 (INT-026)** | **Core Valid Forward Transitions & Skip Transitions** | 12 | `FR10-AI-001` – `FR10-AI-012` | **ACTIVE GENERATION** |
| **Batch 2 (INT-027)** | **Backward Regressions, Terminal Immutability & User Cancel** | 10 | `FR10-AI-013` – `FR10-AI-022` | Pending |
| **Batch 3 (INT-028)** | **Authentication (`SEC-02`), RBAC (`SEC-03`) & Ownership** | 8 | `FR10-AI-023` – `FR10-AI-030` | Pending |
| **Batch 4 (INT-029)** | **Status Input Domain, Order ID Boundaries & Schema/SEC-05** | 10 | `FR10-AI-031` – `FR10-AI-040` | Pending |
| **Total** | **Comprehensive Raw AI Suite** | **40** | `FR10-AI-001` – `FR10-AI-040` | — |
