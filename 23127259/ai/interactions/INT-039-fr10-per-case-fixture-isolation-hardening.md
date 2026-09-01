# Interaction Log: INT-039

- **Interaction ID:** INT-039
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 22:29:34+07:00
- **Timezone:** UTC+07:00
- **Project Stage:** Phase 2D.0.3 – FR-10 Per-Case Fixture Isolation + Fail-Fast Fixture Extraction
- **Transcript Reference:** `transcript_full.jsonl` (Prompt: Step 1753, Output: Pending backfill)

---

## 1. Submitted Prompt

```text
/Speckit /Speckit We found a MATERIAL fixture-isolation defect in the FR-10 execution
harness after reviewing the Phase 2D.0.2 report.

PHASE 2D.0.3 – FR-10 PER-CASE FIXTURE ISOLATION + FAIL-FAST FIXTURE EXTRACTION

Current execution-readiness commit:

d1afa4f

DO NOT run Postman.
DO NOT run Newman.
DO NOT call localhost.
DO NOT create live orders yet.

The previous report MUST NOT be treated as execution-ready until the following
contradictions are repaired.

==================================================
1. HUMAN-IDENTIFIED MATERIAL DEFECT
==================================================

The Phase 2D.0.2 report claims:

Unsafe Shared Mutable Fixtures:
0

But its own fixture table says:

orderPendingId
consumed by Folders 01..03, 05, 06, 08, HUM-005

orderConfirmedId
consumed by Folders 01..03, 07, HUM-004

orderShippingId
consumed by Folders 01, 03

orderId
consumed by:
AI-004
AI-041
HUM-001
HUM-003

orderAId
consumed by:
AI-033
HUM-002

These are NOT safely isolated merely because many expected mutations are
rejected.

Examples:

AI-001 is a VALID:
pending -> confirmed

Therefore a shared orderPendingId no longer remains pending after AI-001.

AI-002 is a VALID:
confirmed -> shipping

Therefore a shared orderConfirmedId no longer remains confirmed.

AI-003 is a VALID:
shipping -> delivered

Therefore a shared orderShippingId no longer remains shipping.

AI-004, AI-041, HUM-001, and HUM-003 all mutate lifecycle state and cannot
share one order created once at the beginning of the run.

Also:

A negative test MUST NOT share a mutable fixture with a later formal test merely
because the expected outcome is "rejected".

If the SUT contains the exact bug under test and the invalid mutation succeeds,
the shared fixture becomes polluted and contaminates later cases.

Test isolation must survive failing SUT behavior.

==================================================
2. AI AUDIT NUMBERING
==================================================

Previous interaction:

INT-038
FR-10 Fixture Provenance / Variable Dataflow / Route Readiness Audit

Current interaction:

INT-039

First backfill the COMPLETE exact output of INT-038 from the completed
Antigravity transcript.

Locate the actual:
- USER_INPUT
- corresponding PLANNER_RESPONSE

Do not guess indices.

Create:

23127259/ai/interactions/
INT-039-fr10-per-case-fixture-isolation-hardening.md

Record:
- actual Tool
- actual Model
- actual Date/Time
- timezone UTC+07:00
- Stage:
  FR-10 Per-Case Fixture Isolation + Fail-Fast Fixture Extraction
- THIS COMPLETE PROMPT verbatim

Append to:

23127259/ai/prompts/AI_PROMPT_LOG.md

Update:

23127259/ai/AI_AUDIT_REPORT.md

INT-039 Exact AI Output:

PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES

until this interaction completes.

==================================================
3. RAW / FORMAL ACCOUNTING MUST NOT CHANGE
==================================================

Frozen raw hash:

303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc

Formal executable cases:

46

Rejected raw AI:

FR10-AI-012

Human Extensions:

FR10-HUM-001 .. 005

Do NOT modify:
FR10_AI_DRAFT.md

Do NOT change Human Audit verdicts.

==================================================
4. NEW FIXTURE-ISOLATION RULE
==================================================

A mutable order fixture MUST NOT be shared across different formal IDs if ANY
of those formal cases can mutate it.

This applies even when mutation is EXPECTED to fail.

Reason:

if the SUT has a defect, an expected-rejected mutation may succeed and pollute
subsequent tests.

Therefore:

one formal case
=
one isolated mutable order fixture

unless the formal case itself intentionally requires multiple orders.

Exception:

pure synthetic ID cases that do not target a real resource may not require a
dedicated target order, except where a control order is required to verify
absence of unintended mutation.

==================================================
5. CO-LOCATE FIXTURE SETUP WITH FORMAL CASE
==================================================

Prefer deterministic per-case setup immediately before the formal action.

Naming pattern:

[FR10-AI-001][SETUP] ...
[FR10-AI-001][ACTION] ...
[FR10-AI-001][VERIFY] ...

All requests belong to ONE formal ID.

SETUP and VERIFY requests do NOT increase the formal-case count.

Avoid one giant reusable mutable fixture pool in Folder 00.

Folder 00 may still contain:

- Admin login
- User A login
- User B login
- truly immutable global setup

but mutable order creation/state preparation should be isolated per formal case
or per intentional multi-order Human case.

==================================================
6. UNIQUE FIXTURE VARIABLE STRATEGY
==================================================

Use deterministic case-scoped variables.

Examples:

order_FR10_AI_001
order_FR10_AI_002
order_FR10_AI_003
...
order_FR10_AI_041

For Human cases:

order_FR10_HUM_001

For HUM-002:

order_FR10_HUM_002_A
order_FR10_HUM_002_B

Variable naming may differ, but uniqueness must be machine-verifiable.

Do NOT keep ambiguous shared mutable variables such as:

orderId
orderPendingId
orderConfirmedId
orderShippingId

across unrelated formal IDs.

==================================================
7. STATE PRECONDITION PER FORMAL CASE
==================================================

For every formal case, independently establish its required starting state.

Example:

AI-003 requires shipping.

Its isolated setup must produce:

fresh pending order
-> Admin confirm
-> Admin ship

THEN:

AI-003 formal action:
shipping -> delivered

AI-014 also requires shipping.

It must receive a DIFFERENT fresh order and independently establish:

pending
-> confirmed
-> shipping

Then perform:

shipping -> confirmed

Do NOT let AI-014 consume the order mutated by AI-003.

==================================================
8. NEGATIVE CASE ISOLATION
==================================================

Apply dedicated fixture isolation to negative cases too.

Example:

AI-009:
pending -> shipping expected rejected

It must use its own pending order.

AI-010:
pending -> delivered expected rejected

It must use another pending order.

Do not assume AI-009 remains pending.

If AI-009 exposes a bug and becomes shipping, AI-010 must still execute from an
independent pending fixture.

This principle applies to:

- invalid skip cases
- backward cases
- terminal cases
- SEC-02
- SEC-03
- ownership cases
- malformed-status cases
- exploratory Human cases

where a real order is involved.

==================================================
9. AI-033 / AI-034 OWNERSHIP ISOLATION
==================================================

AI-033 needs its own User-A-owned pending order.

AI-034 needs a DIFFERENT User-A-owned order independently prepared to confirmed.

They must not share the same mutable order.

Creation actor:
User A

Attack/mutation actor:
User B

Persistence verification:
User A or another documented authorized actor

Do not reuse either ownership fixture for HUM-002.

==================================================
10. HUM-002 ISOLATION
==================================================

HUM-002 must create TWO dedicated fresh orders only for HUM-002:

A
B

Prove:

A != B

Both initially:
pending

Mutate:
A -> confirmed

Verify:
A = confirmed
B = pending

Neither A nor B may have been used by AI-033, AI-034, or another formal case.

==================================================
11. MULTI-STEP CASE ISOLATION
==================================================

The following MUST each have their own independent fresh order:

FR10-AI-004
FR10-AI-041
FR10-HUM-001
FR10-HUM-003

Do NOT use one shared:

orderId

for these four cases.

Each sequence may reuse its OWN order across the internal sequence because all
operations belong to the same formal case.

==================================================
12. REMOVE DANGEROUS ORDER-ID FALLBACK
==================================================

Current checkout extraction reportedly uses semantic logic:

jsonData.id
|| jsonData.order.id
|| jsonData.data.id
|| '1'

The fallback:

|| '1'

is FORBIDDEN.

It can silently cause the harness to mutate an unrelated Order ID 1 when
fixture creation fails or the response schema differs.

Remove every fallback to:
1
or another existing-looking order ID.

Use fail-fast extraction.

Semantic requirement:

const body = pm.response.json();

const id =
    body.id ??
    body.order?.id ??
    body.data?.id;

if (!id) {
    throw new Error(
        "Fixture checkout succeeded without a recognizable order ID; aborting"
    );
}

Only include response shapes that have documentary or controlled-smoke support.

Do not silently substitute an ID.

==================================================
13. CHECK CHECKOUT SUCCESS BEFORE WRITING VARIABLE
==================================================

Every fixture-creation helper must first verify that checkout actually produced
a successful response appropriate to the documented contract.

Do not write an order variable from:

- HTML error body
- authentication failure
- validation failure
- stock failure
- malformed JSON

If checkout fails:
the dependent formal case must not proceed using stale data.

Prefer clearing the target case variable BEFORE fixture creation.

Then populate only after successful extraction.

==================================================
14. INVENTORY / PRODUCT FIXTURE RISK
==================================================

Current checkout body reportedly hardcodes:

productId: 1
quantity: 1

Do a STATIC documentary check now:

Is product ID 1 a documented deterministic seed product?

If YES:
cite the source in fixture documentation.

If NO:
do not claim productId 1 is guaranteed.

Record:

RUNTIME FIXTURE SMOKE REQUIRED

before the full Newman run.

Also assess whether checkout reduces stock.

If repeated isolated checkouts may consume inventory:

document this as a runtime risk.

Do NOT inspect DB.

Do NOT execute yet.

==================================================
15. CANCEL ROUTE DOCUMENTATION CORRECTION
==================================================

The previous report says documented customer cancellation is:

PUT/POST /api/orders/:id/cancel

Our frozen formal FR-10 contract uses:

PUT /api/orders/:id/cancel

Correct all FR-10 harness documentation to state the executable formal route
exactly as:

PUT /api/orders/:id/cancel

Do NOT advertise POST cancellation coverage.

Do NOT add a POST formal case.

If some secondary document is ambiguous, record that ambiguity separately
without weakening the frozen executable endpoint.

==================================================
16. AUTH ROUTE SOURCE DISCIPLINE
==================================================

The previous report says:

POST /api/auth/login

Ensure the route basis comes from the actual authoritative API documentation,
not merely from a derived FR10_REQUIREMENT_ANALYSIS.md summary.

Document exact source path/section.

Do not alter route if already correct.

==================================================
17. REBUILD OPERATION ACCOUNTING
==================================================

After per-case fixture isolation, recalculate:

- authentication helpers
- checkout/order-creation setup calls
- prerequisite-state setup calls
- formal ACTION requests
- standalone VERIFY requests
- pm.sendRequest verification calls
- expected total network operations

The number will likely exceed:

113

That is acceptable.

Formal case count MUST remain:

46.

Accuracy and determinism are more important than a smaller network count.

==================================================
18. PER-CASE FIXTURE MATRIX
==================================================

Create:

23127259/postman/
FR10_PER_CASE_FIXTURE_MATRIX.md

Exactly 46 formal rows:

| Formal ID | Fixture Variable(s) | Creation Actor | Initial Creation State | Precondition Transitions | Formal Mutation | Persistence Actor | Shared Across Formal IDs? |

For every real-order formal case:

Shared Across Formal IDs? = NO

For synthetic malformed/nonexistent-ID cases:
describe the control fixture strategy if applicable.

==================================================
19. MACHINE-VERIFY ISOLATION
==================================================

Create/update validator:

23127259/postman/
validate_fr10_fixture_isolation.py

It must prove:

- 46 formal IDs
- AI-012 excluded
- no mutable order variable is referenced by >1 formal ID
- HUM-002 has exactly two dedicated order variables
- AI-033 and AI-034 have different User-A-owned fixtures
- AI-004, AI-041, HUM-001, HUM-003 use four different fixtures
- every required initial state has a real setup transition pipeline
- no fallback order ID "1"
- no stale prefilled order IDs
- fixture variable cleared before creation
- X-Student-Id included in all relevant HTTP mechanisms
- exact formal cancel method = PUT
- raw hash unchanged

No network I/O.

==================================================
20. FAILURE-TOLERANT COLLECTION ORDER
==================================================

Design the collection such that:

A failing formal case does not corrupt fixtures for later formal cases.

Examples:

If AI-009 unexpectedly succeeds:
AI-010 still receives a fresh pending order.

If AI-017 unexpectedly mutates a delivered order:
AI-018 still receives its own fresh delivered order.

If AI-033 unexpectedly permits cross-user cancellation:
HUM-002 is unaffected.

This is the required definition of isolation.

==================================================
21. UPDATE DOCUMENTATION
==================================================

Update:

FR10_FIXTURE_STRATEGY.md
FR10_VARIABLE_PROVENANCE.md
FR10_EXECUTION_VARIABLE_READINESS.md
FR10_HTTP_OPERATION_INVENTORY.md
FR10_MATERIALIZATION_DEEP_AUDIT.md
FR10_POSTMAN_IMPLEMENTATION_STRATEGY.md

Remove superseded claims about:

7 shared fixture families

if they are no longer accurate.

Do not leave contradictory old counts.

==================================================
22. NO EXECUTION
==================================================

STRICTLY DO NOT:

- send HTTP
- run Postman
- run Newman
- call localhost
- create orders
- inspect DB
- confirm bugs

Static harness repair only.

==================================================
23. GIT
==================================================

After validator passes:

commit:

fix(23127259): isolate FR-10 fixtures per formal case

Include:

- corrected collection
- environment if changed
- per-case fixture matrix
- fixture isolation validator
- updated execution-readiness documentation
- INT-038 backfill
- INT-039
- AI_AUDIT_REPORT.md
- AI_PROMPT_LOG.md

Push:

origin/thang/hw06-implementation

Do NOT merge main.

==================================================
24. END REPORT
==================================================

Return:

# Phase 2D.0.3 FR-10 Per-Case Fixture Isolation Report

## AI Audit
- INT-038 output backfilled
- INT-039 prompt stored
- INT-039 output pending

## Defect Confirmation
- previous shared mutable fixture defect confirmed: YES/NO
- affected fixture variables
- affected formal IDs

## Repairs
- per-case fixtures implemented
- shared mutable formal fixtures remaining
- order-ID fallback "1" removed
- fail-fast extraction implemented

## Special Isolation
- AI-033 fixture
- AI-034 fixture
- HUM-002 fixtures A/B
- AI-004 fixture
- AI-041 fixture
- HUM-001 fixture
- HUM-003 fixture

## Route Discipline
- login exact route
- checkout exact route
- cancellation exact route = PUT
- read exact route

## Product Fixture Risk
- productId 1 documentary guarantee YES/NO
- checkout inventory-consumption risk
- runtime smoke required YES/NO

## HTTP Reconciliation
- auth helper calls
- fixture creation calls
- prerequisite-state calls
- formal action/verify requests
- script-triggered calls
- expected total runtime HTTP
- formal count = 46

## Validator
- 46 fixture mappings
- shared mutable variables = 0
- fallback IDs = 0
- unsafe state dependency = 0
- PASS/FAIL

## Execution
Postman: NOT RUN
Newman: NOT RUN

## Git
- commit SHA
- push result
- working tree

Then STOP.

Next phase ONLY IF PASS:

PHASE 2D.1A – FR-10 MINIMAL AUTH + CHECKOUT + STATE-FIXTURE SMOKE
```

---

## 2. Exact AI Output

```markdown
PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES
```

---

## 3. Human Evaluation & Outcome

- **Verdict:** In progress. Conducting comprehensive per-case fixture isolation and fail-fast fixture extraction hardening. Designing dedicated co-located or case-scoped order fixtures for all 46 formal cases, eliminating fallback order ID '1', creating FR10_PER_CASE_FIXTURE_MATRIX.md and validate_fr10_fixture_isolation.py.
- **Status:** EXACT PROMPT STORED; OUTPUT PENDING BACKFILL.
