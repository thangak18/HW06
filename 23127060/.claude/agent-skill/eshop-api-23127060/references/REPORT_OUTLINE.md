# REPORT_OUTLINE — Khung báo cáo HW06 (SV 23127060)

Mỗi mục dưới đây ánh xạ trực tiếp vào 1 yêu cầu chấm điểm của đề bài.
Không được bỏ mục nào — "Missing any required document results in 0 points".

---

## Cây file báo cáo

```
report/
├── MAIN_REPORT.md          <- ban chinh, gop tat ca (xuat PDF)
├── MAIN_REPORT.pdf
├── 00_environment.md
├── 01_api_selection.md
├── 02_generation.md
├── 03_audit.md
├── 04_extend.md
├── 05_postman_features.md
├── 06_execution.md
└── 07_test_generator_design.md
bugs/BUG_REPORT.md
ci/CI_CD_REPORT.md
ai/audit/AI_AUDIT_REPORT.md
ai/critique/AI_CRITIQUE.md
README.md
```

---

## MAIN_REPORT.md — khung chi tiết

### 1. Thông tin
Họ tên, MSSV, lớp, link GitHub repo công khai, link video (nếu có), ngày nộp,
tự đánh giá điểm.

### 2. Môi trường thực nghiệm
OS, Node, npm, Postman, Newman, base URL, cách chạy SUT, commit hash của SUT.

### 3. Lựa chọn 3 API (mục 5 đề bài)

| API | Pool | FR | Endpoint | Lý do chọn | Không trùng với ai |
|---|---|---|---|---|---|
| API-1 | A | FR-03 | `POST /api/forgot-password`, `POST /api/reset-password` | luồng 2 bước, giàu rủi ro bảo mật | 23127195 làm FR-04, 23127259 làm FR-02 |
| API-2 | B | FR-08 | `POST /api/checkout` (+FR-09, FR-10) | có state machine + tính tiền | 23127195 làm FR-09, 23127259 làm FR-10 |
| API-3 | C | FR-15 | `POST/PUT/DELETE /api/products` | CRUD đầy đủ + phân quyền | 23127195 làm FR-16, 23127259 làm FR-14 |

> Ghi rõ: **Pool D (mobile) không sử dụng trong HW06** theo mục 5 đề bài.

### 4. Quy trình sinh test case bằng AI (mục 6.1)
**Bắt buộc chứng minh không dùng 1 prompt tổng.** Trình bày 4 vòng:

| Vòng | Mục tiêu | Prompt (trích) | Số case thu được | AI_log entry |
|---|---|---|---|---|
| 2a | domain partition | ... | 16 | #4 |
| 2b | state transition | ... | 9 | #5 |
| 2c | security SEC-01..07 | ... | 11 | #6 |
| 2d | schema validation | ... | 6 | #7 |

Kèm bảng độ phủ: mọi tham số / mọi chuyển trạng thái / mọi mã SEC đều có >=1 case.

### 5. Audit kết quả AI (mục 6.2)

| API | Tổng AI | VALID | INVALID | INCOMPLETE | % VALID |
|---|---|---|---|---|---|
| API-1 | 36 | 22 | 5 | 9 | 61% |

Kèm **>= 5 ví dụ chi tiết** dạng: case gốc -> nhãn -> lý do -> bản đã sửa.

### 6. Test case tự bổ sung (mục 6.3)

| TC_ID | Tiêu đề | Nhóm | Tại sao AI bỏ sót |
|---|---|---|---|
| TC-C3-SEC-901 | DELETE sản phẩm không cần token | SEC-03 | AI suy diễn từ tên endpoint, không đọc code |

Tối thiểu 5 case/API, tổng >= 15.

### 7. Thực thi (mục 6.4)

| API | Tổng case | Passed | Failed | Fail do bug SUT | Thời gian | Report |
|---|---|---|---|---|---|---|
| API-1 | 41 | 27 | 14 | 14 | 12.3s | `newman/23127060_API-1_*.html` |

- Ảnh chụp Postman Console có `X-Student-Id: 23127060`.
- Giải thích rõ: case FAIL nào là **expected failure** (phơi bày bug), case nào là lỗi thật.

### 8. Postman features đã dùng (mục 6, bắt buộc liệt kê)
Bảng checklist từ `report/05_postman_features.md`, kèm screenshot cho feature GUI.

### 9. Bug report (mục 6.5)
Tóm tắt bảng, chi tiết ở `bugs/BUG_REPORT.md`, mỗi bug 1 link GitHub Issue + screenshot.

| ID | Tiêu đề | Mức | SEC | API | Issue |
|---|---|---|---|---|---|
| C-01 | Product CRUD không yêu cầu xác thực | Critical | SEC-02, SEC-03 | API-3 | #12 |

### 10. CI/CD (mục 6)
Cấu hình pipeline, 2 run (1 pass / 1 fail), screenshot + link, 2 commit hash.

### 11. Thiết kế bộ sinh test bằng AI (mục 7 — 10 điểm)
- **Diagram tự vẽ** (không được AI sinh) — `agent-skill/diagram/23127060_generator_diagram.png`.
- **Pseudocode** — `agent-skill/pseudocode/generator.pseudo.md`.
- Bản hiện thực: `scripts/gen_testcases.py`, cách chạy, ví dụ đầu ra.
- Hạn chế và hướng mở rộng.

### 12. Phụ lục A — AI Audit Report (mục 9)
Câu mở đầu bắt buộc: **"I use AI tools for the following tasks"**, sau đó bảng
Tool / Date-time / Prompt / Output cho từng tương tác.

### 13. Phụ lục B — AI Critique (mục 10, 200-300 từ)
Trả lời đủ 3 câu: AI sai/thiên lệch/thiếu ở đâu? Vì sao AI không bắt được?
Bản thân học được nguyên tắc gì khi làm việc với AI?

---

## README.md (bắt buộc trong zip)

```markdown
# HW06 — API Testing — Ninh Van Khai — 23127060

## Test summary
| Chi so | Gia tri |
|---|---|
| So API | 3 |
| Test case AI sinh | |
| Test case tu them | |
| Tong test case | |
| Da thuc thi | |
| Passed | |
| Failed | |
| Failed do bug SUT (expected) | |
| So bug bao cao | |
| So GitHub Issue | |

## Bang tu danh gia
| No. | Tieu chi | Diem toi da | Tu cham |
|---|---|---|---|
| 1 | API 1 — full pipeline | 30 | |
| 2 | API 2 — full pipeline | 30 | |
| 3 | API 3 — full pipeline | 30 | |
| 4 | Agent Skills (AI-driven test generator) | 10 | |
| | **Tong** | **100** | |

## Link
- GitHub repo:
- GitHub Issues:
- Video demo generator (neu co):

## Cach chay lai
...
```

Tên file nộp: `23127060_HW06_AI_API_<3 chữ số>.zip`

---

## Bảng kiểm trước khi nộp (chạy `validate_submission.py`)

- [ ] MAIN_REPORT.md + .pdf
- [ ] Link GitHub repo công khai
- [ ] 3 Postman collection .json
- [ ] Newman report .html (>=3)
- [ ] Danh sách Postman feature
- [ ] CI/CD report + 2 screenshot + 2 link run
- [ ] Excel test case + sheet summary
- [ ] Diagram (PNG/Mermaid) + pseudocode — diagram TỰ VẼ
- [ ] (tùy chọn) OpenAPI .yaml — nếu AI sinh thì phải audit
- [ ] Bug report + screenshot GitHub Issues
- [ ] AI_AUDIT_REPORT.md + .pdf
- [ ] AI_CRITIQUE.md + .pdf (200-300 từ)
- [ ] git commit log (.txt)
- [ ] README.md có bảng tự đánh giá + test summary
