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

## 1. Required Bug Screenshots for Confirmed Issues

| Bug ID | Title | Target File Path | What the Student Must Capture |
|---|---|---|---|
| **`BUG-FR02-001`** | Plaintext Password Exposure | `23127259/bugs/screenshots/BUG-FR02-001_plaintext_password.png` | Postman response pane showing `POST /api/login` with HTTP `200 OK` and `"password": "..."` visible under `user`. |
| **`BUG-FR02-002`** | Lockout Does Not Expire After 30s | `23127259/bugs/screenshots/BUG-FR02-002_lockout_no_expire.png` | Postman response pane showing `POST /api/login` with valid password returning HTTP `403 Forbidden` after waiting $>30$ seconds. |
| **`BUG-FR02-003`** | Premature Lockout at N=2 Boundary | `23127259/bugs/screenshots/BUG-FR02-003_premature_lockout_n2.png` | Postman response pane showing HTTP `403 Forbidden` on valid password login attempt following 2 failed attempts. |

---

## 2. Step-by-Step Reproduction Guide for Student Capture

### Capturing BUG-FR02-001:
1. Open Postman, navigate to request `01 – Positive Authentication / FR02-AI-001 – Valid User Login`.
2. Click **Send**.
3. Capture a screenshot of the response body showing `"password": "..."` inside the `user` JSON object.

### Capturing BUG-FR02-002:
1. In Postman, open `03 – Lockout Boundary / FR02-AI-014 – Lockout Threshold Boundary N=3` and send 3 wrong attempts until HTTP 403 is returned.
2. Wait 35 seconds.
3. Open `FR02-AI-021 – Post-Expiration Lockout Timing Boundary T=32s` and send valid credentials.
4. Capture a screenshot showing HTTP 403 Forbidden response.

### Capturing BUG-FR02-003:
1. In Postman, open `06 – Human Extensions / FR02-HUM-003 – Consecutive Failure Reset at N=2 Pre-Lockout Boundary`.
2. Click **Send** (the pre-request script executes 2 failed logins, then main request sends valid password).
3. Capture a screenshot showing HTTP 403 Forbidden on the valid login attempt.
