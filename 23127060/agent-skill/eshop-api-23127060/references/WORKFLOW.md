# WORKFLOW — 10 bước chi tiết (HW06, SV 23127060)

Quy ước: đứng ở `23127060/`. Đặt `S=agent-skill/eshop-api-23127060/scripts`.
Repo root là `HW06/` (2 cấp trên).

---

## STEP 0 — Trinh sát môi trường & đọc spec thật

```bash
node -v && npm -v && python3 -V
newman -v || npm i -g newman newman-reporter-htmlextra
ls ../../../eshop-sut/backend/ 2>/dev/null || echo "CAN HOI USER duong dan SUT"
```

Việc phải làm:
1. Đọc `eshop-sut/api_specification.md` — **đối chiếu từng endpoint với `server.js`**.
2. Đối chiếu bảng SEC-01..SEC-07 trong `references/API_SPEC_NOTES.md` với spec thật.
   Khác => sửa lại file đó và báo CRITICAL [C3].
3. Đọc `../../docs/team-api-allocation.md` (chỉ đọc) kiểm tra 3 API không trùng nhóm.
4. Ghi `report/00_environment.md`: version Node/npm/newman/Postman, OS, base URL,
   đường dẫn SUT, cách khởi động backend.

**Output:** `report/00_environment.md` + (nếu cần) bản vá `references/API_SPEC_NOTES.md`.
**Commit:** `HW06(23127060): step0 - trinh sat moi truong va doi chieu spec`

---

## STEP 1 — Lập spec máy đọc được

Sinh 3 file `spec/api-1.json`, `spec/api-2.json`, `spec/api-3.json` theo schema mô tả
sẵn trong `spec/_SCHEMA.md`. Mỗi file gồm: endpoints, params (kèm `partitions`),
`states` + `transitions`, `security` (SEC-01..07 áp dụng), `responseSchemas`.

Đây là **đầu vào của bộ sinh test** — tức là hiện thực hóa yêu cầu mục 7 đề bài
("given the API specification, it produces test cases automatically").

```bash
# kiem tra hop le
python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('spec/api-*.json')];print('spec OK')"
```

**Output:** `spec/api-1.json`, `spec/api-2.json`, `spec/api-3.json`
**Commit:** `HW06(23127060): step1 - lap spec may doc duoc cho 3 API`

---

## STEP 2 — Sinh test case (4 VÒNG PROMPT RIÊNG, không gộp)

Đề bài cấm "1 prompt tổng". Chạy đúng 4 vòng, **mỗi vòng 1 entry AI_log riêng**:

| Vòng | Nhóm | Mục tiêu | Lệnh |
|---|---|---|---|
| 2a | DOM | >=14/API | `python3 $S/gen_testcases.py --spec spec/api-1.json --only DOM --out testcases/API-1_generated.csv` |
| 2b | STA | >=8/API | `... --only STA --append` |
| 2c | SEC | >=9/API | `... --only SEC --append` |
| 2d | SCH | >=5/API | `... --only SCH --append` |

Lặp lại cho `api-2.json`, `api-3.json`.

Sau mỗi vòng, agent **đọc lại CSV** và bổ sung tay những case mà bộ sinh chưa bao phủ
(bộ sinh lọt các tổ hợp đặc thù — phần này chính là "drive it step by step").

```bash
# dem so case moi API
for f in testcases/API-*_generated.csv; do echo -n "$f: "; tail -n +2 "$f" | wc -l; done
```

**Output:** `testcases/API-1_generated.csv`, `API-2_generated.csv`, `API-3_generated.csv`
**Ghi lại:** nội dung 4 prompt (chính là 4 lần gọi + phần bổ sung tay) vào `ai/prompts/step2_*.md`.
**Commit:** 4 commit riêng, mỗi vòng 1 commit.

---

## STEP 3 — Audit VALID / INVALID / INCOMPLETE

1. Copy `*_generated.csv` -> `*_audited.csv`.
2. Với TỪNG case: điền `Audit_Label` + `Audit_Note` (>=1 câu lý do).
3. Sửa trực tiếp các case INVALID / INCOMPLETE trong file audited (ghi rõ đã sửa gì).
4. Sinh thống kê:

```bash
python3 - <<'PY'
import csv,glob,collections
for f in sorted(glob.glob('testcases/API-*_audited.csv')):
    c=collections.Counter(r['Audit_Label'] for r in csv.DictReader(open(f,encoding='utf-8')))
    print(f, dict(c))
PY
```

5. Viết `report/03_audit.md`: bảng thống kê + 5-8 ví dụ điển hình (trước/sau khi sửa).

> Cảnh báo: nếu tỷ lệ VALID > 85% thì audit chưa nghiêm túc. Đọc lại
> `references/TESTCASE_TAXONOMY.md` mục "Hướng dẫn gắn nhãn AUDIT".

**Human gate H2:** user chốt lại nhãn. Agent vẫn chạy tiếp, đánh dấu `pending` trong AI_log.
**Commit:** `HW06(23127060/API-n): step3 audit - gan nhan va sua case`

---

## STEP 4 — Extend >= 5 case/API

Thêm case mới với `Source=HUMAN`, `TC_ID` bắt đầu từ `900`.
Mỗi case bắt buộc có cột `Why_AI_Missed` (1 trong 4 lý do ở TAXONOMY).

```bash
cp testcases/API-1_audited.csv testcases/API-1_final.csv
# them dong ... roi kiem tra
python3 - <<'PY'
import csv,glob
for f in sorted(glob.glob('testcases/API-*_final.csv')):
    rows=list(csv.DictReader(open(f,encoding='utf-8')))
    print(f,'tong',len(rows),'| HUMAN',sum(1 for r in rows if r['Source']=='HUMAN'))
PY
```

**Output:** `testcases/API-*_final.csv`, `report/04_extend.md`
**Commit:** `HW06(23127060/API-n): step4 extend - them N case AI bo sot`

---

## STEP 5 — Build Postman collection

```bash
python3 $S/build_collection.py \
  --csv testcases/API-1_final.csv \
  --api API-1 --sid 23127060 \
  --out postman/collections/23127060_HW06_API-1.postman_collection.json

python3 $S/build_collection.py --env-only --sid 23127060 \
  --out postman/environments/23127060_local.postman_environment.json
```

Sau đó:
- Kiểm tra JSON hợp lệ và đếm số request.
- Tạo data file `postman/data/brute_force_tokens.csv`, `postman/data/state_transitions.csv`.
- Lưu schema vào `postman/scripts/schemas/`.
- Viết `report/05_postman_features.md` theo `references/POSTMAN_GUIDE.md`.

**Commit:** `HW06(23127060): step5 - build 3 postman collection + environment`

---

## STEP 6 — Chạy Newman & thu bằng chứng

```bash
# 1) reset SUT ve trang thai biet truoc
node $S/seed_sut.js reset --db ../../../eshop-sut/backend/database.sqlite

# 2) bat backend (nen)
(cd ../../../eshop-sut/backend && nohup node server.js > /tmp/eshop.log 2>&1 &)
sleep 2 && curl -sf http://localhost:3000/api/products > /dev/null && echo "SUT UP"

# 3) chay
bash $S/run_newman.sh API-1
bash $S/run_newman.sh API-2
bash $S/run_newman.sh API-3

# 4) tong hop
python3 $S/summarize_newman.py --dir newman --out report/06_execution.md
```

Lưu ý:
- Các case tag `@bug` **sẽ fail** — đúng ý đồ. `run_newman.sh` chạy 2 lần:
  `--folder`-filter cho `@contract` (phải 100% pass) và full run (có fail).
- Chụp screenshot Postman Console (**HUMAN H4**) — phải thấy dòng `[HW06][23127060]`.

**Output:** `newman/*.json`, `newman/*.html`, `report/06_execution.md`
**Commit:** `HW06(23127060): step6 - chay newman va thu ket qua`

---

## STEP 7 — Bug report + GitHub Issues

1. Với mỗi bug **đã được chứng minh bằng request thật**, viết 1 mục trong
   `bugs/BUG_REPORT.md`: ID, tiêu đề, mức độ, SEC ref, endpoint, bước tái hiện
   (curl đầy đủ), kết quả thực tế (response thật), kết quả mong đợi (trích spec),
   ảnh hưởng, đề xuất fix (trỏ tới dòng code).
2. Sinh sẵn file để human copy-paste lên GitHub Issues:
   `bugs/ISSUE_TEMPLATES/<BUG_ID>.md`.
3. **HUMAN H3:** mở Issue, chụp screenshot, lưu vào `bugs/screenshots/<BUG_ID>.png`,
   điền link Issue ngược lại vào `BUG_REPORT.md`.

**Commit:** `HW06(23127060): step7 - bug report N bug`

---

## STEP 8 — CI/CD (GitHub Actions)

```bash
mkdir -p ../../.github/workflows
cp ci/api-tests-23127060.yml ../../.github/workflows/api-tests-23127060.yml
```

Workflow phải: checkout, setup node, cài deps SUT, khởi động backend nền, wait-on,
cài newman + htmlextra, chạy 3 collection, upload artifact HTML.

Hai run bắt buộc:
- **Run PASS:** chạy collection `@contract`. Commit `ci: run all api tests (expect pass)`.
- **Run FAIL:** sửa **đúng 1** assertion cho sai (vd đổi `expect 200` thành `expect 201`
  trong 1 test) hoặc thêm 1 case `@bug` vào workflow. Commit
  `ci: introduce one failing assertion to demo pipeline failure`.

**HUMAN H5:** push, đợi 2 run xong, chụp screenshot + copy link vào `ci/CI_CD_REPORT.md`.

**Output:** `.github/workflows/api-tests-23127060.yml`, `ci/CI_CD_REPORT.md`, `ci/evidence/*.png`

---

## STEP 9 — Agent Skill: bộ sinh test tự động (G9.5, 10 điểm)

1. `agent-skill/pseudocode/generator.pseudo.md` — pseudocode đầy đủ (đã có bản nháp).
2. `agent-skill/eshop-api-23127060/scripts/gen_testcases.py` — **bản hiện thực thật**,
   chạy được, là bằng chứng mạnh nhất cho mục này.
3. `agent-skill/diagram/DIAGRAM_BRIEF.md` — mô tả khối + luồng để **HUMAN tự vẽ**.
   > Đề bài mục 11: diagram **không được do AI sinh**. Agent TUYỆT ĐỐI không tạo
   > file ảnh/mermaid cho diagram này. Chỉ mô tả bằng chữ.
4. **HUMAN H1:** vẽ diagram (draw.io / Excalidraw / vẽ tay chụp ảnh) ->
   `agent-skill/diagram/23127060_generator_diagram.png`.
5. **HUMAN H6 (khuyến khích):** quay video demo generator sinh test cho 1 API,
   up YouTube unlisted, điền link vào `README.md`.

**Commit:** `HW06(23127060): step9 - agent skill generator + pseudocode`

---

## STEP 10 — Báo cáo chính + AI Audit + Critique + validate

```bash
# 1) Excel test case + sheet summary
python3 $S/tc_to_excel.py --csv testcases/API-1_final.csv testcases/API-2_final.csv \
    testcases/API-3_final.csv --out testcases/23127060_HW06_testcases.xlsx

# 2) AI Audit Report tu AI_log
python3 $S/ai_log.py build-audit --root . --sid 23127060

# 3) AI Critique (200-300 tu) - dem tu truoc khi nop
python3 -c "print(len(open('ai/critique/AI_CRITIQUE.md',encoding='utf-8').read().split()))"

# 4) Git log
git log --pretty=format:'%h | %ad | %s' --date=iso -- . > git-log/23127060_git_commit_log.txt

# 5) Kiem tra du deliverable
python3 $S/validate_submission.py --root . --sid 23127060
```

Viết `report/MAIN_REPORT.md` theo `references/REPORT_OUTLINE.md`, cập nhật `README.md`
(bảng tự đánh giá + test summary), rồi:

```bash
# xuat PDF (dung script cua bo skill, khong can pandoc)
python3 $S/md_to_pdf.py
```

**Nén nộp:**
```bash
cd ../ && zip -r 23127060_HW06_AI_API_<3 chu so>.zip 23127060/ -x '*/node_modules/*' '*/.git/*'
```

**Commit:** `HW06(23127060): step10 - bao cao chinh, AI audit, critique`
