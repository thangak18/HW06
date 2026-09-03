# HW06 – API Testing – 23127259

- **Course:** Software Testing / Kiểm thử phần mềm
- **Assignment:** HW06 – API Testing (EShop SUT)
- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** 23127259
- **GitHub Account:** [thangak18](https://github.com/thangak18)
- **Repository:** [thangak18/HW06](https://github.com/thangak18/HW06)
- **Personal Branch:** `thang/hw06-implementation`

---

## 1. Selected Features Scope

| Pool | Feature ID | Feature Name | Primary Endpoint(s) | Role Gate |
|:---:|:---:|---|---|:---:|
| **A** | **FR-02** | Login and Account Lockout | `POST /api/login` | Public (generates JWT) |
| **B** | **FR-10** | Order State Machine | `PUT /api/admin/orders/:id/status`<br>`PUT /api/orders/:id/cancel`<br>`GET /api/orders/:id`<br>`GET /api/orders/my-orders` | User + Admin / Admin |
| **C** | **FR-14** | Category Management (CRUD) | `GET /api/categories`<br>`POST /api/categories`<br>`PUT /api/categories/:id`<br>`DELETE /api/categories/:id` | Public / Admin |

---

## 2. Test Accounting Standards

The assignment establishes a strict requirement of **≥ 35 AI-generated test cases** per selected feature, supplemented by **≥ 5 human-designed extension cases** per feature to address AI blind spots. Human-designed cases are accounted for strictly outside the AI total.

| Feature ID | Feature Description | AI Raw | AI Usable | Human | Formal | Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|
| **FR-02** | Login and Account Lockout | 37 | 35 | 5 | **40** | DONE |
| **FR-10** | Order State Machine | 42 | 41 | 5 | **46** | DONE |
| **FR-14** | Category Management CRUD | 42 | 40 | 6 | **46** | DONE |
| **TOTAL** | **All 3 Features** | **121** | **116** | **16** | **132** | DONE |

---

## 3. Implementation Phases Status Checklist

| Phase | Description | Status | Target Deliverables |
|:---:|---|:---:|---|
| **Phase 0** | Workspace, Tooling & SUT Environment Baseline | **COMPLETE** | Workspace layout, Newman/Postman readiness, Smoke check, SUT verification |
| **Phase 1** | FR-02 Full Pipeline (AI Test Generation, Audit, Newman, Bugs) | **COMPLETE (Technical) – PENDING_CODEX_VISUAL_AUDIT** | 37 raw AI + 5 Human cases, Newman HTML report, 3 bug reports |
| **Phase 2** | FR-10 Full Pipeline (AI Test Generation, Audit, Newman, Bugs) | **COMPLETE (Technical) – PENDING_CODEX_VISUAL_AUDIT** | 42 raw AI + 5 Human cases, Run04 canonical Newman, 3 bug reports |
| **Phase 3** | FR-14 Full Pipeline (AI Test Generation, Audit, Newman, Bugs) | **COMPLETE (Technical) – PENDING_CODEX_VISUAL_AUDIT** | 42 raw AI + 6 Human cases, Run01 canonical Newman, 4 confirmed root-cause bugs |
| **Phase 4** | CI/CD Integration (GitHub Actions Automated Newman Runs) | **COMPLETE (Technical) – PENDING_CODEX_VISUAL_AUDIT** | PASS run 33651923618 + deliberate FAIL run 33651923391 |
| **Phase 5** | Agent Skill (Self-Drawn Architecture & Pseudocode) | **COMPLETE (Content) – PENDING_CODEX_VISUAL_TASK** | Diagram spec in `docs/AI_TEST_GENERATOR_DIAGRAM_SPEC.md`, pseudocode in `docs/test_generator.md` |
| **Phase 6** | Final Documentation & AI Audit Report Compilation | **COMPLETE (Content) – PENDING_CODEX_VISUAL_AUDIT** | Main report, AI Audit, Commit log export, Excel workbook |

---

## 4. Video Demonstration

- **Video Link:** Not provided (optional assignment bonus).
- **Video Script & Checklist:** Located in `23127259/video/`

---

## 5. Self-Assessment & Evaluation Checklist (per assignment template)

| # | Requirement | Status | Notes |
|:---:|---|:---:|---|
| 1 | Three Pool A/B/C features selected and documented | DONE | FR-02 / FR-10 / FR-14 |
| 2 | ≥35 AI test cases per feature | DONE | 37 / 42 / 42 raw AI respectively |
| 3 | Human Audit of every AI case | DONE | `testcases/TC_AUDIT_FR*.md` |
| 4 | Gap analysis and ≥5 Human extensions per feature | DONE | 5 / 5 / 6 Human extensions (FR14 H07 was rejected as out-of-scope) |
| 5 | Postman collection with Newman execution | DONE | Three `.postman_collection.json` files; canonical Newman runs `FR02-Run03`, `FR10-Run04`, `FR14-Run01` |
| 6 | X-Student-Id on every HTTP operation | DONE | Static + runtime validation in `validate_*_collection.py` |
| 7 | Bug reports with GitHub Issues | DONE | FR02 #1/#2/#3, FR10 #29/#30/#31, FR14 #32/#33/#34/#36; #37 closed duplicate |
| 8 | CI/CD pipeline PASS/FAIL run | DONE (technical), PENDING screenshots | PASS [33651923618](https://github.com/thangak18/HW06/actions/runs/33651923618), FAIL [33651923391](https://github.com/thangak18/HW06/actions/runs/33651923391) |
| 9 | AI Audit Report (Markdown + PDF) | DONE (Markdown), PENDING_CODEX (PDF) | `ai/AI_AUDIT_REPORT.md` |
| 10 | AI Critique 200–300 words | DONE | `ai/AI_CRITIQUE.md` (programmatically counted) |
| 11 | AI test generator diagram | DONE (spec), PENDING_CODEX (visual) | `docs/AI_TEST_GENERATOR_DIAGRAM_SPEC.md` |
| 12 | Test generator pseudocode | DONE | `docs/test_generator.md` |
| 13 | Postman features list | DONE | `postman/POSTMAN_FEATURES_FR*.md` |
| 14 | Excel test cases workbook | DONE | `excel/HW06_Test_Cases.xlsx` (Cover + FR02/FR10/FR14 + Summary + Bugs) |
| 15 | Final main report (Markdown + PDF) | DONE (Markdown), PENDING_CODEX (PDF) | `00_MAIN_REPORT.md` |
| 16 | Git commit log per procedure step | DONE | `evidence/git_commit_log.txt` |
| 17 | Visual screenshots of Postman (Console / Runner / Bug / CI) | PENDING_CODEX_VISUAL_AUDIT | Delegated to Codex per division of responsibility |

---

## 6. Grader Navigation

| Need | Where to look |
|---|---|
| Final main report (Markdown) | [`23127259/00_MAIN_REPORT.md`](./00_MAIN_REPORT.md) |
| Final main report (PDF) | [`23127259/pdf/HW06_Main_Report.pdf`](./pdf/) – PENDING_CODEX_VISUAL_AUDIT |
| Feature audits | [`23127259/audit/FR02_FINAL_AUDIT.md`](./audit/) [`audit/FR10_FINAL_AUDIT.md`](./audit/) [`audit/FR14_FINAL_AUDIT.md`](./audit/) |
| Compliance matrix | [`23127259/audit/HW06_REQUIREMENTS_COMPLIANCE_MATRIX.md`](./audit/HW06_REQUIREMENTS_COMPLIANCE_MATRIX.md) |
| Per-feature test cases | [`23127259/testcases/`](./testcases/) |
| Postman collections | [`23127259/postman/collections/`](./postman/collections/) |
| Newman runs (CLI / JSON / HTML / exit) | [`23127259/evidence/fr02/newman/`](./evidence/fr02/newman/) [`evidence/fr10/newman/`](./evidence/fr10/newman/) [`evidence/fr14/newman/`](./evidence/fr14/newman/) |
| Bug reports | [`23127259/bugs/`](./bugs/) |
| GitHub Issues | FR02 #1/#2/#3, FR10 #29/#30/#31, FR14 #32/#33/#34/#36 (#37 closed duplicate) |
| AI audit | [`23127259/ai/AI_AUDIT_REPORT.md`](./ai/AI_AUDIT_REPORT.md) |
| AI critique | [`23127259/ai/AI_CRITIQUE.md`](./ai/AI_CRITIQUE.md) |
| Diagram specification | [`23127259/docs/AI_TEST_GENERATOR_DIAGRAM_SPEC.md`](./docs/AI_TEST_GENERATOR_DIAGRAM_SPEC.md) |
| CI/CD report | [`23127259/ci/CI_CD_REPORT.md`](./ci/CI_CD_REPORT.md) |
| Excel workbook | [`23127259/excel/HW06_Test_Cases.xlsx`](./excel/HW06_Test_Cases.xlsx) |
| Public-safe artifacts | [`23127259/evidence/*/newman/public-safe/`](./evidence/) |
| Visual handoff | [`23127259/audit/CODEX_VISUAL_HANDOFF.md`](./audit/CODEX_VISUAL_HANDOFF.md) |
| Final evidence manifest | [`23127259/evidence/FINAL_EVIDENCE_MANIFEST.md`](./evidence/FINAL_EVIDENCE_MANIFEST.md) |
| Checkpoint | [`23127259/audit/CURSOR_OPUS_PROGRESS_CHECKPOINT.md`](./audit/CURSOR_OPUS_PROGRESS_CHECKPOINT.md) |
| Git commit log | [`23127259/evidence/git_commit_log.txt`](./evidence/git_commit_log.txt) |

---

## 7. Visual Status

All visual evidence (Postman Console / Runner screenshots, CI PASS/FAIL
screenshots, bug screenshots, AI diagram, PDF page-by-page visual
inspection, Excel visual inspection) is intentionally
**PENDING_CODEX_VISUAL_AUDIT** as per the project division of
responsibility. A separate Codex agent performs the visual verification.

## 8. Status Declaration

`HW06_TECHNICALLY_READY_PENDING_CODEX_VISUAL_AUDIT`

No full submission readiness (`HW06_SUBMISSION_READY`) is claimed because
this report intentionally excludes visual verification.
