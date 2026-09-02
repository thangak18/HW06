# STEP 0 — Trinh sat moi truong & doi chieu dac ta

> HW06 — API Testing | SV **Ninh Van Khai — 23127060** | Ngay 01/09/2026

---

## 1. Moi truong thuc nghiem

| Hang muc | Gia tri |
|---|---|
| He dieu hanh | Linux 6.18.33.2-microsoft-standard-WSL2 (Ubuntu tren WSL2 / Windows) |
| Node.js | v20.20.2 |
| npm | 10.8.2 |
| Newman | 6.2.2 |
| Reporter | `newman-reporter-htmlextra` (cai kem, ban moi nhat tren npm) |
| Python | 3.13.5 (dung cho cac script sinh test / tong hop bao cao) |
| Postman | Ban Desktop dung cho phan thao tac GUI (workspace, Console, Runner, Mock, Monitor) |
| Base URL | `http://localhost:3000` — thoa yeu cau chong gian lan muc 11 de bai (`localhost`/`127.0.0.1`) |
| Shell | bash |

Lenh xac minh phien ban da chay:

```bash
node -v        # v20.20.2
npm -v         # 10.8.2
python3 -V     # Python 3.13.5
newman -v      # 6.2.2
```

## 2. System Under Test

| Hang muc | Gia tri |
|---|---|
| Repo | https://github.com/ttbhanh/eshop-sut |
| Commit dang test | `85af3ba875c88283615e22cb108f13e2fccaf0e9` |
| Ngay commit | 2026-05-15 08:30:35 +0700 — *"first upload"* |
| Duong dan cuc bo | `../../../eshop-sut/` (ngang hang voi thu muc repo `HW06/`, **khong** nam trong repo bai nop) |
| Backend | Node.js + Express + SQLite (`backend/server.js`, 572 dong) |
| CSDL | `backend/database.sqlite`, khoi tao boi `backend/database.js` (119 dong) |

### Cach khoi dong / dung

```bash
cd ../../../eshop-sut/backend
npm install                                   # chi lan dau
setsid nohup node server.js > /tmp/eshop.log 2>&1 < /dev/null &
curl -sf http://localhost:3000/api/products >/dev/null && echo "SUT UP"

pkill -f "node server.js"                     # dung
```

### CANH BAO VE VONG DOI CSDL

`database.js` goi `initDatabase()` **ngay khi module duoc `require`**, va `initDatabase()`
bat dau bang mot loat `DROP TABLE IF EXISTS`. Hau qua: **moi lan khoi dong lai backend la
toan bo CSDL bi xoa va seed lai tu dau.**

Vi vay thu tu bat buoc cho moi lan chay test la:

1. Khoi dong (hoac khoi dong lai) backend — CSDL ve trang thai goc.
2. `node agent-skill/eshop-api-23127060/scripts/seed_sut.js reset` — tao 2 tai khoan test.
3. Chay Newman.

Khong duoc restart backend o giua buoc 2 va 3. Ngoai ra `POST /api/register` cua SUT khong
co rang buoc `UNIQUE` tren `email`, nen chay `seed_sut.js reset` hai lan tren cung mot lan
backend chay se tao user trung email va lam lech `userId` cua cac test IDOR.

## 3. Cac tai lieu duoc dung lam oracle

SUT co **hai** tai lieu, vai tro khac han nhau. Xac dinh dung vai tro la viec quan trong
nhat cua STEP 0, vi no quyet dinh moi ky vong (`Expected_Status`) ve sau.

| Tai lieu | Vai tro thuc su | Dung lam oracle? |
|---|---|---|
| `eshop-sut/README.md` (288 dong) | **SRS** — tu tuyen bo "Mo ta **yeu cau nghiep vu dung** cua he thong EShop". Chua FR-01..FR-24 va bang SEC-01..SEC-07. | **CO — day la oracle `SPEC`** |
| `eshop-sut/api_specification.md` (214 dong) | Huong dan goi API: danh sach endpoint, body mau, response mau. **Khong mo ta rang buoc nghiep vu.** | Chi de lay hinh dang request/response |
| `eshop-sut/backend/server.js` | Hanh vi thuc te dang chay. | Oracle `IMPL` — dung cho test hoi quy |

Khi hai tai lieu mau thuan, lay `README.md` lam chuan. Vi du dien hinh: `api_specification.md`
in response mau cua `forgot-password` la `"resetToken": "123456"` (6 chu so) trong khi
`README.md` FR-03 va SEC-07 doi **toi thieu 6 chu so** — con code that sinh **4 chu so**.
Ca hai tai lieu deu chong lai implementation, nen day chac chan la bug (A-02).

## 4. [C3] DA SUA — bang SEC-01..SEC-07 truoc do la suy dien va sai hoan toan

`references/API_SPEC_NOTES.md` ban dau chua mot bang SEC **tu suy dien theo OWASP**
(SEC-01 = SQL Injection, SEC-04 = IDOR, SEC-07 = brute force...), kem ghi chu
"GIA DINH — phai xac nhan lai voi spec that o STEP 0".

Doi chieu voi `eshop-sut/README.md` muc 9 cho thay bang suy dien **khong trung mot dong nao**
voi bang that. Neu giu nguyen thi toan bo cot `SEC_Ref` cua >120 test case se sai, va phan
"do phu SEC-01..07" trong bao cao se la bia dat. Da sua lai file tham chieu theo bang that:

| Ma | Yeu cau that (SRS muc 9) | Truoc day bi suy dien nham thanh |
|---|---|---|
| SEC-01 | Mat khau **khong** duoc luu plaintext | "Chong SQL Injection" |
| SEC-02 | API co tinh bao mat phai yeu cau JWT hop le | "Khong lo du lieu nhay cam" |
| SEC-03 | API Admin phai kiem `role='admin'` trong token, khong chi kiem token ton tai | "Endpoint thay doi du lieu phai xac thuc" |
| SEC-04 | Du lieu user nhap phai duoc escape khi hien thi (khong `innerHTML`) | "Chong IDOR" |
| SEC-05 | Truy van CSDL phai dung Parameterized Query | "Chong role escalation" |
| SEC-06 | API cap nhat ho so khong duoc cho doi `role` tu client | "Validate input / chong XSS" |
| SEC-07 | OTP reset phai >= 6 chu so, co thoi han, vo hieu hoa sau khi dung | "Chong brute force / rate limit" |

**Gioi han da ghi nhan:** SEC-04 la yeu cau o tang hien thi (UI). O tang API chi kiem duoc
**nua nguon** cua stored XSS — tuc la server co luu nguyen payload `<script>` hay khong.
Bao cao se ghi ro gioi han nay, khong tuyen bo "da phu day du SEC-04".

## 5. Ba API duoc chon — khong trung voi thanh vien khac

| ID | Pool | FR | Endpoint chinh | Endpoint ho tro |
|---|---|---|---|---|
| API-1 | A | FR-03 Quen & dat lai mat khau | `POST /api/forgot-password`, `POST /api/reset-password` | `POST /api/login`, `POST /api/register` |
| API-2 | B | FR-08 Thanh toan | `POST /api/checkout` | `POST /api/apply-coupon` (FR-09), `PUT /api/orders/:id/cancel`, `PUT /api/admin/orders/:id/status`, `GET /api/orders/:id` (FR-10) |
| API-3 | C | FR-15 Quan ly san pham | `POST` / `PUT` / `DELETE /api/products` | `GET /api/products`, `GET /api/products?search=`, `GET /api/products/:id` |

**Pool D (Mobile) khong duoc su dung** — de bai muc 5 ghi ro: *"Pool D, the mobile app, is not
used here, because this homework targets the backend API"*.

Da doc `../../docs/team-api-allocation.md` (chi doc, khong sua). Tai thoi diem STEP 0 bang
phan cong cua nhom con de `TODO` cho ca 3 thanh vien, nen **chua the doi chieu tu dong**.
Bo ba (FR-03, FR-08, FR-15) da duoc chot trong `CLAUDE.md` va `SKILL.md` cua rieng SV
23127060; SV chiu trach nhiem xac nhan mieng voi 2 thanh vien con lai truoc khi nop.
Day la **rui ro mo** duoc theo doi, khong phai loi ky thuat.

**Cap nhat (02/09/2026, sau khi merge `origin/main`):** bang phan cong da duoc dien day du,
nen **da doi chieu duoc**. Ba bo API cua nhom:

| SV | Pool A | Pool B | Pool C |
|---|---|---|---|
| **23127060** (SV nay) | FR-03 | FR-08 | FR-15 |
| 23127195 | FR-04 | FR-09 | FR-16 |
| 23127259 | FR-02 | FR-10 | FR-14 |

**Khong co FR nao trung nhau** giua ba thanh vien -> thoa rang buoc muc 5 cua de bai.
Rui ro mo neu tren **da duoc dong**.

## 6. Kiem chung so bo bang request that

Truoc khi sinh test case, da chay mot loat `curl` de xac minh cac bug ghi trong
`references/API_SPEC_NOTES.md` la co that chu khong phai chep lai tu tri nho. Ket qua:
**toan bo bug da liet ke deu tai hien duoc**, va phat hien them 1 bug moi (X-01).

| Bug | Request | Response that quan sat duoc |
|---|---|---|
| A-01 | `POST /api/forgot-password {"email":"api.victim.23127060@test.local"}` | `200 {"message":"Ma dat lai mat khau da duoc tao","resetToken":"5740"}` |
| A-02 | (nhu tren) | token `"5740"` — **4 chu so**, trong khi SEC-07 doi toi thieu 6 |
| A-03 | `POST /api/forgot-password {"email":"nobody.23127060@test.local"}` | `HTTP/1.1 404 Not Found` — lo su ton tai cua tai khoan |
| A-07 | `POST /api/login` | body chua `"password":"Api1234!"` va `"reset_token":null` |
| B-01 | `POST /api/checkout {"total_amount":1,"shipping_address":"123 Test"}` | `200 {"orderId":1}`; `GET /api/orders/1` -> `"total_amount":1` |
| B-01b | `POST /api/checkout {"total_amount":-500000,...}` | `200 {"orderId":2}` — chap nhan tong tien am |
| B-02 | `GET /api/orders/1` **khong** header `Authorization` | `200 {"id":1,"user_id":3,...}` — IDOR |
| B-03 | attacker (id=4) `PUT /api/admin/orders/1/status {"status":"confirmed"}` | `200 {"message":"Order status updated"}` — doi don cua nguoi khac |
| B-05 | `POST /api/apply-coupon {"code":"SAVE10","total_amount":500000,"user_id":3}` | `{"discount_amount":-4500000,"final_amount":5000000}` — giam gia **am** |
| B-06 | `... {"code":"SAVE10","total_amount":300000}` (min = 300000) | `400 "Don hang chua du gia tri toi thieu 300,000"` — loi bien `>` vs `>=` |
| B-07 | `POST /api/apply-coupon {"code":"SAVE10","total_amount":500000}` (khong token, khong `user_id`) | `200 success:true` — bo qua toan bo kiem tra han muc |
| B-08 | `... {"code":"EXPIRED","total_amount":50000}` | `400 "chua du gia tri toi thieu 100,000"` — dang le phai bao "het han" |
| B-09 | don o `shipping` -> `PUT /api/orders/1/cancel` (token user) | `200`, trang thai thanh `canceled` — vi pham FR-10 |
| B-10 | don o `canceled` -> `PUT /api/admin/orders/1/status {"status":"delivered"}` | `200 {"message":"Order status updated"}` |
| B-12 | `POST /api/checkout {"total_amount":100}` (thieu `shipping_address`) | `200 {"orderId":3}` |
| C-01 | `POST /api/products` **khong** header `Authorization` | `200 {"message":"Product created","id":7}` |
| C-02 | `GET /api/products?search=%25' OR '1'='1` | tra ve **ca 5 san pham** thay vi 0 ket qua |
| C-03 | `GET /api/products?search='` | `500`, `Content-Type: text/html; charset=utf-8`, body `<h1>Database Error</h1>...` |
| C-04 | `GET /api/products/999999` | `200 {}` thay vi `404` |
| C-05 | `GET /api/products/1` vs `GET /api/products/2` | `price` la `int 30000000` vs `str "28000000"` |
| C-06 | `POST /api/products {"name":"NoAuth2","price":-100,"category_id":9999}` | `200` — gia am + danh muc khong ton tai deu duoc chap nhan |
| **X-01** | `PUT /api/users/me {"role":"admin"}` voi token user thuong | `200 {"message":"Profile updated"}`; `GET /api/users/me` -> `"role":"admin"` |

**X-01 la bug moi**, chua co trong ban `API_SPEC_NOTES.md` truoc do. No vi pham dich danh
SEC-06 va FR-04 ("khong the tu thay doi thuoc tinh `role`"). Da bo sung vao muc "3bis. Bug
lien API" cua file tham chieu, va se duoc dung lam **buoc leo thang** cho cac test SEC-03
cua API-2 va API-3.

## 7. Cac dinh chinh khac da ap dung vao `API_SPEC_NOTES.md`

| Muc | Truoc | Sau (theo `database.js` that) |
|---|---|---|
| Ten coupon seed | `PERC10`, `FIX50K`, `EXPIRED`, `INACTIVE` | `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED` |
| Coupon `is_active=0` | gia dinh co san | **khong co** — phai dung ma khong ton tai lam dai dien, da ghi ro gioi han |
| Thoi gian khoa tai khoan | khong ghi | impl khoa **180s**, SRS FR-02 ghi **30s** — them vao bug A-09 |
| So chu so OTP mong doi | khong ghi | SRS + SEC-07 doi **6**, impl sinh **4** |
| Bug A-11, B-01b, B-14 | chua co | bo sung sau khi doc lai `server.js` |

## 8. Ket luan STEP 0

- Moi truong day du, SUT chay duoc tren `localhost:3000`, Newman 6.2.2 san sang.
- Oracle da duoc xac dinh ro: `README.md` (SRS) = `SPEC`, `server.js` = `IMPL`.
- Bang SEC-01..07 da duoc sua ve dung ban goc — day la dinh chinh quan trong nhat cua buoc nay.
- 22 bug da tai hien duoc bang request that, san sang lam co so cho STEP 2 va STEP 7.
- **STEP ke tiep:** STEP 1 — ra soat lai `spec/api-1..3.json` cho khop voi cac dinh chinh tren.
