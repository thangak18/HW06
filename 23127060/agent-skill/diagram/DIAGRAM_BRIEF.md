# DIAGRAM_BRIEF — Mô tả để SINH VIÊN TỰ VẼ sơ đồ bộ sinh test

> HW06 — SV **Ninh Văn Khải — 23127060** | Đề bài mục 7 và mục 11

> **Trạng thái (02/09/2026): sơ đồ đã vẽ xong** —
> `agent-skill/diagram/23127060_generator_diagram.png` (vẽ bằng draw.io).
> File này giữ lại làm bản mô tả đầu vào đã dùng để vẽ, và làm bảng kiểm khi rà lại.

---

## ⚠ Quy tắc bắt buộc đọc trước

Đề bài **mục 11 (Anti-AI Cheat Constraints)** ghi rõ:

> *"The AI test generator diagram, which must be self-drawn — designed by you, not generated
> directly by an AI."*

Vì vậy:

- File này **chỉ chứa mô tả bằng chữ**. Trong cả thư mục `agent-skill/diagram/` **không có**
  và **không được có** bất kỳ file ảnh, file `.mmd`, khối `mermaid`, `graphviz`, PlantUML hay
  ASCII-art nào do AI sinh ra. Nếu có, đó là vi phạm mục 11 và bài bị tính là gian lận.
- Sinh viên **tự vẽ** sơ đồ, bằng công cụ tùy ý (draw.io, Excalidraw, Figma, hoặc vẽ tay rồi
  chụp ảnh — đề bài chấp nhận hết, miễn là **quyết định thiết kế là của sinh viên**).
- Lưu kết quả thành `agent-skill/diagram/23127060_generator_diagram.png`.
- Nên lưu thêm file nguồn (`.drawio` / `.excalidraw`) cạnh file PNG: nó chứng minh sơ đồ do
  sinh viên dùng tay dựng nên, và sửa lại được khi bảo vệ miệng.

Mô tả dưới đây là **thông tin đầu vào** để vẽ. Sinh viên đọc và tự quyết định bố cục, hình
dáng khối, màu sắc, cách đặt mũi tên. **Không cần vẽ giống hệt** — hiểu kiến trúc rồi vẽ theo
cách của mình là đạt yêu cầu.

---

## 1. Sơ đồ cần trả lời được ba câu hỏi

Trước khi vẽ, ghi nhớ ba câu hỏi mà người chấm sẽ nhìn sơ đồ để tìm câu trả lời:

1. **Đầu vào là gì, đầu ra là gì?**
2. **Vì sao kết quả lặp lại được?** (cùng một đầu vào luôn cho ra cùng một bộ test)
3. **Con người xen vào ở đâu?** (đề bài coi trọng điểm này: AI là trợ lý có kỷ luật, không
   phải hộp đen)

Nếu sơ đồ vẽ xong mà không trả lời được một trong ba câu, thì còn thiếu.

---

## 2. Các khối cần có

### Cột 1 — ĐẦU VÀO (bên trái)

| Khối | Nhãn gợi ý | Ghi chú |
|---|---|---|
| A1 | `eshop-sut/README.md` (SRS: FR-01..FR-24, SEC-01..07) | tài liệu văn xuôi |
| A2 | `eshop-sut/api_specification.md` | hình dạng request/response |
| A3 | `eshop-sut/backend/server.js` | mã nguồn — dùng để đối chiếu |

Ba khối này nên vẽ chung một màu (màu "tài liệu"), và **ngoài đường viền** của hệ thống —
chúng là thứ có sẵn, không phải thứ mình xây.

### Khối bản lề — DỊCH SANG DẠNG MÁY ĐỌC ĐƯỢC

| Khối | Nhãn gợi ý |
|---|---|
| B | **Dịch đặc tả sang dạng máy đọc được** → `spec/api-N.json` |

**Đây là khối quan trọng nhất của cả sơ đồ.** Nó nên được vẽ **to hơn** các khối khác, và
phải thể hiện rõ ràng đây là **công đoạn có con người tham gia** (xem mục 3).

Lý do: đặc tả văn xuôi không nói rõ đâu là trục phân hoạch. Câu *"Giá: bắt buộc, phải là số
dương (> 0)"* chứa ba thông tin ẩn: tên tham số, kiểu dữ liệu, và **một biên tại 0**. Con
người đọc ra ngay; chương trình thì không. Khối B chính là nơi biến đổi đó xảy ra.

Bên trong khối B, vẽ bốn ô nhỏ ứng với bốn trục của file JSON:

- `endpoints[].params[].partitions[]`
- `state_machine.transitions[]`
- `security[]`
- `schema_cases[]`

### Cột 2 — BỐN BỘ SINH (giữa)

Bốn khối **song song**, mỗi khối nhận đầu vào từ đúng một trục tương ứng ở khối B:

| Khối | Nhãn | Kỹ thuật kiểm thử | Kết quả bài này |
|---|---|---|---|
| C1 | `SINH_DOMAIN` | Equivalence Partitioning, BVA, Decision Table | 128 case |
| C2 | `SINH_STATE` | State Transition Testing (0-switch) | 38 case |
| C3 | `SINH_SECURITY` | Ánh xạ SEC-01..SEC-07 | 41 case |
| C4 | `SINH_SCHEMA` | JSON Schema Validation | 18 case |

Vẽ **song song, không nối tiếp** — đây là điểm thiết kế cố ý: bốn bộ sinh độc lập nhau nên
chạy được riêng từng cái (`--only DOM`, `--only STA`...). Đó chính là cơ sở kỹ thuật để thỏa
yêu cầu *"drive it step by step, not with a single generic prompt"* của đề bài mục 6.

Nên ghi con số lên từng khối: nó cho thấy ngay độ phủ lệch về đâu.

### Cột 3 — HẬU XỬ LÝ (phải giữa)

| Khối | Nhãn | Ghi chú |
|---|---|---|
| D | `KHU_TRUNG` | Khóa gồm 7 trường — xem mục 4, đây là chỗ đáng chú thích |
| E | `DANH_SO_LAI` | `TC-<prefix>-<NHOM>-<3 chu so>` |
| F | `KIEM_TRA_DO_PHU` | **công tắc chặn** — xem mục 4 |

Khối F nên vẽ khác hình (ví dụ hình thoi / hình bình hành) vì nó là điểm **quyết định**,
không phải điểm biến đổi. Từ F vẽ **một mũi tên quay ngược lại khối B**, nhãn
*"chưa đủ độ phủ -> bổ sung vào spec rồi chạy lại"*. Vòng lặp này là thứ thể hiện rõ nhất
rằng bộ sinh có kiểm soát chất lượng, chứ không chỉ là một máy in test case.

### Cột 4 — ĐẦU RA (bên phải)

| Khối | Nhãn |
|---|---|
| G | `testcases/API-N_generated.csv` (22 cột) |
| H | `build_collection.py` → Postman Collection v2.1 |
| I | `newman` → báo cáo HTML/JSON |
| J | Báo cáo + bug report |

---

## 3. Ba điểm CON NGƯỜI xen vào — phần phải nổi bật nhất

Đề bài coi trọng điều này hơn cả số lượng test case. **Dùng màu khác hoặc viền đứt** cho ba
điểm này, và **ghi chú thích ngay trên sơ đồ**:

| Điểm | Vị trí trên sơ đồ | Con người làm gì |
|---|---|---|
| **H1** | tại khối **B** | Đọc đặc tả, quyết định đâu là phân hoạch, đâu là biên, chuyển trạng thái nào hợp lệ. **Chất lượng cả bộ test nằm ở đây.** |
| **H2** | sau khối **G** | **AUDIT**: gắn `VALID` / `INVALID` / `INCOMPLETE` cho từng case, ghi lý do, sửa case sai. Kết quả bài này: 83 VALID, 68 INVALID, 74 INCOMPLETE |
| **H3** | sau khối **H2** | **EXTEND**: thêm case mà bộ sinh không thể nghĩ ra. Kết quả bài này: 18 case, mỗi case có cột `Why_AI_Missed` |

Vẽ H2 và H3 thành một khối nối tiếp giữa G và H, **không** được vẽ như một nhánh phụ — chúng
nằm trên đường đi chính của dữ liệu.

---

## 4. Ba chú thích nên ghi thẳng lên sơ đồ

Đây là những điều em học được trong quá trình làm. Ghi chúng lên sơ đồ làm cho nó là **thiết kế
của người đã chạy thật**, không phải một sơ đồ khối chung chung.

**Chú thích 1 — cạnh khối D (`KHU_TRUNG`):**
> Khóa khử trùng phải gồm cả `Category`, `Expected_Assertions` và `Preconditions`.
> Ban đầu khóa chỉ có `(method, endpoint, body, status)` nên coi hai case là trùng nhau khi
> chúng gửi cùng một request, bất kể chúng khẳng định điều gì. Kết quả: 34 test case bị nuốt
> oan (191 thay vì 225), và độ phủ bảng chuyển trạng thái bị báo thiếu (11/25 thay vì 20/25).

**Chú thích 2 — cạnh khối C3 (`SINH_SECURITY`):**
> Mã SEC là nhãn không tự giải thích. Bảng SEC-01..07 phải lấy từ `README.md` mục 9, không
> được điền từ trí nhớ về OWASP. Lần đầu làm theo trí nhớ: 39/41 test case bảo mật bị gán sai mã.

**Chú thích 3 — cạnh cụm C1..C4:**
> Bốn bộ sinh đều sinh ra test case **độc lập**, mỗi case một request. Đó là giới hạn cấu trúc:
> 9/18 bug mà con người phải tự bổ sung chỉ lộ ra khi nối **nhiều request** lại với nhau.

---

## 5. Bố cục gợi ý

Trái sang phải, bốn cột:

```
[ TAI LIEU ] -> [ DICH SANG JSON ] -> [ 4 BO SINH ] -> [ HAU XU LY ] -> [ DAU RA ]
   A1 A2 A3            B                C1 C2 C3 C4      D  E  F        G H I J
                       ^                                    |
                       |                                    |
                       +----- chua du do phu, bo sung -------+
```

Con người (H1, H2, H3) vẽ ở **hàng dưới**, mỗi điểm có một mũi tên đứt nối lên khối tương ứng.
Cách này làm nổi bật rằng con người chạm vào quy trình ở ba chỗ khác nhau, chứ không phải chỉ
ở cuối.

---

## 6. Bảng kiểm trước khi coi là vẽ xong

- [x] Nhìn sơ đồ đoán được **đầu vào** và **đầu ra** mà không cần đọc chú giải
- [x] Bốn bộ sinh vẽ **song song**, không vẽ nối tiếp
- [x] Có **mũi tên phản hồi** từ `KIEM_TRA_DO_PHU` quay về khối dịch spec
- [x] Ba điểm con người H1/H2/H3 được làm nổi bật và **nằm trên đường đi chính**
- [x] Có ít nhất một trong ba chú thích ở mục 4
- [ ] Góc sơ đồ có ghi **họ tên + MSSV + ngày vẽ** — rà lại trước khi nộp
- [x] Đã lưu `agent-skill/diagram/23127060_generator_diagram.png`
- [ ] Nên lưu kèm file nguồn `.drawio` cạnh file PNG
- [x] **Không có** file mermaid / graphviz / ảnh nào do AI sinh trong thư mục này
