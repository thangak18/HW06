# Interaction Log: INT-004

- **Interaction ID:** INT-004
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 18:25:00+07:00
- **Purpose / Stage:** Final Implementation Plan Freeze & Pre-Implementation Gate Confirmation

---

## 1. Submitted Prompt
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

## 2. AI Output Summary
- Corrected FR-10 state matrix to show `confirmed -> canceled` as valid for User and Admin.
- Refactored FR-02 oracles and removed dependency on internal DB fields in `/api/admin/users`.
- Clarified partial black-box coverage for SEC-01 and SEC-05.
- Enforced strict accounting ($\ge 120$ cases across 3 features) with distinct ID scheme and comprehensive inventory.
- Added Section 18 Final Pre-Implementation Gate checklist.

---

## 3. Human Evaluation & Outcome
- **Verdict:** VALID. Plan is 100% compliant, frozen, and approved for Phase 0 execution.
