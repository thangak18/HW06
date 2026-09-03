# FR14 Human Audit of 42 Raw AI Cases

- **Raw source:** `testcases/FR14_AI_DRAFT.md`
- **Frozen SHA-256:** `95ac502b0880efcc1c6ceb040a1171eeacebff5c262a5f6df8d49a86cadcaf70`
- **Audit basis:** assignment, SRS FR-12/FR-14/SEC-02/SEC-03/SEC-05, API specification §3.4
- **Audit result:** **3 VALID, 2 INVALID, 37 INCOMPLETE; 40 usable after correction**

The preliminary Anti audit (39 VALID, 3 INCOMPLETE) was rejected because it treated implementation behavior, REST conventions, exact response codes, and example response bodies as normative requirements. This table evaluates the immutable raw generation, not the later collection.

## Complete Decision Table

| Raw ID | Verdict | Human Reasoning | Required Correction / Disposition |
|---|:---:|---|---|
| `TC-FR14-001` | INCOMPLETE | Public list objective is valid, but exact seed count/order/id/name and exact element schema are not Level-1 requirements. | Assert successful list retrieval and observable category entities; treat seed/schema detail as partial observation. |
| `TC-FR14-002` | INCOMPLETE | Valid Admin creation is normative; exact 200, message text, and response schema are unspecified. | Accept success class and require API-visible created entity through GET. |
| `TC-FR14-003` | VALID | Read-after-create verifies the core CRUD persistence effect without inventing a defect. | None. |
| `TC-FR14-004` | INCOMPLETE | PUT route is normative; exact 200/message is not. | Require successful update and GET-visible name change for only the target category. |
| `TC-FR14-005` | VALID | Read-after-update verifies the required CRUD state effect. | None. |
| `TC-FR14-006` | INCOMPLETE | Valid Admin delete is normative; exact 200/message is not. | Require successful deletion and GET-visible absence. |
| `TC-FR14-007` | INCOMPLETE | Missing JWT must be rejected, but exact 401 and error JSON are unspecified. | Assert non-success and no created category. Map to SEC-02, not SEC-01. |
| `TC-FR14-008` | INCOMPLETE | Missing JWT update test is valid; exact 401/error schema is not. | Assert non-success and unchanged target state. |
| `TC-FR14-009` | INCOMPLETE | Missing JWT delete test is valid; exact 401/error schema is not. | Assert non-success and target remains present. |
| `TC-FR14-010` | INCOMPLETE | Invalid JWT must be rejected; exact 403/message is unspecified. | Assert 4xx/non-success and no mutation. |
| `TC-FR14-011` | INCOMPLETE | Tampered-token objective is valid, but a hardcoded pseudo-token and exact 403 are weak. | Derive a tampered token from a valid Admin JWT at runtime; assert non-success and no deletion. |
| `TC-FR14-012` | INCOMPLETE | Normal User creation must be rejected under FR-12/SEC-03; exact 403 is unspecified. | Assert 4xx/non-success plus no GET-visible creation. |
| `TC-FR14-013` | INCOMPLETE | Normal User update must be rejected; exact 403 is unspecified. | Use isolated fixture; assert 4xx/non-success and unchanged state. |
| `TC-FR14-014` | INCOMPLETE | Normal User delete must be rejected; exact 403 is unspecified. | Use isolated fixture; assert 4xx/non-success and target remains present. |
| `TC-FR14-015` | VALID | Authenticated User can call the public list route; no mutation or over-specific negative oracle is involved. | None. |
| `TC-FR14-016` | INCOMPLETE | Empty name violates explicit FR-14, but exact 400 is unspecified. | Assert non-success or, if SUT returns success, confirm invalid entity persistence as BUG-FR14-002. |
| `TC-FR14-017` | INCOMPLETE | Null does not satisfy a mandatory non-empty name; exact 400 is unspecified. | Same weak status/persistence oracle as TC-016. |
| `TC-FR14-018` | INCOMPLETE | Missing key does not satisfy the mandatory name; exact 400 is unspecified. | Same weak status/persistence oracle as TC-016. |
| `TC-FR14-019` | INCOMPLETE | Whitespace-only is semantically empty; exact 400 is unspecified. | Same weak status/persistence oracle as TC-016. |
| `TC-FR14-020` | INCOMPLETE | No maximum name length exists in Level-1. | Make an exploratory 1,001-character robustness observation; do not require 200 or 400. |
| `TC-FR14-021` | INCOMPLETE | Unicode support is not expressly specified. | Retain as exploratory interoperability check with read-after-write observation. |
| `TC-FR14-022` | INCOMPLETE | Duplicate-name uniqueness and 409 are unspecified. | Retain as exploratory; accept documented observed behavior without a normative failure. |
| `TC-FR14-023` | INCOMPLETE | Name type/coercion is unspecified beyond the string example. | Retain as exploratory type-handling observation; do not require 400 or 200. |
| `TC-FR14-024` | INCOMPLETE | Exact 404 for nonexistent update is invented. | Use weak CRUD-integrity oracle: response must not falsely claim a successful update of a nonexistent entity. |
| `TC-FR14-025` | INCOMPLETE | Exact 404 for nonexistent delete is invented. | Use weak CRUD-integrity oracle: response must not falsely claim a successful deletion of a nonexistent entity. |
| `TC-FR14-026` | INCOMPLETE | Zero-ID status behavior is unspecified. | Exploratory safe-handling observation; no exact status oracle. |
| `TC-FR14-027` | INCOMPLETE | Negative-ID behavior is unspecified. | Exploratory safe-handling observation; no exact status oracle. |
| `TC-FR14-028` | INCOMPLETE | Non-numeric-ID behavior is unspecified. | Exploratory safe-handling observation; no exact status oracle. |
| `TC-FR14-029` | INCOMPLETE | SEC-05 objective is valid; exact 200 and literal storage are not required. | Assert no injection effect/table loss; note black-box limitation. |
| `TC-FR14-030` | INCOMPLETE | SEC-04 is UI escaping; raw JSON storage cannot prove or violate UI rendering. | Retain only as UI-scoped exploratory persistence observation. |
| `TC-FR14-031` | INCOMPLETE | Extra-field behavior and SEC-07 mapping are unsupported (SEC-07 concerns OTP). | Retain as partial request-schema observation; assert no unintended ID/role property effect. |
| `TC-FR14-032` | INCOMPLETE | Body-ID override handling is not explicitly specified. | Retain as partial path-vs-body identity observation, without SEC-07 claim. |
| `TC-FR14-033` | INCOMPLETE | NoSQL payload is irrelevant to SQLite and exact response is unspecified. | Reframe as generic object-type robustness observation; no normative pass/fail. |
| `TC-FR14-034` | INVALID | Categories have no user ownership model; this is mislabeled IDOR and duplicates TC-FR14-014's User DELETE RBAC scenario. | Reject from canonical execution. |
| `TC-FR14-035` | INCOMPLETE | Full lifecycle sequence is valuable; exact 200 at every step is over-specific and shared fixtures risk contamination. | Use an isolated unique category and success-class plus GET-visible state transitions. |
| `TC-FR14-036` | INVALID | Category/product referential policy is absent from FR-14; the case is cross-feature and destructively targets seeded data. | Reject from canonical execution; preserve only as historical exploratory candidate on Anti branch. |
| `TC-FR14-037` | INCOMPLETE | Exact 404 for update-after-delete is unspecified. | Use weak false-success/no-op oracle on an isolated deleted fixture. |
| `TC-FR14-038` | INCOMPLETE | Exact 404 for double delete is unspecified. | Use weak false-success/no-op oracle on an isolated deleted fixture. |
| `TC-FR14-039` | INCOMPLETE | Exact GET element schema/content-type is not defined by API spec. | Treat observed `id`/`name` array structure as partial-oracle schema evidence. |
| `TC-FR14-040` | INCOMPLETE | Exact POST response fields/message are implementation-derived. | Assert only success plus GET-visible creation; record schema as partial observation. |
| `TC-FR14-041` | INCOMPLETE | Exact PUT response message is implementation-derived. | Assert success plus GET-visible update; record schema as partial observation. |
| `TC-FR14-042` | INCOMPLETE | Exact DELETE response message is implementation-derived. | Assert success plus GET-visible absence; record schema as partial observation. |

## Accounting

- Raw AI: 42
- Audited: 42
- VALID: 3
- INVALID: 2 (`TC-FR14-034`, `TC-FR14-036`)
- INCOMPLETE: 37
- Corrected usable AI-derived: 40
- Rejected raw IDs must not appear in the final collection.

## Audit Gate

**PASS - EVERY RAW AI CASE CLASSIFIED; IMPLEMENTATION-DERIVED ORACLES REMOVED**
