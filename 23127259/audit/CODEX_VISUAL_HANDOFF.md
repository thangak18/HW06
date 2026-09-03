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

## FR02 – Login / Account Lockout

| Item | Expected Path | What the screenshot must prove |
|---|---|---|
| Console screenshot (collection) | `23127259/evidence/postman/FR02-postman-console-x-student-id.png` | Real Postman Console shows an FR02 request to localhost with `X-Student-Id: 23127259`. |
| Runner screenshot (collection) | `23127259/evidence/postman/FR02-postman-runner-result.png` | Real Postman Runner shows FR02 collection, FR02-local, 71 assertions, 67 passed, 4 failed, 0 errors. |
| Newman CLI/JSON/HTML | `23127259/newman/fr02/FR02-run-03.{json,html}` | Sanitized Newman outputs. Codex should re-open the HTML and visually verify the table shows expected case names and pass/fail counts. |
| Bug #1 screenshot | `23127259/bugs/screenshots/FR02/BUG-FR02-001-login-password-exposure.png` | Login response exposes plaintext password. |
| Bug #2 screenshot | `23127259/bugs/screenshots/FR02/BUG-FR02-002-lock-after-30s.png` | Correct login remains rejected after the documented 30-second lock expires. |
| Bug #3 screenshot | `23127259/bugs/screenshots/FR02/BUG-FR02-003-correct-login-at-n2.png` | Correct login is rejected after only two failed attempts. |

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## FR10 – Order State Machine

| Item | Expected Path | What the screenshot must prove |
|---|---|---|
| Console screenshot | `23127259/evidence/fr10/FR10-postman-console-x-student-id-smoke.png` | Real Postman Console shows FR10 localhost request and student header. |
| Runner screenshot (Run04) | `23127259/evidence/postman/FR10_POSTMAN_RUNNER_SCREENSHOT.png` | Runner view of FR10 collection Run04. Must show 176 HTTP operations, 12 red assertions corresponding to 3 confirmed normative bugs. |
| Newman CLI/JSON/HTML | `23127259/evidence/fr10/newman/public-safe/FR10-run04-*.{txt,json,html}` | Sanitized Newman outputs. HTML must show case names, methods, statuses, pass/fail. |
| Bug #29 screenshot | `23127259/evidence/fr10/bugs/BUG-FR10-001-postman-runner.png` | Owner User cancels a shipping order; HTTP 200 and persisted canceled state. |
| Bug #30 screenshot | `23127259/evidence/fr10/bugs/BUG-FR10-002-postman-runner.png` | Canceled terminal order transitions to delivered. |
| Bug #31 screenshot | `23127259/evidence/fr10/bugs/BUG-FR10-003-postman-runner.png` | Normal `role=user` token mutates order status through Admin route. |
| Historical Run03 evidence | `23127259/evidence/postman/FR10_HON_RUN03_HISTORICAL.png` | Historical run captured before the canonical correction; must be **excluded** from final visual evidence. Codex must visually confirm it is not used as primary evidence. |

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## FR14 – Category CRUD (canonical run: Run01)

| Item | Expected Path | What the screenshot must prove |
|---|---|---|
| Console screenshot (Run01) | `23127259/evidence/postman/FR14_POSTMAN_CONSOLE_SCREENSHOT.png` | Postman Console for canonical Run01. Must show `X-Student-Id: 23127259` on every HTTP operation including helpers and `pm.sendRequest` calls. |
| Runner screenshot (Run01) | `23127259/evidence/postman/FR14_POSTMAN_RUNNER_SCREENSHOT.png` | Runner view of FR14 canonical collection. Must show 60 HTTP operations and 70 `pm.test()` assertions. |
| Newman CLI/JSON/HTML | `23127259/evidence/fr14/newman/FR14-run01.{cli,json,html}` (and `FR14-run01-sanitized.{json,html}`) | Sanitized public-safe outputs. |
| Bug #32 screenshot | PENDING_CODEX | Non-admin `customer` role mutates categories (TC `TC-FR14-014`). |
| Bug #33 screenshot | PENDING_CODEX | Empty / null / whitespace / missing name accepted on POST `/api/categories` (TCs `TC-FR14-016..019`). |
| Bug #34 screenshot | PENDING_CODEX | False-success for nonexistent/already-deleted category PUT/DELETE (TCs `TC-FR14-024`, `025`, `037`, `038`). Issue #37 is a closed duplicate. |
| BUG-FR14-004 screenshot | PENDING_CODEX_VISUAL_AUDIT (Issue [#36](https://github.com/thangak18/HW06/issues/36) live) | Empty PUT body corrupts existing category name to `null` (TC `TC-FR14-H05`). |
| Exploratory TC-H01 | NO screenshot needed | Content-Type HTTP 500 is exploratory; not a confirmed defect. |

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## CI/CD

| Run | URL | Run ID | SHA | Expected Visual |
|---|---|---|---|---|
| PASS | https://github.com/thangak18/HW06/actions/runs/33651923618 | 33651923618 | `fa6eac3` | Green run: SUT healthy, 9 requests, 10/10 assertions passed, 0 harness errors. |
| FAIL | https://github.com/thangak18/HW06/actions/runs/33651923391 | 33651923391 | `fa6eac3` | Red run: same healthy harness, exactly one named DELIBERATE_RED assertion failure. |

Run `33649719887` is superseded and must not be used as PASS evidence because its green conclusion masked a missing FR10 collection and FR14 assertion failures.

Screenshots remain `PENDING_CODEX_VISUAL_AUDIT` for the two final runs.

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
| Workbook | [`23127259/excel/HW06_Test_Cases.xlsx`](../../excel/HW06_Test_Cases.xlsx) | Sheets: Cover, FR02_Login (41 rows), FR10_Orders (47), FR14_Categories (47), Summary, Bugs (11 rows = header + 10 distinct bugs) |

Codex should visually inspect:
- header formatting
- row counts matching the summary (40 / 46 / 46 formal cases; 10 distinct bugs total: FR02 3, FR10 3, FR14 4)
- bug sheet columns
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
  normative). GitHub Issue [#36](https://github.com/thangak18/HW06/issues/36) is live.
- TC-FR14-037/038 are manifestations of BUG-FR14-003, the same false-success-on-no-entity root cause as TC-FR14-024/025. Issue [#37](https://github.com/thangak18/HW06/issues/37) is closed as duplicate of [#34](https://github.com/thangak18/HW06/issues/34).
- TC-FR14-H01 (missing Content-Type → HTTP 500) is **EXPLORATORY**, NOT
  a bug; no screenshot required for it.
