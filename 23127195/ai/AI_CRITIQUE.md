# AI Critique

**HW06 — API Testing** · **Sinh viên: 23127195** · **Ngày: 2026-09-01**
**AI tool: Claude Opus 5** (`claude-opus-5`)

---

Sai sót đáng kể nhất của AI nằm ở tầng hạ tầng, không ở từng test case. AI sinh assertion bất
đồng bộ theo mẫu gọi `pm.sendRequest` rồi đặt `done()` ngay sau `pm.expect`. Mẫu này chạy đúng
khi assertion đạt, nhưng khi assertion hỏng thì ngoại lệ được ném trước `done()`, và Newman âm
thầm bỏ qua test đó — không PASS, không FAIL, biến mất khỏi báo cáo. Test cho lỗi nghiêm trọng nhất
của cả bài — leo quyền lên admin — vì vậy ban đầu hiện ra như đã pass. Một bộ test
báo cáo thiếu nguy hiểm hơn một bộ test báo cáo sai, vì nó tạo cảm giác an toàn giả.

AI không tự phát hiện được lỗi này, kể cả khi tôi yêu cầu nó tự phê bình. Lý do là nó rà soát
từng case riêng lẻ, mà xét riêng thì mỗi case đều đúng; khiếm khuyết chỉ tồn tại ở mức tương tác
giữa đoạn mã và cách Newman ghi nhận kết quả. Nó chỉ lộ ra khi tôi đối chiếu báo cáo với kết quả
`curl` thủ công và nhận ra một assertion đã biến mất — dấu hiệu là sự vắng mặt, không phải dòng sai.

Thiên lệch thứ hai rõ hơn: AI neo kỳ vọng theo hành vi quan sát được, ràng buộc mã 400 cho mọi
đầu vào trông có vẻ sai kể cả khi đặc tả im lặng. Chín test case phải nới lại.

Nguyên tắc rút ra: AI đáng tin ở việc phủ có hệ thống nhưng không đáng tin ở việc tự kiểm chứng
chính nó. Mọi kết quả phải xác nhận bằng một đường đo độc lập, và phải chú ý tới thứ vắng mặt
chứ không chỉ thứ sai.

---

*Độ dài phần thân bài: 296 từ (yêu cầu 200–300 từ).*

**Bằng chứng đối chiếu cho các nhận định trên:**
- Khiếm khuyết assertion bất đồng bộ: [`AI_AUDIT_REPORT.md` §4.1](./AI_AUDIT_REPORT.md) và [`../agent-skill/DESIGN.md` §5.1](../agent-skill/DESIGN.md)
- Chín test case bị nới kỳ vọng: cột *Nhãn audit* = `INCOMPLETE` trong [`../testcases/TESTCASES_23127195.xlsx`](../testcases/TESTCASES_23127195.xlsx)
- Prompt tự phê bình đã dùng và giới hạn của nó: [`prompts/PROMPT_LIBRARY.md`](./prompts/PROMPT_LIBRARY.md) mục P6
