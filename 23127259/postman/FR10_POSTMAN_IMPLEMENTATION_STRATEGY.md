# FR-10 Postman Implementation Strategy & Technical Architecture (Execution-Ready)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Planned Formal Executable Suite:** `46` Formal Test Cases

---

## 1. Formal Suite Accounting & Folder Architecture

The collection is organized into 11 logical folders with 77 total collection request definitions:

```
FR10_Order_State_Machine
├── 00 – Setup / Authentication & Fixture Helpers (17 requests: 3 auth + 14 fixture setup)
├── 01 – Valid Forward & Lifecycle Transitions (4 formal cases: 001..004, 7 request items)
├── 02 – Order Cancellation Pathways (4 formal cases: 005..008, 4 request items)
├── 03 – Invalid Forward Skips & Backward Regressions (7 formal cases: 009..011, 013..016, 7 request items)
├── 04 – Terminal-State Immutability (8 formal cases: 017..024, 8 request items)
├── 05 – SEC-02 Authentication Invariants (5 formal cases: 025..029, 5 request items)
├── 06 – SEC-03 Role-Based Access Control (RBAC) (3 formal cases: 030..032, 3 request items)
├── 07 – Cross-User Ownership & Partial Authorization (2 formal cases: 033, 034, 2 request items)
├── 08 – Status Enum & Order-ID Input Domain (6 formal cases: 035..040, 6 request items)
├── 09 – Response Schema, Persistence & SEC-05 (2 formal cases: 041, 042, 3 request items)
└── 10 – Human-Designed Extension Cases (5 formal cases: HUM-001..HUM-005, 15 request items)
```

---

## 2. Anti-Cheat & Header Injection Architecture

Collection-Level Pre-Request Script (Fail-Fast):
```javascript
const studentId = pm.environment.get("studentId");
if (!studentId) {
    throw new Error("studentId environment variable is required");
}
pm.request.headers.upsert({
    key: "X-Student-Id",
    value: studentId
});
```

Script-Triggered Request Pre-Configuration (`pm.sendRequest`):
```javascript
pm.sendRequest({
    url: pm.environment.get('baseUrl') + '/api/orders/' + pm.environment.get('orderPendingId'),
    method: 'GET',
    header: {
        'X-Student-Id': pm.environment.get('studentId'),
        'Authorization': 'Bearer ' + pm.environment.get('adminToken')
    }
}, function (err, res) { ... });
```

---

## 3. Formal Case vs Helper Request Accounting

- **Formal Test Cases:** Exactly **46** formal test cases.
- **Collection Request Definitions:** Exactly **77** request items (17 setup helpers + 60 formal steps).
- **Script-Triggered HTTP Verification Calls:** **36** `pm.sendRequest` GET queries.
- **Expected Total Runtime Operations:** **113** HTTP executions.
