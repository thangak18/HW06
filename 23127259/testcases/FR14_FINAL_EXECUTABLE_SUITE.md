# FR-14 Final Executable Test Suite Specification

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-14 – Category Management CRUD (Pool C – Web Admin)
- **Status:** **FINAL EXECUTABLE SPECIFICATION (POST-HUMAN AUDIT & EXTENSION)**
- **Total Formal Test Cases:** `49` (42 Audited AI Cases + 7 Human Extension Cases)
- **Total Executable Requests in Collection:** `57` (3 Setup Helpers + 54 Test Requests)
- **Total Assertions Executed:** `94`

---

## 1. Executive Suite Summary & Composition

This document defines the authoritative, finalized **49-case executable test suite** for feature **FR-14 (Category Management CRUD)**. It integrates:
1. **42 Audited & Corrected AI-Derived Test Cases (`TC-FR14-001` .. `TC-FR14-042`):** Derived from `FR14_AI_DRAFT.md`, audited in `FR14_HUMAN_AUDIT_CORRECTIONS.md`, and finalized with dual-assertion oracles that verify both ideal specification compliance and actual SUT bug detection.
2. **7 Student-Selected Human Extension Test Cases (`TC-FR14-H01` .. `TC-FR14-H07`):** Selected and finalized in `FR14_HUMAN_TEST_CASES.md` addressing protocol robustness (`H01`), zero-payload streams (`H02`), unsupported HTTP verbs (`H03`), response header contracts (`H04`), silent data corruption (`H05`), rapid-fire sequential allocation (`H06`), and relational foreign key orphaning (`H07`).

---

## 2. Test Suite Classification & Oracle Discipline

- **`SPECIFICATION-BACKED` (34 Cases):** Verifiable against explicit SRS rules, REST CRUD conventions, and security requirements (`SEC-01`, `SEC-02`, `SEC-03`, `SEC-07`).
- **`DUAL-ASSERTION DEFECT CONFIRMATION` (10 Cases):** Tests designed to document expected SRS behavior (which fails) alongside verified SUT defect confirmation (which passes), providing definitive evidence of underlying bugs (`BUG-FR14-001`, `BUG-FR14-002`, `BUG-FR14-003`).
- **`EXPLORATORY / BOUNDARY` (5 Cases):** Boundary length limits, non-numeric ID coercion, and rapid sequential creation observing SQLite storage characteristics.

---

## 3. Formal Executable Test Cases Inventory

### Folder 01 – Happy-Path CRUD (6 Cases)

| Test ID | Method | Endpoint | Description | Expected Status | SUT Actual Status | Verdict |
|---|:---:|---|---|:---:|:---:|:---:|
| **TC-FR14-001** | `GET` | `/api/categories` | Public list categories without authentication | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-002** | `POST` | `/api/categories` | Admin creates category "Tablet" | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-003** | `GET` | `/api/categories` | Verify created category present in list | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-004** | `PUT` | `/api/categories/:id` | Admin updates category name to "Tablets & iPads" | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-005** | `GET` | `/api/categories` | Verify updated category name persisted | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-006** | `DELETE` | `/api/categories/:id` | Admin deletes created category | `200 OK` | `200 OK` | ✅ PASS |

---

### Folder 02 – Authentication Enforcement (SEC-01) (5 Cases)

| Test ID | Method | Endpoint | Description | Expected Status | SUT Actual Status | Verdict |
|---|:---:|---|---|:---:|:---:|:---:|
| **TC-FR14-007** | `POST` | `/api/categories` | Create without `Authorization` header | `401 Unauthorized` | `401 Unauthorized` | ✅ PASS |
| **TC-FR14-008** | `PUT` | `/api/categories/1` | Update without `Authorization` header | `401 Unauthorized` | `401 Unauthorized` | ✅ PASS |
| **TC-FR14-009** | `DELETE` | `/api/categories/1` | Delete without `Authorization` header | `401 Unauthorized` | `401 Unauthorized` | ✅ PASS |
| **TC-FR14-010** | `POST` | `/api/categories` | Create with malformed token string | `403 Forbidden` | `403 Forbidden` | ✅ PASS |
| **TC-FR14-011** | `DELETE` | `/api/categories/1` | Delete with cryptographically tampered token | `403 Forbidden` | `403 Forbidden` | ✅ PASS |

---

### Folder 03 – Authorization & RBAC (SEC-02) (4 Cases)

| Test ID | Method | Endpoint | Description | Expected Status (SRS) | SUT Actual Status | Defect Confirmed |
|---|:---:|---|---|:---:|:---:|:---:|
| **TC-FR14-012** | `POST` | `/api/categories` | Regular customer creates category | `403 Forbidden` | `200 OK` | ⚠️ **BUG-FR14-001** |
| **TC-FR14-013** | `PUT` | `/api/categories/2` | Regular customer updates category | `403 Forbidden` | `200 OK` | ⚠️ **BUG-FR14-001** |
| **TC-FR14-014** | `DELETE` | `/api/categories/:id` | Regular customer deletes category | `403 Forbidden` | `200 OK` | ⚠️ **BUG-FR14-001** |
| **TC-FR14-015** | `GET` | `/api/categories` | Regular customer reads category list | `200 OK` | `200 OK` | ✅ PASS |

---

### Folder 04 – Input Validation: Name Parameter (8 Cases)

| Test ID | Method | Endpoint | Payload / Input | Expected Status | SUT Actual Status | Defect Confirmed |
|---|:---:|---|---|:---:|:---:|:---:|
| **TC-FR14-016** | `POST` | `/api/categories` | `{"name": ""}` | `400 Bad Request` | `200 OK` | ⚠️ **BUG-FR14-002** |
| **TC-FR14-017** | `POST` | `/api/categories` | `{"name": null}` | `400 Bad Request` | `200 OK` | ⚠️ **BUG-FR14-002** |
| **TC-FR14-018** | `POST` | `/api/categories` | `{}` | `400 Bad Request` | `200 OK` | ⚠️ **BUG-FR14-002** |
| **TC-FR14-019** | `POST` | `/api/categories` | `{"name": "   "}` | `400 Bad Request` | `200 OK` | ⚠️ **BUG-FR14-002** |
| **TC-FR14-020** | `POST` | `/api/categories` | 1001-character string | `200 / 400` | `200 OK` | ✅ PASS (Unbounded) |
| **TC-FR14-021** | `POST` | `/api/categories` | "Điện tử 📱 & Phụ kiện" | `200 OK` | `200 OK` | ✅ PASS (Unicode) |
| **TC-FR14-022** | `POST` | `/api/categories` | Duplicate name "Laptop" | `409 Conflict` | `200 OK` | ⚠️ Non-unique |
| **TC-FR14-023** | `POST` | `/api/categories` | `{"name": 12345}` | `200 / 400` | `200 OK` | ✅ PASS (Coerced) |

---

### Folder 05 – Input Validation: ID Parameter (5 Cases)

| Test ID | Method | Endpoint | Parameter Value | Expected Status | SUT Actual Status | Defect Confirmed |
|---|:---:|---|---|:---:|:---:|:---:|
| **TC-FR14-024** | `PUT` | `/api/categories/99999` | Non-existent ID | `404 Not Found` | `200 OK` | ⚠️ **BUG-FR14-003** |
| **TC-FR14-025** | `DELETE` | `/api/categories/99999` | Non-existent ID | `404 Not Found` | `200 OK` | ⚠️ **BUG-FR14-003** |
| **TC-FR14-026** | `PUT` | `/api/categories/0` | Zero ID boundary | `200 / 400 / 404` | `200 OK` | ✅ Handled |
| **TC-FR14-027** | `DELETE` | `/api/categories/-1` | Negative integer ID | `200 / 400 / 404` | `200 OK` | ✅ Handled |
| **TC-FR14-028** | `PUT` | `/api/categories/abc` | Alphanumeric string ID | `200 / 400 / 404` | `200 OK` | ✅ Handled |

---

### Folder 06 – Security Probes (SEC-03 / SEC-04 / SEC-07) (6 Cases / 7 Requests)

| Test ID | Method | Endpoint | Probe Target | Expected Result | SUT Actual Result | Verdict |
|---|:---:|---|---|---|---|:---:|
| **TC-FR14-029** | `POST` | `/api/categories` | SQL Injection: `'; DROP TABLE...` | Parameterized execution, table preserved | Stored as literal string | ✅ PASS (SEC-03) |
| **TC-FR14-029b** | `GET` | `/api/categories` | Post-SQLi table verification | Categories table returns rows | Table intact | ✅ PASS (SEC-03) |
| **TC-FR14-030** | `POST` | `/api/categories` | Stored XSS: `<script>alert('XSS')</script>` | Stored verbatim | Stored verbatim | ⚠️ Stored XSS |
| **TC-FR14-031** | `POST` | `/api/categories` | Mass assignment extra fields (`id`, `admin`) | Extra fields discarded, auto ID | Auto-increment preserved | ✅ PASS (SEC-07) |
| **TC-FR14-032** | `PUT` | `/api/categories/2` | Mass assignment ID override | ID parameter path preserved | ID preserved | ✅ PASS (SEC-07) |
| **TC-FR14-033** | `POST` | `/api/categories` | NoSQL Injection object payload | Handled without server crash | Handled gracefully | ✅ PASS (SEC-03) |
| **TC-FR14-034** | `DELETE` | `/api/categories/3` | IDOR: User deletes Category 3 | `403 Forbidden` | `200 OK` | ⚠️ **BUG-FR14-001** |

---

### Folder 07 – State Transitions & Referential Integrity (4 Cases / 8 Requests)

| Test ID | Method | Endpoint | Transition / Operation | Expected Status | SUT Actual Status | Defect Confirmed |
|---|:---:|---|---|:---:|:---:|:---:|
| **TC-FR14-035a** | `POST` | `/api/categories` | Lifecycle: Create "Lifecycle Test" | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-035b** | `GET` | `/api/categories` | Lifecycle: Verify created entity | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-035c** | `PUT` | `/api/categories/:id` | Lifecycle: Update to "Lifecycle Updated" | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-035d** | `DELETE` | `/api/categories/:id` | Lifecycle: Delete entity | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-035e** | `GET` | `/api/categories` | Lifecycle: Verify entity removed | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-036** | `DELETE` | `/api/categories/1` | Delete Category 1 with products | `409 Conflict` (ideal) | `200 OK` | ⚠️ No FK check |
| **TC-FR14-037** | `PUT` | `/api/categories/:id` | Update recently deleted category | `404 Not Found` | `200 OK` | ⚠️ **BUG-FR14-003** |
| **TC-FR14-038** | `DELETE` | `/api/categories/:id` | Double delete on same category | `404 Not Found` | `200 OK` | ⚠️ **BUG-FR14-003** |

---

### Folder 08 – Schema Validation (4 Cases)

| Test ID | Method | Endpoint | Schema Target | Assertions | Verdict |
|---|:---:|---|---|---|:---:|
| **TC-FR14-039** | `GET` | `/api/categories` | Array of `{id: int, name: str}` | Array type, item properties, Content-Type | ✅ PASS |
| **TC-FR14-040** | `POST` | `/api/categories` | `{message: string, id: int}` | Message equals "Category created", id > 0 | ✅ PASS |
| **TC-FR14-041** | `PUT` | `/api/categories/:id` | `{message: string}` | Message equals "Category updated" | ✅ PASS |
| **TC-FR14-042** | `DELETE` | `/api/categories/:id` | `{message: string}` | Message equals "Category deleted" | ✅ PASS |

---

### Folder 09 – Human Extension Cases (7 Cases / 7 Requests)

| Test ID | Method | Endpoint | Technique / Objective | Expected Status | SUT Actual Status | Verdict |
|---|:---:|---|---|:---:|:---:|:---:|
| **TC-FR14-H03** | `PATCH` | `/api/categories/2` | Unsupported HTTP method probe | `404 / 405` | `404 Not Found` | ✅ PASS |
| **TC-FR14-H04** | `GET` | `/api/categories` | Response headers contract validation | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-H05** | `PUT` | `/api/categories/2` | Silent corruption probe: empty body `{}` | `400 Bad Request` | `200 OK` | ⚠️ Corrupts to NULL |
| **TC-FR14-H06a** | `POST` | `/api/categories` | Rapid batch sequential create 1 | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-H06b** | `POST` | `/api/categories` | Rapid batch sequential create 2 | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-H06c** | `POST` | `/api/categories` | Rapid batch sequential create 3 | `200 OK` | `200 OK` | ✅ PASS |
| **TC-FR14-H07** | `GET` | `/api/products` | Referential orphan detection after delete | `200 OK` | `200 OK` | ⚠️ Products orphaned |

---

## 4. Execution Summary

- **Total Requests in Collection:** 57 (3 setup helpers + 54 formal test requests)
- **Total Assertions:** 94
- **Passed Assertions:** 80 (85.1%)
- **Failed Assertions:** 14 (14.9%) — 100% of failures correspond to **intentional dual-assertion defect confirmations** for `BUG-FR14-001`, `BUG-FR14-002`, and `BUG-FR14-003`.
