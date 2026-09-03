# FR-02 Bug Screenshot Authenticity Manifest

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`
- **Verification Date/Time:** 2026-09-02 12:25:22+07:00

---

## 1. Master Screenshot Authenticity Registry

| Bug ID | Defect Title | Screenshot File | Capture Source | Size | SHA-256 | JWT Visible? | Verified Status |
|:---:|---|---|---|---:|---|:---:|:---:|
| **`BUG-FR02-001`** | Sensitive Password Exposure in Login Response | [`BUG-FR02-001-login-password-exposure.png`](screenshots/FR02/BUG-FR02-001-login-password-exposure.png) | Real Postman Desktop Collection Runner via native Computer Use | 192,550 bytes | `57b3c3d8af3d5194fe4c5abce34519d2914fea9789059d159bd7416c4c926c9a` | **NO** | **PASS** |
| **`BUG-FR02-002`** | Account Remains Locked Beyond 30s Duration | [`BUG-FR02-002-lock-after-30s.png`](screenshots/FR02/BUG-FR02-002-lock-after-30s.png) | Real Postman Desktop Collection Runner via native Computer Use | 173,025 bytes | `f2cb12236b277a0a718ba21bdbfdc9747eebfa290cd34ad01069cddf2dc95ba0` | **NO** | **PASS** |
| **`BUG-FR02-003`** | Correct Login Rejected After N=2 Failures | [`BUG-FR02-003-correct-login-at-n2.png`](screenshots/FR02/BUG-FR02-003-correct-login-at-n2.png) | Real Postman Desktop Collection Runner via native Computer Use | 173,191 bytes | `a166792be577e1d9765645f9e12a8ae8d216f2cb7ac540dedf31becf73049840` | **NO** | **PASS** |

---

## 2. Integrity & Non-Fabrication Certification
1. All three final bug screenshots were captured directly from a genuine Postman Desktop Collection Runner execution against `http://localhost:3000` on 2026-09-02.
2. Canonical counting remains based on immutable Newman Run03; the native run was performed only to obtain attributable visual evidence.
3. No DOM injection, synthetic rendering, image composition, image editing, or generated imagery was used.
4. A live response-detail view that displayed a JWT was deliberately not retained. The saved PNGs expose no JWT.
5. The three final PNGs are non-empty, visually inspected, and have distinct SHA-256 hashes.
