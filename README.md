# HW06 – API Testing

## Assignment
- **Course Homework:** HW06 – API Testing
- **System Under Test (SUT):** EShop (Vietnamese e-commerce demo application designed for testing practice)
- **SUT Repository:** [https://github.com/ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut)
- **Testing Stack:**
  - **API Design & Execution:** Postman (v10+ / v11+)
  - **CLI Test Runner:** Newman (with `newman-reporter-htmlextra` / CLI output)
  - **CI/CD Automation:** GitHub Actions
  - **AI Testing Assistance:** Prompt-driven test case generation, human audit, boundary/partition analysis, security rules (SEC-01–SEC-07), and AI Agent Skill generator

---

## Team Organization

> **Note on Individual Submission:**  
> This homework is an individual assignment. The three students use one shared GitHub repository only for source-control organization. Each student's deliverables are isolated under their own directory.

### Team Allocation Matrix

| Member | Student ID | GitHub | Pool A | Pool B | Pool C | Workspace |
|---|---|---|---|---|---|---|
| Member 1 | TODO | TODO | TODO | TODO | TODO | [members/member-1](./members/member-1) |
| Member 2 | TODO | TODO | TODO | TODO | TODO | [members/member-2](./members/member-2) |
| Member 3 | TODO | TODO | TODO | TODO | TODO | [members/member-3](./members/member-3) |

*(Note: Placeholders (`TODO`) will be filled by respective members without duplicating API selections).*

### Individual Ownership & Governance Rules
- **Isolated Ownership:** Each student owns their own API test suite, collections, environments, and test data.
- **AI Audit Trail:** Each student maintains their own independent AI Audit Report (`ai/audit/`) documenting every prompt, output, and human review.
- **Attributable Execution:** All Newman runs and Postman requests must carry the custom header `X-Student-Id: {StudentID}` for anti-cheat verification.
- **No Shared Evidence:** Newman HTML reports, execution logs, CI/CD run links, and bug reports must not be cross-copied between members.
- **Distinct Feature Selections:** No two group members may select the exact same combination of 3 APIs (1 from Pool A, 1 from Pool B, 1 from Pool C).
- **Attributable Git Commits:** Each student's commits should be attributable to their individual user/branch/workspace.

---

## Repository Structure

```
HW06/
├── README.md                          # Root overview & team coordination matrix
├── .gitignore                         # Environment & build ignores
├── docs/                              # Assignment reference docs & allocation sheets
│   ├── assignment-notes.md            # Detailed summary of HW06 requirements & rubrics
│   └── team-api-allocation.md         # API selection tracking table & collision prevention
├── members/                           # Isolated member workspaces
│   ├── member-1/                      # Workspace for Member 1
│   ├── member-2/                      # Workspace for Member 2
│   └── member-3/                      # Workspace for Member 3
├── scripts/                           # Shared utility scripts (local newman runners, etc.)
│   └── README.md
└── .github/workflows/                 # CI/CD pipelines for Newman automated runs
    └── README.md
```

---

## Deliverables Checklist per Member

Each member workspace contains the following standard folder layout:

1. **`report/`**: Final API testing report (`.md` and `.pdf`).
2. **`testcases/`**: Excel / CSV / Markdown test specification files (≥ 35 AI generated + ≥ 5 human extension cases per API).
3. **`postman/`**:
   - `collections/`: Postman collection JSON files.
   - `environments/`: Postman environment JSON files.
   - `data/`: Data-driven test files (CSV / JSON) for Collection Runner.
   - `scripts/`: Custom pre-request and test assertion scripts.
4. **`newman/`**: Newman execution output, CLI logs, and HTML reports.
5. **`bugs/`**: Genuine bug reports with steps to reproduce, actual vs. expected behavior, and screenshots.
6. **`ai/`**:
   - `audit/`: Complete `AI_AUDIT_REPORT.md` interaction logs.
   - `critique/`: 200–300 word AI critique paragraph.
   - `prompts/`: Raw prompts and prompt-engineering iterations.
7. **`agent-skill/`**:
   - `diagram/`: Self-drawn architecture/workflow diagram (PNG / Mermaid).
   - `pseudocode/`: Pseudocode and implementation files (`.md` / `.py`).
8. **`ci/`**:
   - `evidence/`: Screenshots, run logs, and direct links for passing & failing CI/CD pipeline runs.
9. **`git-log/`**: Formatted text file of individual Git commit history.

---

## References
- SUT Repository: [https://github.com/ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut)
- Official SUT API Specification: `api_specification.md` (in SUT repo)
- ISTQB Foundation Level Syllabus
