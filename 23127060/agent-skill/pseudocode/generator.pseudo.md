# Pseudocode — Bo sinh test case tu dong (AI-driven API test generator)

SV: Ninh Van Khai — 23127060 — HW06
Ban hien thuc that: `agent-skill/eshop-api-23127060/scripts/gen_testcases.py`
So do tuong ung: `agent-skill/diagram/23127060_generator_diagram.png` — **do sinh vien tu ve**
(de bai muc 11 cam so do nay duoc sinh bang AI). Mo ta khoi va luong de ve: `agent-skill/diagram/DIAGRAM_BRIEF.md`.

---

## 0. Y tuong

Thay vi bao AI "hay viet 35 test case" (ket qua khong on dinh, khong lap lai duoc),
ta tach lam 2 lop:

- **Lop tri thuc (AI + nguoi lam)**: dich dac ta API thanh mot file `spec/api-N.json`
  may doc duoc — liet ke param, phan hoach tuong duong, gia tri bien, chuyen trang thai,
  ca kiem thu bao mat.
- **Lop sinh (may lam, tat dinh)**: mot chuong trinh duyet spec do va sinh ra test case
  theo dung 4 ky thuat kiem thu. Cung 1 spec luon cho ra cung 1 bo test case.

Nho vay: bo test **lap lai duoc**, **do phu do duoc**, va **mo rong duoc** cho API moi
chi bang cach viet them 1 file JSON.

---

## 1. Cau truc du lieu

```
SPEC := {
    api_id, fr, pool, name, base_url, tc_prefix,
    endpoints    : [ ENDPOINT ],
    state_machine: STATE_MACHINE,
    security     : [ SEC_CASE ],
    schema_cases : [ SCHEMA_CASE ]
}

ENDPOINT := { key, method, path, auth_required, success_status,
              preconditions, headers, valid_body, params: [ PARAM ] }

PARAM    := { name, in(body|query|path), type, required,
              partitions: [ PARTITION ] }

PARTITION := { id, value | omit, valid, desc, technique, boundary,
               expected_status, assertions, oracle, sec, priority, tag, bug }

STATE_MACHINE := { name, endpoint, method, states: [S],
                   transitions: [ { from, to, allowed, method, endpoint,
                                    preconditions, headers, body,
                                    expected_status, assertions, bug } ] }

TESTCASE := 22 truong (xem COLUMNS trong gen_testcases.py)
```

---

## 2. Thuat toan chinh

```
HAM main(duong_dan_spec, duong_dan_csv, cac_nhom_can_sinh):

    spec  <- DOC_JSON(duong_dan_spec)
    spec  <- CHUAN_HOA(spec)          # dien mac dinh, suy ra tc_prefix

    cases <- danh sach rong

    NEU "DOM" thuoc cac_nhom_can_sinh: cases += SINH_DOMAIN(spec)
    NEU "STA" thuoc cac_nhom_can_sinh: cases += SINH_STATE(spec)
    NEU "SEC" thuoc cac_nhom_can_sinh: cases += SINH_SECURITY(spec)
    NEU "SCH" thuoc cac_nhom_can_sinh: cases += SINH_SCHEMA(spec)

    cases <- KHU_TRUNG(cases)
    cases <- DANH_SO_LAI(cases)       # TC-<prefix>-<NHOM>-<3 chu so>

    bao_cao <- KIEM_TRA_DO_PHU(spec, cases)
    IN(bao_cao)

    GHI_CSV(cases, duong_dan_csv)     # utf-8-sig, 22 cot
    TRA VE cases
```

---

## 3. Bo sinh Domain — Equivalence Partitioning + BVA

```
HAM SINH_DOMAIN(spec):
    ket_qua <- rong

    VOI MOI ep TRONG spec.endpoints:
        VOI MOI p TRONG ep.params:
            VOI MOI part TRONG p.partitions:

                # Nguyen tac "one-variable-at-a-time":
                # chi bien doi DUY NHAT param dang xet, cac param khac giu gia tri hop le.
                body <- BAN_SAO(ep.valid_body)

                NEU part.omit == dung:
                    XOA_KHOA(body, p.name)
                NGUOC LAI NEU p.in == "body":
                    body[p.name] <- part.value
                NGUOC LAI NEU p.in == "query":
                    duong_dan <- ep.path + "?" + p.name + "=" + part.value
                NGUOC LAI NEU p.in == "path":
                    duong_dan <- THAY_THE(ep.path, ":" + p.name, part.value)

                ky_thuat <- "BVA" NEU part.boundary NGUOC LAI "EP"

                tc <- TAO_CASE(
                    nhom            = "DOM",
                    ky_thuat        = ky_thuat,
                    tieu_de         = ep.method + " " + ep.path + " - "
                                      + p.name + " = " + part.desc,
                    body            = body,
                    trang_thai_mong_doi = part.expected_status
                                          HOAC (ep.success_status NEU part.valid
                                                NGUOC LAI 400),
                    khang_dinh      = part.assertions HOAC SINH_MAC_DINH(part),
                    oracle          = part.oracle HOAC ("IMPL" NEU part.bug
                                                        NGUOC LAI "SPEC"),
                    tag             = "@bug" NEU part.bug NGUOC LAI "@contract",
                    bug_ref         = part.bug,
                    nguon           = "AI"
                )
                ket_qua.THEM(tc)

    TRA VE ket_qua
```

> Do phu dat duoc: **moi phan hoach cua moi tham so deu co it nhat 1 test case**.
> Voi tham so so hoc, spec luon khai bao bo ba bien `duoi bien / dung bien / tren bien`.

---

## 4. Bo sinh State Transition

```
HAM SINH_STATE(spec):
    sm <- spec.state_machine
    NEU sm rong: TRA VE rong

    ket_qua <- rong
    VOI MOI t TRONG sm.transitions:

        NEU t.allowed == dung:
            # chuyen hop le -> phai thanh cong
            trang_thai_mong_doi <- t.expected_status HOAC 200
            tieu_de <- "Chuyen hop le: " + t.from + " -> " + t.to
        NGUOC LAI:
            # chuyen KHONG hop le -> phai bi tu choi.
            # Day la phan AI hay bo sot nhat: sinh du ca o "cam" cua ma tran.
            trang_thai_mong_doi <- t.expected_status HOAC 400
            tieu_de <- "Chuyen KHONG hop le: " + t.from + " -> " + t.to
                       + " (phai bi tu choi)"

        tc <- TAO_CASE(
            nhom      = "STA",
            ky_thuat  = "State Transition Testing",
            tieu_de   = tieu_de,
            dieu_kien_truoc = t.preconditions
                              HOAC ("Dua doi tuong ve trang thai " + t.from),
            body      = t.body,
            trang_thai_mong_doi = trang_thai_mong_doi,
            khang_dinh = t.assertions
                         HOAC ("trang thai sau khi goi phai la "
                               + (t.to NEU t.allowed NGUOC LAI t.from)),
            tag       = "@bug" NEU t.bug NGUOC LAI "@contract",
            bug_ref   = t.bug,
            nguon     = "AI"
        )
        ket_qua.THEM(tc)

    TRA VE ket_qua
```

> Kiem tra do phu: so o da phu / (so trang thai)^2. Bao cao o nao con trong.

---

## 5. Bo sinh Security — anh xa SEC-01..SEC-07

```
# CANH BAO DA HOC DUOC: bang nay tung duoc viet theo TRI NHO ve cac lo hong OWASP quen
# thuoc (SEC-01 = SQL Injection, SEC-04 = IDOR, SEC-05 = leo thang quyen, SEC-07 = brute
# force). Doi chieu voi `eshop-sut/README.md` muc 9 thi bang do SAI HOAN TOAN, va hau qua la
# 39/41 test case bao mat bi gan sai ma. Bang duoi day la bang THAT.
#
# Ma SEC la mot NHAN KHONG TU GIAI THICH: doc "SEC-01" khong ai doan duoc no noi gi. Bo sinh
# nao dung nhan kieu nay deu phai lay dinh nghia tu chinh tai lieu dac ta, khong duoc dien
# tu tri nho. Xem `report/03_audit.md` muc 4.
BANG_KHANG_DINH_MAC_DINH := {
    "SEC-01": "response KHONG chua truong password; mat khau khong duoc luu plaintext",
    "SEC-02": "thieu token -> 401; token sai -> 403; du lieu KHONG bi doc hay thay doi",
    "SEC-03": "token hop le nhung role != 'admin' -> 403; thao tac admin KHONG duoc thuc hien",
    "SEC-04": "payload HTML/script khong duoc luu tho; server escape hoac tu choi (4xx)",
    "SEC-05": "payload SQLi bi coi la chuoi tim kiem thuong, khong doi ngu nghia cau lenh",
    "SEC-06": "truong role trong body bi bo qua; role cua tai khoan van la 'user'",
    "SEC-07": "OTP dai >= 6 chu so, co han su dung, va khong dung lai duoc lan hai"
}

HAM SINH_SECURITY(spec):
    ket_qua <- rong
    VOI MOI s TRONG spec.security:
        tc <- TAO_CASE(
            nhom       = "SEC",
            ky_thuat   = s.technique,
            tieu_de    = "[" + s.sec + "] " + s.title,
            headers    = s.headers,
            body       = s.body,
            trang_thai_mong_doi = s.expected_status,
            khang_dinh = s.assertions HOAC BANG_KHANG_DINH_MAC_DINH[s.sec],
            sec_ref    = s.sec,
            oracle     = "IMPL" NEU s.bug NGUOC LAI "SPEC",
            tag        = "@bug" NEU s.bug NGUOC LAI "@contract",
            uu_tien    = s.priority HOAC "P1",
            nguon      = "AI"
        )
        ket_qua.THEM(tc)

    # Chot chan ve do phu.
    #
    # Phien ban dau doi "moi API phai phu du 7 ma SEC". Yeu cau do BAT KHA THI: SEC-07 noi ve
    # vong doi OTP thi khong the ap vao API quan ly san pham, SEC-01 noi ve luu tru mat khau
    # thi khong lien quan gi den luong thanh toan. Va chinh yeu cau do gay hai: cach duy nhat
    # de "dat chi tieu" la gan bua mot ma SEC cho mot case khong thuoc no.
    #
    # Chi tieu dung: du 7 ma tren TOAN BO bo test, con tung API chi phu nhung ma thuc su ap
    # dung duoc, va phan khong ap dung phai co giai trinh.
    thieu <- { SEC-01..SEC-07 } \ { s.sec : s trong spec.security }
    NEU thieu khong rong:
        BAO_CAO("API nay khong ap dung cac ma: " + thieu
                + " -> can mot dong giai trinh trong bao cao, khong phai mot case gan bua")

    TRA VE ket_qua
```

---

## 6. Bo sinh Schema

```
HAM SINH_SCHEMA(spec):
    ket_qua <- rong
    VOI MOI sc TRONG spec.schema_cases:
        tc <- TAO_CASE(
            nhom       = "SCH",
            ky_thuat   = "JSON Schema Validation",
            tieu_de    = sc.title,
            trang_thai_mong_doi = sc.expected_status,
            khang_dinh = sc.assertions
                         + "; pm.response.to.have.jsonSchema(" + sc.schema_ref + ")",
            oracle     = "IMPL" NEU sc.bug NGUOC LAI "SPEC",
            nguon      = "AI"
        )
        ket_qua.THEM(tc)
    TRA VE ket_qua
```

---

## 7. Khu trung

```
HAM KHU_TRUNG(cases):
    da_thay <- tap rong
    giu_lai <- rong
    VOI MOI c TRONG cases:
        # Hai test case chi trung nhau khi chung gui CUNG mot request VA khang dinh CUNG mot
        # dieu, trong CUNG mot nhom ky thuat, VA xuat phat tu CUNG mot precondition.
        khoa <- (c.Category, c.Method, c.Endpoint, c.Request_Body,
                 c.Expected_Status, c.Expected_Assertions, c.Preconditions)
        NEU khoa KHONG thuoc da_thay:
            da_thay.THEM(khoa)
            giu_lai.THEM(c)
    TRA VE giu_lai
```

> **Loi da mac va da sua o buoc nay.** Khoa khu trung ban dau chi gom
> `(Method, Endpoint, Request_Body, Expected_Status)` — tuc la coi hai case la trung nhau khi
> chung gui cung mot request, **bat ke chung khang dinh dieu gi**. Hau qua:
>
> - Mot case `SCH` ("response 200 khop schema `{message: string}`") va mot case `DOM`
>   ("email hop le tra 200") gui y het nhau nhung kiem hai thu khac han. Case `SCH` bi nuot:
>   API-1 khai bao 6 case schema nhung chi sinh ra **1**.
> - Hai case `STA` "huy don dang `pending`" va "huy don dang `confirmed`" cung goi
>   `PUT /api/orders/:id/cancel` voi body rong; chung chi khac nhau o **trang thai ban dau**.
>   Case thu hai bi nuot: 9 chuyen trang thai chi sinh ra **5**.
>
> Sau khi bo sung `Category`, `Expected_Assertions` va `Preconditions` vao khoa: tong so case
> tu 191 len **225**, va do phu bang chuyen trang thai cua API-2 tu 11/25 len **20/25**.
>
> Bai hoc: **cong cu tu dong cung phai duoc kiem thu.** Neu tin ngay con so dau tien thi da
> bao cao thieu 34 test case va mot do phu state machine sai.

---

## 8. Kiem tra do phu — "cong tac chan" cua toan bo bo sinh

```
HAM KIEM_TRA_DO_PHU(spec, cases):
    dem_theo_nhom <- DEM(cases theo Category)

    canh_bao <- rong

    NEU TONG(cases) < 35:
        canh_bao.THEM("CHUA DAT: chi co " + TONG(cases)
                      + " case, de bai yeu cau >= 35")

    param_chua_phu <- rong
    VOI MOI ep, p TRONG spec.endpoints:
        NEU khong co case nao nhac den p.name:
            param_chua_phu.THEM(ep.key + "." + p.name)

    sec_thieu <- { SEC-01..07 } \ { c.SEC_Ref : c trong cases }

    o_trong <- { (a,b) : a,b trong sm.states
                 va khong co transition nao phu (a,b) }

    TRA VE bao cao gom: dem_theo_nhom, canh_bao,
                        param_chua_phu, sec_thieu, o_trong
```

---

## 9. Vi tri cua con nguoi trong quy trinh

Bo sinh **khong** thay the nguoi kiem thu. Sau buoc 8, con nguoi phai:

1. **Audit**: doc tung case AI sinh, gan `VALID` / `INVALID` / `INCOMPLETE`, ghi ly do va sua lai.
2. **Extend**: them >= 5 case ma bo sinh khong the nghi ra, danh so tu `900`, kem cot
   `Why_AI_Missed` — roi vao 4 nhom:
   - `PROMPT`  — prompt khoanh vung qua chat (vd chi neu 2 endpoint chinh cua FR-03)
   - `MODEL`   — AI suy dien tu hinh dang API thay vi doc ma nguon
   - `API`     — bug chi lo ra khi **ket hop nhieu request**
   - `SPECGAP` — dac ta khong mo ta hanh vi nay nen AI khong co gi de bam vao

   > **So lieu thuc te cua bai nay: 9/18 case bo sung thuoc nhom `API`.** Do la gioi han
   > **cau truc** cua chinh thiet ke o tren: vong lap `VOI MOI part TRONG p.partitions` sinh
   > ra cac test case **doc lap**, moi case mot request. Nhung mot nua so bug nghiem trong cua
   > he thong nay chi lo ra khi noi nhieu request lai: kieu cua `price` chi sai khi so sanh
   > hai response; don hang chi vao duoc trang thai `shipping` sau mot chuoi 4 request; mot
   > lenh `PUT` thieu truong chi lam sap may chu o lan `GET` ke tiep.
   >
   > Huong mo rong: bo sung mot truc thu nam `scenarios[]` khai bao **chuoi** request kem
   > khang dinh bac cao lien ket cac buoc — xem `report/07_test_generator_design.md` muc 6.
3. **Xac nhan oracle**: quyet dinh case nao la `@contract` (hop dong dung, dung cho CI)
   va case nao la `@bug` (phoi bay loi that cua SUT, FAIL la dung).

---

## 10. Do phuc tap

Goi `E` = so endpoint, `P` = so param trung binh moi endpoint,
`K` = so phan hoach trung binh moi param, `T` = so chuyen trang thai,
`S` = so ca bao mat, `C` = so ca schema.

```
So test case sinh ra  =  E * P * K  +  T  +  S  +  C
Do phuc tap thoi gian =  O(E*P*K + T + S + C)
Do phuc tap bo nho    =  O(so test case)
```

Voi API-3 (FR-15): `E=5`, `P~2`, `K~6` → khoang 60 case DOM `+` 9 STA `+` 14 SEC `+` 6 SCH,
sau khu trung con khoang 70–80 case — vuot xa nguong 35 cua de bai.
