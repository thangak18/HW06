# FR-10 Materialized Postman Features & Architecture

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)

---

## 1. Materialized Features Inventory

The following Postman features are formally materialized in the FR-10 test harness:

1. **Postman Collection Schema v2.1:** Modern collection schema structured into 11 logical folders with machine-detectable formal test ID tagging.
2. **Postman Environment (`FR10-local`):** Fully decoupled environment variables for `baseUrl`, `studentId`, credentials, dynamic authentication tokens, and order fixture IDs.
3. **Collection-Level Pre-Request Script (Centrally Injected Anti-Cheat Header):**
   - Automatically injects `X-Student-Id: {{studentId}}` (value: `23127259`) into **every single HTTP request** without error-prone manual per-request configuration.
4. **Dynamic Token Extraction & Propagation:**
   - Login setup requests dynamically extract JWT tokens from responses and store them in `adminToken`, `userAToken`, and `userBToken` for downstream requests.
5. **Dynamic Fixture Creation & ID Extraction:**
   - Pre-test setup requests dynamically extract created order IDs and store them in environment variables (`orderId`, `orderAId`, `orderBId`).
6. **Multi-Step Continuity & Recovery Workflows:**
   - Complex formal cases (`FR10-AI-041`, `FR10-HUM-001`, `FR10-HUM-002`, `FR10-HUM-003`) are structured with atomic action and verification steps tagged under the parent formal ID.
7. **Static Domain Data File (`fr10-domain-data.json`):**
   - Reusable static boundary payloads (invalid enums, malformed IDs, SQL injection vectors).
8. **Automated Assertion Scripts (`pm.test`):**
   - Rigorous, specification-backed assertions validating status codes, response bodies, and read-after-write state persistence.
9. **Newman CLI & Collection Runner Ready:**
   - Fully optimized for automated execution via `newman run` with JSON/CLI reporting.
