# `spec/api-*.json` — Định dạng spec máy đọc được (đầu vào của bộ sinh test)

> HW06 — SV 23127060. File này mô tả **hợp đồng dữ liệu** giữa con người và bộ sinh test
> `agent-skill/eshop-api-23127060/scripts/gen_testcases.py`.
>
> Ý tưởng cốt lõi của mục 7 đề bài: *"given the API specification, it produces test cases
> automatically"*. Đặc tả văn xuôi (`eshop-sut/README.md`) không thể đưa thẳng cho máy;
> phải dịch nó sang một cấu trúc có **trục phân hoạch rõ ràng**. Đó chính là file này.

---

## 1. Cấu trúc tổng thể

```jsonc
{
  "api_id":     "API-3",          // ma API trong bai
  "tc_prefix":  "C3",             // tien to ma test case: TC-C3-DOM-001
  "pool":       "C",              // Pool A / B / C theo de bai
  "fr":         "FR-15",          // ma yeu cau chuc nang trong SRS
  "name":       "Quan ly san pham (CRUD + tim kiem)",
  "base_url":   "{{baseUrl}}",    // bien Postman, khong hardcode host

  "endpoints":     [ /* muc 2 */ ],   // -> sinh nhom DOM
  "state_machine": { /* muc 3 */ },   // -> sinh nhom STA
  "security":      [ /* muc 4 */ ],   // -> sinh nhom SEC
  "schema_cases":  [ /* muc 5 */ ]    // -> sinh nhom SCH
}
```

Bốn khóa `endpoints` / `state_machine` / `security` / `schema_cases` ánh xạ **một đối một**
sang bốn nhóm kỹ thuật mà đề bài mục 6.1 đòi hỏi: domain partition, state transition,
security SEC-01..07, schema validation. Đó là lý do bộ sinh chạy được 4 vòng prompt riêng
(`--only DOM`, `--only STA`, ...) thay vì một prompt tổng.

## 2. `endpoints[]` — nguồn của nhóm DOM

```jsonc
{
  "key":            "create",              // ten ngan de tham chieu
  "method":         "POST",
  "path":           "/api/products",
  "auth_required":  true,                  // theo SRS, khong phai theo impl
  "success_status": 201,                   // theo SRS
  "preconditions":  "Da login bang tai khoan admin, co {{token_admin}}",
  "headers":        "Authorization: Bearer {{token_admin}}",
  "valid_body":     { "name": "...", "price": 150000, "category_id": 1 },
  "params": [ /* muc 2.1 */ ]
}
```

`valid_body` là **body neo**: khi sinh case cho tham số `price`, bộ sinh giữ nguyên mọi
trường khác của `valid_body` và chỉ thay `price`. Nhờ vậy mỗi case chỉ thay đổi **đúng một
biến** — điều kiện bắt buộc để kết quả test quy được trách nhiệm về đúng tham số đó.

### 2.1 `params[].partitions[]` — một lớp tương đương

```jsonc
{
  "id":              "negative",        // dinh danh lop, duy nhat trong pham vi tham so
  "value":           -100,              // gia tri dai dien cua lop
  "omit":            false,             // true = bo han key khoi body (khac han null)
  "valid":           false,             // lop hop le hay khong
  "boundary":        true,              // true => Technique mac dinh la BVA thay vi EP
  "technique":       "Decision Table",  // ghi de Technique neu can
  "desc":            "gia am - SRS FR-15 doi gia > 0",
  "expected_status": 400,               // theo SPEC; thieu thi suy ra tu valid + success_status
  "assertions":      "body co truong error; san pham KHONG duoc tao",
  "oracle":          "SPEC",            // SPEC (mac dinh) hoac IMPL
  "sec":             "SEC-05",          // gan them ma SEC neu lop nay cham bao mat
  "priority":        "P0",
  "bug":             "C-06",            // co gia tri => case duoc gan tag @bug
  "tag":             "@contract"        // ghi de tag neu can
}
```

**Quy tắc suy diễn khi thiếu trường:**

| Trường thiếu | Giá trị suy ra |
|---|---|
| `expected_status` | `endpoint.success_status` nếu `valid=true`, ngược lại `400` |
| `assertions` | "body là JSON; khớp schema thành công" / "body là JSON; có trường error" |
| `technique` | `BVA` nếu `boundary=true`, ngược lại `EP` |
| `priority` | `P1` nếu `valid=true`, ngược lại `P2` |
| `oracle` | `SPEC` |
| `tag` | `@bug` nếu có `bug`, ngược lại `@contract` |

`in` nhận 3 giá trị: `body` (mặc định), `query` (nối vào query string), `path`
(thay `:tên` trong đường dẫn).

## 3. `state_machine` — nguồn của nhóm STA

```jsonc
{
  "states":   ["pending", "confirmed", "shipping", "delivered", "canceled"],
  "endpoint": "/api/admin/orders/{{orderId}}/status",   // endpoint mac dinh
  "transitions": [
    {
      "from": "shipping", "to": "canceled",
      "allowed": false,                                  // theo SRS FR-10
      "method": "PUT",
      "endpoint": "/api/orders/{{orderId}}/cancel",      // ghi de endpoint mac dinh
      "body": {},
      "headers": "Authorization: Bearer {{token_user}}",
      "preconditions": "Don da duoc admin chuyen sang shipping",
      "expected_status": 400,
      "assertions": "trang thai KHONG doi, van la shipping",
      "bug": "B-09"
    }
  ]
}
```

Bộ sinh phủ **0-switch coverage**: mỗi phần tử `transitions[]` là một ô trong bảng
`states x states`. Hàm `coverage()` in ra tỷ lệ `số ô đã test / |states|^2` để biết còn
thiếu ô nào. `allowed` là kỳ vọng theo **SRS**, không phải theo code — nhờ vậy các ô mà
impl làm sai (B-09, B-10) vẫn được sinh ra với kỳ vọng đúng và sẽ FAIL có chủ đích.

## 4. `security[]` — nguồn của nhóm SEC

```jsonc
{
  "sec":       "SEC-05",                       // BAT BUOC, phai thuoc SEC-01..SEC-07
  "technique": "SQL Injection",
  "title":     "UNION SELECT doc bang users qua ?search",
  "method":    "GET",
  "endpoint":  "/api/products?search=<payload da url-encode>",
  "headers":   "-",
  "body":      null,
  "preconditions": "SUT da seed",
  "expected_status": 200,
  "assertions": "chi tra ve san pham khop tu khoa; khong tra ve email/password",
  "bug": "C-02"
}
```

Nếu thiếu `assertions`, bộ sinh điền assertion mặc định theo `sec` từ bảng
`SEC_DEFAULT_ASSERT` trong `gen_testcases.py`. **Bảng đó bám theo `eshop-sut/README.md`
mục 9 (bản thật), không phải bảng SEC suy diễn theo OWASP** — xem `report/00_environment.md`
mục 4 để biết vì sao điều này từng sai.

Hàm `coverage()` cảnh báo nếu chưa đủ 7 mã SEC-01..SEC-07.

## 5. `schema_cases[]` — nguồn của nhóm SCH

```jsonc
{
  "title":      "price luon la number ke ca voi id chan",
  "method":     "GET",
  "endpoint":   "/api/products/2",
  "headers":    "-",
  "body":       null,
  "expected_status": 200,
  "schema_ref": "product",          // tro toi postman/scripts/schemas/<API>.json
  "assertions": "typeof price === 'number'",
  "bug":        "C-05"
}
```

`schema_ref` được `build_collection.py` dịch thành một lời gọi
`pm.response.to.have.jsonSchema(schemas["product"])` trong tests script.

## 6. Ràng buộc bắt buộc khi sửa file spec

1. **`sec` phải nằm trong SEC-01..SEC-07 thật.** Đặt sai mã là lỗi nghiêm trọng: nó làm
   sai toàn bộ bảng độ phủ bảo mật trong báo cáo.
2. **`expected_status` luôn viết theo SRS**, không bao giờ viết theo hành vi thực tế. Case
   nào phơi bày bug thì đặt thêm `bug` — bộ sinh sẽ tự gắn tag `@bug`, và người đọc báo cáo
   hiểu ngay đây là "expected failure".
3. **Không hardcode host.** Luôn dùng `{{baseUrl}}` và các biến Postman khác.
4. **Chỉ dùng dữ liệu có thật trong `database.js`.** Ví dụ: chỉ có 4 mã giảm giá
   `SAVE10` / `BIGBUY` / `VIP100` / `EXPIRED`; không có mã nào `is_active = 0`.
   Đặt một giá trị không tồn tại làm cho test thất bại vì lý do sai.
5. **Kiểm tra lại sau mỗi lần sửa:**

```bash
python3 -c "import json,glob;[json.load(open(f,encoding='utf-8')) for f in glob.glob('spec/api-*.json')];print('spec OK')"
python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py --spec spec/api-2.json --stats
```
