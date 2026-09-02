# FR02 Final Audit

## Final Gate

**FR02_COMPLETE**

The feature pipeline is complete and independently reconciled. Canonical execution accounting is based only on immutable Newman Run03. A separate real Postman Desktop run was used solely to repair missing visual bug evidence.

## Canonical Accounting

| Metric | Verified Value | Verification Basis |
|---|---:|---|
| Raw AI | 37 | Continuous unique IDs `FR02-AI-001..037` parsed from `FR02_AI_DRAFT.md` |
| Audited | 37 | One Human Audit verdict per raw ID |
| VALID | 16 | Recalculated from `TC_AUDIT_FR02.md` |
| INVALID | 2 | `FR02-AI-016`, `FR02-AI-017`, both semantic duplicates |
| INCOMPLETE | 19 | Accepted only with documented corrections |
| Usable AI | 35 | 16 VALID + 19 corrected INCOMPLETE |
| Human | 5 | `FR02-HUM-001..005`, added after gap analysis |
| Formal | 40 | 35 usable AI-derived + 5 Human; unique IDs; rejected IDs absent |
| HTTP executions | 56 | Raw Run03 JSON `run.stats.requests.total` |
| Assertions | 71 | Raw Run03 JSON `run.stats.assertions.total` |
| Assertion PASS | 67 | 71 total - 4 failures |
| Assertion FAIL | 4 | Three confirmed defects + one exploratory observation |
| Formal PASS | 36 | Reconciled one verdict per formal ID |
| Formal normative FAIL | 3 | `FR02-AI-021`, `FR02-AI-028`, `FR02-HUM-003` |
| Exploratory observation | 1 | `FR02-HUM-005` HTTP 500 on undocumented form encoding |
| BLOCKED | 0 | No request, pre-request, test-script, or fixture failures in Run03 |
| Confirmed bugs | 3 | `BUG-FR02-001..003` |
| GitHub Issues | 3 | Live Issues [#1](https://github.com/thangak18/HW06/issues/1), [#2](https://github.com/thangak18/HW06/issues/2), [#3](https://github.com/thangak18/HW06/issues/3) |

## Provenance and Human Audit

- Raw draft SHA-256: `b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c`, matching `FR02_AI_GENERATION_MANIFEST.md`.
- Raw IDs are continuous and unique; no Human-designed IDs are mixed into the raw draft.
- Every raw ID has one `VALID`, `INVALID`, or `INCOMPLETE` verdict with reasoning.
- The 19 incomplete cases have corrected oracle boundaries; the two duplicates are excluded from the canonical suite.
- Human gap analysis precedes the five final Human cases and records why the AI missed each area.

## Collection and Student Header

- Collection SHA-256: `b705979c4f3f526c9ac6661c51f04e7e78344d4eb3dc7c3e74c640eff02d4097`.
- Environment SHA-256: `871eb3aade5fe426d15bdca66ca22e3ef8e7ccc364957680c48fcadf2ab8c21b`.
- 48 collection requests statically checked; all carry an explicit active `X-Student-Id` header.
- Eight `pm.sendRequest` calls across four multi-step cases were inspected; every emitted request supplies `X-Student-Id`.
- Raw Run03 JSON contains 56 executions; every serialized outgoing request includes `X-Student-Id: 23127259`.
- No hardcoded JWT exists in the collection or environment.

## Immutable Newman Run03

| File | SHA-256 |
|---|---|
| `FR02-run-03-console.txt` | `e1cc0e3684ead159e7d32e35227d8563f75dc4ca6cb0db5bc5efebc8d0f5fd3a` |
| `FR02-run-03.json` | `b76900e1c6b436b1d9467e606ecb0254b1c2c6e462f5d9222a36d3761468f683` |
| `FR02-run-03.html` | `993abeab930850e396467c0c30fd414a85c37cc7bf18b53f7e7d30be47037b18` |

- Hostname: `localhost:3000`.
- Requests: 56.
- Assertions: 71.
- Passed assertions: 67.
- Failed assertions: 4.
- Request/script/harness failures: 0.
- All 40 formal IDs are present exactly once in the formal reconciliation.

## Confirmed Bugs

| Bug | Normative Basis | Run03 Failure | Native Postman Screenshot | GitHub Issue |
|---|---|---|---|---|
| `BUG-FR02-001` plaintext password disclosure | API login returns user information; SEC-01 prohibits plaintext password storage; exact plaintext credential is exposed | `FR02-AI-028` | `57b3c3d8af3d5194fe4c5abce34519d2914fea9789059d159bd7416c4c926c9a` | #1 |
| `BUG-FR02-002` lock persists beyond 30 seconds | SRS FR-02 temporary 30-second lock | `FR02-AI-021` | `f2cb12236b277a0a718ba21bdbfdc9747eebfa290cd34ad01069cddf2dc95ba0` | #2 |
| `BUG-FR02-003` correct login rejected after two failures | SRS FR-02 increments by exactly one and locks at three failures | `FR02-HUM-003` | `a166792be577e1d9765645f9e12a8ae8d216f2cb7ac540dedf31becf73049840` | #3 |

`FR02-HUM-005` remains an exploratory robustness observation because the Level-1 sources do not specify form-urlencoded behavior or a no-500 rule for that transport.

## Visual Evidence Authenticity

- Console screenshot: PASS - real Postman Desktop, real request, visible `X-Student-Id: "23127259"`, SHA `ff37fd5cc13d56f37a97df37e4ff5ba0e5afae7ba89d655624d0585f91a55851`.
- Runner screenshot: PASS - real Postman Desktop Runner, `FR02-local`, 71 tests, 67 passed, 4 failed, 0 errors, SHA `cc017ada960ad3fa60d4d7523bc8efade654d4abd49eb0cbd2ae8ee37d362f46`.
- Bug screenshots: PASS - three distinct native Runner screenshots; relevant IDs, HTTP results, and organic failed assertions visible; no JWT visible.
- Synthetic or generated final evidence: NONE.

## AI Audit

- Core FR02 generation interactions `INT-005..011` and Human Audit interactions `INT-012..016` are traceable to the feature artifacts and procedural commits.
- Several later historical Antigravity interactions retain unrecoverable `PENDING TRANSCRIPT BACKFILL` output markers. No exact output was invented. This is documented as a global historical audit limitation for final AI compliance review; it does not alter the verified raw draft, Human classifications, executable suite, or runtime evidence.

## Procedural Git History

| Stage | Commit |
|---|---|
| Generation | `f6164ef test(23127259): add AI-generated FR-02 test cases` |
| Human Audit | `5deecd7 test(23127259): audit AI-generated FR-02 test cases` |
| Human Extension | `1634d8f test(23127259): add human-designed FR-02 extension cases` |
| Postman Implementation | `bfa9b92 test(23127259): implement FR-02 Postman collection` |
| Execution | `6af5080 test(23127259): execute FR-02 API test suite` |

## Repairs Performed

- Replaced three weak Newman-HTML bug PNGs (including a duplicate pair) with three distinct genuine Postman Desktop Runner captures.
- Avoided saving a live response-detail view that exposed a JWT.
- Corrected screenshot manifests, paths, hashes, capture method, and authenticity claims.
- Rewrote the three Markdown bug reports to remove unsupported exact schema claims, stale Python/cURL emphasis, broken math escapes, local-only file URLs, and exposed token examples.
- Verified live Issues #1/#2/#3 and prepared their screenshot embedding repair after the native files are pushed.

## Gate Result

**FR02_COMPLETE**
