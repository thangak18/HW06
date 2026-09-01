# BAO CAO HW06 — API TESTING

**Ho ten:** Ninh Van Khai — **MSSV:** 23127060
**Mon:** Kiem thu phan mem | **Bai:** HW06 — API Testing
**SUT:** EShop — https://github.com/ttbhanh/eshop-sut, commit `85af3ba875c88283615e22cb108f13e2fccaf0e9`
**Ngay lam:** 01/09/2026

| | |
|---|---|
| Repo GitHub cong khai | `<dien link sau khi push — xem ci/CI_CD_REPORT.md muc 5>` |
| GitHub Issues | `<dien link>` |
| Video demo bo sinh (YouTube, tuy chon) | `<dien link — kich ban o agent-skill/VIDEO_SCRIPT.md>` |
| Tu danh gia | **`<dien 3 chu so>`** / 100 |

---

## Muc luc

1. [Moi truong thuc nghiem](#1-moi-truong-thuc-nghiem)
2. [Lua chon 3 API](#2-lua-chon-3-api)
3. [Sinh test case bang AI — bon vong rieng biet](#3-sinh-test-case-bang-ai--bon-vong-rieng-biet)
4. [Audit ket qua AI](#4-audit-ket-qua-ai)
5. [Test case tu bo sung](#5-test-case-tu-bo-sung)
6. [Thuc thi bang Postman + Newman](#6-thuc-thi-bang-postman--newman)
7. [Cac tinh nang Postman da dung](#7-cac-tinh-nang-postman-da-dung)
8. [Bug report](#8-bug-report)
9. [CI/CD](#9-cicd)
10. [Thiet ke bo sinh test bang AI](#10-thiet-ke-bo-sinh-test-bang-ai)
11. [Nhung dieu con lai cua sinh vien](#11-nhung-dieu-con-lai-cua-sinh-vien)
12. [Phu luc](#12-phu-luc)

---

## 1. Moi truong thuc nghiem

| Hang muc | Gia tri |
|---|---|
| He dieu hanh | Linux 6.18.33.2 (WSL2 tren Windows) |
| Node.js / npm | v20.20.2 / 10.8.2 |
| Newman | 6.2.2 + `newman-reporter-htmlextra` |
| Python | 3.13.5 (cac script sinh test, tong hop bao cao) |
| Base URL | `http://localhost:3000` — thoa yeu cau chong gian lan cua de bai muc 11 |
| SUT | Node.js + Express + SQLite, commit `85af3ba` |

Chi tiet day du va cach khoi dong lai SUT: [`report/00_environment.md`](00_environment.md).

### Mot chi tiet ky thuat quyet dinh toan bo quy trinh chay

`backend/database.js` goi `initDatabase()` **ngay khi module duoc `require`**, va ham do bat
dau bang mot loat `DROP TABLE`. Nghia la **moi lan khoi dong lai backend la toan bo CSDL bi
xoa va seed lai**.

Dieu nay bien thanh mot rang buoc bat buoc: **phai khoi dong lai backend truoc moi collection**.
Ly do khong phai de cho sach ma vi SUT co bug **A-09** — moi lan dang nhap sai cong `+2` vao bo
dem va khoa tai khoan 180 giay khi dat 3. Chay collection thu hai tren CSDL cu thi tai khoan
test da bi khoa, va hang loat test se that bai vi mot ly do khong lien quan gi den chat luong
API. Lan chay dau tien o may cuc bo dinh dung loi nay: **7 test case that bai day chuyen tu mot
nguyen nhan duy nhat**.

### Xac dinh oracle: hai tai lieu, vai tro khac han nhau

| Tai lieu | Vai tro thuc su | Lam oracle? |
|---|---|---|
| `eshop-sut/README.md` | **SRS** — tu tuyen bo "mo ta yeu cau nghiep vu **dung**". Chua FR-01..FR-24 va bang SEC-01..07 | **CO — oracle `SPEC`** |
| `eshop-sut/api_specification.md` | Huong dan goi API: endpoint, body mau. Khong mo ta rang buoc nghiep vu | Chi lay hinh dang request/response |
| `eshop-sut/backend/server.js` | Hanh vi thuc te | Oracle `IMPL`, dung cho test hoi quy |

Xac dinh dung vai tro nay la viec quan trong nhat cua buoc chuan bi, vi no quyet dinh moi
`Expected_Status` ve sau. Vi du dien hinh: `api_specification.md` in response mau cua
`forgot-password` la `"resetToken": "123456"` (6 chu so), `README.md` doi **toi thieu 6 chu so**,
con code that sinh **4 chu so**. Ca hai tai lieu deu chong lai implementation nen day chac chan
la bug (A-02).

## 2. Lua chon 3 API

| ID | Pool | FR | Endpoint chinh | Endpoint ho tro | Ly do chon |
|---|---|---|---|---|---|
| **API-1** | A | FR-03 Quen & dat lai mat khau | `POST /api/forgot-password`, `POST /api/reset-password` | `POST /api/login`, `POST /api/register` | Luong **2 buoc co trang thai** (chua co token → da cap → da dung), nen vua co phan hoach mien vua co state machine that. Dong thoi la be mat tan cong dam dac nhat: SEC-01 va SEC-07 deu hoi tu o day |
| **API-2** | B | FR-08 Thanh toan | `POST /api/checkout` | `POST /api/apply-coupon` (FR-09), `GET /api/orders/:id`, `PUT /api/orders/:id/cancel`, `PUT /api/admin/orders/:id/status` (FR-10) | Ket hop ba thu de bai doi: tinh tien, **state machine 5 trang thai**, va phan quyen. FR-09 con cho san mot **bang quyet dinh 5 dieu kien** viet trong SRS |
| **API-3** | C | FR-15 Quan ly san pham | `POST` / `PUT` / `DELETE /api/products` | `GET /api/products`, `?search=`, `/:id` | CRUD day du nen co vong doi tai nguyen; tham so o ca **body, path va query**; va la noi duy nhat co **SQL noi chuoi** — bat buoc de phu SEC-05 |

**Pool D (Mobile) khong su dung** — de bai muc 5: *"Pool D, the mobile app, is not used here,
because this homework targets the backend API."*

**Kiem tra trung lap trong nhom:** da doc `docs/team-api-allocation.md` (chi doc). Tai thoi diem
lam bai, bang phan cong con de `TODO` o ca ba dong thanh vien nen **khong the doi chieu tu dong**.
Bo ba (FR-03, FR-08, FR-15) can duoc **xac nhan mieng voi hai thanh vien con lai truoc khi nop**.

Chi tiet: [`report/01_api_selection.md`](01_api_selection.md).

## 3. Sinh test case bang AI — bon vong rieng biet

De bai muc 6.1 cam mot prompt tong. Quy trinh o day chia thanh **bon vong doc lap**, moi vong
mot ky thuat kiem thu, moi vong mot commit rieng va mot entry AI_log rieng.

| Vong | Nhom | Ky thuat | Lenh | Ket qua | AI_log |
|---|---|---|---|---|---|
| 2a | DOM | Equivalence Partitioning, BVA, Decision Table | `gen_testcases.py --only DOM` | 128 case | #3 |
| 2b | STA | State Transition Testing (0-switch) | `--only STA --append` | 38 case | #4 |
| 2c | SEC | Anh xa SEC-01..SEC-07 | `--only SEC --append` | 41 case | #5 |
| 2d | SCH | JSON Schema Validation | `--only SCH --append` | 18 case | #6 |
| | | | | **225 case** | |

| API | DOM | STA | SEC | SCH | Tong AI sinh |
|---|---|---|---|---|---|
| API-1 (FR-03) | 36 | 9 | 13 | 6 | **64** |
| API-2 (FR-08) | 41 | 20 | 14 | 6 | **81** |
| API-3 (FR-15) | 51 | 9 | 14 | 6 | **80** |

Ca ba API deu vuot xa nguong **35 case/API** cua de bai.

**Vi sao chia duoc bon vong:** file spec may doc duoc (`spec/api-N.json`) co bon truc doc lap,
anh xa mot doi mot sang bon nhom ky thuat. Do la mot **quyet dinh thiet ke** chu khong phai
tien ich phu — xem muc 10.

Chi tiet: [`report/01_api_selection.md`](01_api_selection.md), [`spec/_SCHEMA.md`](../spec/_SCHEMA.md).

## 4. Audit ket qua AI

De bai muc 6.2 doi gan nhan **VALID / INVALID / INCOMPLETE** kem ly do, va **sua** cac case sai.

| API | Tong AI sinh | VALID | INVALID | INCOMPLETE | % VALID |
|---|---|---|---|---|---|
| API-1 | 64 | 22 | 23 | 19 | 34% |
| API-2 | 81 | 40 | 18 | 23 | 49% |
| API-3 | 80 | 21 | 27 | 32 | 26% |
| **Tong** | **225** | **83** | **68** | **74** | **37%** |

Theo nhom ky thuat — cho thay ngay loi tap trung o dau:

| Nhom | Tong | VALID | INVALID | INCOMPLETE | Nhan xet |
|---|---|---|---|---|---|
| DOM | 128 | 33 | 23 | 72 | Phan hoach mien lam tot; diem yeu la assertion qua chung chung |
| STA | 38 | 34 | 4 | 0 | **Tot nhat** — bang chuyen trang thai buoc AI phai bam vao dac ta |
| SEC | 41 | **0** | **41** | 0 | **Toan bo nhom sai** — xem duoi |
| SCH | 18 | 16 | 0 | 2 | Ky vong ve hinh dang response de doi chieu |

### Phat hien nghiem trong nhat: toan bo 41 case bao mat deu INVALID

Day khong phai 41 loi doc lap ma la **mot loi duy nhat nhan ban 41 lan**.

Bang SEC-01..07 dung de gan nhan duoc suy ra tu ten cac lo hong OWASP quen thuoc. Bang **that**
nam trong `eshop-sut/README.md` muc 9 va noi nhung dieu khac han:

| Ma | Suy dien (sai) | That (SRS muc 9) |
|---|---|---|
| SEC-01 | Chong SQL Injection | Mat khau **khong** duoc luu plaintext |
| SEC-02 | Khong lo du lieu nhay cam | API bao mat phai yeu cau JWT hop le |
| SEC-03 | Endpoint ghi phai xac thuc | API Admin phai kiem `role='admin'` |
| SEC-04 | Chong IDOR | Du lieu user nhap phai duoc escape khi hien thi |
| SEC-05 | Chong role escalation | Truy van CSDL phai dung Parameterized Query |
| SEC-06 | Validate input / chong XSS | API cap nhat ho so khong duoc cho doi `role` |
| SEC-07 | Chong brute force | OTP >= 6 chu so, co thoi han, vo hieu hoa sau khi dung |

Doi chieu tung case: **39/41 bi gan sai ma**, 2 case con lai dung ma nhung ky vong `429` khong
co can cu.

**Vi sao nghiem trong hon no thoat nhin:** cac test case **van chay dung** — mot phep thu SQL
Injection van la mot phep thu SQL Injection du bi dan nhan sai. Cai hong la **bang do phu bao
mat trong bao cao**: no se ghi *"API-3 da phu SEC-01 voi 8 test case"* trong khi SEC-01 (mat
khau plaintext) khong he duoc kiem o API-3 dong nao. Do la loai khang dinh sai ma nguoi doc bao
cao khong the tu phat hien.

### Bon nguyen nhan goc

| # | Nguyen nhan | So case |
|---|---|---|
| N1 | Mot gia dinh sai lan ra ca nhom (bang SEC) | 61 |
| N2 | Bo sinh dien assertion mac dinh chung chung, khong kiem tac dung phu | 67 |
| N3 | AI ap chuan nganh thay vi doc dac ta (rate limiting, rang buoc khoa ngoai) | 7 |
| N4 | AI bia ra thu khong ton tai de lap day mo hinh (`?debug=true`, trang thai `EXPIRED`) | 4 |

> Ty le VALID **37%** thap hon khoang 55-70% du kien trong taxonomy cua chinh toi. Con so nay
> **khong duoc dieu chinh cho dep**: nguyen nhan cu the va truy nguyen duoc, va ha thap tieu
> chuan gan nhan de con so dep hon se dung nghia la audit hoi hot.

Chi tiet, kem 9 vi du truoc/sau khi sua: [`report/03_audit.md`](03_audit.md).

## 5. Test case tu bo sung

De bai muc 6.3 doi **toi thieu 5 case/API** ma AI bo sot. Da bo sung **6 case/API, tong 18**.

| Ly do bo sot | So case | Y nghia |
|---|---|---|
| **API** — dac diem cua API | **9** | Bug chi lo ra khi **ket hop nhieu request** |
| **MODEL** — gioi han mo hinh | 4 | AI suy dien tu hinh dang API thay vi doc ma nguon |
| **PROMPT** — prompt khoanh vung qua chat | 3 | Vi du: prompt chi neu 2 endpoint chinh cua FR-03 |
| **SPECGAP** — dac ta khong noi | 2 | AI khong co gi de bam vao |

**Ket qua dang chu y nhat: 9/18 thuoc nhom `API`.** Mot nua so case ma AI bo sot khong phai vi
AI kem hay prompt do, ma vi mot **gioi han cau truc**: bo sinh sinh ra test case **doc lap**,
moi case mot request; trong khi mot nua so bug nghiem trong cua he thong nay chi lo ra khi noi
nhieu request lai voi nhau.

Ba vi du:

| TC_ID | Vi sao can nhieu request |
|---|---|
| `TC-C3-SCH-901` | `{"price": 30000000}` va `{"price": "28000000"}` deu la JSON hop le. Vi pham chi hien ra khi **so sanh hai response** |
| `TC-B2-STA-901` | Dua don ve trang thai `shipping` doi hoi di qua dung hai buoc admin — chuoi 4 request |
| `TC-A1-SEC-903` | AI viet case *"sai 3 lan thi phai khoa"* (PASS). Bug nam o phia con lai cua bien: code cong `+2` nen khoa ngay o lan **thu hai**. Phai viet case khang dinh dieu **nguoc lai** moi thay |

Chi tiet: [`report/04_extend.md`](04_extend.md).

## 6. Thuc thi bang Postman + Newman

### 6.1 Bo test day du (Oracle = SPEC)

| API | Case | PASS | FAIL | Assertion | Assertion FAIL | Bao cao |
|---|---|---|---|---|---|---|
| API-1 | 70 | 33 | 37 | 328 | 51 | `newman/23127060_API-1_20260901-151823.html` |
| API-2 | 87 | 34 | 53 | 413 | 78 | `newman/23127060_API-2_20260901-151831.html` |
| API-3 | 86 | 17 | 69 | 405 | 105 | `newman/23127060_API-3_20260901-151839.html` |
| **Tong** | **243** | **84** | **159** | **1146** | **234** | |

Trong 159 case that bai: **91 case gan `@bug`** (that bai co chu dich, phoi bay bug da biet) va
**68 case gan `@contract`** (ngoai du kien). Nhom thu hai chinh la phan co gia tri nhat: no chua
nhung bug **chua co trong danh sach bug da biet** — vi du 63 case that bai vi
`forgot-password` tra `404 "User not found"` cho **moi** dau vao xau (rong, `null`, thieu key,
sai dinh dang) thay vi `400`, cho thay endpoint nay khong he validate dau vao.

### 6.2 Bo hoi quy — lan chay all-pass cho CI

| API | Case | Assertion | Assertion FAIL |
|---|---|---|---|
| API-1 | 33 | 163 | **0** |
| API-2 | 34 | 164 | **0** |
| API-3 | 17 | 79 | **0** |
| **Tong** | **84** | **406** | **0** |

Bo nay gom cac test case ma SUT **hien dang dap ung**, chot tu ket qua chay that bang
`derive_contract.py`. No **khong** khang dinh *"API nay dung"*, ma khang dinh *"nhung dieu API
nay dang lam dung thi khong duoc pha"* — mot **moc hoi quy**.

> Vi sao khong ep bo test day du phai xanh: SUT co **34 bug that**, nen bo test day du **phai
> do** — do la ket qua kiem thu dung. Ep no xanh thi chi con cach sua ky vong cho khop voi hanh
> vi sai cua SUT, tuc la **nguy tao ket qua**.

### 6.3 Lan chay data-driven

| Bo | Data file | Vong lap | Assertion | FAIL |
|---|---|---|---|---|
| DD1 Brute force OTP | `brute_force_tokens.csv` | 20 | 40 | 20 |
| DD2 Bang chuyen trang thai FR-10 | `state_transitions.csv` | 17 | 34 | 1 |
| DD3 Lam dung han muc coupon | `coupon_abuse.csv` | 4 | 8 | 2 |
| DD4 Dau vao khong hop le | `product_invalid.csv` | 7 | 14 | 7 |

### 6.4 Hai loi cua chinh bo test, tim ra va sua truoc khi chot so lieu

1. **Assertion doi nguyen van chuoi `"Invalid state transition"` o ca hai endpoint.** Endpoint
   `PUT /api/orders/:id/cancel` tu choi bang thong bao khac (`"Cannot cancel this order."`) va
   dieu do hoan toan hop le — SRS chi doi *"thong bao loi phu hop"*. Day la **loi cua test**,
   khong phai loi cua API. Da sua.
2. **`TC-C3-DOM-041` xoa san pham `id = 1`**, ma `id = 1` lai la vat co dinh ma hang chuc case
   khac dung lam moc. Xoa no o giua lan chay khien nhung case chay sau that bai vi mot ly do
   khong lien quan gi den chinh chung. Da doi sang san pham thu do `_setup` tao rieng.

Chi tiet: [`report/06_execution.md`](06_execution.md).

## 7. Cac tinh nang Postman da dung

**23 tinh nang**, trong do **19 co bang chung tu dong kiem chung duoc**. Bang day du:
[`report/05_postman_features.md`](05_postman_features.md).

Noi bat: collection + folder theo nhom ky thuat, environment 26 bien, pre-request script cap
collection **va** cap request, JSON Schema validation (13 schema **thiet ke de bat bug** — vi du
khai bao `price` la `number` de bat C-05, `additionalProperties: false` de bat viec lo truong
`password`), `pm.sendRequest` (~90 lan, dung de doc lai tai nguyen kiem tac dung phu),
data-driven run, Newman CLI + `htmlextra`, `--folder`, `--export-environment`, `--env-var`.

Bon tinh nang can thao tac GUI (Workspace, Mock server, Monitor, Console) da co huong dan chi
tiet trong bao cao, danh cho sinh vien thuc hien.

### Bang chung header `X-Student-Id` (de bai muc 11)

Header duoc chen o pre-request script cap **collection** nen khong request nao co the thieu.
Bang chung duoc thu o **hai muc**:

1. **Kiem chung tu dong** — `verify_header.py` doc thang phan `request.header` ma Newman ghi lai
   cho tung request that su roi len duong: **823/823 request mang `X-Student-Id: 23127060`**.
   Ket qua: [`ci/evidence/header_evidence.md`](../ci/evidence/header_evidence.md).
2. **Anh chup Postman Console** — dong `console.log("[HW06][23127060] ...")` xuat hien trong
   bao cao HTML (nho `--reporter-htmlextra-logs`) va trong Console.

> Mot dong `console.log` chi chung minh **script da chay**, chua chung minh **header da duoc
> gui**. Vi vay cach thu nhat moi la bang chung that; anh chup Console nop kem cho dung yeu cau
> hinh thuc cua de bai.

## 8. Bug report

**34 bug**, tat ca deu **tai hien duoc bang request that**: **12 Critical, 11 High, 9 Medium, 2 Low**.

| API | So bug |
|---|---|
| API-1 (FR-03) | 7 |
| API-2 (FR-08) | 13 |
| API-3 (FR-15) | 13 |
| Lien API | 1 |

De bai doi toi thieu 3 bug/API; ca ba deu vuot xa.

Request va response trong bao cao **khong duoc go tay**: chung duoc trich thang tu
`bugs/evidence/<ID>.md`, la ket qua cua mot lan chay that bang `capture_bug_evidence.py`.

### Muoi hai bug Critical

| ID | Tieu de | API | Vi pham |
|---|---|---|---|
| **A-01** | `forgot-password` tra thang ma OTP trong response body | API-1 | SEC-07 |
| **A-07** | Mat khau luu plaintext va bi tra ve trong response `login` / `users/me` | API-1 | SEC-01 |
| **B-01** | `checkout` tin tuyet doi `total_amount` do client gui | API-2 | FR-08 |
| **B-01b** | `checkout` chap nhan `total_amount` am | API-2 | FR-08 |
| **B-02** | `GET /api/orders/:id` thieu han xac thuc — IDOR | API-2 | SEC-02 |
| **B-03** | `PUT /api/admin/orders/:id/status` khong kiem `role` | API-2 | SEC-03 |
| **B-05** | Cong thuc giam gia `percent` sai dau, cho ra so tien giam **am** | API-2 | FR-09 |
| **B-07** | `apply-coupon` khong xac thuc; bo `user_id` la bo qua kiem tra han muc | API-2 | SEC-02 |
| **C-01** | `POST`/`PUT`/`DELETE /api/products` hoan toan khong xac thuc | API-3 | SEC-02, SEC-03 |
| **C-02** | SQL Injection qua `?search=` | API-3 | SEC-05 |
| **C-13** | Mot san pham co `price = null` lam **sap han backend** | API-3 | FR-15 |
| **X-01** | `PUT /api/users/me` cho user thuong tu nang `role` len `admin` | lien API | SEC-06 |

### Hai bug dang noi rieng

**C-02 — SQL Injection lay duoc thong tin dang nhap cua quan tri vien.** Lan chay thu nghiem voi
payload `UNION SELECT id,email,password,role,1,1 FROM users--` tra ve nguyen van:

```json
[{"id":1,"name":"admin@eshop.com","price":"Admin123!","description":"admin",...}, ...]
```

Ket hop voi A-07 (mat khau luu plaintext), **mot request duy nhat** lay duoc mat khau quan tri.

**C-13 — bug tu choi dich vu, va la bug tu tim ra trong luc thu bang chung.** No la **he qua
day chuyen cua ba bug khac**, khong bug nao trong so do tu no gay sap:

1. **C-01** cho phep goi `PUT /api/products/:id` **khong can token**.
2. **C-09**: mot `PUT` thieu truong ghi de `price` thanh `null`.
3. **C-05**: `GET /api/products/:id` chay `row.price.toString()` khi id la so **chan**.

`TypeError` nem ra trong callback cua `sqlite3` khong duoc ai bat → tien trinh Node **thoat
han** → toan bo API ngung phuc vu. Bang chung: request tiep theo tra `Connection refused`, va
moi kich ban chay sau do khong chay duoc nua cho toi khi khoi dong lai may chu. **Mot nguoi
hoan toan khong dang nhap ha guc duoc ca he thong bang hai request.**

Bug nay minh hoa mot dieu ma kiem thu tung endpoint doc lap khong bao gio thay: **rui ro nam o
to hop, khong nam o tung thanh phan**.

Chi tiet 34 bug: [`bugs/BUG_REPORT.md`](../bugs/BUG_REPORT.md). Bang chung:
[`bugs/evidence/`](../bugs/evidence/). File san sang dan len GitHub Issues:
[`bugs/ISSUE_TEMPLATES/`](../bugs/ISSUE_TEMPLATES/).

## 9. CI/CD

Pipeline: **GitHub Actions**, file `.github/workflows/api-tests-23127060.yml`.

Cac buoc: checkout → Node 20 → cai Newman → clone SUT va **`git checkout 85af3ba`** (ghim commit)
→ cai dependency → chay 3 collection (**khoi dong lai backend truoc moi collection**) → tong hop
ket qua vao Job Summary → **kiem chung header `X-Student-Id` ngay trong pipeline** → upload
artifact.

Hai che do: `contract` (ky vong xanh) va `full` (ky vong do — SUT co 34 bug that).

Ca hai kich ban da duoc **kiem chung tren may cuc bo** truoc khi bao cao:

| Kich ban | Ket qua do duoc | Bang chung |
|---|---|---|
| Lan chay PASS | 406 assertion, **0 that bai**, exit code 0 | `ci/evidence/local_ci_run_pass.log` |
| Lan chay FAIL | 406 assertion, **dung 1 that bai**, newman exit code **1** | `ci/evidence/local_ci_run_fail.log` |

Lan chay FAIL duoc tao bang `ci/inject_failing_test.py --apply`, doi ky vong ma trang thai cua
`TC-A1-DOM-012` tu 200 thanh 201, va tra lai duoc bang `--revert`.

> **Chua day ma len GitHub.** Remote hien tai la `https://github.com/thangak18/HW06.git` —
> khong phai tai khoan cua sinh vien. Day ma vao repo cua nguoi khac phai duoc chinh chu dong y
> truoc. Quy trinh 6 buoc de sinh vien tu thuc hien da viet san.

Chi tiet: [`ci/CI_CD_REPORT.md`](../ci/CI_CD_REPORT.md).

## 10. Thiet ke bo sinh test bang AI

### Kien truc: tach lam hai lop

| Lop | Ai lam | San pham | Tinh chat |
|---|---|---|---|
| **Tri thuc** | Con nguoi + AI | `spec/api-N.json` | Doi hoi doc hieu; quyet dinh chat luong |
| **Sinh** | May | `testcases/API-N_generated.csv` | **Tat dinh** — cung dau vao luon cho cung dau ra |

AI khong duoc phep "sang tac" test case; no chi giup **dich dac ta van xuoi sang cau truc co
truc phan hoach ro rang**. Tu do tro di la mot chuong trinh tat dinh. Loi ich cu the: khi mot
test case sai, truy nguoc duoc ngay ve **dong nao trong file spec** gay ra no.

```
PARSE → NORMALISE → 4 BO SINH SONG SONG → KHU_TRUNG → DANH_SO → KIEM_TRA_DO_PHU → EMIT
                                                                       |
                                        (chua du do phu) ──────────────┘
```

Bon bo sinh **doc lap** nen chay duoc rieng tung cai — do chinh la co so ky thuat de thoa yeu
cau *"drive it step by step"* cua de bai.

### Hai loi that trong chinh bo sinh

**1. Khoa khu trung nuot mat 34 test case.** Khoa ban dau la
`(Method, Endpoint, Request_Body, Expected_Status)` — coi hai case la trung nhau khi chung gui
cung mot request, **bat ke chung khang dinh dieu gi**. Hau qua: API-1 khai bao 6 case schema chi
sinh ra 1; 9 chuyen trang thai chi sinh ra 5. Sau khi bo sung `Category`,
`Expected_Assertions`, `Preconditions` vao khoa: **191 → 225 case**, do phu state machine cua
API-2 **11/25 → 20/25**.

**2. Bang `SEC_DEFAULT_ASSERT` duoc dien tu tri nho** — xem muc 4.

> Bai hoc: **cong cu tu dong cung phai duoc kiem thu.** Neu tin ngay con so dau tien thi bao cao
> da ghi thieu 34 test case va mot do phu sai.

### Han che lon nhat va huong mo rong

Ca bon bo sinh deu theo mot khuon: mot vong lap tren mot danh sach khai bao, moi phan tu cho ra
**mot** test case, **mot** request. Do la gioi han **cau truc**. So lieu do duoc: **9/18** case
con nguoi phai bo sung thuoc nhom *"bug chi lo ra khi ket hop nhieu request"*.

Huong mo rong: bo sung truc thu nam `scenarios[]` khai bao **chuoi** request kem khang dinh
`cross_step` lien ket cac buoc — chuyen tu **0-switch** sang **n-switch coverage**.

**So do:** `agent-skill/diagram/23127060_generator_diagram.png` — **do sinh vien tu ve** theo de
bai muc 11. Mo ta de ve: [`agent-skill/diagram/DIAGRAM_BRIEF.md`](../agent-skill/diagram/DIAGRAM_BRIEF.md).
**Pseudocode:** [`agent-skill/pseudocode/generator.pseudo.md`](../agent-skill/pseudocode/generator.pseudo.md).
**Ban hien thuc:** `agent-skill/eshop-api-23127060/scripts/gen_testcases.py`.
Chi tiet: [`report/07_test_generator_design.md`](07_test_generator_design.md).

## 11. Nhung dieu con lai cua sinh vien

Cac hang muc duoi day **bat buoc phai do sinh vien tu lam**, vi chung doi hoi thao tac tren
giao dien, quyen truy cap tai khoan, hoac vi de bai cam AI lam.

| Ma | Cong viec | Da chuan bi san gi | Vi sao AI khong lam duoc |
|---|---|---|---|
| **H1** | **Ve so do** bo sinh test | `agent-skill/diagram/DIAGRAM_BRIEF.md` (182 dong mo ta) | De bai muc 11 cam so do do AI sinh |
| **H2** | Doc lai va chot 68 nhan `INVALID` | Cot `Audit_Note` da ghi ly do tung dong | Sinh vien chiu trach nhiem cuoi cung ve test case |
| **H3** | Mo **GitHub Issues** cho tung bug + chup man hinh | 34 file trong `bugs/ISSUE_TEMPLATES/` san sang dan | Can quyen ghi tren GitHub |
| **H4** | Chup man hinh **Postman Console** co header | Huong dan 6 buoc trong `report/05_postman_features.md` | Can thao tac GUI |
| **H5** | Day ma, chay **2 lan CI**, chup man hinh, lay link | Workflow + `inject_failing_test.py` + quy trinh 6 buoc | Remote la repo cua nguoi khac |
| **H6** | **Mock server** va **Monitor** tren Postman | Huong dan chi tiet, kem canh bao Monitor khong goi duoc `localhost` | Can tai khoan Postman |
| **H7** | Quay **video demo** (khuyen khich) | `agent-skill/VIDEO_SCRIPT.md` kich ban 6 phut | — |
| **H8** | Danh dau `human-verified` trong AI_log | `ai_log.py verify --id N --status yes` | Chi sinh vien xac nhan duoc |
| **H9** | Xuat PDF, dat ten zip, nop Moodle | `validate_submission.py` bao con thieu gi | — |

## 12. Phu luc

| Phu luc | Noi dung | File |
|---|---|---|
| A | **AI Audit Report** — 13 luot tuong tac, day du prompt goc va output | [`ai/audit/AI_AUDIT_REPORT.md`](../ai/audit/AI_AUDIT_REPORT.md) |
| B | **AI Critique** (299 tu) | [`ai/critique/AI_CRITIQUE.md`](../ai/critique/AI_CRITIQUE.md) |
| C | Nhat ky AI theo thoi gian thuc | [`ai/AI_log.md`](../ai/AI_log.md) |
| D | Prompt goc cua tung buoc | [`ai/prompts/`](../ai/prompts/) |
| E | Test case dang Excel (3 sheet + Summary) | [`testcases/23127060_HW06_testcases.xlsx`](../testcases/23127060_HW06_testcases.xlsx) |
| F | Git commit log | [`git-log/23127060_git_commit_log.txt`](../git-log/23127060_git_commit_log.txt) |
| G | Bang chung header chong gian lan | [`ci/evidence/header_evidence.md`](../ci/evidence/header_evidence.md) |

### Tuyen bo su dung AI (de bai muc 9)

**I use AI tools for the following tasks.**

Cong cu: **Claude Code (`claude-opus-5`)**. Toan bo **13 luot tuong tac** duoc ghi lai **tu dong
ngay tai thoi diem xay ra** bang `scripts/ai_log.py`, khong viet lai tu tri nho. Moi luot luu
day du prompt goc va tom tat output.

Cac so lieu passed/failed **khong** do AI uoc luong ma tinh tu `newman/*.json` that qua
`summarize_newman.py`. So do bo sinh test do **sinh vien tu ve**, khong do AI sinh (de bai muc 11).
