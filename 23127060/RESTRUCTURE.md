# RESTRUCTURE — Ghi chép quá trình đổi cấu trúc thư mục

> **ĐÃ LỖI THỜI (cập nhật 02/09/2026, sau khi merge `origin/main`).**
> Tài liệu này ban đầu đề xuất giữ `members/<MSSV>/`. Nhóm đã chốt cấu trúc khác:
> bỏ hẳn `members/`, đưa thư mục thành viên lên **gốc repo** — `23127060/`, `23127195/`,
> `23127259/`. Em giữ lại file này làm ghi chép quá trình; **các lệnh bên dưới không còn
> dùng nữa**, và `restructure.sh` cũng đã thi hành xong, không cần chạy lại.
>
> Đường dẫn thực tế hiện tại: `23127060/`. Lệnh nộp bài đúng là:
> `zip -r 23127060_HW06_AI_API_001.zip 23127060/ -x '*/node_modules/*' '*/__pycache__/*'`
> (chạy tại repo root).

---

Mục tiêu ban đầu: khi nộp bài chỉ cần zip thẳng thư mục của mình là xong, không phải gom
file thủ công.

## 1. Vì sao nên đổi tên thành MSSV

| Vấn đề với `member-1` | Sau khi đổi thành `23127060` |
|---|---|
| Không biết folder nào là của ai khi chấm | Nhìn tên là biết ngay |
| Nén xong phải đổi tên thư mục gốc trong zip | Zip thẳng, tên thư mục gốc đã đúng |
| Agent dễ đọc nhầm folder người khác | Luật cách ly viết được rõ ràng: chỉ được dùng `23127060/` |
| CI/CD khó phân biệt workflow của ai | `api-tests-23127060.yml` |

---

## 2. Làm thế nào (dùng `git mv` để giữ lịch sử)

Chạy tại **repo root** (`HW06/`):

```bash
git mv members/member-1 members/23127060
git mv members/member-2 members/23127195
git mv members/member-3 members/23127259
git commit -m "HW06: doi ten thu muc thanh vien theo MSSV"
```

> Quan trọng: phải thống nhất với nhóm trước khi đổi, vì ai đang mở nhánh riêng sẽ bị conflict.
> Ai là member-1/2/3 thì tra trong `docs/team-api-allocation.md`.

Nếu Git báo "destination exists" trên Windows (không phân biệt hoa thường), đổi qua 2 bước:

```bash
git mv members/member-1 members/_tmp1 && git mv members/_tmp1 members/23127060
```

---

## 3. Cấu trúc đề xuất sau khi đổi

```
HW06/                                   <- repo root (public GitHub repo)
├── .github/workflows/
│   ├── api-tests-23127060.yml           <- BAT BUOC nam o day, Actions khong doc noi khac
│   ├── api-tests-23127195.yml
│   └── api-tests-23127259.yml
├── README.md                            <- gioi thieu nhom + bang phan cong + link 3 folder
├── docs/
│   ├── assignment-notes.md
│   └── team-api-allocation.md           <- chot 9 API, chung minh khong trung nhau
├── scripts/                             <- script dung chung (start SUT, seed, ...)
│   └── README.md
└── members/
    ├── 23127060/                        <- ZIP CHINH THU MUC NAY DE NOP
    │   ├── CLAUDE.md                    <- luat du an cho Claude Code (moi)
    │   ├── README.md                    <- bang tu danh gia + test summary
    │   ├── agent-skill/
    │   │   ├── eshop-api-23127060/      <- SKILL PACKAGE (moi)
    │   │   │   ├── SKILL.md
    │   │   │   ├── references/
    │   │   │   └── scripts/
    │   │   ├── diagram/                 <- PNG tu ve (KHONG dung AI)
    │   │   └── pseudocode/
    │   ├── ai/
    │   │   ├── AI_log.md                <- nhat ky moi luot chat (moi)
    │   │   ├── interactions/            <- prompt goc tung luot (moi)
    │   │   ├── audit/AI_AUDIT_REPORT.md
    │   │   ├── critique/AI_CRITIQUE.md
    │   │   └── prompts/
    │   ├── spec/                        <- spec may doc duoc, dau vao bo sinh test (moi)
    │   ├── bugs/{BUG_REPORT.md, screenshots/}
    │   ├── ci/{CI_CD_REPORT.md, api-tests-23127060.yml, evidence/}
    │   ├── git-log/
    │   ├── newman/
    │   ├── postman/{collections, data, environments, scripts}
    │   ├── report/
    │   └── testcases/
    ├── 23127195/
    └── 23127259/
```

So với cấu trúc lúc đó, chỉ **thêm 4 thứ** vào folder của em:
`CLAUDE.md`, `agent-skill/eshop-api-23127060/`, `ai/AI_log.md` + `ai/interactions/`, và `spec/`.
Phần còn lại giữ nguyên — không phá cấu trúc chung của nhóm.

---

## 4. Điểm cần lưu ý: GitHub Actions

GitHub **chỉ đọc workflow ở `.github/workflows/` tại repo root**. Đặt file YAML trong
`23127060/ci/` sẽ không bao giờ chạy.

Cách làm đúng:
1. File gốc: `.github/workflows/api-tests-23127060.yml`
2. Giữ **1 bản sao** trong `23127060/ci/api-tests-23127060.yml` để bài nộp tự chứa
   được cấu hình CI (người chấm không phải mở repo mới thấy).
3. Screenshot 2 lần chạy + link Actions lưu vào `23127060/ci/evidence/`.

Để workflow chỉ chạy khi folder của em thay đổi:

```yaml
on:
  push:
    paths:
      - '23127060/**'
      - '.github/workflows/api-tests-23127060.yml'
```

---

## 5. Lệnh nộp bài

```bash
zip -r 23127060_HW06_AI_API_001.zip 23127060/ \
  -x '*/node_modules/*' '*/.git/*' '*/__pycache__/*' '*/.DS_Store'
unzip -l 23127060_HW06_AI_API_001.zip | head -30   # kiem tra thu muc goc la 23127060/
```

Trước khi zip, luôn chạy:

```bash
cd 23127060
python3 agent-skill/eshop-api-23127060/scripts/validate_submission.py --root . --sid 23127060
```

Chỉ nộp khi `FAIL=0`.

---

## 6. Thỏa thuận cần chốt với nhóm

1. **Đổi tên folder** — làm 1 lần, tất cả push hết trước khi đổi.
2. **`docs/team-api-allocation.md`** — chốt 9 API (3 người x 3 API), không trùng nhau.
   Đề bài mục 5: trùng nhau là vi phạm. *(Đã chốt xong 02/09/2026: em FR-03/08/15,
   23127195 FR-04/09/16, 23127259 FR-02/10/14 — không trùng.)*
3. **Prompt không được chia sẻ** — mục 17: copy prompt của nhau = 0 điểm cả hai.
   Mỗi người tự viết `ai/prompts/` của mình.
4. **Mỗi người 1 workflow riêng** — tránh đâm commit vào cùng 1 file YAML.
5. **Không sửa chung SUT** — `eshop-sut/` là repo riêng, chỉ clone về, không commit vào
   repo bài tập.
