# FR-10 Newman Run 02 – Failure Analysis

- **Run:** 02
- **Total Normative Failures:** 5
- **Failure Clusters:** 4 candidate root-cause clusters
- **Date:** 2026-09-01

---

## Case: FR10-AI-016

| Field | Value |
|---|---|
| **Formal ID** | FR10-AI-016 |
| **Fixture ID Variable** | `order_FR10_AI_016` |
| **Setup Result** | SUCCESS – order created in pending, advanced to confirmed, advanced to shipping |
| **Initial State** | `shipping` |
| **Actor** | User A (owner, `role=user`) |
| **JWT Role** | `user` |
| **Action** | PUT /api/orders/{{order_FR10_AI_016}}/status with body `{"status":"canceled"}` |
| **HTTP Status** | `200` (expected one of [400, 422, 403, 404]) |
| **Response Semantic** | Success: status accepted and applied |
| **Persisted State** | `canceled` (expected `shipping`) |
| **Expected Oracle** | Shipping->canceled by owner User: NOT allowed per frozen FSM spec |
| **Actual Behavior** | SUT accepted the cancellation and transitioned to canceled |
| **Category** | FAIL – NORMATIVE ORACLE VIOLATION |
| **Cluster** | CANDIDATE-FR10-FSM-01 |
| **Cascade Possible?** | NO – isolated fixture; no downstream cases affected |
| **Confirmation Required?** | YES |

---

## Case: FR10-AI-024

| Field | Value |
|---|---|
| **Formal ID** | FR10-AI-024 |
| **Fixture ID Variable** | `order_FR10_AI_024` |
| **Setup Result** | SUCCESS – order created in pending, then canceled via owner cancel action |
| **Initial State** | `canceled` |
| **Actor** | Admin (`role=admin`) |
| **JWT Role** | `admin` |
| **Action** | PUT /api/orders/{{order_FR10_AI_024}}/status with body `{"status":"delivered"}` |
| **HTTP Status** | `200` (expected one of [400, 422, 403, 404]) |
| **Response Semantic** | Success: status accepted and applied |
| **Persisted State** | `delivered` (expected `canceled`) |
| **Expected Oracle** | Terminal state `canceled` must be immutable – no transitions allowed |
| **Actual Behavior** | SUT accepted canceled->delivered transition for Admin |
| **Category** | FAIL – NORMATIVE ORACLE VIOLATION |
| **Cluster** | CANDIDATE-FR10-FSM-02 |
| **Cascade Possible?** | NO – isolated fixture |
| **Confirmation Required?** | YES |

---

## Case: FR10-AI-026

| Field | Value |
|---|---|
| **Formal ID** | FR10-AI-026 |
| **Fixture ID Variable** | `order_FR10_AI_026` |
| **Setup Result** | SUCCESS – order created in pending state |
| **Initial State** | `pending` |
| **Actor** | Unauthenticated (malformed Bearer token – structurally invalid JWT) |
| **JWT Role** | N/A (invalid token) |
| **Action** | PUT /api/orders/{{order_FR10_AI_026}}/status via Admin route with malformed bearer |
| **HTTP Status** | `403` (expected `401`) |
| **Response Semantic** | Forbidden |
| **Persisted State** | `pending` (unchanged – no mutation) |
| **Expected Oracle** | SEC-02: malformed/invalid token must yield HTTP 401 Unauthorized |
| **Actual Behavior** | SUT returned 403 Forbidden instead of 401 Unauthorized |
| **Category** | FAIL – NORMATIVE ORACLE VIOLATION |
| **Cluster** | CANDIDATE-SEC02-01 |
| **Cascade Possible?** | NO – no state mutation occurred |
| **Confirmation Required?** | YES |

---

## Case: FR10-AI-027

| Field | Value |
|---|---|
| **Formal ID** | FR10-AI-027 |
| **Fixture ID Variable** | `order_FR10_AI_027` |
| **Setup Result** | SUCCESS – order created in pending state |
| **Initial State** | `pending` |
| **Actor** | Unauthenticated (structurally valid JWT with untrusted/invalid signature) |
| **JWT Role** | N/A (invalid signature) |
| **Action** | PUT /api/orders/{{order_FR10_AI_027}}/status via Admin route with bad-signature JWT |
| **HTTP Status** | `403` (expected `401`) |
| **Response Semantic** | Forbidden |
| **Persisted State** | `pending` (unchanged) |
| **Expected Oracle** | SEC-02: untrusted-signature token must yield HTTP 401 Unauthorized |
| **Actual Behavior** | SUT returned 403 Forbidden instead of 401 Unauthorized |
| **Category** | FAIL – NORMATIVE ORACLE VIOLATION |
| **Cluster** | CANDIDATE-SEC02-01 |
| **Cascade Possible?** | NO |
| **Confirmation Required?** | YES |

---

## Case: FR10-AI-029

| Field | Value |
|---|---|
| **Formal ID** | FR10-AI-029 |
| **Fixture ID Variable** | `order_FR10_AI_029` |
| **Setup Result** | SUCCESS – order created in pending state |
| **Initial State** | `pending` |
| **Actor** | Unauthenticated (malformed Bearer token on customer-facing cancel route) |
| **JWT Role** | N/A (invalid token) |
| **Action** | PUT /api/orders/{{order_FR10_AI_029}}/status with malformed bearer on customer cancel endpoint |
| **HTTP Status** | `403` (expected `401`) |
| **Response Semantic** | Forbidden |
| **Persisted State** | `pending` (unchanged) |
| **Expected Oracle** | SEC-02: malformed token on customer cancel must yield 401 |
| **Actual Behavior** | SUT returned 403 Forbidden instead of 401 Unauthorized |
| **Category** | FAIL – NORMATIVE ORACLE VIOLATION |
| **Cluster** | CANDIDATE-SEC02-01 |
| **Cascade Possible?** | NO |
| **Confirmation Required?** | YES |

---

## Case: FR10-AI-030

| Field | Value |
|---|---|
| **Formal ID** | FR10-AI-030 |
| **Fixture ID Variable** | `order_FR10_AI_030` |
| **Setup Result** | SUCCESS – order created in pending state (User A fixture, User B as non-owner attacker) |
| **Initial State** | `pending` |
| **Actor** | User B (`role=user`, non-owner, {{userBToken}}) |
| **JWT Role** | `user` |
| **Action** | PUT /api/orders/{{order_FR10_AI_030}}/status via Admin-privileged status route with body `{"status":"confirmed"}` |
| **HTTP Status** | `200` (expected one of [403, 401, 404]) |
| **Response Semantic** | Success: mutation accepted |
| **Persisted State** | `confirmed` (expected `pending`) |
| **Expected Oracle** | SEC-03 RBAC: normal user token must be rejected on Admin-privileged route |
| **Actual Behavior** | SUT accepted role=user token on Admin route; order state was mutated to confirmed |
| **Category** | FAIL – NORMATIVE ORACLE VIOLATION |
| **Cluster** | CANDIDATE-SEC03-01 |
| **Cascade Possible?** | NO – isolated fixture; AI-031/032 use separate fixtures |
| **Confirmation Required?** | YES |

---

## Case: FR10-HUM-003

| Field | Value |
|---|---|
| **Formal ID** | FR10-HUM-003 |
| **Fixture ID Variable** | `order_FR10_HUM_003` |
| **Setup Result** | SUCCESS – order advanced to shipping state (pending->confirmed->shipping) |
| **Initial State** | `shipping` |
| **Actor** | User A (owner, `role=user`) |
| **JWT Role** | `user` |
| **Action** | PUT /api/orders/{{order_FR10_HUM_003}}/status with body `{"status":"canceled"}` |
| **HTTP Status** | `200` (expected one of [400, 422, 403, 404]) |
| **Response Semantic** | Success: mutation accepted |
| **Persisted State** | `canceled` (expected `shipping`) |
| **Expected Oracle** | Shipping->canceled by owner User: NOT allowed (same rule as AI-016) |
| **Actual Behavior** | SUT accepted cancellation; state transitioned to canceled |
| **Category** | FAIL – NORMATIVE ORACLE VIOLATION |
| **Cluster** | CANDIDATE-FR10-FSM-01 |
| **Cascade Possible?** | YES – within HUM-003 sequence: Admin deliver step was not reached due to wrong state |
| **Confirmation Required?** | YES |

---

## Cross-Case Contamination

- **DOWNSTREAM CROSS-CASE CONTAMINATION:** NO
- Each formal case uses an independently created fixture order variable.
- Failures above are self-contained to their respective fixture.
- HUM-003 internal cascade (Admin deliver step skipped) is contained within HUM-003's sequence.
