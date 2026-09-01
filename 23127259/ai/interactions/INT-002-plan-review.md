# Interaction Log: INT-002

- **Interaction ID:** INT-002
- **Tool:** Antigravity IDE Assistant
- **Model:** Opus Reasoning
- **Date & Time:** 2026-09-01 15:55:00+07:00
- **Purpose / Stage:** Initial Technical Implementation Planning for FR-02, FR-10, FR-14

---

## 1. Submitted Prompt
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

## 2. AI Output Summary
- Produced comprehensive implementation plan grounded in SUT source code inspection.
- Identified potential SUT implementation bugs (lockout counter arithmetic, lockout duration, plaintext password exposure in login responses, state transitions).
- Structured Postman collections, Newman execution commands, and Git commit roadmap.

---

## 3. Human Evaluation & Outcome
- **Review Finding:** Plan inspected implementation code prematurely and mapped security IDs (SEC-01..07) inaccurately. Needed methodological separation of specification from implementation.
- **Action:** Proceeded to revision phase in INT-003.
