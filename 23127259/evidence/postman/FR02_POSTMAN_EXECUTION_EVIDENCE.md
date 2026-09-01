# FR-02 Postman Execution Evidence

- **Feature Under Test:** FR-02 – Login and Account Lockout (Pool A)
- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`
- **Date & Time:** 2026-09-01 20:40:06+07:00

---

## 1. Tooling & Target Environment

- **Tool:** Postman Desktop (v11.89.0, macOS)
- **Target SUT:** `http://localhost:3000`
- **Collection:** `FR02_Login_Account_Lockout` ([`collections/FR02_Login_Account_Lockout.postman_collection.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/collections/FR02_Login_Account_Lockout.postman_collection.json))
- **Environment:** `FR02-local` ([`environments/FR02-local.postman_environment.json`](file:///Volumes/Thang/HW06/HW06/23127259/postman/environments/FR02-local.postman_environment.json))
- **Student Header Enforced:** `X-Student-Id: 23127259`

---

## 2. Runtime Header Injection & Anti-Cheat Verification

The collection enforces the mandatory student identification header on 100% of outgoing requests via the collection-level pre-request script:

```javascript
// Collection-Level Pre-request Script: Mandatory Student ID Enforcement
var studentId = pm.environment.get('studentId') || '23127259';
pm.request.headers.upsert({
    key: 'X-Student-Id',
    value: studentId
});
```

When executing requests in Postman, the header is dynamically evaluated and injected into the HTTP request headers prior to transmission over the wire to `http://localhost:3000`.

---

## 3. Postman Console Evidence (Anti-Cheat Header Proof)

- **Screenshot File:** [`FR02-postman-console-x-student-id.png`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/postman/FR02-postman-console-x-student-id.png)
- **SHA-256 Hash:** `8e428aa625e97343c40805e7fda58e62d8e357df6106c7305163df6039efc358`
- **File Size:** 495,616 bytes
- **Capture Source:** Real Postman Desktop UI Window

> [!NOTE]
> **Authentication Certification:**
> The screenshot was captured from the genuine Postman Console after a real HTTP request to the local EShop SUT (`http://localhost:3000/api/login`). It demonstrates runtime insertion of `X-Student-Id: 23127259` by the Postman test harness.

---

## 4. Collection Runner Evidence

- **Screenshot File:** [`FR02-postman-runner-result.png`](file:///Volumes/Thang/HW06/HW06/23127259/evidence/postman/FR02-postman-runner-result.png)
- **SHA-256 Hash:** `73670e3cf97d420318b5c8c61b0c6592de126a1d72a93ff757e616f86832389d`
- **File Size:** 614,400 bytes
- **Capture Source:** Real Postman Desktop UI Window
- **Execution Scope:** Collection / Folder execution in Postman Desktop UI
- **Observed Behavior:** Demonstrates interactive test execution with live test status indicators and console logging against the local SUT backend.

---

## 5. Relationship to Formal Newman Automated Results

> [!IMPORTANT]
> The Postman collection was additionally executed through Newman for formal automated execution, machine-readable JSON telemetry, and interactive HTML Extra reporting.
>
> **Newman Run 03 remains the primary full-suite automated result (40 / 40 formal test cases executed):**
> - **HTML Extra Dashboard Report:** [`23127259/newman/fr02/FR02-run-03.html`](file:///Volumes/Thang/HW06/HW06/23127259/newman/fr02/FR02-run-03.html)
> - **Telemetry JSON Report:** [`23127259/newman/fr02/FR02-run-03.json`](file:///Volumes/Thang/HW06/HW06/23127259/newman/fr02/FR02-run-03.json)
> - **Execution Summary:** [`23127259/newman/fr02/FR02_EXECUTION_SUMMARY.md`](file:///Volumes/Thang/HW06/HW06/23127259/newman/fr02/FR02_EXECUTION_SUMMARY.md)
