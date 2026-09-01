# Security Requirements Applicability Matrix

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Course:** HW06 – API Testing
- **Authoritative Standard:** EShop System Requirements Specification (SRS) Section 9

---

## 1. Security Applicability Matrix

The table below maps the official security requirements (**SEC-01** through **SEC-07**) against the three selected features: **FR-02** (Pool A: Login & Lockout), **FR-10** (Pool B: Order State Machine), and **FR-14** (Pool C: Category Management CRUD).

| SEC ID | Authoritative SRS Requirement | FR-02 (Login & Lockout) | FR-10 (Order State Machine) | FR-14 (Category CRUD) | Black-Box API Coverage Type | Engineering Rationale & Verification Boundaries |
|:---:|---|:---:|:---:|:---:|:---:|---|
| **SEC-01** | Passwords must **not** be stored in plaintext. | **APPLICABLE (PARTIAL)** | N/A | N/A | **PARTIAL** | Black-box API tests can probe registration/login responses to verify plaintext passwords are not leaked, but full verification of at-rest hashing requires authorized DB/source inspection. |
| **SEC-02** | Security-sensitive APIs must require a valid JWT token. | **APPLICABLE (FULL)** | **APPLICABLE (FULL)** | **APPLICABLE (FULL)** | **FULL** | Login (`POST /api/login`) generates the JWT. Modifying order states (`PUT /api/orders/:id/cancel`, `PUT /api/admin/orders/:id/status`), reading user orders (`GET /api/orders/my-orders`), and mutating categories (`POST/PUT/DELETE /api/categories`) must reject requests lacking a valid JWT with HTTP 401 Unauthorized. |
| **SEC-03** | Admin APIs must verify `role = 'admin'` in the token, not merely token existence. | N/A | **APPLICABLE (FULL)** | **APPLICABLE (FULL)** | **FULL** | Admin order transitions (`PUT /api/admin/orders/:id/status`) and category modifying endpoints (`POST/PUT/DELETE /api/categories`) must enforce `role = 'admin'` per SRS FR-12. Requests with valid user tokens (`role = 'user'`) must be rejected with HTTP 403 Forbidden. |
| **SEC-04** | User-controlled data displayed in the UI must be escaped correctly and must not be inserted through unsafe `innerHTML` usage. | N/A | N/A | N/A | **UI-SCOPED [UI-ONLY]** | SEC-04 applies to UI frontend rendering. Returning raw user-supplied strings in JSON responses is standard API behavior and does not constitute an XSS vulnerability without unsafe UI DOM insertion. Probing XSS payloads via API is categorized as an exploratory security probe. |
| **SEC-05** | Database queries must use parameterized queries rather than direct string concatenation. | **APPLICABLE (PARTIAL)** | **APPLICABLE (PARTIAL)** | **APPLICABLE (PARTIAL)** | **PARTIAL** | Submitting SQL injection payloads (e.g. `' OR '1'='1`) tests black-box behavioral resilience. However, lack of SQL syntax errors or payload rejection alone does not definitively prove parameterized queries are used (e.g. sanitizers/WAF could block inputs). Source inspection provides root-cause confirmation. |
| **SEC-06** | The profile-update API must not allow a client to change the `role` field. | N/A | N/A | N/A | **N/A TO SELECTED SCOPE** | Specifically targets `PUT /api/users/me` (FR-04), which is outside the student's selected feature scope (FR-02, FR-10, FR-14). Not forced into unrelated test suites. |
| **SEC-07** | Password-reset OTP must have sufficient entropy (minimum 6 digits), expire, and become invalid after use. | N/A | N/A | N/A | **N/A TO SELECTED SCOPE** | Specifically targets `POST /api/forgot-password` and `POST /api/reset-password` (FR-03), which is outside the student's selected feature scope. Not forced into unrelated test suites. |

---

## 2. Additional Security & Authorization Probes (`[ADDITIONAL-SEC]`)

Security and authorization aspects that do not map directly to a numbered SEC requirement are classified as **`[ADDITIONAL-SEC]`** to maintain strict terminology alignment with the SRS:

1. **Sensitive Data Exposure in Login Response (`FR02-HUM-005`):**
   - Assert that the successful login response object does not expose plaintext passwords in `response.user.password`.
2. **Horizontal Privilege Escalation / IDOR Probes (`FR10-HUM-004`):**
   - Assert that `GET /api/orders/:id` requires authentication and enforces ownership boundaries (per SRS FR-11: users must only view their own orders).
3. **Exploratory Injection String Reflection Probes (`FR14-AI-035`):**
   - Probe category name inputs with HTML/script strings to evaluate API storage and reflection behavior without prematurely claiming UI vulnerability.
