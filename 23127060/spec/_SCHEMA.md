# `spec/api-*.json` — Dinh dang spec may doc duoc (dau vao cua bo sinh test)

> HW06 — SV 23127060. File nay mo ta **hop dong du lieu** giua con nguoi va bo sinh test
> `agent-skill/eshop-api-23127060/scripts/gen_testcases.py`.
>
> Y tuong cot loi cua muc 7 de bai: *"given the API specification, it produces test cases
> automatically"*. Dac ta van xuoi (`eshop-sut/README.md`) khong the dua thang cho may;
> phai dich no sang mot cau truc co **truc phan hoach ro rang**. Do chinh la file nay.

---

## 1. Cau truc tong the

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

Bon khoa `endpoints` / `state_machine` / `security` / `schema_cases` anh xa **mot doi mot**
sang bon nhom ky thuat ma de bai muc 6.1 doi hoi: domain partition, state transition,
security SEC-01..07, schema validation. Do la ly do bo sinh chay duoc 4 vong prompt rieng
(`--only DOM`, `--only STA`, ...) thay vi mot prompt tong.

## 2. `endpoints[]` — nguon cua nhom DOM

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

`valid_body` la **body neo**: khi sinh case cho tham so `price`, bo sinh giu nguyen moi
truong khac cua `valid_body` va chi thay `price`. Nho vay moi case chi thay doi **dung mot
bien** — dieu kien bat buoc de ket qua test quy duoc trach nhiem ve dung tham so do.

### 2.1 `params[].partitions[]` — mot lop tuong duong

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

**Quy tac suy dien khi thieu truong:**

| Truong thieu | Gia tri suy ra |
|---|---|
| `expected_status` | `endpoint.success_status` neu `valid=true`, nguoc lai `400` |
| `assertions` | "body la JSON; khop schema thanh cong" / "body la JSON; co truong error" |
| `technique` | `BVA` neu `boundary=true`, nguoc lai `EP` |
| `priority` | `P1` neu `valid=true`, nguoc lai `P2` |
| `oracle` | `SPEC` |
| `tag` | `@bug` neu co `bug`, nguoc lai `@contract` |

`in` nhan 3 gia tri: `body` (mac dinh), `query` (noi vao query string), `path`
(thay `:ten` trong duong dan).

## 3. `state_machine` — nguon cua nhom STA

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

Bo sinh phu **0-switch coverage**: moi phan tu `transitions[]` la mot o trong bang
`states x states`. Ham `coverage()` in ra ty le `so o da test / |states|^2` de biet con
thieu o nao. `allowed` la ky vong theo **SRS**, khong phai theo code — nho vay cac o ma
impl lam sai (B-09, B-10) van duoc sinh ra voi ky vong dung va se FAIL co chu dich.

## 4. `security[]` — nguon cua nhom SEC

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

Neu thieu `assertions`, bo sinh dien assertion mac dinh theo `sec` tu bang
`SEC_DEFAULT_ASSERT` trong `gen_testcases.py`. **Bang do bam theo `eshop-sut/README.md`
muc 9 (ban that), khong phai bang SEC suy dien theo OWASP** — xem `report/00_environment.md`
muc 4 de biet vi sao dieu nay tung sai.

Ham `coverage()` canh bao neu chua du 7 ma SEC-01..SEC-07.

## 5. `schema_cases[]` — nguon cua nhom SCH

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

`schema_ref` duoc `build_collection.py` dich thanh mot loi goi
`pm.response.to.have.jsonSchema(schemas["product"])` trong tests script.

## 6. Rang buoc bat buoc khi sua file spec

1. **`sec` phai nam trong SEC-01..SEC-07 that.** Dat sai ma la loi nghiem trong: no lam
   sai toan bo bang do phu bao mat trong bao cao.
2. **`expected_status` luon viet theo SRS**, khong bao gio viet theo hanh vi thuc te. Case
   nao phoi bay bug thi dat them `bug` — bo sinh se tu gan tag `@bug`, va nguoi doc bao cao
   hieu ngay day la "expected failure".
3. **Khong hardcode host.** Luon dung `{{baseUrl}}` va cac bien Postman khac.
4. **Chi dung du lieu co that trong `database.js`.** Vi du: chi co 4 ma giam gia
   `SAVE10` / `BIGBUY` / `VIP100` / `EXPIRED`; khong co ma nao `is_active = 0`.
   Dat mot gia tri khong ton tai lam cho test that bai vi ly do sai.
5. **Kiem tra lai sau moi lan sua:**

```bash
python3 -c "import json,glob;[json.load(open(f,encoding='utf-8')) for f in glob.glob('spec/api-*.json')];print('spec OK')"
python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py --spec spec/api-2.json --stats
```
