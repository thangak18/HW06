# FR-02 Bug Screenshot & Real Verification Checklist

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

> [!IMPORTANT]
> **Genuine Evidence Requirement:**
> HW06 requires real screenshot evidence captured from actual runtime execution by the student.
> Fake or synthesized images are strictly prohibited.

---

## 1. Completed Bug Screenshots for Confirmed Issues

| Bug ID | Title | Final File Path | Visible Proof |
|---|---|---|---|
| **`BUG-FR02-001`** | Plaintext Password Exposure | `23127259/bugs/screenshots/FR02/BUG-FR02-001-login-password-exposure.png` | Native Runner row for `FR02-AI-028`, HTTP 200, failed password-omission assertion. |
| **`BUG-FR02-002`** | Lockout Does Not Expire After 30s | `23127259/bugs/screenshots/FR02/BUG-FR02-002-lock-after-30s.png` | Native Runner row for `FR02-AI-021`, HTTP 403 after the T=32s scenario, failed expected-200 assertion, and lock error response. |
| **`BUG-FR02-003`** | Premature Lockout at N=2 Boundary | `23127259/bugs/screenshots/FR02/BUG-FR02-003-correct-login-at-n2.png` | Native Runner row for `FR02-HUM-003`, HTTP 403 after two failures, failed expected-200 assertion, and lock error response. |

---

## 2. Capture Completion

- [x] Real Postman Desktop Collection Runner executed with `FR02-local`.
- [x] Three distinct native PNGs captured without post-processing.
- [x] Relevant request/test IDs and failed assertions are visible.
- [x] No JWT is visible in any saved final bug screenshot.
- [x] SHA-256 and visual audit recorded in `FR02_SCREENSHOT_MANIFEST.md`.
