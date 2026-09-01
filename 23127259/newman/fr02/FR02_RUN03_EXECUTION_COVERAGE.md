# FR-02 Newman Run 03 Execution Coverage & Request Reconciliation

- **Feature Under Test:** FR-02 – Login and Account Lockout (Pool A)
- **Execution Reference:** `FR02-run-03`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

---

## 1. Formal Test Case Execution Reconciliation (40 / 40 Formal IDs)

Every single one of the 40 formal test cases defined in the final audited suite was executed during Run 03.

| Formal Test ID | Test Name / Purpose | Executed? | Execution Type | Request / Sequence Steps | Assertions | Final Result |
|---|---|:---:|---|:---:|:---:|:---:|
| `FR02-AI-001` | Valid User Login | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-002` | Valid Admin Login | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-003` | Invalid Password on Registered User | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-004` | Unregistered Email Generic Failure | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-005` | Malformed Email Syntax Rejection | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-006` | Empty String Email Rejection | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-007` | Missing Email Property Payload | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-008` | Null Value Email Property Probe | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-009` | Whitespace-Only Email Input | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-010` | Empty String Password Input | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-011` | Missing Password Property Payload | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-012` | Null Value Password Property Probe | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-015` | Consecutive Failure Sequence Initiation N=1 | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-013` | Consecutive Failed Login Boundary N=2 | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-014` | Lockout Threshold Boundary N=3 | **YES** | Single Request | 1 | 1 | **PASS** |
| `FR02-AI-018` | Active Lockout Window Rejection Wrong Creds | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-019` | Active Lockout Window Rejection Valid Creds | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-020` | Pre-Expiration Timing Boundary T=25s | **YES** | Single Request | 1 | 1 | **PASS** |
| `FR02-AI-021` | Post-Expiration Timing Boundary T=32s | **YES** | Single Request | 1 | 1 | **FAIL (BUG)** |
| `FR02-AI-022` | Successful Login Resets Failure Progression | **YES** | Multi-Step Sequence | 2 (1 pre + 1 main) | 1 | **PASS** |
| `FR02-AI-023` | Consecutive Failure Semantics Verification | **YES** | Multi-Step Sequence | 3 (2 pre + 1 main) | 1 | **PASS** |
| `FR02-AI-024` | Post-Lockout Expiration Usability | **YES** | Single Request | 1 | 1 | **PASS** |
| `FR02-AI-025` | SQL Injection Probe in Email Field | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-026` | SQL Injection Probe in Password Field | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-027` | Cross-Response Equality Anti-Enumeration | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-028` | Sensitive Data Exclusion (Password Omission) | **YES** | Single Request | 1 | 1 | **FAIL (BUG)** |
| `FR02-AI-029` | Token Absence on Failed Authentication | **YES** | Single Request | 1 | 1 | **PASS** |
| `FR02-AI-030` | Downstream JWT Usability on Protected Route | **YES** | Single Request | 1 | 1 | **PASS** |
| `FR02-AI-031` | Downstream Tampered JWT Rejection | **YES** | Single Request | 1 | 1 | **PASS** |
| `FR02-AI-032` | Successful Login JSON Schema Contract | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-033` | Invalid Credentials Error Response Contract | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-034` | Locked-Account Error Response Contract | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-AI-035` | Syntactically Malformed JSON Transport | **YES** | Single Request | 1 | 1 | **PASS** |
| `FR02-AI-036` | Response Content-Type Header Contract | **YES** | Single Request | 1 | 1 | **PASS** |
| `FR02-AI-037` | Extraneous Body Role Injection | **YES** | Single Request | 1 | 1 | **PASS** |
| `FR02-HUM-001` | HTTP Verb Method Enforcement on Login | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-HUM-002` | Advanced SQLi Comment Truncation Probe | **YES** | Single Request | 1 | 2 | **PASS** |
| `FR02-HUM-003` | Consecutive Failure Reset at N=2 Boundary | **YES** | Multi-Step Sequence | 3 (2 pre + 1 main) | 1 | **FAIL (BUG)** |
| `FR02-HUM-004` | Lockout State Isolation Between Users | **YES** | Multi-Step Sequence | 4 (3 pre + 1 main) | 2 | **PASS** |
| `FR02-HUM-005` | Form-Encoded Request Body Contract | **YES** | Single Request | 1 | 1 | **FAIL (OBS)** |

---

## 2. Setup Helpers & Multi-Step Support Request Accounting

| Request / Helper ID | Request Name | Requests Count | Why Executed / Operational Purpose |
|---|---|:---:|---|
| `HELPER-000A` | Setup Baseline Regular User Account | 1 | Provisions fresh run-isolated `userEmail` |
| `HELPER-000B` | Setup Baseline Admin User Account | 1 | Provisions fresh run-isolated `adminEmail` |
| `HELPER-000C` | Setup Negative Domain User Account | 1 | Provisions fresh run-isolated `negativeUserEmail` |
| `HELPER-001` | Setup Account for Lockout Lifecycle | 1 | Provisions fresh run-isolated `lockoutEmail` |
| `HELPER-002` | Setup Account for Reset Boundary | 1 | Provisions fresh run-isolated `resetBoundaryEmail` |
| `HELPER-003` | Setup Dedicated Account for Human N=2 Reset | 1 | Provisions fresh run-isolated `humanResetEmail` |
| `HELPER-004` | Setup Account A for Isolation Test | 1 | Provisions fresh run-isolated `victimEmail` |
| `HELPER-005` | Setup Account B for Isolation Test | 1 | Provisions fresh run-isolated `isolatedEmail` |
| `FR02-AI-022 Pre` | Chained Setup Request in Pre-request | 1 | Sends 1 failure prior to main success request |
| `FR02-AI-023 Pre` | Chained Setup Requests in Pre-request | 2 | Sends 1 failure + 1 success prior to main failure request |
| `FR02-HUM-003 Pre`| Chained Setup Requests in Pre-request | 2 | Sends 2 failures prior to main valid login request |
| `FR02-HUM-004 Pre`| Chained Setup Requests in Pre-request | 3 | Sends 3 failures on Account A prior to main Account B request |
| **TOTAL HELPER & SUPPORT REQUESTS** | | **16** | |

---

## 3. Mathematical Reconciliation of Executed Requests

$$egin{aligned}
	ext{Total Newman Executed Requests} &= 	ext{Setup Helpers (Folder 00)} + 	ext{Single-Request Formal Tests} + 	ext{Multi-Step Sequence Requests} \
&= 8 + 36 + 12 \
&= 56 	ext{ Requests}
\end{aligned}$$

- **Formal Test Case Coverage Gate:** **40 / 40 Formal Test Cases (100.0% Executed)**.
- **Execution Gate Status:** **PASSED**.
