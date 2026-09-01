# AI Interaction Audit Report

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`
- **Audit Policy:** All prompts and AI interactions are recorded verbatim in accordance with the HW06 AI Testing & Audit specifications.

---

## 1. Audit Policy & Integrity Principles

1. **Independent Verification:** AI is utilized as a generation and acceleration tool. All generated test artifacts are subject to human evaluation, schema validation, and execution verification.
2. **Specification-First Oracles:** Expected test outcomes are strictly grounded in authoritative specification documents (EShop SRS, `api_specification.md`, and assignment guidance), never inferred from SUT implementation flaws.
3. **Traceability:** Every AI interaction is cataloged with exact prompts, tool/model metadata, generation date/time, and transcript references.
4. **Verbatim Prompt Registry:** A consolidated prompt log is maintained in [`ai/prompts/AI_PROMPT_LOG.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/prompts/AI_PROMPT_LOG.md).

---

## 2. Master AI Interaction Log

| INT ID | Date/Time (UTC+7) | Tool | Model | Stage / Scope | Exact Prompt | Exact Output | Transcript Source | Status |
|:---:|:---:|---|---|---|:---:|:---:|---|:---:|
| **INT-001** | 2026-08-30 22:00 | Antigravity Assistant | Gemini 3.7 Flash | Phase 0 Setup & Repo Architecture | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 0/27) | Logged |
| **INT-002** | 2026-09-01 15:55 | Antigravity Assistant | Opus Reasoning | Implementation Plan Formulation | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 193/229) | Logged |
| **INT-003** | 2026-09-01 16:15 | Antigravity Assistant | Claude Sonnet 4.6 | Plan Revision (SEC Mappings & Spec Oracles) | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 230/241) | Logged |
| **INT-004** | 2026-09-01 18:25 | Antigravity Assistant | Gemini 3.7 Flash | Plan Finalization & Pre-Implementation Gate | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 242/249) | Logged |
| **INT-005** | 2026-09-01 18:48 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.1: FR-02 Requirement & Domain Analysis | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 363/393) | Logged |
| **INT-006** | 2026-09-01 18:53 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.2: FR-02 Domain & Boundary Test Generation | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 394/411) | Logged |
| **INT-007** | 2026-09-01 18:56 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.3: FR-02 Lockout State-Transition Generation | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 412/423) | Logged |
| **INT-008** | 2026-09-01 18:59 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.4: FR-02 Security Test Generation | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 424/437) | Logged |
| **INT-009** | 2026-09-01 19:02 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.5: FR-02 Schema & Error Contract Generation | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 438/451) | Logged |
| **INT-010** | 2026-09-01 19:26 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.6 (Part A): AI Prompt Log Verbatim Repair | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 452/480) | Logged |
| **INT-011** | 2026-09-01 19:33 | Antigravity Assistant | Gemini 3.7 Flash | Phase 1A.6 (Part B): FR-02 Generation Coverage Freeze | YES (Verbatim) | EXACT OUTPUT AVAILABLE | `transcript_full.jsonl` (Step 481) | Logged |

---

## 3. Detailed Planning & Generation Interaction Records

### INT-001: Initial Repository Architecture Planning
- **Date & Time:** 2026-08-30 22:00:00+07:00
- **Tool / Model:** Antigravity IDE Assistant / Gemini 3.7 Flash
- **Purpose:** Set up shared 3-member repository structure for HW06 with isolated student workspaces.
- **Transcript Reference:** `transcript_full.jsonl` (Step 0)
- **Prompt Log Reference:** [`ai/prompts/AI_PROMPT_LOG.md#int-001`](file:///Volumes/Thang/HW06/HW06/23127259/ai/prompts/AI_PROMPT_LOG.md)
- **Detailed Interaction File:** [`ai/interactions/INT-001-plan-initial.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-001-plan-initial.md)

### INT-002: Implementation Plan Formulation
- **Date & Time:** 2026-09-01 15:55:00+07:00
- **Tool / Model:** Antigravity IDE Assistant / Opus Reasoning
- **Purpose:** Formulate implementation plan for selected individual scope: FR-02, FR-10, and FR-14.
- **Transcript Reference:** `transcript_full.jsonl` (Step 193)
- **Detailed Interaction File:** [`ai/interactions/INT-002-plan-review.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-002-plan-review.md)

### INT-003: Plan Revision (SEC Mappings & Methodology)
- **Date & Time:** 2026-09-01 16:15:00+07:00
- **Tool / Model:** Antigravity IDE Assistant / Claude Sonnet 4.6
- **Purpose:** Re-map SEC-01..07 strictly to official EShop SRS Section 9 and ground test oracles in specifications.
- **Transcript Reference:** `transcript_full.jsonl` (Step 230)
- **Detailed Interaction File:** [`ai/interactions/INT-003-plan-revision.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-003-plan-revision.md)

### INT-004: Final Plan Freeze & Pre-Implementation Gate
- **Date & Time:** 2026-09-01 18:25:00+07:00
- **Tool / Model:** Antigravity IDE Assistant / Gemini 3.7 Flash
- **Purpose:** Final plan freeze, FR-10 matrix correction (`confirmed->canceled` User+Admin), test accounting lock ($\ge 120$ cases total).
- **Transcript Reference:** `transcript_full.jsonl` (Step 242)
- **Detailed Interaction File:** [`ai/interactions/INT-004-plan-final.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-004-plan-final.md)

### INT-005: FR-02 Requirement, Parameter, and Domain Analysis
- **Date & Time:** 2026-09-01 18:48:12+07:00
- **Tool / Model:** Antigravity IDE Assistant / Gemini 3.7 Flash
- **Purpose:** Requirement extraction, parameter inventory, equivalence partitions, BVA, state model, and schema analysis for FR-02 (`POST /api/login`).
- **Transcript Reference:** `transcript_full.jsonl` (Step 363)
- **Output Document:** [`docs/FR02_REQUIREMENT_ANALYSIS.md`](file:///Volumes/Thang/HW06/HW06/23127259/docs/FR02_REQUIREMENT_ANALYSIS.md)
- **Detailed Interaction File:** [`ai/interactions/INT-005-fr02-requirement-domain-analysis.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-005-fr02-requirement-domain-analysis.md)

### INT-006: FR-02 Domain Partition and Boundary Test Case Generation
- **Date & Time:** 2026-09-01 18:53:51+07:00
- **Tool / Model:** Antigravity IDE Assistant / Gemini 3.7 Flash
- **Purpose:** Patched requirement analysis (SEC-02 indirect dependency, parameter partition decoupling, 3rd failure response code neutrality) and generated initial 14 domain/boundary test cases (`FR02-AI-001..014`).
- **Transcript Reference:** `transcript_full.jsonl` (Step 394)
- **Output Document:** [`testcases/FR02_AI_DRAFT.md`](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_AI_DRAFT.md) (Stage 1A.2)
- **Detailed Interaction File:** [`ai/interactions/INT-006-fr02-domain-boundary-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-006-fr02-domain-boundary-generation.md)

### INT-007: FR-02 Lockout State-Transition Test Generation
- **Date & Time:** 2026-09-01 18:56:52+07:00
- **Tool / Model:** Antigravity IDE Assistant / Gemini 3.7 Flash
- **Purpose:** Generated 10 state-transition and lockout lifecycle test cases (`FR02-AI-015..024`) covering failure progression (N=1,2,3), request while locked, duration boundaries (T=25s, 32s), and consecutive-reset rules.
- **Transcript Reference:** `transcript_full.jsonl` (Step 412)
- **Output Document:** [`testcases/FR02_AI_DRAFT.md`](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_AI_DRAFT.md) (Stage 1A.3)
- **Detailed Interaction File:** [`ai/interactions/INT-007-fr02-lockout-state-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-007-fr02-lockout-state-generation.md)

### INT-008: FR-02 Security Test Generation
- **Date & Time:** 2026-09-01 18:59:26+07:00
- **Tool / Model:** Antigravity IDE Assistant / Gemini 3.7 Flash
- **Purpose:** Generated 7 security-focused test cases (`FR02-AI-025..031`) covering SQLi probes (SEC-05), anti-enumeration generic error equality, sensitive data exclusion, token omission on failure, and SEC-02 downstream token usability probes.
- **Transcript Reference:** `transcript_full.jsonl` (Step 424)
- **Output Document:** [`testcases/FR02_AI_DRAFT.md`](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_AI_DRAFT.md) (Stage 1A.4)
- **Detailed Interaction File:** [`ai/interactions/INT-008-fr02-security-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-008-fr02-security-generation.md)

### INT-009: FR-02 Schema and Error Contract Test Generation
- **Date & Time:** 2026-09-01 19:02:22+07:00
- **Tool / Model:** Antigravity IDE Assistant / Gemini 3.7 Flash
- **Purpose:** Generated 6 response schema and API error contract test cases (`FR02-AI-032..037`) covering success schema, generic error contract, lockout error contract & non-disclosure, malformed JSON parser contract, Content-Type headers, and extraneous property handling.
- **Transcript Reference:** `transcript_full.jsonl` (Step 438)
- **Output Document:** [`testcases/FR02_AI_DRAFT.md`](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_AI_DRAFT.md) (Stage 1A.5)
- **Detailed Interaction File:** [`ai/interactions/INT-009-fr02-schema-error-generation.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-009-fr02-schema-error-generation.md)

### INT-010: AI Prompt Log Verbatim Repair
- **Date & Time:** 2026-09-01 19:26:56+07:00
- **Tool / Model:** Antigravity IDE Assistant / Gemini 3.7 Flash
- **Purpose:** Restored all summarized prompt blocks across INT-001 through INT-009 with complete, unabbreviated verbatim text extracted directly from `transcript_full.jsonl`.
- **Transcript Reference:** `transcript_full.jsonl` (Step 452)
- **Output Document:** [`ai/prompts/AI_PROMPT_LOG.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/prompts/AI_PROMPT_LOG.md)
- **Detailed Interaction File:** [`ai/interactions/INT-010-ai-prompt-log-verbatim-repair.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-010-ai-prompt-log-verbatim-repair.md)

### INT-011: FR-02 AI Generation Coverage Review, Freeze, and Commit
- **Date & Time:** 2026-09-01 19:33:18+07:00
- **Tool / Model:** Antigravity IDE Assistant / Gemini 3.7 Flash
- **Purpose:** Conducted comprehensive 36-dimension requirement coverage review, established audit questions, generated manifest with SHA-256 hash (`b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c`), and froze raw AI-generated test inventory (`FR02-AI-001..037`).
- **Transcript Reference:** `transcript_full.jsonl` (Step 481)
- **Output Documents:** [`testcases/FR02_AI_GENERATION_REVIEW.md`](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_AI_GENERATION_REVIEW.md), [`testcases/FR02_AI_GENERATION_MANIFEST.md`](file:///Volumes/Thang/HW06/HW06/23127259/testcases/FR02_AI_GENERATION_MANIFEST.md)
- **Detailed Interaction File:** [`ai/interactions/INT-011-fr02-generation-coverage-freeze.md`](file:///Volumes/Thang/HW06/HW06/23127259/ai/interactions/INT-011-fr02-generation-coverage-freeze.md)
