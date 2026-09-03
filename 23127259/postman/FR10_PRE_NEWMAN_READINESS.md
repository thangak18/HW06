# FR-10 Pre-Newman Execution Readiness & Provenance Report

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature Under Test:** FR-10 – Order Status & State Machine (Pool B)
- **Harness Architecture:** Per-Case Fixture Isolation with True Actor Provenance
- **Gate Status:** **`READY_FOR_FULL_NEWMAN`**

---

## 1. True Admin & User Actor Provenance

The test harness requires independent proof of actor identity based on authoritative seed definitions and decoded JWT payload claims (`role`), rather than inferring role status from endpoint acceptance.

| Actor | Credential Identity | Provisioning Source | Decoded JWT Role Claim | Repeat-Safe | Suitable Formal Actor? |
|---|---|---|:---:|:---:|:---:|
| **Administrator** | `adminEmail` (`admin@eshop.com`), password `Admin123!` | Seeded in SUT database (`id: 1`) on initialization | **`admin`** (`{"id":1,"role":"admin"}`) | **YES** | **YES (True Admin Fixture)** |
| **Customer A (Owner)** | `userAEmail` (`user@eshop.com`), password `User1234!` | Seeded in SUT database (`id: 7`) | **`user`** (`{"id":7,"role":"user"}`) | **YES** | **YES (Owner Customer)** |
| **Customer B (Non-Owner)** | `userBEmail` (`user_domain@eshop.com`), password `Domain1234!` | Repeat-Safe Setup Helper in Folder 00 (`POST /api/register`) | **`user`** (`{"id":45,"role":"user"}`) | **YES** | **YES (Non-Owner IDOR Probe)** |

### Elimination of Public Admin Self-Registration Dependency:
- In the e-commerce SRS and API contract, `POST /api/register` is strictly for standard customer account creation.
- Public client-side self-registration with `role: "admin"` is **NOT** contractually supported; in fact, the SUT backend sanitizes client-supplied roles and defaults all public registrations to `role = 'user'`.
- The unsupported setup helper `[SETUP] Register Admin User Account` has been **completely removed** from Folder 00 of the collection.
- The Admin harness derives `{{adminToken}}` exclusively from authenticating the true seeded administrator credential (`admin@eshop.com` / `Admin123!`).

---

## 2. Candidate SEC-03 (RBAC) Implementation Observation

- **Observation:** During Phase 2D.1A diagnostic probing, `PUT /api/admin/orders/:id/status` accepted an authenticated token belonging to a customer account (`role = 'user'`) without returning HTTP `403 Forbidden`.
- **Classification:** **`CANDIDATE SEC-03 IMPLEMENTATION OBSERVATION`** (Broken Function Level Authorization / Missing RBAC check on `/api/admin/*`).
- **Harness Separation:** This observation does **not** count as an Admin actor in our test harness. All formal Admin test cases strictly use `{{adminToken}}` (issued to `role = 'admin'`). Formal SEC-03 defect logging will be handled during dedicated security test execution.

---

## 3. Product Inventory Mechanics & Operational Capacity Proof

To resolve the operational capacity question for 44 isolated checkout fixtures, a focused inspection of the local SUT implementation was conducted:

- **Product API Catalog Exposure:** `GET /api/products` and `GET /api/products/:id` return `{ "id", "name", "price", "description", "imageUrl", "category_id" }`. **No stock or quantity counters are exposed by the public API.**
- **Product Model Schema:** The SQLite `products` table schema contains only `(id, name, price, description, imageUrl, category_id)`. **No stock column exists in the database model.**
- **Checkout Inventory Decrement:** The `POST /api/checkout` route records the order without decrementing any product stock counter.
- **Stock Validation:** No inventory threshold validation is performed during order creation.
- **Operational Capacity Conclusion:** **`OPERATIONALLY UNBOUNDED FOR CURRENT LOCAL HARNESS`**
- **Evidence Classification:** **`IMPLEMENTATION OBSERVATION – NOT TEST ORACLE`**
- **44-Checkout Operational Viability:** **`YES`** (Creating 44 isolated single-quantity order fixtures will not encounter stock depletion rejections).

---

## 4. Formal Actor Token & Variable Mapping

Machine-verified in `validate_fr10_actor_readiness.py`:
1. **Admin Operations:** All requests in `01 – Valid Admin Order Status Transitions` and `04 – Invalid Sequence Rejection (Admin)` strictly use `Authorization: Bearer {{adminToken}}`.
2. **Customer Owner Operations:** All requests in `02 – Valid Customer Order Cancellation` and `03 – Invalid Customer Cancellation Sequences` strictly use `Authorization: Bearer {{userAToken}}`.
3. **Non-Owner IDOR Probes:** All cross-user unauthorized cancellation probes in `05 – Domain Partitions & Security Boundaries` (`FR10-AI-033`, `FR10-HUM-002`) strictly use `Authorization: Bearer {{userBToken}}`.
4. **Zero Shared Order Fixtures:** All 44 formal checkout helpers populate unique per-case variables (`order_FR10_AI_001` .. `_041`, `order_FR10_HUM_001` .. `_005`).

---

## 5. Execution Gate Decision

### **`READY_FOR_FULL_NEWMAN`**

### Summary of Passed Readiness Gates:
- [x] **True Admin Identity Independently Proven:** `admin@eshop.com` verified with `role = 'admin'`.
- [x] **Zero Dependency on Public Admin Self-Registration:** Unsupported helper removed.
- [x] **Normal Roles Proven:** User A and User B verified with `role = 'user'`.
- [x] **Repeat-Safe Credential Workflow:** Verified across clean and repeated runs.
- [x] **Operational Inventory Capacity Defensibly Resolved:** Operationally unbounded based on schema inspection.
- [x] **Per-Case Fixture Isolation Validator:** **PASS** (10/10 checks).
- [x] **Actor Readiness Validator:** **PASS** (11/11 checks).
- [x] **Runtime `X-Student-Id` Evidence Captured:** Verified with Postman Console screenshot.
