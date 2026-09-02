# API_SPEC_NOTES — Ban do endpoint, tham so, va bug da biet (HW06, SV 23127060)

> Nguon: doc truc tiep `eshop-sut/backend/server.js` (Express + sqlite3) va
> `eshop-sut/api_specification.md`.
> **Agent PHAI doi chieu lai voi `api_specification.md` that trong repo o STEP 0.**
> Neu spec khac file nay => bao CRITICAL [C3].

---

## 0. Thong tin chung

- Base URL: `http://localhost:3000`
- Auth: JWT Bearer. `Authorization: Bearer <token>`. Secret hardcode trong source:
  `super_secret_key_that_should_not_be_here` (day la bug SEC).
- Middleware `authenticateToken`: thieu token -> `401 {error:"Unauthorized"}`,
  token sai -> `403 {error:"Forbidden"}`. **Khong he kiem tra `role` o bat ky dau.**
- Header bat buoc cua de bai: `X-Student-Id: 23127060` (SUT khong dung, nhung TA cham).
- DB: SQLite. `database.js` goi `initDatabase()` ngay khi `require` =>
  **moi lan restart backend la DROP + reseed toan bo DB**. Ghi nho khi thiet ke
  precondition va khi chay CI.

### Bang du lieu goc sau khi seed
- `users`: 2 user seed (1 admin, 1 user thuong). Cot: `id, name, email, password (PLAINTEXT),
  role, phone, shipping_address, login_attempts, locked_until, reset_token`.
- `products`: 5 san pham. Cot: `id, name, price, description, imageUrl, category_id`.
- `categories`, `orders` (`id,user_id,total_amount,status,shipping_address`),
  `coupons` (`id,code,type,discount_value,min_order_amount,max_uses_per_user,expired_at,is_active`),
  `coupon_usage` (`id,coupon_id,user_id`).
- Order status hop le (FR-10): `pending -> confirmed -> shipping -> delivered`,
  huy: `pending|confirmed -> canceled`.

### Mapping SEC-01..SEC-07 (DA XAC NHAN o STEP 0 — nguon: `eshop-sut/README.md` muc 9)

> **[C3] DA SUA:** ban truoc cua file nay ghi mot bang SEC **tu suy dien** (SQLi=SEC-01,
> IDOR=SEC-04...). Doi chieu voi `eshop-sut/README.md` muc 9 "Yeu cau Bao mat" cho thay
> bang do **sai hoan toan**. Duoi day la bang THAT, la oracle duy nhat duoc dung.

| Ma | Yeu cau (nguyen van rut gon) | Ap dung cho API |
|---|---|---|
| SEC-01 | Mat khau **khong** duoc luu plaintext | API-1 |
| SEC-02 | Cac API co tinh bao mat phai yeu cau JWT Token hop le | API-2, API-3 |
| SEC-03 | API Admin phai kiem tra `role='admin'` trong token, khong chi kiem tra token ton tai | API-2, API-3 |
| SEC-04 | Du lieu user nhap phai duoc escape khi hien thi (khong `innerHTML`) — stored XSS | API-3 |
| SEC-05 | Truy van CSDL phai dung Parameterized Query, khong noi chuoi | API-3 |
| SEC-06 | API cap nhat ho so **khong duoc** cho doi truong `role` tu client | API-2, API-3 (chuoi leo thang quyen) |
| SEC-07 | OTP dat lai mat khau phai du entropy (**toi thieu 6 chu so**), **co thoi han**, **vo hieu hoa sau khi dung** | API-1 |

**Luu y quan trong ve pham vi:** SEC-04 noi ve tang hien thi (UI). O tang API ta chi kiem
duoc **ve nua**: server co luu nguyen payload `<script>` khong (stored XSS source). Ghi ro
gioi han nay trong bao cao, khong duoc noi "da test day du SEC-04 tren API".

### Oracle: 2 tai lieu, khong phai 1

| Tai lieu | Vai tro |
|---|---|
| `eshop-sut/README.md` | **SRS — nghiep vu DUNG** (FR-01..FR-24, SEC-01..07). Day la oracle `SPEC`. |
| `eshop-sut/api_specification.md` | Chi la huong dan goi API (endpoint + body mau), **khong** phai oracle nghiep vu. |
| `eshop-sut/backend/server.js` | Hanh vi thuc te. Day la oracle `IMPL`. |

Khi `api_specification.md` va `README.md` khac nhau => **lay `README.md` lam chuan**,
vi no la tai lieu duy nhat tu tuyen bo "Mo ta yeu cau nghiep vu **dung** cua he thong".

---

## 1. API-1 — Pool A / FR-03: Quen mat khau & Dat lai mat khau

### 1.1 `POST /api/forgot-password`
**Auth:** khong. **Body:** `{ email }`

| Truong | Kieu | Rang buoc theo spec | Phan hoach mien |
|---|---|---|---|
| `email` | string | bat buoc, dung dinh dang email, phai ton tai | hop le / sai dinh dang / rong / null / thieu key / khong ton tai / SQLi / >254 ky tu / unicode / co khoang trang dau-cuoi / hoa-thuong |

**Response impl:**
- 200 `{ message: "Ma dat lai mat khau da duoc tao", resetToken: "<4 chu so>" }`
- 404 `{ error: "User not found" }`
- 500 `{ error }`

### 1.2 `POST /api/reset-password`
**Auth:** khong. **Body:** `{ email, resetToken, newPassword }`

| Truong | Kieu | Rang buoc theo spec | Phan hoach mien |
|---|---|---|---|
| `email` | string | bat buoc, khop voi token | dung / sai / rong / null / cua user khac |
| `resetToken` | string | bat buoc, dung, con han, dung 1 lan | dung / sai / rong / null / da dung / cua user khac / kieu so thay vi chuoi / SQLi |
| `newPassword` | string | >=8 ky tu, co hoa+thuong+so | hop le / <8 / rong / null / chi so / 1000 ky tu / trung mat khau cu / co khoang trang / unicode |

**Response impl:**
- 200 `{ message: "Password reset successfully" }`
- 400 `{ error: "Invalid token or email" }`

### 1.3 Bug da biet (API-1) — **DA KIEM CHUNG BANG REQUEST THAT o STEP 0**

| ID | Muc | SEC / FR bi vi pham | Mo ta | Bang chung thuc nghiem |
|---|---|---|---|---|
| **A-01** | Critical | SEC-07 | `forgot-password` tra thang `resetToken` trong response body. Bat ky ai biet email deu chiem duoc tai khoan. | `POST /api/forgot-password {"email":"api.victim..."}` -> `200 {"message":"Ma dat lai mat khau da duoc tao","resetToken":"5740"}` |
| **A-02** | High | SEC-07 | Token chi **4 chu so** (`Math.floor(1000+Math.random()*9000)`). SRS FR-03 + SEC-07 doi **6 chu so**. Khong gioi han so lan thu => vet brute-force toi da 9000. | token quan sat duoc: `"5740"` (4 ky tu) |
| **A-03** | High | — (lo thong tin) | User enumeration: email khong ton tai -> `404 {"error":"User not found"}`; email ton tai -> `200`. Do duoc danh sach user. | `POST /api/forgot-password {"email":"nobody..."}` -> `HTTP/1.1 404` |
| **A-04** | High | SEC-07 | Token **khong co han su dung**: cot `reset_token` khong kem timestamp, khong co bat ky phep so sanh thoi gian nao. | `database.js` schema `users`; `server.js` reset-password |
| **A-05** | High | FR-01 / FR-03 | `reset-password` **khong validate do manh mat khau**. SRS doi >=8 ky tu, co hoa+thuong+so+ky tu dac biet. Chap nhan `"1"`, `""`. | khong co nhanh kiem tra nao trong handler |
| **A-06** | Medium | FR-02 | Reset thanh cong **khong xoa `login_attempts` / `locked_until`** => doi mat khau xong van bi khoa. | `UPDATE users SET password=?, reset_token=NULL ...` |
| **A-07** | Critical | SEC-01 | Mat khau luu **plaintext**; `POST /api/login` va `GET /api/users/me` tra ve nguyen ban ghi `user` gom `password` va `reset_token`. | login -> `"user":{...,"password":"Api1234!","reset_token":null}` |
| **A-08** | Medium | — | `forgot-password` **bo qua bien `err`** cua `db.get` => loi DB bi bao thanh 404 "User not found". | `(err, user) => { if (!user) return 404 }` |
| **A-09** | High | FR-02 | Bo dem dang nhap sai cong **+2** moi lan (`user.login_attempts + 2`) => khoa sau **2** lan sai chu khong phai 3. Ngoai ra khoa **180000ms = 180s** trong khi SRS ghi **30s**. | `const newAttempts = user.login_attempts + 2;` `Date.now() + 180000` |
| **A-10** | Low | — | `reset-password` chi kiem `this.changes === 0`, **khong kiem `err`** => loi DB tra ve 200 "Password reset successfully". | callback `function (err)` khong dung `err` |
| **A-11** | High | SEC-07 | Xin token lan 2 **ghi de** token lan 1 nhung khong co co che vo hieu hoa/thu hoi ro rang; token cu im lang chet, khong co thong bao. Ket hop A-04 => vong doi token khong xac dinh. | 2 lan `forgot-password` lien tiep |

> **A-01, A-02, A-03, A-07 da co response that luu trong `bugs/BUG_REPORT.md`.**

---

## 2. API-2---

## 2. API-2 — Pool B / FR-08: Thanh toan (+ FR-09 coupon, FR-10 state machine)

### 2.1 `POST /api/checkout`
**Auth:** co (`authenticateToken`). **Body:** `{ total_amount, shipping_address }`
(FE con gui `items`, `coupon_id` nhung **backend bo qua hoan toan**).

| Truong | Kieu | Rang buoc theo spec | Phan hoach mien |
|---|---|---|---|
| `total_amount` | number | > 0, phai khop tong gio hang server-side | duong / 0 / am / chuoi so / chuoi chu / null / thieu / rat lon (1e18) / thap phan / NaN |
| `shipping_address` | string | bat buoc, khong rong | hop le / rong / null / thieu / 1000 ky tu / XSS payload / unicode |
| `items` | array | phai co >=1 item ton tai | (spec yeu cau, impl bo qua) |

**Response impl:** 200 `{ message:"Checkout successful", orderId:<int> }` | 401 | 403 | 500

### 2.2 `POST /api/apply-coupon`
**Auth: KHONG** (bug). **Body:** `{ code, total_amount, user_id }`

| Truong | Phan hoach mien |
|---|---|
| `code` | ton tai+active / ton tai+inactive / khong ton tai / rong / null / thieu / SQLi / khac hoa-thuong |
| `total_amount` | > min / = min (bien!) / < min / 0 / am / chuoi |
| `user_id` | cua minh / cua nguoi khac / khong gui / id khong ton tai |

### 2.3 State machine (FR-10)
- `PUT /api/orders/:id/cancel` (auth, chi order cua minh)
- `PUT /api/admin/orders/:id/status` (auth, **khong check role**) body `{ status }`
- `GET /api/orders/:id` — **khong auth** (bug)
- `GET /api/orders/my-orders` — auth

Bang chuyen trang thai can test day du (5 trang thai x 5 dich = 25 o):

| Tu \ Den | pending | confirmed | shipping | delivered | canceled |
|---|---|---|---|---|---|
| **pending** | ✗ | ✓ | ✗ | ✗ | ✓ |
| **confirmed** | ✗ | ✗ | ✓ | ✗ | ✓ |
| **shipping** | ✗ | ✗ | ✗ | ✓ | ✗ (impl cho phep qua `/cancel` — BUG) |
| **delivered** | ✗ | ✗ | ✗ | ✗ | ✗ |
| **canceled** | ✗ | ✗ | ✗ | ✗ (impl cho phep — BUG) | ✗ |

### 2.4 Bug da biet (API-2) — **DA KIEM CHUNG BANG REQUEST THAT o STEP 0**

| ID | Muc | SEC / FR bi vi pham | Mo ta | Bang chung thuc nghiem |
|---|---|---|---|---|
| **B-01** | Critical | FR-08 | `checkout` **tin tuyet doi `total_amount` tu client**. SRS FR-08: "Backend phai tu tinh lai tong tien; khong chap nhan `total_amount` do client gui len". | `POST /api/checkout {"total_amount":1,...}` -> `200 {"orderId":1}`; `GET /api/orders/1` -> `"total_amount":1` |
| **B-01b** | Critical | FR-08 | Chap nhan ca `total_amount` **am**. | `{"total_amount":-500000}` -> `200 {"orderId":2}` |
| **B-02** | Critical | SEC-02 | `GET /api/orders/:id` **thieu `authenticateToken`** => IDOR, doc duoc don hang cua bat ky ai chi bang id. | `curl /api/orders/1` khong header -> `200 {"id":1,"user_id":3,...}` |
| **B-03** | Critical | SEC-03 | `PUT /api/admin/orders/:id/status` co token nhung **khong kiem `role`** => user thuong doi trang thai don cua **nguoi khac**. | attacker(id=4) doi don cua victim(id=3) -> `200 {"message":"Order status updated"}` |
| **B-04** | High | FR-08 | `checkout` **bo qua `items` hoan toan**: don tao ra khong co dong hang, khong tru ton kho, khong validate san pham. | destructuring chi lay `total_amount`, `shipping_address` |
| **B-05** | Critical | FR-09 | Cong thuc `percent` sai: `discount = floor(total*(1-discount_value))`. Dung phai la `total*discount_value/100`. Voi `discount_value=10` => **discount am** => `final_amount > total`. | `SAVE10` tren `500000` -> `{"discount_amount":-4500000,"final_amount":5000000}` |
| **B-06** | High | FR-09 (C3) | Nguong don toi thieu dung `>` thay vi `>=`: don **bang dung** `min_order_amount` bi tu choi. | `SAVE10` + `total_amount=300000` (min=300000) -> `400 "Don hang chua du gia tri toi thieu 300,000"` |
| **B-07** | Critical | SEC-02 / FR-09 (C4) | `apply-coupon` **khong co `authenticateToken`**, lay `user_id` tu body => **bo `user_id` di la bo qua toan bo kiem tra han muc su dung**. | `{"code":"SAVE10","total_amount":500000}` (khong token, khong user_id) -> `200 success:true` |
| **B-08** | Medium | FR-09 | Kiem tra han su dung nam **ben trong** nhanh `total > min` => don nho + ma het han tra thong bao "chua du gia tri" thay vi "het han". Sai thu tu uu tien C2/C3. | `EXPIRED` + `total=50000` -> `400 "chua du gia tri toi thieu 100,000"` (dang le "het han") |
| **B-09** | High | FR-10 | `PUT /api/orders/:id/cancel` cho phep huy don dang `shipping` (chi chan `delivered`/`canceled`). SRS: "Khi don o `shipping`, User khong duoc tu huy". Comment trong source tu thua nhan sai. | don o `shipping` -> `PUT /cancel` -> `200`, `status` thanh `canceled` |
| **B-10** | High | FR-10 | `admin/orders/:id/status` co dong code **co y** cho phep `canceled -> delivered`, vi pham rang buoc trang thai ket thuc. | don `canceled` -> `{"status":"delivered"}` -> `200 {"message":"Order status updated"}` |
| **B-11** | Medium | FR-09 | `POST /api/coupon-usage` nhan `coupon_id` bat ky, khong gan voi order, khong kiem tra coupon ton tai => ban ghi rac lam sai han muc. | `INSERT INTO coupon_usage` khong validate |
| **B-12** | Medium | FR-08 | `shipping_address` khong bat buoc: thieu han truong nay van tao duoc don. | `{"total_amount":100}` -> `200 {"orderId":3}` |
| **B-13** | Medium | FR-08 | Gio hang server `userCarts` la object in-memory, **khong bao gio duoc xoa sau checkout**. SRS FR-08: "Sau thanh toan thanh cong, gio hang duoc xoa". | `const userCarts = {}`, khong co `delete` |
| **B-14** | Medium | FR-08 | `POST /api/checkout` tra `200` thay vi `201 Created` cho thao tac tao tai nguyen. | `res.json(...)` |

---

## 3. API-3---

## 3. API-3 — Pool C / FR-15: Quan ly san pham (CRUD)

### 3.1 Endpoint
| Method | Path | Auth theo spec | Auth thuc te |
|---|---|---|---|
| GET | `/api/products` | khong | khong |
| GET | `/api/products?search=` | khong | khong |
| GET | `/api/products/:id` | khong | khong |
| POST | `/api/products` | **admin** | **KHONG CO** (bug) |
| PUT | `/api/products/:id` | **admin** | **KHONG CO** (bug) |
| DELETE | `/api/products/:id` | **admin** | **KHONG CO** (bug) |

**Body POST/PUT:** `{ name, price, description, imageUrl, category_id }`

| Truong | Rang buoc theo spec | Phan hoach mien |
|---|---|---|
| `name` | bat buoc, 1..255 ky tu | hop le / rong / null / thieu / 256 ky tu / chi khoang trang / XSS `<script>` / unicode / trung ten |
| `price` | number > 0 | duong / 0 (bien) / am / chuoi so `"100"` / chuoi chu / null / thieu / thap phan / 1e18 / NaN |
| `description` | tuy chon, <=2000 | hop le / rong / null / 5000 ky tu / HTML |
| `imageUrl` | tuy chon, URL hop le | http / https / khong phai URL / `javascript:` / rong / null |
| `category_id` | phai ton tai trong `categories` | ton tai / khong ton tai (9999) / 0 / am / chuoi / null |
| `:id` (path) | so nguyen duong ton tai | ton tai / khong ton tai / 0 / am / chuoi / SQLi / rat lon |

### 3.2 Bug da biet (API-3) — **DA KIEM CHUNG BANG REQUEST THAT o STEP 0**

| ID | Muc | SEC / FR bi vi pham | Mo ta | Bang chung thuc nghiem |
|---|---|---|---|---|
| **C-01** | Critical | SEC-02 + SEC-03 / FR-12 | `POST` / `PUT` / `DELETE /api/products` **hoan toan khong xac thuc**. SRS FR-12 liet ke dich danh 3 endpoint nay la phai co token + `role='admin'`. Khach vang lai xoa duoc ca catalog. | `POST /api/products` khong header Authorization -> `200 {"message":"Product created","id":7}` |
| **C-02** | Critical | SEC-05 | `GET /api/products?search=` **noi chuoi SQL truc tiep**: `` WHERE name LIKE '%${searchQuery}%' ``. | `?search=%' OR '1'='1` -> tra ve **toan bo 5 san pham** thay vi 0 ket qua |
| **C-03** | High | — (vo hop dong) | Khi SQL loi, tra ve **HTML** `<h1>Database Error</h1><p>{err.message}</p>` voi `Content-Type: text/html` (500) => vua lo cau truc DB vua pha vo hop dong JSON. | `?search='` -> `HTTP/1.1 500`, `Content-Type: text/html; charset=utf-8` |
| **C-04** | High | — | `GET /api/products/:id` voi id khong ton tai tra **`200 {}`** thay vi `404`. | `GET /api/products/999999` -> `HTTP/1.1 200`, body `{}` |
| **C-05** | High | — (vo schema) | `GET /api/products/:id` tra `price` kieu **string** khi `id` chan, **number** khi id le. Client tinh tien sai. | id=1 -> `price` la `int 30000000`; id=2 -> `price` la `str "28000000"` |
| **C-06** | High | FR-15 | Khong validate gi: tao duoc san pham `price: -100`, `price: "abc"`, `name: null`. SRS FR-15: ten bat buoc <=255, gia phai > 0, danh muc bat buoc. | `POST {"name":"NoAuth2","price":-100,"category_id":9999}` -> `200` |
| **C-07** | Medium | — | `PUT /api/products/:id` voi id khong ton tai van tra `200 {"message":"Product updated"}` (khong dung `this.changes`). | callback bo qua `this.changes` |
| **C-08** | Medium | — | `DELETE /api/products/:id` voi id khong ton tai van tra `200 {"message":"Product deleted"}`. | callback bo qua `this.changes` |
| **C-09** | Medium | FR-15 | `PUT` khong ho tro cap nhat mot phan: truong khong gui bi ghi de thanh `null`. | `UPDATE products SET name=?,price=?,description=?,imageUrl=?,category_id=?` |
| **C-10** | Medium | FR-15 | `category_id` khong duoc kiem khoa ngoai => tao san pham thuoc danh muc khong ton tai (`9999`). | `POST ... "category_id":9999` -> `200` |
| **C-11** | Medium | SEC-04 | Khong sanitize `name` / `description`; server luu nguyen payload `<script>`. (Phan render la tang UI — o tang API chi kiem duoc **nua nguon** cua stored XSS.) | `POST {"name":"<script>alert(1)</script>"}` -> luu nguyen van |
| **C-12** | Low | — | `POST /api/products` tra `200` thay vi `201 Created`. | `res.json({message:"Product created", id})` |

---

## 3bis. Bug lien API (dung lam buoc leo thang cho SEC-03)

| ID | Muc | SEC | Mo ta | Bang chung thuc nghiem |
|---|---|---|---|---|
| **X-01** | Critical | SEC-06 | `PUT /api/users/me` nhan truong `role` tu body va ghi thang vao DB => **bat ky user thuong nao cung tu nang minh len `admin`**. SRS FR-04 + SEC-06 cam dich danh. | `PUT /api/users/me {"role":"admin"}` (token user thuong) -> `200`; `GET /api/users/me` -> `"role":"admin"` |

> X-01 khong thuoc 1 trong 3 API duoc chon nhung **bat buoc phai bao cao** (de bai muc 6.5:
> "Report any genuine bugs you find"). No con la **tien de** de test SEC-03 cho API-2/API-3:
> chuoi tan cong `user thuong -> tu nang role -> goi API admin` chung minh rang du co them
> check role thi van thung neu SEC-06 con ho.

---

## 4. Du lieu test co dinh (dung cho precondition)

`database.js` goi `initDatabase()` ngay khi `require` => **moi lan restart backend la DROP +
reseed toan bo DB**. Vi vay thu tu bat buoc la: **(1) restart backend -> (2) seed_sut.js reset
-> (3) newman**. Khong duoc restart giua chung.

### Du lieu co san sau khi backend khoi dong (tu `database.js`)

| Bang | Noi dung |
|---|---|
| `users` | id=1 `admin@eshop.com` / `Admin123!` role=admin; id=2 `test@eshop.com` / `Test1234!` role=user |
| `categories` | id=1 `Dien thoai`, id=2 `Laptop`, id=3 `Phu kien` |
| `products` | id=1..5 (1 iPhone 15 Pro Max 30000000, 2 Samsung S24 Ultra 28000000, 3 MacBook Pro M3 45000000, 4 AirPods Pro 2 6000000, 5 Keychron Q1 4000000) |
| `orders` | **rong** |
| `coupons` | xem bang duoi |
| `coupon_usage` | **rong** |

### Coupon da seed (TEN THAT — ban truoc cua file nay ghi sai `PERC10`/`FIX50K`/`INACTIVE`)

| Ma | type | discount_value | min_order_amount | expired_at | is_active | max_uses_per_user |
|---|---|---|---|---|---|---|
| `SAVE10` | percent | 10 | 300000 | 2099-12-31 | 1 | 1 |
| `BIGBUY` | fixed | 50000 | 500000 | 2099-12-31 | 1 | 1 |
| `VIP100` | fixed | 100000 | 300000 | 2099-12-31 | 1 | 2 |
| `EXPIRED` | percent | 20 | 100000 | 2020-01-01 | 1 | 1 |

> **Khong co coupon `is_active = 0` nao duoc seed.** Muon test nhanh C1 ("ma bi vo hieu hoa")
> phai tu tao qua `POST /api/admin/coupons` (nhung `is_active` mac dinh = 1, khong the tat qua API)
> hoac dung `sqlite3` CLI. Test case tuong ung dung ma **khong ton tai** (`NOTEXIST99`) lam
> dai dien cho nhanh "ma khong hop le", va ghi ro gioi han nay trong bao cao.

### Du lieu do `seed_sut.js reset` tao them

| Bien | Gia tri | Ghi chu |
|---|---|---|
| `userEmail` (nan nhan IDOR) | `api.victim.23127060@test.local` / `Api1234!` | id=3 sau seed sach |
| `attackerEmail` (ke tan cong) | `api.attacker.23127060@test.local` / `Api1234!` | id=4 sau seed sach |
| `adminEmail` | `admin@eshop.com` / `Admin123!` | co san tu `database.js` |
| `productIdOdd` | 1 | `price` la number |
| `productIdEven` | 2 | `price` bi ep thanh string — bug C-05 |
| `couponPercent` | `SAVE10` | min 300000 — dung cho B-05, B-06 |
| `couponFixed` | `BIGBUY` | min 500000 |
| `couponMultiUse` | `VIP100` | max 2 luot — dung cho B-07 |
| `couponExpired` | `EXPIRED` | dung cho B-08 |

> Luu y: `POST /api/register` cua SUT **khong kiem tra email trung** (khong co rang buoc
> `UNIQUE` tren cot `email`), nen chay `seed_sut.js reset` nhieu lan tren cung mot lan
> backend chay se tao user trung email va lam lech `userId`. Luon restart backend truoc khi seed.
