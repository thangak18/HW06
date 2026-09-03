# Codex to Fable Final Visual Handoff

## FR02

Visual: PASS

The five required FR02 final images were previously pixel-audited and remain accepted. Exact findings and hashes are recorded in `23127259/audit/CODEX_VISUAL_WORKLOG.md`.

## FR10

Visual: PASS

The final FR10 evidence was previously pixel-audited after Codex replaced the stale FR02-mislabeled Console image with authentic Postman Desktop evidence. Historical synthetic `int053` and `int054` remain excluded.

## FR14

Canonical visual-run context: current 46-case collection imported separately as `FR14_Category_CRUD Copy`, environment `FR14-local`. The stale 49-case / 7-Human collection was not used.

Runner path: `23127259/evidence/fr14/FR14-postman-runner-result.png`

Runner status: VALID_FINAL

Console path: `23127259/evidence/fr14/FR14-postman-console-x-student-id.png`

Console status: VALID_FINAL

BUG-FR14-001 path: `23127259/evidence/fr14/bugs/BUG-FR14-001-postman-runner.png`

BUG-FR14-001 status: VALID_FINAL

BUG-FR14-002 path: `23127259/evidence/fr14/bugs/BUG-FR14-002-postman-runner.png`

BUG-FR14-002 status: VALID_FINAL

BUG-FR14-003 path: `23127259/evidence/fr14/bugs/BUG-FR14-003-postman-runner.png`

BUG-FR14-003 status: VALID_FINAL

BUG-FR14-004 path: `23127259/evidence/fr14/bugs/BUG-FR14-004-postman-runner.png`

BUG-FR14-004 status: VALID_FINAL

No standalone BUG-FR14-005 screenshot exists. Issue #37 remains a historical duplicate manifestation of BUG-FR14-003 / Issue #34.

### FR14 Metric Distinction

- 58 stored collection request items.
- 60 actual Newman HTTP operations.
- Difference: one scripted verification GET from TC-FR14-029 and one scripted verification GET from TC-FR14-H05 via `pm.sendRequest`.
- No contradiction; no canonical data change required.

## CI

PASS Run: 33651923618

PASS URL: `https://github.com/thangak18/HW06/actions/runs/33651923618`

PASS SHA: `fa6eac3d83c4b46b3fa164f3460bcc846e6ef6a0`

PASS Screenshot: `23127259/ci/evidence/CI-PASS-33651923618.png`

PASS Screenshot status: VALID_FINAL

FAIL Run: 33651923391

FAIL URL: `https://github.com/thangak18/HW06/actions/runs/33651923391`

FAIL SHA: `fa6eac3d83c4b46b3fa164f3460bcc846e6ef6a0`

FAIL Screenshot: `23127259/ci/evidence/CI-FAIL-33651923391.png`

FAIL Screenshot status: VALID_FINAL

The FAIL screenshot visibly identifies the `HW06 Deliberate Red Sample` workflow and `deliberate-red` job. Machine logs previously verified 9 requests, 10 assertions, exactly one `DELIBERATE_RED: intentional single CI failure`, and zero request/script/harness errors. Historical run 33649719887 remains rejected as final PASS evidence.

## New Visual Batch Hashes

| Path | SHA-256 | Status |
|---|---|---|
| `23127259/evidence/fr14/FR14-postman-runner-result.png` | `65cc316415efb76c09e0369c8f1812709fb5bf2aa0b4586213f55b8f8e5d3f9b` | VALID_FINAL |
| `23127259/evidence/fr14/FR14-postman-console-x-student-id.png` | `a7eb1faee23ad8c35dde401c0b4b1d98a07f6543199a7ddb86b44e9be0c65791` | VALID_FINAL |
| `23127259/evidence/fr14/bugs/BUG-FR14-001-postman-runner.png` | `9d03d85e62936609f460d7e7947a0b02436cb6ed16e3bc2e480a6fd8f4eb39d4` | VALID_FINAL |
| `23127259/evidence/fr14/bugs/BUG-FR14-002-postman-runner.png` | `15919c31baf60b391b694bb53633c1173aeb7e42c30fdfe943f8cc7ffe61c7f0` | VALID_FINAL |
| `23127259/evidence/fr14/bugs/BUG-FR14-003-postman-runner.png` | `9d3d6c65008d483e75277fbe0a7bed406f69bc04b3136a3b30277f08998bb0b8` | VALID_FINAL |
| `23127259/evidence/fr14/bugs/BUG-FR14-004-postman-runner.png` | `e06a8377bd7b93a209ed5efa1e04e0912342b5ea6d91e490dc6dd269356172e7` | VALID_FINAL |
| `23127259/ci/evidence/CI-PASS-33651923618.png` | `76ad1a1b46a17e9b7cc8aa30044fcaa42117c03af01947436169e5fa850da840` | VALID_FINAL |
| `23127259/ci/evidence/CI-FAIL-33651923391.png` | `cb2156503b20b10ba278c85e4b9eaf9b51dd86e210f7cf83e50b4fc0a496797c` | VALID_FINAL |

All eight files were opened from their final saved bytes. They are authentic, readable, distinct, correctly scoped, and visually secret-free.

## Remaining Fable Tasks

- diagram visual
- Excel visual
- PDF page-by-page visual
- global all-image forensic audit
- final evidence manifest
- final compliance cleanup
- final commit/push

## Codex Visual Batch Status

PASS
