# FR-02 AI Generation Manifest

- **Feature Name:** FR-02 – Login and Account Lockout
- **Pool Allocation:** Pool A
- **Target Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

---

## 1. Inventory Metadata

- **Raw AI-Generated Test Count:** 37 test cases
- **Test Case ID Range:** `FR02-AI-001` .. `FR02-AI-037`
- **Target File:** [`testcases/FR02_AI_DRAFT.md`](FR02_AI_DRAFT.md)
- **Raw Generation SHA-256:** `b5ab203bac9e560190649f50b7d7b5c258810915e7ae84ec02f87e371573317c`

---

## 2. Traceability to AI Interactions

| Interaction ID | Stage / Scope | Generated IDs | Case Count |
|:---:|---|:---:|---:|
| **`INT-005`** | Phase 1A.1: Requirement, Parameter, and Domain Analysis | Foundation Analysis | 0 |
| **`INT-006`** | Phase 1A.2: Domain Partition and Boundary Generation | `FR02-AI-001` .. `FR02-AI-014` | 14 |
| **`INT-007`** | Phase 1A.3: Lockout State-Transition Generation | `FR02-AI-015` .. `FR02-AI-024` | 10 |
| **`INT-008`** | Phase 1A.4: Security Test Generation | `FR02-AI-025` .. `FR02-AI-031` | 7 |
| **`INT-009`** | Phase 1A.5: Schema & Error Contract Generation | `FR02-AI-032` .. `FR02-AI-037` | 6 |
| **`INT-010`** | Phase 1A.6 (Part A): AI Prompt Log Verbatim Repair | Support Interaction | 0 |
| **`INT-011`** | Phase 1A.6 (Part B): Generation Review & Manifest Freeze | Support Interaction | 0 |
| **TOTAL** | **Full Raw AI-Generated Inventory** | **`FR02-AI-001` .. `FR02-AI-037`** | **37** |

---

## 3. Techniques Represented

- **Equivalence Partitioning (EP):** Positive, negative, malformed, empty, null, and whitespace domain partitions.
- **Boundary Value Analysis (BVA):** Failure threshold boundaries ($N=1, 2, 3$) and lockout duration timing boundaries ($T=25\text{s}, 32\text{s}$).
- **State Transition & Sequence Testing:** Full lockout state machine progression, reset on successful login, and consecutive failure semantics.
- **Negative Testing:** Parameter presence, type checking, and malformed syntax rejection.
- **Security Probes:** SEC-05 SQL injection behavioral resistance, anti-enumeration cross-response equality, sensitive response data exclusion, token isolation, and SEC-02 downstream token usability probes.
- **Schema Validation & Error Contracts:** Top-level/nested data type checking, JSON error structure validation, transport parser contract, and MIME type consistency.

---

## 4. Authoritative Oracle Sources

- 📋 **[SRS]** EShop System Requirements Specification (Section 2: FR-02; Section 9: SEC-01..07)
- 🗂️ **[API-SPEC]** `api_specification.md` (Section 1.2: Đăng nhập)
- 📜 **[PDF]** HW06 Assignment Specification & Guidance

---

## 5. Formal Declaration & Freeze Status

> **Declaration:**
> "These 37 test cases are raw AI-generated test cases. They have not yet undergone the mandatory student Human Test-Case Audit. Potential AI errors, unsupported assumptions, overlap, or incomplete cases are intentionally preserved for later VALID / INVALID / INCOMPLETE classification."

**FR-02 AI GENERATION STATUS: FROZEN**
