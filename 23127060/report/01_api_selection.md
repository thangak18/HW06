# STEP 1 — Lua chon 3 API va lap dac ta may doc duoc

> HW06 — API Testing | SV **Ninh Van Khai — 23127060**

---

## 1. Ba API duoc chon (de bai muc 5)

De bai yeu cau chon **dung 3 API**, moi Pool mot cai, va khong duoc trung voi thanh vien khac.

| ID | Pool | FR | Endpoint chinh | Endpoint ho tro | Ly do chon |
|---|---|---|---|---|---|
| **API-1** | A | FR-03 Quen & dat lai mat khau | `POST /api/forgot-password`<br>`POST /api/reset-password` | `POST /api/login`, `POST /api/register` | La luong **2 buoc co trang thai** (chua co token -> da cap token -> da dung token), nen vua co domain partition day du vua co state machine that su. Dong thoi la be mat tan cong dam dac nhat: SEC-01 (mat khau plaintext) va SEC-07 (entropy/vong doi OTP) deu hoi tu o day. |
| **API-2** | B | FR-08 Thanh toan | `POST /api/checkout` | `POST /api/apply-coupon` (FR-09), `GET /api/orders/:id`, `PUT /api/orders/:id/cancel`, `PUT /api/admin/orders/:id/status` (FR-10) | Ket hop **ba** thu ma de bai doi: tinh tien (domain partition tren so tien), **state machine 5 trang thai** cua FR-10, va phan quyen (SEC-02, SEC-03). FR-09 con cho mot **bang quyet dinh 5 dieu kien** viet san trong SRS. |
| **API-3** | C | FR-15 Quan ly san pham | `POST` / `PUT` / `DELETE /api/products` | `GET /api/products`, `GET /api/products?search=`, `GET /api/products/:id` | CRUD day du nen co vong doi tai nguyen (`NOT_EXIST -> CREATED -> UPDATED -> DELETED`), co tham so o ca **body, path va query** (3 vi tri khac nhau), va la noi duy nhat co **SQL noi chuoi** — bat buoc de phu SEC-05. |

**Pool D (Mobile) khong duoc su dung.** De bai muc 5 ghi ro: *"Pool D, the mobile app, is not
used here, because this homework targets the backend API."* Neu can, phan mobile chi co the
lam phu luc khong tinh diem.

### Kiem tra trung lap trong nhom

Da doc `../../docs/team-api-allocation.md` (chi doc, khong sua). Tai thoi diem lam bai, bang
phan cong con de `TODO` o ca 3 dong thanh vien, nen **khong the doi chieu tu dong**. Bo ba
(FR-03, FR-08, FR-15) da duoc chot tu dau trong `CLAUDE.md`. Day la **rui ro mo can xac nhan
mieng voi 2 thanh vien con lai truoc khi nop**, khong phai van de ky thuat.

**Cap nhat (02/09/2026, sau khi merge `origin/main`):** bang phan cong da duoc dien day du,
nen **da doi chieu duoc**. Ba bo API cua nhom:

| SV | Pool A | Pool B | Pool C |
|---|---|---|---|
| **23127060** (SV nay) | FR-03 | FR-08 | FR-15 |
| 23127195 | FR-04 | FR-09 | FR-16 |
| 23127259 | FR-02 | FR-10 | FR-14 |

**Khong co FR nao trung nhau** giua ba thanh vien -> thoa rang buoc muc 5 cua de bai.
Rui ro mo neu tren **da duoc dong**.

## 2. Vi sao phai lap dac ta may doc duoc

De bai muc 7 (10 diem, muc Create G9.5) yeu cau mot bo sinh test: *"given the API
specification, it produces test cases automatically"*. Dac ta van xuoi cua SUT
(`eshop-sut/README.md`) khong the dua thang cho chuong trinh doc, vi no **khong noi ro dau la
truc phan hoach**. Vi du cau "Gia: bat buoc, phai la so duong (> 0)" chua ba thong tin an:
tham so `price`, kieu so, va mot **bien tai 0**. Con nguoi doc ra ngay; chuong trinh thi khong.

Vi vay STEP 1 dich SRS sang `spec/api-1.json`, `api-2.json`, `api-3.json` — moi file goi
**bon truc**, anh xa mot doi mot sang bon nhom ky thuat ma de bai muc 6.1 doi hoi:

| Khoa trong spec | Nhom sinh ra | Ky thuat kiem thu |
|---|---|---|
| `endpoints[].params[].partitions[]` | `DOM` | Equivalence Partitioning, BVA, Decision Table |
| `state_machine.transitions[]` | `STA` | State Transition Testing (0-switch) |
| `security[]` | `SEC` | Security Testing theo SEC-01..SEC-07 |
| `schema_cases[]` | `SCH` | JSON Schema Validation |

Dinh dang day du: xem `spec/_SCHEMA.md`.

**He qua thiet ke quan trong:** vi bon truc tach roi nhau, bo sinh chay duoc tung vong doc lap
(`--only DOM`, `--only STA`, `--only SEC`, `--only SCH`). Do chinh la co so ky thuat de STEP 2
tuan thu yeu cau *"drive it step by step, not with a single generic prompt"* cua de bai.

## 3. Do phu hien tai cua ba file spec

```
$ python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py --spec spec/api-N.json --stats
```

| API | DOM | STA | SEC | SCH | **Tong** | Tham so chua phu | Ma SEC chua phu | O state machine da phu |
|---|---|---|---|---|---|---|---|---|
| API-1 | 36 | 9 | 13 | 6 | **64** | (khong) | (du 7) | 9 / 9 |
| API-2 | 41 | 20 | 14 | 6 | **81** | (khong) | (du 7) | 20 / 25 |
| API-3 | 51 | 9 | 14 | 6 | **80** | (khong) | (du 7) | 9 / 16 |

Nguong toi thieu cua de bai la **35 case/API**; ca ba deu vuot xa. Cac o state machine con
thieu deu la o **tu chuyen ve chinh no** (`pending -> pending`, ...) — se duoc bo sung o
STEP 4 (extend) vi day dung la loai case AI hay bo sot.

## 4. Hai loi that trong bo sinh test da duoc sua o buoc nay

Chay thu bo sinh lan dau cho ket qua bat thuong: API-1 khai bao 6 truong hop schema nhung chi
sinh ra **1**, va khai bao 9 chuyen trang thai nhung chi sinh ra **5**. Truy nguyen ve ham
`dedup()`:

```python
key = (r["Method"], r["Endpoint"], r["Request_Body"], str(r["Expected_Status"]))
```

Khoa nay coi hai test case la trung nhau khi chung **gui cung mot request**, bat ke chung
**khang dinh dieu gi**. Hai hau qua:

1. Mot case `SCH` ("response 200 cua forgot-password khop schema `{message: string}`") va mot
   case `DOM` ("email hop le tra 200") gui y het nhau nhung kiem hai thu khac han. Case `SCH`
   bi nuot.
2. Hai case `STA` "huy don dang `pending`" va "huy don dang `confirmed`" cung goi
   `PUT /api/orders/:id/cancel` voi body rong; chung chi khac nhau o **trang thai ban dau**.
   Case thu hai bi nuot.

Da sua khoa dedup thanh:

```python
key = (r["Category"], r["Method"], r["Endpoint"], r["Request_Body"],
       str(r["Expected_Status"]), r["Expected_Assertions"], r["Preconditions"])
```

Ket qua: API-1 tu 52 -> **64** case, API-2 tu 67 -> **81**, API-3 tu 72 -> **80**; do phu state
machine cua API-2 tu 11/25 len **20/25**. Day la vi du cu the cho thay **cong cu tu dong cung
can duoc kiem thu** — neu tin ngay con so dau tien thi da bao cao thieu 26 test case va mot do
phu state machine sai.

Loi thu hai: bang `SEC_DEFAULT_ASSERT` trong bo sinh van dien assertion theo **bang SEC suy
dien sai** da phat hien o STEP 0 (vi du `SEC-05` sinh ra assertion "tra 403; hanh dong admin
KHONG duoc thuc hien", trong khi SEC-05 that la "truy van CSDL phai dung Parameterized
Query"). Da viet lai toan bo bang theo `eshop-sut/README.md` muc 9.

## 5. Cac du lieu khong ton tai da bi loai khoi spec

`spec/api-2.json` tham chieu ba ma giam gia **khong he ton tai** trong `database.js`. Neu giu
nguyen, moi test coupon deu roi vao nhanh "ma khong ton tai" va **that bai vi ly do sai** —
tuc la test van do nhung khong con kiem dung thu can kiem.

| Trong spec (sai) | Trong `database.js` (that) | Da xu ly |
|---|---|---|
| `PERC10` — percent 10%, min 100000 | `SAVE10` — percent 10, min **300000** | doi ten + doi nguong BVA 99999/100000/100001 -> **299999/300000/300001** |
| `FIX50K` — fixed 50000 | `BIGBUY` — fixed 50000, min **500000** | doi ten |
| `INACTIVE` — ma bi vo hieu hoa | **khong ton tai** | xem duoi |

`valid_body` cua `apply-coupon` cung dung `total_amount: 200000`, thap hon nguong that
300000 cua `SAVE10`, nen **moi** case coupon se bi tu choi ngay tu dieu kien C3 va khong bao
gio cham toi cong thuc giam gia. Da nang len `500000` de thoa nguong cua ca `SAVE10` lan `BIGBUY`.

### Gioi han da ghi nhan: khong kiem duoc dieu kien C1 "ma bi vo hieu hoa"

SRS FR-09 dieu kien C1 doi ma phai `is_active = 1`. Nhung:

- `database.js` seed **4 ma va ca 4 deu co `is_active = 1`**;
- `POST /api/admin/coupons` **khong nhan** tham so `is_active` (cot nay mac dinh `1` o tang DB),
  nen khong the tao ma bi vo hieu hoa qua API.

Ket luan: nhanh `is_active = 0` **khong the kiem duoc qua API** neu khong dung `sqlite3` CLI
tac dong truc tiep vao CSDL. Da thay dong T4 cua bang quyet dinh bang mot dong khac co gia tri
that: `VIP100` (fixed 100000, min 300000, **max 2 luot/user**) — dong nay kiem dieu kien C5
(han muc su dung), la dieu kien duy nhat trong 5 dieu kien chua co case rieng. Gioi han nay
duoc ghi lai trong bao cao chinh thay vi giau di bang mot test luon pass.

## 6. Ket luan STEP 1

- Ba file spec hop le, tong **225 test case** se duoc sinh ra o STEP 2 (vuot xa nguong 105).
- Do phu: du 7 ma SEC cho ca 3 API, khong tham so nao bi bo sot, state machine API-2 dat 20/25.
- Da sua **2 loi that trong bo sinh test** va **3 tham chieu du lieu khong ton tai** trong spec.
- **STEP ke tiep:** STEP 2 — sinh test case theo 4 vong rieng biet (DOM, STA, SEC, SCH).
