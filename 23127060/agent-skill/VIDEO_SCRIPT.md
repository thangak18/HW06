# VIDEO_SCRIPT — Kịch bản quay demo bộ sinh test (khoảng 6 phút)

> HW06 — SV **Ninh Văn Khải — 23127060** | Đề bài mục 7 (khuyến khích, không bắt buộc)
>
> *"You are encouraged to implement it as a reusable Agent Skill and submit a demonstration
> video (YouTube link) showing it generate tests for one API."*

Em chọn **API-3 (FR-15 — quản lý sản phẩm)** để demo: nó có tham số ở cả ba vị trí (body, path,
query), và có bug SQL Injection để kết thúc video bằng một kết quả ấn tượng.

---

## Chuẩn bị trước khi bấm ghi

```bash
cd 23127060
# CSDL ve trang thai goc
pkill -f "[n]ode serv""er.js"; sleep 1
( cd ../../../../eshop-sut/backend && setsid --fork node server.js ) > /tmp/sut.log 2>&1 < /dev/null
curl -sf http://localhost:3000/api/products > /dev/null && echo "SUT san sang"
# don dep dau ra cu de quay cho sach
rm -f testcases/API-3_generated.csv
```

Mở sẵn hai cửa sổ: một terminal (chữ to, nền tối) và một trình soạn thảo mở `spec/api-3.json`.

---

## Phần 1 — Vấn đề (0:00–0:45)

**Nói:**
> "Chào thầy cô. Em là Ninh Văn Khải, MSSV 23127060. Em demo bộ sinh test case API cho HW06.
>
> Cách làm hiển nhiên là bảo AI 'đọc đặc tả này và viết 35 test case'. Nhưng cách đó có ba vấn
> đề: chạy lại cho ra kết quả khác, không đo được độ phủ, và thêm một API là làm lại từ đầu.
>
> Thiết kế của em tách làm hai lớp: một lớp cần đọc hiểu — do con người và AI cùng làm; và một
> lớp sinh — hoàn toàn tất định, cùng đầu vào luôn cho cùng đầu ra."

**Màn hình:** mở sơ đồ tự vẽ `agent-skill/diagram/23127060_generator_diagram.png`, chỉ tay vào
khối "dịch sang JSON" và cụm bốn bộ sinh.

## Phần 2 — Đầu vào (0:45–2:00)

**Nói:**
> "Đây là đặc tả gốc của hệ thống. Câu này nói: 'Giá: bắt buộc, phải là số dương'. Con người đọc
> ra ngay ba điều: có tham số tên price, kiểu số, và có một biên tại 0. Chương trình thì không.
>
> Nên bước đầu tiên là dịch câu đó sang dạng máy đọc được."

**Màn hình:** mở `eshop-sut/README.md` phần FR-15, rồi chuyển sang `spec/api-3.json`, cuộn tới
tham số `price` và đọc to bốn phân hoạch `valid` / `zero` / `negative` / `string`.

**Nói tiếp:**
> "File spec có bốn trục, ứng với bốn kỹ thuật kiểm thử mà đề bài yêu cầu: phân hoạch miền,
> chuyển trạng thái, bảo mật SEC-01 đến 07, và kiểm tra schema."

## Phần 3 — Chạy bộ sinh (2:00–3:30)

**Nói:** "Đề bài cấm dùng một prompt tổng, nên em chạy bốn vòng độc lập."

```bash
python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py \
  --spec spec/api-3.json --only DOM --out testcases/API-3_generated.csv
```
> "Vòng một: phân hoạch miền. 51 test case. Dòng 'Tham so CHUA phu DOM: (khong)' nghĩa là không
> tham số nào bị bỏ sót."

```bash
... --only STA --append   # 9 case
... --only SEC --append   # 14 case
... --only SCH --append   # 6 case
```
> "Bốn vòng, 80 test case, vượt xa ngưỡng 35 của đề bài."

**Màn hình:** mở CSV bằng `column -s, -t | less -S` hoặc Excel, chỉ vào cột `Oracle`, `SEC_Ref`,
`Tag`.
> "Mỗi case ghi rõ oracle là đặc tả hay là hành vi thực tế, và tag @bug nghĩa là case này sẽ
> thất bại — vì nó phơi bày một lỗi thật của hệ thống."

## Phần 4 — Bộ sinh tự chấm độ phủ (3:30–4:15)

```bash
python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py --spec spec/api-2.json --stats
```
> "Bộ sinh không chỉ in ra test case, nó còn tự chấm độ phủ của chính mình. Dòng cuối: 'O bang
> chuyen trang thai da test: 20 / 25'. Nó chỉ thẳng ra còn 5 ô chưa phủ — và đó là 5 ô đường
> chéo, kiểu chuyển một trạng thái về chính nó. Em bổ sung tay ở bước extend."

## Phần 5 — Chạy thật (4:15–5:30)

```bash
python3 agent-skill/eshop-api-23127060/scripts/build_collection.py \
  --csv testcases/API-3_final.csv --api API-3 \
  --out postman/collections/23127060_HW06_API-3.postman_collection.json

bash agent-skill/eshop-api-23127060/scripts/run_newman.sh API-3
```
> "86 test case, 405 assertion, 105 thất bại. Nghe như bộ test hỏng, nhưng không: hệ thống này
> có 34 bug thật và em cố ý viết kỳ vọng theo đặc tả chứ không theo hành vi thực tế."

**Màn hình:** mở báo cáo HTML, cuộn tới một test SQL Injection.
> "Đây là kết quả ấn tượng nhất: một câu UNION SELECT qua tham số search trả về nguyên văn
> email và mật khẩu của tài khoản quản trị — `admin@eshop.com` và `Admin123!`."

## Phần 6 — Con người ở đâu (5:30–6:00)

**Nói:**
> "Bộ sinh không thay thế người kiểm thử. Sau khi nó chạy xong, em vẫn phải làm ba việc: audit
> từng case — kết quả là 68 case sai và 74 case thiếu, em đã sửa hết; thêm 18 case mà bộ sinh
> không thể nghĩ ra; và quyết định case nào là hợp đồng, case nào phơi bày bug.
>
> Đáng chú ý nhất: một nửa số case em phải tự thêm là những bug chỉ lộ ra khi kết hợp nhiều
> request. Đó là giới hạn cấu trúc của thiết kế hiện tại, và em đã viết hướng mở rộng cho nó
> trong báo cáo. Em cảm ơn thầy cô."

---

## Bảng kiểm sau khi quay

> Video đã up: https://youtu.be/JZwzS1jXhUw — link đã điền vào `README.md` và
> `report/MAIN_REPORT.md`. Bốn dòng đầu em tự xác nhận khi xem lại video (AI không xem được
> nội dung video).

- [ ] Video < 8 phút, tiếng nói rõ
- [ ] Có cảnh **chạy thật** trong terminal (không phải ảnh tĩnh)
- [ ] Có cảnh mở **sơ đồ tự vẽ**
- [ ] Có cảnh mở báo cáo HTML của Newman
- [x] Up YouTube, điền link vào `README.md` và `report/MAIN_REPORT.md`
