# Postman & Newman Test Automation Strategy

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Course:** HW06 – API Testing
- **Target Collection:** `HW06-23127259`

---

## 1. Global Attribution Mechanism (`X-Student-Id`)

To guarantee strict academic attribution and individual authorship across every API request executed in Postman and Newman, a **Collection-level Pre-request Script** is configured at the root of the collection:

```javascript
// Collection-level Pre-request Script (Applies globally to all requests)
pm.request.headers.upsert({
    key: "X-Student-Id",
    value: pm.environment.get("studentId") || "23127259"
});
```

### Execution Evidence Protocol
- **No Fabricated Screenshots:** In accordance with academic integrity rules, actual Postman Console screenshots showing `X-Student-Id: 23127259` in the outgoing HTTP request headers will be captured during real execution in Phase 1, Phase 2, and Phase 3.
- The captured screenshots will be stored in `23127259/evidence/` and embedded in the final Main Report.

---

## 2. Postman Variable Scope & Management Strategy

Variables are categorized and managed across three distinct scopes to prevent state contamination:

| Scope | Variables | Purpose & Safety Rules |
|---|---|---|
| **Environment Variables** | `baseUrl`, `studentId`, `lockoutEmail` | Shared configuration across runs. `HW06-env-template.json` is committed with empty token placeholders. Real tokens are kept in local non-committed environment or populated dynamically. |
| **Collection Variables** | `userToken`, `adminToken`, `dynamicCatId`, `orderId_fwd`, `orderId_cancel` | Dynamically captured at runtime via `pm.collectionVariables.set()` during setup requests and referenced across subsequent chained test steps. |
| **Data Variables (Data-Driven)** | `email`, `password`, `expectedStatus`, `scenarioDesc` | Injected via JSON data files (e.g. `23127259/postman/data/lockout-scenarios.json`) during Newman parameterized executions. |

---

## 3. Postman Feature Coverage Matrix

The automated test suite exercises the following advanced Postman capabilities:

1. **Pre-request Scripts:** Dynamic timestamp generation, header upserts, and payload preparation.
2. **Post-response Assertion Scripts (`pm.test`):**
   - Status code assertions (`pm.response.to.have.status`)
   - Response time thresholds (`pm.expect(pm.response.responseTime).to.be.below(2000)`)
   - JSON Schema validation (`tv4` / `ajv`)
   - Header validation (`Content-Type`, security headers)
   - Deep object property assertions and sensitive field exclusion checks
3. **Dynamic State Chaining:** Capturing created entity IDs from response bodies and reusing them in subsequent PUT/DELETE requests.
4. **Data-Driven Testing (DDT):** Executing parameterized test matrices using external JSON data files with Newman `-d` flag.
