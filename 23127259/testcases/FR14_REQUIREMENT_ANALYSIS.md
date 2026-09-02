# FR-14 Requirement & CRUD State Analysis

**Feature ID:** FR-14 – Category Management CRUD (Pool C – Web Admin)  
**Student Name:** Nguyễn Tấn Thắng  
**Student ID:** `23127259`  
**Authoritative Standards:** EShop SRS, `api_specification.md` (Section: Admin Categories), HW06 Assignment Requirements  
**Analysis Date:** September 2, 2026

---

## 0. Human Review Corrections Before Generation

> [!NOTE]
> **SUT Source-Code Grounding Notice:**  
> This analysis was grounded against the actual SUT implementation at `/Volumes/Thang/eshop-sut/backend/server.js` (lines 243–279) and `database.js` (lines 23–26, 84–87).  
> The following critical deviations between the assignment specification and the actual SUT implementation were identified:
> 1. **Route Path Mismatch:** The assignment specification (FR-14) specifies `POST/PUT/DELETE /api/admin/categories` (admin-prefix routes). The actual SUT implements `POST/PUT/DELETE /api/categories` (non-admin routes). The `GET /api/categories` is public (no auth). This is a **normative discrepancy** that must be tested against the actual implementation.
> 2. **Missing RBAC/Authorization:** The SUT applies `authenticateToken` middleware to POST/PUT/DELETE but performs **NO role check** (no `isAdmin` middleware). Any authenticated user (role=`user` or role=`admin`) can create, update, and delete categories. This is a potential **SEC-02 (Authorization) security bug**.
> 3. **Missing Input Validation:** The SUT does not validate the `name` field — null, empty, whitespace, extremely long values are all accepted.
> 4. **No Duplicate Prevention:** The SUT does not enforce unique category names.
> 5. **No Referential Integrity Check on DELETE:** Deleting a category that has products referencing it (via `category_id` FK) does not cascade or block — it succeeds silently, orphaning products.
> 6. **No GET-by-ID endpoint:** There is no `GET /api/categories/:id` endpoint; only the list endpoint exists.

---

## 1. Feature Scope

FR-14 governs the full lifecycle of product category entities in the EShop admin panel. Categories serve as the organizational taxonomy for products — each product carries a `category_id` foreign key referencing the categories table.

Testing FR-14 requires verifying:
1. **CRUD operations:** Create, Read (list), Update, Delete of category entities.
2. **Authentication enforcement:** All mutating endpoints (POST/PUT/DELETE) require a valid JWT Bearer token.
3. **Authorization enforcement (RBAC):** Per SRS, only administrators should be able to manage categories (Pool C = Web Admin). Test whether the SUT correctly enforces role=admin.
4. **Input validation:** Proper handling of missing, empty, null, and boundary-length `name` values.
5. **Schema conformance:** Response JSON structure and HTTP status codes match API specification.
6. **Referential integrity:** Behavior when deleting categories that have associated products.
7. **Security dimensions:** Injection, IDOR, mass assignment, sensitive data exposure.

---

## 2. API Surface & Exact Endpoints

| HTTP Method | Actual SUT Endpoint | Assignment Spec Endpoint | Auth Middleware | Role Check | Request Body | Response Contract |
|---|---|---|:---:|:---:|---|---|
| `GET` | `/api/categories` | `/api/admin/categories` (implied) | **NONE** | **NONE** | None | `200`: Array of `{id, name}` |
| `POST` | `/api/categories` | `POST /api/admin/categories` | `authenticateToken` | **NONE** ⚠️ | `{ "name": "<string>" }` | `200`: `{ "message": "Category created", "id": <int> }` |
| `PUT` | `/api/categories/:id` | `PUT /api/admin/categories/:id` | `authenticateToken` | **NONE** ⚠️ | `{ "name": "<string>" }` | `200`: `{ "message": "Category updated" }` |
| `DELETE` | `/api/categories/:id` | `DELETE /api/admin/categories/:id` | `authenticateToken` | **NONE** ⚠️ | None | `200`: `{ "message": "Category deleted" }` |

> [!WARNING]
> **Route Path Discrepancy:** The SUT uses `/api/categories` (no `admin` prefix) while the assignment FR-14 definition specifies `/api/admin/categories`. Tests will target the **actual SUT routes** (`/api/categories`), but document this discrepancy as a potential specification violation.

---

## 3. Database Schema

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);
```

**Seed Data (3 categories):**
| Seeded ID | Name |
|---|---|
| 1 | Điện thoại |
| 2 | Laptop |
| 3 | Phụ kiện |

---

## 4. Actors and Authorization Model

FR-14 operates under four actor contexts:

1. **Unauthenticated Client (`ANON`):** No `Authorization` header. Expected: Can `GET` categories (public). Should be rejected (`401`) for POST/PUT/DELETE.
2. **Authenticated Regular User (`USER`):** Valid JWT with `role = 'user'`. Per SRS/assignment (FR-14 is Pool C = Web Admin), regular users should NOT be authorized for category management. **SUT Behavior: Currently ALLOWS all CRUD operations** — a SEC-02 violation.
3. **Authenticated Administrator (`ADMIN`):** Valid JWT with `role = 'admin'`. Authorized for all category CRUD operations.
4. **Invalid/Expired Token Bearer (`INVALID-TOKEN`):** Malformed or expired JWT. Expected: `403 Forbidden`.

---

## 5. Parameter Inventory

### 5.1 POST /api/categories

| Parameter | Data Type | Requirement | Format Constraint | Semantic Constraint | Boundary Limits | Security Relevance |
|---|---|---|---|---|---|---|
| `name` | String (JSON body) | Mandatory (logical) | Free text | Should be non-empty, meaningful category name | NOT SPECIFIED in SUT (no min/max validation) | Injection vector (SQLi via parameterized query — mitigated), XSS in stored name |

### 5.2 PUT /api/categories/:id

| Parameter | Data Type | Requirement | Format Constraint | Semantic Constraint | Boundary Limits | Security Relevance |
|---|---|---|---|---|---|---|
| `:id` (URL path) | Integer | Mandatory | Positive integer | Must reference existing category row | NOT SPECIFIED | IDOR vector — can any user update any category? |
| `name` | String (JSON body) | Mandatory (logical) | Free text | New name for category | NOT SPECIFIED | Same as POST |

### 5.3 DELETE /api/categories/:id

| Parameter | Data Type | Requirement | Format Constraint | Semantic Constraint | Boundary Limits | Security Relevance |
|---|---|---|---|---|---|---|
| `:id` (URL path) | Integer | Mandatory | Positive integer | Must reference existing category row | NOT SPECIFIED | Referential integrity — products orphaned? |

---

## 6. Equivalence Partitions

### 6.1 `name` Parameter (POST/PUT)

| Partition ID | Description | Classification | Spec Basis |
|---|---|:---:|---|
| EP-NM-01 | Valid non-empty string (e.g. "Electronics") | Valid | SRS FR-14 |
| EP-NM-02 | Empty string (`""`) | Invalid | Implied business logic |
| EP-NM-03 | Null value (`null`) | Invalid | Implied business logic |
| EP-NM-04 | Missing key (no `name` in body) | Invalid | Implied business logic |
| EP-NM-05 | Whitespace-only (`"   "`) | Invalid | Implied business logic |
| EP-NM-06 | Very long string (>1000 chars) | Boundary | NOT SPECIFIED |
| EP-NM-07 | Unicode/special chars (e.g. "Điện tử 📱") | Valid | Seed data uses Vietnamese |
| EP-NM-08 | Duplicate name (existing category name) | Exploratory | NOT SPECIFIED |
| EP-NM-09 | SQL injection probe (`'; DROP TABLE categories;--`) | Invalid/Probe | SEC-03 |
| EP-NM-10 | XSS payload (`<script>alert(1)</script>`) | Invalid/Probe | SEC-03 |
| EP-NM-11 | Integer value instead of string | Invalid | Type safety |

### 6.2 `:id` Parameter (PUT/DELETE)

| Partition ID | Description | Classification | Spec Basis |
|---|---|:---:|---|
| EP-ID-01 | Valid existing category ID (e.g. `1`) | Valid | SRS FR-14 |
| EP-ID-02 | Non-existent ID (e.g. `99999`) | Invalid | Business logic |
| EP-ID-03 | Zero (`0`) | Invalid | Boundary |
| EP-ID-04 | Negative number (`-1`) | Invalid | Boundary |
| EP-ID-05 | Non-numeric string (`"abc"`) | Invalid | Type safety |
| EP-ID-06 | Float number (`1.5`) | Invalid | Type safety |

### 6.3 Authentication Token

| Partition ID | Description | Classification | Spec Basis |
|---|---|:---:|---|
| EP-TK-01 | Valid admin JWT token | Valid | SEC-01 |
| EP-TK-02 | Valid user JWT token (non-admin) | Invalid for admin routes | SEC-02 |
| EP-TK-03 | Missing Authorization header | Invalid | SEC-01 |
| EP-TK-04 | Malformed token (random string) | Invalid | SEC-01 |
| EP-TK-05 | Expired/tampered token | Invalid | SEC-01 |

---

## 7. State Transitions (CRUD Lifecycle)

Category entities follow a simple existence lifecycle:

```
[Non-Existent] --POST (create)--> [Existing] --PUT (update)--> [Existing (modified)]
                                      |
                                      +--DELETE (remove)--> [Non-Existent]
```

### State Transition Table

| Current State | Action | Expected Next State | Expected HTTP Status | Notes |
|---|---|---|:---:|---|
| Non-Existent | POST with valid name | Existing | 200 | Category created with auto-incremented ID |
| Existing | GET list | Existing (no change) | 200 | Returns array including this category |
| Existing | PUT with valid name | Existing (name updated) | 200 | Name field overwritten |
| Existing | DELETE | Non-Existent | 200 | Row removed from database |
| Non-Existent | PUT with ID | Non-Existent | ⚠️ 200 (SUT returns success even for non-existent) | SUT does NOT check existence before UPDATE |
| Non-Existent | DELETE with ID | Non-Existent | ⚠️ 200 (SUT returns success even for non-existent) | SUT does NOT check existence before DELETE |
| Existing (with products) | DELETE | Non-Existent (products orphaned) | 200 | ⚠️ No referential integrity check |

---

## 8. Security Requirement Mapping

| Security Req | Description | FR-14 Applicability | Test Priority |
|---|---|---|:---:|
| SEC-01 | Authentication & session validity | POST/PUT/DELETE require valid JWT | HIGH |
| SEC-02 | Authorization & RBAC | Only admin should manage categories; **SUT MISSING** | CRITICAL |
| SEC-03 | Input sanitization & injection protection | SQL injection via `name` param (parameterized — likely safe); XSS in stored name | HIGH |
| SEC-04 | Insecure Direct Object Reference (IDOR) | Any auth user can target any category by ID | MEDIUM |
| SEC-05 | Sensitive data exposure | Category data is not sensitive; check for server info leakage in errors | LOW |
| SEC-06 | Rate limiting & brute force | Not typically applicable to CRUD admin endpoints | LOW |
| SEC-07 | Mass assignment & parameter tampering | Can user inject extra fields like `id` in POST body? | MEDIUM |

---

## 9. Identified Bug Candidates (Pre-Testing)

Based on source code analysis:

| Bug ID | Summary | Severity | SUT Evidence |
|---|---|:---:|---|
| BUG-FR14-CAND-01 | Missing RBAC: Regular user can create/update/delete categories | High | `authenticateToken` but no `isAdmin` check (server.js:249-279) |
| BUG-FR14-CAND-02 | No input validation: Empty/null/whitespace names accepted | Medium | No validation before `INSERT INTO categories (name) VALUES (?)` (server.js:251) |
| BUG-FR14-CAND-03 | No existence check on UPDATE: PUT succeeds for non-existent ID | Medium | `this.changes` not checked (server.js:258-266) |
| BUG-FR14-CAND-04 | No existence check on DELETE: DELETE succeeds for non-existent ID | Medium | `this.changes` not checked (server.js:269-277) |
| BUG-FR14-CAND-05 | No referential integrity: DELETE category orphans products | Medium | No FK constraint check (server.js:269-277) |
| BUG-FR14-CAND-06 | Route path mismatch: `/api/categories` vs spec `/api/admin/categories` | Low | server.js routes vs assignment spec |

---

## 10. Generation Plan

Target: **≥40 raw AI test cases** across the following dimensions:

| Dimension | Target Count | Coverage |
|---|:---:|---|
| Happy-path CRUD operations | 6 | Create, Read, Update, Delete with valid data |
| Domain partitions (name) | 8 | EP-NM-01 through EP-NM-11 |
| Domain partitions (id) | 5 | EP-ID-01 through EP-ID-06 |
| Authentication variations | 5 | EP-TK-01 through EP-TK-05 |
| Authorization / RBAC (SEC-02) | 4 | User vs Admin for each mutating endpoint |
| Security probes (SEC-03/04/07) | 6 | SQLi, XSS, IDOR, mass assignment |
| State transitions | 4 | Create→Read→Update→Delete lifecycle, orphaned products |
| Schema validation | 4 | Response structure, status codes, content-type |
| **Total** | **≥42** | |
