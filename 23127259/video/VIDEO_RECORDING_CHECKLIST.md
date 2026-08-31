# Video Recording Checklist

Checklist chuẩn bị trước và sau khi quay video demo nộp bài:

## Trước khi quay
- [ ] Backend EShop SUT đang chạy ổn định trên `localhost:3000` (hoặc cổng cấu hình).
- [ ] Postman Collection đã được lưu đầy đủ test scripts và pre-request scripts.
- [ ] Đã kiểm tra header `X-Student-Id: 23127259` xuất hiện chính xác trong Postman Console.
- [ ] File data-driven (`data.json` / `data.csv`) và môi trường (`environment.json`) đã được cấu hình đường dẫn chuẩn.
- [ ] Sơ đồ tự vẽ `agent-skill/diagram/` và pseudocode đã sẵn sàng để trình chiếu.

## Trong khi quay
- [ ] Thời lượng video đạt tối thiểu **>= 6 phút** (khuyến nghị 7–8 phút).
- [ ] Giọng thuyết minh tiếng Việt rõ ràng của sinh viên.
- [ ] Không quay lén thông tin bí mật (token production, private keys).
- [ ] Minh chứng đầy đủ cả Postman GUI, Newman CLI và GitHub Actions.

## Sau khi quay
- [ ] Upload video lên YouTube ở chế độ **Unlisted** (Không công khai).
- [ ] Dán link YouTube vào:
  - `23127259/README.md`
  - `23127259/docs/00_MAIN_REPORT.md`
  - Root `README.md`
