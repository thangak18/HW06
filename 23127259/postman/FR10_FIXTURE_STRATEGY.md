# FR-10 State Fixture Allocation & Isolation Strategy (Execution-Ready)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)

---

## 1. Overview & Core Invariants

Feature FR-10 is inherently **stateful**. State transitions permanently mutate order entities in the database. To achieve 100% deterministic test execution across repeated collection runs and Newman CI executions without brittle inter-test dependencies, this fixture strategy defines:
1. **Per-Family Dedicated Fixture Variables:** Every test family operates on a dedicated fixture variable established during Setup in Folder 00 (`orderPendingId`, `orderConfirmedId`, `orderShippingId`, `orderDeliveredId`, `orderCanceledId`, `orderAId`, `orderBId`, and sequential `orderId`).
2. **API-Visible Setup Mechanics Only:** No direct database hacking or out-of-band manipulation. Setup is performed exclusively via documented API calls (`POST /api/auth/login`, `POST /api/checkout`, `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel`).
3. **Dynamic Variable Binding:** Tokens and order identifiers are captured dynamically from responses and passed via environment variables.

---

## 2. Authentication & Credential Allocation Strategy

| Actor Role | Postman Variable | Seed Email | Seed Password | Purpose / Scope |
|---|---|---|---|---|
| **System Administrator** | `adminToken` | `admin@eshop.com` | `Admin1234!` | Admin status updates (`PUT /api/admin/orders/:id/status`) & authorized persistence checks |
| **Customer A (Owner)** | `userAToken` | `user@eshop.com` | `User1234!` | Order fixture creation (`POST /api/checkout`), legitimate cancellations (`PUT /api/orders/:id/cancel`) |
| **Customer B (Non-Owner)** | `userBToken` | `user_domain@eshop.com` | `Domain1234!` | Cross-user ownership probes (`FR10-AI-033`, `034`) |

---

## 3. Order Fixture Lifecycle Families & Variables

| Fixture Family | Postman Variable | Target State | Creation & Transition Sequence | Consuming Formal Tests |
|---|---|---|---|---|
| **Family A: Fresh Pending** | `orderPendingId` | `pending` | Created by User A (`POST /api/checkout`) | `001`, `005`, `007`, `009`, `010`, `025`..`030`, `032`, `035`..`038`, `HUM-005` |
| **Family B: Confirmed** | `orderConfirmedId` | `confirmed` | Created by User A $ightarrow$ Admin transitions `pending` $ightarrow$ `confirmed` | `002`, `006`, `008`, `011`, `013`, `034`, `HUM-004` |
| **Family C: In-Transit Shipping** | `orderShippingId` | `shipping` | Created by User A $ightarrow$ Admin `pending` $ightarrow$ `confirmed` $ightarrow$ `shipping` | `003`, `014`, `015`, `016` |
| **Family D: Terminal Delivered** | `orderDeliveredId` | `delivered` | Created by User A $ightarrow$ Admin linear progression to `delivered` | `017` .. `020` |
| **Family E: Terminal Canceled** | `orderCanceledId` | `canceled` | Created by User A $ightarrow$ User A cancels order to `canceled` | `021` .. `024` |
| **Family F: Dual-Entity Isolation** | `orderAId`, `orderBId` | 2x `pending` | Created independently via User A checkout | `HUM-002`, `AI-033` |
| **Family G: Multi-Step Sequential** | `orderId` | `pending` | Fresh order for multi-step continuity sequences | `AI-004`, `AI-041`, `HUM-001`, `HUM-003` |
| **Family H: Synthetic IDs** | Literals | N/A | Synthetic IDs (`999999`, `"not-an-id"`, `"1' OR '1'='1"`) | `039`, `040`, `042` |

---

## 4. Cross-Test State Isolation Matrix

| Fixture Variable | Initial Setup Actor | Consuming Formal Cases | Mutated In-Place? | Isolation Safety Guarantee |
|---|---|---|:---:|---|
| `orderPendingId` | User A / Checkout | Folders 01..03, 05, 06, 08, HUM-005 | Probed / Rejected | Probes and invalid transitions leave state unchanged at `pending`. |
| `orderConfirmedId`| User A + Admin | Folders 01..03, 07, HUM-004 | Probed / Rejected | Probes leave state unchanged at `confirmed`. |
| `orderShippingId` | User A + Admin | Folders 01, 03 | Probed / Rejected | Probes leave state unchanged at `shipping`. |
| `orderDeliveredId`| User A + Admin | Folder 04 (`017`..`020`) | Probed / Rejected | Terminal state is permanently immutable. |
| `orderCanceledId` | User A + User A | Folder 04 (`021`..`024`) | Probed / Rejected | Terminal state is permanently immutable. |
| `orderAId` | User A (Owner) | `FR10-AI-033`, `FR10-HUM-002` | Scoped | Customer B probe is rejected; Order A remains `pending` for `HUM-002`. |
| `orderBId` | User A (Owner) | `FR10-HUM-002` | No (Verification Only) | Independent unmutated control order in dual-entity test. |
| `orderId` | User A (Owner) | `AI-004`, `AI-041`, `HUM-001`, `HUM-003` | Yes (Sequential) | Each multi-step case executes its own dedicated lifecycle progression. |
