# Codex Visual Evidence Handoff

> **Purpose.** This document enumerates every visual evidence task that
> remains for the Codex agent. All non-visual work has been completed and
> reviewed by the Senior QA / Test Architect persona. Codex is responsible
> for inspecting, capturing, or recapturing screenshots, validating the AI
> test-generator diagram visually, and performing the final image-based
> forensic audit.

## Division of Responsibility Reminder

| Concern | Owner |
|---|---|
| Code-level Newman runs, validators, secrets, bug reproduction | Senior QA (already done) |
| Markdown / Excel / PDF content generation | Senior QA (already done) |
| Visual screenshot capture and inspection | **Codex** |
| Pixel-level image validation | **Codex** |
| AI test-generator diagram visual rendering / verification | **Codex** |
| Final image duplicate / wrong-FR / secret leak forensic audit | **Codex** |

---

## Final Canonical Truth (read this before any visual work)

| Item | Value | Source |
|---|---|---|
| FR02 canonical run | `FR02-Run03` | `23127259/newman/fr02/FR02-run-03.{json,html}` |
| FR10 canonical run | `FR10-Run04` | `23127259/evidence/fr10/newman/FR10-run04.*` |
| FR14 canonical run | **`FR14-Run01`** (NOT Run05) | `23127259/evidence/fr14/newman/FR14-run01.*` |
| FR14 usable AI | 40 | TC-034 and TC-036 rejected |
| FR14 Human extensions | **6** (TC-H01..H06; H07 rejected) | `FR14_HUMAN_TEST_CASES.md` |
| FR14 formal count | **46** | `fr14_canonical_cases.json` |
| FR14 confirmed normative bugs | **5** | BUG-FR14-001..005 |
| FR14 exploratory observations | 1 | TC-FR14-H01 (Content-Type HTTP 500; not a separate bug) |
| GitHub Issues filed | #1/#2/#3 (FR02), #29/#30/#31 (FR10), #32/#33/#34 (FR14) | live |
| GitHub Issues pending | 2 (BUG-FR14-004, BUG-FR14-005) | `GH_AUTH_REQUIRED` |
| Run01 HTTP requests | 60 | raw JSON `run.stats.requests.total` |
| Run01 pm.test() assertions | 70 | raw JSON |
| Run01 failed assertions | 13 | mapped to 5 confirmed bugs + 6 exploratory + 2 part-of-bug |
| Run01 exit code | 1 (PIPESTATUS[0]) | `FR14-run01-exitcode.txt` |

---

## FR02 – Login / Account Lockout

| Item | Expected Path | What the screenshot must prove |
|---|---|---|
| Console screenshot (Run03) | `23127259/evidence/postman/FR02_POSTMAN_CONSOLE_SCREENSHOT.png` | Postman Console shows outgoing requests with `X-Student-Id: 23127259` header on every request. |
| Runner screenshot (Run03) | `23127259/evidence/postman/FR02_POSTMAN_RUNNER_SCREENSHOT.png` | Postman Runner green/red pass-fail view of FR02 canonical collection. Must show 56 HTTP operations, 71 assertions, and the 4 red assertions corresponding to 3 confirmed bugs (+1 exploratory). |
| Newman CLI/JSON/HTML | `23127259/newman/fr02/FR02-run-03.{json,html}` | Public-safe, sanitized Newman outputs. Codex should re-open the HTML and visually verify the table shows expected case names and pass/fail counts. |
| Bug #1 screenshot | PENDING_CODEX | Visible plaintext password leak in `/api/users` response. |
| Bug #2 screenshot | PENDING_CODEX | Multiple `/api/login` attempts without rate-limit / lockout escalation. |
| Bug #3 screenshot | PENDING_CODEX | Account-lockout counter reset observation (exploratory). |

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## FR10 – Order State Machine

| Item | Expected Path | What the screenshot must prove |
|---|---|---|
| Console screenshot (Run04) | `23127259/evidence/postman/FR10_POSTMAN_CONSOLE_SCREENSHOT.png` | Postman Console for Run04 (canonical Run04). Must show `X-Student-Id: 23127259` on every request. |
| Runner screenshot (Run04) | `23127259/evidence/postman/FR10_POSTMAN_RUNNER_SCREENSHOT.png` | Runner view of FR10 collection Run04. Must show 176 HTTP operations, 176 assertions, 12 red assertions corresponding to 3 confirmed normative bugs. |
| Newman CLI/JSON/HTML | `23127259/evidence/fr10/newman/FR10-run04.{txt,json,html}` (disclosure-controlled public-safe copies present) | Sanitized Newman outputs. |
| Bug #29 screenshot | PENDING_CODEX | Server allows confirmed → cancelled transition (RBAC bypass for owner; canonical TC `FR10-AI-007`). |
| Bug #30 screenshot | PENDING_CODEX | Non-existent order status update returns 200 with echoed payload (TC `FR10-AI-034`). |
| Bug #31 screenshot | PENDING_CODEX | Delivered order can be re-shipped (TC `FR10-AI-033`). |
| Historical Run03 evidence | `23127259/evidence/fr10/newman/FR10-run03.{cli,json,html}` | Historical; must be **excluded** from final visual evidence. |

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## FR14 – Category CRUD (canonical run: Run01)

| Item | Expected Path | What the screenshot must prove |
|---|---|---|
| Console screenshot (Run01) | `23127259/evidence/postman/FR14_POSTMAN_CONSOLE_SCREENSHOT.png` | Postman Console for canonical Run01. Must show `X-Student-Id: 23127259` on every HTTP operation including helpers and `pm.sendRequest` calls. |
| Runner screenshot (Run01) | `23127259/evidence/postman/FR14_POSTMAN_RUNNER_SCREENSHOT.png` | Runner view of FR14 canonical collection. Must show 60 HTTP operations and 70 `pm.test()` assertions. |
| Newman CLI/JSON/HTML | `23127259/evidence/fr14/newman/FR14-run01.{cli,json,html}` (and `FR14-run01-sanitized.{json,html}`) | Sanitized public-safe outputs. |
| Bug #32 screenshot | PENDING_CODEX | Non-admin `customer` role mutates categories (TC `TC-FR14-012`). |
| Bug #33 screenshot | PENDING_CODEX | Empty / null / whitespace / missing name accepted on POST `/api/categories` (TCs `TC-FR14-016..019`). |
| Bug #34 screenshot | PENDING_CODEX | Nonexistent category PUT/DELETE returns 200 with stale payload (TCs `TC-FR14-024`, `TC-FR14-025`). |
| BUG-FR14-004 screenshot | PENDING_CODEX (Issue pending) | Empty PUT body corrupts existing category name to `null` (TC `TC-FR14-H05`). |
| BUG-FR14-005 screenshot | PENDING_CODEX (Issue pending) | PUT/DELETE on already-deleted category returns false-success (TCs `TC-FR14-037`, `TC-FR14-038`). |
| Exploratory TC-H01 | NO screenshot needed | Content-Type HTTP 500 is exploratory; not a confirmed defect. |

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## CI/CD

| Run | URL | Run ID | SHA | Expected Visual |
|---|---|---|---|---|
| PASS | `GH_AUTH_REQUIRED` | `GH_AUTH_REQUIRED` | `GH_AUTH_REQUIRED` | Green Actions run with Newman artifacts uploaded. |
| FAIL | `GH_AUTH_REQUIRED` | `GH_AUTH_REQUIRED` | `GH_AUTH_REQUIRED` | Red Actions run with exactly one failed assertion (deliberate red flag). |

> **GH_AUTH_REQUIRED.** The `gh` CLI authentication is not available in
> this sandbox. The CI operator must run `gh auth login -h github.com`
> (or set `GITHUB_TOKEN`) to perform the first authentic PASS/FAIL run.
> The workflow YAMLs at
> `.github/workflows/hw06-23127259-api-tests.yml` and
> `.github/workflows/hw06-deliberate-red.yml` are committed and ready to
> trigger. Until the first authentic run is created, the run URL / ID /
> SHA remain `GH_AUTH_REQUIRED` and the PASS/FAIL screenshots remain
> `PENDING_CODEX_VISUAL_AUDIT` by transitive dependency.

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## AI Test-Generator Diagram

| Item | Path | What must be verified |
|---|---|---|
| Content specification | [`23127259/docs/AI_TEST_GENERATOR_DIAGRAM_SPEC.md`](../../docs/AI_TEST_GENERATOR_DIAGRAM_SPEC.md) | This file defines the exact nodes, edges, and labels. |
| Visual file | PENDING_CODEX_VISUAL_TASK | The final image should be saved as `23127259/docs/AI_TEST_GENERATOR_DIAGRAM.{png|svg|pdf}`. It must NOT be AI-generated. |
| Self-drawn declaration | Required | The diagram must be self-drawn (or hand-coded) per assignment policy. Codex should record the authorship declaration. |

**Visual status: PENDING_CODEX_VISUAL_TASK**

---

## PDF Deliverables

| PDF | Source content | Visual status |
|---|---|---|
| `23127259/pdf/HW06_Main_Report.pdf` | Generated from `00_MAIN_REPORT.md` | PENDING_CODEX_VISUAL_AUDIT |
| `23127259/pdf/HW06_AI_AUDIT.pdf` | Generated from `ai/AI_AUDIT_REPORT.md` | PENDING_CODEX_VISUAL_AUDIT |
| `23127259/pdf/HW06_AI_CRITIQUE.pdf` | Generated from `ai/AI_CRITIQUE.md` | PENDING_CODEX_VISUAL_AUDIT |

Codex should open each PDF and verify page-by-page:
- no truncated headings
- no missing tables
- no leaked secret values
- no broken figure references
- no wrong-FR labels

---

## Excel Workbook

| Item | Path | Visual inspection required |
|---|---|---|
| Workbook | [`23127259/excel/HW06_Test_Cases.xlsx`](../../excel/HW06_Test_Cases.xlsx) | Sheets: Cover, FR02_Login (41 rows = header + 40 cases), FR10_Orders (47), FR14_Categories (47), Summary, Bugs (11 rows = header + 10 bugs) |

Codex should visually inspect:
- header formatting
- row counts matching the summary
- bug sheet columns (10 bugs: FR02 3, FR10 3, FR14 5)
- hyperlinks (if any)

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## Known Bad / Historical Images

These paths must **NOT** be used as final visual evidence:

- `23127259/evidence/postman/FR10_HON_RUN03_HISTORICAL.png` (historical FR10 Run03)
- Any image with `PLACEHOLDER`, `TODO`, or zero-byte size
- Any image whose SHA-256 duplicates an unrelated feature image
- Synthetic Mockaroo JSON previews (those are textual, not visual, and must
  not be presented as screenshots)
- Any image labelled as `Run05` for FR14 — **Run05 does not exist**;
  the canonical FR14 run is **Run01**.

---

## Final Visual Tasks Checklist

- [ ] FR02 Console screenshot inspect/recapture
- [ ] FR02 Runner screenshot inspect/recapture
- [ ] FR02 Bug #1/#2/#3 screenshots inspect/recapture
- [ ] FR10 Console (Run04) screenshot inspect/recapture
- [ ] FR10 Runner (Run04) screenshot inspect/recapture
- [ ] FR10 Bug #29/#30/#31 screenshots inspect/recapture
- [ ] FR14 Console (Run01) screenshot inspect/recapture
- [ ] FR14 Runner (Run01) screenshot inspect/recapture
- [ ] FR14 Bug #32/#33/#34 screenshots inspect/recapture
- [ ] FR14 BUG-FR14-004 screenshot inspect/recapture (after Issue created)
- [ ] FR14 BUG-FR14-005 screenshot inspect/recapture (after Issue created)
- [ ] CI PASS screenshot inspect/capture (after authentic run)
- [ ] CI FAIL screenshot inspect/capture (after authentic run)
- [ ] AI test-generator diagram rendering/inspection
- [ ] Excel visual inspection
- [ ] PDF page-by-page visual inspection
- [ ] Final image duplicate / wrong-FR / secret leak audit

---

## Notes for Codex

- Always verify `X-Student-Id: 23127259` is visible on every request in
  Console screenshots; if a screenshot predates this header, recapture.
- Never replace a screenshot with a placeholder or mocked PNG; flag it as
  `MISSING` and trigger recapture.
- Document every image replacement or recapture in
  `23127259/audit/POSTMAN_IMAGE_FORENSIC_AUDIT.md` with before/after SHA-256.
- Visual PASS is the only state that flips `PENDING_CODEX_VISUAL_AUDIT` to
  `PASS` for visual-only requirements. Technical PASS/FAIL has already been
  determined.
- The canonical FR14 run is **Run01**, NOT Run05. Any pre-existing path
  referencing `FR14-run05-*` is stale and must not be used.
- BUG-FR14-004 is **CONFIRMED_NORMATIVE_BUG** (TC-FR14-H05 empty PUT body
  corrupts existing name; FR-14 explicit rule treats corruption as
  normative). BUG-FR14-005 is **CONFIRMED_NORMATIVE_BUG** (TC-FR14-037/038
  already-deleted entity PUT/DELETE returns false-success; FR-14 CRUD
  integrity is normative). Both have prepared issue bodies but require
  `gh` auth or a GitHub PAT to POST.
- TC-FR14-H01 (missing Content-Type → HTTP 500) is **EXPLORATORY**, NOT
  a bug; no screenshot required for it.