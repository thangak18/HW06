# FR-10 Run02 Reconciled Formal Results

- **Phase:** 2D.1D.1 – Post Semantic Traceability Audit
- **Interaction:** INT-046
- **Date:** 2026-09-01
- **Basis:** FR10_RUN02_SEMANTIC_TRACEABILITY_AUDIT.md

> CORRECTED AFTER SEMANTIC TRACEABILITY AUDIT

---

## Key Correction: Newman Exit Code

- **Shell pipeline exit code:** `0` (the exit code of `tee`, not Newman)
- **Newman process exit code:** `NOT RELIABLY CAPTURED` (no `set -o pipefail` or `${PIPESTATUS[0]}`)
- **Run02 JSON confirms:** 11 failed assertions → Newman would ordinarily exit non-zero
- **Future Run03 must use:** `set -o pipefail` or capture `${PIPESTATUS[0]}`

---

## Key Correction: pm.sendRequest Execution Artifact

The Newman execution log shows GET entries attributed to ACTION items that were PUT requests. This is because `pm.sendRequest` callbacks inside test scripts appear as additional execution entries under the parent item name. The PUT requests DID execute; `pm.response` assertions captured the correct PUT response codes. This is a **reporting artifact only** — not an execution defect.

---

## Reconciled Formal Accounting

| Classification | Count |
|---|---:|
| **Trustworthy PASS** | **37** |
| **Trustworthy normative FAIL** | **7** |
| **Partial-Oracle Observation** | **0** |
| **Exploratory Observation** | **2** |
| **Invalidated – Collection Semantic Drift** | **0** |
| **Blocked – Harness** | **0** |
| **TOTAL** | **46** |

---

## Per-Case Reconciled Results

| Formal ID | Semantic Match | Run02 Trustworthy? | Correct Classification | Confirmation Allowed? | Reason |
|---|:---:|:---:|---|:---:|---|
| FR10-AI-001 | EXACT | YES | **PASS** | YES | Admin pending->confirmed via admin/status; state verified |
| FR10-AI-002 | EXACT | YES | **PASS** | YES | Admin confirmed->shipping; state verified |
| FR10-AI-003 | EXACT | YES | **PASS** | YES | Admin shipping->delivered; state verified |
| FR10-AI-004 | EXACT | YES | **PASS** | YES | Full lifecycle; all states verified |
| FR10-AI-005 | EXACT | YES | **PASS** | YES | Owner cancel pending via /api/orders/:id/cancel |
| FR10-AI-006 | EXACT | YES | **PASS** | YES | Owner cancel confirmed via cancel endpoint |
| FR10-AI-007 | EXACT | YES | **PASS** | YES | Admin cancel pending via admin/status |
| FR10-AI-008 | EXACT | YES | **PASS** | YES | Admin cancel confirmed via admin/status |
| FR10-AI-009 | EXACT | YES | **PASS** | YES | Invalid skip pending->shipping rejected |
| FR10-AI-010 | EXACT | YES | **PASS** | YES | Invalid skip pending->delivered rejected |
| FR10-AI-011 | EXACT | YES | **PASS** | YES | Invalid skip confirmed->delivered rejected |
| FR10-AI-013 | EXACT | YES | **PASS** | YES | Backward delivered->confirmed rejected |
| FR10-AI-014 | EXACT | YES | **PASS** | YES | Backward confirmed->pending rejected |
| FR10-AI-015 | EXACT | YES | **PASS** | YES | Backward shipping->confirmed rejected |
| FR10-AI-016 | EXACT | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-FR10-FSM-01) | PUT /api/orders/:id/cancel on shipping: HTTP 200; state=canceled (expected 4xx, shipping) |
| FR10-AI-017 | EXACT | YES | **PASS** | YES | canceled->confirmed rejected; terminal immutable |
| FR10-AI-018 | EXACT | YES | **PASS** | YES | canceled->shipping rejected |
| FR10-AI-019 | EXACT | YES | **PASS** | YES | canceled->delivered rejected |
| FR10-AI-020 | EXACT | YES | **PASS** | YES | delivered->shipping rejected; terminal immutable |
| FR10-AI-021 | EXACT | YES | **PASS** | YES | delivered->canceled rejected |
| FR10-AI-022 | EXACT | YES | **PASS** | YES | delivered->pending rejected |
| FR10-AI-023 | EXACT | YES | **PASS** | YES | delivered->confirmed rejected |
| FR10-AI-024 | EXACT | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-FR10-FSM-02) | PUT /api/admin/orders/:id/status canceled->delivered: HTTP 200; state=delivered |
| FR10-AI-025 | EXACT | YES | **PASS** | YES | No auth on admin status: HTTP 401 ✅ |
| FR10-AI-026 | EXACT | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-SEC02-01) | Malformed bearer: HTTP 403 (spec requires 401) |
| FR10-AI-027 | EXACT | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-SEC02-01) | Bad signature JWT: HTTP 403 (spec requires 401) |
| FR10-AI-028 | EXACT | YES | **PASS** | YES | No auth on cancel: HTTP 401 ✅ |
| FR10-AI-029 | EXACT | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-SEC02-01) | Malformed bearer on cancel: HTTP 403 (spec requires 401) |
| FR10-AI-030 | EXACT | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-SEC03-01) | role=user token on admin route: HTTP 200; state mutated |
| FR10-AI-031 | EXACT | YES | **PASS** | YES | Admin token on cancel: correctly rejected (403/401/404) |
| FR10-AI-032 | EXACT | YES | **PASS** | YES | Guest on admin status: correctly rejected (403/401/404) |
| FR10-AI-033 | EXACT | YES | **PASS** | YES | User B cancel User A pending: rejected (partial oracle) |
| FR10-AI-034 | EXACT | YES | **PASS** | YES | User B cancel User A confirmed: rejected (partial oracle) |
| FR10-AI-035 | EXACT | YES | **PASS** | YES | Input "processing": rejected 4xx |
| FR10-AI-036 | EXACT | YES | **PASS** | YES | Input {}: rejected 4xx |
| FR10-AI-037 | EXACT | YES | **PASS** | YES | Input null status: rejected 4xx |
| FR10-AI-038 | EXACT | YES | **PASS** | YES | Input numeric 123: rejected 4xx |
| FR10-AI-039 | EXACT | YES | **PASS** | YES | Non-existent ID 999999: HTTP 404 |
| FR10-AI-040 | EXACT | YES | **PASS** | YES | Malformed ID not-an-id: HTTP 404 (safe rejection) |
| FR10-AI-041 | EXACT | YES | **PASS** | YES | Mutation+GET consistency oracle: PASS |
| FR10-AI-042 | EXACT | YES | **PASS** | YES | SEC-05 black-box: safe rejection (HTTP 404) |
| FR10-HUM-001 | EXACT | YES | **PASS** | YES | Illegal skip rejected; lifecycle continuity maintained |
| FR10-HUM-002 | EXACT | YES | **PASS** | YES | Entity isolation: A=confirmed, B=pending |
| FR10-HUM-003 | EXACT | YES | **FAIL – NORMATIVE ORACLE VIOLATION** | YES (CANDIDATE-FR10-FSM-01) | PUT /api/orders/:id/cancel during shipping: HTTP 200; state=canceled |
| FR10-HUM-004 | EXACT | YES | **EXPLORATORY OBSERVATION** | N/A | confirmed->confirmed: HTTP 400 (safe rejection); state stable |
| FR10-HUM-005 | EXACT | YES | **EXPLORATORY OBSERVATION** | N/A | text/plain Content-Type: HTTP 500; state not corrupted |

---

## Candidate Cluster Re-Evaluation

| Candidate | Decision | Reason |
|---|---|---|
| **CANDIDATE-FR10-FSM-01** | **RETAIN FOR CONFIRMATION** | AI-016, HUM-003: both TRUSTWORTHY. PUT /api/orders/:id/cancel during shipping accepted. Frozen rule prohibits. |
| **CANDIDATE-FR10-FSM-02** | **RETAIN FOR CONFIRMATION** | AI-024: TRUSTWORTHY. PUT /api/admin/orders/:id/status canceled->delivered accepted. Terminal state not immutable. |
| **CANDIDATE-SEC02-01** | **RETAIN FOR CONFIRMATION** | AI-026, AI-027, AI-029: TRUSTWORTHY. Spec explicitly requires 401. SUT returns 403. Real normative discrepancy. |
| **CANDIDATE-SEC03-01** | **RETAIN FOR CONFIRMATION** | AI-030: TRUSTWORTHY. role=user token accepted on Admin route. State mutated. AI-031, AI-032 are PASS (different actors/routes correctly rejected). |

---

## Evidence Hash Verification

| File | SHA-256 | Status |
|---|---|:---:|
| FR10-run02-cli.txt | `86f7c2e8f9b2b8f3822c43eceb23e47d7948fcddece0574c6a3907d18d59ffb9` | **UNCHANGED** |
| FR10-run02.json | `b3395b7c8968d8eb576fc9adf5dce64106891b41728b8afa10a402036de1b5dd` | **UNCHANGED** |
| FR10-run02.html | `83e422acc86ceeb19fa5008c1680b05b541d4022aab19fc10d64b609780da65b` | **UNCHANGED** |
