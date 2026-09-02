# FR-10 Canonical Map Self-Check Report

- **Phase:** 2D.1D.3 – Canonical Derived-Suite + Collection Repair
- **Validator Script:** `testcases/validate_fr10_canonical_map.py`
- **Target Map:** `testcases/fr10_canonical_cases.json`
- **Status:** **ALL GATES PASS (46/46 Canonical Cases Verified)**

---

## 1. Provenance Integrity Gates

| Gate | Requirement | Actual Status | Result |
|---|---|---|:---:|
| **Raw AI Draft Hash** | Immutable SHA-256 (`303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc`) | Matches exactly | **PASS** |
| **Total Canonical Entries** | Exactly 46 executable cases | 46 cases loaded | **PASS** |
| **Rejected AI-012** | Omitted from canonical map | Absent from JSON | **PASS** |
| **ID Uniqueness & Order** | Unique sequence AI-001..011, AI-013..042, HUM-001..005 | Validated 46/46 | **PASS** |

---

## 2. Critical Case Invariant Checks

| Case ID | Verified Canonical Semantics | Validator Check | Result |
|---|---|---|:---:|
| **FR10-AI-013** | Admin backward regression: `confirmed` -> `pending` (`PUT /api/admin/orders/:id/status`) | `initial_state = 'confirmed'`, `input = {'status': 'pending'}` | **PASS** |
| **FR10-AI-014** | Admin backward regression: `shipping` -> `confirmed` (`PUT /api/admin/orders/:id/status`) | `initial_state = 'shipping'`, `input = {'status': 'confirmed'}` | **PASS** |
| **FR10-AI-015** | Admin backward regression: `shipping` -> `pending` (`PUT /api/admin/orders/:id/status`) | `initial_state = 'shipping'`, `input = {'status': 'pending'}` | **PASS** |
| **FR10-AI-028** | Cryptographically tampered JWT on Admin status (`PUT /api/admin/orders/:id/status`) | `endpoint = '/api/admin/orders/:id/status'`, `auth = 'Tampered Admin JWT'` | **PASS** |
| **FR10-AI-029** | Missing Authorization on Customer cancellation (`PUT /api/orders/:id/cancel`) | `endpoint = '/api/orders/:id/cancel'`, `auth = 'Missing Authorization'` | **PASS** |
| **FR10-AI-030** | Normal Customer (`role = 'user'`) on Admin status `pending` -> `confirmed` | `endpoint = '/api/admin/orders/:id/status'`, `actor = 'Normal Customer'` | **PASS** |
| **FR10-AI-031** | Normal Customer (`role = 'user'`) on Admin status `pending` -> `canceled` | `endpoint = '/api/admin/orders/:id/status'`, `actor = 'Normal Customer'` | **PASS** |
| **FR10-AI-032** | Normal Customer (`role = 'user'`) on Admin status `confirmed` -> `shipping` | `endpoint = '/api/admin/orders/:id/status'`, `actor = 'Normal Customer'` | **PASS** |
| **FR10-AI-033** | Customer B probes cancellation on Customer A's `pending` order | `endpoint = '/api/orders/:id/cancel'`, `actor = 'User B'` | **PASS** |
| **FR10-AI-034** | Customer B probes cancellation on Customer A's `confirmed` order | `endpoint = '/api/orders/:id/cancel'`, `actor = 'User B'` | **PASS** |
| **FR10-AI-035..040** | Status enum `'processing'`, missing `{}`', `null`, numeric `123`, `999999`, `not-an-id` | Exact input types and values verified | **PASS** |
| **FR10-HUM-001..005** | Human extension sequence, multi-order isolation, in-transit cancel, exploratory probes | 5 Human extension cases verified | **PASS** |

---

## 3. Conclusion
The canonical machine-readable map (`fr10_canonical_cases.json`) is verified to be 100% faithful to Level 1–4 provenance with zero ID shifts or off-by-one errors.
