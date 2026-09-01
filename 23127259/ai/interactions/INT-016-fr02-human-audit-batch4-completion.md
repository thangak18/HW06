# Interaction Log: INT-016

- **Interaction ID:** INT-016
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-01 19:56:42+07:00
- **Project Stage:** Phase 1B.4 – FR-02 Human Audit Batch 4 Decisions & Audit Completion
- **Transcript Reference:** `transcript_full.jsonl` (Prompt: Step 616, Output: Pending backfill)

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
PENDING TRANSCRIPT BACKFILL AFTER INTERACTION COMPLETES
```

---

## 3. Human Evaluation & Outcome

- **Verdict:** In progress. Recorded Batch 4 decisions (1 VALID, 6 INCOMPLETE) in `TC_AUDIT_FR02.md`. All 37 AI test cases completed student human audit (16 VALID, 2 INVALID, 19 INCOMPLETE).
- **Status:** EXACT PROMPT STORED; OUTPUT PENDING BACKFILL.
