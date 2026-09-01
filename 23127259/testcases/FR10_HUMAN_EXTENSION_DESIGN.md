# FR-10 Human Extension Test Design & Traceability Specification

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Provenance Model:** Student-selected and finalized Human Extension cases after AI-assisted coverage-gap analysis.
- **Selected Gap Directions:** `G-04`, `G-05`, `G-07`, `G-01`, `G-08`
- **Total Human Extension Cases:** `5` (`FR10-HUM-001` .. `FR10-HUM-005`)
- **Total Planned Formal Executable Suite:** `46` (41 Usable AI-Derived Cases + 5 Human Extension Cases)

---

## 1. Provenance & Methodological Framework

In accordance with HW06 integrity and spec-driven guidelines:
1. **AI-Assisted Gap Analysis:** An exhaustive gap analysis against the 41 usable AI-derived test cases identified 8 testing blindspots in `FR10_HUMAN_EXTENSION_GAP_ANALYSIS.md`.
2. **Student Selection:** The student reviewed the gap recommendations and explicitly selected 5 high-value directions (`G-04`, `G-05`, `G-07`, `G-01`, `G-08`) while intentionally excluding redundant or adjacent-feature directions (`G-02`, `G-03`).
3. **Formalization:** The 5 selected directions are formalized into executable, deterministic test specifications (`FR10-HUM-001` .. `FR10-HUM-005`) adhering strictly to the 24-field formal test case standard.
4. **Anti-Cheat Traceability:** Every test execution in Postman/Newman carries the collection-level runtime header `X-Student-Id: 23127259`.

---

## 2. Human Extension Traceability Matrix

| Human Test ID | Source Gap | Oracle Classification | Closest AI Baseline | Distinct Added Value & Technical Rationale |
|:---:|:---:|---|---|---|
| **`FR10-HUM-001`** | `G-04` | `SPECIFICATION-BACKED / STATE-MACHINE CONTINUITY` | `FR10-AI-009` (Isolated rejection) | **State-Machine Recovery Sequence:** Proves that after an illegal skip attempt (`pending` $\rightarrow$ `shipping`) is rejected, the state remains `pending` and a subsequent legitimate transition (`pending` $\rightarrow$ `confirmed`) succeeds cleanly without state-machine locking or corruption. |
| **`FR10-HUM-002`** | `G-05` | `SPECIFICATION-BACKED / ENTITY-STATE ISOLATION` | `FR10-AI-001` (Single order) | **Multi-Entity Isolation:** Establishes two independent orders in `pending`. Mutates Order A to `confirmed`. Explicitly queries both orders to prove Order A is `confirmed` and Order B remains strictly `pending`, preventing bulk mutation or missing `WHERE` clause flaws. |
| **`FR10-HUM-003`** | `G-07` | `SPECIFICATION-BACKED / LIFECYCLE CONTINUITY` | `FR10-AI-016` (Isolated cancel rejection) | **Downstream Fulfillment Recovery:** Transitions an order to `shipping`. Verifies that an owner customer's prohibited cancellation attempt is rejected, and subsequently proves that the Admin can successfully fulfill the order to terminal `delivered`. |
| **`FR10-HUM-004`** | `G-01` | `EXPLORATORY / API CONTRACT` | None (AI tested distinct-state edges only) | **Same-State Self-Loop Probe:** Admin submits `confirmed` $\rightarrow$ `confirmed`. Probes whether redundant status updates are handled idempotently or rejected without corrupting state. (Spec-undefined; observational oracle only). |
| **`FR10-HUM-005`** | `G-08` | `EXPLORATORY / API CONTRACT` | `FR10-AI-036`..`038` (JSON only) | **Non-JSON Content-Type Robustness:** Admin sends JSON-formatted body with `Content-Type: text/plain`. Probes whether the server handles unexpected media types gracefully without unhandled HTTP 500 crashes. (Observational oracle). |

---

## 3. Exploratory & Non-Normative Oracle Discipline

- **`FR10-HUM-004` (Same-State Self-Loop):** The authoritative specification does not define whether same-state mutations must return HTTP 200 (idempotent no-op) or HTTP 400 (redundant transition error). Both are valid implementations. The test asserts *only* that the order remains in `confirmed` state and is not corrupted. A difference in status code is NOT a normative bug.
- **`FR10-HUM-005` (Non-JSON Media Type):** Probes content-negotiation robustness. If the server returns HTTP 500, it is recorded as an exploratory robustness observation, not an automatic specification bug, unless a documented contract is violated.

---

## 4. Complete Test Suite Accounting

```
+-----------------------------------------------------------------------+
| FR-10 COMPLETE TEST SUITE RECONCILIATION                              |
+-----------------------------------------------------------------------+
| Raw AI-Generated Test Cases (Frozen Draft)               :  42         |
|   - Human-Audited Valid As-Is                            :  38         |
|   - Human-Audited Incomplete (Corrected Derivatives)      :   3         |
|   - Human-Audited Invalid (Rejected from Suite)          :   1 (AI-012)|
| Usable AI-Derived Executable Cases                       :  41         |
+-----------------------------------------------------------------------+
| Student-Selected Human Extension Test Cases (Phase 2C)   :   5         |
+-----------------------------------------------------------------------+
| TOTAL PLANNED FORMAL EXECUTABLE SUITE                    :  46         |
| Assignment Threshold Check (>= 35 AI + >= 5 Human)       : SATISFIED   |
+-----------------------------------------------------------------------+
```
