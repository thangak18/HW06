---
name: api-test-generator
description: Sinh bộ test case API đầy đủ từ tài liệu đặc tả, phủ domain partition, state transition, security và schema validation, rồi biên dịch ra Postman Collection chạy được bằng Newman. Dùng khi cần kiểm thử một REST API có tài liệu đặc tả và cần độ phủ có hệ thống, kiểm toán được.
---

# API Test Generator

Bản cài đặt chạy được của thiết kế trong [`agent-skill/DESIGN.md`](../../../agent-skill/DESIGN.md).
Phương pháp đầy đủ — sáu giai đoạn, danh mục quy tắc, quy trình audit — nằm ở
[`agent-skill/SKILL.md`](../../../agent-skill/SKILL.md). File này là **đầu vào để chạy**.

## Nguyên tắc

Chỉ dùng mô hình ngôn ngữ cho **đúng một việc**: đọc hiểu tài liệu đặc tả (giai đoạn G1).
Năm giai đoạn còn lại là mã tất định. Độ phủ đến từ **danh mục quy tắc phân vùng**, không đến từ
mô hình — hỏi mô hình *"nghĩ ra test case đi"* thì nó sinh dày ở chỗ dễ và bỏ sót ở chỗ khó.

## Cách chạy

Mọi lệnh chạy từ thư mục `23127195/`.

### Bước 1 — Xác định API cần sinh test case

Hỏi người dùng API nào nếu chưa rõ. Ba API của bài này:

| API | FR | Endpoint |
|---|---|---|
| API-1 | FR-04 | `GET/PUT /api/users/me` |
| API-2 | FR-09 | `POST /api/apply-coupon`, `POST /api/coupon-usage` |
| API-3 | FR-16 | `POST /api/admin/import-products` |

### Bước 2 — Nạp **cả hai** tài liệu, không chỉ đặc tả API

```
../../.sut/eshop-sut/api_specification.md    hợp đồng dữ liệu
../../.sut/eshop-sut/README.md               ràng buộc nghiệp vụ + SEC-01…SEC-07
```

Đặc tả API **không hề chứa** SEC-01…SEC-07 — chúng nằm ở README của SUT. Chỉ nạp một tài liệu là
mất hẳn một chiều kiểm thử; ba trong số các lỗi nghiêm trọng nhất của bài nằm đúng vào chỗ đặc tả
API im lặng còn SRS thì nói rõ.

### Bước 3 — Trích xuất `EndpointModel` *(chỗ duy nhất dùng LLM)*

Sinh JSON đúng lược đồ mô tả trong
[`agent-skill/pseudocode/generator_pseudocode.md`](../../../agent-skill/pseudocode/generator_pseudocode.md),
ghi ra một file tạm.

Hai ràng buộc bắt buộc:

- **Mọi ràng buộc phải kèm trích dẫn nguyên văn** từ tài liệu. Ràng buộc không có nguồn là ràng
  buộc bịa. Không tìm thấy ở đâu thì ghi `"KHÔNG ĐƯỢC ĐẶC TẢ"`, đừng suy đoán.
- **Không được gọi thử API thật ở bước này.** Nhìn response thật trước khi chốt kỳ vọng sẽ neo kỳ
  vọng theo hành vi hiện có, và mọi lỗi sẽ được hợp thức hoá thành "đúng như thiết kế".

### Bước 4 — Sinh test case bằng mã tất định

```bash
python agent-skill/pseudocode/generator.py <endpoint_model.json> -o <ir.json>
```

Thử nhanh không cần model (dùng model FR-04 dựng sẵn, ra 44 case):

```bash
python agent-skill/pseudocode/generator.py --demo
```

Bộ sinh áp bốn danh mục quy tắc: phân vùng miền, chuyển trạng thái, bảo mật, lược đồ. Chi tiết
từng danh mục ở [`agent-skill/SKILL.md`](../../../agent-skill/SKILL.md) bước 3.

### Bước 5 — Đọc kết quả kiểm tra IR

Bộ sinh tự chạy bộ kiểm tra G6a và in số lỗi / cảnh báo ra `stderr`. Nó chặn nếu thiếu
`expected_by_spec`, thiếu nhãn audit, hoặc assertion bất đồng bộ không bọc
`try { … done(); } catch (e) { done(e); }`.

Điều kiện cuối bắt nguồn từ sự cố thật: assertion bất đồng bộ hỏng thì ngoại lệ ném trước `done()`
và Newman **âm thầm bỏ qua** test đó — không PASS, không FAIL. Lỗi nghiêm trọng nhất của đợt kiểm
thử đầu tiên hiện ra là "đã pass" chính vì lý do này.

### Bước 6 — Nói rõ đây mới là một nửa công việc

Sau khi sinh xong, **luôn** nhắc người dùng: máy chỉ làm được phần phủ có hệ thống. Bước audit của
con người (G6b) không tự động hoá được, và trong bài này **34/144 test case do người thêm, tìm ra
6/24 lỗi**. Sáu câu hỏi dẫn đường cho bước đó nằm ở
[`agent-skill/SKILL.md`](../../../agent-skill/SKILL.md) bước 5.

## Biên dịch sang Postman (tuỳ chọn)

```bash
python postman/scripts/build_collections.py     # IR -> Postman Collection v2.1
bash scripts/run_newman.sh                      # restart SUT rồi chạy Newman
python scripts/export_testcases.py              # IR + kết quả -> Excel
```

## Điều cần tránh

| Đừng | Vì |
|---|---|
| Cho mô hình xem response thật trước khi chốt kỳ vọng | Kỳ vọng bị neo theo hành vi, lỗi thành "đúng thiết kế" |
| Để mô hình sinh thẳng ra JavaScript | Lỗi cú pháp và lỗi bất đồng bộ rải rác, không rà soát nổi |
| Bỏ qua phân vùng đúng tại biên (`v == min`) | Đây chính là điểm phân biệt `>` với `>=` |
| Kiểm lược đồ chỉ theo chiều "có đủ trường" | Không phát hiện được `SELECT *` làm rò rỉ cột nhạy cảm |
| Coi bước audit của con người là tuỳ chọn | 6/24 lỗi của bài này chỉ tìm ra nhờ test case do người viết |
