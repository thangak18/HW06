# FR-10 Targeted Defect Confirmation Report

- **Phase:** 2D.1E – FR-10 Targeted Defect Confirmation + Bug Evidence + GitHub Issues
- **Execution Date:** 2026-09-02
- **Tested Deployment:** `http://localhost:3000` (Student ID: `23127259`)
- **Confirmation Collection:** `postman/collections/FR10_Defect_Confirmation.postman_collection.json`
- **Confirmation Evidence CLI:** `evidence/fr10/confirmation/FR10-confirmation-cli.txt`
- **Confirmation Evidence JSON:** `evidence/fr10/confirmation/FR10-confirmation.json`
- **Confirmation Evidence HTML:** `evidence/fr10/confirmation/FR10-confirmation.html`
- **Full-Suite Rerun Executed:** **NO**
- **Run 04 Executed:** **NO**
- **Total Confirmation HTTP Traffic:** Exactly **19 requests** (2 auth logins + 17 isolated fixture & verification steps)

---

## 1. Defect Confirmation Summary Table

| Candidate Cluster | Fresh Fixture ID | Precondition State | Candidate Action | HTTP Status | Persisted State via Authorized GET | Reproduction Result | Confirmed Bug ID | GitHub Issue |
|---|---|---|---|:---:|---|:---:|---|---|
| **`CANDIDATE-FR10-FSM-01`** | `95` | `shipping` | `PUT /api/orders/95/cancel` with User A token | `200 OK` | `'canceled'` | **CONFIRMED** | `BUG-FR10-001` | [#29](https://github.com/thangak18/HW06/issues/29) |
| **`CANDIDATE-FR10-FSM-02`** | `96` | `canceled` | `PUT /api/admin/orders/96/status` body `{"status":"delivered"}` with Admin token | `200 OK` | `'delivered'` | **CONFIRMED** | `BUG-FR10-002` | [#30](https://github.com/thangak18/HW06/issues/30) |
| **`CANDIDATE-SEC03-01` (Variant A)** | `97` | `pending` | `PUT /api/admin/orders/97/status` body `{"status":"confirmed"}` with User A token | `200 OK` | `'confirmed'` | **CONFIRMED** | `BUG-FR10-003` | [#31](https://github.com/thangak18/HW06/issues/31) |
| **`CANDIDATE-SEC03-01` (Variant B)** | `98` | `pending` | `PUT /api/admin/orders/98/status` body `{"status":"canceled"}` with User A token | `200 OK` | `'canceled'` | **CONFIRMED** | `BUG-FR10-003` | [#31](https://github.com/thangak18/HW06/issues/31) |

---

## 2. Supporting Run 03 Evidence vs. Confirmation Evidence

| Bug ID | Supporting Run 03 Formal IDs | Run 03 Result | Isolated Confirmation Result | Total Observations |
|---|---|---|---|:---:|
| **`BUG-FR10-001`** | `FR10-AI-016`, `FR10-HUM-003` | Status 200, state `'canceled'` | Status 200, state `'canceled'` (Fixture `95`) | **2 / 2** |
| **`BUG-FR10-002`** | `FR10-AI-024` | Status 200, state `'delivered'` | Status 200, state `'delivered'` (Fixture `96`) | **2 / 2** |
| **`BUG-FR10-003`** | `FR10-AI-030`, `FR10-AI-031`, `FR10-AI-032` | Status 200 across 3 Admin routes | Status 200 across 2 fresh routes (Fixtures `97`, `98`) | **5 / 5** |

---

## 3. Evidence Artifact Checksums

| Artifact | File Path | SHA-256 Checksum |
|---|---|---|
| **Screenshot BUG-FR10-001** | `evidence/fr10/bugs/BUG-FR10-001-postman.png` | `0aa586375eae9781bcb472b4b54777eafabf3735c97e9abcec93b25cc979f46b` |
| **Screenshot BUG-FR10-002** | `evidence/fr10/bugs/BUG-FR10-002-postman.png` | `0aa586375eae9781bcb472b4b54777eafabf3735c97e9abcec93b25cc979f46b` |
| **Screenshot BUG-FR10-003** | `evidence/fr10/bugs/BUG-FR10-003-postman.png` | `0aa586375eae9781bcb472b4b54777eafabf3735c97e9abcec93b25cc979f46b` |
| **Confirmation JSON** | `evidence/fr10/confirmation/FR10-confirmation.json` | Calculated at commit |
