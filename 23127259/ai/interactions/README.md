# AI Interaction Logs Directory

This directory stores individual verbatim interaction transcripts between the student and AI tools throughout the HW06 project lifecycle.

---

## 1. Naming Convention

Each interaction is recorded in a dedicated Markdown file following the standard:

`INT-<NNN>-<stage-descriptor>.md`

### Current Interaction Index:
- **`INT-001-plan-initial.md`**: Initial project architecture & workspace planning
- **`INT-002-plan-review.md`**: Implementation plan formulation (FR-02, FR-10, FR-14)
- **`INT-003-plan-revision.md`**: Implementation plan correction (SEC definitions & oracles)
- **`INT-004-plan-final.md`**: Final implementation plan freeze and accounting lock
- **`INT-005-fr02-requirement-domain-analysis.md`**: Phase 1A.1: FR-02 Requirement & Domain Analysis
- **`INT-006-fr02-domain-boundary-generation.md`**: Phase 1A.2: FR-02 Domain Partition & Boundary Generation
- **`INT-007-fr02-lockout-state-generation.md`**: Phase 1A.3: FR-02 Lockout State-Transition Generation
- **`INT-008-fr02-security-generation.md`**: Phase 1A.4: FR-02 Security Test Generation
- **`INT-009-fr02-schema-error-generation.md`**: Phase 1A.5: FR-02 Schema & Error Contract Generation
- **`INT-010-ai-prompt-log-verbatim-repair.md`**: Phase 1A.6 (Part A): AI Prompt Log Verbatim Repair
- **`INT-011-fr02-generation-coverage-freeze.md`**: Phase 1A.6 (Part B): FR-02 Generation Coverage Freeze & Commit
- *(Subsequent interactions continue sequentially for Phase 1B, Phase 2, Phase 3)*

---

## 2. Interaction Record Format

Each interaction file contains:
1. **Metadata:** Tool, Model, Timestamp (UTC+7), Purpose
2. **Exact Prompt:** Full verbatim prompt submitted
3. **Raw AI Output:** Complete unedited AI response
4. **Human Evaluation:** Initial review observations prior to test-case audit
