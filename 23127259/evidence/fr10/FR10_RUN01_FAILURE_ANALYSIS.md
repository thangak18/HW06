# FR-10 Newman Run 01 Failure Analysis Inventory (Corrected)

> **RUN 01 DERIVED ANALYSIS CORRECTED AFTER HUMAN REVIEW**
> All 130 assertion failures in Run 01 stem from the single root cause: Folder 00 login helpers targeted `/api/auth/login` (404 Not Found), preventing token population and causing downstream setup checkouts to fail with 401 Unauthorized.

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature Under Test:** FR-10 – Order Status & State Machine (Pool B)
- **Total Failed Assertions:** `130`
- **Primary Root Cause:** **Harness Auth Route Prefix Mismatch** (`/api/auth/login` vs active `/api/login` in Folder 00 setup items).

---

## 1. Root Cause & Precondition Evaluation

1. **Authentication Setup Failure in Folder 00:**
   - `[SETUP] Register User B` succeeded (`POST /api/register` returned `200 OK`, `id: 56`).
   - `[SETUP] Login Admin`, `[SETUP] Login User A`, and `[SETUP] Login User B` targeted `POST /api/auth/login`.
   - The active SUT route is `POST /api/login`. As a result, the SUT returned `HTTP 404 Cannot POST /api/auth/login`.
   - Consequently, `adminToken`, `userAToken`, and `userBToken` were not populated in the active environment during execution.

2. **Downstream Precondition Collapse:**
   - All 44 isolated checkout fixtures received `HTTP 401 Unauthorized`.
   - Because no order ID was ever created, **precondition established = NO** for all 46 formal cases.
   - For `FR10-AI-025` and `FR10-AI-028` (missing auth probes), receiving 401 was a premature rejection before resource binding occurred; therefore, they are correctly reclassified as `BLOCKED – HARNESS/SETUP`.
   - For `FR10-HUM-004` and `FR10-HUM-005`, initial confirmed/pending orders were never established; therefore, they are correctly reclassified as `BLOCKED – HARNESS/SETUP`.

3. **Classification Rule:**
   - **All 46 formal cases are classified as `BLOCKED – HARNESS/SETUP`.**
   - **Zero failures are classified as SUT business defects in Run 01.**

---

## 2. Representative Failure Breakdown

| Failure Scope | Requests Involved | Observed Status | Failure Category | Resolution |
|---|---|:---:|---|---|
| **Folder 00 Auth Helpers** | 3 login requests (`Admin`, `User A`, `User B`) | `HTTP 404` | HARNESS / SETUP | Update URL to `POST /api/login` |
| **Case Setup Checkouts** | 44 isolated checkout requests | `HTTP 401` | HARNESS / SETUP | Resolved automatically once tokens propagate |
| **Formal Action Steps** | 88 transition & cancel requests | `HTTP 401 / 404` | HARNESS / SETUP | Resolved automatically once order fixtures exist |
