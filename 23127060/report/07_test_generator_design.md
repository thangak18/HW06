# STEP 9 — Thiet ke bo sinh test case bang AI (Agent Skill)

> HW06 — API Testing | SV **Ninh Van Khai — 23127060** | De bai muc 7 (10 diem, muc Create G9.5)

De bai: *"design an AI-driven API test generator for the SUT: given the API specification, it
produces test cases automatically. Provide a self-drawn diagram and pseudocode of the design."*

---

## 1. Y tuong: tach lam hai lop

Cach lam hien nhien la bao AI *"doc dac ta nay va viet 35 test case"*. Cach do co ba van de:

- **Khong lap lai duoc.** Chay lai cung mot prompt cho ra bo test khac.
- **Khong do duoc do phu.** Khong tra loi duoc cau "tham so `price` da co bao nhieu phan hoach?"
- **Khong mo rong duoc.** Them mot API la lam lai tu dau.

Thiet ke o day tach quy trinh lam hai lop co ranh gioi ro:

| Lop | Ai lam | San pham | Tinh chat |
|---|---|---|---|
| **Lop tri thuc** | Con nguoi + AI cung lam | `spec/api-N.json` | Doi hoi doc hieu; day la noi quyet dinh chat luong |
| **Lop sinh** | May lam mot minh | `testcases/API-N_generated.csv` | **Tat dinh**: cung dau vao luon cho cung dau ra |

Ranh gioi nay la quyet dinh thiet ke quan trong nhat. AI khong duoc phep "sang tac" test case;
no chi duoc giup **dich dac ta van xuoi sang mot cau truc co truc phan hoach ro rang**. Tu do
tro di la mot chuong trinh tat dinh.

Loi ich cu the: khi mot test case sai, truy nguoc duoc ngay ve **dong nao trong file spec** gay
ra no. Voi bo sinh dang hop den thi khong truy duoc.

## 2. Vi sao dac ta van xuoi khong dua thang cho may duoc

Cau nay trong SRS FR-15:

> *"Gia: bat buoc, phai la so **duong** (> 0)."*

chua **ba** thong tin an ma con nguoi doc ra ngay con chuong trinh thi khong:

1. Co mot tham so ten `price`.
2. Kieu cua no la so.
3. Co mot **bien tai 0**, va bien do thuoc phia khong hop le.

Khoi "dich sang dang may doc duoc" chinh la noi bien doi nay xay ra. Sau khi dich, cung thong
tin do tro thanh:

```json
{ "name": "price", "in": "body", "type": "number", "required": true,
  "partitions": [
    { "id": "valid",    "value": 150000, "valid": true,  "expected_status": 201 },
    { "id": "zero",     "value": 0,      "valid": false, "boundary": true, "expected_status": 400 },
    { "id": "negative", "value": -100,   "valid": false, "expected_status": 400, "bug": "C-06" },
    { "id": "string",   "value": "abc",  "valid": false, "expected_status": 400, "bug": "C-06" }
  ]
}
```

Bay gio thi mot vong lap sinh duoc test case, va cau hoi *"tham so `price` da co bao nhieu
phan hoach?"* tra loi duoc bang mot lenh dem.

## 3. Kien truc

```
PARSE -> NORMALISE -> 4 BO SINH SONG SONG -> KHU_TRUNG -> DANH_SO -> KIEM_TRA_DO_PHU -> EMIT
                                                                            |
                                              (chua du do phu) -------------+
                                                          quay lai bo sung vao spec
```

Bon truc trong file spec anh xa **mot doi mot** sang bon nhom ky thuat ma de bai muc 6.1 doi:

| Truc trong spec | Bo sinh | Ky thuat | So case sinh ra |
|---|---|---|---|
| `endpoints[].params[].partitions[]` | `gen_domain` | Equivalence Partitioning, BVA, Decision Table | 128 |
| `state_machine.transitions[]` | `gen_state` | State Transition Testing (0-switch) | 38 |
| `security[]` | `gen_security` | Anh xa SEC-01..SEC-07 | 41 |
| `schema_cases[]` | `gen_schema` | JSON Schema Validation | 18 |
| | | **Tong** | **225** |

Bon bo sinh **doc lap** nhau, nen chay duoc rieng tung cai:

```bash
python3 gen_testcases.py --spec spec/api-2.json --only DOM --out out.csv
python3 gen_testcases.py --spec spec/api-2.json --only STA --out out.csv --append
```

Day khong phai tien ich phu ma la **co so ky thuat** de thoa yeu cau *"drive it step by step,
not with a single generic prompt"* cua de bai: STEP 2 chay dung bon vong doc lap, moi vong mot
ky thuat kiem thu, moi vong mot entry AI_log rieng.

**So do:** `agent-skill/diagram/23127060_generator_diagram.png` — **do sinh vien tu ve**, theo
de bai muc 11. Mo ta khoi va luong: `agent-skill/diagram/DIAGRAM_BRIEF.md`.
**Pseudocode day du:** `agent-skill/pseudocode/generator.pseudo.md`.
**Ban hien thuc chay duoc:** `agent-skill/eshop-api-23127060/scripts/gen_testcases.py` (chi dung
thu vien chuan cua Python).

## 4. `KIEM_TRA_DO_PHU` — cong tac chan

Bo sinh khong chi in ra test case, no con **tu cham do phu cua chinh minh**:

```
$ python3 gen_testcases.py --spec spec/api-2.json --stats
So case theo nhom: DOM=41, STA=20, SEC=14, SCH=6
Tong: 81
Tham so CHUA phu DOM: (khong)
Ma SEC CHUA phu: (du 7)
O bang chuyen trang thai da test: 20 / 25
```

Bon phep do:

1. **Moi tham so** cua moi endpoint phai co it nhat mot case.
2. **Bay ma SEC-01..07** phai duoc phu (tren toan bo suite — xem muc 5.2).
3. **Bang chuyen trang thai**: bao nhieu o trong `states x states` da co case.
4. **Nguong 35 case/API** cua de bai.

Dong `20 / 25` la vi du cho thay phep do nay co ich: no chi thang ra 5 o con thieu, va do dung
la nam o **duong cheo** (`pending -> pending`, ...). Nhung o do bi bo qua vi truc quan chung
"khong phai mot buoc chuyen" — nhung trong thuc te chung hay gay loi nhat (mot request bi gui
lai hai lan do mang cham hoac nguoi dung bam hai lan). Chung da duoc bo sung o STEP 4.

## 5. Hai loi that trong bo sinh, va cach tim ra

Phan nay quan trong hon phan mo ta kien truc: **cong cu tu dong cung phai duoc kiem thu.**

### 5.1 Khoa khu trung nuot mat 34 test case

Chay lan dau, API-1 khai bao 6 truong hop schema nhung chi sinh ra **1**, va khai bao 9 chuyen
trang thai nhung chi sinh ra **5**. Con so khong khop voi khai bao — do la dau hieu duy nhat.

Truy nguyen ve ham `dedup()`:

```python
key = (r["Method"], r["Endpoint"], r["Request_Body"], str(r["Expected_Status"]))
```

Khoa nay coi hai test case la trung nhau khi chung **gui cung mot request**, bat ke chung
**khang dinh dieu gi**. Hai hau qua:

- Mot case `SCH` (*"response 200 khop schema `{message: string}`"*) va mot case `DOM`
  (*"email hop le tra 200"*) gui y het nhau nhung kiem hai thu khac han. Case `SCH` bi nuot.
- Hai case `STA` *"huy don dang `pending`"* va *"huy don dang `confirmed`"* cung goi
  `PUT /api/orders/:id/cancel` voi body rong; chung chi khac nhau o **trang thai ban dau**.
  Case thu hai bi nuot.

Khoa sau khi sua:

```python
key = (r["Category"], r["Method"], r["Endpoint"], r["Request_Body"],
       str(r["Expected_Status"]), r["Expected_Assertions"], r["Preconditions"])
```

Ket qua: **191 -> 225 case**, do phu state machine cua API-2 **11/25 -> 20/25**.

Neu tin ngay con so dau tien thi bao cao da ghi thieu 34 test case va mot do phu sai.

### 5.2 Bang SEC-01..07 duoc dien tu tri nho

Bang `SEC_DEFAULT_ASSERT` trong bo sinh duoc viet theo **tri nho ve cac lo hong OWASP quen
thuoc**: SEC-01 = SQL Injection, SEC-04 = IDOR, SEC-05 = leo thang quyen, SEC-07 = brute force.

Bang **that** nam trong `eshop-sut/README.md` muc 9 va noi nhung dieu hoan toan khac: SEC-01 la
*"mat khau khong duoc luu plaintext"*, SEC-05 la *"truy van CSDL phai dung Parameterized
Query"*. **39/41 test case bao mat bi gan sai ma.**

Dieu dang noi: cac test case **van chay dung** — mot phep thu SQL Injection van la mot phep thu
SQL Injection du no bi dan nhan SEC-01 hay SEC-05. Cai hong la **bang do phu bao mat trong bao
cao**: no se ghi *"API-3 da phu SEC-01 voi 8 test case"* trong khi SEC-01 khong he duoc kiem o
API-3 dong nao.

Nguyen nhan sau xa: **`SEC-01` la mot nhan khong tu giai thich.** Doc "SEC-01" khong ai doan
duoc no noi gi, nen rat de dien vao bang mo hinh manh nhat co san. Chi mot lenh
`grep -n "SEC-0" README.md` la ra su that.

Bai hoc cho thiet ke: **moi nhan ma bo sinh gan len test case ma khong tu giai thich duoc thi
phai co mot buoc doi chieu voi tai lieu goc**, khong duoc coi la kien thuc nen.

### 5.3 Mot chi tieu do luong dat sai gay ra chinh cai loi no dinh ngan chan

`references/TESTCASE_TAXONOMY.md` do chinh toi viet co dong: *"Bat buoc phu du 7 ma
SEC-01..SEC-07 cho **moi** API"*. Sau khi biet bang SEC that, yeu cau do la **bat kha thi**:
SEC-07 noi ve vong doi OTP thi khong the ap vao API quan ly san pham; SEC-01 noi ve luu tru
mat khau thi khong lien quan gi den luong thanh toan.

Va chinh yeu cau do gay hai: cach duy nhat de "dat chi tieu" la **gan bua** mot ma SEC cho mot
case khong thuoc no. Chi tieu dung phai la: *du 7 ma tren toan bo suite; tung API phu nhung ma
thuc su ap dung duoc, phan khong ap dung co giai trinh mot dong.* Da sua lai taxonomy.

## 6. Han che va huong mo rong

### 6.1 Han che lon nhat: bo sinh sinh ra test case DOC LAP

Ca bon bo sinh deu theo cung mot khuon: mot vong lap tren mot danh sach khai bao, moi phan tu
cho ra **mot** test case, moi test case **mot** request. Do la gioi han **cau truc**, khong phai
gioi han ve prompt hay ve mo hinh.

So lieu do duoc: trong 18 test case ma con nguoi phai tu bo sung o STEP 4, **9 case (mot nua)**
thuoc nhom `API` — tuc la *"bug chi lo ra khi ket hop nhieu request"*:

| Bug | Vi sao can nhieu request |
|---|---|
| C-05 | `{"price": 30000000}` va `{"price": "28000000"}` deu la JSON hop le. Vi pham chi hien ra khi **so sanh hai response** |
| B-09 | Dua don ve trang thai `shipping` doi hoi di qua dung hai buoc admin — mot chuoi 4 request |
| C-09 | Phai `POST` roi `PUT` thieu truong roi `GET` moi thay 4 truong bi xoa trang |
| C-13 | Sap may chu chi xay ra o request **thu ba** cua chuoi, va no la he qua cua hai bug khac cong lai |

**Huong mo rong:** bo sung mot truc thu nam vao file spec:

```jsonc
"scenarios": [
  {
    "id": "SCN-C3-01",
    "title": "PUT mot phan lam sap may chu khi doc lai",
    "steps": [
      { "method": "POST", "path": "/api/products", "body": {...}, "save": { "pid": "id" } },
      { "method": "PUT",  "path": "/api/products/{pid}", "body": { "name": "chi ten" } },
      { "method": "GET",  "path": "/api/products/{pid}" }
    ],
    "assertions": [
      { "type": "cross_step", "expr": "steps[2].price != null" },
      { "type": "server_alive" }
    ]
  }
]
```

Bo sinh se sinh ra mot chuoi request kem cac **khang dinh bac cao** lien ket cac buoc
(`cross_step`). Day la buoc chuyen tu **0-switch coverage** sang **n-switch coverage**, va no
xu ly dung nhom bug ma phien ban hien tai bo sot.

### 6.2 Cac han che khac

| Han che | Anh huong | Huong xu ly |
|---|---|---|
| Chat luong dau ra **hoan toan** phu thuoc chat luong file spec. Spec sai thi test sai theo — nhu vu bang SEC | Cao | Them buoc doi chieu tu dong: kiem moi ma SEC dung trong spec co ton tai trong tai lieu goc khong |
| Chi sinh duoc **assertion o dang van xuoi**; 17-23% khong dich duoc sang phep kiem Postman | Trung binh | Cho phep spec khai bao assertion co cau truc (`{"type":"json_path","path":"$.price","op":"is_number"}`) thay vi chuoi tu do |
| Khong sinh duoc du lieu test ngau nhien (property-based testing) | Trung binh | Ket noi voi `hypothesis` hoac `fast-check` de sinh gia tri bien tu dinh nghia kieu |
| Khong tu do duoc thoi gian phan hoi hay tai trong | Thap | Ngoai pham vi HW06 (thuoc HW05 Performance Testing) |
| Bang quyet dinh phai liet ke tay tung to hop | Trung binh | Sinh to hop tu dong tu danh sach dieu kien, kem thuat toan pairwise de giam so case |

## 7. Bang chung bo sinh chay duoc that

```bash
$ python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py \
    --spec spec/api-3.json --only DOM --out testcases/API-3_generated.csv
Da ghi 51 case (DOM) vao testcases/API-3_generated.csv | tong file: 51
So case theo nhom: DOM=51, STA=0, SEC=0, SCH=0
Tong: 51
Tham so CHUA phu DOM: (khong)
```

Toan bo chuoi cong cu, chay duoc doc lap:

| Script | Vai tro |
|---|---|
| `gen_testcases.py` | **Bo sinh test case** — trong tam cua muc 7 de bai |
| `audit_testcases.py` | Gan nhan VALID / INVALID / INCOMPLETE bang 10 luat tai lap duoc |
| `extend_testcases.py` | 18 case do con nguoi viet, kem ly do AI bo sot |
| `build_collection.py` | CSV -> Postman Collection v2.1 chay duoc |
| `run_newman.sh` / `run_datadriven.sh` | Chay Newman tren CSDL sach |
| `derive_contract.py` | Chot moc hoi quy tu ket qua chay that |
| `summarize_newman.py` | Newman JSON -> bang tong hop bao cao |
| `verify_header.py` | Kiem chung header `X-Student-Id` chong gian lan |
| `capture_bug_evidence.py` | Chay lai kich ban tai hien tung bug, ghi request/response that |
| `make_bug_report.py` | Sinh bug report + file dan len GitHub Issues |
| `tc_to_excel.py` | CSV -> Excel co sheet Summary |
| `ai_log.py` | Ghi AI_log va sinh AI Audit Report |
| `validate_submission.py` | Kiem du deliverable truoc khi nen nop |

## 8. Bo cong cu nay tai su dung duoc cho bai khac khong

Duoc, va do la muc tieu cua de bai (*"You are encouraged to build Agent Skills that can
automatically perform these activities on similar exercises"*). De ap cho mot SUT khac:

1. Viet file `spec/api-N.json` moi theo `spec/_SCHEMA.md` — **day la viec duy nhat ton cong**.
2. Sua bang `SEC_DEFAULT_ASSERT` theo bang yeu cau bao mat cua he thong do (**va nho bai hoc o
   muc 5.2: doc tu tai lieu, khong dien tu tri nho**).
3. Sua `build_env()` cho khop tai khoan va bien moi truong cua he thong moi.
4. Toan bo phan con lai — sinh, audit, dung collection, chay, tong hop, thu bang chung bug —
   chay duoc ngay khong sua.
