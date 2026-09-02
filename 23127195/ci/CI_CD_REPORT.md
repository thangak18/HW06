# Báo cáo CI/CD

**HW06 · 23127195** · Workflow: [`.github/workflows/newman-23127195.yml`](../../.github/workflows/newman-23127195.yml)

---

## 1. Vấn đề thiết kế: một pipeline luôn đỏ là một pipeline vô dụng

SUT hiện có **24 khiếm khuyết**, tương ứng **52/144 test case FAIL**. Nếu đưa thẳng cả bộ test
vào CI với quy tắc thông thường *"có test đỏ thì build đỏ"*, pipeline sẽ **luôn đỏ ở mọi commit**.
Một pipeline luôn đỏ thì lập trình viên sẽ ngừng nhìn nó sau vài ngày, và giá trị cảnh báo bằng
không — đúng lúc nó cần cảnh báo thì không ai để ý.

Vì vậy pipeline được thiết kế **hai tầng**:

| Tầng | Nội dung | Chặn build? | Ý nghĩa khi đỏ |
|---|---|---|---|
| **1 — Baseline** | 92 test case **hiện đang đạt**, liệt kê tường minh trong [`baseline_allowlist.json`](./baseline_allowlist.json) | ✅ **Có** | Có **hồi quy** — một thứ đang chạy được vừa bị làm hỏng |
| **2 — Full suite** | Cả 144 test case | ❌ Không | Theo dõi tiến độ sửa 24 lỗi đã báo cáo |
| **2b — Data-driven** | 39 iteration từ 3 file CSV | ❌ Không | Kiểm tra bảng phân vùng / bảng quyết định |

Khi một khiếm khuyết được sửa, test case tương ứng được **thêm vào allowlist** và từ đó trở thành
một phần của cổng chặn — bảo vệ chính bản sửa đó khỏi bị phá vỡ lần sau. Đây là cơ chế để bộ test
lớn dần theo tiến độ sửa lỗi thay vì bị tắt đi.

## 2. Cấu hình pipeline

**Kích hoạt:** push vào `main` (chỉ khi có thay đổi trong `23127195/**`), pull request, hoặc chạy tay.
**Runner:** `ubuntu-latest`, Node.js 22, giới hạn 20 phút.

### Các bước

| # | Bước | Mục đích |
|---|---|---|
| 1 | Checkout bài làm | |
| 2 | Cài Node.js 22 | Khớp phiên bản chạy local (v22.20.0) |
| 3 | **Clone SUT** (`ttbhanh/eshop-sut`) | SUT không nằm trong repo bài làm nên phải lấy về lúc chạy |
| 4 | `npm install` cho backend SUT | |
| 5 | **Khởi động SUT** + chờ sẵn sàng | Thăm dò `GET /api/products` tối đa 60 giây rồi mới chạy test |
| 6 | Cài Newman | |
| 7 | **Kiểm tra collection đồng bộ với nguồn** | Chạy lại 3 script sinh collection rồi `git diff`. Nếu lệch → build đỏ. Chống việc ai đó sửa tay collection làm nó lệch khỏi `testcases/*.json` |
| 8 | **Tầng 1 — Baseline** | Được phép làm đỏ build |
| 9 | Tầng 2 — Full suite | `continue-on-error: true` |
| 10 | Tầng 2b — Data-driven | `continue-on-error: true` |
| 11 | Tổng hợp vào Job Summary | Bảng số liệu hiển thị ngay trên trang run |
| 12 | Tải lên artifact | Báo cáo HTML/JSON/JUnit, giữ 30 ngày |

### Hai điểm đáng chú ý trong cấu hình

**a) SUT khởi động lại giữa các lần chạy là điều bắt buộc.** `backend/database.js` thực hiện
`DROP TABLE` rồi seed lại **mỗi lần server khởi động**. Đây vừa là ràng buộc vừa là lợi thế: nó
đảm bảo mọi lần chạy đều xuất phát từ đúng một trạng thái dữ liệu. Script chạy local
[`scripts/run_newman.sh`](../scripts/run_newman.sh) restart SUT trước mỗi lần chạy vì lý do này.

**b) Bước 7 chống lệch nguồn.** Vì collection được **sinh ra** từ `testcases/*.json`, việc sửa tay
file collection sẽ bị mất ở lần sinh tiếp theo. Bước này biến sự lệch đó thành lỗi build ngay
lập tức thay vì để nó âm thầm gây nhầm lẫn.

## 3. Bằng chứng chạy thật (local)

Chạy trên máy trước khi đưa lên CI, cùng cấu hình lệnh:

### Tầng 1 — Baseline: **XANH**

```
baseline_api1_fr04_user_profile      assertions: 183   failed: 0
baseline_api2_fr09_apply_coupon      assertions: 160   failed: 0
baseline_api3_fr16_import_products   assertions: 207   failed: 0
────────────────────────────────────────────────────────────────
TỔNG                                 assertions: 550   failed: 0     ✅
```

### Tầng 2 — Full suite: 52 FAIL (kết quả **mong đợi**)

| Collection | Request | Assertion | FAIL | Test case FAIL |
|---|---|---|---|---|
| `api1_fr04_user_profile` | 88 | 256 | 23 | 20 |
| `api2_fr09_apply_coupon` | 57 | 210 | 20 | 12 |
| `api3_fr16_import_products` | 96 | 280 | 30 | 20 |
| **Tổng** | **241** | **746** | **73** | **52** |

Toàn bộ 52 test case FAIL đều truy vết được về một trong 24 mã lỗi trong
[`../bugs/BUG_REPORTS.md`](../bugs/BUG_REPORTS.md).

### Tầng 2b — Data-driven

| Collection | File dữ liệu | Iteration | Assertion | FAIL |
|---|---|---|---|---|
| `dd1_phone_partitions` | `api1_phone_partitions.csv` | 15 | 105 | 12 |
| `dd2_coupon_decision_table` | `api2_coupon_decision_table.csv` | 14 | 83 | 25 |
| `dd3_import_rows` | `api3_import_rows.csv` | 10 | 48 | 12 |

Báo cáo HTML của cả ba nằm trong [`../newman/`](../newman/).

## 4. Hai commit mẫu theo yêu cầu §6 của đề bài

Đề bài yêu cầu *"two sample commits: one whose pipeline run shows all API test cases passing, and
another whose pipeline run shows one test case failing"*.

### Commit A — pipeline **xanh**

Trạng thái hiện tại của nhánh. Allowlist gồm đúng 92 test case đang đạt → tầng 1 xanh → build xanh.

```bash
git log --oneline -1        # commit A
```

### Commit B — pipeline **đỏ với đúng một test case FAIL**

Kịch bản mô phỏng đúng tình huống thực tế: *một lập trình viên tuyên bố đã sửa lỗi ngưỡng đơn hàng
(BUG-A2-03) và thêm test case tương ứng vào cổng chặn — CI chứng minh lỗi vẫn còn.*

Cách tạo commit B — chỉ thêm **một dòng** vào allowlist:

```bash
cd 23127195
python - <<'PY'
import json, io
p = 'ci/baseline_allowlist.json'
d = json.load(open(p, encoding='utf-8'))
d['test_case_dat'] = sorted(set(d['test_case_dat']) | {'TC-A2-013'})
d['_ghi_chu_commit_B'] = ('Them TC-A2-013 (BVA: don bang dung min_order_amount) vao cong chan '
                          'de mo phong tinh huong lap trinh vien tuyen bo da sua BUG-A2-03. '
                          'CI se chung minh loi van con -> pipeline do voi dung 1 test case FAIL.')
io.open(p, 'w', encoding='utf-8', newline='').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
PY
python postman/scripts/build_baseline.py
git add ci/baseline_allowlist.json postman/collections/baseline_*
git commit -m "ci: them TC-A2-013 vao cong chan hoi quy (BUG-A2-03 duoc bao la da sua)"
git push
```

Kết quả mong đợi: **tầng 1 đỏ**, đúng **một** test case FAIL — `TC-A2-013` với thông báo

```
AssertionError  Status code la 200
                expected response to have status code 200 but got 400
                inside "TC-A2-013 BVA min: SAVE10 voi total = 300.000 (= min) -> PHAI duoc chap nhan"
```

Để quay lại trạng thái xanh, chạy lại:
```bash
python postman/scripts/build_baseline.py --refresh
```

---

## 5. ⚠ Việc sinh viên phải tự làm

Phần này **không thể** hoàn tất từ máy local — phải push lên GitHub thì Actions mới chạy:

| # | Việc | Ghi chú |
|---|---|---|
| 1 | `git push` để kích hoạt lần chạy đầu (commit A) | Repo `thangak18/HW06` |
| 2 | **Chụp màn hình lần chạy xanh** + lưu link run | → `ci/evidence/run_A_pass.png` |
| 3 | Tạo commit B theo hướng dẫn §4, push | |
| 4 | **Chụp màn hình lần chạy đỏ** (thấy rõ 1 test FAIL) + lưu link | → `ci/evidence/run_B_fail.png` |
| 5 | Chạy lại `build_baseline.py --refresh`, commit, push để trả về xanh | Tuỳ chọn |
| 6 | Điền hai link run vào bảng dưới đây | |

| Lần chạy | Commit | Kết quả | Link |
|---|---|---|---|
| A | `<điền SHA>` | ✅ Xanh | `<điền link GitHub Actions run>` |
| B | `<điền SHA>` | ❌ Đỏ — 1 test FAIL | `<điền link GitHub Actions run>` |

> **Lưu ý:** workflow chỉ kích hoạt khi có thay đổi trong `23127195/**`. Nếu cần chạy tay,
> dùng nút **Run workflow** trên tab Actions (đã bật `workflow_dispatch`).
