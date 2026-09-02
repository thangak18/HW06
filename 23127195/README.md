# HW06 — API Testing · Sinh viên 23127195

| | |
|---|---|
| **Bài tập** | HW06 — API Testing (HW06-AI) |
| **SUT** | EShop — [`ttbhanh/eshop-sut`](https://github.com/ttbhanh/eshop-sut) · `http://localhost:3000` |
| **Công cụ** | Postman 12.26.1 · Newman 6.2.2 · `newman-reporter-htmlextra` · GitHub Actions |
| **AI tool** | Claude Opus 5 (`claude-opus-5`) — khai báo tại [`ai/AI_AUDIT_REPORT.md`](./ai/AI_AUDIT_REPORT.md) |
| **Ngày thực hiện** | 2026-09-01 |

📄 **Báo cáo chính:** [`docs/00_MAIN_REPORT.md`](./docs/00_MAIN_REPORT.md)

---

## Báo cáo tổng hợp kiểm thử

| Chỉ số | Giá trị |
|---|---|
| **Số API kiểm thử** | **3** (FR-04 · FR-09 · FR-16 — mỗi API một Pool) |
| **Test case do AI sinh** | **110** |
| **Test case sinh viên tự thêm** | **34** |
| **Tổng số test case** | **144** |
| **Đã thi hành** | **144** (241 request · 746 assertion) |
| **PASS** | **92** |
| **FAIL** | **52** |
| **Số lỗi tìm được** | **24** (4 Critical · 7 High · 8 Medium · 5 Low) |

### Chi tiết theo API

| API | Pool | FR | Endpoint | Test case | AI | SV | PASS | FAIL | Bug |
|---|---|---|---|---|---|---|---|---|---|
| API-1 | A | FR-04 — Hồ sơ cá nhân | `GET/PUT /api/users/me` | 45 | 35 | 10 | 25 | 20 | 5 |
| API-2 | B | FR-09 — Mã giảm giá | `POST /api/apply-coupon`<br>`POST /api/coupon-usage` | 50 | 39 | 11 | 38 | 12 | 8 |
| API-3 | C | FR-16 — Import sản phẩm | `POST /api/admin/import-products` | 49 | 36 | 13 | 29 | 20 | 11 |
| | | | **Tổng** | **144** | **110** | **34** | **92** | **52** | **24** |

### Phân bố theo kỹ thuật kiểm thử

| API | Domain partition | State transition | Security | Schema |
|---|---|---|---|---|
| API-1 | 23 | 6 | 12 | 4 |
| API-2 | 30 | 6 | 9 | 5 |
| API-3 | 31 | 6 | 7 | 5 |
| **Tổng** | **84** | **18** | **28** | **14** |

### Kết quả audit test case do AI sinh

| API | VALID | INCOMPLETE (đã hiệu chỉnh) | INVALID |
|---|---|---|---|
| API-1 | 31 | 4 | 0 |
| API-2 | 36 | 3 | 0 |
| API-3 | 34 | 2 | 0 |
| **Tổng** | **101** | **9** | **0** |

### Bốn lỗi nghiêm trọng nhất

| Mã | Vi phạm | Mô tả |
|---|---|---|
| **BUG-A1-01** 🔴 | SEC-06 | `PUT /api/users/me` nhận trường `role` từ client → **leo quyền lên admin bằng một request** |
| **BUG-A2-01** 🔴 | FR-09 C4, SEC-02 | `apply-coupon` **không yêu cầu đăng nhập** — một trong 5 điều kiện bắt buộc không được cài đặt |
| **BUG-A2-02** 🔴 | FR-09 | Công thức `percent` sai → **giảm giá âm**, khách trả gấp 10 lần giá gốc |
| **BUG-A3-01** 🔴 | SEC-03, FR-12 | **Người dùng thường import được hàng lên cửa hàng** với giá và ảnh do họ kiểm soát |

---

## Bảng tự đánh giá

| No. | Tiêu chí | Điểm tối đa | Tự đánh giá | Căn cứ |
|---|---|---|---|---|
| 1 | **API 1** — trọn quy trình (sinh + audit + mở rộng + thi hành + báo lỗi) | 30 | **28** | 45 test case (35 AI + 10 SV) · 25 PASS / 20 FAIL · 5 lỗi gồm 1 Critical · audit đủ nhãn kèm lý do · thi hành thật |
| 2 | **API 2** — trọn quy trình | 30 | **28** | 50 test case (39 AI + 11 SV) · bảng quyết định 5 điều kiện C1–C5 đầy đủ · oracle số học · 8 lỗi gồm 2 Critical |
| 3 | **API 3** — trọn quy trình | 30 | **28** | 49 test case (36 AI + 13 SV) · kiểm chứng tính nguyên tử của giao dịch · 11 lỗi gồm 1 Critical |
| 4 | **Agent Skill** — bộ sinh test case bằng AI | 10 | **9** | Thiết kế 6 giai đoạn + pseudocode + **cài đặt tham chiếu chạy được** (`generator.py --demo` sinh 44 case, 0 lỗi kiểm tra) + **sơ đồ tự vẽ đã xong**. Trừ điểm vì **video chưa quay** |
| | **Tổng** | **100** | **93** | |

> ⚠ **Điểm tự đánh giá ở trên giả định các hạng mục thủ công đã hoàn tất.**
> Sơ đồ, GitHub Issues, **ảnh chụp Postman Console** (bằng chứng §11) và PDF nay **đã xong**.
> Còn thiếu: ảnh chụp lỗi đính vào issue, lần chạy CI đỏ, và video. Nếu nộp khi chưa có,
> hãy **hạ điểm tương ứng** trước khi đặt tên file nộp. Xem mục *Việc còn phải tự làm* bên dưới.
>
> **Tên file nộp:** `23127195_HW06_AI_API_093.zip` *(đổi `093` theo điểm tự đánh giá cuối cùng)*

---

## Cách chạy lại toàn bộ

```bash
# 1. Lấy SUT về (một lần)
git clone https://github.com/ttbhanh/eshop-sut.git ../../.sut/eshop-sut
(cd ../../.sut/eshop-sut/backend && npm install)

# 2. Cài Newman
npm install

# 3. Sinh collection từ nguồn test case
python postman/scripts/build_collections.py
python postman/scripts/build_datadriven.py
python postman/scripts/build_baseline.py

# 4. Chạy (script tự restart SUT để mỗi lần chạy đều từ cùng trạng thái dữ liệu)
bash scripts/run_newman.sh                 # cả 3 API
bash scripts/run_newman.sh api2            # chỉ 1 API

# 5. Xuất bảng test case + báo cáo tổng hợp
python scripts/export_testcases.py

# 6. Tái hiện toàn bộ lỗi bằng curl (không cần Postman)
bash bugs/reproduce_bugs.sh

# 7. Thử bộ sinh test case của Agent Skill
python agent-skill/pseudocode/generator.py --demo
```

---

## Bản đồ tài liệu

| Hạng mục nộp bài | Vị trí |
|---|---|
| **Báo cáo chính** | [`docs/00_MAIN_REPORT.md`](./docs/00_MAIN_REPORT.md) |
| Lý do chọn 3 API + phân tích đặc tả | [`docs/01_API_SELECTION.md`](./docs/01_API_SELECTION.md) |
| **Danh sách tính năng Postman đã dùng** | [`docs/02_POSTMAN_FEATURES.md`](./docs/02_POSTMAN_FEATURES.md) |
| **Test case (Excel)** | [`testcases/TESTCASES_23127195.xlsx`](./testcases/TESTCASES_23127195.xlsx) |
| Test case (CSV + nguồn JSON) | [`testcases/`](./testcases/) |
| Bảng tổng hợp test | [`testcases/TEST_SUMMARY.md`](./testcases/TEST_SUMMARY.md) |
| **Postman collection** | [`postman/collections/`](./postman/collections/) — 9 collection |
| Environment · dữ liệu data-driven | [`postman/environments/`](./postman/environments/) · [`postman/data/`](./postman/data/) |
| **Báo cáo Newman (HTML)** | [`newman/`](./newman/) |
| **Báo cáo lỗi** | [`bugs/BUG_REPORTS.md`](./bugs/BUG_REPORTS.md) |
| Nội dung GitHub Issues sẵn sàng dán | [`bugs/GITHUB_ISSUES.md`](./bugs/GITHUB_ISSUES.md) |
| Script tái hiện lỗi + bằng chứng | [`bugs/reproduce_bugs.sh`](./bugs/reproduce_bugs.sh) · [`bugs/evidence/`](./bugs/evidence/) |
| **Báo cáo CI/CD** | [`ci/CI_CD_REPORT.md`](./ci/CI_CD_REPORT.md) |
| Workflow GitHub Actions | [`../.github/workflows/newman-23127195.yml`](../.github/workflows/newman-23127195.yml) |
| **Agent Skill — thiết kế** | [`agent-skill/DESIGN.md`](./agent-skill/DESIGN.md) |
| Agent Skill — pseudocode + cài đặt | [`agent-skill/pseudocode/`](./agent-skill/pseudocode/) |
| Agent Skill — skill tái sử dụng | [`agent-skill/SKILL.md`](./agent-skill/SKILL.md) |
| **AI Audit Report** | [`ai/AI_AUDIT_REPORT.md`](./ai/AI_AUDIT_REPORT.md) |
| **AI Critique** (296 từ) | [`ai/AI_CRITIQUE.md`](./ai/AI_CRITIQUE.md) |
| Nhật ký tương tác AI | [`ai/interactions/`](./ai/interactions/) |
| Thư viện prompt theo từng bước | [`ai/prompts/PROMPT_LIBRARY.md`](./ai/prompts/PROMPT_LIBRARY.md) |
| **Git commit log** | [`evidence/git_commit_log.txt`](./evidence/git_commit_log.txt) |
| Chỉ mục bằng chứng | [`evidence/EVIDENCE_INDEX.md`](./evidence/EVIDENCE_INDEX.md) |

---

## ⚠ Việc còn phải tự làm

Theo §11 (Anti-AI-Cheat) của đề bài, những hạng mục sau **bắt buộc do người thật thực hiện** và
TA sẽ kiểm tra khi chấm:

- [x] ~~**Vẽ sơ đồ** bộ sinh test case~~ → ✅ **xong**: [`agent-skill/diagram/ai_test_generator_diagram.png`](./agent-skill/diagram/ai_test_generator_diagram.png) (kèm nguồn `.drawio`), đã nhúng vào báo cáo chính §4
- [x] ~~**Chụp Postman Console**~~ → ✅ **xong**: 3 ảnh trong [`evidence/`](./evidence/). Ảnh [`postman_console_timestamps.png`](./evidence/postman_console_timestamps.png) bung sẵn khối *Request Headers*, thấy `X-Student-Id: "23127195"` và `Host: "localhost:3000"` — phủ cả hai yêu cầu §11
- [x] ~~**Tạo 24 GitHub Issue**~~ → ✅ **xong**: [issue #5 → #28](https://github.com/thangak18/HW06/issues?q=is%3Aissue+label%3Ahw06-23127195), nhãn `hw06-23127195`
- [ ] **Đính ảnh chụp vào từng issue** (API không đính được ảnh) → mở từng issue ở link trên, kéo thả ảnh, lưu bản sao vào `bugs/screenshots/`
- [ ] **Push để chạy CI** rồi chụp 2 lần chạy (một xanh, một đỏ đúng 1 test) → [`ci/CI_CD_REPORT.md`](./ci/CI_CD_REPORT.md) §4–5
- [ ] **Quay video demo** Agent Skill và lấy link YouTube → [`video/VIDEO_DEMO_SCRIPT.md`](./video/VIDEO_DEMO_SCRIPT.md)
- [ ] **Xác nhận không trùng API** với 23127060 và 23127259
- [x] ~~**Xuất PDF** báo cáo chính + AI audit~~ → ✅ **xong**: 9 file trong [`pdf/`](./pdf/), sinh bằng `python scripts/export_pdf.py`
- [ ] **Chốt lại điểm tự đánh giá** và đổi tên file zip cho khớp
