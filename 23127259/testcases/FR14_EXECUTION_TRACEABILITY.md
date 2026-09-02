# FR-14 Test Execution Traceability Matrix

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-14 – Category Management CRUD (Pool C – Web Admin)
- **Total Formal Executable Cases:** `49` (42 AI + 7 Human Extension)
- **Total Executable Requests in Collection:** `57` (3 Setup Helpers + 54 Test Requests)

---

## 1. Executable Test Cases Traceability Table

| Formal ID | Provenance | Human Audit Verdict | Postman Folder | HTTP Method | Endpoint | Setup Dependency | Target Oracle / Assertion | Defect Association |
|---|---|:---:|---|:---:|---|---|---|:---:|
| `TC-FR14-001` | AI-Generated | VALID | `01 – Happy-Path CRUD` | `GET` | `/api/categories` | SUT Seed Data | Status 200, array length $\ge 3$, valid `{id, name}` | — |
| `TC-FR14-002` | AI-Generated | VALID | `01 – Happy-Path CRUD` | `POST` | `/api/categories` | Admin Token | Status 200, message "Category created", numeric ID | — |
| `TC-FR14-003` | AI-Generated | VALID | `01 – Happy-Path CRUD` | `GET` | `/api/categories` | TC-FR14-002 | Status 200, created category found in array | — |
| `TC-FR14-004` | AI-Generated | VALID | `01 – Happy-Path CRUD` | `PUT` | `/api/categories/:id` | TC-FR14-002 | Status 200, message "Category updated" | — |
| `TC-FR14-005` | AI-Generated | VALID | `01 – Happy-Path CRUD` | `GET` | `/api/categories` | TC-FR14-004 | Status 200, updated name "Tablets & iPads" verified | — |
| `TC-FR14-006` | AI-Generated | VALID | `01 – Happy-Path CRUD` | `DELETE` | `/api/categories/:id` | TC-FR14-002 | Status 200, message "Category deleted" | — |
| `TC-FR14-007` | AI-Generated | VALID | `02 – Authentication (SEC-01)` | `POST` | `/api/categories` | None | Status 401, error "Unauthorized" | — |
| `TC-FR14-008` | AI-Generated | VALID | `02 – Authentication (SEC-01)` | `PUT` | `/api/categories/1` | None | Status 401, error "Unauthorized" | — |
| `TC-FR14-009` | AI-Generated | VALID | `02 – Authentication (SEC-01)` | `DELETE` | `/api/categories/1` | None | Status 401, error "Unauthorized" | — |
| `TC-FR14-010` | AI-Generated | VALID | `02 – Authentication (SEC-01)` | `POST` | `/api/categories` | Malformed JWT | Status 403, error "Forbidden" | — |
| `TC-FR14-011` | AI-Generated | INCOMPLETE (Corrected) | `02 – Authentication (SEC-01)` | `DELETE` | `/api/categories/1` | Tampered JWT | Status 403, error "Forbidden" | — |
| `TC-FR14-012` | AI-Generated | VALID | `03 – Authorization RBAC (SEC-02)` | `POST` | `/api/categories` | User Token | Expected 403 vs Actual 200 | **BUG-FR14-001** |
| `TC-FR14-013` | AI-Generated | VALID | `03 – Authorization RBAC (SEC-02)` | `PUT` | `/api/categories/2` | User Token | Expected 403 vs Actual 200 | **BUG-FR14-001** |
| `TC-FR14-014` | AI-Generated | VALID | `03 – Authorization RBAC (SEC-02)` | `DELETE` | `/api/categories/:id` | User Token | Expected 403 vs Actual 200 | **BUG-FR14-001** |
| `TC-FR14-015` | AI-Generated | VALID | `03 – Authorization RBAC (SEC-02)` | `GET` | `/api/categories` | User Token | Status 200, public read allowed | — |
| `TC-FR14-016` | AI-Generated | VALID | `04 – Input Validation (Name)` | `POST` | `/api/categories` | Admin Token | Expected 400 vs Actual 200 | **BUG-FR14-002** |
| `TC-FR14-017` | AI-Generated | VALID | `04 – Input Validation (Name)` | `POST` | `/api/categories` | Admin Token | Expected 400 vs Actual 200 | **BUG-FR14-002** |
| `TC-FR14-018` | AI-Generated | VALID | `04 – Input Validation (Name)` | `POST` | `/api/categories` | Admin Token | Expected 400 vs Actual 200 | **BUG-FR14-002** |
| `TC-FR14-019` | AI-Generated | VALID | `04 – Input Validation (Name)` | `POST` | `/api/categories` | Admin Token | Expected 400 vs Actual 200 | **BUG-FR14-002** |
| `TC-FR14-020` | AI-Generated | INCOMPLETE (Corrected) | `04 – Input Validation (Name)` | `POST` | `/api/categories` | Admin Token | Status 200/400, 1001-char string | — |
| `TC-FR14-021` | AI-Generated | VALID | `04 – Input Validation (Name)` | `POST` | `/api/categories` | Admin Token | Status 200, Unicode & emoji preserved | — |
| `TC-FR14-022` | AI-Generated | VALID | `04 – Input Validation (Name)` | `POST` | `/api/categories` | Admin Token | Expected 409 vs Actual 200 | Non-unique |
| `TC-FR14-023` | AI-Generated | VALID | `04 – Input Validation (Name)` | `POST` | `/api/categories` | Admin Token | Status 200/400, number coerced to text | — |
| `TC-FR14-024` | AI-Generated | VALID | `05 – Input Validation (ID)` | `PUT` | `/api/categories/99999` | Admin Token | Expected 404 vs Actual 200 | **BUG-FR14-003** |
| `TC-FR14-025` | AI-Generated | VALID | `05 – Input Validation (ID)` | `DELETE` | `/api/categories/99999` | Admin Token | Expected 404 vs Actual 200 | **BUG-FR14-003** |
| `TC-FR14-026` | AI-Generated | VALID | `05 – Input Validation (ID)` | `PUT` | `/api/categories/0` | Admin Token | Status 200/400/404 handled | — |
| `TC-FR14-027` | AI-Generated | VALID | `05 – Input Validation (ID)` | `DELETE` | `/api/categories/-1` | Admin Token | Status 200/400/404 handled | — |
| `TC-FR14-028` | AI-Generated | VALID | `05 – Input Validation (ID)` | `PUT` | `/api/categories/abc` | Admin Token | Status 200/400/404 handled | — |
| `TC-FR14-029` | AI-Generated | VALID | `06 – Security Probes` | `POST` | `/api/categories` | Admin Token | Status $\ne$ 500, parameterized SQLi safe | — |
| `TC-FR14-029b` | AI-Generated | VALID | `06 – Security Probes` | `GET` | `/api/categories` | None | Status 200, table intact after SQLi probe | — |
| `TC-FR14-030` | AI-Generated | VALID | `06 – Security Probes` | `POST` | `/api/categories` | Admin Token | Status 200, stored XSS payload accepted | Stored XSS |
| `TC-FR14-031` | AI-Generated | VALID | `06 – Security Probes` | `POST` | `/api/categories` | Admin Token | Status 200, mass assignment fields discarded | — |
| `TC-FR14-032` | AI-Generated | VALID | `06 – Security Probes` | `PUT` | `/api/categories/2` | Admin Token | Status 200, body ID override ignored | — |
| `TC-FR14-033` | AI-Generated | INCOMPLETE (Corrected) | `06 – Security Probes` | `POST` | `/api/categories` | Admin Token | Status 200/400/500, object payload handled | — |
| `TC-FR14-034` | AI-Generated | VALID | `06 – Security Probes` | `DELETE` | `/api/categories/3` | User Token | Expected 403 vs Actual 200 | **BUG-FR14-001** |
| `TC-FR14-035a` | AI-Generated | VALID | `07 – State Transitions` | `POST` | `/api/categories` | Admin Token | Lifecycle 1: Create entity | — |
| `TC-FR14-035b` | AI-Generated | VALID | `07 – State Transitions` | `GET` | `/api/categories` | None | Lifecycle 2: Read verify creation | — |
| `TC-FR14-035c` | AI-Generated | VALID | `07 – State Transitions` | `PUT` | `/api/categories/:id` | Admin Token | Lifecycle 3: Update entity name | — |
| `TC-FR14-035d` | AI-Generated | VALID | `07 – State Transitions` | `DELETE` | `/api/categories/:id` | Admin Token | Lifecycle 4: Delete entity | — |
| `TC-FR14-035e` | AI-Generated | VALID | `07 – State Transitions` | `GET` | `/api/categories` | None | Lifecycle 5: Read verify deletion | — |
| `TC-FR14-036` | AI-Generated | VALID | `07 – State Transitions` | `DELETE` | `/api/categories/1` | Admin Token | Status 200, no referential integrity check | Orphaned FK |
| `TC-FR14-037` | AI-Generated | VALID | `07 – State Transitions` | `PUT` | `/api/categories/:id` | Admin Token | Expected 404 vs Actual 200 | **BUG-FR14-003** |
| `TC-FR14-038` | AI-Generated | VALID | `07 – State Transitions` | `DELETE` | `/api/categories/:id` | Admin Token | Expected 404 vs Actual 200 | **BUG-FR14-003** |
| `TC-FR14-039` | AI-Generated | VALID | `08 – Schema Validation` | `GET` | `/api/categories` | None | Schema array of `{id, name}`, Content-Type | — |
| `TC-FR14-040` | AI-Generated | VALID | `08 – Schema Validation` | `POST` | `/api/categories` | Admin Token | Schema `{message, id}`, message validation | — |
| `TC-FR14-041` | AI-Generated | VALID | `08 – Schema Validation` | `PUT` | `/api/categories/:id` | Admin Token | Schema `{message}`, message validation | — |
| `TC-FR14-042` | AI-Generated | VALID | `08 – Schema Validation` | `DELETE` | `/api/categories/:id` | Admin Token | Schema `{message}`, message validation | — |
| `TC-FR14-H03` | Student Extension | VALID | `09 – Human Extension Cases` | `PATCH` | `/api/categories/2` | Admin Token | Status 404/405, route whitelisting | — |
| `TC-FR14-H04` | Student Extension | VALID | `09 – Human Extension Cases` | `GET` | `/api/categories` | None | Response `Content-Type: application/json` | — |
| `TC-FR14-H05` | Student Extension | VALID | `09 – Human Extension Cases` | `PUT` | `/api/categories/2` | Admin Token | Expected 400 vs Actual 200 | Corrupts NULL |
| `TC-FR14-H06a` | Student Extension | VALID | `09 – Human Extension Cases` | `POST` | `/api/categories` | Admin Token | Rapid batch sequential create 1 | — |
| `TC-FR14-H06b` | Student Extension | VALID | `09 – Human Extension Cases` | `POST` | `/api/categories` | Admin Token | Rapid batch sequential create 2 | — |
| `TC-FR14-H06c` | Student Extension | VALID | `09 – Human Extension Cases` | `POST` | `/api/categories` | Admin Token | Rapid batch sequential create 3 | — |
| `TC-FR14-H07` | Student Extension | VALID | `09 – Human Extension Cases` | `GET` | `/api/products` | TC-FR14-036 | Products with `category_id=1` exist orphaned | Orphaned FK |
