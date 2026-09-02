# STEP 9 — Thiết kế bộ sinh test case bằng AI (Agent Skill)

> HW06 — API Testing | SV **Ninh Văn Khải — 23127060** | Đề bài mục 7 (10 điểm, mức Create G9.5)

Đề bài: *"design an AI-driven API test generator for the SUT: given the API specification, it
produces test cases automatically. Provide a self-drawn diagram and pseudocode of the design."*

---

## 1. Ý tưởng: tách làm hai lớp

Cách làm hiển nhiên là bảo AI *"đọc đặc tả này và viết 35 test case"*. Cách đó có ba vấn đề:

- **Không lặp lại được.** Chạy lại cùng một prompt cho ra bộ test khác.
- **Không đo được độ phủ.** Không trả lời được câu "tham số `price` đã có bao nhiêu phân hoạch?"
- **Không mở rộng được.** Thêm một API là làm lại từ đầu.

Thiết kế của em tách quy trình làm hai lớp có ranh giới rõ:

| Lớp | Ai làm | Sản phẩm | Tính chất |
|---|---|---|---|
| **Lớp tri thức** | Em và AI cùng làm | `spec/api-N.json` | Đòi hỏi đọc hiểu; đây là nơi quyết định chất lượng |
| **Lớp sinh** | Máy làm một mình | `testcases/API-N_generated.csv` | **Tất định**: cùng đầu vào luôn cho cùng đầu ra |

Ranh giới này là quyết định thiết kế quan trọng nhất. Em không cho phép AI "sáng tác" test case;
nó chỉ được giúp **dịch đặc tả văn xuôi sang một cấu trúc có trục phân hoạch rõ ràng**. Từ đó
trở đi là một chương trình tất định.

Lợi ích cụ thể: khi một test case sai, em truy ngược được ngay về **dòng nào trong file spec**
gây ra nó. Với bộ sinh dạng hộp đen thì không truy được.

## 2. Vì sao đặc tả văn xuôi không đưa thẳng cho máy được

Câu này trong SRS FR-15:

> *"Giá: bắt buộc, phải là số **dương** (> 0)."*

chứa **ba** thông tin ẩn mà con người đọc ra ngay còn chương trình thì không:

1. Có một tham số tên `price`.
2. Kiểu của nó là số.
3. Có một **biên tại 0**, và biên đó thuộc phía không hợp lệ.

Khối "dịch sang dạng máy đọc được" chính là nơi biến đổi này xảy ra. Sau khi dịch, cùng thông
tin đó trở thành:

```json
{ "name": "price", "in": "body", "type": "number", "required": true,
  "partitions": [
    { "id": "valid",    "value": 150000, "valid": true,  "expected_status": 201 },
    { "id": "zero",     "value": 0,      "valid": false, "boundary": true, "expected_status": 400 },
    { "id": "negative", "value": -100,   "valid": false, "expected_status": 400, "bug": "C-06" },
    { "id": "string",   "value": "abc",  "valid": false, "expected_status": 400, "bug": "C-06" }
  ]
}
```

Bây giờ thì một vòng lặp sinh được test case, và câu hỏi *"tham số `price` đã có bao nhiêu
phân hoạch?"* trả lời được bằng một lệnh đếm.

## 3. Kiến trúc

```
PARSE -> NORMALISE -> 4 BO SINH SONG SONG -> KHU_TRUNG -> DANH_SO -> KIEM_TRA_DO_PHU -> EMIT
                                                                            |
                                              (chua du do phu) -------------+
                                                          quay lai bo sung vao spec
```

Bốn trục trong file spec ánh xạ **một đối một** sang bốn nhóm kỹ thuật mà đề bài mục 6.1 đòi:

| Trục trong spec | Bộ sinh | Kỹ thuật | Số case sinh ra |
|---|---|---|---|
| `endpoints[].params[].partitions[]` | `gen_domain` | Equivalence Partitioning, BVA, Decision Table | 128 |
| `state_machine.transitions[]` | `gen_state` | State Transition Testing (0-switch) | 38 |
| `security[]` | `gen_security` | Ánh xạ SEC-01..SEC-07 | 41 |
| `schema_cases[]` | `gen_schema` | JSON Schema Validation | 18 |
| | | **Tổng** | **225** |

Bốn bộ sinh **độc lập** nhau, nên chạy được riêng từng cái:

```bash
python3 gen_testcases.py --spec spec/api-2.json --only DOM --out out.csv
python3 gen_testcases.py --spec spec/api-2.json --only STA --out out.csv --append
```

Đây không phải tiện ích phụ mà là **cơ sở kỹ thuật** để thỏa yêu cầu *"drive it step by step,
not with a single generic prompt"* của đề bài: STEP 2 chạy đúng bốn vòng độc lập, mỗi vòng một
kỹ thuật kiểm thử, mỗi vòng một entry AI_log riêng.

**Sơ đồ:** `agent-skill/diagram/23127060_generator_diagram.png` — **do em tự vẽ**, theo đề bài
mục 11. Mô tả khối và luồng: `agent-skill/diagram/DIAGRAM_BRIEF.md`.
**Pseudocode đầy đủ:** `agent-skill/pseudocode/generator.pseudo.md`.
**Bản hiện thực chạy được:** `agent-skill/eshop-api-23127060/scripts/gen_testcases.py` (chỉ dùng
thư viện chuẩn của Python).

## 4. `KIEM_TRA_DO_PHU` — cổng tự chặn

Bộ sinh không chỉ in ra test case, nó còn **tự chấm độ phủ của chính mình**:

```
$ python3 gen_testcases.py --spec spec/api-2.json --stats
So case theo nhom: DOM=41, STA=20, SEC=14, SCH=6
Tong: 81
Tham so CHUA phu DOM: (khong)
Ma SEC CHUA phu: (du 7)
O bang chuyen trang thai da test: 20 / 25
```

Bốn phép đo:

1. **Mọi tham số** của mọi endpoint phải có ít nhất một case.
2. **Bảy mã SEC-01..07** phải được phủ (trên toàn bộ suite — xem mục 5.2).
3. **Bảng chuyển trạng thái**: bao nhiêu ô trong `states x states` đã có case.
4. **Ngưỡng 35 case/API** của đề bài.

Dòng `20 / 25` là ví dụ cho thấy phép đo này có ích: nó chỉ thẳng ra 5 ô còn thiếu, và đó đúng
là nằm ở **đường chéo** (`pending → pending`, ...). Những ô đó bị bỏ qua vì trực quan chúng
"không phải một bước chuyển" — nhưng trong thực tế chúng hay gây lỗi nhất (một request bị gửi
lại hai lần do mạng chậm hoặc người dùng bấm hai lần). Em đã bổ sung chúng ở STEP 4.

## 5. Hai lỗi thật trong bộ sinh, và cách em tìm ra

Phần này quan trọng hơn phần mô tả kiến trúc: **công cụ tự động cũng phải được kiểm thử.**

### 5.1 Khóa khử trùng nuốt mất 34 test case

Chạy lần đầu, API-1 khai báo 6 trường hợp schema nhưng chỉ sinh ra **1**, và khai báo 9 chuyển
trạng thái nhưng chỉ sinh ra **5**. Con số không khớp với khai báo — đó là dấu hiệu duy nhất.

Em truy nguyên về hàm `dedup()`:

```python
key = (r["Method"], r["Endpoint"], r["Request_Body"], str(r["Expected_Status"]))
```

Khóa này coi hai test case là trùng nhau khi chúng **gửi cùng một request**, bất kể chúng
**khẳng định điều gì**. Hai hậu quả:

- Một case `SCH` (*"response 200 khớp schema `{message: string}`"*) và một case `DOM`
  (*"email hợp lệ trả 200"*) gửi y hệt nhau nhưng kiểm hai thứ khác hẳn. Case `SCH` bị nuốt.
- Hai case `STA` *"hủy đơn đang `pending`"* và *"hủy đơn đang `confirmed`"* cùng gọi
  `PUT /api/orders/:id/cancel` với body rỗng; chúng chỉ khác nhau ở **trạng thái ban đầu**.
  Case thứ hai bị nuốt.

Khóa sau khi em sửa:

```python
key = (r["Category"], r["Method"], r["Endpoint"], r["Request_Body"],
       str(r["Expected_Status"]), r["Expected_Assertions"], r["Preconditions"])
```

Kết quả: **191 → 225 case**, độ phủ state machine của API-2 **11/25 → 20/25**.

Nếu em tin ngay con số đầu tiên thì báo cáo đã ghi thiếu 34 test case và một độ phủ sai.

### 5.2 Bảng SEC-01..07 được điền từ trí nhớ

Bảng `SEC_DEFAULT_ASSERT` trong bộ sinh được viết theo **trí nhớ về các lỗ hổng OWASP quen
thuộc**: SEC-01 = SQL Injection, SEC-04 = IDOR, SEC-05 = leo thang quyền, SEC-07 = brute force.

Bảng **thật** nằm trong `eshop-sut/README.md` mục 9 và nói những điều hoàn toàn khác: SEC-01 là
*"mật khẩu không được lưu plaintext"*, SEC-05 là *"truy vấn CSDL phải dùng Parameterized
Query"*. **39/41 test case bảo mật bị gắn sai mã.**

Điều đáng nói: các test case **vẫn chạy đúng** — một phép thử SQL Injection vẫn là một phép thử
SQL Injection dù nó bị dán nhãn SEC-01 hay SEC-05. Cái hỏng là **bảng độ phủ bảo mật trong báo
cáo**: nó sẽ ghi *"API-3 đã phủ SEC-01 với 8 test case"* trong khi SEC-01 không hề được kiểm ở
API-3 dòng nào.

Nguyên nhân sâu xa: **`SEC-01` là một nhãn không tự giải thích.** Đọc "SEC-01" không ai đoán
được nó nói gì, nên rất dễ điền vào bằng mô hình mạnh nhất có sẵn. Chỉ một lệnh
`grep -n "SEC-0" README.md` là ra sự thật.

Bài học cho thiết kế: **mọi nhãn mà bộ sinh gắn lên test case mà không tự giải thích được thì
phải có một bước đối chiếu với tài liệu gốc**, không được coi là kiến thức nền.

### 5.3 Một chỉ tiêu đo lường đặt sai gây ra chính cái lỗi nó định ngăn chặn

`references/TESTCASE_TAXONOMY.md` do chính em viết có dòng: *"Bắt buộc phủ đủ 7 mã
SEC-01..SEC-07 cho **mọi** API"*. Sau khi biết bảng SEC thật, yêu cầu đó là **bất khả thi**:
SEC-07 nói về vòng đời OTP thì không thể áp vào API quản lý sản phẩm; SEC-01 nói về lưu trữ
mật khẩu thì không liên quan gì đến luồng thanh toán.

Và chính yêu cầu đó gây hại: cách duy nhất để "đạt chỉ tiêu" là **gán bừa** một mã SEC cho một
case không thuộc nó. Chỉ tiêu đúng phải là: *đủ 7 mã trên toàn bộ suite; từng API phủ những mã
thực sự áp dụng được, phần không áp dụng có giải trình một dòng.* Em đã sửa lại taxonomy.

## 6. Hạn chế và hướng mở rộng

### 6.1 Hạn chế lớn nhất: bộ sinh sinh ra test case ĐỘC LẬP

Cả bốn bộ sinh đều theo cùng một khuôn: một vòng lặp trên một danh sách khai báo, mỗi phần tử
cho ra **một** test case, mỗi test case **một** request. Đó là giới hạn **cấu trúc**, không phải
giới hạn về prompt hay về mô hình.

Số liệu đo được: trong 18 test case mà em phải tự bổ sung ở STEP 4, **9 case (một nửa)**
thuộc nhóm `API` — tức là *"bug chỉ lộ ra khi kết hợp nhiều request"*:

| Bug | Vì sao cần nhiều request |
|---|---|
| C-05 | `{"price": 30000000}` và `{"price": "28000000"}` đều là JSON hợp lệ. Vi phạm chỉ hiện ra khi **so sánh hai response** |
| B-09 | Đưa đơn về trạng thái `shipping` đòi hỏi đi qua đúng hai bước admin — một chuỗi 4 request |
| C-09 | Phải `POST` rồi `PUT` thiếu trường rồi `GET` mới thấy 4 trường bị xóa trắng |
| C-13 | Sập máy chủ chỉ xảy ra ở request **thứ ba** của chuỗi, và nó là hệ quả của hai bug khác cộng lại |

**Hướng mở rộng:** bổ sung một trục thứ năm vào file spec:

```jsonc
"scenarios": [
  {
    "id": "SCN-C3-01",
    "title": "PUT mot phan lam sap may chu khi doc lai",
    "steps": [
      { "method": "POST", "path": "/api/products", "body": {...}, "save": { "pid": "id" } },
      { "method": "PUT",  "path": "/api/products/{pid}", "body": { "name": "chi ten" } },
      { "method": "GET",  "path": "/api/products/{pid}" }
    ],
    "assertions": [
      { "type": "cross_step", "expr": "steps[2].price != null" },
      { "type": "server_alive" }
    ]
  }
]
```

Bộ sinh sẽ sinh ra một chuỗi request kèm các **khẳng định bậc cao** liên kết các bước
(`cross_step`). Đây là bước chuyển từ **0-switch coverage** sang **n-switch coverage**, và nó
xử lý đúng nhóm bug mà phiên bản hiện tại bỏ sót.

### 6.2 Các hạn chế khác

| Hạn chế | Ảnh hưởng | Hướng xử lý |
|---|---|---|
| Chất lượng đầu ra **hoàn toàn** phụ thuộc chất lượng file spec. Spec sai thì test sai theo — như vụ bảng SEC | Cao | Thêm bước đối chiếu tự động: kiểm mọi mã SEC dùng trong spec có tồn tại trong tài liệu gốc không |
| Chỉ sinh được **assertion ở dạng văn xuôi**; 17-23% không dịch được sang phép kiểm Postman | Trung bình | Cho phép spec khai báo assertion có cấu trúc (`{"type":"json_path","path":"$.price","op":"is_number"}`) thay vì chuỗi tự do |
| Không sinh được dữ liệu test ngẫu nhiên (property-based testing) | Trung bình | Kết nối với `hypothesis` hoặc `fast-check` để sinh giá trị biên từ định nghĩa kiểu |
| Không tự đo được thời gian phản hồi hay tải trọng | Thấp | Ngoài phạm vi HW06 (thuộc HW05 Performance Testing) |
| Bảng quyết định phải liệt kê tay từng tổ hợp | Trung bình | Sinh tổ hợp tự động từ danh sách điều kiện, kèm thuật toán pairwise để giảm số case |

## 7. Bằng chứng bộ sinh chạy được thật

```bash
$ python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py \
    --spec spec/api-3.json --only DOM --out testcases/API-3_generated.csv
Da ghi 51 case (DOM) vao testcases/API-3_generated.csv | tong file: 51
So case theo nhom: DOM=51, STA=0, SEC=0, SCH=0
Tong: 51
Tham so CHUA phu DOM: (khong)
```

Toàn bộ chuỗi công cụ, chạy được độc lập:

| Script | Vai trò |
|---|---|
| `gen_testcases.py` | **Bộ sinh test case** — trọng tâm của mục 7 đề bài |
| `audit_testcases.py` | Gắn nhãn VALID / INVALID / INCOMPLETE bằng 10 luật tái lập được |
| `extend_testcases.py` | 18 case do em tự viết, kèm lý do AI bỏ sót |
| `build_collection.py` | CSV → Postman Collection v2.1 chạy được |
| `run_newman.sh` / `run_datadriven.sh` | Chạy Newman trên CSDL sạch |
| `derive_contract.py` | Chốt mốc hồi quy từ kết quả chạy thật |
| `summarize_newman.py` | Newman JSON → bảng tổng hợp báo cáo |
| `verify_header.py` | Kiểm chứng header `X-Student-Id` chống gian lận |
| `capture_bug_evidence.py` | Chạy lại kịch bản tái hiện từng bug, ghi request/response thật |
| `make_bug_report.py` | Sinh bug report + file dán lên GitHub Issues |
| `tc_to_excel.py` | CSV → Excel có sheet Summary |
| `ai_log.py` | Ghi AI_log và sinh AI Audit Report |
| `validate_submission.py` | Kiểm đủ deliverable trước khi nén nộp |

## 8. Bộ công cụ này tái sử dụng được cho bài khác không

Được, và đó là mục tiêu của đề bài (*"You are encouraged to build Agent Skills that can
automatically perform these activities on similar exercises"*). Để áp cho một SUT khác:

1. Viết file `spec/api-N.json` mới theo `spec/_SCHEMA.md` — **đây là việc duy nhất tốn công**.
2. Sửa bảng `SEC_DEFAULT_ASSERT` theo bảng yêu cầu bảo mật của hệ thống đó (**và nhớ bài học ở
   mục 5.2: đọc từ tài liệu, không điền từ trí nhớ**).
3. Sửa `build_env()` cho khớp tài khoản và biến môi trường của hệ thống mới.
4. Toàn bộ phần còn lại — sinh, audit, dựng collection, chạy, tổng hợp, thu bằng chứng bug —
   chạy được ngay không sửa.
