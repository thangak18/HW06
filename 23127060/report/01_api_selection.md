# STEP 1 — Lựa chọn 3 API và lập đặc tả máy đọc được

> HW06 — API Testing | SV **Ninh Văn Khải — 23127060**

---

## 1. Ba API em chọn (đề bài mục 5)

Đề bài yêu cầu chọn **đúng 3 API**, mỗi Pool một cái, và không được trùng với thành viên khác.

| ID | Pool | FR | Endpoint chính | Endpoint hỗ trợ | Lý do em chọn |
|---|---|---|---|---|---|
| **API-1** | A | FR-03 Quên & đặt lại mật khẩu | `POST /api/forgot-password`<br>`POST /api/reset-password` | `POST /api/login`, `POST /api/register` | Đây là luồng **2 bước có trạng thái** (chưa có token → đã cấp token → đã dùng token), nên vừa có domain partition đầy đủ vừa có state machine thật sự. Đồng thời đây là bề mặt tấn công đậm đặc nhất: SEC-01 (mật khẩu plaintext) và SEC-07 (entropy / vòng đời OTP) đều hội tụ ở đây. |
| **API-2** | B | FR-08 Thanh toán | `POST /api/checkout` | `POST /api/apply-coupon` (FR-09), `GET /api/orders/:id`, `PUT /api/orders/:id/cancel`, `PUT /api/admin/orders/:id/status` (FR-10) | Kết hợp được **ba** thứ mà đề bài đòi: tính tiền (domain partition trên số tiền), **state machine 5 trạng thái** của FR-10, và phân quyền (SEC-02, SEC-03). FR-09 còn cho sẵn một **bảng quyết định 5 điều kiện** viết trong SRS. |
| **API-3** | C | FR-15 Quản lý sản phẩm | `POST` / `PUT` / `DELETE /api/products` | `GET /api/products`, `GET /api/products?search=`, `GET /api/products/:id` | CRUD đầy đủ nên có vòng đời tài nguyên (`NOT_EXIST → CREATED → UPDATED → DELETED`), có tham số ở cả **body, path và query** (3 vị trí khác nhau), và là nơi duy nhất có **SQL nối chuỗi** — bắt buộc phải có để phủ SEC-05. |

**Pool D (Mobile) em không sử dụng.** Đề bài mục 5 ghi rõ: *"Pool D, the mobile app, is not
used here, because this homework targets the backend API."* Nếu cần, phần mobile chỉ có thể
làm phụ lục không tính điểm.

### Kiểm tra trùng lặp trong nhóm

Em đã đọc `../../docs/team-api-allocation.md` (chỉ đọc, không sửa). Tại thời điểm làm bài, bảng
phân công còn để `TODO` ở cả 3 dòng thành viên, nên em **không thể đối chiếu tự động**. Bộ ba
(FR-03, FR-08, FR-15) đã được em chốt từ đầu trong `CLAUDE.md`. Đây là **rủi ro mở cần xác nhận
miệng với 2 thành viên còn lại trước khi nộp**, không phải vấn đề kỹ thuật.

**Cập nhật (02/09/2026, sau khi merge `origin/main`):** bảng phân công đã được điền đầy đủ,
nên em **đã đối chiếu được**. Ba bộ API của nhóm:

| SV | Pool A | Pool B | Pool C |
|---|---|---|---|
| **23127060** (em) | FR-03 | FR-08 | FR-15 |
| 23127195 | FR-04 | FR-09 | FR-16 |
| 23127259 | FR-02 | FR-10 | FR-14 |

**Không có FR nào trùng nhau** giữa ba thành viên → thỏa ràng buộc mục 5 của đề bài.
Rủi ro mở nêu trên **đã được đóng**.

## 2. Vì sao phải lập đặc tả máy đọc được

Đề bài mục 7 (10 điểm, mức Create G9.5) yêu cầu một bộ sinh test: *"given the API
specification, it produces test cases automatically"*. Đặc tả văn xuôi của SUT
(`eshop-sut/README.md`) không thể đưa thẳng cho chương trình đọc, vì nó **không nói rõ đâu là
trục phân hoạch**. Ví dụ câu "Giá: bắt buộc, phải là số dương (> 0)" chứa ba thông tin ẩn:
tham số `price`, kiểu số, và một **biên tại 0**. Con người đọc ra ngay; chương trình thì không.

Vì vậy ở STEP 1 em dịch SRS sang `spec/api-1.json`, `api-2.json`, `api-3.json` — mỗi file gồm
**bốn trục**, ánh xạ một đối một sang bốn nhóm kỹ thuật mà đề bài mục 6.1 đòi hỏi:

| Khóa trong spec | Nhóm sinh ra | Kỹ thuật kiểm thử |
|---|---|---|
| `endpoints[].params[].partitions[]` | `DOM` | Equivalence Partitioning, BVA, Decision Table |
| `state_machine.transitions[]` | `STA` | State Transition Testing (0-switch) |
| `security[]` | `SEC` | Security Testing theo SEC-01..SEC-07 |
| `schema_cases[]` | `SCH` | JSON Schema Validation |

Định dạng đầy đủ: xem `spec/_SCHEMA.md`.

**Hệ quả thiết kế quan trọng:** vì bốn trục tách rời nhau, bộ sinh chạy được từng vòng độc lập
(`--only DOM`, `--only STA`, `--only SEC`, `--only SCH`). Đó chính là cơ sở kỹ thuật để STEP 2
tuân thủ yêu cầu *"drive it step by step, not with a single generic prompt"* của đề bài.

## 3. Độ phủ hiện tại của ba file spec

```
$ python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py --spec spec/api-N.json --stats
```

| API | DOM | STA | SEC | SCH | **Tổng** | Tham số chưa phủ | Mã SEC chưa phủ | Ô state machine đã phủ |
|---|---|---|---|---|---|---|---|---|
| API-1 | 36 | 9 | 13 | 6 | **64** | (không) | (đủ 7) | 9 / 9 |
| API-2 | 41 | 20 | 14 | 6 | **81** | (không) | (đủ 7) | 20 / 25 |
| API-3 | 51 | 9 | 14 | 6 | **80** | (không) | (đủ 7) | 9 / 16 |

Ngưỡng tối thiểu của đề bài là **35 case/API**; cả ba đều vượt xa. Các ô state machine còn
thiếu đều là ô **tự chuyển về chính nó** (`pending → pending`, ...) — em sẽ bổ sung ở
STEP 4 (extend), vì đây đúng là loại case mà AI hay bỏ sót.

## 4. Hai lỗi thật trong bộ sinh test em đã sửa ở bước này

Chạy thử bộ sinh lần đầu cho kết quả bất thường: API-1 khai báo 6 trường hợp schema nhưng chỉ
sinh ra **1**, và khai báo 9 chuyển trạng thái nhưng chỉ sinh ra **5**. Em truy nguyên về hàm
`dedup()`:

```python
key = (r["Method"], r["Endpoint"], r["Request_Body"], str(r["Expected_Status"]))
```

Khóa này coi hai test case là trùng nhau khi chúng **gửi cùng một request**, bất kể chúng
**khẳng định điều gì**. Hai hậu quả:

1. Một case `SCH` ("response 200 của forgot-password khớp schema `{message: string}`") và một
   case `DOM` ("email hợp lệ trả 200") gửi y hệt nhau nhưng kiểm hai thứ khác hẳn. Case `SCH`
   bị nuốt.
2. Hai case `STA` "hủy đơn đang `pending`" và "hủy đơn đang `confirmed`" cùng gọi
   `PUT /api/orders/:id/cancel` với body rỗng; chúng chỉ khác nhau ở **trạng thái ban đầu**.
   Case thứ hai bị nuốt.

Em đã sửa khóa dedup thành:

```python
key = (r["Category"], r["Method"], r["Endpoint"], r["Request_Body"],
       str(r["Expected_Status"]), r["Expected_Assertions"], r["Preconditions"])
```

Kết quả: API-1 từ 52 → **64** case, API-2 từ 67 → **81**, API-3 từ 72 → **80**; độ phủ state
machine của API-2 từ 11/25 lên **20/25**. Đây là ví dụ cụ thể cho thấy **công cụ tự động cũng
cần được kiểm thử** — nếu em tin ngay con số đầu tiên thì đã báo cáo thiếu 26 test case và một
độ phủ state machine sai.

Lỗi thứ hai: bảng `SEC_DEFAULT_ASSERT` trong bộ sinh vẫn điền assertion theo **bảng SEC suy
diễn sai** mà em đã phát hiện ở STEP 0 (ví dụ `SEC-05` sinh ra assertion "trả 403; hành động
admin KHÔNG được thực hiện", trong khi SEC-05 thật là "truy vấn CSDL phải dùng Parameterized
Query"). Em đã viết lại toàn bộ bảng theo `eshop-sut/README.md` mục 9.

## 5. Các dữ liệu không tồn tại em đã loại khỏi spec

`spec/api-2.json` tham chiếu ba mã giảm giá **không hề tồn tại** trong `database.js`. Nếu giữ
nguyên, mọi test coupon đều rơi vào nhánh "mã không tồn tại" và **thất bại vì lý do sai** —
tức là test vẫn đỏ nhưng không còn kiểm đúng thứ cần kiểm.

| Trong spec (sai) | Trong `database.js` (thật) | Em đã xử lý |
|---|---|---|
| `PERC10` — percent 10%, min 100000 | `SAVE10` — percent 10, min **300000** | đổi tên + đổi ngưỡng BVA 99999/100000/100001 → **299999/300000/300001** |
| `FIX50K` — fixed 50000 | `BIGBUY` — fixed 50000, min **500000** | đổi tên |
| `INACTIVE` — mã bị vô hiệu hóa | **không tồn tại** | xem dưới |

`valid_body` của `apply-coupon` cũng dùng `total_amount: 200000`, thấp hơn ngưỡng thật
300000 của `SAVE10`, nên **mọi** case coupon sẽ bị từ chối ngay từ điều kiện C3 và không bao
giờ chạm tới công thức giảm giá. Em đã nâng lên `500000` để thỏa ngưỡng của cả `SAVE10` lẫn `BIGBUY`.

### Giới hạn em ghi nhận: không kiểm được điều kiện C1 "mã bị vô hiệu hóa"

SRS FR-09 điều kiện C1 đòi mã phải `is_active = 1`. Nhưng:

- `database.js` seed **4 mã và cả 4 đều có `is_active = 1`**;
- `POST /api/admin/coupons` **không nhận** tham số `is_active` (cột này mặc định `1` ở tầng DB),
  nên không thể tạo mã bị vô hiệu hóa qua API.

Kết luận: nhánh `is_active = 0` **không thể kiểm được qua API** nếu không dùng `sqlite3` CLI
tác động trực tiếp vào CSDL. Em đã thay dòng T4 của bảng quyết định bằng một dòng khác có giá
trị thật: `VIP100` (fixed 100000, min 300000, **max 2 lượt/user**) — dòng này kiểm điều kiện C5
(hạn mức sử dụng), là điều kiện duy nhất trong 5 điều kiện chưa có case riêng. Giới hạn này em
ghi lại trong báo cáo chính thay vì giấu đi bằng một test luôn pass.

## 6. Kết luận STEP 1

- Ba file spec hợp lệ, tổng **225 test case** sẽ được sinh ra ở STEP 2 (vượt xa ngưỡng 105).
- Độ phủ: đủ 7 mã SEC cho cả 3 API, không tham số nào bị bỏ sót, state machine API-2 đạt 20/25.
- Em đã sửa **2 lỗi thật trong bộ sinh test** và **3 tham chiếu dữ liệu không tồn tại** trong spec.
- **STEP kế tiếp:** STEP 2 — sinh test case theo 4 vòng riêng biệt (DOM, STA, SEC, SCH).
