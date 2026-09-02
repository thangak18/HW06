# FR14 Post-Audit Gap Analysis and Human Extension Selection

## Sequence Control

This gap analysis was performed **after** the complete 42-case Human Audit. It uses the 40 usable corrected AI-derived cases and does not alter the frozen raw draft.

## Coverage Gaps

| Gap | Missing Coverage | Level-1 Strength | Selection |
|---|---|---|---|
| `GAP-H01` | POST body with no `Content-Type` | Unspecified transport robustness | `TC-FR14-H01` exploratory |
| `GAP-H02` | True zero-byte POST body vs JSON `{}` | Mandatory name overlaps FR-14; transport details unspecified | `TC-FR14-H02` exploratory/partial |
| `GAP-H03` | Unsupported PATCH must not invoke documented PUT behavior | API specification defines PUT, not PATCH | `TC-FR14-H03` specification-backed non-success/no mutation |
| `GAP-H04` | Response MIME/header observation | Exact header unspecified | `TC-FR14-H04` partial-oracle observation |
| `GAP-H05` | Missing-name update may erase an existing valid name | FR-14 mandatory non-empty name | `TC-FR14-H05` normative mutation-integrity test |
| `GAP-H06` | Multiple independent rapid creates and ID/entity isolation | CRUD persistence; ordering details unspecified | `TC-FR14-H06` partial stress/isolation observation |

## Rejected Candidate Extension

`TC-FR14-H07` from the Anti candidate is rejected. It depends on rejected raw `TC-FR14-036`, deletes seeded category 1, crosses into product referential integrity, and relies on a policy absent from FR-14. The historical candidate remains available only on `thang/fr14-anti`.

## AI Blind-Spot Analysis

- The AI focused on JSON values and missed transport-level absence of headers and body bytes.
- It followed documented verbs and omitted a negative method dispatch.
- It asserted body schemas but did not explicitly distinguish partial header observations.
- It tested missing names on create but missed corruption of an existing name through update.
- It tested isolated single creates but not rapid multi-entity isolation.

## Selected Human Cases

Six Human cases are retained, exceeding the assignment minimum of five. They are distinct from the 40 usable AI-derived cases and use isolated fixtures wherever state changes.
