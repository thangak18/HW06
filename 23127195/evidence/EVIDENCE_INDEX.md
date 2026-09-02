# Chỉ mục bằng chứng — HW06 · 23127195

Tài liệu này liệt kê **mọi bằng chứng có thể kiểm chứng được** của bài làm, để người chấm đối
chiếu nhanh. Cột *Kiểm chứng bằng cách nào* nêu rõ cách xác minh từng mục.

---

## 1. Bằng chứng bắt buộc theo §11 (Anti-AI-Cheat)

| # | Hạng mục | Trạng thái | Vị trí | Kiểm chứng bằng cách nào |
|---|---|---|---|---|
| 1 | **Header `X-Student-Id`** trong mọi request | ✅ Có | Pre-request script cấp collection của cả 9 collection | Mở bất kỳ file `postman/collections/*.json`, tìm `X-Student-Id` trong khối `event[listen=prerequest]` |
| 1b | **Log console** của header | ✅ Có | [`newman/*.console.log`](../newman/) | `grep -c "X-Student-Id" newman/*.console.log` → **604 dòng** trên 6 file (3 API + 3 lần chạy data-driven) |
| 1c | **Ảnh chụp Postman Console** | ✅ Có | [`postman_console.png`](./postman_console.png) · [`postman_console_runner.png`](./postman_console_runner.png) · [`postman_console_timestamps.png`](./postman_console_timestamps.png) | Ảnh `_timestamps` là ảnh mạnh nhất: khối *Request Headers* đã bung sẵn, thấy `X-Student-Id: "23127195"` là header **thật trên đường truyền** chứ không chỉ là dòng `console.log` |
| 1d | **Assertion tự động kiểm header** | ✅ Có | Test script cấp collection của cả 9 collection | **334 lần kiểm, 0 lần trượt** — assertion `[GLOBAL]` áp lên mọi request và kiểm cả định dạng `/^\d{8}$/`. Máy kiểm, không phải mắt người nhìn |
| 2 | **Newman output với hostname khớp deployment** | ✅ Có | [`newman/`](../newman/) · [`postman_console_timestamps.png`](./postman_console_timestamps.png) | Mọi URL trong log đều là `http://localhost:3000` — `localhost` được đề bài chấp nhận. Ảnh `_timestamps` cho thấy trực tiếp header `Host: "localhost:3000"` |
| 3 | **Sơ đồ tự vẽ** | ✅ Có | [`agent-skill/diagram/ai_test_generator_diagram.png`](../agent-skill/diagram/ai_test_generator_diagram.png) | SV tự dựng bằng draw.io; kèm file nguồn `.drawio` mở lại được để kiểm chứng. Repo không chứa bản vẽ do AI sinh |

## 2. Bằng chứng thi hành

| Hạng mục | Vị trí | Số liệu |
|---|---|---|
| Báo cáo HTML (htmlextra) — API-1 | `newman/api1_20260901-204738.html` | 88 request · 256 assertion · 23 FAIL |
| Báo cáo HTML — API-2 | `newman/api2_20260901-204738.html` | 57 request · 210 assertion · 20 FAIL |
| Báo cáo HTML — API-3 | `newman/api3_20260901-204738.html` | 96 request · 280 assertion · 30 FAIL |
| Báo cáo JSON (máy đọc được) | `newman/*_20260901-204738.json` | Nguồn số liệu cho mọi bảng trong báo cáo |
| Báo cáo JUnit XML | `newman/*_20260901-204738.xml` | Định dạng chuẩn cho CI |
| Log console đầy đủ | `newman/*_20260901-204738.console.log` | Chứa dòng `[X-Student-Id]` cho từng request |
| Log của SUT khi chạy | `newman/sut-server.log` | Xác nhận SUT khởi động và seed lại dữ liệu |
| Data-driven — phân vùng phone | `newman/dd1_phone_partitions.html` | 15 iteration · 105 assertion · 12 FAIL |
| Data-driven — bảng quyết định coupon | `newman/dd2_coupon_decision_table.html` | 14 iteration · 83 assertion · 25 FAIL |
| Data-driven — phân vùng import | `newman/dd3_import_rows.html` | 10 iteration · 48 assertion · 12 FAIL |

**Cách kiểm chứng số liệu:**
```bash
python - <<'PY'
import json, glob
for f in sorted(glob.glob('newman/api*_20260901-204738.json')):
    st = json.load(open(f, encoding='utf-8'))['run']['stats']
    print(f, st['requests']['total'], st['assertions']['total'], st['assertions']['failed'])
PY
```

## 3. Bằng chứng lỗi

| Hạng mục | Vị trí | Ghi chú |
|---|---|---|
| Báo cáo 24 lỗi | [`bugs/BUG_REPORTS.md`](../bugs/BUG_REPORTS.md) | Mỗi lỗi có: mức độ, điều khoản vi phạm, bước tái hiện, kết quả kỳ vọng/thực tế, tác động, vị trí trong mã nguồn, đề xuất sửa |
| **Script tái hiện độc lập** | [`bugs/reproduce_bugs.sh`](../bugs/reproduce_bugs.sh) | Chỉ dùng `curl` — người chấm **không cần cài Postman** |
| Output tái hiện thật | [`bugs/evidence/reproduce_output.txt`](../bugs/evidence/reproduce_output.txt) | 218 dòng, chạy lúc 2026-09-02 16:20:53 +0700. Mỗi lệnh `curl` được **in ra đúng như khi chạy** — người chấm copy lại chạy được ngay |
| **24 GitHub Issue đã tạo thật** | [issue #5 → #28](https://github.com/thangak18/HW06/issues?q=is%3Aissue+label%3Ahw06-23127195) | ✅ Nhãn `hw06-23127195`; nội dung gốc tại [`bugs/GITHUB_ISSUES.md`](../bugs/GITHUB_ISSUES.md) |
| Ảnh chụp lỗi | [`bugs/screenshots/`](../bugs/screenshots/) | ✅ 32 ảnh chụp toàn màn hình cho 24 mã lỗi (8 mã dài phải cắt làm 2 ảnh). Mỗi ảnh hiện **lệnh curl đầy đủ** rồi mới đến response |

**Cách kiểm chứng:**
```bash
# khởi động SUT rồi chạy
bash bugs/reproduce_bugs.sh | less
```

## 4. Truy vết từ test case đến lỗi

Mọi test case FAIL đều truy được về một mã lỗi cụ thể:

| Nguồn | Cột / trường | Ý nghĩa |
|---|---|---|
| [`testcases/TESTCASES_23127195.xlsx`](../testcases/TESTCASES_23127195.xlsx) | *Mã lỗi* | Nối test case ↔ bug |
| | *Nguồn (AI/HUMAN)* | Phân biệt test case do AI sinh và do người thêm |
| | *Nhãn audit* + *Lý do audit* | Kết quả rà soát của con người |
| | *Kết quả chạy thật (Newman)* | Thông báo assertion thật, trích từ báo cáo JSON |
| `testcases/*_testcases.json` | `known_defect` | Cùng thông tin, dạng máy đọc được |

**Cách kiểm chứng liên kết:**
```bash
python - <<'PY'
import json, glob
for f in glob.glob('testcases/*_testcases.json'):
    d = json.load(open(f, encoding='utf-8'))
    for c in d['cases']:
        if c.get('known_defect'):
            print('%-12s -> %s' % (c['id'], c['known_defect']))
PY
```

## 5. Bằng chứng CI/CD

| Hạng mục | Vị trí | Trạng thái |
|---|---|---|
| Workflow | [`.github/workflows/newman-23127195.yml`](../../.github/workflows/newman-23127195.yml) | ✅ YAML hợp lệ, 13 bước |
| Báo cáo CI/CD | [`ci/CI_CD_REPORT.md`](../ci/CI_CD_REPORT.md) | ✅ |
| Danh sách cổng chặn hồi quy | [`ci/baseline_allowlist.json`](../ci/baseline_allowlist.json) | ✅ 157 mục (92 test case + setup) |
| Chứng minh baseline xanh (local) | `ci/CI_CD_REPORT.md` §3 | ✅ 550 assertion, 0 FAIL |
| **Lần chạy mẫu A — xanh** | [Actions run #3](https://github.com/thangak18/HW06/actions/runs/33609193249) · commit `3de872b` | ✅ Chạy thật, log do GitHub lưu — kiểm chứng trực tiếp, không cần ảnh chụp |
| **Lần chạy mẫu B — đỏ đúng 1 test case** | [Actions run #4](https://github.com/thangak18/HW06/actions/runs/33609400346) · commit `03d0cb9` | ✅ Chỉ bước *Tầng 1 · Baseline* đỏ; `TC-A2-013` là test case duy nhất trượt |
| Cả hai nằm trong cùng một pull request | [PR #35](https://github.com/thangak18/HW06/pull/35) | Hai lần chạy cách nhau đúng một commit, mọi yếu tố khác giữ nguyên |

## 6. Bằng chứng về quá trình dùng AI

| Hạng mục | Vị trí |
|---|---|
| Khai báo bắt buộc + bảng công cụ | [`ai/AI_AUDIT_REPORT.md`](../ai/AI_AUDIT_REPORT.md) §1–2 |
| 12 lượt tương tác (prompt nguyên văn + output + phán quyết review) | [`ai/interactions/SESSION-01_2026-09-01.md`](../ai/interactions/SESSION-01_2026-09-01.md) |
| 4 nhóm sai sót của AI đã được sửa | [`ai/AI_AUDIT_REPORT.md`](../ai/AI_AUDIT_REPORT.md) §4 |
| Phê bình AI (296 từ) | [`ai/AI_CRITIQUE.md`](../ai/AI_CRITIQUE.md) |
| 6 prompt theo từng bước | [`ai/prompts/PROMPT_LIBRARY.md`](../ai/prompts/PROMPT_LIBRARY.md) |

**Mốc thời gian đối chứng được** (chứng minh phiên làm việc là thật):
- JWT `iat = 1788263362` → `2026-09-01 18:49:22 +07` — lần đăng nhập admin đầu tiên
- npm debug log `2026-09-01T11_47_21Z` → `18:47:21 +07` — lúc cài Newman
- `bugs/evidence/reproduce_output.txt` dòng 2 → `2026-09-02 16:20:53 +0700`
- Dấu thời gian tên file báo cáo Newman → `20260901-204738`
- Ảnh [`postman_console_timestamps.png`](./postman_console_timestamps.png) — ba mốc thời gian **độc lập nhau
  nhưng khớp nhau** trong cùng một khung hình: dấu thời gian console `15:07:56.847`, header
  `Date: "Wed, 02 Sep 2026 08:07:56 GMT"` do SUT trả về (= 15:07:56 giờ VN), và đồng hồ Windows
  `3:16 PM 9/2/2026` lúc chụp. Ba nguồn này không thể dựng khớp nhau nếu ảnh là giả

## 7. Git commit log

| Hạng mục | Vị trí |
|---|---|
| Commit log dạng text | [`git_commit_log.txt`](./git_commit_log.txt) — 19 commit |
| Script sinh lại file trên | [`scripts/export_git_log.py`](../scripts/export_git_log.py) — `python scripts/export_git_log.py` |

Theo §12 của đề bài, mỗi bước của quy trình có một commit riêng. Bảng đối chiếu commit ↔ bước
nằm ngay đầu file `git_commit_log.txt`.

---

## 8. Cách tái hiện ảnh chụp Postman Console (mục 1c)

> ✅ **Mục này đã hoàn tất** — ba ảnh nằm sẵn trong thư mục này. Phần dưới giữ lại để người chấm
> tự dựng lại được cùng một bằng chứng trên máy của mình.

1. Mở Postman desktop.
2. **Import** collection: `File → Import` → chọn `postman/collections/api1_fr04_user_profile.postman_collection.json`.
3. **Import** environment: `postman/environments/eshop-local.postman_environment.json`, rồi chọn nó ở góc trên bên phải.
4. Khởi động SUT: `cd ../../.sut/eshop-sut/backend && node server.js`
5. Mở Console: **View → Show Postman Console** (hoặc `Ctrl+Alt+C`).
6. Chạy collection: chọn collection → **Run** → **Run HW06 - 23127195 - API-1**.
7. Quay lại cửa sổ Console — sẽ thấy các dòng:
   ```
   [X-Student-Id] 23127195  ->  PUT /api/users/me
   [X-Student-Id] 23127195  ->  GET /api/users/me
   ```
8. **Chụp màn hình** sao cho thấy rõ **cả mã số sinh viên và tên request**, lưu thành
   `evidence/postman_console.png`.

> Đây là bằng chứng chống gian lận bắt buộc theo §11 — TA có kiểm tra mục này.
