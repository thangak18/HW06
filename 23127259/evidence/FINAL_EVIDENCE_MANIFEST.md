# Final Evidence Manifest - HW06 23127259

## Canonical Runtime Evidence

| Feature | Canonical Run | Requests | Assertions | Pass | Fail | Exit | Grader-Facing Artifacts |
|---|---|---:|---:|---:|---:|---:|---|
| FR02 | Run03 | 56 | 71 | 67 | 4 | 1 | `newman/fr02/FR02-run-03-console.txt`, `.json`, `.html` |
| FR10 | Run04 | 176 | 176 | 164 | 12 | 1 | `evidence/fr10/newman/FR10-run04-cli.txt`, `.json`, `.html` |
| FR14 | Run01 | 60 | 70 | 58 | 12 | 1 | `evidence/fr14/newman/FR14-run01-cli.txt`, `FR14-run01-sanitized.json`, `FR14-run01-sanitized.html` |

### Runtime SHA-256

| Artifact | SHA-256 |
|---|---|
| FR02 CLI | `e1cc0e3684ead159e7d32e35227d8563f75dc4ca6cb0db5bc5efebc8d0f5fd3a` |
| FR02 JSON | `b76900e1c6b436b1d9467e606ecb0254b1c2c6e462f5d9222a36d3761468f683` |
| FR02 HTML | `993abeab930850e396467c0c30fd414a85c37cc7bf18b53f7e7d30be47037b18` |
| FR10 CLI | `482ffbc833cccf678f3a0fd87e93f6af6e19f1cd825ea2c36edbfd35389c6635` |
| FR10 JSON | `de73cc49094f7bdcea1db88f3f7f9c5369f973cf227d5b4efad192f6d1f81b99` |
| FR10 HTML | `52141602b2933640e49b7cde40130b4836c48e33977d26b50319975c9f855de6` |
| FR14 CLI | `94a2e379e35289c9c28f5658928960d2d41072a35a6d0e2551cdb5d5833368bb` |
| FR14 JSON (raw) | `eb3d05509d304a736ba99fbe0ea96dfcccceaa67b8fc97e81de1a945e8a24868` |
| FR14 sanitized JSON | `6fc6a6fc194f0bfc248f125745e3f59de879fc9b4a46d6488413ce326a86a676` |
| FR14 sanitized HTML | `790cd4de01f8ec72814d633c95b0b5dd7d17aed10b3ab3f934c7bfa34662de80` |

## Frozen AI Provenance

| Feature | Raw Count | SHA-256 |
|---|---:|---|
| FR02 | 37 | `b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c` |
| FR10 | 42 | `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` |
| FR14 | 42 | `95ac502b0880efcc1c6ceb040a1171eeacebff5c262a5f6df8d49a86cadcaf70` |

## Canonical Formal Accounting

| Feature | Usable AI | Human | Formal |
|---|---:|---:|---:|
| FR02 | 35 | 5 | 40 |
| FR10 | 41 | 5 | 46 |
| FR14 | 40 | 6 | 46 |

## Confirmed Bugs and Issues

| Feature | Distinct Bugs | Issues |
|---|---:|---|
| FR02 | 3 | #1, #2, #3 |
| FR10 | 3 | #29, #30, #31 |
| FR14 | 4 | #32, #33, #34, #36 |

Issue #37 is closed as duplicate of FR14 Issue #34 and is not separately counted.

## Authentic CI Evidence

| Sample | Run | Commit | Result | Technical Proof | Screenshot |
|---|---|---|---|---|---|
| PASS | [33651923618](https://github.com/thangak18/HW06/actions/runs/33651923618) | `fa6eac3d83c4b46b3fa164f3460bcc846e6ef6a0` | success | 9 requests; 10/10 assertions; 0 harness errors | `ci/evidence/CI-PASS-33651923618.png` **PASS** |
| FAIL | [33651923391](https://github.com/thangak18/HW06/actions/runs/33651923391) | `fa6eac3d83c4b46b3fa164f3460bcc846e6ef6a0` | failure | same healthy harness; exactly one `DELIBERATE_RED` assertion failure | `ci/evidence/CI-FAIL-33651923391.png` **PASS** |

Run 33649719887 is superseded and excluded because its green conclusion masked harness and assertion failures.

## Visual Evidence Status

All visual evidence has been pixel-audited (Fable, 2026-09-03). All images are authentic, secret-free, and correctly scoped.

| Area | Status |
|---|---|
| FR02 Console (Postman) | **PASS** — `FR02-postman-console-x-student-id.png` |
| FR02 Runner | **PASS** — `FR02-postman-runner-result.png` |
| FR02 3 bug screenshots | **PASS** — `bugs/screenshots/FR02/` |
| FR10 Console | **PASS** — `FR10-postman-console-x-student-id-smoke.png` (replaced stale FR02-mislabeled image) |
| FR10 Runner | **PASS** — `BUG-FR10-001-postman-runner.png` |
| FR10 3 bug screenshots | **PASS** — `evidence/fr10/bugs/` |
| FR14 Console | **PASS** — `FR14-postman-console-x-student-id.png` — `X-Student-Id: 23127259` visible |
| FR14 Runner | **PASS** — `FR14-postman-runner-result.png` — 46 tests, 6 failed, 0 errors |
| FR14 4 bug screenshots | **PASS** — `evidence/fr14/bugs/` (BUG-FR14-001/002/003/004). No standalone BUG-FR14-005 screenshot (Issue #37 is duplicate of #34) |
| CI PASS screenshot | **PASS** — `CI-PASS-33651923618.png` — green, 9 requests, 10/10 assertions |
| CI FAIL screenshot | **PASS** — `CI-FAIL-33651923391.png` — red, DELIBERATE_RED failure |
| AI test-generator diagram | **PASS** — `AI_TEST_GENERATOR_DIAGRAM.png` (self-drawn PIL; 14 nodes, 15 edges, correct values) |
| Excel workbook | **PASS** — 6 sheets, 10 bugs, all counts correct |
| Three PDFs | **PASS** — Main Report 4pp, AI Audit 16pp, AI Critique 1pp; no stale values |

## Current Gate

**SUBMISSION_READY**
