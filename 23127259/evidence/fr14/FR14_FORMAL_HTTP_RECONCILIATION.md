# FR14 Formal-vs-HTTP Reconciliation

## Definitions

- **Formal case** = one canonical test ID (`TC-FR14-XXX` or `TC-FR14-HXX`) that represents one normative test point.
- **HTTP request** = one `newman` execution item, including setup/login/helper/verification calls and `pm.sendRequest` callbacks.

The two counts differ because some formal cases require multiple HTTP operations (login → setup → main → verify → cleanup), while others combine steps into one call.

## Reconciliation Table

| Formal ID | Setup HTTP | Main HTTP | Verification HTTP | Cleanup HTTP | Total HTTP | Oracle | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| TC-FR14-001 | 1 (HELPER-000A), 1 (HELPER-000B), 1 (HELPER-000C) | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |
| TC-FR14-002 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-003 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-004 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-005 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-006 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-007 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-008 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-009 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-010 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-011 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-012 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | FAIL |
| TC-FR14-013 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | FAIL |
| TC-FR14-014 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | FAIL |
| TC-FR14-015 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-016 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | FAIL |
| TC-FR14-017 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | FAIL |
| TC-FR14-018 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | FAIL |
| TC-FR14-019 | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | FAIL |
| TC-FR14-020 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-021 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-022 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-023 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-024 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | FAIL |
| TC-FR14-025 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | FAIL |
| TC-FR14-026 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-027 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-028 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-029 | 1, 1, 1 | 1 | 1 (pm.sendRequest) | 0 | 5 | SPECIFICATION-BACKED | PASS |
| TC-FR14-030 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-031 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | EXPLORATORY |
| TC-FR14-032 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | EXPLORATORY |
| TC-FR14-033 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-035a | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-035b | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-035c | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-035d | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-035e | 1, 1, 1 | 1 | 0 | 0 | 4 | SPECIFICATION-BACKED | PASS |
| TC-FR14-037 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | FAIL |
| TC-FR14-038 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | FAIL |
| TC-FR14-039 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |
| TC-FR14-040 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |
| TC-FR14-041 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |
| TC-FR14-042 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |
| TC-FR14-H01 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-H02 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-H03 | 1, 1, 1 | 1 | 0 | 0 | 4 | EXPLORATORY | EXPLORATORY |
| TC-FR14-H04 | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |
| TC-FR14-H05 | 1, 1, 1 | 1 (setup) + 1 (main) + 1 (pm.sendRequest verify) | 1 (verify) | 1 (cleanup) | 7 | SPECIFICATION-BACKED | FAIL |
| TC-FR14-H06a | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |
| TC-FR14-H06b | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |
| TC-FR14-H06c | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |
| TC-FR14-H06 (verify) | 1, 1, 1 | 1 | 0 | 0 | 4 | PARTIAL-ORACLE | PASS |

## Totals

| Category | Count |
|---|---:|
| Formal cases | 46 |
| Helper HTTP requests | 3 (HELPER-000A, HELPER-000B, HELPER-000C) |
| Test HTTP requests | 58 |
| Total HTTP requests | 60 |
| pm.sendRequest HTTP | 1 (TC-029 verification GET) |
| Plus TC-H05 multi-step adds 2 extra | — |

The Newman 60 HTTP executions reflect: 3 helpers + 58 test steps (including 3 multi-step operations broken into separate Newman items: TC-035 lifecycle, TC-H05 empty PUT, TC-H06 batch). 1 `pm.sendRequest` callback (TC-029) does NOT count as a separate Newman HTTP request in the run totals.

## Why the counts differ

- **Formal cases** are logical test points that may span multiple HTTP operations.
- **Newman request counts** count every individual HTTP call (helpers + main + verifications + cleanup).
- **Multi-step cases** (TC-035 lifecycle, TC-H05 empty PUT, TC-H06 batch) intentionally split their lifecycle into separate Newman items for better isolation and clarity.
- **pm.sendRequest callbacks** for verification GETs do not show up as separate Newman HTTP items.

## Source

- 46-case canonical map: `23127259/testcases/fr14_canonical_cases.json`
- Canonical collection: `23127259/postman/collections/FR14_Category_CRUD.postman_collection.json`
- Newman raw: `23127259/evidence/fr14/newman/FR14-run01.json`
