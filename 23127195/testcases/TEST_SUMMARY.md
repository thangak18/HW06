# Test Summary — HW06 · 23127195

> Sinh tu dong boi `scripts/export_testcases.py`. Cot *Ket qua chay* lay tu bao cao Newman moi nhat trong `newman/`.

- Nguon ket qua **API1**: `newman/api1_20260901-204738.json`
- Nguon ket qua **API2**: `newman/api2_20260901-204738.json`
- Nguon ket qua **API3**: `newman/api3_20260901-204738.json`

## Tong hop theo API

| API | FR | Test case | AI sinh | SV tu them | PASS | FAIL | Bug lien quan |
|---|---|---|---|---|---|---|---|
| API-1 | FR-04 | 45 | 35 | 10 | 25 | 20 | 5 |
| API-2 | FR-09 | 50 | 39 | 11 | 38 | 12 | 8 |
| API-3 | FR-16 | 49 | 36 | 13 | 29 | 20 | 11 |
| **Tong** | | **144** | **110** | **34** | **92** | **52** | **24** |

## Phan bo theo ky thuat kiem thu

| API | Domain partition | State transition | Security | Schema |
|---|---|---|---|---|
| API-1 | 23 | 6 | 12 | 4 |
| API-2 | 30 | 6 | 9 | 5 |
| API-3 | 31 | 6 | 7 | 5 |

## Ket qua audit (human review tren test case do AI sinh)

| API | VALID | INCOMPLETE (da hieu chinh) | INVALID (da loai/sua) |
|---|---|---|---|
| API-1 | 31 | 4 | 0 |
| API-2 | 36 | 3 | 0 |
| API-3 | 34 | 2 | 0 |
