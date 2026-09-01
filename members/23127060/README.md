# HW06 — API Testing with AI — 23127060 — Ninh Van Khai

> Thay cac phan `<...>` bang so lieu that sau khi chay xong. File nay la deliverable bat buoc
> (de bai muc 14: README voi bang tu danh gia + test summary).

| | |
|---|---|
| Ho ten | Ninh Van Khai |
| MSSV | 23127060 |
| Lop / Nhom | `<lop>` / `<nhom>` |
| Repo cong khai | `<https://github.com/...>` |
| SUT | https://github.com/ttbhanh/eshop-sut (commit `<hash>`) |
| Ngay nop | `<dd/mm/2026>` |
| Video demo (neu co) | `<link YouTube>` |

---

## 1. Ba API duoc chon

| # | Pool | FR | API | Endpoint chinh |
|---|------|----|-----|----------------|
| API-1 | A | FR-03 | Quen mat khau & Dat lai mat khau | `POST /api/forgot-password`, `POST /api/reset-password` |
| API-2 | B | FR-08 | Thanh toan | `POST /api/checkout` |
| API-3 | C | FR-15 | Quan ly san pham | `POST/PUT/DELETE /api/products` |

Phan cong ca nhom (khong trung nhau): xem `../../docs/team-api-allocation.md`.

---

## 2. Test summary

| API | TC do AI sinh | TC tu bo sung | Tong | Da chay | Pass | Fail | Bug tim duoc |
|-----|---------------|---------------|------|---------|------|------|--------------|
| API-1 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |
| API-2 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |
| API-3 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |
| **Tong** | | | | | | | |

Phan bo theo loai:

| API | Domain (DOM) | State transition (STA) | Security (SEC) | Schema (SCH) |
|-----|--------------|------------------------|----------------|--------------|
| API-1 | `<>` | `<>` | `<>` | `<>` |
| API-2 | `<>` | `<>` | `<>` | `<>` |
| API-3 | `<>` | `<>` | `<>` | `<>` |

Ket qua audit test case do AI sinh:

| API | VALID | INVALID | INCOMPLETE |
|-----|-------|---------|------------|
| API-1 | `<>` | `<>` | `<>` |
| API-2 | `<>` | `<>` | `<>` |
| API-3 | `<>` | `<>` | `<>` |

> Ghi chu: nhieu test FAIL la **co y** — chung phoi bay bug that cua SUT (gan tag `@bug`).
> Cac test `@contract` la phan hop dong API dung, dung cho CI/CD va phai PASS 100%.

---

## 3. Bug noi bat

| ID | API | Muc do | Mo ta ngan | GitHub Issue |
|----|-----|--------|------------|--------------|
| A-01 | API-1 | Critical | `resetToken` bi tra thang trong response body | `<link>` |
| A-02 | API-1 | High | Token reset chi 4 chu so — brute-force duoc | `<link>` |
| B-01 | API-2 | Critical | Checkout tin `total_amount` do client gui | `<link>` |
| B-02 | API-2 | Critical | `GET /api/orders/:id` khong xac thuc — IDOR | `<link>` |
| C-01 | API-3 | Critical | CRUD san pham hoan toan khong xac thuc | `<link>` |
| C-02 | API-3 | Critical | SQL Injection qua `?search=` | `<link>` |

Chi tiet day du: `bugs/BUG_REPORT.md`.

---

## 4. Cau truc thu muc

```
23127060/
├── README.md                  <- file nay
├── CLAUDE.md                  <- luat lam viec cho Claude Code
├── agent-skill/
│   ├── eshop-api-23127060/    <- goi skill (SKILL.md + references + scripts)
│   ├── diagram/               <- so do bo sinh test (TU VE)
│   └── pseudocode/
├── ai/                       <- AI_log.md, interactions/, audit/, critique/, prompts/
├── spec/                     <- spec may doc duoc, dau vao cua bo sinh test
├── testcases/                <- CSV + Excel test case
├── postman/                  <- collections, environments, data, scripts
├── newman/                   <- bao cao HTML/JSON
├── ci/                       <- workflow + CI_CD_REPORT.md + evidence/
├── bugs/                     <- BUG_REPORT.md + screenshots/
├── report/                   <- MAIN_REPORT.md (+ PDF)
└── git-log/                  <- commit log dang text
```

---

## 5. Cach chay lai

```bash
# 1. Khoi dong SUT
(cd ../../../eshop-sut/backend && npm install && nohup node server.js > /tmp/sut.log 2>&1 &)

# 2. Seed du lieu
node agent-skill/eshop-api-23127060/scripts/seed_sut.js reset

# 3. Chay test
bash agent-skill/eshop-api-23127060/scripts/run_newman.sh API-1 full
bash agent-skill/eshop-api-23127060/scripts/run_newman.sh API-2 full
bash agent-skill/eshop-api-23127060/scripts/run_newman.sh API-3 full

# 4. Tong hop
python3 agent-skill/eshop-api-23127060/scripts/summarize_newman.py --dir newman --out report/06_execution.md

# 5. Kiem tra truoc khi nop
python3 agent-skill/eshop-api-23127060/scripts/validate_submission.py --root . --sid 23127060
```

---

## 6. Bang tu danh gia (self-assessment)

| Muc | Yeu cau de bai | Diem toi da | Tu cham | Bang chung |
|-----|----------------|-------------|---------|------------|
| API-1 — Generate | >= 35 TC, du 4 nhom ky thuat | 8 | `<>` | `testcases/API-1_final.csv` |
| API-1 — Audit | Gan nhan VALID/INVALID/INCOMPLETE + ly giai | 7 | `<>` | `report/03_audit_API-1.md` |
| API-1 — Extend | >= 5 TC tu viet + ly do AI bo sot | 5 | `<>` | `testcases/API-1_final.csv` (TC-A1-*-9xx) |
| API-1 — Execute | Postman + Newman + HTML report | 6 | `<>` | `newman/23127060_API-1_*.html` |
| API-1 — Bug report | Markdown + GitHub Issues + screenshot | 4 | `<>` | `bugs/BUG_REPORT.md` |
| **API-1 tong** | | **30** | `<>` | |
| API-2 — Generate | | 8 | `<>` | `testcases/API-2_final.csv` |
| API-2 — Audit | | 7 | `<>` | `report/03_audit_API-2.md` |
| API-2 — Extend | | 5 | `<>` | |
| API-2 — Execute | | 6 | `<>` | `newman/23127060_API-2_*.html` |
| API-2 — Bug report | | 4 | `<>` | |
| **API-2 tong** | | **30** | `<>` | |
| API-3 — Generate | | 8 | `<>` | `testcases/API-3_final.csv` |
| API-3 — Audit | | 7 | `<>` | `report/03_audit_API-3.md` |
| API-3 — Extend | | 5 | `<>` | |
| API-3 — Execute | | 6 | `<>` | `newman/23127060_API-3_*.html` |
| API-3 — Bug report | | 4 | `<>` | |
| **API-3 tong** | | **30** | `<>` | |
| Agent Skill | Bo sinh test + so do tu ve + pseudocode | 10 | `<>` | `agent-skill/` |
| **TONG** | | **100** | `<>` | |

Deliverable phu (khong tinh diem rieng nhung thieu la 0 diem — muc 17):

| Deliverable | Trang thai | Duong dan |
|-------------|-----------|-----------|
| Bao cao chinh (MD + PDF) | `<>` | `report/MAIN_REPORT.md` / `.pdf` |
| Postman collection JSON | `<>` | `postman/collections/` |
| Danh sach Postman features | `<>` | `report/05_postman_features.md` |
| Newman HTML report | `<>` | `newman/` |
| Bao cao CI/CD + 2 run | `<>` | `ci/CI_CD_REPORT.md`, `ci/evidence/` |
| Excel test case | `<>` | `testcases/23127060_HW06_testcases.xlsx` |
| So do + pseudocode bo sinh | `<>` | `agent-skill/diagram/`, `agent-skill/pseudocode/` |
| OpenAPI spec (tuy chon) | `<>` | `spec/openapi.yaml` |
| Bug report + Issues | `<>` | `bugs/` |
| AI Critique (200–300 tu, MD+PDF) | `<>` | `ai/critique/` |
| AI Audit Report (MD+PDF) | `<>` | `ai/audit/` |
| Git commit log | `<>` | `git-log/` |

---

## 7. Cong cu AI da dung

| Cong cu | Phien ban | Dung vao viec gi |
|---------|-----------|------------------|
| Claude Code (CLI) | `claude-sonnet-4.5` | Sinh test case, dung Postman collection, viet nhap bao cao |
| `<cong cu khac>` | | |

Toan bo `<N>` luot tuong tac duoc ghi trong `ai/AI_log.md` va tong hop thanh
`ai/audit/AI_AUDIT_REPORT.md`. Danh gia ca nhan ve AI: `ai/critique/AI_CRITIQUE.md`.

---

## 8. Cam ket lien chinh (muc 11 de bai)

- [ ] Moi request deu gui header `X-Student-Id: 23127060` (chen bang pre-request script cap collection), co screenshot Postman Console tai `bugs/screenshots/console_header.png`.
- [ ] Newman chay tren `localhost` / `127.0.0.1`, hostname hien ro trong HTML report.
- [ ] So do bo sinh test do toi **tu ve tay**, khong dung AI sinh anh; anh chup qua trinh ve tai `agent-skill/diagram/`.
- [ ] Khong sao chep prompt / bai lam cua thanh vien khac trong nhom.
