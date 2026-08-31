# HW06 – API Testing – Individual Workspace

## Student Information
- **Full Name:** TODO
- **Student ID:** TODO
- **GitHub Username:** TODO
- **Workspace:** `member-2/`

---

## Selected APIs

| Pool | FR | Feature | Method & Endpoint | Description |
|---|---|---|---|---|
| **Pool A** | TODO (e.g., FR-01) | TODO (e.g., Account registration) | `POST /api/auth/register` | Registration validation & duplicate prevention |
| **Pool B** | TODO (e.g., FR-08) | TODO (e.g., Checkout) | `POST /api/checkout` | Order calculation, stock decrement & checkout |
| **Pool C** | TODO (e.g., FR-14) | TODO (e.g., Category CRUD) | `POST /api/admin/categories` | Admin category management & hierarchy validation |

---

## 5-Step Testing Pipeline

1. **AI Generation:** Prompt-driven generation of test cases (target **≥ 35 AI-generated test cases per API**).
2. **Human Audit:** Audit and label every AI test case (`VALID` / `INVALID` / `INCOMPLETE`) with rationale.
3. **Human Extension:** Design and append **≥ 5 human extension test cases per API** focusing on edge cases, security vulnerabilities, and state transitions missed by AI.
4. **Execution:** Execute with Postman & Newman with mandatory `X-Student-Id: {StudentID}` header.
5. **Bug Reporting:** File genuine bugs discovered during testing on GitHub Issues and in Markdown report.

---

## Postman & Newman Configuration

- **Collection:** `postman/collections/`
- **Environment:** `postman/environments/`
- **Data File:** `postman/data/`
- **Pre-request Script (`X-Student-Id` Injection):**
  ```javascript
  pm.request.headers.upsert({
      key: 'X-Student-Id',
      value: pm.environment.get('studentId') || 'TODO'
  });
  ```
- **Newman HTML Extra Report:** Exported to `newman/report.html`

---

## CI/CD Pipeline Runs

- **Workflow File:** `.github/workflows/`
- **Successful Pipeline Run:**
  - Run URL / ID: TODO
  - Evidence: `ci/evidence/passing_run.png`
- **Failing Pipeline Run:**
  - Run URL / ID: TODO
  - Evidence: `ci/evidence/failing_run.png`

---

## Test Summary

| Metric | Count |
|---|---:|
| **APIs Tested** | 3 |
| **AI-Generated Test Cases** | TODO |
| **Human-Added Extension Cases** | TODO |
| **Total Test Cases** | TODO |
| **Executed** | TODO |
| **Passed** | TODO |
| **Failed** | TODO |
| **Bugs Discovered** | TODO |
| **Demo Video Link (Unlisted YouTube)** | TODO |

---

## Self-Assessment

| No. | Assessment Criteria | Max Grade | Self-Assessed Grade |
|:---:|---|:---:|:---:|
| 1 | **API 1** — Full pipeline (generate + audit + extend + execute + bugs) | 30 | TODO |
| 2 | **API 2** — Full pipeline (same criteria) | 30 | TODO |
| 3 | **API 3** — Full pipeline (same criteria) | 30 | TODO |
| 4 | **Agent Skills** (AI-driven test generator design & pseudocode) | 10 | TODO |
| **Total** | | **100** | **TODO** |
