# STEP 6 — Thuc thi bang Postman + Newman

> HW06 — API Testing | SV **Ninh Van Khai — 23127060** | De bai muc 6.4

Moi con so trong tai lieu nay duoc sinh tu `newman/*.json` bang
`agent-skill/eshop-api-23127060/scripts/summarize_newman.py`. Khong con so nao duoc go tay.

---

## 1. Bo test day du (Oracle = SPEC)

Day la ket qua kiem thu that su: moi ky vong deu viet theo dac ta, nen cac case phoi bay
bug cua SUT **se that bai** — do la muc dich cua chung.

| API | Case | Case PASS | Case FAIL | Assertion | Assertion FAIL | Thoi gian | Bao cao HTML |
|---|---|---|---|---|---|---|---|
| API-1 | 70 | 33 | 37 | 328 | 51 | 3.0s | `newman/23127060_API-1_20260901-151823.html` |
| API-2 | 87 | 34 | 53 | 413 | 78 | 3.6s | `newman/23127060_API-2_20260901-151831.html` |
| API-3 | 86 | 17 | 69 | 405 | 105 | 6.0s | `newman/23127060_API-3_20260901-151839.html` |
| **Tong** | **243** | **84** | **159** | **1146** | **234** | | |

Ty le case PASS: **35%** (84/243). Ty le assertion PASS: **80%** (912/1146).

## 2. Phan loai case that bai

| API | FAIL tong | Co chu dich (`@bug`) | Ngoai du kien (`@contract`) |
|---|---|---|---|
| API-1 | 37 | 18 | 19 |
| API-2 | 53 | 25 | 28 |
| API-3 | 69 | 48 | 21 |

## 3. Bug duoc phoi bay, theo ma bug

| Ma bug | So case that bai phoi bay no | API |
|---|---|---|
| **A-01** | 2 | API-1 |
| **A-02** | 1 | API-1 |
| **A-03** | 2 | API-1 |
| **A-04** | 1 | API-1 |
| **A-05** | 5 | API-1 |
| **A-06** | 2 | API-1 |
| **A-07** | 4 | API-1 |
| **A-09** | 1 | API-1 |
| **B-01** | 3 | API-2 |
| **B-02** | 2 | API-2 |
| **B-03** | 2 | API-2 |
| **B-04** | 2 | API-2 |
| **B-05** | 2 | API-2 |
| **B-06** | 1 | API-2 |
| **B-07** | 5 | API-2 |
| **B-09** | 2 | API-2 |
| **B-10** | 1 | API-2 |
| **B-11** | 1 | API-2 |
| **B-12** | 3 | API-2 |
| **C-01** | 8 | API-3 |
| **C-02** | 7 | API-3 |
| **C-03** | 3 | API-3 |
| **C-04** | 3 | API-3 |
| **C-05** | 3 | API-3 |
| **C-06** | 9 | API-3 |
| **C-07** | 2 | API-3 |
| **C-08** | 3 | API-3 |
| **C-10** | 2 | API-3 |
| **C-11** | 3 | API-3 |
| **C-12** | 4 | API-3 |
| **X-01** | 3 | API-1, API-2, API-3 |

## 4. That bai ngoai du kien — phai ra soat tung cai

Day la cac case gan `@contract` (nghia la luc thiet ke toi nghi SUT dap ung duoc) nhung
van that bai. Moi dong o day hoac la **mot bug chua co trong danh sach bug da biet**,
hoac la **mot ky vong sai cua chinh test case**. Khong duoc bo qua.

### API-1 — 19 case

| TC_ID | Tieu de | Thong bao that bai dau tien |
|---|---|---|
| `TC-A1-DOM-003` | POST /api/forgot-password \| email =  (email rong) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-004` | POST /api/forgot-password \| email = <thieu key> (thieu key email) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-005` | POST /api/forgot-password \| email = - (email null) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-006` | POST /api/forgot-password \| email = 12345 (email sai kieu (number)) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-007` | POST /api/forgot-password \| email = abc@@test (email sai dinh dang) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-008` | POST /api/forgot-password \| email = aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-009` | POST /api/forgot-password \| email = API.VICTIM.23127060@TEST.LOCAL (em | expected response to have status code 200 but got 404 |
| `TC-A1-DOM-010` | POST /api/forgot-password \| email =   api.victim.23127060@test.local   | expected response to have status code 200 but got 404 |
| `TC-A1-DOM-011` | POST /api/forgot-password \| email = ["a@b.c"] (email la array) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-027` | POST /api/reset-password \| newPassword = <thieu key> (thieu newPasswor | expected response to have status code 400 but got 200 |
| `TC-A1-DOM-028` | POST /api/reset-password \| newPassword = - (newPassword null) | expected response to have status code 400 but got 200 |
| `TC-A1-DOM-034` | POST /api/reset-password \| newPassword = <script>alert(1)</script> (pa | expected response to have status code 400 but got 200 |
| `TC-A1-DOM-036` | POST /api/reset-password \| newPassword = A1!aaaaaaaaaaaaaaaaaaaaaaaaaa | expected response to have status code 400 but got 200 |
| `TC-A1-SCH-002` | Response loi cua forgot-password khop schema { error: string } | expected response to have status code 400 but got 404 |
| `TC-A1-SEC-001` | [SEC-05] SQLi qua truong email cua forgot-password | expected response to have status code 400 but got 404 |
| `TC-A1-SEC-009` | [SEC-04] Email chua payload XSS phai bi tu choi hoac escape | expected response to have status code 400 but got 404 |
| `TC-A1-SEC-010` | [SEC-04] Path traversal trong email khong duoc gay loi 500 | expected response to have status code 400 but got 404 |
| `TC-A1-SEC-013` | [SEC-07] Xin OTP lan 2 thi OTP lan 1 phai bi vo hieu hoa | expected response to have status code 400 but got 200 |
| `TC-A1-STA-006` | Chuyen trang thai USED -> USED (dung lai OTP da dung - KHONG hop le) | expected response to have status code 400 but got 200 |

### API-2 — 28 case

| TC_ID | Tieu de | Thong bao that bai dau tien |
|---|---|---|
| `TC-B2-DOM-001` | POST /api/checkout \| total_amount = 200000 (tong tien khop voi gio han | expected response to have status code 201 but got 200 |
| `TC-B2-DOM-005` | POST /api/checkout \| total_amount = 200000 (tong tien sai kieu (string | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-006` | POST /api/checkout \| total_amount = <thieu key> (thieu total_amount) | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-007` | POST /api/checkout \| total_amount = - (total_amount null) | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-008` | POST /api/checkout \| total_amount = 999999999999999 (BVA - tong tien v | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-009` | POST /api/checkout \| total_amount = 200000.999 (tong tien co phan thap | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-012` | POST /api/checkout \| items = [{"product_id":1,"quantity":0}] (BVA - so | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-013` | POST /api/checkout \| items = [{"product_id":1,"quantity":-5}] (so luon | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-014` | POST /api/checkout \| items = [{"product_id":1,"quantity":1}] (BVA - so | expected response to have status code 201 but got 200 |
| `TC-B2-DOM-015` | POST /api/checkout \| items = [{"product_id":999999,"quantity":1}] (san | expected response to have status code 404 but got 200 |
| `TC-B2-DOM-016` | POST /api/checkout \| items = [{"product_id":1,"quantity":100000}] (vuo | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-017` | POST /api/checkout \| items = khong-phai-array (items sai kieu) | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-018` | POST /api/checkout \| shipping_address = 123 Nguyen Van Cu, Q5, TP.HCM  | expected response to have status code 201 but got 200 |
| `TC-B2-DOM-022` | POST /api/checkout \| shipping_address = <script>alert('23127060')</scr | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-023` | POST /api/checkout \| shipping_address = A123456789A123456789A123456789 | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-025` | POST /api/apply-coupon \| code = BIGBUY (Decision table T2 - ma so tien | expected response to have status code 200 but got 400 |
| `TC-B2-DOM-031` | POST /api/apply-coupon \| code = ' OR '1'='1 (SQLi trong ma giam gia) | expected response to have status code 400 but got 404 |
| `TC-B2-DOM-032` | POST /api/apply-coupon \| code = perc10 (ma viet thuong - hanh vi phai  | expected response to have status code 200 but got 404 |
| `TC-B2-DOM-035` | POST /api/apply-coupon \| total_amount = 300001 (BVA - tren min_order_a | expected data to satisfy schema but found following errors:  data.discount_amount should b |
| `TC-B2-DOM-038` | POST /api/apply-coupon \| user_id = {{userId}} (user_id cua chinh minh) | expected data to satisfy schema but found following errors:  data.discount_amount should b |
| `TC-B2-SCH-001` | Response 201 cua checkout khop schema { orderId: integer, message: str | expected response to have status code 201 but got 200 |
| `TC-B2-SCH-002` | Response loi cua checkout khop schema { error: string } | expected response to have status code 400 but got 200 |
| `TC-B2-SEC-001` | [SEC-05] SQLi qua ma giam gia | expected response to have status code 400 but got 404 |
| `TC-B2-SEC-002` | [-] Response checkout khong duoc lo thong tin noi bo | expected response to have status code 201 but got 200 |
| `TC-B2-SEC-008` | [SEC-02] Huy don hang cua nguoi khac | expected response to have status code 403 but got 404 |
| `TC-B2-SEC-010` | [SEC-03] User thuong xem toan bo don hang qua GET /api/admin/orders | expected response to have status code 403 but got 200 |
| `TC-B2-SEC-011` | [SEC-04] XSS trong shipping_address phai bi chan hoac escape | expected response to have status code 400 but got 200 |
| `TC-B2-SEC-012` | [-] Gui kem status='delivered' khi checkout | expected response to have status code 201 but got 200 |

### API-3 — 21 case

| TC_ID | Tieu de | Thong bao that bai dau tien |
|---|---|---|
| `TC-C3-DOM-006` | POST /api/products \| name = A (BVA - 1 ky tu (duoi bien toi thieu)) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-007` | POST /api/products \| name = A123456789A123456789A123456789A123456789 ( | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-008` | POST /api/products \| name = A123456789A123456789A123456789A123456789 ( | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-010` | POST /api/products \| name = San pham tieng Viet co dau 23127060 (ten c | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-011` | POST /api/products \| price = 150000 (gia hop le) | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-014` | POST /api/products \| price = 1 (BVA - gia 1 (bien duoi hop le)) | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-018` | POST /api/products \| price = 999999999999999 (BVA - gia vuot gioi han) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-019` | POST /api/products \| price = 150000.55 (gia co phan thap phan) | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-023` | POST /api/products \| category_id = abc (category_id sai kieu) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-024` | POST /api/products \| category_id = - (category_id null (khong bat buoc | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-026` | POST /api/products \| imageUrl = javascript:alert('23127060') (URL sche | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-027` | POST /api/products \| imageUrl = ../../etc/passwd (path traversal trong | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-028` | POST /api/products \| imageUrl = khong-phai-url (chuoi khong phai URL) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-029` | PUT /api/products/:id \| id = 1 (id ton tai) | expected data to satisfy schema but found following errors:  data should NOT have addition |
| `TC-C3-DOM-031` | PUT /api/products/:id \| id = 0 (BVA - id = 0) | expected response to have status code 404 but got 200 |
| `TC-C3-DOM-032` | PUT /api/products/:id \| id = -1 (id am) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-033` | PUT /api/products/:id \| id = abc (id khong phai so) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-034` | PUT /api/products/:id \| id = 1%20OR%201=1 (SQLi trong path param) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-036` | PUT /api/products/:id \| description = Mo ta moi 23127060 (cap nhat mo  | expected data to satisfy schema but found following errors:  data should NOT have addition |
| `TC-C3-DOM-043` | GET /api/products \| search =  (tu khoa rong - tra ve tat ca) | expected data to satisfy schema but found following errors:  data[7].name should be string |
| `TC-C3-SEC-013` | [-] Gui kem truong id de ghi de khoa chinh | expected response to have status code 400 but got 200 |

## 5. Bo hoi quy (`@contract`) — lan chay all-pass cho CI

Bo nay gom cac test case ma SUT **hien dang dap ung**, duoc chot tu ket qua chay that
bang `derive_contract.py`. No khong khang dinh 'API nay dung', ma khang dinh 'nhung dieu
API nay dang lam dung thi khong duoc pha'. Day la lan chay duoc dung cho yeu cau
'all API test cases passing' cua de bai muc 6.

| API | Case | Assertion | Assertion FAIL | Bao cao HTML |
|---|---|---|---|---|
| API-1 | 33 | 163 | **0** | `newman/23127060_API-1_contract_20260901-151940.html` |
| API-2 | 34 | 164 | **0** | `newman/23127060_API-2_contract_20260901-151946.html` |
| API-3 | 17 | 79 | **0** | `newman/23127060_API-3_contract_20260901-151952.html` |
| **Tong** | **84** | **406** | **0** | |

## 6. Lan chay data-driven (Postman Collection Runner / `newman -d`)

| Bo | Data file | Vong lap | Request | Assertion | Assertion FAIL |
|---|---|---|---|---|---|
| DD1 Brute force OTP | `postman/data/brute_force_tokens.csv` | 20 | 40 | 40 | 20 |
| DD2 Bang chuyen trang thai FR-10 | `postman/data/state_transitions.csv` | 17 | 70 | 34 | 1 |
| DD3 Lam dung han muc coupon | `postman/data/coupon_abuse.csv` | 4 | 7 | 8 | 2 |
| DD4 Dau vao khong hop le POST /api/products | `postman/data/product_invalid.csv` | 7 | 20 | 14 | 7 |

