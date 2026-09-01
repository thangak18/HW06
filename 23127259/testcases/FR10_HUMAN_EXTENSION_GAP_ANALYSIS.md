# FR-10 Human Extension Coverage Gap Analysis & Recommendations

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Base Audited Suite:** `41` Usable AI-Derived Test Cases (`FR10-AI-001` .. `FR10-AI-042`, excluding `FR10-AI-012`)
- **Purpose:** Systematic identification of functional, state-continuity, security, and boundary gaps in the AI-derived suite to guide the design of $\ge 5$ Human-designed extension test cases (`FR10-HUM-xxx`).
- **Status:** **ANALYSIS & RECOMMENDATIONS ONLY (NO `FR10-HUM` IDs ASSIGNED YET)**

---

## 1. Baseline AI Suite Coverage & Remaining Blindspots

The 41 usable AI-derived test cases provide extensive coverage across:
1. **Core Lifecycle Progression:** Atomic forward steps (`001`..`003`), full 4-stage linear path (`004`), customer & admin cancellations (`005`..`008`).
2. **Invalid Forward Transitions:** Skips from `pending` $\rightarrow$ `shipping`/`delivered` (`009`, `010`) and `confirmed` $\rightarrow$ `delivered` (`011`).
3. **Invalid Backward Regressions:** 1-step and 2-step reverse regressions (`013`..`015`).
4. **Terminal State Immutability:** Exhaustive pairwise rejection of transitions from `delivered` (`017`..`020`) and `canceled` (`021`..`024`).
5. **Authentication & RBAC:** `SEC-02` header partitions (`025`..`029`) and `SEC-03` role boundaries (`030`..`032`).
6. **Cross-User Ownership & Input Domain:** Customer B cancellation probes (`033`, `034`), enum/schema/type validation (`035`..`038`), non-existent/malformed IDs (`039`, `040`), read-after-write consistency (`041`), and `SEC-05` black-box injection (`042`).

### Identified Testing Blindspots in Pure AI Suites:
While pairwise state edges are heavily represented, AI generation tends to focus on single-request atomic checks. Key blindspots remain in **multi-entity state isolation**, **state-machine continuity after rejection**, **idempotent same-state operations**, **downstream lifecycle recovery**, and **adjacent security/read boundaries**.

---

## 2. Comprehensive Candidate Gap Directions

The following candidate gap directions are identified through systematic gap analysis:

| Gap ID | Proposed Testing Direction | Why AI Coverage Is Insufficient | Specification Strength | Distinctness & Value | Recommended? |
|:---:|---|---|---|---|:---:|
| **`G-01`** | **Same-State / Idempotent Mutation Probe** (`pending` $\rightarrow$ `pending`, `confirmed` $\rightarrow$ `confirmed`) | AI suite tests only distinct-state transitions; does not probe whether requesting the order's current state is treated as a valid no-op (200) or rejected (400). | `EXPLORATORY / API CONTRACT` (Spec does not formally define same-state semantics) | High (Tests FSM self-loops and API idempotency). | **YES (Recommended)** |
| **`G-02`** | **Authentication Absence on Order Read Endpoint** (`GET /api/orders/:id` without token) | AI suite tests `SEC-02` on mutation routes (`PUT /status`, `PUT /cancel`), but does not verify whether query endpoints used for persistence verification are also secured. | `SPECIFICATION-BACKED` (`SEC-02` applies to protected order data) | High (Ensures persistence oracle endpoint is authentic). | **YES (Recommended)** |
| **`G-03`** | **Cross-User Order Query / IDOR Vulnerability Probe** (User B reads User A's order) | AI cases `033` and `034` test cross-user mutation rejection, but do not verify whether customer order details are protected against unauthorized read access (IDOR). | `FR-11 DEPENDENCY / ADDITIONAL-SEC` (Derived from order privacy and customer self-service) | High (Adjacent security boundary complementing cancellation ownership). | **YES (Recommended)** |
| **`G-04`** | **State-Machine Continuity & Recovery After Rejected Mutation** | AI cases verify that invalid mutations leave state unchanged, but do not perform a subsequent valid transition on the same order to prove the FSM engine was not left in a corrupted or locked state. | `SPECIFICATION-BACKED` (SRS FR-10 state persistence and lifecycle continuity) | Very High (Proves transactional integrity and recovery after error). | **YES (Recommended)** |
| **`G-05`** | **Multi-Entity State Isolation (Zero Cross-Order Side-Effects)** | AI tests execute against single isolated orders; none verify that transitioning Order A leaves an identically-staged Order B strictly untouched in the database. | `SPECIFICATION-BACKED` (Relational entity independence and transaction isolation) | Very High (Prevents bulk mutation / `WHERE` clause omission bugs). | **YES (Recommended)** |
| **`G-06`** | **Rapid Sequential Mutation / Idempotency Stress Probe** | AI cases submit one transition per test block; none evaluate sequential duplicate transition requests in rapid succession. | `EXPLORATORY / API CONTRACT` (Specification does not specify concurrency SLAs) | Medium (Black-box race condition probe; risk of non-deterministic timing in Newman). | **NO (Optional)** |
| **`G-07`** | **Post-Rejected Customer Cancellation Fulfillment Continuity** (`pending` $\rightarrow$ `confirmed` $\rightarrow$ `shipping` $\rightarrow$ User cancel rejected $\rightarrow$ Admin `delivered`) | `FR10-AI-016` tests rejection of user cancellation during shipping in isolation. This tests that following this rejected attempt, Admin can cleanly fulfill the order to `delivered`. | `SPECIFICATION-BACKED` (SRS Section 4.10 fulfillment completion flow) | High (Validates end-to-end business resolution after customer rejection). | **YES (Recommended)** |
| **`G-08`** | **Malformed Request `Content-Type` Header Handling** (`application/x-www-form-urlencoded` on Admin status endpoint) | AI suite tests JSON payloads only; non-JSON encodings may trigger unhandled server exceptions (HTTP 500) if middleware lacks content negotiation. | `EXPLORATORY / API CONTRACT` (API contract specifies JSON request bodies) | Medium-High (Discovers unhandled 500 crashes on non-JSON payloads). | **YES (Recommended)** |

---

## 3. Recommended Shortlist for Student Selection (5–7 Directions)

Based on distinctness, deterministic execution reliability in Postman/Newman, and bug-discovery potential, the following **6 candidate directions** are recommended for final Student selection:

1. **`G-01` (Same-State Self-Loop Probe):** Admin attempts `confirmed` $\rightarrow$ `confirmed`. Probes whether redundant status updates are safely idempotent or explicitly rejected without state corruption.
2. **`G-04` (State-Machine Recovery Sequence):** Attempt illegal skip `pending` $\rightarrow$ `shipping` (rejected), verify `pending`, then immediately perform legal Admin transition `pending` $\rightarrow$ `confirmed` (succeeds).
3. **`G-05` (Multi-Order Entity Isolation):** Create Order 1 and Order 2 in `pending`. Transition Order 1 to `confirmed`. Verify Order 1 is `confirmed` and Order 2 remains strictly `pending`.
4. **`G-07` (Lifecycle Fulfillment Following Barred User Cancellation):** Progress order to `shipping`. Owner Customer attempts `PUT /api/orders/:id/cancel` (rejected). Admin subsequently transitions `shipping` $\rightarrow$ `delivered` (succeeds).
5. **`G-03` (Adjacent Security: Cross-User Read / IDOR Probe):** Customer B attempts `GET /api/orders/{{orderAId}}` targeting Customer A's order to verify data isolation.
6. **`G-08` (API Contract Robustness: Non-JSON Content-Type Handling):** Admin submits status mutation with `Content-Type: text/plain` or form-urlencoded to test graceful content negotiation vs server crash.

---

## 4. Human Extension Rules & Policy
- **Human Cases Created in This Phase:** **`0`**
- **Formal Assignment of `FR10-HUM-xxx` IDs:** Reserved exclusively for Phase 2C after explicit Student selection.
- **AI Tooling Role:** AI-assisted gap analysis and candidate recommendations only.
