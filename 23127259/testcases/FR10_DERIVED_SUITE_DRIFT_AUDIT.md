# FR-10 Derived Suite & Collection Semantic Drift Audit

- **Phase:** 2D.1D.2 – Canonical Provenance Reconstruction
- **Authoritative Baseline:** `testcases/FR10_CANONICAL_PROVENANCE_MAP.md` (reconstructed from Level 1 SRS + Level 2 `FR10_AI_DRAFT.md` + Level 3 Human Audit + Level 4 Human Extensions)
- **Derived Comparison Target:** `testcases/FR10_FINAL_EXECUTABLE_SUITE.md`
- **Collection Comparison Target:** `postman/collections/FR10_Order_State_Machine.postman_collection.json`

---

## 1. Executive Summary of Provenance Reconstruction

> **2026-09-02 final-audit correction:** A later comparison against the immutable raw draft found that this historical audit itself had swapped `FR10-AI-006` and `FR10-AI-007`. The canonical meanings are: AI-006 = Admin pending cancellation; AI-007 = owner User confirmed cancellation. The derived suite, canonical JSON, collection labels, and replacement Run04 were repaired. Run03 remains immutable historical evidence and exercised both behaviors under the swapped labels.

Human review of the previous semantic audit correctly identified that `FR10_FINAL_EXECUTABLE_SUITE.md` itself contained **material semantic drift** from the original frozen AI generation (`FR10_AI_DRAFT.md`) and Human Audit decision history (`FR10_HUMAN_AUDIT_CORRECTIONS.md`). 

The previous static validator (`validate_fr10_semantic_traceability.py`) passed 46/46 because its hardcoded rules were circularly derived from the drifted `FR10_FINAL_EXECUTABLE_SUITE.md`, rather than from the true Level 1–4 provenance.

This audit establishes the definitive diff between Canonical Provenance, the Derived Suite, and the Executable Collection.

---

## 2. 46-Case Drift Classification Table

| ID | Canonical Provenance Meaning | Derived Final Suite Meaning | Collection Implementation | Drift Type | Run02 Trustworthiness |
|---|---|---|---|:---:|:---:|
| **FR10-AI-001** | Admin pending -> confirmed (`/api/admin/orders/:id/status`) | Admin pending -> confirmed | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-002** | Admin confirmed -> shipping (`/api/admin/orders/:id/status`) | Admin confirmed -> shipping | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-003** | Admin shipping -> delivered (`/api/admin/orders/:id/status`) | Admin shipping -> delivered | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-004** | Full linear lifecycle (pending -> confirmed -> shipping -> delivered) | Full linear lifecycle | 3x PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-005** | Owner User cancel pending (`/api/orders/:id/cancel`) | Owner User cancel pending | PUT `/api/orders/:id/cancel` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-006** | Admin cancel pending (`/api/admin/orders/:id/status`) | Admin cancel pending | PUT `/api/admin/orders/:id/status` | NONE after Run04 repair | Run03 behavior covered under swapped label; Run04 is canonical |
| **FR10-AI-007** | Owner User cancel confirmed (`/api/orders/:id/cancel`) | Owner User cancel confirmed | PUT `/api/orders/:id/cancel` | NONE after Run04 repair | Run03 behavior covered under swapped label; Run04 is canonical |
| **FR10-AI-008** | Admin cancel confirmed (`/api/admin/orders/:id/status`) | Admin cancel confirmed | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-009** | Admin illegal skip pending -> shipping (`/api/admin/orders/:id/status`) | Admin illegal skip pending -> shipping | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-010** | Admin illegal skip pending -> delivered (`/api/admin/orders/:id/status`) | Admin illegal skip pending -> delivered | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-011** | Admin illegal skip confirmed -> delivered (`/api/admin/orders/:id/status`) | Admin illegal skip confirmed -> delivered | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-013** | Admin backward confirmed -> pending (`/api/admin/orders/:id/status`) | Admin backward confirmed -> pending | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-014** | Admin backward shipping -> confirmed (`/api/admin/orders/:id/status`) | Admin backward shipping -> confirmed | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-015** | Admin backward shipping -> pending (`/api/admin/orders/:id/status`) | Admin backward shipping -> pending | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-016** | Owner User cancel shipping (`/api/orders/:id/cancel`) -> 4xx | Owner User cancel shipping -> 4xx | PUT `/api/orders/:id/cancel` | NONE | **TRUSTWORTHY (FAIL – CANDIDATE-FR10-FSM-01)** |
| **FR10-AI-017** | Admin terminal immutability: delivered -> pending | delivered -> pending | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-018** | Admin terminal immutability: delivered -> confirmed | delivered -> confirmed | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-019** | Admin terminal immutability: delivered -> shipping | delivered -> shipping | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-020** | Admin terminal immutability: delivered -> canceled | delivered -> canceled | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-021** | Admin terminal immutability: canceled -> pending | canceled -> pending | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-022** | Admin terminal immutability: canceled -> confirmed | canceled -> confirmed | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-023** | Admin terminal immutability: canceled -> shipping | canceled -> shipping | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-024** | Admin terminal immutability: canceled -> delivered | canceled -> delivered | PUT `/api/admin/orders/:id/status` | NONE | **TRUSTWORTHY (FAIL – CANDIDATE-FR10-FSM-02)** |
| **FR10-AI-025** | Missing auth on Admin status (`/api/admin/orders/:id/status`) -> non-success | Missing auth on Admin status -> 401 | PUT `/api/admin/orders/:id/status` (no auth) | ORACLE OVER-SPECIFICATION | TRUSTWORTHY (PASS - SUT returns 401) |
| **FR10-AI-026** | Malformed auth header on Admin status -> non-success | Malformed bearer on Admin status -> 401 | PUT `/api/admin/orders/:id/status` (malformed) | ORACLE OVER-SPECIFICATION | **INVALIDATED AS DEFECT (PASS under Level 1/2 non-success oracle; SUT returns 403)** |
| **FR10-AI-027** | Invalid/garbage JWT on Admin status -> non-success | Bad signature on Admin status -> 401 | PUT `/api/admin/orders/:id/status` (bad sig) | ORACLE OVER-SPECIFICATION | **INVALIDATED AS DEFECT (PASS under Level 1/2 non-success oracle; SUT returns 403)** |
| **FR10-AI-028** | **Tampered JWT on Admin status (`PUT /api/admin/orders/:id/status`)** | **Missing auth on Customer cancel (`PUT /api/orders/:id/cancel`)** | **PUT `/api/orders/:id/cancel` (no auth)** | **AUTH CONDITION / ENDPOINT DRIFT** | **INVALIDATED BY DRIFT (Executed wrong endpoint & auth condition)** |
| **FR10-AI-029** | **Missing auth on Customer cancel (`PUT /api/orders/:id/cancel`)** | **Malformed bearer on Customer cancel (`PUT /api/orders/:id/cancel`)** | **PUT `/api/orders/:id/cancel` (malformed)** | **AUTH CONDITION DRIFT** | **INVALIDATED BY DRIFT (Executed wrong auth condition; 403 was safe rejection anyway)** |
| **FR10-AI-030** | User A (`role = 'user'`) on Admin status pending -> confirmed -> reject | User A on Admin status -> reject | PUT `/api/admin/orders/:id/status` (User A token) | NONE | **TRUSTWORTHY (FAIL – CANDIDATE-SEC03-01)** |
| **FR10-AI-031** | **User A (`role = 'user'`) on Admin status pending -> canceled -> reject** | **Admin token on Customer cancel (`PUT /api/orders/:id/cancel`)** | **PUT `/api/orders/:id/cancel` (Admin token)** | **ACTOR / ENDPOINT DRIFT** | **INVALIDATED BY DRIFT (Executed wrong actor & route)** |
| **FR10-AI-032** | **User A (`role = 'user'`) on Admin status confirmed -> shipping -> reject** | **Guest / Non-Admin token on Admin status -> reject** | **PUT `/api/admin/orders/:id/status` (guestToken)** | **ACTOR DRIFT** | **INVALIDATED BY DRIFT (Executed generic guest instead of User A role=user token)** |
| **FR10-AI-033** | User B cancels User A pending order (`/api/orders/:id/cancel`) -> reject | User B cancels User A pending order -> reject | PUT `/api/orders/:id/cancel` (User B token) | NONE | TRUSTWORTHY (PASS - partial oracle) |
| **FR10-AI-034** | User B cancels User A confirmed order (`/api/orders/:id/cancel`) -> reject | User B cancels User A confirmed order -> reject | PUT `/api/orders/:id/cancel` (User B token) | NONE | TRUSTWORTHY (PASS - partial oracle) |
| **FR10-AI-035** | Admin status = "processing" -> 4xx | Admin status = "processing" -> 4xx | PUT `/api/admin/orders/:id/status` body=processing | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-036** | Admin status missing `{}` -> 4xx | Admin status missing `{}` -> 4xx | PUT `/api/admin/orders/:id/status` body={} | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-037** | Admin status = null -> 4xx | Admin status = null -> 4xx | PUT `/api/admin/orders/:id/status` body=null | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-038** | Admin status = 123 -> 4xx | Admin status = 123 -> 4xx | PUT `/api/admin/orders/:id/status` body=123 | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-039** | Admin status on numeric non-existent ID 999999 -> 404 | Admin status on 999999 -> 404 | PUT `/api/admin/orders/999999/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-040** | Admin status on malformed non-numeric ID `not-an-id` -> non-success | Admin status on `not-an-id` -> non-success | PUT `/api/admin/orders/not-an-id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-041** | Admin valid mutation + GET consistency verification | Admin valid mutation + GET consistency | PUT + GET `/api/orders/:id` | NONE | TRUSTWORTHY (PASS) |
| **FR10-AI-042** | SEC-05 black-box SQL injection probe on ID -> 4xx / safe rejection | SEC-05 SQLi probe -> 4xx | PUT `/api/admin/orders/1' OR '1'='1/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-HUM-001** | Illegal skip rejected, valid forward accepted | Illegal skip rejected, valid forward accepted | 2x PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-HUM-002** | Multi-order state isolation (Order A confirmed, Order B pending) | Multi-order state isolation | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (PASS) |
| **FR10-HUM-003** | In-transit cancel rejected (`/api/orders/:id/cancel`), Admin delivers | In-transit cancel rejected, Admin delivers | PUT `/api/orders/:id/cancel` & Admin PUT | NONE | **TRUSTWORTHY (FAIL – CANDIDATE-FR10-FSM-01)** |
| **FR10-HUM-004** | Same-state idempotency probe (`confirmed` -> `confirmed`) | Same-state idempotency probe | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (EXPLORATORY) |
| **FR10-HUM-005** | Non-JSON `text/plain` media type probe | Non-JSON `text/plain` media type probe | PUT `/api/admin/orders/:id/status` | NONE | TRUSTWORTHY (EXPLORATORY) |

---

## 3. Key Drift Categories & Analysis

### 3.1 Material Drift Cases (AI-028, AI-029, AI-031, AI-032)
1. **FR10-AI-028:**
   - **Canonical:** Cryptographically Tampered JWT on Admin status (`PUT /api/admin/orders/:id/status` with `{"status":"confirmed"}`).
   - **Derived / Collection:** Customer cancellation without authorization (`PUT /api/orders/:id/cancel`).
   - **Verdict:** MATERIAL ENDPOINT & AUTH DRIFT.
2. **FR10-AI-029:**
   - **Canonical:** Missing Authorization on Customer cancellation (`PUT /api/orders/:id/cancel`).
   - **Derived / Collection:** Malformed bearer on Customer cancellation (`PUT /api/orders/:id/cancel`).
   - **Verdict:** MATERIAL AUTH CONDITION DRIFT.
3. **FR10-AI-031:**
   - **Canonical:** Normal Customer (`role = 'user'`) on Admin cancellation route (`PUT /api/admin/orders/:id/status` with `{"status":"canceled"}`).
   - **Derived / Collection:** Admin token on Customer cancellation endpoint (`PUT /api/orders/:id/cancel`).
   - **Verdict:** MATERIAL ACTOR & ENDPOINT DRIFT.
4. **FR10-AI-032:**
   - **Canonical:** Normal Customer (`role = 'user'`) on Admin transit dispatch route (`PUT /api/admin/orders/:id/status` with `{"status":"shipping"}`).
   - **Derived / Collection:** Generic Guest token on Admin status endpoint.
   - **Verdict:** MATERIAL ACTOR DRIFT.

### 3.2 SEC-02 Over-Specification (AI-025, AI-026, AI-027, AI-028, AI-029)
- **Canonical Requirement:** Level 1 SRS and Level 2 `FR10_AI_DRAFT.md` prescribe that unauthenticated / invalid JWT requests must result in `ERROR / NON-SUCCESS` (e.g. 401 or 400/403). They do NOT strictly mandate HTTP 401 over HTTP 403.
- **Derived Suite:** Over-specified `pm.expect(pm.response.code).to.eql(401)`.
- **Runtime Outcome:** SUT returned HTTP 403 Forbidden with zero state mutation (safe rejection).
- **Verdict:** Safe rejection. `CANDIDATE-SEC02-01` was a false defect caused by derived-oracle over-specification.

---

## 4. Circularity Analysis of Previous Semantic Validator

The previous validator (`validate_fr10_semantic_traceability.py`) passed with 0 drift because its internal expectations (`FROZEN_MAP`) were hardcoded to match the drifted `FR10_FINAL_EXECUTABLE_SUITE.md` instead of the canonical provenance. 

This confirms **VALIDATOR DESIGN CIRCULARITY**. The new validator (`validate_fr10_canonical_traceability.py`) must consume `fr10_canonical_cases.json` derived strictly from Level 1–4 provenance.
