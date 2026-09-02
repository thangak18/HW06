# FR10 Native Postman Runner Screenshot Audit

## Final Verdict

**PASS - AUTHENTIC NATIVE POSTMAN EVIDENCE**

The final PNGs were captured from a genuine completed `FR10_Defect_Evidence_Strict` run in Postman Desktop 11.89.0, environment `FR10-local`, with 19 tests, 11 passed, 8 failed, and 0 errors. Native Computer Use/accessibility interaction and exact screenshot-byte copies were used. No screenshot was generated, composited, annotated, cropped, or altered.

## Final Inventory

| Bug | Real Runner Visible | Correct Request/Oracle Visible | Actual Failure Visible | JWT Hidden | Size | SHA-256 | Status |
|---|:---:|:---:|:---:|:---:|---:|---|:---:|
| `BUG-FR10-001` | YES | Owner shipping cancellation; HTTP 200 vs expected 4xx | YES | YES | 924,864 | `139d7c19c0b935392f27006c3e4a045525e3f1b1b87fa6040322fe9154099420` | PASS |
| `BUG-FR10-002` | YES | Canceled -> delivered; HTTP 200 and persisted delivered | YES | YES | 809,055 | `919825d75d8d1117bd1076457f11d1a384d652b8263143b955018b2979271180` | PASS |
| `BUG-FR10-003` | YES | `role=user` Admin-route mutation selected; HTTP 200 | YES | YES | 169,378 | `80b4a8251bd0c583e82e6ca7d835607ae0f260e52478369fbf7f6be5269a8625` | PASS |

The first interrupted native captures left FR10-002 and FR10-003 as identical bytes. The valid FR10-002 image was retained; only FR10-003 was recaptured in a distinct focused native view. All three final hashes are now distinct.

## Authenticity Controls

- `Runtime.evaluate`: NO
- DOM mutation (`innerHTML`, `innerText`, `textContent`): NO
- Synthetic Runner rows: NO
- Newman JSON/HTML rendered as Postman UI: NO
- Image generation/composition/editing: NO
- Real Postman Desktop Runner execution: YES
- Native UI/accessibility control: YES
- Visible resolved JWT: NO

## Historical Invalid Evidence

- `historical-invalid/int053/`: synthetic Postman-looking content produced through DOM injection; excluded.
- `historical-invalid/int054/`: later synthetic Runner rendering; excluded.
- Historical invalid files remain quarantined only to preserve the audit trail and are never referenced as final evidence.

## Technical Evidence Relationship

- Canonical replacement execution: Run04, 176 requests and 176 assertions.
- Targeted strict defect execution: immutable strict JSON, 19 requests, 19 assertions, 8 expected defect failures, 0 harness failures.
- Visual execution: native Postman strict Runner, 19 tests, 11 passed, 8 failed, 0 errors.

The strict Newman artifacts establish machine-readable defect evidence; these screenshots provide independently attributable visual evidence from the real Postman application.
