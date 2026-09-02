# STEP 5 — Cac tinh nang Postman da su dung

> HW06 — API Testing | SV **Ninh Van Khai — 23127060** | De bai muc 6

De bai: *"Exercise as many Postman features as you reasonably can... List the Postman
features you used in your report."*

---

## 1. Bang tong hop

Cot **Bang chung** ghi ro file hoac thao tac nao chung minh tinh nang do da duoc dung that.

| # | Tinh nang | Dung vao viec gi trong bai nay | Bang chung |
|---|---|---|---|
| 1 | **Collection** | 7 collection: 3 bo day du, 3 bo hoi quy `@contract`, 1 bo data-driven | `postman/collections/*.json` |
| 2 | **Folder trong collection** | Moi collection chia 5 folder: `_setup` + 4 nhom ky thuat DOM / STA / SEC / SCH | cau truc `item[]` trong file collection |
| 3 | **Environment** | `23127060_local` voi 26 bien | `postman/environments/23127060_local.postman_environment.json` |
| 4 | **Bien moi truong** | `{{baseUrl}}`, `{{token_user}}`, `{{token_admin}}`, `{{token_attacker}}`, `{{orderId}}`, `{{resetToken}}`, `{{newProductId}}`... | dung xuyen suot request va script |
| 5 | **Bien collection** | Cac JSON Schema duoc nap thanh bien `schema_product`, `schema_order`, `schema_error`... | `variable[]` trong collection |
| 6 | **Pre-request script cap collection** | Chen header `X-Student-Id` + `console.log` cho **moi** request | 823/823 request mang header — `ci/evidence/header_evidence.md` |
| 7 | **Pre-request script cap request** | Dua he thong ve dung precondition cua tung case: tao don hang roi day ve trang thai `shipping`, xin OTP moi, dem so ban ghi truoc khi goi | `event[listen=prerequest]` cua tung item |
| 8 | **Tests script cap collection** | Hai phep kiem ap cho moi response: thoi gian phan hoi, ma trang thai hop le | `event[listen=test]` cap collection |
| 9 | **Tests script cap request** | 1146 assertion cho 243 test case | `newman/*.json.gz` |
| 10 | **JSON Schema validation** (`pm.response.to.have.jsonSchema`) | 13 schema, dung `additionalProperties: false` de bat truong thua va `exclusiveMinimum` de bat gia tri sai | `postman/scripts/schemas/*.json` |
| 11 | **`pm.sendRequest`** | Doc lai tai nguyen sau khi goi (kiem tac dung phu), tao tai khoan cach ly, day trang thai don hang | ~90 lan goi trong cac script |
| 12 | **Data-driven run** (Collection Runner + data file) | 4 bo, 48 vong lap, 4 file CSV | `postman/data/*.csv`, `newman/23127060_DD-*` |
| 13 | **`pm.iterationData`** | Doc gia tri tung dong cua data file trong script | folder `DD1`–`DD4` |
| 14 | **Newman CLI** | Chay tu dong toan bo, dung trong CI | `agent-skill/.../run_newman.sh` |
| 15 | **Reporter `htmlextra`** | Bao cao HTML, co `--reporter-htmlextra-logs` de giu lai `console.log` | `newman/*.html` |
| 16 | **Reporter `json`** | Dau vao cho cac script tong hop va kiem chung | `newman/*.json.gz` |
| 17 | **`--folder`** | Chay rieng tung folder voi data file rieng cua no | `run_datadriven.sh` |
| 18 | **`--export-environment`** | Chuyen token tu lan chay `_setup` sang lan chay data-driven | `run_datadriven.sh` |
| 19 | **`--env-var`** | Ghi de `baseUrl` va `studentId` tu dong lenh (CI dung) | workflow GitHub Actions |
| 20 | **Postman Console** | Doc dong `[HW06][23127060] ...` de chup man hinh lam bang chung | **HUMAN H4** — xem muc 4 |
| 21 | **Mock server** | Doi chieu hop dong API theo dac ta voi hanh vi thuc te | **HUMAN** — xem muc 5 |
| 22 | **Monitor** | Chay bo `@contract` dinh ky | **HUMAN** — xem muc 5 |
| 23 | **Workspace** | Workspace ca nhan `HW06-23127060` chua 7 collection + 1 environment | **HUMAN** — xem muc 5 |

**Tong: 23 tinh nang, trong do 19 tinh nang co bang chung tu dong kiem chung duoc.**
Bon tinh nang con lai (20–23) can thao tac tren giao dien Postman va tai khoan Postman.

## 2. Cau truc collection

```
23127060_HW06_API-3
├── _setup - chuan bi du lieu va token
│   ├── 00 Dang ky user nan nhan
│   ├── 01 Dang ky user tan cong
│   ├── 02 Login nan nhan       -> token_user, userId
│   ├── 03 Login ke tan cong    -> token_attacker, attackerId
│   ├── 04 Login admin          -> token_admin, adminId
│   ├── 05 Tao san pham vat thu -> newProductId
│   └── 06 Dem so san pham ban dau
├── DOM - Domain partition        (53 request)
├── STA - State transition        (9 request)
├── SEC - Security SEC-01..07     (16 request)
└── SCH - Schema validation       (8 request)
```

Folder `_setup` chay dau tien va dat toan bo bien ma cac folder sau can. Nho vay collection
chay duoc tu con so khong tren mot CSDL vua seed lai, khong doi thao tac tay nao.

## 3. Hai quyet dinh ky thuat dang ghi lai

### 3.1 Khong dat phep kiem "khong lo password" o cap collection

`references/POSTMAN_GUIDE.md` ban dau de nghi dat ba phep kiem chung o cap collection, trong
do co *"khong lo truong nhay cam"* va *"Content-Type la application/json"*. Da **bo** hai phep
kiem do khoi cap collection.

Ly do: chung that bai o mot so request — nhung do la bug **A-07** (login tra ve ca `password`)
va **C-03** (loi SQL tra ve HTML). Neu de o cap collection, moi bug se bi dem lai **hang chuc
lan**, moi lan mot request, va so lieu `failed` trong bao cao Newman se noi ve so luong bug
gap nhieu lan su that. Hai bug do da co test case rieng phoi bay chung dung mot lan moi cai.

Bai hoc: **mot phep kiem chi nen dat o cap collection khi no dung voi moi request.** Dat mot
phep kiem cua tinh huong cu the len cap collection lam hong phep dem, chu khong lam tang do phu.

### 3.2 Cach ly tai khoan cho cac case dang nhap

SUT co bug **A-09**: moi lan dang nhap sai cong **+2** vao `login_attempts` va khoa 180 giay
khi dat 3. Hau qua khi chay Newman: chi can **mot** case thu mat khau sai la tai khoan
`api.victim` bi khoa, va **moi** case dang nhap chay sau do deu tra 403 — ke ca nhung case
hoan toan khong lien quan. Lan chay dau tien co dung hien tuong nay: 7 case that bai day chuyen
tu mot nguyen nhan duy nhat.

Khong co endpoint nao mo khoa, va cho 180 giay trong CI la khong chap nhan duoc. Giai phap:
tam collection cach ly — 8 case dung `/api/login` **tu tao mot tai khoan rieng** trong
pre-request script, roi tu dua tai khoan do ve dung trang thai minh can (`fresh`, `fail2`,
`reset`, `fail2_then_reset`). Xem bang `ISOLATED` trong `build_collection.py`.

Day la viec cua **tang thuc thi**, khong phai cua thiet ke test case, nen no duoc xu ly trong
bo dung collection chu khong sua vao file CSV test case.

## 4. Bang chung header `X-Student-Id` (de bai muc 11)

Header duoc chen o pre-request script cap **collection**, nen khong request nao co the thieu:

```javascript
const STUDENT_ID = pm.environment.get("studentId") || "23127060";
pm.request.headers.upsert({ key: "X-Student-Id", value: STUDENT_ID });
pm.request.headers.upsert({ key: "Accept", value: "application/json" });

console.log(
  "[HW06][" + STUDENT_ID + "] " +
  pm.request.method + " " + pm.request.url.toString() +
  " | X-Student-Id=" + STUDENT_ID +
  " | " + new Date().toISOString()
);
```

Bang chung duoc thu o **hai muc**:

1. **Kiem chung tu dong** — `scripts/verify_header.py` doc thang phan `request.header` ma
   Newman ghi lai cho tung request that su roi len duong:
   **823/823 request mang `X-Student-Id: 23127060`, khong request nao thieu.**
   Ket qua o `ci/evidence/header_evidence.md`.
2. **Anh chup man hinh** — dong `console.log` tren xuat hien trong bao cao HTML (nho
   `--reporter-htmlextra-logs`) va trong Postman Console.

> Mot dong `console.log` chi chung minh **script da chay**, chua chung minh **header da duoc
> gui**. Vi vay cach thu nhat moi la bang chung that; anh chup Console nop kem cho dung yeu
> cau hinh thuc cua de bai.

### HUMAN H4 — cach chup man hinh Postman Console

1. Mo Postman → import `postman/collections/23127060_HW06_API-1.postman_collection.json`
   va `postman/environments/23127060_local.postman_environment.json`.
2. Chon environment `23127060_local` o goc tren ben phai.
3. Mo Console: **View → Show Postman Console** (hoac `Ctrl+Alt+C`).
4. Chay bat ky request nao trong folder `DOM`.
5. Trong Console, mo rong muc `Request Headers` cua request vua chay — phai thay dong
   `X-Student-Id: 23127060`, kem dong log `[HW06][23127060] POST ... | X-Student-Id=23127060`.
6. Chup toan man hinh (phai thay ro ca dong header lan dong log) →
   luu vao `bugs/screenshots/console_header.png`.

## 5. Bon tinh nang can thao tac tren giao dien Postman (HUMAN)

### H4a — Workspace
Tao workspace ca nhan ten `HW06-23127060`, import ca 7 collection va environment vao do.
Chup man hinh danh sach collection → `ci/evidence/postman_workspace.png`.

### H4b — Mock server
1. Trong Postman: **New → Mock Server**, chon collection `23127060_HW06_API-3`.
2. Them mot example cho `GET /api/products/2` voi body **dung dac ta**:
   `{"id":2,"name":"Samsung Galaxy S24 Ultra","price":28000000,...}` — chu y `price` la **so**.
3. Chay cung mot test case ve schema len ca mock server va len SUT that.
   Mock **pass**, SUT that **fail** — do chinh la bug **C-05** (`price` bi ep thanh chuoi voi id chan).
4. Chup man hinh hai ket qua canh nhau → `ci/evidence/postman_mock.png`.

> Y nghia: mock server o day khong dung de thay the SUT, ma de **hien thuc hoa hop dong API
> theo dac ta**. Su khac nhau giua mock va SUT chinh la bug, va do la cach dung mock server
> co gia tri nhat trong bai nay.

### H4c — Monitor
1. **New → Monitor**, chon collection `23127060_HW06_API-1_contract` va environment `23127060_local`.
2. Dat lich 1 lan/ngay.
3. Luu y: monitor cua Postman chay tren may chu cua Postman nen **khong goi duoc `localhost`**.
   Muon monitor that su chay thi phai dua SUT ra dia chi cong khai (vi du bang ngrok). Neu
   khong lam duoc thi chup man hinh cau hinh monitor va **ghi ro han che nay trong bao cao** —
   khong duoc bao la da chay thanh cong.
4. Chup man hinh → `ci/evidence/postman_monitor.png`.

### H4d — Visualizer (tuy chon)
Them vao tests script cua mot request bat ky doan `pm.visualizer.set(template, data)` de ve
bang tong hop ket qua, roi chup tab **Visualize**.
