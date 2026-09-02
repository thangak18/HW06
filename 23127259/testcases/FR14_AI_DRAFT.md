# FR-14 AI-Generated Test Cases — Raw Draft

**Feature:** FR-14 – Category Management CRUD  
**Student:** Nguyễn Tấn Thắng (23127259)  
**Generation Date:** September 2, 2026  
**Generation Stage:** Phase 1A — Step-by-Step AI Test Design  
**Authoritative Sources:** FR14_REQUIREMENT_ANALYSIS.md, SUT source code, HW06 Assignment Specification  
**Target Count:** ≥42 raw cases (before human audit filtering)

---

## Interaction 1: Happy-Path CRUD Operations (6 cases)

### TC-FR14-001: GET — List all categories (public, no auth)
- **Dimension:** Happy Path / Schema Validation
- **Endpoint:** `GET /api/categories`
- **Precondition:** SUT is freshly seeded (3 default categories)
- **Headers:** `X-Student-Id: 23127259` (no Authorization)
- **Request Body:** None
- **Expected HTTP Status:** 200 OK
- **Expected Response:** JSON array of objects, each containing `id` (integer) and `name` (string). At minimum 3 seeded categories.
- **Oracle:** Response is array with length ≥ 3. First element has `id` = 1, `name` = "Điện thoại".
- **Partition Coverage:** EP-TK-03 (no auth needed for GET)

### TC-FR14-002: POST — Create category with valid name (admin)
- **Dimension:** Happy Path / CRUD Create
- **Endpoint:** `POST /api/categories`
- **Precondition:** Admin is authenticated
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Tablet" }`
- **Expected HTTP Status:** 200
- **Expected Response:** `{ "message": "Category created", "id": <positive integer> }`
- **Oracle:** Response `id` is a positive integer. Subsequent GET confirms new category in list.
- **Partition Coverage:** EP-NM-01 (valid name), EP-TK-01 (admin token)

### TC-FR14-003: GET — Verify created category appears in list
- **Dimension:** Happy Path / State Verification
- **Endpoint:** `GET /api/categories`
- **Precondition:** TC-FR14-002 has executed (new "Tablet" category exists)
- **Headers:** `X-Student-Id: 23127259`
- **Request Body:** None
- **Expected HTTP Status:** 200
- **Expected Response:** Array includes object with `name` = "Tablet"
- **Oracle:** Array length is one more than before creation. Last/new entry matches created category.
- **Partition Coverage:** Read-after-write verification

### TC-FR14-004: PUT — Update existing category name (admin)
- **Dimension:** Happy Path / CRUD Update
- **Endpoint:** `PUT /api/categories/{{createdCategoryId}}`
- **Precondition:** Category from TC-FR14-002 exists
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Tablets & iPads" }`
- **Expected HTTP Status:** 200
- **Expected Response:** `{ "message": "Category updated" }`
- **Oracle:** Subsequent GET shows category name changed to "Tablets & iPads"
- **Partition Coverage:** EP-NM-01, EP-ID-01

### TC-FR14-005: GET — Verify updated category name
- **Dimension:** Happy Path / State Verification
- **Endpoint:** `GET /api/categories`
- **Precondition:** TC-FR14-004 has executed
- **Headers:** `X-Student-Id: 23127259`
- **Request Body:** None
- **Expected HTTP Status:** 200
- **Expected Response:** Array includes object with updated name "Tablets & iPads"
- **Oracle:** Category entry shows new name.

### TC-FR14-006: DELETE — Remove existing category (admin)
- **Dimension:** Happy Path / CRUD Delete
- **Endpoint:** `DELETE /api/categories/{{createdCategoryId}}`
- **Precondition:** Category from TC-FR14-002 exists
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Request Body:** None
- **Expected HTTP Status:** 200
- **Expected Response:** `{ "message": "Category deleted" }`
- **Oracle:** Subsequent GET confirms category no longer in list.
- **Partition Coverage:** EP-ID-01

---

## Interaction 2: Authentication Enforcement (5 cases)

### TC-FR14-007: POST — Create category without auth token
- **Dimension:** Security / SEC-01
- **Endpoint:** `POST /api/categories`
- **Precondition:** No authentication
- **Headers:** `X-Student-Id: 23127259`, `Content-Type: application/json` (NO Authorization header)
- **Request Body:** `{ "name": "Unauthorized Category" }`
- **Expected HTTP Status:** 401 Unauthorized
- **Expected Response:** `{ "error": "Unauthorized" }`
- **Oracle:** Category NOT created. GET list does not contain "Unauthorized Category".
- **Partition Coverage:** EP-TK-03

### TC-FR14-008: PUT — Update category without auth token
- **Dimension:** Security / SEC-01
- **Endpoint:** `PUT /api/categories/1`
- **Precondition:** No authentication
- **Headers:** `X-Student-Id: 23127259`, `Content-Type: application/json` (NO Authorization header)
- **Request Body:** `{ "name": "Hacked Name" }`
- **Expected HTTP Status:** 401 Unauthorized
- **Expected Response:** `{ "error": "Unauthorized" }`
- **Oracle:** Category name unchanged in GET.
- **Partition Coverage:** EP-TK-03

### TC-FR14-009: DELETE — Delete category without auth token
- **Dimension:** Security / SEC-01
- **Endpoint:** `DELETE /api/categories/1`
- **Precondition:** No authentication
- **Headers:** `X-Student-Id: 23127259` (NO Authorization header)
- **Expected HTTP Status:** 401 Unauthorized
- **Expected Response:** `{ "error": "Unauthorized" }`
- **Oracle:** Category still exists in GET list.
- **Partition Coverage:** EP-TK-03

### TC-FR14-010: POST — Create category with malformed token
- **Dimension:** Security / SEC-01
- **Endpoint:** `POST /api/categories`
- **Precondition:** Using invalid/random JWT string
- **Headers:** `Authorization: Bearer invalid.token.here`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Malformed Token Category" }`
- **Expected HTTP Status:** 403 Forbidden
- **Expected Response:** `{ "error": "Forbidden" }`
- **Oracle:** Category NOT created.
- **Partition Coverage:** EP-TK-04

### TC-FR14-011: DELETE — Delete category with tampered token
- **Dimension:** Security / SEC-01
- **Endpoint:** `DELETE /api/categories/1`
- **Precondition:** Using tampered JWT (valid format but wrong signature)
- **Headers:** `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIn0.TAMPERED_SIGNATURE`, `X-Student-Id: 23127259`
- **Expected HTTP Status:** 403 Forbidden
- **Expected Response:** `{ "error": "Forbidden" }`
- **Oracle:** Category still exists.
- **Partition Coverage:** EP-TK-05

---

## Interaction 3: Authorization / RBAC (SEC-02) (4 cases)

### TC-FR14-012: POST — Regular user creates category (RBAC violation test)
- **Dimension:** Security / SEC-02 / Authorization
- **Endpoint:** `POST /api/categories`
- **Precondition:** Authenticated as regular user (role=user)
- **Headers:** `Authorization: Bearer {{userToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "User Created Category" }`
- **Expected HTTP Status (per SRS):** 403 Forbidden (only admin should manage categories)
- **SUT Predicted Behavior:** ⚠️ 200 OK — SUT lacks role check (BUG-FR14-CAND-01)
- **Oracle:** If 200 returned, this confirms missing RBAC bug.
- **Partition Coverage:** EP-TK-02

### TC-FR14-013: PUT — Regular user updates category (RBAC violation test)
- **Dimension:** Security / SEC-02 / Authorization
- **Endpoint:** `PUT /api/categories/1`
- **Precondition:** Authenticated as regular user (role=user)
- **Headers:** `Authorization: Bearer {{userToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "User Modified Name" }`
- **Expected HTTP Status (per SRS):** 403 Forbidden
- **SUT Predicted Behavior:** ⚠️ 200 OK — confirms missing RBAC
- **Partition Coverage:** EP-TK-02

### TC-FR14-014: DELETE — Regular user deletes category (RBAC violation test)
- **Dimension:** Security / SEC-02 / Authorization
- **Endpoint:** `DELETE /api/categories/{{userCreatedCategoryId}}`
- **Precondition:** Authenticated as regular user (role=user), category exists
- **Headers:** `Authorization: Bearer {{userToken}}`, `X-Student-Id: 23127259`
- **Expected HTTP Status (per SRS):** 403 Forbidden
- **SUT Predicted Behavior:** ⚠️ 200 OK — confirms missing RBAC
- **Partition Coverage:** EP-TK-02

### TC-FR14-015: GET — Regular user can list categories (public endpoint)
- **Dimension:** Authorization / Boundary
- **Endpoint:** `GET /api/categories`
- **Precondition:** Authenticated as regular user
- **Headers:** `Authorization: Bearer {{userToken}}`, `X-Student-Id: 23127259`
- **Expected HTTP Status:** 200 OK
- **Expected Response:** Array of category objects
- **Oracle:** GET is public and should work for any caller.
- **Partition Coverage:** Positive auth boundary

---

## Interaction 4: Input Validation — Name Parameter (8 cases)

### TC-FR14-016: POST — Empty name string
- **Dimension:** Domain Partition / Input Validation
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "" }`
- **Expected HTTP Status (ideal):** 400 Bad Request
- **SUT Predicted Behavior:** ⚠️ 200 OK — no validation (BUG-FR14-CAND-02)
- **Partition Coverage:** EP-NM-02

### TC-FR14-017: POST — Null name value
- **Dimension:** Domain Partition / Input Validation
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": null }`
- **Expected HTTP Status (ideal):** 400 Bad Request
- **SUT Predicted Behavior:** ⚠️ 200 OK — null stored as TEXT NULL
- **Partition Coverage:** EP-NM-03

### TC-FR14-018: POST — Missing name key in body
- **Dimension:** Domain Partition / Input Validation
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{}`
- **Expected HTTP Status (ideal):** 400 Bad Request
- **SUT Predicted Behavior:** ⚠️ 200 OK — undefined stored
- **Partition Coverage:** EP-NM-04

### TC-FR14-019: POST — Whitespace-only name
- **Dimension:** Domain Partition / Input Validation
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "   " }`
- **Expected HTTP Status (ideal):** 400 Bad Request
- **SUT Predicted Behavior:** ⚠️ 200 OK — whitespace stored as-is
- **Partition Coverage:** EP-NM-05

### TC-FR14-020: POST — Very long name (boundary)
- **Dimension:** Boundary / Input Validation
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "<1001 character string>" }`
- **Expected HTTP Status (ideal):** 400 Bad Request (or 200 if no limit)
- **SUT Predicted Behavior:** 200 OK — SQLite TEXT has no length limit
- **Partition Coverage:** EP-NM-06

### TC-FR14-021: POST — Unicode/special characters in name
- **Dimension:** Domain Partition / Internationalization
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Điện tử 📱 & Phụ kiện" }`
- **Expected HTTP Status:** 200 OK
- **Expected Response:** `{ "message": "Category created", "id": <int> }`
- **Oracle:** Subsequent GET shows name with Unicode preserved correctly.
- **Partition Coverage:** EP-NM-07

### TC-FR14-022: POST — Duplicate category name
- **Dimension:** Domain Partition / Business Logic
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Điện thoại" }` (already exists in seed data)
- **Expected HTTP Status (ideal):** 409 Conflict (or 400)
- **SUT Predicted Behavior:** ⚠️ 200 OK — no uniqueness constraint
- **Partition Coverage:** EP-NM-08

### TC-FR14-023: POST — Integer value instead of string for name
- **Dimension:** Domain Partition / Type Safety
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": 12345 }`
- **Expected HTTP Status (ideal):** 400 Bad Request
- **SUT Predicted Behavior:** 200 OK — SQLite coerces to text "12345"
- **Partition Coverage:** EP-NM-11

---

## Interaction 5: Input Validation — ID Parameter (5 cases)

### TC-FR14-024: PUT — Non-existent category ID
- **Dimension:** Domain Partition / Boundary
- **Endpoint:** `PUT /api/categories/99999`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Ghost Category" }`
- **Expected HTTP Status (ideal):** 404 Not Found
- **SUT Predicted Behavior:** ⚠️ 200 OK — no existence check (BUG-FR14-CAND-03)
- **Partition Coverage:** EP-ID-02

### TC-FR14-025: DELETE — Non-existent category ID
- **Dimension:** Domain Partition / Boundary
- **Endpoint:** `DELETE /api/categories/99999`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Expected HTTP Status (ideal):** 404 Not Found
- **SUT Predicted Behavior:** ⚠️ 200 OK — no existence check (BUG-FR14-CAND-04)
- **Partition Coverage:** EP-ID-02

### TC-FR14-026: PUT — Zero as category ID
- **Dimension:** Boundary
- **Endpoint:** `PUT /api/categories/0`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Zero ID" }`
- **Expected HTTP Status (ideal):** 404 Not Found (or 400)
- **SUT Predicted Behavior:** 200 OK (no validation)
- **Partition Coverage:** EP-ID-03

### TC-FR14-027: DELETE — Negative category ID
- **Dimension:** Boundary
- **Endpoint:** `DELETE /api/categories/-1`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Expected HTTP Status (ideal):** 404 Not Found (or 400)
- **SUT Predicted Behavior:** 200 OK (no validation)
- **Partition Coverage:** EP-ID-04

### TC-FR14-028: PUT — Non-numeric string as ID
- **Dimension:** Type Safety
- **Endpoint:** `PUT /api/categories/abc`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "String ID" }`
- **Expected HTTP Status (ideal):** 400 Bad Request
- **SUT Predicted Behavior:** 200 OK (SQLite converts "abc" gracefully)
- **Partition Coverage:** EP-ID-05

---

## Interaction 6: Security Probes (6 cases)

### TC-FR14-029: POST — SQL injection in name field
- **Dimension:** Security / SEC-03
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "'; DROP TABLE categories;--" }`
- **Expected HTTP Status:** 200 OK (parameterized query should prevent injection)
- **Oracle:** Categories table still exists. Subsequent GET returns normal list. The injected string is stored literally as the name.
- **Partition Coverage:** EP-NM-09

### TC-FR14-030: POST — XSS payload in name field
- **Dimension:** Security / SEC-03
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "<script>alert('XSS')</script>" }`
- **Expected HTTP Status:** 200 OK
- **Oracle:** Name stored literally (potential stored XSS if rendered in frontend without sanitization). GET returns the raw string.
- **Partition Coverage:** EP-NM-10

### TC-FR14-031: POST — Mass assignment: inject extra fields
- **Dimension:** Security / SEC-07
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Mass Assign Test", "id": 999, "admin": true, "role": "superuser" }`
- **Expected HTTP Status:** 200 OK
- **Oracle:** Extra fields are ignored. Created category has auto-incremented ID (not 999).
- **Partition Coverage:** EP-NM-01 + SEC-07

### TC-FR14-032: PUT — Mass assignment: override ID in body
- **Dimension:** Security / SEC-07
- **Endpoint:** `PUT /api/categories/1`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Updated", "id": 999 }`
- **Expected HTTP Status:** 200 OK
- **Oracle:** Category ID remains 1, not changed to 999.
- **Partition Coverage:** SEC-07

### TC-FR14-033: POST — NoSQL injection probe in name
- **Dimension:** Security / SEC-03
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": {"$gt": ""} }`
- **Expected HTTP Status (ideal):** 400 Bad Request (type mismatch)
- **SUT Predicted Behavior:** 200 or 500 (SQLite may error on object)
- **Partition Coverage:** SEC-03

### TC-FR14-034: DELETE — IDOR: delete seeded category as regular user
- **Dimension:** Security / SEC-04
- **Endpoint:** `DELETE /api/categories/1`
- **Precondition:** Authenticated as regular user
- **Headers:** `Authorization: Bearer {{userToken}}`, `X-Student-Id: 23127259`
- **Expected HTTP Status (per SRS):** 403 Forbidden
- **SUT Predicted Behavior:** ⚠️ 200 OK — no role check (confirms BUG-FR14-CAND-01)
- **Partition Coverage:** SEC-04 + SEC-02

---

## Interaction 7: State Transitions & Referential Integrity (4 cases)

### TC-FR14-035: Full CRUD lifecycle: Create → Read → Update → Read → Delete → Read
- **Dimension:** State Transition / End-to-End
- **Endpoint:** Multiple (POST → GET → PUT → GET → DELETE → GET)
- **Precondition:** Admin authenticated
- **Steps:**
  1. POST create "Lifecycle Test" → capture `id`
  2. GET list → verify present
  3. PUT update to "Lifecycle Updated" → verify 200
  4. GET list → verify updated name
  5. DELETE → verify 200
  6. GET list → verify absent
- **Oracle:** Each step's state change is verified by subsequent GET.
- **Partition Coverage:** Full state transition coverage

### TC-FR14-036: DELETE category with associated products (orphan test)
- **Dimension:** State Transition / Referential Integrity
- **Endpoint:** `DELETE /api/categories/1` (seeded category "Điện thoại" with products referencing it)
- **Precondition:** Admin authenticated. Products with `category_id = 1` exist.
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Expected HTTP Status (ideal):** 409 Conflict (or block with referential integrity error)
- **SUT Predicted Behavior:** ⚠️ 200 OK — orphans products (BUG-FR14-CAND-05)
- **Oracle:** After DELETE, GET `/api/products` shows products with `category_id = 1` but category no longer exists.
- **Partition Coverage:** Referential integrity

### TC-FR14-037: PUT update on recently deleted category
- **Dimension:** State Transition / Invalid Sequence
- **Endpoint:** `PUT /api/categories/{{deletedCategoryId}}`
- **Precondition:** Category was created and then deleted
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Zombie Category" }`
- **Expected HTTP Status (ideal):** 404 Not Found
- **SUT Predicted Behavior:** 200 OK (no existence check)
- **Partition Coverage:** Invalid state transition

### TC-FR14-038: Double DELETE on same category
- **Dimension:** State Transition / Idempotency
- **Endpoint:** `DELETE /api/categories/{{deletedCategoryId}}`
- **Precondition:** Category was already deleted
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Expected HTTP Status (ideal):** 404 Not Found (already deleted)
- **SUT Predicted Behavior:** 200 OK (no existence check)
- **Partition Coverage:** Idempotency / Double-delete

---

## Interaction 8: Schema Validation (4 cases)

### TC-FR14-039: GET — Verify response schema structure
- **Dimension:** Schema Validation
- **Endpoint:** `GET /api/categories`
- **Headers:** `X-Student-Id: 23127259`
- **Expected HTTP Status:** 200
- **Schema Assertions:**
  - Response is a JSON array
  - Each element is an object with exactly `id` (integer) and `name` (string or null)
  - `Content-Type` header includes `application/json`
- **Partition Coverage:** Response schema

### TC-FR14-040: POST — Verify create response schema
- **Dimension:** Schema Validation
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Schema Test" }`
- **Expected HTTP Status:** 200
- **Schema Assertions:**
  - Response is JSON object with `message` (string) and `id` (positive integer)
  - `message` equals "Category created"
- **Partition Coverage:** Create response schema

### TC-FR14-041: PUT — Verify update response schema
- **Dimension:** Schema Validation
- **Endpoint:** `PUT /api/categories/{{schemaCategoryId}}`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "Schema Updated" }`
- **Expected HTTP Status:** 200
- **Schema Assertions:**
  - Response is JSON object with `message` (string)
  - `message` equals "Category updated"
- **Partition Coverage:** Update response schema

### TC-FR14-042: DELETE — Verify delete response schema
- **Dimension:** Schema Validation
- **Endpoint:** `DELETE /api/categories/{{schemaCategoryId}}`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Expected HTTP Status:** 200
- **Schema Assertions:**
  - Response is JSON object with `message` (string)
  - `message` equals "Category deleted"
- **Partition Coverage:** Delete response schema

---

## Generation Summary

| Dimension | Case IDs | Count |
|---|---|:---:|
| Happy-path CRUD | TC-FR14-001 to 006 | 6 |
| Authentication (SEC-01) | TC-FR14-007 to 011 | 5 |
| Authorization/RBAC (SEC-02) | TC-FR14-012 to 015 | 4 |
| Input Validation (name) | TC-FR14-016 to 023 | 8 |
| Input Validation (id) | TC-FR14-024 to 028 | 5 |
| Security Probes (SEC-03/04/07) | TC-FR14-029 to 034 | 6 |
| State Transitions | TC-FR14-035 to 038 | 4 |
| Schema Validation | TC-FR14-039 to 042 | 4 |
| **Total** | | **42** |
