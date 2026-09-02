# FR-10 Canonical Test Provenance Map

- **Stage:** Phase 2D.1D.2 – Canonical Test Provenance Reconstruction
- **Authoritative Provenance Sources:**
  - **Level 1 (Normative Requirements):** `docs/assignment-notes.md`, `testcases/FR10_REQUIREMENT_ANALYSIS.md`, `docs/ORACLE_POLICY.md`
  - **Level 2 (Immutable AI Generation):** `testcases/FR10_AI_DRAFT.md` (SHA: `303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc`)
  - **Level 3 (Human Audit Provenance):** `testcases/FR10_HUMAN_AUDIT_CORRECTIONS.md`, `ai/TC_AUDIT_FR10.md`
  - **Level 4 (Human Extensions):** `testcases/FR10_HUMAN_TEST_CASES.md`, `testcases/FR10_HUMAN_EXTENSION_DESIGN.md`

---

## 1. Overview & Source Hierarchy Rules

In accordance with strict specification-first testing principles:
1. **Level 1 (Normative Product Sources):** The SRS, API Specification, and Assignment Rules define true system behavior and oracle boundaries.
2. **Level 2 (Raw AI Provenance):** `FR10_AI_DRAFT.md` is frozen and immutable. It determines what each AI test ID originally meant.
3. **Level 3 (Human Audit Decisions):** `FR10_HUMAN_AUDIT_CORRECTIONS.md` governs audit classifications (`VALID`, `INVALID`, `INCOMPLETE`). Only explicit documented corrections modify raw cases.
4. **Level 4 (Human Extensions):** `FR10_HUMAN_TEST_CASES.md` defines `FR10-HUM-001` through `FR10-HUM-005`.
5. **Derived Files Rule:** Derived files (`FR10_FINAL_EXECUTABLE_SUITE.md`, Postman collections) MUST NOT override Levels 1–4.

---

## 2. Canonical AI Case Mapping (FR10-AI-001 through FR10-AI-042)

| ID | Title / Technique | Actor | Initial State | Method | Endpoint | Body / Input | Expected Semantic Outcome | Expected HTTP Status | Audit Disposition |
|---|---|---|---|:---:|---|---|---|---|:---:|
| FR10-AI-001 | Valid Admin Forward Transition: Pending to Confirmed | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Order successfully advances from `pendin | `200 OK` | **VALID AS-IS** |
| FR10-AI-002 | Valid Admin Forward Transition: Confirmed to Shipping | System Administrator | confirmed | PUT | `/api/admin/orders/:id/status` | `{     "status": "shipping"   }` | Order successfully transitions from `con | `200 OK` | **VALID AS-IS** |
| FR10-AI-003 | Valid Admin Forward Transition: Shipping to Delivered | System Administrator | shipping | PUT | `/api/admin/orders/:id/status` | `{     "status": "delivered"   }` | Order successfully reaches terminal `del | `200 OK` | **VALID AS-IS** |
| FR10-AI-004 | Complete Happy-Path Order Lifecycle Continuity Sequence | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{ "status": "confirmed" }` | Complete linear progression succeeds uni | `200 OK` | **VALID AS-IS** |
| FR10-AI-005 | Valid Customer Self-Cancellation on Pending Order | Order Owner Customer | pending | PUT | `/api/orders/:id/cancel` | `Empty` | Order is successfully canceled by custom | `200 OK` | **VALID AS-IS** |
| FR10-AI-006 | Valid Admin Cancellation on Pending Order | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "canceled"   }` | Order is successfully canceled by admini | `200 OK` | **VALID AS-IS** |
| FR10-AI-007 | Valid Customer Self-Cancellation on Confirmed Order | Order Owner Customer | confirmed | PUT | `/api/orders/:id/cancel` | `Empty` | Customer successfully cancels order in ` | `200 OK` | **VALID AS-IS** |
| FR10-AI-008 | Valid Admin Cancellation on Confirmed Order | System Administrator | confirmed | PUT | `/api/admin/orders/:id/status` | `{     "status": "canceled"   }` | Administrator successfully voids confirm | `200 OK` | **VALID AS-IS** |
| FR10-AI-009 | Invalid Forward Skip Transition: Pending Directly to Shipping | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "shipping"   }` | Transition rejected; intermediate `confi | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-010 | Invalid Forward Skip Transition: Pending Directly to Delivered | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "delivered"   }` | Transition rejected; order cannot bypass | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-011 | Invalid Forward Skip Transition: Confirmed Directly to Delivered | System Administrator | confirmed | PUT | `/api/admin/orders/:id/status` | `{     "status": "delivered"   }` | Transition rejected; intermediate `shipp | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-012 | Invalid Forward Skip Attempt by Normal Customer Token | Normal Customer (`ro | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "shipping"   }` | Request rejected due to unauthorized rol | `NOT SPECIFIED – ERROR / NON-SU` | **REJECTED** |
| FR10-AI-013 | Invalid Backward State Regression: Confirmed to Pending | System Administrator | confirmed | PUT | `/api/admin/orders/:id/status` | `{     "status": "pending"   }` | Backward transition rejected; confirmed  | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-014 | Invalid Backward State Regression: Shipping to Confirmed | System Administrator | shipping | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Backward transition rejected; in-transit | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-015 | Invalid Backward State Regression: Shipping to Pending | System Administrator | shipping | PUT | `/api/admin/orders/:id/status` | `{     "status": "pending"   }` | Multi-stage regression rejected; dispatc | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-016 | Customer Prohibited In-Transit Cancellation Attempt | Order Owner Customer | shipping | PUT | `/api/orders/:id/cancel` | `Empty` | Cancellation rejected; customer is barre | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-017 | Invalid Terminal State Mutation: Delivered to Pending | System Administrator | delivered | PUT | `/api/admin/orders/:id/status` | `{     "status": "pending"   }` | Mutation rejected; completed order in te | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-018 | Invalid Terminal State Mutation: Delivered to Confirmed | System Administrator | delivered | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Mutation rejected; fulfilled order canno | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-019 | Invalid Terminal State Mutation: Delivered to Shipping | System Administrator | delivered | PUT | `/api/admin/orders/:id/status` | `{     "status": "shipping"   }` | Mutation rejected; delivered package can | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-020 | Invalid Terminal State Mutation: Delivered to Canceled | System Administrator | delivered | PUT | `/api/admin/orders/:id/status` | `{     "status": "canceled"   }` | Mutation rejected; completed order canno | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-021 | Invalid Terminal State Mutation: Canceled to Pending | System Administrator | canceled | PUT | `/api/admin/orders/:id/status` | `{     "status": "pending"   }` | Mutation rejected; voided/canceled order | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-022 | Invalid Terminal State Mutation: Canceled to Confirmed | System Administrator | canceled | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Mutation rejected; canceled order cannot | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-023 | Invalid Terminal State Mutation: Canceled to Shipping | System Administrator | canceled | PUT | `/api/admin/orders/:id/status` | `{     "status": "shipping"   }` | Mutation rejected; canceled order cannot | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-024 | Invalid Terminal State Mutation: Canceled to Delivered | System Administrator | canceled | PUT | `/api/admin/orders/:id/status` | `{     "status": "delivered"   }` | Mutation rejected; canceled order cannot | `NOT SPECIFIED – ERROR / NON-SU` | **VALID AS-IS** |
| FR10-AI-025 | SEC-02: Missing Authorization Header on Valid Admin Status Transition | Unauthenticated Clie | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Request rejected due to missing authenti | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-026 | SEC-02: Malformed Authorization Header on Valid Admin Status Transition | Unauthenticated Clie | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Request rejected due to malformed authen | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-027 | SEC-02: Syntactically Invalid / Random JWT on Valid Admin Transition | Unauthenticated Atta | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Request rejected due to invalid token si | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-028 | SEC-02: Cryptographically Tampered JWT on Valid Admin Transition | Attacker attempting  | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Request rejected due to cryptographic si | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-029 | SEC-02: Missing Authorization Header on Customer Cancellation Endpoint | Unauthenticated Clie | pending | PUT | `/api/orders/:id/cancel` | `Empty` | Request rejected because cancellation re | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-030 | SEC-03: Normal Customer Role Attempting Valid Admin Transition | Normal Customer (`ro | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Request rejected due to insufficient pri | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-031 | SEC-03: Normal Customer Role Attempting Admin Cancellation Route | Normal Customer (`ro | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "canceled"   }` | Request rejected because the admin statu | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-032 | SEC-03: Normal Customer Role Attempting Admin Transit Dispatch | Normal Customer (`ro | confirmed | PUT | `/api/admin/orders/:id/status` | `{     "status": "shipping"   }` | Request rejected due to non-admin role;  | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-033 | Cross-User Ownership Boundary: Customer B Cancelling Customer A's Pending Order | Unrelated Authentica | pending | PUT | `/api/orders/:id/cancel` | `Empty` | Cancellation rejected; authenticated cus | `ERROR / NON-SUCCESS – EXACT CO` | **CORRECTED DERIVATIVE** |
| FR10-AI-034 | Cross-User Ownership Boundary: Customer B Cancelling Customer A's Confirmed Order | Unrelated Authentica | confirmed | PUT | `/api/orders/:id/cancel` | `Empty` | Cancellation rejected; User B cannot can | `ERROR / NON-SUCCESS – EXACT CO` | **CORRECTED DERIVATIVE** |
| FR10-AI-035 | Status Domain: Undocumented Status Enum Value | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "processing"   }` | Status mutation rejected because `"proce | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-036 | Status Domain: Missing Required Status Property in Request Body | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{}` | Request rejected due to missing mandator | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-037 | Status Domain: Null Status Value in Mutation Body | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": null   }` | Request rejected; null values are invali | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-038 | Status Domain: Wrong JSON Type for Status Field | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": 123   }` | Request rejected due to data type mismat | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-039 | Order ID Partitions: Well-Formed Non-Existing Order ID | System Administrator | Non-existent order target | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Request rejected because the target orde | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |
| FR10-AI-040 | Order ID Partitions: Malformed / Non-Numeric Order ID Path Parameter | System Administrator | N/A (Invalid path parameter syntax) | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | Request rejected due to malformed path p | `ERROR / NON-SUCCESS – EXACT CO` | **CORRECTED DERIVATIVE** |
| FR10-AI-041 | Response + Persistence Consistency on Valid Transition | System Administrator | pending | PUT | `/api/admin/orders/:id/status` | `{     "status": "confirmed"   }` | - **Mutation Response:** Confirms succes | `200 OK` | **VALID AS-IS** |
| FR10-AI-042 | SEC-05: Partial Black-Box Behavioral SQL Injection Probe in Order ID Path Parameter | Attacker attempting  | Baseline existing database orders | PUT | `/api/admin/orders/:id/status` | `{     "status": "delivered"   }` | Injection attempt is neutralized; query  | `ERROR / NON-SUCCESS – EXACT CO` | **VALID AS-IS** |

---

## 3. Canonical Human Extension Mapping (FR10-HUM-001 through FR10-HUM-005)

| ID | Title / Purpose | Actor | Initial State | Method | Endpoint | Expected Semantic Outcome | Expected HTTP Status | Classification |
|---|---|---|---|:---:|---|---|---|:---:|
| **FR10-HUM-001** | Illegal Skip & Valid Transition Recovery | Admin | `pending` | PUT | `/api/admin/orders/:id/status` | Reject skip to shipping; accept transition to confirmed | Step 1: 400; Step 2: 200 | SPECIFICATION-BACKED |
| **FR10-HUM-002** | Multi-Order State Isolation | Admin | `pending` (A & B) | PUT | `/api/admin/orders/:id/status` | Mutate Order A to confirmed; assert Order B remains pending | 200 OK; verify B pending | SPECIFICATION-BACKED |
| **FR10-HUM-003** | In-Transit Cancellation Prohibited & Fulfillment Continuity | Owner User & Admin | `shipping` | PUT | `/api/orders/:id/cancel` & `/api/admin/orders/:id/status` | Reject customer cancel during shipping; Admin delivers successfully | Cancel: 4xx; Deliver: 200 | SPECIFICATION-BACKED |
| **FR10-HUM-004** | Same-State Transition Idempotency Probe | Admin | `confirmed` | PUT | `/api/admin/orders/:id/status` | Safe handling of redundant update (`confirmed` -> `confirmed`) | 200 (NOP) or 400 (rejection) | EXPLORATORY OBSERVATION |
| **FR10-HUM-005** | Non-JSON Media Type (`text/plain`) Robustness | Admin | `pending` | PUT | `/api/admin/orders/:id/status` | SUT handles unsupported content type safely without DB corruption | Non-success (400/415/500) | EXPLORATORY OBSERVATION |

---

## 4. Key Provenance Reconstructions

### AI-028 & AI-029
- **AI-028 (Raw Provenance):** Cryptographically Tampered JWT on Valid Admin Transition (`PUT /api/admin/orders/:id/status` with `{"status":"confirmed"}` and tampered signature).
- **AI-029 (Raw Provenance):** Missing Authorization Header on Customer Cancellation (`PUT /api/orders/:id/cancel` with empty body `{}`).

### AI-030, AI-031, AI-032 (SEC-03 RBAC Boundary)
- **AI-030 (Raw Provenance):** Normal Customer (`role = 'user'`) attempting Admin status mutation `pending` -> `confirmed` (`PUT /api/admin/orders/:id/status`).
- **AI-031 (Raw Provenance):** Normal Customer (`role = 'user'`) attempting Admin cancellation `pending` -> `canceled` (`PUT /api/admin/orders/:id/status`).
- **AI-032 (Raw Provenance):** Normal Customer (`role = 'user'`) attempting Admin transit dispatch `confirmed` -> `shipping` (`PUT /api/admin/orders/:id/status`).

### AI-033 & AI-034 (Cross-User Ownership)
- **AI-033 (Raw Provenance + Human Audit):** User B attempts to cancel User A's `pending` order via `PUT /api/orders/:id/cancel`. Human audit classification: `PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION`.
- **AI-034 (Raw Provenance + Human Audit):** User B attempts to cancel User A's `confirmed` order via `PUT /api/orders/:id/cancel`. Human audit classification: `PARTIALLY SPECIFICATION-BACKED / BUSINESS AUTHORIZATION`.

### AI-035..040 (Input Domain & ID Robustness)
- **AI-035:** Admin mutation with `status: "processing"` (undocumented enum) -> 4xx rejection.
- **AI-036:** Admin mutation with empty body `{}` (missing mandatory status key) -> 4xx rejection.
- **AI-037:** Admin mutation with `status: null` -> 4xx rejection.
- **AI-038:** Admin mutation with numeric status `status: 123` -> 4xx rejection.
- **AI-039:** Admin mutation on well-formed non-existent order ID `999999` -> 404 Not Found.
- **AI-040:** Admin mutation on malformed non-numeric order ID `not-an-id` -> Non-success error / safe rejection.
