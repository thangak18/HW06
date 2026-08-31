# Kịch bản Video Demo HW06 (Thời lượng: >= 6 phút)

**Sinh viên:** TODO  
**MSSV:** {StudentID}  
**Bài tập:** HW06 – API Testing (EShop SUT)  
**Yêu cầu:** Tự thuyết minh tiếng Việt, quay trực tiếp màn hình thực thi Postman, Newman CLI và header `X-Student-Id: {StudentID}`.

---

## Phân đoạn thời gian chi tiết

### 0:00 – 0:45 | Xác minh danh tính & Tổng quan bài nộp
- Mở Terminal chạy: `whoami`, `hostname`, `git log -n 5 --oneline`.
- Giới thiệu họ tên, MSSV, trình bày 3 API đã chọn (Pool A, Pool B, Pool C).
- Mở file `README.md` cá nhân và cho thấy cấu trúc repository.

### 0:45 – 2:30 | Trình diễn Postman Collection & Pre-request Script
- Mở Postman hiển thị Collection chứa 3 API test suite.
- Mở Pre-request script minh chứng tự động gắn header `X-Student-Id: {StudentID}`.
- Mở Postman Console và gửi 1 request mẫu, chỉ rõ header `X-Student-Id` được gửi thành công đến SUT.
- Trình bày các test assertion (status code, schema validation `tv4`/`ajv`, token chaining).

### 2:30 – 4:00 | Thực thi Newman CLI & Báo cáo HTML
- Mở Terminal chạy lệnh Newman:
  ```bash
  newman run postman/collections/collection.json \
    -e postman/environments/environment.json \
    -d postman/data/testdata.json \
    -r cli,htmlextra \
    --reporter-htmlextra-export newman/report.html
  ```
- Quan sát output CLI, giải thích kết quả pass/fail.
- Mở file `newman/report.html` trên trình duyệt và duyệt qua các tab kết quả kiểm thử.

### 4:00 – 5:15 | CI/CD GitHub Actions & Báo cáo Bug
- Mở giao diện GitHub Actions của repo `thangak18/HW06`.
- Cho xem run thành công (All tests passed) và run phát hiện lỗi (Failing test case).
- Cho xem Issue đã tạo trên GitHub Issues kèm screenshot bug tìm được trên EShop SUT.

### 5:15 – 6:30 | Agent Skill / AI Test Generator & Lời kết
- Trình bày sơ đồ thiết kế tự vẽ (`agent-skill/diagram/`) và mã giả (`pseudocode/`).
- Tóm tắt kết luận và bài học rút ra từ AI Critique.
