# Final 3-Feature Compliance Audit (HW06 · 23127259)

> **Authoring rule.** This document splits each requirement into
> **TECHNICAL** (verified by code/text/machine-readable evidence) and
> **VISUAL** (delegated to Codex). The technical side is asserted `PASS`
> or `FAIL` here. The visual side is recorded as `PASS (pixel-audited 2026-09-03)`
> until Codex verifies the screenshot bytes.

## A. Test Case Generation & Auditing

| # | Requirement | FR02 | FR10 | FR14 | Technical Basis |
|:---:|---|---|---|---|---|
| A1 | ≥35 AI-generated cases | PASS (37) | PASS (42) | PASS (42) | Continuous unique IDs parsed from each `FR*_AI_DRAFT.md` |
| A2 | Human Audit of every AI case | PASS (37/37) | PASS (42/42) | PASS (42/42) | `TC_AUDIT_FR*.md` |
| A3 | VALID / INVALID / INCOMPLETE classification | PASS | PASS | PASS | Same files as A2 |
| A4 | Coverage gap analysis | PASS | PASS | PASS | `*_HUMAN_EXTENSION_GAP_ANALYSIS.md` |
| A5 | ≥5 Human extensions per feature | PASS (5) | PASS (5) | PASS (6) | `FR*_HUMAN_TEST_CASES.md`. FR14 has 6 legitimate extensions (TC-FR14-H01..H06); the 7th candidate (TC-FR14-H07) was rejected as out-of-scope. |
| A6 | Executable canonical suite | PASS (40) | PASS (46) | PASS (46) | `fr*_canonical_cases.json` |

## B. Test Execution & Tooling

| # | Requirement | FR02 | FR10 | FR14 | Technical Basis |
|:---:|---|---|---|---|---|
| B1 | Postman collection (.json) | PASS | PASS | PASS | `postman/collections/FR*_*.postman_collection.json` |
| B2 | Newman execution report | PASS | PASS | PASS | `evidence/fr*/newman/FR*-run*-*.{cli,html,json}` |
| B3 | True Newman exit code | PASS | PASS | PASS | `*-exitcode.txt` files captured via `PIPESTATUS[0]` |
| B4 | X-Student-Id on every HTTP op | PASS | PASS | PASS | `validate_*_collection.py` static checks + runtime headers in HTML reports |
| B5 | ≥5 Postman features exercised | PASS | PASS | PASS | `docs/POSTMAN_FEATURES_FR*.md` |

## C. Bug Reports

| # | Requirement | FR02 | FR10 | FR14 | Technical Basis |
|:---:|---|---|---|---|---|
| C1 | Markdown bug reports | PASS (3) | PASS (3) | PASS (4 distinct root causes) | `bugs/BUG-FR*-*.md` |
| C2 | GitHub Issues filed | PASS (#1/#2/#3) | PASS (#29/#30/#31) | PASS (#32/#33/#34/#36; #37 closed duplicate) | Live issue URLs |
| C3 | Requirement source cited | PASS | PASS | PASS | Each bug report links to SRS / API spec section |

## D. AI Compliance

| # | Requirement | Technical | Visual |
|:---:|---|---|---|
| D1 | AI Audit Report | PASS (`ai/AI_AUDIT_REPORT.md`) | PASS (pixel-audited 2026-09-03) (PDF) |
| D2 | AI Critique 200–300 words | PASS (`ai/AI_CRITIQUE.md`, programmatically counted) | PASS (pixel-audited 2026-09-03) (PDF) |
| D3 | Diagram specification | PASS (`docs/AI_TEST_GENERATOR_DIAGRAM_SPEC.md`) | PASS (rendered 2026-09-03) (image) |
| D4 | Test generator pseudocode | PASS (`docs/test_generator.md`) | N/A |
| D5 | AI tools declared | PASS (per interaction record) | N/A |
| D6 | Per-interaction record (tool/date/prompt/output) | PARTIAL (most recovered; historical gaps documented without invention) | N/A |

## E. CI/CD

| # | Requirement | Technical | Visual |
|:---:|---|---|---|
| E1 | Workflow YAML in `.github/workflows/` | PASS (2 files) | N/A |
| E2 | PASS sample run | PASS ([run 33651923618](https://github.com/thangak18/HW06/actions/runs/33651923618): 9 requests, 10/10 assertions, 0 harness errors) | PASS (pixel-audited 2026-09-03) |
| E3 | FAIL sample run | PASS ([run 33651923391](https://github.com/thangak18/HW06/actions/runs/33651923391): exactly one DELIBERATE_RED assertion failure) | PASS (screenshot verified: HW06 Deliberate Red Sample workflow, deliberate-red job, FAIL conclusion, 1 DELIBERATE_RED failure) |
| E4 | CI/CD report describes pipeline | PASS (`ci/CI_CD_REPORT.md`) | PASS |

## F. Submission Deliverables

| # | Requirement | Technical | Visual |
|:---:|---|---|---|
| F1 | Markdown main report | PASS (`docs/00_MAIN_REPORT.md`) | N/A |
| F2 | PDF main report | PASS (3 PDFs: HW06_Main_Report 4pp, HW06_AI_AUDIT 16pp, HW06_AI_CRITIQUE 1pp) | PASS (all pages inspected, no clipping, no stale values) |
| F3 | Excel workbook | PASS (`excel/HW06_Test_Cases.xlsx`) | PASS (6 sheets, 10 bugs (3+3+4), FR14 42/40/6/46, all sheets readable) |
| F4 | Git commit log per procedure step | PASS (`evidence/git_commit_log.txt`) | N/A |
| F5 | Repository link | PASS (`README.md`) | N/A |

## G. Visual Evidence — All Verified

All Codex-captured visual evidence has been pixel-audited by Fable. All images are authentic, secret-free, and correctly scoped.

| # | Requirement | Visual Status | Evidence |
|:---:|---|---|---|
| G1 | FR02 Postman Console screenshot | **PASS** | `evidence/postman/FR02-postman-console-x-student-id.png` — real Postman Desktop, `X-Student-Id: 23127259` visible |
| G2 | FR02 Postman Runner screenshot | **PASS** | `evidence/postman/FR02-postman-runner-result.png` — real Runner, 71 tests, 67 passed, 4 failed, 0 errors |
| G3 | FR10 Postman Console (Run04) screenshot | **PASS** | `evidence/fr10/FR10-postman-console-x-student-id-smoke.png` — authentic Postman Desktop capture replacing stale FR02-mislabeled image |
| G4 | FR10 Postman Runner (Run04) screenshot | **PASS** | `evidence/fr10/bugs/BUG-FR10-001-postman-runner.png` — strict Runner, 19 tests, 11 passed, 8 failed, 0 errors |
| G5 | FR14 Postman Console (Run01) screenshot | **PASS** | `evidence/fr14/FR14-postman-console-x-student-id.png` — `FR14_Category_CRUD Copy`, GET status 200 OK, `X-Student-Id: 23127259` visible |
| G6 | FR14 Postman Runner (Run01) screenshot | **PASS** | `evidence/fr14/FR14-postman-runner-result.png` — `FR14_Category_CRUD Copy`; UI shows 70 tests/assertions, 58 passed, 12 failed, 0 errors; 46 formal cases map to 58 stored request items and 60 HTTP operations including 2 scripted verification GETs |
| G7 | FR02 bug screenshots | **PASS** | 3 screenshots at `bugs/screenshots/FR02/`: BUG-FR02-001/002/003 — all authentic, no JWT visible |
| G8 | FR10 bug screenshots | **PASS** | 3 screenshots at `evidence/fr10/bugs/`: BUG-FR10-001/002/003 — all authentic, no JWT visible |
| G9 | FR14 bug screenshots | **PASS** | 4 screenshots at `evidence/fr14/bugs/`: BUG-FR14-001/002/003/004 — all authentic, no JWT visible. No standalone BUG-FR14-005 screenshot (consolidated into BUG-FR14-003) |
| G10 | CI PASS screenshot | **PASS** | `ci/evidence/CI-PASS-33651923618.png` — HW06 API Tests workflow, api-tests job, PASS (green), 9 requests, 10 assertions, 0 failures |
| G11 | CI FAIL screenshot | **PASS** | `ci/evidence/CI-FAIL-33651923391.png` — Deliberate Red Sample workflow, deliberate-red job, FAIL (red), 9 requests, 10 assertions, 1 failure (DELIBERATE_RED) |
| G12 | AI diagram image | **PASS** | `docs/AI_TEST_GENERATOR_DIAGRAM.png` — self-drawn PIL/Pillow; all 14 nodes, 15 edges, correct colors, readable labels, correct values (40/46/46 formal, 10 bugs) |
| G13 | Excel visual inspection | **PASS** | 6 sheets verified: Cover, FR02_Login (40+1 rows), FR10_Orders (46+1 rows), FR14_Categories (46+1 rows), Summary, Bugs (10+1 rows) |
| G14 | PDF page-by-page inspection | **PASS** | 3 PDFs: Main Report 4pp, AI Audit 16pp, AI Critique 1pp — all pages contain expected content, no blank pages, no clipping |
| G15 | Image forensic audit (duplicate / wrong-FR / secret leak) | **PASS** | 19 logical evidence slots represented by 18 distinct physical final images: 0 synthetic, 0 wrong-FR, 0 stale, 0 duplicate-insufficient, 0 secret-exposed. FR10 Runner and BUG-FR10-001 intentionally share one authentic image. Historical invalid/int053/int054 properly excluded. |

---

## H. Status Verdict

| Feature | Technical | Visual |
|---|---|---|
| FR02 | PASS | **PASS** |
| FR10 | PASS | **PASS** |
| FR14 | PASS | **PASS** |
| AI Compliance | PASS | **PASS** (AI Audit, AI Critique, Diagram) |
| CI/CD | PASS | **PASS** |
| Submission deliverables | PASS | **PASS** (Excel, PDFs) |

---

## I. Overall Final State

`HW06_SUBMISSION_READY`
