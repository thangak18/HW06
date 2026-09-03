# FR10 Defect Confirmation Report

## Scope

- Target: `http://localhost:3000`
- Student header: `X-Student-Id: 23127259`
- Canonical formal execution: disclosure-controlled Run04
- Targeted strict evidence: immutable `FR10-bug-evidence.*`
- Visual evidence: genuine Postman Desktop strict Runner screenshots

## Confirmed Root Causes

| Bug | Fresh API-visible Preconditions | Candidate Action | Actual Result | Persistence Verification | Formal IDs | Issue |
|---|---|---|---|---|---|---|
| `BUG-FR10-001` | Owner order advanced to `shipping` | Owner `PUT /api/orders/:id/cancel` | HTTP 200; cancellation accepted | Authorized GET observes `canceled`, not `shipping` | `FR10-AI-016`, `FR10-HUM-003` | [#29](https://github.com/thangak18/HW06/issues/29) |
| `BUG-FR10-002` | Order established as terminal `canceled` | Admin `PUT /api/admin/orders/:id/status` with `delivered` | HTTP 200; transition accepted | Authorized GET observes `delivered`, not `canceled` | `FR10-AI-024` | [#30](https://github.com/thangak18/HW06/issues/30) |
| `BUG-FR10-003` | Fresh `pending`/`confirmed` owner orders; caller has `role=user` | User token calls Admin status endpoint | HTTP 200; mutations accepted | Authorized GET observes `confirmed`, `canceled`, or `shipping` | `FR10-AI-030..032` | [#31](https://github.com/thangak18/HW06/issues/31) |

All persistence claims mean **API-visible persisted state observed through authorized GET**. No direct database inspection is claimed.

## Canonical and Strict Evidence

| Evidence | Requests | Assertions | Passed | Failed | Harness Errors | Exit |
|---|---:|---:|---:|---:|---:|---:|
| Historical Run03 (immutable; AI-006/007 labels swapped) | 176 | 176 | 164 | 12 | 0 | 1 |
| Corrected Run04 (canonical replacement) | 176 | 176 | 164 | 12 | 0 | 1 |
| Strict defect evidence | 19 | 19 | 11 | 8 | 0 | 1 |

### Immutable Strict Hashes

| Artifact | SHA-256 |
|---|---|
| `FR10-bug-evidence-cli.txt` | `c85457ac825ded6a46d839140c511f88623bc0947d3bfe9f387b4f7222e1ae2d` |
| `FR10-bug-evidence.json` | `25bf0214768921d1d902093e867bcacf8504f1b0e13252769b593b5c7ec9c1d2` |
| `FR10-bug-evidence.html` | `203f06097f47fce9abcc5df77fe26933f79a159367114670c25f734f34624aa1` |

## Triage Decisions

- SEC-02 401-vs-403 candidate: **DROPPED**. Level-1 requires rejection of invalid JWT, not exact 401.
- `FR10-HUM-004`: **EXPLORATORY OBSERVATION** for same-state transition behavior.
- `FR10-HUM-005`: **EXPLORATORY OBSERVATION** for `text/plain`/HTTP 500 robustness.
- No duplicate GitHub Issues were created.

## Visual Evidence

| Bug | Screenshot | SHA-256 |
|---|---|---|
| `BUG-FR10-001` | `bugs/BUG-FR10-001-postman-runner.png` | `139d7c19c0b935392f27006c3e4a045525e3f1b1b87fa6040322fe9154099420` |
| `BUG-FR10-002` | `bugs/BUG-FR10-002-postman-runner.png` | `919825d75d8d1117bd1076457f11d1a384d652b8263143b955018b2979271180` |
| `BUG-FR10-003` | `bugs/BUG-FR10-003-postman-runner.png` | `80b4a8251bd0c583e82e6ca7d835607ae0f260e52478369fbf7f6be5269a8625` |

All final images show real Postman Desktop Runner output and expose no JWT. Historical synthetic images remain quarantined under `historical-invalid/` and are excluded from final evidence.
