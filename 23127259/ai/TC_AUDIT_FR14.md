# Human Test-Case Audit Matrix – FR-14 (Category Management CRUD)

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Feature:** FR-14 – Category Management (CRUD)
- **Target Accounting:** $\ge 35\text{ AI-generated cases}$ (`FR14-AI-001..035`) $+ \ge 5\text{ Human-designed extension cases}$ (`FR14-HUM-001..005`) $= \ge 40\text{ Total Cases}$

---

## 1. Audit Standards & Verdict Definitions

Every AI-generated test case is evaluated against the authoritative EShop SRS FR-14 / FR-12 specifications and `api_specification.md` before implementation:

- **`VALID`:** Test case correctly implements CRUD endpoints, mandatory name requirements, admin role gates (SEC-03), or public read behavior without modification.
- **`INVALID`:** Test case invents requirements not in the SRS (e.g. asserts duplicate names are bugs without a uniqueness requirement) or uses wrong HTTP verbs.
- **`INCOMPLETE`:** Test case verifies response code but omits subsequent state verification (e.g. deleting without verifying removal via GET).

---

## 2. FR-14 Test-Case Audit Log

| Test Case ID | AI Interaction | Description | Verdict | Rationale | Correction |
|---|---|---|:---:|---|---|
| *FR14-AI-001* | *Pending Phase 3A* | *To be populated in Phase 3A* | *PENDING* | *Pending audit* | — |

*(Full matrix of $\ge 35\text{ AI cases}$ will be populated and classified during Phase 3A)*

---

## 3. Human-Designed Extension Cases Summary (`FR14-HUM-001..005`)

*(To be populated in Phase 3B with full rationale explaining AI blind spots addressed)*
