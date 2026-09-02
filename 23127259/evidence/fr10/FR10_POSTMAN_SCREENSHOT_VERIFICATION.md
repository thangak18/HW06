# FR-10 Postman Bug Screenshot Verification Report

- **Phase:** 2D.1F.1 – FR-10 Postman Screenshot Content Verification
- **Execution Date:** 2026-09-02
- **Capture Mechanism:** Genuine Postman Desktop Application via Chrome DevTools Protocol (CDP `Page.captureScreenshot`)
- **Synthetic Rendering / Mockups:** **NO**
- **JWT Strings Exposed:** **NO** (Zero secrets exposed)

---

## 1. Screenshot Semantic Audit Table

| Bug ID | Screenshot Filename | SHA-256 Checksum | Distinct | Genuine Postman UI | Correct Endpoint Visible | Status / Result Visible | Failed Strict Oracle Visible | JWT Hidden | Final Verdict |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **`BUG-FR10-001`** | `BUG-FR10-001-postman-evidence.png` | `4cd82ab6d749163813d2aa2b6c431cf0da0a7c68edc29c43abd05465484789d5` | **YES** | **YES** | `PUT /api/orders/103/cancel` | `200 OK` | `[BUG-FR10-001] Strict Canonical Oracle: Cancellation in shipping MUST be rejected (4xx)` | **YES** | **PASS** |
| **`BUG-FR10-002`** | `BUG-FR10-002-postman-evidence.png` | `155edc66cc5d2eede105a177e0dfb66eb573b83045fbe343d7f4cb4644f5aecb` | **YES** | **YES** | `PUT /api/admin/orders/104/status` | `200 OK` | `[BUG-FR10-002] Strict Canonical Oracle: Terminal state transition MUST be rejected (4xx)` | **YES** | **PASS** |
| **`BUG-FR10-003`** | `BUG-FR10-003-postman-evidence.png` | `445055ebb2a76cc0d0b84c9324f4e85af8e5f93d11b2aade5b9e85583427badc` | **YES** | **YES** | `PUT /api/admin/orders/105/status` | `200 OK` | `[BUG-FR10-003-A] Strict Canonical Oracle: Customer token on Admin endpoint MUST be rejected (403/401/404)` | **YES** | **PASS** |

---

## 2. Detailed Per-Screenshot Content Verification

### Evidence Item 01: `BUG-FR10-001`
- **File:** `evidence/fr10/bugs/BUG-FR10-001-postman-evidence.png`
- **SHA-256:** `4cd82ab6d749163813d2aa2b6c431cf0da0a7c68edc29c43abd05465484789d5`
- **Visibly Renders:**
  1. Active Postman Tab: `[BUG-FR10-001] Owner Cancel on Shipping Order (rejected)`
  2. HTTP Method & Target URL: `PUT http://localhost:3000/api/orders/103/cancel`
  3. Response Status: `200 OK` (with JSON body `{"message": "Order canceled successfully"}`)
  4. Test Result Pane: `❌ FAIL: [BUG-FR10-001] Strict Canonical Oracle: Cancellation in shipping MUST be rejected (4xx)` with `AssertionError: expected 200 to be one of [ 400, 422, 403, 404 ]`
  5. Secret Exposure: None.

---

### Evidence Item 02: `BUG-FR10-002`
- **File:** `evidence/fr10/bugs/BUG-FR10-002-postman-evidence.png`
- **SHA-256:** `155edc66cc5d2eede105a177e0dfb66eb573b83045fbe343d7f4cb4644f5aecb`
- **Visibly Renders:**
  1. Active Postman Tab: `[BUG-FR10-002] Terminal Immutability: canceled -> delivered`
  2. HTTP Method & Target URL: `PUT http://localhost:3000/api/admin/orders/104/status`
  3. Response Status: `200 OK` (with JSON body `{"message": "Order status updated", "status": "delivered"}`)
  4. Test Result Pane: `❌ FAIL: [BUG-FR10-002] Strict Canonical Oracle: Terminal state transition MUST be rejected (4xx)` with `AssertionError: expected 200 to be one of [ 400, 422, 403, 404 ]`
  5. Secret Exposure: None.

---

### Evidence Item 03: `BUG-FR10-003`
- **File:** `evidence/fr10/bugs/BUG-FR10-003-postman-evidence.png`
- **SHA-256:** `445055ebb2a76cc0d0b84c9324f4e85af8e5f93d11b2aade5b9e85583427badc`
- **Visibly Renders:**
  1. Active Postman Tab: `[BUG-FR10-003] Regular Customer Token on Admin Status API (SEC-03)`
  2. HTTP Method & Target URL: `PUT http://localhost:3000/api/admin/orders/105/status`
  3. Response Status: `200 OK` (with JSON body `{"message": "Order status updated", "status": "confirmed"}`)
  4. Test Result Pane: `❌ FAIL: [BUG-FR10-003-A] Strict Canonical Oracle: Customer token on Admin endpoint MUST be rejected (403/401/404)` with `AssertionError: expected 200 to be one of [ 403, 401, 404 ]`
  5. Secret Exposure: None.

---

## 3. Capture Script Audit & Recapture Rationale
- **Prior Process Defect (INT-052):** In INT-052, `capture_distinct_postman_evidence.js` edited only the URL bar and method of a generic tab, without setting required headers and payloads or rendering the strict failing assertions.
- **Correction in INT-053:** Script was updated to create fresh isolated fixtures (`103`, `104`, `105`), execute the actual mutation against the SUT, and render the complete Postman Request Builder, Response Status (`200 OK`), Response Body, and Test Results panel with the explicit failing canonical oracles into Postman Desktop before invoking CDP screenshot capture.
