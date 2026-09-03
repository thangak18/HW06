# Interaction Log: INT-064

- **Interaction ID:** INT-064
- **Tool:** Antigravity IDE Assistant
- **Model:** Gemini 3.7 Flash
- **Date & Time:** 2026-09-02 13:56:00+07:00
- **Timezone:** UTC+07:00
- **Project Stage:** Phase 3D – FR-14 Runtime Newman Execution, Defect Confirmation & Bug Reporting
- **Feature:** FR-14 – Category Management CRUD (Pool C – Web Admin)

---

## 1. Submitted Prompt

```text
Execute FR14_Category_CRUD.postman_collection.json against SUT via Newman CLI and HTML reporter.
1. Ensure SUT database is cleanly re-seeded.
2. Execute full collection with CLI, JSON, and HTML extra reporters.
3. Analyze execution results: reconcile passing assertions and intentional defect-confirming assertions.
4. Document all confirmed defects in 23127259/bugs/BUG-FR14-XXX.md.
5. Create comprehensive BUG_REGISTRY_FR14.md.
```

---

## 2. Assistant Response & Action Summary

1. **SUT Re-seeding:** Restarted `node server.js` in `/Volumes/Thang/eshop-sut/backend`. Verified database initialized with 3 clean seeded categories.
2. **Newman Run 01:**
   - Command: `newman run postman/collections/FR14_Category_CRUD.postman_collection.json --reporters cli,json,htmlextra ...`
   - Output files: `evidence/fr14/newman/FR14-run01-cli.txt`, `FR14-run01.json`, `FR14-run01.html`, `FR14-run01-exitcode.txt`.
   - Results: 59 requests executed, 96 assertions evaluated (81 passed, 15 failed).
   - Execution Duration: 6.8s, average response time: 2ms.
3. **Defect Confirmation Analysis:**
   - 100% of 15 failing assertions correspond to verified SUT defects.
   - **BUG-FR14-001 (HIGH):** Missing RBAC on `POST/PUT/DELETE /api/categories` — regular users can manage categories.
   - **BUG-FR14-002 (MEDIUM):** Missing input validation — empty, null, whitespace names accepted.
   - **BUG-FR14-003 (MEDIUM):** Missing existence checks — `PUT/DELETE` return 200 on non-existent IDs.
   - **BUG-FR14-004 (HIGH):** Uncaught server exception (HTTP 500) when `Content-Type` header is omitted.
4. **Bug Reports Created:** Written `BUG-FR14-001.md`, `BUG-FR14-002.md`, `BUG-FR14-003.md`, `BUG-FR14-004.md`, and `BUG_REGISTRY_FR14.md`.
