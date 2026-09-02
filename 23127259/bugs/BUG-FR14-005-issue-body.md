## Title
[Bug][FR14] Already-deleted category PUT/DELETE returns false success

## Body
### Severity
MEDIUM — Data-integrity defect; API claims successful mutation of a
non-existent entity.

### Feature Under Test
FR-14 Category Management (CRUD).

### Reproduction
1. Login as admin.
2. Create category `ZombieTarget` via `POST /api/categories`.
3. Capture the new category ID.
4. Delete the category via `DELETE /api/categories/{id}`.
5. Send `PUT /api/categories/{id}` with `{"name":"ZombieResurrected"}`.
6. Send `DELETE /api/categories/{id}` again.
7. Verify via `GET /api/categories`.

### Expected
PUT/DELETE on an already-deleted category must not falsely report
success. Any accurate non-success response is acceptable.

### Actual
Both PUT and DELETE return **200 OK** with success-style payloads
("Category updated" / "Category deleted").

### Affected Tests
- TC-FR14-037 (PUT on already-deleted)
- TC-FR14-038 (DELETE on already-deleted)

### Newman Evidence
- Run01 CLI: `23127259/evidence/fr14/newman/FR14-run01-cli.txt`
- Run01 JSON: `23127259/evidence/fr14/newman/FR14-run01.json`
- Run01 HTML: `23127259/evidence/fr14/newman/FR14-run01.html`

### Requirement Source
- SRS FR-14 (CRUD must reflect actual persisted state)
- API specification §3.4 (PUT/DELETE on existing entities)

### Visual Evidence
Pending Codex visual audit. Screenshot path placeholder
`23127259/evidence/fr14/bugs/BUG-FR14-005-*.png`.
