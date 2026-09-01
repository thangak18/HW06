# 01 — Lựa chọn 3 API & Phân tích đặc tả

**Sinh viên:** 23127195 · **HW06 — API Testing** · **SUT:** EShop (`ttbhanh/eshop-sut`)

## 1. Ràng buộc chọn API

Theo §5 của đề:
- Chọn đúng **3 API**, mỗi API hiện thực một tính năng thuộc **Pool A**, **Pool B**, **Pool C**.
- Pool D (Mobile) không dùng.
- **Không trùng** với thành viên khác trong nhóm.

Thành viên khác đã nhận: **FR-02** (Login & lockout), **FR-10** (Order state machine), **FR-14** (Category CRUD)
→ ba FR này bị loại khỏi danh sách ứng viên.

## 2. Bộ API đã chọn

| | Pool | FR | Endpoint | Tham số chính | Kỹ thuật phủ được |
|---|---|---|---|---|---|
| **API-1** | A | FR-03 — Quên & Đặt lại mật khẩu (2 bước) | `POST /api/forgot-password`<br>`POST /api/reset-password` | `email`, `resetToken`, `newPassword` | Domain partition (3 tham số), State transition (vòng đời OTP), Security (SEC-01/05/07), Schema |
| **API-2** | B | FR-09 — Áp mã giảm giá | `POST /api/apply-coupon`<br>`POST /api/coupon-usage` | `code`, `total_amount`, `user_id` | Decision table 5 điều kiện C1–C5, Boundary trên `min_order_amount`, Security (SEC-02/05), Schema + oracle số học |
| **API-3** | C | FR-15 — Quản lý sản phẩm (Admin CRUD) | `POST /api/products`<br>`PUT /api/products/:id`<br>`DELETE /api/products/:id` | `name`, `price`, `description`, `imageUrl`, `category_id` | Domain partition (5 tham số), Resource lifecycle Create→Update→Delete, Access control FR-12 (SEC-02/03), SQLi (SEC-05), Schema |

## 3. Vì sao chọn bộ này

Tiêu chí áp dụng cho từng pool:

1. **Đủ tham số để phủ domain partition.** Đề yêu cầu "domain partitions on **every** parameter". API chỉ có 0–1 tham số
   (ví dụ `GET /api/cart`) không đủ chất liệu. Ba API đã chọn có lần lượt 3, 3 và 5 tham số.
2. **Có vòng đời trạng thái.** Đề yêu cầu phủ state transition. FR-03 có vòng đời OTP (`NONE → ISSUED → USED/INVALIDATED`),
   FR-09 có trạng thái sử dụng mã theo user (`chưa dùng → đã dùng n lần → hết lượt`), FR-15 có vòng đời tài nguyên
   (`không tồn tại → tồn tại → đã sửa → đã xoá`). Không API nào phải mượn lại state machine đơn hàng (FR-10) của bạn cùng nhóm.
3. **Chạm được nhiều mục SEC.** Tổng cộng bộ 3 API chạm SEC-01, SEC-02, SEC-03, SEC-05, SEC-07 (5/7 mục).
   SEC-04 thuần UI và SEC-06 thuộc FR-04 nên không nằm trong phạm vi 3 API này — được nêu rõ trong báo cáo chính.
4. **Response có schema kiểm chứng được.** Cả 3 API đều trả JSON có cấu trúc mô tả trong `api_specification.md`,
   nên bước schema validation có oracle rõ ràng.

## 4. Khoảng trống của đặc tả (phát hiện khi phân tích)

`api_specification.md` **không** chứa SEC-01…SEC-07; các yêu cầu bảo mật này nằm ở `README.md` (SRS) của SUT.
Đây là điểm cần lưu ý khi "đưa API specification cho AI": nếu chỉ đưa `api_specification.md`, AI **không thể** sinh được
test case bảo mật đúng ngữ cảnh. Xem `ai/prompts/` — prompt của bước Generate đã nạp **cả hai** tài liệu.

Ngoài ra `api_specification.md` không mô tả:
- Mã lỗi (chỉ mô tả response 200 thành công) → phần lớn kỳ vọng status 4xx phải suy ra từ SRS + nguyên tắc REST.
- Ràng buộc độ mạnh mật khẩu ở bước reset (phải tham chiếu chéo sang FR-01 trong SRS).
- Ràng buộc `price > 0`, `name ≤ 255 ký tự` (chỉ có trong SRS FR-15).

## 5. Xác nhận không trùng nhóm

Xem `docs/team-api-allocation.md` ở thư mục gốc repo. **Việc cần làm của SV:** xác nhận với 23127259 trước khi nộp.
