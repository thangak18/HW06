# HW06 — API Testing with AI — Ninh Van Khai — 23127060

| | |
|---|---|
| Ho ten | **Ninh Van Khai** |
| MSSV | **23127060** |
| Lop / Nhom | `<dien lop>` / `<dien nhom>` |
| Repo cong khai | `<dien link — xem ci/CI_CD_REPORT.md muc 5>` |
| SUT | https://github.com/ttbhanh/eshop-sut, commit `85af3ba875c88283615e22cb108f13e2fccaf0e9` |
| Ngay lam | 01/09/2026 |
| Video demo bo sinh (tuy chon) | `<dien link YouTube — kich ban o agent-skill/VIDEO_SCRIPT.md>` |

**Bao cao chinh:** [`report/MAIN_REPORT.md`](report/MAIN_REPORT.md)

---

## 1. Ba API duoc chon

| # | Pool | FR | Chuc nang | Endpoint chinh |
|---|---|---|---|---|
| API-1 | A | FR-03 | Quen mat khau & dat lai mat khau | `POST /api/forgot-password`, `POST /api/reset-password` |
| API-2 | B | FR-08 | Thanh toan (+ FR-09 coupon, FR-10 vong doi don hang) | `POST /api/checkout` |
| API-3 | C | FR-15 | Quan ly san pham (CRUD + tim kiem) | `POST` / `PUT` / `DELETE /api/products` |

**Pool D (Mobile) khong su dung** — de bai muc 5 loai tru vi bai nay nham vao backend API.

---

## 2. Test summary

| Chi so | Gia tri |
|---|---|
| So API kiem thu | **3** |
| Test case do AI sinh | **225** |
| Test case tu bo sung | **18** |
| **Tong test case** | **243** |
| Da thuc thi | **243** (100%) |
| Test case PASS | **84** |
| Test case FAIL | **159** |
| — trong do that bai **co chu dich** (`@bug`) | 91 |
| — trong do that bai **ngoai du kien** (`@contract`) | 68 |
| Tong assertion da chay | **1146** |
| Assertion that bai | **234** |
| So bug bao cao | **34** (12 Critical, 11 High, 9 Medium, 2 Low) |
| So GitHub Issue da mo | `<dien sau khi lam H3>` |

### Phan bo theo nhom ky thuat

| API | Domain (DOM) | State transition (STA) | Security (SEC) | Schema (SCH) | Tong |
|---|---|---|---|---|---|
| API-1 | 36 | 10 | 18 | 6 | 70 |
| API-2 | 43 | 22 | 16 | 6 | 87 |
| API-3 | 53 | 9 | 16 | 8 | 86 |
| **Tong** | **132** | **41** | **50** | **20** | **243** |

### Ket qua audit test case do AI sinh

| API | Tong AI sinh | VALID | INVALID | INCOMPLETE | % VALID |
|---|---|---|---|---|---|
| API-1 | 64 | 22 | 23 | 19 | 34% |
| API-2 | 81 | 40 | 18 | 23 | 49% |
| API-3 | 80 | 21 | 27 | 32 | 26% |
| **Tong** | **225** | **83** | **68** | **74** | **37%** |

> **Toan bo 41 test case nhom bao mat deu INVALID** — khong phai 41 loi doc lap ma la mot loi
> duy nhat nhan ban 41 lan: bang SEC-01..07 duoc dien tu tri nho ve OWASP thay vi doc
> `eshop-sut/README.md` muc 9. Xem [`report/03_audit.md`](report/03_audit.md) muc 4.

### Ket qua thuc thi

| Bo | Case | Assertion | Assertion FAIL | Y nghia |
|---|---|---|---|---|
| Day du (Oracle = SPEC) | 243 | 1146 | 234 | Ket qua kiem thu that su — **phai** co that bai vi SUT co 34 bug |
| Hoi quy (`@contract`) | 84 | 406 | **0** | Moc hoi quy, dung cho lan chay CI all-pass |
| Data-driven | 48 vong lap | 96 | 30 | 4 data file, chay bang `newman -d` |

> Nhieu test FAIL la **co chu dich**: moi ky vong duoc viet theo dac ta chu khong theo hanh vi
> thuc te cua SUT. Neu sua ky vong cho khop hanh vi sai de bo test xanh thi do la nguy tao
> ket qua.

---

## 3. Bug noi bat (12 bug Critical)

| ID | API | Mo ta ngan | GitHub Issue |
|---|---|---|---|
| **A-01** | API-1 | `forgot-password` tra thang ma OTP trong response body | `<link>` |
| **A-07** | API-1 | Mat khau luu plaintext, bi tra ve trong response `login` | `<link>` |
| **B-01** | API-2 | `checkout` tin tuyet doi `total_amount` do client gui | `<link>` |
| **B-01b** | API-2 | `checkout` chap nhan `total_amount` am | `<link>` |
| **B-02** | API-2 | `GET /api/orders/:id` thieu han xac thuc — IDOR | `<link>` |
| **B-03** | API-2 | `admin/orders/:id/status` khong kiem `role` | `<link>` |
| **B-05** | API-2 | Cong thuc coupon `percent` sai dau — so tien giam **am** | `<link>` |
| **B-07** | API-2 | `apply-coupon` khong xac thuc; bo `user_id` la bo qua han muc | `<link>` |
| **C-01** | API-3 | CRUD san pham hoan toan khong xac thuc | `<link>` |
| **C-02** | API-3 | SQL Injection qua `?search=` — lay duoc mat khau admin | `<link>` |
| **C-13** | API-3 | `price = null` lam **sap han backend** (tu choi dich vu) | `<link>` |
| **X-01** | lien API | `PUT /api/users/me` cho user thuong tu nang `role` len `admin` | `<link>` |

Chi tiet 34 bug + bang chung request/response that:
[`bugs/BUG_REPORT.md`](bugs/BUG_REPORT.md).

---

## 4. Cau truc thu muc

```
23127060/
├── README.md                  <- file nay
├── CLAUDE.md                  <- luat lam viec cho Claude Code
├── agent-skill/
│   ├── eshop-api-23127060/    <- goi skill: SKILL.md + references/ + scripts/ (13 script)
│   ├── diagram/               <- DIAGRAM_BRIEF.md (so do do SINH VIEN TU VE)
│   ├── pseudocode/            <- generator.pseudo.md
│   └── VIDEO_SCRIPT.md
├── spec/                      <- spec may doc duoc (dau vao cua bo sinh) + _SCHEMA.md
├── testcases/                 <- CSV (generated / audited / final) + Excel
├── postman/
│   ├── collections/           <- 7 collection (3 day du, 3 hoi quy, 1 data-driven)
│   ├── environments/          <- environment 26 bien
│   ├── data/                  <- 4 data file cho Collection Runner
│   ├── scripts/schemas/       <- 13 JSON Schema
│   └── contract_baseline/     <- danh sach TC_ID cua moc hoi quy
├── newman/                    <- bao cao HTML + JSON (da nen gzip)
├── ci/                        <- workflow, CI_CD_REPORT.md, inject_failing_test.py, evidence/
├── bugs/                      <- BUG_REPORT.md, evidence/ (34 file), ISSUE_TEMPLATES/ (34 file)
├── ai/                        <- AI_log.md, prompts/, interactions/, audit/, critique/
├── report/                    <- MAIN_REPORT.md + 7 bao cao thanh phan
└── git-log/                   <- commit log dang text
```

---

## 5. Cach chay lai toan bo

```bash
# 0) Chuan bi (chay mot lan)
git clone https://github.com/ttbhanh/eshop-sut.git ../../../../eshop-sut
(cd ../../../../eshop-sut/backend && npm install)
npm install -g newman newman-reporter-htmlextra
pip install openpyxl

# 1) Sinh test case — bon vong doc lap, khong dung mot prompt tong
S=agent-skill/eshop-api-23127060/scripts
for n in 1 2 3; do
  python3 $S/gen_testcases.py --spec spec/api-$n.json --only DOM --out testcases/API-${n}_generated.csv
  for c in STA SEC SCH; do
    python3 $S/gen_testcases.py --spec spec/api-$n.json --only $c --out testcases/API-${n}_generated.csv --append
  done
done

# 2) Audit + bo sung
python3 $S/audit_testcases.py --report
python3 $S/extend_testcases.py

# 3) Dung Postman collection
python3 $S/build_collection.py --env-only --out postman/environments/23127060_local.postman_environment.json
for n in 1 2 3; do
  python3 $S/build_collection.py --csv testcases/API-${n}_final.csv --api API-${n} \
    --out postman/collections/23127060_HW06_API-${n}.postman_collection.json
done

# 4) Chay Newman (script tu khoi dong lai SUT de CSDL ve trang thai goc)
bash $S/run_newman.sh all
bash $S/run_datadriven.sh

# 5) Chot moc hoi quy tu ket qua that, roi dung va chay bo hoi quy
python3 $S/derive_contract.py
for n in 1 2 3; do
  python3 $S/build_collection.py --csv testcases/API-${n}_final.csv --api API-${n} \
    --tc-list postman/contract_baseline/API-${n}.txt \
    --out postman/collections/23127060_HW06_API-${n}_contract.postman_collection.json
done
bash $S/run_newman.sh all contract

# 6) Tong hop, thu bang chung, xuat bao cao
python3 $S/summarize_newman.py --dir newman --tc testcases --out report/06_execution.md
python3 $S/verify_header.py --dir newman --sid 23127060 --out ci/evidence/header_evidence.md
python3 $S/capture_bug_evidence.py --base http://localhost:3000 --out bugs/evidence \
  --sut-dir ../../../../eshop-sut/backend
python3 $S/make_bug_report.py
python3 $S/tc_to_excel.py --csv testcases/API-*_final.csv --out testcases/23127060_HW06_testcases.xlsx
python3 $S/ai_log.py build-audit --root . --sid 23127060

# 7) Kiem tra truoc khi nop
python3 $S/validate_submission.py --root . --sid 23127060
```

---

## 6. Bang tu danh gia

| Muc | Yeu cau de bai | Diem toi da | Tu cham | Bang chung |
|---|---|---|---|---|
| API-1 — Generate | >= 35 TC, du 4 nhom ky thuat | 8 | `<>` | 64 TC — `testcases/API-1_final.csv` |
| API-1 — Audit | Gan nhan + ly giai + sua | 7 | `<>` | `report/03_audit.md` |
| API-1 — Extend | >= 5 TC tu viet + ly do AI bo sot | 5 | `<>` | 6 TC — `TC-A1-*-9xx` |
| API-1 — Execute | Postman + Newman + HTML report | 6 | `<>` | `newman/23127060_API-1_*.html` |
| API-1 — Bug report | Markdown + Issues + screenshot | 4 | `<>` | 7 bug — `bugs/BUG_REPORT.md` |
| **API-1 tong** | | **30** | `<>` | |
| API-2 — Generate | | 8 | `<>` | 81 TC |
| API-2 — Audit | | 7 | `<>` | |
| API-2 — Extend | | 5 | `<>` | 6 TC |
| API-2 — Execute | | 6 | `<>` | `newman/23127060_API-2_*.html` |
| API-2 — Bug report | | 4 | `<>` | 13 bug |
| **API-2 tong** | | **30** | `<>` | |
| API-3 — Generate | | 8 | `<>` | 80 TC |
| API-3 — Audit | | 7 | `<>` | |
| API-3 — Extend | | 5 | `<>` | 6 TC |
| API-3 — Execute | | 6 | `<>` | `newman/23127060_API-3_*.html` |
| API-3 — Bug report | | 4 | `<>` | 13 bug |
| **API-3 tong** | | **30** | `<>` | |
| Agent Skill | Bo sinh + so do tu ve + pseudocode | 10 | `<>` | `agent-skill/`, `report/07_*.md` |
| **TONG** | | **100** | `<>` | |

### Deliverable bat buoc (thieu mot muc la 0 diem — de bai muc 17)

| Deliverable | Trang thai | Duong dan |
|---|---|---|
| Bao cao chinh (MD) | ✅ | `report/MAIN_REPORT.md` |
| Bao cao chinh (PDF) | ✅ | `report/MAIN_REPORT.pdf` (10 trang) |
| Link GitHub cong khai | ⬜ HUMAN | xem `ci/CI_CD_REPORT.md` muc 5 |
| Postman collection `.json` | ✅ | `postman/collections/` (7 file) |
| Danh sach Postman feature | ✅ | `report/05_postman_features.md` (23 feature) |
| Newman report HTML | ✅ | `newman/` (10 file) |
| Bao cao CI/CD + 2 lan chay | ⚠️ cau hinh xong, **chua push** | `ci/CI_CD_REPORT.md` |
| Excel test case + sheet Summary | ✅ | `testcases/23127060_HW06_testcases.xlsx` |
| So do bo sinh (**TU VE**) | ⬜ HUMAN | `agent-skill/diagram/DIAGRAM_BRIEF.md` |
| Pseudocode bo sinh | ✅ | `agent-skill/pseudocode/generator.pseudo.md` |
| Bug report (MD + PDF) | ✅ | `bugs/BUG_REPORT.md` / `.pdf` (34 bug, 25 trang) |
| Screenshot GitHub Issues | ⬜ HUMAN | `bugs/ISSUE_TEMPLATES/` da san sang |
| AI Audit Report (MD + PDF) | ✅ | `ai/audit/AI_AUDIT_REPORT.md` / `.pdf` |
| AI Critique (MD + PDF, 200–300 tu) | ✅ **299 tu** | `ai/critique/AI_CRITIQUE.md` / `.pdf` |
| Git commit log | ✅ | `git-log/23127060_git_commit_log.txt` |
| README co bang tu danh gia | ✅ | file nay |

### Trang thai kiem tra tu dong

```
$ python3 agent-skill/eshop-api-23127060/scripts/validate_submission.py --root . --sid 23127060
PASS=62  WARN=2  FAIL=3

CHO SINH VIEN LAM (3 muc, khong tu dong hoa duoc):
  - Diagram bo sinh test        -> H1: ve tay theo agent-skill/diagram/DIAGRAM_BRIEF.md
  - Link GitHub Issues          -> H3: mo Issue tu bugs/ISSUE_TEMPLATES/*.md
  - Screenshot Issues + Console -> H3+H4: chup man hinh, luu vao bugs/screenshots/
```

Ba muc con lai **khong the tu dong hoa**: mot muc bi de bai cam AI lam (so do phai tu ve), hai
muc con lai doi hoi thao tac tren giao dien va quyen truy cap tai khoan GitHub.

---

## 7. Cong cu AI da dung

| Cong cu | Phien ban | Dung vao viec gi |
|---|---|---|
| Claude Code (CLI) | `claude-opus-5` | Sinh test case, audit, dung Postman collection, phan tich ket qua Newman, soan bao cao |

**13 luot tuong tac** duoc ghi **tu dong ngay tai thoi diem xay ra** trong
[`ai/AI_log.md`](ai/AI_log.md), tong hop thanh
[`ai/audit/AI_AUDIT_REPORT.md`](ai/audit/AI_AUDIT_REPORT.md). Prompt goc cua tung buoc:
[`ai/prompts/`](ai/prompts/). Danh gia ca nhan ve AI:
[`ai/critique/AI_CRITIQUE.md`](ai/critique/AI_CRITIQUE.md).

---

## 8. Cam ket lien chinh (de bai muc 11)

- ✅ **Header `X-Student-Id: 23127060` tren moi request** — kiem chung tu dong:
  **823/823 request**, xem `ci/evidence/header_evidence.md`. Anh chup Postman Console:
  `bugs/screenshots/console_header.png` (HUMAN H4).
- ✅ **Newman chay tren `localhost:3000`**, hostname hien ro trong bao cao HTML.
- ⬜ **So do bo sinh do sinh vien TU VE**, khong dung AI sinh anh. Thu muc
  `agent-skill/diagram/` hien **khong chua** file anh / mermaid / graphviz nao (HUMAN H1).
- ✅ **Khong bia so lieu:** moi con so passed/failed sinh tu `newman/*.json.gz` bang
  `summarize_newman.py`; moi request/response trong bug report trich tu `bugs/evidence/`
  do `capture_bug_evidence.py` chay that.
- ✅ **Khong sao chep prompt / bai lam cua thanh vien khac trong nhom.**
