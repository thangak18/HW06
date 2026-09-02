# TESTCASE_TAXONOMY — Cong thuc dam bao >= 35 test case / API

De bai cam "1 prompt tong". Vi vay STEP 2 phai chay **4 vong prompt rieng biet**,
moi vong 1 nhom ky thuat, moi vong ghi 1 entry AI_log rieng.

---

## Cau truc bat buoc cua 1 test case (cot trong CSV)

| Cot | Y nghia |
|---|---|
| `TC_ID` | `TC-<API>-<CAT>-<nnn>` vd `TC-A1-SEC-007` |
| `API` | `API-1` / `API-2` / `API-3` |
| `FR` | `FR-03` / `FR-08` / `FR-15` |
| `Category` | `DOM` / `STA` / `SEC` / `SCH` |
| `Technique` | EP, BVA, Decision Table, State Transition, Pairwise, Error Guessing, Fuzzing, Schema |
| `Title` | 1 cau, bat dau bang dong tu |
| `Method` | GET/POST/PUT/DELETE |
| `Endpoint` | duong dan |
| `Preconditions` | trang thai DB / token can co |
| `Request_Body` | JSON 1 dong (hoac `-`) |
| `Request_Headers` | ngoai `X-Student-Id` va `Content-Type` |
| `Expected_Status` | ma HTTP mong doi |
| `Expected_Assertions` | dieu kien tren body, ngan cach `;` |
| `Oracle` | `SPEC` hoac `IMPL` |
| `SEC_Ref` | SEC-01..07 hoac `-` |
| `Priority` | P0/P1/P2 |
| `Source` | `AI` hoac `HUMAN` |
| `Audit_Label` | `VALID` / `INVALID` / `INCOMPLETE` |
| `Audit_Note` | ly do gan nhan + da sua gi |
| `Tag` | `@contract` hoac `@bug` |
| `Bug_Ref` | ma bug lien quan (A-01, B-05, C-02...) hoac `-` |

---

## Vong 1 — DOMAIN PARTITION (`DOM`), muc tieu >= 14 case/API

Voi **moi tham so** cua API, sinh day du:

1. **Equivalence Partitioning**: 1 case hop le + moi lop khong hop le 1 case.
2. **Boundary Value Analysis**: voi tham so co bien (do dai chuoi, gia tri so) lay
   `min-1, min, min+1, max-1, max, max+1`.
3. **Missing / null / wrong type**: thieu key, `null`, sai kieu (so <-> chuoi), array/object thay vi scalar.
4. **Decision table** khi co >= 2 tham so tuong tac (vd `apply-coupon`:
   `code hop le?` x `total >= min?` x `con han?` x `chua vuot han muc?` = 16 to hop, chon 8-10 to hop dai dien).

Cong thuc nhanh: `so tham so x 4 lop toi thieu + so bien x 3`.

**Vi du API-3 `POST /api/products`:** 5 tham so x 4 = 20 case DOM ngay tu dau.

---

## Vong 2 — STATE TRANSITION (`STA`), muc tieu >= 8 case/API

Dung ky thuat **State Transition Testing (0-switch coverage day du)**.

- **API-2 (FR-10 order state machine):** bang 5x5 = 25 o. Test toan bo 25 o la ly tuong;
  toi thieu: 4 chuyen hop le + 10 chuyen khong hop le + 2 chuyen "bug co y"
  (`shipping -> canceled` qua `/cancel`, `canceled -> delivered` qua admin).
- **API-1 (FR-03 la state machine 2 buoc):** trang thai token =
  `NONE -> ISSUED -> USED`. Test: reset khi chua co token; reset 2 lan voi cung token;
  xin token 2 lan roi dung token cu; dung token cua user khac; reset roi login bang mat khau cu;
  reset khi tai khoan dang bi khoa.
- **API-3 (vong doi san pham):** `NOT_EXIST -> CREATED -> UPDATED -> DELETED -> NOT_EXIST`.
  Test: GET sau DELETE; PUT sau DELETE; DELETE 2 lan; POST trung ten; GET id vua tao.

---

## Vong 3 — SECURITY (`SEC`), muc tieu >= 9 case/API

> **DA SUA sau STEP 3.** Ban truoc cua muc nay ghi: *"Bat buoc phu du 7 ma SEC-01..SEC-07 cho
> **moi** API"*, va dung mot bang SEC **suy dien theo OWASP**. Ca hai deu sai, va chung gay hai
> that: yeu cau "du 7 ma cho moi API" la bat kha thi (SEC-07 noi ve OTP thi khong the ap vao
> API quan ly san pham), nen cach duy nhat de "dat chi tieu" la gan bua. Ket qua o STEP 3:
> **39/41 case SEC bi gan sai ma**. Xem `report/03_audit.md` muc 4.

### Bang SEC-01..SEC-07 (nguon duy nhat: `eshop-sut/README.md` muc 9)

| Ma | Yeu cau | Kiem the nao o tang API |
|---|---|---|
| SEC-01 | Mat khau **khong** duoc luu plaintext | Doc response cua `login` / `users/me`: neu thay `password` dung nguyen van mat khau da gui thi da chung minh vi pham |
| SEC-02 | API co tinh bao mat phai yeu cau JWT hop le | Goi khong `Authorization`; `Bearer ` rong; token sai chu ky; token cua user khac. Ky vong 401/403 |
| SEC-03 | API Admin phai kiem `role='admin'`, **khong chi** kiem token ton tai | Dung token cua user thuong (hop le) goi endpoint admin. Ky vong 403 |
| SEC-04 | Du lieu user nhap phai duoc escape khi hien thi | Gui `<script>`, `<img src=x onerror=>`, `javascript:` roi doc lai xem server co luu tho khong |
| SEC-05 | Truy van CSDL phai dung Parameterized Query | `%' OR '1'='1`, `' UNION SELECT ...`, `'; DROP TABLE ...--`, va mot dau nhay don don le |
| SEC-06 | API cap nhat ho so **khong duoc** cho doi truong `role` tu client | `PUT /api/users/me` kem `{"role":"admin"}` roi doc lai role |
| SEC-07 | OTP reset phai >= 6 chu so, co thoi han, vo hieu hoa sau khi dung | Do dai token; dung lai token da dung; dung token cua email khac; token cu sau khi xin token moi |

### Chi tieu do phu — dat lai cho dung

- **Toan bo suite phai phu du 7 ma SEC-01..SEC-07.** Day moi la yeu cau cua de bai.
- **Tung API chi phu nhung ma thuc su ap dung duoc**, va phan khong ap dung **phai co giai
  trinh mot dong** trong bao cao. Vi du: API-3 (quan ly san pham) khong dung toi luu tru mat
  khau lan OTP, nen khong co case SEC-01 va SEC-07 — do la dung, khong phai thieu sot.
- Nguong so luong van la **>= 9 case SEC/API**, nhung dem theo **so phep thu bao mat**, khong
  phai theo so ma SEC khac nhau.

**Quy tac chong tai pham:** truoc khi gan mot ma SEC, phai tra loi duoc cau
*"dieu nay vi pham cau nao trong `README.md` muc 9?"*. Neu khong tra loi duoc thi **de
`SEC_Ref = '-'`**, khong duoc gan ma gan dung nhat. Mot so vector tan cong that su **khong**
duoc SEC-01..07 phu (user enumeration, path traversal, mass assignment truong khac `role`,
thieu rate limiting) — chung van la test hop le, chi la khong co ma SEC de gan.

**Quy tac ve ky vong:** `Expected_Status` phai truy nguoc duoc ve mot cau trong SRS. Ky vong
`429` (rate limiting) va `409` (conflict) **khong co can cu trong SRS nay** — dung dat chung
tru khi trich duoc dong cu the.

## Vong 4 — SCHEMA VALIDATION (`SCH`), muc tieu >= 5 case/API

Dung `pm.response.to.have.jsonSchema(schema)` (Postman ho tro AJV san).

Moi API can it nhat:
1. Schema cua response thanh cong (200) — dung ten truong, dung kieu, khong thua truong.
2. Schema cua tung response loi (400 / 401 / 403 / 404 / 500) — phai la
   `{ "error": string }`.
3. `Content-Type` phai la `application/json` (bat bug **C-03** tra HTML).
4. Kieu du lieu on dinh giua cac lan goi (bat bug **C-05** `price` khi string khi number).
5. Khong lo truong nhay cam (`password`, `reset_token`) — giao voi SEC-02.

Schema JSON luu tai `postman/scripts/schemas/<API>.json`, nap vao collection variable.

---

## Bang kiem so luong (dien truoc khi qua STEP 3)

| API | DOM | STA | SEC | SCH | AI tong | HUMAN them | Tong |
|---|---|---|---|---|---|---|---|
| API-1 FR-03 | >=14 | >=8 | >=9 | >=5 | **>=36** | >=5 | >=41 |
| API-2 FR-08 | >=14 | >=8 | >=9 | >=5 | **>=36** | >=5 | >=41 |
| API-3 FR-15 | >=16 | >=6 | >=9 | >=5 | **>=36** | >=5 | >=41 |

Neu chua du: **khong duoc che them case rac**. Quay lai vong tuong ung, tang do sau
(them bien, them to hop decision table, them payload SEC) va ghi ro trong AI_log
la da phai prompt lai vong nao.

---

## Huong dan gan nhan AUDIT (STEP 3)

| Nhan | Khi nao dung |
|---|---|
| **VALID** | Buoc, du lieu, ky vong deu dung so voi spec; chay duoc ngay. |
| **INVALID** | Ky vong sai (vd doi 400 nhung spec noi 404), endpoint sai, precondition bat kha thi, hoac trung lap voi case khac. **Phai sua roi ghi cai gi da sua.** |
| **INCOMPLETE** | Y tuong dung nhung thieu: thieu assertion tren body, thieu precondition, thieu du lieu cu the, khong kiem tra tac dung phu (vd doi mat khau xong khong thu login lai). **Phai bo sung.** |

Moi nhan phai co `Audit_Note` >= 1 cau ly do. Ty le ky vong hop ly:
khoang 55-70% VALID, 10-20% INVALID, 20-30% INCOMPLETE. Neu AI ra 100% VALID
=> gan nhu chac chan la audit hoi hot, phai ra soat lai.

---

## Huong dan EXTEND (STEP 4) — >= 5 case/API AI thuong bo sot

Danh sach goi y (chon >=5, phai giai thich **tai sao AI bo sot**):

**API-1:**
- Brute force 4 chu so token bang Collection Runner + data file 20 gia tri (SEC-07).
- Dung token cua user A de doi mat khau user B (IDOR tren luong reset).
- Reset mat khau khi tai khoan dang `locked_until` -> kiem tra co mo khoa khong (A-06).
- Race condition: goi `forgot-password` 2 lan song song, token dau con dung khong.
- Kiem tra `login` sau reset khong con tra `password` trong body (A-07).

**API-2:**
- Checkout voi `total_amount` am roi kiem tra `GET /api/orders/:id` (B-01).
- Ap coupon voi `total_amount` **bang dung** `min_order_amount` (loi bien `>` — B-06).
- Bo `user_id` khoi `apply-coupon` de vuot han muc su dung (B-07).
- User B goi `PUT /api/admin/orders/<order cua A>/status` (B-03, role escalation).
- Chuoi `pending -> confirmed -> shipping -> canceled` phai bi chan (B-09).
- `canceled -> delivered` phai bi chan (B-10).

**API-3:**
- `DELETE /api/products/1` **khong token** (C-01) — AI hay gia dinh endpoint admin thi da co auth.
- `GET /api/products?search=%25' UNION SELECT ...` doc bang `users` (C-02).
- Kiem tra `Content-Type` khi SQL loi (C-03) — AI hiem khi test content-type.
- So sanh kieu `price` giua id chan va id le (C-05) — can 2 request moi lo ra.
- `PUT` thieu truong `description` -> kiem tra co bi ghi `null` khong (C-09).

**Ly do AI bo sot — chon 1 trong 4 khi viet bao cao:**
1. *Prompt quality*: prompt khong yeu cau ro "test ca truong hop endpoint thieu auth".
2. *Model limitation*: AI suy dien tu ten endpoint (`/api/admin/...`) chu khong doc code, nen gia dinh da co phan quyen.
3. *API characteristic*: bug chi lo ra khi **ket hop 2 request** (vd so kieu `price` id chan/le), AI sinh tung case doc lap.
4. *Spec gap*: spec khong mo ta hanh vi nay nen AI khong co gi de bam vao.
