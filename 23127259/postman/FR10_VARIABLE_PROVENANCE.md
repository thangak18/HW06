# FR-10 Dynamic Variable & Fixture Provenance Inventory (Per-Case Isolated)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)

---

## 1. Dynamic Variable Provenance Table

| Variable | Initial Environment Value | First Writer | HTTP Operation Producing Value | Consumers | Generated Before First Use? | Safe? |
|---|---|---|---|---|:---:|:---:|
| **`baseUrl`** | `http://localhost:3000` | Environment | None (Static Config) | All Collection Requests | YES | YES |
| **`studentId`** | `23127259` | Environment | None (Static Config) | Pre-request scripts & all `pm.sendRequest` | YES | YES |
| **`adminEmail`** | `admin@eshop.com` | Environment | None (Static Credential) | `[SETUP] Login Admin` | YES | YES |
| **`adminPassword`** | `Admin1234!` | Environment | None (Static Credential) | `[SETUP] Login Admin` | YES | YES |
| **`userAEmail`** | `user@eshop.com` | Environment | None (Static Credential) | `[SETUP] Login User A` | YES | YES |
| **`userAPassword`** | `User1234!` | Environment | None (Static Credential) | `[SETUP] Login User A` | YES | YES |
| **`userBEmail`** | `user_domain@eshop.com` | Environment | None (Static Credential) | `[SETUP] Login User B` | YES | YES |
| **`userBPassword`** | `Domain1234!` | Environment | None (Static Credential) | `[SETUP] Login User B` | YES | YES |
| **`adminToken`** | `""` (Empty) | `[SETUP] Login Admin` | `POST /api/auth/login` | All Admin Operations & Persistence GETs | YES | YES |
| **`userAToken`** | `""` (Empty) | `[SETUP] Login User A` | `POST /api/auth/login` | Setup Checkout Requests, Cancellation & Verification GETs | YES | YES |
| **`userBToken`** | `""` (Empty) | `[SETUP] Login User B` | `POST /api/auth/login` | Folder 07 Ownership Probes (`AI-033`, `AI-034`) | YES | YES |
| **`guestToken`** | Synthetic Invalid JWT | Environment | None (Synthetic) | Folder 06 RBAC (`AI-032`) | YES | YES |
| **`order_FR10_AI_001` .. `_041`** | `""` (Unset) | Co-located Setup Item | `POST /api/checkout` (by User A) | Dedicated single formal case only | YES | YES |
| **`order_FR10_HUM_001` .. `_005`** | `""` (Unset) | Co-located Setup Item | `POST /api/checkout` (by User A) | Dedicated single formal case only | YES | YES |
| **`order_FR10_HUM_002_A`, `_B`** | `""` (Unset) | Co-located Setup Items | `POST /api/checkout` (by User A) | Dedicated to `FR10-HUM-002` only | YES | YES |

---

## 2. Strict Per-Case Setup Architecture

Each formal test case containing a real order fixture operates through a dedicated, self-contained lifecycle sequence:
1. `[FR10-xxx][SETUP-CREATE]` $ightarrow$ Clears case variable, creates fresh order via `POST /api/checkout`, fail-fast extracts ID into `order_FR10_xxx`.
2. `[FR10-xxx][SETUP-CONFIRM / SHIP / DELIVER / CANCEL]` $ightarrow$ Preconditions state if starting state is non-pending.
3. `[FR10-xxx][ACTION]` $ightarrow$ Performs formal mutation/probe under test.
4. `[FR10-xxx][VERIFY]` $ightarrow$ Read-after-write persistence verification oracle.
