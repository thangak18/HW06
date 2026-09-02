# FR14 Category CRUD - Level-1 Requirement Analysis

## Scope and Source Hierarchy

- **Feature:** FR-14 Category Management (CRUD), Pool C.
- **Assignment:** requires a full AI generate -> Human Audit -> Human extension -> execute -> bug-report pipeline.
- **Normative SRS:** `/Volumes/Thang/eshop-sut/README.md`, FR-12, FR-14, SEC-02, SEC-03, SEC-05.
- **Endpoint specification:** `/Volumes/Thang/eshop-sut/api_specification.md`, §3.4.
- **Runtime/source observations:** harness compatibility and defect confirmation only; never product oracle.

## Normative Endpoint and Actor Matrix

| Operation | Route | Actor / Auth | Normative Behavior |
|---|---|---|---|
| List | `GET /api/categories` | Public | Return the category list. |
| Create | `POST /api/categories` | Valid JWT with `role=admin` | Create a category from JSON `{"name":"..."}`. |
| Update | `PUT /api/categories/:id` | Valid JWT with `role=admin` | Update the named category. |
| Delete | `DELETE /api/categories/:id` | Valid JWT with `role=admin` | Delete the named category. |

The API specification supplies all four CRUD methods. The SRS FR-14 heading says CRUD and expressly describes Add/View/Delete; the PUT route is therefore retained from the endpoint specification. SRS FR-12 explicitly makes every data-affecting category route Admin-only.

## Binding Rules

1. `POST`, `PUT`, and `DELETE /api/categories[/:id]` require a valid JWT (SEC-02).
2. Those mutations require `role = 'admin'` (FR-12 / SEC-03). A normal `role=user` token must not mutate category state.
3. Category `name` is mandatory and must not be empty (FR-14). Empty string, missing value, and null do not establish a valid required name. Whitespace-only input is treated as semantically empty.
4. Valid CRUD operations must be API-visible through later GET list observations.
5. Category database queries must resist injection through parameterized execution (SEC-05). A black-box probe can establish behavioral resistance but cannot alone prove query construction.
6. `X-Student-Id: 23127259` is an assignment execution requirement on every HTTP operation, including setup and verification.

## Oracle Boundary - Not Specified

The Level-1 sources do **not** define:

- exact 400/401/403/404/409 response codes for failures;
- exact error-message keys or text;
- exact success response messages or complete JSON schemas;
- category-name uniqueness;
- maximum name length or accepted character set;
- whether numeric names are coerced or rejected;
- exact behavior for zero, negative, malformed, or nonexistent IDs;
- missing/unsupported `Content-Type` behavior;
- same-operation idempotency semantics;
- category/product referential-integrity policy;
- UI rendering behavior from raw API JSON.

Tests in these areas use the weakest supported oracle and are classified as partial or exploratory unless they overlap a binding rule above. Runtime behavior never upgrades an unspecified convention into a normative requirement.

## Defect-Candidate Rules

| Candidate | Level-1 Decision |
|---|---|
| Normal User successfully mutates categories | Normative FR-12 / SEC-03 violation if reproduced with persisted state change. |
| Empty/null/missing/whitespace name accepted | Normative FR-14 violation if an invalid category is actually created or an existing category is corrupted. Exact 400 is not required. |
| Nonexistent update/delete reports success | Weak CRUD-integrity oracle: no exact 404. Confirm only if the API falsely reports a successful modification/deletion rather than an accurate no-op/not-found outcome. |
| Missing Content-Type returns 500 | Exploratory robustness observation unless a stronger source is found. |
| Duplicate name accepted | Exploratory; uniqueness is unspecified. |
| Category deletion orphans products | Exploratory cross-feature relational observation; no FR-14 referential policy exists. |

## Harness Compatibility Observations

- Runtime routes are exactly `/api/categories` as specified.
- Default Admin/user accounts come from the SRS setup data.
- The current implementation returns 200 for many mutations; these observations are not used to define expected behavior.

## Analysis Gate

**PASS - LEVEL-1 ORACLE ESTABLISHED BEFORE SENIOR QA DERIVATION**
