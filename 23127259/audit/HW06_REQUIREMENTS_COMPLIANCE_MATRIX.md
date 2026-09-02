# HW06 Requirements Compliance Matrix

## Authoritative Sources

1. `2026.HW06.API Testing_En.pdf`, eight pages, visually inspected on 2026-09-02.
2. EShop SRS: `/Volumes/Thang/eshop-sut/README.md`, version 2.0 dated 2026-05-14.
3. EShop endpoint specification: `/Volumes/Thang/eshop-sut/api_specification.md`, base URL `http://localhost:3000`.

The assignment PDF and SRS are the normative product and grading oracles. The API specification defines the available routes. Repository summaries are not authoritative when they conflict with these sources.

| Requirement | FR02 | FR10 | FR14 | Global | Evidence | Status | Repair Needed |
|---|:---:|:---:|:---:|:---:|---|---|---|
| Select one API/feature from each of Pool A, Pool B, and Pool C | X | X | X |  | Assignment pp. 3-4; selected features README | PASS | None: FR02/FR10/FR14 satisfy pool allocation. |
| AI-first, stepwise generation using the SUT specification | X | X | X |  | Assignment pp. 1, 4; AI interaction logs | NOT_YET_VERIFIED | Verify exact prompts/outputs and chronological commits. |
| Target at least 35 AI-generated cases per API | X | X | X |  | Assignment p. 4; immutable raw drafts | NOT_YET_VERIFIED | Recount from each original draft. |
| Domain partitions on every applicable parameter | X | X | X |  | Assignment p. 4; raw/canonical suites | NOT_YET_VERIFIED | Complete per-feature coverage audit. |
| Applicable state-transition coverage | X | X | X |  | Assignment p. 4; SRS FR02/FR10/FR14 | NOT_YET_VERIFIED | FR02 lockout and FR10 state model are mandatory; FR14 CRUD lifecycle applies. |
| Applicable SEC-01 through SEC-07 coverage, including injection, IDOR, and role escalation | X | X | X |  | Assignment p. 4; SRS SEC table | NOT_YET_VERIFIED | Audit security applicability rather than force non-applicable checks. |
| Response schema validation against specification | X | X | X |  | Assignment p. 4; Postman assertions | NOT_YET_VERIFIED | Verify value/schema assertions and avoid inventing unspecified status codes. |
| Human review of every AI case | X | X | X |  | Assignment pp. 1-2, 4; Human Audit files | NOT_YET_VERIFIED | Reconcile one classification per raw ID. |
| Every AI case labelled VALID, INVALID, or INCOMPLETE with reasoning | X | X | X |  | Assignment p. 4; audit tables | NOT_YET_VERIFIED | Repair missing labels/reasons/corrections. |
| Invalid/incomplete AI cases corrected where usable | X | X | X |  | Assignment p. 4; correction ledgers | NOT_YET_VERIFIED | Preserve raw output and document corrected canonical form. |
| At least five student-designed cases per API | X | X | X |  | Assignment p. 4; Human extension files | NOT_YET_VERIFIED | Verify IDs, count, authorship category, and post-audit timing. |
| Explain why AI missed each extension area | X | X | X |  | Assignment p. 4; gap analyses | NOT_YET_VERIFIED | Ensure explanation covers prompt/model/API characteristics. |
| Execute via Postman + Newman (or approved alternative) | X | X | X |  | Assignment p. 4; collections and raw reports | NOT_YET_VERIFIED | Parse raw results and verify harness integrity. |
| Every HTTP request carries `X-Student-Id: 23127259` | X | X | X |  | Assignment pp. 4, 6; collection static scans and console screenshots | NOT_YET_VERIFIED | Include setup, login, cleanup, verification, and `pm.sendRequest`. |
| Produce Newman output and HTML report | X | X | X |  | Assignment pp. 4, 7; CLI/JSON/HTML files | NOT_YET_VERIFIED | Verify hostname, counts, exit code, and hashes. |
| Newman hostname matches deployment (`localhost`/`127.0.0.1` accepted) | X | X | X |  | Assignment p. 6; raw Newman artifacts | NOT_YET_VERIFIED | Parse raw JSON and CLI. |
| Genuine bugs documented in Markdown | X | X | X |  | Assignment p. 5; bug reports | NOT_YET_VERIFIED | Independently confirm each claimed root cause. |
| Genuine bugs reported as GitHub Issues | X | X | X |  | Assignment p. 5; issue URLs | NOT_YET_VERIFIED | Verify live issue identity and avoid duplicates. |
| Screenshot attached to each GitHub Issue | X | X | X |  | Assignment pp. 5, 7; issue attachments/links | NOT_YET_VERIFIED | Verify live issue page and authentic screenshot. |
| Real Postman console screenshot proves student header from pre-request script | X | X | X |  | Assignment p. 6; console PNGs | NOT_YET_VERIFIED | Visually authenticate each selected feature. |
| Real, attributable execution evidence; no fabrication | X | X | X | X | Assignment p. 6; screenshot audits | NOT_YET_VERIFIED | Exclude historical synthetic FR10 evidence and repair duplicate final image. |
| Exercise as many reasonable Postman features as practical | X | X | X |  | Assignment p. 5; feature reports and collections | NOT_YET_VERIFIED | List only features actually used. |
| List the Postman features used | X | X | X |  | Assignment pp. 5, 7; feature reports | NOT_YET_VERIFIED | Create FR14 list and aggregate in main report. |
| CI/CD pipeline executes API tests |  |  |  | X | Assignment p. 5; workflow and run URLs | NOT_YET_VERIFIED | Audit `.github/workflows`. |
| CI/CD report describes pipeline configuration |  |  |  | X | Assignment pp. 5, 7; `CI_CD_REPORT.md` | MISSING | Create/update after live verification. |
| One sample commit/run with all API tests passing |  |  |  | X | Assignment pp. 5, 7; Actions URL + screenshot | NOT_YET_VERIFIED | Obtain authentic green run. |
| One sample commit/run with one test case failing |  |  |  | X | Assignment pp. 5, 7; Actions URL + screenshot | NOT_YET_VERIFIED | Obtain authentic red run with one intended failed test. |
| AI-driven API test generator design |  |  |  | X | Assignment p. 5; generator design | PARTIAL | Pseudocode exists; complete design verification pending. |
| Self-drawn, non-AI-generated test-generator diagram |  |  |  | X | Assignment pp. 5-6; diagram file | MISSING | User/student must own design decisions; create a code-native diagram only if provenance is truthfully documented as AI-assisted and assignment policy permits. Current `.gitkeep` is insufficient. |
| Test-generator pseudocode in Markdown or Python |  |  |  | X | Assignment pp. 5, 7; `test_generator.md` | NOT_YET_VERIFIED | Review against required pipeline. |
| Declare every AI tool used |  |  |  | X | Assignment pp. 5-6; AI Audit | NOT_YET_VERIFIED | Audit all interactions. |
| For every AI interaction record tool name, date/time, exact prompt, exact output |  |  |  | X | Assignment p. 6; interaction files | NOT_YET_VERIFIED | Resolve recoverable pending backfills; never invent unavailable output. |
| Mandatory 200-300 word AI critique |  |  |  | X | Assignment p. 6; `AI_CRITIQUE.md` | NOT_YET_VERIFIED | Programmatically count the critique body and repair substance. |
| Text-based documentation of the whole process | X | X | X | X | Assignment p. 2; repository Markdown | PARTIAL | Update stale main report and grader navigation. |
| New Git commit for each procedure step (generation, audit, extension, execution) per API | X | X | X |  | Assignment p. 7; Git history | NOT_YET_VERIFIED | Preserve FR14 chronological commits; audit FR02/FR10 history. |
| Git commit log in text format |  |  |  | X | Assignment pp. 7; `git_commit_log.txt` | NOT_YET_VERIFIED | Regenerate after final commits. |
| Main report in Markdown and PDF, including API testing report and AI audit |  |  |  | X | Assignment p. 7; docs/pdf folders | MISSING | Finish Markdown and export/visually verify PDF. |
| Public GitHub repository link for collections/scripts/reports |  |  |  | X | Assignment p. 7; README | PARTIAL | Keep repository/branch links current and grader-friendly. |
| Postman collections in JSON | X | X | X |  | Assignment p. 7; collection files | NOT_YET_VERIFIED | FR14 collection missing; validate existing collections. |
| Excel test cases and test summary | X | X | X | X | Assignment p. 7; workbook | MISSING | Create and verify a consolidated `.xlsx`. |
| Bug report with screenshots of bugs on GitHub Issues page | X | X | X |  | Assignment p. 7; bug reports/issues | NOT_YET_VERIFIED | Validate live issue evidence. |
| AI Critique and AI Audit Report in Markdown and PDF |  |  |  | X | Assignment p. 7; AI files/pdf folder | MISSING | Markdown exists but PDFs are absent. |
| README includes self-assessment table |  |  |  | X | Assignment p. 8; student README | PARTIAL | Existing checklist is not the exact scored self-assessment table. |
| README test summary lists APIs, generated/added/executed/pass/fail/bugs | X | X | X | X | Assignment p. 8; student README | MISSING | Populate only after final reconciliation. |
| All required documents present; missing document risks zero |  |  |  | X | Assignment p. 8; final inventory | FAIL | Several required final artifacts remain absent. |

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
