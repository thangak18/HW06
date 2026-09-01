# Postman Features & Architecture Document – FR-02

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

---

## 1. Postman Features Utilized in Phase 1D

This collection leverages standard, advanced Postman capabilities to achieve modularity, security, and traceability:

### 1.1 Hierarchical Collection Organization
- **Structured Folders:** The collection is structured into 7 logical folders:
  - `00 – Setup Helpers` (Deterministic account provisioning)
  - `01 – Positive Authentication` (Baseline login contracts)
  - `02 – Domain and Negative Inputs` (Equivalence partitions & missing/null inputs)
  - `03 – Lockout Boundary and State Progression` (N=1, N=2, N=3, active lock, timing)
  - `04 – Security and Token Integrity` (SQLi probes, response sanitization, JWT usability)
  - `05 – Schema and Contract Validation` (JSON structure, transport contracts)
  - `06 – Human Extensions` (Method enforcement, multi-vector SQLi, N=2 reset, account isolation, non-JSON MIME)

### 1.2 Multi-Tier Variable Scoping
- **Environment Variables (`FR02-local`):** Stores `baseUrl`, `studentId`, dedicated email fixtures, passwords, and dynamic tokens.
- **Dynamic Variables:** Employs `{{$timestamp}}` and `{{$randomInt}}` for generating unique collision-free test data.
- **Runtime Variables:** Captures generated tokens dynamically (`pm.environment.set("userToken", data.token)`) for downstream usability checks without hardcoding secret keys.

### 1.3 Automated Pre-request Scripts
- **Mandatory Header Enforcement:** A collection-level pre-request script automatically injects the student ID tracking header onto every request:
  ```javascript
  pm.request.headers.upsert({
      key: 'X-Student-Id',
      value: pm.environment.get('studentId') || '23127259'
  });
  ```
- **Safety Pre-condition Checks:** Validates that mandatory environment variables exist before executing requests.

### 1.4 Comprehensive Test Scripts & Oracles
- **Chai.js Assertions:** Implements `pm.test` assertions adhering strictly to the Human Audit verdicts:
  - Positive success assertions: status 200, JWT token structure, user object schema.
  - Neutral 4xx assertions: asserts authentication failure and token non-usability without overspecifying undocumented 400 vs 401 codes.
  - Security assertions: checks that response bodies omit sensitive password data and SQL exception traces.
  - Downstream integration checks: tests token authorization on `GET /api/orders/my-orders`.

### 1.5 Data-Driven Testing Capability
- External dataset [`postman/data/fr02-domain-data.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/data/fr02-domain-data.json) prepared for parameterized execution of domain equivalence partitions.

---

## 2. Postman Features Roadmap (Future Phases)
- **Newman CLI Runner:** Scheduled for Phase 1D.1.
- **Newman HTML/CLI Reporting:** Scheduled for Phase 1D.1.
- **CI/CD Integration (GitHub Actions):** Scheduled for Phase 3.
