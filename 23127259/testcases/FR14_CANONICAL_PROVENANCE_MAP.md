# FR-14 Canonical Test Provenance Map

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-14 – Category Management CRUD (Pool C – Web Admin)
- **Authoritative Provenance Sources:**
  - **Level 1 (Normative Requirements):** `docs/assignment-notes.md`, `testcases/FR14_REQUIREMENT_ANALYSIS.md`, `docs/ORACLE_POLICY.md`
  - **Level 2 (Immutable AI Generation):** `testcases/FR14_AI_DRAFT.md`
  - **Level 3 (Human Audit Provenance):** `testcases/FR14_HUMAN_AUDIT_CORRECTIONS.md`, `ai/TC_AUDIT_FR14.md`
  - **Level 4 (Human Extensions):** `testcases/FR14_HUMAN_TEST_CASES.md`, `testcases/FR14_HUMAN_EXTENSION_DESIGN.md`

---

## 1. Source Hierarchy & Precedence Rules

1. **Level 1 (Normative Product Sources):** SRS, API Specification, and Assignment Rules define system boundaries and expected behaviors.
2. **Level 2 (Raw AI Provenance):** `FR14_AI_DRAFT.md` is the immutable record of raw AI generation.
3. **Level 3 (Human Audit Decisions):** `FR14_HUMAN_AUDIT_CORRECTIONS.md` records audit decisions (`VALID`, `INCOMPLETE`, `INVALID`). Only documented corrections adjust expectations.
4. **Level 4 (Human Extensions):** `FR14_HUMAN_TEST_CASES.md` defines `TC-FR14-H01` through `TC-FR14-H07`.
5. **Derived Files Rule:** Postman collections and execution scripts strictly conform to Levels 1–4.

---

## 2. Canonical AI Case Mapping (TC-FR14-001 through TC-FR14-042)

| Canonical ID | Title / Technique | Actor | Method | Target Route | Body / Parameter | Expected Semantic Outcome | Expected HTTP Status | Audit Disposition |
|---|---|---|:---:|---|---|---|---|:---:|
| `TC-FR14-001` | Public Category Catalog Reading | Unauthenticated Client | `GET` | `/api/categories` | None | Returns JSON array of category entities ($\ge 3$) | `200 OK` | **VALID AS-IS** |
| `TC-FR14-002` | Valid Admin Category Creation | System Administrator | `POST` | `/api/categories` | `{"name": "Tablet"}` | Category created with auto-increment ID | `200 OK` | **VALID AS-IS** |
| `TC-FR14-003` | Read-After-Write Verification (Create) | Client Caller | `GET` | `/api/categories` | None | New category present in returned array | `200 OK` | **VALID AS-IS** |
| `TC-FR14-004` | Valid Admin Category Name Update | System Administrator | `PUT` | `/api/categories/:id` | `{"name": "Tablets & iPads"}` | Existing category name updated | `200 OK` | **VALID AS-IS** |
| `TC-FR14-005` | Read-After-Write Verification (Update) | Client Caller | `GET` | `/api/categories` | None | Updated category name reflects in listing | `200 OK` | **VALID AS-IS** |
| `TC-FR14-006` | Valid Admin Category Deletion | System Administrator | `DELETE` | `/api/categories/:id` | None | Category removed from catalog | `200 OK` | **VALID AS-IS** |
| `TC-FR14-007` | SEC-01: Anonymous Create Rejection | Unauthenticated Client | `POST` | `/api/categories` | `{"name": "Unauthorized"}` | Request rejected; auth required | `401 Unauthorized` | **VALID AS-IS** |
| `TC-FR14-008` | SEC-01: Anonymous Update Rejection | Unauthenticated Client | `PUT` | `/api/categories/1` | `{"name": "Hacked"}` | Request rejected; auth required | `401 Unauthorized` | **VALID AS-IS** |
| `TC-FR14-009` | SEC-01: Anonymous Delete Rejection | Unauthenticated Client | `DELETE` | `/api/categories/1` | None | Request rejected; auth required | `401 Unauthorized` | **VALID AS-IS** |
| `TC-FR14-010` | SEC-01: Malformed Token Rejection | Malformed Token Client | `POST` | `/api/categories` | `{"name": "Malformed"}` | Request rejected; invalid token | `403 Forbidden` | **VALID AS-IS** |
| `TC-FR14-011` | SEC-01: Cryptographically Tampered Token | Attacker / Forged Signature | `DELETE` | `/api/categories/1` | None | Request rejected; bad signature | `403 Forbidden` | **CORRECTED DERIVATIVE** |
| `TC-FR14-012` | SEC-02: Regular User Create Rejection | Regular Customer (`role=user`) | `POST` | `/api/categories` | `{"name": "User Created"}` | Request rejected; admin role required | `403 Forbidden` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-013` | SEC-02: Regular User Update Rejection | Regular Customer (`role=user`) | `PUT` | `/api/categories/2` | `{"name": "User Updated"}` | Request rejected; admin role required | `403 Forbidden` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-014` | SEC-02: Regular User Delete Rejection | Regular Customer (`role=user`) | `DELETE` | `/api/categories/:id` | None | Request rejected; admin role required | `403 Forbidden` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-015` | Read Permission Boundary: Customer List | Regular Customer (`role=user`) | `GET` | `/api/categories` | None | Category list returned cleanly | `200 OK` | **VALID AS-IS** |
| `TC-FR14-016` | Input Validation: Empty String Name | System Administrator | `POST` | `/api/categories` | `{"name": ""}` | Request rejected; non-empty name required | `400 Bad Request` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-017` | Input Validation: Null Name Value | System Administrator | `POST` | `/api/categories` | `{"name": null}` | Request rejected; valid name required | `400 Bad Request` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-018` | Input Validation: Missing Name Key | System Administrator | `POST` | `/api/categories` | `{}` | Request rejected; mandatory name missing | `400 Bad Request` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-019` | Input Validation: Whitespace-Only Name | System Administrator | `POST` | `/api/categories` | `{"name": "   "}` | Request rejected; non-whitespace required | `400 Bad Request` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-020` | Boundary: Extremely Long Name (1001 chars) | System Administrator | `POST` | `/api/categories` | `{"name": "<1001 chars>"}` | Handled safely (created or rejected) | `200 / 400` | **CORRECTED DERIVATIVE** |
| `TC-FR14-021` | I18N: Unicode and Emoji Characters | System Administrator | `POST` | `/api/categories` | `{"name": "Điện tử 📱"}` | Created cleanly with Unicode preserved | `200 OK` | **VALID AS-IS** |
| `TC-FR14-022` | Business Logic: Duplicate Name Rejection | System Administrator | `POST` | `/api/categories` | `{"name": "Laptop"}` | Rejected or duplicate noted | `409 Conflict` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-023` | Type Safety: Integer Value Coercion | System Administrator | `POST` | `/api/categories` | `{"name": 12345}` | Coerced to string or rejected | `200 / 400` | **VALID AS-IS** |
| `TC-FR14-024` | Boundary: Non-Existent ID Update | System Administrator | `PUT` | `/api/categories/99999` | `{"name": "Ghost"}` | Request rejected; entity not found | `404 Not Found` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-025` | Boundary: Non-Existent ID Deletion | System Administrator | `DELETE` | `/api/categories/99999` | None | Request rejected; entity not found | `404 Not Found` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-026` | Boundary: Zero ID Mutation | System Administrator | `PUT` | `/api/categories/0` | `{"name": "Zero"}` | Handled safely without crash | `200 / 400 / 404` | **VALID AS-IS** |
| `TC-FR14-027` | Boundary: Negative ID Mutation | System Administrator | `DELETE` | `/api/categories/-1` | None | Handled safely without crash | `200 / 400 / 404` | **VALID AS-IS** |
| `TC-FR14-028` | Type Safety: Non-Numeric ID String | System Administrator | `PUT` | `/api/categories/abc` | `{"name": "String"}` | Handled safely without crash | `200 / 400 / 404` | **VALID AS-IS** |
| `TC-FR14-029` | SEC-03: SQL Injection Payload in Name | Attacker / Security Tester | `POST` | `/api/categories` | `{"name": "'; DROP..."}` | Parameterized; table preserved | `200 / Non-500` | **VALID AS-IS** |
| `TC-FR14-029b` | SEC-03: Post-SQLi Table Verification | Client Caller | `GET` | `/api/categories` | None | Categories table intact and accessible | `200 OK` | **VALID AS-IS** |
| `TC-FR14-030` | SEC-03: Stored XSS Script Payload | Attacker / Security Tester | `POST` | `/api/categories` | `{"name": "<script>..."}` | Stored verbatim; sanitization noted | `200 OK` | **VALID AS-IS** |
| `TC-FR14-031` | SEC-07: Mass Assignment Extra Body Keys | Attacker / Security Tester | `POST` | `/api/categories` | `{"name": "X", "id": 999}` | Extra fields discarded; auto ID used | `200 OK` | **VALID AS-IS** |
| `TC-FR14-032` | SEC-07: Mass Assignment ID Path Override | Attacker / Security Tester | `PUT` | `/api/categories/2` | `{"name": "X", "id": 999}` | Path ID enforced; body ID ignored | `200 OK` | **VALID AS-IS** |
| `TC-FR14-033` | SEC-03: Object Payload Type Tampering | Attacker / Security Tester | `POST` | `/api/categories` | `{"name": {"$gt": ""}}` | Handled gracefully without crash | `200 / 400 / 500` | **CORRECTED DERIVATIVE** |
| `TC-FR14-034` | SEC-04: IDOR Deletion as Regular User | Regular Customer (`role=user`) | `DELETE` | `/api/categories/3` | None | Request rejected; unauthorized IDOR | `403 Forbidden` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-035a` | Lifecycle Continuity: Entity Creation | System Administrator | `POST` | `/api/categories` | `{"name": "Lifecycle"}` | Entity created | `200 OK` | **VALID AS-IS** |
| `TC-FR14-035b` | Lifecycle Continuity: Read After Create | Client Caller | `GET` | `/api/categories` | None | Created entity found | `200 OK` | **VALID AS-IS** |
| `TC-FR14-035c` | Lifecycle Continuity: Entity Update | System Administrator | `PUT` | `/api/categories/:id` | `{"name": "Updated"}` | Entity updated | `200 OK` | **VALID AS-IS** |
| `TC-FR14-035d` | Lifecycle Continuity: Entity Delete | System Administrator | `DELETE` | `/api/categories/:id` | None | Entity deleted | `200 OK` | **VALID AS-IS** |
| `TC-FR14-035e` | Lifecycle Continuity: Read After Delete | Client Caller | `GET` | `/api/categories` | None | Deleted entity absent | `200 OK` | **VALID AS-IS** |
| `TC-FR14-036` | Referential Integrity: Delete Parent Category | System Administrator | `DELETE` | `/api/categories/1` | None | Should restrict or cascade | `409 / 200` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-037` | Invalid Sequence: Update Deleted Category | System Administrator | `PUT` | `/api/categories/:id` | `{"name": "Zombie"}` | Request rejected; entity not found | `404 Not Found` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-038` | Idempotency: Double Delete on Same Entity | System Administrator | `DELETE` | `/api/categories/:id` | None | Second delete returns 404 | `404 Not Found` | **VALID AS-IS (DEFECT)** |
| `TC-FR14-039` | Schema Conformance: Category Array Response | Client Caller | `GET` | `/api/categories` | None | Valid JSON array of `{id, name}` | `200 OK` | **VALID AS-IS** |
| `TC-FR14-040` | Schema Conformance: Create Response Object | System Administrator | `POST` | `/api/categories` | `{"name": "Schema"}` | `{message: string, id: int}` | `200 OK` | **VALID AS-IS** |
| `TC-FR14-041` | Schema Conformance: Update Response Object | System Administrator | `PUT` | `/api/categories/:id` | `{"name": "Schema U"}` | `{message: string}` | `200 OK` | **VALID AS-IS** |
| `TC-FR14-042` | Schema Conformance: Delete Response Object | System Administrator | `DELETE` | `/api/categories/:id` | None | `{message: string}` | `200 OK` | **VALID AS-IS** |

---

## 3. Canonical Human Extension Mapping (TC-FR14-H01 through TC-FR14-H07)

| Canonical ID | Title / Technique | Actor | Method | Target Route | Body / Parameter | Expected Semantic Outcome | Expected HTTP Status | Audit Disposition |
|---|---|---|:---:|---|---|---|---|:---:|
| `TC-FR14-H01` | Protocol: Missing Content-Type Header | System Administrator | `POST` | `/api/categories` | Raw text stream | Request rejected or handled safely | `400 / 415` | **STUDENT EXTENSION** |
| `TC-FR14-H02` | Robustness: Zero-Byte Request Body | System Administrator | `POST` | `/api/categories` | *(0 bytes)* | Request rejected; invalid JSON | `400 Bad Request` | **STUDENT EXTENSION** |
| `TC-FR14-H03` | Protocol: Unsupported PATCH Method Probe | System Administrator | `PATCH` | `/api/categories/2` | `{"name": "PATCH"}` | Route rejected; method not allowed | `404 / 405` | **STUDENT EXTENSION** |
| `TC-FR14-H04` | Header Conformance: Response Content-Type | Client Caller | `GET` | `/api/categories` | None | Headers include `application/json` | `200 OK` | **STUDENT EXTENSION** |
| `TC-FR14-H05` | Silent Corruption: Empty Body `{}` PUT | System Administrator | `PUT` | `/api/categories/2` | `{}` | Rejected; name preserved | `400 Bad Request` | **STUDENT EXTENSION (DEFECT)** |
| `TC-FR14-H06a` | Stress: Rapid Batch Allocation 1 | System Administrator | `POST` | `/api/categories` | `{"name": "Batch 1"}` | Category 1 created with auto ID | `200 OK` | **STUDENT EXTENSION** |
| `TC-FR14-H06b` | Stress: Rapid Batch Allocation 2 | System Administrator | `POST` | `/api/categories` | `{"name": "Batch 2"}` | Category 2 created with auto ID | `200 OK` | **STUDENT EXTENSION** |
| `TC-FR14-H06c` | Stress: Rapid Batch Allocation 3 | System Administrator | `POST` | `/api/categories` | `{"name": "Batch 3"}` | Category 3 created with auto ID | `200 OK` | **STUDENT EXTENSION** |
| `TC-FR14-H07` | Defect Proof: Foreign Key Orphan Verification | Client Caller | `GET` | `/api/products` | None | Products with `category_id=1` exist orphaned | `200 OK` | **STUDENT EXTENSION (DEFECT)** |
