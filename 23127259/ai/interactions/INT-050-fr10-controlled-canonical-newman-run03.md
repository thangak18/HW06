# Interaction Log: INT-050

- **Interaction ID:** INT-050
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-02 08:59:17+07:00
- **Timezone:** UTC+07:00
- **Project Stage:** Phase 2D.1D.4 – FR-10 Controlled Canonical Newman Run 03
- **Transcript Reference:** `transcript_full.jsonl` (Prompt: Step 2164, Output: Pending backfill)

---

## 1. Submitted Prompt

See `AI_PROMPT_LOG.md#int-050` for complete verbatim prompt (44 sections, Phase 2D.1D.4).

---

## 2. Exact AI Output

```markdown
# Phase 2D.1D.4 FR-10 Canonical Newman Run03 Report

## AI Audit
- INT-049 Output Backfilled: INT-049-fr10-ai028-tampered-jwt-failfast-hardening.md
- INT-050 Prompt Stored: INT-050-fr10-controlled-canonical-newman-run03.md & AI_PROMPT_LOG.md
- INT-050 Output: Pending backfill

## Artifact Integrity
- Collection SHA-256: 48b760d071a1b1080c2071ca56b26938763a30b9a35cd4c867a7fc5641467c89 (MATCH / PASS)
- Environment SHA-256: 6cde9f7cbaf49176d8f6a3236f38e7ea52017025951de5dfac3a786ab90904b1 (MATCH / PASS)
- Raw AI Draft SHA-256: 303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc (MATCH / PASS)

## Static Gates
- Canonical Map Self-Check: PASS (46/46)
- Canonical Traceability: PASS (46/46)
- Fixture Isolation: PASS (140 reqs, 0 shared vars)
- Actor Readiness: PASS
- Auth Harness: PASS
- Tampered JWT Harness: PASS (5/5 Gates)

## Newman
- Version: 6.2.2
- Pipefail Enabled: YES
- Actual Newman / Pipeline Exit Code: 1 (12 assertion failures across 6 normative defect cases)
- Host Under Test: http://localhost:3000

## Runtime Metrics
- Collection Request Definitions: 140
- Script-Triggered Requests (pm.sendRequest): 36
- Total Executed Requests: 176
- Total Assertions: 176 (Passed: 164, Failed: 12)
- Fatal Script Errors: 0
- Total Runtime: 2.21 seconds

## Formal Reconciliation
- PASS: 38
- FAIL – NORMATIVE ORACLE VIOLATION: 6 (AI-016, AI-024, AI-030, AI-031, AI-032, HUM-003)
- EXPLORATORY OBSERVATION: 2 (HUM-004, HUM-005)
- BLOCKED – HARNESS/SETUP: 0
- TOTAL: 46

## Canonical Repaired Cases
- FR10-AI-028: PASS (HTTP 403, 0 state mutation)
- FR10-AI-029: PASS (HTTP 401, 0 state mutation)
- FR10-AI-031: FAIL – NORMATIVE ORACLE VIOLATION (HTTP 200, RBAC bypass)
- FR10-AI-032: FAIL – NORMATIVE ORACLE VIOLATION (HTTP 200, RBAC bypass)

## Candidate Clusters
- CANDIDATE-FR10-FSM-01: Affected IDs AI-016, HUM-003 (Retain for confirmation)
- CANDIDATE-FR10-FSM-02: Affected IDs AI-024 (Retain for confirmation)
- CANDIDATE-SEC03-01: Affected IDs AI-030, AI-031, AI-032 (Retain for confirmation)
- CANDIDATE-SEC02-01: DROPPED

## Run03 Evidence Hashes
- CLI SHA-256: 313e5c275ee1776dfa543c3013dd5c8b6fee5d324a104cab457ddea40ea21175
- JSON SHA-256: 553445dd8adb86fbd2fe8cd6f8dbb1c5a21283c1944559e8c854461e815140f7
- HTML SHA-256: b73519b7bb3fba999879fea45fd37c5fd8434cb4522c7df3b959dd432dcd1c09

Run03 Verdict: TARGETED_CONFIRMATION_REQUIRED
Commit SHA: 9da6647
```

---

## 3. Human Evaluation & Outcome

- **Verdict:** COMPLETED. Executed controlled canonical Newman Run 03. All 46 formal cases executed with 100% harness trustworthiness and zero setup blockers. 3 candidate clusters retained for confirmation. Committed as `9da6647`.
- **Status:** COMPLETED & COMMITTED (`9da6647`). Authorized Phase 2D.1E Targeted Defect Confirmation.
