# FR-10 Controlled Canonical Newman Run 03 Summary

- **Phase:** 2D.1D.4 – Controlled Canonical Newman Run 03
- **Commit Under Test:** `609005e`
- **Execution Date:** 2026-09-02
- **Host Deployment:** `http://localhost:3000` (Student ID: `23127259`)
- **Newman Version:** `6.2.2`
- **Shell Invocation Strategy:** `bash -o pipefail -c '...'`
- **Newman / Pipeline Exit Code:** `1` (12 assertion failures across 6 normative violation cases)

---

## 1. Frozen Artifact Integrity

| Artifact | File Path | Expected SHA-256 | Actual SHA-256 | Status |
|---|---|---|---|:---:|
| **Collection** | `postman/collections/FR10_Order_State_Machine.postman_collection.json` | `48b760d071a1b1080c2071ca56b26938763a30b9a35cd4c867a7fc5641467c89` | `48b760d071a1b1080c2071ca56b26938763a30b9a35cd4c867a7fc5641467c89` | **MATCH (PASS)** |
| **Environment** | `postman/environments/FR10-local.postman_environment.json` | `6cde9f7cbaf49176d8f6a3236f38e7ea52017025951de5dfac3a786ab90904b1` | `6cde9f7cbaf49176d8f6a3236f38e7ea52017025951de5dfac3a786ab90904b1` | **MATCH (PASS)** |
| **Raw AI Draft** | `testcases/FR10_AI_DRAFT.md` | `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` | `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` | **MATCH (PASS)** |

---

## 2. Raw Evidence Hashes

| Evidence File | File Path | SHA-256 Checksum |
|---|---|---|
| **Run 03 CLI Log** | `evidence/fr10/newman/FR10-run03-cli.txt` | `313e5c275ee1776dfa543c3013dd5c8b6fee5d324a104cab457ddea40ea21175` |
| **Run 03 JSON Report** | `evidence/fr10/newman/FR10-run03.json` | `553445dd8adb86fbd2fe8cd6f8dbb1c5a21283c1944559e8c854461e815140f7` |
| **Run 03 HTML Report** | `evidence/fr10/newman/FR10-run03.html` | `b73519b7bb3fba999879fea45fd37c5fd8434cb4522c7df3b959dd432dcd1c09` |

---

## 3. Actual Runtime Metrics

- **Iterations:** 1
- **Collection Request Definitions:** 140 (3 auth helpers + 137 case steps)
- **Script-Triggered HTTP Requests (`pm.sendRequest`):** 36
- **Total Executed HTTP Requests:** 176
- **Pre-request Scripts Executed:** 140
- **Test Scripts Executed:** 140
- **Total Assertions Evaluated:** 176
- **Passed Assertions:** 164
- **Failed Assertions:** 12
- **Script Exceptions / Fatal Errors:** 0
- **Total Execution Runtime:** 2,207 ms

---

## 4. Formal Canonical Reconciliation

| Classification | Count | Description |
|---|---:|---|
| **PASS** | **38** | Test execution and authorized GET persistence check completely satisfy canonical oracles |
| **FAIL – NORMATIVE ORACLE VIOLATION** | **6** | Genuine normative product failures (`AI-016`, `AI-024`, `AI-030`, `AI-031`, `AI-032`, `HUM-003`) |
| **EXPLORATORY OBSERVATION** | **2** | Robustness probes (`HUM-004`, `HUM-005`) |
| **BLOCKED – HARNESS/SETUP** | **0** | Zero harness errors or fixture setup failures |
| **TOTAL** | **46** | Full formal canonical test suite |

---

## 5. Candidate Defect Summary

1. **`CANDIDATE-FR10-FSM-01` (Retain for Targeted Confirmation):**
   - Affected Cases: `FR10-AI-016`, `FR10-HUM-003`
   - Description: Owner customer cancellation (`PUT /api/orders/:id/cancel`) was accepted on an order in `shipping` state (HTTP 200, state mutated to `canceled`). Level 1 SRS Section 4.10 strictly prohibits cancellation during transit.
2. **`CANDIDATE-FR10-FSM-02` (Retain for Targeted Confirmation):**
   - Affected Cases: `FR10-AI-024`
   - Description: Admin status update (`PUT /api/admin/orders/:id/status` body `{"status":"delivered"}`) was accepted on an order in terminal `canceled` state (HTTP 200, state mutated to `delivered`). Terminal immutability violated.
3. **`CANDIDATE-SEC03-01` (Retain for Targeted Confirmation):**
   - Affected Cases: `FR10-AI-030`, `FR10-AI-031`, `FR10-AI-032`
   - Description: Normal customer token (`role = 'user'`) was accepted on Admin status endpoints (HTTP 200), successfully executing status transitions (`pending -> confirmed`, `pending -> canceled`, `confirmed -> shipping`). Critical RBAC vulnerability.
4. **`CANDIDATE-SEC02-01` (DROPPED):**
   - All 5 SEC-02 cases (`FR10-AI-025..029`) safely rejected unauthenticated/tampered requests with safe `4xx` status codes (`401` and `403`) and zero database mutations.

---

## 6. Run 02 vs. Run 03 Comparison

| Aspect | Run 02 (Pre-Repair) | Run 03 (Canonical Repaired) | Delta / Impact |
|---|---|---|---|
| **Traceability Baseline** | Validated against derived suite | Validated against machine-readable Level 1–4 canonical map | Resolved all historical collection drift |
| **`FR10-AI-028`** | Customer cancel without auth (Drifted) | Tampered JWT on Admin status (`PUT /api/admin/orders/:id/status`) | **PASS (HTTP 403, 0 state mutation)** |
| **`FR10-AI-029`** | Malformed bearer on customer cancel (Drifted) | Missing auth on Customer cancel (`PUT /api/orders/:id/cancel`) | **PASS (HTTP 401, 0 state mutation)** |
| **`FR10-AI-031`** | Admin token on customer cancel (Drifted) | Normal customer on Admin status cancel (`pending -> canceled`) | **FAIL (Normative RBAC bypass, HTTP 200)** |
| **`FR10-AI-032`** | Guest token on Admin status (Drifted) | Normal customer on Admin status shipping (`confirmed -> shipping`) | **FAIL (Normative RBAC bypass, HTTP 200)** |
| **SEC-02 Oracle** | Strict 401 assertion (False defect candidate) | Semantic 4xx rejection + unchanged state | Dropped `CANDIDATE-SEC02-01` cleanly |
| **SEC-03 Coverage** | Single failing case (`AI-030`) | Triple confirmed failure across all Admin mutation routes (`AI-030`, `AI-031`, `AI-032`) | Robust proof of complete RBAC bypass |
| **Exit Code Capture** | Exit Code 0 (Masked by pipe) | Exit Code 1 (Captured via `pipefail`) | Accurate CI/CD status reporting |

---

## 7. Downstream Contamination Analysis

- **Per-Case Fixture Isolation:** 100% verified. Each formal case created its own unique checkout order into dedicated environment variables (`order_FR10_*`).
- **Downstream Cross-Case Contamination:** **NO**. Failures in `AI-016`, `AI-024`, `AI-030`, `AI-031`, `AI-032`, and `HUM-003` had zero impact on any other test case execution.
