# HW06 – API Testing: Assignment Notes & Requirements Reference

This document summarizes the core guidelines, technical specifications, and evaluation criteria for **HW06 – API Testing**.

---

## 1. General Overview

| Item | Details |
|---|---|
| **Exercise ID** | HW06-AI |
| **Form** | Individual Assignment (Shared team repository for organization) |
| **System Under Test (SUT)** | EShop ([https://github.com/ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut)) |
| **AI Policy** | Open — Mandatory AI declaration and attached AI Audit Report |
| **Bloom-AI Level** | G9.2 (Apply), G9.3 (Analyse), G9.4 (Collaborate), G9.5 (Create) |

---

## 2. Core Guiding Principles

1. **AI-First Strategy:** Drive AI systematically through testing techniques (domain partitions, state transitions, security, schema validation) rather than single generic prompts.
2. **Human Review & Responsibility:** Every AI output must be audited and labeled (`VALID`, `INVALID`, `INCOMPLETE`). The student is solely responsible for test correctness.
3. **AI Audit Trail:** Complete recording of prompts, timestamps, outputs, and revisions in text/Markdown format.
4. **Attributable Execution:** All test requests must carry the `X-Student-Id: {StudentID}` header.
5. **Quality over Completion:** Evaluated on rigor, thoroughness of test dimensions, bug findings, and clean CI/CD evidence.

---

## 3. Feature Pools & API Selection Rules

Each student must select **three (3) distinct APIs**:
- **1 API from Pool A**
- **1 API from Pool B**
- **1 API from Pool C**
*(Note: Pool D — Mobile App is excluded because this homework targets the backend REST API).*

### Pool A — Authentication, Categories, and Products
- **FR-01:** Account registration (`POST /api/auth/register`)
- **FR-02:** Login and account lockout (`POST /api/auth/login`)
- **FR-03:** Forgot password & password reset (two steps: `POST /api/auth/forgot-password`, `POST /api/auth/reset-password`)
- **FR-04:** Personal profile management (`GET /api/user/profile`, `PUT /api/user/profile`, `PUT /api/user/change-password`)
- **FR-05:** Product listing and search (`GET /api/products`, `GET /api/products/search`)
- **FR-06:** Product detail view (`GET /api/products/:id`)

### Pool B — Shopping Cart and Checkout
- **FR-07:** Shopping cart (`GET /api/cart`, `POST /api/cart/items`, `PUT /api/cart/items/:id`, `DELETE /api/cart/items/:id`)
- **FR-08:** Checkout (`POST /api/checkout`, `POST /api/checkout/calculate`)
- **FR-09:** Discount coupons (`POST /api/coupons/apply`, `GET /api/coupons/validate`)
- **FR-10:** Order state machine (`GET /api/orders/:id/status`, `POST /api/orders/:id/transition`, `POST /api/orders/:id/cancel`)
- **FR-11:** Order history view (user) (`GET /api/orders`, `GET /api/orders/:id`)

### Pool C — Web Admin
- **FR-12:** Access control (`/api/admin/*` role verification, RBAC)
- **FR-13:** Dashboard statistics (`GET /api/admin/dashboard/stats`, `GET /api/admin/dashboard/revenue`)
- **FR-14:** Category management CRUD (`POST /api/admin/categories`, `PUT /api/admin/categories/:id`, `DELETE /api/admin/categories/:id`)
- **FR-15:** Product management CRUD (`POST /api/admin/products`, `PUT /api/admin/products/:id`, `DELETE /api/admin/products/:id`)
- **FR-16:** Product import from CSV (`POST /api/admin/products/import-csv`)
- **FR-17:** Coupon management CRUD (`POST /api/admin/coupons`, `PUT /api/admin/coupons/:id`, `DELETE /api/admin/coupons/:id`)
- **FR-18:** Order management admin (`GET /api/admin/orders`, `PUT /api/admin/orders/:id/status`)
- **FR-19:** User management admin (`GET /api/admin/users`, `PUT /api/admin/users/:id/status`, `PUT /api/admin/users/:id/role`)

---

## 4. 5-Step Pipeline Required for Each Selected API

```
   +--------------------+
   | 1. AI Generate     | --> Target: >= 35 test cases per API (guided step-by-step)
   +--------------------+
             |
             v
   +--------------------+
   | 2. Human Audit     | --> Label VALID / INVALID / INCOMPLETE + corrective actions
   +--------------------+
             |
             v
   +--------------------+
   | 3. Human Extend    | --> Add >= 5 test cases missed by AI (security/state edge cases)
   +--------------------+
             |
             v
   +--------------------+
   | 4. Execute         | --> Postman + Newman CLI/HTML runner with X-Student-Id header
   +--------------------+
             |
             v
   +--------------------+
   | 5. Report Bugs     | --> Log genuine bugs in Markdown + GitHub Issues with screenshots
   +--------------------+
```

### Required Test Dimensions
1. **Domain Partitions & Boundaries:** Valid/invalid partitions for all parameters (e.g., email format, boundary lengths, negative numbers, empty payloads).
2. **State Transitions:** State changes, invalid sequence transitions (e.g., transition rules for orders, cart mutations, lockout triggers).
3. **Security Requirements (SEC-01 – SEC-07):**
   - SEC-01: Authentication & Session validity
   - SEC-02: Authorization & Role-based Access Control (RBAC / Privilege escalation)
   - SEC-03: Input sanitization & Injection protection (SQLi, NoSQLi, XSS)
   - SEC-04: Insecure Direct Object References (IDOR)
   - SEC-05: Sensitive data exposure & masking
   - SEC-06: Rate limiting & Brute force protection / Lockout
   - SEC-07: Mass assignment & parameter tampering
4. **Schema Validation:** Status code assertions, header format, exact response JSON schema validation against `api_specification.md`.

---

## 5. Technical Requirements

### Postman Features to Exercise
- [ ] Multi-environment variables (`baseUrl`, `adminToken`, `userToken`, `studentId`)
- [ ] Pre-request scripts (dynamic data generation, timestamping, mandatory `X-Student-Id` header injection)
- [ ] Post-response test assertions (`pm.test`, `pm.response.to.have.status`, JSON Schema validation using `ajv` or `tv4`)
- [ ] Data-driven testing (Newman / Collection Runner with CSV or JSON data files)
- [ ] Optional: Dynamic request chaining (`pm.collectionVariables.set`, `postman.setNextRequest`), monitors, or mock servers.

### CI/CD Pipeline Requirements
- GitHub Actions workflow running Newman against the SUT.
- Two distinct runs documented with links and screenshots:
  1. **Pass Run:** 100% tests passing on working endpoints.
  2. **Fail Run:** Demonstrating a test failure on invalid behavior / edge case detection.

### Agent Skill / AI-Driven Test Generator (Level G9.5)
- Design an automated AI-driven API test generator that produces test cases from an API specification.
- Required: **Self-drawn architecture diagram** (draw.io, Excalidraw, Mermaid) + **Pseudocode** (`.md` / `.py`).
- Optional/Bonus: Reusable Agent Skill implementation with YouTube demo video link.

---

## 6. Anti-AI-Cheat Constraints

Graders will strictly inspect evidence for:
1. **Header Verification:** Real execution showing `X-Student-Id: {StudentID}` in Postman console / Newman logs.
2. **Execution Environment:** Newman hostname matching localhost/127.0.0.1 or active deployment.
3. **Human Diagram:** Self-drawn design diagram (not raw AI image generation).
4. **Independent Work:** Zero plagiarism across group members and cohorts.

---

## 7. Grading Matrix (100 Points Total)

| No. | Criteria | Max Points |
|:---:|---|:---:|
| 1 | **API 1** — Full pipeline (Generate + Audit + Extend + Execute + Bugs) | 30 |
| 2 | **API 2** — Full pipeline (Generate + Audit + Extend + Execute + Bugs) | 30 |
| 3 | **API 3** — Full pipeline (Generate + Audit + Extend + Execute + Bugs) | 30 |
| 4 | **Agent Skill** — AI-driven test generator design (Diagram + Pseudocode) | 10 |
| **Total** | | **100** |
