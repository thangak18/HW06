# AI_log — Nhat ky lam viec voi AI (HW06 API Testing, SV 23127060)

Moi luot chat = 1 entry. Prompt goc va output day du luu trong `ai/interactions/`.
File nay la nguon duy nhat de sinh `ai/audit/AI_AUDIT_REPORT.md` (`ai_log.py build-audit`).

### #1 · 2026-09-01T14:29:39+07:00 · STEP 0 · Trinh sat moi truong va doi chieu dac ta SUT
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step0_user_prompt.txt`
  > Read @2026.HW06.API Testing_En.md and @CLAUDE.md and @agent-skill/ Do the HW06 as guideline to complete all tasks
- Output: `ai/interactions/20260901T142939+0700_trinh-sat-moi-truong-va-doi-chieu-dac-ta_OUTPUT.md`
- Files touched: report/00_environment.md, agent-skill/eshop-api-23127060/references/API_SPEC_NOTES.md, agent-skill/eshop-api-23127060/scripts/ai_log.py
- Human verified: pending

### #2 · 2026-09-01T14:36:00+07:00 · STEP 1 · Lap dac ta may doc duoc + va 2 loi trong bo sinh test
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step1_spec.txt`
  > [STEP 1 — noi tiep prompt goc cua user o ai/prompts/step0_user_prompt.txt] Lap dac ta may doc duoc cho ca 3 API lam dau vao cho bo sinh test (de bai muc 7).
- Output: `ai/interactions/20260901T143600+0700_lap-dac-ta-may-doc-duoc-va-2-loi-trong-b_OUTPUT.md`
- Files touched: spec/api-2.json, spec/_SCHEMA.md, agent-skill/eshop-api-23127060/scripts/gen_testcases.py, report/01_api_selection.md
- Human verified: pending

### #3 · 2026-09-01T14:36:46+07:00 · STEP 2a · Vong 1/4 - sinh test case DOMAIN PARTITION
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step2a_dom.txt`
  > [STEP 2 — VONG 2a / 4: DOMAIN PARTITION] De bai cam mot prompt tong ("generate all the API test cases from the spec and run them").
- Output: `ai/interactions/20260901T143646+0700_vong-1-4-sinh-test-case-domain-partition_OUTPUT.md`
- Files touched: testcases/API-1_generated.csv, testcases/API-2_generated.csv, testcases/API-3_generated.csv
- Human verified: pending

### #4 · 2026-09-01T14:37:10+07:00 · STEP 2b · Vong 2/4 - sinh test case STATE TRANSITION
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step2b_sta.txt`
  > [STEP 2 — VONG 2b / 4: STATE TRANSITION] Vong 2/4. Chi sinh nhom STA, khong dung lai nhom DOM da sinh o vong truoc.
- Output: `ai/interactions/20260901T143710+0700_vong-2-4-sinh-test-case-state-transition_OUTPUT.md`
- Files touched: testcases/API-1_generated.csv, testcases/API-2_generated.csv, testcases/API-3_generated.csv
- Human verified: pending

### #5 · 2026-09-01T14:37:58+07:00 · STEP 2c · Vong 3/4 - sinh test case SECURITY SEC-01..07
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step2c_sec.txt`
  > [STEP 2 — VONG 2c / 4: SECURITY] Vong 3/4. Chi sinh nhom SEC.
- Output: `ai/interactions/20260901T143758+0700_vong-3-4-sinh-test-case-security-sec-01-_OUTPUT.md`
- Files touched: testcases/API-1_generated.csv, testcases/API-2_generated.csv, testcases/API-3_generated.csv
- Human verified: pending

### #6 · 2026-09-01T14:37:58+07:00 · STEP 2d · Vong 4/4 - sinh test case SCHEMA VALIDATION
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step2d_sch.txt`
  > [STEP 2 — VONG 2d / 4: SCHEMA VALIDATION] Vong 4/4, vong cuoi. Chi sinh nhom SCH.
- Output: `ai/interactions/20260901T143758+0700_vong-4-4-sinh-test-case-schema-validatio_OUTPUT.md`
- Files touched: testcases/API-1_generated.csv, testcases/API-2_generated.csv, testcases/API-3_generated.csv
- Human verified: pending

### #7 · 2026-09-01T14:49:56+07:00 · STEP 3 · Audit 225 test case bang bo luat tai lap duoc
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step3_audit.txt`
  > [STEP 3 — AUDIT: gan nhan VALID / INVALID / INCOMPLETE] De bai muc 6.2: "Label each AI-generated test case VALID / INVALID / INCOMPLETE with reasoning,
- Output: `ai/interactions/20260901T144956+0700_audit-225-test-case-bang-bo-luat-tai-lap_OUTPUT.md`
- Files touched: agent-skill/eshop-api-23127060/scripts/audit_testcases.py, testcases/API-1_audited.csv, testcases/API-2_audited.csv, testcases/API-3_audited.csv, report/03_audit.md, agent-skill/eshop-api-23127060/references/TESTCASE_TAXONOMY.md
- Human verified: pending

### #8 · 2026-09-01T14:56:08+07:00 · STEP 4 · Bo sung 18 test case AI bo sot, phan tich nguyen nhan
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step4_extend.txt`
  > [STEP 4 — EXTEND: bo sung test case AI bo sot] De bai muc 6.3: "Add at least five test cases of your own that the AI missed - especially around
- Output: `ai/interactions/20260901T145608+0700_bo-sung-18-test-case-ai-bo-sot-phan-tich_OUTPUT.md`
- Files touched: agent-skill/eshop-api-23127060/scripts/extend_testcases.py, testcases/API-1_final.csv, testcases/API-2_final.csv, testcases/API-3_final.csv, report/04_extend.md
- Human verified: pending

### #9 · 2026-09-01T15:28:02+07:00 · STEP 5 · Viet lai bo dung Postman collection, bo assertion gia
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step5_postman.txt`
  > [STEP 5 — Dung Postman collection tu test case] Yeu cau:
- Output: `ai/interactions/20260901T152802+0700_viet-lai-bo-dung-postman-collection-bo-a_OUTPUT.md`
- Files touched: agent-skill/eshop-api-23127060/scripts/build_collection.py, postman/collections/*.json, postman/environments/*.json, postman/scripts/schemas/*.json, postman/data/*.csv, report/05_postman_features.md
- Human verified: pending

### #10 · 2026-09-01T15:28:02+07:00 · STEP 6 · Chay Newman, phan tich that bai, chot moc hoi quy
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step6_newman.txt`
  > [STEP 6 — Chay Newman va thu bang chung] Yeu cau:
- Output: `ai/interactions/20260901T152802+0700_chay-newman-phan-tich-that-bai-chot-moc-_OUTPUT.md`
- Files touched: newman/*.html, newman/*.json.gz, report/06_execution.md, ci/evidence/header_evidence.md, postman/contract_baseline/*.txt, agent-skill/eshop-api-23127060/scripts/summarize_newman.py, agent-skill/eshop-api-23127060/scripts/derive_contract.py, agent-skill/eshop-api-23127060/scripts/verify_header.py, agent-skill/eshop-api-23127060/scripts/run_newman.sh, agent-skill/eshop-api-23127060/scripts/run_datadriven.sh
- Human verified: pending

### #11 · 2026-09-01T15:37:40+07:00 · STEP 7 · Thu bang chung va viet bug report cho 34 bug
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step7_bugs.txt`
  > [STEP 7 — Bug report + GitHub Issues] De bai muc 6.5: "Report any genuine bugs you find - including bugs the AI missed - both in the
- Output: `ai/interactions/20260901T153740+0700_thu-bang-chung-va-viet-bug-report-cho-34_OUTPUT.md`
- Files touched: agent-skill/eshop-api-23127060/scripts/capture_bug_evidence.py, agent-skill/eshop-api-23127060/scripts/make_bug_report.py, bugs/BUG_REPORT.md, bugs/evidence/*.md, bugs/ISSUE_TEMPLATES/*.md
- Human verified: pending

### #12 · 2026-09-01T15:43:43+07:00 · STEP 8 · Workflow CI/CD + kiem chung 2 lan chay tren may cuc bo
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step8_cicd.txt`
  > [STEP 8 — CI/CD] De bai muc 6: "Add your API test cases to a CI/CD pipeline for the SUT (for example, run Newman
- Output: `ai/interactions/20260901T154343+0700_workflow-ci-cd-kiem-chung-2-lan-chay-tre_OUTPUT.md`
- Files touched: .github/workflows/api-tests-23127060.yml, ci/api-tests-23127060.yml, ci/CI_CD_REPORT.md, ci/inject_failing_test.py, ci/evidence/local_ci_run_pass.log, ci/evidence/local_ci_run_fail.log, ci/evidence/header_evidence.md
- Human verified: pending

### #13 · 2026-09-01T15:50:21+07:00 · STEP 9 · Thiet ke bo sinh test: pseudocode, mo ta so do, bao cao thiet ke
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step9_generator.txt`
  > [STEP 9 — Agent Skill: bo sinh test case tu dong] De bai muc 7 (10 diem, muc Create G9.5): "design an AI-driven API test generator for the SUT:
- Output: `ai/interactions/20260901T155021+0700_thiet-ke-bo-sinh-test-pseudocode-mo-ta-s_OUTPUT.md`
- Files touched: agent-skill/pseudocode/generator.pseudo.md, agent-skill/diagram/DIAGRAM_BRIEF.md, agent-skill/VIDEO_SCRIPT.md, report/07_test_generator_design.md
- Human verified: pending

### #14 · 2026-09-01T16:04:02+07:00 · STEP 10 · Bao cao chinh, AI Audit, AI Critique, xuat PDF, kiem tra bai nop
- Tool: Claude Code (claude-opus-5)
- Prompt: `ai/prompts/step10_final.txt`
  > [STEP 10 — Bao cao chinh, AI Audit, AI Critique, kiem tra truoc khi nop] Yeu cau:
- Output: `ai/interactions/20260901T160402+0700_bao-cao-chinh-ai-audit-ai-critique-xuat-_OUTPUT.md`
- Files touched: testcases/23127060_HW06_testcases.xlsx, ai/critique/AI_CRITIQUE.md, ai/audit/AI_AUDIT_REPORT.md, report/MAIN_REPORT.md, README.md, git-log/23127060_git_commit_log.txt, agent-skill/eshop-api-23127060/scripts/md_to_pdf.py, agent-skill/eshop-api-23127060/scripts/validate_submission.py
- Human verified: pending

