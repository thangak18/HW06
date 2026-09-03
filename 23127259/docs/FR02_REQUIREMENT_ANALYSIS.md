# FR-02 Requirement Analysis

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Assignment:** HW06 – API Testing
- **Analysis Stage:** Phase 1A.1 – Step-by-Step AI Test Design Foundation (Patched in 1A.2)
- **Authoritative Sources:**
  - 📋 **[SRS]** EShop System Requirements Specification (Section 2: FR-02; Section 9: SEC-01..07)
  - 🗂️ **[API-SPEC]** `api_specification.md` (Section 1.2: Đăng nhập)
  - 📜 **[PDF]** HW06 Assignment Specification & Guidance

---

## 1. Requirement Traceability

| Requirement Item | Authoritative Specification Rule | Source Reference |
|---|---|:---:|
| **Target Endpoint** | `POST /api/login` | 🗂️ [API-SPEC §1.2] |
| **Authentication Type** | Public entrypoint; generates and issues JWT Bearer token upon success | 📋 [SRS §2 FR-02] |
| **Input Fields** | `email` (string), `password` (string) in JSON body | 🗂️ [API-SPEC §1.2] |
| **Mandatory Fields** | Both `email` and `password` are logically required to authenticate | 📋 [SRS §2 FR-02] |
| **Success Condition** | Valid registered email matching correct password | 📋 [SRS §2 FR-02] |
| **Success Response** | HTTP 200 OK; returns JWT `token` string and `user` profile object | 🗂️ [API-SPEC §1.2] |
| **Failure Progression** | System increments consecutive failed attempt counter by **exactly 1** per failed attempt | 📋 [SRS §2 FR-02] |
| **Lockout Threshold** | If failed attempts reach **$\ge 3$ consecutive times**, account transitions to temporarily locked | 📋 [SRS §2 FR-02] |
| **Lockout Duration** | **30 seconds** in demo environment | 📋 [SRS §2 FR-02] |
| **Lockout Response** | Appropriate error notice indicating temporary lock without disclosing internal implementation details | 📋 [SRS §2 FR-02] |
| **Reset Rule** | Successful authentication resets the failure counter to 0 and clears lock status | 📋 [SRS §2 FR-02] |
| **Generic Failure Non-Disclosure** | Invalid credentials response must not disclose whether the email or password was incorrect | 📋 [SRS §2 FR-02] |
| **Downstream Token Contract** | Returned JWT must be accepted in `Authorization: Bearer <token>` on protected routes | 📋 [SRS §2 FR-02] |

---

## 2. Endpoint Contract

```http
POST /api/login
Host: localhost:3000
Content-Type: application/json
Accept: application/json

{
  "email": "user@domain.com",
  "password": "Password123!"
}
```

---

## 3. Parameter Inventory

| Parameter Name | Data Type | Requirement Status | Format Constraint | Semantic / Business Constraint | Boundary / Length Limits | Security Relevance |
|---|---|---|---|---|---|---|
| **`email`** | String (JSON) | Mandatory | Valid email syntax (`user@domain.com`) | Must correspond to an active, registered account in system | Minimum / Maximum length: **NOT SPECIFIED** in API spec | Injection probe vector (SQLi), credential enumeration vector |
| **`password`** | String (JSON) | Mandatory | Raw string (plain text over transport) | Must match password established during registration (FR-01) | Minimum / Maximum length on login: **NOT SPECIFIED** (Registration specifies min 8 chars, 1 upper, 1 lower, 1 digit, 1 special) | Sensitive credential, brute-force vector, plaintext exposure probe |

---

## 4. Equivalence Partitions

Equivalence partitions are defined on **independent single-parameter characteristics** rather than cross-parameter couplings. Cross-parameter combinations are evaluated during test-case generation.

| Parameter | Partition ID | Partition Description | Classification | Spec Basis | Future Test Need |
|---|---|---|:---:|---|---|
| **`email`** | **EP-EM-01** | Registered, syntactically valid email | Valid | 📋 [SRS FR-02] | Basis for valid authentication combinations |
| **`email`** | **EP-EM-02** | Unregistered, syntactically valid email | Invalid | 📋 [SRS FR-02] | Verify generic credential failure (no enumeration) |
| **`email`** | **EP-EM-03** | Malformed email syntax (missing `@` or domain) | Invalid | 📋 [SRS FR-02] | Verify validation error / generic 4xx rejection |
| **`email`** | **EP-EM-04** | Empty string (`""`) | Invalid | 📋 [SRS FR-02] | Verify missing input rejection |
| **`email`** | **EP-EM-05** | Missing key in JSON body (`{ "password": "..." }`) | Invalid | 🗂️ [API-SPEC] | Verify payload schema validation |
| **`email`** | **EP-EM-06** | `null` value in JSON body | Invalid | 🗂️ [API-SPEC] | Verify null pointer / type safety |
| **`email`** | **EP-EM-07** | Whitespace-only string (`"   "`) | Invalid | 📋 [SRS FR-02] | Verify whitespace trimming / rejection |
| **`email`** | **EP-EM-08** | Email casing variation (e.g. `TEST@ESHOP.COM`) | Exploratory | **NOT SPECIFIED** | Observe email case sensitivity behavior |
| **`email`** | **EP-EM-09** | SQL injection probe string (`' OR '1'='1`) | Invalid / Probe | 📋 [SRS §9 SEC-05] | Behavioral SQL injection probe (SEC-05) |
| **`password`** | **EP-PW-01** | Correct matching password for user | Valid | 📋 [SRS FR-02] | Basis for successful authentication |
| **`password`** | **EP-PW-02** | Incorrect password for user | Invalid | 📋 [SRS FR-02] | Verify generic rejection & failure counter increment |
| **`password`** | **EP-PW-03** | Empty string (`""`) | Invalid | 📋 [SRS FR-02] | Verify missing credential handling |
| **`password`** | **EP-PW-04** | Missing key in JSON body (`{ "email": "..." }`) | Invalid | 🗂️ [API-SPEC] | Verify payload schema validation |
| **`password`** | **EP-PW-05** | `null` value in JSON body | Invalid | 🗂️ [API-SPEC] | Verify null pointer / type safety |
| **`password`** | **EP-PW-06** | Whitespace-only string (`"   "`) | Invalid | 📋 [SRS FR-02] | Verify whitespace handling |
| **`password`** | **EP-PW-07** | Very long arbitrary string (1000+ characters) | Exploratory | **NOT SPECIFIED** | Verify buffer / parser resilience |
| **`password`** | **EP-PW-08** | SQL injection probe string (`' OR 1=1 --`) | Invalid / Probe | 📋 [SRS §9 SEC-05] | Behavioral SQL injection probe (SEC-05) |

---

## 5. Boundary Value Analysis

### 5.1 Failed Attempt Counter Progression Boundaries ($N=3$)

> [!NOTE]
> **Third-Failure Response Status Oracle:** The SRS explicitly states that after 3 consecutive failed attempts, the account transitions to **LOCKED**. However, whether failed request #3 itself returns an ordinary credential error (HTTP 401) or an immediate lockout response (HTTP 403) is **NOT SPECIFIED** in the specification text. The authoritative oracle guarantees state transition to LOCKED on attempt 3, and guarantees rejection of subsequent requests during the 30s window.

| Boundary Metric | Just Below Boundary ($N-1$) | At Boundary ($N$) | Just Above Boundary ($N+1$) | Authoritative Expected State | Source Reference |
|---|---|---|---|---|:---:|
| **Consecutive Failures ($N=3$)** | **2 Failures ($N=2$):** Account remains **UNLOCKED**; returns generic credential failure (HTTP 4xx). | **3 Failures ($N=3$):** Account transitions to **LOCKED**; response status on request #3 is **NOT SPECIFIED** (401 or 403), but state becomes LOCKED. | **4 Failures / Next Request:** Account is **LOCKED**; request during lock window is rejected with temporary lockout notice. | State transition to temporary lockout activates strictly upon 3rd consecutive failure. | 📋 [SRS §2 FR-02] |

### 5.2 Lockout Duration Timing Boundaries (30 Seconds Window)

| Timing Boundary | Just Before Expiry ($T < 30\text{s}$) | Around Expiry ($T \approx 30\text{s}$) | Just After Expiry ($T > 30\text{s}$) | Authoritative Expected State | Source Reference |
|---|---|---|---|---|:---:|
| **Lockout Expiration ($T=30\text{s}$)** | **$T = 25\text{s}$:** Login attempt rejected with locked status. | **$T = 30\text{s}$:** Boundary transition from locked to unlocked. | **$T = 32\text{s}$:** Account is **UNLOCKED**; valid credentials authenticate successfully (200 OK). | Account automatically unlocks once 30 seconds have elapsed. | 📋 [SRS §2 FR-02] |

---

## 6. Specification State Model

```
                    ┌─────────────────────────┐
                    │         NORMAL          │ ◄──────────────────────┐
                    │ (attempts=0, unlocked)  │                        │
                    └───────────┬─────────────┘                        │
                                │                                      │
              1st / 2nd Failure │                                      │ Success on correct credentials
         (Increment attempts+1) │                                      │ (attempts reset to 0)
                                ▼                                      │
                    ┌─────────────────────────┐                        │
                    │       ACCUMULATING      │                        │
                    │ (attempts=1..2,unlocked)│                        │
                    └───────────┬─────────────┘                        │
                                │                                      │
                    3rd Failure │ (State transitions to LOCKED;        │
           (Threshold reached)  │  response code NOT SPECIFIED)        │
                                ▼                                      │
                    ┌─────────────────────────┐                        │
                    │         LOCKED          │                        │
                    │ (temporary 30s window)  │                        │
                    └───────────┬─────────────┘                        │
                                │                                      │
                30s Window Pass │ (Auto-unlock)                        │
                                ▼                                      │
                    ┌─────────────────────────┐                        │
                    │      LOCK_EXPIRED       │                        │
                    │  (ready for auth retry) ├────────────────────────┘
                    └─────────────────────────┘
```

### State Definition Table

| State Name | State Description | Triggering Event | Expected Response Class | Next State |
|---|---|---|---|---|
| **`NORMAL`** | Initial baseline state (zero failed attempts). | Valid login | HTTP 200 OK + JWT | `NORMAL` |
| **`NORMAL`** | Initial baseline state. | 1st invalid login | Generic 4xx error | `ACCUMULATING` (attempts=1) |
| **`ACCUMULATING`** | 1 or 2 failed attempts recorded. | 2nd invalid login | Generic 4xx error | `ACCUMULATING` (attempts=2) |
| **`ACCUMULATING`** | 2 failed attempts recorded. | 3rd invalid login | Generic 4xx or Lockout error (Status: NOT SPECIFIED) | `LOCKED` |
| **`LOCKED`** | Account in active 30s lockout. | Any login attempt (valid or invalid) | 4xx Lockout error | `LOCKED` |
| **`LOCKED`** | Account in active 30s lockout. | Time elapses ($> 30\text{s}$) | N/A (Internal timer) | `LOCK_EXPIRED` |
| **`LOCK_EXPIRED`** | Lock window passed; awaiting retry. | Valid login | HTTP 200 OK + JWT | `NORMAL` (reset counter) |

---

## 7. Response Schema Analysis

Based strictly on `api_specification.md` Section 1.2 and SRS requirements:

### 7.1 Successful Login Response (HTTP 200 OK)
- **Documented Fields:**
  - `token`: String (Valid JWT format: `header.payload.signature`)
  - `user`: Object (User profile information)
  - `message`: String (e.g. `"Login successful"`)
- **Type Constraints:**
  - `token` must be a non-empty string.
  - `user` must be an object containing user attributes.
- **Sensitive Data Constraint:** Per security principles, the `user` object should **not** expose sensitive fields like `password` in plain text.

### 7.2 Invalid Credentials Response (HTTP 4xx)
- **Documented Status:** HTTP 401 Unauthorized (or general 4xx)
- **Top-Level Fields:** JSON object containing error information (e.g. `error` or `message` string)
- **Semantic Rule:** Must return generic message without revealing which credential failed.

### 7.3 Locked Account Response (HTTP 4xx)
- **Documented Status:** HTTP 403 Forbidden / 429 / 4xx (Exact code for request #3 vs subsequent: NOT SPECIFIED)
- **Top-Level Fields:** JSON object containing lockout error message
- **Semantic Rule:** Clearly informs user of temporary lock without disclosing internal variables or stack traces.

---

## 8. Security Applicability

| SEC ID | Authoritative Definition | Relevance to FR-02 | Verification Scope & Black-Box Limitations |
|:---:|---|:---:|---|
| **SEC-01** | Passwords must **not** be stored in plaintext. | **PARTIALLY APPLICABLE** | Black-box API tests can probe responses during registration/login to verify plain text passwords are not leaked, but full verification of hashing at rest requires DB/source inspection. |
| **SEC-02** | Security-sensitive APIs must require a valid JWT. | **INDIRECT / AUTHENTICATION DEPENDENCY** | `POST /api/login` itself does not require a JWT; it issues the JWT that protected endpoints later consume. Downstream protected-endpoint probes may validate token usability, but they are not the primary behavioral contract of `POST /api/login`. |
| **SEC-03** | Admin APIs must validate `role = 'admin'`. | **NOT APPLICABLE TO FR-02** | Login endpoint is public and authenticates both standard users and admins. (Role enforcement applies to FR-10 and FR-14). |
| **SEC-04** | User-controlled data in UI must be escaped. | **UI-SCOPED [UI-ONLY]** | Applies to HTML DOM rendering in frontend. Not directly testable via raw backend API JSON responses. |
| **SEC-05** | Database queries must use parameterized queries. | **PARTIALLY APPLICABLE** | SQL injection probes in `email` and `password` fields test black-box resilience. Payload rejection alone provides behavioral evidence; source code confirms parameterization. |
| **SEC-06** | Profile update must not allow role changes. | **NOT APPLICABLE TO FR-02** | Targets `PUT /api/users/me` (FR-04), outside FR-02 scope. |
| **SEC-07** | OTP must have entropy, expire, single-use. | **NOT APPLICABLE TO FR-02** | Targets password reset flow (FR-03), outside FR-02 scope. |

### Additional Security Dimensions for FR-02 (`[ADDITIONAL-SEC]`)
1. **Sensitive Data Exposure Probe:** Explicitly assert that successful login response does not echo the plaintext password back in the response body.
2. **Credential Enumeration Prevention:** Assert that non-existent email and wrong password for existing email yield identical generic error messages.

---

## 9. Open / Undefined Specification Questions

The following boundaries and behaviors are **NOT SPECIFIED** in the authoritative SRS or `api_specification.md` and are noted as exploratory points:

1. **Email Case Sensitivity:** Does the system treat `User@Domain.Com` as identical to `user@domain.com`? *(Label: EXPLORATORY)*
2. **Maximum String Lengths:** What is the maximum acceptable length for email and password on the login endpoint? *(Label: NOT SPECIFIED)*
3. **Leading/Trailing Whitespace:** Are leading and trailing spaces trimmed from email inputs automatically? *(Label: EXPLORATORY)*
4. **JWT Expiration Claim (`exp`):** Is JWT token lifetime bounded by an explicit expiration window in the demo environment? *(Label: NOT SPECIFIED)*
5. **Exact HTTP Status on 3rd Failed Attempt:** Whether attempt #3 returns 401 (credential error) or 403 (lockout notice) immediately. *(Label: NOT SPECIFIED)*

---

## 10. Inputs for Next AI Generation Stage

The partitions, state transitions, boundaries, and security rules established in this document provide the direct inputs for generating the $\ge 35\text{ AI-generated test cases}$ (`FR02-AI-001..035`) across Phase 1A stages:

- **Stage 1A.2 (This stage):** Domain Partitions & Boundary Cases (`FR02-AI-001..014`, $\sim 14\text{ test cases}$)
- **Stage 1A.3 (Next stage):** Lockout State Machine & Timing Cases (`FR02-AI-015..024`, $\sim 10\text{ test cases}$)
- **Stage 1A.4 (Subsequent):** Security & Schema Probes (`FR02-AI-025..035`, $\sim 11\text{ test cases}$)
- **Total AI Generation Target:** $\ge 35\text{ structured cases}$
