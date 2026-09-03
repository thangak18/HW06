# FR-14 Formal GitHub Issues Registry

- **Feature Under Test:** FR-14 Category Management (CRUD), Pool C.
- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** 23127259
- **Repository:** `thangak18/HW06`
- **Primary Branch:** `thang/hw06-implementation`

---

## 1. Filed GitHub Issues Registry

| Bug ID | Title | Severity | GitHub Issue # | Live GitHub URL | Screenshot Evidence Reference |
|:---:|---|:---:|:---:|---|---|
| `BUG-FR14-001` | Regular `role=user` can mutate Categories | HIGH | [#32](https://github.com/thangak18/HW06/issues/32) | `https://github.com/thangak18/HW06/issues/32` | `23127259/evidence/fr14/bugs/BUG-FR14-001-*.png` (PASS (pixel-audited 2026-09-03)) |
| `BUG-FR14-002` | Empty/null/whitespace/missing `name` accepted on POST `/api/categories` | MEDIUM | [#33](https://github.com/thangak18/HW06/issues/33) | `https://github.com/thangak18/HW06/issues/33` | `23127259/evidence/fr14/bugs/BUG-FR14-002-*.png` (PASS (pixel-audited 2026-09-03)) |
| `BUG-FR14-003` | Non-existent category PUT/DELETE returns false-success | MEDIUM | [#34](https://github.com/thangak18/HW06/issues/34) | `https://github.com/thangak18/HW06/issues/34` | `23127259/evidence/fr14/bugs/BUG-FR14-003-*.png` (PASS (pixel-audited 2026-09-03)) |
| `BUG-FR14-004` | Empty PUT body corrupts existing category name to `null` | MEDIUM | [#36](https://github.com/thangak18/HW06/issues/36) | `https://github.com/thangak18/HW06/issues/36` | `23127259/evidence/fr14/bugs/BUG-FR14-004-*.png` (PASS (pixel-audited 2026-09-03)) |

## 2. Policy Compliance Confirmation

- **Total Distinct Confirmed Issues Filed:** Exactly 4
- **Live distinct Issue Numbers:** `#32` (FR14-001), `#33` (FR14-002), `#34` (FR14-003), `#36` (FR14-004).
- **Exploratory Observations Filed:** 0 (TC-FR14-H01 missing-Content-Type behaviour is `EXPLORATORY_ROBUSTNESS_OBSERVATION`; not promoted to a confirmed bug)
- **Live Issue Authenticity:** #32 / #33 / #34 / #36 fetched directly and confirmed open. #37 is closed as duplicate of #34 because TC-037/038 exercise the same false-success-on-no-entity root cause as TC-024/025.
- **Pending Issues:** None. All four distinct normative FR14 bugs have a live GitHub Issue; #37 is preserved closed as a duplicate audit artifact.
