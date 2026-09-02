# FR14 Execution Traceability Plan

| Formal IDs | Provenance | Collection Dimension | Actor | Fixture / Verification | Expected Final Classification |
|---|---|---|---|---|---|
| 001-006 | AI corrected | Happy-path CRUD | Public/Admin | isolated lifecycle variables + GET | PASS |
| 007-011 | AI corrected | Authentication | Missing/invalid JWT | disposable targets + GET | PASS if rejected |
| 012-014 | AI corrected | RBAC | `role=user` | unique create/isolated update-delete + GET | normative FAIL if mutation succeeds |
| 015 | AI valid | Public read boundary | User | none | PASS |
| 016-019 | AI corrected | Mandatory name | Admin | deterministic invalid names + GET | normative FAIL if invalid entity persists |
| 020-023 | AI corrected | Name exploratory | Admin | unique names + observations | exploratory |
| 024-025, 037-038 | AI corrected | Nonexistent CRUD integrity | Admin | guaranteed nonexistent IDs | normative/partial false-success finding |
| 026-028 | AI corrected | Invalid ID robustness | Admin | no shared state | exploratory |
| 029 | AI corrected | SEC-05 probe | Admin | unique payload + table/list verification | PASS/partial |
| 030-033 | AI corrected | UI/request-shape robustness | Admin | isolated observations | partial/exploratory |
| 035 | AI corrected | Full lifecycle | Admin | isolated create/update/delete + GET | PASS |
| 039-042 | AI corrected | Response shapes | Public/Admin | state assertions take priority | partial oracle |
| H01-H06 | Human | Post-audit gaps | Public/Admin | isolated fixtures where mutating | mixed normative/partial/exploratory |

Rejected IDs 034, 036, and H07 must have zero executable collection items.
