# AI Capability & Limitation Critique – API Testing

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Course:** HW06 – API Testing
- **Required Length:** 200–300 words
- **Evidence Foundation:** Grounded in audit data from `ai/TC_AUDIT_FR02.md`, `ai/TC_AUDIT_FR10.md`, and `ai/TC_AUDIT_FR14.md`.

---

## Critical Assessment

The HW06 pipeline demonstrates that AI accelerates API test generation substantially but cannot serve as the final oracle. Across three features, 121 raw AI-generated test cases were produced efficiently, covering broad SRS surface area including happy paths, boundary conditions, and RBAC permutations. This generation phase would have taken a human tester significantly longer to author manually.

However, human audit classified every AI case, revealing that raw output cannot be accepted blindly. FR-10 required correcting AI-generated assertions that assumed incorrect HTTP status codes based on implicit implementation guesses rather than strict SRS state-transition rules. FR-02 required eliminating security tests that conflated UI-level cookie disclosure (SEC-04) with API-level token leakage (SEC-01). Most critically, FR-14's 42 raw AI cases produced only 3 VALID verdicts; 2 were INVALID (conflicting oracle references) and 37 were INCOMPLETE (missing mandatory headers, incorrect HTTP methods, or body-parameter misalignments). After human correction, 40 usable AI cases plus 6 human-designed extensions produced a formal suite of 46 cases.

Human gap analysis added cases the AI generation systematically missed: state-reset logic at failure-count boundaries (FR02-HUM-003), terminal-state immutability (FR10-HUM-002), and mass-assignment vulnerabilities (FR10-HUM-005). AI also failed to consolidate duplicate bug manifestations — FR-14's Issue #37 was independently filed as BUG-FR14-005 but merged into Issue #34 after human root-cause analysis revealed identical backend causes.

These findings confirm that AI is valuable for speed and breadth, but human judgment remains essential for oracle accuracy, completeness, and defect deduplication.
