# Postman Collection Architecture & Demonstrated Features: FR-02

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Collection File:** [`23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json)
- **Environment File:** [`23127259/postman/environments/FR02-local.postman_environment.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/environments/FR02-local.postman_environment.json)

---

## 1. Postman Features Demonstrated in FR-02

The following table records the Postman capabilities actively implemented, verified, and executed in the FR-02 test suite:

| Postman Feature | Implemented? | Demonstration & Evidence Reference |
|---|:---:|---|
| **Postman Collection** | **YES** | Master collection `FR02_Login_Account_Lockout.postman_collection.json` containing 48 requests (40 formal tests + 8 setup helpers). |
| **Folders & Logical Hierarchy** | **YES** | 7 structured folders (`00 – Setup Helpers`, `01 – Positive Auth`, `02 – Domain Inputs`, `03 – Lockout Boundary`, `04 – Security`, `05 – Schema`, `06 – Human Extensions`). |
| **Environment Variables** | **YES** | `FR02-local.postman_environment.json` managing `baseUrl`, `studentId`, and dynamic credentials. |
| **Collection / Dynamic Variables** | **YES** | Dynamic per-run state isolation variables (`runId`, `userEmail`, `adminEmail`, `lockoutEmail`, `resetBoundaryEmail`, etc.) set dynamically via `pm.environment.set()`. |
| **Pre-request Scripts** | **YES** | Collection-level mandatory `X-Student-Id` header enforcement and multi-step request chaining (`pm.sendRequest`). |
| **pm.test Assertions** | **YES** | 71 formal Chai.js assertions validating status codes, response schemas, token integrity, and security bounds. |
| **Postman Console** | **YES** | Runtime inspection of outgoing headers and payloads. Evidence: [`FR02-postman-console-x-student-id.png`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/postman/FR02-postman-console-x-student-id.png). |
| **Collection Runner** | **YES** | Interactive suite execution in Postman Desktop UI. Evidence: [`FR02-postman-runner-result.png`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/postman/FR02-postman-runner-result.png). |
| **Newman CLI Execution** | **YES** | Automated headless execution (`FR02-run-03-console.txt` and `FR02-run-03.json`). |
| **Newman HTML Reporter** | **YES** | Rich HTML Extra interactive dashboard (`FR02-run-03.html`). |
| **Data-Driven Testing (Data File)** | **PREPARED** | Fixture file `fr02-domain-data.json` prepared in `postman/data/`. |
| **Postman Monitor / Mock Server** | **N/A** | Not applicable for local backend SUT testing. |

---

## 2. Advanced Postman Implementation Details

### 2.1 Collection-Level Pre-Request Script
Enforces mandatory student identification header on 100% of outgoing requests:
```javascript
var studentId = pm.environment.get('studentId') || '23127259';
pm.request.headers.upsert({
    key: 'X-Student-Id',
    value: studentId
});
```

### 2.2 Dynamic Run-to-Run State Isolation
In `00 – Setup Helpers`, each run dynamically generates a unique `runId` timestamp ensuring completely fresh test accounts and zero state interference between executions:
```javascript
if (!pm.environment.get("runId")) {
    var runId = Date.now().toString().slice(-6);
    pm.environment.set("runId", runId);
    pm.environment.set("userEmail", "user_" + runId + "@eshop.com");
    pm.environment.set("adminEmail", "admin_" + runId + "@eshop.com");
    pm.environment.set("lockoutEmail", "lockout_" + runId + "@eshop.com");
    // ...
}
```

### 2.3 Asynchronous Chaining with `pm.sendRequest`
Complex multi-step state progression tests (such as consecutive failure sequences in `FR02-AI-023` and `FR02-HUM-003` and isolation tests in `FR02-HUM-004`) utilize nested `pm.sendRequest` workflows inside Pre-request scripts to make each test case completely autonomous and self-contained.

### 2.4 Precise Timing Synchronization
`FR02-AI-021` records the start timestamp `lockStartTime` at failure #3 and synchronizes execution until exactly 32 seconds have elapsed before issuing the post-expiration verification probe.

---

## 3. Execution References
- **Postman Execution Evidence Report:** [`23127259/evidence/postman/FR02_POSTMAN_EXECUTION_EVIDENCE.md`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/postman/FR02_POSTMAN_EXECUTION_EVIDENCE.md)
- **Newman Automated Execution Report:** [`23127259/newman/fr02/FR02-run-03.html`](file:///Volumes/Thang/HW06/HW06/23127259/newman/fr02/FR02-run-03.html)
