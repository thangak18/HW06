# Chỉ mục bằng chứng tái hiện bug

Sinh tự động bằng `capture_bug_evidence.py`. Mỗi file chứa nguyên văn cặp
request/response của từng bước.

| Bug | Mô tả | Số bước | File |
|---|---|---|---|
| **A-01** | Response của forgot-password trả thẳng mã OTP ra ngoài | 2 | [`A-01.md`](A-01.md) |
| **A-02** | OTP chỉ có 4 chữ số trong khi SEC-07 đòi tối thiểu 6 | 2 | [`A-02.md`](A-02.md) |
| **A-03** | User enumeration: email không tồn tại trả 404, email tồn tại trả 200 | 3 | [`A-03.md`](A-03.md) |
| **A-05** | reset-password không kiểm tra độ mạnh mật khẩu | 4 | [`A-05.md`](A-05.md) |
| **A-07** | login trả về nguyên bản ghi user gồm cả password plaintext và reset_token | 3 | [`A-07.md`](A-07.md) |
| **A-08** | forgot-password bỏ qua biến err của db.get nên lỗi CSDL bị báo thành 404 | 1 | [`A-08.md`](A-08.md) |
| **A-09** | Bộ đếm đăng nhập sai cộng +2 mỗi lần nên khóa ngay ở lần sai thứ HAI | 4 | [`A-09.md`](A-09.md) |
| **B-01** | checkout tin tuyệt đối total_amount từ client | 4 | [`B-01.md`](B-01.md) |
| **B-01b** | checkout chấp nhận total_amount âm | 3 | [`B-01b.md`](B-01b.md) |
| **B-02** | GET /api/orders/:id thiếu xác thực - IDOR đọc đơn hàng của bất kỳ ai | 4 | [`B-02.md`](B-02.md) |
| **B-03** | PUT /api/admin/orders/:id/status không kiểm role - user thường đổi đơn người khác | 6 | [`B-03.md`](B-03.md) |
| **B-05** | Công thức coupon percent sai: discount = total*(1-value) cho ra số ÂM | 1 | [`B-05.md`](B-05.md) |
| **B-06** | Ngưỡng đơn tối thiểu dùng > thay vì >=: đơn bằng đúng min_order_amount bị từ chối | 2 | [`B-06.md`](B-06.md) |
| **B-07** | apply-coupon không xác thực; bỏ user_id đi là bỏ qua toàn bộ kiểm tra hạn mức | 1 | [`B-07.md`](B-07.md) |
| **B-08** | Kiểm tra hạn sử dụng nằm trong nhánh total > min nên thông báo lỗi sai nguyên nhân | 1 | [`B-08.md`](B-08.md) |
| **B-09** | PUT /api/orders/:id/cancel cho phép hủy đơn đang shipping | 7 | [`B-09.md`](B-09.md) |
| **B-10** | admin/orders/:id/status cho phép canceled -> delivered | 6 | [`B-10.md`](B-10.md) |
| **B-11** | POST /api/coupon-usage ghi nhận lượt dùng cho coupon_id không tồn tại | 3 | [`B-11.md`](B-11.md) |
| **B-12** | checkout tạo được đơn hàng khi thiếu hẳn shipping_address | 4 | [`B-12.md`](B-12.md) |
| **B-14** | checkout trả 200 thay vì 201 Created cho thao tác tạo tài nguyên | 3 | [`B-14.md`](B-14.md) |
| **C-01** | POST/PUT/DELETE /api/products hoàn toàn không xác thực | 3 | [`C-01.md`](C-01.md) |
| **C-02** | GET /api/products?search= nối chuỗi SQL trực tiếp - SQL Injection | 2 | [`C-02.md`](C-02.md) |
| **C-03** | Lỗi SQL trả về HTML kèm thông điệp của tầng CSDL thay vì JSON | 1 | [`C-03.md`](C-03.md) |
| **C-04** | GET /api/products/:id với id không tồn tại trả 200 {} thay vì 404 | 1 | [`C-04.md`](C-04.md) |
| **C-05** | price là number với id lẻ nhưng là string với id chẵn | 2 | [`C-05.md`](C-05.md) |
| **C-06** | POST /api/products không validate gì: giá âm, giá là chuỗi, tên null đều được chấp nhận | 2 | [`C-06.md`](C-06.md) |
| **C-07** | PUT /api/products/:id với id không tồn tại vẫn trả 200 Product updated | 1 | [`C-07.md`](C-07.md) |
| **C-08** | DELETE /api/products/:id với id không tồn tại vẫn trả 200 Product deleted | 1 | [`C-08.md`](C-08.md) |
| **C-09** | PUT không hỗ trợ cập nhật một phần: trường không gửi bị ghi đè thành null | 3 | [`C-09.md`](C-09.md) |
| **C-10** | category_id không được kiểm khóa ngoại: tạo được sản phẩm thuộc danh mục không tồn tại | 2 | [`C-10.md`](C-10.md) |
| **C-11** | name và description không được sanitize: payload script được lưu nguyên văn | 2 | [`C-11.md`](C-11.md) |
| **C-12** | POST /api/products trả 200 thay vì 201 Created | 1 | [`C-12.md`](C-12.md) |
| **C-13** | Một sản phẩm có price = null làm SẬP HẲN backend khi đọc lại (từ chối dịch vụ) | 4 | [`C-13.md`](C-13.md) |
| **X-01** | PUT /api/users/me cho phép user thường tự nâng role lên admin | 4 | [`X-01.md`](X-01.md) |
