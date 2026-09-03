# FR14 Formal Reconciliation Report — Run01

## Run Summary

| Metric | Value |
|---|---:|
| Total HTTP requests | 60 |
| Total pm.test() assertions | 70 |
| Passed assertions | 58 |
| Failed assertions | 12 |
| Request errors | 0 |
| Script errors | 0 |
| Harness errors | 0 |
| Newman exit code | 1 |

## Formal Case Verdict Assignment

Each formal ID receives exactly one final verdict.

| Formal ID | Run01 Verdict | Rationale |
|---|---|---|
| TC-FR14-001 | PASS | Public GET succeeds; array response |
| TC-FR14-002 | PASS | Admin POST succeeds with captured ID |
| TC-FR14-003 | PASS | Created category visible in GET |
| TC-FR14-004 | PASS | Admin PUT succeeds |
| TC-FR14-005 | PASS | Updated name visible in GET |
| TC-FR14-006 | PASS | Admin DELETE succeeds |
| TC-FR14-007 | PASS | Missing auth → 401 (4xx) |
| TC-FR14-008 | PASS | Missing auth → 401 (4xx) |
| TC-FR14-009 | PASS | Missing auth → 401 (4xx) |
| TC-FR14-010 | PASS | Malformed JWT → 403 (4xx) |
| TC-FR14-011 | PASS | Tampered JWT → 403 (4xx) |
| TC-FR14-012 | **FAIL** — NORMATIVE ORACLE VIOLATION | `role=user` POST returns **200** instead of rejection; SRS FR-12/SEC-03 require Admin-only mutations |
| TC-FR14-013 | **FAIL** — NORMATIVE ORACLE VIOLATION | `role=user` PUT returns **200** instead of rejection; SRS FR-12/SEC-03 violation |
| TC-FR14-014 | **FAIL** — NORMATIVE ORACLE VIOLATION | `role=user` DELETE returns **200** instead of rejection; SRS FR-12/SEC-03 violation |
| TC-FR14-015 | PASS | User GET of public list succeeds |
| TC-FR14-016 | **FAIL** — NORMATIVE ORACLE VIOLATION | Empty string name accepted with **200** + persisted entity; SRS FR-14 mandatory name rule violated |
| TC-FR14-017 | **FAIL** — NORMATIVE ORACLE VIOLATION | null name accepted with **200** + persisted entity; SRS FR-14 mandatory name rule violated |
| TC-FR14-018 | **FAIL** — NORMATIVE ORACLE VIOLATION | Missing `name` key accepted with **200** + persisted entity; SRS FR-14 mandatory name rule violated |
| TC-FR14-019 | **FAIL** — NORMATIVE ORACLE VIOLATION | Whitespace-only name accepted with **200** + persisted entity; SRS FR-14 mandatory name rule violated |
| TC-FR14-020 | EXPLORATORY OBSERVATION | Long name accepted; exact length limit not specified |
| TC-FR14-021 | EXPLORATORY OBSERVATION | Unicode name accepted; no restriction specified |
| TC-FR14-022 | EXPLORATORY OBSERVATION | Duplicate name accepted; uniqueness not specified |
| TC-FR14-023 | EXPLORATORY OBSERVATION | Integer name accepted; type coercion not specified |
| TC-FR14-024 | **FAIL** — NORMATIVE ORACLE VIOLATION | PUT on nonexistent ID reports **200 "Category updated"**; false-success for no entity mutated |
| TC-FR14-025 | **FAIL** — NORMATIVE ORACLE VIOLATION | DELETE on nonexistent ID reports **200 "Category deleted"**; false-success for no entity mutated |
| TC-FR14-026 | EXPLORATORY OBSERVATION | ID=0 handled gracefully |
| TC-FR14-027 | EXPLORATORY OBSERVATION | ID=-1 handled gracefully |
| TC-FR14-028 | EXPLORATORY OBSERVATION | Non-numeric ID handled gracefully |
| TC-FR14-029 | PASS | SQL payload treated as text; table intact |
| TC-FR14-030 | EXPLORATORY OBSERVATION | XSS payload accepted as text |
| TC-FR14-031 | EXPLORATORY OBSERVATION | Mass-assignment fields ignored |
| TC-FR14-032 | EXPLORATORY OBSERVATION | PUT body-id override ignored |
| TC-FR14-033 | EXPLORATORY OBSERVATION | Object-type name handled |
| TC-FR14-035 | PASS | Full lifecycle succeeds end-to-end |
| TC-FR14-037 | **FAIL** — NORMATIVE ORACLE VIOLATION | Deleted category reports **200 "Category updated"**; false-success on no entity |
| TC-FR14-038 | **FAIL** — NORMATIVE ORACLE VIOLATION | Deleted category reports **200 "Category deleted"**; false-success on no entity |
| TC-FR14-039 | PASS | GET schema observation |
| TC-FR14-040 | PASS | POST schema observation |
| TC-FR14-041 | PASS | PUT schema observation |
| TC-FR14-042 | PASS | DELETE schema observation |
| TC-FR14-H01 | EXPLORATORY OBSERVATION | Missing Content-Type returns 415 (expected) |
| TC-FR14-H02 | EXPLORATORY OBSERVATION | Zero-byte body observation |
| TC-FR14-H03 | EXPLORATORY OBSERVATION | PATCH method handled gracefully |
| TC-FR14-H04 | PASS | GET response headers observation |
| TC-FR14-H05 | **FAIL** — NORMATIVE ORACLE VIOLATION | Empty PUT body corrupts name to `null`; SRS FR-14 integrity rule violated |
| TC-FR14-H06 | PASS | Three batch creates succeed and are all distinct |

## Verdict Summary

| Verdict | Count |
|---|---:|
| PASS | 20 |
| FAIL — NORMATIVE ORACLE VIOLATION | 12 |
| EXPLORATORY OBSERVATION | 14 |
| BLOCKED | 0 |
| **Total** | **46** |

## Confirmed Normative Bugs

| Bug ID | Affected IDs | Root Cause |
|---|---|---|
| BUG-FR14-001 | TC-FR14-012, TC-FR14-013, TC-FR14-014 | `role=user` can mutate categories (RBAC violation) |
| BUG-FR14-002 | TC-FR14-016, TC-FR14-017, TC-FR14-018, TC-FR14-019 | Empty/null/whitespace/missing name accepted (FR-14 violation) |
| BUG-FR14-003 | TC-FR14-024, TC-FR14-025, TC-FR14-037, TC-FR14-038 | Nonexistent/already-deleted entity mutations report false-success (one CRUD-integrity root cause) |
| BUG-FR14-004 | TC-FR14-H05 | Empty PUT body corrupts existing name to null (FR-14 mutation integrity) |

## Canonical Evidence

- Collection SHA-256: computed at execution time
- Environment SHA-256: computed at execution time
- Run CLI/JSON/HTML: `23127259/evidence/fr14/newman/FR14-run01.*`
