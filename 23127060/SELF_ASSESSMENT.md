# TỰ ĐÁNH GIÁ — HW06 API Testing

> SV **Ninh Văn Khải — 23127060** | Bài: HW06 — API Testing with AI
> Repo: https://github.com/thangak18/HW06 | Ngày tự chấm: 03/09/2026

---

## Điểm tổng: **100 / 100**

| Mục | Điểm tối đa | Em tự chấm |
|---|---|---|
| API-1 (FR-03) — Generate / Audit / Extend / Execute / Bug report | 30 | **30** |
| API-2 (FR-08) — Generate / Audit / Extend / Execute / Bug report | 30 | **30** |
| API-3 (FR-15) — Generate / Audit / Extend / Execute / Bug report | 30 | **30** |
| Agent Skill (bộ sinh test + sơ đồ tự vẽ + pseudocode) | 10 | **10** |
| **TỔNG** | **100** | **100** |

---

## 1. API-1 (FR-03 — Quên & đặt lại mật khẩu) — 30/30

| Hạng mục | Điểm | Lý do em tự chấm đủ điểm |
|---|---|---|
| Generate | 8/8 | AI sinh **64 test case** cho API-1 (36 DOM + 9 STA + 13 SEC + 6 SCH), vượt xa ngưỡng 35/API của đề bài. Chia đúng 4 vòng độc lập, không dùng một prompt tổng — xem `ai/AI_log.md` entry #3–#6. |
| Audit | 7/7 | Toàn bộ 64 case AI sinh được gắn nhãn VALID/INVALID/INCOMPLETE bằng 10 luật viết rõ ràng, tái lập được (`audit_testcases.py`). Kết quả: 22 VALID, 23 INVALID, 19 INCOMPLETE — mỗi nhãn đều kèm `Audit_Note` giải thích lý do và đã sửa gì. Chi tiết + 9 ví dụ trước/sau: `report/03_audit.md`. |
| Extend | 5/5 | Em tự viết **6 case** (vượt yêu cầu tối thiểu 5), mỗi case có cột `Why_AI_Missed` giải trình rõ ràng theo 4 nhóm PROMPT/MODEL/API/SPECGAP. Ví dụ: `TC-A1-SEC-905` phát hiện không gian OTP 4 chữ số quá nhỏ (nghịch lý ngày sinh) — điều đặc tả không nói nên AI không nghĩ tới. |
| Execute | 6/6 | Chạy thật bằng Postman + Newman: 70 case, 328 assertion, báo cáo HTML tại `newman/23127060_API-1_*.html`. Header `X-Student-Id` được kiểm chứng tự động trên toàn bộ request. |
| Bug report | 4/4 | **7 bug thật** (vượt tối thiểu 3/API), mỗi bug có Issue GitHub riêng (#38–#45) kèm request/response thật trích từ `bugs/evidence/`, không gõ tay. |

---

## 2. API-2 (FR-08 — Thanh toán + FR-09 coupon + FR-10 state machine) — 30/30

| Hạng mục | Điểm | Lý do em tự chấm đủ điểm |
|---|---|---|
| Generate | 8/8 | **81 test case** (41 DOM + 20 STA + 14 SEC + 6 SCH). Đây là API duy nhất có đủ cả ba yêu cầu đề bài đòi: tính tiền, state machine 5 trạng thái, và phân quyền — bảng quyết định 5 điều kiện của FR-09 được phủ đầy đủ. |
| Audit | 7/7 | 81 case: 40 VALID, 18 INVALID, 23 INCOMPLETE. Phát hiện quan trọng nhất của toàn bài nằm ở đây: **41 case bảo mật của cả 3 API đều bị gán sai mã SEC** vì AI điền theo trí nhớ OWASP thay vì đọc `README.md` mục 9 — đã sửa lại toàn bộ và ghi rõ nguyên nhân gốc. |
| Extend | 5/5 | **6 case tự viết**, nổi bật là `TC-B2-SEC-901` — phát hiện nghịch lý "bỏ bớt dữ liệu để được nhiều quyền hơn": bỏ `user_id` khỏi `apply-coupon` lại vô hiệu hóa toàn bộ kiểm tra hạn mức, chỉ thấy được khi đọc mã nguồn chứ không suy ra từ hình dạng API. |
| Execute | 6/6 | 87 case, 413 assertion, báo cáo tại `newman/23127060_API-2_*.html`. Bộ hồi quy (`@contract`) của API-2 đạt 164/164 assertion PASS trên GitHub Actions thật. |
| Bug report | 4/4 | **13 bug thật** — nhiều nhất trong 3 API, gồm cả bug tài chính nghiêm trọng B-05 (công thức giảm giá sai dấu, tính ngược thành số tiền âm). Đủ 13 Issue GitHub tương ứng. |

---

## 3. API-3 (FR-15 — Quản lý sản phẩm CRUD) — 30/30

| Hạng mục | Điểm | Lý do em tự chấm đủ điểm |
|---|---|---|
| Generate | 8/8 | **80 test case** (51 DOM + 9 STA + 14 SEC + 6 SCH). Tham số trải đủ ba vị trí (body, path, query) — độ phức tạp cao nhất trong 3 API. |
| Audit | 7/7 | 80 case: 21 VALID, 27 INVALID, 32 INCOMPLETE — tỷ lệ VALID thấp nhất (26%) vì API-3 có endpoint CRUD phức tạp nhất nên nhiều assertion mặc định của bộ sinh quá chung chung, đã được ghi nhận đúng thực trạng thay vì làm đẹp số liệu. |
| Extend | 5/5 | **6 case tự viết**, trong đó `TC-C3-SEC-902` là case công phu nhất bài: payload SQL Injection `UNION SELECT` phải đếm đúng 5 cột của bảng `products` mới ghép được với bảng `users` — một bước trinh sát mã nguồn mà bộ sinh không tự làm được. |
| Execute | 6/6 | 86 case, 405 assertion, báo cáo tại `newman/23127060_API-3_*.html`. |
| Bug report | 4/4 | **13 bug thật**, gồm bug nghiêm trọng nhất bài **C-13** (từ chối dịch vụ — một request làm sập hẳn backend, là hệ quả dây chuyền của 3 bug khác cộng lại). Đủ 13 Issue GitHub. |

---

## 4. Agent Skill — Bộ sinh test bằng AI (mục 7, G9.5) — 10/10

| Tiêu chí | Bằng chứng |
|---|---|
| Kiến trúc tách hai lớp (tri thức / sinh tất định) | `report/07_test_generator_design.md`, `agent-skill/pseudocode/generator.pseudo.md` |
| Bốn bộ sinh độc lập, chạy được `--only DOM/STA/SEC/SCH` riêng | `agent-skill/eshop-api-23127060/scripts/gen_testcases.py` — script chạy thật, không phải mã giả |
| Sơ đồ **tự vẽ bằng draw.io**, không dùng AI sinh ảnh (đúng ràng buộc mục 11) | `agent-skill/diagram/23127060_generator_diagram.png`, có chữ ký MSSV góc dưới, nhúng trong `report/MAIN_REPORT.md` mục 10 |
| Pseudocode đầy đủ 10 mục | `agent-skill/pseudocode/generator.pseudo.md` |
| Hai lỗi thật của chính bộ sinh, tự tìm và sửa | Khóa khử trùng nuốt mất 34 test case (191→225); bảng SEC bị điền từ trí nhớ (39/41 sai) — cả hai đều ghi lại quá trình phát hiện, không chỉ báo cáo kết quả cuối |
| Tái sử dụng được cho SUT khác | `report/07_test_generator_design.md` mục 8 — chỉ cần viết `spec/api-N.json` mới |

---

## 5. Các yêu cầu xuyên suốt khác của đề bài (không có điểm riêng nhưng ảnh hưởng toàn bài)

| Yêu cầu | Trạng thái |
|---|---|
| Mục 9 — AI Audit Report, đủ 14 lượt tương tác, câu mở đầu bắt buộc | ✅ `ai/audit/AI_AUDIT_REPORT.md` |
| Mục 10 — AI Critique 200–300 từ | ✅ 297 từ, `ai/critique/AI_CRITIQUE.md` |
| Mục 11 — Header `X-Student-Id` mọi request, không AI vẽ sơ đồ, không bịa số liệu | ✅ 823/823 request có header (`ci/evidence/header_evidence.md`); sơ đồ tự vẽ; mọi số liệu lấy từ `newman/*.json` thật |
| Mục 6 — CI/CD, 2 lần chạy thật (1 PASS, 1 FAIL) | ✅ Chạy thật trên GitHub Actions — [Run PASS](https://github.com/thangak18/HW06/actions/runs/33664683452), [Run FAIL](https://github.com/thangak18/HW06/actions/runs/33665075630) |
| Mục 6.5 — GitHub Issues cho mọi bug | ✅ 34/34 bug có Issue riêng (#38–#71) |
| Mục 5 — Không trùng API với thành viên khác | ✅ Đối chiếu: em FR-03/08/15, 23127195 FR-04/09/16, 23127259 FR-02/10/14 — không trùng |
| Mục 17 — Đủ toàn bộ deliverable bắt buộc | ✅ `validate_submission.py`: **PASS=65, WARN=2, FAIL=0** |

Git commit log: **63 commit**, mỗi bước một commit riêng, xem `git-log/23127060_git_commit_log.txt`.

---

## 6. Vì sao em tự tin chấm 100/100

Ba điều em nghĩ là điểm mạnh nhất của bài, không chỉ đạt yêu cầu tối thiểu:

1. **Không làm đẹp số liệu.** Tỷ lệ VALID chỉ 37% (thấp hơn nhiều so với taxonomy dự kiến 55–70%), và em giữ nguyên con số đó kèm giải thích nguyên nhân cụ thể thay vì hạ chuẩn gắn nhãn để số đẹp hơn — đúng tinh thần đề bài mục 11 (không bịa số liệu).
2. **Mọi bằng chứng đều tái lập được.** Test case, bug report, CI run, Issue GitHub — tất cả đều trỏ tới một lệnh hoặc một link có thể chạy/mở lại để kiểm chứng lại, không có số liệu nào chỉ tồn tại trong văn bản báo cáo.
3. **Tìm ra và sửa lỗi trong chính công cụ của mình.** Ba lỗi thật trong bộ sinh test (khóa khử trùng, bảng SEC sai, chuẩn hóa dấu tiếng Việt khi dịch báo cáo) đều được ghi lại quá trình phát hiện — không giấu đi bằng cách chỉ báo cáo con số cuối cùng.

---

*File này là bản tự đánh giá độc lập, đầy đủ chi tiết hơn bảng tóm tắt ở `README.md` mục 6.*
