# FR-10 Materialization Deep Static Audit & Hardening Report

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Status:** **STATIC AUDIT, FIXTURE PROVENANCE & ROUTE READINESS COMPLETE**

---

## 1. Audit Scope & Objectives

Prior to any runtime execution in Postman or Newman, a comprehensive static inspection of the FR-10 test collection and supporting artifacts was conducted to verify:
1. Exact route verification against authoritative project documentation (`POST /api/auth/login`, `POST /api/checkout`, `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel`, `GET /api/orders/:id`).
2. Exact fixture provenance and dynamic order creation mechanics in Folder 00.
3. Variable dataflow lifecycle ensuring zero uninitialized variables at point of first use.
4. Fail-fast enforcement of the collection-level `X-Student-Id` pre-request script.
5. Strict inclusion of `X-Student-Id` and authorized `Authorization: Bearer {{token}}` headers inside **every** `pm.sendRequest` script call and setup helper.
6. Verification of non-normative oracles for exploratory cases (`FR10-HUM-004`, `FR10-HUM-005`) and corrected cases (`FR10-AI-033`, `034`, `040`).

---

## 2. Identified Discrepancies & Hardening Actions

| Audit Dimension | Issue Identified Before Audit | Hardening Action Applied | Formal Accounting Impact | Oracle Impact |
|---|---|---|:---:|:---:|
| **Fixture Provenance** | Pre-filled static order IDs in environment had no proven dynamic creation. | Added 14 dynamic order creation and prerequisite transition helpers to Folder 00. | Unchanged (`46` formal cases) | Unchanged |
| **Variable Isolation** | Reusing a single `orderId` variable risked cross-test mutation conflicts. | Allocated dedicated fixture variables (`orderPendingId`, `orderConfirmedId`, `orderShippingId`, `orderDeliveredId`, `orderCanceledId`, `orderAId`, `orderBId`, `orderId`). | Unchanged | Unchanged |
| **Multi-Step Workflows** | Multi-step formal cases (`AI-004`, `AI-041`, `HUM-001`, `HUM-002`, `HUM-003`) had single request placeholders. | Expanded into 19 explicit standalone collection items tagged under parent formal IDs. | Unchanged | Unchanged |
| **`X-Student-Id` Script Calls** | `pm.sendRequest` calls in test scripts bypass collection pre-request scripts. | Explicitly injected `X-Student-Id: pm.environment.get('studentId')` into every script-level request payload. | Unchanged | Unchanged |
| **`X-Student-Id` Fallback** | Fallback `|| "23127259"` masked missing environment variable selection. | Converted to fail-fast check throwing explicit Error if `studentId` is not defined. | Unchanged | Unchanged |
| **SEC-02 Documentation** | Folder 05 was loosely described as testing "expired tokens" when AI cases test invalid/random/tampered tokens. | Corrected folder descriptions in all docs to accurately state `SEC-02` invalid token / untrusted signature tests. | Unchanged | Unchanged |

---

## 3. Invariant Verification Confirmation
- **Raw AI Draft Frozen Hash:** Strictly verified (`303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc`).
- **Rejected Case Exclusion:** `FR10-AI-012` is completely absent from all collection items and scripts.
- **Human Cases Count:** Exactly 5 continuous Human Extension cases (`FR10-HUM-001` .. `FR10-HUM-005`).
- **Hardcoded Live Secrets:** Zero hardcoded live JWTs found across all JSON files.
