# WORKFLOW — 10 buoc chi tiet (HW06, SV 23127060)

Quy uoc: dung o `23127060/`. Dat `S=agent-skill/eshop-api-23127060/scripts`.
Repo root la `HW06/` (2 cap tren).

---

## STEP 0 — Trinh sat moi truong & doc spec that

```bash
node -v && npm -v && python3 -V
newman -v || npm i -g newman newman-reporter-htmlextra
ls ../../../eshop-sut/backend/ 2>/dev/null || echo "CAN HOI USER duong dan SUT"
```

Viec phai lam:
1. Doc `eshop-sut/api_specification.md` — **doi chieu tung endpoint voi `server.js`**.
2. Doi chieu bang SEC-01..SEC-07 trong `references/API_SPEC_NOTES.md` voi spec that.
   Khac => sua lai file do va bao CRITICAL [C3].
3. Doc `../../docs/team-api-allocation.md` (chi doc) kiem tra 3 API khong trung nhom.
4. Ghi `report/00_environment.md`: version Node/npm/newman/Postman, OS, base URL,
   duong dan SUT, cach khoi dong backend.

**Output:** `report/00_environment.md` + (neu can) ban vá `references/API_SPEC_NOTES.md`.
**Commit:** `HW06(23127060): step0 - trinh sat moi truong va doi chieu spec`

---

## STEP 1 — Lap spec may doc duoc

Sinh 3 file `spec/api-1.json`, `spec/api-2.json`, `spec/api-3.json` theo schema mo ta
san trong `spec/_SCHEMA.md`. Moi file gom: endpoints, params (kem `partitions`),
`states` + `transitions`, `security` (SEC-01..07 ap dung), `responseSchemas`.

Day la **dau vao cua bo sinh test** — tuc la hien thuc hoa yeu cau muc 7 de bai
("given the API specification, it produces test cases automatically").

```bash
# kiem tra hop le
python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('spec/api-*.json')];print('spec OK')"
```

**Output:** `spec/api-1.json`, `spec/api-2.json`, `spec/api-3.json`
**Commit:** `HW06(23127060): step1 - lap spec may doc duoc cho 3 API`

---

## STEP 2 — Sinh test case (4 VONG PROMPT RIENG, khong gop)

De bai cam "1 prompt tong". Chay dung 4 vong, **moi vong 1 entry AI_log rieng**:

| Vong | Nhom | Muc tieu | Lenh |
|---|---|---|---|
| 2a | DOM | >=14/API | `python3 $S/gen_testcases.py --spec spec/api-1.json --only DOM --out testcases/API-1_generated.csv` |
| 2b | STA | >=8/API | `... --only STA --append` |
| 2c | SEC | >=9/API | `... --only SEC --append` |
| 2d | SCH | >=5/API | `... --only SCH --append` |

Lap lai cho `api-2.json`, `api-3.json`.

Sau moi vong, agent **doc lai CSV** va bo sung tay nhung case ma bo sinh chua bao phu
(bo sinh lo cac to hop dac thu — phan nay chinh la "drive it step by step").

```bash
# dem so case moi API
for f in testcases/API-*_generated.csv; do echo -n "$f: "; tail -n +2 "$f" | wc -l; done
```

**Output:** `testcases/API-1_generated.csv`, `API-2_generated.csv`, `API-3_generated.csv`
**Ghi lai:** noi dung 4 prompt (chinh la 4 lan goi + phan bo sung tay) vao `ai/prompts/step2_*.md`.
**Commit:** 4 commit rieng, moi vong 1 commit.

---

## STEP 3 — Audit VALID / INVALID / INCOMPLETE

1. Copy `*_generated.csv` -> `*_audited.csv`.
2. Voi TUNG case: dien `Audit_Label` + `Audit_Note` (>=1 cau ly do).
3. Sua truc tiep cac case INVALID / INCOMPLETE trong file audited (ghi ro da sua gi).
4. Sinh thong ke:

```bash
python3 - <<'PY'
import csv,glob,collections
for f in sorted(glob.glob('testcases/API-*_audited.csv')):
    c=collections.Counter(r['Audit_Label'] for r in csv.DictReader(open(f,encoding='utf-8')))
    print(f, dict(c))
PY
```

5. Viet `report/03_audit.md`: bang thong ke + 5-8 vi du dien hinh (truoc/sau khi sua).

> Canh bao: neu ty le VALID > 85% thi audit chua nghiem tuc. Doc lai
> `references/TESTCASE_TAXONOMY.md` muc "Huong dan gan nhan AUDIT".

**Human gate H2:** user chot lai nhan. Agent van chay tiep, danh dau `pending` trong AI_log.
**Commit:** `HW06(23127060/API-n): step3 audit - gan nhan va sua case`

---

## STEP 4 — Extend >= 5 case/API

Them case moi voi `Source=HUMAN`, `TC_ID` bat dau tu `900`.
Moi case bat buoc co cot `Why_AI_Missed` (1 trong 4 ly do o TAXONOMY).

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

Sau do:
- Kiem tra JSON hop le va dem so request.
- Tao data file `postman/data/brute_force_tokens.csv`, `postman/data/state_transitions.csv`.
- Luu schema vao `postman/scripts/schemas/`.
- Viet `report/05_postman_features.md` theo `references/POSTMAN_GUIDE.md`.

**Commit:** `HW06(23127060): step5 - build 3 postman collection + environment`

---

## STEP 6 — Chay Newman & thu bang chung

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

Luu y:
- Cac case tag `@bug` **se fail** — dung y do. `run_newman.sh` chay 2 lan:
  `--folder`-filter cho `@contract` (phai 100% pass) va full run (co fail).
- Chup screenshot Postman Console (**HUMAN H4**) — phai thay dong `[HW06][23127060]`.

**Output:** `newman/*.json`, `newman/*.html`, `report/06_execution.md`
**Commit:** `HW06(23127060): step6 - chay newman va thu ket qua`

---

## STEP 7 — Bug report + GitHub Issues

1. Voi moi bug **da duoc chung minh bang request that**, viet 1 muc trong
   `bugs/BUG_REPORT.md`: ID, tieu de, muc do, SEC ref, endpoint, buoc tai hien
   (curl day du), ket qua thuc te (response that), ket qua mong doi (trich spec),
   anh huong, de xuat fix (tro toi dong code).
2. Sinh san file de human copy-paste len GitHub Issues:
   `bugs/ISSUE_TEMPLATES/<BUG_ID>.md`.
3. **HUMAN H3:** mo Issue, chup screenshot, luu vao `bugs/screenshots/<BUG_ID>.png`,
   dien link Issue nguoc lai vao `BUG_REPORT.md`.

**Commit:** `HW06(23127060): step7 - bug report N bug`

---

## STEP 8 — CI/CD (GitHub Actions)

```bash
mkdir -p ../../.github/workflows
cp ci/api-tests-23127060.yml ../../.github/workflows/api-tests-23127060.yml
```

Workflow phai: checkout, setup node, cai deps SUT, khoi dong backend nen, wait-on,
cai newman + htmlextra, chay 3 collection, upload artifact HTML.

Hai run bat buoc:
- **Run PASS:** chay collection `@contract`. Commit `ci: run all api tests (expect pass)`.
- **Run FAIL:** sua **dung 1** assertion cho sai (vd doi `expect 200` thanh `expect 201`
  trong 1 test) hoac them 1 case `@bug` vao workflow. Commit
  `ci: introduce one failing assertion to demo pipeline failure`.

**HUMAN H5:** push, doi 2 run xong, chup screenshot + copy link vao `ci/CI_CD_REPORT.md`.

**Output:** `.github/workflows/api-tests-23127060.yml`, `ci/CI_CD_REPORT.md`, `ci/evidence/*.png`

---

## STEP 9 — Agent Skill: bo sinh test tu dong (G9.5, 10 diem)

1. `agent-skill/pseudocode/generator.pseudo.md` — pseudocode day du (da co ban nhap).
2. `agent-skill/eshop-api-23127060/scripts/gen_testcases.py` — **ban hien thuc that**,
   chay duoc, la bang chung manh nhat cho muc nay.
3. `agent-skill/diagram/DIAGRAM_BRIEF.md` — mo ta khoi + luong de **HUMAN tu ve**.
   > De bai muc 11: diagram **khong duoc do AI sinh**. Agent TUYET DOI khong tao
   > file anh/mermaid cho diagram nay. Chi mo ta bang chu.
4. **HUMAN H1:** ve diagram (draw.io / Excalidraw / ve tay chup anh) ->
   `agent-skill/diagram/23127060_generator_diagram.png`.
5. **HUMAN H6 (khuyen khich):** quay video demo generator sinh test cho 1 API,
   up YouTube unlisted, dien link vao `README.md`.

**Commit:** `HW06(23127060): step9 - agent skill generator + pseudocode`

---

## STEP 10 — Bao cao chinh + AI Audit + Critique + validate

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

Viet `report/MAIN_REPORT.md` theo `references/REPORT_OUTLINE.md`, cap nhat `README.md`
(bang tu danh gia + test summary), roi:

```bash
# xuat PDF (HUMAN hoac agent neu co pandoc)
pandoc report/MAIN_REPORT.md -o report/MAIN_REPORT.pdf
pandoc ai/audit/AI_AUDIT_REPORT.md -o ai/audit/AI_AUDIT_REPORT.pdf
pandoc ai/critique/AI_CRITIQUE.md -o ai/critique/AI_CRITIQUE.pdf
```

**Nen nop:**
```bash
cd ../ && zip -r 23127060_HW06_AI_API_<3 chu so>.zip 23127060/ -x '*/node_modules/*' '*/.git/*'
```

**Commit:** `HW06(23127060): step10 - bao cao chinh, AI audit, critique`
