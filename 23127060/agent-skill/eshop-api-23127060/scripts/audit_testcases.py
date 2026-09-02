#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_testcases.py - Gắn nhãn VALID / INVALID / INCOMPLETE cho test case do AI sinh.

  python3 audit_testcases.py --in testcases/API-1_generated.csv --out testcases/API-1_audited.csv
  python3 audit_testcases.py --report          # in bang thong ke cho ca 3 API

Đề bài mục 6.2 đòi: "Label each AI-generated test case VALID / INVALID / INCOMPLETE with
reasoning, and correct the invalid or incomplete ones."

Vì sao dùng script thay vì sửa tay từng dòng:
  225 test case sửa tay thì không thể tái lập và không thể kiểm chứng. Ở đây mỗi nhãn đều
  đến từ một LUẬT viết rõ ràng, bám vào một câu cụ thể trong eshop-sut/README.md. Ai đọc
  file này cũng kiểm tra được luật có đúng không, và chạy lại cho ra đúng kết quả đó.
  Phần đòi hỏi phán đoán riêng cho từng case (chủ yếu là gán lại mã SEC) nằm trong bảng
  OVERRIDES bên dưới, mỗi dòng đều kèm lý do.

Nhãn:
  VALID      bước, dữ liệu, kỳ vọng đều đúng so với SRS; chạy được ngay.
  INVALID    kỳ vọng sai / không có căn cứ trong SRS / tham số bịa / mâu thuẫn nội tại.
             BẮT BUỘC sửa rồi ghi rõ đã sửa gì.
  INCOMPLETE ý tưởng đúng nhưng thiếu assertion, thiếu precondition, hoặc oracle chưa rõ.
             BẮT BUỘC bổ sung.
"""
import argparse
import csv
import os
import re
from collections import Counter, defaultdict

COLUMNS = None  # lấy từ file đầu vào

# ---------------------------------------------------------------------------
# BANG 1 — Gan lai ma SEC.
#
# Toàn bộ cột SEC_Ref do AI sinh đều bám theo một bảng SEC SUY DIỄN THEO OWASP
# (SEC-01=SQLi, SEC-04=IDOR, SEC-05=role escalation, SEC-07=brute force).
# Bang SEC THAT nam o eshop-sut/README.md muc 9 va khac han:
#
#   SEC-01 Mật khẩu không được lưu plaintext
#   SEC-02 API có tính bảo mật phải yêu cầu JWT hợp lệ
#   SEC-03 API Admin phải kiểm role='admin', không chỉ kiểm token tồn tại
#   SEC-04 Dữ liệu user nhập phải được escape khi hiển thị (stored XSS)
#   SEC-05 Truy vấn CSDL phải dùng Parameterized Query
#   SEC-06 API cập nhật hồ sơ không được cho đổi trường role từ client
#   SEC-07 OTP reset phải >= 6 chữ số, có thời hạn, vô hiệu hóa sau khi dùng
#
# Vì vậy gần như mọi case SEC đều bị gán sai mã. Đây không phải lỗi vặt: cột SEC_Ref là
# thứ duy nhất chứng minh độ phủ bảo mật trong báo cáo, gán sai là báo cáo sai.
# ---------------------------------------------------------------------------
SEC_REMAP = {
    # --- API-1 ---
    "TC-A1-SEC-001": ("SEC-05", "SQLi là vi phạm SEC-05 (parameterized query), không phải SEC-01 (lưu mật khẩu plaintext)."),
    "TC-A1-SEC-002": ("SEC-05", "Nhu tren: SQLi thuoc SEC-05."),
    "TC-A1-SEC-003": ("SEC-07", "Trả thẳng OTP ra response là lỗi vòng đời OTP -> SEC-07, không phải SEC-02 (yêu cầu JWT)."),
    "TC-A1-SEC-004": ("-", "User enumeration KHÔNG được bất kỳ mã SEC-01..07 nào phủ. Vẫn là test hợp lệ nhưng phải để SEC_Ref = '-' thay vì gán bừa."),
    "TC-A1-SEC-005": ("SEC-01", "Response login lộ trường password chính là bằng chứng mật khẩu được lưu plaintext -> đúng SEC-01."),
    "TC-A1-SEC-006": ("SEC-07", "Reset phải đòi OTP hợp lệ -> thuộc vòng đời OTP SEC-07, không phải SEC-03 (kiểm role admin)."),
    "TC-A1-SEC-007": ("SEC-07", "'OTP chỉ hợp lệ cho email đã yêu cầu' là yêu cầu của SEC-07 + FR-03, không phải SEC-04 (escape XSS)."),
    "TC-A1-SEC-008": ("SEC-06", "Gửi kèm trường role đúng là SEC-06; SEC-05 là parameterized query."),
    "TC-A1-SEC-009": ("SEC-04", "Payload XSS thuộc SEC-04; SEC-06 chỉ nói riêng về trường role."),
    "TC-A1-SEC-010": ("SEC-04", "Nhu tren."),
    "TC-A1-SEC-011": ("SEC-07", "Dò token thuộc SEC-07 (entropy OTP) - mã đúng, nhưng kỳ vọng 429 sai, xem luật R1."),
    "TC-A1-SEC-012": ("-", "Khóa tài khoản sau 3 lần sai là FR-02, không nằm trong SEC-01..07."),
    "TC-A1-SEC-013": ("SEC-07", "Mã đúng nhưng nội dung case sai, xem luật R1."),
    # --- API-2 ---
    "TC-B2-SEC-001": ("SEC-05", "SQLi -> SEC-05."),
    "TC-B2-SEC-002": ("-", "Không lộ stack trace không được SEC-01..07 phủ."),
    "TC-B2-SEC-003": ("SEC-02", "Thiếu JWT -> SEC-02; SEC-03 dành riêng cho việc kiểm role."),
    "TC-B2-SEC-004": ("SEC-02", "Nhu tren."),
    "TC-B2-SEC-005": ("SEC-02", "Token sai chữ ký = token không hợp lệ -> SEC-02."),
    "TC-B2-SEC-006": ("SEC-02", "GET /api/orders/:id thiếu hẳn middleware xác thực -> vi phạm SEC-02. SEC-04 là escape XSS."),
    "TC-B2-SEC-007": ("SEC-02", "Nhu tren."),
    "TC-B2-SEC-008": ("SEC-02", "Nhu tren."),
    "TC-B2-SEC-009": ("SEC-03", "User thuong goi API admin -> dung SEC-03; SEC-05 la parameterized query."),
    "TC-B2-SEC-010": ("SEC-03", "Nhu tren."),
    "TC-B2-SEC-011": ("SEC-04", "XSS -> SEC-04."),
    "TC-B2-SEC-012": ("-", "Mass assignment trường 'status' không phải 'role' nên không thuộc SEC-06; đây là yêu cầu FR-08/FR-10."),
    "TC-B2-SEC-013": ("-", "Hạn mức sử dụng coupon là FR-09 điều kiện C5, không nằm trong SEC-01..07."),
    "TC-B2-SEC-014": ("SEC-06", "Đã viết lại thành chuỗi leo thang quyền (xem luật R1)."),
    # --- API-3 ---
    "TC-C3-SEC-001": ("SEC-05", "SQLi -> SEC-05."),
    "TC-C3-SEC-002": ("SEC-05", "Nhu tren."),
    "TC-C3-SEC-003": ("SEC-05", "Trả về thông điệp lỗi SQL là hệ quả trực tiếp của việc nối chuỗi -> vẫn là SEC-05."),
    "TC-C3-SEC-004": ("-", "Xem luật R5: tham số ?debug=true không tồn tại."),
    "TC-C3-SEC-005": ("SEC-02", "Thiếu JWT -> SEC-02."),
    "TC-C3-SEC-006": ("SEC-02", "Nhu tren."),
    "TC-C3-SEC-007": ("SEC-02", "Nhu tren."),
    "TC-C3-SEC-008": ("SEC-02", "Token sai chu ky -> SEC-02."),
    "TC-C3-SEC-009": ("SEC-03", "User thường sửa sản phẩm = thiếu kiểm role -> SEC-03, không phải SEC-04."),
    "TC-C3-SEC-010": ("SEC-03", "Dung SEC-03; truoc do gan SEC-05."),
    "TC-C3-SEC-011": ("SEC-03", "Nhu tren."),
    "TC-C3-SEC-012": ("SEC-04", "Stored XSS -> SEC-04."),
    "TC-C3-SEC-013": ("-", "Ghi đè khóa chính 'id' không phải trường 'role' nên không thuộc SEC-06."),
    "TC-C3-SEC-014": ("SEC-06", "Đã viết lại thành chuỗi leo thang quyền (xem luật R1)."),
}

# --- Các case NGOÀI nhóm SEC nhưng vẫn bị gán mã SEC theo bảng suy diễn ---
# Cùng một lỗi hệ thống: SQLi bị gán SEC-01, XSS bị gán SEC-06, IDOR bị gán SEC-04,
# leo thang quyen bi gan SEC-05. Chung nam rai rac trong nhom DOM/STA nen de bi bo sot
# hơn các case trong nhóm SEC.
SEC_REMAP.update({
    "TC-A1-DOM-013": ("SEC-07", "Dùng OTP của tài khoản khác chính là điều SEC-07 + FR-03 quy định ('OTP chỉ hợp lệ cho email đã yêu cầu'), không phải SEC-04 (escape XSS)."),
    "TC-A1-DOM-022": ("SEC-05", "SQLi -> SEC-05 (parameterized query), không phải SEC-01 (lưu mật khẩu plaintext)."),
    "TC-A1-DOM-026": ("-", "Độ mạnh mật khẩu là yêu cầu FR-01/FR-03, không nằm trong SEC-01..07. SEC-06 chỉ nói riêng về trường role."),
    "TC-A1-DOM-029": ("-", "Như trên: độ dài mật khẩu là FR-01, không phải mã SEC."),
    "TC-A1-DOM-031": ("-", "Nhu tren: yeu cau co chu hoa la FR-01."),
    "TC-A1-DOM-032": ("-", "Nhu tren: yeu cau co chu so la FR-01."),
    "TC-A1-DOM-033": ("-", "Như trên: mật khẩu yếu vi phạm FR-01, không phải mã SEC."),
    "TC-A1-DOM-034": ("SEC-04", "Payload <script> -> SEC-04 (escape du lieu user nhap)."),
    "TC-B2-DOM-022": ("SEC-04", "Payload <script> trong shipping_address -> SEC-04. SRS FR-18 còn nói rõ địa chỉ giao hàng phải hiển thị an toàn."),
    "TC-B2-DOM-031": ("SEC-05", "SQLi -> SEC-05."),
    "TC-B2-DOM-039": ("SEC-02", "Lấy user_id từ body thay vì từ JWT là vi phạm SEC-02 (API bảo mật phải dựa trên token hợp lệ), không phải SEC-04."),
    "TC-B2-STA-020": ("SEC-03", "User thường tự xác nhận đơn hàng = thao tác admin không kiểm role -> SEC-03, không phải SEC-05."),
    "TC-C3-DOM-009": ("SEC-04", "Stored XSS qua tên sản phẩm -> SEC-04."),
    "TC-C3-DOM-026": ("SEC-04", "URL scheme javascript: la vector XSS khi render -> SEC-04."),
    "TC-C3-DOM-027": ("-", "Path traversal trong imageUrl không được bất kỳ mã SEC-01..07 nào phủ. Vẫn là test hợp lệ, để SEC_Ref = '-'."),
    "TC-C3-DOM-034": ("SEC-05", "SQLi trong path param -> SEC-05."),
    "TC-C3-DOM-037": ("SEC-04", "Stored XSS qua description -> SEC-04."),
    "TC-C3-DOM-045": ("SEC-05", "Làm vỡ câu SQL bằng một dấu nháy đơn -> bằng chứng trực tiếp của việc nối chuỗi -> SEC-05."),
    "TC-C3-DOM-046": ("SEC-05", "SQLi -> SEC-05."),
    "TC-C3-DOM-047": ("SEC-05", "SQLi UNION SELECT -> SEC-05."),
    "TC-C3-DOM-048": ("SEC-05", "SQLi stacked query -> SEC-05."),
    "TC-C3-DOM-049": ("SEC-04", "Reflected XSS qua tham so search -> SEC-04."),
})

# ---------------------------------------------------------------------------
# BẢNG 2 — Các case phải VIẾT LẠI vì kỳ vọng không có căn cứ trong SRS,
# hoặc vì tham số / trạng thái được bịa ra.
# Mỗi mục: (nhãn, lý do, các cột cần ghi đè)
# ---------------------------------------------------------------------------
REWRITE = {
    # ---- R1: ky vong 429 (rate limiting) ----
    "TC-A1-SEC-011": ("INVALID",
        "R1 - Kỳ vọng 429 không có căn cứ: không một dòng nào trong FR-01..FR-24 hay SEC-01..07 yêu cầu rate limiting. AI suy ra từ thói quen bảo mật chung chứ không từ đặc tả. ĐÃ SỬA: giữ nguyên kịch bản dò 20 giá trị (vẫn là cách chứng minh entropy yếu) nhưng đổi oracle sang điều SRS THỰC SỰ nói - SEC-07 đòi OTP tối thiểu 6 chữ số: khẳng định độ dài token >= 6 và không lần dò nào được chấp nhận.",
        {"Expected_Status": "400",
         "Expected_Assertions": "mỗi lần dò đều trả 400; độ dài resetToken lấy từ forgot-password phải >= 6 ký tự theo SEC-07",
         "Title": "[SEC-07] Dò 20 giá trị token: không lần nào được chấp nhận và OTP phải dài >= 6 chữ số",
         "Bug_Ref": "A-02"}),
    "TC-A1-SEC-013": ("INVALID",
        "R1 - Kỳ vọng 429 không có căn cứ trong SRS (không có yêu cầu giới hạn số lần gọi). ĐÃ SỬA: đổi thành điều SEC-07 thật sự quy định - OTP phải được vô hiệu hóa khi bị thay thế: xin OTP lần 2 rồi dùng lại OTP lần 1.",
        {"Expected_Status": "400",
         "Expected_Assertions": "OTP cấp lần 1 phải bị vô hiệu hóa sau khi cấp OTP lần 2; body có trường error",
         "Title": "[SEC-07] Xin OTP lần 2 thì OTP lần 1 phải bị vô hiệu hóa",
         "Technique": "State Transition", "Bug_Ref": "A-04"}),
    "TC-B2-SEC-014": ("INVALID",
        "R1 - Kỳ vọng 429 không có căn cứ trong SRS. ĐÃ SỬA: thay bằng chuỗi leo thang quyền thật sự kiểm được và vi phạm SEC-06 - user thường tự nâng role='admin' qua PUT /api/users/me rồi gọi API admin đổi trạng thái đơn. Bug X-01 phát hiện ở STEP 0.",
        {"Expected_Status": "403",
         "Expected_Assertions": "PUT /api/users/me KHÔNG được phép đổi role; role sau khi gọi vẫn là 'user'; bước gọi API admin sau đó phải bị từ chối",
         "Title": "[SEC-06] User thường tự nâng role='admin' rồi đổi trạng thái đơn hàng",
         "Method": "PUT", "Endpoint": "/api/users/me",
         "Request_Body": '{"name":"Attacker 23127060","phone":"0900000000","shipping_address":"Q5","role":"admin"}',
         "Request_Headers": "Authorization: Bearer {{token_attacker}}",
         "Technique": "Privilege Escalation", "Bug_Ref": "X-01", "Tag": "@bug", "Priority": "P0"}),
    "TC-C3-SEC-014": ("INVALID",
        "R1 - Kỳ vọng 429 không có căn cứ trong SRS. ĐÃ SỬA: thay bằng chuỗi leo thang quyền SEC-06 -> SEC-03: user thường tự nâng role rồi tạo sản phẩm.",
        {"Expected_Status": "403",
         "Expected_Assertions": "role sau khi gọi PUT /api/users/me vẫn phải là 'user'; POST /api/products sau đó phải trả 403",
         "Title": "[SEC-06] User thường tự nâng role='admin' rồi tạo sản phẩm",
         "Method": "PUT", "Endpoint": "/api/users/me",
         "Request_Body": '{"name":"Attacker 23127060","phone":"0900000000","shipping_address":"Q5","role":"admin"}',
         "Request_Headers": "Authorization: Bearer {{token_attacker}}",
         "Technique": "Privilege Escalation", "Bug_Ref": "X-01", "Tag": "@bug", "Priority": "P0"}),

    # ---- R2: kỳ vọng 409 không có căn cứ ----
    "TC-C3-DOM-041": ("INVALID",
        "R2 - Kỳ vọng 409 không có căn cứ: SRS FR-15 chỉ nói 'Admin có thể Thêm/Xem/Sửa/Xóa sản phẩm', không hề đặt ràng buộc khóa ngoại giữa sản phẩm và đơn hàng. AI suy diễn từ kinh nghiệm CSDL. ĐÃ SỬA: kỳ vọng 200 (xóa thành công) và bổ sung khẳng định sản phẩm thực sự biến mất.",
        {"Expected_Status": "200",
         "Endpoint": "/api/products/{{newProductId}}",
         "Expected_Assertions": "body có message; GET lại sản phẩm đó sau khi xóa KHÔNG được trả về dữ liệu (bug C-04 trả 200 {})",
         "Title": "DELETE /api/products/:id (xóa sản phẩm vật thử do _setup tạo ra)",
         "Bug_Ref": "C-08"}),
    # Ghi chú thêm: ban đầu case này xóa sản phẩm id = 1. Nhưng id = 1 là vật cố định được
    # hàng chục case khác dùng làm mốc (vd TC-C3-DOM-051 kiểm kiểu của price ở id lẻ). Xóa nó
    # ở giữa lần chạy khiến những case chạy sau đó thất bại vì một lý do không liên quan gì
    # đến chính chúng. Đã đổi sang sản phẩm thứ do folder _setup tạo riêng.
    "TC-C3-STA-007": ("INVALID",
        "R2 - Kỳ vọng 409 không có căn cứ: SRS không yêu cầu tên sản phẩm duy nhất, và cột 'name' trong database.js không có ràng buộc UNIQUE. ĐÃ SỬA: kỳ vọng 201 (tạo thành công) và chuyển trọng tâm sang điều kiểm được - hai bản ghi phải có id khác nhau.",
        {"Expected_Status": "201",
         "Expected_Assertions": "tạo thành công; id trả về khác id của sản phẩm đầu tiên; SRS không cấm trùng tên",
         "Title": "Tạo sản phẩm trùng tên với sản phẩm đã có (SRS không cấm)",
         "Tag": "@bug", "Bug_Ref": "C-12"}),

    # ---- R4: mau thuan noi tai ----
    "TC-A1-STA-006": ("INVALID",
        "R4 - Mâu thuẫn nội tại: case đánh dấu chuyển trạng thái HỢP LỆ nhưng lại kỳ vọng 400. Ngoài ra 'EXPIRED' không phải một trạng thái mà bộ sinh điều khiển được: SUT không lưu thời điểm cấp OTP nên không thể đưa OTP về trạng thái hết hạn qua API. ĐÃ SỬA: đổi thành chuyển KHÔNG hợp lệ ISSUED -> USED_TWICE (dùng lại OTP đã dùng), là điều SEC-07 quy định rõ và kiểm được hoàn toàn qua API.",
        {"Expected_Status": "400",
         "Expected_Assertions": "lần reset thứ hai với cùng OTP phải bị từ chối; body có trường error",
         "Title": "Chuyển trạng thái USED -> USED (dùng lại OTP đã dùng - KHÔNG hợp lệ)",
         "Preconditions": "Đã reset mật khẩu thành công một lần bằng OTP này",
         "Tag": "@contract", "Bug_Ref": "-"}),
    "TC-C3-STA-009": ("INVALID",
        "R4 - Mâu thuẫn nội tại: đánh dấu KHÔNG hợp lệ nhưng kỳ vọng 200. Ngoài ra 'IN_SEARCH' không phải một trạng thái của vòng đời tài nguyên mà là một phép đọc. ĐÃ SỬA: giữ phép kiểm (sản phẩm đã xóa không được xuất hiện trong kết quả tìm kiếm) nhưng phát biểu lại cho đúng: kỳ vọng 200 với mảng KHÔNG chứa sản phẩm đã xóa.",
        {"Expected_Status": "200",
         "Expected_Assertions": "HTTP 200 với mảng kết quả; mảng KHÔNG được chứa sản phẩm vừa bị xóa",
         "Title": "Sau khi DELETE, sản phẩm không được còn trong kết quả GET /api/products?search="}),

    # ---- R5: tham so bia ----
    "TC-C3-SEC-004": ("INVALID",
        "R5 - Tham số bịa: `?debug=true` không tồn tại trong api_specification.md lẫn trong server.js. AI tự nghĩ ra một cờ debug để test. Test sẽ 'pass' nhưng không chứng minh điều gì vì tham số bị bỏ qua hoàn toàn. ĐÃ SỬA: bỏ tham số bịa, kiểm đúng điều có thể kiểm - response sản phẩm không được chứa trường nằm ngoài schema đã đặc tả.",
        {"Endpoint": "/api/products/1",
         "Expected_Assertions": "body chỉ được chứa đúng 6 trường id,name,price,description,imageUrl,category_id; không có trường nội bộ nào khác",
         "Title": "[--] Response sản phẩm không được chứa trường nằm ngoài schema"}),

    # ---- R3b: kỳ vọng không có căn cứ (không liên quan SEC) ----
    "TC-A1-DOM-035": ("INVALID",
        "R3b - Kỳ vọng 400 không có căn cứ: SRS FR-01/FR-03 chỉ đòi mật khẩu mới THỎA ĐIỀU KIỆN ĐỘ MẠNH, không hề cấm đặt lại trùng mật khẩu cũ. AI áp một chính sách mà đặc tả không có. ĐÃ SỬA: kỳ vọng 200, và thêm khẳng định mật khẩu cũ vẫn đăng nhập được (vì nó chính là mật khẩu mới).",
        {"Expected_Status": "200",
         "Expected_Assertions": "reset thành công; SRS không cấm đặt lại trùng mật khẩu cũ; login bằng mật khẩu đó phải thành công",
         "Title": "POST /api/reset-password | newPassword = Api1234! (đặt lại trùng mật khẩu cũ - SRS không cấm)"}),
}

# ---------------------------------------------------------------------------
# BẢNG 3 — Case có ý tưởng đúng nhưng kỳ vọng dựa trên suy diễn, không phải điều
# SRS viết ra. Không sai đến mức INVALID, nhưng phải ghi rõ oracle là suy diễn.
# ---------------------------------------------------------------------------
INFERRED_ORACLE = {
    "TC-A1-DOM-002": "email không tồn tại vẫn trả 200 (chống user enumeration)",
    "TC-A1-DOM-009": "email không phân biệt hoa thường",
    "TC-A1-DOM-010": "email tu cat khoang trang dau-cuoi",
    "TC-A1-DOM-020": "do dai OTP duoi bien",
    "TC-A1-DOM-021": "do dai OTP tren bien",
}

# Chỉ những assertion THẬT SỰ chung chung. Lưu ý: assertion mặc định của nhóm STA
# ("body.error chua Invalid state transition; trang thai KHONG doi") KHÔNG nằm trong đây,
# vì vế cuối của nó đã chính là phép kiểm tác dụng phụ mà luật R7 đòi hỏi.
GENERIC_ASSERTS = {
    "body là JSON; có trường error",
    "body là JSON; khớp schema thành công",
}
MUTATING = {"POST", "PUT", "DELETE", "PATCH"}

# Luật R7 chỉ có nghĩa khi thao tác bị từ chối CÓ một tác dụng phụ QUAN SÁT ĐƯỢC.
# Doi chieu tung endpoint voi server.js:
#   - /api/checkout, /api/products, /api/categories, /api/admin/*, /api/orders/:id/cancel,
#     /api/users/me, /api/coupon-usage  -> có INSERT/UPDATE/DELETE, đọc lại được qua GET.
#   - /api/reset-password                -> UPDATE users.password, kiểm được bằng cách login lại.
#   - /api/apply-coupon                  -> THUẦN TÍNH TOÁN, không ghi gì cả.
#   - /api/forgot-password               -> có ghi reset_token nhưng trên nhánh lỗi thì không có
#                                           user nào để mà đọc lại, nên không quan sát được.
#   - /api/login, /api/register          -> không phải đối tượng kiểm của 3 API đã chọn.
# Đòi hỏi "chứng minh thao tác không xảy ra" ở hai nhóm cuối là đòi hỏi một phép kiểm
# không tồn tại -> sẽ biến nhãn INCOMPLETE thành vô nghĩa.
OBSERVABLE_WRITE = (
    "/api/checkout", "/api/products", "/api/categories", "/api/admin/",
    "/api/orders/", "/api/users/me", "/api/coupon-usage", "/api/reset-password",
)


def has_observable_side_effect(r):
    if r["Method"] not in MUTATING:
        return False
    ep = r["Endpoint"].split("?")[0]
    return any(ep.startswith(x) for x in OBSERVABLE_WRITE)


def audit_row(r):
    "Trả về (label, note, overrides). Thứ tự luật là thứ tự ưu tiên."
    tc = r["TC_ID"]
    notes = []
    ov = {}
    label = None

    # --- Luật SEC: gán lại mã SEC (áp dụng trước, có thể cộng dồn với luật khác) ---
    if tc in SEC_REMAP:
        new_sec, why = SEC_REMAP[tc]
        if new_sec != r["SEC_Ref"]:
            ov["SEC_Ref"] = new_sec
            notes.append("R3 - Gan sai ma SEC (%s -> %s). %s" % (r["SEC_Ref"], new_sec, why))
            label = "INVALID"

    # --- Luật viết lại (R1, R2, R4, R5, R3b) ---
    if tc in REWRITE:
        lab, why, fixes = REWRITE[tc]
        label = "INVALID"
        notes.append(why)
        ov.update(fixes)

    if label == "INVALID":
        return label, " | ".join(notes), ov

    # --- Luật oracle suy diễn ---
    if tc in INFERRED_ORACLE:
        notes.append("R6 - Kỳ vọng '%s' KHÔNG được SRS phát biểu trực tiếp; đây là suy diễn từ thông lệ. ĐÃ SỬA: ghi rõ Oracle = SPEC(suy diễn) để người chấm phân biệt được với các kỳ vọng trích thẳng từ đặc tả." % INFERRED_ORACLE[tc])
        ov["Oracle"] = "SPEC(suy dien)"
        return "INCOMPLETE", " | ".join(notes), ov

    # --- Luật assertion chung chung ---
    a = r["Expected_Assertions"].strip()
    st = int(r["Expected_Status"])
    if a in GENERIC_ASSERTS:
        if has_observable_side_effect(r) and st >= 400:
            notes.append("R7 - Case từ chối một thao tác GHI nhưng chỉ kiểm 'có trường error'. Thiếu phần quan trọng nhất: chứng minh THAO TÁC ĐÃ KHÔNG XẢY RA. Một API trả 400 rồi vẫn ghi vào CSDL sẽ pass case này. ĐÃ SỬA: bổ sung bước đọc lại tài nguyên sau khi gọi.")
            ov["Expected_Assertions"] = a + "; VÀ đọc lại tài nguyên sau khi gọi để xác nhận dữ liệu KHÔNG bị thay đổi"
            return "INCOMPLETE", " | ".join(notes), ov
        if st < 300:
            notes.append("R8 - Case thành công nhưng chỉ kiểm 'khớp schema'. Thiếu khẳng định giá trị thật sự được lưu đúng. ĐÃ SỬA: bổ sung bước đọc lại tài nguyên và so khớp giá trị vừa gửi.")
            ov["Expected_Assertions"] = a + "; VA doc lai tai nguyen de xac nhan gia tri luu dung bang gia tri da gui"
            return "INCOMPLETE", " | ".join(notes), ov
        # Con lai: endpoint CHI DOC bi tu choi dau vao xau. "Tra 4xx + co truong error" da la
        # một phép kiểm trọn vẹn vì không có tác dụng phụ nào để mà kiểm. Không gắn INCOMPLETE.

    # --- Luật thiếu precondition cho case phụ thuộc biến động ---
    if "{{" in r["Request_Body"] and r["Preconditions"] in ("SUT da seed", "-", ""):
        notes.append("R10 - Case dùng biến Postman ({{...}}) nhưng precondition chỉ ghi 'SUT da seed', không nói biến đó được đặt ở đâu. Chạy độc lập sẽ thất bại. ĐÃ SỬA: ghi rõ bước _setup phải chạy trước.")
        ov["Preconditions"] = "Folder _setup đã chạy xong và đã đặt các biến môi trường cần thiết"
        return "INCOMPLETE", " | ".join(notes), ov

    return "VALID", ("Bước, dữ liệu và kỳ vọng đều đối chiếu được với SRS; assertion đã cụ thể; chạy độc lập được sau khi _setup chạy xong."), ov


def process(path_in, path_out):
    with open(path_in, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        cols = rd.fieldnames
        rows = list(rd)
    counter = Counter()
    for r in rows:
        label, note, ov = audit_row(r)
        r.update(ov)
        # Bộ sinh nhét mã SEC vào đầu Title ("[SEC-04] Xem don hang..."). Khi gán lại mã ở
        # cột SEC_Ref mà quên sửa Title thì báo cáo sẽ tự mâu thuẫn với chính nó.
        if r["Title"].startswith("[SEC-0") or r["Title"].startswith("[--]"):
            r["Title"] = re.sub(r"^\[(SEC-0\d|--)\] ", "[%s] " % r["SEC_Ref"], r["Title"])
        r["Audit_Label"] = label
        r["Audit_Note"] = note
        counter[label] += 1
    os.makedirs(os.path.dirname(os.path.abspath(path_out)), exist_ok=True)
    with open(path_out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    return counter, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src")
    ap.add_argument("--out", dest="dst")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    if a.report:
        grand = Counter()
        print("| API | Tong | VALID | INVALID | INCOMPLETE | %% VALID |")
        print("|---|---|---|---|---|---|")
        for n in (1, 2, 3):
            src = "testcases/API-%d_generated.csv" % n
            dst = "testcases/API-%d_audited.csv" % n
            c, _ = process(src, dst)
            t = sum(c.values())
            grand.update(c)
            print("| API-%d | %d | %d | %d | %d | %.0f%% |"
                  % (n, t, c["VALID"], c["INVALID"], c["INCOMPLETE"], 100.0 * c["VALID"] / t))
        t = sum(grand.values())
        print("| **Tong** | **%d** | **%d** | **%d** | **%d** | **%.0f%%** |"
              % (t, grand["VALID"], grand["INVALID"], grand["INCOMPLETE"], 100.0 * grand["VALID"] / t))
        return

    c, _ = process(a.src, a.dst)
    print("%s -> %s | %s" % (a.src, a.dst, dict(c)))


if __name__ == "__main__":
    main()
