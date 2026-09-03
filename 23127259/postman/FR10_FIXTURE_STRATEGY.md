# FR-10 State Fixture Allocation & Isolation Strategy (Per-Case Isolated)

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)

---

## 1. Defect Confirmation & Strict Per-Case Isolation Architecture

Previously, sharing mutable order variables across test families posed a material defect: a failing test or valid state mutation would pollute the state for subsequent tests.

Under the hardened **Per-Case Fixture Isolation Architecture**:
1. **One Formal Case = One Dedicated Fixture:** Every formal test case operating on a real order creates its own fresh order via a co-located `[SETUP-CREATE]` request.
2. **Unique Variable Namespace:** Dedicated variables (`order_FR10_AI_001` .. `order_FR10_AI_041`, `order_FR10_HUM_001` .. `order_FR10_HUM_005`, `order_FR10_HUM_002_A`, `_B`).
3. **Fail-Fast ID Extraction:** Extraction enforces valid response schema and throws an immediate error if no ID is found, eliminating dangerous `'1'` fallbacks.
4. **Co-located State Preconditions:** Each test independently brings its dedicated order to the required starting state (`confirmed`, `shipping`, `delivered`, `canceled`) immediately before the formal action.

---

## 2. Inventory & Product Fixture Risk Assessment
- **Product ID 1:** Checkout payloads use `productId: 1` as standard seed inventory.
- **Inventory Consumption Risk:** In an SUT with strict stock tracking, repeated isolated checkouts (44 checkouts per run) could deplete stock for product 1 if initial inventory is low.
- **Mitigation:** Documented as a runtime risk. A minimal auth/checkout fixture smoke run will precede the full Newman collection run in Phase 2D.1.
