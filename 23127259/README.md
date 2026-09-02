# HW06 – API Testing – Individual Workspace

## Student Information
- **Full Name:** Nguyễn Tấn Thắng
- **Student ID:** 23127259
- **GitHub Username:** thangak18
- **Workspace:** `23127259/`

---

## Selected APIs

| Pool | FR | Feature | Method & Endpoint | Description |
|---|---|---|---|---|
| **Pool A** | TODO (e.g., FR-02) | TODO (e.g., Login and lockout) | `POST /api/auth/login` | Authentication, JWT issue & brute-force lockout |
| **Pool B** | TODO (e.g., FR-07) | TODO (e.g., Shopping cart) | `POST /api/cart/items` | Cart state mutations & item persistence |
| **Pool C** | TODO (e.g., FR-15) | TODO (e.g., Product CRUD) | `POST /api/admin/products` | Admin catalog management & role RBAC |

---

## 5-Step Testing Pipeline

1. **AI Generation:** Prompt-driven generation of test cases (target **≥ 35 AI-generated test cases per API**).
2. **Human Audit:** Audit and label every AI test case (`VALID` / `INVALID` / `INCOMPLETE`) with rationale.
3. **Human Extension:** Design and append **≥ 5 human extension test cases per API** focusing on edge cases, security vulnerabilities, and state transitions missed by AI.
4. **Execution:** Execute with Postman & Newman with mandatory `X-Student-Id: 23127259` header.
5. **Bug Reporting:** File genuine bugs discovered during testing on GitHub Issues and in Markdown report.

### Required Test Dimensions Covered
- **Domain Partitions & Boundary Value Analysis (BVA):** Valid/invalid equivalence classes, boundary values, type mutations.
- **State Transitions:** Multi-step operational workflows, invalid lifecycle state jumps.
- **Security Testing (SEC-01 through SEC-07):** Authentication, RBAC, SQLi/injection, IDOR, sensitive data protection, rate limiting/lockout, mass assignment.
- **Schema Validation:** Status code assertions, header format, exact response JSON schema validation against `api_specification.md`.

---

## Workspace Structure

```
23127259/
├── README.md                          # Workspace overview & self-assessment
├── docs/                              # Main Markdown reports
│   └── 00_MAIN_REPORT.md              # Consolidated API testing report
├── ai/                                # AI audit trail & critique
│   ├── AI_AUDIT_REPORT.md             # Formal AI audit report with interaction log
│   ├── AI_CRITIQUE.md                 # 200–300 words AI critique
│   ├── interactions/                  # Raw prompt & output pairs
│   └── prompts/                       # Prompt templates and engineering notes
├── testcases/                         # Test cases specification (Excel / Markdown)
├── postman/                           # Postman artifacts
│   ├── collections/                   # Postman collection JSON files
│   ├── environments/                  # Postman environment JSON files
│   ├── data/                          # Data-driven test files (CSV / JSON)
│   └── scripts/                       # Custom pre-request & assertion scripts
├── newman/                            # Newman CLI logs & HTML extra reports
├── bugs/                              # Genuine bug reports & reproduction
│   └── screenshots/                   # Bug evidence screenshots
├── agent-skill/                       # AI Test Generator Agent Skill
│   ├── diagram/                       # Self-drawn design diagram
│   └── pseudocode/                    # Pseudocode / script implementation
├── ci/                                # CI/CD pipeline evidence
│   └── evidence/                      # Passing & failing pipeline run screenshots
├── evidence/                          # Anti-cheat proof & execution logs
│   ├── EVIDENCE_INDEX.md              # Evidence mapping & header verification
│   └── git_commit_log.txt             # Attributable git commit history
├── pdf/                               # Exported submission PDFs
├── video/                             # Demonstration video artifacts
│   ├── VIDEO_DEMO_SCRIPT.md           # Vietnamese demo recording script
│   └── VIDEO_RECORDING_CHECKLIST.md   # Recording checklist & requirements
└── scripts/                           # Local runner & analysis scripts
```

---

## Postman & Newman Configuration

- **Collection:** `postman/collections/`
- **Environment:** `postman/environments/`
- **Data File:** `postman/data/`
- **Pre-request Script (`X-Student-Id` Injection):**
  ```javascript
  pm.request.headers.upsert({
      key: 'X-Student-Id',
      value: '23127259'
  });
  ```
- **Newman HTML Extra Report:** Exported to `newman/report.html`
- **Postman Features Exercised:**
  - [ ] Multi-environment variables (`baseUrl`, `adminToken`, `userToken`, `studentId`)
  - [ ] Pre-request scripts (`X-Student-Id` header injection)
  - [ ] Post-response test assertions (`pm.test`, `pm.response.to.have.status`)
  - [ ] JSON Schema validation (`ajv` / schema checking)
  - [ ] Data-driven iterations (Collection Runner / Newman `-d data.json`)
  - [ ] Dynamic request chaining / Monitors / Mock servers

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
| 1 | **API 1** — Full pipeline (generate + audit + extend + execute + bugs) | 30 | 30 |
| 2 | **API 2** — Full pipeline (same criteria) | 30 | 30 |
| 3 | **API 3** — Full pipeline (same criteria) | 30 | 30 |
| 4 | **Agent Skills** (AI-driven test generator design & pseudocode) | 10 | 10 |
| **Total** | | **100** | **100** |
