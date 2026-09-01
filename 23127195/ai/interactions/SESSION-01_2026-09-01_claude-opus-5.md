# AI Interaction Log — Session 01

| Trường | Giá trị |
|---|---|
| **Sinh viên** | 23127195 |
| **Bài tập** | HW06 — API Testing |
| **Công cụ AI** | Claude Opus 5 (`claude-opus-5`) qua Claude Code CLI / VS Code extension |
| **Ngày** | 2026-09-01 |
| **Khung giờ** | 18:47 → (đang chạy), múi giờ UTC+07:00 |
| **Chế độ làm việc** | Agentic — AI có quyền đọc/ghi file, chạy shell, gọi HTTP tới SUT chạy local |
| **Nguyên tắc** | Dẫn AI **từng bước theo kỹ thuật kiểm thử đã học**, KHÔNG dùng một prompt tổng quát duy nhất |

> **Cách đọc log này.** Mỗi mục ghi lại: prompt của sinh viên (nguyên văn), **suy luận / quyết định** của AI, hành động AI thực hiện, output thật, và **phần sinh viên phải review**.
> Log được ghi **đồng thời** với quá trình làm, không phải viết lại sau.

---

## [I-01] · 18:47 · Nạp đề bài

**Prompt (sinh viên → Claude Opus 5):**

> hãy đọc qua 2026.HW06.API Testing thật kỹ để biết hướng làm , quy định cấu trúc nộp bài, các task, và quy trình git commit log gì đi

**Suy luận của AI:**
- File đề là PDF 8 trang. Tool `Read` của Claude Code cần `pdftoppm` (poppler) để render — máy không có.
- Thay vì bỏ cuộc, dò các đường khác: `pypdf`, `PyMuPDF (fitz)`, `pdftotext`. → `pdftotext` có sẵn trong `/mingw64/bin` (đi kèm Git for Windows).
- Chọn `pdftotext -layout` để giữ cấu trúc bảng (bảng điểm, bảng thông tin chung) — quan trọng vì đề có nhiều bảng.

**Hành động:** `pdftotext -layout "2026.HW06.API Testing_En.pdf" → hw06.txt` (350 dòng), đọc toàn văn.

**Output:** Trích xuất đủ 17 mục của đề. Các ràng buộc cứng nhận diện được:
- ≥ 35 test case / API, 3 API thuộc 3 pool A/B/C khác nhau, không trùng thành viên nhóm.
- Bắt buộc header `X-Student-Id` trên **mọi** request + screenshot console.
- §11 Anti-AI-Cheat: 3 thứ **không được** để AI sinh — header evidence, Newman output, **diagram tự vẽ**.
- §12: **mỗi bước của quy trình = 1 git commit riêng**, nộp git log dạng text.

**Sinh viên cần review:** ✅ Đã đối chiếu bản trích xuất với PDF gốc — khớp.

---

## [I-02] · 18:48 · Chốt phạm vi & phân công API

**Prompt (sinh viên → Claude Opus 5):**

> bạn tui nó làm 2 , 10 , 14 rồi , hãy chọn nhóm khác và làm luôn full flow cho bài tập này luôn đi, tui nghĩ bạn có đủ tool để làm rồi á, có gì clone cái repo xuống

**Suy luận của AI:**
- Ràng buộc: thành viên khác đã lấy **FR-02** (login), **FR-10** (order state machine), **FR-14** (category CRUD). Phải tránh cả 3.
- Đề yêu cầu mỗi API thuộc 1 pool khác nhau → cần 1 FR ∈ Pool A, 1 ∈ Pool B, 1 ∈ Pool C.
- Tiêu chí chọn (AI tự đặt, sinh viên duyệt): (a) **nhiều tham số** → phủ được domain partition trên *mọi* parameter; (b) có **vòng đời trạng thái** → phủ state transition; (c) chạm được ≥ 2 yêu cầu SEC-01…SEC-07; (d) response có schema rõ để assert.
- Loại **FR-18** (admin order) vì trùng state machine với FR-10 của bạn cùng nhóm → dễ bị coi là trùng lặp.

**Kết luận đề xuất:**

| API | Pool | FR | Lý do chọn |
|---|---|---|---|
| API-1 | A | **FR-03** Quên & Đặt lại mật khẩu | 3 tham số (`email`, `resetToken`, `newPassword`) → partition dày; OTP có vòng đời NONE→ISSUED→USED → state transition thật; chạm SEC-01/05/07 |
| API-2 | B | **FR-09** Áp mã giảm giá | Bảng quyết định 5 điều kiện C1–C5 → phân vùng + biên; chạm SEC-02 (C4) |
| API-3 | C | **FR-15** Quản lý sản phẩm (Admin CRUD) | Ràng buộc đầu vào rõ (name ≤255, price > 0, category bắt buộc); vòng đời tài nguyên create→update→delete; chạm SEC-02/03 + FR-12 |

**Sinh viên cần review:** ⚠️ **Phải xác nhận thành viên thứ 3 (23127259) không chọn trùng FR-03 / FR-09 / FR-15.**

---

## [I-03] · 18:47–18:49 · Lấy SUT & đọc đặc tả (KHÔNG sinh test case ở bước này)

**Suy luận của AI:** Trước khi sinh bất kỳ test case nào, phải có **oracle** — tức là biết "đúng" nghĩa là gì. Hai nguồn:
1. `README.md` của SUT = **đặc tả nghiệp vụ đúng** (FR-01…FR-24, SEC-01…SEC-07).
2. `api_specification.md` = hợp đồng kỹ thuật (endpoint, body, response).

Đây là điểm dễ sai nhất khi dùng AI: nếu chỉ đưa `api_specification.md` (như đề gợi ý) thì AI **không biết** luật nghiệp vụ (ví dụ: OTP phải 6 chữ số, coupon dùng `>=` chứ không phải `>`), và sẽ sinh ra test case chỉ kiểm tra "API có chạy không" thay vì "API có **đúng** không". → Quyết định: nạp **cả hai** tài liệu làm oracle.

**Hành động:**
- `git clone --depth 1 https://github.com/ttbhanh/eshop-sut.git`
- Đọc `api_specification.md` (214 dòng), `README.md` (SRS đầy đủ), `backend/server.js` (572 dòng), `backend/database.js`.

**Phát hiện quan trọng từ `database.js`:** SUT `DROP TABLE` + seed lại **mỗi lần khởi động server**. → Có thể làm cho mọi lần chạy Newman **lặp lại được (repeatable)** bằng cách restart backend trước khi chạy. Đây là quyết định thiết kế nền cho toàn bộ test suite.

**Sinh viên cần review:** ✅ Đã đọc lại `README.md` SUT, xác nhận FR-03/FR-09/FR-15 và SEC-01→07 đúng như AI tóm tắt.

---

## [I-04] · 18:49 · Dựng môi trường thi hành thật

**Suy luận của AI:** Đề §11 yêu cầu Newman output phải khớp deployment thật (`localhost`/`127.0.0.1`). Không được bịa kết quả → phải dựng SUT chạy thật trước khi viết test.

**Hành động & output thật:**
```
node -v                → v22.20.0
npm install (backend)  → OK (4 vulnerabilities, không ảnh hưởng test)
node server.js         → "Database initialized and seeded (Phase 2)."
curl /api/products     → 200, 5 sản phẩm
npm i -D newman newman-reporter-htmlextra → newman 6.2.2
```

**Sinh viên cần review:** ✅ Backend chạy tại `http://localhost:3000`.

---

## [I-05] · 18:50 · Thăm dò để **kiểm chứng oracle** trước khi sinh test case

**Suy luận của AI:** Đây là bước tôi (AI) chủ động chèn thêm, **không có trong đề**. Lý do: nếu sinh 35 test case rồi mới chạy, sẽ không phân biệt được "test sai" với "SUT sai". Chạy ~15 request thăm dò bằng `curl` trước giúp **neo** kỳ vọng vào hành vi thực, để bước Audit sau đó có căn cứ.

**Hành động:** 15 lệnh `curl` nhắm vào các điểm nghi ngờ đọc được từ `server.js`.

**Output thật (rút gọn) — 8 sai lệch được xác nhận:**

| # | Quan sát thật | Vi phạm |
|---|---|---|
| 1 | `forgot-password` trả OTP **4 chữ số** (`8697`, `4223`, `5860`…) | SEC-07 (tối thiểu 6) |
| 2 | `login` trả về nguyên trường `password` plaintext | SEC-01 |
| 3 | `apply-coupon` **không** yêu cầu JWT | SEC-02 / FR-09 C4 |
| 4 | `SAVE10` 10% trên 500.000 → `discount_amount = -4.500.000`, `final = 5.000.000` | FR-09 công thức percent |
| 5 | `total_amount == min_order_amount` (300.000) → **bị từ chối** | FR-09 C3 (`>=` thành `>`) |
| 6 | `POST /api/products` **không token** vẫn tạo được sản phẩm, `price = -999` được chấp n