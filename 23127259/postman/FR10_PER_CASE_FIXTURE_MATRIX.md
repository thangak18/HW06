# FR-10 Per-Case Fixture Isolation Matrix

- **Student Name:** Nguyễn Tấn Thắng
- **Student ID:** `23127259`
- **Feature:** FR-10 – Order Status & State Machine (Pool B)
- **Total Formal Executable Test Cases:** `46` (41 AI-Derived + 5 Human Extensions)

---

## 1. Complete Formal Fixture Isolation Matrix

| Formal ID | Fixture Variable(s) | Creation Actor | Initial Creation State | Precondition Transitions | Formal Mutation | Persistence Actor | Shared Across Formal IDs? |
|---|---|---|---|---|---|---|:---:|
| **`FR10-AI-001`** | `order_FR10_AI_001` | User A | `pending` | None | `pending -> confirmed` | Admin | **NO** |
| **`FR10-AI-002`** | `order_FR10_AI_002` | User A | `pending` | Admin `confirmed` | `confirmed -> shipping` | Admin | **NO** |
| **`FR10-AI-003`** | `order_FR10_AI_003` | User A | `pending` | Admin `confirmed -> shipping` | `shipping -> delivered` | Admin | **NO** |
| **`FR10-AI-004`** | `order_FR10_AI_004` | User A | `pending` | Sequential Lifecycle | 3x `PUT /status` | Admin | **NO** |
| **`FR10-AI-005`** | `order_FR10_AI_005` | User A | `pending` | None | `pending -> canceled` (User) | User A | **NO** |
| **`FR10-AI-006`** | `order_FR10_AI_006` | User A | `pending` | Admin `confirmed` | `confirmed -> canceled` (User) | User A | **NO** |
| **`FR10-AI-007`** | `order_FR10_AI_007` | User A | `pending` | None | `pending -> canceled` (Admin) | Admin | **NO** |
| **`FR10-AI-008`** | `order_FR10_AI_008` | User A | `pending` | Admin `confirmed` | `confirmed -> canceled` (Admin) | Admin | **NO** |
| **`FR10-AI-009`** | `order_FR10_AI_009` | User A | `pending` | None | `pending -> shipping` (Rejected) | Admin | **NO** |
| **`FR10-AI-010`** | `order_FR10_AI_010` | User A | `pending` | None | `pending -> delivered` (Rejected) | Admin | **NO** |
| **`FR10-AI-011`** | `order_FR10_AI_011` | User A | `pending` | Admin `confirmed` | `confirmed -> delivered` (Rejected) | Admin | **NO** |
| **`FR10-AI-013`** | `order_FR10_AI_013` | User A | `pending` | Admin `confirmed` | `confirmed -> pending` (Rejected) | Admin | **NO** |
| **`FR10-AI-014`** | `order_FR10_AI_014` | User A | `pending` | Admin `confirmed -> shipping` | `shipping -> confirmed` (Rejected) | Admin | **NO** |
| **`FR10-AI-015`** | `order_FR10_AI_015` | User A | `pending` | Admin `confirmed -> shipping` | `shipping -> pending` (Rejected) | Admin | **NO** |
| **`FR10-AI-016`** | `order_FR10_AI_016` | User A | `pending` | Admin `confirmed -> shipping` | `shipping -> canceled` (User Rejected) | User A | **NO** |
| **`FR10-AI-017`** | `order_FR10_AI_017` | User A | `pending` | Admin `confirmed -> shipping -> delivered` | `delivered -> pending` (Rejected) | Admin | **NO** |
| **`FR10-AI-018`** | `order_FR10_AI_018` | User A | `pending` | Admin `confirmed -> shipping -> delivered` | `delivered -> confirmed` (Rejected) | Admin | **NO** |
| **`FR10-AI-019`** | `order_FR10_AI_019` | User A | `pending` | Admin `confirmed -> shipping -> delivered` | `delivered -> shipping` (Rejected) | Admin | **NO** |
| **`FR10-AI-020`** | `order_FR10_AI_020` | User A | `pending` | Admin `confirmed -> shipping -> delivered` | `delivered -> canceled` (Rejected) | Admin | **NO** |
| **`FR10-AI-021`** | `order_FR10_AI_021` | User A | `pending` | User A `canceled` | `canceled -> pending` (Rejected) | Admin | **NO** |
| **`FR10-AI-022`** | `order_FR10_AI_022` | User A | `pending` | User A `canceled` | `canceled -> confirmed` (Rejected) | Admin | **NO** |
| **`FR10-AI-023`** | `order_FR10_AI_023` | User A | `pending` | User A `canceled` | `canceled -> shipping` (Rejected) | Admin | **NO** |
| **`FR10-AI-024`** | `order_FR10_AI_024` | User A | `pending` | User A `canceled` | `canceled -> delivered` (Rejected) | Admin | **NO** |
| **`FR10-AI-025`** | `order_FR10_AI_025` | User A | `pending` | None | Missing Auth on Admin Status (Rejected) | Admin | **NO** |
| **`FR10-AI-026`** | `order_FR10_AI_026` | User A | `pending` | None | Malformed Bearer on Admin Status (Rejected) | Admin | **NO** |
| **`FR10-AI-027`** | `order_FR10_AI_027` | User A | `pending` | None | Untrusted Signature on Admin Status (Rejected) | Admin | **NO** |
| **`FR10-AI-028`** | `order_FR10_AI_028` | User A | `pending` | None | Tampered JWT on Admin Status (Rejected) | Admin | **NO** |
| **`FR10-AI-029`** | `order_FR10_AI_029` | User A | `pending` | None | Missing Auth on Customer Cancel (Rejected) | Admin | **NO** |
| **`FR10-AI-030`** | `order_FR10_AI_030` | User A | `pending` | None | Customer Token on Admin Status (Rejected) | Admin | **NO** |
| **`FR10-AI-031`** | `order_FR10_AI_031` | User A | `pending` | None | Customer Token on Admin Cancel (Rejected) | Admin | **NO** |
| **`FR10-AI-032`** | `order_FR10_AI_032` | User A | `pending` | Admin `confirmed` | Customer Token on Admin Shipping (Rejected) | Admin | **NO** |
| **`FR10-AI-033`** | `order_FR10_AI_033` | User A | `pending` | None | Customer B Cancel on User A Order (Rejected) | User A | **NO** |
| **`FR10-AI-034`** | `order_FR10_AI_034` | User A | `pending` | Admin `confirmed` | Customer B Cancel on User A Confirmed Order | User A | **NO** |
| **`FR10-AI-035`** | `order_FR10_AI_035` | User A | `pending` | None | Invalid Enum `'processing'` (Rejected) | Admin | **NO** |
| **`FR10-AI-036`** | `order_FR10_AI_036` | User A | `pending` | None | Missing `status` Key (Rejected) | Admin | **NO** |
| **`FR10-AI-037`** | `order_FR10_AI_037` | User A | `pending` | None | Explicit `null` Status (Rejected) | Admin | **NO** |
| **`FR10-AI-038`** | `order_FR10_AI_038` | User A | `pending` | None | Numeric Status Type `123` (Rejected) | Admin | **NO** |
| **`FR10-AI-039`** | Synthetic `999999` | N/A | N/A | N/A | Admin Mutation on Non-Existent ID | N/A | **NO** |
| **`FR10-AI-040`** | Synthetic `not-an-id` | N/A | N/A | N/A | Admin Mutation on Malformed Non-Numeric ID | N/A | **NO** |
| **`FR10-AI-041`** | `order_FR10_AI_041` | User A | `pending` | None | `pending -> confirmed` | Admin | **NO** |
| **`FR10-AI-042`** | Synthetic SQLi | N/A | N/A | N/A | Admin Mutation with SQLi Payload | N/A | **NO** |
| **`FR10-HUM-001`** | `order_FR10_HUM_001` | User A | `pending` | Sequential Recovery | Illegal Skip -> Verify -> Legal Confirm | Admin | **NO** |
| **`FR10-HUM-002`** | `order_FR10_HUM_002_A`, `_B` | User A | 2x `pending` | Dual Fresh Orders | Mutate A -> Verify A & B | Admin | **NO** |
| **`FR10-HUM-003`** | `order_FR10_HUM_003` | User A | `pending` | Sequential Lifecycle | Confirm -> Ship -> Cancel Rejected -> Deliver | Admin | **NO** |
| **`FR10-HUM-004`** | `order_FR10_HUM_004` | User A | `pending` | Admin `confirmed` | Same-State Probe `confirmed -> confirmed` | Admin | **NO** |
| **`FR10-HUM-005`** | `order_FR10_HUM_005` | User A | `pending` | None | Non-JSON `text/plain` Media Type Probe | Admin | **NO** |

---

## 2. Machine-Verifiable Isolation Guarantees
1. **Zero Shared Mutable Fixtures:** Every single formal test case operating on a real order creates and initializes its own dedicated order variable (`order_FR10_AI_001` .. `order_FR10_HUM_005`).
2. **Defect-Surviving Isolation:** If an invalid mutation unexpectedly succeeds due to a backend bug in test $N$, subsequent tests $N+1 \dots$ are completely unpolluted because they operate on newly created, dedicated orders.
3. **Fail-Fast Fixture Extraction:** All fixture creation requests extract the returned order ID without silent fallbacks to `'1'` or existing IDs.
