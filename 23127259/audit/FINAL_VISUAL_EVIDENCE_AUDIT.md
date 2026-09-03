# Final Visual Evidence Audit — HW06 23127259

> **Auditor:** Fable (Cursor Fable 5.1, Final Visual-Closure Agent)
> **Date:** 2026-09-03
> **Scope:** All grader-facing images in `23127259/`
> **Method:** Pixel inspection via actual image read, hash verification against
> Codex documented SHAs, and visual content analysis.

---

## Audit Summary

| Category | Count |
|---|---:|
| Logical grader-facing evidence slots | 19 |
| Distinct physical final image files | 18 |
| VALID_FINAL logical slots | 19 |
| VALID_FINAL (historical) | 0 |
| Historical excluded (int053/int054 synthetic) | 0 in final set |
| Wrong FR | 0 |
| Wrong bug | 0 |
| Duplicate-insufficient | 0 |
| Secret-exposed | 0 |
| Synthetic final evidence | 0 |
| Standalone BUG-FR14-005 screenshot | 0 (consolidated into BUG-FR14-003) |

---

## FR02 Images

| Path | Intended FR | Actual FR | Purpose | Visible Evidence | SHA-256 | Authentic | Secret-Free | Status |
|---|---|---|---|---|---|---|---|---|
| `evidence/postman/FR02-postman-console-x-student-id.png` | FR02 | FR02 | Console + X-Student-Id | Real Postman Desktop; FR02 login request; expanded headers with `X-Student-Id: 23127259` | `ff37fd5cc13d56f37a97df37e4ff5ba0e5afae7ba89d655624d0585f91a55851` | YES | YES | **VALID_FINAL** |
| `evidence/postman/FR02-postman-runner-result.png` | FR02 | FR02 | Runner overview | Real Postman Desktop Runner; `FR02_Login_Account_Lockout`; 71 tests, 67 passed, 4 failed, 0 errors | `cc017ada960ad3fa60d4d7523bc8efade654d4abd49eb0cbd2ae8ee37d362f46` | YES | YES | **VALID_FINAL** |
| `bugs/screenshots/FR02/BUG-FR02-001-login-password-exposure.png` | FR02 | FR02 | Bug #1 evidence | Real Postman Runner; failed password-omission assertion identifies FR02-AI-028 with HTTP 200. The credential value itself is not displayed. | `57b3c3d8af3d5194fe4c5abce34519d2914fea9789059d159bd7416c4c926c9a` | YES | YES | **VALID_FINAL** |
| `bugs/screenshots/FR02/BUG-FR02-002-lock-after-30s.png` | FR02 | FR02 | Bug #2 evidence | Real Postman Runner; FR02-AI-021 selected; HTTP 403 after T=32s; lock response visible | `f2cb12236b277a0a718ba21bdbfdc9747eebfa290cd34ad01069cddf2dc95ba0` | YES | YES | **VALID_FINAL** |
| `bugs/screenshots/FR02/BUG-FR02-003-correct-login-at-n2.png` | FR02 | FR02 | Bug #3 evidence | Real Postman Runner; FR02-HUM-003 selected; HTTP 403 at N=2; lock response visible | `a166792be577e1d9765645f9e12a8ae8d216f2cb7ac540dedf31becf73049840` | YES | YES | **VALID_FINAL** |

---

## FR10 Images

| Path | Intended FR | Actual FR | Purpose | Visible Evidence | SHA-256 | Authentic | Secret-Free | Status |
|---|---|---|---|---|---|---|---|---|
| `evidence/fr10/FR10-postman-console-x-student-id-smoke.png` | FR10 | FR10 | Console + X-Student-Id | Real Postman Desktop; `FR10_Defect_Evidence_Strict`; HTTP 200 setup request; headers with `X-Student-Id: 23127259`. Replaced the stale image whose pixels showed FR02 Runner. | `82286c348e9e8ae48583a704c4c671d96295ecc576549dbd804ff9da1d5cd387` | YES | YES | **VALID_FINAL** |
| `evidence/fr10/bugs/BUG-FR10-001-postman-runner.png` | FR10 | FR10 | Bug #29 + Runner | Real Postman strict Runner; 19 tests, 11 passed, 8 failed, 0 errors; owner cancellation during shipping visible; HTTP 200 and `canceled` state | `139d7c19c0b935392f27006c3e4a045525e3f1b1b87fa6040322fe9154099420` | YES | YES | **VALID_FINAL** |
| `evidence/fr10/bugs/BUG-FR10-002-postman-runner.png` | FR10 | FR10 | Bug #30 evidence | Real Postman strict Runner; Admin mutation from `canceled` to `delivered` visible; HTTP 200; forbidden state persisted | `919825d75d8d1117bd1076457f11d1a384d652b8263143b955018b2979271180` | YES | YES | **VALID_FINAL** |
| `evidence/fr10/bugs/BUG-FR10-003-postman-runner.png` | FR10 | FR10 | Bug #31 evidence | Real Postman strict Runner; User `(role=user)` mutates Admin route visible; HTTP 200 and `Order status updated` | `80b4a8251bd0c583e82e6ca7d835607ae0f260e52478369fbf7f6be5269a8625` | YES | YES | **VALID_FINAL** |

---

## FR14 Images

| Path | Intended FR | Actual FR | Purpose | Visible Evidence | SHA-256 | Authentic | Secret-Free | Status |
|---|---|---|---|---|---|---|---|---|
| `evidence/fr14/FR14-postman-console-x-student-id.png` | FR14 | FR14 | Console + X-Student-Id | Real Postman Desktop; `FR14_Category_CRUD Copy`; GET `http://localhost:3000/api/categories`; status 200 OK; headers with `X-Student-Id: 23127259` | `a7eb1faee23ad8c35dde401c0b4b1d98a07f6543199a7ddb86b44e9be0c65791` | YES | YES | **VALID_FINAL** |
| `evidence/fr14/FR14-postman-runner-result.png` | FR14 | FR14 | Runner overview | Real Postman Runner; `FR14_Category_CRUD Copy`; environment `FR14-local`; UI summary shows 70 tests/assertions, 58 passed, 12 failed, 0 errors. These cover 46 formal cases, 58 stored request items, and 60 HTTP operations including 2 scripted verification GETs. | `65cc316415efb76c09e0369c8f1812709fb5bf2aa0b4586213f55b8f8e5d3f9b` | YES | YES | **VALID_FINAL** |
| `evidence/fr14/bugs/BUG-FR14-001-postman-runner.png` | FR14 | FR14 | Bug #32 evidence | Real Postman Runner; TC-FR14-012/013/014 selected; `role=user` mutates category with HTTP 200 visible | `9d03d85e62936609f460d7e7947a0b02436cb6ed16e3bc2e480a6fd8f4eb39d4` | YES | YES | **VALID_FINAL** |
| `evidence/fr14/bugs/BUG-FR14-002-postman-runner.png` | FR14 | FR14 | Bug #33 evidence | Real Postman Runner; TC-FR14-016/017/018/019 selected; empty/null/whitespace name accepted visible | `15919c31baf60b391b694bb53633c1173aeb7e42c30fdfe943f8cc7ffe61c7f0` | YES | YES | **VALID_FINAL** |
| `evidence/fr14/bugs/BUG-FR14-003-postman-runner.png` | FR14 | FR14 | Bug #34 evidence (covers TC-024/025/037/038) | Real Postman Runner; TC-FR14-024 selected; nonexistent ID PUT returns HTTP 200 visible. Also covers TC-FR14-037/038 (already-deleted ID, same root cause). | `9d3d6c65008d483e75277fbe0a7bed406f69bc04b3136a3b30277f08998bb0b8` | YES | YES | **VALID_FINAL** |
| `evidence/fr14/bugs/BUG-FR14-004-postman-runner.png` | FR14 | FR14 | Bug #36 evidence | Real Postman Runner; TC-FR14-H05 selected; empty PUT body corrupts existing name visible; HTTP 200 | `e06a8377bd7b93a209ed5efa1e04e0912342b5ea6d91e490dc6dd269356172e7` | YES | YES | **VALID_FINAL** |

> **BUG-FR14-005 note:** No standalone screenshot exists. TC-FR14-037/038 (already-deleted ID false-success) are manifestations of the same Level-1 oracle as TC-FR14-024/025 (nonexistent ID false-success). Both are confirmed by the single BUG-FR14-003 screenshot above. Issue #37 is preserved closed as duplicate of #34.

---

## CI Images

| Path | Intended FR | Actual FR | Purpose | Visible Evidence | SHA-256 | Authentic | Secret-Free | Status |
|---|---|---|---|---|---|---|---|---|
| `ci/evidence/CI-PASS-33651923618.png` | CI | CI | PASS sample | `HW06 API Tests (23127259)` → `api-tests` job → **PASS** (green). Newman summary: 9 requests, 10 assertions, 0 failures. | `76ad1a1b46a17e9b7cc8aa30044fcaa42117c03af01947436169e5fa850da840` | YES | YES | **VALID_FINAL** |
| `ci/evidence/CI-FAIL-33651923391.png` | CI | CI | FAIL sample | `HW06 Deliberate Red Sample (23127259)` → `deliberate-red` job → **FAIL** (red). Newman summary: 9 requests, 10 assertions, **1 failed** (`DELIBERATE_RED`). | `cb2156503b20b10ba278c85e4b9eaf9b51dd86e210f7cf83e50b4fc0a496797c` | YES | YES | **VALID_FINAL** |

---

## Diagram Image

| Path | Type | Purpose | Evidence | SHA-256 | Status |
|---|---|---|---|---|---|
| `docs/AI_TEST_GENERATOR_DIAGRAM.png` | Self-drawn | AI test-generation pipeline | PIL/Pillow-rendered; 14 nodes, 15 edges; normative blue / partial green / exploratory amber; readable labels; correct values (40/46/46 formal, 10 bugs); author declaration present | `af60403064962decb731252d44d06ca8efdabb4b3573c55a0fcc78e345a5a621` | **VALID_FINAL** |

---

## Historical Synthetic Exclusion

The following are NOT in the final grader-facing image set. They are preserved in `historical-invalid/` directories for audit traceability and are NOT referenced as final evidence:

- `evidence/fr10/bugs/historical-invalid/int053/` — synthetic `int053` Postman UI images (excluded from final set)
- `evidence/fr10/bugs/historical-invalid/int054/` — synthetic `int054` Runner images (excluded from final set)

No stale or wrong-FR images remain in the final image set.

---

## Secret Audit

All 19 logical evidence slots represented by 18 distinct final image files were checked for visible secrets:

- No JWT tokens visible in any Postman or CI screenshot.
- No bearer tokens visible in any screenshot.
- No plaintext passwords are visibly rendered in any screenshot. `BUG-FR02-001` proves the defect through the failed password-omission assertion without displaying the credential value.
- No API keys, OAuth tokens, or session cookies visible.

---

## Final Gate

`ALL VISUAL EVIDENCE AUDITED — SUBMISSION_READY`
