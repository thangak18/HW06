# Final Evidence Manifest (HW06 · 23127259)

> **Scope.** This manifest records every canonical non-visual evidence
> artifact produced during the HW06 pipeline, with its SHA-256 and
> integrity status. Visual evidence is intentionally **not** asserted here;
> visual files are listed only as `PENDING_CODEX_VISUAL_AUDIT` placeholders.

## 1. Canonical Newman Runs

### FR02 — Run03 (immutable historical)

| Artifact | Path | Status |
|---|---|---|
| JSON | `23127259/newman/fr02/FR02-run-03.json` | IMMUTABLE |
| HTML | `23127259/newman/fr02/FR02-run-03.html` | IMMUTABLE |

### FR02 — Run03 public-safe (grader-facing)

| Artifact | Path | Status |
|---|---|---|
| JSON | `23127259/newman/fr02/FR02-run-03.json` (single canonical run; public-safe copies present where created) | IMMUTABLE |

### FR10 — Run04 (canonical)

| Artifact | Path | Status |
|---|---|---|
| CLI | `23127259/evidence/fr10/newman/FR10-run04-cli.txt` | CANONICAL |
| JSON | `23127259/evidence/fr10/newman/FR10-run04.json` | CANONICAL |
| HTML | `23127259/evidence/fr10/newman/FR10-run04.html` | CANONICAL |
| Exit | `23127259/evidence/fr10/newman/FR10-run04-exitcode.txt` (value = `1`, accepted: 3 confirmed normative bugs) |

### FR10 — Run04 public-safe

| Artifact | Path | Status |
|---|---|---|
| CLI | `23127259/evidence/fr10/newman/public-safe/FR10-run04-cli.txt` | CANONICAL |
| JSON | `23127259/evidence/fr10/newman/public-safe/FR10-run04.json` | CANONICAL |
| HTML | `23127259/evidence/fr10/newman/public-safe/FR10-run04.html` | CANONICAL |

### FR14 — Run01 (canonical)

| Artifact | Path | SHA-256 | Status |
|---|---|---|---|
| CLI | `23127259/evidence/fr14/newman/FR14-run01-cli.txt` | `94a2e379e35289c9c28f5658928960d2d41072a35a6d0e2551cdb5d5833368bb` | CANONICAL |
| JSON | `23127259/evidence/fr14/newman/FR14-run01.json` | `eb3d05509d304a736ba99fbe0ea96dfcccceaa67b8fc97e81de1a945e8a24868` | CANONICAL |
| HTML | `23127259/evidence/fr14/newman/FR14-run01.html` | `89294e4c7f59f2a206c85b7565c8814a28a66da3a9537b30918c6065ae8887b6` | CANONICAL |
| Exit | `23127259/evidence/fr14/newman/FR14-run01-exitcode.txt` | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` (value = `1`, accepted: 5 confirmed normative bugs) |

### FR14 — Run01 sanitized

| Artifact | Path | SHA-256 |
|---|---|---|
| JSON | `23127259/evidence/fr14/newman/FR14-run01-sanitized.json` | `6fc6a6fc194f0bfc248f125745e3f59de879fc9b4a46d6488413ce326a86a676` |
| HTML | `23127259/evidence/fr14/newman/FR14-run01-sanitized.html` | `790cd4de01f8ec72814d633c95b0b5dd7d17aed10b3ab3f934c7bfa34662de80` |

## 2. Postman Collections

| Feature | Path | Status |
|---|---|---|
| FR02 | `23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json` | CANONICAL |
| FR10 | `23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json` | CANONICAL |
| FR14 | `23127259/postman/collections/FR14_Category_CRUD.postman_collection.json` | CANONICAL |

## 3. Environments

| Feature | Path | Status |
|---|---|---|
| FR02 | `23127259/postman/environments/FR02-local.postman_environment.json` | CANONICAL |
| FR10 | `23127259/postman/environments/FR10-local.postman_environment.json` | CANONICAL |
| FR14 | `23127259/postman/environments/FR14-local.postman_environment.json` | CANONICAL |

## 4. Canonical Maps

| Feature | Path | Count |
|---|---|---|
| FR02 | `23127259/testcases/FR02_FINAL_EXECUTABLE_SUITE.md` | 40 |
| FR10 | `23127259/testcases/fr10_canonical_cases.json` | 46 |
| FR14 | `23127259/testcases/fr14_canonical_cases.json` | 46 |

## 5. Raw AI Drafts (Frozen)

| Feature | Path | SHA-256 |
|---|---|---|
| FR02 | `23127259/testcases/FR02_AI_DRAFT.md` | `b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c` |
| FR10 | `23127259/testcases/FR10_AI_DRAFT.md` | `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` |
| FR14 | `23127259/testcases/FR14_AI_DRAFT.md` | `95ac502b0880efcc1c6ceb040a1171eeacebff5c262a5f6df8d49a86cadcaf70` |

## 6. Bug Reports

| Bug | Path | Issue |
|---|---|---|
| BUG-FR02-001..003 | `23127259/bugs/issues/BUG-FR02-*.md` | #1, #2, #3 |
| BUG-FR10-001..003 | `23127259/bugs/BUG-FR10-*.md` | #29, #30, #31 |
| BUG-FR14-001..005 | `23127259/bugs/BUG-FR14-*.md` | #32, #33, #34, `PENDING_GH_ISSUE` (×2) |

## 7. Validators

| Script | Purpose |
|---|---|
| `scripts/validate_fr14_collection.py` | Static validation of FR14 collection (X-Student-Id, no hardcoded JWT, fixture isolation, etc.) |
| `scripts/validate_fr10_canonical_map.py` | Canonical-map validator for FR10 |
| `scripts/sanitize_fr14_artifacts.py` | JWT/Bearer redactor for FR14 JSON/HTML |
| `scripts/build_excel_workbook.py` | Excel workbook generator + validator |
| `scripts/automated_final_checks.py` | Final automated non-visual checks |

## 8. Visual Artifacts (Codex-owned)

| Expected Path | Status |
|---|---|
| `23127259/evidence/postman/FR02_POSTMAN_CONSOLE_SCREENSHOT.png` | PENDING_CODEX_VISUAL_AUDIT |
| `23127259/evidence/postman/FR02_POSTMAN_RUNNER_SCREENSHOT.png` | PENDING_CODEX_VISUAL_AUDIT |
| `23127259/evidence/postman/FR10_POSTMAN_CONSOLE_SCREENSHOT.png` | PENDING_CODEX_VISUAL_AUDIT |
| `23127259/evidence/postman/FR10_POSTMAN_RUNNER_SCREENSHOT.png` | PENDING_CODEX_VISUAL_AUDIT |
| `23127259/evidence/postman/FR14_POSTMAN_CONSOLE_SCREENSHOT.png` | PENDING_CODEX_VISUAL_AUDIT |
| `23127259/evidence/postman/FR14_POSTMAN_RUNNER_SCREENSHOT.png` | PENDING_CODEX_VISUAL_AUDIT |
| Bug screenshots #1/#2/#3 (FR02), #29/#30/#31 (FR10), #32/#33/#34 (FR14) | PENDING_CODEX_VISUAL_AUDIT |
| CI PASS / FAIL screenshots | PENDING_CODEX_VISUAL_AUDIT |
| AI test-generator diagram image | PENDING_CODEX_VISUAL_TASK |
| PDF page renders | PENDING_CODEX_VISUAL_AUDIT |

## 9. Final Compliance Summary

- **Technical:** All non-visual requirements pass.
- **Visual:** Pending Codex visual audit per
  [`CODEX_VISUAL_HANDOFF.md`](../../audit/CODEX_VISUAL_HANDOFF.md).
- **Final state:** `HW06_TECHNICALLY_READY_PENDING_CODEX_VISUAL_AUDIT`.