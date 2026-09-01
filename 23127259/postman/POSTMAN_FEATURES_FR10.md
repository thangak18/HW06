# FR-10 Materialized Postman Features & Architecture (Hardened)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)

---

## 1. Materialized Features Inventory

The following Postman features are formally materialized in the FR-10 test harness:

1. **Postman Collection Schema v2.1:** Modern collection schema structured into 11 logical folders with 63 standalone request items.
2. **Fail-Fast Collection-Level Pre-Request Script:**
   - Automatically validates `studentId` environment variable existence and injects `X-Student-Id: {{studentId}}` (value: `23127259`) into **every single HTTP request**.
3. **Explicit Script-Level Header Injection:**
   - Every `pm.sendRequest` call explicitly attaches `X-Student-Id` and valid `Authorization: Bearer {{token}}` headers.
4. **Postman Environment (`FR10-local`):** Fully decoupled environment variables for `baseUrl`, `studentId`, credentials, dynamic authentication tokens, and order fixture IDs.
5. **Dynamic Token Extraction & Propagation:**
   - Login setup requests dynamically extract JWT tokens from responses and store them in `adminToken`, `userAToken`, and `userBToken` for downstream requests.
6. **Multi-Step Workflows & Continuity Sequences:**
   - Complex formal cases (`FR10-AI-004`, `FR10-AI-041`, `FR10-HUM-001`, `FR10-HUM-002`, `FR10-HUM-003`) are structured with atomic action and verification steps tagged under parent formal IDs.
7. **Static Domain Data File (`fr10-domain-data.json`):**
   - Reusable static boundary payloads (invalid enums, malformed IDs, SQL injection vectors).
8. **Automated Assertion Scripts (`pm.test` & `pm.sendRequest`):**
   - Rigorous, specification-backed assertions validating status codes, response bodies, and read-after-write state persistence.
9. **Newman CLI & Collection Runner Ready:**
   - Fully optimized for automated execution via `newman run` with JSON/CLI reporting.
