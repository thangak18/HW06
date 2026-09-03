# FR-10 Confirmed Defect Registry

- **Feature Area:** FR-10 Order State Machine & Lifecycle Transitions
- **Student ID:** `23127259`
- **Execution Date:** 2026-09-02
- **Evidence Baseline:** Phase 2D.1F Strict Confirmation & Genuine Postman Evidence

---

## 1. Confirmed Defect Registry Table

| Bug ID | Title | Root Cause Cluster | Formal Test Cases | Severity | Confirmed | GitHub Issue | Screenshot |
|---|---|---|---|:---:|:---:|---|---|
| **`BUG-FR10-001`** | Owner can cancel an order after it enters shipping state | `CANDIDATE-FR10-FSM-01` | `FR10-AI-016`, `FR10-HUM-003` | **HIGH** | **YES** | [#29](https://github.com/thangak18/HW06/issues/29) | [`BUG-FR10-001-postman-runner.png`](../evidence/fr10/bugs/BUG-FR10-001-postman-runner.png) |
| **`BUG-FR10-002`** | Canceled terminal order can be transitioned to delivered | `CANDIDATE-FR10-FSM-02` | `FR10-AI-024` | **HIGH** | **YES** | [#30](https://github.com/thangak18/HW06/issues/30) | [`BUG-FR10-002-postman-runner.png`](../evidence/fr10/bugs/BUG-FR10-002-postman-runner.png) |
| **`BUG-FR10-003`** | Regular customer can mutate order status through Admin API | `CANDIDATE-SEC03-01` | `FR10-AI-030`, `FR10-AI-031`, `FR10-AI-032` | **CRITICAL** | **YES** | [#31](https://github.com/thangak18/HW06/issues/31) | [`BUG-FR10-003-postman-runner.png`](../evidence/fr10/bugs/BUG-FR10-003-postman-runner.png) |

---

## 2. Dropped Candidates & Non-Bugs

| Candidate ID | Description | Resolution | Justification |
|---|---|:---:|---|
| **`CANDIDATE-SEC02-01`** | 403 Forbidden returned instead of 401 Unauthorized | **DROPPED** | Level 1 SEC-02 specifies authentication rejection; exact 401 status code is not mandated. SUT returning HTTP 403 with zero state mutation is a compliant safe rejection. |
| **`FR10-HUM-005`** | HTTP 500 observed on `text/plain` media type | **EXPLORATORY OBSERVATION** | Order state was preserved in `pending`; no API-visible lifecycle corruption. Not classified as a normative FR-10 defect without explicit specification backing. |
