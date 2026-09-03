# FR-10 Test Execution Traceability Matrix

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Total Formal Executable Cases:** `46`
- **Total Excluded Raw Cases:** `1` (`FR10-AI-012`)

---

## 1. Executable Test Cases Traceability Table

| Formal ID | Provenance | Human Audit Verdict | Correction Applied | Postman Folder | Primary Request | Setup Helpers | Persistence Oracle | Formal Executable? |
|---|---|:---:|---|---|---|---|---|:---:|
| `FR10-AI-001` | AI-Generated | VALID | NONE | `01` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `confirmed` | **YES** |
| `FR10-AI-002` | AI-Generated | VALID | NONE | `01` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `shipping` | **YES** |
| `FR10-AI-003` | AI-Generated | VALID | NONE | `01` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `delivered` | **YES** |
| `FR10-AI-004` | AI-Generated | VALID | NONE | `01` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `delivered` | **YES** |
| `FR10-AI-005` | AI-Generated | VALID | NONE | `02` | `PUT /api/orders/{{orderId}}/cancel` | Login Admin, Login User A, Create Order Fixture | GET /api/orders/:id -> `canceled` | **YES** |
| `FR10-AI-006` | AI-Generated | VALID | NONE | `02` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `canceled` | **YES (Run04 canonical)** |
| `FR10-AI-007` | AI-Generated | VALID | NONE | `02` | `PUT /api/orders/{{orderId}}/cancel` | Login Admin, Login User A, Create Order Fixture, advance to confirmed | GET /api/orders/:id -> `canceled` | **YES (Run04 canonical)** |
| `FR10-AI-008` | AI-Generated | VALID | NONE | `02` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `canceled` | **YES** |
| `FR10-AI-009` | AI-Generated | VALID | NONE | `03` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-010` | AI-Generated | VALID | NONE | `03` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-011` | AI-Generated | VALID | NONE | `03` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `confirmed` | **YES** |
| `FR10-AI-013` | AI-Generated | VALID | NONE | `03` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `confirmed` | **YES** |
| `FR10-AI-014` | AI-Generated | VALID | NONE | `03` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `shipping` | **YES** |
| `FR10-AI-015` | AI-Generated | VALID | NONE | `03` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `shipping` | **YES** |
| `FR10-AI-016` | AI-Generated | VALID | NONE | `03` | `PUT /api/orders/{{orderId}}/cancel` | Login Admin, Login User A, Create Order Fixture | GET /api/orders/:id -> `shipping` | **YES** |
| `FR10-AI-017` | AI-Generated | VALID | NONE | `04` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `delivered` | **YES** |
| `FR10-AI-018` | AI-Generated | VALID | NONE | `04` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `delivered` | **YES** |
| `FR10-AI-019` | AI-Generated | VALID | NONE | `04` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `delivered` | **YES** |
| `FR10-AI-020` | AI-Generated | VALID | NONE | `04` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `delivered` | **YES** |
| `FR10-AI-021` | AI-Generated | VALID | NONE | `04` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `canceled` | **YES** |
| `FR10-AI-022` | AI-Generated | VALID | NONE | `04` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `canceled` | **YES** |
| `FR10-AI-023` | AI-Generated | VALID | NONE | `04` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `canceled` | **YES** |
| `FR10-AI-024` | AI-Generated | VALID | NONE | `04` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `canceled` | **YES** |
| `FR10-AI-025` | AI-Generated | VALID | NONE | `05` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-026` | AI-Generated | VALID | NONE | `05` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-027` | AI-Generated | VALID | NONE | `05` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-028` | AI-Generated | VALID | NONE | `05` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture, Tamper JWT | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-029` | AI-Generated | VALID | NONE | `05` | `PUT /api/orders/{{orderId}}/cancel` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-030` | AI-Generated | VALID | NONE | `06` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Login User A, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-031` | AI-Generated | VALID | NONE | `06` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Login User A, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-032` | AI-Generated | VALID | NONE | `06` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Login User A, Create Order Fixture, Advance to confirmed | GET /api/orders/:id -> `confirmed` | **YES** |
| `FR10-AI-033` | AI-Generated | INCOMPLETE | Refined as Business Auth / Accept any 4xx | `07` | `PUT /api/orders/{{orderAId}}/cancel` | Login Admin, Login User B, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-034` | AI-Generated | INCOMPLETE | Refined as Business Auth / Accept any 4xx | `07` | `PUT /api/orders/{{orderAId}}/cancel` | Login Admin, Login User B, Create Order Fixture | GET /api/orders/:id -> `confirmed` | **YES** |
| `FR10-AI-035` | AI-Generated | VALID | NONE | `08` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-036` | AI-Generated | VALID | NONE | `08` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-037` | AI-Generated | VALID | NONE | `08` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-038` | AI-Generated | VALID | NONE | `08` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |
| `FR10-AI-039` | AI-Generated | VALID | NONE | `08` | `PUT /api/admin/orders/999999/status` | Login Admin | N/A | **YES** |
| `FR10-AI-040` | AI-Generated | INCOMPLETE | Refined as Input Robustness / Accept safe 4xx | `08` | `PUT /api/admin/orders/not-an-id/status` | Login Admin | N/A | **YES** |
| `FR10-AI-041` | AI-Generated | VALID | NONE | `09` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `confirmed` | **YES** |
| `FR10-AI-042` | AI-Generated | VALID | NONE | `09` | `PUT /api/admin/orders/1' OR '1'='1/status` | Login Admin | N/A | **YES** |
| `FR10-HUM-001` | Student Human Extension | VALID | Student Formalization from Gap Analysis | `10` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `confirmed` | **YES** |
| `FR10-HUM-002` | Student Human Extension | VALID | Student Formalization from Gap Analysis | `10` | `PUT /api/admin/orders/{{orderAId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `Order A: confirmed, Order B: pending` | **YES** |
| `FR10-HUM-003` | Student Human Extension | VALID | Student Formalization from Gap Analysis | `10` | `PUT /api/orders/{{orderId}}/cancel` | Login Admin, Login User A, Create Order Fixture | GET /api/orders/:id -> `delivered` | **YES** |
| `FR10-HUM-004` | Student Human Extension | VALID | Student Formalization from Gap Analysis | `10` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `confirmed` | **YES** |
| `FR10-HUM-005` | Student Human Extension | VALID | Student Formalization from Gap Analysis | `10` | `PUT /api/admin/orders/{{orderId}}/status` | Login Admin, Create Order Fixture | GET /api/orders/:id -> `pending` | **YES** |

---

## 2. Excluded Raw Test Cases Table

| Formal ID | Provenance | Human Audit Verdict | Correction Applied | Postman Folder | Primary Request | Setup Helpers | Persistence Oracle | Formal Executable? |
|---|---|:---:|---|---|---|---|---|:---:|
| `FR10-AI-012` | Raw AI Generated | **INVALID** | REJECTED (Confounded Dimensions) | N/A | N/A | N/A | N/A | **NO (REJECTED)** |
