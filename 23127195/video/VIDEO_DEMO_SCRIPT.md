# Kịch bản video demo Agent Skill — HW06 · 23127195

**MSSV:** 23127195 · **Bài tập:** HW06 — API Testing (SUT: EShop)
**Thời lượng đề xuất:** 3–4 phút · **Ngôn ngữ:** tiếng Việt, tự thuyết minh
**Nộp:** link YouTube (có thể để *Unlisted*)

> **Phạm vi:** §7 của đề bài yêu cầu video *"showing it generate tests for one API"* — tức là
> chỉ cần cho thấy **Agent Skill sinh test case cho một API**. Đây **không phải** video demo cả
> bài: không cần nói về Postman, Newman, 24 lỗi, hay CI/CD. Những phần đó đã có báo cáo riêng.
>
> Cả video chỉ trả lời đúng một câu: *gọi skill này ra thì nó làm được gì?*

---

## Chuẩn bị

```bash
# Mở Claude Code tại thư mục 23127195/
cd d:/Kiem_thu/HW6/HW06/23127195
claude
```

- [ ] **Không cần khởi động SUT** — bước sinh test case cố ý *không* gọi API thật
      (xem lý do ở phân đoạn 2)
- [ ] Phóng to cỡ chữ terminal ít nhất 16pt
- [ ] Đóng tab và thông báo không liên quan
- [ ] Thử micro trước

**Kiểm tra skill đã cài đúng chưa** (chạy trước khi bấm ghi hình):

```bash
ls .claude/skills/api-test-generator/SKILL.md
```

Trong Claude Code, gõ `/` sẽ thấy `api-test-generator` trong danh sách. Nếu không thấy thì Claude
Code đang mở ở thư mục khác — phải mở đúng tại `23127195/`.

---

## Phân đoạn

### 0:00 – 0:25 · Danh tính và mục tiêu

**Làm:** chạy trong terminal

```bash
whoami && hostname
```

**Nói:**
> "Em là ⟨họ tên⟩, MSSV 23127195. Video này demo Agent Skill mà em thiết kế cho bài HW06 —
> một bộ sinh test case API từ tài liệu đặc tả. Em sẽ gọi nó ngay trong Claude Code và cho
> chạy trên một API của hệ thống EShop."

---

### 0:25 – 1:00 · Skill là gì, nằm ở đâu

**Làm:** mở `.claude/skills/api-test-generator/SKILL.md`, cuộn qua phần frontmatter và mục
*Nguyên tắc*.

**Nói:**
> "Skill nằm ở `.claude/skills/api-test-generator`. Phần khai báo ở đầu file cho Claude Code biết
> khi nào nên dùng nó.
>
> Ý tưởng trung tâm nằm ngay ở mục Nguyên tắc: **chỉ dùng mô hình ngôn ngữ cho đúng một việc là
> đọc hiểu tài liệu đặc tả.** Toàn bộ phần sinh test case là mã tất định. Độ phủ đến từ một danh
> mục quy tắc phân vùng, không đến từ mô hình — vì nếu chỉ bảo AI 'sinh test case đi' thì nó sinh
> rất dày ở chỗ dễ và bỏ sót đúng những chỗ khó."

---

### 1:00 – 2:15 · **Gọi skill và để nó chạy** ⭐ *phần chính*

**Làm:** trong Claude Code, gõ:

```
/api-test-generator sinh test case cho API-1 (FR-04, GET/PUT /api/users/me)
```

Để Claude Code tự chạy. Nó sẽ lần lượt: đọc hai tài liệu đặc tả, dựng `EndpointModel`, rồi gọi
bộ sinh tất định.

**Nói trong lúc nó chạy — khi thấy nó mở tài liệu:**
> "Chú ý nó nạp **hai** tài liệu chứ không phải một. Đặc tả API chỉ mô tả hợp đồng dữ liệu, còn
> các yêu cầu bảo mật SEC-01 đến SEC-07 lại nằm ở README của hệ thống. Nếu chỉ nạp đặc tả API là
> mất hẳn một chiều kiểm thử — và ba trong số các lỗi nghiêm trọng nhất em tìm được nằm đúng vào
> chỗ đặc tả API im lặng còn tài liệu kia thì nói rõ."

**Nói khi thấy nó dựng EndpointModel:**
> "Đây là giai đoạn duy nhất dùng mô hình ngôn ngữ. Ràng buộc bắt buộc là mỗi ràng buộc trích ra
> phải kèm câu trích dẫn nguyên văn từ tài liệu — ràng buộc không có nguồn là ràng buộc bịa.
>
> Và ở bước này skill **cấm gọi API thật**. Nếu nhìn response thật trước khi chốt kỳ vọng thì kỳ
> vọng sẽ bị neo theo hành vi đang có, và mọi lỗi sẽ được hợp thức hoá thành 'đúng như thiết kế'."

---

### 2:15 – 3:00 · Kết quả

Khi bộ sinh chạy xong, bảng tổng kết hiện ra trên terminal:

```
  G2 domain partition :  26 case
  G3 state transition :   0 case
  G4 security         :  14 case
  G5 schema           :   4 case
  ----------------------------
  TONG                :  44 case

  G6a kiem tra IR     : 0 loi, 0 canh bao
```

**Nói:**
> "Từ một EndpointModel, bộ sinh cho ra 44 test case và qua bộ kiểm tra nội bộ với 0 lỗi.
> Để so sánh: bộ test em làm bằng quy trình đầy đủ cho chính API này có 45 test case."

**Làm:** mở `agent-skill/pseudocode/generator.py`, cuộn tới nhánh `c["loai"] == "bien"`.

**Nói:**
> "Đây là chỗ em muốn chỉ ra. Với mỗi ràng buộc biên, danh mục **bắt buộc** sinh đủ sáu điểm:
> min trừ 1, min, min cộng 1, và tương tự ở đầu max. Điểm ngay tại biên — `v` bằng đúng `min` —
> chính là điểm phân biệt một cài đặt dùng dấu lớn hơn với một cài đặt dùng lớn hơn hoặc bằng.
> Hỏi AI chung chung thì nó bỏ qua điểm này. Và đó đúng là lỗi BUG-A2-03 em tìm được trong bài."

---

### 3:00 – 3:30 · Giới hạn của nó, và kết

**Nói:**
> "Điều cuối cùng em muốn nói là giới hạn của chính công cụ này. Nó chỉ làm được phần phủ **có hệ
> thống** — những gì suy ra được từ tài liệu bằng quy tắc. Bước audit của con người thì không tự
> động hoá được: trong bài này 34 trên 144 test case là do em tự thêm, và riêng 34 case đó tìm ra
> 6 trên 24 lỗi. Skill có nhắc điều này mỗi lần chạy xong, cố ý để người dùng không tưởng nhầm là
> đã xong việc.
>
> Em xin hết, cảm ơn thầy cô đã xem."

---

## Sau khi quay

- [ ] Xem lại: có đoạn nào lộ thông tin cá nhân không nên công khai?
- [ ] Kiểm tra mã số **23127195** hiển thị rõ ít nhất một lần
- [ ] Tải lên YouTube, đặt **Unlisted**
- [ ] Dán link vào `README.md` và `docs/00_MAIN_REPORT.md` §4
- [ ] Ghi link vào đây: `<điền link YouTube>`

---

## Phương án dự phòng

Nếu Claude Code không chạy được lúc quay (mất mạng, hết hạn mức), vẫn demo được phần lõi bằng bộ
sinh tất định — nó chạy hoàn toàn cục bộ, không cần mạng và không cần SUT:

```bash
python agent-skill/pseudocode/generator.py --demo
```

Lệnh này dùng một `EndpointModel` dựng sẵn cho **FR-04** và cho ra đúng 44 test case như trên.
Khi đó bỏ phân đoạn 1:00–2:15, nói thay bằng: *"đây là giai đoạn G2 đến G6, phần mã tất định mà
skill gọi tới sau khi đã trích xuất xong EndpointModel."*
