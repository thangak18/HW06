# Postman Collection Architecture & Advanced Features: FR-02

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Primary Endpoint:** `POST /api/login`
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Collection File:** [`23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json)
- **Environment File:** [`23127259/postman/environments/FR02-local.postman_environment.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/environments/FR02-local.postman_environment.json)

---

## 1. Advanced Postman Capabilities Implemented

### 1.1 Collection-Level Pre-Request Script
Enforces mandatory student identification header on 100% of outgoing requests:
```javascript
var studentId = pm.environment.get('studentId') || '23127259';
pm.request.headers.upsert({
    key: 'X-Student-Id',
    value: studentId
});
```

### 1.2 Dynamic Run-to-Run State Isolation
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

### 1.3 Asynchronous Chaining with `pm.sendRequest`
Complex multi-step state progression tests (such as consecutive failure sequences in `FR02-AI-023` and `FR02-HUM-003` and isolation tests in `FR02-HUM-004`) utilize nested `pm.sendRequest` workflows inside Pre-request scripts to make each test case completely autonomous and self-contained.

### 1.4 Precise Timing Synchronization
`FR02-AI-021` records the start timestamp `lockStartTime` at failure #3 and synchronizes execution until exactly 32 seconds have elapsed before issuing the post-expiration verification probe.

---

## 2. Automated Newman Execution & Reporting

The collection is fully compatible with Newman CLI and HTML Extra reporting:

```bash
# Run full automated test suite with HTML Extra report
newman run 23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json \
  -e 23127259/postman/environments/FR02-local.postman_environment.json \
  --timeout-script 60000 \
  -r cli,json,htmlextra \
  --reporter-json-export 23127259/newman/fr02/FR02-run-03.json \
  --reporter-htmlextra-export 23127259/newman/fr02/FR02-run-03.html
```
