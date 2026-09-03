# Interaction Log: INT-001

- **Interaction ID:** INT-001
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-08-30 22:00:00+07:00
- **Purpose / Stage:** Initial Repository Architecture & Multi-Member Setup Planning

---

## 1. Submitted Prompt
```text
/Speckit You are setting up the GitHub repository for my university assignment:

HW06 – API Testing

GitHub owner/account:
thangak18

Repository name:
HW06

IMPORTANT:
Follow the assignment requirements exactly.
This is an INDIVIDUAL ASSIGNMENT, but our group has 3 members and we intentionally use ONE SHARED GITHUB REPOSITORY, similar to our previous homework.
Each member must have a clearly separated personal workspace inside the repository.
Do NOT mix individual evidence, reports, test cases, AI audit logs, or generated reports between members.

==================================================
1. CREATE GITHUB REPOSITORY
==================================================

Create a PUBLIC GitHub repository:

https://github.com/thangak18/HW06

Repository name:
HW06

Description:
HW06 – API Testing | EShop SUT | Postman, Newman, AI-assisted Test Design and CI/CD

Initialize it with:
- README.md
- .gitignore
- LICENSE only if appropriate; otherwise skip LICENSE

Default branch:
main

If repository "HW06" already exists:
- DO NOT delete it
- DO NOT force push
- inspect the existing repository first
- preserve all existing work
- only add missing structure safely

Use git and GitHub CLI if available.

==================================================
2. ASSIGNMENT CONTEXT
==================================================

System Under Test:
EShop

Official SUT:
https://github.com/ttbhanh/eshop-sut

HW06 requires each student to select THREE APIs:
- one API implementing a feature from Pool A
- one API implementing a feature from Pool B
- one API implementing a feature from Pool C

Pool A:
FR-01 Account registration
FR-02 Login and account lockout
FR-03 Forgot/reset password
FR-04 Personal profile
FR-05 Product listing/search
FR-06 Product detail

Pool B:
FR-07 Shopping cart
FR-08 Checkout
FR-09 Discount coupons
FR-10 Order state machine
FR-11 Order history

Pool C:
FR-12 Access control
FR-13 Dashboard
FR-14 Category CRUD
FR-15 Product CRUD
FR-16 Product CSV import
FR-17 Coupon CRUD
FR-18 Admin order management
FR-19 Admin user management

There are 3 students in our group.

The assignment is still individual.
The shared repository is only used to organize the three individual submissions.

No two group members should use the exact same selection of three APIs.

DO NOT invent the other students' Student IDs, names, GitHub accounts, or API selections.
Use placeholders where information has not been provided.

==================================================
3. REPOSITORY STRUCTURE
==================================================

Create the following structure:

HW06/
│
├── README.md
├── .gitignore
│
├── docs/
│   ├── assignment-notes.md
│   └── team-api-allocation.md
│
├── members/
│   │
│   ├── member-1/
│   │   ├── README.md
│   │   ├── report/
│   │   ├── testcases/
│   │   ├── postman/
│   │   │   ├── collections/
│   │   │   ├── environments/
│   │   │   ├── data/
│   │   │   └── scripts/
│   │   ├── newman/
│   │   ├── bugs/
│   │   │   └── screenshots/
│   │   ├── ai/
│   │   │   ├── audit/
│   │   │   ├── critique/
│   │   │   └── prompts/
│   │   ├── agent-skill/
│   │   │   ├── diagram/
│   │   │   └── pseudocode/
│   │   ├── ci/
│   │   │   └── evidence/
│   │   └── git-log/
│   │
│   ├── member-2/
│   │   └── same structure as member-1
│   │
│   └── member-3/
│       └── same structure as member-1
│
├── scripts/
│   └── README.md
│
└── .github/
    └── workflows/
        └── README.md

Use .gitkeep where necessary so empty required directories can be committed.

Do NOT create fake test results just to populate folders.

==================================================
4. ROOT README
==================================================

Create a professional root README.md.

It should include:

# HW06 – API Testing

## Assignment
- Course homework: HW06 – API Testing
- SUT: EShop
- SUT repository link
- Testing stack:
  - Postman
  - Newman
  - GitHub Actions
  - AI-assisted API test generation

## Team Organization

Explain clearly:

"This homework is an individual assignment. The three students use one
shared GitHub repository only for source-control organization. Each student's
deliverables are isolated under their own directory."

Create this table:

| Member | Student ID | GitHub | Pool A | Pool B | Pool C | Workspace |
|---|---|---|---|---|---|---|
| Member 1 | TODO | TODO | TODO | TODO | TODO | members/member-1 |
| Member 2 | TODO | TODO | TODO | TODO | TODO | members/member-2 |
| Member 3 | TODO | TODO | TODO | TODO | TODO | members/member-3 |

DO NOT guess missing information.

Also document that:
- each student owns their own API test suite
- each student owns their own AI Audit Report
- each student owns their own Newman evidence
- each student owns their own test summary
- each student owns their own bug reports
- each student's commits should be attributable
- API selections must follow the homework rules

==================================================
5. MEMBER README TEMPLATE
==================================================

Create a README.md inside every member folder containing:

# HW06 – API Testing – Individual Workspace

## Student Information
- Name:
- Student ID:
- GitHub username:

## Selected APIs

| Pool | FR | Feature | Endpoint |
|---|---|---|---|
| A | TODO | TODO | TODO |
| B | TODO | TODO | TODO |
| C | TODO | TODO | TODO |

## Required Pipeline for Each API

1. AI Generate
2. Human Audit
3. Human Extension
4. Execute
5. Bug Report

Target:
- >= 35 AI-generated test cases per API
- >= 5 additional human-designed cases per API

Required test dimensions:
- domain partitions
- state transitions
- SEC-01 through SEC-07 security requirements
- schema validation

## Postman / Newman
Include placeholders for:
- collection
- environment
- data-driven files
- Newman HTML report
- Postman features used

## CI/CD
Include placeholders for:
- workflow
- successful pipeline run
- failing pipeline run
- screenshots
- links

## AI
Include:
- AI Audit Report
- AI Critique 200–300 words
- Agent Skill / AI-driven API test generator
- self-designed diagram
- pseudocode

## Bugs
Include placeholders for:
- GitHub Issue links
- screenshots
- expected result
- actual result

## Test Summary

| Metric | Count |
|---|---:|
| APIs | 3 |
| AI-generated test cases | TODO |
| Human-added test cases | TODO |
| Executed | TODO |
| Passed | TODO |
| Failed | TODO |
| Bugs | TODO |

==================================================
6. AI AUDIT TEMPLATE
==================================================

Create:

members/<member>/ai/audit/AI_AUDIT_TEMPLATE.md

Use this structure:

# AI Audit Report

## Declaration

I use AI tools for the following tasks.

## Interaction Log

### Interaction XXX

- AI Tool:
- Date:
- Time:
- Task:
- Prompt:

```text
PASTE THE EXACT PROMPT HERE
```

---

## 2. AI Output Summary
- Formulated initial implementation plan for repository initialization.
- Scaffolding templates for shared documentation (`docs/`), member workspaces (`members/` and subsequently student ID folders), and CI/CD workflow placeholders.

---

## 3. Human Evaluation & Outcome
- **Verdict:** VALID for initial directory structure and assignment reference docs.
- **Action:** Created initial repository baseline on GitHub.
