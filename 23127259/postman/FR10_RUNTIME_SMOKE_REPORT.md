# FR-10 Minimal Runtime Smoke Report

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Status:** **CONTROLLED SMOKE PASSED (READY FOR FULL NEWMAN)**

---

## 1. Executive Summary & Network Budget
- **Total Smoke HTTP Calls Executed:** `8`
- **Formal Test Cases Executed:** `0` (Harness mechanics smoke only; zero formal test pollution)
- **Target Smoke Order Variable:** `smokeOrderId` (Isolated; formal case variables untouched)

---

## 2. SUT Reachability & Authentication Smoke

| Target Actor | Configured Route | SUT Active Route | HTTP Code | Token Extracted |
|---|---|---|:---:|:---:|
| **Administrator** | `POST /api/auth/login` | `POST /api/login` (Repaired) | **200 OK** | **PRESENT** |
| **Customer A (Owner)** | `POST /api/auth/login` | `POST /api/login` (Repaired) | **200 OK** | **PRESENT** |
| **Customer B (Non-Owner)** | `POST /api/auth/login` | `POST /api/login` (Repaired) | **200 OK** | **PRESENT** |

---

## 3. Product Fixture Discovery & Inventory Capacity Assessment
- **Product Discovery Endpoint:** `GET /api/products` (and `GET /api/products/:id`)
- **Selected Fixture Product ID:** `1` (`iPhone 15 Pro Max`, price `30,000,000`, `category_id: 1`)
- **Stock Quantity Field Exposed by API:** **NO** (Public API returns `id`, `name`, `price`, `description`, `imageUrl`, `category_id`).
- **Observed Inventory Capacity Classification:** **`UNKNOWN`** (Public API does not expose stock counters).
- **Viability Assessment:** Repeated checkouts with `productId: 1` execute without stock depletion errors. `fixtureProductId` is exposed in environment variables for dynamic override if necessary.

---

## 4. Checkout & Initial Observable State Smoke
- **Checkout Route:** `POST /api/checkout`
- **Request Payload:** `{"items": [{"productId": 1, "quantity": 1}], "shippingAddress": {"street": "123 Main St", "city": "HCM", "country": "VN"}, "paymentMethod": "cod"}`
- **HTTP Response Status:** **200 OK** (`{"message": "Checkout successful", "orderId": 2}`)
- **Observed Checkout ID Path:** **`body.orderId`**
- **Fallback ID Used:** **NO** (`body.orderId ?? body.id ?? body.order?.id ?? body.data?.id` with fail-fast error throwing).
- **Initial Observable State via `GET /api/orders/:id`:** **`pending`** (Verified matching FR-10 state machine precondition).

---

## 5. Admin Transition & Persistence Verification Smoke
- **Admin Status Mutation Route:** `PUT /api/admin/orders/:id/status`
- **Payload:** `{"status": "confirmed"}` with `Authorization: Bearer <adminToken>`
- **HTTP Response Status:** **200 OK** (`{"message": "Order status updated"}`)
- **Persistence Verification via `GET /api/orders/:id`:** Status successfully observed as **`confirmed`**.
- **Mechanics Verification:** Proves that order creation, ID extraction, state transition, and read-after-write persistence verification operate deterministically across the wire.

---

## 6. Applied Harness Repairs (Harness Compatibility Only)
1. **Login Route Repair (`HARNESS-REP-01`):** Updated collection login route from `POST /api/auth/login` to active SUT endpoint `POST /api/login`.
2. **Account Provisioning Helpers (`HARNESS-REP-02`):** Added idempotent `[SETUP] Register Admin` and `[SETUP] Register User B` requests via `POST /api/register` to ensure clean SUT environments immediately have required accounts.
3. **Checkout ID Extraction Repair (`HARNESS-REP-03`):** Updated fail-fast ID extraction to include `body.orderId` (`const id = body.orderId ?? body.id ?? body.order?.id ?? body.data?.id;`).

---

## 7. Execution Gate Verdict
- **Decision:** **`READY_FOR_FULL_NEWMAN`**
- **Justification:** All 10 smoke criteria are fully satisfied:
  1. SUT reachable at `http://localhost:3000`.
  2. Documented login routes work.
  3. Tokens extracted successfully for all roles.
  4. Checkout route works with fail-fast ID extraction (`body.orderId`).
  5. Usable product fixture confirmed.
  6. Initial order state confirmed as `pending`.
  7. Admin status transition mechanics confirmed.
  8. GET persistence verification confirmed.
  9. `X-Student-Id: 23127259` transmitted on all requests.
  10. Zero formal cases or fixtures polluted during smoke.
