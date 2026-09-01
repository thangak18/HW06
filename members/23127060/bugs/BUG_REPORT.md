# BUG REPORT — HW06 API Testing

> SV **Ninh Van Khai — 23127060** | SUT: EShop @ `85af3ba` | De bai muc 6.5

Moi bug trong tai lieu nay deu **tai hien duoc bang request that**. Phan `curl` va phan response o tung muc duoc trich thang tu `bugs/evidence/<ID>.md` — la ket qua cua mot lan chay that bang `scripts/capture_bug_evidence.py`, khong go tay.

Chay lai toan bo bang chung:

```bash
python3 agent-skill/eshop-api-23127060/scripts/capture_bug_evidence.py \
  --base http://localhost:3000 --out bugs/evidence \
  --sut-dir ../../../../eshop-sut/backend
```

---

## 1. Bang tong hop

| ID | Muc do | Tieu de | API | Vi pham | Bang chung | GitHub Issue |
|---|---|---|---|---|---|---|
| **A-01** | 🔴 Critical | `POST /api/forgot-password` tra thang ma OTP trong response body | API-1 | SEC-07, FR-03 | [`A-01.md`](evidence/A-01.md) | `<dien link>` |
| **A-07** | 🔴 Critical | Mat khau luu plaintext va bi tra ve trong response cua `login` / `users/me` | API-1 | SEC-01 | [`A-07.md`](evidence/A-07.md) | `<dien link>` |
| **B-01** | 🔴 Critical | `checkout` tin tuyet doi `total_amount` do client gui | API-2 | FR-08 | [`B-01.md`](evidence/B-01.md) | `<dien link>` |
| **B-01b** | 🔴 Critical | `checkout` chap nhan `total_amount` am | API-2 | FR-08 | [`B-01b.md`](evidence/B-01b.md) | `<dien link>` |
| **B-02** | 🔴 Critical | `GET /api/orders/:id` thieu han xac thuc - IDOR | API-2 | SEC-02 | [`B-02.md`](evidence/B-02.md) | `<dien link>` |
| **B-03** | 🔴 Critical | `PUT /api/admin/orders/:id/status` khong kiem tra `role` | API-2 | SEC-03, FR-12 | [`B-03.md`](evidence/B-03.md) | `<dien link>` |
| **B-05** | 🔴 Critical | Cong thuc giam gia `percent` sai dau, cho ra so tien giam AM | API-2 | FR-09 | [`B-05.md`](evidence/B-05.md) | `<dien link>` |
| **B-07** | 🔴 Critical | `apply-coupon` khong xac thuc; bo `user_id` la bo qua toan bo kiem tra han muc | API-2 | SEC-02, FR-09 | [`B-07.md`](evidence/B-07.md) | `<dien link>` |
| **C-01** | 🔴 Critical | `POST` / `PUT` / `DELETE /api/products` hoan toan khong xac thuc | API-3 | SEC-02, SEC-03, FR-12 | [`C-01.md`](evidence/C-01.md) | `<dien link>` |
| **C-02** | 🔴 Critical | SQL Injection qua tham so `?search=` | API-3 | SEC-05 | [`C-02.md`](evidence/C-02.md) | `<dien link>` |
| **C-13** | 🔴 Critical | Mot san pham co `price = null` lam SAP HAN backend khi doc lai (tu choi dich vu) | API-3 | FR-15 | [`C-13.md`](evidence/C-13.md) | `<dien link>` |
| **X-01** | 🔴 Critical | `PUT /api/users/me` cho phep user thuong tu nang `role` len `admin` | lien API | SEC-06, FR-04, FR-12 | [`X-01.md`](evidence/X-01.md) | `<dien link>` |
| **A-02** | 🟠 High | OTP chi co 4 chu so trong khi dac ta doi toi thieu 6 | API-1 | SEC-07, FR-03 | [`A-02.md`](evidence/A-02.md) | `<dien link>` |
| **A-03** | 🟠 High | User enumeration qua ma trang thai cua `forgot-password` | API-1 | FR-03 | [`A-03.md`](evidence/A-03.md) | `<dien link>` |
| **A-05** | 🟠 High | `reset-password` khong kiem tra do manh mat khau | API-1 | FR-01, FR-03 | [`A-05.md`](evidence/A-05.md) | `<dien link>` |
| **A-09** | 🟠 High | Bo dem dang nhap sai cong +2 moi lan nen tai khoan bi khoa o lan sai thu HAI | API-1 | FR-02 | [`A-09.md`](evidence/A-09.md) | `<dien link>` |
| **B-06** | 🟠 High | Nguong don toi thieu dung `>` thay vi `>=` | API-2 | FR-09 | [`B-06.md`](evidence/B-06.md) | `<dien link>` |
| **B-09** | 🟠 High | `PUT /api/orders/:id/cancel` cho phep huy don dang giao (`shipping`) | API-2 | FR-10 | [`B-09.md`](evidence/B-09.md) | `<dien link>` |
| **B-10** | 🟠 High | `admin/orders/:id/status` cho phep chuyen `canceled` -> `delivered` | API-2 | FR-10 | [`B-10.md`](evidence/B-10.md) | `<dien link>` |
| **C-03** | 🟠 High | Loi SQL tra ve HTML kem thong diep cua tang CSDL | API-3 | SEC-05 | [`C-03.md`](evidence/C-03.md) | `<dien link>` |
| **C-04** | 🟠 High | `GET /api/products/:id` voi id khong ton tai tra `200 {}` thay vi `404` | API-3 | FR-15 | [`C-04.md`](evidence/C-04.md) | `<dien link>` |
| **C-05** | 🟠 High | `price` la so voi id le nhung la chuoi voi id chan | API-3 | FR-15 | [`C-05.md`](evidence/C-05.md) | `<dien link>` |
| **C-06** | 🟠 High | `POST /api/products` khong validate bat ky truong nao | API-3 | FR-15 | [`C-06.md`](evidence/C-06.md) | `<dien link>` |
| **A-08** | 🟡 Medium | `forgot-password` bo qua bien loi cua `db.get` nen loi CSDL bi bao thanh 404 | API-1 | FR-03 | [`A-08.md`](evidence/A-08.md) | `<dien link>` |
| **B-08** | 🟡 Medium | Kiem tra han su dung nam ben trong nhanh nguong don nen thong bao loi sai nguyen nhan | API-2 | FR-09 | [`B-08.md`](evidence/B-08.md) | `<dien link>` |
| **B-11** | 🟡 Medium | `POST /api/coupon-usage` ghi nhan luot dung cho `coupon_id` khong ton tai | API-2 | FR-09 | [`B-11.md`](evidence/B-11.md) | `<dien link>` |
| **B-12** | 🟡 Medium | `checkout` tao duoc don hang khi thieu han `shipping_address` | API-2 | FR-08 | [`B-12.md`](evidence/B-12.md) | `<dien link>` |
| **C-07** | 🟡 Medium | `PUT /api/products/:id` voi id khong ton tai van tra `200 Product updated` | API-3 | FR-15 | [`C-07.md`](evidence/C-07.md) | `<dien link>` |
| **C-08** | 🟡 Medium | `DELETE /api/products/:id` voi id khong ton tai van tra `200 Product deleted` | API-3 | FR-15 | [`C-08.md`](evidence/C-08.md) | `<dien link>` |
| **C-09** | 🟡 Medium | `PUT` khong ho tro cap nhat mot phan: truong khong gui bi ghi de thanh `null` | API-3 | FR-15 | [`C-09.md`](evidence/C-09.md) | `<dien link>` |
| **C-10** | 🟡 Medium | `category_id` khong duoc kiem khoa ngoai | API-3 | FR-15 | [`C-10.md`](evidence/C-10.md) | `<dien link>` |
| **C-11** | 🟡 Medium | `name` va `description` khong duoc sanitize - nguon cua stored XSS | API-3 | SEC-04 | [`C-11.md`](evidence/C-11.md) | `<dien link>` |
| **B-14** | ⚪ Low | `checkout` tra ve 200 thay vi 201 Created | API-2 | FR-08 | [`B-14.md`](evidence/B-14.md) | `<dien link>` |
| **C-12** | ⚪ Low | `POST /api/products` tra ve 200 thay vi 201 Created | API-3 | FR-15 | [`C-12.md`](evidence/C-12.md) | `<dien link>` |

**Tong 34 bug:** 12 Critical, 11 High, 9 Medium, 2 Low.

| API | So bug |
|---|---|
| API-1 | 7 |
| API-2 | 13 |
| API-3 | 13 |
| lien API | 1 |

De bai doi toi thieu 3 bug that cho moi API; ca ba deu vuot xa nguong nay.

---

## 2. Chi tiet tung bug

### A-01 — `POST /api/forgot-password` tra thang ma OTP trong response body

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-1 |
| **Vi pham** | SEC-07, FR-03 |
| **Bang chung day du** | [`bugs/evidence/A-01.md`](evidence/A-01.md) |

**Anh huong:** Bat ky ai biet dia chi email cua nan nhan deu chiem duoc tai khoan trong hai request, khong can truy cap hop thu. Day la duong chiem tai khoan ngan nhat trong toan he thong: goi forgot-password de lay OTP, roi goi reset-password de dat mat khau moi.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/forgot-password' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"email": "api.a01.victim.23127060@test.local"}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Mã đặt lại mật khẩu đã được tạo","resetToken":"5656"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-07, FR-03).

**De xuat sua:** Bo `resetToken` khoi response. Gui OTP qua email. Trong moi truong demo, ghi ra log may chu chu khong tra ve cho client.

---

### A-07 — Mat khau luu plaintext va bi tra ve trong response cua `login` / `users/me`

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-1 |
| **Vi pham** | SEC-01 |
| **Bang chung day du** | [`bugs/evidence/A-07.md`](evidence/A-07.md) |

**Anh huong:** Cot `password` luu nguyen van. `SELECT *` roi `res.json(user)` dua ca `password` lan `reset_token` ra ngoai. Bat ky ai xem duoc mot response login (log, proxy, cache trinh duyet) deu co mat khau that. Vi nguoi dung thuong dung lai mat khau, thiet hai vuot ra ngoai he thong nay.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/users/me' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -H 'Authorization: Bearer <token>'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":7,"name":"Victim","email":"api.a07.victim.23127060@test.local","password":"Api1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-01).

**De xuat sua:** Bam mat khau bang `bcrypt` khi ghi. Khi doc, chon dung cot can dung thay vi `SELECT *`, hoac loai bo `password` va `reset_token` truoc khi tra ve.

---

### B-01 — `checkout` tin tuyet doi `total_amount` do client gui

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-2 |
| **Vi pham** | FR-08 |
| **Bang chung day du** | [`bugs/evidence/B-01.md`](evidence/B-01.md) |

**Anh huong:** SRS FR-08 ghi ro: "Backend phai tu tinh lai tong tien; khong chap nhan gia tri `total_amount` do client gui len". Thuc te gia tri duoc ghi thang vao bang `orders`. Mua duoc dien thoai 30 trieu voi gia 1 dong. Day la lo hong gay thiet hai tai chinh truc tiep.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/orders/9' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -H 'Authorization: Bearer <token>'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":9,"user_id":9,"total_amount":1,"status":"pending","shipping_address":"1 Le Loi","created_at":"2026-09-01 08:33:12"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-08).

**De xuat sua:** Bo `total_amount` khoi body. Tinh lai tu gio hang phia may chu: doc `userCarts[userId]`, tra cuu gia tung san pham trong bang `products`, roi cong lai.

---

### B-01b — `checkout` chap nhan `total_amount` am

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-2 |
| **Vi pham** | FR-08 |
| **Bang chung day du** | [`bugs/evidence/B-01b.md`](evidence/B-01b.md) |

**Anh huong:** Truong hop rieng cua B-01 nhung dang chu y rieng: don hang co tong tien am duoc tao thanh cong. Neu he thong co buoc hoan tien hoac tinh doanh thu, so am se lam sai toan bo so sach.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/checkout' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -H 'Authorization: Bearer <token>' \
     -d '{"total_amount": -500000, "shipping_address": "1 Le Loi"}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Checkout successful","orderId":10}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-08).

**De xuat sua:** Sau khi tu tinh lai tong tien phia may chu, them rang buoc `CHECK (total_amount > 0)` o tang CSDL.

---

### B-02 — `GET /api/orders/:id` thieu han xac thuc - IDOR

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-2 |
| **Vi pham** | SEC-02 |
| **Bang chung day du** | [`bugs/evidence/B-02.md`](evidence/B-02.md) |

**Anh huong:** Endpoint khong co middleware `authenticateToken`. Bat ky ai duyet lan luot id tu 1 deu doc duoc toan bo don hang cua moi nguoi dung: dia chi giao hang, tong tien, trang thai. Day la lo lot du lieu ca nhan tren dien rong.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/orders/11' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":11,"user_id":11,"total_amount":500000,"status":"pending","shipping_address":"1 Le Loi","created_at":"2026-09-01 08:33:12"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-02).

**De xuat sua:** Them `authenticateToken` vao endpoint, va them dieu kien `AND user_id = ?` vao cau truy van de nguoi dung chi doc duoc don cua chinh minh.

---

### B-03 — `PUT /api/admin/orders/:id/status` khong kiem tra `role`

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-2 |
| **Vi pham** | SEC-03, FR-12 |
| **Bang chung day du** | [`bugs/evidence/B-03.md`](evidence/B-03.md) |

**Anh huong:** Endpoint co `authenticateToken` nhung khong he doc `req.user.role`. Bat ky nguoi dung dang nhap nao cung doi duoc trang thai don hang cua nguoi khac - vi du danh dau don cua nguoi khac la da giao de chan viec huy don.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X PUT 'http://localhost:3000/api/admin/orders/12/status' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -H 'Authorization: Bearer <token>' \
     -d '{"status": "confirmed"}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Order status updated"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-03, FR-12).

**De xuat sua:** Them middleware kiem quyen: `if (req.user.role !== 'admin') return res.status(403).json(...)`. Ap cho toan bo nhom duong dan `/api/admin/*`.

---

### B-05 — Cong thuc giam gia `percent` sai dau, cho ra so tien giam AM

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-2 |
| **Vi pham** | FR-09 |
| **Bang chung day du** | [`bugs/evidence/B-05.md`](evidence/B-05.md) |

**Anh huong:** Code tinh `discount = Math.floor(total * (1 - discount_value))`. Voi `discount_value = 10` (nghia la 10%), cong thuc thanh `total * (1 - 10) = total * (-9)`. Voi don 500.000d, `discount_amount` la **-4.500.000** va `final_amount` thanh **5.000.000** - khach hang bi tinh gap muoi lan khi ap ma giam gia. SRS FR-09 ghi ro cong thuc dung la `total * discount_value / 100`.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/apply-coupon' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"code": "SAVE10", "total_amount": 500000, "user_id": 1}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"success":true,"coupon_id":1,"discount_amount":-4500000,"final_amount":5000000,"message":"Áp dụng thành công! Giảm 10%"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-09).

**De xuat sua:** Sua thanh `Math.floor(total_amount * coupon.discount_value / 100)`.

---

### B-07 — `apply-coupon` khong xac thuc; bo `user_id` la bo qua toan bo kiem tra han muc

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-2 |
| **Vi pham** | SEC-02, FR-09 |
| **Bang chung day du** | [`bugs/evidence/B-07.md`](evidence/B-07.md) |

**Anh huong:** Endpoint khong co `authenticateToken` va lay `user_id` tu body. Nghiem trong hon: phep kiem han muc nam trong nhanh `if (user_id)`, nen **khong gui** truong nay se di vao nhanh `else` va ap ma ma khong dem luot nao ca. Day la nghich ly "bo bot du lieu de duoc nhieu quyen hon": ma gioi han mot luot moi nguoi tro thanh dung duoc vo han.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/apply-coupon' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"code": "VIP100", "total_amount": 500000}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"success":true,"coupon_id":3,"discount_amount":100000,"final_amount":400000,"message":"Áp dụng thành công! Giảm 100,000 ₫"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-02, FR-09).

**De xuat sua:** Them `authenticateToken` va lay `user_id` tu `req.user.id`, khong bao gio tu body. Bo hoan toan nhanh `else`.

---

### C-01 — `POST` / `PUT` / `DELETE /api/products` hoan toan khong xac thuc

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-3 |
| **Vi pham** | SEC-02, SEC-03, FR-12 |
| **Bang chung day du** | [`bugs/evidence/C-01.md`](evidence/C-01.md) |

**Anh huong:** SRS FR-12 liet ke dich danh ba endpoint nay trong nhom bat buoc phai co token JWT hop le **va** `role = 'admin'`. Thuc te khong co middleware nao ca. Mot nguoi hoan toan khong dang nhap co the xoa sach toan bo catalog san pham, hoac sua gia moi mat hang ve 0. Day la bug nghiem trong nhat cua API-3.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X DELETE 'http://localhost:3000/api/products/14' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Product deleted"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-02, SEC-03, FR-12).

**De xuat sua:** Them `authenticateToken` va middleware kiem `role === 'admin'` cho ca ba endpoint.

---

### C-02 — SQL Injection qua tham so `?search=`

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-3 |
| **Vi pham** | SEC-05 |
| **Bang chung day du** | [`bugs/evidence/C-02.md`](evidence/C-02.md) |

**Anh huong:** Cau truy van duoc noi chuoi truc tiep: ``WHERE name LIKE '%${searchQuery}%'``. Payload `%' OR '1'='1` tra ve toan bo bang. Nghiem trong hon, payload `UNION SELECT` doc duoc bang `users`: lan chay thu nghiem tra ve nguyen van `admin@eshop.com` kem mat khau `Admin123!` trong truong `price`. Ket hop voi A-07 (mat khau luu plaintext), mot request duy nhat lay duoc thong tin dang nhap cua quan tri vien.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/products?search=%25%27%20UNION%20SELECT%20id%2Cemail%2Cpassword%2Crole%2C1%2C1%20FROM%20users--%20' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

[{"id":1,"name":"admin@eshop.com","price":"Admin123!","description":"admin","imageUrl":1,"category_id":1},{"id":1,"name":"iPhone 15 Pro Max","price":30000000,"description":"Điện thoại cao cấp của Apple","imageUrl":"https://placehold.co/300x300/png?text=iPhone+15","category_id":1},{"id":2,"name":"Samsung Galaxy S24 Ultra","price":28000000,"description":"Màn hình hiển thị xuất sắc, camera siêu zoom","imageUrl":"https://placehold.co/300x300/png?text=Samsung+S24","category_id":1},{"id":2,"name":"test@eshop.com","price":"Test1234!","description":"user","imageUrl":1,"category_id":1},{"id":3,"name":"MacBook Pro M3","price":45000000,"description":"Laptop chuyên nghiệp mạnh mẽ","imageUrl":"https://placehold.co/300x300/png?text=Macbook+Pro","category_id":2},{"id":3,"name":"api.a01.victim.23127060@test.local","price":"Api1234!","description":"user","imageUrl":1,"category_id":1},{"id":4,"name":"Tai nghe AirPods Pro 2","price":6000000,"description":"Chống ồn chủ động xuất sắc","imageUrl":"https://placehold.co/300x300/png?text=AirPods+Pro","category_id":3},{"id":4,"name":"api.a02.victim.23127060@test.local","price":"Api1234!","description":"user","imageUrl":1,"category_id":1},{"id":5,"name":"Bàn
... (da cat bot)
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-05).

**De xuat sua:** Dung tham so hoa: `db.all("SELECT * FROM products WHERE name LIKE ?", ['%' + searchQuery + '%'], ...)`. Day dung la dieu SEC-05 yeu cau.

---

### C-13 — Mot san pham co `price = null` lam SAP HAN backend khi doc lai (tu choi dich vu)

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | API-3 |
| **Vi pham** | FR-15 |
| **Bang chung day du** | [`bugs/evidence/C-13.md`](evidence/C-13.md) |

**Anh huong:** Day la bug nguy hiem nhat tim duoc, va no la **he qua day chuyen cua hai bug khac**. C-09 cho phep mot lenh `PUT` thieu truong ghi de `price` thanh `null`. Sau do, C-05 chay `row.price.toString()` tren gia tri `null` khi id la so chan. `TypeError` nem ra trong callback cua `sqlite3` khong duoc ai bat, Node thoat han, **toan bo API ngung phuc vu**. Trong lan chay thu nghiem, request tiep theo tra ve `Connection refused` va moi kich ban sau do khong chay duoc nua. Mot nguoi khong dang nhap co the ha guc toan bo he thong bang **hai** request (C-01 cho phep goi `PUT` ma khong can token). Khong bug nao trong ba bug thanh phan tu no gay sap; chi to hop cua chung moi gay.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/products' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 0
Content-Type: (khong co)

<urlopen error [Errno 111] Connection refused>
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-15).

**De xuat sua:** Sua ca ba: (1) C-01 them xac thuc; (2) C-09 chi cap nhat truong duoc gui; (3) C-05 xoa dong ep kieu. Ngoai ra bat buoc phai co `process.on('uncaughtException')` va mot tang xu ly loi cho moi callback cua tang CSDL, de mot ban ghi hong khong the ha duoc ca tien trinh.

---

### X-01 — `PUT /api/users/me` cho phep user thuong tu nang `role` len `admin`

| | |
|---|---|
| **Muc do** | 🔴 Critical |
| **API** | lien API |
| **Vi pham** | SEC-06, FR-04, FR-12 |
| **Bang chung day du** | [`bugs/evidence/X-01.md`](evidence/X-01.md) |

**Anh huong:** Endpoint nhan truong `role` tu body va ghi thang vao CSDL. Bat ky tai khoan nao cung tu tro thanh admin bang mot request. Ket hop voi viec cac API admin khac chi kiem su ton tai cua token, day la duong leo thang quyen tron ven.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/users/me' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -H 'Authorization: Bearer <token>'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":3,"name":"Attacker","email":"api.x01.attacker.23127060@test.local","password":"Api1234!","role":"admin","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":"Q5","phone":"0900000000"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-06, FR-04, FR-12).

**De xuat sua:** Bo `role` khoi danh sach truong duoc phep cap nhat. Chi cho phep dung ba truong `name`, `phone`, `shipping_address` nhu SRS FR-04 quy dinh.

---

### A-02 — OTP chi co 4 chu so trong khi dac ta doi toi thieu 6

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-1 |
| **Vi pham** | SEC-07, FR-03 |
| **Bang chung day du** | [`bugs/evidence/A-02.md`](evidence/A-02.md) |

**Anh huong:** Khong gian ma chi 9000 gia tri (1000-9999). Khong co gioi han so lan thu nen do het toan bo khong gian la kha thi. Nghiem trong hon: voi 4 chu so, chi can khoang 100 nguoi cung dang cho reset la xac suat co hai nguoi trung ma vuot 40% (nghich ly ngay sinh) - khi do dieu kien `email AND reset_token` khong con bao ve duoc ai.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/forgot-password' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"email": "api.a02.victim.23127060@test.local"}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Mã đặt lại mật khẩu đã được tạo","resetToken":"2269"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-07, FR-03).

**De xuat sua:** `Math.floor(100000 + Math.random() * 900000)` cho 6 chu so, va tot hon la dung `crypto.randomInt` thay vi `Math.random` (khong an toan ve mat mat ma).

---

### A-03 — User enumeration qua ma trang thai cua `forgot-password`

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-1 |
| **Vi pham** | FR-03 |
| **Bang chung day du** | [`bugs/evidence/A-03.md`](evidence/A-03.md) |

**Anh huong:** Email khong ton tai tra 404, email ton tai tra 200. Ke tan cong do duoc toan bo danh sach nguoi dung cua he thong chi bang cach thu lan luot cac dia chi email.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/forgot-password' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"email": "khongtontai.23127060@test.local"}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 404
Content-Type: application/json; charset=utf-8

{"error":"User not found"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-03).

**De xuat sua:** Luon tra ve 200 voi cung mot thong diep chung chung, bat ke email co ton tai hay khong.

---

### A-05 — `reset-password` khong kiem tra do manh mat khau

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-1 |
| **Vi pham** | FR-01, FR-03 |
| **Bang chung day du** | [`bugs/evidence/A-05.md`](evidence/A-05.md) |

**Anh huong:** SRS doi mat khau toi thieu 8 ky tu, co chu hoa, chu thuong, chu so va ky tu dac biet. Thuc te chap nhan ca chuoi mot ky tu `"1"`. Nguoi dung di qua luong quen mat khau se dat duoc mot mat khau ma luong dang ky khong bao gio cho phep.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/login' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"email": "api.a05.victim.23127060@test.local", "password": "1"}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Login successful","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Niwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODgyNTE1OTJ9.QdfpV08ef8akzW7CPaYXz_VmF6uUE73cAiJ6wM52xqw","user":{"id":6,"name":"Victim","email":"api.a05.victim.23127060@test.local","password":"1","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-01, FR-03).

**De xuat sua:** Tach phep kiem do manh mat khau thanh mot ham dung chung, goi o ca `register` lan `reset-password`.

---

### A-09 — Bo dem dang nhap sai cong +2 moi lan nen tai khoan bi khoa o lan sai thu HAI

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-1 |
| **Vi pham** | FR-02 |
| **Bang chung day du** | [`bugs/evidence/A-09.md`](evidence/A-09.md) |

**Anh huong:** SRS quy dinh khoa tu lan sai thu ba va khoa 30 giay. Thuc te: `user.login_attempts + 2` nen dat nguong 3 ngay o lan sai thu hai, va thoi gian khoa la `180000` ms = 180 giay, gap sau lan quy dinh. Nguoi dung go nham mat khau hai lan bi khoa ba phut.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/login' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"email": "api.a09.victim.23127060@test.local", "password": "Api1234!"}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 403
Content-Type: application/json; charset=utf-8

{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-02).

**De xuat sua:** Doi `+ 2` thanh `+ 1` va `180000` thanh `30000`.

---

### B-06 — Nguong don toi thieu dung `>` thay vi `>=`

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-2 |
| **Vi pham** | FR-09 |
| **Bang chung day du** | [`bugs/evidence/B-06.md`](evidence/B-06.md) |

**Anh huong:** SRS FR-09 dieu kien C3 ghi ro "Tong don hang **>= (lon hon hoac bang)** `min_order_amount`". Code viet `if (total_amount > coupon.min_order_amount)`. Don co gia tri bang dung nguong bi tu choi. Day la loi bien kinh dien, va no roi dung vao truong hop nguoi dung hay gap nhat: mua vua du nguong de duoc giam gia.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/apply-coupon' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"code": "SAVE10", "total_amount": 300001, "user_id": 1}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"success":true,"coupon_id":1,"discount_amount":-2700009,"final_amount":3000010,"message":"Áp dụng thành công! Giảm 10%"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-09).

**De xuat sua:** Doi `>` thanh `>=`.

---

### B-09 — `PUT /api/orders/:id/cancel` cho phep huy don dang giao (`shipping`)

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-2 |
| **Vi pham** | FR-10 |
| **Bang chung day du** | [`bugs/evidence/B-09.md`](evidence/B-09.md) |

**Anh huong:** SRS FR-10 ghi ro: "Khi don hang da o trang thai `shipping`, User khong duoc phep tu huy - chi Admin moi co the thao tac". Code chi chan `delivered` va `canceled`. Khach hang huy don khi hang dang tren duong giao, gay that thoat hang va chi phi van chuyen. Chinh comment trong ma nguon cung thua nhan dieu kien nay sai.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/orders/13' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":13,"user_id":14,"total_amount":500000,"status":"canceled","shipping_address":"1 Le Loi","created_at":"2026-09-01 08:33:12"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-10).

**De xuat sua:** Doi dieu kien thanh `if (order.status !== 'pending' && order.status !== 'confirmed')` dung nhu comment trong ma nguon da ghi.

---

### B-10 — `admin/orders/:id/status` cho phep chuyen `canceled` -> `delivered`

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-2 |
| **Vi pham** | FR-10 |
| **Bang chung day du** | [`bugs/evidence/B-10.md`](evidence/B-10.md) |

**Anh huong:** SRS FR-10 ghi ro `delivered` va `canceled` la **trang thai ket thuc**, khong duoc chuyen sang bat ky trang thai nao khac. Trong ma nguon co mot dong rieng biet `if (currentStatus === 'canceled' && status === 'delivered') isValidTransition = true` - mot don da huy co the bi danh dau la da giao.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/orders/14' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":14,"user_id":15,"total_amount":500000,"status":"delivered","shipping_address":"1 Le Loi","created_at":"2026-09-01 08:33:12"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-10).

**De xuat sua:** Xoa dong do. Tot hon: thay chuoi `if` bang mot bang chuyen trang thai khai bao duoc, de so do FR-10 va ma nguon doc ra cung mot thu.

---

### C-03 — Loi SQL tra ve HTML kem thong diep cua tang CSDL

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-3 |
| **Vi pham** | SEC-05 |
| **Bang chung day du** | [`bugs/evidence/C-03.md`](evidence/C-03.md) |

**Anh huong:** Khi truy van loi, may chu tra `res.status(500).send('<h1>Database Error</h1><p>' + err.message + '</p>')` voi `Content-Type: text/html`. Hai hau qua: lo cau truc CSDL cho ke tan cong (giup tinh chinh payload SQLi), va pha vo hop dong JSON khien client goi `response.json()` bi nem loi.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/products?search=%27' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 500
Content-Type: text/html; charset=utf-8

<h1>Database Error</h1><p>SQLITE_ERROR: unrecognized token: "'"</p>
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-05).

**De xuat sua:** Tra ve `res.status(500).json({ error: 'Internal server error' })`. Ghi `err.message` vao log may chu, khong gui cho client.

---

### C-04 — `GET /api/products/:id` voi id khong ton tai tra `200 {}` thay vi `404`

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-3 |
| **Vi pham** | FR-15 |
| **Bang chung day du** | [`bugs/evidence/C-04.md`](evidence/C-04.md) |

**Anh huong:** Dong `if (!row) return res.status(200).json({})` tra ve thanh cong cho mot tai nguyen khong ton tai. Client khong phan biet duoc "khong tim thay" voi "tim thay nhung rong", va lop hien thi se ve ra mot san pham trong thay vi bao loi.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/products/999999' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-15).

**De xuat sua:** `return res.status(404).json({ error: 'Product not found' })`.

---

### C-05 — `price` la so voi id le nhung la chuoi voi id chan

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-3 |
| **Vi pham** | FR-15 |
| **Bang chung day du** | [`bugs/evidence/C-05.md`](evidence/C-05.md) |

**Anh huong:** Dong `if (row.id % 2 === 0) row.price = row.price.toString()` doi kieu du lieu theo tinh chan le cua khoa chinh. Client cong tien se nhan `"28000000" + 1000` ra chuoi `"280000001000"`. Bug chi lo ra khi so sanh hai response voi nhau; test rieng tung response deu thay hop le.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/products/2' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":2,"name":"Samsung Galaxy S24 Ultra","price":"28000000","description":"Màn hình hiển thị xuất sắc, camera siêu zoom","imageUrl":"https://placehold.co/300x300/png?text=Samsung+S24","category_id":1}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-15).

**De xuat sua:** Xoa dong do. Them rang buoc kieu vao hop dong API va kiem bang JSON Schema trong bo test hoi quy.

---

### C-06 — `POST /api/products` khong validate bat ky truong nao

| | |
|---|---|
| **Muc do** | 🟠 High |
| **API** | API-3 |
| **Vi pham** | FR-15 |
| **Bang chung day du** | [`bugs/evidence/C-06.md`](evidence/C-06.md) |

**Anh huong:** SRS FR-15 doi: ten bat buoc toi da 255 ky tu, gia bat buoc va phai duong, danh muc bat buoc chon tu danh sach co san. Thuc te tao duoc san pham voi `price: -100`, `price: "abc"`, `name: null`. Du lieu hong di vao CSDL va gay hau qua day chuyen - xem C-13.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/products' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"name": null, "price": "abc", "description": "x", "imageUrl": "", "category_id": 1}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Product created","id":16}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-15).

**De xuat sua:** Them tang validate dau vao (vi du `express-validator` hoac mot ham kiem tay) truoc khi ghi.

---

### A-08 — `forgot-password` bo qua bien loi cua `db.get` nen loi CSDL bi bao thanh 404

| | |
|---|---|
| **Muc do** | 🟡 Medium |
| **API** | API-1 |
| **Vi pham** | FR-03 |
| **Bang chung day du** | [`bugs/evidence/A-08.md`](evidence/A-08.md) |

**Anh huong:** Callback nhan `(err, user)` nhung chi kiem `if (!user)`. Moi su co tang CSDL deu bien thanh "User not found", che mat su co that va lam nguoi dung tuong tai khoan cua ho khong ton tai.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/forgot-password' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"email": null}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 404
Content-Type: application/json; charset=utf-8

{"error":"User not found"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-03).

**De xuat sua:** Kiem `if (err) return res.status(500).json({ error: 'Internal error' })` truoc khi kiem `!user`.

---

### B-08 — Kiem tra han su dung nam ben trong nhanh nguong don nen thong bao loi sai nguyen nhan

| | |
|---|---|
| **Muc do** | 🟡 Medium |
| **API** | API-2 |
| **Vi pham** | FR-09 |
| **Bang chung day du** | [`bugs/evidence/B-08.md`](evidence/B-08.md) |

**Anh huong:** Phep kiem `expired_at` duoc long ben trong `if (total_amount > min_order_amount)`. Mot ma da het han dung cho don nho hon nguong se bao "chua du gia tri toi thieu" thay vi "ma da het han". Nguoi dung se co mua them hang de dat nguong roi van bi tu choi.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/apply-coupon' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"code": "EXPIRED", "total_amount": 50000, "user_id": 1}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 400
Content-Type: application/json; charset=utf-8

{"error":"Đơn hàng chưa đủ giá trị tối thiểu 100,000 ₫ để áp dụng mã này"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-09).

**De xuat sua:** Tach nam dieu kien C1-C5 cua FR-09 thanh nam phep kiem doc lap, chay theo dung thu tu uu tien va moi phep kiem tra ve thong bao rieng.

---

### B-11 — `POST /api/coupon-usage` ghi nhan luot dung cho `coupon_id` khong ton tai

| | |
|---|---|
| **Muc do** | 🟡 Medium |
| **API** | API-2 |
| **Vi pham** | FR-09 |
| **Bang chung day du** | [`bugs/evidence/B-11.md`](evidence/B-11.md) |

**Anh huong:** Khong kiem tra ma giam gia co ton tai khong, cung khong gan voi don hang nao. Ke tan cong tao duoc ban ghi rac, hoac chen luot dung gia cho tai khoan nguoi khac de ho khong dung duoc ma nua.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/coupon-usage' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -H 'Authorization: Bearer <token>' \
     -d '{"coupon_id": 999999}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Usage recorded"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-09).

**De xuat sua:** Kiem `coupon_id` ton tai va gan ban ghi voi `order_id` that. Tot nhat la ghi nhan luot dung ngay trong giao dich thanh toan thay vi de client goi mot endpoint rieng.

---

### B-12 — `checkout` tao duoc don hang khi thieu han `shipping_address`

| | |
|---|---|
| **Muc do** | 🟡 Medium |
| **API** | API-2 |
| **Vi pham** | FR-08 |
| **Bang chung day du** | [`bugs/evidence/B-12.md`](evidence/B-12.md) |

**Anh huong:** Khong co phep kiem nao. Don hang duoc tao voi dia chi giao hang `null`, khong the giao duoc va chi phat hien ra o khau van hanh.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/orders/15' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":15,"user_id":17,"total_amount":100,"status":"pending","shipping_address":null,"created_at":"2026-09-01 08:33:12"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-08).

**De xuat sua:** Kiem `shipping_address` bat buoc va khong rong truoc khi ghi; hoac lay dia chi mac dinh tu ho so nguoi dung khi client khong gui.

---

### C-07 — `PUT /api/products/:id` voi id khong ton tai van tra `200 Product updated`

| | |
|---|---|
| **Muc do** | 🟡 Medium |
| **API** | API-3 |
| **Vi pham** | FR-15 |
| **Bang chung day du** | [`bugs/evidence/C-07.md`](evidence/C-07.md) |

**Anh huong:** Callback khong doc `this.changes`, nen khong phan biet duoc "da cap nhat 1 dong" voi "khong dong nao khop". Client tuong da luu thanh cong trong khi khong co gi thay doi.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X PUT 'http://localhost:3000/api/products/999999' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"name": "Khong ton tai", "price": 1, "description": "x", "imageUrl": "", "category_id": 1}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Product updated"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-15).

**De xuat sua:** `if (this.changes === 0) return res.status(404).json({ error: 'Product not found' })`.

---

### C-08 — `DELETE /api/products/:id` voi id khong ton tai van tra `200 Product deleted`

| | |
|---|---|
| **Muc do** | 🟡 Medium |
| **API** | API-3 |
| **Vi pham** | FR-15 |
| **Bang chung day du** | [`bugs/evidence/C-08.md`](evidence/C-08.md) |

**Anh huong:** Cung nguyen nhan voi C-07.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X DELETE 'http://localhost:3000/api/products/999999' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Product deleted"}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-15).

**De xuat sua:** Kiem `this.changes` truoc khi tra ve thanh cong.

---

### C-09 — `PUT` khong ho tro cap nhat mot phan: truong khong gui bi ghi de thanh `null`

| | |
|---|---|
| **Muc do** | 🟡 Medium |
| **API** | API-3 |
| **Vi pham** | FR-15 |
| **Bang chung day du** | [`bugs/evidence/C-09.md`](evidence/C-09.md) |

**Anh huong:** Cau `UPDATE products SET name=?, price=?, description=?, imageUrl=?, category_id=?` luon ghi ca nam cot. Gui mot body chi co `name` se xoa trang bon truong con lai. Lan chay thu nghiem cho ket qua `{"price": null, "description": null, "imageUrl": null, "category_id": null}`. Day la nguyen nhan truc tiep cua C-13.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/products/17' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":17,"name":"Chi doi ten 23127060","price":null,"description":null,"imageUrl":null,"category_id":null}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-15).

**De xuat sua:** Dung cau `UPDATE` dong chi gom cac truong that su co mat trong body, hoac doi hoi PUT phai gui du va dung `PATCH` cho cap nhat mot phan.

---

### C-10 — `category_id` khong duoc kiem khoa ngoai

| | |
|---|---|
| **Muc do** | 🟡 Medium |
| **API** | API-3 |
| **Vi pham** | FR-15 |
| **Bang chung day du** | [`bugs/evidence/C-10.md`](evidence/C-10.md) |

**Anh huong:** Tao duoc san pham voi `category_id = 9999` trong khi bang `categories` chi co id 1, 2, 3. San pham tro toi mot danh muc khong ton tai va se khong hien ra o bat ky bo loc theo danh muc nao.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/categories' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

[{"id":1,"name":"Điện thoại"},{"id":2,"name":"Laptop"},{"id":3,"name":"Phụ kiện"}]
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-15).

**De xuat sua:** Kiem `category_id` ton tai truoc khi ghi, va khai bao `FOREIGN KEY (category_id) REFERENCES categories(id)` trong `database.js` kem `PRAGMA foreign_keys = ON`.

---

### C-11 — `name` va `description` khong duoc sanitize - nguon cua stored XSS

| | |
|---|---|
| **Muc do** | 🟡 Medium |
| **API** | API-3 |
| **Vi pham** | SEC-04 |
| **Bang chung day du** | [`bugs/evidence/C-11.md`](evidence/C-11.md) |

**Anh huong:** Payload `<script>` va `<img src=x onerror=>` duoc luu nguyen van vao CSDL va tra ve nguyen van. SEC-04 doi du lieu nguoi dung nhap phai duoc escape khi hien thi. **Gioi han cua phep kiem nay:** o tang API chi chung minh duoc **nua nguon** - rang may chu luu payload tho. Viec no co thuc su chay tren trinh duyet hay khong con phu thuoc vao lop hien thi, phai kiem rieng o tang giao dien.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X GET 'http://localhost:3000/api/products/19' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"id":19,"name":"<script>alert('23127060')</script>","price":1000,"description":"<img src=x onerror=alert(1)>","imageUrl":"","category_id":1}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (SEC-04).

**De xuat sua:** Escape khi hien thi (khong dung `dangerouslySetInnerHTML`), va loc dau vao ngay o tang API nhu mot lop phong thu thu hai.

---

### B-14 — `checkout` tra ve 200 thay vi 201 Created

| | |
|---|---|
| **Muc do** | ⚪ Low |
| **API** | API-2 |
| **Vi pham** | FR-08 |
| **Bang chung day du** | [`bugs/evidence/B-14.md`](evidence/B-14.md) |

**Anh huong:** Thao tac tao tai nguyen moi phai tra `201 Created`. Khong gay hai truc tiep nhung pha vo quy uoc REST va lam client kho phan biet "da tao" voi "da co san".

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/checkout' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -H 'Authorization: Bearer <token>' \
     -d '{"total_amount": 500000, "shipping_address": "1 Le Loi"}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Checkout successful","orderId":16}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-08).

**De xuat sua:** `res.status(201).json({ ... })`.

---

### C-12 — `POST /api/products` tra ve 200 thay vi 201 Created

| | |
|---|---|
| **Muc do** | ⚪ Low |
| **API** | API-3 |
| **Vi pham** | FR-15 |
| **Bang chung day du** | [`bugs/evidence/C-12.md`](evidence/C-12.md) |

**Anh huong:** Cung loai voi B-14.

**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):

```bash
curl -i -X POST 'http://localhost:3000/api/products' \
     -H 'Content-Type: application/json' \
     -H 'X-Student-Id: 23127060' \
     -d '{"name": "Ma trang thai 23127060", "price": 1000, "description": "x", "imageUrl": "", "category_id": 1}'
```

**Ket qua thuc te:**

```http
HTTP/1.1 200
Content-Type: application/json; charset=utf-8

{"message":"Product created","id":20}
```

**Ket qua mong doi:** theo `eshop-sut/README.md` (FR-15).

**De xuat sua:** `res.status(201).json({ ... })`.

---

## 3. Cong viec con lai cua sinh vien (HUMAN H3)

De bai muc 6.5 doi moi bug phai duoc mo thanh mot GitHub Issue **kem anh chup man hinh**.
Cac file trong `bugs/ISSUE_TEMPLATES/` da san sang de dan thang len GitHub:

1. Mo `https://github.com/<tai-khoan>/<repo>/issues/new`.
2. Dan noi dung `bugs/ISSUE_TEMPLATES/<ID>.md` (dong dau la tieu de Issue).
3. Gan nhan theo muc do: `critical` / `high` / `medium` / `low`, kem nhan `api-1` / `api-2` / `api-3`.
4. Chup man hinh Issue vua tao, luu vao `bugs/screenshots/<ID>.png`.
5. Dien so hieu Issue vao cot **GitHub Issue** cua bang o muc 1.

> Uu tien mo Issue cho 12 bug Critical truoc neu khong du thoi gian lam het.

