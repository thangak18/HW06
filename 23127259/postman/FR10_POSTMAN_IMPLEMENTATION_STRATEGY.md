# FR-10 Postman Implementation Strategy & Technical Architecture (Per-Case Isolated)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Planned Formal Executable Suite:** `46` Formal Test Cases

---

## 1. Collection Folder Structure (138 Request Definitions)

```
FR10_Order_State_Machine
├── 00 – Setup / Authentication Helpers (3 login requests)
├── 01 – Valid Forward & Lifecycle Transitions (4 formal cases: 001..004, 15 request items)
├── 02 – Order Cancellation Pathways (4 formal cases: 005..008, 10 request items)
├── 03 – Invalid Forward Skips & Backward Regressions (7 formal cases: 009..011, 013..016, 23 request items)
├── 04 – Terminal-State Immutability (8 formal cases: 017..024, 32 request items)
├── 05 – SEC-02 Authentication Invariants (5 formal cases: 025..029, 10 request items)
├── 06 – SEC-03 Role-Based Access Control (RBAC) (3 formal cases: 030..032, 6 request items)
├── 07 – Cross-User Ownership & Partial Authorization (2 formal cases: 033, 034, 5 request items)
├── 08 – Status Enum & Order-ID Input Domain (6 formal cases: 035..040, 10 request items)
├── 09 – Response Schema, Persistence & SEC-05 (2 formal cases: 041, 042, 4 request items)
└── 10 – Human-Designed Extension Cases (5 formal cases: HUM-001..HUM-005, 16 request items)
```

---

## 2. Operation Reconciliation
- **Formal Test Cases:** **`46`**
- **Collection Request Definitions:** **`138`**
- **Script-Triggered Persistence GETs:** **`36`**
- **Expected Total Runtime Operations:** **`174`**
