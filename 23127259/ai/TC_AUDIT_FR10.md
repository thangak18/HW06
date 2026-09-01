# Human Test-Case Audit Matrix – FR-10 (Order State Machine)

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Feature:** FR-10 – Order State Machine
- **Target Accounting:** $\ge 35\text{ AI-generated cases}$ (`FR10-AI-001..035`) $+ \ge 5\text{ Human-designed extension cases}$ (`FR10-HUM-001..005`) $= \ge 40\text{ Total Cases}$

---

## 1. Audit Standards & Verdict Definitions

Every AI-generated test case is evaluated against the authoritative EShop SRS FR-10 state machine specification before implementation:

- **`VALID`:** Test case correctly implements SRS state transition rules, roles, expected status codes, and assertions without modification.
- **`INVALID`:** Test case specifies an incorrect transition rule, treats valid terminal states as non-terminal, or misattributes user/admin cancellation permissions.
- **`INCOMPLETE`:** Test case lacks initial order setup steps, misses intermediate status checks, or lacks response schema assertions.

---

## 2. FR-10 Test-Case Audit Log

| Test Case ID | AI Interaction | Description | Verdict | Rationale | Correction |
|---|---|---|:---:|---|---|
| *FR10-AI-001* | *Pending Phase 2A* | *To be populated in Phase 2A* | *PENDING* | *Pending audit* | — |

*(Full matrix of $\ge 35\text{ AI cases}$ will be populated and classified during Phase 2A)*

---

## 3. Human-Designed Extension Cases Summary (`FR10-HUM-001..005`)

*(To be populated in Phase 2B with full rationale explaining AI blind spots addressed)*
