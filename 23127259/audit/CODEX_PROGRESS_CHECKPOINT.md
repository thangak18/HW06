# HW06 Codex Progress Checkpoint

## Timestamp

2026-09-02 16:10:01 +0700 (Asia/Ho_Chi_Minh)

## Current Phase

Phase 3 - read-only FR14 candidate audit and selective integration planning.

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
- Verified FR10 immutable provenance and evidence hashes exactly match the expected raw draft, Run03 CLI/JSON/HTML, and strict CLI/JSON/HTML values.
- Recalculated FR10 accounting: 42 raw and audited; 38 VALID, 1 INVALID, 3 INCOMPLETE; 41 usable AI-derived; 5 Human; 46 canonical executable cases.
- Found and repaired a previously missed semantic ID shift: raw `FR10-AI-006` is Admin pending cancellation and raw `FR10-AI-007` is owner User confirmed cancellation. The derived suite/collection had them swapped.
- Preserved Run03 unchanged, repaired canonical JSON/final suite/collection/traceability/validators, and obtained 46/46 canonical static matches with every current FR10 validator passing.
- Executed corrected canonical FR10 Run04 with trustworthy Bash `PIPESTATUS[0]`: 176 requests, 176 assertions, 164 passed, 12 failed, 0 request/script/harness failures, exit 1.
- Reconciled all 46 Run04 formal IDs: 38 PASS, 6 normative FAIL, 2 exploratory observations, 0 blocked.
- Created disclosure-controlled Run04 JSON/HTML because raw Newman exports serialize live JWTs; verified final evidence contains no JWT/Bearer pattern and removed the untracked secret-bearing temp files.
- Rewrote FR10 confirmation, screenshot-authenticity, bug-reference, Run04 reconciliation, and final-audit documents. FR10 final gate is `FR10_COMPLETE`.
- Fetched and inspected FR14 branches/worktrees read-only: only `origin/thang/fr14-anti` exists at `75203b4`; no `fr14-final` branch exists. The Anti worktree contains substantial uncommitted Run02 and oracle-repair work that must be audited and selectively integrated.
- Completed the FR14 Level-1 candidate audit: Category GET is public; POST/PUT/DELETE are Admin-only under FR-12/SEC-03 and require valid JWT under SEC-02; category name is mandatory/non-empty; duplicate names, exact error/status codes, exact response schemas, invalid-ID codes, content negotiation, and referential integrity are not explicitly specified.
- Verified candidate raw draft: 42 continuous AI cases, SHA-256 `95ac502b0880efcc1c6ceb040a1171eeacebff5c262a5f6df8d49a86cadcaf70`.
- Classified Anti artifacts: raw generation VERIFIED_COMPLETE; requirement analysis/audit/canonical/collection VERIFIED_PARTIAL; Run01 historical with untrustworthy manually written exit proof and exposed secrets; uncommitted Run02 historical with mixed weak oracles and exposed secrets; screenshot attempts INVALID/STALE (one shows Chrome/Facebook, others show FR02 or incomplete Runner setup rather than FR14 results).
- Senior QA integration decision: reject raw Run01/Run02 and all candidate screenshots as final evidence; preserve candidate branch/worktree unchanged; reconstruct selected verified FR14 artifacts on the primary branch using honest generation -> audit -> extension -> execution commits.
- Integrated the immutable FR14 raw draft and completed a fresh Human Audit of all 42 cases: 3 VALID, 2 INVALID, 37 INCOMPLETE, 40 usable after corrections. `TC-FR14-034` (duplicate/mislabelled IDOR) and `TC-FR14-036` (unspecified destructive referential test) are rejected.

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

Raw AI: 42
Audited: 42
VALID: 38
INVALID: 1 (`FR10-AI-012`)
INCOMPLETE: 3
Usable AI: 41
Human: 5
Formal: 46
PASS: 38 formal cases in corrected Run04
FAIL: 6 normative formal cases in corrected Run04
BLOCKED: 0
Bugs: 3
Issues: #29, #30, #31 (live; permanent commit-backed native screenshots embedded and verified)

## FR14 Canonical Accounting

Raw AI: 42
Audited: 42
VALID: 3
INVALID: 2
INCOMPLETE: 37
Usable AI: 40
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
- `FR10-run04.json` - `de73cc49094f7bdcea1db88f3f7f9c5369f973cf227d5b4efad192f6d1f81b99`; disclosure-controlled canonical replacement, 176 requests/176 assertions.
- `FR10-run04-cli.txt` - `482ffbc833cccf678f3a0fd87e93f6af6e19f1cd825ea2c36edbfd35389c6635`.
- `FR10-run04.html` - `52141602b2933640e49b7cde40130b4836c48e33977d26b50319975c9f855de6`.

## Git State

Branch: `thang/hw06-implementation`
HEAD: `b069174`
Last meaningful commit: `b069174 fix(23127259): complete FR10 canonical replacement and evidence`
Working tree clean: NO
Uncommitted paths: interrupted AI-audit files, three FR10 screenshots, and this checkpoint.

## External State

SUT: Reachable through genuine FR02 and FR10 Postman Desktop Runner executions on `http://localhost:3000`.
Postman: Live Desktop 11.89.0 controlled through Computer Use; FR02 native run and screenshots complete; FR10 strict run remains open and verified.
GitHub Actions: NOT_YET_VERIFIED.
Issues: FR02 #1/#2/#3 and FR10 #29/#30/#31 verified live and updated in place with permanent native screenshot embeds.

## Known Problems / Risks

- Historical Run03 and strict JSON/HTML contain resolved runtime tokens. They remain immutable by instruction and require explicit legacy-risk documentation; final Run04 is disclosure-controlled.
- FR14 Human Audit is repaired; Human gap analysis/extension selection, canonical suite, and collection still need reconstruction. Candidate Human H07 depends on rejected TC-FR14-036 and will be excluded.
- Candidate Run01/Run02 JSON/HTML expose resolved JWTs and passwords and will not be integrated as final evidence.
- Existing AI-interaction logs contain pending transcript backfills that require evidence-based resolution without invention.

## Remaining Work

- [x] Extract and visually review all relevant assignment requirements.
- [x] Complete independent FR02 audit and repairs.
- [x] Complete independent FR10 audit and distinct native evidence repair.
- [ ] Implement and execute FR14 end to end.
- [ ] Complete AI compliance, critique, diagram, CI/CD, hygiene, README, and final audits.
- [ ] Commit logical milestones, push the branch, and verify a clean working tree.

## NEXT EXACT ACTION

Commit and push the reconstructed FR14 Human Audit, then audit the seven candidate Human cases against the corrected gap analysis, retain six meaningful cases, exclude H07, and build the 46-case canonical provenance map/final suite in the Human-extension commit.
