---
name: eshop-api-23127060
description: >
  Quy trinh API Testing HW06 tren SUT EShop cho SV 23127060 (Ninh Van Khai).
  Dung khi can: sinh test case tu API spec (>=35/API), audit VALID/INVALID/INCOMPLETE,
  extend >=5 case, build Postman collection, chay Newman, viet bug report, CI/CD,
  AI Audit Report va AI Critique. Bat buoc ghi AI_log moi luot.
---

# SKILL — EShop API Testing (HW06, SV 23127060)

## 0. Danh tinh & pham vi

- Sinh vien: **Ninh Van Khai — MSSV 23127060**.
- Thu muc lam viec duy nhat: `members/23127060/`.
- **CACH LY NHOM (luat cung):** TUYET DOI khong doc/ghi/tham chieu
  `members/23127195/`, `members/23127259/`, hay bat ky thu muc member khac.
  Neu user lo nhac toi, tu choi va nhac lai luat nay.
- Duoc phep doc (chi doc): `../../docs/`, `../../scripts/`, `../../README.md`,
  va source cua SUT tai `eshop-sut/` (khong duoc sua SUT).
- Duoc phep ghi: `.github/workflows/api-tests-23127060.yml` o repo root
  (GitHub Actions bat buoc nam o root, khong the nam trong member folder).

## 1. Ba API duoc chon (KHOA — khong tu doi)

HW06 yeu cau **dung 3 API**, moi Pool 1 cai. **Pool D (mobile) KHONG dung trong HW06**
(de bai: "Pool D, the mobile app, is not used here, because this homework targets the backend API").

| ID | Pool | FR | API chinh | Endpoint phu (ho tro state/security) |
|----|------|----|-----------|--------------------------------------|
| **API-1** | A | FR-03 Quen & Dat lai mat khau | `POST /api/forgot-password` + `POST /api/reset-password` | `POST /api/login`, `POST /api/register` |
| **API-2** | B | FR-08 Thanh toan | `POST /api/checkout` | `POST /api/apply-coupon`, `POST /api/coupon-usage`, `GET /api/orders/:id`, `GET /api/orders/my-orders`, `PUT /api/orders/:id/cancel`, `PUT /api/admin/orders/:id/status` (FR-10 state machine) |
| **API-3** | C | FR-15 Quan ly san pham (CRUD) | `POST/PUT/DELETE /api/products` | `GET /api/products`, `GET /api/products/:id`, `GET /api/products?search=` |

> Neu user muon van lam Pool D: chi lam nhu **phu luc khong tinh diem**, khong duoc
> thay the 1 trong 3 API tren. Phai canh bao user truoc.

Rang buoc: bo 3 API nay khong duoc trung voi 2 thanh vien con lai. Kiem tra
`docs/team-api-allocation.md` (chi doc) truoc khi bat dau — neu trung, dung lai va bao user.

## 2. Muc tieu so luong (bat buoc de khong mat diem)

| Hang muc | Toi thieu | Ghi chu |
|---|---|---|
| Test case AI sinh / API | **35** | tong >= 105 |
| Test case tu them (human extend) / API | **5** | tong >= 15, uu tien security + state transition |
| Do phu 4 nhom | 100% | domain partition, state transition, security SEC-01..07, schema validation |
| Bug that / API | >= 3 | phai mo GitHub Issue + screenshot |
| Postman feature dung | >= 8 | xem `references/POSTMAN_GUIDE.md` |
| CI/CD run | 2 | 1 run all-pass, 1 run co dung 1 test fail |
| AI Critique | 200-300 tu | dem tu, khong duoc lech |

## 3. LUAT AI_LOG — BAT BUOC MOI LUOT

Moi luot tra loi (ke ca luot chi doc file), **truoc khi ket thuc** phai:

```bash
S=agent-skill/eshop-api-23127060/scripts
# 1) luu prompt goc cua user vao file
cat > /tmp/last_prompt.txt <<'EOF'
<dan nguyen van prompt cua user o day>
EOF
# 2) ghi entry
python3 $S/ai_log.py add --root . --sid 23127060 \
  --tool "Claude Code (claude-sonnet-4.5)" \
  --step "<STEP n>" --title "<mo ta ngan>" \
  --prompt-file /tmp/last_prompt.txt \
  --output "<tom tat 2-4 dong ket qua>" \
  --files "<danh sach file tao/sua, ngan cach dau phay>" \
  --human-verified pending
```

Roi in dung 1 dong: `AI_log: da ghi entry #<n>`

- Khong co dong do => luot lam viec **chua hoan thanh**, phai lam lai.
- File sinh ra: `ai/AI_log.md` + ban day du trong `ai/prompts/` va `ai/interactions/`.
- Cuoi ky: `python3 $S/ai_log.py build-audit --root . --sid 23127060`
  -> sinh `ai/audit/AI_AUDIT_REPORT.md` dung format de bai (Tool / Date-time / Prompt / Output).
- Khong duoc viet tay `AI_log.md`. Chi ghi qua `ai_log.py`.

## 4. LUAT CHONG BIA

1. **Khong bao cao test case da chay neu chua co Newman report that.** Moi con so
   passed/failed phai lay tu `newman/*.json` qua `python3 $S/summarize_newman.py`.
2. **Khong bia bug.** Moi bug phai co: request that (curl/Postman), response that,
   va tro duoc ve dong code trong `eshop-sut/backend/server.js`.
3. **Khong ve diagram bang AI.** De bai cam ro (muc 11). Agent chi duoc viet
   `agent-skill/diagram/DIAGRAM_BRIEF.md` mo ta y tuong; **human tu ve**.
4. **Header `X-Student-Id: 23127060` bat buoc tren MOI request**, dat o
   collection-level pre-request script, kem `console.log` de human chup screenshot.
5. Newman phai chay voi host `localhost`/`127.0.0.1` (de bai chap nhan).

## 5. Phan chia MCP-doable vs HUMAN-only

### Agent lam duoc het (khong hoi)
- Doc `eshop-sut/backend/api_specification.md`, doi chieu voi `server.js`.
- Sinh spec may doc duoc `spec/api-1..3.json`.
- Chay `gen_testcases.py` -> CSV test case.
- Audit tu dong vong 1 (gan nhan de xuat + ly do), chay `build_collection.py`.
- Chay `newman`, parse report, sinh bang tong hop.
- Viet toan bo `report/`, `bugs/BUG_REPORT.md`, `ai/critique/AI_CRITIQUE.md` (draft).
- Viet `.github/workflows/api-tests-23127060.yml`, `ci/CI_CD_REPORT.md`.
- Xuat Excel test case (`tc_to_excel.py`), chay `validate_submission.py`.

### HUMAN bat buoc lam (agent chi chuan bi san)
| # | Viec | Agent chuan bi san |
|---|------|--------------------|
| H1 | Ve **diagram** AI test generator (tay/draw.io/Excalidraw) | `agent-skill/diagram/DIAGRAM_BRIEF.md` + pseudocode |
| H2 | Chot nhan audit VALID/INVALID/INCOMPLETE | cot `Audit_Label` da dien de xuat, human sua |
| H3 | Mo **GitHub Issues** cho tung bug + chup screenshot | `bugs/BUG_REPORT.md` + `bugs/ISSUE_TEMPLATES/*.md` san sang copy |
| H4 | Chup screenshot Postman Console co header `X-Student-Id` | script da `console.log`, kem huong dan chup |
| H5 | Push repo, chay 2 CI run, chup screenshot + lay link | workflow file + `ci/CI_CD_REPORT.md` cho san cho dien link |
| H6 | Quay video demo generator (khuyen khich, YouTube) | `agent-skill/VIDEO_SCRIPT.md` |
| H7 | Doc lai & sua AI_CRITIQUE cho dung giong minh | draft 200-300 tu |
| H8 | Danh dau `human-verified yes` trong AI_log | `ai_log.py verify --id N --status yes` |
| H9 | Xuat PDF, dat ten zip, nop Moodle | `validate_submission.py` bao con thieu gi |

### Khi nao agent PHAI hoi user (CRITICAL)
Chi hoi khi roi vao 1 trong 6 truong hop:
- **C1** So lieu Newman bat thuong khong giai thich duoc bang bug da biet.
- **C2** Can cai phan mem moi / doi port / dung toi network ngoai.
- **C3** API spec mau thuan voi `server.js` va khong ro theo ben nao lam oracle.
- **C4** Phat hien bug moi chua co trong `references/API_SPEC_NOTES.md`.
- **C5** Bo 3 API bi trung voi thanh vien khac.
- **C6** Chon giua 2 huong viet bao cao anh huong diem ro ret.

Format khi hoi:
```
CAN NGUOI QUYET - [C<x>]
Boi canh: ...
Lua chon: (a) ... (b) ... (c) ...
He qua tung lua chon: ...
De xuat mac dinh neu khong tra loi: ...
```
Cac quyet dinh vun vat khac (dat ten file, thu tu folder Postman, wording bao cao,
retry request loi vat) => **agent tu quyet, khong hoi**.

## 6. Oracle — lay dau lam chuan

SUT co RAT NHIEU bug co y. Vi vay moi test case phai ghi ro cot `Oracle`:

- `SPEC` — ky vong theo `api_specification.md` (dung de **phat hien bug**).
- `IMPL` — hanh vi thuc te cua code (dung de test hoi quy, khong dung de cham diem dung/sai).

**Mac dinh dung `SPEC`.** Test fail vi SUT sai => day KHONG phai loi test case,
ma la **bug can bao cao**. Trong Newman, cac case nay se FAIL — dieu do la **dung y do**.
De CI run "all pass" (yeu cau muc 6 de bai), tach collection thanh 2 tag:

- `@contract` — case ma SUT hien dang dap ung (dung cho CI run all-pass).
- `@bug` — case phoi bay bug (chay rieng, ghi ro trong bao cao la "expected failure").

## 7. Luong 10 buoc

Chi tiet lenh tung buoc: doc `references/WORKFLOW.md`.

| STEP | Ten | Output chinh |
|---|---|---|
| 0 | Trinh sat moi truong + doc spec | `report/00_environment.md` |
| 1 | Lap spec may doc duoc | `spec/api-1.json`, `api-2.json`, `api-3.json` |
| 2 | Sinh test case (AI, tung buoc, KHONG 1 prompt tong) | `testcases/API-*_generated.csv` |
| 3 | Audit VALID/INVALID/INCOMPLETE | `testcases/API-*_audited.csv` + `report/03_audit.md` |
| 4 | Extend >=5 case/API | `testcases/API-*_final.csv` + `report/04_extend.md` |
| 5 | Build Postman collection + environment + data file | `postman/collections/*.json` |
| 6 | Chay Newman, thu bang chung | `newman/*.html`, `*.json`, `report/06_execution.md` |
| 7 | Bug report + GitHub Issues | `bugs/BUG_REPORT.md` |
| 8 | CI/CD 2 run | `.github/workflows/...`, `ci/CI_CD_REPORT.md` |
| 9 | Agent Skill generator (diagram + pseudocode) | `agent-skill/` |
| 10 | Bao cao chinh + AI Audit + Critique + validate | `report/MAIN_REPORT.md`, `README.md` |

## 8. Quy uoc dat ten

- Test case ID: `TC-<API_ID>-<CAT>-<3 so>` — vd `TC-A1-SEC-007`.
  `CAT` in {`DOM` domain partition, `STA` state transition, `SEC` security, `SCH` schema}.
- Nguon: cot `Source` = `AI` | `HUMAN`.
- File Postman: `23127060_HW06_<API_ID>.postman_collection.json`.
- Newman: `23127060_<API_ID>_<yyyymmdd-HHMM>.html` / `.json`.
- Commit: `HW06(23127060/<API_ID>): <step> - <mo ta>` — vd
  `HW06(23127060/API-2): step4 extend - them 6 case state transition`.

## 9. Tai lieu tham chieu

Doc TRUOC khi lam viec tuong ung:

| File | Khi nao doc |
|---|---|
| `references/API_SPEC_NOTES.md` | truoc STEP 1-2 — endpoint, param, bug da biet, mapping SEC-01..07 |
| `references/TESTCASE_TAXONOMY.md` | truoc STEP 2-4 — cong thuc dam bao >=35 case/API |
| `references/POSTMAN_GUIDE.md` | truoc STEP 5-6 — feature checklist, script mau |
| `references/WORKFLOW.md` | moi STEP — lenh cu the |
| `references/REPORT_OUTLINE.md` | STEP 10 — khung bao cao |

## 10. Scripts

```
S=agent-skill/eshop-api-23127060/scripts
$S/ai_log.py             add | verify | build-audit | stats
$S/gen_testcases.py      spec JSON -> testcases CSV (bo sinh test, chinh la Agent Skill G9.5)
$S/build_collection.py   testcases CSV -> Postman collection v2.1 + environment
$S/run_newman.sh         chay newman + htmlextra, luu json/html vao newman/
$S/summarize_newman.py   newman JSON -> bang tong hop markdown
$S/tc_to_excel.py        CSV -> testcases/23127060_HW06_testcases.xlsx (co sheet Summary)
$S/seed_sut.js           reset/seed DB SUT ve trang thai biet truoc
$S/validate_submission.py kiem tra du deliverable truoc khi nen zip
```

## 11. Ket thuc moi STEP

1. Chay lenh cua STEP.
2. Ghi file output.
3. `git add -A && git commit -m "HW06(23127060/...): ..."`.
4. Ghi AI_log (muc 3).
5. In tom tat 3 dong: da lam gi / file nao / STEP ke tiep.
