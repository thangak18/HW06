# AI Audit Report — HW06 API Testing (SV 23127060 — Ninh Van Khai)

> Phu luc bat buoc theo de bai muc 9.

## Tuyen bo su dung AI

**I use AI tools for the following tasks.**

Toan bo qua trinh lam HW06 (sinh test case tu API spec, audit, mo rong, dung Postman
collection, phan tich ket qua Newman, soan bao cao) deu co su tham gia cua cong cu AI.
Moi luot tuong tac deu duoc ghi lai tu dong ngay tai thoi diem xay ra bang
`agent-skill/eshop-api-23127060/scripts/ai_log.py`, khong viet lai tu tri nho.

| Cong cu AI da dung | Vai tro |
|---|---|
| Claude Code (claude-opus-5) | Sinh / bien doi tai lieu va test case, chay script, tong hop bao cao |

Cac ket qua so lieu (passed/failed) **khong** do AI uoc luong ma duoc tinh tu file
`newman/*.json` that qua `scripts/summarize_newman.py`. So do bo sinh test do sinh vien
**tu ve**, khong do AI sinh (de bai muc 11).

Sinh tu `ai/AI_log.md` luc 2026-09-01T16:04:02+07:00 · tong 14 luot tuong tac.

## Phu luc A — Bang tuong tac AI

| # | Thoi diem | Buoc | Tool | Noi dung | Prompt goc | Output | Human verified |
|---|---|---|---|---|---|---|---|
| 1 | 2026-09-01T14:29:39+07:00 | STEP 0 | Claude Code (claude-opus-5) | Trinh sat moi truong va doi chieu dac ta SUT | `ai/prompts/step0_user_prompt.txt` | `ai/interactions/20260901T142939+0700_trinh-sat-moi-truong-va-doi-chieu-dac-ta_OUTPUT.md` | pending |
| 2 | 2026-09-01T14:36:00+07:00 | STEP 1 | Claude Code (claude-opus-5) | Lap dac ta may doc duoc + va 2 loi trong bo sinh test | `ai/prompts/step1_spec.txt` | `ai/interactions/20260901T143600+0700_lap-dac-ta-may-doc-duoc-va-2-loi-trong-b_OUTPUT.md` | pending |
| 3 | 2026-09-01T14:36:46+07:00 | STEP 2a | Claude Code (claude-opus-5) | Vong 1/4 - sinh test case DOMAIN PARTITION | `ai/prompts/step2a_dom.txt` | `ai/interactions/20260901T143646+0700_vong-1-4-sinh-test-case-domain-partition_OUTPUT.md` | pending |
| 4 | 2026-09-01T14:37:10+07:00 | STEP 2b | Claude Code (claude-opus-5) | Vong 2/4 - sinh test case STATE TRANSITION | `ai/prompts/step2b_sta.txt` | `ai/interactions/20260901T143710+0700_vong-2-4-sinh-test-case-state-transition_OUTPUT.md` | pending |
| 5 | 2026-09-01T14:37:58+07:00 | STEP 2c | Claude Code (claude-opus-5) | Vong 3/4 - sinh test case SECURITY SEC-01..07 | `ai/prompts/step2c_sec.txt` | `ai/interactions/20260901T143758+0700_vong-3-4-sinh-test-case-security-sec-01-_OUTPUT.md` | pending |
| 6 | 2026-09-01T14:37:58+07:00 | STEP 2d | Claude Code (claude-opus-5) | Vong 4/4 - sinh test case SCHEMA VALIDATION | `ai/prompts/step2d_sch.txt` | `ai/interactions/20260901T143758+0700_vong-4-4-sinh-test-case-schema-validatio_OUTPUT.md` | pending |
| 7 | 2026-09-01T14:49:56+07:00 | STEP 3 | Claude Code (claude-opus-5) | Audit 225 test case bang bo luat tai lap duoc | `ai/prompts/step3_audit.txt` | `ai/interactions/20260901T144956+0700_audit-225-test-case-bang-bo-luat-tai-lap_OUTPUT.md` | pending |
| 8 | 2026-09-01T14:56:08+07:00 | STEP 4 | Claude Code (claude-opus-5) | Bo sung 18 test case AI bo sot, phan tich nguyen nhan | `ai/prompts/step4_extend.txt` | `ai/interactions/20260901T145608+0700_bo-sung-18-test-case-ai-bo-sot-phan-tich_OUTPUT.md` | pending |
| 9 | 2026-09-01T15:28:02+07:00 | STEP 5 | Claude Code (claude-opus-5) | Viet lai bo dung Postman collection, bo assertion gia | `ai/prompts/step5_postman.txt` | `ai/interactions/20260901T152802+0700_viet-lai-bo-dung-postman-collection-bo-a_OUTPUT.md` | pending |
| 10 | 2026-09-01T15:28:02+07:00 | STEP 6 | Claude Code (claude-opus-5) | Chay Newman, phan tich that bai, chot moc hoi quy | `ai/prompts/step6_newman.txt` | `ai/interactions/20260901T152802+0700_chay-newman-phan-tich-that-bai-chot-moc-_OUTPUT.md` | pending |
| 11 | 2026-09-01T15:37:40+07:00 | STEP 7 | Claude Code (claude-opus-5) | Thu bang chung va viet bug report cho 34 bug | `ai/prompts/step7_bugs.txt` | `ai/interactions/20260901T153740+0700_thu-bang-chung-va-viet-bug-report-cho-34_OUTPUT.md` | pending |
| 12 | 2026-09-01T15:43:43+07:00 | STEP 8 | Claude Code (claude-opus-5) | Workflow CI/CD + kiem chung 2 lan chay tren may cuc bo | `ai/prompts/step8_cicd.txt` | `ai/interactions/20260901T154343+0700_workflow-ci-cd-kiem-chung-2-lan-chay-tre_OUTPUT.md` | pending |
| 13 | 2026-09-01T15:50:21+07:00 | STEP 9 | Claude Code (claude-opus-5) | Thiet ke bo sinh test: pseudocode, mo ta so do, bao cao thiet ke | `ai/prompts/step9_generator.txt` | `ai/interactions/20260901T155021+0700_thiet-ke-bo-sinh-test-pseudocode-mo-ta-s_OUTPUT.md` | pending |
| 14 | 2026-09-01T16:04:02+07:00 | STEP 10 | Claude Code (claude-opus-5) | Bao cao chinh, AI Audit, AI Critique, xuat PDF, kiem tra bai nop | `ai/prompts/step10_final.txt` | `ai/interactions/20260901T160402+0700_bao-cao-chinh-ai-audit-ai-critique-xuat-_OUTPUT.md` | pending |

## Phu luc B — Chi tiet tung luot

### #1 · Trinh sat moi truong va doi chieu dac ta SUT
- Thoi diem: 2026-09-01T14:29:39+07:00 · Buoc: STEP 0 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step0_user_prompt.txt`
- Output: `ai/interactions/20260901T142939+0700_trinh-sat-moi-truong-va-doi-chieu-dac-ta_OUTPUT.md`
- Files: report/00_environment.md, agent-skill/eshop-api-23127060/references/API_SPEC_NOTES.md, agent-skill/eshop-api-23127060/scripts/ai_log.py
- Human verified: pending

### #2 · Lap dac ta may doc duoc + va 2 loi trong bo sinh test
- Thoi diem: 2026-09-01T14:36:00+07:00 · Buoc: STEP 1 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step1_spec.txt`
- Output: `ai/interactions/20260901T143600+0700_lap-dac-ta-may-doc-duoc-va-2-loi-trong-b_OUTPUT.md`
- Files: spec/api-2.json, spec/_SCHEMA.md, agent-skill/eshop-api-23127060/scripts/gen_testcases.py, report/01_api_selection.md
- Human verified: pending

### #3 · Vong 1/4 - sinh test case DOMAIN PARTITION
- Thoi diem: 2026-09-01T14:36:46+07:00 · Buoc: STEP 2a · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step2a_dom.txt`
- Output: `ai/interactions/20260901T143646+0700_vong-1-4-sinh-test-case-domain-partition_OUTPUT.md`
- Files: testcases/API-1_generated.csv, testcases/API-2_generated.csv, testcases/API-3_generated.csv
- Human verified: pending

### #4 · Vong 2/4 - sinh test case STATE TRANSITION
- Thoi diem: 2026-09-01T14:37:10+07:00 · Buoc: STEP 2b · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step2b_sta.txt`
- Output: `ai/interactions/20260901T143710+0700_vong-2-4-sinh-test-case-state-transition_OUTPUT.md`
- Files: testcases/API-1_generated.csv, testcases/API-2_generated.csv, testcases/API-3_generated.csv
- Human verified: pending

### #5 · Vong 3/4 - sinh test case SECURITY SEC-01..07
- Thoi diem: 2026-09-01T14:37:58+07:00 · Buoc: STEP 2c · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step2c_sec.txt`
- Output: `ai/interactions/20260901T143758+0700_vong-3-4-sinh-test-case-security-sec-01-_OUTPUT.md`
- Files: testcases/API-1_generated.csv, testcases/API-2_generated.csv, testcases/API-3_generated.csv
- Human verified: pending

### #6 · Vong 4/4 - sinh test case SCHEMA VALIDATION
- Thoi diem: 2026-09-01T14:37:58+07:00 · Buoc: STEP 2d · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step2d_sch.txt`
- Output: `ai/interactions/20260901T143758+0700_vong-4-4-sinh-test-case-schema-validatio_OUTPUT.md`
- Files: testcases/API-1_generated.csv, testcases/API-2_generated.csv, testcases/API-3_generated.csv
- Human verified: pending

### #7 · Audit 225 test case bang bo luat tai lap duoc
- Thoi diem: 2026-09-01T14:49:56+07:00 · Buoc: STEP 3 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step3_audit.txt`
- Output: `ai/interactions/20260901T144956+0700_audit-225-test-case-bang-bo-luat-tai-lap_OUTPUT.md`
- Files: agent-skill/eshop-api-23127060/scripts/audit_testcases.py, testcases/API-1_audited.csv, testcases/API-2_audited.csv, testcases/API-3_audited.csv, report/03_audit.md, agent-skill/eshop-api-23127060/references/TESTCASE_TAXONOMY.md
- Human verified: pending

### #8 · Bo sung 18 test case AI bo sot, phan tich nguyen nhan
- Thoi diem: 2026-09-01T14:56:08+07:00 · Buoc: STEP 4 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step4_extend.txt`
- Output: `ai/interactions/20260901T145608+0700_bo-sung-18-test-case-ai-bo-sot-phan-tich_OUTPUT.md`
- Files: agent-skill/eshop-api-23127060/scripts/extend_testcases.py, testcases/API-1_final.csv, testcases/API-2_final.csv, testcases/API-3_final.csv, report/04_extend.md
- Human verified: pending

### #9 · Viet lai bo dung Postman collection, bo assertion gia
- Thoi diem: 2026-09-01T15:28:02+07:00 · Buoc: STEP 5 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step5_postman.txt`
- Output: `ai/interactions/20260901T152802+0700_viet-lai-bo-dung-postman-collection-bo-a_OUTPUT.md`
- Files: agent-skill/eshop-api-23127060/scripts/build_collection.py, postman/collections/*.json, postman/environments/*.json, postman/scripts/schemas/*.json, postman/data/*.csv, report/05_postman_features.md
- Human verified: pending

### #10 · Chay Newman, phan tich that bai, chot moc hoi quy
- Thoi diem: 2026-09-01T15:28:02+07:00 · Buoc: STEP 6 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step6_newman.txt`
- Output: `ai/interactions/20260901T152802+0700_chay-newman-phan-tich-that-bai-chot-moc-_OUTPUT.md`
- Files: newman/*.html, newman/*.json.gz, report/06_execution.md, ci/evidence/header_evidence.md, postman/contract_baseline/*.txt, agent-skill/eshop-api-23127060/scripts/summarize_newman.py, agent-skill/eshop-api-23127060/scripts/derive_contract.py, agent-skill/eshop-api-23127060/scripts/verify_header.py, agent-skill/eshop-api-23127060/scripts/run_newman.sh, agent-skill/eshop-api-23127060/scripts/run_datadriven.sh
- Human verified: pending

### #11 · Thu bang chung va viet bug report cho 34 bug
- Thoi diem: 2026-09-01T15:37:40+07:00 · Buoc: STEP 7 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step7_bugs.txt`
- Output: `ai/interactions/20260901T153740+0700_thu-bang-chung-va-viet-bug-report-cho-34_OUTPUT.md`
- Files: agent-skill/eshop-api-23127060/scripts/capture_bug_evidence.py, agent-skill/eshop-api-23127060/scripts/make_bug_report.py, bugs/BUG_REPORT.md, bugs/evidence/*.md, bugs/ISSUE_TEMPLATES/*.md
- Human verified: pending

### #12 · Workflow CI/CD + kiem chung 2 lan chay tren may cuc bo
- Thoi diem: 2026-09-01T15:43:43+07:00 · Buoc: STEP 8 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step8_cicd.txt`
- Output: `ai/interactions/20260901T154343+0700_workflow-ci-cd-kiem-chung-2-lan-chay-tre_OUTPUT.md`
- Files: .github/workflows/api-tests-23127060.yml, ci/api-tests-23127060.yml, ci/CI_CD_REPORT.md, ci/inject_failing_test.py, ci/evidence/local_ci_run_pass.log, ci/evidence/local_ci_run_fail.log, ci/evidence/header_evidence.md
- Human verified: pending

### #13 · Thiet ke bo sinh test: pseudocode, mo ta so do, bao cao thiet ke
- Thoi diem: 2026-09-01T15:50:21+07:00 · Buoc: STEP 9 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step9_generator.txt`
- Output: `ai/interactions/20260901T155021+0700_thiet-ke-bo-sinh-test-pseudocode-mo-ta-s_OUTPUT.md`
- Files: agent-skill/pseudocode/generator.pseudo.md, agent-skill/diagram/DIAGRAM_BRIEF.md, agent-skill/VIDEO_SCRIPT.md, report/07_test_generator_design.md
- Human verified: pending

### #14 · Bao cao chinh, AI Audit, AI Critique, xuat PDF, kiem tra bai nop
- Thoi diem: 2026-09-01T16:04:02+07:00 · Buoc: STEP 10 · Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step10_final.txt`
- Output: `ai/interactions/20260901T160402+0700_bao-cao-chinh-ai-audit-ai-critique-xuat-_OUTPUT.md`
- Files: testcases/23127060_HW06_testcases.xlsx, ai/critique/AI_CRITIQUE.md, ai/audit/AI_AUDIT_REPORT.md, report/MAIN_REPORT.md, README.md, git-log/23127060_git_commit_log.txt, agent-skill/eshop-api-23127060/scripts/md_to_pdf.py, agent-skill/eshop-api-23127060/scripts/validate_submission.py
- Human verified: pending

## Ghi chu

- Toan bo prompt goc (nguyen van) va output nam trong `ai/interactions/`.
- Cot `Human verified` = `yes` nghia la sinh vien da doc lai va chiu trach nhiem ve ket qua luot do.
- So lieu passed/failed trong bao cao duoc tinh tu `newman/*.json` bang
  `scripts/summarize_newman.py`, khong do AI uoc luong.
- So do bo sinh test (`agent-skill/diagram/`) do sinh vien tu ve, khong do AI sinh.
