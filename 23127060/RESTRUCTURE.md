# RESTRUCTURE — Doi `members/member-N/` thanh `members/<MSSV>/`

> **DA LOI THOI (cap nhat sau khi merge origin/main).**
> Tai lieu nay de xuat giu `members/<MSSV>/`. Nhom da chot cau truc khac:
> bo han `members/`, dua thu muc thanh vien len **goc repo** — `23127060/`, `23127195/`, `23127259/`.
> Giu lai file nay lam ghi chep qua trinh; **cac lenh ben duoi khong con dung nua**.
> Duong dan thuc te hien tai: `23127060/`. Lenh nop bai dung la:
> `zip -r 23127060_HW06_AI_API_001.zip 23127060/ -x '*/node_modules/*' '*/__pycache__/*'` (chay tai repo root).
> `restructure.sh` cung da thi hanh xong va khong can chay lai.

---


Muc tieu: khi nop bai chi can `cd members && zip -r 23127060_HW06_AI_API_001.zip 23127060/`
la xong, khong phai gom file thu cong.

---

## 1. Vi sao nen doi ten thanh MSSV

| Van de voi `member-1` | Sau khi doi thanh `23127060` |
|---|---|
| Khong biet folder nao la cua ai khi cham | Nhin ten la biet ngay |
| Nen zip xong phai doi ten thu muc goc trong zip | Zip thang, ten thu muc goc da dung |
| Agent de doc nham folder nguoi khac | Luat cach ly viet duoc ro rang: chi duoc dung `members/23127060/` |
| CI/CD kho phan biet workflow cua ai | `api-tests-23127060.yml` |

---

## 2. Lam the nao (dung `git mv` de giu lich su)

Chay tai **repo root** (`HW06/`):

```bash
git mv members/member-1 members/23127060
git mv members/member-2 members/23127195
git mv members/member-3 members/23127259
git commit -m "HW06: doi ten thu muc thanh vien theo MSSV"
```

> Quan trong: phai thong nhat voi nhom truoc khi doi, vi ai dang mo nhanh rieng se bi conflict.
> Ai la member-1/2/3 thi tra trong `docs/team-api-allocation.md`.

Neu Git bao "destination exists" tren Windows (khong phan biet hoa thuong), doi qua 2 buoc:

```bash
git mv members/member-1 members/_tmp1 && git mv members/_tmp1 members/23127060
```

---

## 3. Cau truc de xuat sau khi doi

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

So voi cau truc hien tai, chi **them 4 thu** vao folder cua ban:
`CLAUDE.md`, `agent-skill/eshop-api-23127060/`, `ai/AI_log.md` + `ai/interactions/`, va `spec/`.
Phan con lai giu nguyen — khong pha cau truc chung cua nhom.

---

## 4. Diem can luu y: GitHub Actions

GitHub **chi doc workflow o `.github/workflows/` tai repo root**. Dat file YAML trong
`members/23127060/ci/` se khong bao gio chay.

Cach lam dung:
1. File goc: `.github/workflows/api-tests-23127060.yml`
2. Giu **1 ban sao** trong `members/23127060/ci/api-tests-23127060.yml` de bai nop tu chua
   duoc cau hinh CI (nguoi cham khong phai mo repo moi thay).
3. Screenshot 2 lan chay + link Actions luu vao `members/23127060/ci/evidence/`.

De workflow chi chay khi folder cua ban thay doi:

```yaml
on:
  push:
    paths:
      - 'members/23127060/**'
      - '.github/workflows/api-tests-23127060.yml'
```

---

## 5. Lenh nop bai

```bash
cd members
zip -r 23127060_HW06_AI_API_001.zip 23127060/ \
  -x '*/node_modules/*' '*/.git/*' '*/__pycache__/*' '*/.DS_Store'
unzip -l 23127060_HW06_AI_API_001.zip | head -30   # kiem tra thu muc goc la 23127060/
```

Truoc khi zip, luon chay:

```bash
cd members/23127060
python3 agent-skill/eshop-api-23127060/scripts/validate_submission.py --root . --sid 23127060
```

Chi nop khi `FAIL=0`.

---

## 6. Thoa thuan can chot voi nhom

1. **Doi ten folder** — lam 1 lan, tat ca push het truoc khi doi.
2. **`docs/team-api-allocation.md`** — chot 9 API (3 nguoi x 3 API), khong trung nhau.
   De bai muc 5: trung nhau la vi pham.
3. **Prompt khong duoc chia se** — muc 17: copy prompt cua nhau = 0 diem ca hai.
   Moi nguoi tu viet `ai/prompts/` cua minh.
4. **Moi nguoi 1 workflow rieng** — tranh dam commit vao cung 1 file YAML.
5. **Khong sua chung SUT** — `eshop-sut/` la repo rieng, chi clone ve, khong commit vao repo bai tap.
