# FR-02 Postman Execution & State Isolation Strategy

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

---

## 1. Executive Summary & Design Principles

Stateful testing of authentication lockout mechanics presents unique challenges:
1. **Destructive State Changes:** Lockout triggers an account transition to a 30-second locked state, which would cause subsequent tests on the same account to fail unexpectedly.
2. **Order Dependence & Repeatability:** Tests must be repeatable without requiring manual database resets or corrupting subsequent test runs.
3. **Black-Box Integrity:** Tests must rely on externally observable HTTP responses and standard API mechanisms, never assuming undocumented database reset backdoors.

To achieve complete state isolation, this strategy establishes **Account Segregation**, **Deterministic Lifecycle Partitioning**, and **Time-Bracketed State Verification**.

---

## 2. Account Segregation Architecture

Instead of sharing a single test user across the entire suite, test cases are assigned to distinct, isolated account fixtures:

| Account Role | Target Account / Variable | Associated Test Scope | Justification & Lifecycle |
|---|---|---|---|
| **Baseline Normal User** | `{{userEmail}}` (`user@eshop.com`) | Positive user login (`FR02-AI-001`), schema validation (`FR02-AI-032`), HTTP method check (`FR02-HUM-001`), Content-Type check (`FR02-HUM-005`) | Guaranteed to remain in `NORMAL` state with 0 failures. No negative tests are run on this account. |
| **Baseline Admin User** | `{{adminEmail}}` (`admin@eshop.com`) | Admin login (`FR02-AI-002`), SQL injection probes (`FR02-AI-025`, `FR02-HUM-002`) | Dedicated administrator credential. |
| **Negative Domain User** | `{{negativeUserEmail}}` (`user_domain@eshop.com`) | Single-attempt negative inputs: wrong passwords, empty strings, nulls, whitespace (`FR02-AI-003`, `FR02-AI-005`..`012`) | Evaluates stateless input validation without exceeding the $N=3$ lockout threshold. |
| **Dedicated Lockout User** | `{{lockoutEmail}}` (`lockout_fr02@eshop.com`) | Lockout progression ($N=1, 2, 3$), active lock rejection, and timing boundaries (`FR02-AI-013`..`015`, `018`..`021`, `024`) | Isolated lifecycle dedicated exclusively to the full lockout and recovery sequence. |
| **Reset Boundary User** | `{{resetBoundaryEmail}}` (`reset_fr02@eshop.com`) | Reset-on-success tests (`FR02-AI-022`, `FR02-AI-023`, `FR02-HUM-003`) | Dedicated account for verifying counter reset after 1 or 2 consecutive failures. |
| **Isolation User A (Victim)** | `{{victimEmail}}` (`victim_fr02@eshop.com`) | Cross-account lockout isolation (`FR02-HUM-004` Part 1) | Account locked via 3 failures. |
| **Isolation User B (Observer)** | `{{isolatedEmail}}` (`isolated_fr02@eshop.com`) | Cross-account lockout isolation (`FR02-HUM-004` Part 2) | Proves Account B authenticates normally despite Account A being locked. |

---

## 3. Test Setup Mechanism

To ensure clean initial conditions across automated test runs, the collection utilizes documented API setup requests located in `00 – Setup Helpers`:
- Setup requests invoke documented user registration (`POST /api/register`) or health-check endpoints.
- All helper requests are explicitly labeled: `HELPER – SETUP ONLY – NOT FR-02 TEST CASE` and are excluded from the 40-case formal count.
- If an account already exists from a prior run, helper scripts handle the response gracefully without blocking test execution.

---

## 4. Timing Strategy for 30-Second Lockout Window

The SRS specifies a **30-second lockout duration**:
- **Pre-Expiration Boundary (`FR02-AI-020`):** Tested at $T pprox 25	ext{s}$ (or immediately during active lock $T < 30	ext{s}$). The account is verified to remain locked.
- **Post-Expiration Boundary (`FR02-AI-021`):** Requires waiting for the 30-second window to expire ($T pprox 32	ext{s}$).
  - In automated Newman execution, Postman execution scripts or external runner hooks safely bracket the timing window ($T=32	ext{s}$).
  - Exact millisecond synchronization is avoided in favor of deterministic timing windows.

---

## 5. Non-Reliance on Internal Database Fields

In accordance with Human Audit findings:
- Postman test scripts **never** assert against internal database column values (e.g. `login_attempts = 2` or `lockout_until = ...`).
- All test oracles are evaluated purely through **observable HTTP status codes**, **response payloads**, and **subsequent request acceptance/rejection behavior**.
