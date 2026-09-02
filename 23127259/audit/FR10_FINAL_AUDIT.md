# FR10 Final Audit

## Final Gate

**FR10_COMPLETE**

FR10 is complete after preserving immutable historical evidence, repairing a derived ID-label defect, executing canonical replacement Run04, reconciling all 46 formal IDs, and replacing final synthetic/duplicate visual evidence with authentic Postman Desktop screenshots.

## Canonical Accounting

| Metric | Verified Value |
|---|---:|
| Raw AI | 42 continuous unique IDs `FR10-AI-001..042` |
| Audited | 42 |
| VALID | 38 |
| INVALID | 1 (`FR10-AI-012`) |
| INCOMPLETE | 3 |
| Usable AI-derived | 41 |
| Human-designed | 5 |
| Formal | 46 |
| Run04 HTTP requests | 176 |
| Run04 assertions | 176 |
| Passed assertions | 164 |
| Failed assertions | 12 |
| Formal PASS | 38 |
| Normative formal FAIL | 6 |
| Exploratory observations | 2 |
| BLOCKED | 0 |
| Confirmed root-cause bugs | 3 |
| GitHub Issues | #29, #30, #31 |

## Frozen Raw Provenance

- `FR10_AI_DRAFT.md` SHA-256: `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` - exact expected match.
- The raw draft is unchanged.
- Every raw ID has one Human Audit classification.
- `FR10-AI-012` is the sole rejected case and is absent from canonical JSON, collection, and execution.

### Critical Raw-ID Verification

Direct reading of the frozen raw draft establishes:

| ID | Frozen Meaning |
|---|---|
| AI-005 | owner User cancels pending |
| AI-006 | Admin cancels pending |
| AI-007 | owner User cancels confirmed |
| AI-008 | Admin cancels confirmed |
| AI-013 | confirmed -> pending |
| AI-014 | shipping -> confirmed |
| AI-015 | shipping -> pending |
| AI-016 | owner shipping cancellation prohibited |
| AI-025 | missing auth on Admin status |
| AI-026 | malformed auth on Admin status |
| AI-027 | random/invalid JWT on Admin status |
| AI-028 | cryptographically tampered otherwise-valid Admin JWT |
| AI-029 | missing auth on User cancellation |
| AI-030 | normal User calls Admin pending -> confirmed |
| AI-031 | normal User calls Admin pending -> canceled |
| AI-032 | normal User calls Admin confirmed -> shipping |
| AI-033/034 | cross-user cancellation probes |
| AI-035..040 | `processing`, missing, null, numeric, nonexistent ID, malformed ID |
| AI-041 | mutation plus GET persistence consistency |
| AI-042 | SEC-05 black-box ID probe |

The later resume summary stated the opposite AI-006/AI-007 pairing. Under the mandated source hierarchy, the immutable raw draft prevails; the repaired artifacts use the table above.

## Derived Mapping Defect and Repair

Historical Run03 materialized AI-006 as owner-confirmed cancellation and AI-007 as Admin-pending cancellation: both behaviors executed, but the labels were swapped relative to the raw draft. Run03 was not altered.

Repaired artifacts:

- `FR10_FINAL_EXECUTABLE_SUITE.md`
- `FR10_CANONICAL_PROVENANCE_MAP.md`
- `fr10_canonical_cases.json`
- `FR10_EXECUTION_TRACEABILITY.md`
- `FR10_DERIVED_SUITE_DRIFT_AUDIT.md`
- `FR10_Order_State_Machine.postman_collection.json`
- canonical, semantic, deep, readiness, fixture, actor, auth, and tampered-JWT validators

All current validators pass; canonical collection comparison reports 46/46 exact semantic matches and zero drift.

## Historical Run03 Integrity

Run03 is preserved as immutable historical runtime evidence and is not the final canonical label reference.

| Artifact | Expected SHA-256 | Actual | Status |
|---|---|---|:---:|
| CLI | `313e5c275ee1776dfa543c3013dd5c8b6fee5d324a104cab457ddea40ea21175` | exact match | PASS |
| JSON | `553445dd8adb86fbd2fe8cd6f8dbb1c5a21283c1944559e8c854461e815140f7` | exact match | PASS |
| HTML | `b73519b7bb3fba999879fea45fd37c5fd8434cb4522c7df3b959dd432dcd1c09` | exact match | PASS |

Run03: 176 HTTP requests, 176 assertions, 164 passed, 12 failed, 0 request/script/harness failures, exit 1. Its AI-006/007 behavior labels are historical and superseded by Run04.

## Corrected Canonical Run04

- Collection SHA-256: `86b831fd088cebe4ac434812a2b23a301865cf0745afa55a5cee79c56bb22084`.
- Environment SHA-256: `6cde9f7cbaf49176d8f6a3236f38e7ea52017025951de5dfac3a786ab90904b1`.
- Newman exit captured from Bash `PIPESTATUS[0]`: `1`.
- Hostname: `localhost:3000`.
- 4 global helper requests + 172 formal-case operations = 176 HTTP requests.
- 176 assertions: 164 passed, 12 failed.
- 0 request failures, test-script failures, pre-request-script failures, or setup/harness failures.
- Formal reconciliation: 38 PASS, 6 normative FAIL, 2 exploratory, 0 blocked.

| Artifact | SHA-256 |
|---|---|
| `FR10-run04-cli.txt` | `482ffbc833cccf678f3a0fd87e93f6af6e19f1cd825ea2c36edbfd35389c6635` |
| `FR10-run04.json` | `de73cc49094f7bdcea1db88f3f7f9c5369f973cf227d5b4efad192f6d1f81b99` |
| `FR10-run04.html` | `52141602b2933640e49b7cde40130b4836c48e33977d26b50319975c9f855de6` |
| `FR10-run04-exitcode.txt` | `5eda2c28de329db0e296734e4d076de52ff4fb0569ab6c258d9ba7b1fd407efd` |

Because Newman serializes resolved headers, the final Run04 JSON/HTML are disclosure-controlled structural exports. A deterministic checked-in script removed only credential values; counts, cases, URLs, statuses, assertions, and failures remain unchanged. No JWT/Bearer pattern remains. Secret-bearing temporary raw files were never tracked and were deleted after verification.

## Strict Defect Evidence

| Artifact | Expected SHA-256 | Status |
|---|---|:---:|
| `FR10-bug-evidence-cli.txt` | `c85457ac825ded6a46d839140c511f88623bc0947d3bfe9f387b4f7222e1ae2d` | PASS |
| `FR10-bug-evidence.json` | `25bf0214768921d1d902093e867bcacf8504f1b0e13252769b593b5c7ec9c1d2` | PASS |
| `FR10-bug-evidence.html` | `203f06097f47fce9abcc5df77fe26933f79a159367114670c25f734f34624aa1` | PASS |

Strict evidence: 19 requests, 19 assertions, 11 passed, 8 expected product-defect failures, 0 harness failures, exit 1.

## Confirmed Bugs and Triage

| Root Cause | Formal Manifestations | Normative Basis | Issue |
|---|---|---|---|
| `BUG-FR10-001` owner can cancel shipping order | AI-016, HUM-003 | SRS FR-10 prohibits User shipping cancellation | [#29](https://github.com/thangak18/HW06/issues/29) |
| `BUG-FR10-002` canceled terminal order can become delivered | AI-024 | SRS FR-10 terminal-state immutability | [#30](https://github.com/thangak18/HW06/issues/30) |
| `BUG-FR10-003` normal User mutates via Admin route | AI-030..032 | SRS FR-12 and SEC-03 Admin-role enforcement | [#31](https://github.com/thangak18/HW06/issues/31) |

- SEC-02 403-vs-401: DROPPED; exact status is not normative.
- HUM-004: EXPLORATORY same-state observation.
- HUM-005: EXPLORATORY media-type robustness observation.

## Student Header

- Collection-level pre-request injection is fail-fast and supplies `X-Student-Id: 23127259` to every normal request.
- All 36 `pm.sendRequest` calls explicitly supply `X-Student-Id` and Authorization.
- Every one of the 176 historical Run03 serialized executions carried the student header.
- Every Run04 request visibly targeted the same local deployment; static validators confirm header coverage after repair.
- No hardcoded JWT exists in the collection or environment.

## Authentic Postman Visual Evidence

| Bug | SHA-256 | Verification |
|---|---|---|
| `BUG-FR10-001` | `139d7c19c0b935392f27006c3e4a045525e3f1b1b87fa6040322fe9154099420` | real Runner, correct failure, no JWT |
| `BUG-FR10-002` | `919825d75d8d1117bd1076457f11d1a384d652b8263143b955018b2979271180` | real Runner, correct failure, no JWT |
| `BUG-FR10-003` | `80b4a8251bd0c583e82e6ca7d835607ae0f260e52478369fbf7f6be5269a8625` | real Runner, focused role=user mutation, no JWT |

The three hashes are distinct. INT-053 and INT-054 synthetic screenshots remain quarantined under `historical-invalid/` and are excluded from final evidence.

## AI Audit

- Raw generation and Human Audit artifacts are traceable to the historical AI interactions and procedural commits.
- INT-055's exact output is backfilled.
- INT-056 was manually interrupted after producing the native screenshots; its exact final assistant response is not recoverable. The limitation is documented without inventing output. Artifact facts were independently reverified by Codex.

## Gate Result

**FR10_COMPLETE**
