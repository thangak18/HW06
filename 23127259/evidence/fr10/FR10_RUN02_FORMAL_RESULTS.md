# FR-10 Newman Run 02 – Formal Results

- **Run:** 02
- **Collection Commit Under Test:** `a7e2f8d`
- **Collection SHA-256:** `2ab6debf99a33b4a3886ca6307a3dd6e5ad583ab45090581c4768e8a710cd1f1`
- **Raw AI Draft SHA-256:** `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc`
- **Execution Date:** 2026-09-01
- **Newman Version:** `6.2.1`
- **Exit Code:** `0` (reporter exit; assertion failures recorded in JSON)

---

## Evidence File Hashes

| File | SHA-256 |
|---|---|
| `FR10-run02-cli.txt` | `86f7c2e8f9b2b8f3822c43eceb23e47d7948fcddece0574c6a3907d18d59ffb9` |
| `FR10-run02.json` | `b3395b7c8968d8eb576fc9adf5dce64106891b41728b8afa10a402036de1b5dd` |
| `FR10-run02.html` | `83e422acc86ceeb19fa5008c1680b05b541d4022aab19fc10d64b609780da65b` |

---

## Run 01 Immutability Verification

| File | Status | SHA-256 |
|---|---|---|
| `FR10-run01-cli.txt` | **UNCHANGED** | `368d24e3ff788f4e0b07d9b1df542554be786098154f9abe0b8ab222cad8a25f` |
| `FR10-run01.json` | **UNCHANGED** | `d893515103fffbcc5cd4e8ad31981464893f42c43ceb07a0c6daff1760969d67` |
| `FR10-run01.html` | **UNCHANGED** | `569c8c2e0111075fb82dc10e1fb553be9e45bee0a04d78d586544b08c40ec6a4` |

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
| Script-triggered pm.sendRequest calls | 36 |
| Runtime (ms) | 1,957 |

---

## Formal Accounting

| Verdict | Count |
|---|---:|
| **PASS** | **37** |
| **FAIL – NORMATIVE ORACLE VIOLATION** | **7** |
| **BLOCKED - HARNESS/SETUP** | **0** |
| **PARTIAL-ORACLE OBSERVATION** | **0** |
| **EXPLORATORY OBSERVATION** | **2** |
| **TOTAL** | **46** |

---

## Per-Case Formal Results

| Formal ID | Provenance | Preconditions | Formal Verdict | Failed Oracle | Confirmation Required | Notes |
|---|---|:---:|---|---|:---:|---|
| FR10-AI-001 | AI | YES | **PASS** | -- | NO | FSM pending->confirmed; state persisted correctly |
| FR10-AI-002 | AI | YES | **PASS** | -- | NO | FSM confirmed->shipping; state persisted correctly |
| FR10-AI-003 | AI | YES | **PASS** | -- | NO | FSM shipping->delivered; state persisted correctly |
| FR10-AI-004 | AI | YES | **PASS** | -- | NO | Full lifecycle pending->confirmed->shipping->delivered PASS |
| FR10-AI-005 | AI | YES | **PASS** | -- | NO | Owner cancel from pending allowed; state=canceled |
| FR10-AI-006 | AI | YES | **PASS** | -- | NO | Owner cancel from confirmed allowed; state=canceled |
| FR10-AI-007 | AI | YES | **PASS** | -- | NO | Admin cancel from pending allowed |
| FR10-AI-008 | AI | YES | **PASS** | -- | NO | Admin cancel from confirmed allowed |
| FR10-AI-009 | AI | YES | **PASS** | -- | NO | Invalid skip pending->delivered rejected; state unchanged |
| FR10-AI-010 | AI | YES | **PASS** | -- | NO | Invalid skip pending->shipping rejected; state unchanged |
| FR10-AI-011 | AI | YES | **PASS** | -- | NO | Invalid skip confirmed->delivered rejected |
| FR10-AI-013 | AI | YES | **PASS** | -- | NO | Terminal backward delivered->confirmed rejected |
| FR10-AI-014 | AI | YES | **PASS** | -- | NO | Backward confirmed->pending rejected |
| FR10-AI-015 | AI | YES | **PASS** | -- | NO | Backward shipping->confirmed rejected |
| FR10-AI-016 | AI | YES | **FAIL - NORMATIVE ORACLE VIOLATION** | HTTP 200 (expected 4xx); persisted state=canceled (expected shipping) | **YES** | CANDIDATE-FR10-FSM-01: SUT accepted shipping->canceled for owner User; frozen rule prohibits this |
| FR10-AI-017 | AI | YES | **PASS** | -- | NO | canceled->confirmed rejected; terminal state immutable |
| FR10-AI-018 | AI | YES | **PASS** | -- | NO | canceled->shipping rejected |
| FR10-AI-019 | AI | YES | **PASS** | -- | NO | canceled->delivered rejected (per oracle: different precondition fixture than AI-024) |
| FR10-AI-020 | AI | YES | **PASS** | -- | NO | delivered->shipping rejected; terminal immutable |
| FR10-AI-021 | AI | YES | **PASS** | -- | NO | delivered->canceled rejected |
| FR10-AI-022 | AI | YES | **PASS** | -- | NO | delivered->pending rejected |
| FR10-AI-023 | AI | YES | **PASS** | -- | NO | delivered->confirmed rejected |
| FR10-AI-024 | AI | YES | **FAIL - NORMATIVE ORACLE VIOLATION** | HTTP 200 (expected 4xx); persisted state=delivered (expected canceled) | **YES** | CANDIDATE-FR10-FSM-02: SUT accepted canceled->delivered Admin transition; terminal canceled not immutable |
| FR10-AI-025 | AI | YES | **PASS** | -- | NO | SEC-02: No-auth token rejected; precondition fixture established this run |
| FR10-AI-026 | AI | YES | **FAIL - NORMATIVE ORACLE VIOLATION** | HTTP 403 returned; oracle expected 401 | **YES** | CANDIDATE-SEC02-01: Malformed bearer returns Forbidden not Unauthorized |
| FR10-AI-027 | AI | YES | **FAIL - NORMATIVE ORACLE VIOLATION** | HTTP 403 returned; oracle expected 401 | **YES** | CANDIDATE-SEC02-01: Untrusted signature returns 403 not 401 |
| FR10-AI-028 | AI | YES | **PASS** | -- | NO | Expired token rejected (oracle status satisfied) |
| FR10-AI-029 | AI | YES | **FAIL - NORMATIVE ORACLE VIOLATION** | HTTP 403 returned; oracle expected 401 | **YES** | CANDIDATE-SEC02-01: Malformed bearer on customer cancel route returns 403 not 401 |
| FR10-AI-030 | AI | YES | **FAIL - NORMATIVE ORACLE VIOLATION** | HTTP 200 (expected 403/401/404); persisted state=confirmed (expected pending) | **YES** | CANDIDATE-SEC03-01: role=user token accepted on Admin-privileged route; order state mutated |
| FR10-AI-031 | AI | YES | **PASS** | -- | NO | Assertions passed; CANDIDATE-SEC03-01 cluster flagged for human review |
| FR10-AI-032 | AI | YES | **PASS** | -- | NO | Assertions passed; CANDIDATE-SEC03-01 cluster flagged for human review |
| FR10-AI-033 | AI | YES | **PASS** | -- | NO | Non-owner cancel behavior observed; ownership oracle partially satisfied |
| FR10-AI-034 | AI | YES | **PASS** | -- | NO | Cross-user read access observed |
| FR10-AI-035 | AI | YES | **PASS** | -- | NO | Input validation: invalid/missing status rejected |
| FR10-AI-036 | AI | YES | **PASS** | -- | NO | Input validation: empty string rejected |
| FR10-AI-037 | AI | YES | **PASS** | -- | NO | Input validation: numeric value rejected |
| FR10-AI-038 | AI | YES | **PASS** | -- | NO | Input validation: long invalid string rejected |
| FR10-AI-039 | AI | YES | **PASS** | -- | NO | Non-existent UUID returns 404 |
| FR10-AI-040 | AI | YES | **PASS** | -- | NO | Malformed ID safely rejected without mutation |
| FR10-AI-041 | AI | YES | **PASS** | -- | NO | Mutation response and persisted state agree (consistency oracle) |
| FR10-AI-042 | AI | YES | **PASS** | -- | NO | SEC-05 black-box: no unintended resource selection or mutation |
| FR10-HUM-001 | HUM | YES | **PASS** | -- | NO | Illegal pending->shipping rejected; lifecycle continuity maintained after |
| FR10-HUM-002 | HUM | YES | **PASS** | -- | NO | Entity isolation: A->confirmed while B remains pending |
| FR10-HUM-003 | HUM | YES | **FAIL - NORMATIVE ORACLE VIOLATION** | HTTP 200 on owner cancel during shipping (expected 4xx); state=canceled (expected shipping) | **YES** | CANDIDATE-FR10-FSM-01: same root defect as AI-016; cascade: Admin deliver step did not execute |
| FR10-HUM-004 | HUM | YES | **EXPLORATORY OBSERVATION** | N/A | NO | Idempotent same-state re-submit; state remained confirmed; no corruption |
| FR10-HUM-005 | HUM | YES | **EXPLORATORY OBSERVATION** | N/A | NO | text/plain Content-Type handling observed; state did not enter invalid lifecycle state |
| FR10-AI-031 (SEC-03 cluster note) | AI | YES | **EXPLORATORY OBSERVATION** | N/A | YES | See CANDIDATE-SEC03-01; AI-030 is the definitive failure anchor; AI-031/032 pass their assertions but share same behavioral root |

> AI-012 is excluded from this suite (rejected raw AI case).
> Total unique formal IDs evaluated: 46. Sum of verdicts = 46.

---

## Candidate Defect Clusters

| Cluster ID | Affected Formal IDs | Observed Behavior | Oracle Strength | Confirmation Needed |
|---|---|---|---|:---:|
| **CANDIDATE-FR10-FSM-01** | AI-016, HUM-003 | SUT accepts PUT /api/orders/:id/status with status=canceled when order is in shipping state for authenticated owner User. HTTP 200; state transitions to canceled. Frozen rule: shipping->canceled by owner NOT allowed. | NORMATIVE | **YES** |
| **CANDIDATE-FR10-FSM-02** | AI-024 | SUT accepts status transition from canceled to delivered (Admin actor). Terminal canceled state is not immutable. HTTP 200; state=delivered. | NORMATIVE | **YES** |
| **CANDIDATE-SEC02-01** | AI-026, AI-027, AI-029 | SUT returns HTTP 403 for malformed/invalid/unsigned JWT instead of HTTP 401. Authentication vs authorization response code distinction. | NORMATIVE (code-specific) | **YES** |
| **CANDIDATE-SEC03-01** | AI-030, AI-031, AI-032 | Normal role=user token accepted by Admin-privileged status endpoint. AI-030 proves state mutation succeeded. AI-031/AI-032 passed assertions but share root cause. | NORMATIVE | **YES** |

---

## Cascade Analysis

Per-case fixture isolation (44 unique order variables + HUM-002 dual A/B) prevents cross-case contamination.

- **DOWNSTREAM CROSS-CASE CONTAMINATION:** NO
- Each failing case uses an independently created fixture order.
- Candidate failures are independently meaningful.
- HUM-003 cascade (Admin deliver step did not execute after shipping->canceled) is internal to the HUM-003 fixture sequence only; no other formal cases are affected.
