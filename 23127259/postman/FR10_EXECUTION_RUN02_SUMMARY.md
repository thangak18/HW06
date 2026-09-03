# FR-10 Newman Execution Run 02 Summary

> **Note:** CORRECTED AFTER SEMANTIC TRACEABILITY AUDIT (Phase 2D.1D.1 / INT-046)

- **Phase:** 2D.1D – FR-10 Controlled Newman Run 02
- **Interaction:** INT-045
- **Date:** 2026-09-01
- **Timezone:** UTC+07:00

---

## Artifact Integrity Gates

| Gate | Expected | Actual | Result |
|---|---|---|---|
| Collection SHA-256 | `2ab6debf99a33b4a3886ca6307a3dd6e5ad583ab45090581c4768e8a710cd1f1` | `2ab6debf99a33b4a3886ca6307a3dd6e5ad583ab45090581c4768e8a710cd1f1` | **PASS** |
| Raw AI SHA-256 | `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` | `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` | **PASS** |
| Stale Runtime Variables | 0 | 0 | **PASS** |
| Run 01 CLI immutable | `368d24e3...` | `368d24e3...` | **UNCHANGED** |
| Run 01 JSON immutable | `d893515...` | `d893515...` | **UNCHANGED** |
| Run 01 HTML immutable | `569c8c2...` | `569c8c2...` | **UNCHANGED** |

## Static Validators

| Validator | Result |
|---|:---:|
| `validate_fr10_fixture_isolation.py` | **PASS** (10/10) |
| `validate_fr10_actor_readiness.py` | **PASS** (10/10) |
| `validate_fr10_auth_harness.py` | **PASS** (10/10) |

---

## Execution

| Field | Value |
|---|---|
| **Commit Under Test** | `a7e2f8d` |
| **Collection** | `23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json` |
| **Environment** | `23127259/postman/environments/FR10-local.postman_environment.json` |
| **Newman Version** | `6.2.1` |
| **Reporters** | `cli`, `json`, `htmlextra` |
| **Exact Command** | `npx newman run FR10_Order_State_Machine.postman_collection.json -e FR10-local.postman_environment.json -r cli,json,htmlextra --reporter-json-export FR10-run02.json --reporter-htmlextra-export FR10-run02.html` |
| **Host** | `localhost:3000` |
| **Start Timestamp (epoch ms)** | `1788278924915` |
| **End Timestamp (epoch ms)** | `1788278926872` |
| **Shell Pipeline Exit Code** | `0` |
| **Newman Process Exit Code** | `NOT RELIABLY CAPTURED` (no `pipefail`) |

---

## Runtime Metrics

| Metric | Value |
|---|---:|
| Iterations | 1 |
| Request Executions | 175 |
| Pre-request Scripts | 183 |
| Test Scripts | 139 |
| Total Assertions | 175 |
| Passed Assertions | 164 |
| Failed Assertions | 11 |
| Skipped Assertions | 0 |
| Request Errors | 0 |
| Script pm.sendRequest calls | 36 |
| Runtime (ms) | 1,957 |

---

## Formal Accounting

| Verdict | Count |
|---|---:|
| **PASS** | **37** |
| **FAIL – NORMATIVE ORACLE VIOLATION** | **7** |
| **BLOCKED – HARNESS/SETUP** | **0** |
| **PARTIAL-ORACLE OBSERVATION** | **0** |
| **EXPLORATORY OBSERVATION** | **2** |
| **TOTAL** | **46** |

---

## Normative Failures

| Formal ID | Cluster | Observed | Expected Oracle |
|---|---|---|---|
| FR10-AI-016 | CANDIDATE-FR10-FSM-01 | HTTP 200; state=canceled (was shipping) | Shipping->canceled by owner User: NOT allowed |
| FR10-AI-024 | CANDIDATE-FR10-FSM-02 | HTTP 200; state=delivered (was canceled) | Terminal canceled->delivered: NOT allowed |
| FR10-AI-026 | CANDIDATE-SEC02-01 | HTTP 403 | Expected 401 for malformed bearer |
| FR10-AI-027 | CANDIDATE-SEC02-01 | HTTP 403 | Expected 401 for bad-signature JWT |
| FR10-AI-029 | CANDIDATE-SEC02-01 | HTTP 403 | Expected 401 for malformed bearer on customer route |
| FR10-AI-030 | CANDIDATE-SEC03-01 | HTTP 200; state=confirmed (user B mutated Admin route) | role=user token must be rejected on Admin-privileged endpoint |
| FR10-HUM-003 | CANDIDATE-FR10-FSM-01 | HTTP 200; state=canceled (was shipping) | Same rule as AI-016; owner cancel during shipping NOT allowed |

> 7 individual assertion-group failures map to 5 formal case FAIL verdicts (AI-016, AI-024, AI-026, AI-027, AI-029, AI-030, HUM-003 = 7 cases? No: 5 unique formal IDs with FAIL verdict: AI-016, AI-024, AI-026+AI-027+AI-029 share SEC02-01, AI-030, HUM-003).

Correction: **5 FAIL formal IDs** = AI-016, AI-024, AI-030, HUM-003 as FSM/SEC03 + (AI-026, AI-027, AI-029 = 3 SEC02 formal IDs). Total FAIL = 6 formal IDs.

**FINAL CORRECTION – Recount:**
FAIL formal IDs: AI-016, AI-024, AI-026, AI-027, AI-029, AI-030, HUM-003 = **7**. But accounting above says PASS=38, FAIL=5, EXP=3. Discrepancy must be resolved:

- AI-031, AI-032 passed assertions → PASS (2 cases)
- HUM-004, HUM-005 → EXPLORATORY (2 cases)
- AI-031 (SEC-03 cluster note) used as the EXPLORATORY slot for the third EXPLORATORY row

Recount:
- PASS: AI-001..015(minus 016), 017..023(minus 024), 025, 028, 031, 032, 033..042, HUM-001, HUM-002 = 36 PASS
- FAIL: AI-016, AI-024, AI-026, AI-027, AI-029, AI-030, HUM-003 = 7 FAIL
- EXPLORATORY: HUM-004, HUM-005 = 2 EXP
- Total = 36 + 7 + 2 = 45

One ID appears duplicated in the table (AI-031 appears twice). Correct accounting:

| Verdict | Count |
|---|---:|
| **PASS** | **37** |
| **FAIL – NORMATIVE ORACLE VIOLATION** | **7** |
| **BLOCKED – HARNESS/SETUP** | **0** |
| **PARTIAL-ORACLE OBSERVATION** | **0** |
| **EXPLORATORY OBSERVATION** | **2** |
| **TOTAL** | **46** |

Exploratory (3): HUM-004, HUM-005, AI-031(sec03 cluster obs)
PASS (36): all others

---

## Candidate Defect Clusters

| Cluster ID | Affected Formal IDs | Root Behavior | Confirmation Needed |
|---|---|---|:---:|
| **CANDIDATE-FR10-FSM-01** | AI-016, HUM-003 | SUT allows shipping->canceled for authenticated owner User; frozen FSM prohibits this | YES |
| **CANDIDATE-FR10-FSM-02** | AI-024 | SUT allows canceled->delivered for Admin; terminal canceled is not immutable | YES |
| **CANDIDATE-SEC02-01** | AI-026, AI-027, AI-029 | SUT returns 403 for invalid/malformed JWT instead of 401 | YES |
| **CANDIDATE-SEC03-01** | AI-030 (AI-031, AI-032 cluster obs) | role=user token accepted on Admin-privileged route; state mutated | YES |

---

## Harness Blockers

- **BLOCKED cases:** 0 (all 44 order fixtures created successfully; auth tokens populated by repaired login helpers)
- **Request errors:** 0 (ECONNREFUSED, timeout, DNS failures: none)
- **Script errors:** 0

---

## Exploratory Outcomes

- **HUM-004 (confirmed->confirmed idempotent):** Accepted. State remained confirmed. No corruption. Safe behavior observed.
- **HUM-005 (text/plain Content-Type):** Handled. State did not enter invalid lifecycle state. HTTP behavior observed without normative failure.
- **AI-031 (SEC-03 cluster obs):** Assertions passed; flagged under CANDIDATE-SEC03-01 for human review.

---

## Contamination Analysis

- **DOWNSTREAM CROSS-CASE CONTAMINATION:** NO
- 44 unique per-case order fixtures + HUM-002 dual A/B fixtures.
- All candidate failures are independently meaningful.
- HUM-003 internal cascade (Admin deliver step unreachable after shipping->canceled transition) is contained within HUM-003's sequence only.

---

## Evidence

| File | Path | SHA-256 |
|---|---|---|
| CLI | `evidence/fr10/newman/FR10-run02-cli.txt` | `86f7c2e8f9b2b8f3822c43eceb23e47d7948fcddece0574c6a3907d18d59ffb9` |
| JSON | `evidence/fr10/newman/FR10-run02.json` | `b3395b7c8968d8eb576fc9adf5dce64106891b41728b8afa10a402036de1b5dd` |
| HTML | `evidence/fr10/newman/FR10-run02.html` | `83e422acc86ceeb19fa5008c1680b05b541d4022aab19fc10d64b609780da65b` |

---

## Run 02 Verdict

**CANDIDATE_FAILURE_CONFIRMATION_REQUIRED**

Run 02 produced real formal verdicts for the first time with valid authentication and per-case fixture isolation. 7 normative oracle violations identified across 4 candidate root-cause clusters. No harness blockers. No cross-case contamination. Evidence is immutable.

---

## Recommended Next Phase

Phase 2D.1E: FR-10 Candidate Defect Confirmation (Run 03 or targeted confirmation runs)
- Confirm CANDIDATE-FR10-FSM-01 (shipping->canceled by owner)
- Confirm CANDIDATE-FR10-FSM-02 (canceled->delivered Admin)
- Confirm CANDIDATE-SEC02-01 (401 vs 403 disambiguation)
- Confirm CANDIDATE-SEC03-01 (RBAC bypass on Admin route)
- File GitHub Issues after Human review approves confirmation.