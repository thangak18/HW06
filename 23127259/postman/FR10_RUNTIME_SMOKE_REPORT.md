# FR-10 Minimal Runtime Smoke & Readiness Report (Corrected)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature Under Test:** FR-10 – Order Status & State Machine (Pool B)
- **Harness Architecture:** Per-Case Fixture Isolation with Fail-Fast Extraction
- **Gate Status:** **`READY_FOR_FULL_NEWMAN`**

---

## 1. Corrected Network Traffic Accounting

During the Phase 2D.1A runtime smoke investigation (INT-040), network requests were executed across diagnostic probes, route discovery, and the final controlled smoke flow:

| Category | HTTP Requests | Details / Operations |
|---|:---:|---|
| **Base Reachability Check** | `1` | `curl -I http://localhost:3000/api/auth/login` (Returned 404; discovered route prefix) |
| **Auth Route Diagnostic Probes** | `7` | Probed `/api/auth/login` (3x 404), probed `/api/login` (401 admin, 200 user, 401 domain), checked 403 lockout response body |
| **Account Provisioning Probes** | `4` | `POST /api/register` for admin (ID 44), user B (ID 45), fresh `admin_fr10` (ID 46), and verified login role |
| **Product Discovery Probes** | `2` | `GET /api/products` (list of 7 products), `GET /api/products/1` (detail inspection) |
| **Checkout ID Path Discovery** | `2` | `POST /api/checkout` (observed `body.orderId: 1`), validated fail-fast extraction |
| **Final Controlled Smoke Flow** | `8` | 1x Reachability curl, 3x Login (`admin`, `userA`, `userB`), 1x Product discovery, 1x Checkout (`smokeOrderId: 2`), 1x Initial GET (`pending`), 1x Admin update (`confirmed`), 1x Persistence GET (`confirmed`) |
| **Postman UI / Console Captures** | `4` | Browser/CDP driven requests inside Postman UI to capture runtime console evidence |
| **TOTAL INT-040 HTTP TRAFFIC** | **`28`** | **Total diagnostic, discovery, and smoke traffic executed during INT-040** |
| **FINAL CONTROLLED SMOKE FLOW** | **`8`** | **Minimal repeatable smoke flow budget** |
| **FORMAL TEST CASES EXECUTED** | **`0`** | **Formal suite untouched; zero formal test pollution** |

> *(Correction Note: The previous report's "Total HTTP Requests Executed = 8" was an under-reporting that reflected only the final successful sequence. Total interaction network activity is now accurately audited as 28 requests).*

---

## 2. Product Inventory Capacity & Full-Run Strategy

- **Discovery Endpoint:** `GET /api/products` (and `GET /api/products/:id`)
- **Selected `fixtureProductId`:** `1` (`iPhone 15 Pro Max`, price `30,000,000`, `category_id: 1`)
- **Stock Quantity Field Exposed by API:** **NO** (The public catalog returns `id`, `name`, `price`, `description`, `imageUrl`, `category_id`; no stock or inventory counters are exposed).
- **Observed Inventory Capacity:** **`UNKNOWN`**
- **44-Checkout Capacity Mathematically Proven via API:** **`NO`** (A single successful smoke checkout validates route mechanics, but cannot prove stock capacity for 44 creations without visible counters).
- **Defensible Full-Run Strategy:**
  1. All 44 formal checkout helpers request minimal item quantity (`quantity: 1`).
  2. `fixtureProductId` is exposed as an environment variable (default `1`).
  3. If product 1 encounters inventory depletion in any environment, `fixtureProductId` can be overridden to any alternate seeded product (`2`, `3`, `4`, `5`).
  4. SUT runtime behavior does not reject repeated checkouts on product 1.

---

## 3. Account Provisioning & Role Contract Audit

| Actor | Target Variable | Provisioning Source | Registration Needed | Repeat-Safe | Role Basis / Contract |
|---|---|---|:---:|:---:|---|
| **Administrator** | `adminEmail` (`admin_fr10@eshop.com` / `admin@eshop.com`) | Dedicated / Seeded Credential | Idempotent Setup Helper in Folder 00 | **YES** | Pre-seeded admin or dedicated test credential; SUT status update route accepts valid JWT bearer token. Public self-registration does NOT contractually grant admin role. |
| **Customer A (Owner)** | `userAEmail` (`user@eshop.com`) | Seeded Baseline Customer | No (Pre-seeded in DB) | **YES** | Standard seeded customer (`role = 'user'`), password `User1234!`. |
| **Customer B (Non-Owner)** | `userBEmail` (`user_domain@eshop.com`) | Dedicated Secondary Customer | Idempotent Setup Helper in Folder 00 | **YES** | Standard customer (`role = 'customer'/'user'`), password `Domain1234!`. Used for IDOR isolation (`FR10-AI-033`, `FR10-HUM-002`). |

### Repeat-Safe Provisioning Details:
- The setup helpers `[SETUP] Register Admin User Account` and `[SETUP] Register User B Account` in Folder 00 issue `POST /api/register` with test assertions accepting `[200, 201, 400, 409]`.
- On initial run, accounts are provisioned (200/201). On subsequent runs, existing accounts are handled gracefully without aborting.
- Subsequent `POST /api/login` requests deterministically authenticate and extract valid JWTs into `adminToken`, `userAToken`, and `userBToken`.

---

## 4. Route & Response-Shape Compatibility (Harness Repairs)

1. **Active Login Route (`HARNESS-REP-01`):**
   - Active SUT route: `POST /api/login`
   - Historical docs / assignment notes: `POST /api/auth/login`
   - Resolution: Collection updated to `{{baseUrl}}/api/login` to match active SUT routing.
2. **Checkout Response Extraction (`HARNESS-REP-03`):**
   - Observed response body: `{"message": "Checkout successful", "orderId": 2}`
   - Resolution: Fail-fast extraction updated to `const id = body.orderId ?? body.id ?? body.order?.id ?? body.data?.id;` across all 44 checkout helpers. Fallback ID `'1'` strictly eliminated.
3. **Environment Alignment (`HARNESS-REP-04`):**
   - Added `fixtureProductId: "1"` to `FR10-local.postman_environment.json`.

---

## 5. X-Student-Id Runtime Evidence

- **Header Transmitted:** `X-Student-Id: 23127259`
- **Postman Console Screenshot:** [`23127259/evidence/fr10/FR10-postman-console-x-student-id-smoke.png`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/fr10/FR10-postman-console-x-student-id-smoke.png)
- **Hostname Visible:** `localhost:3000`
- **Request URL Visible:** `http://localhost:3000/api/login`

---

## 6. Execution Gate Decision

### **`READY_FOR_FULL_NEWMAN`**

### Comprehensive Readiness Rationale:
1. **SUT Health:** Responsive at `http://localhost:3000`.
2. **Auth & Tokens:** All 3 actor roles (Admin, User A, User B) authenticate deterministically with repeat-safe credentials.
3. **Per-Case Isolation:** All 44 checkout fixtures are strictly co-located and isolated to unique test variables (`order_FR10_AI_001` .. `_041`, `order_FR10_HUM_001` .. `_005`).
4. **Fail-Fast Extraction:** Zero fallback order IDs exist; all checkouts extract real runtime IDs from `body.orderId` and throw on failure.
5. **State Machine Mechanics:** Verified `pending` initial state $\rightarrow$ Admin `confirmed` status transition $\rightarrow$ `confirmed` read-after-write persistence GET.
6. **Header Attribution:** `X-Student-Id: 23127259` transmitted across all collection requests and script calls.
7. **Static Integrity:** `validate_fr10_fixture_isolation.py` passes 10/10 gates (100% compliant).
8. **Formal Integrity:** Exactly 46 formal cases (41 AI-derived + 5 Human Extensions; raw draft hash `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc` immutable).
