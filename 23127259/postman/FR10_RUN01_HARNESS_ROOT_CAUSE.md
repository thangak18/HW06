# FR-10 Newman Run 01 Harness Root Cause & Synchronization Defect Analysis

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature Under Test:** FR-10 – Order Status & State Machine (Pool B)
- **Execution Run:** Run 01 (`1bf476a`)
- **Classification:** **`HARNESS ARTIFACT / REPORT SYNCHRONIZATION DEFECT`**

---

## 1. Actual Runtime Execution Failure Evidence from `FR10-run01.json`

Inspection of the raw execution stream in `FR10-run01.json` reveals the exact runtime requests and responses for the authentication helpers in Folder 00:

| Execution Item | Target Method & URL | HTTP Status | Response Body Stream Snippet |
|---|---|:---:|---|
| `[SETUP] Register User B (Non-Owner) Account` | `POST http://localhost:3000/api/register` | **`200 OK`** | `{"message":"User registered successfully","id":56}` |
| `[SETUP] Login Admin` | `POST http://localhost:3000/api/auth/login` | **`404 Not Found`** | `<!DOCTYPE html><html lang="en">...<pre>Cannot POST /api/auth/login</pre>...` |
| `[SETUP] Login User A (Customer A - Owner)` | `POST http://localhost:3000/api/auth/login` | **`404 Not Found`** | `<!DOCTYPE html><html lang="en">...<pre>Cannot POST /api/auth/login</pre>...` |
| `[SETUP] Login User B (Customer B - Non-Owner)` | `POST http://localhost:3000/api/auth/login` | **`404 Not Found`** | `<!DOCTYPE html><html lang="en">...<pre>Cannot POST /api/auth/login</pre>...` |
| `[FR10-AI-001][SETUP-CREATE] Create Isolated Order Fixture` | `POST http://localhost:3000/api/checkout` | **`401 Unauthorized`** | `{"error":"Unauthorized"}` (Bearer token was empty) |

---

## 2. Process Inconsistency & Artifact Synchronization Root Cause

### The Discrepancy:
- In Phase 2D.1A (`INT-040`), smoke testing successfully identified that the active SUT route is `POST /api/login` (rather than `/api/auth/login`).
- Smoke reports (`FR10_RUNTIME_SMOKE_REPORT.md`) claimed `HARNESS-REP-01: active assignment SUT accepts /api/login`.
- However, when Newman Run 01 executed the committed collection (`FR10_Order_State_Machine.postman_collection.json`), the 3 login items in Folder 00 still executed `POST http://localhost:3000/api/auth/login` and failed with HTTP 404.

### Technical Root Cause:
1. **Generator Script Hardcoding:** The underlying generator `build_per_case_isolation_harness.py` originally defined Folder 00 login items with URL path `['api', 'auth', 'login']`.
2. **Partial In-Memory vs Disk Persistence:** During Phase 2D.1A smoke scripting, dynamic probes tested `POST /api/login` directly via Python, while the static JSON collection file on disk retained the `/api/auth/login` URL template in Folder 00.
3. **Validator Coverage Gap:** While `validate_fr10_fixture_isolation.py` and `validate_fr10_actor_readiness.py` checked test case IDs, token variables (`adminToken`, `userAToken`), and script headers, neither script statically verified the exact URL path elements (`path: ["api", "login"]`) of Folder 00 items.
4. **Correction Mechanism:** In Phase 2D.1C, a dedicated static validator `validate_fr10_auth_harness.py` is introduced to strictly enforce zero occurrences of `/api/auth/login` directly against the collection JSON file before any future Newman execution.

---

## 3. Impact on Formal Run 01 Reconciliation

- Because Folder 00 login helpers returned 404, no JWT tokens were extracted into `adminToken`, `userAToken`, or `userBToken`.
- All downstream checkout setup steps received `HTTP 401 Unauthorized`.
- Because order fixtures were never created, zero formal test case preconditions were established.
- Consequently, **all 46 formal cases are classified as `BLOCKED – HARNESS/SETUP`** in the corrected Run 01 formal reconciliation. Zero failures are attributed to SUT defects.
