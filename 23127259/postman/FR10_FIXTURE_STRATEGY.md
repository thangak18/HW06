# FR-10 State Fixture Allocation & Isolation Strategy

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)

---

## 1. Overview & Core Invariants

Feature FR-10 is inherently **stateful**. State transitions permanently mutate order entities in the database. To achieve 100% deterministic test execution across repeated collection runs and Newman CI executions without brittle inter-test dependencies, this fixture strategy defines:
1. **Per-Test / Per-Family Independent Fixtures:** No formal mutation test relies on the residual state left by a preceding test.
2. **API-Visible Setup Mechanisms Only:** No direct database hacking or out-of-band manipulation. Setup is performed exclusively via documented API calls (`POST /api/auth/login`, `POST /api/orders`, `POST /api/checkout`, or dynamic deterministic seeded fixtures).
3. **Dynamic Variable Binding:** Tokens (`adminToken`, `userAToken`, `userBToken`) and order identifiers (`orderId`, `orderAId`, `orderBId`) are captured dynamically at runtime and passed via environment variables.

---

## 2. Authentication & Credential Allocation Strategy

| Actor Role | Postman Variable | Seed Email | Seed Password | Purpose / Scope |
|---|---|---|---|---|
| **System Administrator** | `adminToken` | `admin@eshop.com` | `Admin1234!` | Admin status updates (`PUT /api/admin/orders/:id/status`) & authorized persistence checks |
| **Customer A (Owner)** | `userAToken` | `user@eshop.com` | `User1234!` | Primary customer order creation, legitimate cancellations (`PUT /api/orders/:id/cancel`) |
| **Customer B (Non-Owner)** | `userBToken` | `user_domain@eshop.com` | `Domain1234!` | Cross-user ownership and multi-tenant authorization probes (`FR10-AI-033`, `034`) |

---

## 3. Order Fixture Lifecycle Families

| Fixture Family | Initial State | Creation Sequence | Target Formal Tests |
|---|---|---|---|
| **Family A: Fresh Pending** | `pending` | Created by User A (`POST /api/orders` / checkout) | `001`, `005`, `007`, `009`, `010`, `025`..`030`, `032`, `035`..`038`, `041`, `HUM-001`, `HUM-005` |
| **Family B: Pre-Shipment Confirmed** | `confirmed` | Created in `pending` $ightarrow$ Admin transitions `pending` $ightarrow$ `confirmed` | `002`, `006`, `008`, `011`, `013`, `034`, `HUM-004` |
| **Family C: In-Transit Shipping** | `shipping` | Created in `pending` $ightarrow$ Admin `pending` $ightarrow$ `confirmed` $ightarrow$ `shipping` | `003`, `014`, `015`, `016`, `HUM-003` |
| **Family D: Terminal Delivered** | `delivered` | Created in `pending` $ightarrow$ Admin linear progression to `delivered` | `017` .. `020` |
| **Family E: Terminal Canceled** | `canceled` | Created in `pending` $ightarrow$ Admin/User cancels order to `canceled` | `021` .. `024` |
| **Family F: Dual-Entity Isolation** | 2x `pending` | Create Order A and Order B independently | `HUM-002` |
| **Family G: Synthetic / Non-Existent IDs** | N/A | Use synthetic IDs (`999999`, `"not-an-id"`, `"1' OR '1'='1"`) | `039`, `040`, `042` |

---

## 4. Execution-Order Determinism & Isolation Rules

1. **Folder Execution Order:** Collection folders are ordered logically (00 Setup $ightarrow$ 01 Valid Forward $ightarrow$ 02 Cancellation $ightarrow$ ... $ightarrow$ 10 Human Extensions).
2. **Read-After-Write Verification:** Every state transition test performs persistence verification using `GET /api/orders/:id` with an authorized token (`adminToken` or `userAToken`).
3. **No Cross-Test Contamination:** Each folder or test block initializes its required target order ID before executing the mutation under test.
