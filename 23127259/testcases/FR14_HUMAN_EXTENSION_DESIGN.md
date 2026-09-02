# FR-14 Human Extension — Gap Analysis & Additional Test Cases

**Feature:** FR-14 – Category Management CRUD  
**Student:** Nguyễn Tấn Thắng (23127259)  
**Extension Date:** September 2, 2026  
**Input:** `FR14_HUMAN_AUDIT_CORRECTIONS.md` (Gap Analysis Section)

---

## Gap Analysis Summary

The AI-generated suite covered the primary dimensions well but missed these edge cases:

| Gap ID | Description | Dimension | Missed By AI |
|---|---|---|---|
| GAP-01 | Wrong/missing Content-Type header on POST/PUT | Input Validation | Not tested |
| GAP-02 | Empty request body (not JSON, raw empty) | Input Validation | Not tested |
| GAP-03 | HTTP method override / unsupported methods | Protocol Boundary | Not tested |
| GAP-04 | Response Content-Type header validation | Schema Validation | Not tested |
| GAP-05 | GET categories after SUT database reset (clean state) | State Transition | Not tested |
| GAP-06 | Multiple rapid category creations (batch stress) | Boundary | Not tested |
| GAP-07 | PUT update with empty body | Input Validation | Not tested |

---

## Human-Designed Test Cases (7 additional)

### TC-FR14-H01: POST — Missing Content-Type header
- **Dimension:** Input Validation / Protocol
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259` (**NO Content-Type header**)
- **Request Body (raw text):** `{ "name": "No Content Type" }`
- **Expected HTTP Status:** 400 or 415 (Unsupported Media Type)
- **SUT Predicted Behavior:** Express `bodyParser.json()` may reject or return empty `req.body`. Category may not be created (name would be undefined).
- **Oracle:** If 200, check whether name is null/undefined. If error, verify error message.
- **Rationale:** Tests Express middleware behavior when Content-Type is missing.

### TC-FR14-H02: POST — Request body is completely empty (not even `{}`)
- **Dimension:** Input Validation / Robustness
- **Endpoint:** `POST /api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** *(empty — no body at all)*
- **Expected HTTP Status:** 400 (malformed JSON)
- **SUT Predicted Behavior:** Express `bodyParser.json()` may parse empty as `{}`, resulting in `name = undefined`.
- **Oracle:** If 200 returned, category with null name is created (bug). If 400, properly rejected.
- **Rationale:** Tests zero-payload robustness.

### TC-FR14-H03: PATCH — Unsupported HTTP method on categories endpoint
- **Dimension:** Protocol Boundary / Method Safety
- **Endpoint:** `PATCH /api/categories/1`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{ "name": "PATCH attempt" }`
- **Expected HTTP Status:** 404 or 405 Method Not Allowed
- **SUT Predicted Behavior:** Express returns 404 (no PATCH route defined)
- **Oracle:** Category name for ID 1 should NOT change.
- **Rationale:** Verifies that only defined HTTP methods are accepted.

### TC-FR14-H04: GET — Verify response Content-Type and Cache headers
- **Dimension:** Schema Validation / Response Headers
- **Endpoint:** `GET /api/categories`
- **Headers:** `X-Student-Id: 23127259`
- **Expected HTTP Status:** 200
- **Response Header Assertions:**
  - `Content-Type` includes `application/json`
  - Response should be well-formed JSON parseable by `JSON.parse()`
- **Oracle:** Headers conform to REST API best practices.
- **Rationale:** Extends schema validation to response headers, not just body.

### TC-FR14-H05: PUT — Update with completely empty JSON body
- **Dimension:** Input Validation / Edge Case
- **Endpoint:** `PUT /api/categories/1`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Body:** `{}`
- **Expected HTTP Status (ideal):** 400 Bad Request
- **SUT Predicted Behavior:** 200 OK — sets `name = undefined` (which SQLite stores as NULL)
- **Oracle:** If 200, verify category name is now null via GET. This is a data corruption bug.
- **Rationale:** Tests missing mandatory field in update.

### TC-FR14-H06: POST — Rapid sequential creation (5 categories)
- **Dimension:** Boundary / Stress
- **Endpoint:** `POST /api/categories` (5 sequential calls)
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`, `Content-Type: application/json`
- **Request Bodies:** 
  1. `{ "name": "Batch 1" }`
  2. `{ "name": "Batch 2" }`
  3. `{ "name": "Batch 3" }`
  4. `{ "name": "Batch 4" }`
  5. `{ "name": "Batch 5" }`
- **Expected HTTP Status:** All 200
- **Oracle:** Each returns unique auto-incremented ID. GET list shows all 5 new categories.
- **Rationale:** Tests that auto-increment works correctly under sequential rapid creation.

### TC-FR14-H07: DELETE — Attempt to delete seeded category ID=1 and verify product orphaning
- **Dimension:** Referential Integrity / Data Integrity
- **Endpoint Sequence:**
  1. `GET /api/products` → filter products with `category_id = 1` → count them
  2. `DELETE /api/categories/1`
  3. `GET /api/products` → verify products with `category_id = 1` still exist (orphaned)
  4. `GET /api/categories` → verify category ID 1 is gone
- **Expected Behavior:** Products are orphaned — their `category_id` still references non-existent category.
- **Oracle:** Product count unchanged, category count decremented by 1.
- **Rationale:** Directly confirms BUG-FR14-CAND-05 (no referential integrity) with full evidence chain.

---

## Extension Summary

| Case ID | Dimension | Gap Covered |
|---|---|---|
| TC-FR14-H01 | Input Validation / Protocol | GAP-01 |
| TC-FR14-H02 | Input Validation / Robustness | GAP-02 |
| TC-FR14-H03 | Protocol Boundary | GAP-03 |
| TC-FR14-H04 | Schema / Response Headers | GAP-04 |
| TC-FR14-H05 | Input Validation / Edge Case | GAP-07 |
| TC-FR14-H06 | Boundary / Stress | GAP-06 |
| TC-FR14-H07 | Referential Integrity | GAP-05 variant |

**Total Human Extension Cases:** 7 (exceeds minimum of 5)  
**Grand Total (AI + Human):** 42 + 7 = **49 test cases**
