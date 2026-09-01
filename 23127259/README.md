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

| Feature ID | Feature Description | AI Target | Human Extension Target | Final Minimum Total | Status |
|:---:|---|:---:|:---:|:---:|:---:|
| **FR-02** | Login and Account Lockout | $\ge 35$ (`FR02-AI-001..035`) | $\ge 5$ (`FR02-HUM-001..005`) | $\ge 40$ | Planned |
| **FR-10** | Order State Machine | $\ge 35$ (`FR10-AI-001..035`) | $\ge 5$ (`FR10-HUM-001..005`) | $\ge 40$ | Planned |
| **FR-14** | Category Management CRUD | $\ge 35$ (`FR14-AI-001..035`) | $\ge 5$ (`FR14-HUM-001..005`) | $\ge 40$ | Planned |
| **TOTAL** | **All 3 Features** | **$\ge 105$** | **$\ge 15$** | **$\ge 120$** | **Planned** |

---

## 3. Implementation Phases Status Checklist

| Phase | Description | Status | Target Deliverables |
|:---:|---|:---:|---|
| **Phase 0** | Workspace, Tooling & SUT Environment Baseline | **COMPLETE** | Workspace layout, Newman/Postman readiness, Smoke check, SUT verification |
| **Phase 1** | FR-02 Full Pipeline (AI Test Generation, Audit, Newman, Bugs) | **NOT STARTED** | $\ge 35$ AI + $\ge 5$ Human cases, HTML Newman report, Bug candidate evidence |
| **Phase 2** | FR-10 Full Pipeline (AI Test Generation, Audit, Newman, Bugs) | **NOT STARTED** | $\ge 35$ AI + $\ge 5$ Human cases, State matrix tests, Newman report |
| **Phase 3** | FR-14 Full Pipeline (AI Test Generation, Audit, Newman, Bugs) | **NOT STARTED** | $\ge 35$ AI + $\ge 5$ Human cases, CRUD tests, Newman report |
| **Phase 4** | CI/CD Integration (GitHub Actions Automated Newman Runs) | **NOT STARTED** | Passing run & failing demo workflow evidence URLs/screenshots |
| **Phase 5** | Agent Skill (Self-Drawn Architecture & Pseudocode) | **NOT STARTED** | Self-drawn architecture diagram, Test generator pseudocode |
| **Phase 6** | Final Documentation & AI Audit Report Compilation | **NOT STARTED** | Main Report PDF, AI Audit PDF, Commit log export, Video demo |

---

## 4. Video Demonstration

- **Video Link:** `TODO – record and upload video during final phase`
- **Video Script & Checklist:** Located in `23127259/video/`

---

## 5. Self-Assessment & Evaluation Checklist

- [x] Workspace properly isolated under `23127259/` with no cross-member pollution
- [x] SUT execution baseline confirmed and smoke-tested on `http://localhost:3000`
- [x] Global `X-Student-Id: 23127259` attribution mechanism configured
- [x] AI Audit tracking established from initial planning interactions
- [ ] Test cases generated ($\ge 120$ total: $\ge 105$ AI + $\ge 15$ Human) across all 3 pools *(Phase 1–3)*
- [ ] Newman HTML execution reports generated *(Phase 1–3)*
- [ ] CI/CD automated execution pipelines passing & failing demonstrated *(Phase 4)*
- [ ] Agent Skill self-drawn design & pseudocode committed *(Phase 5)*
- [ ] Main report & AI Audit report completed and exported to PDF *(Phase 6)*
