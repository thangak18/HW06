# Test Oracle and Verification Policy

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Course:** HW06 – API Testing

---

## 1. Primary Test Oracle Hierarchy

In accordance with rigorous black-box testing methodology and the HW06 academic requirements, all expected results for formal test cases are derived strictly from authoritative specification documents in the following order of precedence:

1. **HW06 Assignment Specification (PDF):** Defines grading criteria, required accounting ($\ge 35\text{ AI} + \ge 5\text{ Human}$), security mapping guidelines, and deliverables.
2. **EShop System Requirements Specification (SRS / README):** Defines authoritative business rules, state transition constraints, input validation rules, and the official security requirements (**SEC-01** through **SEC-07**).
3. **API Specification (`api_specification.md`):** Defines endpoint paths, HTTP verbs, request payload contracts, expected response status codes, and baseline JSON schemas.

---

## 2. Strict Separation of Specification and Implementation

> [!IMPORTANT]
> **Implementation source code (`server.js`, `database.js`) is NOT a test oracle.**

- Expected outcomes in all test cases must reflect the **correct, expected business logic** specified in the SRS.
- Expected results must never be altered to match buggy or non-compliant implementation behavior simply to produce passing tests.
- When an API test execution produces an outcome that diverges from the SRS-derived expected result, the divergence is flagged as a defect candidate.

---

## 3. Defect Classification & Root-Cause Analysis Protocol

1. **Phase A (Specification-First Design):** Design test cases and define expected results based strictly on the SRS and API spec.
2. **Phase B (Execution & Evidence Capture):** Execute tests via Postman / Newman against the live SUT. Capture verbatim response codes, response bodies, and logs.
3. **Phase C (Discrepancy Verification):** Compare actual responses with expected results. If a discrepancy exists, reproduce it consistently.
4. **Phase D (Root-Cause Explanation):** Only after a discrepancy is reproduced at runtime may the source code (`server.js`) be inspected to provide root-cause analysis in the bug report.
5. **Candidate Observations:** Preliminary observations identified during source inspection are strictly labelled **`UNCONFIRMED`** until verified through real execution.
