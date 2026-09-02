# TESTCASE_TAXONOMY — Công thức đảm bảo >= 35 test case / API

Đề bài cấm "1 prompt tổng". Vì vậy STEP 2 phải chạy **4 vòng prompt riêng biệt**,
mỗi vòng 1 nhóm kỹ thuật, mỗi vòng ghi 1 entry AI_log riêng.

---

## Cấu trúc bắt buộc của 1 test case (cột trong CSV)

| Cột | Ý nghĩa |
|---|---|
| `TC_ID` | `TC-<API>-<CAT>-<nnn>` vd `TC-A1-SEC-007` |
| `API` | `API-1` / `API-2` / `API-3` |
| `FR` | `FR-03` / `FR-08` / `FR-15` |
| `Category` | `DOM` / `STA` / `SEC` / `SCH` |
| `Technique` | EP, BVA, Decision Table, State Transition, Pairwise, Error Guessing, Fuzzing, Schema |
| `Title` | 1 câu, bắt đầu bằng động từ |
| `Method` | GET/POST/PUT/DELETE |
| `Endpoint` | đường dẫn |
| `Preconditions` | trạng thái DB / token cần có |
| `Request_Body` | JSON 1 dòng (hoặc `-`) |
| `Request_Headers` | ngoài `X-Student-Id` và `Content-Type` |
| `Expected_Status` | mã HTTP mong đợi |
| `Expected_Assertions` | điều kiện trên body, ngăn cách `;` |
| `Oracle` | `SPEC` hoặc `IMPL` |
| `SEC_Ref` | SEC-01..07 hoặc `-` |
| `Priority` | P0/P1/P2 |
| `Source` | `AI` hoặc `HUMAN` |
| `Audit_Label` | `VALID` / `INVALID` / `INCOMPLETE` |
| `Audit_Note` | lý do gắn nhãn + đã sửa gì |
| `Tag` | `@contract` hoặc `@bug` |
| `Bug_Ref` | mã bug liên quan (A-01, B-05, C-02...) hoặc `-` |

---

## Vòng 1 — DOMAIN PARTITION (`DOM`), mục tiêu >= 14 case/API

Với **mỗi tham số** của API, sinh đầy đủ:

1. **Equivalence Partitioning**: 1 case hợp lệ + mỗi lớp không hợp lệ 1 case.
2. **Boundary Value Analysis**: với tham số có biên (độ dài chuỗi, giá trị số) lấy
   `min-1, min, min+1, max-1, max, max+1`.
3. **Missing / null / wrong type**: thiếu key, `null`, sai kiểu (số <-> chuỗi), array/object thay vì scalar.
4. **Decision table** khi có >= 2 tham số tương tác (vd `apply-coupon`:
   `code hợp lệ?` x `total >= min?` x `còn hạn?` x `chưa vượt hạn mức?` = 16 tổ hợp, chọn 8-10 tổ hợp đại diện).

Công thức nhanh: `số tham số x 4 lớp tối thiểu + số biên x 3`.

**Ví dụ API-3 `POST /api/products`:** 5 tham số x 4 = 20 case DOM ngay từ đầu.

---

## Vòng 2 — STATE TRANSITION (`STA`), mục tiêu >= 8 case/API

Dùng kỹ thuật **State Transition Testing (0-switch coverage đầy đủ)**.

- **API-2 (FR-10 order state machine):** bảng 5x5 = 25 ô. Test toàn bộ 25 ô là lý tưởng;
  tối thiểu: 4 chuyển hợp lệ + 10 chuyển không hợp lệ + 2 chuyển "bug cố ý"
  (`shipping -> canceled` qua `/cancel`, `canceled -> delivered` qua admin).
- **API-1 (FR-03 là state machine 2 bước):** trạng thái token =
  `NONE -> ISSUED -> USED`. Test: reset khi chưa có token; reset 2 lần với cùng token;
  xin token 2 lần rồi dùng token cũ; dùng token của user khác; reset rồi login bằng mật khẩu cũ;
  reset khi tài khoản đang bị khóa.
- **API-3 (vòng đời sản phẩm):** `NOT_EXIST -> CREATED -> UPDATED -> DELETED -> NOT_EXIST`.
  Test: GET sau DELETE; PUT sau DELETE; DELETE 2 lần; POST trùng tên; GET id vừa tạo.

---

## Vòng 3 — SECURITY (`SEC`), mục tiêu >= 9 case/API

> **ĐÃ SỬA sau STEP 3.** Bản trước của mục này ghi: *"Bắt buộc phủ đủ 7 mã SEC-01..SEC-07 cho
> **mọi** API"*, và dùng một bảng SEC **suy diễn theo OWASP**. Cả hai đều sai, và chúng gây hại
> thật: yêu cầu "đủ 7 mã cho mọi API" là bất khả thi (SEC-07 nói về OTP thì không thể áp vào
> API quản lý sản phẩm), nên cách duy nhất để "đạt chỉ tiêu" là gán bừa. Kết quả ở STEP 3:
> **39/41 case SEC bị gán sai mã**. Xem `report/03_audit.md` mục 4.

### Bảng SEC-01..SEC-07 (nguồn duy nhất: `eshop-sut/README.md` mục 9)

| Mã | Yêu cầu | Kiểm thế nào ở tầng API |
|---|---|---|
| SEC-01 | Mật khẩu **không** được lưu plaintext | Đọc response của `login` / `users/me`: nếu thấy `password` đúng nguyên văn mật khẩu đã gửi thì đã chứng minh vi phạm |
| SEC-02 | API có tính bảo mật phải yêu cầu JWT hợp lệ | Gọi không `Authorization`; `Bearer ` rỗng; token sai chữ ký; token của user khác. Kỳ vọng 401/403 |
| SEC-03 | API Admin phải kiểm `role='admin'`, **không chỉ** kiểm token tồn tại | Dùng token của user thường (hợp lệ) gọi endpoint admin. Kỳ vọng 403 |
| SEC-04 | Dữ liệu user nhập phải được escape khi hiển thị | Gửi `<script>`, `<img src=x onerror=>`, `javascript:` rồi đọc lại xem server có lưu thô không |
| SEC-05 | Truy vấn CSDL phải dùng Parameterized Query | `%' OR '1'='1`, `' UNION SELECT ...`, `'; DROP TABLE ...--`, và một dấu nháy đơn đơn lẻ |
| SEC-06 | API cập nhật hồ sơ **không được** cho đổi trường `role` từ client | `PUT /api/users/me` kèm `{"role":"admin"}` rồi đọc lại role |
| SEC-07 | OTP reset phải >= 6 chữ số, có thời hạn, vô hiệu hóa sau khi dùng | Độ dài token; dùng lại token đã dùng; dùng token của email khác; token cũ sau khi xin token mới |

### Chỉ tiêu độ phủ — đặt lại cho đúng

- **Toàn bộ suite phải phủ đủ 7 mã SEC-01..SEC-07.** Đây mới là yêu cầu của đề bài.
- **Từng API chỉ phủ những mã thực sự áp dụng được**, và phần không áp dụng **phải có giải
  trình một dòng** trong báo cáo. Ví dụ: API-3 (quản lý sản phẩm) không dùng tới lưu trữ mật
  khẩu lẫn OTP, nên không có case SEC-01 và SEC-07 — đó là đúng, không phải thiếu sót.
- Ngưỡng số lượng vẫn là **>= 9 case SEC/API**, nhưng đếm theo **số phép thử bảo mật**, không
  phải theo số mã SEC khác nhau.

**Quy tắc chống tái phạm:** trước khi gắn một mã SEC, phải trả lời được câu
*"điều này vi phạm câu nào trong `README.md` mục 9?"*. Nếu không trả lời được thì **để
`SEC_Ref = '-'`**, không được gắn mã gần đúng nhất. Một số vector tấn công thật sự **không**
được SEC-01..07 phủ (user enumeration, path traversal, mass assignment trường khác `role`,
thiếu rate limiting) — chúng vẫn là test hợp lệ, chỉ là không có mã SEC để gắn.

**Quy tắc về kỳ vọng:** `Expected_Status` phải truy ngược được về một câu trong SRS. Kỳ vọng
`429` (rate limiting) và `409` (conflict) **không có căn cứ trong SRS này** — đừng đặt chúng
trừ khi trích được dòng cụ thể.

## Vòng 4 — SCHEMA VALIDATION (`SCH`), mục tiêu >= 5 case/API

Dùng `pm.response.to.have.jsonSchema(schema)` (Postman hỗ trợ AJV sẵn).

Mỗi API cần ít nhất:
1. Schema của response thành công (200) — đúng tên trường, đúng kiểu, không thừa trường.
2. Schema của từng response lỗi (400 / 401 / 403 / 404 / 500) — phải là
   `{ "error": string }`.
3. `Content-Type` phải là `application/json` (bắt bug **C-03** trả HTML).
4. Kiểu dữ liệu ổn định giữa các lần gọi (bắt bug **C-05** `price` khi string khi number).
5. Không lộ trường nhạy cảm (`password`, `reset_token`) — giao với SEC-02.

Schema JSON lưu tại `postman/scripts/schemas/<API>.json`, nạp vào collection variable.

---

## Bảng kiểm số lượng (điền trước khi qua STEP 3)

| API | DOM | STA | SEC | SCH | AI tổng | HUMAN thêm | Tổng |
|---|---|---|---|---|---|---|---|
| API-1 FR-03 | >=14 | >=8 | >=9 | >=5 | **>=36** | >=5 | >=41 |
| API-2 FR-08 | >=14 | >=8 | >=9 | >=5 | **>=36** | >=5 | >=41 |
| API-3 FR-15 | >=16 | >=6 | >=9 | >=5 | **>=36** | >=5 | >=41 |

Nếu chưa đủ: **không được chế thêm case rác**. Quay lại vòng tương ứng, tăng độ sâu
(thêm biên, thêm tổ hợp decision table, thêm payload SEC) và ghi rõ trong AI_log
là đã phải prompt lại vòng nào.

---

## Hướng dẫn gắn nhãn AUDIT (STEP 3)

| Nhãn | Khi nào dùng |
|---|---|
| **VALID** | Bước, dữ liệu, kỳ vọng đều đúng so với spec; chạy được ngay. |
| **INVALID** | Kỳ vọng sai (vd đòi 400 nhưng spec nói 404), endpoint sai, precondition bất khả thi, hoặc trùng lặp với case khác. **Phải sửa rồi ghi cái gì đã sửa.** |
| **INCOMPLETE** | Ý tưởng đúng nhưng thiếu: thiếu assertion trên body, thiếu precondition, thiếu dữ liệu cụ thể, không kiểm tra tác dụng phụ (vd đổi mật khẩu xong không thử login lại). **Phải bổ sung.** |

Mỗi nhãn phải có `Audit_Note` >= 1 câu lý do. Tỷ lệ kỳ vọng hợp lý:
khoảng 55-70% VALID, 10-20% INVALID, 20-30% INCOMPLETE. Nếu AI ra 100% VALID
=> gần như chắc chắn là audit hời hợt, phải rà soát lại.

---

## Hướng dẫn EXTEND (STEP 4) — >= 5 case/API AI thường bỏ sót

Danh sách gợi ý (chọn >=5, phải giải thích **tại sao AI bỏ sót**):

**API-1:**
- Brute force 4 chữ số token bằng Collection Runner + data file 20 giá trị (SEC-07).
- Dùng token của user A để đổi mật khẩu user B (IDOR trên luồng reset).
- Reset mật khẩu khi tài khoản đang `locked_until` -> kiểm tra có mở khóa không (A-06).
- Race condition: gọi `forgot-password` 2 lần song song, token đầu còn dùng không.
- Kiểm tra `login` sau reset không còn trả `password` trong body (A-07).

**API-2:**
- Checkout với `total_amount` âm rồi kiểm tra `GET /api/orders/:id` (B-01).
- Áp coupon với `total_amount` **bằng đúng** `min_order_amount` (lỗi biên `>` — B-06).
- Bỏ `user_id` khỏi `apply-coupon` để vượt hạn mức sử dụng (B-07).
- User B gọi `PUT /api/admin/orders/<order của A>/status` (B-03, role escalation).
- Chuỗi `pending -> confirmed -> shipping -> canceled` phải bị chặn (B-09).
- `canceled -> delivered` phải bị chặn (B-10).

**API-3:**
- `DELETE /api/products/1` **không token** (C-01) — AI hay giả định endpoint admin thì đã có auth.
- `GET /api/products?search=%25' UNION SELECT ...` đọc bảng `users` (C-02).
- Kiểm tra `Content-Type` khi SQL lỗi (C-03) — AI hiếm khi test content-type.
- So sánh kiểu `price` giữa id chẵn và id lẻ (C-05) — cần 2 request mới lộ ra.
- `PUT` thiếu trường `description` -> kiểm tra có bị ghi `null` không (C-09).

**Lý do AI bỏ sót — chọn 1 trong 4 khi viết báo cáo:**
1. *Prompt quality*: prompt không yêu cầu rõ "test cả trường hợp endpoint thiếu auth".
2. *Model limitation*: AI suy diễn từ tên endpoint (`/api/admin/...`) chứ không đọc code, nên giả định đã có phân quyền.
3. *API characteristic*: bug chỉ lộ ra khi **kết hợp 2 request** (vd so kiểu `price` id chẵn/lẻ), AI sinh từng case độc lập.
4. *Spec gap*: spec không mô tả hành vi này nên AI không có gì để bám vào.
