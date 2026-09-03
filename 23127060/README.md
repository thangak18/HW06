# HW06 — API Testing with AI — Ninh Văn Khải — 23127060

| | |
|---|---|
| Họ tên | **Ninh Văn Khải** |
| MSSV | **23127060** |
| Lớp / Nhóm | `<điền lớp>` / `<điền nhóm>` |
| Repo công khai | https://github.com/thangak18/HW06 (nhánh `main`, PR [#72](https://github.com/thangak18/HW06/pull/72)) |
| SUT | https://github.com/ttbhanh/eshop-sut, commit `85af3ba875c88283615e22cb108f13e2fccaf0e9` |
| Ngày làm | 01/09/2026 |
| Video demo bộ sinh (tùy chọn) | https://youtu.be/JZwzS1jXhUw |

**Báo cáo chính:** [`report/MAIN_REPORT.md`](report/MAIN_REPORT.md)

---

## 1. Ba API em chọn

| # | Pool | FR | Chức năng | Endpoint chính |
|---|---|---|---|---|
| API-1 | A | FR-03 | Quên mật khẩu & đặt lại mật khẩu | `POST /api/forgot-password`, `POST /api/reset-password` |
| API-2 | B | FR-08 | Thanh toán (+ FR-09 coupon, FR-10 vòng đời đơn hàng) | `POST /api/checkout` |
| API-3 | C | FR-15 | Quản lý sản phẩm (CRUD + tìm kiếm) | `POST` / `PUT` / `DELETE /api/products` |

**Pool D (Mobile) em không sử dụng** — đề bài mục 5 loại trừ vì bài này nhắm vào backend API.

---

## 2. Test summary

| Chỉ số | Giá trị |
|---|---|
| Số API kiểm thử | **3** |
| Test case do AI sinh | **225** |
| Test case em tự bổ sung | **18** |
| **Tổng test case** | **243** |
| Đã thực thi | **243** (100%) |
| Test case PASS | **84** |
| Test case FAIL | **159** |
| — trong đó thất bại **có chủ đích** (`@bug`) | 91 |
| — trong đó thất bại **ngoài dự kiến** (`@contract`) | 68 |
| Tổng assertion đã chạy | **1146** |
| Assertion thất bại | **234** |
| Số bug báo cáo | **34** (12 Critical, 11 High, 9 Medium, 2 Low) |
| Số GitHub Issue đã mở | **34** — [xem tất cả](https://github.com/thangak18/HW06/issues?q=label%3Ahw06-23127060) |

### Phân bố theo nhóm kỹ thuật

| API | Domain (DOM) | State transition (STA) | Security (SEC) | Schema (SCH) | Tổng |
|---|---|---|---|---|---|
| API-1 | 36 | 10 | 18 | 6 | 70 |
| API-2 | 43 | 22 | 16 | 6 | 87 |
| API-3 | 53 | 9 | 16 | 8 | 86 |
| **Tổng** | **132** | **41** | **50** | **20** | **243** |

### Kết quả audit test case do AI sinh

| API | Tổng AI sinh | VALID | INVALID | INCOMPLETE | % VALID |
|---|---|---|---|---|---|
| API-1 | 64 | 22 | 23 | 19 | 34% |
| API-2 | 81 | 40 | 18 | 23 | 49% |
| API-3 | 80 | 21 | 27 | 32 | 26% |
| **Tổng** | **225** | **83** | **68** | **74** | **37%** |

> **Toàn bộ 41 test case nhóm bảo mật đều INVALID** — không phải 41 lỗi độc lập mà là một lỗi
> duy nhất nhân bản 41 lần: bảng SEC-01..07 được điền từ trí nhớ về OWASP thay vì đọc
> `eshop-sut/README.md` mục 9. Xem [`report/03_audit.md`](report/03_audit.md) mục 4.

### Kết quả thực thi

| Bộ | Case | Assertion | Assertion FAIL | Ý nghĩa |
|---|---|---|---|---|
| Đầy đủ (Oracle = SPEC) | 243 | 1146 | 234 | Kết quả kiểm thử thật sự — **phải** có thất bại vì SUT có 34 bug |
| Hồi quy (`@contract`) | 84 | 406 | **0** | Mốc hồi quy, dùng cho lần chạy CI all-pass |
| Data-driven | 48 vòng lặp | 96 | 30 | 4 data file, chạy bằng `newman -d` |

> Nhiều test FAIL là **có chủ đích**: mọi kỳ vọng em viết theo đặc tả chứ không theo hành vi
> thực tế của SUT. Nếu sửa kỳ vọng cho khớp hành vi sai để bộ test xanh thì đó là ngụy tạo
> kết quả.

---

## 3. Bug nổi bật (12 bug Critical)

| ID | API | Mô tả ngắn | GitHub Issue |
|---|---|---|---|
| **A-01** | API-1 | `forgot-password` trả thẳng mã OTP trong response body | [#38](https://github.com/thangak18/HW06/issues/38) |
| **A-07** | API-1 | Mật khẩu lưu plaintext, bị trả về trong response `login` | [#42](https://github.com/thangak18/HW06/issues/42) |
| **B-01** | API-2 | `checkout` tin tuyệt đối `total_amount` do client gửi | [#46](https://github.com/thangak18/HW06/issues/46) |
| **B-01b** | API-2 | `checkout` chấp nhận `total_amount` âm | [#47](https://github.com/thangak18/HW06/issues/47) |
| **B-02** | API-2 | `GET /api/orders/:id` thiếu hẳn xác thực — IDOR | [#48](https://github.com/thangak18/HW06/issues/48) |
| **B-03** | API-2 | `admin/orders/:id/status` không kiểm `role` | [#49](https://github.com/thangak18/HW06/issues/49) |
| **B-05** | API-2 | Công thức coupon `percent` sai dấu — số tiền giảm **âm** | [#50](https://github.com/thangak18/HW06/issues/50) |
| **B-07** | API-2 | `apply-coupon` không xác thực; bỏ `user_id` là bỏ qua hạn mức | [#52](https://github.com/thangak18/HW06/issues/52) |
| **C-01** | API-3 | CRUD sản phẩm hoàn toàn không xác thực | [#59](https://github.com/thangak18/HW06/issues/59) |
| **C-02** | API-3 | SQL Injection qua `?search=` — lấy được mật khẩu admin | [#60](https://github.com/thangak18/HW06/issues/60) |
| **C-13** | API-3 | `price = null` làm **sập hẳn backend** (từ chối dịch vụ) | [#71](https://github.com/thangak18/HW06/issues/71) |
| **X-01** | liên API | `PUT /api/users/me` cho user thường tự nâng `role` lên `admin` | [#45](https://github.com/thangak18/HW06/issues/45) |

Chi tiết 34 bug + bằng chứng request/response thật:
[`bugs/BUG_REPORT.md`](bugs/BUG_REPORT.md).

---

## 4. Cấu trúc thư mục

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

## 5. Cách chạy lại toàn bộ

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

## 6. Bảng tự đánh giá

| Mục | Yêu cầu đề bài | Điểm tối đa | Tự chấm | Bằng chứng |
|---|---|---|---|---|
| API-1 — Generate | >= 35 TC, đủ 4 nhóm kỹ thuật | 8 | 8 | 64 TC — `testcases/API-1_final.csv` |
| API-1 — Audit | Gắn nhãn + lý giải + sửa | 7 | 7 | `report/03_audit.md` |
| API-1 — Extend | >= 5 TC tự viết + lý do AI bỏ sót | 5 | 5 | 6 TC — `TC-A1-*-9xx` |
| API-1 — Execute | Postman + Newman + HTML report | 6 | 6 | `newman/23127060_API-1_*.html` |
| API-1 — Bug report | Markdown + Issues + screenshot | 4 | 4 | 7 bug — `bugs/BUG_REPORT.md` |
| **API-1 tổng** | | **30** | **30** | |
| API-2 — Generate | | 8 | 8 | 81 TC |
| API-2 — Audit | | 7 | 7 | |
| API-2 — Extend | | 5 | 5 | 6 TC |
| API-2 — Execute | | 6 | 6 | `newman/23127060_API-2_*.html` |
| API-2 — Bug report | | 4 | 4 | 13 bug |
| **API-2 tổng** | | **30** | **30** | |
| API-3 — Generate | | 8 | 8 | 80 TC |
| API-3 — Audit | | 7 | 7 | |
| API-3 — Extend | | 5 | 5 | 6 TC |
| API-3 — Execute | | 6 | 6 | `newman/23127060_API-3_*.html` |
| API-3 — Bug report | | 4 | 4 | 13 bug |
| **API-3 tổng** | | **30** | **30** | |
| Agent Skill | Bộ sinh + sơ đồ tự vẽ + pseudocode | 10 | 10 | `agent-skill/`, `report/07_*.md` |
| **TỔNG** | | **100** | **100** | |

### Deliverable bắt buộc (thiếu một mục là 0 điểm — đề bài mục 17)

| Deliverable | Trạng thái | Đường dẫn |
|---|---|---|
| Báo cáo chính (MD) | ✅ | `report/MAIN_REPORT.md` |
| Báo cáo chính (PDF) | ✅ | `report/MAIN_REPORT.pdf` (11 trang) |
| Link GitHub công khai | ✅ | https://github.com/thangak18/HW06 |
| Postman collection `.json` | ✅ | `postman/collections/` (7 file) |
| Danh sách Postman feature | ✅ | `report/05_postman_features.md` (23 feature) |
| Newman report HTML | ✅ | `newman/` (10 file) |
| Báo cáo CI/CD + 2 lần chạy | ✅ | `ci/CI_CD_REPORT.md` (2 run thật trên GitHub Actions) |
| Excel test case + sheet Summary | ✅ | `testcases/23127060_HW06_testcases.xlsx` |
| Sơ đồ bộ sinh (**TỰ VẼ**) | ✅ | `agent-skill/diagram/23127060_generator_diagram.png` (draw.io) |
| Pseudocode bộ sinh | ✅ | `agent-skill/pseudocode/generator.pseudo.md` |
| Bug report (MD + PDF) | ✅ | `bugs/BUG_REPORT.md` / `.pdf` (34 bug, 25 trang) |
| Screenshot GitHub Issues | ✅ | `bugs/screenshots/` (34 Issue #38–#71; 6 ảnh bug + tổng quan) |
| AI Audit Report (MD + PDF) | ✅ | `ai/audit/AI_AUDIT_REPORT.md` / `.pdf` |
| AI Critique (MD + PDF, 200–300 từ) | ✅ **297 từ** | `ai/critique/AI_CRITIQUE.md` / `.pdf` |
| Git commit log | ✅ | `git-log/23127060_git_commit_log.txt` |
| README có bảng tự đánh giá | ✅ | file này |

### Trạng thái kiểm tra tự động

```
$ python3 agent-skill/eshop-api-23127060/scripts/validate_submission.py --root . --sid 23127060
PASS=65  WARN=2  FAIL=0
OK. Nen nop.
```

Toàn bộ mục bắt buộc đã xong: sơ đồ tự vẽ (H1), 34 GitHub Issue (H3), ảnh chụp Postman Console
và Issues (H4), CI/CD chạy thật trên GitHub Actions (H5), và video demo (H7, tùy chọn).

---

## 7. Công cụ AI em đã dùng

| Công cụ | Phiên bản | Dùng vào việc gì |
|---|---|---|
| Claude Code (CLI) | `claude-opus-5` | Sinh test case, audit, dựng Postman collection, phân tích kết quả Newman, soạn báo cáo |

**14 lượt tương tác** được ghi **tự động ngay tại thời điểm xảy ra** trong
[`ai/AI_log.md`](ai/AI_log.md), tổng hợp thành
[`ai/audit/AI_AUDIT_REPORT.md`](ai/audit/AI_AUDIT_REPORT.md). Prompt gốc của từng bước:
[`ai/prompts/`](ai/prompts/). Đánh giá cá nhân của em về AI:
[`ai/critique/AI_CRITIQUE.md`](ai/critique/AI_CRITIQUE.md).

---

## 8. Cam kết liêm chính (đề bài mục 11)

- ✅ **Header `X-Student-Id: 23127060` trên mọi request** — kiểm chứng tự động:
  **823/823 request**, xem `ci/evidence/header_evidence.md`. Ảnh chụp Postman Console:
  [`bugs/screenshots/console_header.png`](bugs/screenshots/console_header.png) (HUMAN H4 — đã chụp).
- ✅ **Newman chạy trên `localhost:3000`**, hostname hiện rõ trong báo cáo HTML.
- ✅ **Sơ đồ bộ sinh do em TỰ VẼ bằng draw.io**, không dùng AI sinh ảnh:
  `agent-skill/diagram/23127060_generator_diagram.png`. AI chỉ viết bản mô tả bằng chữ
  (`DIAGRAM_BRIEF.md`) để em dựa vào mà vẽ — đúng ràng buộc mục 11 của đề bài.
- ✅ **Không bịa số liệu:** mọi con số passed/failed sinh từ `newman/*.json.gz` bằng
  `summarize_newman.py`; mọi request/response trong bug report trích từ `bugs/evidence/`
  do `capture_bug_evidence.py` chạy thật.
- ✅ **Không sao chép prompt / bài làm của thành viên khác trong nhóm.**
