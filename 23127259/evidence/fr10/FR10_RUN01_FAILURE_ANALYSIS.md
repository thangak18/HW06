# FR-10 Newman Run 01 Failure Analysis Inventory

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature Under Test:** FR-10 – Order Status & State Machine (Pool B)
- **Total Failed Assertions:** `130`
- **Primary Root Cause:** **Harness Auth Route Prefix Mismatch** (`/api/auth/login` vs active `/api/login` in Folder 00 setup items).

---

## 1. Root Cause & Cascade Analysis

1. **Authentication Setup Failure in Folder 00:**
   - `[SETUP] Register User B` succeeded (`POST /api/register` returned `200 OK`, `id: 56`).
   - `[SETUP] Login Admin`, `[SETUP] Login User A`, and `[SETUP] Login User B` targeted `POST /api/auth/login`.
   - The active SUT route is `POST /api/login`. As a result, the SUT returned `HTTP 404 Cannot POST /api/auth/login`.
   - Consequently, `adminToken`, `userAToken`, and `userBToken` were not populated in the active environment during execution.

2. **Downstream Cascade Effect:**
   - Subsequent isolated fixture checkout requests (`POST /api/checkout` with empty `Authorization: Bearer `) failed with `HTTP 401 Unauthorized`.
   - Order creation responses did not yield `orderId` values, causing downstream action and verification steps to receive `401 Unauthorized` or `404 Not Found`.

3. **Classification Distinction:**
   - **All 130 assertion failures in Run 01 are classified as `HARNESS / SETUP` failures.**
   - **Zero failures are classified as SUT business defects in Run 01.**
   - Per assignment instructions, no bugs or GitHub Issues are filed based on harness setup failures.

---

## 2. Failed Assertion Inventory

| Formal ID | Step / Request Name | Failure Category | Expected | Actual Failure Message | Confirmation Needed |
|---|---|---|---|---|:---:|
| `SETUP` | `[SETUP] Login Admin` | `HARNESS / SETUP` | Status 200/201 | expected 404 to be one of [ 200, 201 ] | YES |
| `SETUP` | `[SETUP] Login User A (Customer A - Owner)` | `HARNESS / SETUP` | Status 200/201 | expected 404 to be one of [ 200, 201 ] | YES |
| `SETUP` | `[SETUP] Login User B (Customer B - Non-Owner)` | `HARNESS / SETUP` | Status 200/201 | expected 404 to be one of [ 200, 201 ] | YES |
| `FR10-AI-001` | `[FR10-AI-001][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-001` | `[FR10-AI-001][ACTION] Admin Confirms Pending Order (pending -> confirmed)` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-002` | `[FR10-AI-002][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-002` | `[FR10-AI-002][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-002` | `[FR10-AI-002][ACTION] Admin Dispatches Confirmed Order (confirmed -> shipping)` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-003` | `[FR10-AI-003][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-003` | `[FR10-AI-003][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-003` | `[FR10-AI-003][SETUP-SHIP] Transition to shipping` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-003` | `[FR10-AI-003][ACTION] Admin Delivers Shipping Order (shipping -> delivered)` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-004` | `[FR10-AI-004][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-004` | `[FR10-AI-004][STEP-1] Linear Progression: pending -> confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-004` | `[FR10-AI-004][STEP-2] Linear Progression: confirmed -> shipping` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-004` | `[FR10-AI-004][STEP-3] Linear Progression: shipping -> delivered` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-004` | `[FR10-AI-004][VERIFY] Read Terminal State: GET delivered` | `HARNESS / SETUP` | Status 200/201 | expected 404 to be one of [ 200, 201 ] | YES |
| `FR10-AI-005` | `[FR10-AI-005][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-005` | `[FR10-AI-005][ACTION] Customer Cancellation on Pending Order` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-006` | `[FR10-AI-006][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-006` | `[FR10-AI-006][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-006` | `[FR10-AI-006][ACTION] Customer Cancellation on Confirmed Order` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-007` | `[FR10-AI-007][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-007` | `[FR10-AI-007][ACTION] Admin Status Cancellation on Pending Order` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-008` | `[FR10-AI-008][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-008` | `[FR10-AI-008][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-008` | `[FR10-AI-008][ACTION] Admin Status Cancellation on Confirmed Order` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-009` | `[FR10-AI-009][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-009` | `[FR10-AI-009][ACTION] Invalid Skip: Admin Attempts pending -> shipping` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 400, 422, 403, 404 ] | YES |
| `FR10-AI-010` | `[FR10-AI-010][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-010` | `[FR10-AI-010][ACTION] Invalid Skip: Admin Attempts pending -> delivered` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 400, 422, 403, 404 ] | YES |
| `FR10-AI-011` | `[FR10-AI-011][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-011` | `[FR10-AI-011][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-011` | `[FR10-AI-011][ACTION] Invalid Skip: Admin Attempts confirmed -> delivered` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 400, 422, 403, 404 ] | YES |
| `FR10-AI-013` | `[FR10-AI-013][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-013` | `[FR10-AI-013][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-013` | `[FR10-AI-013][ACTION] Invalid Regression: Admin Attempts confirmed -> pending` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 400, 422, 403, 404 ] | YES |
| `FR10-AI-014` | `[FR10-AI-014][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-014` | `[FR10-AI-014][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-014` | `[FR10-AI-014][SETUP-SHIP] Transition to shipping` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-014` | `[FR10-AI-014][ACTION] Invalid Regression: Admin Attempts shipping -> confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 400, 422, 403, 404 ] | YES |
| `FR10-AI-015` | `[FR10-AI-015][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-015` | `[FR10-AI-015][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-015` | `[FR10-AI-015][SETUP-SHIP] Transition to shipping` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-015` | `[FR10-AI-015][ACTION] Invalid Regression: Admin Attempts shipping -> pending` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 400, 422, 403, 404 ] | YES |
| `FR10-AI-016` | `[FR10-AI-016][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-016` | `[FR10-AI-016][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-016` | `[FR10-AI-016][SETUP-SHIP] Transition to shipping` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-016` | `[FR10-AI-016][ACTION] Customer Cancel on In-Transit Order (rejected)` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 400, 422, 403, 404 ] | YES |
| `FR10-AI-017` | `[FR10-AI-017][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-017` | `[FR10-AI-017][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-017` | `[FR10-AI-017][SETUP-SHIP] Transition to shipping` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-017` | `[FR10-AI-017][SETUP-DELIVER] Transition to delivered` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-017` | `[FR10-AI-017][ACTION] Terminal Immutability: delivered -> pending` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 400, 422, 403, 404 ] | YES |
| `FR10-AI-018` | `[FR10-AI-018][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-018` | `[FR10-AI-018][SETUP-CONFIRM] Transition to confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-018` | `[FR10-AI-018][SETUP-SHIP] Transition to shipping` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-018` | `[FR10-AI-018][SETUP-DELIVER] Transition to delivered` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
| `FR10-AI-018` | `[FR10-AI-018][ACTION] Terminal Immutability: delivered -> confirmed` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 400, 422, 403, 404 ] | YES |
| `FR10-AI-019` | `[FR10-AI-019][SETUP-CREATE] Create Isolated Order Fixture` | `HARNESS / SETUP` | Status 200/201 | expected 401 to be one of [ 200, 201 ] | YES |
