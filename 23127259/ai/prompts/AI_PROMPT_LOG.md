# HW06 – Consolidated AI Prompt Log

- **Student:** Nguyễn Tấn Thắng
- **Student ID:** 23127259
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

> This document contains the exact prompts submitted to AI tools during HW06.
> Prompts are preserved verbatim and ordered chronologically by interaction ID.
> Corresponding AI outputs and analytical evaluations are stored separately in `../interactions/`.

---

## Prompt Index

| INT | Date/Time (UTC+7) | Tool | Model | Stage / Purpose | Prompt Available | Interaction File |
|:---:|:---:|---|---|---|:---:|---|
| **INT-001** | 2026-08-30 22:00 | Antigravity Assistant | Gemini 3.7 Flash | Initial Repository Architecture & Multi-Member Setup Planning | YES (Verbatim) | [`INT-001-plan-initial.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-001-plan-initial.md) |
| **INT-002** | 2026-09-01 15:55 | Antigravity Assistant | Opus Reasoning | Initial Technical Implementation Planning for FR-02, FR-10, FR-14 | YES (Verbatim) | [`INT-002-plan-review.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-002-plan-review.md) |
| **INT-003** | 2026-09-01 16:15 | Antigravity Assistant | Claude Sonnet 4.6 | Implementation Plan Revision (SEC Mappings & Specification Oracle Separation) | YES (Verbatim) | [`INT-003-plan-revision.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-003-plan-revision.md) |
| **INT-004** | 2026-09-01 18:25 | Antigravity Assistant | Gemini 3.7 Flash | Final Implementation Plan Freeze & Pre-Implementation Gate Confirmation | YES (Verbatim) | [`INT-004-plan-final.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-004-plan-final.md) |
| **INT-005** | 2026-09-01 18:48 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.1: FR-02 Requirement, Parameter, and Domain Analysis | YES (Verbatim) | [`INT-005-fr02-requirement-domain-analysis.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-005-fr02-requirement-domain-analysis.md) |
| **INT-006** | 2026-09-01 18:53 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.2: FR-02 Domain Partition and Boundary Test Case Generation | YES (Verbatim) | [`INT-006-fr02-domain-boundary-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-006-fr02-domain-boundary-generation.md) |
| **INT-007** | 2026-09-01 18:56 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.3: FR-02 Lockout State-Transition Test Generation | YES (Verbatim) | [`INT-007-fr02-lockout-state-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-007-fr02-lockout-state-generation.md) |
| **INT-008** | 2026-09-01 18:59 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.4: FR-02 Security Test Generation | YES (Verbatim) | [`INT-008-fr02-security-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-008-fr02-security-generation.md) |
| **INT-009** | 2026-09-01 19:02 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.5: FR-02 Response Schema and Error-Contract Test Generation | YES (Verbatim) | [`INT-009-fr02-schema-error-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-009-fr02-schema-error-generation.md) |
| **INT-010** | 2026-09-01 19:26 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.6 (Part A): AI Prompt Log Verbatim Repair | YES (Verbatim) | [`INT-010-ai-prompt-log-verbatim-repair.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-010-ai-prompt-log-verbatim-repair.md) |
| **INT-011** | 2026-09-01 19:33 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.6 (Part B): FR-02 AI Generation Coverage Review and Freeze | YES (Verbatim) | [`INT-011-fr02-generation-coverage-freeze.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-011-fr02-generation-coverage-freeze.md) |
| **INT-012** | 2026-09-01 19:37 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1B.0: INT-011 Audit Repair + FR-02 Human Audit Workspace Preparation | YES (Verbatim) | [`INT-012-fr02-human-audit-preparation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-012-fr02-human-audit-preparation.md) |

---

## INT-001 – Initial Repository Architecture & Multi-Member Setup Planning

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-08-30 22:00:00+07:00
- **Interaction File:** [`../interactions/INT-001-plan-initial.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-001-plan-initial.md)

### Exact Prompt

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

## INT-002 – Initial Technical Implementation Planning for FR-02, FR-10, FR-14

- **Tool:** Antigravity IDE Assistant
- **Model:** Opus Reasoning
- **Date/Time:** 2026-09-01 15:55:00+07:00
- **Interaction File:** [`../interactions/INT-002-plan-review.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-002-plan-review.md)

### Exact Prompt

```text
/Speckit Switch to the strongest available Opus reasoning model for this planning task.

You are acting as a Senior QA Automation Engineer + API Testing Architect.

Your job in THIS TURN is PLAN ONLY.

DO NOT:
- modify any source files
- create implementation code
- create Postman collections yet
- generate the full test-case set yet
- create Git commits
- push anything to GitHub
- fabricate screenshots, Newman results, CI/CD results, bugs, or execution evidence
- modify the official SUT repository

I want a rigorous implementation plan for my university assignment:

HW06 – API Testing

==================================================
1. MY ASSIGNMENT SCOPE
==================================================

My selected features are:

Pool A:
FR-02 – Login and account lockout

Pool B:
FR-10 – Order state machine

Pool C:
FR-14 – Category management (CRUD)

These are MY individual features.

The group uses one shared GitHub repository:

GitHub account:
thangak18

Repository:
HW06

However, HW06 is still an INDIVIDUAL ASSIGNMENT.
My work, test cases, evidence, reports, AI audit, commits, and CI/CD evidence must remain clearly attributable to me.

Before planning implementation, verify that FR-02, FR-10, and FR-14 satisfy the assignment rule:
- one feature/API from Pool A
- one from Pool B
- one from Pool C

==================================================
2. AUTHORITATIVE SOURCES
==================================================

Use the HW06 assignment PDF available in this conversation as the primary assignment source.

Official SUT:
https://github.com/ttbhanh/eshop-sut

You MUST inspect the official SUT repository and especially:

api_specification.md

Also inspect other relevant files only where necessary to understand:
- endpoints
- request schemas
- response schemas
- authentication
- authorization
- state transitions
- business rules
- SEC-01 through SEC-07
- test data requirements
- database/data-seeding assumptions
- how to run the SUT locally

Do NOT rely on assumptions where the repository/specification can answer the question.

If the wording "three APIs" does not map one-to-one to FR-02, FR-10, and FR-14 because a feature uses multiple HTTP endpoints, identify this explicitly and propose the correct interpretation based on the assignment and API specification.

==================================================
3. FIRST: BUILD A REQUIREMENT TRACEABILITY MAP
==================================================

Before proposing the execution plan, create a concise traceability table for MY scope.

For each of:

FR-02
FR-10
FR-14

identify:

- Pool
- Feature name
- Actual HTTP endpoint(s)
- HTTP method(s)
- Authentication required?
- Admin role required?
- Request parameters/body
- Important response fields
- Relevant business rules
- Relevant SEC-01 to SEC-07 requirements
- Relevant state transitions
- Relevant schema-validation concerns
- Preconditions/test data needed
- Dependencies on other APIs

Do not invent details.
Mark anything not supported by the specification as:
NEEDS VERIFICATION

==================================================
4. HW06 REQUIREMENTS TO ACCOUNT FOR
==================================================

The implementation plan MUST cover every mandatory HW06 requirement.

For EACH of the three selected APIs/features:

A. AI Generation
- target >= 35 AI-generated test cases per selected API
- AI must be guided step-by-step
- not one generic "generate all tests" prompt

Coverage must include:
1. domain partitioning for every relevant parameter
2. boundary values
3. state transitions
4. security
5. SEC-01 through SEC-07 where applicable
6. schema validation
7. positive cases
8. negative cases
9. authentication/authorization cases
10. business-rule validation

B. Human Audit
Every AI-generated test case must be classified:
- VALID
- INVALID
- INCOMPLETE

For invalid/incomplete cases:
- explain why
- correct the case

C. Human Extension
For EACH selected API:
- add at least 5 test cases that AI missed
- prioritize security and state-transition weaknesses
- explain why AI likely missed them

D. Execution
Use:
- Postman
- Newman

Every executed request must contain:

X-Student-Id: {StudentID}

This header must eventually be demonstrated using REAL execution evidence.

Do NOT fabricate it.

E. Postman Features
Plan reasonable use of:
- collections
- environments
- variables
- pre-request scripts
- test scripts
- Collection Runner
- data-driven testing
- mock server if genuinely useful
- monitor if genuinely useful
- other relevant Postman features

Do not use features merely for decoration.
Explain which ones are actually useful for FR-02, FR-10, FR-14.

F. Bugs
For genuine discovered bugs:
- record in Markdown
- create GitHub Issues
- attach real screenshots/evidence

Never create a fake bug just to satisfy the report.

G. CI/CD
Integrate API tests into GitHub Actions/Newman.

Eventually we need TWO real pipeline examples:
1. one commit/run where all relevant tests pass
2. one commit/run where at least one test fails

The plan must explain how to create the failing demonstration safely without corrupting the actual final test suite.

H. AI-driven Test Generator / Agent Skill
Need:
- architecture/design
- self-drawn diagram
- pseudocode

IMPORTANT:
The final diagram must be based on my own design and must not be falsely presented as manually designed if AI directly generated it.

You may propose:
- what I should draw
- components
- data flow
- pseudocode structure

But identify clearly which part must be manually drawn by me.

I. AI Audit Report
Every AI interaction must record:
- AI tool
- date/time
- exact prompt
- AI output
- human review/correction where appropriate

J. AI Critique
Mandatory:
200–300 words

Must eventually discuss:
- what AI got wrong/incomplete
- why it missed issues
- lessons from human-AI collaboration

Do NOT write the final critique now.
Only plan what evidence we should collect so the final critique is authentic.

K. Git Commit Log
The assignment requires commits by working step.

Design a commit sequence that naturally reflects:
- generation
- audit
- extension
- implementation
- execution
for each selected API.

Do not create fake commits.

L. Submission artifacts
Account for all required submission files:
- main report Markdown
- main report PDF
- public GitHub repository link
- Postman collection JSON
- environment/data files where applicable
- Newman HTML report
- Postman feature list
- CI/CD report
- successful pipeline evidence
- failing pipeline evidence
- Excel test cases
- test summary
- Agent Skill/test-generator diagram
- pseudocode
- bug reports
- GitHub Issues/screenshots
- AI Critique
- AI Audit Report Markdown/PDF
- Git commit log text file
- README with self-assessment and test summary
- other required supporting evidence

==================================================
5. PAY SPECIAL ATTENTION TO MY THREE FEATURES
==================================================

FR-02 – Login and account lockout

The plan should specifically investigate/test areas such as:
- valid login
- invalid credentials
- account lockout threshold
- lockout duration
- attempt counter behavior
- counter reset rules
- email partitions
- password partitions
- JWT/authentication response
- account enumeration
- brute-force-related behavior
- SQL injection where applicable
- response schema
- error-message behavior
- state before/during/after lockout

BUT do not assume exact lockout rules until confirmed from the SUT specification.

--------------------------------------------------

FR-10 – Order state machine

This should be the strongest state-transition part of my assignment.

Build a plan around the ACTUAL allowed order-state graph from the specification.

Investigate:
- valid transitions
- invalid transitions
- skipped states
- backwards transitions
- cancellation rules
- terminal states
- repeated/idempotent state requests
- unauthorized changes
- role restrictions
- nonexistent order
- malformed identifiers
- concurrency/race-like considerations if reasonably testable
- response schema after transition

Create a state-transition matrix as part of the planning output.

Do not invent state-transition rules.

--------------------------------------------------

FR-14 – Category Management CRUD

Plan coverage for:
- create
- read/list if part of the feature/spec
- update
- delete
- admin authorization
- normal-user access
- unauthenticated access
- category-name partitions
- empty/null values
- duplicate categories
- maximum/minimum lengths if specified
- malformed IDs
- nonexistent IDs
- SQL injection where applicable
- XSS-like payload storage/reflection where applicable
- delete/update state effects
- response schemas
- CRUD lifecycle

IMPORTANT:
The assignment says "select three APIs", while FR-14 is CRUD and may map to multiple endpoints.

You MUST explicitly determine from api_specification.md how FR-14 should be scoped for HW06.

==================================================
6. TEST DATA AND EXECUTION DEPENDENCIES
==================================================

Identify all data/setup we will need, such as:

- normal user account
- admin account
- locked/unlocked account state
- bearer tokens
- category IDs
- order IDs
- orders in each necessary state
- seeded products if required
- database reset strategy
- deterministic setup for Newman
- cleanup strategy

Plan how Postman scripts can capture and reuse:

{{baseUrl}}
{{userToken}}
{{adminToken}}
{{orderId}}
{{categoryId}}

Do NOT place real secrets in Git.

Recommend:
- committed safe environment templates
- local/private environment values
- .env/example strategy if needed

==================================================
7. TEST-CASE DESIGN STRATEGY
==================================================

Do NOT generate all test cases yet.

Instead, estimate how we can reach >=35 meaningful AI-generated cases PER selected API without padding or duplicate cases.

For each selected feature/API, break the future test suite into categories and estimated counts.

Example format:

FR-02:
- Happy path: X
- Domain partitions: X
- Boundaries: X
- State/lockout: X
- Security: X
- Schema: X
Total planned: >=35

FR-10:
...

FR-14:
...

The cases must be meaningful and non-duplicative.

Also identify where >=5 HUMAN-added cases per API are most likely to come from.

==================================================
8. POSTMAN COLLECTION ARCHITECTURE
==================================================

Propose a clean Postman structure for MY individual work.

For example:

HW06 – <StudentID>
|
+-- 00 Setup
|
+-- FR-02 Login
|   +-- Positive
|   +-- Domain
|   +-- Lockout State
|   +-- Security
|   +-- Schema
|
+-- FR-10 Order State Machine
|   +-- Setup
|   +-- Valid Transitions
|   +-- Invalid Transitions
|   +-- Security
|   +-- Schema
|
+-- FR-14 Category CRUD
    +-- Setup
    +-- Create
    +-- Update
    +-- Delete
    +-- Authorization
    +-- Security
    +-- Schema
    +-- Cleanup

But improve this architecture based on the actual API specification.

Plan:
- variables
- environment
- pre-request scripts
- response tests
- setup/cleanup requests
- data-driven execution
- order dependencies

==================================================
9. REPORT / REPOSITORY ARCHITECTURE
==================================================

Our shared repository is:

thangak18/HW06

Recommend a folder structure for my INDIVIDUAL workspace that prevents my artifacts from being confused with the other two members.

Do not assume my Student ID if it has not been provided in the current task.

Use a placeholder such as:

members/<MY_STUDENT_ID>/

Plan where to store:

- report/
- testcases/
- postman/
- newman/
- bugs/
- ci/
- ai-audit/
- ai-critique/
- agent-skill/
- screenshots/
- git-log/

Do not reorganize the repository yet.
Only propose the structure.

==================================================
10. GIT / CI STRATEGY
==================================================

Recommend a branch and commit workflow suitable for a shared repository.

My work must remain attributable to me.

Propose commit names for all major stages.

For example:

feat(<id>): initialize FR-02 test design
test(<id>): add AI-generated FR-02 cases
review(<id>): audit FR-02 AI cases
test(<id>): add human FR-02 edge cases
test(<id>): automate FR-02 in Postman
...

Continue through FR-10, FR-14, CI/CD, reports, and Agent Skill.

Explain when to merge into main.

Also plan GitHub Actions architecture for Newman while avoiding conflicts with the other members' test suites.

==================================================
11. RISK ANALYSIS
==================================================

Identify likely risks before implementation, including:

- misunderstanding "three APIs" vs "three FRs"
- FR-14 mapping to several CRUD endpoints
- FR-10 setup complexity
- state pollution between Newman iterations
- lockout tests affecting later FR-02 cases
- flaky tests
- shared database state
- multiple group members running against the same SUT
- environment-variable leakage
- secrets in GitHub
- nondeterministic category/order IDs
- CI setup complexity
- accidentally fabricating evidence
- missing AI Audit interactions
- missing required submission artifact
- commit history becoming mixed across members

For each risk:
- impact
- prevention
- recovery

==================================================
12. OUTPUT FORMAT
==================================================

Return the planning document in this exact high-level structure:

# HW06 Implementation Plan – FR-02 / FR-10 / FR-14

## 1. Assignment Requirement Check
Confirm whether my selection complies with HW06.

## 2. Requirement Traceability
Detailed FR/API/security mapping.

## 3. API Scope Resolution
Resolve exactly which HTTP endpoint(s) count for:
- FR-02
- FR-10
- FR-14

Highlight any ambiguity in the assignment wording.

## 4. Dependency and Test Data Plan

## 5. FR-02 Detailed Testing Plan
- planned test categories
- estimated case counts
- state model
- security areas
- schema areas
- likely human-added cases

## 6. FR-10 Detailed Testing Plan
Include a state-transition matrix based on the real specification.

## 7. FR-14 Detailed Testing Plan
Include the CRUD lifecycle and endpoint mapping.

## 8. AI Generation and Human Audit Workflow
Explain a MULTI-PROMPT strategy.
Do not write the final prompts yet; define the stages.

## 9. Postman Architecture

## 10. Newman Execution Strategy

## 11. CI/CD Strategy

## 12. Bug Reporting Strategy

## 13. AI Audit Strategy

## 14. Agent Skill / Test Generator Plan

## 15. Repository and Branch Strategy

## 16. Git Commit Roadmap

## 17. Report and Submission Artifact Map

## 18. Risk Register

## 19. Step-by-Step Execution Roadmap
Give phases such as:
Phase 0
Phase 1
Phase 2
...

For every phase include:
- Objective
- Inputs
- Actions
- Outputs
- Evidence
- Git commit(s)
- Completion criteria

## 20. Definition of Done
A complete checklist against HW06 requirements.

## 21. Recommended First Implementation Step
Tell me exactly what we should implement first AFTER I approve this plan.

==================================================
13. IMPORTANT PLANNING RULES
==================================================

Be critical rather than agreeable.

If my assumptions are wrong, tell me.

If FR-02 / FR-10 / FR-14 creates an assignment-scope problem, identify it before implementation.

Distinguish:
- what the HW06 PDF explicitly requires
- what api_specification.md explicitly defines
- what you are recommending as engineering practice

Do not silently mix those three categories.

Do not fabricate requirements.

Do not optimize for speed at the expense of assignment compliance.

The goal is:
1. satisfy HW06 exactly
2. produce real execution evidence
3. maximize test quality
4. keep the work defensible in a 5–7 minute oral defense
5. make every artifact attributable to my individual work

At the end, STOP.

Do not implement anything until I explicitly approve the plan.
```

---

## INT-003 – Implementation Plan Revision (SEC Mappings & Specification Oracle Separation)

- **Tool:** Antigravity IDE Assistant
- **Model:** Claude Sonnet 4.6
- **Date/Time:** 2026-09-01 16:15:00+07:00
- **Interaction File:** [`../interactions/INT-003-plan-revision.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-003-plan-revision.md)

### Exact Prompt

```text
/Speckit Review and REVISE the HW06 plan you just produced.

PLAN REVISION ONLY.
DO NOT implement anything.
DO NOT create files.
DO NOT modify the repository.
DO NOT create Postman collections.
DO NOT create test cases yet.
DO NOT commit or push.

Your previous plan has several issues that must be corrected before implementation.

==================================================
1. CRITICAL: FIX SEC-01 THROUGH SEC-07
==================================================

You mapped the Security Requirements incorrectly.

Use the authoritative EShop SRS definitions exactly:

SEC-01:
Passwords must not be stored in plaintext.

SEC-02:
Security-sensitive APIs must require a valid JWT token.

SEC-03:
Admin APIs must verify role='admin' in the token, not merely token existence.

SEC-04:
User-controlled data displayed in the UI must be escaped correctly and must
not be inserted through unsafe innerHTML usage.

SEC-05:
Database queries must use parameterized queries rather than direct string
concatenation.

SEC-06:
The profile-update API must not allow a client to change the role field.

SEC-07:
Password-reset OTP must have sufficient entropy (minimum 6 digits), expire,
and become invalid after use.

Audit EVERY SEC reference in the previous plan and correct it.

Examples:
- missing admin role check on category/order admin API -> SEC-03
- missing JWT on a protected endpoint -> SEC-02
- parameterized SQL -> SEC-05
- plaintext password storage -> SEC-01

Do NOT label:
- IDOR as SEC-04
- rate limiting as SEC-06
- data exposure as SEC-05
because those mappings are incorrect.

Security issues may still be tested even when they do not correspond exactly
to an SEC ID, but label them separately as:
"Additional security test / business authorization test".

==================================================
2. SEPARATE SPECIFICATION FROM IMPLEMENTATION
==================================================

The previous plan inspected server.js/database.js and effectively revealed
intentional defects before test generation.

Revise the methodology.

The primary test oracle must come from:

1. HW06 PDF
2. EShop SRS / README requirements
3. api_specification.md

NOT from server.js implementation behavior.

New methodology:

SPECIFICATION
    ->
AI-generated test design
    ->
Human audit against specification
    ->
Human-added tests
    ->
Freeze expected results
    ->
Execute against SUT
    ->
Observe discrepancies
    ->
Report genuine bugs
    ->
Only THEN inspect server.js/database.js to explain root cause if useful.

Source-code inspection may identify CANDIDATE defects during planning, but
those candidates MUST NOT be treated as confirmed bugs until reproduced
through real API execution.

In the revised plan, move source-derived implementation anomalies into a
section:

"Known implementation observations — NOT YET CONFIRMED BY EXECUTION"

Do not let those observations determine the expected result.

==================================================
3. FIX FR-14 TEST ORACLES
==================================================

Do NOT call behavior a defect unless supported by a requirement.

FR-14 explicitly requires:
- Admin category management
- category name is mandatory/non-empty
- admin access requirements are inherited from FR-12
- api_specification.md exposes GET/POST/PUT/DELETE category endpoints

Therefore strong spec-backed tests include:
- empty category name
- missing category name
- JWT enforcement where required
- admin-role enforcement on modifying endpoints
- CRUD endpoint behavior/schema

However:

A. DUPLICATE CATEGORY NAME
There is no explicit requirement stating category names must be unique.

Therefore:
- it may be an exploratory test
- acceptance of duplicates MUST NOT automatically be reported as a bug

B. ORPHAN PRODUCTS
There is no explicit referential-integrity requirement stating what must happen
to products when their category is deleted.

Therefore:
- exploratory only
- do not declare a bug without a requirement oracle

C. XSS PAYLOAD
SEC-04 requires safe escaping when user-controlled content is DISPLAYED ON UI.

Returning a raw "<script>..." string in JSON is not by itself proof of an XSS
bug.

For HW06 backend API tests:
- such payload may be used as a security probe
- do not call raw JSON reflection an XSS vulnerability unless the consuming UI
  renders it unsafely and real execution evidence proves this.

Revise all FR-14 test counts and human-added cases accordingly.

==================================================
4. FIX FR-02 SECURITY INTERPRETATION
==================================================

The successful login implementation appears to return the complete user row,
including password.

Treat this as:
- a sensitive-data exposure candidate
- potentially related evidence that plaintext password handling is unsafe

BUT:
SEC-01 specifically states that passwords must NOT BE STORED in plaintext.

Do not incorrectly map response exposure to SEC-05.

Distinguish:
A. password storage violation -> SEC-01
B. password appearing in API response -> additional sensitive-data exposure
   defect

Also avoid making direct database inspection a normal API test-case oracle.

==================================================
5. FIX FR-10 SECURITY INTERPRETATION
==================================================

For FR-10:

- invalid/final-state transitions -> FR-10 business-rule testing
- admin endpoint accessible to regular user -> SEC-03
- protected endpoint accessible without JWT -> SEC-02
- accessing another user's order -> authorization / ownership / IDOR-style test

Do not map IDOR to SEC-04.

Keep:
- canceled -> delivered
- shipping user-cancel
- normal user calling admin transition
- unauthenticated order access

as HIGH-VALUE candidate tests, but mark implementation outcomes as:
"candidate observation until reproduced via real execution."

==================================================
6. FR-14 SCOPE AMBIGUITY
==================================================

Do not state as fact that "three APIs" unquestionably means three features.

Document the exact evidence:

HW06 asks for:
- one API implementing a feature from Pool A
- one API implementing a feature from Pool B
- one API implementing a feature from Pool C
- consult api_specification.md for endpoints behind the selected feature

FR-14 is Category Management CRUD.

api_specification.md exposes:
- GET /api/categories
- POST /api/categories
- PUT /api/categories/:id
- DELETE /api/categories/:id

The SRS text explicitly mentions Add/View/Delete, while the API specification
also exposes PUT Update.

Recommended scope:
include all four category endpoints for complete FR-14/API-spec coverage.

Label this as a defensible SCOPE DECISION, not as an explicit PDF statement.

==================================================
7. REMOVE INVENTED MANDATORY REQUIREMENTS
==================================================

The previous plan added some engineering targets that are NOT assignment
requirements.

Correct them:

- "minimum 6 AI interactions per API" -> engineering recommendation only
- "at least 2 bugs" -> REMOVE as a mandatory requirement
- specific Postman features as mandatory -> distinguish recommendations from PDF
- exact number of Git commits -> engineering recommendation

The PDF requires reporting genuine bugs that are found.
Do not create a bug-count quota.

Continue to recommend multiple focused AI interactions, but label them [ENG].

==================================================
8. AI AUDIT VS TEST-CASE AUDIT
==================================================

Do not conflate these two audits.

AI Audit Report:
For each AI interaction record:
- AI tool
- date/time
- exact prompt
- AI output

Human test-case audit:
For EACH AI-generated test case classify:
- VALID
- INVALID
- INCOMPLETE
with rationale and correction.

They are related but not the same artifact.

Make this distinction explicit in the revised plan.

==================================================
9. AGENT SKILL DIAGRAM WORDING
==================================================

Correct the phrase "must be hand-drawn."

The assignment says the diagram must be SELF-DRAWN:
the student makes the design decisions and produces the diagram;
any diagramming tool is acceptable;
the final diagram must not be AI-generated.

Therefore:
- draw.io / Excalidraw / manually authored Mermaid are acceptable as applicable
- do not have AI generate the final diagram and claim it as self-drawn
- it does NOT literally have to be drawn with pen and paper

==================================================
10. CI/CD PASS/FAIL STRATEGY
==================================================

Reconsider the previous suggestion:

"Passing run = only happy-path folders."

The assignment wording asks for:
- one sample commit whose pipeline run shows all API test cases passing
- another sample commit whose pipeline run shows one test case failing

Do not silently reinterpret "all API test cases" as only a happy-path subset.

Design a defensible CI demonstration strategy.

Clearly distinguish:
A. full regression execution results against the buggy SUT
B. assignment-required CI demonstration run
C. intentionally failing CI demonstration

Do NOT change legitimate test expected results merely to force a green build.

If there is unavoidable ambiguity because the SUT intentionally contains
defects, flag it as a point to confirm with the TA rather than inventing an
interpretation.

==================================================
11. STATEFUL EXECUTION
==================================================

Keep the useful observation that restarting the backend resets the SQLite DB.

However, design automated tests so that each state-sensitive scenario is as
independent and deterministic as reasonably possible.

For FR-10:
- create fresh orders for independent transition scenarios
- do not reuse one order across incompatible transition tests
- setup must create the exact initial state required

For FR-02:
- use a dedicated lockout account
- avoid locking the primary user used by other suites

For FR-14:
- generate unique temporary category names for tests that require isolation
- clean only records created by the current test

==================================================
12. REVISE THE BUG-CANDIDATE TABLE
==================================================

Classify candidates into:

A. Strong specification-backed candidates
Examples:
- FR-02 attempt increment mismatch
- FR-02 lockout duration mismatch
- FR-10 canceled -> delivered
- FR-10 user cancel while shipping
- FR-10 admin transition missing role check
- protected order endpoint missing JWT where applicable
- FR-14 modifying category with normal user
- FR-14 empty/missing category name accepted

B. Additional security candidates
- password exposed in login response
- cross-user order access

C. Exploratory observations, NOT automatically bugs
- duplicate category names
- orphan categories/products
- raw XSS-like strings returned in JSON
- unspecified maximum lengths

All bugs remain UNCONFIRMED until reproduced by real execution.

==================================================
13. FINAL OUTPUT
==================================================

Return a corrected version:

# HW06 Revised Implementation Plan – FR-02 / FR-10 / FR-14

Preserve the strong parts of the original plan:
- traceability
- Postman architecture
- test-count planning
- state-transition matrix
- repository organization
- branch strategy
- commit roadmap
- CI/CD
- submission artifact map
- risk register
- definition of done

But correct all issues above.

At the end add:

## Changes From Previous Plan

with a table containing:
- previous issue
- correction
- reason
- source (PDF / SRS / API Spec / ENG)

Then STOP.

DO NOT IMPLEMENT ANYTHING.
```

---

## INT-004 – Final Implementation Plan Freeze & Pre-Implementation Gate Confirmation

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-09-01 18:25:00+07:00
- **Interaction File:** [`../interactions/INT-004-plan-final.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-004-plan-final.md)

### Exact Prompt

```text
/Speckit Make one FINAL REVISION to the current HW06 Revised Implementation Plan.

PLAN EDIT ONLY.
Do not implement, create files, modify the repository, commit, push,
or generate the actual test cases yet.

Preserve everything that is already correct.
Fix ONLY the following issues:

1. FR-10 STATE MACHINE CORRECTION

The SRS diagram explicitly allows:

pending -> canceled     by User/Admin
confirmed -> canceled   by User/Admin

Your current matrix incorrectly labels confirmed -> canceled as Admin only.

Correct every occurrence of this mistake.

The SRS states that when an order is shipping, User cannot cancel it.
Do not invent a shipping -> canceled transition unless explicitly supported.

2. FR-02 ERROR MESSAGE ORACLE

Do not require wrong-email, wrong-password, and locked-account responses
to have identical error text.

Correct oracle:

- wrong email vs wrong password must not reveal which credential was incorrect;
- a locked account may return a distinct temporary-lock message;
- messages must not disclose sensitive internal details.

Update the human-added error-message test accordingly.

3. DO NOT DEPEND ON UNDOCUMENTED login_attempts RESPONSE FIELD

api_specification.md documents GET /api/admin/users but does not guarantee
that login_attempts is part of its response schema.

Therefore do not make black-box API tests depend on reading login_attempts
through /api/admin/users.

Test FR-02 externally through observable state:

failure #1 -> not locked
failure #2 -> not locked
failure #3 -> lock should activate
during 30-second window -> locked
after expiration -> usable according to specification
successful authentication -> failure sequence should reset as specified

Direct DB/source inspection may be used later as supplemental root-cause
evidence, but not as the primary API oracle.

4. CLARIFY BLACK-BOX LIMITATIONS OF SEC-01 AND SEC-05

SEC-01 requires passwords not to be stored as plaintext.
The absence of a password field in an API response does NOT prove SEC-01.

Separate:
- SEC-01 storage verification
- additional sensitive-data exposure testing

Mark SEC-01 black-box API coverage as PARTIAL.
Full verification may require authorized DB/source inspection.

SEC-05 requires parameterized queries.
SQL injection requests through Postman are useful behavioral probes,
but successful resistance to an injection payload does NOT prove that
parameterized queries are used.

Mark SEC-05 API testing as PARTIAL behavioral evidence.
Source inspection can later confirm implementation technique.

5. ENFORCE TEST-COUNT ACCOUNTING

The assignment requires target >=35 AI-generated cases per selected API,
then at least 5 additional human-designed cases per API.

Use this safe accounting:

FR-02:
>=35 AI-generated
+ >=5 human-added
= >=40 final

FR-10:
>=35 AI-generated
+ >=5 human-added
= >=40 final

FR-14:
>=35 AI-generated
+ >=5 human-added
= >=40 final

TOTAL:
>=105 AI-generated
+ >=15 human-added
= >=120 final test cases.

Do NOT count the human-added cases toward the >=35 AI-generated target.

The current Postman architecture enumerates only approximately:
FR-02 31,
FR-10 30,
FR-14 27.

Fix this.

Either:
A. expand the architecture to contain >=35 AI case IDs PLUS >=5 HUMAN case IDs
for every feature,

or preferably:
B. clearly mark the tree as an illustrative subset and add a mandatory
Test Inventory section that will contain the complete >=40 cases per feature.

Use distinct IDs:

FR02-AI-001...
FR02-HUM-001...

FR10-AI-001...
FR10-HUM-001...

FR14-AI-001...
FR14-HUM-001...

This distinction must also appear in Excel and test summary accounting.

6. CI/CD WORDING

Keep the current three-scenario CI proposal, but do NOT claim that a
CI-PASS subset unquestionably satisfies the PDF phrase
"all API test cases passing."

Mark this as:
[ENG - PENDING TA CLARIFICATION]

Do not alter legitimate expected results merely to obtain a green pipeline.

At the end add a short section:

## Final Pre-Implementation Gate

It must confirm:
- FR mapping correct
- security mapping correct
- test oracle comes from specification
- >=35 AI + >=5 human per feature planned
- X-Student-Id evidence planned
- no implementation evidence fabricated
- no bug marked confirmed before execution

Then STOP.
Do not begin Phase 0.
```

---

## INT-005 – Phase 1A.1: FR-02 Requirement, Parameter, and Domain Analysis

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-09-01 18:48:12+07:00
- **Interaction File:** [`../interactions/INT-005-fr02-requirement-domain-analysis.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-005-fr02-requirement-domain-analysis.md)

### Exact Prompt

```text
/Speckit We are starting:

PHASE 1A.1 – FR-02 REQUIREMENT, PARAMETER, AND DOMAIN ANALYSIS

This is the FIRST AI-generation interaction for FR-02.

IMPORTANT:
This is a STEP-BY-STEP AI testing workflow required by HW06.

DO NOT generate all 35 FR-02 test cases in this turn.

DO NOT:
- execute Postman
- execute Newman
- trigger account lockout
- inspect runtime behavior
- confirm bugs
- file GitHub Issues
- use server.js/database.js as the test oracle
- generate FR-10 tests
- generate FR-14 tests
- add the >=5 human-designed cases
- perform the human VALID/INVALID/INCOMPLETE audit yet
- modify the SUT
- merge to main

==================================================
1. CONTEXT
==================================================

Assignment:
HW06 – API Testing

Student:
Nguyễn Tấn Thắng

Student ID:
23127259

Repository:
https://github.com/thangak18/HW06

Branch:
thang/hw06-implementation

Personal workspace:
23127259/

Selected feature for this phase:

FR-02 – Login and Account Lockout
Pool A

Endpoint:
POST /api/login

Final FR-02 accounting will eventually be:

>=35 AI-generated cases
+ >=5 Human-designed extension cases
= >=40 final cases

BUT THIS TURN IS ANALYSIS ONLY.

==================================================
2. AUTHORITATIVE TEST ORACLE SOURCES
==================================================

Before producing anything, read the authoritative project documents available
locally:

1. HW06 assignment PDF / assignment notes
2. EShop SRS / README requirements
3. api_specification.md

For formal expected behavior, use ONLY:

[SRS]
[API-SPEC]
[PDF]

Do NOT derive expected results from:
server.js
database.js
or previously known implementation defects.

You may already know implementation observations from planning.

IGNORE THEM for this generation step.

Imagine you are designing tests before executing the SUT.

==================================================
3. FR-02 REQUIREMENTS TO EXTRACT
==================================================

Extract and cite/trace the exact FR-02 behavior including:

- login endpoint
- HTTP method
- request fields
- required fields
- successful login behavior
- invalid credential behavior
- account lockout threshold
- failed-attempt progression
- lockout duration
- successful-login reset rule
- generic/non-disclosing credential errors
- JWT returned on success
- any explicitly documented status codes
- any explicitly documented response structure

Also identify which security requirements are actually applicable:

SEC-01
SEC-02
SEC-03
SEC-04
SEC-05
SEC-06
SEC-07

Use these exact definitions:

SEC-01:
Passwords must not be stored in plaintext.

SEC-02:
Security-sensitive APIs must require a valid JWT.

SEC-03:
Admin APIs must validate role='admin'.

SEC-04:
User-controlled data rendered in UI must be safely escaped.

SEC-05:
Database queries must use parameterized queries.

SEC-06:
Profile update must not allow client-side role modification.

SEC-07:
Password-reset OTP must have sufficient entropy, expire, and be single-use.

Do NOT force irrelevant SEC requirements into FR-02.

For every SEC requirement classify:

- DIRECTLY APPLICABLE
- PARTIALLY TESTABLE THROUGH FR-02 API
- NOT APPLICABLE TO FR-02

Give reasoning.

==================================================
4. PARAMETER INVENTORY
==================================================

Build a formal parameter inventory for:

POST /api/login

At minimum inspect:

email
password

For each parameter identify from specification:

- data type
- required/optional
- format constraint
- semantic constraint
- known valid class
- known invalid classes
- empty value
- missing value
- null value
- whitespace value
- unusual but syntactically valid value
- boundary possibilities
- security-relevant values

IMPORTANT:

Do not invent a length limit if none is stated.

If no minimum/maximum length exists in the specification, write:

NOT SPECIFIED

Do not turn an unspecified boundary into a mandatory expected rejection.

==================================================
5. EQUIVALENCE PARTITIONING
==================================================

Create an equivalence-partition table.

Required columns:

| Parameter | Partition ID | Partition | Valid/Invalid | Spec Basis | Future Test Need |

Examples of partition categories to investigate:

email:
- registered valid email
- unregistered syntactically-valid email
- malformed email
- empty
- missing
- null
- whitespace
- case variation
- SQL injection-like payload

password:
- correct password
- incorrect password
- empty
- missing
- null
- whitespace
- long arbitrary value
- special-character value
- SQL injection-like payload

However:

Do not blindly classify a value as invalid unless the specification establishes
that rule.

For uncertain cases use:

SPEC-UNDEFINED / EXPLORATORY

==================================================
6. BOUNDARY VALUE ANALYSIS
==================================================

Identify real boundaries that exist in the specification.

The most important FR-02 boundaries include:

- failed login attempt progression
- lockout threshold
- lockout duration

Build a boundary table such as:

| Boundary | Just Below | At Boundary | Just Above | Expected State Source |

For example, analyze the specification around:

attempt count:
0
1
2
3
4

lockout duration:
just before expiry
at/around expiry
just after expiry

Do not use implementation values.

Use the SRS-defined behavior only.

==================================================
7. FR-02 STATE MODEL
==================================================

Build a specification-derived state model.

Identify states such as:

NORMAL
FAILED_ATTEMPTS_ACCUMULATING
LOCKED
LOCK_EXPIRED
AUTHENTICATED / COUNTER_RESET

Do not use implementation-specific counter anomalies.

Provide:

A. state definitions
B. triggering event
C. expected response class
D. next state

Then provide a simple text transition representation.

==================================================
8. SCHEMA ANALYSIS
==================================================

From api_specification.md only, enumerate the expected response contract for:

A. successful login
B. invalid credentials
C. locked account

For each response identify:

- expected HTTP status if explicitly documented
- top-level fields
- required fields
- expected primitive/object type
- security-sensitive fields that SHOULD NOT be present if supported by requirement

If exact schema information is not specified:

write:
NOT SPECIFIED

Do NOT invent JSON Schema constraints.

==================================================
9. SECURITY TEST-DESIGN ANALYSIS
==================================================

Do not create full security test cases yet.

Instead list security dimensions worth generating tests for in a later stage.

Separate:

A. Numbered SRS security requirements applicable to FR-02
B. Additional security probes not mapped to a numbered SEC requirement

Examples may include:

- SQL injection behavioral probes
- credential enumeration
- sensitive data exposure
- JWT structure/issuance
- authentication behavior on a downstream protected endpoint

For SEC-01 and SEC-05 explicitly retain these limitations:

SEC-01:
black-box API evidence is PARTIAL;
storage-at-rest verification requires DB/source evidence.

SEC-05:
SQL injection resistance is PARTIAL behavioral evidence;
it does not prove parameterized queries are used.

==================================================
10. OUTPUT FILES
==================================================

Create/update ONLY:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md

The document must contain:

# FR-02 Requirement Analysis

## 1. Requirement Traceability
## 2. Endpoint Contract
## 3. Parameter Inventory
## 4. Equivalence Partitions
## 5. Boundary Value Analysis
## 6. Specification State Model
## 7. Response Schema Analysis
## 8. Security Applicability
## 9. Open / Undefined Specification Questions
## 10. Inputs for Next AI Generation Stage

Do NOT create the 35-case Excel file yet.

Do NOT create Postman requests yet.

==================================================
11. AI AUDIT LOGGING
==================================================

This interaction must be logged as the next real AI interaction.

Determine the next available INT number by inspecting:

23127259/ai/interactions/

Create:

INT-XXX-fr02-requirement-domain-analysis.md

Record:

- Interaction ID
- AI Tool
- Model
- real date
- real local time
- Stage:
  FR-02 Stage 1 – Requirement/Domain Analysis
- Exact prompt used for THIS interaction
- Exact AI output from THIS interaction

Do not invent past information.

Also add the interaction entry to:

23127259/ai/AI_AUDIT_REPORT.md

IMPORTANT:

This interaction is part of the required AI Audit evidence.

==================================================
12. QUALITY CHECK
==================================================

Before finishing, verify:

- no implementation behavior used as oracle
- no known defect stated as expected behavior
- no FR-10/FR-14 material generated
- no human extension test case generated
- no formal FR-02 test cases generated yet
- undefined requirements are labelled NOT SPECIFIED or EXPLORATORY
- SEC mappings are correct
- analysis is traceable to SRS/API specification

==================================================
13. GIT POLICY
==================================================

Do NOT create the FR-02 generation commit yet.

The assignment needs a meaningful generation-stage commit.

We will commit after the complete FR-02 AI-generation sequence is finished,
not after every micro-interaction.

Leave the current changes uncommitted after this interaction.

At the end show:

1. file created/updated
2. AI interaction ID
3. short summary of FR-02 partitions found
4. open specification ambiguities
5. git status

Then STOP.

The next interaction will be:

PHASE 1A.2 – FR-02 BOUNDARY AND DOMAIN TEST CASE GENERATION
```

---

## INT-006 – Phase 1A.2: FR-02 Domain Partition and Boundary Test Case Generation

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-09-01 18:53:51+07:00
- **Interaction File:** [`../interactions/INT-006-fr02-domain-boundary-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-006-fr02-domain-boundary-generation.md)

### Exact Prompt

```text
/Speckit We are continuing with:

PHASE 1A.2 – FR-02 DOMAIN PARTITION AND BOUNDARY TEST CASE GENERATION

This is the SECOND FR-02 AI-generation interaction.

IMPORTANT:
Do NOT generate the complete FR-02 suite yet.

This stage should generate ONLY:
- equivalence-partition test cases
- request-domain negative cases
- specification-backed boundary cases

Do NOT generate:
- the full state-transition suite
- the dedicated security suite
- schema-focused suite
- the final coverage-gap cases
- Human-designed extension cases
- FR-10 cases
- FR-14 cases

Do NOT execute the SUT.
Do NOT run Postman/Newman.
Do NOT inspect implementation source as the test oracle.
Do NOT confirm bugs.

==================================================
1. FIRST PATCH THREE ANALYSIS ISSUES
==================================================

Before generating cases, make these corrections to:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md

A. SEC-02 CLASSIFICATION

POST /api/login itself does not require JWT.
It issues the JWT.

Therefore do NOT classify SEC-02 as directly enforced by the login endpoint.

Use wording such as:

SEC-02:
INDIRECT / AUTHENTICATION DEPENDENCY for FR-02.
FR-02 issues the JWT that protected endpoints later consume.
Downstream protected-endpoint probes may validate token usability,
but they are not the primary behavioral contract of POST /api/login.

B. PARAMETER PARTITION INDEPENDENCE

Do not define email equivalence partitions using password correctness.

For email, partitions should describe EMAIL characteristics only.

For example:

- registered syntactically valid email
- unregistered syntactically valid email
- malformed email
- empty
- missing
- null
- whitespace-only
- casing variation
- SQLi-like probe

Password correctness belongs to password partitions.

Cross-parameter combinations belong to test-case generation,
not the single-parameter partition table.

C. THIRD-FAILURE RESPONSE ORACLE

Distinguish:

1. state transition caused by the third consecutive failed authentication
2. HTTP response/status of the third failed request itself

If SRS/API-SPEC does not explicitly state whether failed request #3 itself
returns the ordinary credential error or a locked-account response,
mark that exact response detail as:

NOT SPECIFIED

The specification-backed state oracle is:

failure #1 -> not locked
failure #2 -> not locked
failure #3 -> account becomes locked
subsequent request during lock window -> rejected because account is locked

Do not invent an exact status for failure #3 unless documented.

==================================================
2. HUMAN-CASE INTEGRITY RULE
==================================================

This is critical.

Previous planning documents contain example ideas labelled as
"Human-Designed Extensions."

Those were suggested by AI during planning.

Therefore they MUST NOT automatically become the final
FR02-HUM-001..005 cases.

For this assignment, actual human extension cases must be selected AFTER:

1. >=35 AI-generated FR-02 cases exist
2. human audit is completed
3. actual coverage gaps are identified

Do NOT create any FR02-HUM case in this interaction.

Do NOT reserve final HUM IDs based on plan examples.

Treat previous AI-suggested human-case ideas only as planning notes.

==================================================
3. AUTHORITATIVE INPUT
==================================================

Read:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md

and the authoritative:

- EShop SRS / README requirements
- api_specification.md

Use only specification-derived expected behavior.

Ignore:

- server.js implementation behavior
- database.js implementation behavior
- known candidate defects
- OBS-xx findings

==================================================
4. OBJECTIVE OF THIS STAGE
==================================================

Generate approximately 12–16 UNIQUE AI-generated FR-02 test cases covering:

A. email equivalence partitions
B. password equivalence partitions
C. cross-parameter domain combinations
D. missing/null/empty request values
E. specification-backed boundaries
F. lockout threshold boundary cases ONLY at the boundary-design level

Do not pad the count.

Every case must test a meaningfully distinct behavior.

Use IDs beginning:

FR02-AI-001

Continue sequentially.

These are AI-generated cases.

==================================================
5. REQUIRED TEST CASE FORMAT
==================================================

For every generated test case include:

| Field | Required |
|---|---|
| Test Case ID | Yes |
| Title | Yes |
| Technique | EP / BVA / Negative |
| Requirement | SRS/API-SPEC reference |
| Preconditions | Yes |
| Request Method | POST |
| Endpoint | /api/login |
| Headers | Content-Type and X-Student-Id placeholder |
| Request Body | Exact test data/example |
| State Before | If relevant |
| Action | Yes |
| Expected HTTP Status | Only if specified |
| Expected Response | Specification-derived |
| State After | If relevant |
| Oracle Confidence | EXPLICIT / PARTIAL / SPEC-UNDEFINED |
| Notes | Any ambiguity |

IMPORTANT:

If specification does not define exact HTTP status for a malformed or
missing-field case:

do NOT invent one.

Use:

Expected HTTP Status: NOT SPECIFIED
Expected semantic result: authentication must not succeed

where appropriate.

==================================================
6. DOMAIN TEST DESIGN RULES
==================================================

EMAIL:

Generate meaningful cases from partitions such as:

- registered valid email
- unregistered syntactically valid email
- malformed syntax
- empty string
- missing key
- null
- whitespace-only
- casing variation

But:

case sensitivity is SPEC-UNDEFINED unless explicitly documented.

Do not assert uppercase email must pass or fail.

PASSWORD:

Generate meaningful cases such as:

- correct password
- incorrect password
- empty string
- missing key
- null
- whitespace-only
- long arbitrary string

But:

maximum/minimum login password length is NOT SPECIFIED unless an authoritative
document explicitly states otherwise.

A long password case is exploratory/domain robustness;
do not assert rejection purely because of length.

==================================================
7. BOUNDARY CASES
==================================================

Include specification-backed boundary design around:

consecutive failure threshold N=3.

At minimum distinguish:

N=1
N=2
N=3
N>3 / request while locked

But remember:

if exact status of failure #3 is not specified,
assert state transition rather than inventing response status.

Lock-duration timing cases will be generated in the dedicated
state-transition stage, not here, except you may document the 30-second
boundary as an input for the next stage.

Do NOT create sleeps/timers or execute timing tests yet.

==================================================
8. SECURITY PROBES
==================================================

Do NOT generate the dedicated security suite yet.

If an SQLi-like payload naturally belongs to a domain partition, you may
include at most:

- one email SQLi domain probe
- one password SQLi domain probe

Label them:

SEC-05 behavioral probe – PARTIAL black-box evidence

Do not claim that passing such a test proves parameterized queries.

Sensitive-data response checks, JWT misuse, credential enumeration, etc.
belong to a later security stage.

==================================================
9. OUTPUT ARTIFACT
==================================================

Create:

23127259/testcases/FR02_AI_DRAFT.md

This is an incremental AI-generated inventory.

Add:

# FR-02 AI-Generated Test Case Draft

## Stage 1A.2 – Domain and Boundary Cases

Then the generated test cases.

Also create/update a summary table at the top:

| Stage | ID Range | Generated Count |
|---|---|---:|
| 1A.2 Domain/BVA | FR02-AI-001..XXX | N |

Do NOT create Excel yet.

The Excel workbook will be generated only after the complete FR-02
AI-generation sequence and deduplication are finished.

==================================================
10. DO NOT AUDIT THE CASES YET
==================================================

This interaction is AI GENERATION.

Do not label generated cases:

VALID
INVALID
INCOMPLETE

That classification is the later HUMAN AUDIT stage.

The generating AI may mark:

Oracle Confidence:
- EXPLICIT
- PARTIAL
- SPEC-UNDEFINED

but must not perform the student's final audit.

==================================================
11. AI AUDIT INTERACTION
==================================================

Inspect:

23127259/ai/interactions/

Determine next INT ID.

Expected next ID should be INT-006 if no other interaction exists.

Create:

INT-006-fr02-domain-boundary-generation.md

Record truthfully:

- Interaction ID
- AI Tool
- Model
- Date/time
- Stage
- Exact prompt
- Full AI output

Update:

23127259/ai/AI_AUDIT_REPORT.md

Do not fabricate metadata.

==================================================
12. COUNT AND DUPLICATION CHECK
==================================================

Before finishing:

- count generated cases
- ensure IDs are unique
- ensure no two cases are semantically duplicates
- ensure no Human case IDs exist
- ensure only FR-02 is covered
- ensure no implementation-derived expected result appears
- ensure SPEC-UNDEFINED properties remain explicitly undefined

Target for this stage:

12–16 AI-generated cases

NOT 35.

Later stages will bring the AI-generated total to >=35.

==================================================
13. GIT POLICY
==================================================

Do NOT commit yet.

Keep all FR-02 generation-stage changes uncommitted until the full
AI-generation sequence is complete.

At the end report:

1. Analysis patches made
2. Interaction ID
3. FR02 AI IDs generated
4. Generated count
5. Technique counts:
   - EP
   - BVA
   - Negative
6. SPEC-UNDEFINED cases
7. Current cumulative AI-generated FR-02 count
8. git status

Then STOP.

Next stage:

PHASE 1A.3 – FR-02 LOCKOUT STATE-TRANSITION TEST GENERATION
```

---

## INT-007 – Phase 1A.3: FR-02 Lockout State-Transition Test Generation

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-09-01 18:56:52+07:00
- **Interaction File:** [`../interactions/INT-007-fr02-lockout-state-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-007-fr02-lockout-state-generation.md)

### Exact Prompt

```text
/Speckit We are continuing with:

PHASE 1A.3 – FR-02 LOCKOUT STATE-TRANSITION TEST GENERATION

This is the THIRD FR-02 AI-generation interaction.

Current FR-02 AI inventory:
FR02-AI-001 .. FR02-AI-014
Cumulative count: 14

This stage generates ONLY state-transition and lockout-lifecycle cases.

Do NOT:
- generate the complete remaining suite
- generate dedicated security cases
- generate schema-only cases
- generate Human-designed extension cases
- audit VALID / INVALID / INCOMPLETE
- execute Postman/Newman
- run the SUT
- inspect server.js/database.js as oracle
- confirm implementation defects
- generate FR-10 or FR-14 material
- commit yet

==================================================
1. AUTHORITATIVE INPUT
==================================================

Read:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md
23127259/testcases/FR02_AI_DRAFT.md

Also use the authoritative:
- EShop SRS / README requirements
- api_specification.md

Formal expected behavior must come ONLY from:
[SRS]
[API-SPEC]

Ignore all known implementation observations when setting expected results.

==================================================
2. FIRST CORRECT ONE COVERAGE GAP
==================================================

The previous Stage 1A.2 was instructed to distinguish:

N=1
N=2
N=3
N>3 / request while locked

but only explicit cases for N=2 and N=3 were generated.

Therefore this stage MUST include an explicit case for:

FR02-AI-015:
First consecutive failed login attempt.

Specification-derived oracle:
- authentication fails
- account must NOT yet be in locked state
- subsequent login attempt must still be accepted for credential evaluation

Do not depend on reading an undocumented internal login_attempts field.

==================================================
3. FR-02 SPECIFICATION STATE MODEL
==================================================

Use the specification-derived lifecycle only:

NORMAL
  |
  | failed login #1
  v
FAILURE_SEQUENCE_ACTIVE
  |
  | failed login #2
  v
FAILURE_SEQUENCE_ACTIVE
  |
  | failed login #3
  v
LOCKED
  |
  | 30-second lock period expires
  v
LOCK_EXPIRED / AUTHENTICATION_ALLOWED

Successful authentication before lockout:
- resets consecutive-failure progression to zero

Successful authentication after lock expiry:
- must restore the account to a clean usable authentication state according
  to the specification.

IMPORTANT:

Do not model the source-code +2 anomaly.

Do not model a 3-minute lock.

Those are implementation observations, not test oracle.

==================================================
4. GENERATION TARGET
==================================================

Generate approximately 8–10 UNIQUE AI-generated test cases.

Continue IDs sequentially beginning:

FR02-AI-015

Expected end range should be approximately:

FR02-AI-022 .. FR02-AI-024

Do not pad the count.

Every test must exercise a distinct state-transition behavior.

==================================================
5. REQUIRED STATE SCENARIOS
==================================================

Cover at minimum:

A. Failure progression

1. First failed attempt:
   NORMAL -> FAILURE_SEQUENCE_ACTIVE
   Not locked.

2. Second consecutive failed attempt:
   Still not locked.

3. Third consecutive failed attempt:
   Account enters LOCKED state.

Important:
If exact HTTP status returned by the THIRD request itself is not explicitly
specified:
Expected HTTP Status = NOT SPECIFIED
Expected state after request = LOCKED

B. Request while locked

Test a subsequent login request during the lock window.

Include both:

- wrong credentials while locked
- correct credentials while locked

Expected semantic behavior:
authentication must be rejected while lock is active.

Do not assume correct password bypasses lockout.

Use documented locked response status only if explicitly available.

C. Lock duration boundary

Specification duration:
30 seconds.

Design state tests around:

- clearly before expiry, e.g. T+25s
- clearly after expiry, e.g. T+32s

Do NOT depend on exact scheduler precision at exactly 30.000 seconds.

If you discuss T=30s itself, label exact millisecond behavior:
IMPLEMENTATION/TIMING TOLERANCE – NOT SUITABLE AS STRICT BLACK-BOX ORACLE.

D. Successful-login reset

Generate a case:

wrong login
-> then successful login
-> subsequent wrong login must behave as the FIRST failure of a new
   consecutive-failure sequence.

Do not inspect login_attempts internally.

Validate externally through observable lockout behavior.

E. Consecutive-failure semantics

Generate a case showing failures must be consecutive.

Example conceptual sequence:

wrong
-> success
-> wrong
-> wrong

The two failures after the success must not be treated as failure #3 from the
earlier sequence.

Expected behavior must come from the SRS reset-on-success rule.

F. Post-lock-expiry usability

After lockout expires:
- a valid credential attempt should be processed normally
- account should not remain permanently inaccessible

If the specification does NOT explicitly define whether the failure counter is
reset automatically merely by time expiry, do NOT invent that internal state.

Test only externally observable behavior.

==================================================
6. TEST CASE FORMAT
==================================================

Append each generated case to:

23127259/testcases/FR02_AI_DRAFT.md

Use the same format as Stage 1A.2.

Every case must include:

- Test Case ID
- Title
- Technique
- Requirement reference
- Preconditions
- Request method
- Endpoint
- Headers
- Exact sequence of requests/actions
- State Before
- Expected HTTP Status per step where specified
- Expected semantic response
- State After
- Oracle Confidence
- Notes

Technique should be one or more of:

STATE TRANSITION
BVA
SEQUENCE TESTING
NEGATIVE

==================================================
7. STATE-INDEPENDENCE RULE
==================================================

These are design-level test cases.

Each formal test case should declare a deterministic precondition.

Examples:

Precondition:
Dedicated lockout test account exists and is currently unlocked with no active
consecutive-failure sequence.

Do not assume one formal test case happens to inherit the correct state from a
previous unrelated case.

When later implementing Postman:
setup/reset will be designed explicitly.

Do NOT implement that setup now.

==================================================
8. STATUS-CODE DISCIPLINE
==================================================

Do not invent exact statuses.

For each step:

If SRS/API-SPEC explicitly gives status:
use it.

If only semantic behavior is specified:
write:

Expected HTTP Status: NOT SPECIFIED
Expected semantic behavior: <spec-derived behavior>

Especially preserve this rule for:
- the third failed request itself
- timing transition behavior where exact response status is undocumented

==================================================
9. HUMAN-CASE INTEGRITY
==================================================

Do NOT create any:

FR02-HUM-xxx

The final human-designed extension cases will be chosen only AFTER:
1. >=35 AI-generated cases exist
2. Human Audit is complete
3. actual remaining coverage gaps are identified

Ideas previously suggested by AI in planning documents are not automatically
eligible as final Human cases.

==================================================
10. DO NOT AUDIT
==================================================

This is still AI GENERATION.

Do not classify cases:
VALID
INVALID
INCOMPLETE

The student will do that later.

You may use Oracle Confidence:

EXPLICIT
PARTIAL
SPEC-UNDEFINED

==================================================
11. UPDATE STAGE SUMMARY
==================================================

Update the summary table at the top of:

23127259/testcases/FR02_AI_DRAFT.md

It should contain:

| Stage | ID Range | Generated Count |
|---|---|---:|
| 1A.2 Domain/BVA | FR02-AI-001..014 | 14 |
| 1A.3 State/Lockout | FR02-AI-015..XXX | N |

Then show cumulative total.

Do not renumber existing cases.

==================================================
12. AI AUDIT LOG
==================================================

Determine the next real interaction ID.

Expected:
INT-007

Create:

23127259/ai/interactions/INT-007-fr02-lockout-state-generation.md

Record truthfully:
- Interaction ID
- AI Tool
- Model
- real date/time
- Stage:
  FR-02 Stage 3 – Lockout State-Transition Generation
- Exact prompt
- Full AI output

Update:

23127259/ai/AI_AUDIT_REPORT.md

Do not fabricate any metadata.

==================================================
13. QUALITY CHECK
==================================================

Before finishing verify:

- FR02-AI-015 explicitly covers failure #1
- failure #1 does not lock account
- failure #2 does not lock account
- failure #3 transitions account into LOCKED state
- exact response of failure #3 is not invented if unspecified
- correct credentials while locked do not bypass lock
- before-expiry and after-expiry behavior are distinguished
- reset-on-success sequence is covered
- consecutive-failure semantics are covered
- no implementation anomaly is used as expected behavior
- no Human cases generated
- no duplicate semantics with FR02-AI-001..014
- only FR-02 appears

==================================================
14. GIT POLICY
==================================================

Do NOT commit.

The FR-02 AI-generation commit occurs after all FR-02 generation stages and
deduplication are complete.

At the end report:

1. Interaction ID
2. IDs generated in this stage
3. Generated count
4. State scenarios covered
5. Oracle-confidence breakdown
6. Any SPEC-UNDEFINED state questions
7. Cumulative FR-02 AI count
8. Remaining number needed to reach >=35
9. git status

Then STOP.

Next stage:

PHASE 1A.4 – FR-02 SECURITY TEST GENERATION
```

---

## INT-008 – Phase 1A.4: FR-02 Security Test Generation

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-09-01 18:59:26+07:00
- **Interaction File:** [`../interactions/INT-008-fr02-security-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-008-fr02-security-generation.md)

### Exact Prompt

```text
/Speckit We are continuing with:

PHASE 1A.4 – FR-02 SECURITY TEST CASE GENERATION

This is the FOURTH FR-02 AI-generation interaction.

Current FR-02 AI inventory:

FR02-AI-001 .. FR02-AI-024
Cumulative AI-generated count: 24

This stage generates ONLY security-focused FR-02 test cases.

DO NOT:
- generate schema-only cases
- generate general malformed/error cases already covered
- generate Human-designed extension cases
- audit VALID / INVALID / INCOMPLETE
- execute Postman or Newman
- run the SUT
- confirm candidate bugs
- inspect server.js/database.js as the expected-result oracle
- generate FR-10 or FR-14 tests
- commit yet

==================================================
1. PRESERVE PRIOR AI OUTPUT
==================================================

Do NOT silently correct or rewrite previously generated cases
FR02-AI-001..024.

This is important for the later Human Audit.

In particular, some previous AI cases may contain questionable assumptions,
for example internal failure-counter state after lock expiry.

Leave them exactly as generated.

The student will later classify every case as:

VALID
INVALID
INCOMPLETE

and correct them during the Human Audit phase.

==================================================
2. AUTHORITATIVE INPUT
==================================================

Read:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md
23127259/testcases/FR02_AI_DRAFT.md
23127259/docs/SECURITY_APPLICABILITY.md

Also consult authoritative:

- EShop SRS / README requirements
- api_specification.md

Expected results must come only from:

[SRS]
[API-SPEC]

Do NOT derive the oracle from:
- server.js
- database.js
- OBS-xx implementation observations
- known candidate bugs

==================================================
3. SECURITY REQUIREMENT DISCIPLINE
==================================================

Use these authoritative security requirements:

SEC-01:
Passwords must not be stored in plaintext.

SEC-02:
Security-sensitive APIs must require a valid JWT.

SEC-03:
Admin APIs must verify role='admin'.

SEC-04:
User-controlled UI-rendered data must be safely escaped.

SEC-05:
Database queries must use parameterized queries.

SEC-06:
Profile update must not permit client-side role modification.

SEC-07:
Password-reset OTP must have sufficient entropy, expiry, and single-use.

For FR-02:

SEC-01:
PARTIAL black-box coverage.

SEC-02:
INDIRECT / AUTHENTICATION DEPENDENCY.
POST /api/login issues the JWT; it does not itself require JWT.

SEC-05:
PARTIAL black-box behavioral coverage through injection probes.

SEC-03:
NOT directly applicable to POST /api/login.

SEC-04:
UI scoped, not a core login API test.

SEC-06:
NOT applicable to selected FR-02 endpoint.

SEC-07:
Belongs to password-reset / FR-03, not FR-02.

Do NOT force SEC-03/04/06/07 cases into FR-02 just to increase count.

==================================================
4. GENERATION TARGET
==================================================

Generate approximately 7–8 UNIQUE security-focused AI cases.

Continue IDs sequentially from:

FR02-AI-025

Expected end range:

approximately FR02-AI-031 or FR02-AI-032.

Do not pad count.

Each case must have a distinct security objective.

==================================================
5. REQUIRED SECURITY DIMENSIONS
==================================================

Cover the following where specification-supported.

--------------------------------------------------
A. SEC-05 – SQL Injection Behavioral Probes
--------------------------------------------------

Generate:

1. SQL injection-like payload in email
2. SQL injection-like payload in password

Examples may include classic authentication-bypass strings.

Expected behavior:

- payload must not cause unauthorized authentication
- authentication must not succeed unless valid credentials are genuinely
  supplied

Label:

SEC-05 – PARTIAL BLACK-BOX EVIDENCE

Do NOT claim that failure of an injection attack proves that parameterized
queries are implemented.

--------------------------------------------------
B. Credential Enumeration / Error Disclosure
--------------------------------------------------

Generate a security case comparing:

A:
registered email + incorrect password

versus

B:
unregistered syntactically valid email + arbitrary password

Security objective:

the response must not reveal which credential element is incorrect or whether
the email exists, where the SRS explicitly requires generic credential-error
behavior.

This must be distinct from FR02-AI-003 and FR02-AI-004:

Those cases test authentication rejection individually.

This new case tests CROSS-RESPONSE SECURITY EQUIVALENCE / INFORMATION
DISCLOSURE.

Do not create a semantic duplicate.

--------------------------------------------------
C. Sensitive Data Exposure
--------------------------------------------------

Generate a successful-login security case asserting that sensitive credential
material should not be exposed in the API response where supported by the
security requirements.

Separate clearly:

SEC-01:
password storage at rest — PARTIAL / not fully provable via API

from

[ADDITIONAL-SEC]:
plaintext password or credential material appearing in the API response.

Do not claim response-field absence alone proves SEC-01 compliance.

--------------------------------------------------
D. Token Issuance on Authentication Failure
--------------------------------------------------

Generate a case asserting:

invalid credentials must NOT result in successful authentication and must NOT
issue a usable authentication token.

This security assertion must be distinct from merely checking HTTP 401.

If exact error schema is unspecified, do not invent fields.

--------------------------------------------------
E. Token Issuance During Active Lock
--------------------------------------------------

Generate a security case:

account is in LOCKED state
-> submit correct credentials during active lock

Security objective:

lockout must not be bypassed
and no successful authenticated session/token should be issued.

Avoid duplicating FR02-AI-019 by making the security assertion focus
specifically on authentication/token issuance rather than only state
transition.

If this would still be semantically duplicate after review, do NOT create it;
choose another distinct security dimension.

--------------------------------------------------
F. SEC-02 Supporting Token-Usability Probe
--------------------------------------------------

At most one or two supporting cases may verify that a JWT returned by
successful login functions as the authentication credential expected by a
documented protected endpoint.

Clearly label:

SEC-02 SUPPORTING / INDIRECT FR-02 TEST

Possible conceptual flow:

1. POST /api/login with valid credentials
2. capture returned JWT
3. call one documented protected endpoint using:
   Authorization: Bearer <token>
4. authenticated request should be accepted if all other preconditions are met

Optionally contrast with a tampered token.

However:

- do not turn this stage into testing another feature
- do not create a large downstream endpoint suite
- choose the simplest documented protected endpoint available
- document that SEC-02 enforcement belongs primarily to the protected
  endpoint, while FR-02 provides the token

==================================================
6. DO NOT CREATE UNSUPPORTED SECURITY REQUIREMENTS
==================================================

Do NOT generate cases merely because they are common security practices if the
assignment/SRS does not define an oracle.

Examples requiring caution:

- JWT expiration
- refresh tokens
- token revocation
- MFA
- IP-based throttling
- CAPTCHA
- arbitrary password maximum length
- account lock based on IP

If useful, these may later appear as exploratory observations, but they must
not become specification-backed expected failures.

==================================================
7. TEST CASE FORMAT
==================================================

Append cases to:

23127259/testcases/FR02_AI_DRAFT.md

Use the existing format.

Every test must contain:

- Test Case ID
- Title
- Technique
- Security classification
- Requirement reference
- Preconditions
- Request Method
- Endpoint
- Headers
- Exact request data / request sequence
- Expected HTTP Status only when specified
- Expected semantic result
- Expected security result
- State Before
- State After if relevant
- Oracle Confidence
- Black-box limitation
- Notes

Technique may include:

SECURITY
NEGATIVE
INJECTION PROBE
INFORMATION DISCLOSURE
AUTHENTICATION
SEQUENCE TESTING

==================================================
8. ORACLE CONFIDENCE
==================================================

Use:

EXPLICIT
PARTIAL
SPEC-UNDEFINED

Examples:

SQL injection probe:
PARTIAL
because behavioral resistance does not prove parameterized implementation.

Sensitive response field:
PARTIAL unless explicit response exclusion is specified.

Generic wrong-email / wrong-password behavior:
EXPLICIT if SRS explicitly requires non-disclosure.

Downstream JWT usability:
PARTIAL / INDIRECT where appropriate.

==================================================
9. DUPLICATION RULE
==================================================

Before adding each case compare against:

FR02-AI-001..024.

Do NOT add a case if its only difference is wording.

Examples:

FR02-AI-003 already verifies wrong-password rejection.

A new security test is acceptable only if it adds a different assertion,
such as comparing its error message against the unregistered-email response.

FR02-AI-019 already tests correct password during lockout.

Do not duplicate it unless the new test has a genuinely separate security
assertion not already represented.

==================================================
10. HUMAN-CASE INTEGRITY
==================================================

Do NOT create:

FR02-HUM-xxx

Actual Human-designed extension cases are selected only after:

1. >=35 AI-generated cases are complete
2. Human Audit is completed
3. real coverage gaps are identified

Prior AI planning suggestions do NOT count as Human cases.

==================================================
11. UPDATE SUMMARY
==================================================

Update the summary at the top of:

23127259/testcases/FR02_AI_DRAFT.md

Maintain:

| Stage | ID Range | Generated Count |
|---|---|---:|
| 1A.2 Domain/BVA | FR02-AI-001..014 | 14 |
| 1A.3 State/Lockout | FR02-AI-015..024 | 10 |
| 1A.4 Security | FR02-AI-025..XXX | N |

Show cumulative total.

Do not renumber old cases.

==================================================
12. AI AUDIT LOGGING
==================================================

Determine the next real interaction ID.

Expected:
INT-008

Create:

23127259/ai/interactions/INT-008-fr02-security-generation.md

Record truthfully:

- Interaction ID
- AI Tool
- Model
- actual date/time
- Stage:
  FR-02 Stage 4 – Security Test Generation
- Exact prompt
- Full AI output

Update:

23127259/ai/AI_AUDIT_REPORT.md

Do not fabricate metadata.

==================================================
13. QUALITY GATE
==================================================

Before finishing verify:

- only FR-02 security tests were generated
- no FR02-HUM IDs exist
- no source-derived implementation behavior became expected behavior
- SEC mappings are correct
- SEC-01 limitation is documented
- SEC-05 limitation is documented
- credential enumeration test is cross-response, not duplicate rejection
- no unnecessary SEC-03/04/06/07 cases created
- no JWT expiry requirement invented
- cases are semantically distinct from FR02-AI-001..024

==================================================
14. GIT POLICY
==================================================

Do NOT commit.

At the end report:

1. Interaction ID
2. IDs generated
3. Generated count
4. Security dimensions covered
5. SEC requirement mapping
6. Additional-security dimensions
7. Oracle-confidence breakdown
8. Cases intentionally NOT generated due to lack of requirement
9. Cumulative FR-02 AI count
10. Remaining cases needed to reach >=35
11. git status

Then STOP.

Next stage:

PHASE 1A.5 – FR-02 SCHEMA AND ERROR-CONTRACT TEST GENERATION
```

---

## INT-009 – Phase 1A.5: FR-02 Response Schema and Error-Contract Test Generation

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-09-01 19:02:22+07:00
- **Interaction File:** [`../interactions/INT-009-fr02-schema-error-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-009-fr02-schema-error-generation.md)

### Exact Prompt

```text
/Speckit We are continuing with:

PHASE 1A.5 – FR-02 RESPONSE SCHEMA AND ERROR-CONTRACT TEST GENERATION

This is the FIFTH FR-02 AI-generation interaction.

Current FR-02 AI inventory:

FR02-AI-001 .. FR02-AI-031
Cumulative AI-generated count: 31

This stage generates ONLY:

1. response-schema validation cases
2. documented success/error contract cases
3. response-type / structural assertions
4. any remaining API-contract case that is genuinely distinct

DO NOT:
- generate additional general domain tests already covered
- generate additional lockout state tests already covered
- generate a new dedicated security suite
- generate Human-designed cases
- audit VALID / INVALID / INCOMPLETE
- execute Postman/Newman
- run the SUT
- inspect server.js/database.js as oracle
- confirm bugs
- generate FR-10/FR-14 tests
- commit yet

==================================================
1. PRESERVE ALL EXISTING AI OUTPUT
==================================================

Do NOT rewrite, repair, renumber, or silently improve:

FR02-AI-001 .. FR02-AI-031

Even if some previous AI cases contain questionable assumptions or imperfect
security classification, preserve them for the later Human Audit.

Examples that must remain untouched:
- assumptions about internal post-lockout counter state
- SEC-01 classification nuances
- supporting downstream JWT tests

The later Human Audit is responsible for classifying each AI case as:
VALID / INVALID / INCOMPLETE.

==================================================
2. AUTHORITATIVE SOURCES
==================================================

Read:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md
23127259/testcases/FR02_AI_DRAFT.md
23127259/docs/SECURITY_APPLICABILITY.md

Also consult:

- EShop SRS / README requirements
- api_specification.md

Expected results must come ONLY from specification sources.

Do NOT use:
- server.js
- database.js
- known implementation observations
- candidate defect knowledge

as expected-result oracle.

==================================================
3. GENERATION TARGET
==================================================

Generate approximately:

5–7 UNIQUE AI-generated cases.

Continue sequentially from:

FR02-AI-032

Expected end range:
approximately FR02-AI-036 .. FR02-AI-038.

Quality is more important than stopping at exactly 35.

Do NOT pad the suite merely to increase count.

==================================================
4. SUCCESS RESPONSE CONTRACT
==================================================

Analyze the documented successful login response from api_specification.md.

Generate schema/contract cases only for fields explicitly documented.

Potential assertions may include:

- HTTP status if explicitly documented
- response is valid JSON
- top-level documented fields exist
- token exists
- token is a string if specified/inferable from contract
- user object exists if documented
- documented user fields have expected primitive/object types
- Content-Type if API contract provides enough basis

IMPORTANT:

Do not invent required fields that do not appear in api_specification.md.

If a particular property is shown only in an example but not normatively
required, label the oracle confidence appropriately.

==================================================
5. INVALID-CREDENTIAL ERROR CONTRACT
==================================================

Generate a schema/contract test for invalid credentials.

Focus on:

- documented HTTP status if explicit
- JSON response form
- documented error/message field
- absence of a success token
- generic credential error semantics

Avoid duplicating:

FR02-AI-003
FR02-AI-004
FR02-AI-027
FR02-AI-029

Those already test:
- wrong-password rejection
- unknown-email rejection
- cross-response equivalence
- no token on authentication failure

A new case is allowed only if its PRIMARY purpose is response-contract/schema
validation rather than authentication behavior.

==================================================
6. LOCKED-ACCOUNT ERROR CONTRACT
==================================================

If the API specification documents the locked-account response:

Generate one schema/contract case covering:

- response must be valid error JSON
- documented error/message field
- no successful token/session issued
- exact HTTP status only if explicitly documented

Do not duplicate state cases FR02-AI-017..021.

The new case should validate RESPONSE SHAPE, not lockout lifecycle.

If the exact locked response schema is NOT specified, write:

Oracle Confidence: PARTIAL / NOT SPECIFIED

and do not invent a schema.

==================================================
7. RESPONSE TYPE / STRUCTURE CASES
==================================================

Consider distinct contract checks such as:

A. Successful response is parseable JSON.

B. JWT/token field has the expected primitive type.

C. `user` is an object where documented.

D. Error responses use the documented error structure rather than returning
successful response structure.

E. Successful response does not accidentally match an error schema and vice
versa.

Only create cases that are meaningful and non-duplicative.

==================================================
8. CONTENT-TYPE DISCIPLINE
==================================================

If the specification explicitly requires or clearly defines JSON responses,
you may generate a Content-Type contract test.

If Content-Type is not explicitly specified:

do not claim an exact header value such as:
application/json; charset=utf-8

unless supported.

Use:
Oracle Confidence = PARTIAL

where appropriate.

==================================================
9. REQUEST ERROR-CONTRACT CASES
==================================================

Do NOT regenerate these already-covered semantic inputs:

- malformed email
- empty email
- missing email
- null email
- whitespace email
- empty password
- missing password
- null password

Those cases already exist.

However, you MAY generate at most one contract-focused case that takes one
representative malformed/missing request and checks:

"Does the API return a structurally valid documented error response?"

Only if this is genuinely distinct from the existing input-domain case.

If exact malformed-request response schema is undocumented:
do not invent it.

==================================================
10. JSON PARSING / MALFORMED JSON
==================================================

Review whether invalid JSON body has already been covered.

If NOT already represented in FR02-AI-001..031:

you may add a case for syntactically invalid JSON request body.

But carefully separate:

transport/parser behavior
from
FR-02 business authentication behavior.

If the SRS/API-SPEC does not define the exact status:

Expected HTTP Status: NOT SPECIFIED
Expected semantic result: request must not result in successful login
Oracle Confidence: PARTIAL

Do not assert arbitrary 400 unless documented.

==================================================
11. TEST CASE FORMAT
==================================================

Append to:

23127259/testcases/FR02_AI_DRAFT.md

Use the same detailed format as existing cases.

Every generated case must contain:

- Test Case ID
- Title
- Technique
- Requirement reference
- Preconditions
- Request Method
- Endpoint
- Headers
- Request Body / request sequence
- Expected HTTP Status
- Expected Response Contract
- Required Fields
- Field Types
- Fields That Must Not Indicate Successful Authentication
- Oracle Confidence
- Specification Limitations
- Notes

Technique should primarily be:

SCHEMA VALIDATION
API CONTRACT
NEGATIVE CONTRACT
RESPONSE VALIDATION

==================================================
12. DO NOT OVERSTATE JSON SCHEMA
==================================================

There is no permission to invent a formal JSON Schema if the specification
does not define one.

Examples:

If API spec says:

{
  "message": "...",
  "token": "...",
  "user": {...}
}

you may test documented shape and primitive/object types.

You may NOT invent:
- minLength
- regex
- additionalProperties=false
- undocumented nullable constraints
- exact timestamp formatting
- undocumented user object fields

Mark unspecified details accordingly.

==================================================
13. DUPLICATION CHECK
==================================================

Before adding every case compare it against:

FR02-AI-001 .. FR02-AI-031.

Do not generate a new test merely because it uses different wording.

Specifically avoid duplicates of:

FR02-AI-001 / 002
successful authentication

FR02-AI-003 / 004
credential rejection

FR02-AI-017..024
lockout behavior

FR02-AI-027
generic error equivalence

FR02-AI-028
sensitive response content

FR02-AI-029
token omitted on auth failure

FR02-AI-030 / 031
downstream JWT use

Schema cases must add new contract assertions.

==================================================
14. HUMAN-CASE INTEGRITY
==================================================

DO NOT generate any:

FR02-HUM-xxx

Actual human extension cases are selected only after:

1. AI generation is complete
2. every AI case has undergone Human Audit
3. actual uncovered gaps are identified

Previous AI planning suggestions are NOT automatically Human cases.

==================================================
15. UPDATE SUMMARY
==================================================

Update the summary table in:

23127259/testcases/FR02_AI_DRAFT.md

Expected structure:

| Stage | ID Range | Generated Count |
|---|---|---:|
| 1A.2 Domain/BVA | FR02-AI-001..014 | 14 |
| 1A.3 State/Lockout | FR02-AI-015..024 | 10 |
| 1A.4 Security | FR02-AI-025..031 | 7 |
| 1A.5 Schema/Error Contract | FR02-AI-032..XXX | N |

Show cumulative count.

Do NOT renumber previous cases.

==================================================
16. AI AUDIT LOGGING
==================================================

Determine the next real AI interaction ID.

Expected:
INT-009

Create:

23127259/ai/interactions/INT-009-fr02-schema-error-generation.md

Record truthfully:

- Interaction ID
- AI Tool
- Model
- actual date/time
- Stage:
  FR-02 Stage 5 – Schema and Error Contract Generation
- Exact prompt
- Full AI output

Update:

23127259/ai/AI_AUDIT_REPORT.md

Do not fabricate metadata.

==================================================
17. QUALITY GATE
==================================================

Before finishing verify:

- only FR-02 cases generated
- all IDs sequential from FR02-AI-032
- no Human IDs
- schema cases add distinct assertions
- no implementation-derived expected behavior
- no undocumented fields invented
- no arbitrary HTTP statuses invented
- malformed request exact status remains unspecified where appropriate
- previous AI cases remain unchanged
- total FR-02 AI count is now >=35

==================================================
18. GIT POLICY
==================================================

DO NOT COMMIT YET.

Even if cumulative count reaches >=35, generation is not frozen until the
next stage:

PHASE 1A.6 – FR-02 AI COVERAGE REVIEW, DEDUPLICATION, AND FREEZE

That stage will:

- check duplicate semantics
- check requirement coverage
- identify AI-generated gaps
- remove/merge duplicates if needed
- preserve evidence of removed cases
- ensure final AI-generated count remains >=35
- freeze the inventory
- then create the generation commit

At the end report:

1. Interaction ID
2. IDs generated
3. Generated count
4. Schema dimensions covered
5. Error-contract dimensions covered
6. Oracle confidence breakdown
7. SPEC-UNDEFINED contract details
8. Cumulative FR-02 AI count
9. Whether >=35 has been reached
10. git status

Then STOP.

Next stage:

PHASE 1A.6 – FR-02 AI COVERAGE REVIEW, DEDUPLICATION, AND FREEZE
```

---

## INT-010 – Phase 1A.6 (Part A): AI Prompt Log Verbatim Repair

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-09-01 19:26:56+07:00
- **Interaction File:** [`../interactions/INT-010-ai-prompt-log-verbatim-repair.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-010-ai-prompt-log-verbatim-repair.md)

### Exact Prompt

```text
/Speckit IMPORTANT ADDITIONAL AI AUDIT REQUIREMENT

Create and continuously maintain a consolidated prompt registry:

23127259/ai/prompts/AI_PROMPT_LOG.md

This file must contain EVERY AI prompt I send during HW06, in chronological
interaction order.

This is separate from the per-interaction files under:

23127259/ai/interactions/

The purpose is to provide one master file containing all exact prompts used
throughout the assignment.

==================================================
1. REQUIRED FILE STRUCTURE
==================================================

Create:

23127259/ai/prompts/AI_PROMPT_LOG.md

Use this structure:

# HW06 – Consolidated AI Prompt Log

Student: Nguyễn Tấn Thắng
Student ID: 23127259

> This document contains the exact prompts submitted to AI tools during HW06.
> Prompts are preserved verbatim and ordered by interaction ID.
> AI outputs are stored separately in `../interactions/`.

## Prompt Index

| INT | Date/Time | Tool | Model | Stage / Purpose | Prompt Available | Interaction File |
|---|---|---|---|---|---|---|

---

## INT-001 – <Stage Name>

**Tool:** ...
**Model:** ...
**Date/Time:** ...
**Interaction File:** `../interactions/INT-001-....md`

### Exact Prompt

```text
EXACT ORIGINAL PROMPT VERBATIM
```

---

## INT-011 – Phase 1A.6 (Part B): FR-02 AI Generation Coverage Review and Freeze

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-09-01 19:33:18+07:00
- **Interaction File:** [`../interactions/INT-011-fr02-generation-coverage-freeze.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-011-fr02-generation-coverage-freeze.md)

### Exact Prompt

```text
/Speckit /Speckit We are continuing with:

PHASE 1A.6 (PART B) – FR-02 AI COVERAGE REVIEW, GENERATION FREEZE, AND COMMIT

IMPORTANT AUDIT NUMBERING CORRECTION:

The immediately PREVIOUS interaction, which repaired AI_PROMPT_LOG.md using
transcript_full.jsonl, was itself a real AI interaction.

Therefore:

PREVIOUS INTERACTION = INT-010
CURRENT INTERACTION = INT-011

Do NOT reuse INT-010 for this turn.

==================================================
1. FIRST BACKFILL INT-010
==================================================

Before doing coverage review, create:

23127259/ai/interactions/INT-010-ai-prompt-log-verbatim-repair.md

INT-010 corresponds to the immediately previous interaction whose purpose was:

"AI Prompt Log Verbatim Repair"

Use the actual Antigravity transcript/history to recover:

- exact previous user prompt
- exact previous AI output
- real Tool
- real Model
- real Date
- real Local Time
- timezone UTC+07:00

The previous AI output began with:

# Phase 1A.6 (Part A) – AI Prompt Log Verbatim Repair Complete

Do NOT reconstruct either prompt or output.

Extract them from the real transcript/session.

Then append INT-010 to:

23127259/ai/prompts/AI_PROMPT_LOG.md

with the COMPLETE exact prompt verbatim.

Also update:

23127259/ai/AI_AUDIT_REPORT.md

==================================================
2. CURRENT INTERACTION = INT-011
==================================================

This current prompt is:

INT-011

Create:

23127259/ai/interactions/INT-011-fr02-generation-coverage-freeze.md

For INT-011 preserve:

- actual Tool
- actual Model
- actual Date/Time
- THIS COMPLETE PROMPT verbatim
- the COMPLETE AI output produced by this interaction

Also append THIS FULL PROMPT to:

23127259/ai/prompts/AI_PROMPT_LOG.md

and add INT-011 to:

23127259/ai/AI_AUDIT_REPORT.md

From now on:
EVERY new user prompt = a new INT number.

==================================================
3. VERIFY AI OUTPUT EVIDENCE FOR INT-001..010
==================================================

The prompt log is now repaired, but HW06 also requires AI OUTPUT.

Inspect:

23127259/ai/interactions/INT-001*
through
23127259/ai/interactions/INT-010*

For every interaction verify whether it contains the COMPLETE exact AI output.

Use statuses:

EXACT OUTPUT AVAILABLE
OUTPUT PARTIAL
OUTPUT MISSING – TODO

Do NOT call an output verbatim if it is only a summary.

If the full output exists in transcript_full.jsonl or agent history:
extract and save it exactly.

If not available:
mark TODO honestly.

Do NOT regenerate old outputs.

Update master table:

| INT | Exact Prompt | Exact Output | Transcript Source | Status |
|---|---|---|---|---|

==================================================
4. PRESERVE RAW FR-02 AI INVENTORY
==================================================

Current raw file:

23127259/testcases/FR02_AI_DRAFT.md

contains:

FR02-AI-001 .. FR02-AI-037

Raw AI count:
37

DO NOT:

- delete
- merge
- renumber
- rewrite
- silently correct
- change Oracle Confidence
- assign VALID / INVALID / INCOMPLETE
- create FR02-HUM cases

The raw AI output must remain preserved for the later mandatory Human Audit.

==================================================
5. CREATE FR-02 AI GENERATION COVERAGE REVIEW
==================================================

Create:

23127259/testcases/FR02_AI_GENERATION_REVIEW.md

Use:

# FR-02 AI Generation Coverage Review

## 1. Raw Inventory

Feature:
FR-02 – Login and Account Lockout

Pool:
A

Raw AI-generated cases:
37

ID range:
FR02-AI-001 .. FR02-AI-037

Generation interactions:
INT-005 .. INT-009

## 2. Stage Accounting

| Stage | Interaction | IDs | Count |
|---|---|---|---:|
| Requirement / Domain Analysis | INT-005 | Analysis only | 0 |
| Domain / BVA | INT-006 | FR02-AI-001..014 | 14 |
| Lockout / State | INT-007 | FR02-AI-015..024 | 10 |
| Security | INT-008 | FR02-AI-025..031 | 7 |
| Schema / Error Contract | INT-009 | FR02-AI-032..037 | 6 |
| TOTAL | | FR02-AI-001..037 | 37 |

==================================================
6. BUILD REQUIREMENT COVERAGE MATRIX
==================================================

Map all 37 raw cases to these areas:

- valid authentication
- invalid credentials
- registered email
- unregistered email
- malformed email
- empty email
- missing email
- null email
- whitespace email
- correct password
- incorrect password
- empty password
- missing password
- null password
- lockout N=1
- lockout N=2
- lockout N=3
- active lock
- correct credentials while locked
- 30-second pre-expiry boundary
- post-expiry behavior
- successful-login reset
- consecutive-failure semantics
- SQL injection behavioral probes
- credential enumeration / generic error
- sensitive response information
- token issuance on success
- token omission on failure
- JWT supporting behavior
- successful response schema
- invalid-credential error schema
- locked-account error schema
- malformed JSON handling
- Content-Type behavior
- extraneous-field behavior
- other exploratory / SPEC-UNDEFINED behavior

Use:

| Coverage Area | Raw AI Case IDs | Coverage Present? | Notes |
|---|---|---|---|

Do not perform Human Audit verdicts.

==================================================
7. POTENTIAL QUESTIONS FOR LATER HUMAN AUDIT
==================================================

Add:

## Potential Questions for Later Human Audit

Allowed labels ONLY:

POTENTIAL OVERLAP
POTENTIAL SCOPE QUESTION
POTENTIAL SPEC ASSUMPTION
POTENTIAL ORACLE QUESTION
POTENTIAL SECURITY CLASSIFICATION QUESTION

Do NOT use:

VALID
INVALID
INCOMPLETE

At minimum inspect and flag where appropriate:

FR02-AI-024
Potential assumption that post-lock-expiry failure progression is automatically
a fresh counter state.

FR02-AI-028
Sensitive data exposure in response is different from SEC-01 password storage
at rest.

FR02-AI-030
Uses downstream protected endpoint behavior; supporting / indirect FR-02 scope.

FR02-AI-031
Tampered JWT downstream behavior may similarly cross feature boundary.

FR02-AI-036
Check whether exact Content-Type requirement is explicitly documented or
AI-inferred.

FR02-AI-037
Extraneous properties / role handling may be exploratory and may lack a
formal login-spec oracle.

Also identify any other potential duplicate or questionable assumption.

Do not fix them.

==================================================
8. COVERAGE GAP CHECK
==================================================

Evaluate only HW06-required FR-02 dimensions:

- domain partitions
- boundary analysis
- relevant state transitions
- applicable security
- schema validation

If all major areas are represented, write:

No critical AI-generation coverage gap exists before Human Audit.

Do NOT generate additional cases for padding.

If a true required area has zero coverage:
report the gap but do not automatically generate new cases in this turn.

==================================================
9. CREATE GENERATION MANIFEST
==================================================

Create:

23127259/testcases/FR02_AI_GENERATION_MANIFEST.md

Include:

# FR-02 AI Generation Manifest

Feature:
FR-02 – Login and Account Lockout

Pool:
A

Raw AI-generated count:
37

ID range:
FR02-AI-001 .. FR02-AI-037

Generation interactions:
INT-005
INT-006
INT-007
INT-008
INT-009

Generation-support interactions:
INT-010
INT-011

Techniques represented:
- Equivalence Partitioning
- Boundary Value Analysis
- State Transition Testing
- Sequence Testing
- Negative Testing
- Security Probes
- Schema Validation
- Error Contract Testing

Oracle sources:
- EShop SRS
- api_specification.md
- HW06 requirements where applicable

Declaration:

"These 37 test cases are raw AI-generated test cases. They have not yet
undergone the mandatory student Human Test-Case Audit. Potential AI errors,
unsupported assumptions, overlap, or incomplete cases are intentionally
preserved for later VALID / INVALID / INCOMPLETE classification."

==================================================
10. HASH THE RAW AI ARTIFACT
==================================================

Run:

shasum -a 256 23127259/testcases/FR02_AI_DRAFT.md

Record:

Raw Generation SHA-256:
<hash>

in:

FR02_AI_GENERATION_MANIFEST.md

This is engineering evidence, not a PDF requirement.

==================================================
11. FREEZE RAW AI GENERATION
==================================================

If:

- 37 cases still exist
- IDs remain FR02-AI-001..037
- no raw cases were silently rewritten
- major HW06 dimensions have coverage
- AI audit evidence is honestly documented

then mark:

FR-02 AI GENERATION STATUS: FROZEN

Important:

This freezes only the RAW AI-generated inventory.

It does NOT mean:
- tests are valid
- tests are executable
- tests passed
- Human Audit is complete

==================================================
12. SECRET / EVIDENCE SAFETY CHECK
==================================================

Before committing run:

git diff
git status

Inspect all changed files.

Verify NO:

- runtime JWT values
- API keys
- secrets
- private tokens
- fake test executions
- fake Newman reports
- fake screenshots
- confirmed bug claims without execution
- modifications to other group members
- modifications to official SUT source

If a real JWT appears in documentation/transcripts:
replace only its VALUE with:

[REDACTED_RUNTIME_JWT]

Preserve surrounding context.

==================================================
13. COMMIT THE COMPLETED FR-02 AI GENERATION STEP
==================================================

After checks pass:

stage only relevant files for:

- FR-02 requirement analysis
- raw FR-02 AI generation
- generation coverage review
- generation manifest
- AI audit records
- prompt log
- interaction policy

Commit:

test(23127259): add AI-generated FR-02 test cases

Expected included files:

23127259/docs/FR02_REQUIREMENT_ANALYSIS.md
23127259/testcases/FR02_AI_DRAFT.md
23127259/testcases/FR02_AI_GENERATION_REVIEW.md
23127259/testcases/FR02_AI_GENERATION_MANIFEST.md

23127259/ai/AI_AUDIT_REPORT.md
23127259/ai/prompts/AI_PROMPT_LOG.md
23127259/ai/interactions/README.md

INT-001..011 interaction files that were updated/created for audit integrity.

Do not stage unrelated future artifacts.

Push:

origin/thang/hw06-implementation

Do NOT merge to main.

==================================================
14. FINAL COMPLETION REPORT
==================================================

Return:

# Phase 1A.6 Completion Report

## A. AI Audit Evidence

| INT | Exact Prompt? | Exact Output? | Transcript Source | Status |
|---|---|---|---|---|

Include:
INT-001 .. INT-011

## B. Prompt Log

- total interactions indexed
- exact prompts stored
- prompts requiring TODO
- consistency issues

## C. AI Output Evidence

- exact outputs recovered
- partial outputs
- missing outputs/TODO

## D. FR-02 Generation

- raw case count
- ID range
- stage accounting
- coverage summary
- potential questions
- critical coverage gaps

## E. Freeze

- status
- SHA-256

## F. Git

- files committed
- commit SHA
- push result
- git status

Then STOP.

DO NOT BEGIN HUMAN AUDIT.

Next phase:

PHASE 1B – FR-02 HUMAN TEST-CASE AUDIT
```

---

## INT-012 – Phase 1B.0: INT-011 Audit Repair + FR-02 Human Audit Workspace Preparation

- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date/Time:** 2026-09-01 19:37:53+07:00
- **Interaction File:** [`../interactions/INT-012-fr02-human-audit-preparation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-012-fr02-human-audit-preparation.md)

### Exact Prompt

```text
/Speckit /Speckit We are starting:

PHASE 1B.0 – INT-011 AUDIT REPAIR + FR-02 HUMAN AUDIT WORKSPACE PREPARATION

IMPORTANT:

The FR-02 raw AI generation has already been frozen:

FR02-AI-001 .. FR02-AI-037
Raw AI-generated count: 37
Generation commit: f6164ef

DO NOT modify the frozen raw AI-generated test cases.

This interaction has TWO purposes:

A. Correct a possible AI Audit evidence problem for INT-011.
B. Prepare the mandatory HUMAN Test-Case Audit workspace.

This interaction itself is:

INT-012

DO NOT perform the student's Human Audit decisions in this turn.

==================================================
PART A – REPAIR / VERIFY INT-011 EXACT OUTPUT
==================================================

There is a potential integrity issue in the previous completion report.

INT-011 was reported as:

Exact Prompt: YES
Exact Output: YES
Transcript source: transcript_full.jsonl Step 481

However, Step 481 appears to be the USER INPUT that started INT-011.

An AI interaction cannot truthfully preserve its own final output before that
output has actually completed.

Therefore verify INT-011 again from the NOW-COMPLETED transcript.

==================================================
A1. FIND THE REAL INT-011 TRANSCRIPT PAIR
==================================================

Inspect:

/Users/thangnhi/.gemini/antigravity-ide/brain/c80640ee-13f9-4258-ac3b-ab554a6053f1/.system_generated/logs/transcript_full.jsonl

Do NOT assume any output step number in advance.

Locate:

1. the USER_INPUT containing the complete prompt beginning approximately with:

PHASE 1A.6 (PART B) – FR-02 AI COVERAGE REVIEW, GENERATION FREEZE, AND COMMIT

2. the corresponding COMPLETED AI OUTPUT beginning approximately with:

# Phase 1A.6 Completion Report

Verify the JSONL entry `type` for both.

Record the actual step/index for:
- INT-011 prompt
- INT-011 output

The prompt entry and output entry MUST be different transcript records.

==================================================
A2. REPAIR INT-011 IF NECESSARY
==================================================

Update:

23127259/ai/interactions/INT-011-fr02-generation-coverage-freeze.md

Ensure it contains:

## Exact Prompt

the complete actual INT-011 USER prompt verbatim.

## Exact AI Output

the complete actual final AI response verbatim.

Do NOT store:
- this INT-012 prompt
- a summary
- the USER_INPUT as AI output
- reconstructed output

Update:

23127259/ai/AI_AUDIT_REPORT.md

with the verified INT-011 prompt/output transcript indices.

AI_PROMPT_LOG.md contains prompts only, so ensure INT-011 prompt remains the
exact prompt and do NOT insert AI output there.

==================================================
A3. DO NOT REWRITE HISTORY
==================================================

Generation commit:

f6164ef

has already been pushed.

Do NOT:
- amend it
- force push
- reset history
- delete evidence of the previous audit mistake

If INT-011 evidence required correction, create a NEW correction commit:

docs(23127259): correct INT-011 AI audit evidence

Push normally to:

origin/thang/hw06-implementation

This transparent correction is preferable to rewriting Git history.

==================================================
PART B – LOG THIS CURRENT INTERACTION AS INT-012
==================================================

Current interaction:

INT-012

Create:

23127259/ai/interactions/INT-012-fr02-human-audit-preparation.md

Record:

- actual Tool
- actual Model
- actual Date
- actual Local Time
- timezone UTC+07:00
- Stage:
  FR-02 Human Audit Preparation

Save THIS COMPLETE PROMPT verbatim.

Append THIS COMPLETE PROMPT verbatim to:

23127259/ai/prompts/AI_PROMPT_LOG.md

Update:

23127259/ai/AI_AUDIT_REPORT.md

IMPORTANT:

The complete final AI output for INT-012 cannot be extracted until this
interaction has finished.

Therefore do NOT fabricate the final Exact AI Output inside INT-012 before the
response exists.

Use a temporary marker if necessary:

Exact AI Output:
PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES

The NEXT interaction must backfill the completed INT-012 output from the real
transcript.

This rule applies to every future interaction.

==================================================
PART C – HUMAN AUDIT PRINCIPLE
==================================================

HW06 requires the learner to audit EVERY AI-generated test case and classify it:

VALID
INVALID
INCOMPLETE

with:
- reasoning
- corrections where necessary

Therefore the FINAL verdict must be a STUDENT decision.

AI may:
- organize the cases
- reproduce specification evidence
- identify the relevant requirement
- point out specification ambiguity
- prepare a review worksheet

AI MUST NOT:
- automatically assign final VALID / INVALID / INCOMPLETE verdicts
- automatically write the student's final rationale
- pretend that AI review is Human Review
- silently correct the raw AI-generated test cases

The student's explicit decision must be captured separately.

==================================================
PART D – PRESERVE FROZEN RAW GENERATION
==================================================

Read but DO NOT MODIFY:

23127259/testcases/FR02_AI_DRAFT.md

Frozen raw inventory:

FR02-AI-001 .. FR02-AI-037

SHA-256 currently recorded:

b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c

Verify the file hash still matches.

Run:

shasum -a 256 23127259/testcases/FR02_AI_DRAFT.md

If the hash differs:

STOP and report:

RAW AI GENERATION INTEGRITY WARNING

Do not continue Human Audit preparation until investigated.

==================================================
PART E – CREATE HUMAN AUDIT WORKSHEET
==================================================

Create or initialize:

23127259/ai/TC_AUDIT_FR02.md

Use:

# FR-02 Human Test-Case Audit

Feature:
FR-02 – Login and Account Lockout

Raw AI Generation:
FR02-AI-001 .. FR02-AI-037

Raw AI Generation Hash:
b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c

## Audit Policy

Every raw AI-generated case must receive a STUDENT verdict:

- VALID
- INVALID
- INCOMPLETE

For every case record:

1. raw AI case ID
2. raw AI title
3. specification/oracle basis
4. student verdict
5. student reasoning
6. student correction, if required
7. final disposition
8. student decision timestamp

The AI may prepare evidence but must not invent the student's decision.

==================================================
E1. MASTER AUDIT TABLE
==================================================

Create one row for all 37 cases:

| AI Case ID | Raw Title | Oracle Basis | Student Verdict | Student Reasoning | Student Correction | Final Disposition | Decision Time |
|---|---|---|---|---|---|---|---|

Populate:

AI Case ID
Raw Title
Oracle Basis

Leave these fields EMPTY / PENDING STUDENT REVIEW:

Student Verdict
Student Reasoning
Student Correction
Final Disposition
Decision Time

Use exactly:

PENDING STUDENT REVIEW

Do not pre-fill verdicts.

==================================================
PART F – PREPARE HUMAN REVIEW BATCH 1
==================================================

For manageability, Human Audit will be performed in FOUR batches:

Batch 1:
FR02-AI-001 .. FR02-AI-010

Batch 2:
FR02-AI-011 .. FR02-AI-020

Batch 3:
FR02-AI-021 .. FR02-AI-030

Batch 4:
FR02-AI-031 .. FR02-AI-037

THIS interaction prepares ONLY Batch 1.

Do NOT audit Batch 2–4 yet.

==================================================
F1. BATCH 1 REVIEW PACKET
==================================================

At the end of TC_AUDIT_FR02.md add:

## Human Review Batch 1 – FR02-AI-001..010

For EACH case reproduce concisely:

### FR02-AI-00X – <Raw Title>

Raw Technique:
<from frozen case>

Raw AI Expected Result:
<copy accurately from frozen case>

Relevant Specification Evidence:
<quote/reference only what SRS/API-SPEC actually supports>

Specification Ambiguity:
<if any, otherwise NONE IDENTIFIED>

Human Decision:

Verdict:
PENDING STUDENT REVIEW

Reasoning:
PENDING STUDENT REVIEW

Correction:
PENDING STUDENT REVIEW

Final Disposition:
PENDING STUDENT REVIEW

Do NOT recommend a verdict.

Do NOT write:
"should be VALID"
"likely INVALID"
"this is INCOMPLETE"

The purpose is to give the student the evidence needed to decide.

==================================================
PART G – STUDENT RESPONSE FORMAT
==================================================

At the END of the AI response, present Batch 1 in a compact decision table:

| ID | Short Test Objective | Key Oracle Question | Student Verdict |
|---|---|---|---|
| FR02-AI-001 | ... | ... | ? |
...
| FR02-AI-010 | ... | ... | ? |

Then explicitly ask the student to provide their decisions.

Use this response format:

FR02-AI-001
Verdict: VALID / INVALID / INCOMPLETE
Reasoning: <student's own reasoning>
Correction: <NONE or student's correction>

FR02-AI-002
Verdict:
Reasoning:
Correction:

...

FR02-AI-010
Verdict:
Reasoning:
Correction:

Do NOT proceed to Batch 2 until the student has supplied Batch 1 decisions.

==================================================
PART H – IMPORTANT: DO NOT AUTO-FILL HUMAN DECISIONS
==================================================

Even if a case seems obviously wrong, do not assign the verdict.

For example, later cases may contain possible issues such as:

- unsupported internal counter assumptions
- overlap
- cross-feature JWT checks
- Content-Type assumptions
- exploratory extraneous-field behavior

Those may be presented as specification questions when their batch is reached,
but the student's verdict is still required.

This preserves the distinction:

AI-assisted evidence preparation
vs
Human test-case audit decision.

==================================================
PART I – GIT POLICY
==================================================

Do NOT commit the incomplete Human Audit worksheet yet.

The Human Audit procedural commit should occur after ALL 37 cases have received
real student decisions.

Expected later commit:

test(23127259): audit AI-generated FR-02 test cases

For now:

- INT-011 audit correction may be separately committed if necessary
- TC_AUDIT_FR02.md remains uncommitted while audit is incomplete
- INT-012 audit preparation evidence remains uncommitted until the appropriate
  audit checkpoint unless the correction commit requires otherwise

Do NOT mix Human Extension cases into this commit.

==================================================
PART J – END REPORT
==================================================

Return:

# Phase 1B.0 Completion Report

## 1. INT-011 Evidence Repair

- verified prompt transcript step
- verified output transcript step
- prompt entry type
- output entry type
- correction required? YES/NO
- correction commit SHA, if applicable

## 2. INT-012 Audit Logging

- exact prompt stored?
- prompt log updated?
- output status:
  PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES

## 3. Raw Generation Integrity

- case count
- current SHA-256
- matches frozen manifest? YES/NO

## 4. Human Audit Workspace

- TC_AUDIT_FR02.md created/updated
- rows prepared: 37
- student verdicts pre-filled: 0
- Batch 1 prepared: FR02-AI-001..010

## 5. Git Status

Show git status.

Then present the Batch 1 Student Decision Table and STOP.

DO NOT BEGIN BATCH 2.

DO NOT ASSIGN HUMAN VERDICTS.
```

