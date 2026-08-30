# HW06 – API Testing – Individual Workspace

## Student Information
- **Name:** TODO
- **Student ID:** TODO
- **GitHub Username:** TODO

---

## Selected APIs

| Pool | FR | Feature | Endpoint |
|---|---|---|---|
| **A** | TODO (e.g., FR-01) | TODO (e.g., Account registration) | `POST /api/auth/register` |
| **B** | TODO (e.g., FR-08) | TODO (e.g., Checkout) | `POST /api/checkout` |
| **C** | TODO (e.g., FR-14) | TODO (e.g., Category CRUD) | `POST /api/admin/categories` |

---

## Required Pipeline for Each API

Each selected API must complete the standard 5-step pipeline:

1. **AI Generate:** Prompt-driven generation of test cases (target **≥ 35 AI-generated test cases per API**).
2. **Human Audit:** Review and label every generated test case as `VALID`, `INVALID`, or `INCOMPLETE` with rationale.
3. **Human Extension:** Design and append **≥ 5 additional human-designed test cases per API** focusing on edge cases, security, and state transitions missed by the AI.
4. **Execute:** Execute via Postman & Newman with mandatory `X-Student-Id: {StudentID}` header.
5. **Bug Report:** File genuine bugs discovered during testing on GitHub Issues and in Markdown.

### Required Test Dimensions
- **Domain Partitions & Boundaries:** Input partition equivalence, length boundaries, type handling.
- **State Transitions:** Multi-step lifecycle flows, invalid state mutations.
- **Security (SEC-01 – SEC-07):** Auth, RBAC, SQLi/injection, IDOR, sensitive data, rate limiting/lockout, mass assignment.
- **Schema Validation:** Status codes, payload headers, response structure compliance.

---

## Postman / Newman

- **Postman Collection:** `postman/collections/`
- **Postman Environment:** `postman/environments/`
- **Data-Driven Files:** `postman/data/`
- **Pre-request / Test Scripts:** `postman/scripts/`
- **Newman HTML Extra Report:** `newman/`
- **Postman Features Exercised:**
  - [ ] Environments & Variables
  - [ ] Pre-request Scripts (`X-Student-Id` header injection)
  - [ ] Response Assertions & JSON Schema Validation
  - [ ] Collection Runner / Data-driven iteration (CSV/JSON)
  - [ ] Dynamic request chaining / Monitors / Mock servers

---

## CI/CD

- **CI/CD Configuration:** GitHub Actions workflow executing Newman automated runs.
- **Successful Pipeline Run:**
  - URL / Run ID: TODO
  - Screenshot: `ci/evidence/`
- **Failing Pipeline Run:**
  - URL / Run ID: TODO
  - Screenshot: `ci/evidence/`

---

## AI

- **AI Audit Report:** Located at [ai/audit/AI_AUDIT_TEMPLATE.md](./ai/audit/AI_AUDIT_TEMPLATE.md)
- **AI Critique (200–300 words):** Located at `ai/critique/ai_critique.md`
- **Agent Skill / AI-Driven Test Generator:**
  - Self-drawn Architecture Diagram: `agent-skill/diagram/`
  - Pseudocode / Script Implementation: `agent-skill/pseudocode/`
  - Demo Video (Optional): TODO

---

## Bugs

| Bug ID | Title / Endpoint | Severity | GitHub Issue Link | Status |
|---|---|---|---|---|
| BUG-01 | TODO | High / Medium / Low | TODO | Open / Confirmed |
| BUG-02 | TODO | High / Medium / Low | TODO | Open / Confirmed |

*Bug details and evidence screenshots are stored under `bugs/` and `bugs/screenshots/`.*

---

## Test Summary

| Metric | Count |
|---|---:|
| **APIs** | 3 |
| **AI-generated test cases** | TODO |
| **Human-added test cases** | TODO |
| **Total Test Cases** | TODO |
| **Executed** | TODO |
| **Passed** | TODO |
| **Failed** | TODO |
| **Bugs Discovered** | TODO |

---

## Self-Assessment

| No. | Criteria | Max Grade | Self-Assessed Grade |
|:---:|---|:---:|:---:|
| 1 | API 1 — full pipeline (generate + audit + extend + execute + bugs) | 30 | TODO |
| 2 | API 2 — full pipeline (same criteria) | 30 | TODO |
| 3 | API 3 — full pipeline (same criteria) | 30 | TODO |
| 4 | Agent Skills (AI-driven test generator design & pseudocode) | 10 | TODO |
| **Total** | | **100** | **TODO** |
