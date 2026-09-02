# STEP 0 — Trinh sát môi trường & đối chiếu đặc tả

> HW06 — API Testing | SV **Ninh Văn Khải — 23127060** | Ngày 01/09/2026

---

## 1. Môi trường thực nghiệm

| Hạng mục | Giá trị |
|---|---|
| Hệ điều hành | Linux 6.18.33.2-microsoft-standard-WSL2 (Ubuntu trên WSL2 / Windows) |
| Node.js | v20.20.2 |
| npm | 10.8.2 |
| Newman | 6.2.2 |
| Reporter | `newman-reporter-htmlextra` (cài kèm, bản mới nhất trên npm) |
| Python | 3.13.5 (em dùng cho các script sinh test / tổng hợp báo cáo) |
| Postman | Bản Desktop dùng cho phần thao tác GUI (workspace, Console, Runner, Mock, Monitor) |
| Base URL | `http://localhost:3000` — thỏa yêu cầu chống gian lận mục 11 đề bài (`localhost`/`127.0.0.1`) |
| Shell | bash |

Lệnh xác minh phiên bản em đã chạy:

```bash
node -v        # v20.20.2
npm -v         # 10.8.2
python3 -V     # Python 3.13.5
newman -v      # 6.2.2
```

## 2. System Under Test

| Hạng mục | Giá trị |
|---|---|
| Repo | https://github.com/ttbhanh/eshop-sut |
| Commit đang test | `85af3ba875c88283615e22cb108f13e2fccaf0e9` |
| Ngày commit | 2026-05-15 08:30:35 +0700 — *"first upload"* |
| Đường dẫn cục bộ | `../../../eshop-sut/` (ngang hàng với thư mục repo `HW06/`, **không** nằm trong repo bài nộp) |
| Backend | Node.js + Express + SQLite (`backend/server.js`, 572 dòng) |
| CSDL | `backend/database.sqlite`, khởi tạo bởi `backend/database.js` (119 dòng) |

### Cách khởi động / dừng

```bash
cd ../../../eshop-sut/backend
npm install                                   # chi lan dau
setsid nohup node server.js > /tmp/eshop.log 2>&1 < /dev/null &
curl -sf http://localhost:3000/api/products >/dev/null && echo "SUT UP"

pkill -f "node server.js"                     # dung
```

### CẢNH BÁO VỀ VÒNG ĐỜI CSDL

`database.js` gọi `initDatabase()` **ngay khi module được `require`**, và `initDatabase()`
bắt đầu bằng một loạt `DROP TABLE IF EXISTS`. Hậu quả: **mỗi lần khởi động lại backend là
toàn bộ CSDL bị xóa và seed lại từ đầu.**

Vì vậy thứ tự bắt buộc cho mỗi lần chạy test là:

1. Khởi động (hoặc khởi động lại) backend — CSDL về trạng thái gốc.
2. `node agent-skill/eshop-api-23127060/scripts/seed_sut.js reset` — tạo 2 tài khoản test.
3. Chạy Newman.

Không được restart backend ở giữa bước 2 và 3. Ngoài ra `POST /api/register` của SUT không
có ràng buộc `UNIQUE` trên `email`, nên chạy `seed_sut.js reset` hai lần trên cùng một lần
backend chạy sẽ tạo user trùng email và làm lệch `userId` của các test IDOR.

## 3. Các tài liệu em dùng làm oracle

SUT có **hai** tài liệu, vai trò khác hẳn nhau. Xác định đúng vai trò là việc quan trọng
nhất của STEP 0, vì nó quyết định mọi kỳ vọng (`Expected_Status`) về sau.

| Tài liệu | Vai trò thực sự | Dùng làm oracle? |
|---|---|---|
| `eshop-sut/README.md` (288 dòng) | **SRS** — tự tuyên bố "Mô tả **yêu cầu nghiệp vụ đúng** của hệ thống EShop". Chứa FR-01..FR-24 và bảng SEC-01..SEC-07. | **CÓ — đây là oracle `SPEC`** |
| `eshop-sut/api_specification.md` (214 dòng) | Hướng dẫn gọi API: danh sách endpoint, body mẫu, response mẫu. **Không mô tả ràng buộc nghiệp vụ.** | Chỉ để lấy hình dạng request/response |
| `eshop-sut/backend/server.js` | Hành vi thực tế đang chạy. | Oracle `IMPL` — dùng cho test hồi quy |

Khi hai tài liệu mâu thuẫn, em lấy `README.md` làm chuẩn. Ví dụ điển hình:
`api_specification.md` in response mẫu của `forgot-password` là `"resetToken": "123456"`
(6 chữ số) trong khi `README.md` FR-03 và SEC-07 đòi **tối thiểu 6 chữ số** — còn code thật
sinh **4 chữ số**. Cả hai tài liệu đều chống lại implementation, nên đây chắc chắn là bug (A-02).

## 4. [C3] ĐÃ SỬA — bảng SEC-01..SEC-07 trước đó là suy diễn và sai hoàn toàn

`references/API_SPEC_NOTES.md` ban đầu chứa một bảng SEC **tự suy diễn theo OWASP**
(SEC-01 = SQL Injection, SEC-04 = IDOR, SEC-07 = brute force...), kèm ghi chú
"GIẢ ĐỊNH — phải xác nhận lại với spec thật ở STEP 0".

Đối chiếu với `eshop-sut/README.md` mục 9 cho thấy bảng suy diễn **không trùng một dòng nào**
với bảng thật. Nếu em giữ nguyên thì toàn bộ cột `SEC_Ref` của hơn 120 test case sẽ sai, và
phần "độ phủ SEC-01..07" trong báo cáo sẽ là bịa đặt. Em đã sửa lại file tham chiếu theo
bảng thật:

| Mã | Yêu cầu thật (SRS mục 9) | Trước đây bị suy diễn nhầm thành |
|---|---|---|
| SEC-01 | Mật khẩu **không** được lưu plaintext | "Chống SQL Injection" |
| SEC-02 | API có tính bảo mật phải yêu cầu JWT hợp lệ | "Không lộ dữ liệu nhạy cảm" |
| SEC-03 | API Admin phải kiểm `role='admin'` trong token, không chỉ kiểm token tồn tại | "Endpoint thay đổi dữ liệu phải xác thực" |
| SEC-04 | Dữ liệu user nhập phải được escape khi hiển thị (không `innerHTML`) | "Chống IDOR" |
| SEC-05 | Truy vấn CSDL phải dùng Parameterized Query | "Chống role escalation" |
| SEC-06 | API cập nhật hồ sơ không được cho đổi `role` từ client | "Validate input / chống XSS" |
| SEC-07 | OTP reset phải >= 6 chữ số, có thời hạn, vô hiệu hóa sau khi dùng | "Chống brute force / rate limit" |

**Giới hạn em ghi nhận:** SEC-04 là yêu cầu ở tầng hiển thị (UI). Ở tầng API em chỉ kiểm được
**nửa nguồn** của stored XSS — tức là server có lưu nguyên payload `<script>` hay không.
Báo cáo sẽ ghi rõ giới hạn này, em không tuyên bố "đã phủ đầy đủ SEC-04".

## 5. Ba API em chọn — không trùng với thành viên khác

| ID | Pool | FR | Endpoint chính | Endpoint hỗ trợ |
|---|---|---|---|---|
| API-1 | A | FR-03 Quên & đặt lại mật khẩu | `POST /api/forgot-password`, `POST /api/reset-password` | `POST /api/login`, `POST /api/register` |
| API-2 | B | FR-08 Thanh toán | `POST /api/checkout` | `POST /api/apply-coupon` (FR-09), `PUT /api/orders/:id/cancel`, `PUT /api/admin/orders/:id/status`, `GET /api/orders/:id` (FR-10) |
| API-3 | C | FR-15 Quản lý sản phẩm | `POST` / `PUT` / `DELETE /api/products` | `GET /api/products`, `GET /api/products?search=`, `GET /api/products/:id` |

**Pool D (Mobile) em không sử dụng** — đề bài mục 5 ghi rõ: *"Pool D, the mobile app, is not
used here, because this homework targets the backend API"*.

Em đã đọc `../../docs/team-api-allocation.md` (chỉ đọc, không sửa). Tại thời điểm STEP 0, bảng
phân công của nhóm còn để `TODO` cho cả 3 thành viên, nên em **chưa thể đối chiếu tự động**.
Bộ ba (FR-03, FR-08, FR-15) đã được chốt trong `CLAUDE.md` và `SKILL.md` của riêng em;
em chịu trách nhiệm xác nhận miệng với 2 thành viên còn lại trước khi nộp.
Đây là **rủi ro mở** được theo dõi, không phải lỗi kỹ thuật.

**Cập nhật (02/09/2026, sau khi merge `origin/main`):** bảng phân công đã được điền đầy đủ,
nên em **đã đối chiếu được**. Ba bộ API của nhóm:

| SV | Pool A | Pool B | Pool C |
|---|---|---|---|
| **23127060** (em) | FR-03 | FR-08 | FR-15 |
| 23127195 | FR-04 | FR-09 | FR-16 |
| 23127259 | FR-02 | FR-10 | FR-14 |

**Không có FR nào trùng nhau** giữa ba thành viên → thỏa ràng buộc mục 5 của đề bài.
Rủi ro mở nêu trên **đã được đóng**.

## 6. Kiểm chứng sơ bộ bằng request thật

Trước khi sinh test case, em đã chạy một loạt `curl` để xác minh các bug ghi trong
`references/API_SPEC_NOTES.md` là có thật chứ không phải chép lại từ trí nhớ. Kết quả:
**toàn bộ bug đã liệt kê đều tái hiện được**, và em phát hiện thêm 1 bug mới (X-01).

> Cột "Response thật" dưới đây là nguyên văn phản hồi của SUT (kể cả phần tiếng Việt không
> dấu do chính server trả về), em giữ nguyên để làm bằng chứng.

| Bug | Request | Response thật quan sát được |
|---|---|---|
| A-01 | `POST /api/forgot-password {"email":"api.victim.23127060@test.local"}` | `200 {"message":"Ma dat lai mat khau da duoc tao","resetToken":"5740"}` |
| A-02 | (như trên) | token `"5740"` — **4 chữ số**, trong khi SEC-07 đòi tối thiểu 6 |
| A-03 | `POST /api/forgot-password {"email":"nobody.23127060@test.local"}` | `HTTP/1.1 404 Not Found` — lộ sự tồn tại của tài khoản |
| A-07 | `POST /api/login` | body chứa `"password":"Api1234!"` và `"reset_token":null` |
| B-01 | `POST /api/checkout {"total_amount":1,"shipping_address":"123 Test"}` | `200 {"orderId":1}`; `GET /api/orders/1` → `"total_amount":1` |
| B-01b | `POST /api/checkout {"total_amount":-500000,...}` | `200 {"orderId":2}` — chấp nhận tổng tiền âm |
| B-02 | `GET /api/orders/1` **không** header `Authorization` | `200 {"id":1,"user_id":3,...}` — IDOR |
| B-03 | attacker (id=4) `PUT /api/admin/orders/1/status {"status":"confirmed"}` | `200 {"message":"Order status updated"}` — đổi đơn của người khác |
| B-05 | `POST /api/apply-coupon {"code":"SAVE10","total_amount":500000,"user_id":3}` | `{"discount_amount":-4500000,"final_amount":5000000}` — giảm giá **âm** |
| B-06 | `... {"code":"SAVE10","total_amount":300000}` (min = 300000) | `400 "Don hang chua du gia tri toi thieu 300,000"` — lỗi biên `>` vs `>=` |
| B-07 | `POST /api/apply-coupon {"code":"SAVE10","total_amount":500000}` (không token, không `user_id`) | `200 success:true` — bỏ qua toàn bộ kiểm tra hạn mức |
| B-08 | `... {"code":"EXPIRED","total_amount":50000}` | `400 "chua du gia tri toi thieu 100,000"` — đáng lẽ phải báo "hết hạn" |
| B-09 | đơn ở `shipping` → `PUT /api/orders/1/cancel` (token user) | `200`, trạng thái thành `canceled` — vi phạm FR-10 |
| B-10 | đơn ở `canceled` → `PUT /api/admin/orders/1/status {"status":"delivered"}` | `200 {"message":"Order status updated"}` |
| B-12 | `POST /api/checkout {"total_amount":100}` (thiếu `shipping_address`) | `200 {"orderId":3}` |
| C-01 | `POST /api/products` **không** header `Authorization` | `200 {"message":"Product created","id":7}` |
| C-02 | `GET /api/products?search=%25' OR '1'='1` | trả về **cả 5 sản phẩm** thay vì 0 kết quả |
| C-03 | `GET /api/products?search='` | `500`, `Content-Type: text/html; charset=utf-8`, body `<h1>Database Error</h1>...` |
| C-04 | `GET /api/products/999999` | `200 {}` thay vì `404` |
| C-05 | `GET /api/products/1` vs `GET /api/products/2` | `price` là `int 30000000` vs `str "28000000"` |
| C-06 | `POST /api/products {"name":"NoAuth2","price":-100,"category_id":9999}` | `200` — giá âm + danh mục không tồn tại đều được chấp nhận |
| **X-01** | `PUT /api/users/me {"role":"admin"}` với token user thường | `200 {"message":"Profile updated"}`; `GET /api/users/me` → `"role":"admin"` |

**X-01 là bug mới**, chưa có trong bản `API_SPEC_NOTES.md` trước đó. Nó vi phạm đích danh
SEC-06 và FR-04 ("không thể tự thay đổi thuộc tính `role`"). Em đã bổ sung vào mục "3bis. Bug
liên API" của file tham chiếu, và sẽ dùng nó làm **bước leo thang** cho các test SEC-03
của API-2 và API-3.

## 7. Các đính chính khác em đã áp dụng vào `API_SPEC_NOTES.md`

| Mục | Trước | Sau (theo `database.js` thật) |
|---|---|---|
| Tên coupon seed | `PERC10`, `FIX50K`, `EXPIRED`, `INACTIVE` | `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED` |
| Coupon `is_active=0` | giả định có sẵn | **không có** — phải dùng mã không tồn tại làm đại diện, em đã ghi rõ giới hạn |
| Thời gian khóa tài khoản | không ghi | impl khóa **180s**, SRS FR-02 ghi **30s** — em thêm vào bug A-09 |
| Số chữ số OTP mong đợi | không ghi | SRS + SEC-07 đòi **6**, impl sinh **4** |
| Bug A-11, B-01b, B-14 | chưa có | em bổ sung sau khi đọc lại `server.js` |

## 8. Kết luận STEP 0

- Môi trường đầy đủ, SUT chạy được trên `localhost:3000`, Newman 6.2.2 sẵn sàng.
- Oracle đã được xác định rõ: `README.md` (SRS) = `SPEC`, `server.js` = `IMPL`.
- Bảng SEC-01..07 đã được sửa về đúng bản gốc — đây là đính chính quan trọng nhất của bước này.
- 22 bug em đã tái hiện được bằng request thật, sẵn sàng làm cơ sở cho STEP 2 và STEP 7.
- **STEP kế tiếp:** STEP 1 — rà soát lại `spec/api-1..3.json` cho khớp với các đính chính trên.
