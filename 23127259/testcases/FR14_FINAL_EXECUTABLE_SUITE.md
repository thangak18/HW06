# FR14 Final Executable Suite Specification

## Accounting

| Category | Count |
|---|---:|
| Raw AI | 42 |
| Rejected AI | 2 (`TC-FR14-034`, `TC-FR14-036`) |
| Usable corrected AI-derived | 40 |
| Accepted Human | 6 (`TC-FR14-H01..H06`) |
| Rejected Human candidate | 1 (`TC-FR14-H07`) |
| Final formal cases | **46** |

## Oracle Policy

- Exact 400/401/403/404/409 and exact message/schema assertions are not normative unless explicitly sourced.
- Binding mutation rejections use any 4xx/non-success plus API-visible state verification.
- Valid CRUD uses success class plus API-visible state.
- Name-validation cases require that invalid empty/missing names are not persisted.
- Nonexistent-ID cases use a weak false-success oracle, not exact 404.
- Unspecified behaviors are partial or exploratory and cannot create product bugs.

## Formal Inventory

| Dimension | Accepted IDs | Count | Oracle Class |
|---|---|---:|---|
| Public and valid CRUD | 001-006, 015, 035 | 8 | Specification-backed / state-based |
| JWT authentication | 007-011 | 5 | SEC-02 specification-backed |
| Admin RBAC | 012-014 | 3 | FR-12 / SEC-03 specification-backed |
| Mandatory name | 016-019 | 4 | FR-14 specification-backed |
| Name boundary/type | 020-023 | 4 | Exploratory |
| Nonexistent/invalid IDs | 024-028, 037-038 | 7 | Partial or exploratory |
| Security and request-shape probes | 029-033 | 5 | SEC-05 plus partial/exploratory |
| Response-shape observations | 039-042 | 4 | Partial oracle |
| Human extensions | H01-H06 | 6 | 2 specification-backed, 3 partial, 1 exploratory |
| **Total** | | **46** | |

## Confirmed Rejection Log

- `TC-FR14-034`: categories have no user ownership model; mislabeled IDOR and duplicate of User DELETE RBAC case 014.
- `TC-FR14-036`: no Level-1 category/product referential-integrity rule; destructive seeded dependency.
- `TC-FR14-H07`: depends on rejected 036 and repeats the same out-of-scope relational observation.

## Fixture Strategy

- Create deterministic unique names per run.
- Never mutate/delete seeded category IDs for final formal cases.
- RBAC and validation defects use disposable fixtures or unique names.
- Capture mutation IDs as variables and verify via public GET list.
- Reset collection variables at run start.
- Derive Admin/User JWTs at runtime; no hardcoded live tokens.
- Add `X-Student-Id: 23127259` to every request and every script-generated verification request.

## Verdict Vocabulary

Each formal ID receives exactly one final verdict after execution:

- `PASS`
- `FAIL - NORMATIVE ORACLE VIOLATION`
- `BLOCKED - HARNESS/SETUP`
- `PARTIAL-ORACLE OBSERVATION`
- `EXPLORATORY OBSERVATION`

## Canonical Source

`fr14_canonical_cases.json` is the machine-readable 46-case map. `FR14_CANONICAL_PROVENANCE_MAP.md` is its grader-readable rendering.
