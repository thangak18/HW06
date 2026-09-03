# FR14 Human Audit Correction Policy

This ledger converts the 37 INCOMPLETE raw AI cases into executable, source-grounded cases without changing the frozen raw draft.

## Global Corrections

1. Replace exact authentication/authorization status expectations with `4xx/non-success` unless Level-1 states an exact code.
2. For mutation rejection, verify API-visible state when practical; status alone is not persistence proof.
3. For valid CRUD, use success class plus GET-visible state instead of exact message/schema.
4. Name-validation cases use the FR-14 mandatory/non-empty rule but do not require exact 400.
5. Nonexistent-ID cases use a weak false-success oracle, not exact 404.
6. Duplicate, length, Unicode, numeric-name, invalid-ID, content-type, and response-schema behaviors are exploratory/partial where unspecified.
7. SEC-02 means valid JWT enforcement; SEC-03 means Admin-role enforcement; SEC-04 is UI escaping; SEC-05 is parameterized query; SEC-07 is OTP and does not apply.
8. All fixtures are unique and isolated. No final test deletes seeded categories.
9. Every HTTP operation carries `X-Student-Id: 23127259`.

## Rejected Raw Cases

| ID | Reason |
|---|---|
| `TC-FR14-034` | Mislabelled IDOR and semantic duplicate of User DELETE RBAC case TC-FR14-014. |
| `TC-FR14-036` | Unspecified cross-feature referential-integrity policy and destructive seeded-data dependency. |

## Corrected Oracle Families

| Family | Raw IDs | Corrected Executable Oracle |
|---|---|---|
| Public/valid CRUD | 001-006, 015, 035, 039-042 | Success where behavior is normative; GET-visible state; schema detail partial only. |
| JWT authentication | 007-011 | 4xx/non-success; no state mutation; runtime-derived tampered token for 011. |
| Admin RBAC | 012-014 | 4xx/non-success and no created/updated/deleted state. |
| Mandatory name | 016-019 | Non-success; if success, confirm invalid API-visible persistence as one validation defect cluster. |
| Unspecified name/type behavior | 020-023 | Exploratory observation; no invented defect. |
| Nonexistent-ID integrity | 024-025, 037-038 | Response may use any status, but must not falsely report a successful mutation/deletion of no entity. |
| Malformed/boundary IDs | 026-028 | Exploratory safe-handling observation. |
| Security probes | 029-033 | SEC-05 behavioral resistance for 029; UI/partial/robustness observations for 030-033. |

## Result

40 AI-derived cases remain usable after correction, exceeding the assignment minimum of 35.
