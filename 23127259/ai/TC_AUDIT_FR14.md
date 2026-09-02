# Human Test-Case Audit Matrix – FR-14 (Category Management CRUD)

- **Student:** Nguyễn Tấn Thắng (`23127259`)
- **Feature:** FR-14 – Category Management (CRUD) (Pool C – Web Admin)
- **Raw AI-Generated Cases:** `42` (`TC-FR14-001` .. `TC-FR14-042` from `FR14_AI_DRAFT.md`)
- **Frozen Raw AI SHA-256:** `95ac502b0880efcc1c6ceb040a1171eeacebff5c262a5f6df8d49a86cadcaf70`
- **Human-Designed Extension Cases:** `7` (`TC-FR14-H01` .. `TC-FR14-H07`)
- **Human Audit Status:** `COMPLETE (39 VALID, 0 INVALID, 3 INCOMPLETE; 42 USABLE AFTER CORRECTIONS)`
- **Total Executable Cases:** `49`

---

## 1. Audit Standards & Verdict Definitions

Every AI-generated test case is evaluated against authoritative specifications (HW06 Requirements, EShop SRS FR-14 / FR-12, `api_specification.md`):

- **`VALID`:** Test case correctly implements CRUD endpoints, parameter validation, admin role gates (SEC-02), or public read behavior without modification.
- **`INVALID`:** Test case invents unsupported requirements, conflates multiple orthogonal dimensions, or uses an irrecoverably broken oracle.
- **`INCOMPLETE`:** Test case addresses a valid objective, but requires refinement (e.g. concrete payload value, status code disjunction, or dual-assertion defect framing) before executable use.

---

## 2. Complete 42-Case Human Audit Decision Table

| Test ID | AI Objective | Spec Basis | Oracle Strength | Human Verdict | Human Reasoning | Required Correction | Executable? |
|---|---|---|---|:---:|---|---|:---:|
| `TC-FR14-001` | Public GET category listing without auth | API-SPEC §Category | HIGH | **VALID** | Verifies public accessibility of category list; returns $\ge 3$ seeded items. | NONE | **YES** |
| `TC-FR14-002` | Admin creates category "Tablet" | SRS FR-14 | HIGH | **VALID** | Baseline valid creation with Admin auth. Auto-increment ID returned. | NONE | **YES** |
| `TC-FR14-003` | Read-after-write verification of created category | REST Invariants | HIGH | **VALID** | Verifies database persistence of created entity via GET. | NONE | **YES** |
| `TC-FR14-004` | Admin updates category name to "Tablets & iPads" | SRS FR-14 | HIGH | **VALID** | Baseline valid update with Admin auth. | NONE | **YES** |
| `TC-FR14-005` | Read-after-write verification of updated name | REST Invariants | HIGH | **VALID** | Verifies database persistence of modified entity via GET. | NONE | **YES** |
| `TC-FR14-006` | Admin deletes category entity | SRS FR-14 | HIGH | **VALID** | Baseline valid deletion with Admin auth. | NONE | **YES** |
| `TC-FR14-007` | Anonymous POST create rejection | SEC-01 | HIGH | **VALID** | Missing `Authorization` header on mutating endpoint must return 401. | NONE | **YES** |
| `TC-FR14-008` | Anonymous PUT update rejection | SEC-01 | HIGH | **VALID** | Missing `Authorization` header on mutating endpoint must return 401. | NONE | **YES** |
| `TC-FR14-009` | Anonymous DELETE rejection | SEC-01 | HIGH | **VALID** | Missing `Authorization` header on mutating endpoint must return 401. | NONE | **YES** |
| `TC-FR14-010` | Malformed JWT string on POST create | SEC-01 | HIGH | **VALID** | Random invalid string rejected with 403 Forbidden. | NONE | **YES** |
| `TC-FR14-011` | Cryptographically tampered JWT on DELETE | SEC-01 | HIGH | **INCOMPLETE** | Raw AI omitted concrete token string. | Provided valid-header JWT with tampered signature string. | **YES** |
| `TC-FR14-012` | Regular customer creates category | SEC-02 / SRS FR-12 | HIGH | **VALID** | Regular customer (`role=user`) attempting admin mutation. SUT returns 200 (BUG-FR14-001). | Dual-assertion: Assert 403 (SRS) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-013` | Regular customer updates category | SEC-02 / SRS FR-12 | HIGH | **VALID** | Regular customer attempting admin update. SUT returns 200 (BUG-FR14-001). | Dual-assertion: Assert 403 (SRS) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-014` | Regular customer deletes category | SEC-02 / SRS FR-12 | HIGH | **VALID** | Regular customer attempting admin delete. SUT returns 200 (BUG-FR14-001). | Dual-assertion: Assert 403 (SRS) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-015` | Regular customer reads category list | Authorization | HIGH | **VALID** | Verifies public read boundary remains accessible to authenticated users. | NONE | **YES** |
| `TC-FR14-016` | Empty string name (`""`) on POST | Input Validation | HIGH | **VALID** | Empty category name should return 400 Bad Request. SUT accepts it (BUG-FR14-002). | Dual-assertion: Assert 400 (ideal) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-017` | Null name value (`null`) on POST | Input Validation | HIGH | **VALID** | Null category name should return 400. SUT accepts it (BUG-FR14-002). | Dual-assertion: Assert 400 (ideal) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-018` | Missing name key (`{}`) on POST | Input Validation | HIGH | **VALID** | Missing mandatory field should return 400. SUT accepts it (BUG-FR14-002). | Dual-assertion: Assert 400 (ideal) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-019` | Whitespace-only name (`"   "`) on POST | Input Validation | HIGH | **VALID** | Whitespace-only name should return 400. SUT accepts it (BUG-FR14-002). | Dual-assertion: Assert 400 (ideal) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-020` | Boundary: 1001-character string name | Boundary | MEDIUM | **INCOMPLETE** | Raw AI did not specify exact string length or verify storage bounds. | Pre-request generates exact 1001-character repeated string. | **YES** |
| `TC-FR14-021` | Vietnamese Unicode & emoji name | I18N / Boundary | HIGH | **VALID** | Verifies UTF-8 multi-byte storage in SQLite without encoding corruption. | NONE | **YES** |
| `TC-FR14-022` | Duplicate category name ("Laptop") | Business Logic | MEDIUM | **VALID** | Duplicate names permitted by SQLite; flags non-uniqueness. | Dual-assertion: Assert 409 (ideal) + assert 200 duplicate permitted. | **YES** |
| `TC-FR14-023` | Integer value coercion for name | Type Safety | MEDIUM | **VALID** | Non-string numeric value coerced to text in SQLite. | NONE | **YES** |
| `TC-FR14-024` | PUT with non-existent ID (99999) | Boundary / CRUD | HIGH | **VALID** | Updating non-existent entity should return 404. SUT returns 200 (BUG-FR14-003). | Dual-assertion: Assert 404 (ideal) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-025` | DELETE with non-existent ID (99999) | Boundary / CRUD | HIGH | **VALID** | Deleting non-existent entity should return 404. SUT returns 200 (BUG-FR14-003). | Dual-assertion: Assert 404 (ideal) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-026` | PUT with ID = 0 | Boundary | MEDIUM | **VALID** | Boundary zero value handled safely without server crash. | NONE | **YES** |
| `TC-FR14-027` | DELETE with ID = -1 | Boundary | MEDIUM | **VALID** | Boundary negative value handled safely without server crash. | NONE | **YES** |
| `TC-FR14-028` | PUT with non-numeric string ID ("abc") | Type Safety | MEDIUM | **VALID** | Non-numeric path parameter handled safely without server crash. | NONE | **YES** |
| `TC-FR14-029` | SQL Injection probe in name | SEC-03 | HIGH | **VALID** | `'; DROP TABLE categories;--` tested against parameterized query. | NONE | **YES** |
| `TC-FR14-029b` | Post-SQLi table verification | SEC-03 | HIGH | **VALID** | Follow-up GET confirms categories table remains intact. | NONE | **YES** |
| `TC-FR14-030` | Stored XSS payload in name | SEC-03 | HIGH | **VALID** | `<script>alert('XSS')</script>` stored verbatim. | Assert status 200; note stored XSS risk. | **YES** |
| `TC-FR14-031` | Mass assignment extra body fields | SEC-07 | HIGH | **VALID** | Extra fields (`id`, `admin`) discarded; auto-increment preserved. | NONE | **YES** |
| `TC-FR14-032` | Mass assignment body ID override | SEC-07 | HIGH | **VALID** | Body `id: 999` ignored; path ID 2 enforced. | NONE | **YES** |
| `TC-FR14-033` | NoSQL injection object payload | SEC-03 | MEDIUM | **INCOMPLETE** | Object payload may cause parser exception before reaching DB. | Relax oracle to accept 200, 400, or 500 without fatal crash. | **YES** |
| `TC-FR14-034` | IDOR category deletion as regular user | SEC-04 | HIGH | **VALID** | Customer deletes Category 3. SUT returns 200 (confirms BUG-FR14-001). | Dual-assertion: Assert 403 (SRS) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-035` | Multi-step full CRUD lifecycle sequence | Lifecycle | HIGH | **VALID** | Sequential Create $\rightarrow$ Read $\rightarrow$ Update $\rightarrow$ Read $\rightarrow$ Delete $\rightarrow$ Read. | Implemented as 5 sub-requests (a..e) in collection. | **YES** |
| `TC-FR14-036` | DELETE category with associated products | Referential Integrity | HIGH | **VALID** | Seeded Category 1 deleted; products orphaned. | Dual-assertion: Assert 409 (ideal) + assert 200 orphan defect. | **YES** |
| `TC-FR14-037` | PUT update on recently deleted category | State Transition | HIGH | **VALID** | Zombie update should return 404. SUT returns 200 (BUG-FR14-003). | Dual-assertion: Assert 404 (ideal) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-038` | Double DELETE on same category | Idempotency | HIGH | **VALID** | Second delete should return 404. SUT returns 200 (BUG-FR14-003). | Dual-assertion: Assert 404 (ideal) + assert 200 defect confirmation. | **YES** |
| `TC-FR14-039` | Schema: GET category array contract | Schema Validation | HIGH | **VALID** | Validates JSON array schema with required `{id: int, name: str}`. | JSON Schema assertions included. | **YES** |
| `TC-FR14-040` | Schema: POST create response contract | Schema Validation | HIGH | **VALID** | Validates `{message: string, id: int}` schema. | JSON Schema assertions included. | **YES** |
| `TC-FR14-041` | Schema: PUT update response contract | Schema Validation | HIGH | **VALID** | Validates `{message: string}` schema. | JSON Schema assertions included. | **YES** |
| `TC-FR14-042` | Schema: DELETE response contract | Schema Validation | HIGH | **VALID** | Validates `{message: string}` schema. | JSON Schema assertions included. | **YES** |

---

## 3. Human-Designed Extension Cases Summary (`TC-FR14-H01..H07`)

The following 7 test cases were designed by the human engineer to close critical testing blind spots missed by the AI generation:

| Extension ID | Blind Spot Addressed | Technique | Preconditions | Target Route | Expected vs SUT Result |
|---|---|---|---|---|---|
| `TC-FR14-H01` | Missing `Content-Type` header causes server crash | Protocol Robustness | Admin token | `POST /api/categories` | Expected: 400/415. **SUT: 500 Uncaught Exception (BUG-FR14-004)** |
| `TC-FR14-H02` | Zero-byte body stream handling | Input Robustness | Admin token | `POST /api/categories` | Expected: 400. SUT: Handled safely without crash. |
| `TC-FR14-H03` | Unsupported HTTP method (`PATCH`) probe | Verb Whitelisting | Admin token | `PATCH /api/categories/2` | Expected & SUT: 404 Not Found (route whitelisted). |
| `TC-FR14-H04` | Response header MIME type contract | Header Conformance | None | `GET /api/categories` | Expected & SUT: `Content-Type: application/json`. |
| `TC-FR14-H05` | Silent data corruption: empty `{}` PUT | Data Integrity | Admin token | `PUT /api/categories/2` | Expected: 400. **SUT: 200 Corrupts name to NULL**. |
| `TC-FR14-H06` | Rapid batch sequential category creation | Concurrency / Stress | Admin token | `POST /api/categories` (x3) | Expected & SUT: 3 distinct IDs monotonically incrementing. |
| `TC-FR14-H07` | Relational foreign key orphan proof | Defect Confirmation | SUT running | `GET /api/products` | **DEFECT CONFIRMED:** Products with `category_id=1` exist orphaned. |
