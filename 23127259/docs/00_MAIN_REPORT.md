# HW06 – API Testing Main Report

- **Course:** Software Testing / Kiểm thử phần mềm
- **Assignment:** HW06 – API Testing (EShop SUT)
- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** 23127259
- **GitHub Account:** [thangak18](https://github.com/thangak18)
- **Repository:** [thangak18/HW06](https://github.com/thangak18/HW06)
- **Branch:** `thang/hw06-implementation`

---

## 1. Executive Summary

- **Selected Features Scope:**
  1. **Pool A:** FR-02 – Login and Account Lockout (`POST /api/login`)
  2. **Pool B:** FR-10 – Order State Machine (`PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel`, `GET /api/orders/:id`, `GET /api/orders/my-orders`)
  3. **Pool C:** FR-14 – Category Management CRUD (`GET`, `POST`, `PUT`, `DELETE /api/categories`)
- **Total Test Cases Target:** $\ge 120\text{ total}$ ($\ge 35\text{ AI-generated} + \ge 5\text{ Human-designed} = \ge 40\text{ per feature}$)
- **Total Test Cases Executed:** `TODO – fill after Phase 1-3 execution`
- **Bugs Discovered & Verified:** `TODO – fill after real execution reproduction`
- **CI/CD Integration:** GitHub Actions Newman Runner (`.github/workflows/hw06-23127259-api-tests.yml`)

---

## 2. FR-02 Testing Pipeline (Pool A – Login & Account Lockout)

### 2.1 Specification & Endpoint Details
- **Feature Description:** Login authentication and brute-force account lockout mechanism per SRS FR-02.
- **Endpoint:** `POST /api/login`
- **Security Scope:** SEC-01 (partial), SEC-02 (full), SEC-05 (partial), `[ADDITIONAL-SEC]` sensitive data exclusion.

### 2.2 AI Test Generation ($\ge 35$ Cases: `FR02-AI-001..035`)
- `TODO – summarize AI-generated domain partitions, state transitions, security probes, and schema cases after Phase 1A`

### 2.3 Human Audit & Quality Classification
- `TODO – summarize audit matrix results (VALID / INVALID / INCOMPLETE counts and rationale from ai/TC_AUDIT_FR02.md)`

### 2.4 Human-Designed Extension Cases ($\ge 5$ Cases: `FR02-HUM-001..005`)
- `TODO – explain the 5 human cases and why AI generated tests missed these specific boundaries`

### 2.5 Real Execution Results & Defect Findings
- `TODO – attach Newman summary table, pass/fail statistics, and confirmed bug reports with reproduction evidence`

---

## 3. FR-10 Testing Pipeline (Pool B – Order State Machine)

### 3.1 Specification & State Machine Model
- **Feature Description:** Order lifecycle transitions (`pending → confirmed → shipping → delivered`, cancellations, final states) per SRS FR-10.
- **Endpoints:** `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel`, `GET /api/orders/:id`, `GET /api/orders/my-orders`.
- **Security Scope:** SEC-02 (full), SEC-03 (full role gate), `[ADDITIONAL-SEC]` cross-user order ownership.

### 3.2 AI Test Generation ($\ge 35$ Cases: `FR10-AI-001..035`)
- `TODO – summarize AI-generated valid/invalid transition cases after Phase 2A`

### 3.3 Human Audit & Quality Classification
- `TODO – summarize audit matrix results from ai/TC_AUDIT_FR10.md`

### 3.4 Human-Designed Extension Cases ($\ge 5$ Cases: `FR10-HUM-001..005`)
- `TODO – explain the 5 human cases and AI gap analysis`

### 3.5 Real Execution Results & Defect Findings
- `TODO – attach Newman execution findings and confirmed bug reports`

---

## 4. FR-14 Testing Pipeline (Pool C – Category Management CRUD)

### 4.1 Specification & CRUD Scope
- **Feature Description:** Category lifecycle management (Create, Read, Update, Delete) per SRS FR-14, FR-12 (Admin Role), and `api_specification.md`.
- **Target Endpoints:** `GET /api/categories` (Public), `POST /api/categories`, `PUT /api/categories/:id`, `DELETE /api/categories/:id`.
- **Security Scope:** SEC-01 (Authentication & Session Validity), SEC-02 (Authorization & RBAC), SEC-03 (Injection & XSS Protection), SEC-04 (IDOR), SEC-07 (Mass Assignment).

### 4.2 AI Test Generation (42 Cases: `TC-FR14-001..042`)
- **Generation Source:** `FR14_AI_DRAFT.md` (SHA-256: `95ac502b0880efcc1c6ceb040a1171eeacebff5c262a5f6df8d49a86cadcaf70`).
- **Target Count:** 42 raw AI test cases produced across 8 structured interactions (Happy path, SEC-01 auth, SEC-02 RBAC, name input validation, ID boundary validation, security probes, state transitions, schema validation), exceeding the $\ge 35$ minimum requirement by +20%.

### 4.3 Human Audit & Quality Classification
- **Audit Decision Matrix:** Documented in `ai/TC_AUDIT_FR14.md` and `testcases/FR14_HUMAN_AUDIT_CORRECTIONS.md`.
- **Audit Distribution:**
  - **`VALID`:** 39 cases (92.9%) approved as-is or with dual-assertion defect framing.
  - **`INCOMPLETE`:** 3 cases (7.1%) corrected before implementation (`TC-FR14-011` tampered JWT signature, `TC-FR14-020` 1001-character string generation, `TC-FR14-033` object body response handling).
  - **`INVALID`:** 0 cases (0%).
  - **Usable Cases After Audit:** 42 / 42 (100%).

### 4.4 Human-Designed Extension Cases (7 Cases: `TC-FR14-H01..H07`)
- **Extension Rationale:** Authored in `testcases/FR14_HUMAN_TEST_CASES.md` to cover blind spots overlooked by AI generation:
  - `TC-FR14-H01`: Missing `Content-Type` header protocol crash detection (Uncaught 500 error).
  - `TC-FR14-H02`: Zero-byte request body stream robustness.
  - `TC-FR14-H03`: Unsupported HTTP method (`PATCH`) route whitelisting.
  - `TC-FR14-H04`: Response header MIME type contract validation.
  - `TC-FR14-H05`: Silent data corruption via empty `{}` PUT body overwriting name to NULL.
  - `TC-FR14-H06`: Rapid sequential category creation stress and auto-increment monotonicity.
  - `TC-FR14-H07`: Foreign key orphaning verification on `/api/products` after category deletion.

### 4.5 Real Execution Results & Defect Findings
- **Execution Suite:** Postman Collection `FR14_Category_CRUD.postman_collection.json` executed via Newman CLI and HTML Extra reporter against active SUT (`http://localhost:3000`).
- **Newman Metrics:** 59 total requests executed, 96 assertions evaluated, 81 passing (84.4%), 15 failing (15.6%). 100% of failures correspond to intentional defect-confirming dual assertions.
- **Confirmed SUT Bugs (4 Defects):**
  1. [BUG-FR14-001](../bugs/BUG-FR14-001.md) (🔴 HIGH / SEC-02): Missing RBAC — Regular user (`role=user`) can create, update, and delete categories without restriction.
  2. [BUG-FR14-002](../bugs/BUG-FR14-002.md) (🟡 MEDIUM): Missing input validation — Empty string, null, whitespace, and missing `name` accepted.
  3. [BUG-FR14-003](../bugs/BUG-FR14-003.md) (🟡 MEDIUM): No existence checks — `PUT` and `DELETE` return 200 on non-existent category IDs.
  4. [BUG-FR14-004](../bugs/BUG-FR14-004.md) (🔴 HIGH): Unhandled server exception (HTTP 500 TypeError) when `Content-Type` header is omitted.
- **Master Bug Registry:** [`bugs/BUG_REGISTRY_FR14.md`](../bugs/BUG_REGISTRY_FR14.md).


---

## 5. Postman Advanced Features & CI/CD Pipeline

- **Attribution Evidence:** Collection-level `X-Student-Id: 23127259` pre-request script (Postman Console screenshot attached).
- **Postman Features:** Environments, collection variables, dynamic entity ID chaining, JSON schema validation (`tv4`/`ajv`), data-driven execution (`-d`).
- **CI/CD Automation (GitHub Actions):**
  - **Passing Workflow Run:** `TODO – add workflow URL and screenshot`
  - **Failing Demo Workflow Run:** `TODO – add workflow URL and screenshot`

---

## 6. Agent Skill Design (AI Test Generator)

- **Architecture Overview:** Self-drawn diagram (`agent-skill/diagram/agent-skill-design.png`).
- **Pseudocode Implementation:** `agent-skill/pseudocode/test_generator.md`.
- **Demonstration Video Link:** `TODO – record and upload video`

---

## 7. AI Critique & Evaluation

- `TODO – 200–300 words critical analysis grounded in real audit evidence from ai/TC_AUDIT_FR*.md`
