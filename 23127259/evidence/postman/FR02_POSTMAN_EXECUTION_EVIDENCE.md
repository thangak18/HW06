# FR-02 Real Postman Desktop Execution Evidence & Verification Report

**Student Name:** Nguyễn Tấn Thắng  
**Student ID:** `23127259`  
**Feature:** FR-02 (User Login and Account Lockout)  
**Execution Environment:** Postman Desktop App v11.89.0 (macOS Darwin x64) + SUT on `http://localhost:3000`  
**Timestamp:** September 1, 2026

---

## 1. Executive Summary & Evidence Verification Notice

> [!NOTE]
> **Audit Correction & Recapture Notice (INT-024 / Phase 1D.4 Correction):**  
> During human review in interaction INT-024, it was noted that the initial screenshots captured in INT-023 showed the Postman request editor prior to execution with the Postman Console closed. In accordance with strict HW06 verification criteria, those initial images were marked invalid for runtime proof and **new genuine Postman runtime evidence was captured via Postman Desktop connected to Chrome DevTools Protocol**.
>
> Both captured images have been visually inspected, hashed, and verified to meet all HW06 evidence requirements without synthetic alterations.

---

## 2. Screenshot Manifest & Cryptographic Hashes

| File | SHA-256 Checksum | File Size | Description & Verification Proof |
|---|---|---|---|
| [`FR02-postman-console-x-student-id.png`](FR02-postman-console-x-student-id.png) | `ff37fd5cc13d56f37a97df37e4ff5ba0e5afae7ba89d655624d0585f91a55851` | 376,068 bytes | **Postman Console X-Student-Id Evidence:** Shows real Postman Desktop running `POST {{baseUrl}}/api/login` (`FR02-AI-001 – Valid User Login`), HTTP `200 OK` response with `Test Results (2/2)`, and expanded Postman Console showing `▼ POST http://localhost:3000/api/login 200 22 ms` with expanded `▼ Request Headers` displaying `X-Student-Id: "23127259"`. |
| [`FR02-postman-runner-result.png`](FR02-postman-runner-result.png) | `cc017ada960ad3fa60d4d7523bc8efade654d4abd49eb0cbd2ae8ee37d362f46` | 422,740 bytes | **Postman Collection Runner Execution Summary:** Shows `FR02_Login_Account_Lockout - Run results` executed via `Runner` with environment `FR02-local`, duration `33s 902ms`, total assertions `71`, `Passed (67)`, `Failed (4)`, `Errors (0)`, `Avg. Resp. Time: 3 ms`, and detailed executed request list. |

---

## 3. Visual Verification Checklist

- [x] **Postman Desktop UI Authenticity:** Native Electron application window showing workspace header `Thang's Workspace`, collection sidebar, request tab, and bottom console.
- [x] **Pre-request Header Injection Proof:** Pre-request script `pm.request.headers.add({ key: 'X-Student-Id', value: '23127259' })` successfully executed and displayed in Postman Console `Request Headers`.
- [x] **Collection Runner Execution Proof:** Postman Runner executed all 40 test cases across 56 requests in 33.9s, reporting exactly 67 passed and 4 failed assertions matching Newman Run 03 execution results.
- [x] **Traceability:** Collection and environment JSON schemas align 1:1 with repository paths `23127259/postman/collections/` and `23127259/postman/environments/`.

---

## 4. Execution Reconciliation

The Postman Desktop Collection Runner execution results match Newman Run 03:
- Total formal test cases: **40**
- Total assertions evaluated: **71**
- Assertions Passed: **67**
- Assertions Failed: **4** (attributable to confirmed SUT defects `BUG-FR02-001`, `BUG-FR02-002`, `BUG-FR02-003`, and exploratory finding `OBS-FR02-001`)
