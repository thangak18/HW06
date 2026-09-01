# FR-02 AI Generation Coverage Review

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Review Stage:** Phase 1A.6 (Part B) – Generation Review & Inventory Freeze

---

## 1. Raw Inventory

- **Feature Name:** FR-02 – Login and Account Lockout
- **Pool Allocation:** Pool A
- **Raw AI-Generated Test Cases:** 37
- **Test Case ID Range:** `FR02-AI-001` .. `FR02-AI-037`
- **Generation Interactions:** `INT-005` .. `INT-009`
- **Generation Support Interactions:** `INT-010`, `INT-011`

---

## 2. Stage Accounting

| Stage | Interaction ID | ID Range | Generated Count | Sub-Suite Focus |
|---|:---:|:---:|---:|---|
| **Requirement & Domain Analysis** | `INT-005` | N/A | 0 | Baseline specification extraction & parameter inventory |
| **Domain Partitions & BVA** | `INT-006` | `FR02-AI-001` .. `FR02-AI-014` | 14 | Valid/invalid domain inputs, missing/null/empty, BVA $N=2,3$ |
| **Lockout & State Transitions** | `INT-007` | `FR02-AI-015` .. `FR02-AI-024` | 10 | Consecutive failure progression, active lock, timing boundaries |
| **Security Probes & Token Usability** | `INT-008` | `FR02-AI-025` .. `FR02-AI-031` | 7 | SEC-05 SQLi probes, anti-enumeration, SEC-02 token probes |
| **Schema Validation & Error Contracts** | `INT-009` | `FR02-AI-032` .. `FR02-AI-037` | 6 | Success/error schema contracts, MIME types, parser resilience |
| **TOTAL RAW AI-GENERATED CASES** | | **`FR02-AI-001` .. `FR02-AI-037`** | **37** | **Target $\ge 35$ Achieved** |

---

## 3. Requirement Coverage Matrix

| Coverage Area | Raw AI Case IDs | Coverage Present? | Notes |
|---|---|:---:|---|
| **Valid Authentication (User)** | `FR02-AI-001` | YES | Tests user login with valid credentials (200 OK + JWT) |
| **Valid Authentication (Admin)** | `FR02-AI-002` | YES | Tests admin login with valid credentials (200 OK + admin JWT) |
| **Invalid Credentials (General)** | `FR02-AI-003`, `FR02-AI-010` | YES | Tests credential rejection and generic failure response |
| **Registered Email with Wrong Password** | `FR02-AI-003`, `FR02-AI-027` | YES | Tests failure counter accumulation and anti-enumeration equality |
| **Unregistered Syntactically Valid Email** | `FR02-AI-004`, `FR02-AI-027` | YES | Tests non-disclosure of user existence |
| **Malformed Email Syntax (Missing `@`)** | `FR02-AI-005` | YES | Tests syntactic email format validation rejection |
| **Empty Email String (`""`)** | `FR02-AI-006` | YES | Tests mandatory email input validation |
| **Missing Email Property in JSON** | `FR02-AI-007` | YES | Tests request body schema payload structure validation |
| **Null Email Value in JSON** | `FR02-AI-008` | YES | Tests type safety and null pointer resilience |
| **Whitespace-Only Email String** | `FR02-AI-009` | YES | Tests blank input rejection / non-empty validation |
| **Correct Password Matching Registered User** | `FR02-AI-001`, `FR02-AI-002`, `FR02-AI-021`, `FR02-AI-022`, `FR02-AI-032` | YES | Baseline positive credential matching |
| **Incorrect Password for Registered User** | `FR02-AI-003`, `FR02-AI-013`, `FR02-AI-014`, `FR02-AI-015`, `FR02-AI-016`, `FR02-AI-017` | YES | Tests failure progression sequence |
| **Empty Password String (`""`)** | `FR02-AI-010` | YES | Tests mandatory password input validation |
| **Missing Password Property in JSON** | `FR02-AI-011` | YES | Tests payload schema completeness |
| **Null Password Value in JSON** | `FR02-AI-012` | YES | Tests type safety and null value rejection |
| **Lockout Progression: Attempt $N=1$** | `FR02-AI-015` | YES | Explicitly asserts 1st failure increments counter, account remains UNLOCKED |
| **Lockout Progression: Boundary $N=2$** | `FR02-AI-013`, `FR02-AI-016` | YES | Tests $(N-1)$ boundary just below threshold; account remains UNLOCKED |
| **Lockout Progression: Boundary $N=3$** | `FR02-AI-014`, `FR02-AI-017` | YES | Tests threshold boundary; account state transitions to LOCKED |
| **Active Lockout Window Rejection (Wrong Password)** | `FR02-AI-018` | YES | Tests active defense against continued brute-force attempts |
| **Active Lockout Window Rejection (Correct Password)** | `FR02-AI-019` | YES | Verifies correct credentials cannot bypass active lockout |
| **Lockout Duration Timing: Pre-Expiry ($T=25\text{s} < 30\text{s}$)** | `FR02-AI-020` | YES | Boundary check before 30-second duration expires (account still locked) |
| **Lockout Duration Timing: Post-Expiry ($T=32\text{s} > 30\text{s}$)** | `FR02-AI-021` | YES | Boundary check verifying automatic unlock after 30-second window |
| **Successful-Login Reset Rule** | `FR02-AI-022` | YES | Verifies successful login resets consecutive failure counter to 0 |
| **Consecutive-Failure Semantics** | `FR02-AI-023` | YES | Verifies non-consecutive interleaved failures do not trigger lockout |
| **SQL Injection Probe in Email Field** | `FR02-AI-025` | YES | SEC-05 behavioral probe with classic authentication-bypass payload |
| **SQL Injection Probe in Password Field** | `FR02-AI-026` | YES | SEC-05 behavioral probe with tautology/comment payload |
| **Credential Enumeration / Generic Error Equivalence** | `FR02-AI-027` | YES | Compares wrong-password vs unregistered-email responses for identical error text |
| **Sensitive Response Information Exclusion** | `FR02-AI-028` | YES | Verifies plaintext password is omitted from successful login JSON response |
| **Token Issuance on Authentication Success** | `FR02-AI-001`, `FR02-AI-002`, `FR02-AI-032` | YES | Verifies valid JWT token is returned in success payload |
| **Token Omission on Authentication Failure** | `FR02-AI-029`, `FR02-AI-033` | YES | Verifies `token` property is strictly absent on 4xx credential failure |
| **JWT Downstream Supporting Usability** | `FR02-AI-030`, `FR02-AI-031` | YES | Validates token usability and tampered signature rejection on protected route |
| **Successful Response JSON Schema Contract** | `FR02-AI-032` | YES | Deep structural and data-type validation of 200 OK success payload |
| **Invalid-Credential Error Response Contract** | `FR02-AI-033` | YES | Validates error structure and complete absence of auth session objects |
| **Locked-Account Error Response Contract & Non-Disclosure** | `FR02-AI-034` | YES | Validates lockout error structure and non-disclosure of internal variables |
| **Syntactically Malformed JSON Transport Contract** | `FR02-AI-035` | YES | Tests parser resilience against raw truncated/broken JSON syntax |
| **Response Content-Type Header Contract** | `FR02-AI-036` | YES | Validates `application/json` header delivery across 200 and 4xx responses |
| **Extraneous Request Body Properties Ingestion** | `FR02-AI-037` | YES | Evaluates schema parser tolerance and role non-escalation |

---

## 4. Potential Questions for Later Human Audit

The following items are flagged for inspection during the mandatory Human Test-Case Audit (Phase 1B). No verdicts (`VALID`, `INVALID`, `INCOMPLETE`) are assigned at this stage; items are categorized strictly by analytical question type:

1. **`FR02-AI-013` vs `FR02-AI-016` (BVA $N=2$ vs State Transition $N=2$):**
   - **Flag:** `POTENTIAL OVERLAP`
   - **Reasoning:** `FR02-AI-013` was generated as a boundary test for $(N=2)$ and `FR02-AI-016` was generated as a state-transition progression test for attempt 2. The human auditor should evaluate whether both provide distinct test value or represent partial duplication.

2. **`FR02-AI-014` vs `FR02-AI-017` (BVA $N=3$ vs State Transition $N=3$):**
   - **Flag:** `POTENTIAL OVERLAP`
   - **Reasoning:** `FR02-AI-014` evaluates the boundary condition of the 3rd attempt, while `FR02-AI-017` tests the state transition into `LOCKED`. Auditor should assess assertion differences.

3. **`FR02-AI-024` (Post-Lockout Expiration Account Usability):**
   - **Flag:** `POTENTIAL SPEC ASSUMPTION`
   - **Reasoning:** The test assumes that after lockout expiration and subsequent successful login, the internal failure counter starts completely fresh from 0. The human auditor should verify if this internal counter reset is explicitly documented in SRS or inferred from standard lifecycle behavior.

4. **`FR02-AI-028` (Sensitive Response Information Exclusion):**
   - **Flag:** `POTENTIAL SECURITY CLASSIFICATION QUESTION`
   - **Reasoning:** The test checks that plaintext password is omitted from the API JSON response (`[ADDITIONAL-SEC] / Clean Credential Handling`). Auditor must confirm that response omission is not conflated with SEC-01 (which mandates password hashing at rest in the database).

5. **`FR02-AI-030` & `FR02-AI-031` (Downstream JWT Usability Probes):**
   - **Flag:** `POTENTIAL SCOPE QUESTION`
   - **Reasoning:** These tests invoke `GET /api/orders/my-orders` to verify that the token issued by `POST /api/login` is usable and cryptographically valid. Auditor must evaluate whether downstream endpoint invocations are acceptable as supporting/indirect FR-02 tests or cross feature boundaries.

6. **`FR02-AI-036` (Response Content-Type Header Contract):**
   - **Flag:** `POTENTIAL ORACLE QUESTION`
   - **Reasoning:** Tests for `Content-Type: application/json` on all responses. Auditor should verify whether exact header matching is explicitly mandated by `api_specification.md` or is an industry best-practice inference.

7. **`FR02-AI-037` (Extraneous Request Body Properties Ingestion):**
   - **Flag:** `POTENTIAL ORACLE QUESTION`
   - **Reasoning:** Evaluates how the API treats unrecognized JSON fields and attempts to inject `"role": "admin"`. The specification does not specify whether extra properties should be rejected with HTTP 400 or silently ignored; the oracle asserts role non-escalation.

---

## 5. Coverage Gap Check

All required functional, boundary, state, security, and schema testing dimensions mandated by HW06 and the EShop SRS for FR-02 are represented in the raw AI-generated inventory:
- **Domain equivalence partitions:** Covered (`FR02-AI-001` .. `FR02-AI-012`)
- **Boundary value analysis:** Covered ($N=1, 2, 3$; $T=25\text{s}, 32\text{s}$)
- **State transitions & lifecycle:** Covered (`FR02-AI-015` .. `FR02-AI-024`)
- **Security & injection probes:** Covered (SEC-05, anti-enumeration, response sanitization, token isolation, SEC-02)
- **Schema & error contracts:** Covered (`FR02-AI-032` .. `FR02-AI-037`)

**Conclusion:** **No critical AI-generation coverage gap exists before Human Audit.**
