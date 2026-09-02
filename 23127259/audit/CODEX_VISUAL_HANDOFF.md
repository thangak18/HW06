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
| Console screenshot (collection) | `23127259/evidence/postman/FR02_POSTMAN_CONSOLE_SCREENSHOT.png` | Postman Console shows outgoing requests with `X-Student-Id: 23127259` header on every request (login attempts, lockout, register, recovery). |
| Runner screenshot (collection) | `23127259/evidence/postman/FR02_POSTMAN_RUNNER_SCREENSHOT.png` | Postman Runner green/red pass-fail view of FR02 collection. Must show non-zero iterations, an `X-Student-Id` column or pre-request script trace, and green assertions. |
| Newman CLI/JSON/HTML | `23127259/evidence/fr02/newman/public-safe/FR02-run02-*.{txt,json,html}` | Public-safe, sanitized Newman outputs. Codex should re-open the HTML and visually verify the table shows expected case names and pass/fail counts. |
| Bug #1 screenshot | PENDING_CODEX | Visible plaintext password leak in `/api/users` response. |
| Bug #2 screenshot | PENDING_CODEX | Multiple `/api/login` attempts without rate-limit / lockout escalation. |
| Bug #3 screenshot | PENDING_CODEX | Account-lockout counter reset observation (exploratory). |

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## FR10 – Order State Machine

| Item | Expected Path | What the screenshot must prove |
|---|---|---|
| Console screenshot (Run04) | `23127259/evidence/postman/FR10_POSTMAN_CONSOLE_SCREENSHOT.png` | Postman Console for Run04 (canonical Run04). Must show `X-Student-Id: 23127259` on every request. |
| Runner screenshot (Run04) | `23127259/evidence/postman/FR10_POSTMAN_RUNNER_SCREENSHOT.png` | Runner view of FR10 collection Run04. Must show 176 HTTP operations, 12 red assertions corresponding to 3 confirmed normative bugs. |
| Newman CLI/JSON/HTML | `23127259/evidence/fr10/newman/public-safe/FR10-run04-*.{txt,json,html}` | Sanitized Newman outputs. HTML must show case names, methods, statuses, pass/fail. |
| Bug #29 screenshot | PENDING_CODEX | Owner cancels confirmed order despite RBAC (canonical TC `FR10-AI-007`). |
| Bug #30 screenshot | PENDING_CODEX | Non-existent order status update returns 200 with echoed payload (TC `FR10-AI-034`). |
| Bug #31 screenshot | PENDING_CODEX | Delivered order can be re-shipped (TC `FR10-AI-033`). |
| Historical Run03 evidence | `23127259/evidence/postman/FR10_HON_RUN03_HISTORICAL.png` | Historical run captured before the canonical correction; must be **excluded** from final visual evidence. Codex must visually confirm it is not used as primary evidence. |

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## FR14 – Category CRUD

| Item | Expected Path | What the screenshot must prove |
|---|---|---|
| Console screenshot (Run05) | `23127259/evidence/postman/FR14_POSTMAN_CONSOLE_SCREENSHOT.png` | Postman Console for canonical Run05. Must show `X-Student-Id: 23127259` on every HTTP operation including helpers and `pm.sendRequest` calls. |
| Runner screenshot (Run05) | `23127259/evidence/postman/FR14_POSTMAN_RUNNER_SCREENSHOT.png` | Runner view of FR14 canonical collection. Must show 58 HTTP operations and 70 `pm.test()` assertions. |
| Newman CLI/JSON/HTML | `23127259/evidence/fr14/newman/public-safe/FR14-run05-*.{txt,json,html}` | Sanitized public-safe outputs. |
| Bug #32 screenshot | PENDING_CODEX | Non-admin `customer` role mutates categories (TC `TC-FR14-014`). |
| Bug #33 screenshot | PENDING_CODEX | Empty / whitespace / null name accepted on POST `/api/categories` (TCs `TC-FR14-018..022`). |
| Bug #34 screenshot | PENDING_CODEX | Update/Delete on non-existent category returns 200 with stale payload (TCs `TC-FR14-029b / TC-FR14-031`). |
| Bug #TBD screenshot | PENDING_CODEX | Empty PUT body returns HTTP 500 (TC `TC-FR14-040`; non-normative robustness). |

**Visual status: PENDING_CODEX_VISUAL_AUDIT**

---

## CI/CD

| Run | URL | Run ID | SHA | Expected Visual |
|---|---|---|---|---|
| PASS | PENDING_AUTHENTIC_GH_RUN | PENDING_AUTHENTIC_GH_RUN | PENDING_AUTHENTIC_GH_RUN | Green Actions run with Newman artifacts uploaded. |
| FAIL | PENDING_AUTHENTIC_GH_RUN | PENDING_AUTHENTIC_GH_RUN | PENDING_AUTHENTIC_GH_RUN | Red Actions run with exactly one failed assertion (deliberate red flag). |

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
| Workbook | [`23127259/excel/HW06_Test_Cases.xlsx`](../../excel/HW06_Test_Cases.xlsx) | Sheets: Cover, FR02_Login, FR10_Orders, FR14_Categories, Summary, Bugs |

Codex should visually inspect:
- header formatting
- row counts matching the summary (40 / 46 / 46)
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

---

## Final Visual Tasks Checklist

- [ ] FR02 Console screenshot inspect/recapture
- [ ] FR02 Runner screenshot inspect/recapture
- [ ] FR02 Bug #1/#2/#3 screenshots inspect/recapture
- [ ] FR10 Console (Run04) screenshot inspect/recapture
- [ ] FR10 Runner (Run04) screenshot inspect/recapture
- [ ] FR10 Bug #29/#30/#31 screenshots inspect/recapture
- [ ] FR14 Console (Run05) screenshot inspect/recapture
- [ ] FR14 Runner (Run05) screenshot inspect/recapture
- [ ] FR14 Bug #32/#33/#34 + #TBD screenshots inspect/recapture
- [ ] CI PASS screenshot inspect/capture
- [ ] CI FAIL screenshot inspect/capture
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