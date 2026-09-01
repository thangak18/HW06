---
name: api-test-generator
description: Sinh bộ test case API đầy đủ từ tài liệu đặc tả (đặc tả API + SRS), phủ domain partition, state transition, security và schema validation, rồi biên dịch ra Postman Collection chạy được bằng Newman. Dùng khi cần kiểm thử một REST API có tài liệu đặc tả — đặc biệt khi cần phủ có hệ thống và có thể kiểm toán được, thay vì sinh test case ngẫu hứng.
---

# API Test Generator

Sinh test case API từ tài liệu đặc tả theo một đường ống có kiểm toán được.
Thiết kế đầy đủ nằm ở [`DESIGN.md`](./DESIGN.md); pseudocode ở
[`pseudocode/generator_pseudocode.md`](./pseudocode/generator_pseudocode.md).

## Nguyên tắc cốt lõi

**Chỉ dùng mô hình ngôn ngữ cho đúng một việc: đọc hiểu tài liệu.** Việc đảm bảo phủ đủ
thuộc về một danh mục quy tắc tất định. Đừng bao giờ hỏi mô hình *"hãy nghĩ ra các test case"* —
hãy trích xuất cấu trúc từ tài liệu, rồi áp danh mục phân vùng bắt buộc lên cấu trúc đó.

## Quy trình

### Bước 1 — Nạp **toàn bộ** tài liệu, không chỉ đặc tả API

Đặc tả API thường chỉ mô tả *hợp đồng dữ liệu*. Các ràng buộc nghiệp vụ và yêu cầu bảo mật
lại nằm ở tài liệu SRS. Chỉ nạp một tài liệu là mất hẳn một chiều kiểm thử.

> Trong HW06, `api_specification.md` **không hề chứa** SEC-01…SEC-07 — chúng nằm ở `README.md`.
> Ba trong số các lỗi nghiêm trọng nhất tìm được nằm đúng vào chỗ đặc tả API im lặng còn SRS thì nói rõ.

Trước khi sinh, hãy trả lời: *ràng buộc cho tham số này nằm ở tài liệu nào?* Nếu không tìm
thấy ở đâu cả, ghi **"KHÔNG ĐƯỢC ĐẶC TẢ"** — đừng suy đoán.

### Bước 2 — Trích xuất `EndpointModel` (đây là chỗ duy nhất dùng LLM)

Sinh JSON theo lược đồ trong [`pseudocode/generator_pseudocode.md`](./pseudocode/generator_pseudocode.md).
Yêu cầu bắt buộc: **mọi ràng buộc phải kèm trích dẫn nguyên văn** từ tài liệu. Ràng buộc
không có nguồn là ràng buộc bịa.

Ở bước này **không được xem response thật của hệ thống**. Nếu xem, kỳ vọng sẽ bị neo theo
hành vi hiện có và mọi lỗi sẽ được hợp thức hoá thành "đúng như thiết kế".

### Bước 3 — Sinh test case bằng mã tất định

```bash
python agent-skill/pseudocode/generator.py endpoint_model.json -o ir.json
```

Bộ sinh áp bốn danh mục quy tắc — chi tiết ở `DESIGN.md` §2 (N2):

- **Phân vùng miền** — thiếu trường · null · sai kiểu · rỗng · chỉ khoảng trắng · Unicode ·
  biên `min−1/min/min+1/max−1/max/max+1` · khớp mẫu / không khớp / khớp một phần · khoá ngoại
- **Chuyển trạng thái** — mọi cạnh hợp lệ · **mọi** cạnh không hợp lệ · cạnh tự lặp ·
  rời trạng thái kết thúc · bảo toàn trường khi cập nhật một phần
- **Bảo mật** — không token · token rác · JWT ký sai khoá · `alg=none` · sai vai trò ·
  mass assignment · IDOR · SQLi trên mọi tham số chuỗi
- **Lược đồ** — khớp lược đồ · kiểu từng trường · **không có trường thừa** · không rò rỉ trường cấm

### Bước 4 — Chạy bộ kiểm tra IR (bắt buộc)

Bộ kiểm tra chặn build nếu:
- thiếu `expected_by_spec` (kỳ vọng không truy vết được về đặc tả);
- thiếu nhãn audit hoặc lý do audit;
- **assertion bất đồng bộ không bọc `try { … done(); } catch (e) { done(e); }`.**

Điều kiện cuối cùng bắt nguồn từ một sự cố thật: khi assertion bất đồng bộ hỏng, ngoại lệ
được ném trước `done()` và Newman **âm thầm bỏ qua** test đó — không PASS, không FAIL. Lỗi
nghiêm trọng nhất trong đợt kiểm thử ban đầu hiện ra là "đã pass" chính vì lý do này.

### Bước 5 — Audit của con người (không tự động hoá được)

Với mỗi test case do máy sinh, trả lời ba câu hỏi rồi gắn nhãn:

| Câu hỏi | Nếu "có" |
|---|---|
| Kỳ vọng lấy từ **hành vi** thay vì từ **đặc tả**? | `INVALID` — viết lại theo tài liệu |
| Đặc tả **im lặng** nhưng test lại ràng buộc một hành vi cụ thể? | `INCOMPLETE` — nới thành "không được 5xx" hoặc liệt kê status chấp nhận được |
| Test bị **phân loại sai kỹ thuật**? | `INCOMPLETE` — phân loại lại |

Rồi **bổ sung** các test case máy không sinh được. Sáu câu hỏi dưới đây là những câu đã tìm
ra lỗi thật trong HW06:

1. *Nếu client chỉ gửi **một phần** dữ liệu thì sao?* → tìm ra lỗi mất dữ liệu âm thầm
2. ***Vị trí*** *của phần tử lỗi có làm đổi kết luận không?* → phân biệt "dừng khi gặp lỗi" với "giao dịch nguyên tử"
3. *Báo cáo trả về có **nhất quán** với trạng thái thật của CSDL không?* → tìm ra lỗi báo cáo sai lệch
4. *Có **bất biến** nghiệp vụ nào bắt được mọi cách tính sai không?* → `0 ≤ giảm giá ≤ tổng đơn` bắt được giảm giá âm
5. *Hậu quả nghiệp vụ **thật sự** là gì?* → biến "API trả 403 không?" thành "hàng giả có lên sàn không?"
6. *Ngữ nghĩa của **ngôn ngữ cài đặt** có tạo khe hở nào không?* → `" "` là truthy trong JavaScript

### Bước 6 — Biên dịch và chạy

```bash
python postman/scripts/build_collections.py     # IR -> Postman Collection v2.1
bash scripts/run_newman.sh                      # restart SUT roi chay Newman
python scripts/export_testcases.py              # IR + ket qua -> Excel + bang tong hop
python postman/scripts/build_baseline.py --refresh   # cap nhat cong chan hoi quy cho CI
```

## Điều cần tránh

| Đừng | Vì |
|---|---|
| Cho mô hình xem response thật trước khi sinh xong test case | Kỳ vọng sẽ bị neo theo hành vi, mọi lỗi thành "đúng thiết kế" |
| Để mô hình sinh thẳng ra JavaScript | Lỗi cú pháp và lỗi bất đồng bộ rải rác, không rà soát nổi |
| Bỏ qua phân vùng "đúng tại biên" (`v == min`) | Đây chính là điểm phân biệt `>` với `>=` |
| Kiểm tra lược đồ chỉ theo chiều "có đủ trường" | Không bao giờ phát hiện `SELECT *` làm rò rỉ cột nhạy cảm |
| Dừng ở "API có trả 403 không" | Chưa chứng minh được mức độ nghiêm trọng |
| Đặt dữ liệu chuẩn bị trong pre-request script | Bất đồng bộ, không đảm bảo hoàn tất trước request chính |
| Coi bước audit là tuỳ chọn | 6/24 lỗi của HW06 chỉ tìm ra nhờ test case do người viết |

## Cấu trúc đầu ra

```
testcases/<api>_testcases.json      IR — nguồn sự thật duy nhất
postman/collections/*.json          Postman Collection v2.1 (sinh ra)
postman/data/*.csv                  Dữ liệu cho data-driven run
testcases/*.csv + *.xlsx            Bảng test case (sinh ra)
newman/*.html                       Báo cáo thi hành
ci/baseline_allowlist.json          Cổng chặn hồi quy cho CI
```

## Tham chiếu

| Nội dung | Vị trí |
|---|---|
| Thiết kế đầy đủ, kèm đánh giá thực nghiệm | [`DESIGN.md`](./DESIGN.md) |
| Pseudocode từng giai đoạn | [`pseudocode/generator_pseudocode.md`](./pseudocode/generator_pseudocode.md) |
| Cài đặt tham chiếu chạy được | [`pseudocode/generator.py`](./pseudocode/generator.py) — thử bằng `--demo` |
| Bộ biên dịch IR → Postman (dùng thật) | [`../postman/scripts/build_collections.py`](../postman/scripts/build_collections.py) |
