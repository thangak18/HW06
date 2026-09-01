# STEP 4 — Test case tu bo sung (nhung gi AI bo sot)

> HW06 — API Testing | SV **Ninh Van Khai — 23127060** | De bai muc 6.3

De bai: *"Add at least five test cases of your own that the AI missed — especially around
security and state transitions — and explain why the AI missed them (prompt quality, model
limitations, or characteristics of the API)."*

Yeu cau toi thieu 5 case/API. Da bo sung **6 case/API, tong 18 case**, tat ca deu
`Source = HUMAN` va deu co cot `Why_AI_Missed` giai trinh bang van xuoi.

---

## 1. Tong hop sau khi bo sung

| API | Tong | AI sinh | Tu bo sung | DOM | STA | SEC | SCH | `@contract` | `@bug` |
|---|---|---|---|---|---|---|---|---|---|
| API-1 (FR-03) | 70 | 64 | 6 | 36 | 10 | 18 | 6 | 47 | 23 |
| API-2 (FR-08) | 87 | 81 | 6 | 43 | 22 | 16 | 6 | 58 | 29 |
| API-3 (FR-15) | 86 | 80 | 6 | 53 | 9 | 16 | 8 | 35 | 51 |
| **Tong** | **243** | **225** | **18** | 132 | 41 | 50 | 20 | 140 | 103 |

Phan bo ly do AI bo sot:

| Ly do | So case | Y nghia |
|---|---|---|
| **API** — dac diem cua API | 9 | Bug chi lo ra khi **ket hop nhieu request**; bo sinh lam viec tren tung case doc lap |
| **MODEL** — gioi han mo hinh | 4 | AI suy dien tu ten / hinh dang API thay vi doc ma nguon |
| **PROMPT** — chat luong prompt | 3 | Prompt khoanh vung qua chat, khong yeu cau ro dieu do |
| **SPECGAP** — dac ta khong noi | 2 | Dac ta khong mo ta hanh vi nay nen AI khong co gi de bam vao |

**Ket qua dang chu y nhat: 9/18 case thuoc nhom `API`.** Nua so case ma AI bo sot khong phai
vi AI kem hay vi prompt do, ma vi mot **gioi han cau truc**: bo sinh sinh ra cac test case
**doc lap**, trong khi mot nua so bug nghiem trong cua he thong nay chi lo ra khi **noi hai
hay nhieu request lai voi nhau**. Do la ket luan quan trong nhat cua buoc nay.

## 2. Do phu SEC sau khi bo sung

| API | Ma SEC duoc kiem | Khong ap dung | Giai trinh |
|---|---|---|---|
| API-1 | SEC-01(2), SEC-03(1), SEC-04(3), SEC-05(3), SEC-06(1), SEC-07(7) | SEC-02 | Ca hai endpoint chinh cua FR-03 **khong yeu cau xac thuc theo dung dac ta** — nguoi quen mat khau thi khong con token de ma gui |
| API-2 | SEC-02(8), SEC-03(3), SEC-04(2), SEC-05(2), SEC-06(1) | SEC-01, SEC-07 | Luong thanh toan khong dung toi luu tru mat khau lan OTP |
| API-3 | SEC-02(5), SEC-03(3), SEC-04(5), SEC-05(9), SEC-06(1) | SEC-01, SEC-07 | Nhu tren |
| **Toan suite** | **SEC-01(2), SEC-02(13), SEC-03(7), SEC-04(10), SEC-05(14), SEC-06(3), SEC-07(7)** | **(khong thieu ma nao)** | |

`TC-A1-SEC-904` da lap day khoang trong SEC-03 cua API-1 (truoc do la 0) bang mot kich ban co
that: `GET /api/admin/users` tra ve `login_attempts` va `locked_until` cua **moi nguoi dung**,
cho phep do xem tai khoan nao dang bi khoa — dung la thong tin ma ke tan cong luong quen mat
khau can.

## 3. Sau case cua API-1 (FR-03)

| TC_ID | Tieu de | Nhom | Bug | Ly do AI bo sot |
|---|---|---|---|---|
| `TC-A1-STA-901` | Sau reset, mat khau **cu** phai het hieu luc va mat khau **moi** phai dang nhap duoc | STA | — | **API** |
| `TC-A1-SEC-901` | Reset thanh cong nhung tai khoan **van bi khoa** | SEC | A-06 | **API** |
| `TC-A1-SEC-902` | `GET /api/users/me` tra ve ca `password` lan `reset_token` | SEC-01 | A-07 | **PROMPT** |
| `TC-A1-SEC-903` | Tai khoan bi khoa ngay sau **hai** lan sai, trong khi SRS quy dinh ba | SEC | A-09 | **MODEL** |
| `TC-A1-SEC-904` | User thuong doc duoc toan bo bang `users` qua `GET /api/admin/users` | SEC-03 | X-01 | **PROMPT** |
| `TC-A1-SEC-905` | OTP cua nguoi nay dung duoc cho email nguoi kia neu trung gia tri | SEC-07 | A-02 | **SPECGAP** |

### `TC-A1-SEC-903` — vi du dien hinh cua gioi han mo hinh

SRS FR-02 viet: *"Neu dang nhap sai tu **3 lan tro len** lien tiep, tai khoan bi tam khoa."*
Bo sinh doc cau nay va sinh dung case tuong ung: sai 3 lan roi kiem xem da khoa chua. Case do
**PASS** — vi sai 3 lan thi tat nhien la da khoa.

Bug nam o **phia con lai cua bien**. Code cong `login_attempts + 2` moi lan sai, nen khoa ngay
tu lan sai thu **hai**. Muon thay phai viet mot case khang dinh dieu nguoc lai: *"sau dung hai
lan sai, dang nhap bang mat khau **dung** van phai thanh cong"*.

Day la mot thoi quen co he thong cua AI: no viet case **khang dinh** dieu dac ta noi, chu rat
it khi viet case **phu dinh** dieu dac ta khong noi. Ma bien gioi cua mot yeu cau thi luon co
hai phia.

### `TC-A1-SEC-905` — khi dac ta co ve day du nhung van ho

Dac ta noi *"OTP chi hop le cho email da yeu cau"*, va cau lenh cua SUT co du ca hai dieu kien:

```sql
UPDATE users SET password = ?, reset_token = NULL WHERE email = ? AND reset_token = ?
```

Thoat nhin la dung. Cai dac ta **khong** noi la khong gian OTP phai du lon de hai nguoi khong
trung ma. Voi 4 chu so (9000 gia tri), chi can khoang 100 nguoi cung dang cho reset thi xac
suat co it nhat mot cap trung ma da vuot 40% (nghich ly ngay sinh). Khi do dieu kien
`email AND token` khong con bao ve duoc ai ca. AI khong co cau nao trong dac ta de bam vao nen
khong the sinh case nay — day dung la dinh nghia cua **SPECGAP**.

## 4. Sau case cua API-2 (FR-08)

| TC_ID | Tieu de | Nhom | Bug | Ly do AI bo sot |
|---|---|---|---|---|
| `TC-B2-DOM-901` | Checkout `total_amount = 1` roi **doc lai don hang** de xac nhan so tien that su duoc luu | DOM | B-01 | **API** |
| `TC-B2-DOM-902` | Sau thanh toan thanh cong, gio hang phai duoc xoa | DOM | B-13 | **PROMPT** |
| `TC-B2-STA-901` | Chuoi day du `pending -> confirmed -> shipping` roi user tu huy: buoc cuoi phai bi chan | STA | B-09 | **API** |
| `TC-B2-STA-902` | Chuyen tu `pending` sang chinh `pending` phai bi tu choi | STA | — | **MODEL** |
| `TC-B2-SEC-901` | Bo `user_id` khoi `apply-coupon` de dung ma `VIP100` qua muc cho phep | SEC-02 | B-07 | **MODEL** |
| `TC-B2-SEC-902` | `POST /api/coupon-usage` ghi nhan luot dung cho `coupon_id` khong ton tai | SEC | B-11 | **SPECGAP** |

### `TC-B2-SEC-901` — nghich ly "bo bot du lieu de duoc nhieu quyen hon"

Bo sinh coi "thieu tham so bat buoc" la mot lop khong hop le va sinh case *"thieu `user_id` ->
phai tra 400/401"*. Hop ly theo phan hoach mien. Nhung doc ma nguon:

```js
if (user_id) {
  db.get("SELECT COUNT(*) ... FROM coupon_usage WHERE coupon_id = ? AND user_id = ?", ...)
  // ... kiem tra han muc o day
} else {
  // ... ap ma luon, KHONG kiem tra gi
}
```

**Bo `user_id` di khong lam yeu di quyen ma lam bien mat toan bo phep kiem han muc.** Day la
kieu lo hong khong the suy ra tu hinh dang API — no chi lo ra khi doc nhanh `else`. Vi vay
case duoc viet lai thanh mot kich ban data-driven: chay 3 vong voi `VIP100` (gioi han 2
luot/nguoi) va khang dinh vong thu ba phai bi tu choi.

### `TC-B2-STA-901` — gioi han cua 0-switch coverage

Bo sinh phu bang chuyen trang thai theo **tung o rieng le** (0-switch): dat don vao mot trang
thai roi thu **mot** buoc chuyen. Nhung de dua don ve `shipping` phai di qua **dung hai buoc
admin** truoc do. Do la mot chuoi 4 request lien tiep, va bo sinh khong the tu suy ra chuoi
dan nhap tu bang trang thai — do la **1-switch / n-switch coverage**, mot muc do phu cao hon
phai thiet ke tay.

### `TC-B2-STA-902` — nam o duong cheo bi bo trong

Bang chuyen trang thai trong spec liet ke cac cap `(from, to)` **khac nhau**. Nam o duong cheo
(`pending -> pending`, `confirmed -> confirmed`, ...) bi bo trong vi truc quan chung "khong
phai mot buoc chuyen". Do phu STA cua API-2 vi the dung o **20/25**. Trong thuc te day lai la
loai o hay gay loi nhat: mot request bi gui lai hai lan do mang cham hoac nguoi dung bam hai
lan.

## 5. Sau case cua API-3 (FR-15)

| TC_ID | Tieu de | Nhom | Bug | Ly do AI bo sot |
|---|---|---|---|---|
| `TC-C3-SCH-901` | Kieu cua `price` phai giong nhau giua san pham id le va id chan | SCH | C-05 | **API** |
| `TC-C3-SEC-901` | Khach vang lai xoa duoc **toan bo catalog** roi kiem so san pham con lai | SEC-02 | C-01 | **API** |
| `TC-C3-DOM-901` | `PUT` chi gui `name`: cac truong khong gui khong duoc bi ghi de thanh `null` | DOM | C-09 | **API** |
| `TC-C3-SCH-902` | Response loi phai la `application/json`, khong duoc la HTML | SCH | C-03 | **MODEL** |
| `TC-C3-DOM-902` | Tao san pham voi `category_id` khong ton tai roi doi chieu bang danh muc | DOM | C-10 | **API** |
| `TC-C3-SEC-902` | `UNION SELECT` qua `?search` doc duoc mat khau plaintext trong bang `users` | SEC-05 | C-02 | **API** |

### `TC-C3-SCH-901` — vi pham chi ton tai giua hai response

Moi response rieng le deu hop le: `{"price": 30000000}` dung schema, va `{"price": "28000000"}`
cung la mot JSON hop le. Vi pham chi hien ra khi **so sanh hai response voi nhau**. Bo sinh
danh gia tung case doc lap nen khong co cho nao de dat mot khang dinh bac cao hon lien ket hai
request.

Chi tiet dang so: neu chi test san pham `id = 1` — dung ID ma moi vi du trong tai lieu deu
dung — thi **khong bao gio** thay bug nay.

### `TC-C3-SEC-902` — payload SQLi phai duoc trinh sat tu ma nguon

Bo sinh co sinh payload `UNION SELECT` nhung viet chung chung voi so cot tuy y. `UNION` trong
SQLite **chi chay khi so cot khop chinh xac**; doan sai so cot thi chi nhan duoc thong bao loi
va rat de ket luan nham la *"he thong da duoc bao ve"* — mot **am tinh gia**, ket qua te nhat
ma mot phep thu bao mat co the cho ra.

Payload dung phai dem chinh xac 5 cot cua bang `products` (`id`, `name`, `price`,
`description`, `imageUrl`, `category_id` — 6 cot, chon 5 cot khop kieu) roi chon dung so cot
tuong ung tu bang `users`. Do la buoc **trinh sat lay tu `database.js`**, khong the suy ra tu
dac ta.

### `TC-C3-SEC-901` — do hau qua, khong chi do ma tra ve

Bo sinh da co case *"DELETE khong token -> phai 401"* va case do **da bat duoc bug**. Nhung
mot dong `expected 401, got 200` trong bao cao khong noi len duoc muc do thiet hai. Case bo
sung nay goi DELETE cho **ca 5 san pham** ma khong kem token, roi doc lai `GET /api/products`:
neu danh sach rong thi mot nguoi hoan toan khong dang nhap vua xoa sach catalog cua cua hang.

Cung mot bug, nhung bang chung nay moi du suc thuyet phuc nguoi ra quyet dinh uu tien sua.

## 6. Ket luan STEP 4

- Da bo sung **18 case** (6/API, vuot yeu cau 5/API), tong bo test len **243 case**.
- Ly do bo sot duoc phan tich cho **tung case**, khong gop chung chung.
- Phat hien co gia tri nhat: **9/18 case thuoc nhom `API`** — bo sinh sinh test case doc lap,
  trong khi mot nua so bug nghiem trong chi lo ra khi noi nhieu request lai voi nhau. Day la
  gioi han **cau truc**, khong phai gioi han ve prompt hay ve mo hinh, va no duoc ghi thang
  vao muc "Han che va huong mo rong" cua thiet ke bo sinh (`report/07_test_generator_design.md`).
- **STEP ke tiep:** STEP 5 — dung Postman collection tu `testcases/API-*_final.csv`.
