# STEP 6 — Thực thi bằng Postman + Newman

> HW06 — API Testing | SV **Ninh Văn Khải — 23127060** | Đề bài mục 6.4

Mọi con số trong tài liệu này được sinh từ `newman/*.json` bằng
`agent-skill/eshop-api-23127060/scripts/summarize_newman.py`. Em không gõ tay con số nào.

> Cột **Tiêu đề** trong mục 4 lấy nguyên văn từ `testcases/API-*_final.csv`, và cột
> **Thông báo thất bại** là nguyên văn output của Newman — em giữ nguyên để làm bằng chứng.

---

## 1. Bộ test đầy đủ (Oracle = SPEC)

Đây là kết quả kiểm thử thật sự: mọi kỳ vọng đều viết theo đặc tả, nên các case phơi bày
bug của SUT **sẽ thất bại** — đó là mục đích của chúng.

| API | Case | Case PASS | Case FAIL | Assertion | Assertion FAIL | Thời gian | Báo cáo HTML |
|---|---|---|---|---|---|---|---|
| API-1 | 70 | 33 | 37 | 328 | 51 | 4.4s | `newman/23127060_API-1_20260902-235242.html` |
| API-2 | 87 | 34 | 53 | 413 | 78 | 5.2s | `newman/23127060_API-2_20260902-235253.html` |
| API-3 | 86 | 17 | 69 | 405 | 105 | 4.4s | `newman/23127060_API-3_20260902-235305.html` |
| **Tổng** | **243** | **84** | **159** | **1146** | **234** | | |

Tỷ lệ case PASS: **35%** (84/243). Tỷ lệ assertion PASS: **80%** (912/1146).

## 2. Phân loại case thất bại

| API | FAIL tổng | Có chủ đích (`@bug`) | Ngoài dự kiến (`@contract`) |
|---|---|---|---|
| API-1 | 37 | 18 | 19 |
| API-2 | 53 | 25 | 28 |
| API-3 | 69 | 48 | 21 |

## 3. Bug được phơi bày, theo mã bug

| Mã bug | Số case thất bại phơi bày nó | API |
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

## 4. Thất bại ngoài dự kiến — em phải rà soát từng cái

Đây là các case gắn `@contract` (nghĩa là lúc thiết kế em nghĩ SUT đáp ứng được) nhưng
vẫn thất bại. Mỗi dòng ở đây hoặc là **một bug chưa có trong danh sách bug đã biết**,
hoặc là **một kỳ vọng sai của chính test case**. Em không bỏ qua dòng nào.

### API-1 — 19 case

| TC_ID | Tiêu đề | Thông báo thất bại đầu tiên |
|---|---|---|
| `TC-A1-DOM-003` | POST /api/forgot-password \| email =  (email rỗng) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-004` | POST /api/forgot-password \| email = <thieu key> (thiếu key email) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-005` | POST /api/forgot-password \| email = - (email null) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-006` | POST /api/forgot-password \| email = 12345 (email sai kiểu (number)) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-007` | POST /api/forgot-password \| email = abc@@test (email sai định dạng) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-008` | POST /api/forgot-password \| email = aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-009` | POST /api/forgot-password \| email = API.VICTIM.23127060@TEST.LOCAL (em | expected response to have status code 200 but got 404 |
| `TC-A1-DOM-010` | POST /api/forgot-password \| email =   api.victim.23127060@test.local   | expected response to have status code 200 but got 404 |
| `TC-A1-DOM-011` | POST /api/forgot-password \| email = ["a@b.c"] (email la array) | expected response to have status code 400 but got 404 |
| `TC-A1-DOM-027` | POST /api/reset-password \| newPassword = <thieu key> (thiếu newPasswor | expected response to have status code 400 but got 200 |
| `TC-A1-DOM-028` | POST /api/reset-password \| newPassword = - (newPassword null) | expected response to have status code 400 but got 200 |
| `TC-A1-DOM-034` | POST /api/reset-password \| newPassword = <script>alert(1)</script> (pa | expected response to have status code 400 but got 200 |
| `TC-A1-DOM-036` | POST /api/reset-password \| newPassword = A1!aaaaaaaaaaaaaaaaaaaaaaaaaa | expected response to have status code 400 but got 200 |
| `TC-A1-SCH-002` | Response lỗi của forgot-password khớp schema { error: string } | expected response to have status code 400 but got 404 |
| `TC-A1-SEC-001` | [SEC-05] SQLi qua trường email của forgot-password | expected response to have status code 400 but got 404 |
| `TC-A1-SEC-009` | [SEC-04] Email chứa payload XSS phải bị từ chối hoặc escape | expected response to have status code 400 but got 404 |
| `TC-A1-SEC-010` | [SEC-04] Path traversal trong email không được gây lỗi 500 | expected response to have status code 400 but got 404 |
| `TC-A1-SEC-013` | [SEC-07] Xin OTP lần 2 thì OTP lần 1 phải bị vô hiệu hóa | expected response to have status code 400 but got 200 |
| `TC-A1-STA-006` | Chuyển trạng thái USED -> USED (dùng lại OTP đã dùng - KHÔNG hợp lệ) | expected response to have status code 400 but got 200 |

### API-2 — 28 case

| TC_ID | Tiêu đề | Thông báo thất bại đầu tiên |
|---|---|---|
| `TC-B2-DOM-001` | POST /api/checkout \| total_amount = 200000 (tổng tiền khớp với giỏ hàn | expected response to have status code 201 but got 200 |
| `TC-B2-DOM-005` | POST /api/checkout \| total_amount = 200000 (tổng tiền sai kiểu (string | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-006` | POST /api/checkout \| total_amount = <thieu key> (thiếu total_amount) | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-007` | POST /api/checkout \| total_amount = - (total_amount null) | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-008` | POST /api/checkout \| total_amount = 999999999999999 (BVA - tong tien v | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-009` | POST /api/checkout \| total_amount = 200000.999 (tong tien co phan thap | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-012` | POST /api/checkout \| items = [{"product_id":1,"quantity":0}] (BVA - số | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-013` | POST /api/checkout \| items = [{"product_id":1,"quantity":-5}] (số lượn | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-014` | POST /api/checkout \| items = [{"product_id":1,"quantity":1}] (BVA - số | expected response to have status code 201 but got 200 |
| `TC-B2-DOM-015` | POST /api/checkout \| items = [{"product_id":999999,"quantity":1}] (sản | expected response to have status code 404 but got 200 |
| `TC-B2-DOM-016` | POST /api/checkout \| items = [{"product_id":1,"quantity":100000}] (vuo | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-017` | POST /api/checkout \| items = khong-phai-array (items sai kiểu) | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-018` | POST /api/checkout \| shipping_address = 123 Nguyen Van Cu, Q5, TP.HCM  | expected response to have status code 201 but got 200 |
| `TC-B2-DOM-022` | POST /api/checkout \| shipping_address = <script>alert('23127060')</scr | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-023` | POST /api/checkout \| shipping_address = A123456789A123456789A123456789 | expected response to have status code 400 but got 200 |
| `TC-B2-DOM-025` | POST /api/apply-coupon \| code = BIGBUY (Decision table T2 - mã số tiền | expected response to have status code 200 but got 400 |
| `TC-B2-DOM-031` | POST /api/apply-coupon \| code = ' OR '1'='1 (SQLi trong mã giảm giá) | expected response to have status code 400 but got 404 |
| `TC-B2-DOM-032` | POST /api/apply-coupon \| code = perc10 (mã viết thường - hành vi phải  | expected response to have status code 200 but got 404 |
| `TC-B2-DOM-035` | POST /api/apply-coupon \| total_amount = 300001 (BVA - trên min_order_a | expected data to satisfy schema but found following errors:  data.discount_amount should b |
| `TC-B2-DOM-038` | POST /api/apply-coupon \| user_id = {{userId}} (user_id của chính mình) | expected data to satisfy schema but found following errors:  data.discount_amount should b |
| `TC-B2-SCH-001` | Response 201 của checkout khớp schema { orderId: integer, message: str | expected response to have status code 201 but got 200 |
| `TC-B2-SCH-002` | Response lỗi của checkout khớp schema { error: string } | expected response to have status code 400 but got 200 |
| `TC-B2-SEC-001` | [SEC-05] SQLi qua mã giảm giá | expected response to have status code 400 but got 404 |
| `TC-B2-SEC-002` | [-] Response checkout không được lộ thông tin nội bộ | expected response to have status code 201 but got 200 |
| `TC-B2-SEC-008` | [SEC-02] Hủy đơn hàng của người khác | expected response to have status code 403 but got 404 |
| `TC-B2-SEC-010` | [SEC-03] User thường xem toàn bộ đơn hàng qua GET /api/admin/orders | expected response to have status code 403 but got 200 |
| `TC-B2-SEC-011` | [SEC-04] XSS trong shipping_address phải bị chặn hoặc escape | expected response to have status code 400 but got 200 |
| `TC-B2-SEC-012` | [-] Gửi kèm status='delivered' khi checkout | expected response to have status code 201 but got 200 |

### API-3 — 21 case

| TC_ID | Tiêu đề | Thông báo thất bại đầu tiên |
|---|---|---|
| `TC-C3-DOM-006` | POST /api/products \| name = A (BVA - 1 ký tự (dưới biên tối thiểu)) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-007` | POST /api/products \| name = A123456789A123456789A123456789A123456789 ( | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-008` | POST /api/products \| name = A123456789A123456789A123456789A123456789 ( | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-010` | POST /api/products \| name = San pham tieng Viet co dau 23127060 (tên c | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-011` | POST /api/products \| price = 150000 (giá hợp lệ) | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-014` | POST /api/products \| price = 1 (BVA - giá 1 (biên dưới hợp lệ)) | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-018` | POST /api/products \| price = 999999999999999 (BVA - giá vượt giới hạn) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-019` | POST /api/products \| price = 150000.55 (giá có phần thập phân) | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-023` | POST /api/products \| category_id = abc (category_id sai kiểu) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-024` | POST /api/products \| category_id = - (category_id null (không bắt buộc | expected response to have status code 201 but got 200 |
| `TC-C3-DOM-026` | POST /api/products \| imageUrl = javascript:alert('23127060') (URL sche | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-027` | POST /api/products \| imageUrl = ../../etc/passwd (path traversal trong | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-028` | POST /api/products \| imageUrl = khong-phai-url (chuỗi không phải URL) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-029` | PUT /api/products/:id \| id = 1 (id tồn tại) | expected data to satisfy schema but found following errors:  data should NOT have addition |
| `TC-C3-DOM-031` | PUT /api/products/:id \| id = 0 (BVA - id = 0) | expected response to have status code 404 but got 200 |
| `TC-C3-DOM-032` | PUT /api/products/:id \| id = -1 (id am) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-033` | PUT /api/products/:id \| id = abc (id không phải số) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-034` | PUT /api/products/:id \| id = 1%20OR%201=1 (SQLi trong path param) | expected response to have status code 400 but got 200 |
| `TC-C3-DOM-036` | PUT /api/products/:id \| description = Mo ta moi 23127060 (cap nhat mo  | expected data to satisfy schema but found following errors:  data should NOT have addition |
| `TC-C3-DOM-043` | GET /api/products \| search =  (từ khóa rỗng - trả về tất cả) | expected data to satisfy schema but found following errors:  data[7].name should be string |
| `TC-C3-SEC-013` | [-] Gửi kèm trường id để ghi đè khóa chính | expected response to have status code 400 but got 200 |

## 5. Bộ hồi quy (`@contract`) — lần chạy all-pass cho CI

Bộ này gồm các test case mà SUT **hiện đang đáp ứng**, được chốt từ kết quả chạy thật
bằng `derive_contract.py`. Nó không khẳng định 'API này đúng', mà khẳng định 'những điều
API này đang làm đúng thì không được phá'. Đây là lần chạy em dùng cho yêu cầu
'all API test cases passing' của đề bài mục 6.

| API | Case | Assertion | Assertion FAIL | Báo cáo HTML |
|---|---|---|---|---|
| API-1 | 33 | 163 | **0** | `newman/23127060_API-1_contract_20260903-000103.html` |
| API-2 | 34 | 164 | **0** | `newman/23127060_API-2_contract_20260903-000111.html` |
| API-3 | 17 | 79 | **0** | `newman/23127060_API-3_contract_20260903-000121.html` |
| **Tổng** | **84** | **406** | **0** | |

## 6. Lần chạy data-driven (Postman Collection Runner / `newman -d`)

| Bộ | Data file | Vòng lặp | Request | Assertion | Assertion FAIL |
|---|---|---|---|---|---|
| DD1 Brute force OTP | `postman/data/brute_force_tokens.csv` | 20 | 40 | 40 | 20 |
| DD2 Bảng chuyển trạng thái FR-10 | `postman/data/state_transitions.csv` | 17 | 70 | 34 | 1 |
| DD3 Lạm dụng hạn mức coupon | `postman/data/coupon_abuse.csv` | 4 | 7 | 8 | 2 |
| DD4 Đầu vào không hợp lệ POST /api/products | `postman/data/product_invalid.csv` | 7 | 20 | 14 | 7 |

