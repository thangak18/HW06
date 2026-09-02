# FR10 Run04 Formal and HTTP Reconciliation

## Run Identity

- **Purpose:** canonical replacement after repairing the AI-006/AI-007 derived-label swap
- **Collection:** `FR10_Order_State_Machine`
- **Environment:** `FR10-local`
- **Target:** `http://localhost:3000`
- **Newman:** 6.2.2
- **Executed:** 2026-09-02 12:43 +0700
- **Actual Newman exit:** `1`, captured from Bash `PIPESTATUS[0]`

Historical Run03 remains unchanged. Run04 is the first runtime artifact whose formal IDs and behaviors both agree with the frozen raw draft and the corrected canonical map.

## Raw Result Totals

| Metric | Value |
|---|---:|
| Global authentication/setup helpers | 4 HTTP requests |
| Formal-case HTTP operations | 172 |
| Total HTTP requests | 176 |
| Formal IDs | 46 |
| Assertions | 176 |
| Passed assertions | 164 |
| Failed assertions | 12 |
| Request errors | 0 |
| Test-script failures | 0 |
| Pre-request-script failures | 0 |
| Harness/setup failures | 0 |
| Formal PASS | 38 |
| Normative FAIL | 6 |
| Exploratory observations | 2 |
| BLOCKED | 0 |

## One Verdict per Formal ID

`Main HTTP` is the behavior under test. `Setup` establishes isolated actors/state. `Verification` is a follow-up API-visible state check. The four global authentication/setup helpers are outside the per-formal rows.

| Formal ID | Main HTTP | Setup | Verification | Total HTTP | Final Verdict |
|---|---:|---:|---:|---:|---|
| `FR10-AI-001` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-002` | 1 | 2 | 1 | 4 | PASS |
| `FR10-AI-003` | 1 | 3 | 1 | 5 | PASS |
| `FR10-AI-004` | 3 | 1 | 1 | 5 | PASS |
| `FR10-AI-005` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-006` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-007` | 1 | 2 | 1 | 4 | PASS |
| `FR10-AI-008` | 1 | 2 | 1 | 4 | PASS |
| `FR10-AI-009` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-010` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-011` | 1 | 2 | 1 | 4 | PASS |
| `FR10-AI-013` | 1 | 2 | 1 | 4 | PASS |
| `FR10-AI-014` | 1 | 3 | 1 | 5 | PASS |
| `FR10-AI-015` | 1 | 3 | 1 | 5 | PASS |
| `FR10-AI-016` | 1 | 3 | 1 | 5 | FAIL - NORMATIVE ORACLE VIOLATION |
| `FR10-AI-017` | 1 | 4 | 1 | 6 | PASS |
| `FR10-AI-018` | 1 | 4 | 1 | 6 | PASS |
| `FR10-AI-019` | 1 | 4 | 1 | 6 | PASS |
| `FR10-AI-020` | 1 | 4 | 1 | 6 | PASS |
| `FR10-AI-021` | 1 | 2 | 1 | 4 | PASS |
| `FR10-AI-022` | 1 | 2 | 1 | 4 | PASS |
| `FR10-AI-023` | 1 | 2 | 1 | 4 | PASS |
| `FR10-AI-024` | 1 | 2 | 1 | 4 | FAIL - NORMATIVE ORACLE VIOLATION |
| `FR10-AI-025` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-026` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-027` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-028` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-029` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-030` | 1 | 1 | 1 | 3 | FAIL - NORMATIVE ORACLE VIOLATION |
| `FR10-AI-031` | 1 | 1 | 1 | 3 | FAIL - NORMATIVE ORACLE VIOLATION |
| `FR10-AI-032` | 1 | 2 | 1 | 4 | FAIL - NORMATIVE ORACLE VIOLATION |
| `FR10-AI-033` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-034` | 1 | 2 | 1 | 4 | PASS |
| `FR10-AI-035` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-036` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-037` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-038` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-039` | 1 | 0 | 0 | 1 | PASS |
| `FR10-AI-040` | 1 | 0 | 0 | 1 | PASS |
| `FR10-AI-041` | 1 | 1 | 1 | 3 | PASS |
| `FR10-AI-042` | 1 | 0 | 0 | 1 | PASS |
| `FR10-HUM-001` | 2 | 1 | 2 | 5 | PASS |
| `FR10-HUM-002` | 1 | 2 | 2 | 5 | PASS |
| `FR10-HUM-003` | 4 | 1 | 2 | 7 | FAIL - NORMATIVE ORACLE VIOLATION |
| `FR10-HUM-004` | 1 | 2 | 0 | 3 | EXPLORATORY OBSERVATION |
| `FR10-HUM-005` | 1 | 1 | 0 | 2 | EXPLORATORY OBSERVATION |

## Failure-to-Root-Cause Mapping

| Failed Formal IDs | Root Cause |
|---|---|
| `FR10-AI-016`, `FR10-HUM-003` | `BUG-FR10-001`: owner can cancel a shipping order |
| `FR10-AI-024` | `BUG-FR10-002`: canceled terminal order can transition to delivered |
| `FR10-AI-030`, `FR10-AI-031`, `FR10-AI-032` | `BUG-FR10-003`: normal User can mutate through Admin status endpoint |

- SEC-02 401-vs-403 remains dropped: Level-1 requires safe rejection, not exact 401.
- `FR10-HUM-004` records same-state behavior without a normative success/failure oracle.
- `FR10-HUM-005` records HTTP 500 for `text/plain` without promoting it to a normative defect.

## Evidence Integrity

| Artifact | SHA-256 |
|---|---|
| Collection | `86b831fd088cebe4ac434812a2b23a301865cf0745afa55a5cee79c56bb22084` |
| Environment | `6cde9f7cbaf49176d8f6a3236f38e7ea52017025951de5dfac3a786ab90904b1` |
| Run04 CLI | `482ffbc833cccf678f3a0fd87e93f6af6e19f1cd825ea2c36edbfd35389c6635` |
| Run04 JSON | `de73cc49094f7bdcea1db88f3f7f9c5369f973cf227d5b4efad192f6d1f81b99` |
| Run04 HTML | `52141602b2933640e49b7cde40130b4836c48e33977d26b50319975c9f855de6` |
| Run04 exit file | `5eda2c28de329db0e296734e4d076de52ff4fb0569ab6c258d9ba7b1fd407efd` |

Newman serializes resolved authorization headers. Run04 JSON/HTML therefore passed through the checked-in deterministic disclosure-control script before freezing. JWT/password/token values are replaced, while counts, test IDs, requests, statuses, assertions, and failures remain intact. No JWT or resolved Bearer-token pattern remains in the final Run04 artifacts. The secret-bearing raw temporary exports were deleted after verification and were never tracked.
