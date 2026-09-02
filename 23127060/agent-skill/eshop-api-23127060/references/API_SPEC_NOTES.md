# API_SPEC_NOTES — Bản đồ endpoint, tham số, và bug đã biết (HW06, SV 23127060)

> Nguồn: đọc trực tiếp `eshop-sut/backend/server.js` (Express + sqlite3) và
> `eshop-sut/api_specification.md`.
> **Agent PHẢI đối chiếu lại với `api_specification.md` thật trong repo ở STEP 0.**
> Nếu spec khác file này => báo CRITICAL [C3].
>
> Ghi chú: các chuỗi trong cột "Bằng chứng thực nghiệm" là **nguyên văn response của SUT**
> (kể cả phần tiếng Việt không dấu do chính máy chủ trả về) — giữ nguyên, không dịch.

---

## 0. Thông tin chung

- Base URL: `http://localhost:3000`
- Auth: JWT Bearer. `Authorization: Bearer <token>`. Secret hardcode trong source:
  `super_secret_key_that_should_not_be_here` (đây là bug SEC).
- Middleware `authenticateToken`: thiếu token -> `401 {error:"Unauthorized"}`,
  token sai -> `403 {error:"Forbidden"}`. **Không hề kiểm tra `role` ở bất kỳ đâu.**
- Header bắt buộc của đề bài: `X-Student-Id: 23127060` (SUT không dùng, nhưng giảng viên chấm).
- DB: SQLite. `database.js` gọi `initDatabase()` ngay khi `require` =>
  **mỗi lần restart backend là DROP + reseed toàn bộ DB**. Ghi nhớ khi thiết kế
  precondition và khi chạy CI.

### Bảng dữ liệu gốc sau khi seed
- `users`: 2 user seed (1 admin, 1 user thường). Cột: `id, name, email, password (PLAINTEXT),
  role, phone, shipping_address, login_attempts, locked_until, reset_token`.
- `products`: 5 sản phẩm. Cột: `id, name, price, description, imageUrl, category_id`.
- `categories`, `orders` (`id,user_id,total_amount,status,shipping_address`),
  `coupons` (`id,code,type,discount_value,min_order_amount,max_uses_per_user,expired_at,is_active`),
  `coupon_usage` (`id,coupon_id,user_id`).
- Order status hợp lệ (FR-10): `pending -> confirmed -> shipping -> delivered`,
  hủy: `pending|confirmed -> canceled`.

### Mapping SEC-01..SEC-07 (ĐÃ XÁC NHẬN ở STEP 0 — nguồn: `eshop-sut/README.md` mục 9)

> **[C3] ĐÃ SỬA:** bản trước của file này ghi một bảng SEC **tự suy diễn** (SQLi=SEC-01,
> IDOR=SEC-04...). Đối chiếu với `eshop-sut/README.md` mục 9 "Yêu cầu Bảo mật" cho thấy
> bảng đó **sai hoàn toàn**. Dưới đây là bảng THẬT, là oracle duy nhất được dùng.

| Mã | Yêu cầu (nguyên văn rút gọn) | Áp dụng cho API |
|---|---|---|
| SEC-01 | Mật khẩu **không** được lưu plaintext | API-1 |
| SEC-02 | Các API có tính bảo mật phải yêu cầu JWT Token hợp lệ | API-2, API-3 |
| SEC-03 | API Admin phải kiểm tra `role='admin'` trong token, không chỉ kiểm tra token tồn tại | API-2, API-3 |
| SEC-04 | Dữ liệu user nhập phải được escape khi hiển thị (không `innerHTML`) — stored XSS | API-3 |
| SEC-05 | Truy vấn CSDL phải dùng Parameterized Query, không nối chuỗi | API-3 |
| SEC-06 | API cập nhật hồ sơ **không được** cho đổi trường `role` từ client | API-2, API-3 (chuỗi leo thang quyền) |
| SEC-07 | OTP đặt lại mật khẩu phải đủ entropy (**tối thiểu 6 chữ số**), **có thời hạn**, **vô hiệu hóa sau khi dùng** | API-1 |

**Lưu ý quan trọng về phạm vi:** SEC-04 nói về tầng hiển thị (UI). Ở tầng API ta chỉ kiểm
được **về nửa**: server có lưu nguyên payload `<script>` không (stored XSS source). Ghi rõ
giới hạn này trong báo cáo, không được nói "đã test đầy đủ SEC-04 trên API".

### Oracle: 2 tài liệu, không phải 1

| Tài liệu | Vai trò |
|---|---|
| `eshop-sut/README.md` | **SRS — nghiệp vụ ĐÚNG** (FR-01..FR-24, SEC-01..07). Đây là oracle `SPEC`. |
| `eshop-sut/api_specification.md` | Chỉ là hướng dẫn gọi API (endpoint + body mẫu), **không** phải oracle nghiệp vụ. |
| `eshop-sut/backend/server.js` | Hành vi thực tế. Đây là oracle `IMPL`. |

Khi `api_specification.md` và `README.md` khác nhau => **lấy `README.md` làm chuẩn**,
vì nó là tài liệu duy nhất tự tuyên bố "Mô tả yêu cầu nghiệp vụ **đúng** của hệ thống".

---

## 1. API-1 — Pool A / FR-03: Quên mật khẩu & Đặt lại mật khẩu

### 1.1 `POST /api/forgot-password`
**Auth:** không. **Body:** `{ email }`

| Trường | Kiểu | Ràng buộc theo spec | Phân hoạch miền |
|---|---|---|---|
| `email` | string | bắt buộc, đúng định dạng email, phải tồn tại | hợp lệ / sai định dạng / rỗng / null / thiếu key / không tồn tại / SQLi / >254 ký tự / unicode / có khoảng trắng đầu-cuối / hoa-thường |

**Response impl:**
- 200 `{ message: "Ma dat lai mat khau da duoc tao", resetToken: "<4 chu so>" }`
- 404 `{ error: "User not found" }`
- 500 `{ error }`

### 1.2 `POST /api/reset-password`
**Auth:** không. **Body:** `{ email, resetToken, newPassword }`

| Trường | Kiểu | Ràng buộc theo spec | Phân hoạch miền |
|---|---|---|---|
| `email` | string | bắt buộc, khớp với token | đúng / sai / rỗng / null / của user khác |
| `resetToken` | string | bắt buộc, đúng, còn hạn, dùng 1 lần | đúng / sai / rỗng / null / đã dùng / của user khác / kiểu số thay vì chuỗi / SQLi |
| `newPassword` | string | >=8 ký tự, có hoa+thường+số | hợp lệ / <8 / rỗng / null / chỉ số / 1000 ký tự / trùng mật khẩu cũ / có khoảng trắng / unicode |

**Response impl:**
- 200 `{ message: "Password reset successfully" }`
- 400 `{ error: "Invalid token or email" }`

### 1.3 Bug đã biết (API-1) — **ĐÃ KIỂM CHỨNG BẰNG REQUEST THẬT ở STEP 0**

| ID | Mức | SEC / FR bị vi phạm | Mô tả | Bằng chứng thực nghiệm |
|---|---|---|---|---|
| **A-01** | Critical | SEC-07 | `forgot-password` trả thẳng `resetToken` trong response body. Bất kỳ ai biết email đều chiếm được tài khoản. | `POST /api/forgot-password {"email":"api.victim..."}` -> `200 {"message":"Ma dat lai mat khau da duoc tao","resetToken":"5740"}` |
| **A-02** | High | SEC-07 | Token chỉ **4 chữ số** (`Math.floor(1000+Math.random()*9000)`). SRS FR-03 + SEC-07 đòi **6 chữ số**. Không giới hạn số lần thử => vét brute-force tối đa 9000. | token quan sát được: `"5740"` (4 ký tự) |
| **A-03** | High | — (lộ thông tin) | User enumeration: email không tồn tại -> `404 {"error":"User not found"}`; email tồn tại -> `200`. Dò được danh sách user. | `POST /api/forgot-password {"email":"nobody..."}` -> `HTTP/1.1 404` |
| **A-04** | High | SEC-07 | Token **không có hạn sử dụng**: cột `reset_token` không kèm timestamp, không có bất kỳ phép so sánh thời gian nào. | `database.js` schema `users`; `server.js` reset-password |
| **A-05** | High | FR-01 / FR-03 | `reset-password` **không validate độ mạnh mật khẩu**. SRS đòi >=8 ký tự, có hoa+thường+số+ký tự đặc biệt. Chấp nhận `"1"`, `""`. | không có nhánh kiểm tra nào trong handler |
| **A-06** | Medium | FR-02 | Reset thành công **không xóa `login_attempts` / `locked_until`** => đổi mật khẩu xong vẫn bị khóa. | `UPDATE users SET password=?, reset_token=NULL ...` |
| **A-07** | Critical | SEC-01 | Mật khẩu lưu **plaintext**; `POST /api/login` và `GET /api/users/me` trả về nguyên bản ghi `user` gồm `password` và `reset_token`. | login -> `"user":{...,"password":"Api1234!","reset_token":null}` |
| **A-08** | Medium | — | `forgot-password` **bỏ qua biến `err`** của `db.get` => lỗi DB bị báo thành 404 "User not found". | `(err, user) => { if (!user) return 404 }` |
| **A-09** | High | FR-02 | Bộ đếm đăng nhập sai cộng **+2** mỗi lần (`user.login_attempts + 2`) => khóa sau **2** lần sai chứ không phải 3. Ngoài ra khóa **180000ms = 180s** trong khi SRS ghi **30s**. | `const newAttempts = user.login_attempts + 2;` `Date.now() + 180000` |
| **A-10** | Low | — | `reset-password` chỉ kiểm `this.changes === 0`, **không kiểm `err`** => lỗi DB trả về 200 "Password reset successfully". | callback `function (err)` không dùng `err` |
| **A-11** | High | SEC-07 | Xin token lần 2 **ghi đè** token lần 1 nhưng không có cơ chế vô hiệu hóa/thu hồi rõ ràng; token cũ im lặng chết, không có thông báo. Kết hợp A-04 => vòng đời token không xác định. | 2 lần `forgot-password` liên tiếp |

> **A-01, A-02, A-03, A-07 đã có response thật lưu trong `bugs/BUG_REPORT.md`.**

---

## 2. API-2 — Pool B / FR-08: Thanh toán (+ FR-09 coupon, FR-10 state machine)

### 2.1 `POST /api/checkout`
**Auth:** có (`authenticateToken`). **Body:** `{ total_amount, shipping_address }`
(FE còn gửi `items`, `coupon_id` nhưng **backend bỏ qua hoàn toàn**).

| Trường | Kiểu | Ràng buộc theo spec | Phân hoạch miền |
|---|---|---|---|
| `total_amount` | number | > 0, phải khớp tổng giỏ hàng server-side | dương / 0 / âm / chuỗi số / chuỗi chữ / null / thiếu / rất lớn (1e18) / thập phân / NaN |
| `shipping_address` | string | bắt buộc, không rỗng | hợp lệ / rỗng / null / thiếu / 1000 ký tự / XSS payload / unicode |
| `items` | array | phải có >=1 item tồn tại | (spec yêu cầu, impl bỏ qua) |

**Response impl:** 200 `{ message:"Checkout successful", orderId:<int> }` | 401 | 403 | 500

### 2.2 `POST /api/apply-coupon`
**Auth: KHÔNG** (bug). **Body:** `{ code, total_amount, user_id }`

| Trường | Phân hoạch miền |
|---|---|
| `code` | tồn tại+active / tồn tại+inactive / không tồn tại / rỗng / null / thiếu / SQLi / khác hoa-thường |
| `total_amount` | > min / = min (biên!) / < min / 0 / âm / chuỗi |
| `user_id` | của mình / của người khác / không gửi / id không tồn tại |

### 2.3 State machine (FR-10)
- `PUT /api/orders/:id/cancel` (auth, chỉ order của mình)
- `PUT /api/admin/orders/:id/status` (auth, **không check role**) body `{ status }`
- `GET /api/orders/:id` — **không auth** (bug)
- `GET /api/orders/my-orders` — auth

Bảng chuyển trạng thái cần test đầy đủ (5 trạng thái x 5 đích = 25 ô):

| Từ \ Đến | pending | confirmed | shipping | delivered | canceled |
|---|---|---|---|---|---|
| **pending** | ✗ | ✓ | ✗ | ✗ | ✓ |
| **confirmed** | ✗ | ✗ | ✓ | ✗ | ✓ |
| **shipping** | ✗ | ✗ | ✗ | ✓ | ✗ (impl cho phép qua `/cancel` — BUG) |
| **delivered** | ✗ | ✗ | ✗ | ✗ | ✗ |
| **canceled** | ✗ | ✗ | ✗ | ✗ (impl cho phép — BUG) | ✗ |

### 2.4 Bug đã biết (API-2) — **ĐÃ KIỂM CHỨNG BẰNG REQUEST THẬT ở STEP 0**

| ID | Mức | SEC / FR bị vi phạm | Mô tả | Bằng chứng thực nghiệm |
|---|---|---|---|---|
| **B-01** | Critical | FR-08 | `checkout` **tin tuyệt đối `total_amount` từ client**. SRS FR-08: "Backend phải tự tính lại tổng tiền; không chấp nhận `total_amount` do client gửi lên". | `POST /api/checkout {"total_amount":1,...}` -> `200 {"orderId":1}`; `GET /api/orders/1` -> `"total_amount":1` |
| **B-01b** | Critical | FR-08 | Chấp nhận cả `total_amount` **âm**. | `{"total_amount":-500000}` -> `200 {"orderId":2}` |
| **B-02** | Critical | SEC-02 | `GET /api/orders/:id` **thiếu `authenticateToken`** => IDOR, đọc được đơn hàng của bất kỳ ai chỉ bằng id. | `curl /api/orders/1` không header -> `200 {"id":1,"user_id":3,...}` |
| **B-03** | Critical | SEC-03 | `PUT /api/admin/orders/:id/status` có token nhưng **không kiểm `role`** => user thường đổi trạng thái đơn của **người khác**. | attacker(id=4) đổi đơn của victim(id=3) -> `200 {"message":"Order status updated"}` |
| **B-04** | High | FR-08 | `checkout` **bỏ qua `items` hoàn toàn**: đơn tạo ra không có dòng hàng, không trừ tồn kho, không validate sản phẩm. | destructuring chỉ lấy `total_amount`, `shipping_address` |
| **B-05** | Critical | FR-09 | Công thức `percent` sai: `discount = floor(total*(1-discount_value))`. Đúng phải là `total*discount_value/100`. Với `discount_value=10` => **discount âm** => `final_amount > total`. | `SAVE10` trên `500000` -> `{"discount_amount":-4500000,"final_amount":5000000}` |
| **B-06** | High | FR-09 (C3) | Ngưỡng đơn tối thiểu dùng `>` thay vì `>=`: đơn **bằng đúng** `min_order_amount` bị từ chối. | `SAVE10` + `total_amount=300000` (min=300000) -> `400 "Don hang chua du gia tri toi thieu 300,000"` |
| **B-07** | Critical | SEC-02 / FR-09 (C4) | `apply-coupon` **không có `authenticateToken`**, lấy `user_id` từ body => **bỏ `user_id` đi là bỏ qua toàn bộ kiểm tra hạn mức sử dụng**. | `{"code":"SAVE10","total_amount":500000}` (không token, không user_id) -> `200 success:true` |
| **B-08** | Medium | FR-09 | Kiểm tra hạn sử dụng nằm **bên trong** nhánh `total > min` => đơn nhỏ + mã hết hạn trả thông báo "chưa đủ giá trị" thay vì "hết hạn". Sai thứ tự ưu tiên C2/C3. | `EXPIRED` + `total=50000` -> `400 "chua du gia tri toi thieu 100,000"` (đáng lẽ "hết hạn") |
| **B-09** | High | FR-10 | `PUT /api/orders/:id/cancel` cho phép hủy đơn đang `shipping` (chỉ chặn `delivered`/`canceled`). SRS: "Khi đơn ở `shipping`, User không được tự hủy". Comment trong source tự thừa nhận sai. | đơn ở `shipping` -> `PUT /cancel` -> `200`, `status` thành `canceled` |
| **B-10** | High | FR-10 | `admin/orders/:id/status` có dòng code **cố ý** cho phép `canceled -> delivered`, vi phạm ràng buộc trạng thái kết thúc. | đơn `canceled` -> `{"status":"delivered"}` -> `200 {"message":"Order status updated"}` |
| **B-11** | Medium | FR-09 | `POST /api/coupon-usage` nhận `coupon_id` bất kỳ, không gắn với order, không kiểm tra coupon tồn tại => bản ghi rác làm sai hạn mức. | `INSERT INTO coupon_usage` không validate |
| **B-12** | Medium | FR-08 | `shipping_address` không bắt buộc: thiếu hẳn trường này vẫn tạo được đơn. | `{"total_amount":100}` -> `200 {"orderId":3}` |
| **B-13** | Medium | FR-08 | Giỏ hàng server `userCarts` là object in-memory, **không bao giờ được xóa sau checkout**. SRS FR-08: "Sau thanh toán thành công, giỏ hàng được xóa". | `const userCarts = {}`, không có `delete` |
| **B-14** | Medium | FR-08 | `POST /api/checkout` trả `200` thay vì `201 Created` cho thao tác tạo tài nguyên. | `res.json(...)` |

---

## 3. API-3 — Pool C / FR-15: Quản lý sản phẩm (CRUD)

### 3.1 Endpoint
| Method | Path | Auth theo spec | Auth thực tế |
|---|---|---|---|
| GET | `/api/products` | không | không |
| GET | `/api/products?search=` | không | không |
| GET | `/api/products/:id` | không | không |
| POST | `/api/products` | **admin** | **KHÔNG CÓ** (bug) |
| PUT | `/api/products/:id` | **admin** | **KHÔNG CÓ** (bug) |
| DELETE | `/api/products/:id` | **admin** | **KHÔNG CÓ** (bug) |

**Body POST/PUT:** `{ name, price, description, imageUrl, category_id }`

| Trường | Ràng buộc theo spec | Phân hoạch miền |
|---|---|---|
| `name` | bắt buộc, 1..255 ký tự | hợp lệ / rỗng / null / thiếu / 256 ký tự / chỉ khoảng trắng / XSS `<script>` / unicode / trùng tên |
| `price` | number > 0 | dương / 0 (biên) / âm / chuỗi số `"100"` / chuỗi chữ / null / thiếu / thập phân / 1e18 / NaN |
| `description` | tùy chọn, <=2000 | hợp lệ / rỗng / null / 5000 ký tự / HTML |
| `imageUrl` | tùy chọn, URL hợp lệ | http / https / không phải URL / `javascript:` / rỗng / null |
| `category_id` | phải tồn tại trong `categories` | tồn tại / không tồn tại (9999) / 0 / âm / chuỗi / null |
| `:id` (path) | số nguyên dương tồn tại | tồn tại / không tồn tại / 0 / âm / chuỗi / SQLi / rất lớn |

### 3.2 Bug đã biết (API-3) — **ĐÃ KIỂM CHỨNG BẰNG REQUEST THẬT ở STEP 0**

| ID | Mức | SEC / FR bị vi phạm | Mô tả | Bằng chứng thực nghiệm |
|---|---|---|---|---|
| **C-01** | Critical | SEC-02 + SEC-03 / FR-12 | `POST` / `PUT` / `DELETE /api/products` **hoàn toàn không xác thực**. SRS FR-12 liệt kê đích danh 3 endpoint này là phải có token + `role='admin'`. Khách vãng lai xóa được cả catalog. | `POST /api/products` không header Authorization -> `200 {"message":"Product created","id":7}` |
| **C-02** | Critical | SEC-05 | `GET /api/products?search=` **nối chuỗi SQL trực tiếp**: `` WHERE name LIKE '%${searchQuery}%' ``. | `?search=%' OR '1'='1` -> trả về **toàn bộ 5 sản phẩm** thay vì 0 kết quả |
| **C-03** | High | — (vỡ hợp đồng) | Khi SQL lỗi, trả về **HTML** `<h1>Database Error</h1><p>{err.message}</p>` với `Content-Type: text/html` (500) => vừa lộ cấu trúc DB vừa phá vỡ hợp đồng JSON. | `?search='` -> `HTTP/1.1 500`, `Content-Type: text/html; charset=utf-8` |
| **C-04** | High | — | `GET /api/products/:id` với id không tồn tại trả **`200 {}`** thay vì `404`. | `GET /api/products/999999` -> `HTTP/1.1 200`, body `{}` |
| **C-05** | High | — (vỡ schema) | `GET /api/products/:id` trả `price` kiểu **string** khi `id` chẵn, **number** khi id lẻ. Client tính tiền sai. | id=1 -> `price` là `int 30000000`; id=2 -> `price` là `str "28000000"` |
| **C-06** | High | FR-15 | Không validate gì: tạo được sản phẩm `price: -100`, `price: "abc"`, `name: null`. SRS FR-15: tên bắt buộc <=255, giá phải > 0, danh mục bắt buộc. | `POST {"name":"NoAuth2","price":-100,"category_id":9999}` -> `200` |
| **C-07** | Medium | — | `PUT /api/products/:id` với id không tồn tại vẫn trả `200 {"message":"Product updated"}` (không dùng `this.changes`). | callback bỏ qua `this.changes` |
| **C-08** | Medium | — | `DELETE /api/products/:id` với id không tồn tại vẫn trả `200 {"message":"Product deleted"}`. | callback bỏ qua `this.changes` |
| **C-09** | Medium | FR-15 | `PUT` không hỗ trợ cập nhật một phần: trường không gửi bị ghi đè thành `null`. | `UPDATE products SET name=?,price=?,description=?,imageUrl=?,category_id=?` |
| **C-10** | Medium | FR-15 | `category_id` không được kiểm khóa ngoại => tạo sản phẩm thuộc danh mục không tồn tại (`9999`). | `POST ... "category_id":9999` -> `200` |
| **C-11** | Medium | SEC-04 | Không sanitize `name` / `description`; server lưu nguyên payload `<script>`. (Phần render là tầng UI — ở tầng API chỉ kiểm được **nửa nguồn** của stored XSS.) | `POST {"name":"<script>alert(1)</script>"}` -> lưu nguyên văn |
| **C-12** | Low | — | `POST /api/products` trả `200` thay vì `201 Created`. | `res.json({message:"Product created", id})` |

---

## 3bis. Bug liên API (dùng làm bước leo thang cho SEC-03)

| ID | Mức | SEC | Mô tả | Bằng chứng thực nghiệm |
|---|---|---|---|---|
| **X-01** | Critical | SEC-06 | `PUT /api/users/me` nhận trường `role` từ body và ghi thẳng vào DB => **bất kỳ user thường nào cũng tự nâng mình lên `admin`**. SRS FR-04 + SEC-06 cấm đích danh. | `PUT /api/users/me {"role":"admin"}` (token user thường) -> `200`; `GET /api/users/me` -> `"role":"admin"` |

> X-01 không thuộc 1 trong 3 API đã chọn nhưng **bắt buộc phải báo cáo** (đề bài mục 6.5:
> "Report any genuine bugs you find"). Nó còn là **tiền đề** để test SEC-03 cho API-2/API-3:
> chuỗi tấn công `user thường -> tự nâng role -> gọi API admin` chứng minh rằng dù có thêm
> check role thì vẫn thủng nếu SEC-06 còn hở.

---

## 4. Dữ liệu test cố định (dùng cho precondition)

`database.js` gọi `initDatabase()` ngay khi `require` => **mỗi lần restart backend là DROP +
reseed toàn bộ DB**. Vì vậy thứ tự bắt buộc là: **(1) restart backend -> (2) seed_sut.js reset
-> (3) newman**. Không được restart giữa chừng.

### Dữ liệu có sẵn sau khi backend khởi động (từ `database.js`)

| Bảng | Nội dung |
|---|---|
| `users` | id=1 `admin@eshop.com` / `Admin123!` role=admin; id=2 `test@eshop.com` / `Test1234!` role=user |
| `categories` | id=1 `Dien thoai`, id=2 `Laptop`, id=3 `Phu kien` |
| `products` | id=1..5 (1 iPhone 15 Pro Max 30000000, 2 Samsung S24 Ultra 28000000, 3 MacBook Pro M3 45000000, 4 AirPods Pro 2 6000000, 5 Keychron Q1 4000000) |
| `orders` | **rỗng** |
| `coupons` | xem bảng dưới |
| `coupon_usage` | **rỗng** |

### Coupon đã seed (TÊN THẬT — bản trước của file này ghi sai `PERC10`/`FIX50K`/`INACTIVE`)

| Mã | type | discount_value | min_order_amount | expired_at | is_active | max_uses_per_user |
|---|---|---|---|---|---|---|
| `SAVE10` | percent | 10 | 300000 | 2099-12-31 | 1 | 1 |
| `BIGBUY` | fixed | 50000 | 500000 | 2099-12-31 | 1 | 1 |
| `VIP100` | fixed | 100000 | 300000 | 2099-12-31 | 1 | 2 |
| `EXPIRED` | percent | 20 | 100000 | 2020-01-01 | 1 | 1 |

> **Không có coupon `is_active = 0` nào được seed.** Muốn test nhánh C1 ("mã bị vô hiệu hóa")
> phải tự tạo qua `POST /api/admin/coupons` (nhưng `is_active` mặc định = 1, không thể tắt qua API)
> hoặc dùng `sqlite3` CLI. Test case tương ứng dùng mã **không tồn tại** (`NOTEXIST99`) làm
> đại diện cho nhánh "mã không hợp lệ", và ghi rõ giới hạn này trong báo cáo.

### Dữ liệu do `seed_sut.js reset` tạo thêm

| Biến | Giá trị | Ghi chú |
|---|---|---|
| `userEmail` (nạn nhân IDOR) | `api.victim.23127060@test.local` / `Api1234!` | id=3 sau seed sạch |
| `attackerEmail` (kẻ tấn công) | `api.attacker.23127060@test.local` / `Api1234!` | id=4 sau seed sạch |
| `adminEmail` | `admin@eshop.com` / `Admin123!` | có sẵn từ `database.js` |
| `productIdOdd` | 1 | `price` là number |
| `productIdEven` | 2 | `price` bị ép thành string — bug C-05 |
| `couponPercent` | `SAVE10` | min 300000 — dùng cho B-05, B-06 |
| `couponFixed` | `BIGBUY` | min 500000 |
| `couponMultiUse` | `VIP100` | max 2 lượt — dùng cho B-07 |
| `couponExpired` | `EXPIRED` | dùng cho B-08 |

> Lưu ý: `POST /api/register` của SUT **không kiểm tra email trùng** (không có ràng buộc
> `UNIQUE` trên cột `email`), nên chạy `seed_sut.js reset` nhiều lần trên cùng một lần
> backend chạy sẽ tạo user trùng email và làm lệch `userId`. Luôn restart backend trước khi seed.
