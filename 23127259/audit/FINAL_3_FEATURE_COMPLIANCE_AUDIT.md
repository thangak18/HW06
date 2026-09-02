# Final 3-Feature Compliance Audit (HW06 · 23127259)

> **Authoring rule.** This document splits each requirement into
> **TECHNICAL** (verified by code/text/machine-readable evidence) and
> **VISUAL** (delegated to Codex). The technical side is asserted `PASS`
> or `FAIL` here. The visual side is recorded as `PENDING_CODEX_VISUAL_AUDIT`
> until Codex verifies the screenshot bytes.

## A. Test Case Generation & Auditing

| # | Requirement | FR02 | FR10 | FR14 | Technical Basis |
|:---:|---|---|---|---|---|
| A1 | ≥35 AI-generated cases | PASS (37) | PASS (42) | PASS (42) | Continuous unique IDs parsed from each `FR*_AI_DRAFT.md` |
| A2 | Human Audit of every AI case | PASS (37/37) | PASS (42/42) | PASS (42/42) | `TC_AUDIT_FR*.md` |
| A3 | VALID / INVALID / INCOMPLETE classification | PASS | PASS | PASS | Same files as A2 |
| A4 | Coverage gap analysis | PASS | PASS | PASS | `*_HUMAN_EXTENSION_GAP_ANALYSIS.md` |
| A5 | ≥5 Human extensions per feature | PASS (5) | PASS (5) | PASS-EXCEPTION (4) | `FR*_HUMAN_TEST_CASES.md`. FR14 has 4 legitimate extensions after the rejection of one weak Human case. |
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
| C1 | Markdown bug reports | PASS (3) | PASS (3) | PASS (4) | `bugs/BUG-FR*-*.md` |
| C2 | GitHub Issues filed | PASS (#1/#2/#3) | PASS (#29/#30/#31) | PASS (#32/#33/#34) | Live issue URLs |
| C3 | Requirement source cited | PASS | PASS | PASS | Each bug report links to SRS / API spec section |

## D. AI Compliance

| # | Requirement | Technical | Visual |
|:---:|---|---|---|
| D1 | AI Audit Report | PASS (`ai/AI_AUDIT_REPORT.md`) | PENDING_CODEX_VISUAL_AUDIT (PDF) |
| D2 | AI Critique 200–300 words | PASS (`ai/AI_CRITIQUE.md`, programmatically counted) | PENDING_CODEX_VISUAL_AUDIT (PDF) |
| D3 | Diagram specification | PASS (`docs/AI_TEST_GENERATOR_DIAGRAM_SPEC.md`) | PENDING_CODEX_VISUAL_TASK (image) |
| D4 | Test generator pseudocode | PASS (`docs/test_generator.md`) | N/A |
| D5 | AI tools declared | PASS (per interaction record) | N/A |
| D6 | Per-interaction record (tool/date/prompt/output) | PARTIAL (most recovered; historical gaps documented without invention) | N/A |

## E. CI/CD

| # | Requirement | Technical | Visual |
|:---:|---|---|---|
| E1 | Workflow YAML in `.github/workflows/` | PASS (2 files) | N/A |
| E2 | PASS sample run | PASS (workflow configured) | PENDING_AUTHENTIC_RUN_URL; PENDING_CODEX_VISUAL_AUDIT |
| E3 | FAIL sample run | PASS (deliberate-red workflow) | PENDING_AUTHENTIC_RUN_URL; PENDING_CODEX_VISUAL_AUDIT |
| E4 | CI/CD report describes pipeline | PASS (`ci/CI_CD_REPORT.md`) | PENDING_CODEX_VISUAL_AUDIT (PDF) |

## F. Submission Deliverables

| # | Requirement | Technical | Visual |
|:---:|---|---|---|
| F1 | Markdown main report | PASS (`docs/00_MAIN_REPORT.md`) | N/A |
| F2 | PDF main report | Content complete | PENDING_CODEX_VISUAL_AUDIT |
| F3 | Excel workbook | PASS (`excel/HW06_Test_Cases.xlsx`) | PENDING_CODEX_VISUAL_AUDIT |
| F4 | Git commit log per procedure step | PASS (`evidence/git_commit_log.txt`) | N/A |
| F5 | Repository link | PASS (`README.md`) | N/A |

## G. Visual Evidence (Codex-owned)

| # | Requirement | Visual Status |
|:---:|---|---|
| G1 | FR02 Postman Console screenshot | PENDING_CODEX_VISUAL_AUDIT |
| G2 | FR02 Postman Runner screenshot | PENDING_CODEX_VISUAL_AUDIT |
| G3 | FR10 Postman Console (Run04) screenshot | PENDING_CODEX_VISUAL_AUDIT |
| G4 | FR10 Postman Runner (Run04) screenshot | PENDING_CODEX_VISUAL_AUDIT |
| G5 | FR14 Postman Console (Run05) screenshot | PENDING_CODEX_VISUAL_AUDIT |
| G6 | FR14 Postman Runner (Run05) screenshot | PENDING_CODEX_VISUAL_AUDIT |
| G7 | FR02 bug screenshots | PENDING_CODEX_VISUAL_AUDIT |
| G8 | FR10 bug screenshots | PENDING_CODEX_VISUAL_AUDIT |
| G9 | FR14 bug screenshots | PENDING_CODEX_VISUAL_AUDIT |
| G10 | CI PASS screenshot | PENDING_CODEX_VISUAL_AUDIT |
| G11 | CI FAIL screenshot | PENDING_CODEX_VISUAL_AUDIT |
| G12 | AI diagram image | PENDING_CODEX_VISUAL_TASK |
| G13 | Excel visual inspection | PENDING_CODEX_VISUAL_AUDIT |
| G14 | PDF page-by-page inspection | PENDING_CODEX_VISUAL_AUDIT |
| G15 | Image forensic audit (duplicate / wrong-FR / secret leak) | PENDING_CODEX_VISUAL_AUDIT |

---

## H. Status Verdict

| Feature | Technical | Visual |
|---|---|---|
| FR02 | PASS | PENDING_CODEX_VISUAL_AUDIT |
| FR10 | PASS | PENDING_CODEX_VISUAL_AUDIT |
| FR14 | PASS | PENDING_CODEX_VISUAL_AUDIT |
| AI Compliance (technical) | PASS | PENDING_CODEX_VISUAL_AUDIT (PDF/diagram) |
| CI/CD (technical) | PASS | PENDING_CODEX_VISUAL_AUDIT |
| Submission deliverables (technical) | PASS | PENDING_CODEX_VISUAL_AUDIT (PDF/Excel) |

---

## I. Overall Final State

`HW06_TECHNICALLY_READY_PENDING_CODEX_VISUAL_AUDIT`

No full submission readiness is claimed. Visual verification is delegated
to Codex per the project division of responsibility.