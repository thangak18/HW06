# FR14 Canonical Provenance Map

- Raw AI: 42
- Rejected AI: TC-FR14-034, TC-FR14-036
- Usable AI-derived: 40
- Accepted Human: TC-FR14-H01..H06
- Rejected Human candidate: TC-FR14-H07
- Formal canonical total: 46

| ID | Provenance | Actor | Method | Endpoint | Input | Oracle Strength | Corrected Semantic Oracle |
|---|---|---|:---:|---|---|---|---|
| `TC-FR14-001` | LEVEL 2 RAW AI | Unauthenticated Client | GET | `/api/categories` |  | PARTIAL-ORACLE | Successful public category-list observation; exact seeds/order/schema are not normative. |
| `TC-FR14-002` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {"name":"Tablet"} | SPECIFICATION-BACKED | Admin create succeeds and the new unique-name category is API-visible via GET. |
| `TC-FR14-003` | LEVEL 2 RAW AI | Client Caller | GET | `/api/categories` |  | SPECIFICATION-BACKED | Admin create succeeds and the new unique-name category is API-visible via GET. |
| `TC-FR14-004` | LEVEL 2 RAW AI | Admin | PUT | `/api/categories/:id` | {"name":"Tablets & iPads"} | SPECIFICATION-BACKED | Admin update succeeds and only the target category has the new API-visible name. |
| `TC-FR14-005` | LEVEL 2 RAW AI | Client Caller | GET | `/api/categories` |  | SPECIFICATION-BACKED | Admin update succeeds and only the target category has the new API-visible name. |
| `TC-FR14-006` | LEVEL 2 RAW AI | Admin | DELETE | `/api/categories/:id` |  | SPECIFICATION-BACKED | Admin delete succeeds and the isolated target is absent from the later list. |
| `TC-FR14-007` | LEVEL 2 RAW AI | Unauthenticated Client | POST | `/api/categories` | {"name":"Unauthorized Category"} | SPECIFICATION-BACKED | Invalid or missing JWT receives any 4xx/non-success and category state is not mutated. |
| `TC-FR14-008` | LEVEL 2 RAW AI | Unauthenticated Client | PUT | `/api/categories/1` | {"name":"Hacked Name"} | SPECIFICATION-BACKED | Invalid or missing JWT receives any 4xx/non-success and category state is not mutated. |
| `TC-FR14-009` | LEVEL 2 RAW AI | Unauthenticated Client | DELETE | `/api/categories/1` |  | SPECIFICATION-BACKED | Invalid or missing JWT receives any 4xx/non-success and category state is not mutated. |
| `TC-FR14-010` | LEVEL 2 RAW AI | Malformed Token Client | POST | `/api/categories` | {"name":"Malformed Token Category"} | SPECIFICATION-BACKED | Invalid or missing JWT receives any 4xx/non-success and category state is not mutated. |
| `TC-FR14-011` | LEVEL 2 RAW AI | Attacker | DELETE | `/api/categories/1` |  | SPECIFICATION-BACKED | Invalid or missing JWT receives any 4xx/non-success and category state is not mutated. |
| `TC-FR14-012` | LEVEL 2 RAW AI | Regular Customer | POST | `/api/categories` | {"name":"User Created Category"} | SPECIFICATION-BACKED | role=user category mutation receives any 4xx/non-success and no category state mutation. |
| `TC-FR14-013` | LEVEL 2 RAW AI | Regular Customer | PUT | `/api/categories/2` | {"name":"User Modified Name"} | SPECIFICATION-BACKED | role=user category mutation receives any 4xx/non-success and no category state mutation. |
| `TC-FR14-014` | LEVEL 2 RAW AI | Regular Customer | DELETE | `/api/categories/:id` |  | SPECIFICATION-BACKED | role=user category mutation receives any 4xx/non-success and no category state mutation. |
| `TC-FR14-015` | LEVEL 2 RAW AI | Regular Customer | GET | `/api/categories` |  | SPECIFICATION-BACKED | Authenticated User can read the public category list. |
| `TC-FR14-016` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {"name":""} | SPECIFICATION-BACKED | Mandatory non-empty name violation must not create an invalid API-visible category; exact error status is unspecified. |
| `TC-FR14-017` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {"name":null} | SPECIFICATION-BACKED | Mandatory non-empty name violation must not create an invalid API-visible category; exact error status is unspecified. |
| `TC-FR14-018` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {} | SPECIFICATION-BACKED | Mandatory non-empty name violation must not create an invalid API-visible category; exact error status is unspecified. |
| `TC-FR14-019` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {"name":"   "} | SPECIFICATION-BACKED | Mandatory non-empty name violation must not create an invalid API-visible category; exact error status is unspecified. |
| `TC-FR14-020` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {"name":"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"} | EXPLORATORY | Observe unspecified name length/Unicode/duplicate/type behavior without a normative defect verdict. |
| `TC-FR14-021` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {"name":"Điện tử 📱 & Phụ kiện"} | EXPLORATORY | Observe unspecified name length/Unicode/duplicate/type behavior without a normative defect verdict. |
| `TC-FR14-022` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {"name":"Laptop"} | EXPLORATORY | Observe unspecified name length/Unicode/duplicate/type behavior without a normative defect verdict. |
| `TC-FR14-023` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {"name":12345} | EXPLORATORY | Observe unspecified name length/Unicode/duplicate/type behavior without a normative defect verdict. |
| `TC-FR14-024` | LEVEL 2 RAW AI | Admin | PUT | `/api/categories/99999` | {"name":"Ghost Category"} | PARTIAL-ORACLE | Any status is allowed, but the API must not falsely report successful modification/deletion of no existing entity. |
| `TC-FR14-025` | LEVEL 2 RAW AI | Admin | DELETE | `/api/categories/99999` |  | PARTIAL-ORACLE | Any status is allowed, but the API must not falsely report successful modification/deletion of no existing entity. |
| `TC-FR14-026` | LEVEL 2 RAW AI | Admin | PUT | `/api/categories/0` | {"name":"Zero ID"} | EXPLORATORY | Observe unspecified zero/negative/non-numeric ID handling without exact status oracle. |
| `TC-FR14-027` | LEVEL 2 RAW AI | Admin | DELETE | `/api/categories/-1` |  | EXPLORATORY | Observe unspecified zero/negative/non-numeric ID handling without exact status oracle. |
| `TC-FR14-028` | LEVEL 2 RAW AI | Admin | PUT | `/api/categories/abc` | {"name":"String ID"} | EXPLORATORY | Observe unspecified zero/negative/non-numeric ID handling without exact status oracle. |
| `TC-FR14-029` | LEVEL 2 RAW AI | Attacker | POST | `/api/categories` | {"name":"'; DROP TABLE categories;--"} | SPECIFICATION-BACKED | SQL-style input causes no query injection effect or category-table loss; black-box limitation recorded. |
| `TC-FR14-030` | LEVEL 2 RAW AI | Attacker | POST | `/api/categories` | {"name":"<script>alert('XSS')</script>"} | EXPLORATORY | Record raw JSON persistence only; SEC-04 UI escaping cannot be adjudicated by this API response. |
| `TC-FR14-031` | LEVEL 2 RAW AI | Attacker | POST | `/api/categories` | {"name":"Mass Assign Test","id":999,"admin":true,"role":"superuser"} | PARTIAL-ORACLE | Observe that undocumented body fields do not override entity identity/authorization; SEC-07 is not claimed. |
| `TC-FR14-032` | LEVEL 2 RAW AI | Attacker | PUT | `/api/categories/2` | {"name":"Updated via Mass Assign","id":999} | PARTIAL-ORACLE | Observe that undocumented body fields do not override entity identity/authorization; SEC-07 is not claimed. |
| `TC-FR14-033` | LEVEL 2 RAW AI | Attacker | POST | `/api/categories` | {"name":{"$gt":""}} | EXPLORATORY | Observe object-type robustness without a NoSQL or exact-status oracle. |
| `TC-FR14-035` | LEVEL 2 RAW AI | Admin | MULTIPLE (POST, GET, PUT, DELETE) | `/api/categories` | {"name":"Lifecycle Test"} | SPECIFICATION-BACKED | Isolated create/read/update/read/delete/read lifecycle produces the expected API-visible states. |
| `TC-FR14-037` | LEVEL 2 RAW AI | Admin | PUT | `/api/categories/:id` | {"name":"Zombie Category"} | PARTIAL-ORACLE | Any status is allowed, but the API must not falsely report successful modification/deletion of no existing entity. |
| `TC-FR14-038` | LEVEL 2 RAW AI | Admin | DELETE | `/api/categories/:id` |  | PARTIAL-ORACLE | Any status is allowed, but the API must not falsely report successful modification/deletion of no existing entity. |
| `TC-FR14-039` | LEVEL 2 RAW AI | Client Caller | GET | `/api/categories` |  | PARTIAL-ORACLE | Record observed response shape; only CRUD behavior and API-visible state are normative. |
| `TC-FR14-040` | LEVEL 2 RAW AI | Admin | POST | `/api/categories` | {"name":"Schema Test"} | PARTIAL-ORACLE | Record observed response shape; only CRUD behavior and API-visible state are normative. |
| `TC-FR14-041` | LEVEL 2 RAW AI | Admin | PUT | `/api/categories/:id` | {"name":"Schema Updated"} | PARTIAL-ORACLE | Record observed response shape; only CRUD behavior and API-visible state are normative. |
| `TC-FR14-042` | LEVEL 2 RAW AI | Admin | DELETE | `/api/categories/:id` |  | PARTIAL-ORACLE | Record observed response shape; only CRUD behavior and API-visible state are normative. |
| `TC-FR14-H01` | LEVEL 4 HUMAN EXTENSION | Admin | POST | `/api/categories` | "Raw text stream without Content-Type" | EXPLORATORY | Observe missing Content-Type behavior; HTTP 500 is robustness evidence, not a normative FR-14 bug. |
| `TC-FR14-H02` | LEVEL 4 HUMAN EXTENSION | Admin | POST | `/api/categories` | "Zero bytes" | PARTIAL-ORACLE | Zero-byte body does not establish a mandatory name; exact parser status is unspecified. |
| `TC-FR14-H03` | LEVEL 4 HUMAN EXTENSION | Admin | PATCH | `/api/categories/2` | {"name":"PATCH attempt"} | SPECIFICATION-BACKED | Undocumented PATCH receives non-success and does not change the isolated category. |
| `TC-FR14-H04` | LEVEL 4 HUMAN EXTENSION | Client Caller | GET | `/api/categories` |  | PARTIAL-ORACLE | Record JSON parseability and response MIME without treating header variation as a defect. |
| `TC-FR14-H05` | LEVEL 4 HUMAN EXTENSION | Admin | PUT | `/api/categories/2` | {} | SPECIFICATION-BACKED | Missing update name must not erase/corrupt the isolated category name. |
| `TC-FR14-H06` | LEVEL 4 HUMAN EXTENSION | Admin | POST (x3 sequential) | `/api/categories` | [{"name":"Batch 1"},{"name":"Batch 2"},{"name":"Batch 3"}] | PARTIAL-ORACLE | Three rapid unique-name creates remain distinct and API-visible; monotonic IDs are observational. |
