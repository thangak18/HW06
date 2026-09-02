# FR-14 Evidence Index & Artifact Registry

- **Student:** Nguyễn Tấn Thắng (`23127259`)
- **Feature:** FR-14 – Category Management CRUD (Pool C – Web Admin)
- **Status:** Complete Execution & Verified

---

## 1. Newman Runtime Evidence

| Evidence Type | File Path | Details |
|---|---|---|
| **CLI Execution Log** | [`FR14-run01-cli.txt`](newman/FR14-run01-cli.txt) | 59 requests, 96 assertions (81 passed, 15 failed defect confirmations), 6.8s run duration |
| **HTML Extra Report** | [`FR14-run01.html`](newman/FR14-run01.html) | Full interactive Newman HTML Extra report with request/response payloads |
| **JSON Execution Export** | [`FR14-run01.json`](newman/FR14-run01.json) | Complete machine-readable Newman run results export |
| **Exit Code Record** | [`FR14-run01-exitcode.txt`](newman/FR14-run01-exitcode.txt) | Non-zero exit code reflecting intentional defect detection assertions |

---

## 2. Test Suite & Validation Evidence

| Component | Path | Status |
|---|---|:---:|
| **Postman Collection** | `23127259/postman/collections/FR14_Category_CRUD.postman_collection.json` | Validated (10 folders, 59 requests) |
| **Collection Static Validator** | `23127259/postman/validate_fr14_collection.js` | 100% Passed |
| **Canonical Test Cases JSON** | `23127259/testcases/fr14_canonical_cases.json` | 49 canonical cases |
| **Canonical Map Validator** | `23127259/testcases/validate_fr14_canonical_map.py` | 100% Passed (All 5 gates) |

---

## 3. Bug Reports & Defect Evidence

| Bug ID | Title | Severity | Report Path |
|---|---|:---:|---|
| **BUG-FR14-001** | Missing RBAC: Regular user can CRUD categories | 🔴 HIGH | `23127259/bugs/BUG-FR14-001.md` |
| **BUG-FR14-002** | Missing input validation on category name | 🟡 MEDIUM | `23127259/bugs/BUG-FR14-002.md` |
| **BUG-FR14-003** | No existence check: PUT/DELETE succeed on non-existent IDs | 🟡 MEDIUM | `23127259/bugs/BUG-FR14-003.md` |
| **BUG-FR14-004** | Unhandled server exception (HTTP 500) when Content-Type omitted | 🔴 HIGH | `23127259/bugs/BUG-FR14-004.md` |
| **Bug Registry** | Master defect and finding registry | — | `23127259/bugs/BUG_REGISTRY_FR14.md` |

---

## 4. AI Audit & Interaction Evidence

| Interaction ID | Description | Path |
|---|---|---|
| `INT-060` | FR-14 Isolated setup & grounded requirement analysis | `23127259/ai/interactions/INT-060-fr14-requirement-analysis-and-strategy.md` |
| `INT-061` | Step-by-step AI test generation (42 raw cases) | `23127259/ai/interactions/INT-061-fr14-ai-test-generation.md` |
| `INT-062` | Human audit & human extension design (7 cases) | `23127259/ai/interactions/INT-062-fr14-human-audit-and-extension.md` |
| `INT-063` | Postman collection build & static validation | `23127259/ai/interactions/INT-063-fr14-postman-collection-and-static-validation.md` |
| `INT-064` | Newman runtime execution & bug reporting | `23127259/ai/interactions/INT-064-fr14-runtime-execution-and-defect-confirmation.md` |
| Master Audit | Human audit decisions for all cases | `23127259/ai/TC_AUDIT_FR14.md` |
