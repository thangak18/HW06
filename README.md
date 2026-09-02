# HW06 – API Testing

## Assignment Information
- **Course Homework:** HW06 – API Testing
- **Exercise ID:** HW06-AI
- **System Under Test (SUT):** EShop ([https://github.com/ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut))
- **Testing Tech Stack:**
  - **API Specification:** OpenAPI / `api_specification.md`
  - **Design & Scripting:** Postman v10+ / v11+
  - **Automated Execution:** Newman (`newman-reporter-htmlextra`)
  - **CI/CD Integration:** GitHub Actions
  - **AI-Assisted Testing:** Prompt Engineering, Audit Verification, BVA/Partitions, SEC-01–SEC-07, and Agent Skills

---

## Team Organization & Individual Isolation Policy

> **Note on Individual Submission:**  
> This homework is an individual assignment. Group members use one shared GitHub repository for source-control organization. Each student's deliverables, reports, test collections, AI audit trails, and execution evidence are strictly isolated under their own workspace directory.

### Team Allocation Matrix

> ⚠ **Ràng buộc §5 của đề bài:** không hai thành viên nào được chọn trùng bộ 3 API.
> Thành viên 23127195 đã chốt **FR-04 / FR-09 / FR-16**; hai thành viên còn lại cần điền và đối chiếu.

| Member | Full Name | Student ID | GitHub Handle | Pool A (Auth / Catalog) | Pool B (Cart / Order) | Pool C (Admin) | Personal Workspace |
|---|---|---|---|---|---|---|---|
| **Member 1** | Nguyễn Tấn Thắng | 23127259 | @thangak18 | TODO | TODO | TODO | [`23127259/`](./23127259/) |
| **Member 2** | Ninh Văn Khải | 23127060 | @nvkhai238 | **FR-03** — Quên & đặt lại mật khẩu<br>`POST /api/forgot-password`<br>`POST /api/reset-password` | **FR-08** — Thanh toán<br>`POST /api/checkout` | **FR-15** — Quản lý sản phẩm<br>`POST/PUT/DELETE /api/products` | [`23127060/`](./23127060/) |
| **Member 3** | TODO | 23127195 | @hungtmh | **FR-04** — Hồ sơ cá nhân<br>`GET/PUT /api/users/me` | **FR-09** — Mã giảm giá<br>`POST /api/apply-coupon` | **FR-16** — Import sản phẩm<br>`POST /api/admin/import-products` | [`23127195/`](./23127195/) |

---

## Repository Layout (HW05 Standard)

```
HW06/
├── README.md                          # Root assignment README & team coordination matrix
├── .gitignore                         # System & build ignore rules
├── docs/                              # Shared assignment notes & allocation matrix
│   ├── assignment-notes.md            # HW06 assignment rules & rubrics
│   └── team-api-allocation.md         # 3-API allocation tracking per member
├── 23127259/                          # Nguyễn Tấn Thắng individual workspace
│   ├── README.md                      # Student workspace README & Self-Assessment
│   ├── docs/                          # Main Markdown reports (00_MAIN_REPORT.md)
│   ├── ai/                            # AI interaction archive & critique
│   │   ├── AI_AUDIT_REPORT.md
│   │   ├── AI_CRITIQUE.md
│   │   ├── interactions/
│   │   └── prompts/
│   ├── testcases/                     # Excel / Markdown test cases specification
│   ├── postman/                       # Postman test suites
│   │   ├── collections/
│   │   ├── environments/
│   │   ├── data/
│   │   └── scripts/
│   ├── newman/                        # Newman test runner logs & HTML extra reports
│   ├── bugs/                          # Genuine bug reports & reproduction
│   │   └── screenshots/
│   ├── agent-skill/                   # AI Test Generator design (diagram + pseudocode)
│   │   ├── diagram/
│   │   └── pseudocode/
│   ├── ci/                            # CI/CD evidence (passing & failing runs)
│   │   └── evidence/
│   ├── evidence/                      # Execution logs, X-Student-Id evidence, git_commit_log.txt
│   │   ├── EVIDENCE_INDEX.md
│   │   └── git_commit_log.txt
│   ├── pdf/                           # Exported submission PDFs
│   ├── video/                         # Demo video script & recording checklist
│   │   ├── VIDEO_DEMO_SCRIPT.md
│   │   └── VIDEO_RECORDING_CHECKLIST.md
│   └── scripts/                       # Personal automation & Newman run scripts
├── 23127060/                          # Member 2 (23127060) workspace
│   └── (identical individual structure)
├── 23127195/                          # Member 3 (23127195) workspace
│   └── (identical individual structure)
├── scripts/                           # Shared utility scripts
└── .github/workflows/                 # CI/CD automation workflows
```

---

## 5-Step Pipeline Requirements per API

Each member must execute the following pipeline for each of their 3 selected APIs:
1. **AI Generate:** Generate ≥ 35 test cases per API covering domain partitions, state transitions, security (SEC-01–SEC-07), and schema validation.
2. **Human Audit:** Audit and label each test case (`VALID`, `INVALID`, `INCOMPLETE`).
3. **Human Extend:** Add ≥ 5 test cases missed by AI (especially around state transitions and security).
4. **Execute:** Run tests via Postman + Newman with mandatory `X-Student-Id: {StudentID}` header.
5. **Report Bugs:** Report genuine bugs on GitHub Issues and in Markdown.

---

## References
- **SUT Repository:** [https://github.com/ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut)
- **Course Assignment Spec:** `docs/assignment-notes.md`
- **Team Allocation Sheet:** `docs/team-api-allocation.md`
