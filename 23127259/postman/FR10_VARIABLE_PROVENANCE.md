# FR-10 Dynamic Variable & Fixture Provenance Inventory

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Status:** **PROVEN & FULLY DOCUMENTED**

---

## 1. Dynamic Variable Provenance Table

| Variable | Initial Environment Value | First Writer | HTTP Operation Producing Value | Consumers | Generated Before First Use? | Safe? |
|---|---|---|---|---|:---:|:---:|
| **`baseUrl`** | `http://localhost:3000` | Environment | None (Static Config) | All Collection Requests | YES | YES |
| **`studentId`** | `23127259` | Environment | None (Static Config) | Pre-request scripts & all `pm.sendRequest` | YES | YES |
| **`adminEmail`** | `admin@eshop.com` | Environment | None (Static Credential) | `[SETUP] Login Admin` | YES | YES |
| **`adminPassword`** | `Admin1234!` | Environment | None (Static Credential) | `[SETUP] Login Admin` | YES | YES |
| **`userAEmail`** | `user@eshop.com` | Environment | None (Static Credential) | `[SETUP] Login User A` | YES | YES |
| **`userAPassword`** | `User1234!` | Environment | None (Static Credential) | `[SETUP] Login User A` | YES | YES |
| **`userBEmail`** | `user_domain@eshop.com` | Environment | None (Static Credential) | `[SETUP] Login User B` | YES | YES |
| **`userBPassword`** | `Domain1234!` | Environment | None (Static Credential) | `[SETUP] Login User B` | YES | YES |
| **`adminToken`** | `""` (Empty) | `[SETUP] Login Admin` | `POST /api/auth/login` | Folders 01..10 Admin Requests & Verification GETs | YES | YES |
| **`userAToken`** | `""` (Empty) | `[SETUP] Login User A` | `POST /api/auth/login` | Setup Checkout Requests, Cancellation & Verification GETs | YES | YES |
| **`userBToken`** | `""` (Empty) | `[SETUP] Login User B` | `POST /api/auth/login` | Folder 07 Ownership Probes (`AI-033`, `AI-034`) | YES | YES |
| **`guestToken`** | Synthetic Invalid JWT | Environment | None (Synthetic) | Folder 06 RBAC (`AI-032`) | YES | YES |
| **`orderPendingId`** | `""` (Empty) | `[SETUP] Create Pending Fixture` | `POST /api/checkout` (by User A) | Folders 01, 02, 03, 05, 06, 08, HUM-005 | YES | YES |
| **`orderConfirmedId`**| `""` (Empty) | `[SETUP] Create Confirmed Fixture` | `POST /api/checkout` + `PUT /status` (Admin) | Folders 01, 02, 03, 07, HUM-004 | YES | YES |
| **`orderShippingId`** | `""` (Empty) | `[SETUP] Create Shipping Fixture` | `POST /api/checkout` + 2x `PUT /status` (Admin) | Folders 01, 03 | YES | YES |
| **`orderDeliveredId`**| `""` (Empty) | `[SETUP] Create Delivered Fixture` | `POST /api/checkout` + 3x `PUT /status` (Admin) | Folder 04 Terminal Delivered (`AI-017`..`020`) | YES | YES |
| **`orderCanceledId`** | `""` (Empty) | `[SETUP] Create Canceled Fixture` | `POST /api/checkout` + `PUT /cancel` (User A) | Folder 04 Terminal Canceled (`AI-021`..`024`) | YES | YES |
| **`orderId`** | `""` (Empty) | `[SETUP] Create Pending Fixture` | `POST /api/checkout` (by User A) | Sequential cases (`AI-004`, `AI-041`, `HUM-001`, `HUM-003`) | YES | YES |
| **`orderAId`** | `""` (Empty) | `[SETUP] Create Dual A Fixture` | `POST /api/checkout` (by User A) | `AI-033`, `HUM-002` | YES | YES |
| **`orderBId`** | `""` (Empty) | `[SETUP] Create Dual B Fixture` | `POST /api/checkout` (by User A) | `HUM-002` | YES | YES |

---

## 2. Order Fixture Provenance & Setup Request Architecture

Every order fixture is established in Folder 00 prior to test suite execution via API-visible requests:

```
[00 – Setup / Authentication & Fixture Helpers]
├── [SETUP] Login Admin (POST /api/auth/login) -> sets adminToken
├── [SETUP] Login User A (POST /api/auth/login) -> sets userAToken
├── [SETUP] Login User B (POST /api/auth/login) -> sets userBToken
├── [SETUP] Create Order Fixture - Pending (POST /api/checkout by User A) -> sets orderId, orderPendingId (State: pending)
├── [SETUP] Create Order Fixture - Confirmed (Step 1: POST /api/checkout by User A) -> sets orderConfirmedId
├── [SETUP] Create Order Fixture - Confirmed (Step 2: PUT /api/admin/orders/:id/status by Admin) -> transitions to confirmed
├── [SETUP] Create Order Fixture - Shipping (Step 1: POST /api/checkout by User A) -> sets orderShippingId
├── [SETUP] Create Order Fixture - Shipping (Step 2: PUT /api/admin/orders/:id/status by Admin -> confirmed)
├── [SETUP] Create Order Fixture - Shipping (Step 3: PUT /api/admin/orders/:id/status by Admin -> shipping)
├── [SETUP] Create Order Fixture - Delivered (Step 1: POST /api/checkout by User A) -> sets orderDeliveredId
├── [SETUP] Create Order Fixture - Delivered (Step 2: PUT /api/admin/orders/:id/status by Admin -> confirmed)
├── [SETUP] Create Order Fixture - Delivered (Step 3: PUT /api/admin/orders/:id/status by Admin -> shipping)
├── [SETUP] Create Order Fixture - Delivered (Step 4: PUT /api/admin/orders/:id/status by Admin -> delivered)
├── [SETUP] Create Order Fixture - Canceled (Step 1: POST /api/checkout by User A) -> sets orderCanceledId
├── [SETUP] Create Order Fixture - Canceled (Step 2: PUT /api/orders/:id/cancel by User A) -> transitions to canceled
├── [SETUP] Create Order Fixture - Dual A (POST /api/checkout by User A) -> sets orderAId
└── [SETUP] Create Order Fixture - Dual B (POST /api/checkout by User A) -> sets orderBId
```
