# HW06 Confirmed Root-Cause Bug Registry

| Bug ID | Feature | Title | Issue | Visual Evidence |
|---|---|---|---|---|
| BUG-FR02-001 | FR02 | Login response discloses plaintext password | [#1](https://github.com/thangak18/HW06/issues/1) | verified native screenshot |
| BUG-FR02-002 | FR02 | Account remains locked beyond 30 seconds | [#2](https://github.com/thangak18/HW06/issues/2) | verified native screenshot |
| BUG-FR02-003 | FR02 | Correct login rejected after only two failures | [#3](https://github.com/thangak18/HW06/issues/3) | verified native screenshot |
| BUG-FR10-001 | FR10 | Owner can cancel shipping order | [#29](https://github.com/thangak18/HW06/issues/29) | verified native screenshot |
| BUG-FR10-002 | FR10 | Canceled terminal order can become delivered | [#30](https://github.com/thangak18/HW06/issues/30) | verified native screenshot |
| BUG-FR10-003 | FR10 | Normal User mutates order through Admin route | [#31](https://github.com/thangak18/HW06/issues/31) | verified native screenshot |
| BUG-FR14-001 | FR14 | Normal User mutates category data | [#32](https://github.com/thangak18/HW06/issues/32) | PASS (pixel-audited 2026-09-03) |
| BUG-FR14-002 | FR14 | Invalid mandatory category names accepted on create | [#33](https://github.com/thangak18/HW06/issues/33) | PASS (pixel-audited 2026-09-03) |
| BUG-FR14-003 | FR14 | Nonexistent/already-deleted category mutations return false success | [#34](https://github.com/thangak18/HW06/issues/34) | PASS (pixel-audited 2026-09-03) |
| BUG-FR14-004 | FR14 | Empty PUT body corrupts existing name to null | [#36](https://github.com/thangak18/HW06/issues/36) | PASS (pixel-audited 2026-09-03) |

## Accounting

- FR02: 3
- FR10: 3
- FR14: 4
- **Total distinct root-cause bugs: 10**

GitHub Issue #37 is closed as a duplicate manifestation of BUG-FR14-003 / Issue #34 and is not counted as a separate root cause.
