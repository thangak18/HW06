# FR-10 Newman Run 01 Formal Reconciliation Report

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature Under Test:** FR-10 – Order Status & State Machine (Pool B)
- **Execution Run:** Run 01 (Controlled Baseline Execution)
- **Execution Status:** **`HARNESS_REPAIR_REQUIRED`** (Folder 00 login route prefix `/api/auth/login` returned 404, preventing runtime token propagation)

---

## 1. Raw Execution Evidence Hashes

| Artifact | File Path | SHA-256 Checksum |
|---|---|---|
| **CLI Output Log** | [`23127259/evidence/fr10/newman/FR10-run01-cli.txt`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01-cli.txt) | `368d24e3ff788f4e0b07d9b1df542554be786098154f9abe0b8ab222cad8a25f` |
| **JSON Execution Data** | [`23127259/evidence/fr10/newman/FR10-run01.json`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01.json) | `d893515103fffbcc5cd4e8ad31981464893f42c43ceb07a0c6daff1760969d67` |
| **HTML Interactive Report** | [`23127259/evidence/fr10/newman/FR10-run01.html`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/fr10/newman/FR10-run01.html) | `569c8c2e0111075fb82dc10e1fb553be9e45bee0a04d78d586544b08c40ec6a4` |

---

## 2. Formal Case Summary

- **Total Formal Test Cases:** `46` (41 AI-Derived + 5 Human Extensions; raw SHA-256 `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` immutable; AI-012 excluded)
- **`PASS`:** `1`
- **`BLOCKED – HARNESS/SETUP`:** `45`
- **`FAIL – EXPECTED ORACLE VIOLATION`:** `0`
- **`EXPLORATORY OBSERVATION`:** `0`

---

## 3. Formal Test Case Results Matrix

| Formal ID | Provenance | Runtime Steps | Formal Verdict | Failed Assertions | Notes |
|---|---|:---:|---|:---:|---|
| `FR10-AI-001` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-002` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-003` | AI-Derived | 5 | `BLOCKED – HARNESS/SETUP` | 4 | 4 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-004` | AI-Derived | 5 | `BLOCKED – HARNESS/SETUP` | 5 | 5 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-005` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-006` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-007` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-008` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-009` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-010` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-011` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-013` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-014` | AI-Derived | 5 | `BLOCKED – HARNESS/SETUP` | 4 | 4 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-015` | AI-Derived | 5 | `BLOCKED – HARNESS/SETUP` | 4 | 4 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-016` | AI-Derived | 5 | `BLOCKED – HARNESS/SETUP` | 4 | 4 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-017` | AI-Derived | 6 | `BLOCKED – HARNESS/SETUP` | 5 | 5 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-018` | AI-Derived | 6 | `BLOCKED – HARNESS/SETUP` | 5 | 5 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-019` | AI-Derived | 6 | `BLOCKED – HARNESS/SETUP` | 5 | 5 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-020` | AI-Derived | 6 | `BLOCKED – HARNESS/SETUP` | 5 | 5 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-021` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-022` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-023` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-024` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-025` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 1 | 1 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-026` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-027` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-028` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 1 | 1 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-029` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-030` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 1 | 1 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-031` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 1 | 1 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-032` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 1 | 1 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-033` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 1 | 1 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-034` | AI-Derived | 4 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-035` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-036` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-037` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-038` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-039` | AI-Derived | 1 | `BLOCKED – HARNESS/SETUP` | 1 | 1 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-040` | AI-Derived | 1 | `PASS` | 0 | Clean Execution |
| `FR10-AI-041` | AI-Derived | 3 | `BLOCKED – HARNESS/SETUP` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-AI-042` | AI-Derived | 1 | `BLOCKED – HARNESS/SETUP` | 1 | 1 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-HUM-001` | Human Extension | 5 | `BLOCKED – HARNESS/SETUP` | 5 | 5 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-HUM-002` | Human Extension | 5 | `BLOCKED – HARNESS/SETUP` | 5 | 5 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-HUM-003` | Human Extension | 7 | `BLOCKED – HARNESS/SETUP` | 7 | 7 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-HUM-004` | Human Extension | 3 | `EXPLORATORY OBSERVATION (BLOCKED BY SETUP)` | 3 | 3 failure(s) observed (Auth / Setup token unpopulated) |
| `FR10-HUM-005` | Human Extension | 2 | `EXPLORATORY OBSERVATION (BLOCKED BY SETUP)` | 2 | 2 failure(s) observed (Auth / Setup token unpopulated) |
