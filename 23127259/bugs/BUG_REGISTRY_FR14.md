# FR-14 Bug Registry

**Feature:** FR-14 – Category Management CRUD (Pool C – Web Admin)  
**Student:** Nguyễn Tấn Thắng (`23127259`)  
**Registry Date:** September 2, 2026

---

## Confirmed Defects

| Bug ID | Summary | Severity | Priority | SEC Mapping | Test Cases | Status |
|---|---|:---:|:---:|:---:|---|:---:|
| [BUG-FR14-001](BUG-FR14-001.md) | Missing RBAC — Regular user can CRUD categories | 🔴 HIGH | P1 | SEC-02, SEC-04 | TC-FR14-012, 013, 014, 034 | CONFIRMED |
| [BUG-FR14-002](BUG-FR14-002.md) | Missing input validation — Empty/null/whitespace names accepted | 🟡 MEDIUM | P2 | — | TC-FR14-016, 017, 018, 019 | CONFIRMED |
| [BUG-FR14-003](BUG-FR14-003.md) | No existence check — PUT/DELETE succeed on non-existent IDs | 🟡 MEDIUM | P2 | — | TC-FR14-024, 025, 037, 038 | CONFIRMED |
| [BUG-FR14-004](BUG-FR14-004.md) | Unhandled server exception (HTTP 500) when Content-Type omitted | 🔴 HIGH | P1 | — | TC-FR14-H01 | CONFIRMED |

---

## Additional Observations & Risk Findings

| Finding | Description | Test Case | Severity | Risk Classification |
|---|---|:---:|:---:|---|
| **No duplicate name prevention** | Category with existing name can be created repeatedly | TC-FR14-022 | 🟢 LOW | Data Duplication |
| **No referential integrity check on DELETE** | Deleting a category that has products referencing it orphans products without cascade or warning | TC-FR14-036, TC-FR14-H07 | 🟡 MEDIUM | Relational Orphan Risk |
| **Empty body on PUT nullifies category name** | Sending `PUT /api/categories/:id` with `{}` body overwrites existing name to NULL in SQLite | TC-FR14-H05 | 🟡 MEDIUM | Data Corruption |
| **Stored XSS payload acceptance** | Script tags stored verbatim without server-side validation | TC-FR14-030 | 🟡 MEDIUM | Stored XSS Risk (SEC-03) |

---

## Newman Execution Run Summary

| Metric | Run 01 Value |
|---|---|
| **Collection** | `FR14_Category_CRUD.postman_collection.json` |
| **Total Requests Executed** | 59 (3 setup helpers + 56 test requests) |
| **Total Assertions** | 96 |
| **Passing Assertions** | 81 (84.4%) |
| **Failing Assertions** | 15 (15.6%) |
| **Nature of Failures** | **100% Intentional Defect-Confirming Assertions** |
| **Run Duration** | 6.8s |
| **Average Response Time** | 2ms |
| **Evidence Files** | `evidence/fr14/newman/FR14-run01.{cli.txt, html, json, exitcode.txt}` |
