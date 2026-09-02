#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extend_testcases.py - Bổ sung test case do NGƯỜI viết, những case bộ sinh AI đã bỏ sót.

  python3 extend_testcases.py            # sinh testcases/API-*_final.csv tu *_audited.csv

Đề bài mục 6.3: "Add at least five test cases of your own that the AI missed - especially
around security and state transitions - and explain why the AI missed them (prompt quality,
model limitations, or characteristics of the API)."

Bốn lý do AI bỏ sót (mỗi case phải chọn đúng 1):
  PROMPT   Prompt không yêu cầu rõ điều đó.
  MODEL    AI suy diễn từ tên/hình dạng API thay vì đọc mã nguồn.
  API      Bug chỉ lộ ra khi KẾT HỢP NHIỀU REQUEST; bộ sinh làm việc trên từng case độc lập.
  SPECGAP  Đặc tả không mô tả hành vi này nên AI không có gì để bám vào.
"""
import csv
import os

COLS = ["TC_ID","API","FR","Category","Technique","Title","Method","Endpoint","Preconditions",
        "Request_Headers","Request_Body","Expected_Status","Expected_Assertions","Oracle",
        "SEC_Ref","Priority","Source","Audit_Label","Audit_Note","Tag","Bug_Ref","Why_AI_Missed"]

BEARER_U = "Authorization: Bearer {{token_user}}"
BEARER_A = "Authorization: Bearer {{token_attacker}}"

# Mỗi phần tử: dict các cột khác mặc định.
EXTRA = [
# ============================== API-1 — FR-03 ==============================
dict(TC_ID="TC-A1-STA-901", API="API-1", FR="FR-03", Category="STA", Technique="State Transition",
     Title="Sau khi reset, mật khẩu CŨ phải hết hiệu lực và mật khẩu MỚI phải đăng nhập được",
     Method="POST", Endpoint="/api/login",
     Preconditions="Đã chạy xong chuỗi: forgot-password -> reset-password với newPassword = NewApi1234!",
     Request_Headers="-", Request_Body='{"email":"api.victim.23127060@test.local","password":"Api1234!"}',
     Expected_Status="401",
     Expected_Assertions="login bằng mật khẩu CŨ trả 401; ngay sau đó login bằng mật khẩu MỚI trả 200 kèm token",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@contract", Bug_Ref="-",
     Why_AI_Missed="API - Bộ sinh chỉ kiểm RESPONSE của reset-password ('Password reset successfully') rồi dừng lại. Nhưng câu trả lời đó không chứng minh mật khẩu đã thực sự đổi: SUT có thể trả 200 mà không ghi gì (chính là kiểu lỗi C-07/C-08 ở API-3). Chỉ một chuỗi 3 request - reset, login mật khẩu cũ, login mật khẩu mới - mới chứng minh được. Bộ sinh làm việc trên từng case độc lập nên không thể tự dựng chuỗi này."),

dict(TC_ID="TC-A1-SEC-901", API="API-1", FR="FR-03", Category="SEC", Technique="Broken Access Control",
     Title="[-] Đặt lại mật khẩu thành công nhưng tài khoản vẫn bị khóa",
     Method="POST", Endpoint="/api/login",
     Preconditions="Tài khoản đã bị khóa do đăng nhập sai; sau đó đã reset mật khẩu thành công bằng OTP",
     Request_Headers="-", Request_Body='{"email":"api.victim.23127060@test.local","password":"NewApi1234!"}',
     Expected_Status="200",
     Expected_Assertions="đăng nhập thành công bằng mật khẩu mới; login_attempts phải về 0 và locked_until phải được xóa sau khi reset",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="A-06",
     Why_AI_Missed="API - Bug nằm ở CHỖ GIAO NHAU giữa hai chức năng: FR-02 (khóa tài khoản) và FR-03 (đặt lại mật khẩu). Câu lệnh UPDATE trong reset-password chỉ đặt lại password và reset_token, không động tới login_attempts và locked_until. Bộ sinh chỉ đọc đặc tả của FR-03 nên không thể biết FR-02 có để lại trạng thái gì. Cần 5 request liên tiếp (2 lần login sai, forgot, reset, login) mới tái hiện được."),

dict(TC_ID="TC-A1-SEC-902", API="API-1", FR="FR-03", Category="SEC", Technique="Information Disclosure",
     Title="[SEC-01] GET /api/users/me tra ve ca password lan reset_token",
     Method="GET", Endpoint="/api/users/me",
     Preconditions="Da login, co {{token_user}}",
     Request_Headers=BEARER_U, Request_Body="-", Expected_Status="200",
     Expected_Assertions="body KHÔNG được chứa trường password; KHÔNG được chứa trường reset_token; nếu password xuất hiện đúng nguyên văn chuỗi đã gửi khi đăng ký thì đã chứng minh vi phạm SEC-01",
     Oracle="SPEC", SEC_Ref="SEC-01", Priority="P0", Tag="@bug", Bug_Ref="A-07",
     Why_AI_Missed="PROMPT - Prompt khoanh vùng API-1 vào đúng hai endpoint forgot-password và reset-password. Nhưng nơi rò rỉ nghiêm trọng nhất lại là GET /api/users/me: nó làm `SELECT * FROM users` rồi trả thẳng cả bản ghi, kể cả cột reset_token đang còn hiệu lực. Kẻ tấn công đọc được OTP của chính mình là vô hại, nhưng nó chứng minh cột này chưa bao giờ được coi là bí mật. Bộ sinh không được phép bước ra ngoài phạm vi prompt."),

dict(TC_ID="TC-A1-SEC-903", API="API-1", FR="FR-03", Category="SEC", Technique="Boundary / Error Guessing",
     Title="[-] Tài khoản bị khóa ngay sau HAI lần đăng nhập sai, trong khi SRS quy định ba lần",
     Method="POST", Endpoint="/api/login",
     Preconditions="Tài khoản api.victim vừa được seed lại, login_attempts = 0. Đã gọi login sai ĐÚNG HAI lần trước đó",
     Request_Headers="-", Request_Body='{"email":"api.victim.23127060@test.local","password":"Api1234!"}',
     Expected_Status="200",
     Expected_Assertions="sau ĐÚNG hai lần sai, đăng nhập bằng mật khẩu ĐÚNG vẫn phải thành công (SRS FR-02: chỉ khóa từ lần sai thứ ba)",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="A-09",
     Why_AI_Missed="MODEL - SRS viết 'sai từ 3 lần trở lên thì khóa', và bộ sinh sinh đúng case đó: sai 3 lần rồi kiểm đã khóa chưa. Case đó PASS, vì sai 3 lần thì quá nhiên là khóa. Bug nằm ở phía còn lại của biên: code cộng +2 mỗi lần sai nên mở khóa ngay ở lần thứ HAI. Muốn thấy phải kiểm cạnh 'chưa được khóa' chứ không phải cạnh 'đã bị khóa' - AI mặc định viết case khẳng định điều đặc tả nói, chứ không viết case phủ định điều đặc tả không nói."),

dict(TC_ID="TC-A1-SEC-904", API="API-1", FR="FR-03", Category="SEC", Technique="Privilege Escalation",
     Title="[SEC-03] User thường đọc được toàn bộ bảng users qua GET /api/admin/users",
     Method="GET", Endpoint="/api/admin/users",
     Preconditions="Đã login bằng tài khoản thường api.victim, có {{token_user}}",
     Request_Headers=BEARER_U, Request_Body="-", Expected_Status="403",
     Expected_Assertions="token hợp lệ nhưng role = 'user' thì phải bị từ chối 403; không được trả về danh sách email của người khác",
     Oracle="SPEC", SEC_Ref="SEC-03", Priority="P0", Tag="@bug", Bug_Ref="X-01",
     Why_AI_Missed="PROMPT - API-1 không có endpoint admin nào nên bộ sinh không sinh case SEC-03. Nhưng luồng quên mật khẩu vẫn có thể bị khai thác qua đường này: GET /api/admin/users trả về cả login_attempts và locked_until của mọi người, cho phép dò xem tài khoản nào đang bị khóa. Độ phủ SEC-03 của API-1 trước đó là 0 - đây là case làm đầy khoảng trống đó bằng một kịch bản có thật."),

dict(TC_ID="TC-A1-SEC-905", API="API-1", FR="FR-03", Category="SEC", Technique="Error Guessing",
     Title="[SEC-07] OTP của người này dùng được cho email của người kia nếu trùng giá trị",
     Method="POST", Endpoint="/api/reset-password",
     Preconditions="Cả hai tài khoản victim và attacker đều đã gọi forgot-password. Ghi lại OTP của attacker",
     Request_Headers="-",
     Request_Body='{"email":"api.victim.23127060@test.local","resetToken":"{{attackerResetToken}}","newPassword":"Hacked123!"}',
     Expected_Status="400",
     Expected_Assertions="OTP của tài khoản khác phải bị từ chối; mật khẩu của victim KHÔNG được đổi; với không gian chỉ 9000 giá trị, xác suất hai OTP trùng nhau là đáng kể nên điều kiện AND email + token là không đủ",
     Oracle="SPEC", SEC_Ref="SEC-07", Priority="P0", Tag="@contract", Bug_Ref="A-02",
     Why_AI_Missed="SPECGAP - Đặc tả chỉ nói 'OTP chỉ hợp lệ cho email đã yêu cầu', và câu UPDATE của SUT có cả hai điều kiện WHERE email = ? AND reset_token = ? nên thoạt nhìn là đúng. Cái đặc tả KHÔNG nói là không gian OTP phải đủ lớn để hai người không trùng mã. Với 4 chữ số, chỉ cần 100 người cùng đang chờ reset là khả năng trùng vượt 40%. AI không có câu nào trong đặc tả để bám vào nên không sinh case này."),

# ============================== API-2 — FR-08 ==============================
dict(TC_ID="TC-B2-DOM-901", API="API-2", FR="FR-08", Category="DOM", Technique="Error Guessing",
     Title="Checkout với total_amount = 1 rồi đọc lại đơn hàng để xác nhận số tiền thật sự được lưu",
     Method="GET", Endpoint="/api/orders/{{orderId}}",
     Preconditions="Giỏ hàng có 1 sản phẩm giá 30.000.000đ. Đã gọi POST /api/checkout với total_amount = 1",
     Request_Headers=BEARER_U, Request_Body="-", Expected_Status="200",
     Expected_Assertions="total_amount của đơn hàng phải bằng tổng tính từ giỏ hàng (30000000), KHÔNG được bằng 1; SRS FR-08: 'Backend phải tự tính lại tổng tiền; không chấp nhận giá trị total_amount do client gửi lên'",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="B-01",
     Why_AI_Missed="API - Bộ sinh có case 'total_amount = 1 phải bị từ chối' nhưng chỉ kiểm mã trả về của chính request checkout. SUT trả 200 nên case đó đã 'phát hiện' được bug, đúng. Nhưng nó không đo được MỨC ĐỘ thiệt hại. Chỉ khi đọc lại đơn hàng mới thấy số 1 thật sự nằm trong CSDL - tức là mua được điện thoại 30 triệu với giá 1 đồng. Bằng chứng này cần request thứ hai, mà bộ sinh chỉ làm việc trên từng request độc lập."),

dict(TC_ID="TC-B2-DOM-902", API="API-2", FR="FR-08", Category="DOM", Technique="Error Guessing",
     Title="Sau khi thanh toán thành công, giỏ hàng phải được xóa",
     Method="GET", Endpoint="/api/cart",
     Preconditions="Đã thêm sản phẩm vào giỏ và gọi POST /api/checkout thành công",
     Request_Headers=BEARER_U, Request_Body="-", Expected_Status="200",
     Expected_Assertions="giỏ hàng phải là mảng rỗng sau checkout (SRS FR-08: 'Sau thanh toán thành công, giỏ hàng được xóa')",
     Oracle="SPEC", SEC_Ref="-", Priority="P1", Tag="@bug", Bug_Ref="B-13",
     Why_AI_Missed="PROMPT - Prompt khoanh API-2 vào POST /api/checkout. Nhưng một yêu cầu của FR-08 lại được kiểm ở một endpoint KHÁC hẳn (GET /api/cart). Bộ sinh phân hoạch theo endpoint nên không có chỗ nào để đặt case 'hậu quả của checkout lên giỏ hàng'. Đây là giới hạn của cách tổ chức spec theo endpoint thay vì theo yêu cầu."),

dict(TC_ID="TC-B2-STA-901", API="API-2", FR="FR-08", Category="STA", Technique="State Transition (chuỗi đầy đủ)",
     Title="Chuỗi đầy đủ pending -> confirmed -> shipping rồi USER tự hủy: bước cuối phải bị chặn",
     Method="PUT", Endpoint="/api/orders/{{orderId}}/cancel",
     Preconditions="Đơn đã đi hết chuỗi: tạo mới (pending) -> admin confirm -> admin chuyển shipping",
     Request_Headers=BEARER_U, Request_Body="{}", Expected_Status="400",
     Expected_Assertions="phải trả 400; trạng thái đơn vẫn phải là 'shipping' sau khi gọi; SRS FR-10: 'Khi đơn hàng đã ở trạng thái shipping, User không được phép tự hủy'",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="B-09",
     Why_AI_Missed="API - Bộ sinh phủ bảng chuyển trạng thái theo từng Ô RIÊNG LẺ (0-switch): mỗi case đặt đơn vào một trạng thái rồi thử một bước chuyển. Nhưng đưa đơn về trạng thái 'shipping' đòi hỏi đi qua ĐÚNG hai bước admin trước đó - một chuỗi 4 request. Muốn phủ đầy đủ phải chuyển sang 1-switch/n-switch coverage, là thứ phải thiết kế tay chứ bộ sinh không tự suy ra được từ bảng trạng thái."),

dict(TC_ID="TC-B2-STA-902", API="API-2", FR="FR-08", Category="STA", Technique="State Transition (o tu chuyen)",
     Title="Chuyển từ pending sang chính pending phải bị từ chối",
     Method="PUT", Endpoint="/api/admin/orders/{{orderId}}/status",
     Preconditions="Đơn đang ở trạng thái pending",
     Request_Headers=BEARER_A, Request_Body='{"status":"pending"}', Expected_Status="400",
     Expected_Assertions="body.error chứa 'Invalid state transition'; trạng thái KHÔNG đổi; sơ đồ FR-10 không có mũi tên nào từ một trạng thái về chính nó",
     Oracle="SPEC", SEC_Ref="-", Priority="P1", Tag="@contract", Bug_Ref="-",
     Why_AI_Missed="MODEL - Bảng chuyển trạng thái trong spec liệt kê các cặp (from, to) KHÁC nhau; 5 ô đường chéo (pending->pending, confirmed->confirmed, ...) bị bỏ trống vì trực quan chúng 'không phải một bước chuyển'. Độ phủ STA của API-2 vì thế dừng ở 20/25. Đây đúng là loại ô hay bị bỏ sót trong thực tế, và cũng là loại ô hay gây lỗi thật (một request bị gửi lại hai lần)."),

dict(TC_ID="TC-B2-SEC-901", API="API-2", FR="FR-08", Category="SEC", Technique="Business Logic Abuse (data-driven)",
     Title="[SEC-02] Bo user_id khoi apply-coupon de dung ma VIP100 qua muc 2 lan cho phep",
     Method="POST", Endpoint="/api/apply-coupon",
     Preconditions="Coupon VIP100 co max_uses_per_user = 2. Chay Collection Runner 3 vong voi data file coupon_abuse.csv",
     Request_Headers="-", Request_Body='{"code":"VIP100","total_amount":500000}',
     Expected_Status="401",
     Expected_Assertions="apply-coupon phải yêu cầu JWT và lấy user từ token (SRS FR-09 điều kiện C4); không được lấy user_id từ body; vòng thứ 3 phải bị từ chối vì đã hết lượt",
     Oracle="SPEC", SEC_Ref="SEC-02", Priority="P0", Tag="@bug", Bug_Ref="B-07",
     Why_AI_Missed="MODEL - Bộ sinh coi 'thiếu tham số bắt buộc' là một lớp không hợp lệ, nên sinh case 'thiếu user_id -> phải trả 400/401'. Nó không nhận ra rằng trong code, THIẾU tham số này lại là đường vòng qua toàn bộ kiểm tra hạn mức: nhánh `if (user_id)` bị bỏ qua hẳn. Đây là nghịch lý 'bỏ bớt dữ liệu để được nhiều quyền hơn', chỉ thấy được khi đọc mã nguồn chứ không suy ra từ hình dạng API."),

dict(TC_ID="TC-B2-SEC-902", API="API-2", FR="FR-08", Category="SEC", Technique="Data Integrity",
     Title="[-] POST /api/coupon-usage ghi nhận lượt dùng cho một coupon_id không tồn tại",
     Method="POST", Endpoint="/api/coupon-usage",
     Preconditions="Da login, co {{token_user}}",
     Request_Headers=BEARER_U, Request_Body='{"coupon_id":999999}', Expected_Status="400",
     Expected_Assertions="phải từ chối coupon_id không tồn tại; bảng coupon_usage KHÔNG được phát sinh bản ghi rác; bản ghi rác sẽ làm sai phép đếm hạn mức sử dụng của FR-09 điều kiện C5",
     Oracle="SPEC", SEC_Ref="-", Priority="P1", Tag="@bug", Bug_Ref="B-11",
     Why_AI_Missed="SPECGAP - api_specification.md không hề liệt kê endpoint POST /api/coupon-usage; nó chỉ xuất hiện trong server.js với một dòng comment. Bộ sinh đọc đặc tả nên không biết endpoint này tồn tại. Đây là lỗi 'endpoint không được tài liệu hóa' - loại bề mặt tấn công mà kiểm thử dựa trên đặc tả không bao giờ chạm tới."),

# ============================== API-3 — FR-15 ==============================
dict(TC_ID="TC-C3-SCH-901", API="API-3", FR="FR-15", Category="SCH", Technique="Cross-request Type Consistency",
     Title="Kiểu của trường price phải giống nhau giữa sản phẩm id lẻ và id chẵn",
     Method="GET", Endpoint="/api/products/2",
     Preconditions="Đã gọi GET /api/products/1 trước đó và lưu lại kiểu của trường price",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="typeof price của id=2 phải bằng typeof price của id=1; cả hai đều phải là number; GET /api/products (danh sách) cũng phải trả price kiểu number cho MỌI phần tử",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="C-05",
     Why_AI_Missed="API - Mỗi request riêng lẻ đều hợp lệ: `{\"price\": 30000000}` đúng schema, và `{\"price\": \"28000000\"}` cũng là một JSON hợp lệ. Vi phạm chỉ hiện ra khi SO SÁNH hai response với nhau. Bộ sinh đánh giá từng case độc lập nên không có chỗ nào để đặt một khẳng định bậc cao hơn liên kết hai request. Nếu chỉ test id lẻ (như ví dụ trong tài liệu hay dùng) thì không bao giờ thấy bug này."),

dict(TC_ID="TC-C3-SEC-901", API="API-3", FR="FR-15", Category="SEC", Technique="Destructive Test",
     Title="[SEC-02] Khách vãng lai xóa được toàn bộ catalog rồi kiểm số sản phẩm còn lại",
     Method="GET", Endpoint="/api/products",
     Preconditions="Đã gọi DELETE /api/products/:id cho cả 5 sản phẩm seed MÀ KHÔNG kèm header Authorization",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="danh sách sản phẩm phải còn nguyên 5 phần tử vì các lệnh DELETE không token đáng lẽ phải bị từ chối 401; nếu danh sách rỗng thì một người không đăng nhập đã xóa sạch catalog",
     Oracle="SPEC", SEC_Ref="SEC-02", Priority="P0", Tag="@bug", Bug_Ref="C-01",
     Why_AI_Missed="API - Bộ sinh có case 'DELETE không token -> phải 401', và case đó đã bắt được bug. Nhưng một dòng 'expected 401, got 200' trong báo cáo không nói lên được mức độ. Case này đo HẬU QUẢ: sau 5 request không xác thực thì cửa hàng không còn sản phẩm nào để bán. Cùng một bug, nhưng bằng chứng này mới đủ sức thuyết phục người ra quyết định. Cần chuỗi 6 request."),

dict(TC_ID="TC-C3-DOM-901", API="API-3", FR="FR-15", Category="DOM", Technique="Partial Update",
     Title="PUT chỉ gửi trường name: các trường không gửi KHÔNG được bị ghi đè thành null",
     Method="GET", Endpoint="/api/products/{{newProductId}}",
     Preconditions="Đã tạo sản phẩm đầy đủ 5 trường, sau đó gọi PUT chỉ với {\"name\": \"Ten moi 23127060\"}",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="name phải là tên mới; NHƯNG price, description, imageUrl, category_id phải giữ nguyên giá trị cũ, KHÔNG được biến thành null; SRS FR-15: 'Khi Sửa một sản phẩm, chỉ sản phẩm đó bị thay đổi'",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="C-09",
     Why_AI_Missed="API - Bộ sinh phủ từng tham số của PUT một cách độc lập: gửi name sai, gửi price sai... Mọi case đều gửi ĐỦ 5 trường rồi đổi một trường. Không case nào gửi THIẾU trường, vì 'thiếu trường' được coi là lớp không hợp lệ của chính trường đó chứ không phải một phép thử về hành vi cập nhật một phần. Cần chuỗi POST -> PUT -> GET mới thấy được 4 trường còn lại đã bị xóa trắng."),

dict(TC_ID="TC-C3-SCH-902", API="API-3", FR="FR-15", Category="SCH", Technique="Content Negotiation",
     Title="Response lỗi phải là application/json, không được là HTML",
     Method="GET", Endpoint="/api/products?search=%27",
     Preconditions="SUT da seed",
     Request_Headers="-", Request_Body="-", Expected_Status="400",
     Expected_Assertions="header Content-Type phải chứa 'application/json'; body phải parse được thành JSON có trường error; body KHÔNG được chứa thẻ HTML nào (<h1>, <p>); không được lộ thông điệp lỗi của tầng CSDL",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="C-03",
     Why_AI_Missed="MODEL - Bộ sinh mặc định mọi response của một REST API đều là JSON, nên nó khẳng định lên NỘI DUNG body mà không bao giờ khẳng định lên HEADER Content-Type. Khi SUT trả về HTML, bước pm.response.json() ném lỗi và test thất bại với thông báo 'Unexpected token <' - một lỗi trông dẫn đến chẩn đoán sai là 'test bị hỏng' chứ không phải 'API vi phạm hợp đồng'. Phải kiểm Content-Type TRƯỚC khi parse."),

dict(TC_ID="TC-C3-DOM-902", API="API-3", FR="FR-15", Category="DOM", Technique="Referential Integrity",
     Title="Tạo sản phẩm với category_id không tồn tại rồi đối chiếu với danh sách danh mục",
     Method="GET", Endpoint="/api/categories",
     Preconditions="Da goi POST /api/products voi category_id = 9999",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="danh sách danh mục chỉ có id 1, 2, 3; sản phẩm vừa tạo trỏ tới category_id = 9999 là một tham chiếu treo; SRS FR-15: 'Danh mục: bắt buộc, phải chọn từ danh sách có sẵn'",
     Oracle="SPEC", SEC_Ref="-", Priority="P1", Tag="@bug", Bug_Ref="C-10",
     Why_AI_Missed="API - Bộ sinh có case 'category_id = 9999 phải bị từ chối'. Nhưng để CHỨNG MINH đây là tham chiếu treo chứ không phải một danh mục thật mà mình không biết, phải đọc bảng categories bằng một request thứ hai. Ràng buộc toàn vẹn tham chiếu về bản chất nói về QUAN HỆ giữa hai tài nguyên, không thể kiểm trong phạm vi một request."),

dict(TC_ID="TC-C3-SEC-902", API="API-3", FR="FR-15", Category="SEC", Technique="SQL Injection (data exfiltration)",
     Title="[SEC-05] UNION SELECT qua ?search đọc được mật khẩu plaintext trong bảng users",
     Method="GET", Endpoint="/api/products?search=%25%27%20UNION%20SELECT%20id%2Cemail%2Cpassword%2Crole%2C1%20FROM%20users--%20",
     Preconditions="SUT da seed; bang users co admin@eshop.com",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="kết quả trả về chỉ được chứa sản phẩm, KHÔNG được chứa chuỗi '@eshop.com' hay 'Admin123!'; số cột của products (5) trùng với số cột chọn từ users nên UNION ghép được - đây là điều Parameterized Query (SEC-05) ngăn chặn",
     Oracle="SPEC", SEC_Ref="SEC-05", Priority="P0", Tag="@bug", Bug_Ref="C-02",
     Why_AI_Missed="API - Bộ sinh có payload UNION SELECT nhưng viết chung chung với 5 cột tùy ý. UNION trong SQLite chỉ chạy khi SỐ CỘT KHỚP CHÍNH XÁC; đoán sai số cột thì chỉ nhận được lỗi và kết luận nhầm là 'đã được bảo vệ'. Phải đọc database.js đếm đúng 5 cột của bảng products rồi chọn đúng 5 cột từ users. Đó là bước trinh sát lấy từ MÃ NGUỒN, không thể suy ra từ đặc tả."),
]

DEFAULTS = dict(Source="HUMAN", Audit_Label="VALID",
                Audit_Note="Case do sinh viên tự viết sau khi đọc mã nguồn SUT; không qua bộ sinh tự động.")


def main():
    add = {1: [], 2: [], 3: []}
    for e in EXTRA:
        n = int(e["API"].split("-")[1])
        row = {c: "-" for c in COLS}
        row.update(DEFAULTS)
        row.update(e)
        add[n].append(row)

    for n in (1, 2, 3):
        src = "testcases/API-%d_audited.csv" % n
        dst = "testcases/API-%d_final.csv" % n
        with open(src, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        rows += add[n]
        with open(dst, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            w.writerows(rows)
        h = sum(1 for r in rows if r["Source"] == "HUMAN")
        print("API-%d: %s -> %s | tổng %d case (AI %d + HUMAN %d)"
              % (n, src, dst, len(rows), len(rows) - h, h))


if __name__ == "__main__":
    main()
