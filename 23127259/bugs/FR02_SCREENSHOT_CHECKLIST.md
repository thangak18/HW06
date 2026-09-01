# FR-02 Bug Screenshot & Verification Checklist

- **Feature ID:** FR-02 – Login and Account Lockout (Pool A)
- **Student Name:** Nguyễn Tấn Thắng (23127259)
- **Repository:** `thangak18/HW06`
- **Branch:** `thang/hw06-implementation`

> This checklist prepares the exact visual evidence requirements for Phase 1D.2 (Bug Confirmation, Evidence, and GitHub Issue Filing).

---

## 1. Required Bug Screenshots

| Bug ID | Title | Required Screenshot Name | Screenshot Description / Viewport |
|---|---|---|---|
| **`BUG-FR02-001`** | Plaintext Password Exposure | `BUG-FR02-001_plaintext_password.png` | Postman response window showing HTTP 200 and `"password": "User1234!"` in response JSON body |
| **`BUG-FR02-002`** | Permanent Account Lockout | `BUG-FR02-002_permanent_lockout.png` | Postman response window showing HTTP 403 Forbidden after 35s wait with timestamp |
| **`BUG-FR02-003`** | Premature Lockout on Valid Login at N=2 | `BUG-FR02-003_premature_lockout_n2.png` | Postman request with valid password returning HTTP 403 after 2 prior failures |
| **`BUG-FR02-004`** | HTTP 500 Crash on Form Encoding | `BUG-FR02-004_form_encoding_500_crash.png` | Postman response window showing HTTP 500 Internal Server Error on `x-www-form-urlencoded` |

---

## 2. Reproduction Command Snippets

### Repro BUG-FR02-001 (Password Leak):
```bash
curl -s -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@eshop.com", "password": "User1234!"}' | jq .
```

### Repro BUG-FR02-002 (Permanent Lockout):
```bash
python3 /Volumes/Thang/HW06/HW06/23127259/bugs/repro_bug002.py
```

### Repro BUG-FR02-003 (Premature Lockout at N=2):
```bash
python3 /Volumes/Thang/HW06/HW06/23127259/bugs/repro_bug003.py
```

### Repro BUG-FR02-004 (Form URL-Encoded 500 Crash):
```bash
curl -s -w "\nHTTP %{http_code}\n" -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=user%40eshop.com&password=User1234!"
```
