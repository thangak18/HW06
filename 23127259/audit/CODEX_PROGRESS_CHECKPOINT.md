# HW06 Codex Progress Checkpoint

## Timestamp

2026-09-02 12:31:42 +0700 (Asia/Ho_Chi_Minh)

## Current Phase

Phase 2 - independent FR10 forensic audit and repair.

## Current Status

IN_PROGRESS

## Completed Verified Work

- Read the complete current task brief.
- Captured the pre-modification Git state and last 30 commits.
- Confirmed branch `thang/hw06-implementation` at `57d6ea59e04c921b138258f8ed7990328f76ef53`, matching the remote tracking branch before this checkpoint.
- Inspected every interrupted FR10 screenshot visually and recorded size, timestamp, format, and SHA-256.
- Confirmed all three files visibly originate from real Postman Desktop Collection Runner output with an actual strict collection run showing 19 tests, 11 passed, 8 failed, and 0 errors.
- Confirmed no JWT is visible in the three inspected images.
- Confirmed `BUG-FR10-002-postman-runner.png` and `BUG-FR10-003-postman-runner.png` are identical bytes; FR10-003 therefore requires a distinct focused native capture before the final authenticity gate.
- Inspected the interrupted uncommitted AI-audit changes. Valid INT-055 backfill material is salvageable; INT-056 remains incomplete and requires exact-output backfill after this work is reconstructed from available artifacts.
- Located the authoritative assignment PDF and SUT API specification; content review is in progress.
- Rendered and visually inspected all eight assignment PDF pages; extracted every gradable requirement into `23127259/audit/HW06_REQUIREMENTS_COMPLIANCE_MATRIX.md`.
- Read the normative SRS sections for FR02, FR10, FR14, and SEC-01 through SEC-07, plus every relevant endpoint definition in `api_specification.md`.
- Confirmed a critical FR14 oracle boundary: duplicate-name behavior, maximum name length, exact response schema, and exact status codes are not specified and cannot be treated as normative failures.
- Independently reconciled FR02: 37 continuous unique raw AI IDs; 37 audited; 16 VALID, 2 INVALID, 19 INCOMPLETE; 35 usable AI-derived plus 5 Human cases; 40 unique formal cases; rejected duplicates absent from execution.
- Parsed FR02 Run03 JSON: 56 HTTP executions, 71 assertions, 67 passed, 4 failed, zero request/script failures, all 40 formal IDs executed, and every emitted request carried `X-Student-Id: 23127259`.
- Visually authenticated the existing FR02 Postman Console and Runner screenshots.
- Rejected the three existing FR02 bug PNGs as final bug-specific evidence: they are Newman HTML views, and the FR02-002/003 files are byte-identical rather than focused native Postman evidence.
- Verified live GitHub Issues #1/#2/#3 exist but currently contain only a "Screenshot Required" placeholder rather than an embedded screenshot; they need updating after authentic files are committed.
- Executed one genuine Postman Desktop Collection Runner run for FR02 visual evidence only and captured three distinct focused bug screenshots without DOM manipulation, image editing, or visible JWT.
- Completed `FR02_FINAL_AUDIT.md` and marked the feature gate `FR02_COMPLETE` based on immutable Newman Run03 accounting plus repaired native evidence.

## FR02 Canonical Accounting

Raw AI: 37
Audited: 37
VALID: 16
INVALID: 2
INCOMPLETE: 19
Usable AI: 35
Human: 5
Formal: 40
PASS: 36 formal cases
FAIL: 3 normative formal cases
BLOCKED: 0
Bugs: 3
Issues: #1, #2, #3 (live; permanent commit-backed native screenshots embedded and verified)

## FR10 Canonical Accounting

Raw AI: NOT_YET_VERIFIED
Audited: NOT_YET_VERIFIED
VALID: NOT_YET_VERIFIED
INVALID: NOT_YET_VERIFIED
INCOMPLETE: NOT_YET_VERIFIED
Usable AI: NOT_YET_VERIFIED
Human: NOT_YET_VERIFIED
Formal: NOT_YET_VERIFIED
PASS: NOT_YET_VERIFIED
FAIL: NOT_YET_VERIFIED
BLOCKED: NOT_YET_VERIFIED
Bugs: NOT_YET_VERIFIED
Issues: NOT_YET_VERIFIED

## FR14 Canonical Accounting

Raw AI: NOT_YET_VERIFIED
Audited: NOT_YET_VERIFIED
VALID: NOT_YET_VERIFIED
INVALID: NOT_YET_VERIFIED
INCOMPLETE: NOT_YET_VERIFIED
Usable AI: NOT_YET_VERIFIED
Human: NOT_YET_VERIFIED
Formal: NOT_YET_VERIFIED
PASS: NOT_YET_VERIFIED
FAIL: NOT_YET_VERIFIED
BLOCKED: NOT_YET_VERIFIED
Bugs: NOT_YET_VERIFIED
Issues: NOT_YET_VERIFIED

## Files Created / Modified

- Created `23127259/audit/CODEX_PROGRESS_CHECKPOINT.md`.
- Pre-existing interrupted modifications preserved without reset:
  - `23127259/ai/AI_AUDIT_REPORT.md`
  - `23127259/ai/interactions/INT-055-fr10-native-postman-runner-evidence.md`
  - `23127259/ai/prompts/AI_PROMPT_LOG.md`
  - `23127259/ai/interactions/INT-056-fr10-native-postman-runner-retry.md`
  - three untracked FR10 native Runner PNGs

## Immutable Evidence

- `BUG-FR10-001-postman-runner.png` - `139d7c19c0b935392f27006c3e4a045525e3f1b1b87fa6040322fe9154099420`; real Postman Runner view visibly including FR10-001 failures.
- `BUG-FR10-002-postman-runner.png` - `919825d75d8d1117bd1076457f11d1a384d652b8263143b955018b2979271180`; real Postman Runner view visibly including FR10-002 and FR10-003 failures.
- `BUG-FR10-003-postman-runner.png` - `80b4a8251bd0c583e82e6ca7d835607ae0f260e52478369fbf7f6be5269a8625`; repaired distinct native Runner capture with FR10-003 detail selected and no JWT.
- `2026.HW06.API Testing_En.pdf` - authoritative eight-page assignment, fully rendered and visually reviewed; no edits made.
- `FR02-run-03.json` - `b76900e1c6b436b1d9467e606ecb0254b1c2c6e462f5d9222a36d3761468f683`; canonical 56-request, 71-assertion run.
- `BUG-FR02-001-login-password-exposure.png` - `57b3c3d8af3d5194fe4c5abce34519d2914fea9789059d159bd7416c4c926c9a`; native Runner assertion, no JWT.
- `BUG-FR02-002-lock-after-30s.png` - `f2cb12236b277a0a718ba21bdbfdc9747eebfa290cd34ad01069cddf2dc95ba0`; native Runner failure/403 response, no JWT.
- `BUG-FR02-003-correct-login-at-n2.png` - `a166792be577e1d9765645f9e12a8ae8d216f2cb7ac540dedf31becf73049840`; native Runner failure/403 response, no JWT.

## Git State

Branch: `thang/hw06-implementation`
HEAD: `d6b1b04` (full SHA to be refreshed after the issue-linkage commit)
Last meaningful commit: `d6b1b04 audit(23127259): finalize FR02 compliance review`
Working tree clean: NO
Uncommitted paths: interrupted AI-audit files, three FR10 screenshots, and this checkpoint.

## External State

SUT: Reachable through genuine FR02 and FR10 Postman Desktop Runner executions on `http://localhost:3000`.
Postman: Live Desktop 11.89.0 controlled through Computer Use; FR02 native run and screenshots complete; FR10 strict run remains open and verified.
GitHub Actions: NOT_YET_VERIFIED.
Issues: FR02 #1/#2/#3 verified live and updated in place with permanent native screenshot embeds; FR10 #29/#30/#31 verified live but still reference stale screenshot hashes.

## Known Problems / Risks

- FR10 screenshot files are now distinct, but all related reports and live Issues still require hash/path reconciliation against the repaired native evidence.
- FR10 raw artifacts and execution evidence have not yet completed independent parsing in this session.
- FR14 has not yet begun and must wait for truthful FR02 and FR10 final gates.
- Existing AI-interaction logs contain pending transcript backfills that require evidence-based resolution without invention.

## Remaining Work

- [x] Extract and visually review all relevant assignment requirements.
- [x] Complete independent FR02 audit and repairs.
- [ ] Complete independent FR10 audit and distinct native evidence repair.
- [ ] Implement and execute FR14 end to end.
- [ ] Complete AI compliance, critique, diagram, CI/CD, hygiene, README, and final audits.
- [ ] Commit logical milestones, push the branch, and verify a clean working tree.

## NEXT EXACT ACTION

Commit and push the verified FR02 GitHub-issue linkage update, then parse FR10 provenance, canonical Run03, strict evidence, student-header coverage, and formal reconciliation directly from raw artifacts.
