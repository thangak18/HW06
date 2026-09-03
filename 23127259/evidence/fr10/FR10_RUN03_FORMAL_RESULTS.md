# FR-10 Run 03 Formal Results Report

- **Phase:** 2D.1D.4 – Controlled Canonical Newman Run 03
- **Execution Date:** 2026-09-02
- **Raw Evidence CLI:** `evidence/fr10/newman/FR10-run03-cli.txt` (SHA-256: `313e5c275ee1776dfa543c3013dd5c8b6fee5d324a104cab457ddea40ea21175`)
- **Raw Evidence JSON:** `evidence/fr10/newman/FR10-run03.json` (SHA-256: `553445dd8adb86fbd2fe8cd6f8dbb1c5a21283c1944559e8c854461e815140f7`)
- **Raw Evidence HTML:** `evidence/fr10/newman/FR10-run03.html` (SHA-256: `b73519b7bb3fba999879fea45fd37c5fd8434cb4522c7df3b959dd432dcd1c09`)
- **Real Newman Exit Code:** `1` (12 assertion failures across 6 normative defect cases)

---

## 1. Canonical Accounting Summary

| Classification | Count | Description |
|---|---:|---|
| **PASS** | **38** | Test execution and persistence verification completely satisfy canonical oracles |
| **FAIL – NORMATIVE ORACLE VIOLATION** | **6** | Genuine normative violations (`AI-016`, `AI-024`, `AI-030`, `AI-031`, `AI-032`, `HUM-003`) |
| **EXPLORATORY OBSERVATION** | **2** | Robustness probes (`HUM-004`, `HUM-005`) |
| **BLOCKED – HARNESS/SETUP** | **0** | All 140 setup/action items executed without harness failure |
| **PARTIAL-ORACLE OBSERVATION** | **0** | Evaluated under specification-backed oracles |
| **TOTAL** | **46** | Full canonical executable test suite |

---

## 2. 46-Case Formal Results Table

| Formal ID | Provenance | Preconditions | Canonical Match | Runtime Steps | Formal Verdict | Failed Oracle | Confirmation Required | Notes |
|---|---|:---:|:---:|:---:|---|---|:---:|---|
| `FR10-AI-001` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Admin pending -> confirmed valid transition verified (200) |
| `FR10-AI-002` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Admin confirmed -> shipping valid transition verified (200) |
| `FR10-AI-003` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Admin shipping -> delivered valid transition verified (200) |
| `FR10-AI-004` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Linear lifecycle progression pending -> confirmed -> shipping -> delivered verified (200) |
| `FR10-AI-005` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Customer self-service cancellation on pending order verified (200) |
| `FR10-AI-006` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Customer self-service cancellation on confirmed order verified (200) |
| `FR10-AI-007` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Admin cancellation on pending order verified (200) |
| `FR10-AI-008` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Admin cancellation on confirmed order verified (200) |
| `FR10-AI-009` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Illegal forward skip pending -> shipping rejected (400) |
| `FR10-AI-010` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Illegal forward skip pending -> delivered rejected (400) |
| `FR10-AI-011` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Illegal forward skip confirmed -> delivered rejected (400) |
| `FR10-AI-013` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Illegal backward regression confirmed -> pending rejected (400) |
| `FR10-AI-014` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Illegal backward regression shipping -> confirmed rejected (400) |
| `FR10-AI-015` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Illegal backward regression shipping -> pending rejected (400) |
| `FR10-AI-016` | LEVEL 2 RAW AI | PASS | YES | 3 | **FAIL – NORMATIVE ORACLE VIOLATION** | `Status 200 != 400/422/403/404; state mutated to 'canceled'` | **YES (CANDIDATE-FR10-FSM-01)** | Owner cancellation on shipping order accepted by SUT (HTTP 200) |
| `FR10-AI-017` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Terminal immutability delivered -> pending rejected (400) |
| `FR10-AI-018` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Terminal immutability delivered -> confirmed rejected (400) |
| `FR10-AI-019` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Terminal immutability delivered -> shipping rejected (400) |
| `FR10-AI-020` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Terminal immutability delivered -> canceled rejected (400) |
| `FR10-AI-021` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Terminal immutability canceled -> pending rejected (400) |
| `FR10-AI-022` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Terminal immutability canceled -> confirmed rejected (400) |
| `FR10-AI-023` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Terminal immutability canceled -> shipping rejected (400) |
| `FR10-AI-024` | LEVEL 2 RAW AI | PASS | YES | 3 | **FAIL – NORMATIVE ORACLE VIOLATION** | `Status 200 != 400/422/403/404; state mutated to 'delivered'` | **YES (CANDIDATE-FR10-FSM-02)** | Admin mutation on terminal canceled order accepted by SUT (HTTP 200) |
| `FR10-AI-025` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Unauthenticated Admin mutation rejected (401); state remains pending |
| `FR10-AI-026` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Malformed Bearer scheme on Admin mutation rejected (403); state remains pending |
| `FR10-AI-027` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Invalid/Garbage JWT on Admin mutation rejected (403); state remains pending |
| `FR10-AI-028` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Cryptographically tampered JWT on Admin mutation rejected (403); state remains pending |
| `FR10-AI-029` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Missing authorization on customer cancel rejected (401); state remains pending |
| `FR10-AI-030` | LEVEL 2 RAW AI | PASS | YES | 3 | **FAIL – NORMATIVE ORACLE VIOLATION** | `Status 200 != 403/401/404; state mutated to 'confirmed'` | **YES (CANDIDATE-SEC03-01)** | Normal customer token accepted on Admin status confirm route (HTTP 200) |
| `FR10-AI-031` | LEVEL 2 RAW AI | PASS | YES | 3 | **FAIL – NORMATIVE ORACLE VIOLATION** | `Status 200 != 403/401/404; state mutated to 'canceled'` | **YES (CANDIDATE-SEC03-01)** | Normal customer token accepted on Admin status cancel route (HTTP 200) |
| `FR10-AI-032` | LEVEL 2 RAW AI | PASS | YES | 4 | **FAIL – NORMATIVE ORACLE VIOLATION** | `Status 200 != 403/401/404; state mutated to 'shipping'` | **YES (CANDIDATE-SEC03-01)** | Normal customer token accepted on Admin status transit route (HTTP 200) |
| `FR10-AI-033` | LEVEL 3 HUMAN AUDITED | PASS | YES | 3 | **PASS** | `None` | NO | Cross-user cancellation on pending order rejected (403/404); state remains pending |
| `FR10-AI-034` | LEVEL 3 HUMAN AUDITED | PASS | YES | 3 | **PASS** | `None` | NO | Cross-user cancellation on confirmed order rejected (403/404); state remains confirmed |
| `FR10-AI-035` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Undocumented status enum 'processing' rejected (400) |
| `FR10-AI-036` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Missing mandatory status key '{}' rejected (400) |
| `FR10-AI-037` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Explicit null status rejected (400) |
| `FR10-AI-038` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Numeric status '123' rejected (400) |
| `FR10-AI-039` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Non-existent order ID '999999' rejected (404) |
| `FR10-AI-040` | LEVEL 3 HUMAN AUDITED | PASS | YES | 3 | **PASS** | `None` | NO | Malformed non-numeric order ID 'not-an-id' rejected (404) |
| `FR10-AI-041` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | Admin mutation + authorized GET persistence consistency verified (200) |
| `FR10-AI-042` | LEVEL 2 RAW AI | PASS | YES | 3 | **PASS** | `None` | NO | SEC-05 SQLi probe safe rejection (404); no database alteration |
| `FR10-HUM-001` | LEVEL 4 HUMAN EXTENSION | PASS | YES | 3 | **PASS** | `None` | NO | Multi-stage sequence: illegal transition rejected, valid transition confirmed (200) |
| `FR10-HUM-002` | LEVEL 4 HUMAN EXTENSION | PASS | YES | 3 | **PASS** | `None` | NO | Multi-order isolation: Order A mutated, Order B remains pending (200) |
| `FR10-HUM-003` | LEVEL 4 HUMAN EXTENSION | PASS | YES | 6 | **FAIL – NORMATIVE ORACLE VIOLATION** | `Status 200 != 400/422/403/404; state mutated to 'canceled'` | **YES (CANDIDATE-FR10-FSM-01)** | Owner cancellation on shipping order accepted in multi-stage sequence |
| `FR10-HUM-004` | LEVEL 4 HUMAN EXTENSION | PASS | YES | 3 | **EXPLORATORY OBSERVATION** | `None (Exploratory)` | N/A | Exploratory: Same-state transition (confirmed->confirmed) safely rejected (400) |
| `FR10-HUM-005` | LEVEL 4 HUMAN EXTENSION | PASS | YES | 3 | **EXPLORATORY OBSERVATION** | `None (Exploratory)` | N/A | Exploratory: HTTP 500 observed on text/plain probe; order state preserved |
