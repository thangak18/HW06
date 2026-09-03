# FR-10 Raw AI Generation Coverage Matrix & Review Flags

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Primary Source File:** [`23127259/testcases/FR10_AI_DRAFT.md`](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR10_AI_DRAFT.md)
- **Frozen Raw AI Draft SHA-256:** `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc`
- **Total Raw AI Cases:** `42`
- **Status:** **FROZEN FOR HUMAN AUDIT (PHASE 2B)**

---

## 1. Generation Inventory Breakdown

| Batch | Interaction | Coverage Scope | ID Range | Case Count | Status |
|:---:|:---:|---|:---:|:---:|:---:|
| **1** | INT-026 | Core Valid Forward Transitions, Valid Cancellations & Skip Transitions | `FR10-AI-001` .. `FR10-AI-012` | 12 | Complete |
| **2** | INT-027 | Backward Regressions, Terminal Immutability & User In-Transit Cancel | `FR10-AI-013` .. `FR10-AI-024` | 12 | Complete |
| **3** | INT-028 | Authentication (`SEC-02`), RBAC (`SEC-03`) & Ownership Boundaries | `FR10-AI-025` .. `FR10-AI-034` | 10 | Complete |
| **4** | INT-029 | Status Domain, Order ID Boundaries, Schema/Persistence & SEC-05 Probe | `FR10-AI-035` .. `FR10-AI-042` | 8 | Complete |
| **Total** | | **All 4 Raw AI Batches** | `FR10-AI-001` .. `FR10-AI-042` | **42** | **FROZEN** |

---

## 2. Comprehensive Coverage Mapping Matrix

| Coverage Dimension | Included Test Case IDs | Count | Specification Strength / Basis | Primary Test Objective |
|---|---|:---:|---|---|
| **Valid Forward Transitions** | `FR10-AI-001`, `FR10-AI-002`, `FR10-AI-003`, `FR10-AI-004` | 4 | `SPECIFICATION-BACKED` (SRS FR-10) | Single-step and full multi-step sequential happy path progression (`pending` $\rightarrow$ `confirmed` $\rightarrow$ `shipping` $\rightarrow$ `delivered`). |
| **Valid Cancellation Transitions** | `FR10-AI-005`, `FR10-AI-006`, `FR10-AI-007`, `FR10-AI-008` | 4 | `SPECIFICATION-BACKED` (SRS Section 4.10) | User and Admin cancellation in pre-shipment states (`pending`, `confirmed`). |
| **Illegal Forward Skip Transitions** | `FR10-AI-009`, `FR10-AI-010`, `FR10-AI-011`, `FR10-AI-012` | 4 | `SPECIFICATION-BACKED` (SRS FR-10 FSM) | Rejection of illegal state skipping (`pending -> shipping`, `pending -> delivered`, `confirmed -> delivered`). |
| **Backward State Regressions** | `FR10-AI-013`, `FR10-AI-014`, `FR10-AI-015` | 3 | `SPECIFICATION-BACKED` (SRS FR-10 FSM) | Rejection of backward state reversal (`confirmed -> pending`, `shipping -> confirmed`, `shipping -> pending`). |
| **User In-Transit Cancellation Rule** | `FR10-AI-016` | 1 | `SPECIFICATION-BACKED` (SRS Section 4.10) | Customer cancellation barred once order reaches `shipping` state. |
| **Terminal State Immutability** | `FR10-AI-017`, `FR10-AI-018`, `FR10-AI-019`, `FR10-AI-020`, `FR10-AI-021`, `FR10-AI-022`, `FR10-AI-023`, `FR10-AI-024` | 8 | `SPECIFICATION-BACKED` (SRS FR-10 Terminal Invariants) | Immutability of terminal states: all 4 mutations from `delivered` and all 4 mutations from `canceled` rejected. |
| **Authentication Enforcement (`SEC-02`)** | `FR10-AI-025`, `FR10-AI-026`, `FR10-AI-027`, `FR10-AI-028`, `FR10-AI-029` | 5 | `SPECIFICATION-BACKED` (`SEC-02` Standard) | Rejection of unauthenticated, malformed, random, and tampered JWTs across Admin and Customer routes. |
| **Authorization / RBAC (`SEC-03`)** | `FR10-AI-030`, `FR10-AI-031`, `FR10-AI-032` | 3 | `SPECIFICATION-BACKED` (`SEC-03` / SRS FR-12) | Prevention of normal customer tokens invoking Admin status mutations and Admin routes. |
| **Cross-Tenant Ownership Boundaries** | `FR10-AI-033`, `FR10-AI-034` | 2 | `PARTIALLY SPECIFICATION-BACKED / OWNERSHIP` | Prevention of Customer B cancelling Customer A's `pending` or `confirmed` orders. |
| **Status Input Domain Validation** | `FR10-AI-035`, `FR10-AI-036`, `FR10-AI-037`, `FR10-AI-038` | 4 | `SPECIFICATION-BACKED` / `PARTIAL` | Rejection of undocumented enum values, missing status property, null values, and non-string JSON types. |
| **Order ID Partition Validation** | `FR10-AI-039`, `FR10-AI-040` | 2 | `SPECIFICATION-BACKED` (API-SPEC) | Rejection of non-existent order IDs (e.g. `999999`) and malformed non-numeric order ID paths. |
| **Response Schema & Persistence Consistency** | `FR10-AI-041` | 1 | `SPECIFICATION-BACKED` (API-SPEC / SRS 4.10) | Validates response contract attributes and immediate read-after-write (`GET /api/orders/:id`) consistency. |
| **Security / SQL Injection Probe (`SEC-05`)** | `FR10-AI-042` | 1 | `SEC-05 / PARTIAL BLACK-BOX PROBE` | Behavioral black-box probe verifying SQL injection strings in `:id` parameter do not alter database records. |

---

## 3. Potential Human-Audit Review Flags

The following test cases require specific scrutiny during the upcoming Human Audit phase (Phase 2B) before inclusion in the final executable test suite:

1. **`FR10-AI-012` (Multiple Failure Dimensions / Confounded Oracle):**
   - *Issue:* Combines an unauthorized actor (`role = 'user'`) with an illegal skip transition (`pending -> shipping`).
   - *Review Objective:* Audit must decide whether to split, adjust to pure RBAC, adjust to pure skip transition, or classify as incomplete with corrections.

2. **`FR10-AI-033` & `FR10-AI-034` (Ownership Oracle Strength):**
   - *Issue:* Evaluates cross-user cancellation (`PUT /api/orders/:id/cancel`). SRS wording states "customer can cancel their order", implying ownership rather than an explicit multi-tenant specification clause.
   - *Review Objective:* Verify whether the oracle should remain `PARTIALLY SPECIFICATION-BACKED` or be refined against documented API contract expectations.

3. **`FR10-AI-038` (Non-String Type Coercion):**
   - *Issue:* Sends numeric status `{"status": 123}`. Express/JavaScript may handle type coercion differently unless JSON schema validation middleware is enforced.
   - *Review Objective:* Audit should verify whether type validation expectations match normative specification or constitute an exploratory boundary probe.

4. **`FR10-AI-042` (SEC-05 Black-Box Limitations):**
   - *Issue:* Tests SQL injection via URL path parameter `1' OR '1'='1`. Black-box HTTP execution cannot prove internal parameterized queries.
   - *Review Objective:* Ensure the audit verdict evaluates this strictly as behavioral evidence rather than internal cryptographic or architectural proof.

---

## 4. Frozen Raw Inventory Checksum & Integrity Log

- **File Path:** `23127259/testcases/FR10_AI_DRAFT.md`
- **Total Cases:** `42`
- **Continuous ID Range:** `FR10-AI-001` .. `FR10-AI-042` (0 missing, 0 duplicates)
- **Human-Generated Test Cases (`FR10-HUM`):** `0` (Strictly reserved for Phase 2C)
- **Frozen SHA-256:** `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc`
