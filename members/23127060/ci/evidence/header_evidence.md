# Bang chung header `X-Student-Id: 23127060`

> HW06 — SV **Ninh Van Khai — 23127060** | De bai muc 11 (chong gian lan)

Sinh tu `agent-skill/eshop-api-23127060/scripts/verify_header.py`, doc thang phan
`request.header` ma Newman ghi lai cho **tung request that su roi len duong**.

| Bao cao Newman | Request da gui | Co header | Thieu header | Gia tri |
|---|---|---|---|---|
| `23127060_API-1_20260901-151823.json.gz` | 147 | 147 | 0 | `23127060` x147 |
| `23127060_API-1_contract_20260901-151940.json.gz` | 82 | 82 | 0 | `23127060` x82 |
| `23127060_API-2_20260901-151831.json.gz` | 177 | 177 | 0 | `23127060` x177 |
| `23127060_API-2_contract_20260901-151946.json.gz` | 94 | 94 | 0 | `23127060` x94 |
| `23127060_API-3_20260901-151839.json.gz` | 161 | 161 | 0 | `23127060` x161 |
| `23127060_API-3_contract_20260901-151952.json.gz` | 25 | 25 | 0 | `23127060` x25 |
| `23127060_DD-DD1_20260901-152222.json.gz` | 40 | 40 | 0 | `23127060` x40 |
| `23127060_DD-DD2_20260901-152222.json.gz` | 70 | 70 | 0 | `23127060` x70 |
| `23127060_DD-DD3_20260901-152222.json.gz` | 7 | 7 | 0 | `23127060` x7 |
| `23127060_DD-DD4_20260901-152222.json.gz` | 20 | 20 | 0 | `23127060` x20 |
| **Tong** | **823** | **823** | **0** | |

**Ket luan: 823/823 request mang header `X-Student-Id: 23127060`.**

Khong co request nao thieu header hoac mang gia tri khac.


## Header duoc chen o dau

Trong pre-request script cap **collection** (ap cho moi request, khong the quen):

```javascript
const STUDENT_ID = pm.environment.get("studentId") || "23127060";
pm.request.headers.upsert({ key: "X-Student-Id", value: STUDENT_ID });
pm.request.headers.upsert({ key: "Accept", value: "application/json" });

console.log(
  "[HW06][" + STUDENT_ID + "] " +
  pm.request.method + " " + pm.request.url.toString() +
  " | X-Student-Id=" + STUDENT_ID +
  " | " + new Date().toISOString()
);
```

Dong `console.log` tren duoc Newman giu lai trong bao cao HTML nho co
`--reporter-htmlextra-logs`, nen bao cao HTML vua la ket qua vua la bang chung.
