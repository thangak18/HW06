# BÁO CÁO CI/CD — HW06 API Testing

> SV **Ninh Văn Khải — 23127060** | Đề bài mục 6 (Integrate into CI/CD)

Đề bài: *"Add your API test cases to a CI/CD pipeline for the SUT... and write a short CI/CD
report describing the pipeline configuration and the two runs below, with screenshots and
links. Provide two sample commits: one whose pipeline run shows all API test cases passing,
and another whose pipeline run shows one test case failing."*

---

## 1. Cấu hình pipeline

| Hạng mục | Giá trị |
|---|---|
| Nền tảng | GitHub Actions |
| File workflow | `.github/workflows/api-tests-23127060.yml` (bản sao: `ci/api-tests-23127060.yml`) |
| Runner | `ubuntu-latest`, giới hạn 20 phút |
| Kích hoạt | `push` và `pull_request` chạm vào `23127060/**`, hoặc chạy tay bằng `workflow_dispatch` |
| Node.js | 20 |
| Công cụ | `newman` + `newman-reporter-htmlextra` (cài toàn cục) |
| SUT | Clone `ttbhanh/eshop-sut` và **ghim đúng commit `85af3ba`** |
| Base URL | `http://localhost:3000` — thỏa yêu cầu chống gian lận của đề bài mục 11 |
| Sản phẩm đầu ra | Báo cáo HTML + JSON tải lên làm artifact, giữ 30 ngày |

### Các bước trong job

1. **Checkout** bài làm.
2. **Setup Node 20**.
3. **Cài Newman** và reporter `htmlextra`.
4. **Clone SUT và `git checkout 85af3ba`** — ghim commit là bắt buộc: nếu SUT thay đổi, mốc hồi
   quy sẽ đỏ vì một lý do không liên quan gì đến bài làm.
5. **Cài dependency của SUT**.
6. **Xác định chế độ chạy** (`contract` hoặc `full`).
7. **Chạy Newman cho cả 3 API**, mỗi API khởi động lại backend trước (xem mục 2).
8. **Tổng hợp kết quả vào Job Summary** bằng `summarize_newman.py`.
9. **Kiểm chứng header `X-Student-Id`** bằng `verify_header.py`, kết quả in thẳng vào Job Summary.
10. **Upload artifact** báo cáo HTML/JSON.
11. **In log của SUT** nếu job thất bại; **dừng backend** trong mọi trường hợp.

## 2. Hai quyết định cấu hình em muốn giải thích

### 2.1 Khởi động lại backend trước **mọi** collection

`backend/database.js` gọi `initDatabase()` ngay khi module được `require`, và hàm đó bắt đầu
bằng một loạt `DROP TABLE`. Nên khởi động lại backend chính là cách đưa CSDL về trạng thái
seed gốc.

Đây không phải tối ưu cho đẹp mà là **điều kiện để kết quả có nghĩa**. SUT có bug **A-09**:
mỗi lần đăng nhập sai cộng `+2` vào `login_attempts` và khóa tài khoản 180 giây khi đạt 3.
Nếu chạy collection thứ hai trên CSDL của collection thứ nhất, tài khoản test đã bị khóa và
hàng loạt test sẽ thất bại vì một lý do không liên quan gì đến chất lượng API. Lần chạy thử
nghiệm đầu tiên của em ở máy cục bộ dính đúng lỗi này: 7 test case thất bại dây chuyền từ
**một** nguyên nhân duy nhất.

### 2.2 Hai chế độ chạy, và vì sao em không ép bộ test đầy đủ phải xanh

SUT có **34 bug thật**. Bộ test đầy đủ (243 case, oracle là đặc tả) **phải đỏ** — đó là kết
quả kiểm thử đúng. Nếu ép nó xanh thì chỉ còn một cách: sửa kỳ vọng cho khớp với hành vi sai
của SUT, tức là **ngụy tạo kết quả**.

Vì vậy pipeline có hai chế độ:

| Chế độ | Chạy gì | Kỳ vọng | Dùng để làm gì |
|---|---|---|---|
| `contract` | 84 test case mà SUT **hiện đang** đáp ứng | ✅ XANH | Mốc hồi quy — báo động khi một điều đang đúng bị phá |
| `full` | Toàn bộ 243 test case, oracle là đặc tả | ❌ ĐỎ (đúng ý đồ) | Kết quả kiểm thử thật sự; đo khoảng cách giữa đặc tả và hiện thực |

Bộ `contract` **không** khẳng định "API này đúng". Nó khẳng định "những điều API này đang làm
đúng thì không được phá". Danh sách 84 case đó được suy ra từ **kết quả chạy thật** bằng
`scripts/derive_contract.py`, không phải từ phán đoán lúc thiết kế — xem
`postman/contract_baseline/API-*.txt`.

## 3. Hai lần chạy bắt buộc

### 3.1 Lần chạy PASS — chế độ `contract`

| | |
|---|---|
| **Commit** | `<điền hash sau khi push>` |
| **Thông điệp commit** | `ci: run all api tests (expect pass)` |
| **Link run** | `<điền link GitHub Actions>` |
| **Ảnh chụp** | `ci/evidence/ci_run_pass.png` |
| **Kết quả mong đợi** | 84 test case, **406 assertion, 0 thất bại**, job xanh |

Kết quả em **đã kiểm chứng trên máy cục bộ** trước khi push (`ci/evidence/local_ci_run_pass.log`):

```
API-1 contract:  163 assertion,  0 that bai
API-2 contract:  164 assertion,  0 that bai
API-3 contract:   79 assertion,  0 that bai
------------------------------------------
Tong:            406 assertion,  0 that bai   -> exit code 0
```

### 3.2 Lần chạy FAIL — làm sai đúng **một** assertion

| | |
|---|---|
| **Commit** | `<điền hash sau khi push>` |
| **Thông điệp commit** | `ci: introduce one failing assertion to demo pipeline failure` |
| **Link run** | `<điền link GitHub Actions>` |
| **Ảnh chụp** | `ci/evidence/ci_run_fail.png` |
| **Kết quả mong đợi** | 406 assertion, **đúng 1 thất bại**, job đỏ |

Thay đổi được thực hiện bằng script, để tái lập và trả lại được:

```bash
python3 ci/inject_failing_test.py --apply    # lam sai 1 assertion
python3 ci/inject_failing_test.py --check    # xem dang o trang thai nao
python3 ci/inject_failing_test.py --revert   # tra lai nhu cu
```

Script đổi kỳ vọng mã trạng thái của `TC-A1-DOM-012` (`POST /api/reset-password` với dữ liệu
hợp lệ) từ **200** thành **201**. Em chọn đúng case này vì ba lý do:

- Nó nằm trong bộ hồi quy nên bình thường **chắc chắn PASS** — khi pipeline đỏ thì lý do duy
  nhất là thay đổi vừa chèn vào, không thể do nguyên nhân khác.
- Nó là case DOM đầu tiên của bộ hồi quy API-1 nên xuất hiện sớm trong log CI, dễ nhìn thấy.
- Nhầm `200` với `201` là lỗi con người hay mắc thật (quy ước REST cho thao tác tạo mới), nên
  nó minh họa đúng loại lỗi mà pipeline sinh ra để bắt — thay vì một lỗi bịa đặt.

Kết quả em **đã kiểm chứng trên máy cục bộ** (`ci/evidence/local_ci_run_fail.log`):

```
API-1 contract:  163 assertion,  1 that bai
API-2 contract:  164 assertion,  0 that bai
API-3 contract:   79 assertion,  0 that bai

 1.  AssertionError  TC-A1-DOM-012 | HTTP 200
                     expected response to have status code 201 but got 200

newman exit code = 1   -> GitHub Actions danh dau job that bai
```

> Lưu ý kỹ thuật: `scripts/run_newman.sh` dùng cờ `--suppress-exit-code` để một API đỏ không
> làm đứt chuỗi chạy các API còn lại ở máy cục bộ. Workflow CI **không** dùng cờ đó — nó thu
> mã thoát của từng lần chạy và trả về mã khác 0 ở cuối job, nên GitHub Actions đánh dấu job
> là thất bại đúng như mong đợi.

## 4. Bằng chứng header `X-Student-Id` ngay trong pipeline

Bước **"Kiểm chứng header X-Student-Id"** chạy `verify_header.py`, đọc thẳng phần
`request.header` mà Newman ghi lại cho từng request thật sự rời đường, rồi in kết quả vào
**Job Summary** của GitHub Actions. Nghĩa là bằng chứng chống gian lận nằm ngay trong trang
kết quả của pipeline, ai mở link cũng xem được, không phụ thuộc vào một ảnh chụp màn hình.

Kết quả ở máy cục bộ: **823/823 request mang `X-Student-Id: 23127060`, không request nào
thiếu** — xem `ci/evidence/header_evidence.md`.

## 5. CÔNG VIỆC CÒN LẠI CỦA EM (HUMAN H5)

> Toàn bộ phần cấu hình và kiểm chứng logic đã xong và **đã chạy đúng ở máy cục bộ**. Phần còn
> lại bắt buộc em phải tự thực hiện vì nó đòi hỏi quyền đẩy mã lên GitHub.
>
> Thư mục làm việc đang trỏ tới remote `https://github.com/thangak18/HW06.git` — **không phải
> tài khoản của em** (`gh` đang đăng nhập bằng `nvkhai238`). Vì vậy em không tự động đẩy mã
> lên: việc đẩy mã vào repo của người khác phải được chính chủ đồng ý trước.

### Các bước

1. **Chốt repo sẽ dùng.** Hoặc xin quyền ghi vào `thangak18/HW06`, hoặc fork về tài khoản
   `nvkhai238` rồi đổi remote:
   ```bash
   gh repo fork thangak18/HW06 --clone=false --remote=false
   git remote add mine https://github.com/nvkhai238/HW06.git
   ```
2. **Đẩy mã và tạo lần chạy PASS:**
   ```bash
   git push mine main
   gh workflow run "API Tests 23127060" -f mode=contract
   gh run watch
   ```
   Đợi job xanh, chụp màn hình → `ci/evidence/ci_run_pass.png`, chép link run vào mục 3.1.
3. **Tạo lần chạy FAIL:**
   ```bash
   python3 ci/inject_failing_test.py --apply
   git add -A && git commit -m "ci: introduce one failing assertion to demo pipeline failure"
   git push mine main
   gh run watch
   ```
   Đợi job đỏ, chụp màn hình (phải thấy rõ dòng `TC-A1-DOM-012 ... expected 201 but got 200`)
   → `ci/evidence/ci_run_fail.png`, chép link run vào mục 3.2.
4. **Trả lại trạng thái bình thường:**
   ```bash
   python3 ci/inject_failing_test.py --revert
   git add -A && git commit -m "ci: revert the demo failing assertion"
   git push mine main
   ```
5. **Điền hai commit hash và hai link run** vào bảng ở mục 3.
6. **Công khai repo** (đề bài mục 14 đòi link GitHub công khai) và điền link vào `README.md`.

### Bảng kiểm trước khi coi là xong

- [ ] Link run PASS, job xanh, artifact tải về được
- [ ] Link run FAIL, job đỏ, log có dòng `TC-A1-DOM-012 ... expected 201 but got 200`
- [ ] `ci/evidence/ci_run_pass.png` và `ci/evidence/ci_run_fail.png`
- [ ] Hai commit hash đã điền vào mục 3
- [ ] Đã chạy `inject_failing_test.py --revert` và commit lại
