# FR-10 Materialization Deep Static Audit & Hardening Report

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Status:** **PER-CASE FIXTURE ISOLATION COMPLETE**

---

## 1. Audit Scope & Hardening History

- **Phase 2D.0.1:** Hardened fail-fast `X-Student-Id` injection, script-level `pm.sendRequest` headers, removed false expired-token claims.
- **Phase 2D.0.2:** Verified authoritative route mappings, documented variable dataflow.
- **Phase 2D.0.3:** Resolved shared mutable fixture defect by implementing strict **Per-Case Fixture Isolation**, co-located setup helpers, and fail-fast ID extraction without fallbacks.

---

## 2. Fixture Isolation Hardening Summary

| Dimension | Before Hardening | After Hardening | Isolation Impact |
|---|---|---|:---:|
| **Fixture Scoping** | 7 shared fixture families across folders | 44 dedicated per-case order fixtures | **100% Isolated** |
| **Shared Mutable Variables** | Shared `orderPendingId`, `orderConfirmedId`, `orderShippingId`, `orderId` | `0` shared mutable order variables | **0 Collisions** |
| **ID Extraction** | Fallback `|| '1'` | Fail-fast error throwing if ID missing | **Zero Silent Substitution** |
| **Precondition Transitions** | Prerequisite states set once globally | Co-located setup transitions per case | **Defect-Resistant** |
