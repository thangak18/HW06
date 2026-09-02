# FR-10 Defect Confirmation & Evidence Report

- **Phase:** 2D.1F – FR-10 Confirmation Evidence Integrity + Genuine Postman Bug Screenshots
- **Tested Deployment:** `http://localhost:3000` (Student ID: `23127259`)
- **Strict Evidence Collection:** `postman/collections/FR10_Defect_Evidence_Strict.postman_collection.json`
- **Observational Collection (Historical):** `postman/collections/FR10_Defect_Confirmation.postman_collection.json`
- **Full Formal Suite Rerun:** **NO**
- **Run 04 Executed:** **NO**

---

## 1. Historical Confirmation Execution Accounting

| Execution Stage | Purpose / Description | Executed Requests | Status / Output Files | Valid Product Evidence |
|---|---|:---:|---|:---:|
| **Run 01 Attempt (INT-051)** | Initial confirmation run with defective checkout ID extraction | ~19 | **CONFIRMATION PROCESS DEFECT:** Raw files overwritten during INT-051 recovery | **NO** (Harness defect) |
| **Run 02 Observational (INT-051)** | Repaired checkout extraction; verified black-box responses | 19 | Preserved as `FR10-confirmation-run02.*` | **YES** (Observational) |
| **Strict Evidence Run (INT-052)** | Canonical oracle failure verification under strict assertions | 19 | `FR10-bug-evidence.*` | **YES** (Strict Canonical Evidence) |

---

## 2. HTTP Traffic Accounting

| Traffic Component | Target Host | Request Count | Notes |
|---|---|:---:|---|
| **Run 01 Attempt (INT-051)** | `http://localhost:3000` | ~19 | Lower-bound transcript reconstruction |
| **Run 02 Confirmation (INT-051)** | `http://localhost:3000` | 19 | 2 Auth + 17 Fixture & Verification requests |
| **CDP / Postman UI Automation** | `http://localhost:3000` | 9 | 3 Setup + 3 Actions + 3 Verifications |
| **Strict Evidence Run (INT-052)** | `http://localhost:3000` | 19 | 2 Auth + 17 Fixture & Strict Verification requests |
| **Total SUT HTTP Traffic (Phase 2D.1E–F)** | `http://localhost:3000` | **~66 requests** | Full formal suite was NOT rerun |

---

## 3. Defect Confirmation Summary Table

| Candidate Cluster | Fresh Fixture ID | Precondition State | Candidate Action | Observed HTTP | Persisted API State via Authorized GET | Reproduction Result | Confirmed Bug ID | GitHub Issue |
|---|---|---|---|:---:|:---:|:---:|---|---|
| **`CANDIDATE-FR10-FSM-01`** | `99` | `shipping` | `PUT /api/orders/99/cancel` (User A) | `200 OK` | `'canceled'` | **CONFIRMED** | `BUG-FR10-001` | [#29](https://github.com/thangak18/HW06/issues/29) |
| **`CANDIDATE-FR10-FSM-02`** | `100` | `canceled` | `PUT /api/admin/orders/100/status` body `{"status":"delivered"}` | `200 OK` | `'delivered'` | **CONFIRMED** | `BUG-FR10-002` | [#30](https://github.com/thangak18/HW06/issues/30) |
| **`CANDIDATE-SEC03-01` (A)** | `101` | `pending` | `PUT /api/admin/orders/101/status` body `{"status":"confirmed"}` (User A) | `200 OK` | `'confirmed'` | **CONFIRMED** | `BUG-FR10-003` | [#31](https://github.com/thangak18/HW06/issues/31) |
| **`CANDIDATE-SEC03-01` (B)** | `102` | `pending` | `PUT /api/admin/orders/102/status` body `{"status":"canceled"}` (User A) | `200 OK` | `'canceled'` | **CONFIRMED** | `BUG-FR10-003` | [#31](https://github.com/thangak18/HW06/issues/31) |

---

## 4. Retained Evidence Artifacts & Checksums

| Artifact Category | Relative Path | SHA-256 Checksum |
|---|---|---|
| **Strict Evidence CLI** | `evidence/fr10/confirmation/FR10-bug-evidence-cli.txt` | `c85457ac825ded6a46d839140c511f88623bc0947d3bfe9f387b4f7222e1ae2d` |
| **Strict Evidence JSON** | `evidence/fr10/confirmation/FR10-bug-evidence.json` | `25bf0214768921d1d902093e867bcacf8504f1b0e13252769b593b5c7ec9c1d2` |
| **Strict Evidence HTML** | `evidence/fr10/confirmation/FR10-bug-evidence.html` | `203f06097f47fce9abcc5df77fe26933f79a159367114670c25f734f34624aa1` |
| **Strict Exit Code** | `evidence/fr10/confirmation/FR10-bug-evidence-exitcode.txt` | `f620f5ea55284b37237ed886333986eaec4c6502c65b53da7fc2845c6c5ce6b4` |
| **Run 02 CLI** | `evidence/fr10/confirmation/FR10-confirmation-run02-cli.txt` | `efd79ce3444f66f4c0c3f93f875dd828f98a7ca9c92a955a444eedbd6c8227ac` |
| **Run 02 JSON** | `evidence/fr10/confirmation/FR10-confirmation-run02.json` | `6ba61f83ea29713cc3538d75e218c8007fe7f5d4baeedf1bed316dc3fe25d092` |
| **Run 02 HTML** | `evidence/fr10/confirmation/FR10-confirmation-run02.html` | `428f32b7348a4be3ec590a20a10366768d577bfa7c5ff33e6ee8906193df9814` |
| **Run 02 Exit Code** | `evidence/fr10/confirmation/FR10-confirmation-run02-exitcode.txt` | `4b265ba288f0c64ffc10c6d51fbfaa6e1ffc1fcb1eca198237cf5bd8339b86b4` |
| **Screenshot BUG-FR10-001** | `evidence/fr10/bugs/BUG-FR10-001-postman-evidence.png` | `d1183ba747b0d8d5ef838a4dd78e4096504b14e40786bd7fcf896f8900ae209d` |
| **Screenshot BUG-FR10-002** | `evidence/fr10/bugs/BUG-FR10-002-postman-evidence.png` | `375dffd8a176def360b5606f10ee14c54db000d9bd5323e47221a1856618c590` |
| **Screenshot BUG-FR10-003** | `evidence/fr10/bugs/BUG-FR10-003-postman-evidence.png` | `8bfc6f291aaf5b3ff32e2a71af20403798dd577792c967f9508ac258deea2629` |
