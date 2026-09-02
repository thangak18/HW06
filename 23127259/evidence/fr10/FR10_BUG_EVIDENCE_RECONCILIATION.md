# FR-10 Strict Bug Evidence Reconciliation Report

- **Phase:** 2D.1F – FR-10 Confirmation Evidence Integrity + Genuine Postman Bug Screenshots
- **Tested Deployment:** `http://localhost:3000` (Student ID: `23127259`)
- **Strict Evidence Collection:** `postman/collections/FR10_Defect_Evidence_Strict.postman_collection.json`
- **Raw Evidence CLI:** `evidence/fr10/confirmation/FR10-bug-evidence-cli.txt` (SHA-256: `c85457ac825ded6a46d839140c511f88623bc0947d3bfe9f387b4f7222e1ae2d`)
- **Raw Evidence JSON:** `evidence/fr10/confirmation/FR10-bug-evidence.json` (SHA-256: `25bf0214768921d1d902093e867bcacf8504f1b0e13252769b593b5c7ec9c1d2`)
- **Raw Evidence HTML:** `evidence/fr10/confirmation/FR10-bug-evidence.html` (SHA-256: `203f06097f47fce9abcc5df77fe26933f79a159367114670c25f734f34624aa1`)
- **Process Exit Code:** `1` (8 expected product-defect assertion failures across confirmed bug routes)

---

## 1. Strict Evidence Reconciliation Table

| Bug ID | Fresh Fixture ID | Precondition Established | Expected Status / State | Observed Actual Status | Strict Assertion Failed | Harness Error | Persisted API State via Authorized GET | Defect Confirmed |
|---|:---:|:---:|---|:---:|:---:|:---:|:---:|:---:|
| **`BUG-FR10-001`** | `99` | **YES** (`shipping`) | `4xx` Client Error / State `'shipping'` | `200 OK` | **YES (2 Failed)** | **NO** | `'canceled'` | **YES** |
| **`BUG-FR10-002`** | `100` | **YES** (`canceled`) | `4xx` Client Error / State `'canceled'` | `200 OK` | **YES (2 Failed)** | **NO** | `'delivered'` | **YES** |
| **`BUG-FR10-003-A`** | `101` | **YES** (`pending`) | `403/401/404` / State `'pending'` | `200 OK` | **YES (2 Failed)** | **NO** | `'confirmed'` | **YES** |
| **`BUG-FR10-003-B`** | `102` | **YES** (`pending`) | `403/401/404` / State `'pending'` | `200 OK` | **YES (2 Failed)** | **NO** | `'canceled'` | **YES** |

---

## 2. Assertion Failure Characterization

- **Zero Harness Errors:** All fixture creations (User A checkout), authentication logins (Admin and User A), precondition mutations, and precondition verifications executed cleanly with HTTP 200/201 and 100% valid ID extractions.
- **Expected Product-Defect Assertion Failures:** All 8 assertion failures are strict canonical oracle violations directly caused by the SUT's non-compliant behavior:
  1. `[BUG-FR10-001]` Status assertion: expected `400/422/403/404`, observed `200`.
  2. `[BUG-FR10-001]` Persistence assertion: expected `'shipping'`, observed `'canceled'`.
  3. `[BUG-FR10-002]` Status assertion: expected `400/422/403/404`, observed `200`.
  4. `[BUG-FR10-002]` Persistence assertion: expected `'canceled'`, observed `'delivered'`.
  5. `[BUG-FR10-003-A]` Status assertion: expected `403/401/404`, observed `200`.
  6. `[BUG-FR10-003-A]` Persistence assertion: expected `'pending'`, observed `'confirmed'`.
  7. `[BUG-FR10-003-B]` Status assertion: expected `403/401/404`, observed `200`.
  8. `[BUG-FR10-003-B]` Persistence assertion: expected `'pending'`, observed `'canceled'`.
