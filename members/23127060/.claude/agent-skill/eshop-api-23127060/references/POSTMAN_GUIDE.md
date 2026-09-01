# POSTMAN_GUIDE — Feature checklist + script mau (HW06, SV 23127060)

De bai: *"Exercise as many Postman features as you reasonably can... List the Postman
features you used in your report."* => phai dung **>= 8 feature** va liet ke trong bao cao.

---

## 1. Checklist feature (dien vao `report/05_postman_features.md`)

| # | Feature | Bat buoc? | Cach dung trong bai nay | Bang chung |
|---|---|---|---|---|
| 1 | **Workspace** | ✓ | Tao workspace `HW06-23127060` (Personal) | screenshot |
| 2 | **Collection** (3 cai, folder theo Category) | ✓ | `postman/collections/*.json` | file |
| 3 | **Environment** | ✓ | `local` (baseUrl=http://localhost:3000, studentId=23127060) | file |
| 4 | **Collection / Environment variables** | ✓ | `{{baseUrl}}`, `{{token_user}}`, `{{token_admin}}`, `{{orderId}}` | file |
| 5 | **Pre-request script (collection-level)** | ✓ | chen header `X-Student-Id` + `console.log` | screenshot Console |
| 6 | **Tests script** | ✓ | assert status, body, schema, response time | file |
| 7 | **JSON Schema validation** (`pm.response.to.have.jsonSchema`) | ✓ | nhom `SCH` | file |
| 8 | **Data-driven run (Collection Runner + data file)** | ✓ | `postman/data/*.csv` cho brute-force token & bang state transition | csv + screenshot Runner |
| 9 | **Newman CLI + htmlextra reporter** | ✓ | `newman/*.html` | file |
| 10 | **Mock server** | nen co | mock `GET /api/products` theo spec de doi chieu voi impl | screenshot |
| 11 | **Monitor** | nen co | monitor chay collection `@contract` 1 lan/ngay | screenshot |
| 12 | **Postman Console** | ✓ | chung minh header `X-Student-Id` (yeu cau chong gian lan) | screenshot |
| 13 | **Folder-level auth** | tuy | Bearer `{{token_user}}` o folder can auth | file |
| 14 | **`pm.sendRequest`** | tuy | lay token trong pre-request thay vi hardcode | file |
| 15 | **Visualizer** | tuy | bang tong hop ket qua | screenshot |
| 16 | **Example / saved response** | tuy | luu response mau cho tung bug | file |

> Feature 10, 11, 12, 15 can tai khoan Postman + thao tac GUI => **HUMAN lam**, agent chi
> viet huong dan vao `report/05_postman_features.md`.

---

## 2. Collection-level Pre-request Script (BAT BUOC)

```javascript
// ===== HW06 - SV 23127060 - Ninh Van Khai =====
const STUDENT_ID = pm.environment.get("studentId") || "23127060";

// 1) Header bat buoc cua de bai
pm.request.headers.upsert({ key: "X-Student-Id", value: STUDENT_ID });
pm.request.headers.upsert({ key: "Accept", value: "application/json" });

// 2) Log de chup screenshot lam bang chung chong gian lan
console.log(
  "[HW06][" + STUDENT_ID + "] " +
  pm.request.method + " " + pm.request.url.toString() +
  " | X-Student-Id=" + STUDENT_ID +
  " | at " + new Date().toISOString()
);

// 3) Tu dong lay token neu chua co (dung pm.sendRequest - feature 14)
if (!pm.environment.get("token_user")) {
  pm.sendRequest({
    url: pm.environment.get("baseUrl") + "/api/login",
    method: "POST",
    header: { "Content-Type": "application/json", "X-Student-Id": STUDENT_ID },
    body: { mode: "raw", raw: JSON.stringify({
      email: pm.environment.get("userEmail"),
      password: pm.environment.get("userPassword")
    })}
  }, function (err, res) {
    if (!err && res.code === 200) {
      pm.environment.set("token_user", res.json().token);
      pm.environment.set("userId", res.json().user.id);
    }
  });
}
```

---

## 3. Collection-level Tests Script (chay cho MOI request)

```javascript
// Kiem tra chung cho moi response
pm.test("[COMMON] Response time < 2000ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("[COMMON][SEC-02] Khong lo truong nhay cam", function () {
  const t = pm.response.text();
  pm.expect(t).to.not.include("\"password\"");
  pm.expect(t).to.not.include("\"reset_token\"");
});

pm.test("[COMMON][SCH] Content-Type la application/json", function () {
  pm.expect(pm.response.headers.get("Content-Type") || "")
    .to.include("application/json");
});
```

> Test thu 2 va thu 3 se **FAIL** o mot so request — do la bug A-07 va C-03, dung y do.
> Chung chi duoc bat trong collection `@bug`, khong bat trong `@contract`.

---

## 4. Mau Tests script cho tung Category

### DOM — domain partition
```javascript
pm.test("TC-C3-DOM-004 | price am phai bi tu choi (400)", function () {
  pm.response.to.have.status(400);
  pm.expect(pm.response.json()).to.have.property("error");
});
```

### STA — state transition
```javascript
pm.test("TC-B2-STA-011 | canceled -> delivered phai bi chan", function () {
  pm.response.to.have.status(400);
  pm.expect(pm.response.json().error).to.include("Invalid state transition");
});
```

### SEC — security
```javascript
pm.test("TC-C3-SEC-001 | SQLi khong duoc tra du lieu bang users", function () {
  const t = pm.response.text();
  pm.expect(t).to.not.match(/@(eshop|test)\./i);
  pm.expect(t).to.not.include("role");
});
pm.test("TC-C3-SEC-001 | khong tra ve HTML", function () {
  pm.expect(pm.response.text()).to.not.include("<h1>");
});
```

### SCH — schema validation
```javascript
const schema = {
  type: "object",
  required: ["id", "name", "price", "category_id"],
  properties: {
    id:          { type: "integer" },
    name:        { type: "string" },
    price:       { type: "number" },        // BUG C-05: co luc la string
    description: { type: ["string", "null"] },
    imageUrl:    { type: ["string", "null"] },
    category_id: { type: ["integer", "null"] }
  },
  additionalProperties: false
};
pm.test("TC-C3-SCH-002 | product khop schema", function () {
  pm.response.to.have.jsonSchema(schema);
});
```

---

## 5. Data-driven run (feature 8)

File `postman/data/brute_force_tokens.csv`:
```csv
resetToken
1000
1234
2222
...
```
Chay: Collection Runner -> chon folder `A1-SEC-bruteforce` -> Data file -> 20 iterations.
Hoac Newman: `newman run col.json -e env.json -d postman/data/brute_force_tokens.csv --folder "A1-SEC-bruteforce"`.

File `postman/data/state_transitions.csv`:
```csv
from_status,to_status,expected_status,note
pending,confirmed,200,hop le
pending,shipping,400,nhay coc
confirmed,shipping,200,hop le
shipping,pending,400,lui trang thai
canceled,delivered,400,BUG B-10 - impl tra 200
...
```

---

## 6. Lenh Newman chuan

```bash
npm i -g newman newman-reporter-htmlextra

newman run postman/collections/23127060_HW06_API-1.postman_collection.json \
  -e postman/environments/23127060_local.postman_environment.json \
  --reporters cli,json,htmlextra \
  --reporter-json-export newman/23127060_API-1_$(date +%Y%m%d-%H%M).json \
  --reporter-htmlextra-export newman/23127060_API-1_$(date +%Y%m%d-%H%M).html \
  --reporter-htmlextra-title "HW06 API-1 FR-03 - 23127060" \
  --reporter-htmlextra-logs
```

`--reporter-htmlextra-logs` giu lai `console.log` => chinh la bang chung header
`X-Student-Id` trong file HTML (bo tro cho screenshot Console).

---

## 7. Cau truc folder trong collection

```
23127060_HW06_API-1 (FR-03)
├── _setup            (reset DB, dang ky user test, login lay token)
├── DOM - domain partition
├── STA - state transition
├── SEC - security
│   └── A1-SEC-bruteforce   (chay bang data file)
├── SCH - schema validation
└── _teardown         (xoa du lieu test)
```
