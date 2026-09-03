# Interaction Log: INT-016

- **Interaction ID:** INT-016
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 19:56:42+07:00
- **Project Stage:** Phase 1B.4 – FR-02 Human Audit Batch 4 Decisions & Audit Completion
- **Transcript Reference:** `transcript_full.jsonl` (Prompt: Step 616, Output: Step 631)

---

## 1. Submitted Prompt

```text
/Speckit FR02-AI-031
Verdict: VALID
Reasoning: SEC-02 requires security-sensitive APIs to accept only a valid JWT. A token whose payload/signature has been tampered with is no longer valid, so a documented protected endpoint must reject it. This is acceptable as supporting/indirect FR-02 integration coverage because FR-02 is the token issuer and the protected endpoint is the token consumer.
Correction: NONE

FR02-AI-032
Verdict: INCOMPLETE
Reasoning: Validating the successful login response structure is appropriate and the documented contract supports the presence of a token and user information. However, the raw AI case over-specifies several details such as a strictly limited top-level structure, a positive integer ID, exact role enumeration, and a three-part encoded JWT unless all of those are explicitly normative in api_specification.md.
Correction: Retain schema validation for fields and types explicitly documented by API-SPEC. Remove or mark as PARTIAL any constraints that are inferred from examples or JWT conventions rather than explicitly specified.

FR02-AI-033
Verdict: INCOMPLETE
Reasoning: Validating the generic error response for invalid credentials is appropriate, but the specification does not necessarily mandate the exact error property name or require literal absence of both token and user fields. The important behavior is generic authentication failure with no usable authenticated session/token.
Correction: Keep the generic error-contract check. Do not require a particular error key or exact omission representation unless explicitly documented. Assert that authentication fails and no usable authentication token is issued.

FR02-AI-034
Verdict: INCOMPLETE
Reasoning: FR-02 supports a temporary-lockout notification and non-disclosure of sensitive authentication details. However, the raw case expands this into specific prohibitions on stack, SQL, lockout_until, attempts, and other internal fields that are not individually defined by the FR-02 contract.
Correction: Retain the temporary-lockout error response and generic non-disclosure assertion. Leave exact status and field name unspecified, and treat stack trace/database/internal-variable leakage checks as additional security/robustness assertions rather than the formal FR-02 oracle.

FR02-AI-035
Verdict: INCOMPLETE
Reasoning: Malformed JSON is a useful transport/parser robustness case, but malformed JSON handling is not explicitly defined by the FR-02 business specification. Therefore requiring a particular 4xx class response, forbidding 500, or requiring a structured JSON parser error is broader than the documented FR-02 oracle.
Correction: Retain this as an exploratory transport robustness test. Assert only that malformed input must not result in successful authentication or issuance of a usable JWT. Treat exact status, parser error schema, and no-500 behavior as engineering expectations unless separately documented.

FR02-AI-036
Verdict: INCOMPLETE
Reasoning: Checking Content-Type is useful API-contract validation, but the raw test marks application/json as an EXPLICIT requirement based largely on REST convention. Unless api_specification.md explicitly requires this response header, the assertion is inferred rather than a specification-backed FR-02 oracle.
Correction: Keep Content-Type validation only as a PARTIAL or exploratory API-contract check unless the exact JSON response Content-Type is explicitly documented. Do not classify it as EXPLICIT solely because the API uses JSON.

FR02-AI-037
Verdict: INCOMPLETE
Reasoning: Supplying unexpected fields such as role="admin" is a valuable parameter-injection and privilege-escalation probe. However, the login specification does not define whether unknown fields must be rejected or ignored. Therefore the HTTP 200-versus-400 behavior is SPEC-UNDEFINED. The useful security assertion is only that client-supplied login fields must not elevate the authenticated user's actual role.
Correction: Retain the test as an exploratory/additional-security parameter-injection case. Do not require either silent ignoring or HTTP 400. Assert only that the supplied role field cannot alter the authenticated account's real authorization role.
```

---

## 2. Exact AI Output

```markdown
# Phase 1B Complete – FR-02 Human Test-Case Audit Finalized

All 37 raw AI-generated test cases (`FR02-AI-001` .. `FR02-AI-037`) have undergone the mandatory **Student Human Test-Case Audit**. All verdicts, technical rationales, required corrections, and final dispositions have been recorded in [TC_AUDIT_FR02.md](file:///Volumes/Thang/HW06/HW06/23127259/ai/TC_AUDIT_FR02.md).

---

## 1. Human Audit Breakdown & Classification Summary

| Classification | Count | Percentage | Test Case IDs | Strategic Disposition |
|---|:---:|:---:|---|---|
| **`VALID`** | **16** | 43.2% | `FR02-AI-001..004`, `013..015`, `019..024`, `027`, `030..031` | Accepted as-is; direct specification-grounded test oracles. |
| **`INVALID`** | **2** | 5.4% | `FR02-AI-016` (dup of 013), `FR02-AI-017` (dup of 014) | Rejected as redundant duplicates; preserved in audit log for transparency. |
| **`INCOMPLETE`** | **19** | 51.4% | `FR02-AI-005..012`, `018`, `025..026`, `028..029`, `032..037` | Accepted with corrections: removed over-specified oracles, enforced HTTP status neutrality, separated transport sanitization from SEC-01 DB storage, and clarified SEC-05 black-box limitations. |
| **TOTAL** | **37** | 100.0% | `FR02-AI-001` .. `FR02-AI-037` | **100% Student-Audited** |

### Net Executable AI Inventory:
$$\text{Net Accepted AI Test Cases} = 16\text{ (VALID)} + 19\text{ (INCOMPLETE with corrections)} = \mathbf{35\text{ AI Cases}}$$
*(Meets the mandatory $\ge 35$ AI test cases threshold).*

---

## 2. Master Audit Log & Interaction Tracking

| INT ID | Scope / Stage | Date & Time (UTC+7) | Tool & Model | Status |
|:---:|---|:---:|---|:---:|
| **INT-010** | Phase 1A.6 (Part A): AI Prompt Log Verbatim Repair | 2026-09-01 19:26 | Antigravity (Gemini 3.7 Flash) | Verified & Logged |
| **INT-011** | Phase 1A.6 (Part B): Generation Coverage Review & Freeze | 2026-09-01 19:33 | Antigravity (Gemini 3.7 Flash) | Verified & Corrected |
| **INT-012** | Phase 1B.0: Human Audit Preparation & Batch 1 Setup | 2026-09-01 19:37 | Antigravity (Gemini 3.7 Flash) | Verified & Logged |
| **INT-013** | Phase 1B.1: Human Audit Batch 1 Decisions (`001..010`) | 2026-09-01 19:46 | Antigravity (Gemini 3.7 Flash) | Verified & Logged |
| **INT-014** | Phase 1B.2: Human Audit Batch 2 Decisions (`011..020`) | 2026-09-01 19:51 | Antigravity (Gemini 3.7 Flash) | Verified & Logged |
| **INT-015** | Phase 1B.3: Human Audit Batch 3 Decisions (`021..030`) | 2026-09-01 19:54 | Antigravity (Gemini 3.7 Flash) | Verified & Logged |
| **INT-016** | Phase 1B.4: Human Audit Batch 4 Decisions (`031..037`) | 2026-09-01 19:56 | Antigravity (Gemini 3.7 Flash) | Verified & Logged |

- **Consolidated Master Prompt Log:** [AI_PROMPT_LOG.md](file:///Volumes/Thang/HW06/HW06/23127259/ai/prompts/AI_PROMPT_LOG.md) (142,455 bytes, 16 interactions registered verbatim).
- **Master Audit Report:** [AI_AUDIT_REPORT.md](file:///Volumes/Thang/HW06/HW06/23127259/ai/AI_AUDIT_REPORT.md).

---

## 3. Raw Inventory Cryptographic Integrity
- **Raw AI Draft File:** [`23127259/testcases/FR02_AI_DRAFT.md`](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_AI_DRAFT.md)
- **Raw Generation SHA-256:**
  ```text
  b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c
  ```
  *(Confirmed 100% untouched and preserved for raw evidence).*

---

## 4. Git Commit & Push Verification
- **Audit Commit Message:** `test(23127259): audit AI-generated FR-02 test cases`
- **Commit SHA:** [`5deecd7`](https://github.com/thangak18/HW06/commit/5deecd7)
- **Branch:** `thang/hw06-implementation` (Pushed to `origin`, working tree clean).

---

Ready to proceed to **PHASE 1C – HUMAN-DESIGNED EXTENSION TEST CASES FOR FR-02 (`FR02-HUM-001` .. `FR02-HUM-005`)** to bring the total FR-02 test suite to $\ge 40$ test cases.
```

---

## 3. Human Evaluation & Outcome

- **Verdict:** VALID. All 37 AI-generated test cases completed student human audit (16 VALID, 2 INVALID, 19 INCOMPLETE). Committed and pushed under `test(23127259): audit AI-generated FR-02 test cases` (`5deecd7`).
- **Status:** EXACT OUTPUT AVAILABLE.
