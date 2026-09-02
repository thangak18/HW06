# AI Test-Generator Diagram – Content Specification

> **Authoring rule.** This diagram must be **self-drawn / hand-coded**, not
> AI-generated. The Senior QA agent prepared the content specification only;
> the visual rendering is delegated to Codex.
>
> **Visual file (final):** `23127259/docs/AI_TEST_GENERATOR_DIAGRAM.png`
> (or `.svg`, `.pdf`).
>
> **Visual status:** PENDING_CODEX_VISUAL_TASK.

## Diagram Type

Static flow / pipeline diagram, top-down or left-to-right.

## Required Nodes (in order)

1. **Requirements** (`SRS`, `API Specification`, `Security Mapping`)
2. **AI Generation** (per-feature prompt, raw draft file e.g. `FR14_AI_DRAFT.md`)
3. **Raw AI Inventory** (raw case count: 37 / 42 / 42)
4. **Human Audit** (`TC_AUDIT_FR*.md`)
   - VALID / INVALID / INCOMPLETE classification
5. **Gap Analysis** (`*_GAP_ANALYSIS.md`)
6. **Human Extensions** (`*_HUMAN_TEST_CASES.md`, 5 / 5 / 4 cases)
7. **Canonical Suite** (`fr*_canonical_cases.json`, formal count: 40 / 46 / 46)
8. **Postman Collection** (`FR*_*.postman_collection.json`)
9. **X-Student-Id Injection** (pre-request script + `studentId` env var)
10. **Newman Execution** (CLI / JSON / HTML / exit-code artifact)
11. **Formal Reconciliation** (`*_FORMAL_RECONCILIATION.md`)
12. **Targeted Bug Confirmation** (isolated fixtures, GET verification)
13. **Bug Reports** (`BUG-FR*-*.md`, GitHub Issues)
14. **CI/CD** (`.github/workflows/hw06-23127259-api-tests.yml`)

## Required Edges

- Requirements → AI Generation
- AI Generation → Raw AI Inventory
- Raw AI Inventory → Human Audit
- Human Audit → Gap Analysis
- Gap Analysis → Human Extensions
- Human Extensions → Canonical Suite
- Human Audit → Canonical Suite (VALID only)
- Canonical Suite → Postman Collection
- Postman Collection → X-Student-Id Injection (cross-cutting)
- Postman Collection → Newman Execution
- Newman Execution → Formal Reconciliation
- Formal Reconciliation → Targeted Bug Confirmation
- Targeted Bug Confirmation → Bug Reports
- Bug Reports → CI/CD (feedback loop for red sample)

## Required Labels / Captions

- Title: "AI-Driven API Test Generation Pipeline"
- Subtitle: "FR02 / FR10 / FR14"
- Footer: "Self-authored architecture, Senior QA 2026"
- Each node should carry a short label (≤ 8 words)
- Each edge should carry an action verb (e.g., "audits", "extends",
  "executes", "reconciles")

## Color/Style Guidance (for Codex)

- Use a calm color palette (blue / green / amber for normative / partial /
  exploratory oracles).
- Bold the canonical-suite and Newman-execution nodes.
- Use directional arrows for edges.
- Add a small legend distinguishing **LEVEL-1 (normative)** vs
  **PARTIAL-ORACLE** vs **EXPLORATORY** nodes.

## Required Authoring Declaration

The final image must include a small text annotation such as:

```
Authored by Nguyễn Tấn Thắng (23127259). Not AI-generated.
```

This declaration is mandatory per assignment policy.