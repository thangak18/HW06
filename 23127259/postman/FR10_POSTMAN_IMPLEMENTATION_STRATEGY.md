# FR-10 Postman Implementation Strategy & Technical Architecture

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Planned Formal Executable Suite:** `46` Formal Test Cases

---

## 1. Formal Suite Accounting & Folder Architecture

The collection is organized into 11 logical folders:

```
FR10_Order_State_Machine
├── 00 – Setup / Authentication Helpers (Auth & token extraction)
├── 01 – Valid Forward & Lifecycle Transitions (4 formal cases: 001..004)
├── 02 – Order Cancellation Pathways (4 formal cases: 005..008)
├── 03 – Invalid Forward Skips & Backward Regressions (7 formal cases: 009..011, 013..016)
├── 04 – Terminal-State Immutability (8 formal cases: 017..024)
├── 05 – SEC-02 Authentication Invariants (5 formal cases: 025..029)
├── 06 – SEC-03 Role-Based Access Control (RBAC) (3 formal cases: 030..032)
├── 07 – Cross-User Ownership & Partial Authorization (2 formal cases: 033, 034)
├── 08 – Status Enum & Order-ID Input Domain (6 formal cases: 035..040)
├── 09 – Response Schema, Persistence & SEC-05 (2 formal cases: 041, 042)
└── 10 – Human-Designed Extension Cases (5 formal cases: HUM-001..HUM-005)
```

---

## 2. Anti-Cheat & Header Injection Architecture

Collection-Level Pre-Request Script:
```javascript
// Centrally inject mandatory Student ID header into all outgoing requests
pm.request.headers.upsert({
    key: "X-Student-Id",
    value: pm.environment.get("studentId") || "23127259"
});
```

---

## 3. Formal Case vs Helper Request Accounting

To maintain rigorous integrity between formal test counting and HTTP execution counting:
- **Formal Test Case Count:** Exactly **46** formal test cases.
- **Total HTTP Requests in Collection:** Includes setup authentication helpers, fixture creation calls, and multi-step continuity requests.
- **Newman Traceability:** Every request name is prefixed with its formal test ID (e.g. `[FR10-AI-001]`, `[FR10-HUM-001][ACTION]`, `[FR10-HUM-001][VERIFY]`) so that automated tools accurately roll up requests into the 46 formal cases.

---

## 4. Exploratory Case Handling Strategy
- **`FR10-HUM-004` (Same-State Self-Loop):** Postman test captures the response status family (200 OK vs 4xx) and asserts that the persisted state remains `confirmed` without asserting a single hardcoded status code.
- **`FR10-HUM-005` (Non-JSON Media Type):** Postman test captures response handling and asserts that no unexpected state mutation or unhandled crash corrupts the target order.
