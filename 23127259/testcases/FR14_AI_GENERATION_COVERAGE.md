# FR-14 AI Generation Coverage Analysis

**Feature:** FR-14 – Category Management CRUD (Pool C – Web Admin)  
**Student:** Nguyễn Tấn Thắng (`23127259`)  
**Generation Source:** `FR14_AI_DRAFT.md` (42 Raw Cases)  
**Authoritative Standards:** EShop SRS FR-14 / FR-12, `api_specification.md`, HW06 Assignment Notes  
**Analysis Date:** September 2, 2026

---

## 1. Executive Summary

The raw AI generation stage (`FR14_AI_DRAFT.md`) produced **42 test cases** covering the Category Management CRUD functionality. This exceeds the mandatory course requirement of $\ge 35$ AI-generated test cases per API feature by **7 cases (+20%)**.

The generation was structured across 8 discrete interactions ensuring comprehensive coverage of the required testing dimensions:
1. **Domain Partitions & Boundaries** (Input Validation on `name` and `:id`)
2. **State Transitions & CRUD Lifecycle**
3. **Security Requirements** (SEC-01 Authentication, SEC-02 Authorization / RBAC, SEC-03 Injection / XSS, SEC-04 IDOR, SEC-07 Mass Assignment)
4. **Response Schema & Protocol Validation**

---

## 2. Test Dimension Coverage Matrix

| Dimension | Target Area | Case IDs | Count | Spec / Rule Basis |
|---|---|---|:---:|---|
| **Happy Path / CRUD** | Full lifecycle operations (Create, List, Update, Delete) with valid inputs and admin auth | TC-FR14-001 to TC-FR14-006 | 6 | SRS FR-14, API-SPEC Admin Categories |
| **Authentication (SEC-01)** | Missing, malformed, and cryptographically tampered JWT tokens on mutating routes | TC-FR14-007 to TC-FR14-011 | 5 | SRS §9 SEC-01, API-SPEC §0 |
| **Authorization / RBAC (SEC-02)** | Regular customer role (`role='user'`) attempting admin CRUD routes vs public list | TC-FR14-012 to TC-FR14-015 | 4 | SRS §9 SEC-02, SRS FR-12 RBAC |
| **Input Validation: `name`** | Empty string, null, missing key, whitespace, boundary length (1001 chars), Unicode, duplicate, type coercion | TC-FR14-016 to TC-FR14-023 | 8 | SRS FR-14 Input Constraints, Boundary Rules |
| **Input Validation: `:id`** | Non-existent ID, zero, negative integer, non-numeric string type mismatch | TC-FR14-024 to TC-FR14-028 | 5 | Boundary Value Analysis, SQLite Type Safety |
| **Security Probes** | SQL injection probe, stored XSS payload, mass assignment (extra body fields, ID override), NoSQL injection, IDOR | TC-FR14-029 to TC-FR14-034 | 6 | SRS §9 SEC-03, SEC-04, SEC-07 |
| **State Transitions** | End-to-end CRUD sequence, referential integrity (delete with products), zombie update, double delete | TC-FR14-035 to TC-FR14-038 | 4 | FSM State Machine Rules, DB Referential Integrity |
| **Schema Validation** | Array of category objects, status message schemas for Create, Update, Delete | TC-FR14-039 to TC-FR14-042 | 4 | API-SPEC Contract, JSON Schema Draft-07 |
| **Total AI Cases** | | | **42** | $\ge 35$ Minimum Satisfied |

---

## 3. Detailed Parameter Partition Distribution

### 3.1 `name` Parameter Coverage (POST / PUT)

| Equivalence Partition | Description | AI Case ID | Classification |
|---|---|:---:|:---:|
| **EP-NM-01** | Valid standard ASCII name ("Tablet") | TC-FR14-002, 004 | Valid |
| **EP-NM-02** | Empty string (`""`) | TC-FR14-016 | Invalid |
| **EP-NM-03** | Null value (`null`) | TC-FR14-017 | Invalid |
| **EP-NM-04** | Missing parameter key | TC-FR14-018 | Invalid |
| **EP-NM-05** | Whitespace-only string (`"   "`) | TC-FR14-019 | Invalid |
| **EP-NM-06** | Extremely long string (1001 chars) | TC-FR14-020 | Boundary |
| **EP-NM-07** | Vietnamese Unicode & emoji | TC-FR14-021 | Valid / I18N |
| **EP-NM-08** | Duplicate category name ("Điện thoại") | TC-FR14-022 | Exploratory |
| **EP-NM-09** | SQL Injection payload (`'; DROP TABLE...`) | TC-FR14-029 | Security / Probe |
| **EP-NM-10** | Stored XSS payload (`<script>...`) | TC-FR14-030 | Security / Probe |
| **EP-NM-11** | Non-string numeric type (`12345`) | TC-FR14-023 | Type Mismatch |

### 3.2 `:id` Parameter Coverage (PUT / DELETE)

| Equivalence Partition | Description | AI Case ID | Classification |
|---|---|:---:|:---:|
| **EP-ID-01** | Valid existing category ID | TC-FR14-004, 006 | Valid |
| **EP-ID-02** | Non-existent positive integer (`99999`) | TC-FR14-024, 025 | Invalid / Boundary |
| **EP-ID-03** | Zero boundary value (`0`) | TC-FR14-026 | Invalid / Boundary |
| **EP-ID-04** | Negative integer (`-1`) | TC-FR14-027 | Invalid / Boundary |
| **EP-ID-05** | Alphanumeric string (`"abc"`) | TC-FR14-028 | Type Mismatch |

---

## 4. Security Requirement (SEC) Mapping

| Standard Requirement | Description | AI Case Coverage | SUT Assessment |
|---|---|---|---|
| **SEC-01** | Authentication & Token Validity | TC-FR14-007, 008, 009, 010, 011 | SUT verifies JWT presence and signature correctly on protected routes |
| **SEC-02** | Authorization & RBAC | TC-FR14-012, 013, 014, 015 | **VULNERABLE (BUG-FR14-001):** Regular user token is accepted on all CRUD endpoints |
| **SEC-03** | Injection & XSS Protection | TC-FR14-029, 030, 033 | Parameterized queries prevent SQLi; stored XSS risk exists if frontend unescapes |
| **SEC-04** | Insecure Direct Object Reference (IDOR) | TC-FR14-034 | **VULNERABLE:** Regular user can modify/delete arbitrary categories by ID |
| **SEC-05** | Sensitive Data Exposure | TC-FR14-001, 015, 039 | Public GET categories exposes only `id` and `name` — no sensitive leakage |
| **SEC-07** | Mass Assignment & Tampering | TC-FR14-031, 032 | Extra payload keys (`id`, `admin`, `role`) are safely ignored by destructuring |

---

## 5. Audit Transition Summary

All 42 AI-generated test cases were audited in `FR14_HUMAN_AUDIT_CORRECTIONS.md`.  
- **39 cases (92.9%)** were approved as **VALID AS-IS** or with dual-assertion oracle framing.
- **3 cases (7.1%)** were classified as **INCOMPLETE** and received concrete human corrections:
  - `TC-FR14-011`: Concrete tampered JWT structure specified.
  - `TC-FR14-020`: String length fixed to 1001 characters with SQLite unbounded text handling verified.
  - `TC-FR14-033`: Response status disjunction (`[200, 400, 500]`) specified for object body handling.
- **0 cases** were completely rejected as invalid.

Identified testing gaps were forwarded to `FR14_HUMAN_EXTENSION_DESIGN.md` for human test case authoring.
