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

