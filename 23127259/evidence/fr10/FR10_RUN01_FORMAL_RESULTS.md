# FR-10 Newman Run 01 Formal Reconciliation Report (Corrected)

> **RUN 01 DERIVED ANALYSIS CORRECTED AFTER HUMAN REVIEW**
> Reason: Formal precondition establishment is mandatory before awarding PASS or classifying exploratory observations. Because Folder 00 authentication helpers targeted `/api/auth/login` (HTTP 404), zero order fixture preconditions were established.

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature Under Test:** FR-10 – Order Status & State Machine (Pool B)
- **Execution Run:** Run 01 (Controlled Baseline Execution)
- **Execution Status:** **`HARNESS_REPAIR_REQUIRED`** (Authentication route mismatch prevented token propagation)

---

## 1. Raw Execution Evidence Hashes (Verified Immutable)

| Artifact | File Path | SHA-256 Checksum |
|---|---|---|
| **CLI Output Log** | [`23127259/evidence/fr10/newman/FR10-run01-cli.txt`](newman/FR10-run01-cli.txt) | `368d24e3ff788f4e0b07d9b1df542554be786098154f9abe0b8ab222cad8a25f` |
| **JSON Execution Data** | [`23127259/evidence/fr10/newman/FR10-run01.json`](newman/FR10-run01.json) | `d893515103fffbcc5cd4e8ad31981464893f42c43ceb07a0c6daff1760969d67` |
| **HTML Interactive Report** | [`23127259/evidence/fr10/newman/FR10-run01.html`](newman/FR10-run01.html) | `569c8c2e0111075fb82dc10e1fb553be9e45bee0a04d78d586544b08c40ec6a4` |

---

## 2. Formal Case Summary

- **Total Formal Test Cases:** `46` (41 AI-Derived + 5 Human Extensions; raw SHA-256 `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` immutable; AI-012 excluded)
- **`PASS`:** `0`
- **`BLOCKED – HARNESS/SETUP`:** `46`
- **`FAIL – EXPECTED ORACLE VIOLATION`:** `0`
- **`EXPLORATORY OBSERVATION`:** `0`

---

## 3. Formal Test Case Results Matrix

| Formal ID | Provenance | Precondition Established | Formal Verdict | Failed Assertions | Notes |
|---|---|:---:|---|:---:|---|
| `FR10-AI-001` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-002` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-003` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-004` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-005` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-006` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-007` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-008` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-009` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-010` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-011` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-013` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-014` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-015` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-016` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-017` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-018` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-019` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-020` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-021` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-022` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-023` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-024` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-025` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); precondition unestablished (reclassified from accidental PASS) |
| `FR10-AI-026` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-027` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-028` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); precondition unestablished (reclassified from accidental PASS) |
| `FR10-AI-029` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-030` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-031` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-032` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-033` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-034` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-035` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-036` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-037` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-038` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-039` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-040` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-041` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-AI-042` | AI-Derived | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-HUM-001` | Human Extension | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-HUM-002` | Human Extension | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-HUM-003` | Human Extension | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401 (empty token); required order fixture unestablished |
| `FR10-HUM-004` | Human Extension | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401; required confirmed/pending initial fixture unestablished |
| `FR10-HUM-005` | Human Extension | NO | `BLOCKED – HARNESS/SETUP` | 1 | BLOCKED: Dedicated checkout fixture received 401; required confirmed/pending initial fixture unestablished |
