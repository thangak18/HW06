# AI Audit Report – HW06

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Course:** HW06 – API Testing
- **Audit Policy:** Comprehensive logging of all AI interactions (prompts, outputs, evaluation, and downstream corrections).

---

## 1. AI Usage Declaration

AI assistance in this assignment is utilized strictly within academic policy guidelines for:
- Test case ideation and equivalence partitioning / boundary value analysis
- State transition test scenario generation
- Security test scenario design (SEC-01, SEC-02, SEC-03, SEC-05)
- JSON schema assertion generation for Postman
- Edge case exploration and negative scenario identification

All AI-generated outputs are subjected to 100% human audit against the authoritative SRS specification prior to implementation.

---

## 2. Master AI Interaction Log

| Interaction ID | Tool & Model | Date & Time (UTC+7) | Project Stage | Purpose / Summary | Transcript Reference | Status |
|:---:|---|:---:|---|---|---|:---:|
| **INT-001** | Antigravity (Gemini 3.7 Flash) | 2026-08-30 22:00 | Phase 0 Setup | Initial multi-member repository planning & workspace design | `ai/interactions/INT-001-plan-initial.md` | Logged |
| **INT-002** | Antigravity (Opus Reasoning) | 2026-09-01 15:55 | Implementation Plan | Architectural test planning for FR-02, FR-10, FR-14 | `ai/interactions/INT-002-plan-review.md` | Logged |
| **INT-003** | Antigravity (Claude Sonnet 4.6) | 2026-09-01 16:15 | Plan Revision | Correcting SEC mappings and separating spec from source code | `ai/interactions/INT-003-plan-revision.md` | Logged |
| **INT-004** | Antigravity (Gemini 3.7 Flash) | 2026-09-01 18:25 | Plan Finalization | Final plan freeze, FR-10 matrix fix, and test accounting lock | `ai/interactions/INT-004-plan-final.md` | Logged |
| **INT-005** | *Planned for Phase 1A* | *Pending* | FR-02 Stage 1 | FR-02 Parameter scan & Domain partitioning | `ai/interactions/INT-005-fr02-stage1-domain.md` | Scheduled |
| **INT-006** | *Planned for Phase 1A* | *Pending* | FR-02 Stage 2 | FR-02 Boundary value analysis | `ai/interactions/INT-006-fr02-stage2-bva.md` | Scheduled |
| **INT-007** | *Planned for Phase 1A* | *Pending* | FR-02 Stage 3 | FR-02 Lockout state machine transition tests | `ai/interactions/INT-007-fr02-stage3-state.md` | Scheduled |
| **INT-008** | *Planned for Phase 1A* | *Pending* | FR-02 Stage 4 | FR-02 Security & data exposure probes | `ai/interactions/INT-008-fr02-stage4-security.md` | Scheduled |
| **INT-009** | *Planned for Phase 1A* | *Pending* | FR-02 Stage 5 | FR-02 JSON schema assertion scripts | `ai/interactions/INT-009-fr02-stage5-schema.md` | Scheduled |
| **INT-010** | *Planned for Phase 1A* | *Pending* | FR-02 Stage 6 | FR-02 Negative & malformed payload scenarios | `ai/interactions/INT-010-fr02-stage6-negative.md` | Scheduled |

---

## 3. Detailed Planning Interaction Records

### INT-001: Initial Repository Architecture Planning
- **Date & Time:** 2026-08-30 22:00:00+07:00
- **Tool:** Antigravity CLI / Assistant (Gemini 3.7 Flash)
- **Purpose:** Set up shared 3-member repository structure for HW06 with isolated workspaces.
- **Prompt Reference:** Stored in `ai/interactions/INT-001-plan-initial.md`
- **Output Reference:** Generated initial repository templates and workspace layout.

### INT-002: Implementation Plan Formulation
- **Date & Time:** 2026-09-01 15:55:00+07:00
- **Tool:** Antigravity (Opus Reasoning)
- **Purpose:** Formulate implementation plan for FR-02, FR-10, and FR-14.
- **Prompt Reference:** Stored in `ai/interactions/INT-002-plan-review.md`

### INT-003: Plan Revision (SEC Mappings & Methodology)
- **Date & Time:** 2026-09-01 16:15:00+07:00
- **Tool:** Antigravity (Claude Sonnet 4.6)
- **Purpose:** Re-map SEC-01..07 to official EShop SRS and ground test oracles in specifications.
- **Prompt Reference:** Stored in `ai/interactions/INT-003-plan-revision.md`

### INT-004: Final Plan Freeze & Pre-Implementation Gate
- **Date & Time:** 2026-09-01 18:25:00+07:00
- **Tool:** Antigravity (Gemini 3.7 Flash)
- **Purpose:** Final plan freeze, FR-10 matrix correction (`confirmed->canceled` User+Admin), test accounting lock ($\ge 120$ cases).
- **Prompt Reference:** Stored in `ai/interactions/INT-004-plan-final.md`
