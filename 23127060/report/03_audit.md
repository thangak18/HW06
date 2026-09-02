# STEP 3 — Audit test case do AI sinh (VALID / INVALID / INCOMPLETE)

> HW06 — API Testing | SV **Ninh Van Khai — 23127060** | De bai muc 6.2

De bai: *"Label each AI-generated test case VALID / INVALID / INCOMPLETE with reasoning, and
correct the invalid or incomplete ones. You are fully responsible for the final test cases."*

---

## 1. Cach lam: luat viet ra giay, khong sua tay tung dong

225 test case ma sua tay tung dong thi khong tai lap duoc va khong ai kiem chung duoc. Vi vay
moi nhan o day deu den tu **mot luat viet ro rang**, moi luat bam vao **mot cau cu the trong
`eshop-sut/README.md`**. Luat nam trong
`agent-skill/eshop-api-23127060/scripts/audit_testcases.py`; chay lai luon ra dung ket qua nay:

```bash
python3 agent-skill/eshop-api-23127060/scripts/audit_testcases.py --report
```

Phan doi hoi phan doan rieng cho tung case — chu yeu la **gan lai ma SEC** va **viet lai
nhung case co ky vong khong can cu** — nam trong hai bang `SEC_REMAP` va `REWRITE`, moi dong
kem ly do bang van xuoi. Do la phan "human review" that su; script chi lam viec ap dung nhat quan.

## 2. Ket qua tong hop

| API | Tong | VALID | INVALID | INCOMPLETE | % VALID |
|---|---|---|---|---|---|
| API-1 (FR-03) | 64 | 22 | 23 | 19 | 34% |
| API-2 (FR-08) | 81 | 40 | 18 | 23 | 49% |
| API-3 (FR-15) | 80 | 21 | 27 | 32 | 26% |
| **Tong** | **225** | **83** | **68** | **74** | **37%** |

Theo nhom ky thuat — cho thay ro loi tap trung o dau:

| Nhom | Tong | VALID | INVALID | INCOMPLETE | Nhan xet |
|---|---|---|---|---|---|
| DOM | 128 | 33 | 23 | 72 | Phan hoach mien lam tot; diem yeu la assertion qua chung chung |
| STA | 38 | 34 | 4 | 0 | **Nhom tot nhat.** Bang chuyen trang thai buoc AI phai bam vao dac ta |
| SEC | 41 | **0** | **41** | 0 | **Toan bo nhom sai.** Xem muc 4 |
| SCH | 18 | 16 | 0 | 2 | Ky vong ve hinh dang response de doi chieu, it sai |

So lan tung luat duoc kich hoat (mot case co the dinh hai luat):

| Luat | Noi dung | So case |
|---|---|---|
| R3 | Gan sai ma SEC | 61 |
| R7 | Case tu choi thao tac GHI nhung khong chung minh thao tac da khong xay ra | 50 |
| R8 | Case thanh cong nhung chi kiem schema, khong kiem gia tri that su duoc luu | 17 |
| R6 | Ky vong dua tren suy dien, khong phai dieu SRS phat bieu | 5 |
| R1 | Ky vong 429 (rate limiting) khong co can cu trong SRS | 4 |
| R2 | Ky vong 409 (conflict) khong co can cu trong SRS | 2 |
| R4 | Mau thuan noi tai (danh dau "hop le" nhung ky vong 4xx) | 2 |
| R10 | Dung bien Postman nhung precondition khong noi bien duoc dat o dau | 2 |
| R5 | Tham so bia (`?debug=true`) | 1 |
| R3b | Ap mot chinh sach ma dac ta khong he co | 1 |

> Ty le VALID 37% thap hon khoang 55-70% ma `references/TESTCASE_TAXONOMY.md` du kien. Con so
> nay **khong duoc dieu chinh cho dep**. Nguyen nhan la cu the va truy nguyen duoc: mot gia dinh
> sai duy nhat (bang SEC) da lam hong tron ven mot nhom 41 case, va assertion mac dinh cua bo
> sinh qua chung chung nen keo theo 67 case vao nhom INCOMPLETE. Ha thap tieu chuan de con so
> dep hon se dung nghia la audit hoi hot — dung dieu ma taxonomy canh bao.

## 3. Bon nguyen nhan goc

| # | Nguyen nhan | Hau qua | So case |
|---|---|---|---|
| N1 | **Mot gia dinh sai lan ra ca nhom.** Bang SEC-01..07 duoc suy dien theo OWASP thay vi doc `README.md` muc 9 | 61 case bi gan sai ma bao mat | 61 |
| N2 | **Bo sinh dien assertion mac dinh chung chung.** "body la JSON; co truong error" khong noi gi ve tac dung phu | 67 case thieu phan quan trong nhat cua phep kiem | 67 |
| N3 | **AI ap chuan nganh thay vi doc dac ta.** Rate limiting, rang buoc khoa ngoai, cam dung lai mat khau cu — deu la thoi quen tot nhung SRS khong he yeu cau | 7 case ky vong sai han | 7 |
| N4 | **AI bia ra thu khong ton tai** de lap day mo hinh: tham so `?debug=true`, trang thai `EXPIRED` / `IN_SEARCH` / `LOGIN_OLD` | 4 case khong the chay hoac chay ma khong chung minh gi | 4 |

## 4. Phat hien nghiem trong nhat: **toan bo 41 case SEC deu INVALID**

Day khong phai 41 loi doc lap ma la **mot loi duy nhat nhan ban 41 lan**.

Bang SEC-01..07 dung de gan nhan duoc suy ra tu ten cac lo hong OWASP quen thuoc
(SEC-01 = SQL Injection, SEC-04 = IDOR, SEC-05 = role escalation, SEC-07 = brute force). Bang
SEC **that** nam trong `eshop-sut/README.md` muc 9 va noi nhung dieu hoan toan khac:

| Ma | Suy dien (sai) | That (SRS muc 9) |
|---|---|---|
| SEC-01 | Chong SQL Injection | Mat khau **khong** duoc luu plaintext |
| SEC-02 | Khong lo du lieu nhay cam | API bao mat phai yeu cau JWT hop le |
| SEC-03 | Endpoint ghi phai xac thuc | API Admin phai kiem `role='admin'` |
| SEC-04 | Chong IDOR | Du lieu user nhap phai duoc escape khi hien thi |
| SEC-05 | Chong role escalation | Truy van CSDL phai dung Parameterized Query |
| SEC-06 | Validate input / chong XSS | API cap nhat ho so khong duoc cho doi `role` |
| SEC-07 | Chong brute force | OTP >= 6 chu so, co thoi han, vo hieu hoa sau khi dung |

Ket qua doi chieu tung case: **39/41 case bi gan sai ma**, 2 case con lai dung ma nhung ky
vong 429 khong co can cu. Vi vay nhom SEC co 0 case VALID.

**Vi sao dieu nay nghiem trong hon no thoat nhin:** cac test case **van chay dung** — mot phep
thu SQL Injection van la mot phep thu SQL Injection du no bi dan nhan SEC-01 hay SEC-05. Cai
hong la **bang do phu bao mat trong bao cao**. Neu nop ban chua sua, bao cao se ghi "API-3 da
phu SEC-01 voi 8 test case" trong khi SEC-01 (mat khau plaintext) **khong he duoc kiem o
API-3 dong nao**. Do la mot khang dinh sai ve pham vi kiem thu — dung loai sai lam ma nguoi
doc bao cao khong the tu phat hien.

**Vi sao AI khong tu bat duoc:** ma `SEC-01` la mot **nhan khong tu giai thich**. Trong ngu canh
kiem thu API, "SEC-01" gan nhu luon la SQL Injection; do la mo hinh manh nhat va AI dien vao
ma khong thay can kiem lai. Tai lieu chua bang that (`README.md` cua SUT) lai co ten khien
nguoi ta tuong la file gioi thieu repo, trong khi file mang ten `api_specification.md` — cai
ten nghe co ve la "dac ta" — thi **khong he chua bang SEC nao**. Chi mot lenh
`grep -n "SEC-0" README.md` da lam sang to moi chuyen.

### Vi du chi tiet 1 — `TC-B2-SEC-006`

| | |
|---|---|
| **Case goc** | `[SEC-04] Xem don hang cua nguoi khac qua GET /api/orders/:id`, `SEC_Ref = SEC-04` |
| **Nhan** | INVALID |
| **Ly do** | SEC-04 that la "du lieu user nhap phai duoc escape khi hien thi", khong lien quan gi den truy cap trai phep. Loi that o day la `GET /api/orders/:id` **thieu han middleware `authenticateToken`** — dung la dieu SEC-02 quy dinh. |
| **Da sua** | `SEC_Ref` -> `SEC-02`; dong bo lai tien to trong `Title` thanh `[SEC-02]`. Kich ban, request va ky vong 403 giu nguyen vi chung von da dung. |

### Vi du chi tiet 2 — `TC-C3-SEC-010`, `TC-C3-SEC-011`

| | |
|---|---|
| **Case goc** | `[SEC-05] User thuong (role=user) tao/xoa san pham`, `SEC_Ref = SEC-05` |
| **Nhan** | INVALID |
| **Ly do** | Day dung la kiem tra phan quyen, nhung ma dung phai la **SEC-03** ("API Admin phai kiem `role='admin'`, khong chi kiem su ton tai cua token"). SEC-05 that la parameterized query. |
| **Da sua** | `SEC_Ref` -> `SEC-03`. Nho vay bang do phu moi phan anh dung: SEC-03 duoc kiem 3 lan o API-3, va SEC-05 (SQLi) duoc kiem 8 lan — truoc khi sua thi hai con so nay bi hoan doi cho nhau. |

## 5. Ky vong khong co can cu trong dac ta (luat R1, R2, R3b)

Day la loai loi kho thay nhat, vi test case **doc rat hop ly**.

### Vi du chi tiet 3 — `TC-A1-SEC-011` (ky vong 429)

| | |
|---|---|
| **Case goc** | "Do 20 gia tri token 4 chu so lien tiep phai bi chan", `Expected_Status = 429` |
| **Nhan** | INVALID |
| **Ly do** | **Khong mot dong nao** trong FR-01..FR-24 hay SEC-01..SEC-07 yeu cau rate limiting. AI suy ra tu thoi quen bao mat chung. Neu giu nguyen, case nay se FAIL va bi ghi vao bao cao nhu mot "bug" — trong khi SUT khong he vi pham dac ta nao ca. **Bao cao mot bug khong ton tai con te hon la bo sot mot bug that.** |
| **Da sua** | Giu nguyen kich ban do 20 gia tri (no van la cach chung minh entropy yeu), nhung doi oracle sang dieu SEC-07 **thuc su** noi: OTP phai dai toi thieu 6 chu so. `Expected_Status` -> 400; assertion moi: *"moi lan do deu tra 400; do dai `resetToken` lay tu forgot-password phai >= 6 ky tu theo SEC-07"*. Bay gio case FAIL vi mot ly do co that: SUT sinh token 4 chu so. |

### Vi du chi tiet 4 — `TC-C3-DOM-041` (ky vong 409)

| | |
|---|---|
| **Case goc** | "DELETE san pham dang nam trong don hang — phai chan", `Expected_Status = 409` |
| **Nhan** | INVALID |
| **Ly do** | SRS FR-15 chi noi "Admin co the Them / Xem / Sua / Xoa san pham". Khong co bat ky rang buoc khoa ngoai nao giua `products` va `orders`; ban than `database.js` cung khong khai bao `FOREIGN KEY`. AI ap kinh nghiem thiet ke CSDL len mot he thong khong co rang buoc do. |
| **Da sua** | `Expected_Status` -> 200. Chuyen trong tam sang dieu **kiem duoc**: sau khi xoa thi `GET /api/products/1` khong duoc tra ve san pham nua — va chinh phep kiem nay phoi bay bug C-04 (tra `200 {}` thay vi `404`). `Bug_Ref` -> `C-08`. |

### Vi du chi tiet 5 — `TC-A1-DOM-035`

| | |
|---|---|
| **Case goc** | "Dat lai dung mat khau cu phai bi tu choi", `Expected_Status = 400` |
| **Nhan** | INVALID |
| **Ly do** | SRS FR-01/FR-03 chi doi mat khau moi **thoa dieu kien do manh**; khong o dau cam dat lai trung mat khau cu. AI ap mot chinh sach bao mat pho bien ma dac ta khong co. |
| **Da sua** | `Expected_Status` -> 200, kem khang dinh dang nhap bang mat khau do phai thanh cong. |

## 6. Mau thuan noi tai va thu bia ra (luat R4, R5)

### Vi du chi tiet 6 — `TC-A1-STA-006`

| | |
|---|---|
| **Case goc** | "Chuyen trang thai ISSUED -> EXPIRED **(hop le)**" nhung `Expected_Status = 400` |
| **Nhan** | INVALID |
| **Ly do** | Hai loi chong nhau. Thu nhat, tu mau thuan: danh dau chuyen hop le ma lai ky vong bi tu choi. Thu hai, `EXPIRED` **khong phai mot trang thai dieu khien duoc**: SUT khong luu thoi diem cap OTP (bug A-04), nen khong co cach nao dua OTP ve trang thai het han qua API. Case nay khong the chay. |
| **Da sua** | Doi thanh chuyen **KHONG hop le** `USED -> USED`: dung lai OTP da dung. Day la dieu SEC-07 quy dinh ro ("vo hieu hoa sau khi dung") va kiem duoc hoan toan qua API. Precondition duoc viet lai cho khop. |

### Vi du chi tiet 7 — `TC-C3-SEC-004`

| | |
|---|---|
| **Case goc** | "Response san pham khong lo truong noi bo khi bat co debug", `GET /api/products/1?debug=true` |
| **Nhan** | INVALID |
| **Ly do** | Tham so `debug` **khong ton tai** — khong co trong `api_specification.md` lan trong `server.js`. Express bo qua query param la, nen case nay se **PASS** trong moi tinh huong va khong chung minh dieu gi. Mot test luon pass vi ly do sai con nguy hiem hon mot test that bai, vi no tao cam giac an toan gia. |
| **Da sua** | Bo tham so bia. Kiem dung dieu kiem duoc: *"body chi duoc chua dung 6 truong `id`, `name`, `price`, `description`, `imageUrl`, `category_id`"*. |

## 7. Nhom INCOMPLETE: 67 case thieu phan quan trong nhat (luat R7, R8)

### Vi du chi tiet 8 — mau chung cua 50 case dinh luat R7

| | |
|---|---|
| **Case goc** | `POST /api/products` voi `price = -100`, `Expected_Status = 400`, assertion: *"body la JSON; co truong error"* |
| **Nhan** | INCOMPLETE |
| **Ly do** | Case chi kiem **cau tra loi**, khong kiem **hau qua**. Mot API tra `400` roi **van INSERT** vao CSDL se pass case nay. Ma do dung la kieu loi dang co trong SUT: `PUT /api/products/:id` voi id khong ton tai tra `200 "Product updated"` du khong dong nao bi doi (bug C-07). |
| **Da sua** | Bo sung ve sau cua assertion: *"VA doc lai tai nguyen sau khi goi de xac nhan du lieu KHONG bi thay doi"*. Trong Postman, phan nay duoc hien thuc bang mot `pm.sendRequest` doc lai `GET /api/products` va dem so ban ghi truoc/sau. |
| **Pham vi** | Luat R7 chi ap dung cho endpoint co **tac dung phu quan sat duoc** (`/api/products`, `/api/checkout`, `/api/orders/...`, `/api/users/me`, `/api/reset-password`, `/api/categories`, `/api/admin/*`). Khong ap cho `/api/apply-coupon` (thuan tinh toan, khong ghi gi) va `/api/forgot-password` (co ghi nhung tren nhanh loi khong co gi doc lai duoc). Doi hoi mot phep kiem khong ton tai se lam nhan INCOMPLETE mat y nghia. |

### Vi du chi tiet 9 — mau chung cua 17 case dinh luat R8

| | |
|---|---|
| **Case goc** | `POST /api/checkout` voi du lieu hop le, `Expected_Status = 201`, assertion: *"body la JSON; khop schema thanh cong"* |
| **Nhan** | INCOMPLETE |
| **Ly do** | Kiem hinh dang response ma khong kiem **gia tri that su duoc luu**. Case nay se pass ke ca khi SUT luu sai tong tien — dung bug B-01: `checkout` nhan `total_amount` do client gui va ghi thang vao CSDL. |
| **Da sua** | Bo sung: *"VA doc lai tai nguyen de xac nhan gia tri luu dung bang gia tri da gui"* — voi checkout la `GET /api/orders/:id` roi so `total_amount`. |

## 8. Do phu SEC sau khi gan lai — va mot gioi han duoc thua nhan

| API | Ma SEC duoc kiem | Ma khong ap dung | Ly do |
|---|---|---|---|
| API-1 | SEC-01(1), SEC-04(3), SEC-05(3), SEC-06(1), SEC-07(6) | SEC-02, SEC-03 | `forgot-password` va `reset-password` **khong yeu cau xac thuc theo dung dac ta** (nguoi quen mat khau thi lam gi con token). Khong co endpoint admin nao trong pham vi API-1. |
| API-2 | SEC-02(7), SEC-03(3), SEC-04(2), SEC-05(2), SEC-06(1) | SEC-01, SEC-07 | Luong thanh toan khong dung toi luu tru mat khau lan OTP. |
| API-3 | SEC-02(4), SEC-03(3), SEC-04(5), SEC-05(8), SEC-06(1) | SEC-01, SEC-07 | Nhu tren. |
| **Toan suite** | **SEC-01(1), SEC-02(11), SEC-03(6), SEC-04(10), SEC-05(13), SEC-06(3), SEC-07(6)** | **(khong thieu ma nao)** | |

`references/TESTCASE_TAXONOMY.md` do chinh toi viet co mot dong: *"Bat buoc phu du 7 ma
SEC-01..SEC-07 cho **moi** API"*. Sau khi biet bang SEC that, **yeu cau do la bat kha thi va
chinh no la nguyen nhan gay hai**: no ep phai tim cho ra mot case SEC-07 o API-3, va cach
duy nhat de "dat chi tieu" la gan bua mot case rate-limit vao ma SEC-07. Yeu cau dung phai la:
**du 7 ma tren toan bo suite**, va tung API phu nhung ma **thuc su ap dung duoc**, co giai trinh
cho phan khong ap dung. Da sua lai taxonomy theo huong nay.

Day la mot bai hoc doc lap voi SUT: **mot chi tieu do luong dat sai se tao ra chinh cai loi
ma no dinh ngan chan.**

## 9. Ket luan STEP 3

- 225 case duoc gan nhan bang 10 luat viet ro rang, tai lap duoc bang mot lenh.
- 68 case INVALID va 74 case INCOMPLETE **da duoc sua ngay trong `testcases/API-*_audited.csv`**,
  moi dong deu co cot `Audit_Note` ghi ly do va noi ro da sua gi.
- Phat hien lon nhat: **toan bo nhom SEC (41 case) deu sai**, do mot gia dinh duy nhat ve bang
  SEC-01..07. Do phu bao mat sau khi sua da phan anh dung thuc te.
- **Cong viec cua human (H2):** doc lai cot `Audit_Note`, dac biet 68 dong INVALID, va xac nhan
  hoac bac bo tung nhan truoc khi nop.
- **STEP ke tiep:** STEP 4 — bo sung >= 5 case/API ma AI bo sot.
