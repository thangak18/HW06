# Hướng dẫn vẽ sơ đồ AI Test Generator — từ A đến Z

**HW06 · 23127195** · Tài liệu **tự chứa** — đọc mỗi file này là vẽ được, không cần mở file nào khác.

---

## 0. Đọc cái này trước

### 0.1 Bạn sắp vẽ cái gì

Một sơ đồ **kiến trúc đường ống (pipeline)** mô tả **bộ sinh test case API bằng AI** — thứ đã
được thiết kế và cài đặt trong bài này. Sơ đồ trả lời câu hỏi: *"Đưa vào tài liệu đặc tả API,
làm sao ra được 144 test case chạy được trên Postman?"*

### 0.2 Vì sao phải tự vẽ

Đề bài mục §7 và §11 ghi:

> *"Provide a **self-drawn** diagram and pseudocode of the design. ('Self-drawn' means you make
> the design decisions; any diagramming tool is fine, but **the diagram itself must not be
> AI-generated**.)"*
>
> *"The AI test-generator diagram, which **must be self-drawn** — designed by you, not generated
> directly by an AI."*

TA **có kiểm tra mục này khi chấm**. Nộp sơ đồ do AI sinh (kể cả Mermaid, SVG, ASCII art) là vi
phạm trực tiếp. Vẽ tay bằng chuột trong draw.io, hoặc vẽ bút trên giấy rồi chụp — cả hai đều hợp lệ.

### 0.3 Mất bao lâu

- Đọc hiểu Phần 1: **10 phút**
- Chọn bố cục (Phần 3): **5 phút**
- Vẽ trong draw.io (Phần 4): **25–35 phút**
- Tự kiểm tra + xuất file (Phần 6, 8): **10 phút**

**Tổng: khoảng 1 tiếng.** Nếu vẽ tay trên giấy A4 thì nhanh hơn, khoảng 25 phút.

### 0.4 Nguyên tắc quan trọng nhất

**Đừng vẽ trước khi hiểu.** Nếu bị gọi vấn đáp (30 % sinh viên, theo §13 của đề), thầy cô sẽ chỉ
vào một ô bất kỳ trên sơ đồ và hỏi *"cái này làm gì?"*. Phần 1 dưới đây là để bạn trả lời được câu
đó. Phần 7 có sẵn 10 câu hỏi vấn đáp thường gặp kèm gợi ý trả lời.

---

# PHẦN 1 — HIỂU CÁI MÌNH SẮP VẼ

*(Đọc hết phần này rồi mới sang phần vẽ. Toàn bộ thông tin cần thiết nằm ở đây, không phải mở file khác.)*

## 1.1 Vấn đề mà bộ sinh này giải quyết

Cách làm ngây thơ: đưa cả tài liệu đặc tả cho ChatGPT/Claude rồi bảo *"sinh toàn bộ test case cho
API này"*. Cách đó hỏng ở **bốn** điểm:

| # | Vấn đề | Biểu hiện cụ thể trong bài này |
|---|---|---|
| 1 | **Không kiểm toán được** | Không biết test case nào phủ yêu cầu nào → không trả lời được "đã phủ đủ chưa" |
| 2 | **Phủ không đều** | AI sinh dày ở chỗ dễ (status code, trường bắt buộc), mỏng ở chỗ khó (chuyển trạng thái, bất biến nghiệp vụ) |
| 3 | **Kỳ vọng bị neo theo hành vi** | Cho AI xem response thật → nó chép lại response đó thành "kỳ vọng" → mọi lỗi thành "đúng thiết kế" |
| 4 | **Sinh thẳng ra JavaScript** | Lỗi cú pháp và lỗi logic bất đồng bộ nằm rải rác trong hàng trăm request, không rà soát nổi |

**Giải pháp trung tâm — cũng là ý chính mà sơ đồ phải truyền đạt:**

> **Chỉ dùng mô hình ngôn ngữ (LLM) cho đúng MỘT việc: đọc hiểu tài liệu.
> Việc đảm bảo phủ đủ thuộc về một danh mục quy tắc tất định do người viết.**

Nói cách khác: LLM giỏi đọc hiểu tiếng người, dở ở tính đầy đủ. Nên giao cho nó đúng phần đọc hiểu,
còn phần "có bỏ sót trường hợp nào không" thì giao cho mã tất định.

## 1.2 Hai nguồn đầu vào — và vì sao phải là HAI

Đây là chi tiết quan trọng, sơ đồ nên thể hiện được.

| Tài liệu | Chứa gì | Thiếu gì |
|---|---|---|
| `api_specification.md` | Hợp đồng dữ liệu: endpoint, tham số, ví dụ body, response 200 | **Không có** SEC-01…SEC-07. Không có bảng mã lỗi. Không có ràng buộc nghiệp vụ |
| `README.md` (bản SRS) | FR-01…FR-24 (ràng buộc nghiệp vụ) + **SEC-01…SEC-07** (yêu cầu bảo mật) | Không mô tả chi tiết hợp đồng API |

**Hệ quả:** nếu chỉ nạp `api_specification.md` cho AI — đúng như câu chữ của đề bài
(*"Provide the SUT's API specification to an AI tool"*) — thì AI **không thể** sinh được test case
bảo mật đúng ngữ cảnh, vì nó không biết SEC-01…SEC-07 tồn tại.

**Ba trong số các bug nghiêm trọng nhất của bài nằm đúng vào chỗ đặc tả API im lặng còn SRS thì nói rõ:**

| Bug | Ràng buộc bị vi phạm | Nằm ở tài liệu nào |
|---|---|---|
| BUG-A1-01 (Critical, leo quyền lên admin) | SEC-06 *"API cập nhật hồ sơ không được cho phép thay đổi trường `role` từ client"* | **Chỉ SRS** |
| BUG-A2-03 (High, ngưỡng đơn hàng) | FR-09 điều kiện C3 *"Tổng đơn hàng **>=** min_order_amount"* | **Chỉ SRS** |
| BUG-A3-02 (High, import không rollback) | FR-16 *"Nếu có lỗi ở bất kỳ dòng nào, toàn bộ import phải được rollback"* | **Chỉ SRS** |

## 1.3 Sáu giai đoạn — nội dung từng giai đoạn

### G1 — TRÍCH XUẤT ĐẶC TẢ 🧠 *(giai đoạn DUY NHẤT dùng LLM)*

- **Đầu vào:** hai tài liệu ở mục 1.2
- **Đầu ra:** một cấu trúc JSON tên là **`EndpointModel`**, gồm:
  - danh sách **tham số** (tên, kiểu dữ liệu, có bắt buộc không, **ràng buộc** kèm **trích dẫn nguyên văn** từ tài liệu)
  - **máy trạng thái** (nếu API có vòng đời trạng thái)
  - **lược đồ response** (thành công / lỗi / các trường cấm xuất hiện)
  - danh sách **SEC** áp dụng được
- **Ràng buộc bắt buộc của giai đoạn này:**
  1. Mỗi ràng buộc **phải kèm trích dẫn nguyên văn** từ tài liệu — ràng buộc không có nguồn là ràng buộc bịa
  2. **Chưa được sinh test case** ở bước này
  3. **Không được xem response thật của hệ thống** — nếu xem, kỳ vọng sẽ bị neo theo hành vi hiện có

### G2 — SINH PHÂN VÙNG MIỀN ⚙️ *(tất định)*

- **Đầu vào:** `EndpointModel.tham_so` **+ DANH MỤC QUY TẮC PHÂN VÙNG**
- **Cách làm:** với **mỗi** tham số, áp **đầy đủ** danh mục dưới đây, không được bỏ mục nào:

```
Mọi tham số      : thiếu trường · null · sai kiểu
Kiểu chuỗi       : chuỗi rỗng · CHỈ KHOẢNG TRẮNG · Unicode tiếng Việt · khoảng trắng bao quanh
                   · payload SQL injection · payload XSS
Kiểu số          : 0 · số âm · vượt Number.MAX_SAFE_INTEGER · số thực · chuỗi-số
Ràng buộc biên   : min−1 · min · min+1 · max−1 · max · max+1        ← BẮT BUỘC đủ 6 điểm
Ràng buộc mẫu    : khớp · không khớp · khớp một phần · khác hoa/thường
Khoá ngoại       : tồn tại · không tồn tại · 0 · âm
```

- **Vì sao danh mục quan trọng:** điểm **`v == min`** chính là điểm phân biệt một cài đặt dùng dấu
  `>` với một cài đặt dùng `>=`. Nếu chỉ bảo AI *"sinh test phân vùng đi"* thì nó bỏ qua điểm này —
  và đó **đúng là BUG-A2-03**. Tính đầy đủ đến từ danh mục, không từ mô hình.
- Cũng lưu ý: `""` và `"   "` là **hai phân vùng khác nhau**, vì `"   "` là *truthy* trong
  JavaScript nên lọt qua phép kiểm tra `if (!x)` → đó là **BUG-A3-06**.

### G3 — SINH CHUỖI CHUYỂN TRẠNG THÁI ⚙️ *(tất định)*

- **Đầu vào:** `EndpointModel.may_trang_thai`
- **Sinh đủ 5 nhóm:**
  1. Mọi cạnh **hợp lệ** trong máy trạng thái
  2. **Mọi** cặp (từ, đến) **không** nằm trong máy trạng thái → phải bị từ chối
  3. Cạnh **tự lặp** — thực hiện lại hành động đã đưa hệ thống đến trạng thái hiện tại
  4. **Rời khỏi trạng thái kết thúc** → phải bị từ chối
  5. **Cập nhật một phần** — chỉ gửi một tập con các trường, các trường còn lại phải giữ nguyên
- **Quy tắc kiểm chứng bắt buộc:** không được coi message trả về là bằng chứng. `"Profile updated"`
  **không** chứng minh dữ liệu đã đổi — phải **đọc lại** tài nguyên để xác nhận.
- Nhóm 5 chính là thứ tìm ra **BUG-A1-05** (cập nhật một phần xoá trắng các trường không gửi).

### G4 — SINH TEST CASE BẢO MẬT ⚙️ *(tất định)*

- **Đầu vào:** bảng **SEC × bề mặt tấn công**
- **Sinh:**

| Mục SEC | Test case sinh ra |
|---|---|
| SEC-02 (yêu cầu JWT) | không token · token rác · **JWT ký bằng khoá sai** · **JWT `alg=none`** |
| SEC-03 (kiểm tra role) | token hợp lệ nhưng `role=user` gọi API admin |
| SEC-05 (parameterized query) | payload SQL injection trên **mọi** tham số kiểu chuỗi |
| SEC-06 (không đổi role) | gửi kèm **trường không có trong đặc tả**: `role`, `id`, `is_admin`, `email` |
| SEC-01 (không plaintext) | response không được chứa `password`, `reset_token`, `login_attempts` |
| IDOR | mọi tham số tên khớp `id` / `user_id` / `owner` |

- **Hai yêu cầu đặc biệt:**
  - Với SEC-06: các trường cần thử là những trường **không có** trong tài liệu → sinh test chỉ theo
    tài liệu sẽ không bao giờ chạm tới chúng. Đó là lý do lỗi loại này hay lọt lưới.
  - Với mọi lỗi phân quyền: **không dừng ở "API có trả 403 không"**, phải đi thêm một bước chứng
    minh **hậu quả quan sát được từ bên ngoài**. Ví dụ: sau khi user thường ghi được dữ liệu, dữ
    liệu đó **có hiện công khai trên trang chủ không?** → chính bước này nâng BUG-A3-01 từ Medium
    lên **Critical**.

### G5 — SINH TEST CASE KIỂM TRA LƯỢC ĐỒ ⚙️ *(tất định)*

- **Đầu vào:** `EndpointModel.lươc_do_response`
- **Sinh theo CẢ HAI chiều:**
  - **Chiều thuận:** response có đủ trường theo hợp đồng · kiểu dữ liệu từng trường đúng ·
    Content-Type là `application/json` · response lỗi cũng khớp lược đồ
  - **Chiều nghịch:** response **KHÔNG** có trường nào **ngoài** hợp đồng · không chứa trường cấm
- **Chiều nghịch là bắt buộc.** Kiểm tra lược đồ chỉ theo chiều thuận sẽ **không bao giờ** phát hiện
  một câu `SELECT *` vô tình làm rò rỉ cột nhạy cảm — chính chiều nghịch tìm ra **BUG-A1-02**
  (API trả về mật khẩu plaintext và `reset_token`).

### G6a — KIỂM TRA IR ⚙️ *(tất định — đây là một CỔNG CHẶN)*

Chặn không cho đi tiếp nếu:

| Điều kiện chặn | Vì sao |
|---|---|
| Thiếu `expected_by_spec` | Kỳ vọng không truy vết được về đặc tả → có thể là kỳ vọng bịa hoặc neo theo hành vi |
| Thiếu nhãn audit hoặc lý do audit | Bước rà soát của con người bị làm hình thức |
| Trùng ID test case | Lỗi kỹ thuật |
| Thiếu phân vùng bắt buộc theo danh mục | Phủ không đủ |
| **Assertion bất đồng bộ không bọc `try { … done(); } catch (e) { done(e); }`** | **Xem mục 1.5 — đây là bài học lớn nhất của bài** |

### G6b — AUDIT CỦA CON NGƯỜI 👤 *(THỦ CÔNG — không tự động hoá được)*

Đây là **ranh giới trách nhiệm** của toàn bộ thiết kế. Với mỗi test case do máy sinh, con người
trả lời 3 câu hỏi rồi gắn nhãn:

| Câu hỏi | Nếu "có" thì gắn nhãn |
|---|---|
| Kỳ vọng lấy từ **hành vi** thay vì từ **đặc tả**? | `INVALID` — viết lại theo tài liệu |
| Đặc tả **im lặng** nhưng test lại ràng buộc một hành vi cụ thể? | `INCOMPLETE` — nới kỳ vọng |
| Test bị **phân loại sai kỹ thuật**? | `INCOMPLETE` — phân loại lại |

Rồi **bổ sung** test case máy không sinh được. Trong bài này, **34 test case do con người thêm** đã
tìm ra **6 / 24 lỗi** mà không nhánh tất định nào ở G2–G5 sinh được:

| Test case người thêm | Lỗi tìm được | Vì sao máy không sinh được |
|---|---|---|
| Cập nhật một phần | BUG-A1-05 mất dữ liệu âm thầm | Đặc tả liệt kê 3 trường, không chỗ nào nói *"client có thể chỉ gửi một trường"* |
| Vị trí dòng lỗi ở **đầu** vs **cuối** mảng | BUG-A3-02 (kết luận đúng về tính nguyên tử) | "Chạy tuần tự rồi dừng" và "giao dịch nguyên tử" cho **cùng** kết quả khi lỗi ở dòng đầu |
| Báo cáo phải nhất quán với CSDL | BUG-A3-02 (mức nghiêm trọng thật) | Cần hiểu người vận hành sẽ **hành động** dựa trên con số `inserted` |
| Bất biến `0 ≤ giảm giá ≤ tổng đơn` | BUG-A2-02 | Kiểm theo **bất biến** bắt được mọi cách tính sai, kể cả cách chưa nghĩ ra |
| Tên toàn khoảng trắng | BUG-A3-06 | Cần biết `"   "` là truthy trong JavaScript — kiến thức về **cài đặt**, không có trong đặc tả |
| Chuỗi tác động của leo quyền | BUG-A1-01 nâng lên Critical | Phải nối nhiều endpoint mới thấy hậu quả thật |

**Kết luận thiết kế: G6b là bắt buộc, không phải tuỳ chọn.** Bộ sinh làm người kiểm thử rảnh tay
khỏi phần cơ học, **không** thay thế họ.

### G6c — BIÊN DỊCH ⚙️ *(tất định)*

Từ **IR đã audit**, sinh ra **bốn hiện vật**:

1. **Postman Collection v2.1** — chạy được bằng Newman
2. **File Excel test case** — cột: kỹ thuật, tham số/phân vùng, kỳ vọng theo đặc tả, nguồn AI/HUMAN, nhãn audit, kết quả chạy, mã lỗi
3. **Bảng tổng hợp báo cáo** — số liệu trong báo cáo
4. **Cổng chặn hồi quy cho CI** — danh sách test case đang đạt

**Ý quan trọng:** cả bốn cùng sinh từ một nguồn → **số liệu trong báo cáo không thể lệch với
collection**. Đây gọi là nguyên tắc *một nguồn sự thật duy nhất*.

## 1.4 IR là gì (khái niệm phải hiểu rõ)

**IR = Intermediate Representation = Biểu diễn trung gian.**

Đó là một file JSON mô tả test case ở mức **ý định**, chưa phải mã chạy được. Ví dụ một test case
trong IR trông như sau:

```json
{
  "id": "TC-A2-013",
  "title": "BVA min: SAVE10 voi total = 300.000 (= min) -> PHAI duoc chap nhan",
  "technique": "domain-partition",
  "param": "total_amount",
  "partition": "Dung bien: total == min_order_amount",
  "source": "AI",
  "audit": { "label": "VALID", "reason": "FR-09 ghi ro dieu kien C3 dung dau >=" },
  "expected_by_spec": "200 OK - don bang dung nguong phai duoc ap ma",
  "known_defect": "BUG-A2-03",
  "request": { "method": "POST", "path": "/api/apply-coupon", "body": { ... } },
  "expect": { "assert": [ { "t": "status", "v": 200 } ] }
}
```

**Vì sao dùng IR thay vì sinh thẳng JavaScript:**

| Lợi ích | Giải thích |
|---|---|
| **Máy kiểm tra được** | JSON có lược đồ → G6a chặn được test case thiếu trường bắt buộc |
| **Không thể sai cú pháp** | Assertion mô tả bằng *descriptor* (`{"t":"eq","path":"final_amount","v":450000}`) chứ không phải mã JS thô |
| **Sửa một lần, áp cho tất cả** | Mọi test case dịch bằng **cùng một khuôn mã** → một lỗi trong khuôn sửa **một lần** cho toàn bộ 144 test case |
| **Người đọc được** | Nhìn IR biết ngay test này kiểm gì, kỳ vọng lấy từ đâu, ai viết, đã audit chưa |

## 1.5 Bài học lớn nhất — hai lỗi của CHÍNH bộ test

*(Nếu vấn đáp, đây là phần đáng kể nhất. Nắm chắc.)*

**Lỗi 1 — Assertion bất đồng bộ nuốt mất lỗi.**

AI sinh assertion theo mẫu:

```js
pm.test('...', function (done) {
    pm.sendRequest(opts, function (err, res) {
        pm.expect(res.json().role).to.eql('user');   // ném lỗi -> done() KHÔNG BAO GIỜ chạy
        done();
    });
});
```

- Khi assertion **đạt** → `done()` chạy → Newman ghi **PASS**. Trông bình thường.
- Khi assertion **hỏng** → ngoại lệ ném **trước** `done()` → Newman **âm thầm bỏ qua** test đó:
  **không PASS, không FAIL, biến mất khỏi báo cáo.**

**Hậu quả thật:** test cho **BUG-A1-01** (leo quyền lên admin — lỗi nghiêm trọng nhất của cả bài)
ban đầu hiện ra như **"đã pass"**.

**Phát hiện bằng cách nào:** đối chiếu báo cáo Newman với kết quả `curl` thủ công. `curl` cho thấy
`role = admin`, trong khi Newman không có dòng FAIL nào tương ứng.
**Dấu hiệu là SỰ VẮNG MẶT của một assertion, không phải một assertion sai.**

**Sửa:** bọc `try { … done(); } catch (e) { done(e); }` cho **32 assertion**. Vì mọi assertion đều
sinh từ **một khuôn mã dùng chung** nên chỉ sửa một chỗ. → Đây chính là bằng chứng cho lợi ích của IR.
Và G6a nay **chặn** mọi assertion bất đồng bộ thiếu try/catch.

**Lỗi 2 — Dữ liệu chuẩn bị trong pre-request script không đáng tin.**

Chụp mốc số lượng bản ghi bằng `pm.sendRequest` trong pre-request script **không đảm bảo hoàn tất**
trước khi request chính được gửi → 3 kết quả **FAIL giả**. Đã thay bằng **26 request `[SETUP]`
tường minh**.

**Nguyên tắc rút ra:** *AI đáng tin ở việc phủ có hệ thống, nhưng không đáng tin ở việc tự kiểm
chứng chính nó.*

## 1.6 Các con số thật của bài (cần cho sơ đồ)

| Chỉ số | Giá trị |
|---|---|
| Số API kiểm thử | 3 (FR-04 Pool A · FR-09 Pool B · FR-16 Pool C) |
| Test case do AI sinh | **110** |
| Test case do con người thêm | **34** |
| **Tổng test case** | **144** |
| Request thi hành | 241 |
| Assertion | 746 |
| PASS / FAIL | 92 / 52 |
| **Lỗi thật tìm được** | **24** (4 Critical · 7 High · 8 Medium · 5 Low) |
| Lỗi chỉ tìm được nhờ test case con người viết | **6 / 24** |
| Test case AI phải hiệu chỉnh khi audit | 9 / 110 |
| Cổng chặn CI (baseline) | 92 test case · 550 assertion · 0 FAIL |

---

# PHẦN 2 — DANH SÁCH THÀNH PHẦN PHẢI CÓ TRÊN SƠ ĐỒ

Đây là **danh sách nội dung**, không phải bản vẽ. Hình khối, màu sắc, cách sắp xếp là **quyết định
của bạn** — và chính điều đó làm nó thành "self-drawn".

## 2.1 Bắt buộc (thiếu là mất điểm)

- [ ] **Hai nguồn đầu vào tách biệt:** `api_specification.md` và `README.md (SRS)`
      → phải thấy rõ đây là **hai** tài liệu khác nhau
- [ ] **Sáu giai đoạn** với tên đúng: G1 Trích xuất · G2 Phân vùng miền · G3 Chuyển trạng thái ·
      G4 Bảo mật · G5 Lược đồ · G6 (a/b/c)
- [ ] **Phân biệt trực quan "dùng LLM" ↔ "mã tất định"** — chỉ **G1** dùng LLM.
      Đây là **ý trung tâm**, phải nhìn phát ra ngay
- [ ] **IR** vẽ như một **hiện vật riêng** nằm giữa luồng (không phải một mũi tên). Ghi rõ là JSON
- [ ] **G6b Audit của con người** đánh dấu là **thủ công / bắt buộc**, khác biệt rõ với các bước tự động
- [ ] **Bốn đầu ra** từ IR: Postman Collection · Excel test case · Bảng tổng hợp báo cáo · Cổng chặn CI
- [ ] **Vòng phản hồi** từ Newman quay lại cổng chặn CI

## 2.2 Nên có (làm sơ đồ thuyết phục hơn nhiều)

- [ ] **Danh mục quy tắc phân vùng** vẽ như một **đầu vào thứ hai** của G2
      → cho thấy tính đầy đủ đến từ danh mục, không từ mô hình
- [ ] **Cổng kiểm tra G6a** với các điều kiện chặn ghi ra
- [ ] **Số liệu thật** ghi trên sơ đồ: `144 test case → 24 lỗi`
- [ ] **Chú thích (legend)** giải thích quy ước màu — TA nhìn cái này đầu tiên
- [ ] Ghi chú nhỏ ở G1: *"không được xem response thật"*

## 2.3 Tuyệt đối không được có

- [ ] ~~Sơ đồ tải từ mạng hoặc do AI sinh~~ → vi phạm §11
- [ ] ~~Ảnh chụp sơ đồ của người khác~~
- [ ] ~~Mermaid render sẵn dán vào~~

---

# PHẦN 3 — CHỌN BỐ CỤC (bạn chọn 1 trong 3)

Ba phương án dưới đây có ưu nhược khác nhau. **Chọn một** — việc chọn này là một trong những
"design decision" mà đề bài muốn bạn tự làm.

## Phương án A — Dòng chảy dọc, chia 3 băng ngang ⭐ *dễ vẽ nhất*

**Cấu trúc:** trên xuống dưới, ba băng.

- **Băng trên:** 2 hộp tài liệu nằm cạnh nhau → cùng đổ vào G1
- **Băng giữa:** G1 (màu LLM) → 4 hộp G2/G3/G4/G5 (màu tất định) → cùng đổ vào hộp IR ở chính giữa.
  Danh mục quy tắc đặt bên trái, mũi tên trỏ vào G2
- **Băng dưới:** IR → G6a → G6b → G6c → 4 hiện vật đầu ra. Mũi tên phản hồi từ Newman đi ngược lên

| Ưu | Nhược |
|---|---|
| Dễ vẽ, dễ đọc, hợp giấy A4 dọc | Hơi cao, có thể phải thu nhỏ chữ |
| Thứ tự thời gian rõ ràng | |

## Phương án B — Dòng chảy ngang, trái sang phải

**Cấu trúc:** đầu vào bên trái → pipeline ở giữa → đầu ra bên phải.

| Ưu | Nhược |
|---|---|
| Hợp slide 16:9 và giấy A4 nằm ngang | 4 hộp G2–G5 phải xếp dọc, dễ chật |
| Nhìn như một "dây chuyền" rất trực quan | Vòng phản hồi phải vòng dài |

## Phương án C — Sơ đồ băng bơi (swimlane) theo trách nhiệm

**Cấu trúc:** 3 làn ngang chồng lên nhau:

- Làn 1 — **AI (LLM)**: chỉ có G1
- Làn 2 — **Mã tất định**: G2, G3, G4, G5, G6a, G6c
- Làn 3 — **Con người**: G6b + việc rà soát `EndpointModel`

| Ưu | Nhược |
|---|---|
| **Thể hiện ý "ai làm gì" mạnh nhất** — đúng trọng tâm thiết kế | Khó vẽ hơn, mũi tên phải nhảy làn nhiều |
| Gây ấn tượng tốt khi vấn đáp | Cần cẩn thận kẻo rối |

> **Gợi ý:** nếu bạn tự tin thì chọn **C** — nó nói đúng cái ý quan trọng nhất của thiết kế
> (ranh giới trách nhiệm giữa AI / mã / con người). Nếu muốn chắc ăn và nhanh thì chọn **A**.

---

# PHẦN 4 — VẼ BẰNG DRAW.IO, TỪNG BƯỚC

*(Nếu vẽ tay trên giấy thì bỏ qua phần này, nhảy tới Phần 5 và Phần 6.)*

## 4.1 Mở draw.io

1. Mở trình duyệt, vào **https://app.diagrams.net**
   *(Không cần tài khoản, không cần cài đặt, miễn phí.)*
2. Hộp thoại hỏi lưu ở đâu → chọn **Device** (lưu về máy)
3. Bấm **Create New Diagram**
4. Đặt tên file: `ai_test_generator_diagram.drawio`
5. Chọn mẫu **Blank Diagram** → bấm **Create**

## 4.2 Chuẩn bị khung vẽ

1. Menu **File → Page Setup**
2. Chọn khổ **A4**, hướng **Landscape** (nằm ngang) nếu chọn phương án B hoặc C;
   **Portrait** (dọc) nếu chọn phương án A
3. Bật lưới cho dễ căn: menu **View → Grid** (nếu chưa bật)
4. Bật bắt điểm: **View → Snap to Grid**

## 4.3 Vẽ một ô (thao tác cơ bản, làm nhiều lần)

**Cách nhanh nhất:**

1. **Nhấn đúp** vào chỗ trống trên canvas → hiện ô nhập → gõ tên ô → Enter
   → draw.io tự tạo một hình chữ nhật có chữ

**Cách chủ động hơn:**

1. Panel bên trái, ô **Search Shapes** → gõ `rectangle` (hoặc `rounded`, `cylinder`, `document`)
2. **Kéo thả** hình vào canvas
3. **Nhấn đúp** vào hình → gõ chữ → nhấn `Esc` để thoát chế độ gõ

**Chỉnh kích thước / vị trí chính xác:**

- Chọn hình → panel bên phải → tab **Arrange** → có ô nhập **Size** (Width, Height) và
  **Position** (X, Y)
- Muốn nhiều ô bằng nhau: chọn ô mẫu → `Ctrl+C` → `Ctrl+V` → sửa chữ bên trong

## 4.4 Tô màu (phân biệt LLM / tất định / con người)

1. Chọn hình (hoặc chọn nhiều hình bằng cách giữ `Shift` rồi bấm)
2. Panel bên phải → tab **Style**
3. Bấm ô màu bên cạnh chữ **Fill** → chọn màu → hoặc bấm **Edit Style** để gõ mã màu
4. Tương tự với **Line** (màu viền)

**Bảng màu gợi ý** (bạn có thể đổi, miễn là nhất quán và có legend):

| Loại | Fill | Line | Ghi chú |
|---|---|---|---|
| 🧠 Dùng LLM (G1) | `#FFF2CC` vàng nhạt | `#D6B656` | Nổi bật, khác hẳn phần còn lại |
| ⚙️ Mã tất định (G2–G5, G6a, G6c) | `#DAE8FC` xanh dương nhạt | `#6C8EBF` | Màu chủ đạo |
| 👤 Con người (G6b) | `#F8CECC` đỏ/hồng nhạt | `#B85450` | Báo hiệu "dừng lại, cần người" |
| 📄 Tài liệu đầu vào | `#F5F5F5` xám nhạt | `#666666` | Dùng hình dạng *Document* cho ra chất tài liệu |
| 📦 IR (hiện vật trung tâm) | `#D5E8D4` xanh lá nhạt | `#82B366` | Cho to hơn các ô khác để thấy nó là trung tâm |
| 🎯 Đầu ra | `#E1D5E7` tím nhạt | `#9673A6` | |

> **Mẹo:** dùng đúng **3 màu chính** cho 3 loại trách nhiệm (LLM / tất định / con người) là đủ.
> Nhiều màu quá làm loãng thông điệp.

## 4.5 Nối mũi tên

1. Rê chuột lên **mép** một hình → xuất hiện **4 mũi tên xanh** và viền xanh
2. **Bấm giữ** vào mép rồi **kéo** sang hình đích → thả ra
3. Muốn đổi kiểu mũi tên: chọn mũi tên → panel phải → tab **Style** →
   chọn kiểu đường (thẳng / gấp khúc / cong), độ dày, đầu mũi tên
4. Muốn ghi chữ trên mũi tên: **nhấn đúp** vào giữa mũi tên → gõ chữ

**Quy ước gợi ý cho mũi tên:**

| Loại luồng | Kiểu | Vì sao |
|---|---|---|
| Luồng dữ liệu chính | Nét liền, đậm (2pt) | Đường đi chính |
| Danh mục quy tắc → G2 | Nét đứt | Đây là "đầu vào cấu hình", không phải dữ liệu chảy qua |
| Vòng phản hồi Newman → cổng CI | Nét đứt, màu khác (ví dụ cam) | Phân biệt với luồng xuôi |

## 4.6 Vẽ chú thích (legend) — **đừng bỏ qua bước này**

1. Vẽ một hình chữ nhật ở góc dưới (hoặc góc trên) canvas
2. Bên trong, xếp 3–4 ô vuông nhỏ, mỗi ô tô một màu, bên cạnh ghi chữ:
   - 🟨 `Giai đoạn dùng LLM`
   - 🟦 `Giai đoạn mã tất định`
   - 🟥 `Bước thủ công (con người)`
   - ⬜ `Tài liệu / hiện vật`
3. Chọn hết → `Ctrl+G` để **nhóm** lại thành một khối, dễ di chuyển

## 4.7 Thêm tiêu đề và thông tin bài

Vẽ một ô text ở trên cùng (dùng shape **Text** trong panel trái, hoặc nhấn đúp rồi xoá viền):

```
Bộ sinh test case API bằng AI
HW06 · 23127195 · SUT: EShop
144 test case → 24 lỗi
```

## 4.8 Phím tắt hữu ích

| Phím | Tác dụng |
|---|---|
| `Ctrl + Shift + H` | Thu vừa màn hình (fit page) — dùng liên tục |
| `Ctrl + G` | Nhóm các hình đã chọn |
| `Ctrl + Shift + G` | Bỏ nhóm |
| `Ctrl + D` | Nhân bản hình đang chọn |
| `Alt + Shift + H` | Căn đều theo chiều ngang |
| `Alt + Shift + V` | Căn đều theo chiều dọc |
| `Ctrl + Z` | Hoàn tác |
| Giữ `Shift` khi kéo | Kéo theo đường thẳng |
| Giữ `Alt` khi kéo hình | Bỏ qua bắt lưới, đặt tự do |

## 4.9 Thứ tự vẽ đề xuất (tránh phải sắp lại)

1. Vẽ **hộp IR ở giữa canvas trước** — nó là trung tâm, mọi thứ xoay quanh nó
2. Vẽ **2 hộp tài liệu** ở đầu luồng
3. Vẽ **G1**, nối 2 tài liệu vào G1
4. Vẽ **4 hộp G2–G5**, nối G1 → từng hộp, rồi từng hộp → IR
5. Vẽ **danh mục quy tắc**, nối nét đứt vào G2
6. Vẽ **G6a → G6b → G6c** phía sau IR
7. Vẽ **4 hiện vật đầu ra**
8. Vẽ **vòng phản hồi** từ Newman về cổng CI
9. **Tô màu** toàn bộ (làm sau cùng, nhanh hơn nhiều so với tô từng ô lúc vẽ)
10. Vẽ **legend** và **tiêu đề**
11. Căn chỉnh: chọn nhóm ô cùng hàng → `Alt+Shift+H`

---

# PHẦN 5 — QUY ƯỚC THẨM MỸ

Sơ đồ đẹp không phải để làm màu — nó giúp TA đọc nhanh và giúp bạn giải thích trôi khi vấn đáp.

| Yếu tố | Khuyến nghị |
|---|---|
| **Cỡ chữ trong ô** | 11–13 pt. Tiêu đề ô đậm, ghi chú nhỏ 9 pt |
| **Cỡ chữ tiêu đề sơ đồ** | 18–22 pt |
| **Khoảng cách giữa các ô** | Tối thiểu 30 px — đừng để dính nhau |
| **Kích thước ô** | Các ô cùng cấp phải **bằng nhau** (ví dụ G2–G5 cùng 160×70) |
| **Số chữ trong một ô** | Tối đa ~8 từ. Dài hơn thì tách thành ghi chú bên cạnh |
| **Độ dày mũi tên** | 1.5–2 pt. Mũi tên chính đậm hơn mũi tên phụ |
| **Số màu** | 3 màu chính + 1–2 màu phụ. Đừng quá 5 |
| **Căn lề** | Các ô cùng hàng phải thẳng hàng — dùng `Alt+Shift+H` / `Alt+Shift+V` |
| **Khoảng trắng** | Chừa lề quanh sơ đồ, đừng vẽ sát mép |

**Ba lỗi hay gặp cần tránh:**

1. **Nhồi quá nhiều chữ vào ô** → nhìn như một đoạn văn có viền. Chữ trong ô là **nhãn**, không phải mô tả.
2. **Mũi tên cắt chéo qua ô khác** → chọn mũi tên, đổi kiểu đường sang gấp khúc (orthogonal) và
   kéo điểm giữa để tránh.
3. **Không có legend** → TA không biết màu vàng nghĩa là gì, mất luôn ý chính của sơ đồ.

---

# PHẦN 6 — TỰ KIỂM TRA TRƯỚC KHI NỘP

Đọc lại sơ đồ và tự trả lời. Nếu có câu nào "không" → sửa.

## 6.1 Về nội dung

- [ ] Có **hai** hộp tài liệu đầu vào riêng biệt không?
- [ ] Có đủ **sáu** giai đoạn G1–G6 không?
- [ ] Nhìn vào sơ đồ, **trong 3 giây** có nhận ra "chỉ G1 dùng LLM" không?
- [ ] **IR** có được vẽ như một hiện vật riêng (hộp), không phải một mũi tên không?
- [ ] **G6b** có được đánh dấu là bước **thủ công** không?
- [ ] Có đủ **bốn** đầu ra không?
- [ ] Có **vòng phản hồi** từ Newman không?
- [ ] Có **legend** giải thích màu không?

## 6.2 Về hình thức

- [ ] Chữ có đọc được khi thu nhỏ về khổ A4 không? *(Thử: `Ctrl+Shift+H` rồi nheo mắt nhìn)*
- [ ] Các ô cùng cấp có cùng kích thước không?
- [ ] Có mũi tên nào cắt chéo qua ô khác không?
- [ ] Có ô nào chứa quá 8 từ không?
- [ ] Có tiêu đề + MSSV **23127195** trên sơ đồ không?

## 6.3 Phép thử quan trọng nhất

> **Che sơ đồ đi, thử kể lại toàn bộ đường ống bằng lời trong 60 giây.**
> Nếu kể được trôi chảy → bạn hiểu nó, và vấn đáp sẽ ổn.
> Nếu vấp → đọc lại Phần 1 mục 1.3 rồi vẽ lại.

---

# PHẦN 7 — 10 CÂU HỎI VẤN ĐÁP CÓ THỂ BỊ HỎI

*(§13 của đề: 30 % sinh viên bị gọi vấn đáp 5–7 phút trong tuần sau deadline.)*

**1. "IR là gì? Vì sao không sinh thẳng ra mã Postman?"**
> IR là biểu diễn trung gian dạng JSON, mô tả test case ở mức ý định chứ chưa phải mã. Ba lý do:
> (a) JSON có lược đồ nên máy kiểm tra được — cổng G6a chặn được test case thiếu trường bắt buộc;
> (b) assertion mô tả bằng descriptor nên không thể sai cú pháp;
> (c) quan trọng nhất — mọi test case dịch bằng cùng một khuôn mã, nên một lỗi trong khuôn sửa
> một lần cho cả 144 test case. Em đã dùng đúng lợi ích này: 32 assertion bị lỗi bất đồng bộ được
> sửa bằng một thay đổi duy nhất.

**2. "Vì sao chỉ G1 dùng LLM?"**
> Vì LLM giỏi đọc hiểu ngôn ngữ tự nhiên nhưng dở ở tính đầy đủ — nó sinh dày ở chỗ dễ và bỏ sót
> chỗ khó. Nên em giao cho nó đúng việc đọc hiểu tài liệu, còn tính đầy đủ giao cho một danh mục
> quy tắc tất định. Ví dụ cụ thể: nếu chỉ bảo AI "sinh test phân vùng", nó bỏ qua điểm `v == min` —
> mà đó chính là điểm phân biệt cài đặt `>` với `>=`, và là lỗi BUG-A2-03 em tìm được.

**3. "Tại sao phải nạp cả hai tài liệu?"**
> Vì `api_specification.md` không hề chứa SEC-01 đến SEC-07 — chúng nằm ở bản SRS. Nếu chỉ nạp
> đặc tả API thì AI không biết các yêu cầu bảo mật tồn tại. Ba lỗi nghiêm trọng nhất của bài
> (BUG-A1-01, BUG-A2-03, BUG-A3-02) đều nằm đúng chỗ đặc tả API im lặng còn SRS thì nói rõ.

**4. "G6b có tự động hoá được không?"**
> Không. Và em có bằng chứng: 34 test case do em tự viết đã tìm ra 6 trên 24 lỗi mà không nhánh
> tất định nào ở G2–G5 sinh được, vì chúng đòi hiểu **hậu quả nghiệp vụ** chứ không phải cấu trúc
> dữ liệu. Ví dụ: đặc tả liệt kê 3 trường của hồ sơ, nhưng không chỗ nào nói "client có thể chỉ gửi
> một trường" — nghĩ ra tình huống đó là việc của con người.

**5. "Bạn đã tìm ra lỗi nào của chính bộ test chưa?"**
> Có, hai lỗi. Nghiêm trọng nhất: assertion bất đồng bộ gọi `pm.sendRequest` rồi đặt `done()` sau
> `pm.expect`. Khi assertion đạt thì chạy đúng, nhưng khi hỏng thì ngoại lệ ném trước `done()` và
> Newman âm thầm bỏ qua test đó — không PASS, không FAIL. Hậu quả là test cho lỗi leo quyền lên
> admin ban đầu hiện ra như đã pass. Em phát hiện khi đối chiếu báo cáo Newman với `curl` thủ công:
> dấu hiệu là sự vắng mặt của một assertion, không phải một assertion sai.

**6. "Danh mục quy tắc phân vùng gồm những gì?"**
> Bốn nhóm. Phổ quát: thiếu trường, null, sai kiểu. Theo kiểu: chuỗi rỗng, chỉ khoảng trắng,
> Unicode, SQLi, XSS cho chuỗi; 0, số âm, vượt số nguyên an toàn, số thực, chuỗi-số cho số.
> Theo ràng buộc: sáu điểm biên min−1/min/min+1/max−1/max/max+1; khớp mẫu / không khớp / khớp một
> phần; khoá ngoại tồn tại / không tồn tại / 0 / âm. Và với API nhận mảng thì nhân thêm chiều số
> phần tử.

**7. "Vì sao `""` và `"   "` là hai phân vùng khác nhau?"**
> Vì `"   "` là truthy trong JavaScript, nên nó lọt qua phép kiểm tra `if (!x)` mà `""` thì không.
> Đúng khe hở này tạo ra BUG-A3-06 — sản phẩm không tên vẫn được import vào hệ thống.

**8. "Vì sao kiểm tra lược đồ phải theo hai chiều?"**
> Chiều thuận kiểm "có đủ trường mong đợi không". Chiều nghịch kiểm "có trường nào thừa không".
> Chỉ chiều nghịch mới phát hiện được một câu `SELECT *` vô tình rò rỉ cột nhạy cảm — đó là
> BUG-A1-02, API trả về mật khẩu plaintext và `reset_token`.

**9. "Cổng chặn CI hoạt động thế nào?"**
> SUT có 24 lỗi nên chạy cả 144 test case thì pipeline luôn đỏ, mà pipeline luôn đỏ thì không ai
> nhìn nữa. Nên em tách hai tầng: tầng một chỉ gồm 92 test case đang đạt và bắt buộc xanh — nó phát
> hiện hồi quy; tầng hai chạy đầy đủ nhưng không chặn build. Khi một lỗi được sửa, test case tương
> ứng được thêm vào tầng một để bảo vệ bản sửa đó.

**10. "Nếu làm lại, bạn sẽ thay đổi gì?"**
> Em sẽ đưa bước kiểm tra assertion bất đồng bộ vào cổng G6a ngay từ đầu thay vì phát hiện sau khi
> chạy. Và em sẽ tự viết prompt cho từng bước một cách tách bạch hơn thay vì để AI tự phân rã —
> đúng tinh thần mục §2 của đề bài.

---

# PHẦN 8 — XUẤT FILE VÀ HOÀN TẤT

## 8.1 Xuất ảnh PNG từ draw.io

1. Menu **File → Export as → PNG...**
2. Trong hộp thoại, đặt:

| Tuỳ chọn | Giá trị | Vì sao |
|---|---|---|
| **Zoom** | `200%` | Ảnh nét, không vỡ khi in |
| **Border Width** | `10` | Chừa lề, không dính mép |
| **Size** | `Page` hoặc `Diagram` | `Diagram` cắt sát nội dung |
| **Transparent Background** | **BỎ TICK** | Nền trắng, tránh chữ đen trên nền đen khi in |
| **Appearance** | `Light` | |
| **Shadow / Grid** | Bỏ tick | Sạch hơn |

3. Bấm **Export** → **Download**
4. Đổi tên file thành: **`ai_test_generator_diagram.png`**

## 8.2 Lưu file nguồn (quan trọng — chứng minh bạn tự dựng)

1. Menu **File → Save as...** → lưu file `.drawio`
2. Đặt tên: `ai_test_generator_diagram.drawio`

## 8.3 Đặt file vào đúng chỗ

Chép **cả hai** file vào:

```
d:\Kiem_thu\HW6\HW06\23127195\agent-skill\diagram\
    ├── ai_test_generator_diagram.png       ← ảnh nộp
    └── ai_test_generator_diagram.drawio    ← file nguồn, chứng minh tự dựng
```

## 8.4 Nhúng vào báo cáo chính

Mở file `d:\Kiem_thu\HW6\HW06\23127195\docs\00_MAIN_REPORT.md`, tìm mục
**"4. Agent Skill — bộ sinh test case API bằng AI"**, tìm đoạn có chữ
*"Sơ đồ sẽ được nhúng vào mục này sau khi vẽ xong"* và **thay** đoạn cảnh báo đó bằng:

```markdown
![Sơ đồ bộ sinh test case API](../agent-skill/diagram/ai_test_generator_diagram.png)

*Sơ đồ do sinh viên 23127195 tự vẽ bằng draw.io. File nguồn:
[`ai_test_generator_diagram.drawio`](../agent-skill/diagram/ai_test_generator_diagram.drawio)*
```

## 8.5 Xuất lại PDF và commit

Mở terminal:

```bash
cd d:/Kiem_thu/HW6/HW06/23127195
python scripts/export_pdf.py

cd d:/Kiem_thu/HW6/HW06
git add 23127195/agent-skill/diagram/ 23127195/docs/00_MAIN_REPORT.md 23127195/pdf/
git commit -m "docs(agent-skill): bo sung so do thiet ke tu ve (yeu cau muc 11 cua de bai)"
git push
```

## 8.6 Kiểm tra lần cuối

- [ ] File `ai_test_generator_diagram.png` đã có trong `agent-skill/diagram/`
- [ ] Mở ảnh lên, chữ đọc được rõ ràng
- [ ] Đã nhúng vào `docs/00_MAIN_REPORT.md` §4 và ảnh hiển thị được
- [ ] Đã xuất lại PDF (PDF phải có ảnh sơ đồ)
- [ ] Đã commit và push

---

## Phụ lục — Nếu vẽ tay trên giấy

Hoàn toàn hợp lệ, và có khi còn thuyết phục hơn về mặt "self-drawn".

1. Dùng **giấy A4 trắng**, bút bi/bút kim đen cho khung và chữ
2. Dùng **3 màu bút highlight** (vàng / xanh / hồng) đúng theo quy ước ở mục 4.4
3. Viết chữ **in hoa** cho tên giai đoạn để dễ đọc khi chụp
4. **Vẽ nháp bằng bút chì trước**, xong mới đồ bút mực — tránh phải vẽ lại
5. Nhớ vẽ **legend** ở góc và ghi **MSSV 23127195** + ngày
6. Chụp ảnh: đặt giấy trên mặt phẳng, **ánh sáng đều, không bóng tay**, chụp thẳng từ trên xuống
7. Dùng app quét tài liệu (Microsoft Lens, Adobe Scan, CamScanner) để nắn phối cảnh và tăng tương phản
8. Xuất PNG, đặt tên `ai_test_generator_diagram.png`, làm tiếp từ mục 8.3
