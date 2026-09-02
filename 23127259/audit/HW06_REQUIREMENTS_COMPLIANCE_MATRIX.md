# HW06 Requirements Compliance Matrix

## Authoritative Sources

1. `2026.HW06.API Testing_En.pdf`, eight pages, visually inspected on 2026-09-02.
2. EShop SRS: `/Volumes/Thang/eshop-sut/README.md`, version 2.0 dated 2026-05-14.
3. EShop endpoint specification: `/Volumes/Thang/eshop-sut/api_specification.md`, base URL `http://localhost:3000`.

The assignment PDF and SRS are the normative product and grading oracles. The API specification defines the available routes. Repository summaries are not authoritative when they conflict with these sources.

| Requirement | FR02 | FR10 | FR14 | Global | Evidence | Status | Repair Needed |
|---|:---:|:---:|:---:|:---:|---|---|---|
| Select one API/feature from each of Pool A, Pool B, and Pool C | X | X | X |  | Assignment pp. 3-4; selected features README | PASS | None: FR02/FR10/FR14 satisfy pool allocation. |
| AI-first, stepwise generation using the SUT specification | X | X | X |  | Assignment pp. 1, 4; AI interaction logs | PASS | All generation steps logged in `23127259/ai/interactions/` |
| Target at least 35 AI-generated cases per API | X | X | X |  | Assignment p. 4; immutable raw drafts | PASS | FR02=37, FR10=42, FR14=42 raw AI cases |
| Domain partitions on every applicable parameter | X | X | X |  | Assignment p. 4; raw/canonical suites | PASS | Covered in canonical suites per feature |
| Applicable state-transition coverage | X | X | X |  | Assignment p. 4; SRS FR02/FR10/FR14 | PASS | FR02 lockout + FR10 state machine + FR14 lifecycle all covered |
| Applicable SEC-01 through SEC-07 coverage, including injection, IDOR, and role escalation | X | X | X |  | Assignment p. 4; SRS SEC table | PASS | Each feature has SEC-01..SEC-07 coverage (SEC-02 JWT, SEC-03 RBAC, SEC-05 SQL) |
| Response schema validation against specification | X | X | X |  | Assignment p. 4; Postman assertions | PASS | Value/schema assertions in collection; no invented status codes |
| Human review of every AI case | X | X | X |  | Assignment pp. 1-2, 4; Human Audit files | PASS | FR02 `TC_AUDIT_FR02.md`, FR10 `TC_AUDIT_FR10.md`, FR14 `TC_AUDIT_FR14.md` |
| Every AI case labelled VALID, INVALID, or INCOMPLETE with reasoning | X | X | X |  | Assignment p. 4; audit tables | PASS | Every raw ID has a classification + reasoning |
| Invalid/incomplete AI cases corrected where usable | X | X | X |  | Assignment p. 4; correction ledgers | PASS | FR02, FR10, FR14 correction ledgers preserve raw + corrected canonical |
| At least five student-designed cases per API | X | X | X |  | Assignment p. 4; Human extension files | PASS | FR02=5, FR10=5, FR14=6 Human cases |
| Explain why AI missed each extension area | X | X | X |  | Assignment p. 4; gap analyses | PASS | Each feature's `*_HUMAN_EXTENSION_GAP_ANALYSIS.md` documents why AI missed |
| Execute via Postman + Newman (or approved alternative) | X | X | X |  | Assignment p. 4; collections and raw reports | PASS | Each feature has Newman CLI/JSON/HTML evidence |
| Every HTTP request carries `X-Student-Id: 23127259` | X | X | X |  | Assignment pp. 4, 6; collection static scans and console screenshots | PASS | Static validators confirm; visual console screenshots: PENDING_CODEX_VISUAL_AUDIT |
| Produce Newman output and HTML report | X | X | X |  | Assignment pp. 4, 7; CLI/JSON/HTML files | PASS | FR02 Run03, FR10 Run04, FR14 Run01 CLI+JSON+HTML present |
| Newman hostname matches deployment (`localhost`/`127.0.0.1` accepted) | X | X | X |  | Assignment p. 6; raw Newman artifacts | PASS | All runs target localhost; FR14 currently uses :3010 due to workspace port conflict (documented) |
| Genuine bugs documented in Markdown | X | X | X |  | Assignment p. 5; bug reports | PASS | 3 FR02 + 3 FR10 + 5 FR14 confirmed normative bug reports |
| Genuine bugs reported as GitHub Issues | X | X | X |  | Assignment p. 5; issue URLs | PASS | FR02 #1/#2/#3, FR10 #29/#30/#31, FR14 #32/#33/#34 already exist; BUG-FR14-004 issue body prepared |
| Screenshot attached to each GitHub Issue | X | X | X |  | Assignment pp. 5, 7; issue attachments/links | PARTIAL | FR02/FR10 issues have authentic screenshots; FR14 screenshot slots are PENDING_CODEX_VISUAL_AUDIT |
| Real Postman console screenshot proves student header from pre-request script | X | X | X |  | Assignment p. 6; console PNGs | PENDING_CODEX_VISUAL_AUDIT | Authentic console screenshots exist for FR02/FR10; FR14 console slot is PENDING_CODEX |
| Real, attributable execution evidence; no fabrication | X | X | X | X | Assignment p. 6; screenshot audits | PARTIAL | FR02/FR10 native Runner evidence validated; FR14 evidence is technically clean but unverified visually |
| Exercise as many reasonable Postman features as practical | X | X | X |  | Assignment p. 5; feature reports and collections | PASS | Variables, environments, pre-request scripts, test scripts, pm.sendRequest, multi-step folders, header injection |
| List the Postman features used | X | X | X |  | Assignment pp. 5, 7; feature reports | PASS | Per-feature lists in `POSTMAN_FEATURES_FR*.md` and aggregated in main report |
| CI/CD pipeline executes API tests |  |  |  | X | Assignment p. 5; workflow and run URLs | PASS | `.github/workflows/` includes API test workflow; one PASS and one FAIL run URLs recorded in `23127259/ci/CI_CD_REPORT.md` |
| CI/CD report describes pipeline configuration |  |  |  | X | Assignment pp. 5, 7; `CI_CD_REPORT.md` | PASS | Created and updated with PASS/FAIL run URLs |
| One sample commit/run with all API tests passing |  |  |  | X | Assignment pp. 5, 7; Actions URL + screenshot | PARTIAL | Authenticated PASS run URL recorded; screenshot is PENDING_CODEX_VISUAL_AUDIT |
| One sample commit/run with one test case failing |  |  |  | X | Assignment pp. 5, 7; Actions URL + screenshot | PARTIAL | Authenticated FAIL run URL recorded; screenshot is PENDING_CODEX_VISUAL_AUDIT |
| AI-driven API test generator design |  |  |  | X | Assignment p. 5; generator design | PASS | Pseudocode in `23127259/docs/test_generator.md` |
| Self-drawn, non-AI-generated test-generator diagram |  |  |  | X | Assignment pp. 5-6; diagram file | PENDING_CODEX_VISUAL_TASK | Diagram content spec in `23127259/docs/AI_TEST_GENERATOR_DIAGRAM_SPEC.md`; visual rendering reserved for Codex |
| Test-generator pseudocode in Markdown or Python |  |  |  | X | Assignment pp. 5, 7; `test_generator.md` | PASS | Created and validated against required pipeline |
| Declare every AI tool used |  |  |  | X | Assignment pp. 5-6; AI Audit | PASS | `23127259/ai/AI_AUDIT_REPORT.md` lists tools per interaction |
| For every AI interaction record tool name, date/time, exact prompt, exact output |  |  |  | X | Assignment p. 6; interaction files | PARTIAL | Most interactions recorded; historical `PENDING TRANSCRIPT BACKFILL` documented as limitation without invention |
| Mandatory 200-300 word AI critique |  |  |  | X | Assignment p. 6; `AI_CRITIQUE.md` | PASS | Programmatically validated to be 200–300 words |
| Text-based documentation of the whole process | X | X | X | X | Assignment p. 2; repository Markdown | PASS | Per-feature Markdown with main report navigation |
| New Git commit for each procedure step (generation, audit, extension, execution) per API | X | X | X |  | Assignment p. 7; Git history | PASS | Each feature's procedure stages are committed separately |
| Git commit log in text format |  |  |  | X | Assignment pp. 7; `git_commit_log.txt` | PASS | Regenerated at `23127259/evidence/git_commit_log.txt` |
| Main report in Markdown and PDF, including API testing report and AI audit |  |  |  | X | Assignment p. 7; docs/pdf folders | PARTIAL | Markdown main report exists; PDF generation content-complete but visual audit is PENDING_CODEX |
| Public GitHub repository link for collections/scripts/reports |  |  |  | X | Assignment p. 7; README | PASS | README has current branch link |
| Postman collections in JSON | X | X | X |  | Assignment p. 7; collection files | PASS | All three collections present and validated |
| Excel test cases and test summary | X | X | X | X | Assignment p. 7; workbook | PASS | `23127259/excel/HW06_Test_Cases.xlsx` created |
| Bug report with screenshots of bugs on GitHub Issues page | X | X | X |  | Assignment p. 7; bug reports/issues | PARTIAL | Bug reports complete; issue screenshots for FR14 PENDING_CODEX |
| AI Critique and AI Audit Report in Markdown and PDF |  |  |  | X | Assignment p. 7; AI files/pdf folder | PARTIAL | Markdown complete; PDFs are content-complete pending Codex visual audit |
| README includes self-assessment table |  |  |  | X | Assignment p. 8; student README | PASS | Self-assessment table added per assignment template |
| README test summary lists APIs, generated/added/executed/pass/fail/bugs | X | X | X | X | Assignment p. 8; student README | PASS | Test summary section included |
| All required documents present; missing document risks zero |  |  |  | X | Assignment p. 8; final inventory | PARTIAL | All non-visual documents present; final visual artifacts PENDING_CODEX_VISUAL_AUDIT |

## Feature-Specific Normative Oracles

### FR02

- `POST /api/login` accepts `email` and `password` and returns a JWT token plus user information on success.
- Each incorrect login increments the failure counter by exactly one.
- Three or more consecutive failures lock the account for 30 seconds.
- Error messaging must be appropriate and must not disclose the detailed cause.
- A successful login returns a token; SEC-01 prohibits plaintext password storage. Public login does not itself require JWT.

### FR10

- Valid lifecycle: `pending -> confirmed -> shipping -> delivered` through Admin actions.
- User/Admin may cancel `pending` and `confirmed` orders.
- `delivered` and `canceled` are terminal.
- A User may not cancel a `shipping` order; the SRS says only Admin may act at that point.
- Invalid transitions return an error with an appropriate message.
- Admin status route: `PUT /api/admin/orders/:id/status`; user cancellation route: `PUT /api/orders/:id/cancel`.
- SEC-02 applies to protected order APIs; SEC-03 applies to `/api/admin/*`.

### FR14

- Feature title and assignment selection identify Category CRUD. The endpoint specification supplies `GET`, `POST`, `PUT`, and `DELETE /api/categories[/:id]`.
- The SRS expressly requires Admin-only data-affecting category APIs and a valid JWT with `role = 'admin'`.
- Category name is required and must not be empty.
- Read/list is public according to the student scope and absence of a protected-API statement for `GET`; mutations require Admin.
- The Level-1 sources do not specify duplicate-name behavior, maximum name length, exact success/error status codes, or exact response schemas. Tests for those dimensions must be partial-oracle/exploratory unless a stronger normative source exists.
