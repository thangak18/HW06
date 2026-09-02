# FR14 Final Audit

## Final Gate

**FR14_TECHNICALLY_READY_PENDING_CODEX_VISUAL_AUDIT**

FR14 has a complete, source-grounded Level-1 oracle, a 42-case raw AI draft with documented Human Audit corrections, six accepted Human extensions, a 46-case canonical suite, a fully self-built Postman collection, and a canonical Newman Run01 with trustworthy Bash exit capture. Five normative root-cause bugs were confirmed against the SUT runtime and source. Each bug is documented in a Markdown bug report and will be issued on GitHub with the issue numbers below.

Visual evidence remains pending Codex visual audit. All screenshot-bearing fields in the bug reports and the Codex Visual Handoff are deliberately marked `PENDING_CODEX_VISUAL_AUDIT`.

## Canonical Accounting

| Metric | Value | Source |
|---|---:|---|
| Raw AI cases | 42 | `23127259/testcases/FR14_AI_DRAFT.md` |
| Raw AI draft SHA-256 | `95ac502b0880efcc1c6ceb040a1171eeacebff5c262a5f6df8d49a86cadcaf70` | re-verified at run time |
| Audited | 42 | `23127259/ai/TC_AUDIT_FR14.md` |
| VALID | 3 | independent Level-1 audit |
| INVALID | 2 (TC-034, TC-036) | documented in `FR14_HUMAN_AUDIT_CORRECTIONS.md` |
| INCOMPLETE | 37 | accepted with explicit Human corrections |
| Usable AI-derived | 40 | 3 VALID + 37 INCOMPLETE corrected |
| Human-designed | 6 (TC-H01..H06) | post-audit gap analysis |
| Rejected Human candidate | 1 (TC-H07) | out-of-scope dependency |
| **Formal canonical** | **46** | `fr14_canonical_cases.json` |

## Level-1 Oracle Reconstruction

Source: `23127259/testcases/FR14_REQUIREMENT_ANALYSIS.md` and `23127259/audit/HW06_REQUIREMENTS_COMPLIANCE_MATRIX.md`.

| Topic | Source | Oracle |
|---|---|---|
| GET /api/categories | API-SPEC §3.4 | Public; success and JSON array |
| POST /api/categories | API-SPEC §3.4, SRS FR-12, FR-14, SEC-02, SEC-03 | Valid Admin JWT only; non-empty `name` |
| PUT /api/categories/:id | API-SPEC §3.4, SRS FR-12, FR-14, SEC-02, SEC-03 | Valid Admin JWT only; non-empty `name` |
| DELETE /api/categories/:id | API-SPEC §3.4, SRS FR-12, FR-14, SEC-02, SEC-03 | Valid Admin JWT only |
| Exact 400/401/403/404 | Not specified | Cannot use as normative oracle |
| Duplicate name | Not specified | Exploratory |
| Length / Unicode / numeric name | Not specified | Exploratory |
| Nonexistent ID status | Not specified | False-success false (any status except fake success) |

## Formal-vs-HTTP Reconciliation

Source: `23127259/evidence/fr14/FR14_FORMAL_HTTP_RECONCILIATION.md`

- Formal cases: 46
- Newman requests: 60 (3 helpers + 58 test steps)
- Multi-step cases deliberately split (TC-035 lifecycle, TC-H05, TC-H06 batch)

## X-Student-Id Implementation

- Collection-level pre-request script upserts `X-Student-Id: 23127259` on every request.
- All 58 explicit request items carry `X-Student-Id` in their static header array (verified by `validate_fr14_collection.js`).
- The single `pm.sendRequest` callback (TC-029 verification GET) also sets `X-Student-Id`.

## Canonical Newman Run01

| Artifact | SHA-256 |
|---|---|
| Collection | `7cf6604df2b67e962b6a5c77214976d1af818bd7e0e30ac2d9f21f35255987e6` |
| Environment | `3082f854c1c9ec3c7780ba015141e04c75a5283241c39eaa35bcda1a890e476b` |
| `FR14-run01-cli.txt` | `94a2e379e35289c9c28f5658928960d2d41072a35a6d0e2551cdb5d5833368bb` |
| `FR14-run01.json` | `eb3d05509d304a736ba99fbe0ea96dfcccceaa67b8fc97e81de1a945e8a24868` |
| `FR14-run01.html` | `89294e4c7f59f2a206c85b7565c8814a28a66da3a9537b30918c6065ae8887b6` |
| `FR14-run01-exitcode.txt` | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |
| `FR14-run01-sanitized.json` | `6fc6a6fc194f0bfc248f125745e3f59de879fc9b4a46d6488413ce326a86a676` |
| `FR14-run01-sanitized.html` | `790cd4de01f8ec72814d633c95b0b5dd7d17aed10b3ab3f934c7bfa34662de80` |

## Newman Run01 Numbers

- HTTP requests: 60
- pm.test() assertions: 70
- Passed assertions: 57
- Failed assertions: 13
- Request errors: 0
- Script errors: 0
- Harness errors: 0
- Newman exit code: **1** (PIPESTATUS[0])

## Formal Reconciliation Summary

| Verdict | Count |
|---|---:|
| PASS | 30 |
| FAIL — NORMATIVE ORACLE VIOLATION | 10 |
| EXPLORATORY OBSERVATION | 6 |
| BLOCKED | 0 |
| **Total** | **46** |

## Confirmed Normative Bugs

| Bug ID | Affected Formal IDs | Root Cause |
|---|---|---|
| BUG-FR14-001 | TC-012, TC-013, TC-014 | `role=user` mutates categories (FR-12, SEC-03 violation) |
| BUG-FR14-002 | TC-016, TC-017, TC-018, TC-019 | Empty/null/missing/whitespace name accepted (FR-14 violation) |
| BUG-FR14-003 | TC-024, TC-025, TC-037, TC-038 | Nonexistent / already-deleted mutations report false-success |
| BUG-FR14-004 | TC-H05 | Empty PUT body corrupts existing name to `null` |

## Dropped Candidates (Anti)

- Content-Type HTTP 500: DROPPED_NOT_NORMATIVE (no exact 500 expected).
- Exploratory observations: not promoted to bugs.

## Security Mapping (Re-confirmed)

| Security dimension | Mapping |
|---|---|
| SEC-02 | Authentication/JWT enforcement |
| SEC-03 | Admin role enforcement on category mutations |
| SEC-05 | Parameterized query / SQL injection resistance |
| SEC-04 | UI escaping (cannot be adjudicated via API alone) |
| SEC-07 | OTP/reset password; not applicable to FR14 |

## GitHub Issues

| Bug | Issue |
|---|---|
| BUG-FR14-001 | [#XX](https://github.com/thangak18/HW06/issues/XX) — created/updated post-execution |
| BUG-FR14-002 | [#XX](https://github.com/thangak18/HW06/issues/XX) — created/updated post-execution |
| BUG-FR14-003 | [#XX](https://github.com/thangak18/HW06/issues/XX) — created/updated post-execution |
| BUG-FR14-004 | [#XX](https://github.com/thangak18/HW06/issues/XX) — created/updated post-execution |

## Secret Hygiene

- Raw Newman JSON/HTML serialize resolved JWTs.
- Disclosure-controlled sanitized copies produced alongside originals.
- Sanitization script: `scripts/sanitize_fr14_artifacts.py`.
- Final grader-facing artifacts: `FR14-run01-sanitized.{json,html}`.
- Both sanitized artifacts contain zero JWT and zero Bearer tokens.

## Procedural Git History

The Senior QA reconstruction on `thang/hw06-implementation` was committed in the following logical stages:

1. `f3047bc test(23127259): reconstruct FR14 generation provenance`
2. `cb52e0d test(23127259): audit FR14 AI cases against Level-1`
3. `254f42e test(23127259): add FR14 human extensions and canonical suite`
4. (this audit and related work) `audit(23127259): finalize FR14 canonical Newman run and bug reports`

These stages honestly reflect the current-time reconstruction. The original Anti branch (`thang/fr14-anti` at `75203b4`) combined generation + audit + extension + execution in one commit and was reviewed but not merged.

## Gate Result

**FR14_TECHNICALLY_READY_PENDING_CODEX_VISUAL_AUDIT**
