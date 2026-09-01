# AI Interaction Logs Directory

This directory stores individual verbatim interaction transcripts between the student and AI tools throughout the HW06 project lifecycle.

---

## 1. Naming Convention

Each interaction is recorded in a dedicated Markdown file following the standard:

`INT-<NNN>-<stage-descriptor>.md`

### Standard Prefix Sequence:
- **`INT-001-plan-initial.md`**: Initial project architecture & workspace planning
- **`INT-002-plan-review.md`**: Implementation plan review and methodology refinement
- **`INT-003-plan-revision.md`**: Implementation plan correction (SEC definitions & oracles)
- **`INT-004-plan-final.md`**: Final implementation plan freeze and accounting lock
- **`INT-005-fr02-stage1-domain.md`**: FR-02 Stage 1 (Domain & Input Partitioning)
- **`INT-006-fr02-stage2-bva.md`**: FR-02 Stage 2 (Boundary Value Analysis)
- **`INT-007-fr02-stage3-state.md`**: FR-02 Stage 3 (Lockout State Transitions)
- **`INT-008-fr02-stage4-security.md`**: FR-02 Stage 4 (Security & Data Exposure Probes)
- **`INT-009-fr02-stage5-schema.md`**: FR-02 Stage 5 (JSON Schema Validation Scripts)
- **`INT-010-fr02-stage6-negative.md`**: FR-02 Stage 6 (Negative & Malformed Payload Tests)
- *(Subsequent interactions continue sequentially for FR-10 and FR-14)*

---

## 2. Interaction Record Format

Each interaction file contains:
1. **Metadata:** Tool, Model, Timestamp (UTC+7), Purpose
2. **Exact Prompt:** Full verbatim prompt submitted
3. **Raw AI Output:** Complete unedited AI response
4. **Human Evaluation:** Initial review observations prior to test-case audit
