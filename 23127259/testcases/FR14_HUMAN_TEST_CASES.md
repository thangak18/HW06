# FR14 Human-Designed Extension Cases

## Accounting

- Accepted Human IDs: `TC-FR14-H01..H06`
- Count: 6
- Rejected candidate: `TC-FR14-H07` (out-of-scope referential dependency)

### TC-FR14-H01 - Missing Content-Type POST

- **Gap:** `GAP-H01`
- **Actor:** Admin with runtime JWT
- **Request:** `POST /api/categories`, raw JSON text, no `Content-Type`
- **Oracle:** exploratory. Record status/body and whether an entity is created. HTTP 500 is a robustness observation, not a normative bug.
- **Distinctness:** tests MIME/body-parser behavior rather than a JSON value partition.

### TC-FR14-H02 - Zero-Byte POST Body

- **Gap:** `GAP-H02`
- **Actor:** Admin
- **Request:** `POST /api/categories` with `Content-Type: application/json` and zero bytes
- **Oracle:** the request does not establish the mandatory name. Use non-success/no invalid persistence as partial FR-14 oracle; do not require exact 400.
- **Distinctness:** zero bytes differ from the raw AI `{}` object case.

### TC-FR14-H03 - Unsupported PATCH

- **Gap:** `GAP-H03`
- **Actor:** Admin
- **Fixture:** isolated category created for this case
- **Request:** `PATCH /api/categories/:id` with a changed name
- **Oracle:** non-success and subsequent GET shows the original name unchanged. Exact 404/405 is not required.
- **Distinctness:** no AI case tested a method absent from the API specification.

### TC-FR14-H04 - Response MIME Observation

- **Gap:** `GAP-H04`
- **Actor:** public caller
- **Request:** `GET /api/categories`
- **Oracle:** partial observation of JSON parseability and response `Content-Type`; not a normative defect if formatting differs.
- **Distinctness:** isolates transport header behavior from body-shape tests.

### TC-FR14-H05 - Empty PUT Body Corruption

- **Gap:** `GAP-H05`
- **Actor:** Admin
- **Fixture:** isolated category with a valid non-empty name
- **Request:** `PUT /api/categories/:id` with `{}`
- **Normative oracle:** a missing name must not replace the valid name with null/empty. Any error status is acceptable; if success, follow-up GET must still show the original name.
- **Defect mapping:** persisted null/empty name joins `BUG-FR14-002`, not a new root cause.
- **Distinctness:** tests update corruption rather than invalid create.

### TC-FR14-H06 - Rapid Multi-Entity Create Isolation

- **Gap:** `GAP-H06`
- **Actor:** Admin
- **Requests:** three sequential POSTs with deterministic unique names, followed by GET verification
- **Oracle:** all successful creates yield distinct entity identities and all names are independently API-visible. Strict monotonic-ID ordering is observed, not required.
- **Distinctness:** covers multi-entity isolation absent from single-create AI cases.

## Human Extension Gate

**PASS - 6 DISTINCT POST-AUDIT HUMAN CASES**
