# HW06 CI/CD Report

## Pipeline Design

Two branch-local GitHub Actions workflows run against a bundled EShop SUT on `http://localhost:3010`:

- `.github/workflows/hw06-23127259-api-tests.yml` - all-green smoke across FR02, FR10, and FR14.
- `.github/workflows/hw06-deliberate-red.yml` - identical healthy setup with exactly one intentionally failing sentinel assertion.

Both workflows:

1. check out `thang/hw06-implementation`;
2. install Newman 6;
3. start the SUT and require a successful health check;
4. run `HW06_CI_Passing_Smoke.postman_collection.json`;
5. upload safe CLI/JUnit evidence (no response bodies or resolved JWTs).

Every smoke request contains `X-Student-Id: 23127259`. The PASS suite covers valid login (FR02), an Admin category create/read persistence flow (FR14), and a User checkout plus Admin state transition/read persistence flow (FR10).

## Authentic PASS Run

| Attribute | Verified Value |
|---|---|
| Workflow | `HW06 API Tests (23127259)` |
| Run ID | `33651923618` |
| URL | https://github.com/thangak18/HW06/actions/runs/33651923618 |
| Branch | `thang/hw06-implementation` |
| Event | `push` |
| Commit | `fa6eac3d83c4b46b3fa164f3460bcc846e6ef6a0` |
| Conclusion | **success** |
| SUT health check | PASS |
| HTTP requests | 9 executed, 0 failed |
| Assertions | 10 executed, 10 passed, 0 failed |
| Request/script/harness errors | 0 |
| Artifact | `hw06-23127259-passing-33651923618` (artifact ID `9855118936`) |

The log explicitly ends with: `Verified all FR02/FR10/FR14 CI smoke assertions passed.`

## Authentic FAIL Run

| Attribute | Verified Value |
|---|---|
| Workflow | `HW06 Deliberate Red Sample (23127259)` |
| Run ID | `33651923391` |
| URL | https://github.com/thangak18/HW06/actions/runs/33651923391 |
| Branch | `thang/hw06-implementation` |
| Event | `push` via `23127259/ci/deliberate-red-trigger.txt` |
| Commit | `fa6eac3d83c4b46b3fa164f3460bcc846e6ef6a0` |
| Conclusion | **failure** |
| SUT health check | PASS |
| HTTP requests | 9 executed, 0 failed |
| Assertions | 10 executed, 9 passed, exactly 1 failed |
| Failed assertion | `DELIBERATE_RED: intentional single CI failure` |
| Request/script/harness errors | 0 |
| Artifact | `hw06-23127259-deliberate-red-33651923391` (artifact ID `9855119363`) |

The workflow validates the JUnit report before returning Newman's nonzero status. It refuses the run if the failure count is not exactly one or the failed assertion is not named `DELIBERATE_RED`.

## Superseded Green Run

Run `33649719887` had a green GitHub conclusion but is **not** used as PASS evidence. Its logs show a missing FR10 collection path, an HTML reporter setup error, and canonical FR14 assertion failures masked by scripts that always exited zero. The final evidence uses only runs `33651923618` and `33651923391`.

## Screenshots

| Evidence | Path | Status |
|---|---|---|
| PASS Actions run | `23127259/ci/evidence/CI-PASS-33651923618.png` | PENDING_CODEX_VISUAL_AUDIT |
| FAIL Actions run | `23127259/ci/evidence/CI-FAIL-33651923391.png` | PENDING_CODEX_VISUAL_AUDIT |

## Final CI Gate

**TECHNICAL PASS - AUTHENTIC GREEN AND INTENTIONAL RED RUNS VERIFIED; SCREENSHOT CAPTURE PENDING**
