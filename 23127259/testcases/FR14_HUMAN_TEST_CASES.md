# FR-14 Human-Designed Extension Test Cases Specification

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-14 – Category Management CRUD (Pool C – Web Admin)
- **Suite Type:** Human Extension Test Suite ($\ge 5$ cases, actual: `7` cases)
- **Total Cases:** `7` (`TC-FR14-H01` .. `TC-FR14-H07`)
- **Provenance:** Student-selected and finalized Human Extension cases addressing gaps identified in `FR14_HUMAN_AUDIT_CORRECTIONS.md` and `FR14_HUMAN_EXTENSION_DESIGN.md`.

---

### TC-FR14-H01
- **Test Case ID:** `TC-FR14-H01`
- **Human Selection Source:** Gap `GAP-01` (Missing / Unsupported Content-Type Header on POST Mutation)
- **Title:** Protocol Robustness: POST Category Request Omitting `Content-Type: application/json` Header
- **Technique:** Protocol Boundary Testing / MIME Type Handling / Body Parser Robustness
- **Requirement / Gap:** REST API Standards, Express `bodyParser.json()` behavior, Gap `GAP-01`
- **Oracle Classification:** `PROTOCOL-ROBUSTNESS / SPEC-IMPLIED`
- **Why AI Coverage Missed This:** AI assumed all clients send valid headers; did not test body-parser behavior when `Content-Type` is omitted.
- **Why Distinct From Existing AI Cases:** Tests protocol layer behavior rather than payload data values.
- **Preconditions:** SUT running, Admin authenticated.
- **Actor:** System Administrator (`role = 'admin'`)
- **Authentication Context:** `Authorization: Bearer {{adminToken}}`
- **Request Method:** `POST`
- **Endpoint:** `/api/categories`
- **Headers:** `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259` (**NO `Content-Type` header**)
- **Request Body (raw string):** `{"name": "No Content Type"}`
- **Expected HTTP Status:** `400 Bad Request` or `415 Unsupported Media Type` (or non-creation)
- **Expected Semantic Result:** Server either rejects missing media type or fails to parse body, preventing creation of an undefined/corrupt category.
- **SUT Observed Behavior:** `req.body` is undefined without header; SUT attempts `INSERT INTO categories (name) VALUES (undefined)` which SQLite stores as NULL.

---

### TC-FR14-H02
- **Test Case ID:** `TC-FR14-H02`
- **Human Selection Source:** Gap `GAP-02` (Zero-Byte Request Body Robustness)
- **Title:** Zero-Payload Robustness: POST Category Request with Completely Empty Body
- **Technique:** Payload Boundary Testing / Zero-Byte Stream Handling
- **Requirement / Gap:** Input Validation, Schema Conformance, Gap `GAP-02`
- **Oracle Classification:** `INPUT-VALIDATION / ROBUSTNESS`
- **Why AI Coverage Missed This:** AI generated cases with `{}` (empty JSON object), but never tested an actual zero-byte empty body stream.
- **Why Distinct From Existing AI Cases:** Distinguishes between empty JSON `{}` and zero payload stream.
- **Preconditions:** SUT running, Admin authenticated.
- **Actor:** System Administrator
- **Authentication Context:** `Authorization: Bearer {{adminToken}}`
- **Request Method:** `POST`
- **Endpoint:** `/api/categories`
- **Headers:** `Content-Type: application/json`, `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Request Body:** *(Empty / 0 bytes)*
- **Expected HTTP Status:** `400 Bad Request`
- **Expected Semantic Result:** Server rejects empty stream as malformed JSON.

---

### TC-FR14-H03
- **Test Case ID:** `TC-FR14-H03`
- **Human Selection Source:** Gap `GAP-03` (Unsupported HTTP Method Handling)
- **Title:** Protocol Boundary: Attempting PATCH Method on Existing Category Route
- **Technique:** HTTP Verb Tampering / Route Exhaustion Testing
- **Requirement / Gap:** RFC 9110 HTTP Semantics, Route Whitelisting, Gap `GAP-03`
- **Oracle Classification:** `PROTOCOL-BOUNDARY / VERB-TAMPERING`
- **Why AI Coverage Missed This:** AI focused strictly on the documented verbs (GET, POST, PUT, DELETE) and neglected unsupported HTTP method probes.
- **Why Distinct From Existing AI Cases:** Probes router method-matching and 404/405 error handling.
- **Preconditions:** SUT running, Category ID 2 exists.
- **Actor:** System Administrator
- **Authentication Context:** `Authorization: Bearer {{adminToken}}`
- **Request Method:** `PATCH`
- **Endpoint:** `/api/categories/2`
- **Headers:** `Content-Type: application/json`, `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Request Body:** `{"name": "PATCH attempt"}`
- **Expected HTTP Status:** `404 Not Found` or `405 Method Not Allowed`
- **Expected Semantic Result:** PATCH request is rejected without modifying category ID 2.
- **SUT Observed Behavior:** Express returns `404 Cannot PATCH /api/categories/2`. Category name remains intact.

---

### TC-FR14-H04
- **Test Case ID:** `TC-FR14-H04`
- **Human Selection Source:** Gap `GAP-04` (Response Header & Content-Type Rigor)
- **Title:** Contract Conformance: Verification of Response Content-Type and Header Conformance on Category List
- **Technique:** Response Header Inspection / Protocol Conformance
- **Requirement / Gap:** `api_specification.md`, REST Conformance, Gap `GAP-04`
- **Oracle Classification:** `SCHEMA-VALIDATION / HEADER-CONFORMANCE`
- **Why AI Coverage Missed This:** AI asserted only on JSON body attributes; missed asserting HTTP response headers.
- **Why Distinct From Existing AI Cases:** Asserts transport-level HTTP headers (`Content-Type: application/json; charset=utf-8`).
- **Preconditions:** SUT running.
- **Actor:** Public Caller
- **Request Method:** `GET`
- **Endpoint:** `/api/categories`
- **Headers:** `X-Student-Id: 23127259`
- **Expected HTTP Status:** `200 OK`
- **Expected Response Headers:** `Content-Type` header includes `application/json`.
- **Expected Semantic Result:** Response is strictly formatted as parseable JSON with compliant media-type header.

---

### TC-FR14-H05
- **Test Case ID:** `TC-FR14-H05`
- **Human Selection Source:** Gap `GAP-07` (Data Corruption via Empty Body PUT)
- **Title:** Silent Data Corruption Probe: PUT Category with Empty Body `{}` Erasing Existing Name
- **Technique:** Boundary Mutation Testing / Field Erasure Detection / Partial Update Tampering
- **Requirement / Gap:** SRS FR-14 Update Invariants, Data Integrity, Gap `GAP-07`
- **Oracle Classification:** `DATA-INTEGRITY / SILENT-CORRUPTION`
- **Why AI Coverage Missed This:** AI tested empty body on POST, but not on PUT where existing data can be silently overwritten with null.
- **Why Distinct From Existing AI Cases:** Targets field nullification/corruption on an already established entity.
- **Preconditions:** SUT running, Category ID 2 ("Laptop") exists.
- **Actor:** System Administrator
- **Authentication Context:** `Authorization: Bearer {{adminToken}}`
- **Request Method:** `PUT`
- **Endpoint:** `/api/categories/2`
- **Headers:** `Content-Type: application/json`, `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Request Body:** `{}`
- **Expected HTTP Status:** `400 Bad Request`
- **Expected Semantic Result:** Request rejected because `name` is required for category update; existing category name is preserved.
- **SUT Observed Behavior:** ⚠️ **BUG CONFIRMED:** SUT returns `200 OK` and executes `UPDATE categories SET name = undefined WHERE id = 2`, corrupting the category name to NULL in SQLite.

---

### TC-FR14-H06
- **Test Case ID:** `TC-FR14-H06`
- **Human Selection Source:** Gap `GAP-06` (Sequential Rapid-Fire Batch Allocation)
- **Title:** Concurrency & Auto-Increment Integrity: Rapid Sequential Creation of Categories
- **Technique:** Stress Testing / Monotonic ID Ordering / Batch Mutation
- **Requirement / Gap:** Database Auto-Increment Rules, SQLite Sequence Integrity, Gap `GAP-06`
- **Oracle Classification:** `DATABASE-INTEGRITY / STRESS`
- **Why AI Coverage Missed This:** AI tested only single-entity atomic creation; did not verify rapid sequence allocation.
- **Why Distinct From Existing AI Cases:** Executes 3 chained sequential POST requests ("Batch 1", "Batch 2", "Batch 3") and verifies distinct monotonically increasing IDs.
- **Preconditions:** SUT running, Admin authenticated.
- **Actor:** System Administrator
- **Authentication Context:** `Authorization: Bearer {{adminToken}}`
- **Request Method:** 3 sequential `POST` requests
- **Endpoint:** `/api/categories`
- **Headers:** `Content-Type: application/json`, `Authorization: Bearer {{adminToken}}`, `X-Student-Id: 23127259`
- **Request Bodies:** `{"name": "Batch 1"}`, `{"name": "Batch 2"}`, `{"name": "Batch 3"}`
- **Expected HTTP Status:** All three return `200 OK`
- **Expected Semantic Result:** Three distinct categories created with strictly incrementing IDs (`id3 > id2 > id1`).
- **SUT Observed Behavior:** Passed cleanly; SQLite auto-increment handles sequential insertions correctly.

---

### TC-FR14-H07
- **Test Case ID:** `TC-FR14-H07`
- **Human Selection Source:** Gap `GAP-05` (Foreign Key Orphan Verification After Category Deletion)
- **Title:** Referential Integrity Defect Proof: Deleting Seeded Category Leaves Products in Orphaned Foreign Key State
- **Technique:** Relational Integrity Testing / Orphaned Entity Detection / Cross-Resource Invariant Verification
- **Requirement / Gap:** Relational Database Integrity, Product-Category Taxonomy Invariants, Gap `GAP-05`
- **Oracle Classification:** `RELATIONAL-INTEGRITY / DEFECT-CONFIRMATION`
- **Why AI Coverage Missed This:** AI case `TC-FR14-036` checked only the DELETE category HTTP response; did not query `/api/products` to prove that products were actually orphaned in the database.
- **Why Distinct From Existing AI Cases:** Follows up with a `GET /api/products` call and programmatically verifies that products referencing `category_id = 1` still exist, proving foreign key orphaning without cascade or restriction.
- **Preconditions:** SUT running, Category ID 1 was deleted in TC-FR14-036.
- **Actor:** Client Caller
- **Request Method:** `GET`
- **Endpoint:** `/api/products`
- **Headers:** `X-Student-Id: 23127259`
- **Expected Semantic Result:** Either products should have been restricted from deletion, or foreign keys cascaded. In SUT, products with `category_id = 1` persist with no corresponding category parent.
- **SUT Observed Behavior:** ⚠️ **DEFECT CONFIRMED:** Product "iPhone 15 Pro Max" still retains `category_id: 1` despite Category 1 having been deleted, leaving it orphaned.
