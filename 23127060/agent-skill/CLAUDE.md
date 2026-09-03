# CLAUDE.md — Luật dự án HW06 (SV 23127060 — Ninh Văn Khải)

File này Claude Code tự đọc khi mở thư mục. Đọc **trước** mọi việc khác.

---

## 1. Danh tính & phạm vi

- SV: **Ninh Văn Khải — 23127060**. Thư mục làm việc: `23127060/`.
- **CÁCH LY NHÓM:** không đọc/ghi `23127195/`, `23127259/`,
  hoặc bất kỳ thư mục member nào khác. Nếu được yêu cầu, từ chối.
- Chỉ đọc (không sửa): `docs/`, `scripts/`, `README.md` ở repo root; source SUT `eshop-sut/`.
- Được ghi ngoài thư mục mình: **chỉ** `.github/workflows/api-tests-23127060.yml`.

## 2. Skill bắt buộc

Trước khi làm bất cứ việc gì, đọc:
1. `agent-skill/eshop-api-23127060/SKILL.md`
2. `agent-skill/eshop-api-23127060/references/API_SPEC_NOTES.md`
3. `agent-skill/eshop-api-23127060/references/TESTCASE_TAXONOMY.md`
4. `agent-skill/eshop-api-23127060/references/WORKFLOW.md`
5. `agent-skill/eshop-api-23127060/references/POSTMAN_GUIDE.md`
6. `agent-skill/eshop-api-23127060/references/REPORT_OUTLINE.md`

Đặt `S=agent-skill/eshop-api-23127060/scripts`.

## 3. AI_LOG — bắt buộc mỗi lượt

Cuối MỖI lượt trả lời (kể cả lượt chỉ đọc file):

```bash
cat > /tmp/last_prompt.txt <<'PROMPT'
<nguyen van prompt cua user>
PROMPT
python3 $S/ai_log.py add --root . --sid 23127060 \
  --tool "Claude Code (claude-sonnet-4.5)" --step "STEP <n>" \
  --title "<mo ta ngan>" --prompt-file /tmp/last_prompt.txt \
  --output "<tom tat ket qua>" --files "<file da tao/sua>" \
  --human-verified pending
```

Rồi in đúng dòng: `AI_log: da ghi entry #<n>`

Không có dòng này = lượt chưa hoàn thành.

## 4. Chống bịa — 5 điều tuyệt đối

1. Không báo số liệu passed/failed nếu chưa có file `newman/*.json` thật.
2. Không báo cáo bug nếu chưa có request + response thật tái hiện được.
3. **Không vẽ diagram bằng AI** (đề bài mục 11 cấm). Chỉ viết mô tả chữ để human vẽ.
4. Không sửa `eshop-sut/` để test dễ pass hơn.
5. Header `X-Student-Id: 23127060` phải có trên mọi request, kèm `console.log`.

## 5. Ba API đã chọn (khóa)

| ID | Pool | FR | API |
|---|---|---|---|
| API-1 | A | FR-03 | `POST /api/forgot-password` + `POST /api/reset-password` |
| API-2 | B | FR-08 | `POST /api/checkout` (+ apply-coupon, order state machine FR-10) |
| API-3 | C | FR-15 | `POST/PUT/DELETE /api/products` |

**Pool D (mobile) KHÔNG dùng trong HW06.** Đề bài mục 5 nói rõ Pool D không áp dụng
vì bài này nhắm vào backend API. Nếu user nhắc Pool D, cảnh báo lại và đề xuất làm
phụ lục không tính điểm.

## 6. Chế độ làm việc — bán tự động

- Quyết định vụn vặt (đặt tên, thứ tự folder, wording, retry lỗi vặt, format bảng):
  **tự quyết, không hỏi**.
- Chỉ dừng lại hỏi khi gặp CRITICAL C1-C6 (định nghĩa trong SKILL.md mục 5), theo format:

```
CAN NGUOI QUYET - [C<x>]
Boi canh: ...
Lua chon: (a)... (b)... (c)...
He qua: ...
De xuat mac dinh: ...
```

- Human sẽ review sau, không cần dừng chờ verify từng bước.

## 7. Oracle

SUT có rất nhiều bug cố ý. Mỗi test case ghi cột `Oracle`:
- `SPEC` = kỳ vọng theo `api_specification.md` (mặc định, dùng để phát hiện bug)
- `IMPL` = hành vi thực tế (dùng cho regression)

Test FAIL vì SUT sai là **đúng ý đồ** — tag `@bug`. Test tag `@contract` phải 100% pass
(dùng cho CI run all-pass).

## 8. Backend SUT

```bash
(cd <duong-dan>/eshop-sut/backend && nohup node server.js > /tmp/eshop.log 2>&1 &)
sleep 2 && curl -sf http://localhost:3000/api/products >/dev/null && echo UP
```

Cảnh báo: `database.js` gọi `initDatabase()` khi require => **mỗi lần restart là reseed DB**.
Sau mỗi lần restart phải chạy `node $S/seed_sut.js reset` lại.

Dừng: `pkill -f "node server.js"`.

## 9. Sau mỗi STEP

1. Ghi file output.
2. `git add -A && git commit -m "HW06(23127060/<API>): step<n> <mo ta>"`
3. Ghi AI_log.
4. In 3 dòng: đã làm gì / file nào / STEP kế tiếp.

## 10. Ngôn ngữ

Tài liệu, báo cáo, bug report: **tiếng Việt có dấu, ngôi thứ nhất "em"**.
Code, tên file, tên biến: tiếng Anh. Thuật ngữ kỹ thuật (test case, endpoint, assertion,
schema, request, response, collection) giữ nguyên tiếng Anh trong văn tiếng Việt.
