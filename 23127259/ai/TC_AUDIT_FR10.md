# FR-10 Human Audit of Raw AI-Generated Test Cases

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Raw AI-Generated Cases:** `42`
- **Frozen Raw AI SHA-256:** `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc`
- **Human Audit Status:** `COMPLETE (38 VALID, 1 INVALID, 3 INCOMPLETE; 41 USABLE AFTER CORRECTIONS)`

---

## 1. Audit Framework & Verdict Definitions

Every raw AI test case must be evaluated against the authoritative specification hierarchy (HW06 Requirements, EShop SRS Section 4.10, api_specification.md) without inspecting SUT runtime implementation as the oracle.

### Allowed Human Verdicts:

- **`VALID`**: The test objective is relevant, non-duplicate, and its formal oracle is sufficiently supported by the authoritative specification.
- **`INVALID`**: The test is duplicate, irrelevant, logically invalid, uses a false oracle, or cannot be made valid without changing its essential objective.
- **`INCOMPLETE`**: The test has a useful objective, but one or more details/oracles are over-specified, under-specified, confounded, or require correction before executable use.

---

## 2. Complete 42-Case Human Audit Decision Table

| Test ID | AI Objective | Spec Basis | Oracle Strength | Human Verdict | Human Reasoning | Required Correction | Executable After Correction? |
|---|---|---|---|:---:|---|---|:---:|
| `FR10-AI-001` | Valid Admin transition `pending` $\rightarrow$ `confirmed` | SRS Section 4.10 | HIGH | **VALID** | Atomic baseline transition pending -> confirmed using valid Admin actor. Explicitly part of FR-10 state model and distinct from full lifecycle sequence. | NONE. | **YES** |
| `FR10-AI-002` | Valid Admin transition `confirmed` $\rightarrow$ `shipping` | SRS Section 4.10 | HIGH | **VALID** | Cleanly isolates confirmed -> shipping transition with valid Admin authorization and correct starting state. | NONE. | **YES** |
| `FR10-AI-003` | Valid Admin transition `shipping` $\rightarrow$ `delivered` | SRS Section 4.10 | HIGH | **VALID** | Cleanly isolates shipping -> delivered fulfillment edge. Delivered is documented terminal completion state and test uses correct Admin actor. | NONE. | **YES** |
| `FR10-AI-004` | Complete linear lifecycle progression `pending` $\rightarrow$ `delivered` | SRS Section 4.10 | HIGH | **VALID** | Validates lifecycle continuity on one order across complete pending -> confirmed -> shipping -> delivered sequence rather than testing a single transition in isolation; not a duplicate. | NONE. | **YES** |
| `FR10-AI-005` | Customer cancels own `pending` order via `PUT /api/orders/:id/cancel` | SRS Section 4.10 | HIGH | **VALID** | Tests specification-backed customer self-service cancellation of owner's pending order through customer cancellation endpoint. | NONE. | **YES** |
| `FR10-AI-006` | Admin cancels `pending` order via `PUT /api/admin/orders/:id/status` | SRS Section 4.10 | HIGH | **VALID** | Tests distinct Admin cancellation path for pending order through Admin status mutation endpoint; actor and route differ meaningfully from AI-005. | NONE. | **YES** |
| `FR10-AI-007` | Customer cancels own `confirmed` order via `PUT /api/orders/:id/cancel` | SRS Section 4.10 | HIGH | **VALID** | Verifies owner customer may cancel confirmed order before it enters shipping; distinct state boundary from pending cancellation. | NONE. | **YES** |
| `FR10-AI-008` | Admin cancels `confirmed` order via `PUT /api/admin/orders/:id/status` | SRS Section 4.10 | HIGH | **VALID** | Verifies Admin cancellation path from confirmed state; distinct from customer cancellation endpoint used by AI-007. | NONE. | **YES** |
| `FR10-AI-009` | Illegal Admin forward skip `pending` $\rightarrow$ `shipping` | SRS FR-10 FSM | HIGH | **VALID** | Cleanly isolates illegal FSM skip from pending directly to shipping while using valid Admin authorization. Rejection and unchanged persisted state are appropriate semantic oracles. | NONE. | **YES** |
| `FR10-AI-010` | Illegal Admin forward skip `pending` $\rightarrow$ `delivered` | SRS FR-10 FSM | HIGH | **VALID** | Cleanly tests larger illegal skip pending -> delivered; distinct from AI-009 because it bypasses both confirmed and shipping states. | NONE. | **YES** |
| `FR10-AI-011` | Illegal Admin forward skip `confirmed` $\rightarrow$ `delivered` | SRS FR-10 FSM | HIGH | **VALID** | Isolates confirmed -> delivered and verifies shipping stage cannot be skipped after confirmation. | NONE. | **YES** |
| `FR10-AI-012` | Unauthorized customer forward skip `pending` $\rightarrow$ `shipping` | SRS FR-10 / SEC-03 | MEDIUM (Confounded) | **INVALID** | Contains two independent invalid dimensions in same request (normal customer token on Admin mutation endpoint + illegal pending -> shipping FSM skip). Ambiguous failure causality; reducing to Admin duplicates 009, reducing to RBAC overlaps SEC-03 (030). | NONE – REJECT RAW CASE FROM EXECUTABLE SUITE. | **NO** |
| `FR10-AI-013` | Illegal backward regression `confirmed` $\rightarrow$ `pending` | SRS FR-10 FSM | HIGH | **VALID** | Cleanly isolates backward FSM regression confirmed -> pending using valid Admin authorization. State transition itself is only invalid dimension. | NONE. | **YES** |
| `FR10-AI-014` | Illegal backward regression `shipping` $\rightarrow$ `confirmed` | SRS FR-10 FSM | HIGH | **VALID** | Tests distinct backward transition shipping -> confirmed with valid Admin actor. Verifies in-transit order cannot regress to prior confirmed state. | NONE. | **YES** |
| `FR10-AI-015` | Illegal backward multi-stage regression `shipping` $\rightarrow$ `pending` | SRS FR-10 FSM | HIGH | **VALID** | Tests shipping -> pending (larger backward regression than AI-014). Bypasses multiple lifecycle stages in reverse; distinct state-pair test rather than duplicate. | NONE. | **YES** |
| `FR10-AI-016` | Customer prohibited cancellation of in-transit order (`shipping`) | SRS Section 4.10 | HIGH | **VALID** | Directly tests explicit business rule that owner customer cannot cancel order after entering shipping. Auth, ownership, and starting state valid, isolating prohibited shipping-cancellation rule. | NONE. | **YES** |
| `FR10-AI-017` | Illegal terminal state mutation `delivered` $\rightarrow$ `pending` | SRS FR-10 FSM | HIGH | **VALID** | Tests delivered -> pending. Delivered is terminal state; verifies completed order cannot be resurrected to initial state. | NONE. | **YES** |
| `FR10-AI-018` | Illegal terminal state mutation `delivered` $\rightarrow$ `confirmed` | SRS FR-10 FSM | HIGH | **VALID** | Tests delivered -> confirmed. Distinct target state contributing explicit transition-pair coverage for terminal immutability. | NONE. | **YES** |
| `FR10-AI-019` | Illegal terminal state mutation `delivered` $\rightarrow$ `shipping` | SRS FR-10 FSM | HIGH | **VALID** | Tests delivered -> shipping; verifies completed order cannot regress into active transit; distinct prohibited state pair. | NONE. | **YES** |
| `FR10-AI-020` | Illegal terminal state mutation `delivered` $\rightarrow$ `canceled` | SRS FR-10 FSM | HIGH | **VALID** | Tests delivered -> canceled. Important cross-terminal business boundary because fulfilled transaction must not subsequently be voided. | NONE. | **YES** |
| `FR10-AI-021` | Illegal terminal state mutation `canceled` $\rightarrow$ `pending` | SRS FR-10 FSM | HIGH | **VALID** | Tests canceled -> pending; verifies canceled terminal order cannot be resurrected into initial processing state. | NONE. | **YES** |
| `FR10-AI-022` | Illegal terminal state mutation `canceled` $\rightarrow$ `confirmed` | SRS FR-10 FSM | HIGH | **VALID** | Tests canceled -> confirmed. Distinct forbidden target state providing explicit state-pair coverage for terminal immutability. | NONE. | **YES** |
| `FR10-AI-023` | Illegal terminal state mutation `canceled` $\rightarrow$ `shipping` | SRS FR-10 FSM | HIGH | **VALID** | Tests canceled -> shipping; verifies voided order cannot re-enter fulfillment/distribution lifecycle. | NONE. | **YES** |
| `FR10-AI-024` | Illegal terminal state mutation `canceled` $\rightarrow$ `delivered` | SRS FR-10 FSM | HIGH | **VALID** | Tests canceled -> delivered. Critical cross-terminal isolation case ensuring canceled transaction cannot later be marked successfully delivered. | NONE. | **YES** |
| `FR10-AI-025` | SEC-02 missing Authorization header on Admin status transition | SEC-02 Standard | HIGH | **VALID** | Unauthenticated baseline for Admin status mutation; requested pending -> confirmed transition would otherwise be valid, isolating missing authentication. | NONE. | **YES** |
| `FR10-AI-026` | SEC-02 malformed Authorization header on Admin status transition | SEC-02 Standard | HIGH | **VALID** | Malformed Authorization/Bearer header is distinct authentication input partition from completely missing header; tests malformed credential transport rejection. | NONE. | **YES** |
| `FR10-AI-027` | SEC-02 invalid/random JWT on Admin status transition | SEC-02 Standard | HIGH | **VALID** | Invalid/random token string is distinct from missing/malformed scheme; provides valid SEC-02 behavioral authentication partition. | NONE. | **YES** |
| `FR10-AI-028` | SEC-02 cryptographically tampered JWT on Admin status transition | SEC-02 Standard | HIGH | **VALID** | Tampered previously-valid JWT is meaningful distinct authentication partition; black-box oracle limited to behavioral rejection (does not prove internal crypto). | NONE. | **YES** |
| `FR10-AI-029` | SEC-02 missing Authorization header on customer cancel endpoint | SEC-02 Standard | HIGH | **VALID** | Checks SEC-02 authentication enforcement on customer-facing cancellation endpoint rather than Admin mutation route; pending self-cancellation otherwise valid. | NONE. | **YES** |
| `FR10-AI-030` | SEC-03 normal user role attempting Admin transition `pending` $\rightarrow$ `confirmed` | SEC-03 Standard | HIGH | **VALID** | Cleanly isolates SEC-03 using valid normal-user token against otherwise-valid Admin transition pending -> confirmed; state remains unchanged if rejected. | NONE. | **YES** |
| `FR10-AI-031` | SEC-03 normal user role attempting Admin cancellation route | SEC-03 Standard | HIGH | **VALID** | Tests Admin-only route with valid normal-user token while targeting state change otherwise valid for Admin; distinct RBAC probe because target is cancellation. | NONE. | **YES** |
| `FR10-AI-032` | SEC-03 normal user role attempting Admin transit dispatch `confirmed` $\rightarrow$ `shipping` | SEC-03 Standard | HIGH | **VALID** | Checks same Admin-role boundary at confirmed -> shipping stage; distinct state-context coverage demonstrating RBAC is not limited to initial pending state. | NONE. | **YES** |
| `FR10-AI-033` | Cross-user ownership boundary: User B cancelling User A's `pending` order | SRS 4.10 / Ownership | MEDIUM-HIGH | **INCOMPLETE** | Cleanly isolates cross-user ownership, but FR-10 wording lacks explicit access-control matrix stating User B must never cancel User A's order; implied by self-service semantics. | Classify as PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION; preserve valid User B auth, pending cancellable state, only ownership mismatch; do not claim exact HTTP status; report unexpected mutations conservatively. | **YES** |
| `FR10-AI-034` | Cross-user ownership boundary: User B cancelling User A's `confirmed` order | SRS 4.10 / Ownership | MEDIUM-HIGH | **INCOMPLETE** | Same specification-strength limitation as AI-033 on confirmed state; confirmed orders normally cancellable before shipping, but cross-user prohibition is implied rather than explicit rule. | Classify as PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION; preserve valid User B auth, confirmed order belonging to User A, otherwise-valid cancellation state, ownership mismatch; do not invent exact HTTP status. | **YES** |
| `FR10-AI-035` | Undocumented status enum value (`{"status": "processing"}`) | SRS 4.10 Domain | HIGH | **VALID** | Authoritative state model defines allowed domain; "processing" is undocumented out-of-domain value; correctly verifies invalid target does not cause transition and persisted state remains unchanged without inventing specific HTTP code. | NONE. | **YES** |
| `FR10-AI-036` | Missing mandatory `status` property in mutation body (`{}`) | API-SPEC Schema | HIGH | **VALID** | Admin mutation API requires status target; empty body provides no target and cannot represent valid transition; semantic oracle limited to no transition and unchanged state. | NONE. | **YES** |
| `FR10-AI-037` | Null `status` value in mutation body (`{"status": null}`) | API-SPEC Schema | HIGH | **VALID** | Explicit null is distinct from omitted property and not a documented state; valid oracle is null must not cause transition without assuming implementation mechanism. | NONE. | **YES** |
| `FR10-AI-038` | Wrong JSON type for `status` property (`{"status": 123}`) | API-SPEC Type | MEDIUM (Input Contract) | **VALID** | Input-domain robustness test; numeric 123 is not documented state; oracle limited to numeric input must not produce valid transition and state remains unchanged (no JS-specific error asserted). | NONE. | **YES** |
| `FR10-AI-039` | Well-formed non-existent order ID (`:id = 999999`) | API-SPEC Resource | HIGH | **VALID** | Well-formed non-existing ID is meaningful resource boundary; does not require 404 unless documented; core invariant is nonexistent target cannot transition and unrelated orders untouched. | NONE. | **YES** |
| `FR10-AI-040` | Malformed non-numeric order ID (`:id = "not-an-id"`) | API-SPEC Parameter | MEDIUM (Input Robustness) | **INCOMPLETE** | Contract does not establish normative numeric-only syntax for :id path param; cannot infer from implementation/DB. | Classify as PARTIALLY SPECIFICATION-BACKED / INPUT ROBUSTNESS; describe "not-an-id" as malformed/unsupported identifier probe; require only no unintended mutation; do not require exact 400/404; if handled safely, record actual behavior without filing bug. | **YES** |
| `FR10-AI-041` | Valid transition response schema & read-after-write persistence consistency | SRS 4.10 / API-SPEC | HIGH | **VALID** | Distinct from AI-001 (which tests transition permission); AI-041 tests response schema and externally observable persisted state consistency via documented GET order endpoint. | NONE. | **YES** |
| `FR10-AI-042` | SEC-05 black-box SQL injection probe in `:id` parameter | SEC-05 Standard | MEDIUM-HIGH (Behavioral) | **VALID** | Scoped as SEC-05 / PARTIAL BLACK-BOX BEHAVIORAL EVIDENCE; behavioral invariants limited to payload not causing unintended mutation; HTTP 500 alone not treated as SQLi proof or SEC-05 violation. | NONE. | **YES** |

---

## 3. Batch 1 Audited Decisions & Rationale (`FR10-AI-001` .. `FR10-AI-012`)

- **Total Batch 1 Audited:** `12 / 12`
- **Batch 1 Decisions:** `11 VALID`, `1 INVALID`, `0 INCOMPLETE`

### FR10-AI-001 – VERDICT: VALID
- **Human Reasoning:** Atomic baseline transition `pending` $\rightarrow$ `confirmed` using valid Admin actor. Explicitly part of FR-10 state model and distinct from full lifecycle sequence.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-002 – VERDICT: VALID
- **Human Reasoning:** Cleanly isolates `confirmed` $\rightarrow$ `shipping` transition with valid Admin authorization and correct starting state.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-003 – VERDICT: VALID
- **Human Reasoning:** Cleanly isolates `shipping` $\rightarrow$ `delivered` fulfillment edge. Delivered is documented terminal completion state and test uses correct Admin actor.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-004 – VERDICT: VALID
- **Human Reasoning:** Validates lifecycle continuity on one order across complete `pending` $\rightarrow$ `confirmed` $\rightarrow$ `shipping` $\rightarrow$ `delivered` sequence rather than testing a single transition in isolation. Retained for multi-step entity continuity.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-005 – VERDICT: VALID
- **Human Reasoning:** Tests specification-backed customer self-service cancellation of owner's pending order through customer cancellation endpoint.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-006 – VERDICT: VALID
- **Human Reasoning:** Tests distinct Admin cancellation path for pending order through Admin status mutation endpoint; actor and route differ meaningfully from AI-005.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-007 – VERDICT: VALID
- **Human Reasoning:** Verifies owner customer may cancel confirmed order before it enters shipping; distinct state boundary from pending cancellation.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-008 – VERDICT: VALID
- **Human Reasoning:** Verifies Admin cancellation path from confirmed state; distinct from customer cancellation endpoint used by AI-007.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-009 – VERDICT: VALID
- **Human Reasoning:** Cleanly isolates illegal FSM skip from `pending` directly to `shipping` while using valid Admin authorization. Rejection and unchanged persisted state are appropriate semantic oracles.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-010 – VERDICT: VALID
- **Human Reasoning:** Cleanly tests larger illegal skip `pending` $\rightarrow$ `delivered`. Distinct from AI-009 because it bypasses both confirmed and shipping states.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-011 – VERDICT: VALID
- **Human Reasoning:** Isolates `confirmed` $\rightarrow$ `delivered` and verifies shipping stage cannot be skipped after confirmation.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-012 – VERDICT: INVALID
- **Human Reasoning:** Contains two independent invalid dimensions in same request: (1) normal customer token on Admin-only mutation endpoint; (2) `pending` $\rightarrow$ `shipping` is an illegal FSM skip. Rejection cannot establish whether RBAC or FSM caused failure. Reducing to Admin duplicates 009; reducing to RBAC overlaps 030. Retained in raw draft, rejected from executable suite.
- **Required Correction:** NONE – REJECT RAW CASE FROM EXECUTABLE SUITE.
- **Executable After Correction:** NO.

---

## 4. Batch 2 Audited Decisions & Rationale (`FR10-AI-013` .. `FR10-AI-024`)

- **Total Batch 2 Audited:** `12 / 12`
- **Batch 2 Decisions:** `12 VALID`, `0 INVALID`, `0 INCOMPLETE`

### FR10-AI-013 – VERDICT: VALID
- **Human Reasoning:** Cleanly isolates backward FSM regression `confirmed` $\rightarrow$ `pending` using valid Admin authorization. State transition itself is only invalid dimension.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-014 – VERDICT: VALID
- **Human Reasoning:** Tests distinct backward transition `shipping` $\rightarrow$ `confirmed` with valid Admin actor. Verifies in-transit order cannot regress to prior confirmed state.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-015 – VERDICT: VALID
- **Human Reasoning:** Tests `shipping` $\rightarrow$ `pending` (larger backward regression than AI-014). Bypasses multiple lifecycle stages in reverse; distinct state-pair test rather than duplicate.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-016 – VERDICT: VALID
- **Human Reasoning:** Directly tests explicit business rule that owner customer cannot cancel order after entering shipping. Auth, ownership, and starting state valid, isolating prohibited shipping-cancellation rule.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-017 – VERDICT: VALID
- **Human Reasoning:** Tests `delivered` $\rightarrow$ `pending`. Delivered is terminal state; verifies completed order cannot be resurrected to initial state.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-018 – VERDICT: VALID
- **Human Reasoning:** Tests `delivered` $\rightarrow$ `confirmed`. Distinct target state contributing explicit transition-pair coverage for terminal immutability.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-019 – VERDICT: VALID
- **Human Reasoning:** Tests `delivered` $\rightarrow$ `shipping` and verifies completed order cannot regress into active transit; distinct prohibited state pair.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-020 – VERDICT: VALID
- **Human Reasoning:** Tests `delivered` $\rightarrow$ `canceled`. Important cross-terminal business boundary because fulfilled transaction must not subsequently be voided.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-021 – VERDICT: VALID
- **Human Reasoning:** Tests `canceled` $\rightarrow$ `pending`; verifies canceled terminal order cannot be resurrected into initial processing state.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-022 – VERDICT: VALID
- **Human Reasoning:** Tests `canceled` $\rightarrow$ `confirmed`. Distinct forbidden target state providing explicit state-pair coverage for terminal immutability.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-023 – VERDICT: VALID
- **Human Reasoning:** Tests `canceled` $\rightarrow$ `shipping`; verifies voided order cannot re-enter fulfillment/distribution lifecycle.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-024 – VERDICT: VALID
- **Human Reasoning:** Tests `canceled` $\rightarrow$ `delivered`. Critical cross-terminal isolation case ensuring canceled transaction cannot later be marked successfully delivered.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

---

## 5. Batch 3 Audited Decisions & Rationale (`FR10-AI-025` .. `FR10-AI-034`)

- **Total Batch 3 Audited:** `10 / 10`
- **Batch 3 Decisions:** `8 VALID`, `0 INVALID`, `2 INCOMPLETE`

### FR10-AI-025 – VERDICT: VALID
- **Human Reasoning:** Provides unauthenticated baseline for Admin status mutation endpoint. Requested `pending` $\rightarrow$ `confirmed` transition otherwise valid, isolating missing authentication.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-026 – VERDICT: VALID
- **Human Reasoning:** Malformed Authorization/Bearer header is distinct authentication input partition from missing header; tests malformed credential transport rejection.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-027 – VERDICT: VALID
- **Human Reasoning:** Invalid/random token string is distinct from missing/malformed scheme; provides valid `SEC-02` behavioral authentication partition.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-028 – VERDICT: VALID
- **Human Reasoning:** Tampered previously-valid JWT is meaningful distinct authentication partition. Black-box oracle limited to behavioral rejection of tampered token (does NOT prove internal crypto).
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-029 – VERDICT: VALID
- **Human Reasoning:** Checks `SEC-02` authentication enforcement on customer-facing cancellation endpoint. Pending self-cancellation operation would otherwise be valid.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-030 – VERDICT: VALID
- **Human Reasoning:** Cleanly isolates `SEC-03` by using valid normal-user token against otherwise-valid Admin transition `pending` $\rightarrow$ `confirmed`; state remains unchanged.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-031 – VERDICT: VALID
- **Human Reasoning:** Tests Admin-only route with valid normal-user token while targeting cancellation state change otherwise valid for Admin; distinct RBAC probe.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-032 – VERDICT: VALID
- **Human Reasoning:** Checks Admin-role boundary at `confirmed` $\rightarrow$ `shipping` stage; distinct state-context coverage demonstrating RBAC is enforced across lifecycle.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-033 – VERDICT: INCOMPLETE
- **Human Reasoning:** Objective is useful and cleanly isolates cross-user ownership, but FR-10 wording lacks explicit access-control matrix stating User B must never cancel User A's order; implied by self-service semantics.
- **Required Correction:** For corrected executable derivative: (1) classify as `PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION`; (2) preserve valid User B authentication, pending cancellable state, and only ownership mismatch; (3) do not claim exact HTTP status; (4) do not use failure of this case alone as proof of violation of an explicit named requirement; (5) report unexpected mutations conservatively.
- **Executable After Correction:** YES.

### FR10-AI-034 – VERDICT: INCOMPLETE
- **Human Reasoning:** Same specification-strength limitation as AI-033 on confirmed state; confirmed orders normally cancellable before shipping, but cross-user prohibition is implied rather than explicit rule.
- **Required Correction:** For corrected executable derivative: (1) classify as `PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION`; (2) preserve valid User B authentication, legitimately confirmed order belonging to User A, otherwise-valid cancellation state, and ownership mismatch; (3) do not invent exact HTTP status; (4) do not overstate result as proof of explicit requirement violation.
- **Executable After Correction:** YES.

---

## 6. Batch 4 Audited Decisions & Rationale (`FR10-AI-035` .. `FR10-AI-042`)

- **Total Batch 4 Audited:** `8 / 8`
- **Batch 4 Decisions:** `7 VALID`, `0 INVALID`, `1 INCOMPLETE`

### FR10-AI-035 – VERDICT: VALID
- **Human Reasoning:** The authoritative FR-10 state model defines the allowed order status domain as the documented lifecycle states. `"processing"` is outside that domain. The test appropriately verifies that an undocumented target state must not cause a valid transition and that the persisted order remains unchanged. The case does not require a specific conventional HTTP error code.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-036 – VERDICT: VALID
- **Human Reasoning:** The Admin status mutation API requires a status target in its request body. An empty JSON object provides no requested lifecycle target and therefore cannot represent a valid FR-10 transition. The semantic oracle is limited to: (1) no valid transition occurs; (2) state remains unchanged. No exact validation payload or HTTP status is invented.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-037 – VERDICT: VALID
- **Human Reasoning:** Explicit null is distinct from an omitted property and is not one of the documented lifecycle states. The valid oracle is that null must not cause a successful lifecycle transition. No implementation-specific null-handling mechanism is assumed.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-038 – VERDICT: VALID
- **Human Reasoning:** The raw case is already conservatively classified as `PARTIALLY SPECIFICATION-BACKED`. Although the API documentation may not define a strict JSON type schema for status, numeric `123` is not one of the documented lifecycle states. The test remains valid as an input-domain robustness test because its oracle is limited to: (1) numeric input must not produce a legitimate documented state transition; (2) persisted state must remain unchanged. It must NOT assert a JavaScript-specific type error, coercion behavior, or specific validation response.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-039 – VERDICT: VALID
- **Human Reasoning:** A well-formed but non-existing resource identifier is a meaningful API resource boundary for the FR-10 mutation endpoint. The case does not require a conventional 404 unless explicitly documented. The important invariant is: (1) a nonexistent target cannot be successfully transitioned; (2) no unrelated existing order is modified.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-040 – VERDICT: INCOMPLETE
- **Human Reasoning:** The test objective is useful as malformed path-parameter robustness coverage, but the authoritative API contract does not sufficiently establish that the `:id` path parameter has a normative numeric-only syntax. Inferring numeric format merely because the implementation/database uses numeric IDs would incorrectly turn an implementation detail into the oracle.
- **Required Correction:** For the corrected executable derivative: (1) classify as `PARTIALLY SPECIFICATION-BACKED / INPUT ROBUSTNESS`; (2) describe `"not-an-id"` as a malformed/unsupported identifier probe rather than asserting violation of an explicitly documented numeric-ID constraint; (3) require only that the request must not cause unintended mutation of an existing order; (4) do not require exact HTTP 400 or 404 unless supported by authoritative API documentation; (5) if the SUT handles the value differently but safely, record actual behavior without automatically filing a normative FR-10 bug.
- **Executable After Correction:** YES.

### FR10-AI-041 – VERDICT: VALID
- **Human Reasoning:** This case is distinct from `FR10-AI-001`. `FR10-AI-001` primarily verifies that the transition `pending` $\rightarrow$ `confirmed` is permitted. `FR10-AI-041` primarily verifies consistency between: (1) the mutation response; (2) the externally observable persisted order state after the mutation. The documented GET order endpoint provides a valid API-level persistence oracle. Only response fields explicitly guaranteed by the API contract may be asserted.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

### FR10-AI-042 – VERDICT: VALID
- **Human Reasoning:** The case is explicitly scoped as `SEC-05 / PARTIAL BLACK-BOX BEHAVIORAL EVIDENCE` and therefore does not overclaim that black-box testing proves SQL parameterization. The valid behavioral invariants are limited to: (1) the injection-style path value must not cause unauthorized/unintended order selection or mutation; (2) the test records observable handling of the payload; (3) no conclusion is drawn that parameterized SQL has been proven internally. A particular HTTP status code is not required. An HTTP 500 alone must not be treated as proof of SQL injection success or proof that SEC-05 is violated.
- **Required Correction:** NONE.
- **Executable After Correction:** YES.

---

## 7. Final Human Audit Summary

- **Total Raw AI-Generated Test Cases:** `42`
- **Human-Audited:** `42 / 42`
- **VALID:** `38`
- **INVALID:** `1` (`FR10-AI-012`)
- **INCOMPLETE:** `3` (`FR10-AI-033`, `FR10-AI-034`, `FR10-AI-040`)
- **Usable AI Cases As-Is:** `38`
- **Usable AI-Derived Cases After Human Corrections:** `41`
- **Rejected from Executable Suite:** `FR10-AI-012`
- **Corrected Executable Derivatives:** `FR10-AI-033`, `FR10-AI-034`, `FR10-AI-040`
- **HW06 Requirement Gate:** The assignment threshold of $\ge 35$ usable AI-derived FR-10 test cases is **SATISFIED** (41 usable test cases).
- **Human Audit Status:** **COMPLETE**
- **Raw AI Draft Integrity:** `23127259/testcases/FR10_AI_DRAFT.md` remains completely unaltered and frozen.
