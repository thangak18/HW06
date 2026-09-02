# Thư viện Prompt — dẫn AI theo từng bước

**HW06 · 23127195** · AI tool: **Claude Opus 5** (`claude-opus-5`) qua Claude Code

> **Nguyên tắc của đề bài (§2):** *"this does not mean issuing a single, generic prompt such as
> 'generate all the API test cases from the spec and run them'. Instead, you must guide the AI
> through **every step** of the technique as it was taught."*
>
> Sáu prompt dưới đây là sáu bước tách bạch của quy trình. Mỗi prompt có **ràng buộc âm**
> (nói rõ AI *không* được làm gì) — đây là phần quan trọng nhất, vì phần lớn lỗi của AI đến từ
> việc nó làm quá phạm vi được giao.

---

## ⚠ Ghi chú trung thực về cách các prompt này được sử dụng

Trong phiên làm việc ngày 2026-09-01, AI được chạy ở **chế độ agentic** (Claude Code có quyền
đọc/ghi file và chạy shell). Các prompt thực tế của sinh viên là những câu chỉ đạo **ở mức cao**
(ghi nguyên văn trong [`../interactions/SESSION-01_2026-09-01.md`](../interactions/SESSION-01_2026-09-01.md)),
còn việc phân rã thành sáu bước dưới đây do **AI tự thực hiện bên trong**.

Sáu prompt này vì vậy có hai vai trò:
1. **Tài liệu hoá** đúng sáu bước mà quy trình đã thực sự đi qua.
2. **Prompt chạy lại được** để sinh viên tự tay dẫn AI qua từng bước — đúng tinh thần §2 của đề.

Xem thêm mục *"Điều tôi sẽ làm khác lần sau"* trong [`../AI_CRITIQUE.md`](../AI_CRITIQUE.md).

---

## P1 — Trích xuất đặc tả (KHÔNG sinh test case)

```text
Bạn là kỹ sư kiểm thử. Nhiệm vụ ở bước này CHỈ là TRÍCH XUẤT, tuyệt đối chưa sinh test case.

Tài liệu đầu vào (đọc CẢ HAI):
  1. api_specification.md  — hợp đồng dữ liệu của API
  2. README.md (SRS)       — yêu cầu nghiệp vụ FR-01..FR-24 và bảo mật SEC-01..SEC-07

Endpoint cần trích xuất: <METHOD> <PATH>   (thuộc <FR-xx>)

Hãy trả về một JSON theo lược đồ EndpointModel:
  method, path, fr, can_xac_thuc, vai_tro_yeu_cau,
  tham_so[]        : {ten, vi_tri, kieu, bat_buoc, rang_buoc[]}
  may_trang_thai   : {cac_trang_thai, trang_thai_ket_thuc, chuyen_hop_le[]} hoặc null
  lươc_do_response : {thanh_cong, loi, truong_cam[]}
  sec_ap_dung[]

RÀNG BUỘC BẮT BUỘC:
- MỖI ràng buộc phải kèm trường "trich_dan" chứa NGUYÊN VĂN câu trong tài liệu.
  Ràng buộc không có trích dẫn là ràng buộc bịa — không được đưa vào.
- Nếu tài liệu KHÔNG nói gì về một điểm, ghi "KHÔNG ĐƯỢC ĐẶC TẢ". Tuyệt đối không suy đoán.
- KHÔNG gọi API, KHÔNG xem response thật. Bước này chỉ đọc tài liệu.
- KHÔNG sinh test case. Sinh test case là bước P2.

Cuối cùng, liệt kê riêng: những điểm mà api_specification.md im lặng nhưng SRS có nói,
và ngược lại.
```

**Vì sao ràng buộc "không xem response thật":** nếu AI thấy hành vi hiện tại, nó sẽ chép hành vi
đó thành "kỳ vọng", và mọi lỗi sẽ được hợp thức hoá. Đây là dạng thiên lệch nghiêm trọng nhất —
xem `AI_CRITIQUE.md`.

---

## P2 — Sinh phân vùng miền theo danh mục quy tắc

```text
Dựa trên EndpointModel ở bước P1, sinh test case cho kỹ thuật DOMAIN PARTITION.

KHÔNG được tự nghĩ ra test case theo cảm hứng. Với MỖI tham số, hãy áp ĐẦY ĐỦ danh mục sau,
không được bỏ mục nào (nếu một mục không áp dụng được, phải ghi rõ lý do):

  Mọi tham số      : thiếu trường · null · sai kiểu
  Kiểu chuỗi       : chuỗi rỗng · CHỈ KHOẢNG TRẮNG · Unicode tiếng Việt · khoảng trắng bao quanh
  Kiểu số          : 0 · số âm · vượt Number.MAX_SAFE_INTEGER · số thực · chuỗi-số
  Ràng buộc biên   : min−1 · min · min+1 · max−1 · max · max+1     ← BẮT BUỘC đủ 6 điểm
  Ràng buộc mẫu    : khớp · không khớp · khớp một phần · khác hoa/thường
  Khoá ngoại       : tồn tại · không tồn tại · 0 · âm

Lưu ý riêng:
- "chuỗi rỗng" và "chỉ khoảng trắng" là HAI phân vùng KHÁC NHAU. Chuỗi "   " là truthy trong
  JavaScript nên lọt qua phép kiểm tra `if (!x)`.
- Điểm "v == min" là điểm phân biệt cài đặt `>` với `>=`. Không bao giờ được bỏ.

Mỗi test case trả về đúng định dạng IR, trong đó trường expected_by_spec phải TRÍCH DẪN
điều khoản trong tài liệu làm căn cứ. Nếu không trích dẫn được, đánh dấu case đó là
"KHÔNG CÓ CĂN CỨ TRONG ĐẶC TẢ" để tôi xem lại.
```

---

## P3 — Sinh chuỗi chuyển trạng thái

```text
Dựa trên may_trang_thai trong EndpointModel, sinh test case cho kỹ thuật STATE TRANSITION.

Sinh ĐẦY ĐỦ bốn nhóm sau — nhóm (b), (c), (d) là những nhóm hay bị bỏ sót nhất:

  (a) MỌI cạnh hợp lệ trong máy trạng thái.
  (b) MỌI cặp (từ, đến) KHÔNG nằm trong máy trạng thái  → phải bị từ chối.
  (c) Cạnh TỰ LẶP: thực hiện lại hành động đã đưa hệ thống đến trạng thái hiện tại.
      Ví dụ: cấp lại OTP thì OTP cũ phải chết; import lại thì không được nhân đôi dữ liệu.
  (d) Rời khỏi trạng thái KẾT THÚC → phải bị từ chối.

Ngoài ra, nếu endpoint là PUT với nhiều trường:
  (e) CẬP NHẬT MỘT PHẦN: chỉ gửi một tập con các trường. Các trường không gửi PHẢI giữ nguyên
      giá trị cũ, không được bị ghi đè thành NULL.

QUY TẮC KIỂM CHỨNG BẮT BUỘC:
Không được coi message trả về là bằng chứng. "Password reset successfully" KHÔNG chứng minh
mật khẩu đã đổi. Mỗi test case chuyển trạng thái phải có một bước ĐỌC LẠI độc lập để xác nhận
trạng thái thật (đăng nhập lại, GET lại tài nguyên, đếm lại số bản ghi).
```

---

## P4 — Sinh test case bảo mật

```text
Dựa trên sec_ap_dung trong EndpointModel, sinh test case bảo mật.

Với mỗi mục SEC áp dụng được, sinh test theo bảng bề mặt tấn công:

  SEC-02 (yêu cầu JWT)    : không token · token rác · JWT ký bằng KHOÁ SAI · JWT alg=none
  SEC-03 (kiểm tra role)  : token hợp lệ nhưng role=user gọi API admin
  SEC-05 (parameterized)  : payload SQLi trên MỌI tham số kiểu chuỗi
  SEC-06 (không đổi role) : gửi kèm các trường đặc quyền KHÔNG có trong đặc tả:
                            role, id, is_admin, email
  SEC-01 (không plaintext): response không được chứa password, reset_token, login_attempts
  IDOR                    : mọi tham số tên khớp /(^|_)(id|user_id|owner)$/

HAI YÊU CẦU ĐẶC BIỆT:

1. Với SEC-06: các trường cần thử là những trường KHÔNG có trong danh sách tham số của tài liệu.
   Sinh test chỉ theo tài liệu sẽ không bao giờ chạm tới chúng — đó chính là lý do lỗi loại này
   hay lọt lưới.

2. Với mọi lỗi phân quyền: KHÔNG được dừng ở "API có trả 403 không". Phải sinh thêm một test
   CHUỖI TÁC ĐỘNG chứng minh hậu quả quan sát được từ bên ngoài. Ví dụ: sau khi user thường
   ghi được dữ liệu, dữ liệu đó có hiện công khai cho mọi người không?
```

---

## P5 — Sinh test case kiểm tra lược đồ

```text
Dựa trên lươc_do_response trong EndpointModel, sinh test case SCHEMA VALIDATION.

Sinh theo CẢ HAI chiều:

  Chiều thuận  : response có ĐỦ các trường theo hợp đồng · kiểu dữ liệu từng trường đúng ·
                 Content-Type là application/json · response lỗi cũng khớp lược đồ
  Chiều nghịch : response KHÔNG có trường nào NGOÀI hợp đồng (additionalProperties = false) ·
                 không chứa bất kỳ trường nào trong danh sách truong_cam

CHIỀU NGHỊCH LÀ BẮT BUỘC. Kiểm tra lược đồ chỉ theo chiều thuận sẽ không bao giờ phát hiện
một câu `SELECT *` vô tình làm rò rỉ cột nhạy cảm — đó là loại lỗi mà chiều nghịch sinh ra
để bắt.

Với các trường mang giá trị tiền: kiểm tra tường minh rằng kiểu là number chứ không phải string.
Trường tiền trả về dạng chuỗi khiến client nối chuỗi thay vì cộng số.
```

---

## P6 — Tự phê bình bộ test case vừa sinh

```text
Bây giờ hãy phê bình chính bộ test case bạn vừa sinh. Không bào chữa, không tóm tắt lại.

Trả lời từng câu:

1. Test case nào có kỳ vọng lấy từ HÀNH VI của hệ thống thay vì từ ĐẶC TẢ? Liệt kê cụ thể.
2. Test case nào ràng buộc một hành vi mà đặc tả THỰC SỰ KHÔNG quy định? (kỳ vọng quá chặt)
3. Test case nào bị phân loại sai kỹ thuật?
4. Với sáu câu hỏi sau, bộ test của bạn có case nào trả lời được không? Nếu không, vì sao bỏ sót?
     a. Nếu client chỉ gửi MỘT PHẦN dữ liệu thì sao?
     b. VỊ TRÍ của phần tử lỗi trong mảng có làm đổi kết luận không?
     c. Báo cáo trả về có NHẤT QUÁN với trạng thái thật của CSDL không?
     d. Có BẤT BIẾN nghiệp vụ nào bắt được mọi cách tính sai không?
     e. Hậu quả nghiệp vụ THẬT SỰ của lỗi này là gì?
     f. Ngữ nghĩa của NGÔN NGỮ CÀI ĐẶT có tạo khe hở nào không?
5. Có assertion bất đồng bộ nào gọi pm.sendRequest mà không bọc try/catch + done(e) không?
   (Nếu có: khi assertion FAIL, done() không bao giờ chạy và Newman sẽ ÂM THẦM bỏ qua test đó.)

Với mỗi vấn đề, nêu mã test case và cách sửa cụ thể.
```

---

## Ghi chú về hiệu quả của từng prompt

| Prompt | Nhận xét sau khi dùng thật |
|---|---|
| P1 | Ràng buộc "phải trích dẫn nguyên văn" hiệu quả rõ rệt: nó buộc AI phát hiện ra SEC-01…SEC-07 **không** nằm trong `api_specification.md` — một phát hiện định hình toàn bộ phần còn lại. |
| P2 | Danh mục quy tắc là thứ tạo ra khác biệt lớn nhất. Nếu chỉ hỏi "sinh test phân vùng", AI bỏ qua điểm `v == min` — đúng điểm tìm ra BUG-A2-03. |
| P3 | Nhóm (c) *cạnh tự lặp* và nhóm (e) *cập nhật một phần* vẫn bị bỏ sót ngay cả khi đã nêu tường minh trong prompt. Đây là giới hạn thật, không phải lỗi diễn đạt. |
| P4 | Yêu cầu "chuỗi tác động" là prompt hiệu quả nhất trong cả sáu: nó biến một ghi nhận kỹ thuật thành bằng chứng chiếm quyền hệ thống. |
| P5 | Yêu cầu chiều nghịch bắt trúng BUG-A1-02 ngay lần đầu. |
| P6 | Prompt tự phê bình chỉ ra được lỗi *phân loại* nhưng **không** tự phát hiện được lỗi assertion bất đồng bộ — lỗi đó chỉ lộ ra khi con người đối chiếu báo cáo Newman với kết quả `curl` thủ công. |
