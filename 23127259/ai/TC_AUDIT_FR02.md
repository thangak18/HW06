# Human Test-Case Audit Matrix – FR-02 (Login & Account Lockout)

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Feature:** FR-02 – Login and Account Lockout
- **Target Accounting:** $\ge 35\text{ AI-generated cases}$ (`FR02-AI-001..035`) $+ \ge 5\text{ Human-designed extension cases}$ (`FR02-HUM-001..005`) $= \ge 40\text{ Total Cases}$

---

## 1. Audit Standards & Verdict Definitions

Every AI-generated test case is evaluated against the authoritative EShop SRS FR-02 specification before implementation:

- **`VALID`:** Test case correctly implements SRS requirements, parameters, expected status codes, and assertions without modification.
- **`INVALID`:** Test case specifies an incorrect expected result, tests an unsupported endpoint, or violates business logic (e.g. assumes incorrect lockout counter arithmetic).
- **`INCOMPLETE`:** Test case is directionally sound but lacks necessary assertion specifics, payload details, or boundary conditions.

---

## 2. FR-02 Test-Case Audit Log

| Test Case ID | AI Interaction | Description | Verdict | Rationale | Correction |
|---|---|---|:---:|---|---|
| *FR02-AI-001* | *Pending Phase 1A* | *To be populated in Phase 1A* | *PENDING* | *Pending audit* | — |

*(Full matrix of $\ge 35\text{ AI cases}$ will be populated and classified during Phase 1A)*

---

## 3. Human-Designed Extension Cases Summary (`FR02-HUM-001..005`)

*(To be populated in Phase 1B with full rationale explaining AI blind spots addressed)*
