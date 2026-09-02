# FR-10 Run02 Canonical Reconciliation Report

- **Phase:** 2D.1D.2 – Canonical Test Provenance Reconciliation
- **Date:** 2026-09-02
- **Authoritative Baseline:** `testcases/FR10_CANONICAL_PROVENANCE_MAP.md` & `testcases/fr10_canonical_cases.json`
- **Run02 Evidence Reference:** `evidence/fr10/newman/FR10-run02.json`

---

## 1. Canonical Accounting Summary

| Classification | Count | Description |
|---|---:|---|
| **Trustworthy PASS** | **36** | Execution semantics match canonical provenance; assertions evaluate valid Level 1/2 oracles |
| **Trustworthy Normative FAIL** | **4** | Real normative failures against Level 1/2 requirements (AI-016, AI-024, AI-030, HUM-003) |
| **Exploratory Observation** | **2** | Exploratory robustness probes (HUM-004, HUM-005) |
| **Invalidated – Collection Semantic Drift** | **4** | Executed requests drifted from canonical Level 2 provenance (AI-028, AI-029, AI-031, AI-032) |
| **Blocked – Harness/Setup** | **0** | No harness blockers in Run 02 |
| **TOTAL** | **46** | Full executable suite |

---

## 2. 46-Case Canonical Reconciliation Table

| ID | Canonical Match in Run02? | Result Usable? | Canonical Verdict | Confirmation Allowed? | Canonical Reason |
|---|:---:|:---:|---|:---:|---|
| FR10-AI-001 | YES | YES | **PASS** | YES | Admin pending->confirmed valid transition verified |
| FR10-AI-002 | YES | YES | **PASS** | YES | Admin confirmed->shipping valid transition verified |
| FR10-AI-003 | YES | YES | **PASS** | YES | Admin shipping->delivered valid transition verified |
| FR10-AI-004 | YES | YES | **PASS** | YES | Linear progression pending->confirmed->shipping->delivered verified |
| FR10-AI-005 | YES | YES | **PASS** | YES | Customer self-service cancellation on pending order verified |
| FR10-AI-006 | YES | YES | **PASS** | YES | Customer self-service cancellation on confirmed order verified |
| FR10-AI-007 | YES | YES | **PASS** | YES | Admin cancellation on pending order verified |
| FR10-AI-008 | YES | YES | **PASS** | YES | Admin cancellation on confirmed order verified |
| FR10-AI-009 | YES | YES | **PASS** | YES | Illegal skip pending->shipping rejected (400) |
| FR10-AI-010 | YES | YES | **PASS** | YES | Illegal skip pending->delivered rejected (400) |
| FR10-AI-011 | YES | YES | **PASS** | YES | Illegal skip confirmed->delivered rejected (400) |
| FR10-AI-013 | YES | YES | **PASS** | YES | Backward regression delivered->confirmed rejected (400) |
| FR10-AI-014 | YES | YES | **PASS** | YES | Backward regression confirmed->pending rejected (400) |
| FR10-AI-015 | YES | YES | **PASS** | YES | Backward regression shipping->confirmed rejected (400) |
| FR10-AI-016 | YES | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-FR10-FSM-01) | Owner cancel on shipping accepted (HTTP 200, state=canceled); FSM prohibits |
| FR10-AI-017 | YES | YES | **PASS** | YES | Terminal immutability delivered->pending rejected (400) |
| FR10-AI-018 | YES | YES | **PASS** | YES | Terminal immutability delivered->confirmed rejected (400) |
| FR10-AI-019 | YES | YES | **PASS** | YES | Terminal immutability delivered->shipping rejected (400) |
| FR10-AI-020 | YES | YES | **PASS** | YES | Terminal immutability delivered->canceled rejected (400) |
| FR10-AI-021 | YES | YES | **PASS** | YES | Terminal immutability canceled->pending rejected (400) |
| FR10-AI-022 | YES | YES | **PASS** | YES | Terminal immutability canceled->confirmed rejected (400) |
| FR10-AI-023 | YES | YES | **PASS** | YES | Terminal immutability canceled->shipping rejected (400) |
| FR10-AI-024 | YES | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-FR10-FSM-02) | Admin canceled->delivered accepted (HTTP 200, state=delivered); terminal state mutated |
| FR10-AI-025 | YES | YES | **PASS** | YES | Missing auth on Admin status rejected (HTTP 401) |
| FR10-AI-026 | YES | YES | **PASS** | YES | Malformed bearer on Admin status rejected (HTTP 403; safe rejection under non-success oracle) |
| FR10-AI-027 | YES | YES | **PASS** | YES | Invalid JWT on Admin status rejected (HTTP 403; safe rejection under non-success oracle) |
| FR10-AI-028 | NO | NO | **INVALIDATED – COLLECTION SEMANTIC DRIFT** | NO (Requires Run 03 repair) | Collection executed Customer cancel without auth instead of canonical Tampered JWT on Admin status |
| FR10-AI-029 | NO | NO | **INVALIDATED – COLLECTION SEMANTIC DRIFT** | NO (Requires Run 03 repair) | Collection executed Customer cancel with malformed bearer instead of canonical Missing auth on Customer cancel |
| FR10-AI-030 | YES | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-SEC03-01) | Normal user token accepted on Admin status endpoint (HTTP 200, state=confirmed); RBAC bypass |
| FR10-AI-031 | NO | NO | **INVALIDATED – COLLECTION SEMANTIC DRIFT** | NO (Requires Run 03 repair) | Collection executed Admin token on Customer cancel instead of canonical Normal user on Admin cancel |
| FR10-AI-032 | NO | NO | **INVALIDATED – COLLECTION SEMANTIC DRIFT** | NO (Requires Run 03 repair) | Collection executed Guest token instead of canonical Normal user token on Admin shipping |
| FR10-AI-033 | YES | YES | **PASS** | YES | User B cancellation on User A pending order rejected (partial oracle) |
| FR10-AI-034 | YES | YES | **PASS** | YES | User B cancellation on User A confirmed order rejected (partial oracle) |
| FR10-AI-035 | YES | YES | **PASS** | YES | Undocumented status enum 'processing' rejected (400) |
| FR10-AI-036 | YES | YES | **PASS** | YES | Missing mandatory status key '{}' rejected (400) |
| FR10-AI-037 | YES | YES | **PASS** | YES | Explicit null status rejected (400) |
| FR10-AI-038 | YES | YES | **PASS** | YES | Numeric status '123' rejected (400) |
| FR10-AI-039 | YES | YES | **PASS** | YES | Well-formed non-existent ID 999999 rejected (404) |
| FR10-AI-040 | YES | YES | **PASS** | YES | Malformed non-numeric ID 'not-an-id' rejected safely (404) |
| FR10-AI-041 | YES | YES | **PASS** | YES | Admin mutation + GET persistence consistency verified |
| FR10-AI-042 | YES | YES | **PASS** | YES | SEC-05 SQLi probe rejected safely (404); no unintended DB side effects |
| FR10-HUM-001 | YES | YES | **PASS** | YES | Illegal skip rejected (400), valid transition accepted (200) |
| FR10-HUM-002 | YES | YES | **PASS** | YES | Order A mutated to confirmed; Order B remains pending |
| FR10-HUM-003 | YES | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-FR10-FSM-01) | Customer cancellation on shipping order accepted (HTTP 200, state=canceled) |
| FR10-HUM-004 | YES | YES | **EXPLORATORY OBSERVATION** | N/A | Same-state transition probe (confirmed->confirmed) handled safely (HTTP 400) |
| FR10-HUM-005 | YES | YES | **EXPLORATORY OBSERVATION** | N/A | Non-JSON text/plain media type handled safely (HTTP 500) |

---

## 3. Candidate Defect Re-Evaluation

| Candidate ID | Target Cases | Canonical Decision | Rationale |
|---|---|:---:|---|
| **CANDIDATE-FR10-FSM-01** | `FR10-AI-016`, `FR10-HUM-003` | **RETAIN – CANONICAL NORMATIVE FAILURE** | Level 1 SRS Section 4.10 explicitly prohibits customer cancellation once an order is in `shipping`. SUT accepted `PUT /api/orders/:id/cancel` and mutated state to `canceled` (HTTP 200). Confirmed by 2 independent test paths. |
| **CANDIDATE-FR10-FSM-02** | `FR10-AI-024` | **RETAIN – CANONICAL NORMATIVE FAILURE** | Level 1 SRS and Level 2 FSM specify that `canceled` is a terminal, immutable state. SUT accepted `PUT /api/admin/orders/:id/status` transitioning `canceled` -> `delivered` (HTTP 200). |
| **CANDIDATE-SEC02-01** | `FR10-AI-026`, `FR10-AI-027`, `FR10-AI-029` | **DROP – DERIVED ORACLE OVER-SPECIFICATION** | Level 1 SRS SEC-02 and Level 2 raw draft specify `ERROR / NON-SUCCESS` rejection (e.g. 401 or 400/403). SUT returned HTTP 403 Forbidden with zero state alteration. HTTP 403 is a compliant, safe rejection. The failure was an artifact of derived-suite over-specification. |
| **CANDIDATE-SEC03-01** | `FR10-AI-030` | **RETAIN – CANONICAL NORMATIVE FAILURE** | Level 1 SEC-03 mandates that Admin APIs verify `role = 'admin'`. SUT accepted normal customer token (`role = 'user'`) on `PUT /api/admin/orders/:id/status` and mutated state from `pending` to `confirmed` (HTTP 200). Critical RBAC bypass defect. |

---

## 4. Cases Requiring Collection Repair for Run 03

The following 4 test cases must be repaired in the Postman collection during Phase 2D.1D.3 before executing Run 03:
1. **FR10-AI-028:** Repair request to `PUT /api/admin/orders/{{order_FR10_AI_028}}/status` with tampered JWT (`{{tamperedAdminToken}}`) and payload `{"status":"confirmed"}`.
2. **FR10-AI-029:** Repair request to `PUT /api/orders/{{order_FR10_AI_029}}/cancel` with NO Authorization header and empty payload `{}`.
3. **FR10-AI-031:** Repair request to `PUT /api/admin/orders/{{order_FR10_AI_031}}/status` with User A token (`{{userAToken}}`) and payload `{"status":"canceled"}`.
4. **FR10-AI-032:** Repair request to `PUT /api/admin/orders/{{order_FR10_AI_032}}/status` with User A token (`{{userAToken}}`) and payload `{"status":"shipping"}`.
