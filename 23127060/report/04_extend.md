# STEP 4 — Test case em tự bổ sung (những gì AI bỏ sót)

> HW06 — API Testing | SV **Ninh Văn Khải — 23127060** | Đề bài mục 6.3

Đề bài: *"Add at least five test cases of your own that the AI missed — especially around
security and state transitions — and explain why the AI missed them (prompt quality, model
limitations, or characteristics of the API)."*

Yêu cầu tối thiểu 5 case/API. Em đã bổ sung **6 case/API, tổng 18 case**, tất cả đều
`Source = HUMAN` và đều có cột `Why_AI_Missed` giải trình bằng văn xuôi.

---

## 1. Tổng hợp sau khi bổ sung

| API | Tổng | AI sinh | Em bổ sung | DOM | STA | SEC | SCH | `@contract` | `@bug` |
|---|---|---|---|---|---|---|---|---|---|
| API-1 (FR-03) | 70 | 64 | 6 | 36 | 10 | 18 | 6 | 47 | 23 |
| API-2 (FR-08) | 87 | 81 | 6 | 43 | 22 | 16 | 6 | 58 | 29 |
| API-3 (FR-15) | 86 | 80 | 6 | 53 | 9 | 16 | 8 | 35 | 51 |
| **Tổng** | **243** | **225** | **18** | 132 | 41 | 50 | 20 | 140 | 103 |

Phân bố lý do AI bỏ sót:

| Lý do | Số case | Ý nghĩa |
|---|---|---|
| **API** — đặc điểm của API | 9 | Bug chỉ lộ ra khi **kết hợp nhiều request**; bộ sinh làm việc trên từng case độc lập |
| **MODEL** — giới hạn mô hình | 4 | AI suy diễn từ tên / hình dạng API thay vì đọc mã nguồn |
| **PROMPT** — chất lượng prompt | 3 | Prompt em khoanh vùng quá chật, không yêu cầu rõ điều đó |
| **SPECGAP** — đặc tả không nói | 2 | Đặc tả không mô tả hành vi này nên AI không có gì để bám vào |

**Kết quả đáng chú ý nhất: 9/18 case thuộc nhóm `API`.** Nửa số case mà AI bỏ sót không phải
vì AI kém hay vì prompt dở, mà vì một **giới hạn cấu trúc**: bộ sinh sinh ra các test case
**độc lập**, trong khi một nửa số bug nghiêm trọng của hệ thống này chỉ lộ ra khi **nối hai
hay nhiều request lại với nhau**. Đó là kết luận quan trọng nhất của bước này.

## 2. Độ phủ SEC sau khi bổ sung

| API | Mã SEC được kiểm | Không áp dụng | Giải trình |
|---|---|---|---|
| API-1 | SEC-01(2), SEC-03(1), SEC-04(3), SEC-05(3), SEC-06(1), SEC-07(7) | SEC-02 | Cả hai endpoint chính của FR-03 **không yêu cầu xác thực theo đúng đặc tả** — người quên mật khẩu thì không còn token để mà gửi |
| API-2 | SEC-02(8), SEC-03(3), SEC-04(2), SEC-05(2), SEC-06(1) | SEC-01, SEC-07 | Luồng thanh toán không dùng tới lưu trữ mật khẩu lẫn OTP |
| API-3 | SEC-02(5), SEC-03(3), SEC-04(5), SEC-05(9), SEC-06(1) | SEC-01, SEC-07 | Như trên |
| **Toàn suite** | **SEC-01(2), SEC-02(13), SEC-03(7), SEC-04(10), SEC-05(14), SEC-06(3), SEC-07(7)** | **(không thiếu mã nào)** | |

`TC-A1-SEC-904` đã lấp đầy khoảng trống SEC-03 của API-1 (trước đó là 0) bằng một kịch bản có
thật: `GET /api/admin/users` trả về `login_attempts` và `locked_until` của **mọi người dùng**,
cho phép dò xem tài khoản nào đang bị khóa — đúng là thông tin mà kẻ tấn công luồng quên mật
khẩu cần.

## 3. Sáu case của API-1 (FR-03)

| TC_ID | Tiêu đề | Nhóm | Bug | Lý do AI bỏ sót |
|---|---|---|---|---|
| `TC-A1-STA-901` | Sau reset, mật khẩu **cũ** phải hết hiệu lực và mật khẩu **mới** phải đăng nhập được | STA | — | **API** |
| `TC-A1-SEC-901` | Reset thành công nhưng tài khoản **vẫn bị khóa** | SEC | A-06 | **API** |
| `TC-A1-SEC-902` | `GET /api/users/me` trả về cả `password` lẫn `reset_token` | SEC-01 | A-07 | **PROMPT** |
| `TC-A1-SEC-903` | Tài khoản bị khóa ngay sau **hai** lần sai, trong khi SRS quy định ba | SEC | A-09 | **MODEL** |
| `TC-A1-SEC-904` | User thường đọc được toàn bộ bảng `users` qua `GET /api/admin/users` | SEC-03 | X-01 | **PROMPT** |
| `TC-A1-SEC-905` | OTP của người này dùng được cho email người kia nếu trùng giá trị | SEC-07 | A-02 | **SPECGAP** |

### `TC-A1-SEC-903` — ví dụ điển hình của giới hạn mô hình

SRS FR-02 viết: *"Nếu đăng nhập sai từ **3 lần trở lên** liên tiếp, tài khoản bị tạm khóa."*
Bộ sinh đọc câu này và sinh đúng case tương ứng: sai 3 lần rồi kiểm xem đã khóa chưa. Case đó
**PASS** — vì sai 3 lần thì tất nhiên là đã khóa.

Bug nằm ở **phía còn lại của biên**. Code cộng `login_attempts + 2` mỗi lần sai, nên khóa ngay
từ lần sai thứ **hai**. Muốn thấy phải viết một case khẳng định điều ngược lại: *"sau đúng hai
lần sai, đăng nhập bằng mật khẩu **đúng** vẫn phải thành công"*.

Đây là một thói quen có hệ thống của AI: nó viết case **khẳng định** điều đặc tả nói, chứ rất
ít khi viết case **phủ định** điều đặc tả không nói. Mà biên giới của một yêu cầu thì luôn có
hai phía.

### `TC-A1-SEC-905` — khi đặc tả có vẻ đầy đủ nhưng vẫn hở

Đặc tả nói *"OTP chỉ hợp lệ cho email đã yêu cầu"*, và câu lệnh của SUT có đủ cả hai điều kiện:

```sql
UPDATE users SET password = ?, reset_token = NULL WHERE email = ? AND reset_token = ?
```

Thoạt nhìn là đúng. Cái đặc tả **không** nói là không gian OTP phải đủ lớn để hai người không
trùng mã. Với 4 chữ số (9000 giá trị), chỉ cần khoảng 100 người cùng đang chờ reset thì xác
suất có ít nhất một cặp trùng mã đã vượt 40% (nghịch lý ngày sinh). Khi đó điều kiện
`email AND token` không còn bảo vệ được ai cả. AI không có câu nào trong đặc tả để bám vào nên
không thể sinh case này — đây đúng là định nghĩa của **SPECGAP**.

## 4. Sáu case của API-2 (FR-08)

| TC_ID | Tiêu đề | Nhóm | Bug | Lý do AI bỏ sót |
|---|---|---|---|---|
| `TC-B2-DOM-901` | Checkout `total_amount = 1` rồi **đọc lại đơn hàng** để xác nhận số tiền thật sự được lưu | DOM | B-01 | **API** |
| `TC-B2-DOM-902` | Sau thanh toán thành công, giỏ hàng phải được xóa | DOM | B-13 | **PROMPT** |
| `TC-B2-STA-901` | Chuỗi đầy đủ `pending → confirmed → shipping` rồi user tự hủy: bước cuối phải bị chặn | STA | B-09 | **API** |
| `TC-B2-STA-902` | Chuyển từ `pending` sang chính `pending` phải bị từ chối | STA | — | **MODEL** |
| `TC-B2-SEC-901` | Bỏ `user_id` khỏi `apply-coupon` để dùng mã `VIP100` quá mức cho phép | SEC-02 | B-07 | **MODEL** |
| `TC-B2-SEC-902` | `POST /api/coupon-usage` ghi nhận lượt dùng cho `coupon_id` không tồn tại | SEC | B-11 | **SPECGAP** |

### `TC-B2-SEC-901` — nghịch lý "bỏ bớt dữ liệu để được nhiều quyền hơn"

Bộ sinh coi "thiếu tham số bắt buộc" là một lớp không hợp lệ và sinh case *"thiếu `user_id` →
phải trả 400/401"*. Hợp lý theo phân hoạch miền. Nhưng đọc mã nguồn:

```js
if (user_id) {
  db.get("SELECT COUNT(*) ... FROM coupon_usage WHERE coupon_id = ? AND user_id = ?", ...)
  // ... kiem tra han muc o day
} else {
  // ... ap ma luon, KHONG kiem tra gi
}
```

**Bỏ `user_id` đi không làm yếu đi quyền mà làm biến mất toàn bộ phép kiểm hạn mức.** Đây là
kiểu lỗ hổng không thể suy ra từ hình dạng API — nó chỉ lộ ra khi đọc nhánh `else`. Vì vậy em
viết lại case thành một kịch bản data-driven: chạy 3 vòng với `VIP100` (giới hạn 2 lượt/người)
và khẳng định vòng thứ ba phải bị từ chối.

### `TC-B2-STA-901` — giới hạn của 0-switch coverage

Bộ sinh phủ bảng chuyển trạng thái theo **từng ô riêng lẻ** (0-switch): đặt đơn vào một trạng
thái rồi thử **một** bước chuyển. Nhưng để đưa đơn về `shipping` phải đi qua **đúng hai bước
admin** trước đó. Đó là một chuỗi 4 request liên tiếp, và bộ sinh không thể tự suy ra chuỗi
dẫn nhập từ bảng trạng thái — đó là **1-switch / n-switch coverage**, một mức độ phủ cao hơn
phải thiết kế tay.

### `TC-B2-STA-902` — nằm ở đường chéo bị bỏ trống

Bảng chuyển trạng thái trong spec liệt kê các cặp `(from, to)` **khác nhau**. Nằm ở đường chéo
(`pending → pending`, `confirmed → confirmed`, ...) bị bỏ trống vì trực quan chúng "không phải
một bước chuyển". Độ phủ STA của API-2 vì thế dừng ở **20/25**. Trong thực tế đây lại là loại
ô hay gây lỗi nhất: một request bị gửi lại hai lần do mạng chậm hoặc người dùng bấm hai lần.

## 5. Sáu case của API-3 (FR-15)

| TC_ID | Tiêu đề | Nhóm | Bug | Lý do AI bỏ sót |
|---|---|---|---|---|
| `TC-C3-SCH-901` | Kiểu của `price` phải giống nhau giữa sản phẩm id lẻ và id chẵn | SCH | C-05 | **API** |
| `TC-C3-SEC-901` | Khách vãng lai xóa được **toàn bộ catalog** rồi kiểm số sản phẩm còn lại | SEC-02 | C-01 | **API** |
| `TC-C3-DOM-901` | `PUT` chỉ gửi `name`: các trường không gửi không được bị ghi đè thành `null` | DOM | C-09 | **API** |
| `TC-C3-SCH-902` | Response lỗi phải là `application/json`, không được là HTML | SCH | C-03 | **MODEL** |
| `TC-C3-DOM-902` | Tạo sản phẩm với `category_id` không tồn tại rồi đối chiếu bảng danh mục | DOM | C-10 | **API** |
| `TC-C3-SEC-902` | `UNION SELECT` qua `?search` đọc được mật khẩu plaintext trong bảng `users` | SEC-05 | C-02 | **API** |

### `TC-C3-SCH-901` — vi phạm chỉ tồn tại giữa hai response

Mỗi response riêng lẻ đều hợp lệ: `{"price": 30000000}` đúng schema, và `{"price": "28000000"}`
cũng là một JSON hợp lệ. Vi phạm chỉ hiện ra khi **so sánh hai response với nhau**. Bộ sinh
đánh giá từng case độc lập nên không có chỗ nào để đặt một khẳng định bậc cao hơn liên kết hai
request.

Chi tiết đáng sợ: nếu chỉ test sản phẩm `id = 1` — đúng ID mà mọi ví dụ trong tài liệu đều
dùng — thì **không bao giờ** thấy bug này.

### `TC-C3-SEC-902` — payload SQLi phải được trinh sát từ mã nguồn

Bộ sinh có sinh payload `UNION SELECT` nhưng viết chung chung với số cột tùy ý. `UNION` trong
SQLite **chỉ chạy khi số cột khớp chính xác**; đoán sai số cột thì chỉ nhận được thông báo lỗi
và rất dễ kết luận nhầm là *"hệ thống đã được bảo vệ"* — một **âm tính giả**, kết quả tệ nhất
mà một phép thử bảo mật có thể cho ra.

Payload đúng phải đếm chính xác 5 cột của bảng `products` (`id`, `name`, `price`,
`description`, `imageUrl`, `category_id` — 6 cột, chọn 5 cột khớp kiểu) rồi chọn đúng số cột
tương ứng từ bảng `users`. Đó là bước **trinh sát lấy từ `database.js`**, không thể suy ra từ
đặc tả.

### `TC-C3-SEC-901` — đo hậu quả, không chỉ đo mã trả về

Bộ sinh đã có case *"DELETE không token → phải 401"* và case đó **đã bắt được bug**. Nhưng một
dòng `expected 401, got 200` trong báo cáo không nói lên được mức độ thiệt hại. Case bổ sung
này gọi DELETE cho **cả 5 sản phẩm** mà không kèm token, rồi đọc lại `GET /api/products`:
nếu danh sách rỗng thì một người hoàn toàn không đăng nhập vừa xóa sạch catalog của cửa hàng.

Cùng một bug, nhưng bằng chứng này mới đủ sức thuyết phục người ra quyết định ưu tiên sửa.

## 6. Kết luận STEP 4

- Em đã bổ sung **18 case** (6/API, vượt yêu cầu 5/API), tổng bộ test lên **243 case**.
- Lý do bỏ sót được phân tích cho **từng case**, không gộp chung chung.
- Phát hiện có giá trị nhất: **9/18 case thuộc nhóm `API`** — bộ sinh sinh test case độc lập,
  trong khi một nửa số bug nghiêm trọng chỉ lộ ra khi nối nhiều request lại với nhau. Đây là
  giới hạn **cấu trúc**, không phải giới hạn về prompt hay về mô hình, và em ghi thẳng nó
  vào mục "Hạn chế và hướng mở rộng" của thiết kế bộ sinh (`report/07_test_generator_design.md`).
- **STEP kế tiếp:** STEP 5 — dựng Postman collection từ `testcases/API-*_final.csv`.
