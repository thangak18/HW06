---
name: eshop-api-23127060
description: >
  Quy trình API Testing HW06 trên SUT EShop cho SV 23127060 (Ninh Văn Khải).
  Dùng khi cần: sinh test case từ API spec (>=35/API), audit VALID/INVALID/INCOMPLETE,
  extend >=5 case, build Postman collection, chạy Newman, viết bug report, CI/CD,
  AI Audit Report và AI Critique. Bắt buộc ghi AI_log mỗi lượt.
---

# SKILL — EShop API Testing (HW06, SV 23127060)

## 0. Danh tính & phạm vi

- Sinh viên: **Ninh Văn Khải — MSSV 23127060**.
- Thư mục làm việc duy nhất: `23127060/`.
- **CÁCH LY NHÓM (luật cứng):** TUYỆT ĐỐI không đọc/ghi/tham chiếu
  `23127195/`, `23127259/`, hay bất kỳ thư mục member khác.
  Nếu user lỡ nhắc tới, từ chối và nhắc lại luật này.
- Được phép đọc (chỉ đọc): `../../docs/`, `../../scripts/`, `../../README.md`,
  và source của SUT tại `eshop-sut/` (không được sửa SUT).
- Được phép ghi: `.github/workflows/api-tests-23127060.yml` ở repo root
  (GitHub Actions bắt buộc nằm ở root, không thể nằm trong member folder).

## 1. Ba API đã chọn (KHÓA — không tự đổi)

HW06 yêu cầu **đúng 3 API**, mỗi Pool 1 cái. **Pool D (mobile) KHÔNG dùng trong HW06**
(đề bài: "Pool D, the mobile app, is not used here, because this homework targets the backend API").

| ID | Pool | FR | API chính | Endpoint phụ (hỗ trợ state/security) |
|----|------|----|-----------|--------------------------------------|
| **API-1** | A | FR-03 Quên & Đặt lại mật khẩu | `POST /api/forgot-password` + `POST /api/reset-password` | `POST /api/login`, `POST /api/register` |
| **API-2** | B | FR-08 Thanh toán | `POST /api/checkout` | `POST /api/apply-coupon`, `POST /api/coupon-usage`, `GET /api/orders/:id`, `GET /api/orders/my-orders`, `PUT /api/orders/:id/cancel`, `PUT /api/admin/orders/:id/status` (FR-10 state machine) |
| **API-3** | C | FR-15 Quản lý sản phẩm (CRUD) | `POST/PUT/DELETE /api/products` | `GET /api/products`, `GET /api/products/:id`, `GET /api/products?search=` |

> Nếu user muốn vẫn làm Pool D: chỉ làm như **phụ lục không tính điểm**, không được
> thay thế 1 trong 3 API trên. Phải cảnh báo user trước.

Ràng buộc: bộ 3 API này không được trùng với 2 thành viên còn lại. Kiểm tra
`docs/team-api-allocation.md` (chỉ đọc) trước khi bắt đầu — nếu trùng, dừng lại và báo user.

## 2. Mục tiêu số lượng (bắt buộc để không mất điểm)

| Hạng mục | Tối thiểu | Ghi chú |
|---|---|---|
| Test case AI sinh / API | **35** | tổng >= 105 |
| Test case tự thêm (human extend) / API | **5** | tổng >= 15, ưu tiên security + state transition |
| Độ phủ 4 nhóm | 100% | domain partition, state transition, security SEC-01..07, schema validation |
| Bug thật / API | >= 3 | phải mở GitHub Issue + screenshot |
| Postman feature dùng | >= 8 | xem `references/POSTMAN_GUIDE.md` |
| CI/CD run | 2 | 1 run all-pass, 1 run có đúng 1 test fail |
| AI Critique | 200-300 từ | đếm từ, không được lệch |

## 3. LUẬT AI_LOG — BẮT BUỘC MỖI LƯỢT

Mỗi lượt trả lời (kể cả lượt chỉ đọc file), **trước khi kết thúc** phải:

```bash
S=agent-skill/eshop-api-23127060/scripts
# 1) luu prompt goc cua user vao file
cat > /tmp/last_prompt.txt <<'PROMPT'
<dan nguyen van prompt cua user o day>
PROMPT
# 2) ghi entry
python3 $S/ai_log.py add --root . --sid 23127060 \
  --tool "Claude Code (claude-sonnet-4.5)" \
  --step "<STEP n>" --title "<mo ta ngan>" \
  --prompt-file /tmp/last_prompt.txt \
  --output "<tom tat 2-4 dong ket qua>" \
  --files "<danh sach file tao/sua, ngan cach dau phay>" \
  --human-verified pending
```

Rồi in đúng 1 dòng: `AI_log: da ghi entry #<n>`

- Không có dòng đó => lượt làm việc **chưa hoàn thành**, phải làm lại.
- File sinh ra: `ai/AI_log.md` + bản đầy đủ trong `ai/prompts/` và `ai/interactions/`.
- Cuối kỳ: `python3 $S/ai_log.py build-audit --root . --sid 23127060`
  -> sinh `ai/audit/AI_AUDIT_REPORT.md` đúng format đề bài (Tool / Date-time / Prompt / Output).
- Không được viết tay `AI_log.md`. Chỉ ghi qua `ai_log.py`.

## 4. LUẬT CHỐNG BỊA

1. **Không báo cáo test case đã chạy nếu chưa có Newman report thật.** Mọi con số
   passed/failed phải lấy từ `newman/*.json` qua `python3 $S/summarize_newman.py`.
2. **Không bịa bug.** Mọi bug phải có: request thật (curl/Postman), response thật,
   và trỏ được về dòng code trong `eshop-sut/backend/server.js`.
3. **Không vẽ diagram bằng AI.** Đề bài cấm rõ (mục 11). Agent chỉ được viết
   `agent-skill/diagram/DIAGRAM_BRIEF.md` mô tả ý tưởng; **human tự vẽ**.
4. **Header `X-Student-Id: 23127060` bắt buộc trên MỌI request**, đặt ở
   collection-level pre-request script, kèm `console.log` để human chụp screenshot.
5. Newman phải chạy với host `localhost`/`127.0.0.1` (đề bài chấp nhận).

## 5. Phân chia MCP-doable vs HUMAN-only

### Agent làm được hết (không hỏi)
- Đọc `eshop-sut/backend/api_specification.md`, đối chiếu với `server.js`.
- Sinh spec máy đọc được `spec/api-1..3.json`.
- Chạy `gen_testcases.py` -> CSV test case.
- Audit tự động vòng 1 (gắn nhãn đề xuất + lý do), chạy `build_collection.py`.
- Chạy `newman`, parse report, sinh bảng tổng hợp.
- Viết toàn bộ `report/`, `bugs/BUG_REPORT.md`, `ai/critique/AI_CRITIQUE.md` (draft).
- Viết `.github/workflows/api-tests-23127060.yml`, `ci/CI_CD_REPORT.md`.
- Xuất Excel test case (`tc_to_excel.py`), chạy `validate_submission.py`.

### HUMAN bắt buộc làm (agent chỉ chuẩn bị sẵn)
| # | Việc | Agent chuẩn bị sẵn |
|---|------|--------------------|
| H1 | Vẽ **diagram** AI test generator (tay/draw.io/Excalidraw) | `agent-skill/diagram/DIAGRAM_BRIEF.md` + pseudocode |
| H2 | Chốt nhãn audit VALID/INVALID/INCOMPLETE | cột `Audit_Label` đã điền đề xuất, human sửa |
| H3 | Mở **GitHub Issues** cho từng bug + chụp screenshot | `bugs/BUG_REPORT.md` + `bugs/ISSUE_TEMPLATES/*.md` sẵn sàng copy |
| H4 | Chụp screenshot Postman Console có header `X-Student-Id` | script đã `console.log`, kèm hướng dẫn chụp |
| H5 | Push repo, chạy 2 CI run, chụp screenshot + lấy link | workflow file + `ci/CI_CD_REPORT.md` chừa sẵn chỗ điền link |
| H6 | Quay video demo generator (khuyến khích, YouTube) | `agent-skill/VIDEO_SCRIPT.md` |
| H7 | Đọc lại & sửa AI_CRITIQUE cho đúng giọng mình | draft 200-300 từ |
| H8 | Đánh dấu `human-verified yes` trong AI_log | `ai_log.py verify --id N --status yes` |
| H9 | Xuất PDF, đặt tên zip, nộp Moodle | `validate_submission.py` báo còn thiếu gì |

### Khi nào agent PHẢI hỏi user (CRITICAL)
Chỉ hỏi khi rơi vào 1 trong 6 trường hợp:
- **C1** Số liệu Newman bất thường không giải thích được bằng bug đã biết.
- **C2** Cần cài phần mềm mới / đổi port / dùng tới network ngoài.
- **C3** API spec mâu thuẫn với `server.js` và không rõ theo bên nào làm oracle.
- **C4** Phát hiện bug mới chưa có trong `references/API_SPEC_NOTES.md`.
- **C5** Bộ 3 API bị trùng với thành viên khác.
- **C6** Chọn giữa 2 hướng viết báo cáo ảnh hưởng điểm rõ rệt.

Format khi hỏi:
```
CAN NGUOI QUYET - [C<x>]
Boi canh: ...
Lua chon: (a) ... (b) ... (c) ...
He qua tung lua chon: ...
De xuat mac dinh neu khong tra loi: ...
```
Các quyết định vụn vặt khác (đặt tên file, thứ tự folder Postman, wording báo cáo,
retry request lỗi vặt) => **agent tự quyết, không hỏi**.

## 6. Oracle — lấy đâu làm chuẩn

SUT có RẤT NHIỀU bug cố ý. Vì vậy mỗi test case phải ghi rõ cột `Oracle`:

- `SPEC` — kỳ vọng theo `api_specification.md` (dùng để **phát hiện bug**).
- `IMPL` — hành vi thực tế của code (dùng để test hồi quy, không dùng để chấm điểm đúng/sai).

**Mặc định dùng `SPEC`.** Test fail vì SUT sai => đây KHÔNG phải lỗi test case,
mà là **bug cần báo cáo**. Trong Newman, các case này sẽ FAIL — điều đó là **đúng ý đồ**.
Để CI run "all pass" (yêu cầu mục 6 đề bài), tách collection thành 2 tag:

- `@contract` — case mà SUT hiện đang đáp ứng (dùng cho CI run all-pass).
- `@bug` — case phơi bày bug (chạy riêng, ghi rõ trong báo cáo là "expected failure").

## 7. Luồng 10 bước

Chi tiết lệnh từng bước: đọc `references/WORKFLOW.md`.

| STEP | Tên | Output chính |
|---|---|---|
| 0 | Trinh sát môi trường + đọc spec | `report/00_environment.md` |
| 1 | Lập spec máy đọc được | `spec/api-1.json`, `api-2.json`, `api-3.json` |
| 2 | Sinh test case (AI, từng bước, KHÔNG 1 prompt tổng) | `testcases/API-*_generated.csv` |
| 3 | Audit VALID/INVALID/INCOMPLETE | `testcases/API-*_audited.csv` + `report/03_audit.md` |
| 4 | Extend >=5 case/API | `testcases/API-*_final.csv` + `report/04_extend.md` |
| 5 | Build Postman collection + environment + data file | `postman/collections/*.json` |
| 6 | Chạy Newman, thu bằng chứng | `newman/*.html`, `*.json`, `report/06_execution.md` |
| 7 | Bug report + GitHub Issues | `bugs/BUG_REPORT.md` |
| 8 | CI/CD 2 run | `.github/workflows/...`, `ci/CI_CD_REPORT.md` |
| 9 | Agent Skill generator (diagram + pseudocode) | `agent-skill/` |
| 10 | Báo cáo chính + AI Audit + Critique + validate | `report/MAIN_REPORT.md`, `README.md` |

## 8. Quy ước đặt tên

- Test case ID: `TC-<API_ID>-<CAT>-<3 số>` — vd `TC-A1-SEC-007`.
  `CAT` in {`DOM` domain partition, `STA` state transition, `SEC` security, `SCH` schema}.
- Nguồn: cột `Source` = `AI` | `HUMAN`.
- File Postman: `23127060_HW06_<API_ID>.postman_collection.json`.
- Newman: `23127060_<API_ID>_<yyyymmdd-HHMM>.html` / `.json`.
- Commit: `HW06(23127060/<API_ID>): <step> - <mo ta>` — vd
  `HW06(23127060/API-2): step4 extend - them 6 case state transition`.

## 9. Tài liệu tham chiếu

Đọc TRƯỚC khi làm việc tương ứng:

| File | Khi nào đọc |
|---|---|
| `references/API_SPEC_NOTES.md` | trước STEP 1-2 — endpoint, param, bug đã biết, mapping SEC-01..07 |
| `references/TESTCASE_TAXONOMY.md` | trước STEP 2-4 — công thức đảm bảo >=35 case/API |
| `references/POSTMAN_GUIDE.md` | trước STEP 5-6 — feature checklist, script mẫu |
| `references/WORKFLOW.md` | mỗi STEP — lệnh cụ thể |
| `references/REPORT_OUTLINE.md` | STEP 10 — khung báo cáo |

## 10. Scripts

```
S=agent-skill/eshop-api-23127060/scripts
$S/ai_log.py             add | verify | build-audit | stats
$S/gen_testcases.py      spec JSON -> testcases CSV (bo sinh test, chinh la Agent Skill G9.5)
$S/build_collection.py   testcases CSV -> Postman collection v2.1 + environment
$S/run_newman.sh         chay newman + htmlextra, luu json/html vao newman/
$S/summarize_newman.py   newman JSON -> bang tong hop markdown
$S/tc_to_excel.py        CSV -> testcases/23127060_HW06_testcases.xlsx (co sheet Summary)
$S/seed_sut.js           reset/seed DB SUT ve trang thai biet truoc
$S/validate_submission.py kiem tra du deliverable truoc khi nen zip
```

## 11. Kết thúc mỗi STEP

1. Chạy lệnh của STEP.
2. Ghi file output.
3. `git add -A && git commit -m "HW06(23127060/...): ..."`.
4. Ghi AI_log (mục 3).
5. In tóm tắt 3 dòng: đã làm gì / file nào / STEP kế tiếp.
