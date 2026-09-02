# STEP 3 — Audit test case do AI sinh (VALID / INVALID / INCOMPLETE)

> HW06 — API Testing | SV **Ninh Văn Khải — 23127060** | Đề bài mục 6.2

Đề bài: *"Label each AI-generated test case VALID / INVALID / INCOMPLETE with reasoning, and
correct the invalid or incomplete ones. You are fully responsible for the final test cases."*

---

## 1. Cách em làm: luật viết ra giấy, không sửa tay từng dòng

225 test case mà sửa tay từng dòng thì không tái lập được và không ai kiểm chứng được. Vì vậy
mọi nhãn ở đây đều đến từ **một luật viết rõ ràng**, mỗi luật bám vào **một câu cụ thể trong
`eshop-sut/README.md`**. Luật nằm trong
`agent-skill/eshop-api-23127060/scripts/audit_testcases.py`; chạy lại luôn ra đúng kết quả này:

```bash
python3 agent-skill/eshop-api-23127060/scripts/audit_testcases.py --report
```

Phần đòi hỏi phán đoán riêng cho từng case — chủ yếu là **gán lại mã SEC** và **viết lại
những case có kỳ vọng không căn cứ** — nằm trong hai bảng `SEC_REMAP` và `REWRITE`, mỗi dòng
kèm lý do bằng văn xuôi. Đó là phần "human review" thật sự; script chỉ làm việc áp dụng nhất quán.

## 2. Kết quả tổng hợp

| API | Tổng | VALID | INVALID | INCOMPLETE | % VALID |
|---|---|---|---|---|---|
| API-1 (FR-03) | 64 | 22 | 23 | 19 | 34% |
| API-2 (FR-08) | 81 | 40 | 18 | 23 | 49% |
| API-3 (FR-15) | 80 | 21 | 27 | 32 | 26% |
| **Tổng** | **225** | **83** | **68** | **74** | **37%** |

Theo nhóm kỹ thuật — cho thấy rõ lỗi tập trung ở đâu:

| Nhóm | Tổng | VALID | INVALID | INCOMPLETE | Nhận xét |
|---|---|---|---|---|---|
| DOM | 128 | 33 | 23 | 72 | Phân hoạch miền làm tốt; điểm yếu là assertion quá chung chung |
| STA | 38 | 34 | 4 | 0 | **Nhóm tốt nhất.** Bảng chuyển trạng thái buộc AI phải bám vào đặc tả |
| SEC | 41 | **0** | **41** | 0 | **Toàn bộ nhóm sai.** Xem mục 4 |
| SCH | 18 | 16 | 0 | 2 | Kỳ vọng về hình dạng response dễ đối chiếu, ít sai |

Số lần từng luật được kích hoạt (một case có thể dính hai luật):

| Luật | Nội dung | Số case |
|---|---|---|
| R3 | Gán sai mã SEC | 61 |
| R7 | Case từ chối thao tác GHI nhưng không chứng minh thao tác đã không xảy ra | 50 |
| R8 | Case thành công nhưng chỉ kiểm schema, không kiểm giá trị thật sự được lưu | 17 |
| R6 | Kỳ vọng dựa trên suy diễn, không phải điều SRS phát biểu | 5 |
| R1 | Kỳ vọng 429 (rate limiting) không có căn cứ trong SRS | 4 |
| R2 | Kỳ vọng 409 (conflict) không có căn cứ trong SRS | 2 |
| R4 | Mâu thuẫn nội tại (đánh dấu "hợp lệ" nhưng kỳ vọng 4xx) | 2 |
| R10 | Dùng biến Postman nhưng precondition không nói biến được đặt ở đâu | 2 |
| R5 | Tham số bịa (`?debug=true`) | 1 |
| R3b | Áp một chính sách mà đặc tả không hề có | 1 |

> Tỷ lệ VALID 37% thấp hơn khoảng 55-70% mà `references/TESTCASE_TAXONOMY.md` dự kiến. Con số
> này em **không điều chỉnh cho đẹp**. Nguyên nhân là cụ thể và truy nguyên được: một giả định
> sai duy nhất (bảng SEC) đã làm hỏng trọn vẹn một nhóm 41 case, và assertion mặc định của bộ
> sinh quá chung chung nên kéo theo 67 case vào nhóm INCOMPLETE. Hạ thấp tiêu chuẩn để con số
> đẹp hơn sẽ đúng nghĩa là audit hời hợt — đúng điều mà taxonomy cảnh báo.

## 3. Bốn nguyên nhân gốc

| # | Nguyên nhân | Hậu quả | Số case |
|---|---|---|---|
| N1 | **Một giả định sai lan ra cả nhóm.** Bảng SEC-01..07 được suy diễn theo OWASP thay vì đọc `README.md` mục 9 | 61 case bị gán sai mã bảo mật | 61 |
| N2 | **Bộ sinh điền assertion mặc định chung chung.** "body là JSON; có trường error" không nói gì về tác dụng phụ | 67 case thiếu phần quan trọng nhất của phép kiểm | 67 |
| N3 | **AI áp chuẩn ngành thay vì đọc đặc tả.** Rate limiting, ràng buộc khóa ngoại, cấm dùng lại mật khẩu cũ — đều là thói quen tốt nhưng SRS không hề yêu cầu | 7 case kỳ vọng sai hẳn | 7 |
| N4 | **AI bịa ra thứ không tồn tại** để lấp đầy mô hình: tham số `?debug=true`, trạng thái `EXPIRED` / `IN_SEARCH` / `LOGIN_OLD` | 4 case không thể chạy hoặc chạy mà không chứng minh gì | 4 |

## 4. Phát hiện nghiêm trọng nhất: **toàn bộ 41 case SEC đều INVALID**

Đây không phải 41 lỗi độc lập mà là **một lỗi duy nhất nhân bản 41 lần**.

Bảng SEC-01..07 dùng để gán nhãn được suy ra từ tên các lỗ hổng OWASP quen thuộc
(SEC-01 = SQL Injection, SEC-04 = IDOR, SEC-05 = role escalation, SEC-07 = brute force). Bảng
SEC **thật** nằm trong `eshop-sut/README.md` mục 9 và nói những điều hoàn toàn khác:

| Mã | Suy diễn (sai) | Thật (SRS mục 9) |
|---|---|---|
| SEC-01 | Chống SQL Injection | Mật khẩu **không** được lưu plaintext |
| SEC-02 | Không lộ dữ liệu nhạy cảm | API bảo mật phải yêu cầu JWT hợp lệ |
| SEC-03 | Endpoint ghi phải xác thực | API Admin phải kiểm `role='admin'` |
| SEC-04 | Chống IDOR | Dữ liệu user nhập phải được escape khi hiển thị |
| SEC-05 | Chống role escalation | Truy vấn CSDL phải dùng Parameterized Query |
| SEC-06 | Validate input / chống XSS | API cập nhật hồ sơ không được cho đổi `role` |
| SEC-07 | Chống brute force | OTP >= 6 chữ số, có thời hạn, vô hiệu hóa sau khi dùng |

Kết quả đối chiếu từng case: **39/41 case bị gán sai mã**, 2 case còn lại đúng mã nhưng kỳ
vọng 429 không có căn cứ. Vì vậy nhóm SEC có 0 case VALID.

**Vì sao điều này nghiêm trọng hơn nó thoạt nhìn:** các test case **vẫn chạy đúng** — một phép
thử SQL Injection vẫn là một phép thử SQL Injection dù nó bị dán nhãn SEC-01 hay SEC-05. Cái
hỏng là **bảng độ phủ bảo mật trong báo cáo**. Nếu em nộp bản chưa sửa, báo cáo sẽ ghi "API-3
đã phủ SEC-01 với 8 test case" trong khi SEC-01 (mật khẩu plaintext) **không hề được kiểm ở
API-3 dòng nào**. Đó là một khẳng định sai về phạm vi kiểm thử — đúng loại sai lầm mà người
đọc báo cáo không thể tự phát hiện.

**Vì sao AI không tự bắt được:** mã `SEC-01` là một **nhãn không tự giải thích**. Trong ngữ cảnh
kiểm thử API, "SEC-01" gần như luôn là SQL Injection; đó là mô hình mạnh nhất và AI điền vào
mà không thấy cần kiểm lại. Tài liệu chứa bảng thật (`README.md` của SUT) lại có tên khiến
người ta tưởng là file giới thiệu repo, trong khi file mang tên `api_specification.md` — cái
tên nghe có vẻ là "đặc tả" — thì **không hề chứa bảng SEC nào**. Chỉ một lệnh
`grep -n "SEC-0" README.md` đã làm sáng tỏ mọi chuyện.

### Ví dụ chi tiết 1 — `TC-B2-SEC-006`

| | |
|---|---|
| **Case gốc** | `[SEC-04] Xem đơn hàng của người khác qua GET /api/orders/:id`, `SEC_Ref = SEC-04` |
| **Nhãn** | INVALID |
| **Lý do** | SEC-04 thật là "dữ liệu user nhập phải được escape khi hiển thị", không liên quan gì đến truy cập trái phép. Lỗi thật ở đây là `GET /api/orders/:id` **thiếu hẳn middleware `authenticateToken`** — đúng là điều SEC-02 quy định. |
| **Em đã sửa** | `SEC_Ref` → `SEC-02`; đồng bộ lại tiền tố trong `Title` thành `[SEC-02]`. Kịch bản, request và kỳ vọng 403 giữ nguyên vì chúng vốn đã đúng. |

### Ví dụ chi tiết 2 — `TC-C3-SEC-010`, `TC-C3-SEC-011`

| | |
|---|---|
| **Case gốc** | `[SEC-05] User thường (role=user) tạo/xóa sản phẩm`, `SEC_Ref = SEC-05` |
| **Nhãn** | INVALID |
| **Lý do** | Đây đúng là kiểm tra phân quyền, nhưng mã đúng phải là **SEC-03** ("API Admin phải kiểm `role='admin'`, không chỉ kiểm sự tồn tại của token"). SEC-05 thật là parameterized query. |
| **Em đã sửa** | `SEC_Ref` → `SEC-03`. Nhờ vậy bảng độ phủ mới phản ánh đúng: SEC-03 được kiểm 3 lần ở API-3, và SEC-05 (SQLi) được kiểm 8 lần — trước khi sửa thì hai con số này bị hoán đổi cho nhau. |

## 5. Kỳ vọng không có căn cứ trong đặc tả (luật R1, R2, R3b)

Đây là loại lỗi khó thấy nhất, vì test case **đọc rất hợp lý**.

### Ví dụ chi tiết 3 — `TC-A1-SEC-011` (kỳ vọng 429)

| | |
|---|---|
| **Case gốc** | "Dò 20 giá trị token 4 chữ số liên tiếp phải bị chặn", `Expected_Status = 429` |
| **Nhãn** | INVALID |
| **Lý do** | **Không một dòng nào** trong FR-01..FR-24 hay SEC-01..SEC-07 yêu cầu rate limiting. AI suy ra từ thói quen bảo mật chung. Nếu giữ nguyên, case này sẽ FAIL và bị ghi vào báo cáo như một "bug" — trong khi SUT không hề vi phạm đặc tả nào cả. **Báo cáo một bug không tồn tại còn tệ hơn là bỏ sót một bug thật.** |
| **Em đã sửa** | Giữ nguyên kịch bản dò 20 giá trị (nó vẫn là cách chứng minh entropy yếu), nhưng đổi oracle sang điều SEC-07 **thực sự** nói: OTP phải dài tối thiểu 6 chữ số. `Expected_Status` → 400; assertion mới: *"mỗi lần dò đều trả 400; độ dài `resetToken` lấy từ forgot-password phải >= 6 ký tự theo SEC-07"*. Bây giờ case FAIL vì một lý do có thật: SUT sinh token 4 chữ số. |

### Ví dụ chi tiết 4 — `TC-C3-DOM-041` (kỳ vọng 409)

| | |
|---|---|
| **Case gốc** | "DELETE sản phẩm đang nằm trong đơn hàng — phải chặn", `Expected_Status = 409` |
| **Nhãn** | INVALID |
| **Lý do** | SRS FR-15 chỉ nói "Admin có thể Thêm / Xem / Sửa / Xóa sản phẩm". Không có bất kỳ ràng buộc khóa ngoại nào giữa `products` và `orders`; bản thân `database.js` cũng không khai báo `FOREIGN KEY`. AI áp kinh nghiệm thiết kế CSDL lên một hệ thống không có ràng buộc đó. |
| **Em đã sửa** | `Expected_Status` → 200. Chuyển trọng tâm sang điều **kiểm được**: sau khi xóa thì `GET /api/products/1` không được trả về sản phẩm nữa — và chính phép kiểm này phơi bày bug C-04 (trả `200 {}` thay vì `404`). `Bug_Ref` → `C-08`. |

### Ví dụ chi tiết 5 — `TC-A1-DOM-035`

| | |
|---|---|
| **Case gốc** | "Đặt lại đúng mật khẩu cũ phải bị từ chối", `Expected_Status = 400` |
| **Nhãn** | INVALID |
| **Lý do** | SRS FR-01/FR-03 chỉ đòi mật khẩu mới **thỏa điều kiện độ mạnh**; không ở đâu cấm đặt lại trùng mật khẩu cũ. AI áp một chính sách bảo mật phổ biến mà đặc tả không có. |
| **Em đã sửa** | `Expected_Status` → 200, kèm khẳng định đăng nhập bằng mật khẩu đó phải thành công. |

## 6. Mâu thuẫn nội tại và thứ bịa ra (luật R4, R5)

### Ví dụ chi tiết 6 — `TC-A1-STA-006`

| | |
|---|---|
| **Case gốc** | "Chuyển trạng thái ISSUED → EXPIRED **(hợp lệ)**" nhưng `Expected_Status = 400` |
| **Nhãn** | INVALID |
| **Lý do** | Hai lỗi chồng nhau. Thứ nhất, tự mâu thuẫn: đánh dấu chuyển hợp lệ mà lại kỳ vọng bị từ chối. Thứ hai, `EXPIRED` **không phải một trạng thái điều khiển được**: SUT không lưu thời điểm cấp OTP (bug A-04), nên không có cách nào đưa OTP về trạng thái hết hạn qua API. Case này không thể chạy. |
| **Em đã sửa** | Đổi thành chuyển **KHÔNG hợp lệ** `USED → USED`: dùng lại OTP đã dùng. Đây là điều SEC-07 quy định rõ ("vô hiệu hóa sau khi dùng") và kiểm được hoàn toàn qua API. Precondition được viết lại cho khớp. |

### Ví dụ chi tiết 7 — `TC-C3-SEC-004`

| | |
|---|---|
| **Case gốc** | "Response sản phẩm không lộ trường nội bộ khi bật cờ debug", `GET /api/products/1?debug=true` |
| **Nhãn** | INVALID |
| **Lý do** | Tham số `debug` **không tồn tại** — không có trong `api_specification.md` lẫn trong `server.js`. Express bỏ qua query param lạ, nên case này sẽ **PASS** trong mọi tình huống và không chứng minh điều gì. Một test luôn pass vì lý do sai còn nguy hiểm hơn một test thất bại, vì nó tạo cảm giác an toàn giả. |
| **Em đã sửa** | Bỏ tham số bịa. Kiểm đúng điều kiểm được: *"body chỉ được chứa đúng 6 trường `id`, `name`, `price`, `description`, `imageUrl`, `category_id`"*. |

## 7. Nhóm INCOMPLETE: 67 case thiếu phần quan trọng nhất (luật R7, R8)

### Ví dụ chi tiết 8 — mẫu chung của 50 case dính luật R7

| | |
|---|---|
| **Case gốc** | `POST /api/products` với `price = -100`, `Expected_Status = 400`, assertion: *"body là JSON; có trường error"* |
| **Nhãn** | INCOMPLETE |
| **Lý do** | Case chỉ kiểm **câu trả lời**, không kiểm **hậu quả**. Một API trả `400` rồi **vẫn INSERT** vào CSDL sẽ pass case này. Mà đó đúng là kiểu lỗi đang có trong SUT: `PUT /api/products/:id` với id không tồn tại trả `200 "Product updated"` dù không dòng nào bị đổi (bug C-07). |
| **Em đã sửa** | Bổ sung vế sau của assertion: *"VÀ đọc lại tài nguyên sau khi gọi để xác nhận dữ liệu KHÔNG bị thay đổi"*. Trong Postman, phần này được hiện thực bằng một `pm.sendRequest` đọc lại `GET /api/products` và đếm số bản ghi trước/sau. |
| **Phạm vi** | Luật R7 chỉ áp dụng cho endpoint có **tác dụng phụ quan sát được** (`/api/products`, `/api/checkout`, `/api/orders/...`, `/api/users/me`, `/api/reset-password`, `/api/categories`, `/api/admin/*`). Không áp cho `/api/apply-coupon` (thuần tính toán, không ghi gì) và `/api/forgot-password` (có ghi nhưng trên nhánh lỗi không có gì đọc lại được). Đòi hỏi một phép kiểm không tồn tại sẽ làm nhãn INCOMPLETE mất ý nghĩa. |

### Ví dụ chi tiết 9 — mẫu chung của 17 case dính luật R8

| | |
|---|---|
| **Case gốc** | `POST /api/checkout` với dữ liệu hợp lệ, `Expected_Status = 201`, assertion: *"body là JSON; khớp schema thành công"* |
| **Nhãn** | INCOMPLETE |
| **Lý do** | Kiểm hình dạng response mà không kiểm **giá trị thật sự được lưu**. Case này sẽ pass kể cả khi SUT lưu sai tổng tiền — đúng bug B-01: `checkout` nhận `total_amount` do client gửi và ghi thẳng vào CSDL. |
| **Em đã sửa** | Bổ sung: *"VÀ đọc lại tài nguyên để xác nhận giá trị lưu đúng bằng giá trị đã gửi"* — với checkout là `GET /api/orders/:id` rồi so `total_amount`. |

## 8. Độ phủ SEC sau khi gán lại — và một giới hạn em thừa nhận

| API | Mã SEC được kiểm | Mã không áp dụng | Lý do |
|---|---|---|---|
| API-1 | SEC-01(1), SEC-04(3), SEC-05(3), SEC-06(1), SEC-07(6) | SEC-02, SEC-03 | `forgot-password` và `reset-password` **không yêu cầu xác thực theo đúng đặc tả** (người quên mật khẩu thì làm gì còn token). Không có endpoint admin nào trong phạm vi API-1. |
| API-2 | SEC-02(7), SEC-03(3), SEC-04(2), SEC-05(2), SEC-06(1) | SEC-01, SEC-07 | Luồng thanh toán không dùng tới lưu trữ mật khẩu lẫn OTP. |
| API-3 | SEC-02(4), SEC-03(3), SEC-04(5), SEC-05(8), SEC-06(1) | SEC-01, SEC-07 | Như trên. |
| **Toàn suite** | **SEC-01(1), SEC-02(11), SEC-03(6), SEC-04(10), SEC-05(13), SEC-06(3), SEC-07(6)** | **(không thiếu mã nào)** | |

`references/TESTCASE_TAXONOMY.md` do chính em viết có một dòng: *"Bắt buộc phủ đủ 7 mã
SEC-01..SEC-07 cho **mọi** API"*. Sau khi biết bảng SEC thật, **yêu cầu đó là bất khả thi và
chính nó là nguyên nhân gây hại**: nó ép em phải tìm cho ra một case SEC-07 ở API-3, và cách
duy nhất để "đạt chỉ tiêu" là gán bừa một case rate-limit vào mã SEC-07. Yêu cầu đúng phải là:
**đủ 7 mã trên toàn bộ suite**, và từng API phủ những mã **thực sự áp dụng được**, có giải trình
cho phần không áp dụng. Em đã sửa lại taxonomy theo hướng này.

Đây là một bài học độc lập với SUT: **một chỉ tiêu đo lường đặt sai sẽ tạo ra chính cái lỗi
mà nó định ngăn chặn.**

## 9. Kết luận STEP 3

- 225 case được gán nhãn bằng 10 luật viết rõ ràng, tái lập được bằng một lệnh.
- 68 case INVALID và 74 case INCOMPLETE **em đã sửa ngay trong `testcases/API-*_audited.csv`**,
  mỗi dòng đều có cột `Audit_Note` ghi lý do và nói rõ đã sửa gì.
- Phát hiện lớn nhất: **toàn bộ nhóm SEC (41 case) đều sai**, do một giả định duy nhất về bảng
  SEC-01..07. Độ phủ bảo mật sau khi sửa đã phản ánh đúng thực tế.
- **Công việc của human (H2):** đọc lại cột `Audit_Note`, đặc biệt 68 dòng INVALID, và xác nhận
  hoặc bác bỏ từng nhãn trước khi nộp.
- **STEP kế tiếp:** STEP 4 — bổ sung >= 5 case/API mà AI bỏ sót.
