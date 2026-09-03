# FR02 Native Postman Bug Screenshot Audit

- **Capture time:** 2026-09-02 12:22-12:25 +0700
- **Application:** Postman Desktop 11.89.0
- **Collection:** `FR02_Login_Account_Lockout`
- **Environment:** `FR02-local`
- **Source:** genuine Collection Runner execution against `http://localhost:3000`
- **Capture mechanism:** Computer Use accessibility/native UI plus exact screenshot-byte copy; no image editing

| Bug | Real Postman Runner | Correct Test Visible | Organic Failed Assertion | Actual HTTP Result | JWT Hidden | SHA-256 | Status |
|---|:---:|:---:|:---:|:---:|:---:|---|:---:|
| `BUG-FR02-001` | YES | `FR02-AI-028` | YES | `200` | YES | `57b3c3d8af3d5194fe4c5abce34519d2914fea9789059d159bd7416c4c926c9a` | PASS |
| `BUG-FR02-002` | YES | `FR02-AI-021` | YES | `403` after T=32s scenario | YES | `f2cb12236b277a0a718ba21bdbfdc9747eebfa290cd34ad01069cddf2dc95ba0` | PASS |
| `BUG-FR02-003` | YES | `FR02-HUM-003` | YES | `403` on valid login after two failures | YES | `a166792be577e1d9765645f9e12a8ae8d216f2cb7ac540dedf31becf73049840` | PASS |

## Authenticity Controls

- `Runtime.evaluate`: NO
- DOM mutation (`innerHTML`, `innerText`, `textContent`): NO
- Synthetic Runner rendering: NO
- Newman/HTML used to populate the screenshots: NO
- Image generation or compositing: NO
- Real Postman Desktop Runner executed: YES
- Native accessibility/UI interaction: YES
- Screenshot bytes altered after capture: NO

The immutable accepted execution accounting remains `FR02-run-03.json` (56 requests, 71 assertions, 67 passed, 4 failed). The 2026-09-02 desktop run exists only as visual evidence and is not substituted for the canonical Newman artifact.
