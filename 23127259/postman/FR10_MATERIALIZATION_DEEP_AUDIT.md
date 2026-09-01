# FR-10 Materialization Deep Static Audit & Hardening Report

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Status:** **STATIC AUDIT & HARNESS HARDENING COMPLETE**

---

## 1. Audit Scope & Objectives

Prior to any runtime execution in Postman or Newman, a comprehensive static inspection of the FR-10 test collection and supporting artifacts was conducted to verify:
1. Exact mapping between the 46 formal test cases, 63 collection request definitions, and 36 script-triggered persistence verification queries (99 total runtime operations).
2. Fail-fast enforcement of the collection-level `X-Student-Id` pre-request script.
3. Strict inclusion of `X-Student-Id` and authorized `Authorization: Bearer {{token}}` headers inside **every** `pm.sendRequest` script call.
4. Elimination of false "expired token" claims in SEC-02 documentation.
5. Verification of non-normative oracles for exploratory cases (`FR10-HUM-004`, `FR10-HUM-005`) and corrected cases (`FR10-AI-033`, `034`, `040`).

---

## 2. Identified Discrepancies & Hardening Actions

| Audit Dimension | Issue Identified Before Audit | Hardening Action Applied | Formal Accounting Impact | Oracle Impact |
|---|---|---|:---:|:---:|
| **Multi-Step Workflows** | Multi-step formal cases (`AI-004`, `AI-041`, `HUM-001`, `HUM-002`, `HUM-003`) had single request placeholders. | Expanded into 19 explicit standalone collection items tagged under parent formal IDs. | Unchanged (`46` formal cases) | Unchanged |
| **`X-Student-Id` Script Calls** | `pm.sendRequest` calls in test scripts bypass collection pre-request scripts. | Explicitly injected `X-Student-Id: pm.environment.get('studentId')` into every script-level request payload. | Unchanged | Unchanged |
| **`X-Student-Id` Fallback** | Fallback `|| "23127259"` masked missing environment variable selection. | Converted to fail-fast check throwing explicit Error if `studentId` is not defined. | Unchanged | Unchanged |
| **SEC-02 Documentation** | Folder 05 was loosely described as testing "expired tokens" when AI cases test invalid/random/tampered tokens. | Corrected folder descriptions in all docs to accurately state `SEC-02` invalid token / untrusted signature tests. | Unchanged | Unchanged |
| **Persistence Oracles** | 36 state mutation / rejection cases lacked observable post-mutation reads. | Embedded authorized `pm.sendRequest` GET queries verifying persisted database state matches expectations. | Unchanged | Unchanged |

---

## 3. Invariant Verification Confirmation
- **Raw AI Draft Frozen Hash:** Strictly verified (`303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc`).
- **Rejected Case Exclusion:** `FR10-AI-012` is completely absent from all collection items and scripts.
- **Human Cases Count:** Exactly 5 continuous Human Extension cases (`FR10-HUM-001` .. `FR10-HUM-005`).
- **Hardcoded Live Secrets:** Zero hardcoded live JWTs found across all JSON files.
