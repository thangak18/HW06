# Nội dung GitHub Issues — ✅ ĐÃ TẠO

**Repo:** [`thangak18/HW06`](https://github.com/thangak18/HW06) · **Người tạo:** 23127195 (`hungtmh`)
· **Ngày tạo:** 2026-09-01

Toàn bộ **24 issue đã được tạo thật**, gắn nhãn `hw06-23127195`:
**[xem danh sách đầy đủ →](https://github.com/thangak18/HW06/issues?q=is%3Aissue+label%3Ahw06-23127195)**

| Mã lỗi | Mức độ | Issue |
|---|---|---|
| `BUG-A1-01` | Critical | [#5](https://github.com/thangak18/HW06/issues/5) |
| `BUG-A1-02` | High | [#6](https://github.com/thangak18/HW06/issues/6) |
| `BUG-A1-03` | Medium | [#7](https://github.com/thangak18/HW06/issues/7) |
| `BUG-A1-04` | Medium | [#8](https://github.com/thangak18/HW06/issues/8) |
| `BUG-A1-05` | Medium | [#9](https://github.com/thangak18/HW06/issues/9) |
| `BUG-A2-01` | Critical | [#10](https://github.com/thangak18/HW06/issues/10) |
| `BUG-A2-02` | Critical | [#11](https://github.com/thangak18/HW06/issues/11) |
| `BUG-A2-03` | High | [#12](https://github.com/thangak18/HW06/issues/12) |
| `BUG-A2-04` | High | [#13](https://github.com/thangak18/HW06/issues/13) |
| `BUG-A2-05` | High | [#14](https://github.com/thangak18/HW06/issues/14) |
| `BUG-A2-06` | Low | [#15](https://github.com/thangak18/HW06/issues/15) |
| `BUG-A2-07` | Low | [#16](https://github.com/thangak18/HW06/issues/16) |
| `BUG-A2-08` | Medium | [#17](https://github.com/thangak18/HW06/issues/17) |
| `BUG-A3-01` | Critical | [#18](https://github.com/thangak18/HW06/issues/18) |
| `BUG-A3-02` | High | [#19](https://github.com/thangak18/HW06/issues/19) |
| `BUG-A3-03` | High | [#20](https://github.com/thangak18/HW06/issues/20) |
| `BUG-A3-04` | Medium | [#21](https://github.com/thangak18/HW06/issues/21) |
| `BUG-A3-05` | Medium | [#22](https://github.com/thangak18/HW06/issues/22) |
| `BUG-A3-06` | Low | [#23](https://github.com/thangak18/HW06/issues/23) |
| `BUG-A3-07` | Low | [#24](https://github.com/thangak18/HW06/issues/24) |
| `BUG-A3-08` | Medium | [#25](https://github.com/thangak18/HW06/issues/25) |
| `BUG-A3-09` | High | [#26](https://github.com/thangak18/HW06/issues/26) |
| `BUG-A3-10` | Low | [#27](https://github.com/thangak18/HW06/issues/27) |
| `BUG-A3-11` | Medium | [#28](https://github.com/thangak18/HW06/issues/28) |

> ⚠️ **Việc còn phải làm bằng tay:** theo §5 của đề bài, mỗi issue cần **đính kèm ảnh chụp màn hình**.
> API không đính được ảnh, nên hãy mở từng issue ở bảng trên, kéo thả ảnh vào ô bình luận, rồi lưu
> bản sao vào `bugs/screenshots/<mã lỗi>.png`. Ảnh có thể chụp Postman (request/response) hoặc
> terminal khi chạy `bash bugs/reproduce_bugs.sh`.

---

## Nội dung gốc của từng issue

Giữ lại làm bản lưu để đối chiếu với nội dung đã đăng.

---

## Issue 1 — BUG-A1-01

> 🔗 Đã đăng: **[#5](https://github.com/thangak18/HW06/issues/5)**

**Tiêu đề:** `[BUG-A1-01][Critical] Leo quyền lên admin qua trường role trong PUT /api/users/me`
**Nhãn:** `bug`, `critical`, `security`, `api-1-fr04`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
`PUT /api/users/me` đọc trường `role` trực tiếp từ body do client gửi và ghi thẳng vào bảng `users`.
Bất kỳ người dùng đã đăng nhập nào cũng tự nâng mình lên quyền quản trị được.

Vi phạm **SEC-06** ("API cập nhật hồ sơ không được cho phép thay đổi trường `role` từ client")
và **FR-04** ("không thể tự thay đổi thuộc tính `role`").

## Các bước tái hiện
1. Đăng nhập bằng tài khoản thường `test@eshop.com` / `Test1234!`, lấy JWT.
2. Gửi request:
   ```bash
   curl -X PUT http://localhost:3000/api/users/me \
     -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127195' \
     -d '{"name":"Test User","shipping_address":"1 Le Loi","phone":"0912345678","role":"admin"}'
   ```
3. Gọi `GET /api/users/me` để đọc lại vai trò.
4. Đăng nhập lại để lấy JWT mới, rồi gọi `GET /api/admin/users`.

## Kết quả kỳ vọng
Trường `role` bị bỏ qua (hoặc trả `400`). Vai trò tài khoản vẫn là `user`.

## Kết quả thực tế
```
{"message":"Profile updated"}
GET /api/users/me     -> role = admin
JWT mới               -> role = admin
GET /api/admin/users  -> HTTP 200, trả về toàn bộ danh sách người dùng
```

## Tác động
Chiếm quyền quản trị toàn hệ thống bằng đúng một request. Sau đó mở được toàn bộ
`/api/admin/*`: xem/xoá người dùng, sửa đơn hàng, sửa giá, quản lý mã giảm giá.

## Vị trí trong mã nguồn
`backend/server.js:114-127`
```js
const { name, shipping_address, phone, role } = req.body;
if (role) { query += ", role = ?"; params.push(role); }
```

## Đề xuất sửa
Bỏ `role` khỏi phép destructuring body. Đổi vai trò phải là endpoint admin riêng có kiểm tra `req.user.role === 'admin'`.

## Test case liên quan
`TC-A1-037`, `TC-A1-038` — xem `testcases/TESTCASES_23127195.xlsx`
```

---

## Issue 2 — BUG-A1-02

> 🔗 Đã đăng: **[#6](https://github.com/thangak18/HW06/issues/6)**

**Tiêu đề:** `[BUG-A1-02][High] GET /api/users/me trả về mật khẩu plaintext và reset_token`
**Nhãn:** `bug`, `high`, `security`, `api-1-fr04`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Endpoint dùng `SELECT *` nên trả nguyên bản ghi người dùng, gồm `password`, `reset_token`,
`login_attempts`, `locked_until`. Vi phạm **SEC-01**.

## Các bước tái hiện
```bash
curl http://localhost:3000/api/users/me -H "Authorization: Bearer $TOKEN" -H 'X-Student-Id: 23127195'
```

## Kết quả kỳ vọng
Chỉ trả `id`, `name`, `email`, `role`, `shipping_address`, `phone`.

## Kết quả thực tế
```json
{"id":2,"name":"Test User","email":"test@eshop.com","password":"Test1234!","role":"user",
 "login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}
```

## Tác động
1. Mật khẩu trả về **đúng nguyên văn** ⇒ hệ thống lưu plaintext, không băm (SEC-01).
2. `reset_token` bị lộ là đường chiếm đoạt tài khoản **độc lập với mật khẩu**.

## Vị trí trong mã nguồn
`backend/server.js:108-112` (`SELECT *`) và `server.js:22` (INSERT không băm mật khẩu).

## Đề xuất sửa
Băm mật khẩu bằng `bcrypt`; liệt kê cột tường minh trong câu `SELECT`.

## Test case liên quan
`TC-A1-039`, `TC-A1-040`, `TC-A1-042`
```

---

## Issue 3 — BUG-A1-03

> 🔗 Đã đăng: **[#7](https://github.com/thangak18/HW06/issues/7)**

**Tiêu đề:** `[BUG-A1-03][Medium] PUT /api/users/me không kiểm tra định dạng số điện thoại`
**Nhãn:** `bug`, `medium`, `api-1-fr04`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
FR-04 quy định số điện thoại phải **bắt đầu bằng `0` và có 10–11 chữ số**. Hệ thống không kiểm tra gì.

## Kết quả thực tế
Mọi giá trị đều trả `{"message":"Profile updated"}`:

| Giá trị | Vi phạm |
|---|---|
| `"abc"` | không phải chữ số |
| `"12345"` | 5 chữ số |
| `"9912345678"` | không bắt đầu bằng 0 |
| `""` | rỗng |
| `"0912-345-678"` | có ký tự phân cách |
| `"+84912345678"` | định dạng quốc tế |
| `"091234567890"` | 12 chữ số |
| `null` | null |

## Tác động
Dữ liệu liên hệ giao hàng bị rác hoá, đơn hàng không liên hệ được với khách.

## Đề xuất sửa
Kiểm tra `/^0\d{9,10}$/` trước khi ghi.

## Test case liên quan
`TC-A1-011` … `TC-A1-020` (10 test case)
```

---

## Issue 4 — BUG-A1-04

> 🔗 Đã đăng: **[#8](https://github.com/thangak18/HW06/issues/8)**

**Tiêu đề:** `[BUG-A1-04][Medium] PUT /api/users/me không kiểm tra họ tên`
**Nhãn:** `bug`, `medium`, `api-1-fr04`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
`name` nhận `""`, `"   "`, `null` và cả số nguyên — tất cả đều trả `200 OK`.

## Kết quả thực tế
```
name=""          -> {"message":"Profile updated"}
name="   "       -> {"message":"Profile updated"}
name=23127195    -> {"message":"Profile updated"}
```

## Kết quả kỳ vọng
`400 Bad Request` — họ tên là trường bắt buộc theo FR-04.

## Tác động
Hồ sơ tồn tại với họ tên rỗng; màn hình chào mừng và thông tin đơn hàng hiển thị trống.

## Đề xuất sửa
Bắt buộc `typeof name === 'string' && name.trim().length > 0`.

## Test case liên quan
`TC-A1-002`, `TC-A1-003`, `TC-A1-004`, `TC-A1-006`
```

---

## Issue 5 — BUG-A1-05

> 🔗 Đã đăng: **[#9](https://github.com/thangak18/HW06/issues/9)**

**Tiêu đề:** `[BUG-A1-05][Medium] Cập nhật một phần hồ sơ xoá trắng các trường không gửi`
**Nhãn:** `bug`, `medium`, `data-loss`, `api-1-fr04`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Câu `UPDATE` luôn gán cả ba cột `name`, `shipping_address`, `phone`. Nếu client chỉ gửi một
trường, hai trường còn lại nhận `undefined` và bị ghi thành `NULL`.

## Các bước tái hiện
1. Đặt hồ sơ đầy đủ: `PUT {"name":"Baseline","shipping_address":"227 Nguyen Van Cu","phone":"0912345678"}`
2. Cập nhật một phần: `PUT {"name":"Chi doi ten"}`
3. `GET /api/users/me`

## Kết quả kỳ vọng
`name` đổi; `phone` và `shipping_address` giữ nguyên.

## Kết quả thực tế
```
trước: name='Baseline'    phone='0912345678'  addr='227 Nguyen Van Cu'
sau:   name='Chi doi ten'  phone=None          addr=None
```

## Tác động
**Mất dữ liệu âm thầm.** Form "đổi tên hiển thị" ở client sẽ xoá địa chỉ giao hàng và
số điện thoại của khách, không ai phát hiện cho tới lúc đặt hàng.

## Vị trí trong mã nguồn
`backend/server.js:116-118`

## Đề xuất sửa
Xây câu `UPDATE` động, chỉ gồm các trường thực sự có trong body.

## Test case liên quan
`TC-A1-028`
```

---

## Issue 6 — BUG-A2-01

> 🔗 Đã đăng: **[#10](https://github.com/thangak18/HW06/issues/10)**

**Tiêu đề:** `[BUG-A2-01][Critical] POST /api/apply-coupon không yêu cầu đăng nhập (vi phạm điều kiện C4)`
**Nhãn:** `bug`, `critical`, `security`, `api-2-fr09`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Endpoint không gắn middleware `authenticateToken`. Một trong **năm** điều kiện bắt buộc
của FR-09 (C4 — "Đã đăng nhập: người dùng phải có JWT Token hợp lệ") **hoàn toàn không được cài đặt**.
Cũng vi phạm **SEC-02**.

## Các bước tái hiện
```bash
curl -X POST http://localhost:3000/api/apply-coupon \
  -H 'Content-Type: application/json' -H 'X-Student-Id: 23127195' \
  -d '{"code":"SAVE10","total_amount":500000}'      # KHÔNG kèm Authorization
```

## Kết quả kỳ vọng
`401 Unauthorized`.

## Kết quả thực tế
```
HTTP 200
{"success":true,"coupon_id":1,"discount_amount":-4500000,"final_amount":5000000,...}
```

## Tác động
Ngoài việc vi phạm C4, đây là bàn đạp cho BUG-A2-04 và BUG-A2-05: không có JWT nên hệ
thống buộc phải tin `user_id` do client gửi, khiến giới hạn số lượt trở nên vô nghĩa.
Kẻ tấn công cũng dò được toàn bộ mã giảm giá đang hoạt động mà không cần tài khoản.

## Vị trí trong mã nguồn
`backend/server.js:360` — thiếu `authenticateToken` (so với `/api/coupon-usage` ở dòng 434 thì có).

## Test case liên quan
`TC-A2-017`, `TC-A2-018`
```

---

## Issue 7 — BUG-A2-02

> 🔗 Đã đăng: **[#11](https://github.com/thangak18/HW06/issues/11)**

**Tiêu đề:** `[BUG-A2-02][Critical] Công thức giảm giá percent sai — khách hàng bị tính tiền gấp 10 lần`
**Nhãn:** `bug`, `critical`, `api-2-fr09`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
FR-09 quy định `discount_amount = total × discount_value / 100`.
Mã nguồn tính `total × (1 − discount_value)`. Với `discount_value = 10` thì thành `−9 × total`.

## Các bước tái hiện
```bash
curl -X POST http://localhost:3000/api/apply-coupon \
  -H 'Content-Type: application/json' -H 'X-Student-Id: 23127195' \
  -d '{"code":"SAVE10","total_amount":500000,"user_id":2}'
```

## Kết quả kỳ vọng
`discount_amount = 50000`, `final_amount = 450000`.

## Kết quả thực tế
| Đơn hàng | discount kỳ vọng | discount thực tế | final thực tế |
|---|---|---|---|
| 500.000 ₫ | 50.000 | **−4.500.000** | **5.000.000** |
| 1.000.000 ₫ | 100.000 | **−9.000.000** | **10.000.000** |

## Tác động
Khách dùng mã giảm 10% phải trả **gấp 10 lần** giá gốc. Ảnh hưởng mọi mã loại `percent`
(`SAVE10`, `EXPIRED`). Mã loại `fixed` tính đúng.

## Vị trí trong mã nguồn
`backend/server.js:394-396` và `410-412` (công thức bị lặp ở hai nhánh):
```js
discount_amount = Math.floor(total_amount * (1 - coupon.discount_value));
// đúng: Math.floor(total_amount * coupon.discount_value / 100)
```

## Đề xuất sửa
Sửa cả hai nhánh và tách thành một hàm tính giảm giá dùng chung.

## Test case liên quan
`TC-A2-032`, `TC-A2-033`, `TC-A2-036`
```

---

## Issue 8 — BUG-A2-03

> 🔗 Đã đăng: **[#12](https://github.com/thangak18/HW06/issues/12)**

**Tiêu đề:** `[BUG-A2-03][High] Ngưỡng đơn hàng dùng > thay vì >= (điều kiện C3 của FR-09)`
**Nhãn:** `bug`, `high`, `api-2-fr09`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
FR-09 điều kiện C3 ghi rõ: "Tổng đơn hàng **>= (lớn hơn hoặc bằng)** `min_order_amount`".
Mã nguồn dùng `>`.

## Kết quả thực tế
| Mã | min_order_amount | Đơn hàng | Kỳ vọng | Thực tế |
|---|---|---|---|---|
| SAVE10 | 300.000 | 299.999 | Từ chối | Từ chối ✅ |
| SAVE10 | 300.000 | **300.000** | **Chấp nhận** | **Từ chối** ❌ |
| SAVE10 | 300.000 | 300.001 | Chấp nhận | Chấp nhận ✅ |
| BIGBUY | 500.000 | **500.000** | **Chấp nhận** | **Từ chối** ❌ |

## Tác động
Đơn hàng đúng bằng ngưỡng — chính là con số quảng cáo trên chương trình khuyến mãi
("đơn từ 300.000 ₫") — bị từ chối, gây khiếu nại.

## Vị trí trong mã nguồn
`backend/server.js:377` — `if (total_amount > coupon.min_order_amount)`

## Test case liên quan
`TC-A2-013`, `TC-A2-015`
```

---

## Issue 9 — BUG-A2-04

> 🔗 Đã đăng: **[#13](https://github.com/thangak18/HW06/issues/13)**

**Tiêu đề:** `[BUG-A2-04][High] Bỏ user_id là vô hiệu hoá hoàn toàn giới hạn số lượt dùng mã (C5)`
**Nhãn:** `bug`, `high`, `security`, `api-2-fr09`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Phép kiểm tra số lượt nằm trong khối `if (user_id) { ... }`. Không gửi `user_id` thì
toàn bộ nhánh kiểm tra C5 bị bỏ qua.

## Các bước tái hiện
1. Ghi 1 lượt dùng `SAVE10` cho user id=2: `POST /api/coupon-usage {"coupon_id":1}`
   (`SAVE10` có `max_uses_per_user = 1`).
2. Áp mã có `user_id`: bị chặn đúng.
3. Áp mã **không** kèm `user_id`: được chấp nhận.

## Kết quả thực tế
```
có user_id=2  -> {"error":"Bạn đã sử dụng mã này 1 lần (đã đạt giới hạn)"}
BỎ user_id    -> {"success":true, ...}      ← lách được
```

## Tác động
Mã "1 lượt/người" trở thành không giới hạn. Kết hợp BUG-A2-01 (không cần đăng nhập),
bất kỳ ai cũng dùng lại mã vô số lần.

## Vị trí trong mã nguồn
`backend/server.js:384` — `if (user_id) {`

## Đề xuất sửa
Lấy định danh từ `req.user.id` (JWT), không từ body; C5 phải luôn được kiểm tra.

## Test case liên quan
`TC-A2-024`
```

---

## Issue 10 — BUG-A2-05

> 🔗 Đã đăng: **[#14](https://github.com/thangak18/HW06/issues/14)**

**Tiêu đề:** `[BUG-A2-05][High] IDOR — mượn lượt dùng mã giảm giá của người khác qua user_id`
**Nhãn:** `bug`, `high`, `security`, `api-2-fr09`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
`user_id` lấy từ body và không đối chiếu với chủ thể trong JWT. Người dùng đã hết lượt
chỉ cần đổi sang `user_id` của tài khoản khác.

## Kết quả thực tế
```
user_id=2 (đã hết lượt)     -> {"error":"Bạn đã sử dụng mã này 1 lần"}
user_id=1 (tài khoản khác)  -> {"success":true, ...}
```

## Tác động
Giới hạn số lượt không tồn tại trên thực tế. `user_id` là số nguyên tuần tự nên kẻ tấn
công chỉ cần tăng dần để tìm tài khoản còn lượt.

## Đề xuất sửa
Bỏ hẳn `user_id` khỏi body, dùng `req.user.id`.

## Test case liên quan
`TC-A2-025`
```

---

## Issue 11 — BUG-A2-06

> 🔗 Đã đăng: **[#15](https://github.com/thangak18/HW06/issues/15)**

**Tiêu đề:** `[BUG-A2-06][Low] Thứ tự kiểm tra điều kiện làm thông báo lỗi sai lệch (mã hết hạn báo thành chưa đủ ngưỡng)`
**Nhãn:** `bug`, `low`, `api-2-fr09`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Phép kiểm tra hạn dùng (C2) nằm **bên trong** nhánh kiểm tra ngưỡng (C3). Khi mã vừa hết
hạn vừa chưa đủ ngưỡng, hệ thống chỉ báo lỗi ngưỡng.

## Kết quả thực tế
```
EXPIRED, đơn 500.000 (≥ ngưỡng)  -> "Mã giảm giá đã hết hạn"                     ✅
EXPIRED, đơn  50.000 (< ngưỡng)  -> "Đơn hàng chưa đủ giá trị tối thiểu 100.000" ❌
```

## Tác động
Khách được dẫn đi mua thêm hàng cho đủ ngưỡng, rồi vẫn không dùng được mã vì mã đã hết
hạn từ 2020. Thông báo này cũng che mất nguyên nhân thật với bộ phận hỗ trợ.

## Đề xuất sửa
Kiểm tra tuần tự đúng thứ tự C1 → C2 → C3 → C4 → C5, mỗi điều kiện một nhánh phẳng.

## Test case liên quan
`TC-A2-010`
```

---

## Issue 12 — BUG-A2-07

> 🔗 Đã đăng: **[#16](https://github.com/thangak18/HW06/issues/16)**

**Tiêu đề:** `[BUG-A2-07][Low] Mã giảm giá phân biệt chữ hoa/thường`
**Nhãn:** `bug`, `low`, `ux`, `api-2-fr09`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
`SAVE10` → `200 OK`, `save10` → `404 Not Found`.

## Tác động
Mã giảm giá được in trên tờ rơi, đọc qua điện thoại hoặc gõ tay. Bắt buộc gõ đúng chữ hoa
làm tăng tỉ lệ nhập thất bại, trong khi thông báo trả về ("Mã giảm giá không tồn tại")
khiến khách tưởng mình bị cho mã sai.

## Đề xuất sửa
`WHERE UPPER(code) = UPPER(?)`

## Test case liên quan
`TC-A2-006`
```

---

## Issue 13 — BUG-A2-08

> 🔗 Đã đăng: **[#17](https://github.com/thangak18/HW06/issues/17)**

**Tiêu đề:** `[BUG-A2-08][Medium] Không kiểm tra miền giá trị total_amount — tràn số nguyên an toàn`
**Nhãn:** `bug`, `medium`, `api-2-fr09`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
`total_amount` không được kiểm tra: giá trị `0`, số âm, `null` và chuỗi phi số đều lọt qua.
Với giá trị rất lớn thì kết quả vượt `Number.MAX_SAFE_INTEGER`.

## Kết quả thực tế
```
total_amount = 1000000000000000
-> {"discount_amount":-9000000000000000,"final_amount":10000000000000000}
```
`10000000000000000 > Number.MAX_SAFE_INTEGER (9007199254740991)` ⇒ mọi phép tính tiền từ
ngưỡng này không còn đảm bảo chính xác.

## Đề xuất sửa
Kiểm tra `Number.isSafeInteger(total_amount) && total_amount > 0` trước khi tính.

## Test case liên quan
`TC-A2-044`; và `TC-A2-038` … `TC-A2-042` cho các giá trị 0 / âm / null / chuỗi
```

---

## Issue 14 — BUG-A3-01

> 🔗 Đã đăng: **[#18](https://github.com/thangak18/HW06/issues/18)**

**Tiêu đề:** `[BUG-A3-01][Critical] Người dùng thường import được sản phẩm lên cửa hàng (thiếu kiểm tra role admin)`
**Nhãn:** `bug`, `critical`, `security`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
`POST /api/admin/import-products` chỉ dùng `authenticateToken` (xác thực) mà không kiểm
tra vai trò (phân quyền). Đúng tình huống mà **SEC-03** mô tả: *"API Admin phải kiểm tra
`role = 'admin'` trong Token, **không chỉ** kiểm tra sự tồn tại của Token"*. Cũng vi phạm **FR-12**.

## Các bước tái hiện
```bash
# JWT của test@eshop.com (role = user)
curl -X POST http://localhost:3000/api/admin/import-products \
  -H "Authorization: Bearer $USER_TOKEN" -H 'Content-Type: application/json' \
  -H 'X-Student-Id: 23127195' \
  -d '{"products":[{"name":"HANG-GIA-DO-USER-CHEN","price":1,"category_id":1}]}'

curl "http://localhost:3000/api/products?search=HANG-GIA-DO-USER-CHEN"
```

## Kết quả kỳ vọng
`403 Forbidden`; không bản ghi nào được ghi.

## Kết quả thực tế
```
{"message":"Import hoàn tất: 1/1 sản phẩm được thêm","inserted":1,"errors":[]}
[{"id":6,"name":"HANG-GIA-DO-USER-CHEN","price":1,...}]    ← hiện công khai trên cửa hàng
```

## Tác động
Bất kỳ khách vãng lai nào đăng ký tài khoản đều chèn được hàng lên cửa hàng — kèm tên,
giá, mô tả và **đường dẫn ảnh do họ kiểm soát**. Kết hợp BUG-A3-11 (`imageUrl` chấp nhận
`javascript:`) trở thành đường tấn công stored XSS nhắm vào mọi khách xem trang chủ.

## Vị trí trong mã nguồn
`backend/server.js:188`. Lưu ý: **toàn bộ** các endpoint `/api/admin/*` khác cũng mắc lỗi này.

## Đề xuất sửa
Thêm middleware `requireAdmin` và áp cho mọi route `/api/admin/*`.

## Test case liên quan
`TC-A3-040`, `TC-A3-041`
```

---

## Issue 15 — BUG-A3-02

> 🔗 Đã đăng: **[#19](https://github.com/thangak18/HW06/issues/19)**

**Tiêu đề:** `[BUG-A3-02][High] Import sản phẩm không nguyên tử — không rollback khi có dòng lỗi`
**Nhãn:** `bug`, `high`, `data-integrity`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
FR-16 yêu cầu: *"Nếu có lỗi ở bất kỳ dòng nào, toàn bộ import phải được rollback (giao dịch
nguyên tử — all-or-nothing)"*. Mã nguồn duyệt mảng bằng `forEach` và gọi `stmt.run()` cho
từng dòng, không mở transaction.

## Các bước tái hiện
```bash
# đếm số sản phẩm trước
curl http://localhost:3000/api/products | jq length

curl -X POST http://localhost:3000/api/admin/import-products \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -H 'X-Student-Id: 23127195' \
  -d '{"products":[{"name":"ATOMIC-OK","price":5000,"category_id":1},{"price":7000,"category_id":1}]}'

# đếm lại
curl http://localhost:3000/api/products | jq length
```

## Kết quả kỳ vọng
`inserted = 0`; số sản phẩm **không đổi**.

## Kết quả thực tế
```
số sản phẩm trước : 6
{"message":"Import hoàn tất: 1/2 sản phẩm được thêm","inserted":1,"errors":["Hàng 3: Thiếu tên sản phẩm"]}
số sản phẩm sau   : 7        ← dòng hợp lệ đã được ghi
```
Kiểm chứng thêm: lỗi ở **đầu** mảng và lỗi ở **cuối** mảng cho kết quả khác nhau, xác nhận
cơ chế là "chạy tuần tự, bỏ qua dòng lỗi" chứ không phải giao dịch.

## Tác động
Import file 500 dòng có 1 dòng sai sẽ để lại trạng thái **nửa vời**: 499 sản phẩm đã lên
sàn, không có cách thu hồi ngoài xoá tay. Chạy lại file sau khi sửa sẽ tạo 499 bản ghi **trùng lặp**.

## Vị trí trong mã nguồn
`backend/server.js:196-228`

## Đề xuất sửa
`BEGIN TRANSACTION` → validate toàn bộ dòng trước → có lỗi thì `ROLLBACK`, không thì `COMMIT`.

## Test case liên quan
`TC-A3-032`, `TC-A3-033`, `TC-A3-034`, `TC-A3-036`
```

---

## Issue 16 — BUG-A3-03

> 🔗 Đã đăng: **[#20](https://github.com/thangak18/HW06/issues/20)**

**Tiêu đề:** `[BUG-A3-03][High] Import không kiểm tra price (chấp nhận 0, số âm, null, thiếu trường)`
**Nhãn:** `bug`, `high`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
FR-16 yêu cầu "`price` phải là số dương". Mã nguồn chỉ có `if (!row.name)`, hoàn toàn
không kiểm tra `price`.

## Kết quả thực tế
Mọi giá trị đều được ghi với `{"inserted":1,"errors":[]}`:

| price | Vi phạm |
|---|---|
| `0` | không phải số dương |
| `-50000` | số âm |
| `null` | thiếu giá trị |
| *(thiếu trường)* | thiếu trường bắt buộc |

## Tác động
Sản phẩm giá `0 ₫` hoặc **giá âm** lên sàn. Giá âm khiến tổng tiền đơn hàng bị trừ đi —
kết hợp FR-08 (backend nhận `total_amount` từ client) có thể tạo đơn hàng giá trị âm.

## Vị trí trong mã nguồn
`backend/server.js:202-205`

## Test case liên quan
`TC-A3-018`, `TC-A3-019`, `TC-A3-022`, `TC-A3-023`
```

---

## Issue 17 — BUG-A3-04

> 🔗 Đã đăng: **[#21](https://github.com/thangak18/HW06/issues/21)**

**Tiêu đề:** `[BUG-A3-04][Medium] price là chuỗi phi số vẫn được ghi vào cột số`
**Nhãn:** `bug`, `medium`, `data-integrity`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
`price: "khong-phai-so"` → `{"inserted":1}`. SQLite với affinity `INTEGER` lưu nguyên
chuỗi khi không ép kiểu được.

## Tác động
Đây là kịch bản **mặc định** của tính năng import CSV: mọi trường parse từ CSV đều là chuỗi.
Một ô Excel dính chữ ("10.000 đ") tạo ra bản ghi có giá là chuỗi, khiến mọi phép cộng tổng
tiền phía sau nối chuỗi thay vì cộng số.

## Đề xuất sửa
```js
const price = Number(row.price);
if (!Number.isFinite(price) || price <= 0) { /* báo lỗi dòng */ }
```

## Test case liên quan
`TC-A3-020`, `TC-A3-021`
```

---

## Issue 18 — BUG-A3-05

> 🔗 Đã đăng: **[#22](https://github.com/thangak18/HW06/issues/22)**

**Tiêu đề:** `[BUG-A3-05][Medium] Import không kiểm tra khoá ngoại category_id`
**Nhãn:** `bug`, `medium`, `data-integrity`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
FR-15 quy định "Danh mục: bắt buộc, phải chọn từ danh sách có sẵn". `category_id` bằng
`999`, `0` hoặc `-1` đều được chấp nhận (`inserted: 1`).

## Tác động
Sản phẩm gắn vào danh mục không tồn tại **không hiển thị ở bất kỳ trang danh mục nào** —
hàng biến mất khỏi cửa hàng mà quản trị viên không nhận được cảnh báo nào.

## Test case liên quan
`TC-A3-025`, `TC-A3-026`, `TC-A3-027`
```

---

## Issue 19 — BUG-A3-06

> 🔗 Đã đăng: **[#23](https://github.com/thangak18/HW06/issues/23)**

**Tiêu đề:** `[BUG-A3-06][Low] Tên sản phẩm toàn khoảng trắng lọt qua phép kiểm tra`
**Nhãn:** `bug`, `low`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Phép kiểm tra là `if (!row.name)`. Chuỗi `"     "` là **truthy** trong JavaScript nên lọt
qua, tạo ra sản phẩm không tên.

## Kết quả thực tế
```
name="     " -> {"message":"Import hoàn tất: 1/1 sản phẩm được thêm","inserted":1,"errors":[]}
```

## Đề xuất sửa
`if (!row.name || !String(row.name).trim())`

## Test case liên quan
`TC-A3-013`
```

---

## Issue 20 — BUG-A3-07

> 🔗 Đã đăng: **[#24](https://github.com/thangak18/HW06/issues/24)**

**Tiêu đề:** `[BUG-A3-07][Low] Import không giới hạn 255 ký tự cho tên sản phẩm`
**Nhãn:** `bug`, `low`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
FR-15 quy định "Tên sản phẩm: bắt buộc, tối đa 255 ký tự". Tên dài 300 ký tự vẫn được ghi.

## Kết quả thực tế
```
name (300 ký tự) -> {"inserted":1,"errors":[]}
```

## Test case liên quan
`TC-A3-014` (255 ký tự — PASS), `TC-A3-015` (256 ký tự — FAIL)
```

---

## Issue 21 — BUG-A3-08

> 🔗 Đã đăng: **[#25](https://github.com/thangak18/HW06/issues/25)**

**Tiêu đề:** `[BUG-A3-08][Medium] Thiếu category_id bị âm thầm gán mặc định, báo cáo vẫn nói thành công`
**Nhãn:** `bug`, `medium`, `data-integrity`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Dòng thiếu hẳn `category_id` được ghi với `category_id = 1` (`row.category_id || 1` ở
`server.js:213`), và báo cáo trả về `{"inserted":1,"errors":[]}` — không hề có cảnh báo.

## Kết quả thực tế
```
gửi: {"name":"NOCAT","price":1000}          (không có category_id)
-> {"message":"Import hoàn tất: 1/1 sản phẩm được thêm","inserted":1,"errors":[]}
-> đọc lại: category_id = 1
```

## Tác động
Nguy hiểm hơn một lỗi báo sai, vì đây là **lỗi im lặng**: cả lô hàng bị xếp nhầm vào danh
mục "Điện thoại" trong khi báo cáo nói import thành công 100%. Không ai phát hiện cho tới
khi khách hàng phản ánh.

## Test case liên quan
`TC-A3-028`
```

---

## Issue 22 — BUG-A3-09

> 🔗 Đã đăng: **[#26](https://github.com/thangak18/HW06/issues/26)**

**Tiêu đề:** `[BUG-A3-09][High] Phần tử null trong mảng products gây crash 500 và lộ stack trace máy chủ`
**Nhãn:** `bug`, `high`, `security`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Dòng rỗng (phần tử `null`) trong mảng làm sập request và trả về trang HTML lỗi mặc định
của Express, kèm stack trace.

## Các bước tái hiện
```bash
curl -X POST http://localhost:3000/api/admin/import-products \
  -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' \
  -H 'X-Student-Id: 23127195' \
  -d '{"products":[{"name":"OK","price":1000,"category_id":1},null]}'
```

## Kết quả kỳ vọng
`400 Bad Request` với thông báo JSON nêu rõ dòng bị lỗi.

## Kết quả thực tế
`HTTP 500` kèm HTML:
```html
<pre>TypeError: Cannot read properties of null (reading 'name')
    at D:\...\backend\server.js:214:14
    at Array.forEach (&lt;anonymous&gt;)
    at Layer.handleRequest (...\node_modules\router\lib\layer.js:152:17)
```

## Tác động
1. Dòng rỗng trong file CSV xuất từ Excel là chuyện thường ngày, và nó làm sập request
   thay vì báo lỗi tử tế.
2. Response **lộ đường dẫn tuyệt đối trên máy chủ, cấu trúc thư mục và phiên bản thư viện** —
   thông tin hữu ích cho bước tấn công tiếp theo.

## Đề xuất sửa
Kiểm tra `row && typeof row === 'object'` cho từng phần tử; cấu hình error handler chung
trả JSON và ẩn stack trace ở môi trường production.

## Test case liên quan
`TC-A3-008`
```

---

## Issue 23 — BUG-A3-10

> 🔗 Đã đăng: **[#27](https://github.com/thangak18/HW06/issues/27)**

**Tiêu đề:** `[BUG-A3-10][Low] Mất chính xác với price vượt khoảng số nguyên an toàn`
**Nhãn:** `bug`, `low`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Giá trị vượt `Number.MAX_SAFE_INTEGER` bị làm tròn âm thầm, không có cảnh báo.

## Kết quả thực tế
```
gửi lên : 9007199254740993
lưu lại : 9007199254740992      (lệch −1)
```

## Tác động
Thấp trong bối cảnh giá hàng thực tế, nhưng là lỗi im lặng. Ghi nhận để hoàn thiện phần
kiểm tra miền giá trị.

## Đề xuất sửa
Kiểm tra `Number.isSafeInteger(price)`.

## Test case liên quan
`TC-A3-024`
```

---

## Issue 24 — BUG-A3-11

> 🔗 Đã đăng: **[#28](https://github.com/thangak18/HW06/issues/28)**

**Tiêu đề:** `[BUG-A3-11][Medium] imageUrl chấp nhận giao thức javascript: (vector stored XSS)`
**Nhãn:** `bug`, `medium`, `security`, `api-3-fr16`, `hw06-23127195`

**Nội dung:**
```markdown
## Mô tả
Trường `imageUrl` không kiểm tra giao thức và được đổ thẳng vào thuộc tính `src` của thẻ
`<img>` trên giao diện.

## Kết quả thực tế
```
imageUrl gửi lên : "javascript:alert(document.cookie)"
imageUrl lưu lại : "javascript:alert(document.cookie)"
```

## Tác động
Kết hợp với BUG-A3-01 (người dùng thường import được), đây là vector **stored XSS** hoàn
chỉnh: kẻ tấn công không cần chạm vào `name` hay `description` — hai trường mà lập trình
viên thường nhớ escape.

## Đề xuất sửa
Chỉ chấp nhận `imageUrl` có giao thức `http:`/`https:` hoặc đường dẫn tương đối.

## Test case liên quan
`TC-A3-044`
```
