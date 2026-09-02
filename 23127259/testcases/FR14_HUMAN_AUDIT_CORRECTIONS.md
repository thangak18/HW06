# FR-14 Human Audit & Corrections

**Feature:** FR-14 – Category Management CRUD  
**Student:** Nguyễn Tấn Thắng (23127259)  
**Audit Date:** September 2, 2026  
**Input:** `FR14_AI_DRAFT.md` (42 raw AI-generated cases)

---

## Audit Methodology

Each AI-generated test case was reviewed against:
1. **Authoritative Sources:** FR14_REQUIREMENT_ANALYSIS.md, SUT source code analysis
2. **Oracle Correctness:** Expected results grounded against actual SUT implementation behavior
3. **Completeness:** All required assertions and preconditions specified
4. **Executability:** Can be directly translated to Postman requests with programmatic assertions

### Label Definitions
- **VALID:** Case is correct, complete, and directly executable. No changes required.
- **INVALID:** Case contains errors in expected behavior, endpoint, or logic. Must be corrected.
- **INCOMPLETE:** Case is partially correct but missing assertions, preconditions, or edge case handling.

---

## Audit Results

| Case ID | AI Label | Verdict | Corrective Action |
|---|---|:---:|---|
| TC-FR14-001 | Happy Path | **VALID** | None |
| TC-FR14-002 | Happy Path | **VALID** | None |
| TC-FR14-003 | State Verify | **VALID** | None |
| TC-FR14-004 | CRUD Update | **VALID** | None |
| TC-FR14-005 | State Verify | **VALID** | None |
| TC-FR14-006 | CRUD Delete | **VALID** | None |
| TC-FR14-007 | SEC-01 | **VALID** | None |
| TC-FR14-008 | SEC-01 | **VALID** | None |
| TC-FR14-009 | SEC-01 | **VALID** | None |
| TC-FR14-010 | SEC-01 | **VALID** | None |
| TC-FR14-011 | SEC-01 | **INCOMPLETE** | Need to specify exact tampered JWT string that parses but fails verification |
| TC-FR14-012 | SEC-02 | **VALID** | Dual-assertion: test both expected (403) and actual SUT behavior (200) |
| TC-FR14-013 | SEC-02 | **VALID** | Same dual-assertion approach |
| TC-FR14-014 | SEC-02 | **VALID** | Same dual-assertion approach |
| TC-FR14-015 | Auth Boundary | **VALID** | None |
| TC-FR14-016 | Input Val | **VALID** | Dual-assertion for expected vs actual |
| TC-FR14-017 | Input Val | **VALID** | Dual-assertion for expected vs actual |
| TC-FR14-018 | Input Val | **VALID** | Dual-assertion for expected vs actual |
| TC-FR14-019 | Input Val | **VALID** | Dual-assertion for expected vs actual |
| TC-FR14-020 | Boundary | **INCOMPLETE** | Need to specify exact string length (1001 chars) and verify storage behavior |
| TC-FR14-021 | I18N | **VALID** | None |
| TC-FR14-022 | Business Logic | **VALID** | Dual-assertion: expect 409, predict 200 |
| TC-FR14-023 | Type Safety | **VALID** | None |
| TC-FR14-024 | Boundary | **VALID** | Dual-assertion for expected vs actual |
| TC-FR14-025 | Boundary | **VALID** | Dual-assertion for expected vs actual |
| TC-FR14-026 | Boundary | **VALID** | None |
| TC-FR14-027 | Boundary | **VALID** | None |
| TC-FR14-028 | Type Safety | **VALID** | None |
| TC-FR14-029 | SEC-03 | **VALID** | Verify table still exists after injection attempt |
| TC-FR14-030 | SEC-03 | **VALID** | Verify raw string storage (stored XSS risk) |
| TC-FR14-031 | SEC-07 | **VALID** | None |
| TC-FR14-032 | SEC-07 | **VALID** | None |
| TC-FR14-033 | SEC-03 | **INCOMPLETE** | Object body may cause JSON parse error at Express level before reaching SQLite. Adjust to expect 500 or 200. |
| TC-FR14-034 | SEC-04 | **VALID** | Same dual-assertion as SEC-02 tests |
| TC-FR14-035 | State Trans | **VALID** | Multi-step — implement as folder with sequential requests |
| TC-FR14-036 | Ref Integrity | **VALID** | Need setup step to verify products exist with category_id=1 first |
| TC-FR14-037 | Invalid Seq | **VALID** | None |
| TC-FR14-038 | Idempotency | **VALID** | None |
| TC-FR14-039 | Schema | **VALID** | Add JSON Schema definition using tv4/ajv |
| TC-FR14-040 | Schema | **VALID** | Add JSON Schema definition |
| TC-FR14-041 | Schema | **VALID** | Add JSON Schema definition |
| TC-FR14-042 | Schema | **VALID** | Add JSON Schema definition |

---

## Summary

| Verdict | Count | Percentage |
|---|:---:|:---:|
| VALID | 38 | 90.5% |
| INCOMPLETE | 3 | 7.1% |
| INVALID | 0 | 0% |
| **Total Reviewed** | **42** | **100%** |
| **Usable After Correction** | **42** | **100%** |

### Corrections Applied

1. **TC-FR14-011:** Added concrete tampered JWT value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIn0.INVALID_SIG_HERE`
2. **TC-FR14-020:** Fixed boundary string to exactly 1001 `A` characters. Added verification that storage succeeds (SQLite TEXT is unbounded).
3. **TC-FR14-033:** Changed expected behavior to "either 500 (if SQLite errors on object) or 200 (if coerced)". Added assertion to check that categories table remains intact regardless.

### Identified Gap Areas for Human Extension
1. **Content-Type header missing/wrong** — What happens when POST/PUT is sent without `Content-Type: application/json`?
2. **Empty body** — What happens when POST is sent with completely empty body (not even `{}`)?
3. **HTTP method override** — Can PATCH or other methods be used on category endpoints?
4. **Rate limiting** — No rate limiting tests (SEC-06)
5. **Concurrent modification** — No concurrency/race condition tests
6. **Response header validation** — Content-Type, Cache-Control verification
7. **Large batch operations** — Creating many categories in sequence
