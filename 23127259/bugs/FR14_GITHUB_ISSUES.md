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
| `BUG-FR14-001` | Regular `role=user` can mutate Categories | HIGH | [#32](https://github.com/thangak18/HW06/issues/32) | `https://github.com/thangak18/HW06/issues/32` | `23127259/evidence/fr14/bugs/BUG-FR14-001-*.png` (PENDING_CODEX_VISUAL_AUDIT) |
| `BUG-FR14-002` | Empty/null/whitespace/missing `name` accepted on POST `/api/categories` | MEDIUM | [#33](https://github.com/thangak18/HW06/issues/33) | `https://github.com/thangak18/HW06/issues/33` | `23127259/evidence/fr14/bugs/BUG-FR14-002-*.png` (PENDING_CODEX_VISUAL_AUDIT) |
| `BUG-FR14-003` | Non-existent category PUT/DELETE returns false-success | MEDIUM | [#34](https://github.com/thangak18/HW06/issues/34) | `https://github.com/thangak18/HW06/issues/34` | `23127259/evidence/fr14/bugs/BUG-FR14-003-*.png` (PENDING_CODEX_VISUAL_AUDIT) |
| `BUG-FR14-004` | Empty PUT body corrupts existing category name to `null` | MEDIUM | PENDING_GH_ISSUE (`GH_AUTH_REQUIRED`) | body: `23127259/bugs/BUG-FR14-004-issue-body.md` | `23127259/evidence/fr14/bugs/BUG-FR14-004-*.png` (PENDING_CODEX_VISUAL_AUDIT) |
| `BUG-FR14-005` | Already-deleted category PUT/DELETE returns false-success | MEDIUM | PENDING_GH_ISSUE (`GH_AUTH_REQUIRED`) | body: `23127259/bugs/BUG-FR14-005-issue-body.md` | `23127259/evidence/fr14/bugs/BUG-FR14-005-*.png` (PENDING_CODEX_VISUAL_AUDIT) |

## 2. Policy Compliance Confirmation

- **Total Confirmed Issues Filed:** Exactly 5
- **Exploratory Observations Filed:** 0 (TC-FR14-H01 missing-Content-Type behaviour is `EXPLORATORY_ROBUSTNESS_OBSERVATION`; not promoted to a confirmed bug)
- **Live Issue Authenticity:** #32 / #33 / #34 verified against GitHub.
- **Pending Issues:** BUG-FR14-004 and BUG-FR14-005 require GitHub authentication (`gh` CLI) to POST. Issue bodies are committed and ready to file.
