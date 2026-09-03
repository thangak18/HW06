# BUG-FR14-004 — Issue Body Template

This body is intended for issue creation on GitHub.
Cannot be created from sandbox without a personal access token.

## Title

[BUG-FR14-004] Empty PUT Body Corrupts Existing Category Name to null

## Body

## Bug Report: BUG-FR14-004

**Feature:** FR-14 Category Management CRUD (Pool C - Web Admin)
**Severity:** Medium
**Security Mapping:** SEC-02 (Input Validation on Update Operations)

### Summary

A `PUT /api/categories/:id` request with an empty JSON body (`{}`) against an existing category succeeds with HTTP 200 OK but silently overwrites the existing valid `name` field with `null`, corrupting the persisted data and violating FR-14's mandatory-name rule.

### Level-1 Authoritative Oracle

- **SRS Section 6 (FR-14):** Category `name` is mandatory and must not be empty/null.
- **SRS Section 9 (SEC-02):** Update operations must validate mandatory fields and not corrupt existing data.

### Expected Behavior

Either reject the request with a 4xx error (preferred), or preserve the original `name` unchanged. The existing valid name must NOT be silently overwritten with `null` or empty string.

### Actual Behavior

Empty PUT body `{}` returns HTTP 200 OK with response body `{"message":"Category updated"}`. Subsequent GET shows the category's `name` is now `null`.

### Reproduction

1. Login as admin.
2. Create a category with name "EmptyPutTarget" via POST /api/categories.
3. Capture the new category ID.
4. Send PUT /api/categories/{id} with body `{}`.
5. Send GET /api/categories.

### Evidence

- Newman Run01 Report: `23127259/evidence/fr14/newman/FR14-run01.json`
- Affected formal ID: TC-FR14-H05

### Screenshots

PASS (pixel-audited 2026-09-03)
