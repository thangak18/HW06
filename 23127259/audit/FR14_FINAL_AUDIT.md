# FR14 Final Audit

## Final Gate

**FR14_TECHNICALLY_READY_PENDING_CODEX_VISUAL_AUDIT**

FR14 has a complete, source-grounded Level-1 oracle, a 42-case raw AI draft with documented Human Audit corrections, six accepted Human extensions, a 46-case canonical suite, a fully self-built Postman collection, and a canonical Newman Run01 with trustworthy Bash exit capture. Four distinct normative root-cause bugs were confirmed. A fifth issue created later duplicated BUG-FR14-003 and is closed as duplicate.

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
- Passed assertions: 58
- Failed assertions: 12
- Request errors: 0
- Script errors: 0
- Harness errors: 0
- Newman exit code: **1** (PIPESTATUS[0])

## Formal Reconciliation Summary

| Verdict | Count |
|---|---:|
| PASS | 20 |
| FAIL — NORMATIVE ORACLE VIOLATION | 12 |
| EXPLORATORY OBSERVATION | 14 |
| BLOCKED | 0 |
| **Total** | **46** |

## Confirmed Normative Bugs

| Bug ID | Affected Formal IDs | Root Cause | Level-1 Basis |
|---|---|---|---|
| BUG-FR14-001 | TC-012, TC-013, TC-014 | `role=user` mutates categories | SRS FR-12 + SEC-03 |
| BUG-FR14-002 | TC-016, TC-017, TC-018, TC-019 | Empty/null/missing/whitespace name accepted | SRS FR-14 mandatory-name rule |
| BUG-FR14-003 | TC-024, TC-025, TC-037, TC-038 | Nonexistent/already-deleted ID PUT/DELETE returns false-success | FR-14 CRUD-integrity rule |
| BUG-FR14-004 | TC-H05 | Empty PUT body corrupts existing name to `null` | SRS FR-14 (mandatory-name integrity on update) |

**Total confirmed normative root-cause bugs: 4.**

## Exploratory Observations (NOT promoted to bugs)

| ID | Reason |
|---|---|
| TC-FR14-H01 | Missing Content-Type → HTTP 500; FR-14 does not define the required behaviour |
| TC-FR14-020 | Long name accepted; exact length limit not specified |
| TC-FR14-021 | Unicode name accepted; no restriction specified |
| TC-FR14-022 | Duplicate name accepted; uniqueness not specified |
| TC-FR14-023 | Integer name accepted; type coercion not specified |
| TC-FR14-026 | ID=0 handled gracefully |
| TC-FR14-027 | ID=-1 handled gracefully |
| TC-FR14-028 | Non-numeric ID handled gracefully |
| TC-FR14-030 | XSS payload accepted as text (SEC-04 is UI-scoped) |
| TC-FR14-031 | Mass-assignment fields ignored (partial oracle) |
| TC-FR14-032 | PUT body-id override ignored (partial oracle) |
| TC-FR14-033 | Object-type name handled |

## Dropped Candidates

- Content-Type HTTP 500 (TC-FR14-H01): **EXPLORATORY_ROBUSTNESS_OBSERVATION** (FR-14 does not define the required behaviour; HTTP 500 not specified as normative).
- TC-FR14-034: INVALID (semantic duplicate / mislabelled IDOR).
- TC-FR14-036: INVALID (unspecified destructive referential test).
- TC-FR14-H07: Rejected Human candidate (out-of-scope referential dependency).

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
| BUG-FR14-001 | [#32](https://github.com/thangak18/HW06/issues/32) |
| BUG-FR14-002 | [#33](https://github.com/thangak18/HW06/issues/33) |
| BUG-FR14-003 | [#34](https://github.com/thangak18/HW06/issues/34) |
| BUG-FR14-004 | [#36](https://github.com/thangak18/HW06/issues/36) |

Issue [#37](https://github.com/thangak18/HW06/issues/37) is closed as a duplicate manifestation of BUG-FR14-003 / #34.

## Canonical Newman Run01 Provenance

The canonical `FR14-run01.json` is a **genuinely new, distinct execution** produced during the Senior-QA reconstruction on `thang/hw06-implementation`. It is NOT a relabelling of the historical Anti `Run01`.

| Run | Source branch | Last item | Execution count | SHA-256 | Size |
|---|---|---|---:|---|---:|
| Anti `Run01` (historical) | `thang/fr14-anti` | `TC-FR14-H07 – Verify Products Orphaned After Category Delete` | 59 | `212c4aaa25997a0b...` | 947,318 B |
| Primary `Run01` (canonical) | `thang/hw06-implementation` | `TC-FR14-H06 – Verify All Batch Entities` | 60 | `eb3d05509d304a73...` | 5,386,036 B |

Distinguishing facts (no ambiguity remains):

- File size differs by **5.7×** (Anti `947 KB` vs. Primary `5.4 MB`) — Anti was the truncated/early run; Primary carries the complete 46-case suite with 60 requests and 70 assertions.
- Terminal test case differs: Anti ends at `TC-FR14-H07` (orphan-product verify, later dropped); Primary ends at `TC-FR14-H06` (the accepted Human batch-verify extension).
- SHA-256 of the JSON artifact is distinct: Anti `212c4aaa...` vs. Primary `eb3d0550...`.
- Primary collection SHA-256 `7cf6604d...` and environment SHA-256 `3082f854...` are recorded in the table above; Anti does not publish these because its run was superseded.
- The historical Anti `Run01` is retained in worktree `/Volumes/Thang/HW06/HW06-fr14-anti` (untouched, audit-only). It is NOT the canonical run.

Therefore Run01 in this final report refers unambiguously to the Primary canonical execution `eb3d05509d304a73...`. No Run02..Run05 numbering was ever used on `thang/hw06-implementation`, so no monotonic renumber is needed.

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
