# BAO CAO CI/CD — HW06 API Testing

> SV **Ninh Van Khai — 23127060** | De bai muc 6 (Integrate into CI/CD)

De bai: *"Add your API test cases to a CI/CD pipeline for the SUT... and write a short CI/CD
report describing the pipeline configuration and the two runs below, with screenshots and
links. Provide two sample commits: one whose pipeline run shows all API test cases passing,
and another whose pipeline run shows one test case failing."*

---

## 1. Cau hinh pipeline

| Hang muc | Gia tri |
|---|---|
| Nen tang | GitHub Actions |
| File workflow | `.github/workflows/api-tests-23127060.yml` (ban sao: `ci/api-tests-23127060.yml`) |
| Runner | `ubuntu-latest`, gioi han 20 phut |
| Kich hoat | `push` va `pull_request` cham vao `members/23127060/**`, hoac chay tay bang `workflow_dispatch` |
| Node.js | 20 |
| Cong cu | `newman` + `newman-reporter-htmlextra` (cai toan cuc) |
| SUT | Clone `ttbhanh/eshop-sut` va **ghim dung commit `85af3ba`** |
| Base URL | `http://localhost:3000` — thoa yeu cau chong gian lan cua de bai muc 11 |
| San pham dau ra | Bao cao HTML + JSON tai len lam artifact, giu 30 ngay |

### Cac buoc trong job

1. **Checkout** bai lam.
2. **Setup Node 20**.
3. **Cai Newman** va reporter `htmlextra`.
4. **Clone SUT va `git checkout 85af3ba`** — ghim commit la bat buoc: neu SUT thay doi, moc hoi
   quy se do vi mot ly do khong lien quan gi den bai lam.
5. **Cai dependency cua SUT**.
6. **Xac dinh che do chay** (`contract` hoac `full`).
7. **Chay Newman cho ca 3 API**, moi API khoi dong lai backend truoc (xem muc 2).
8. **Tong hop ket qua vao Job Summary** bang `summarize_newman.py`.
9. **Kiem chung header `X-Student-Id`** bang `verify_header.py`, ket qua in thang vao Job Summary.
10. **Upload artifact** bao cao HTML/JSON.
11. **In log cua SUT** neu job that bai; **dung backend** trong moi truong hop.

## 2. Hai quyet dinh cau hinh dang giai thich

### 2.1 Khoi dong lai backend truoc **moi** collection

`backend/database.js` goi `initDatabase()` ngay khi module duoc `require`, va ham do bat dau
bang mot loat `DROP TABLE`. Nen khoi dong lai backend chinh la cach dua CSDL ve trang thai
seed goc.

Day khong phai toi uu cho dep ma la **dieu kien de ket qua co nghia**. SUT co bug **A-09**:
moi lan dang nhap sai cong `+2` vao `login_attempts` va khoa tai khoan 180 giay khi dat 3.
Neu chay collection thu hai tren CSDL cua collection thu nhat, tai khoan test da bi khoa va
hang loat test se that bai vi mot ly do khong lien quan gi den chat luong API. Lan chay thu
nghiem dau tien o may cuc bo dinh dung loi nay: 7 test case that bai day chuyen tu **mot**
nguyen nhan duy nhat.

### 2.2 Hai che do chay, va vi sao khong ep bo test day du phai xanh

SUT co **34 bug that**. Bo test day du (243 case, oracle la dac ta) **phai do** — do la ket
qua kiem thu dung. Neu ep no xanh thi chi con mot cach: sua ky vong cho khop voi hanh vi sai
cua SUT, tuc la **nguy tao ket qua**.

Vi vay pipeline co hai che do:

| Che do | Chay gi | Ky vong | Dung de lam gi |
|---|---|---|---|
| `contract` | 84 test case ma SUT **hien dang** dap ung | ✅ XANH | Moc hoi quy — bao dong khi mot dieu dang dung bi pha |
| `full` | Toan bo 243 test case, oracle la dac ta | ❌ DO (dung y do) | Ket qua kiem thu that su; do khoang cach giua dac ta va hien thuc |

Bo `contract` **khong** khang dinh "API nay dung". No khang dinh "nhung dieu API nay dang lam
dung thi khong duoc pha". Danh sach 84 case do duoc suy ra tu **ket qua chay that** bang
`scripts/derive_contract.py`, khong phai tu phan doan luc thiet ke — xem
`postman/contract_baseline/API-*.txt`.

## 3. Hai lan chay bat buoc

### 3.1 Lan chay PASS — che do `contract`

| | |
|---|---|
| **Commit** | `<dien hash sau khi push>` |
| **Thong diep commit** | `ci: run all api tests (expect pass)` |
| **Link run** | `<dien link GitHub Actions>` |
| **Anh chup** | `ci/evidence/ci_run_pass.png` |
| **Ket qua mong doi** | 84 test case, **406 assertion, 0 that bai**, job xanh |

Ket qua **da kiem chung tren may cuc bo** truoc khi push (`ci/evidence/local_ci_run_pass.log`):

```
API-1 contract:  163 assertion,  0 that bai
API-2 contract:  164 assertion,  0 that bai
API-3 contract:   79 assertion,  0 that bai
------------------------------------------
Tong:            406 assertion,  0 that bai   -> exit code 0
```

### 3.2 Lan chay FAIL — lam sai dung **mot** assertion

| | |
|---|---|
| **Commit** | `<dien hash sau khi push>` |
| **Thong diep commit** | `ci: introduce one failing assertion to demo pipeline failure` |
| **Link run** | `<dien link GitHub Actions>` |
| **Anh chup** | `ci/evidence/ci_run_fail.png` |
| **Ket qua mong doi** | 406 assertion, **dung 1 that bai**, job do |

Thay doi duoc thuc hien bang script, de tai lap va tra lai duoc:

```bash
python3 ci/inject_failing_test.py --apply    # lam sai 1 assertion
python3 ci/inject_failing_test.py --check    # xem dang o trang thai nao
python3 ci/inject_failing_test.py --revert   # tra lai nhu cu
```

Script doi ky vong ma trang thai cua `TC-A1-DOM-012` (`POST /api/reset-password` voi du lieu
hop le) tu **200** thanh **201**. Chon dung case nay vi ba ly do:

- No nam trong bo hoi quy nen binh thuong **chac chan PASS** — khi pipeline do thi ly do duy
  nhat la thay doi vua chen vao, khong the do nguyen nhan khac.
- No la case DOM dau tien cua bo hoi quy API-1 nen xuat hien som trong log CI, de nhin thay.
- Nham `200` voi `201` la loi con nguoi hay mac that (quy uoc REST cho thao tac tao moi), nen
  no minh hoa dung loai loi ma pipeline sinh ra de bat — thay vi mot loi bia dat.

Ket qua **da kiem chung tren may cuc bo** (`ci/evidence/local_ci_run_fail.log`):

```
API-1 contract:  163 assertion,  1 that bai
API-2 contract:  164 assertion,  0 that bai
API-3 contract:   79 assertion,  0 that bai

 1.  AssertionError  TC-A1-DOM-012 | HTTP 200
                     expected response to have status code 201 but got 200

newman exit code = 1   -> GitHub Actions danh dau job that bai
```

> Luu y ky thuat: `scripts/run_newman.sh` dung co `--suppress-exit-code` de mot API do khong
> lam dut chuoi chay cac API con lai o may cuc bo. Workflow CI **khong** dung co do — no thu
> ma thoat cua tung lan chay va tra ve ma khac 0 o cuoi job, nen GitHub Actions danh dau job
> la that bai dung nhu mong doi.

## 4. Bang chung header `X-Student-Id` ngay trong pipeline

Buoc **"Kiem chung header X-Student-Id"** chay `verify_header.py`, doc thang phan
`request.header` ma Newman ghi lai cho tung request that su roi len duong, roi in ket qua vao
**Job Summary** cua GitHub Actions. Nghia la bang chung chong gian lan nam ngay trong trang
ket qua cua pipeline, ai mo link cung xem duoc, khong phu thuoc vao mot anh chup man hinh.

Ket qua o may cuc bo: **823/823 request mang `X-Student-Id: 23127060`, khong request nao
thieu** — xem `ci/evidence/header_evidence.md`.

## 5. CONG VIEC CON LAI CUA SINH VIEN (HUMAN H5)

> Toan bo phan cau hinh va kiem chung logic da xong va **da chay dung o may cuc bo**. Phan con
> lai bat buoc phai do sinh vien thuc hien vi no doi hoi quyen day ma len GitHub.
>
> Thu muc lam viec dang tro toi remote `https://github.com/thangak18/HW06.git` — **khong phai
> tai khoan cua sinh vien** (`gh` dang dang nhap bang `nvkhai238`). Vi vay khong tu dong day
> ma len: viec day ma vao repo cua nguoi khac phai duoc chinh chu dong y truoc.

### Cac buoc

1. **Chot repo se dung.** Hoac xin quyen ghi vao `thangak18/HW06`, hoac fork ve tai khoan
   `nvkhai238` roi doi remote:
   ```bash
   gh repo fork thangak18/HW06 --clone=false --remote=false
   git remote add mine https://github.com/nvkhai238/HW06.git
   ```
2. **Day ma va tao lan chay PASS:**
   ```bash
   git push mine main
   gh workflow run "API Tests 23127060" -f mode=contract
   gh run watch
   ```
   Doi job xanh, chup man hinh -> `ci/evidence/ci_run_pass.png`, chep link run vao muc 3.1.
3. **Tao lan chay FAIL:**
   ```bash
   python3 ci/inject_failing_test.py --apply
   git add -A && git commit -m "ci: introduce one failing assertion to demo pipeline failure"
   git push mine main
   gh run watch
   ```
   Doi job do, chup man hinh (phai thay ro dong `TC-A1-DOM-012 ... expected 201 but got 200`)
   -> `ci/evidence/ci_run_fail.png`, chep link run vao muc 3.2.
4. **Tra lai trang thai binh thuong:**
   ```bash
   python3 ci/inject_failing_test.py --revert
   git add -A && git commit -m "ci: revert the demo failing assertion"
   git push mine main
   ```
5. **Dien hai commit hash va hai link run** vao bang o muc 3.
6. **Cong khai repo** (de bai muc 14 doi link GitHub cong khai) va dien link vao `README.md`.

### Bang kiem truoc khi coi la xong

- [ ] Link run PASS, job xanh, artifact tai ve duoc
- [ ] Link run FAIL, job do, log co dong `TC-A1-DOM-012 ... expected 201 but got 200`
- [ ] `ci/evidence/ci_run_pass.png` va `ci/evidence/ci_run_fail.png`
- [ ] Hai commit hash da dien vao muc 3
- [ ] Da chay `inject_failing_test.py --revert` va commit lai
