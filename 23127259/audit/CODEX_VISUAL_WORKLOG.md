# Codex Visual Worklog

## Ownership Start

- Cross-agent synchronization: COMPLETE
- Sync SHA: `1df132ca1f48efb2d6b1dae86d46d33768e5c7dd`
- Cursor branch/worktree: `thang/cursor-nonvisual` at `/Volumes/Thang/HW06/HW06-cursor-nonvisual`
- Codex scope after sync: visual evidence only
- Cursor scope after sync: non-visual technical/report artifacts

## Stable Technical Inputs

- FR02: 40 formal cases; canonical Run03; 3 confirmed bugs.
- FR10: 46 formal cases; canonical Run04; 3 confirmed bugs.
- FR14: final visual set deferred until Cursor reconfirms the final machine/accounting and root-cause mapping.
- CI: final screenshots deferred until Cursor supplies the accepted PASS and deliberate-FAIL run identities.

## FR02 Pixel Audit

Status: `PASS_COMPLETE`

Every listed file was opened and inspected from its actual pixels rather than accepted by filename.

| Final evidence | SHA-256 | Visible content and authenticity | Secret / duplicate / stale decision | Result |
|---|---|---|---|---|
| `evidence/postman/FR02-postman-console-x-student-id.png` | `ff37fd5cc13d56f37a97df37e4ff5ba0e5afae7ba89d655624d0585f91a55851` | Real Postman Desktop; FR02 login request on `localhost:3000`; expanded request headers visibly show `X-Student-Id: 23127259`. | No JWT, bearer token, or password visible; current and readable. | PASS |
| `evidence/postman/FR02-postman-runner-result.png` | `cc017ada960ad3fa60d4d7523bc8efade654d4abd49eb0cbd2ae8ee37d362f46` | Real Postman Desktop Runner for `FR02_Login_Account_Lockout`, environment `FR02-local`; 71 tests, 67 passed, 4 failed, 0 errors, duration 33s 902ms. | No JWT, bearer token, or password visible; matches canonical Run03 totals. | PASS |
| `bugs/screenshots/FR02/BUG-FR02-001-login-password-exposure.png` | `57b3c3d8af3d5194fe4c5abce34519d2914fea9789059d159bd7416c4c926c9a` | Real Postman Desktop Runner; failed assertion visibly identifies password omission failure for AI028 with HTTP 200. | No JWT visible; distinct bytes. Header shows 5 failures because this is the later evidence-only visual run, not canonical accounting. | PASS WITH NOTE |
| `bugs/screenshots/FR02/BUG-FR02-002-lock-after-30s.png` | `f2cb12236b277a0a718ba21bdbfdc9747eebfa290cd34ad01069cddf2dc95ba0` | Real Postman Desktop Runner; AI021 selected; HTTP 403 after T=32s and failed expected-200 assertion; lock response is visible. | No JWT visible; distinct, focused, and readable. | PASS |
| `bugs/screenshots/FR02/BUG-FR02-003-correct-login-at-n2.png` | `a166792be577e1d9765645f9e12a8ae8d216f2cb7ac540dedf31becf73049840` | Real Postman Desktop Runner; HUM003 selected; correct login at N=2 receives HTTP 403 and the lock response is visible. | No JWT visible; distinct, focused, and readable. | PASS |

No FR02 image required recapture after the sync. The evidence-only 5-failure visual run does not replace or modify canonical Run03 accounting (4 failures).

## FR10 Pixel Audit

Status: `PASS_COMPLETE_AFTER_ONE_RECAPTURE`

Every listed file was opened and inspected from its actual pixels. `BUG-FR10-001-postman-runner.png` also supplies the required overall Runner view because it visibly shows the complete strict-run header and totals.

| Final evidence | SHA-256 | Visible content and authenticity | Secret / duplicate / stale decision | Result |
|---|---|---|---|---|
| `evidence/fr10/FR10-postman-console-x-student-id-smoke.png` | `82286c348e9e8ae48583a704c4c671d96295ecc576549dbd804ff9da1d5cd387` | Recaptured from real Postman Desktop on 2026-09-03. Pixels visibly identify `FR10_Defect_Evidence_Strict`, environment `FR10-local`, a genuine HTTP 200 setup request, and expanded request headers with `X-Student-Id: 23127259`. | Request and response bodies are collapsed; no JWT, bearer token, or password is visible. Replaces the rejected stale image whose pixels showed the FR02 Runner. | PASS |
| `evidence/fr10/bugs/BUG-FR10-001-postman-runner.png` | `139d7c19c0b935392f27006c3e4a045525e3f1b1b87fa6040322fe9154099420` | Real Postman Desktop strict Runner; 19 tests, 11 passed, 8 failed, 0 errors. Visible BUG-FR10-001 rows show owner cancellation during shipping accepted with HTTP 200 and persisted state becoming `canceled`. | No JWT visible; readable; distinct hash. Also accepted as the overall FR10 Runner screenshot. | PASS |
| `evidence/fr10/bugs/BUG-FR10-002-postman-runner.png` | `919825d75d8d1117bd1076457f11d1a384d652b8263143b955018b2979271180` | Real Postman Desktop strict Runner. Visible BUG-FR10-002 rows show Admin mutation from terminal `canceled` to `delivered`, HTTP 200, and persisted forbidden state; FR10-003 rows are also visible lower in the run. | No JWT visible; readable; distinct hash. | PASS |
| `evidence/fr10/bugs/BUG-FR10-003-postman-runner.png` | `80b4a8251bd0c583e82e6ca7d835607ae0f260e52478369fbf7f6be5269a8625` | Real Postman Desktop strict Runner with BUG-FR10-003 action detail selected. The row visibly says User A `(role=user)` mutates the Admin status route; HTTP 200 and `Order status updated` are visible. | No JWT visible; readable; distinct hash; not the former byte-duplicate capture. | PASS |

### FR10 Recapture Record

- Rejected old Console SHA: `0aa5866a6f808b69cba1f09571db2902d6ea5be5d6b2ced0ae632d8396bcb8b9`.
- Rejection reason: actual pixels showed `FR02_Login_Account_Lockout`, `FR02-local`, and `/api/login`; the file was therefore mislabeled/stale as FR10 evidence.
- Replacement source: authentic full-window Postman Desktop capture through Computer Use, without DOM manipulation, compositing, cropping, or synthetic UI generation.
- Replacement dimensions/format: 1228 x 768 PNG.
- Replacement SHA: `82286c348e9e8ae48583a704c4c671d96295ecc576549dbd804ff9da1d5cd387`.

### Historical Synthetic Exclusion

- Everything under `evidence/fr10/bugs/historical-invalid/int053/` remains excluded from final evidence.
- Everything under `evidence/fr10/bugs/historical-invalid/int054/` remains excluded from final evidence.
- None of those files is referenced as a final FR10 Console, Runner, or bug screenshot.

## FR14 Canonical Runner Metric Reconciliation

- Canonical Postman collection request items: 58 (`[.. | objects | select(has("request"))] | length`).
- Canonical Newman HTTP executions: 60 (`run.stats.requests.total`).
- The two additional HTTP executions are legitimate `pm.sendRequest` verification GETs emitted by `TC-FR14-029` and `TC-FR14-H05`.
- The run contains 60 execution records; those two item names each appear twice because the stored request item plus its scripted verification request are both counted.
- Decision: no contradiction and no canonical data change. The correct distinction is 58 stored request items versus 60 actual HTTP operations.

## FR14 Pixel Audit

Status: `PASS_COMPLETE`

The real Postman Desktop run used the separately imported current canonical collection copy, not the stale 49-case / 7-Human collection. The visible collection description states a canonical 46-case suite with 034, 036, and H07 excluded. Environment: `FR14-local`.

| Final evidence | SHA-256 | Actual visible evidence | Final status |
|---|---|---|---|
| `evidence/fr14/FR14-postman-runner-result.png` | `65cc316415efb76c09e0369c8f1812709fb5bf2aa0b4586213f55b8f8e5d3f9b` | Real Postman Desktop Runner; `FR14_Category_CRUD Copy`; `FR14-local`; completed run; 70 tests, 58 passed, 12 failed, 0 errors; Category requests visible. No credential or token is visible. | VALID_FINAL |
| `evidence/fr14/FR14-postman-console-x-student-id.png` | `a7eb1faee23ad8c35dde401c0b4b1d98a07f6543199a7ddb86b44e9be0c65791` | Real Postman Console beneath the same FR14 Runner; public `GET http://localhost:3000/api/categories`; expanded request headers show `X-Student-Id: 23127259`. No Authorization, JWT, bearer value, password, or cookie is visible. | VALID_FINAL |
| `evidence/fr14/bugs/BUG-FR14-001-postman-runner.png` | `9d03d85e62936609f460d7e7947a0b02436cb6ed16e3bc2e480a6fd8f4eb39d4` | Failed-tab view shows TC-FR14-012/013/014 regular-user POST/PUT/DELETE Category mutations all returning HTTP 200 when 4xx is required. Matches BUG-FR14-001 and Issue #32. | VALID_FINAL |
| `evidence/fr14/bugs/BUG-FR14-002-postman-runner.png` | `15919c31baf60b391b694bb53633c1173aeb7e42c30fdfe943f8cc7ffe61c7f0` | TC-FR14-016 invalid empty-name POST is selected; Runner shows HTTP 200 failure and response body `Category created` with an ID. Adjacent invalid-name failures are visible. Matches BUG-FR14-002 and Issue #33. | VALID_FINAL |
| `evidence/fr14/bugs/BUG-FR14-003-postman-runner.png` | `9d3d6c65008d483e75277fbe0a7bed406f69bc04b3136a3b30277f08998bb0b8` | TC-FR14-024 nonexistent-ID PUT is selected; Runner shows `/api/categories/99999`, HTTP 200, false-success assertion failure, and response body `Category updated`; related 025/037/038 manifestations remain visible. Matches BUG-FR14-003 and Issue #34; no separate BUG-FR14-005 image exists. | VALID_FINAL |
| `evidence/fr14/bugs/BUG-FR14-004-postman-runner.png` | `e06a8377bd7b93a209ed5efa1e04e0912342b5ea6d91e490dc6dd269356172e7` | TC-FR14-H05 Empty PUT Body is selected and visible; HTTP 200, `Category updated`, failed no-corruption assertion, and `expected null...` failure context are visible. Matches BUG-FR14-004 and Issue #36. | VALID_FINAL |

All six files were reopened from their final saved PNG bytes. They are readable, authentic, distinct, correctly scoped to FR14, and visually secret-free.

## CI Pixel Audit

Status: `PASS_COMPLETE`

| Final evidence | SHA-256 | Actual visible evidence | Final status |
|---|---|---|---|
| `ci/evidence/CI-PASS-33651923618.png` | `76ad1a1b46a17e9b7cc8aa30044fcaa42117c03af01947436169e5fa850da840` | Genuine GitHub Actions page for public repository `thangak18/HW06`; workflow `HW06 API Tests (23127259)` / `hw06-23127259-api-tests.yml`; commit `fa6eac3`; green `Success`; `api-tests` completed successfully. | VALID_FINAL |
| `ci/evidence/CI-FAIL-33651923391.png` | `cb2156503b20b10ba278c85e4b9eaf9b51dd86e210f7cf83e50b4fc0a496797c` | Genuine GitHub Actions page for `thangak18/HW06`; workflow `HW06 Deliberate Red Sample (23127259)` / `hw06-deliberate-red.yml`; commit `fa6eac3`; red `Failure`; failed job is visibly named `deliberate-red`. Technical logs independently confirm exactly one intentional sentinel assertion and no setup/harness failure. | VALID_FINAL |

Both final screenshots were opened from their saved PNG bytes. Historical invalid green run `33649719887` was not used.

## Concrete Contradictions for Cursor

- Historical CI run 33649719887 is green only because failures were masked; exclude it.
- Canonical FR14 JSON records 12, not 13, failed assertions.
- BUG-FR14-005 duplicates BUG-FR14-003; Issue #37 is closed duplicate of #34.
- FR14 sanitized public files still require Cursor-owned textual secret verification/regeneration.

No new technical contradiction was discovered during the completed FR02/FR10 pixel audit. The stale FR10 Console file was a Codex-owned visual defect and has been repaired in place.

## Remaining Visual Work - Fable Ownership

- Render and inspect the deterministic AI test-generator diagram.
- Visually inspect every required Excel worksheet.
- Render and inspect every PDF page.
- Complete the global all-image forensic audit, final evidence manifest, and compliance cleanup.

## Next Visual Action

Hand off the completed FR02/FR10/FR14/CI visual state to Cursor Fable 5.1. Codex must not continue into diagram, Excel, PDF, global-forensic, manifest, or final-compliance work under the narrowed ownership split.
