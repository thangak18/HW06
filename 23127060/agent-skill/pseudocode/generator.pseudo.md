# Pseudocode — Bộ sinh test case tự động (AI-driven API test generator)

SV: Ninh Văn Khải — 23127060 — HW06
Bản hiện thực thật: `agent-skill/eshop-api-23127060/scripts/gen_testcases.py`
Sơ đồ tương ứng: `agent-skill/diagram/23127060_generator_diagram.png` — **do sinh viên tự vẽ**
(đề bài mục 11 cấm sơ đồ này được sinh bằng AI). Mô tả khối và luồng để vẽ: `agent-skill/diagram/DIAGRAM_BRIEF.md`.

---

## 0. Ý tưởng

Thay vì bảo AI "hãy viết 35 test case" (kết quả không ổn định, không lặp lại được),
em tách làm 2 lớp:

- **Lớp tri thức (AI + người làm)**: dịch đặc tả API thành một file `spec/api-N.json`
  máy đọc được — liệt kê param, phân hoạch tương đương, giá trị biên, chuyển trạng thái,
  ca kiểm thử bảo mật.
- **Lớp sinh (máy làm, tất định)**: một chương trình duyệt spec đó và sinh ra test case
  theo đúng 4 kỹ thuật kiểm thử. Cùng 1 spec luôn cho ra cùng 1 bộ test case.

Nhờ vậy: bộ test **lặp lại được**, **độ phủ đo được**, và **mở rộng được** cho API mới
chỉ bằng cách viết thêm 1 file JSON.

---

## 1. Cấu trúc dữ liệu

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

## 2. Thuật toán chính

```
HÀM main(đường_dẫn_spec, đường_dẫn_csv, các_nhóm_cần_sinh):

    spec  <- ĐỌC_JSON(đường_dẫn_spec)
    spec  <- CHUẨN_HÓA(spec)          # dien mac dinh, suy ra tc_prefix

    cases <- danh sách rỗng

    NẾU "DOM" thuộc các_nhóm_cần_sinh: cases += SINH_DOMAIN(spec)
    NẾU "STA" thuộc các_nhóm_cần_sinh: cases += SINH_STATE(spec)
    NẾU "SEC" thuộc các_nhóm_cần_sinh: cases += SINH_SECURITY(spec)
    NẾU "SCH" thuộc các_nhóm_cần_sinh: cases += SINH_SCHEMA(spec)

    cases <- KHỬ_TRÙNG(cases)
    cases <- ĐÁNH_SỐ_LẠI(cases)       # TC-<prefix>-<NHOM>-<3 chu so>

    báo_cáo <- KIỂM_TRA_ĐỘ_PHỦ(spec, cases)
    IN(báo_cáo)

    GHI_CSV(cases, đường_dẫn_csv)     # utf-8-sig, 22 cot
    TRẢ VỀ cases
```

---

## 3. Bộ sinh Domain — Equivalence Partitioning + BVA

```
HÀM SINH_DOMAIN(spec):
    kết_quả <- rỗng

    VỚI MỖI ep TRONG spec.endpoints:
        VỚI MỖI p TRONG ep.params:
            VỚI MỖI part TRONG p.partitions:

                # Nguyen tac "one-variable-at-a-time":
                # chi bien doi DUY NHAT param dang xet, cac param khac giu gia tri hop le.
                body <- BẢN_SAO(ep.valid_body)

                NẾU part.omit == đúng:
                    XÓA_KHÓA(body, p.name)
                NGƯỢC LẠI NẾU p.in == "body":
                    body[p.name] <- part.value
                NGƯỢC LẠI NẾU p.in == "query":
                    đường_dẫn <- ep.path + "?" + p.name + "=" + part.value
                NGƯỢC LẠI NẾU p.in == "path":
                    đường_dẫn <- THAY_THẾ(ep.path, ":" + p.name, part.value)

                kỹ_thuật <- "BVA" NẾU part.boundary NGƯỢC LẠI "EP"

                tc <- TẠO_CASE(
                    nhóm            = "DOM",
                    kỹ_thuật        = kỹ_thuật,
                    tiêu_đề         = ep.method + " " + ep.path + " - "
                                      + p.name + " = " + part.desc,
                    body            = body,
                    trạng_thái_mong_đợi = part.expected_status
                                          HOẶC (ep.success_status NẾU part.valid
                                                NGƯỢC LẠI 400),
                    khẳng_định      = part.assertions HOẶC SINH_MẶC_ĐỊNH(part),
                    oracle          = part.oracle HOẶC ("IMPL" NẾU part.bug
                                                        NGƯỢC LẠI "SPEC"),
                    tag             = "@bug" NẾU part.bug NGƯỢC LẠI "@contract",
                    bug_ref         = part.bug,
                    nguồn           = "AI"
                )
                kết_quả.THÊM(tc)

    TRẢ VỀ kết_quả
```

> Độ phủ đạt được: **mọi phân hoạch của mọi tham số đều có ít nhất 1 test case**.
> Với tham số số học, spec luôn khai báo bộ ba biên `dưới biên / đúng biên / trên biên`.

---

## 4. Bộ sinh State Transition

```
HÀM SINH_STATE(spec):
    sm <- spec.state_machine
    NẾU sm rỗng: TRẢ VỀ rỗng

    kết_quả <- rỗng
    VỚI MỖI t TRONG sm.transitions:

        NẾU t.allowed == đúng:
            # chuyen hop le -> phai thanh cong
            trạng_thái_mong_đợi <- t.expected_status HOẶC 200
            tiêu_đề <- "Chuyen hop le: " + t.from + " -> " + t.to
        NGƯỢC LẠI:
            # chuyen KHONG hop le -> phai bi tu choi.
            # Day la phan AI hay bo sot nhat: sinh du ca o "cam" cua ma tran.
            trạng_thái_mong_đợi <- t.expected_status HOẶC 400
            tiêu_đề <- "Chuyen KHONG hop le: " + t.from + " -> " + t.to
                       + " (phai bi tu choi)"

        tc <- TẠO_CASE(
            nhóm      = "STA",
            kỹ_thuật  = "State Transition Testing",
            tiêu_đề   = tiêu_đề,
            điều_kiện_trước = t.preconditions
                              HOẶC ("Dua doi tuong ve trang thai " + t.from),
            body      = t.body,
            trạng_thái_mong_đợi = trạng_thái_mong_đợi,
            khẳng_định = t.assertions
                         HOẶC ("trang thai sau khi goi phai la "
                               + (t.to NẾU t.allowed NGƯỢC LẠI t.from)),
            tag       = "@bug" NẾU t.bug NGƯỢC LẠI "@contract",
            bug_ref   = t.bug,
            nguồn     = "AI"
        )
        kết_quả.THÊM(tc)

    TRẢ VỀ kết_quả
```

> Kiểm tra độ phủ: số ô đã phủ / (số trạng thái)^2. Báo cáo ô nào còn trống.

---

## 5. Bộ sinh Security — ánh xạ SEC-01..SEC-07

```
# CANH BAO DA HOC DUOC: bang nay tung duoc viet theo TRI NHO ve cac lo hong OWASP quen
# thuoc (SEC-01 = SQL Injection, SEC-04 = IDOR, SEC-05 = leo thang quyen, SEC-07 = brute
# force). Doi chieu voi `eshop-sut/README.md` muc 9 thi bang do SAI HOAN TOAN, va hau qua la
# 39/41 test case bao mat bi gan sai ma. Bang duoi day la bang THAT.
#
# Ma SEC la mot NHAN KHONG TU GIAI THICH: doc "SEC-01" khong ai doan duoc no noi gi. Bo sinh
# nao dung nhan kieu nay deu phai lay dinh nghia tu chinh tai lieu dac ta, khong duoc dien
# tu tri nho. Xem `report/03_audit.md` muc 4.
BẢNG_KHẲNG_ĐỊNH_MẶC_ĐỊNH := {
    "SEC-01": "response KHONG chua truong password; mat khau khong duoc luu plaintext",
    "SEC-02": "thieu token -> 401; token sai -> 403; du lieu KHONG bi doc hay thay doi",
    "SEC-03": "token hop le nhung role != 'admin' -> 403; thao tac admin KHONG duoc thuc hien",
    "SEC-04": "payload HTML/script khong duoc luu tho; server escape hoac tu choi (4xx)",
    "SEC-05": "payload SQLi bi coi la chuoi tim kiem thuong, khong doi ngu nghia cau lenh",
    "SEC-06": "truong role trong body bi bo qua; role cua tai khoan van la 'user'",
    "SEC-07": "OTP dai >= 6 chu so, co han su dung, va khong dung lai duoc lan hai"
}

HÀM SINH_SECURITY(spec):
    kết_quả <- rỗng
    VỚI MỖI s TRONG spec.security:
        tc <- TẠO_CASE(
            nhóm       = "SEC",
            kỹ_thuật   = s.technique,
            tiêu_đề    = "[" + s.sec + "] " + s.title,
            headers    = s.headers,
            body       = s.body,
            trạng_thái_mong_đợi = s.expected_status,
            khẳng_định = s.assertions HOẶC BẢNG_KHẲNG_ĐỊNH_MẶC_ĐỊNH[s.sec],
            sec_ref    = s.sec,
            oracle     = "IMPL" NẾU s.bug NGƯỢC LẠI "SPEC",
            tag        = "@bug" NẾU s.bug NGƯỢC LẠI "@contract",
            ưu_tiên    = s.priority HOẶC "P1",
            nguồn      = "AI"
        )
        kết_quả.THÊM(tc)

    # Chot chan ve do phu.
    #
    # Phien ban dau doi "moi API phai phu du 7 ma SEC". Yeu cau do BAT KHA THI: SEC-07 noi ve
    # vong doi OTP thi khong the ap vao API quan ly san pham, SEC-01 noi ve luu tru mat khau
    # thi khong lien quan gi den luong thanh toan. Va chinh yeu cau do gay hai: cach duy nhat
    # de "dat chi tieu" la gan bua mot ma SEC cho mot case khong thuoc no.
    #
    # Chi tieu dung: du 7 ma tren TOAN BO bo test, con tung API chi phu nhung ma thuc su ap
    # dung duoc, va phan khong ap dung phai co giai trinh.
    thiếu <- { SEC-01..SEC-07 } \ { s.sec : s trong spec.security }
    NẾU thiếu không rỗng:
        BÁO_CÁO("API nay khong ap dung cac ma: " + thiếu
                + " -> can mot dong giai trinh trong bao cao, khong phai mot case gan bua")

    TRẢ VỀ kết_quả
```

---

## 6. Bộ sinh Schema

```
HÀM SINH_SCHEMA(spec):
    kết_quả <- rỗng
    VỚI MỖI sc TRONG spec.schema_cases:
        tc <- TẠO_CASE(
            nhóm       = "SCH",
            kỹ_thuật   = "JSON Schema Validation",
            tiêu_đề    = sc.title,
            trạng_thái_mong_đợi = sc.expected_status,
            khẳng_định = sc.assertions
                         + "; pm.response.to.have.jsonSchema(" + sc.schema_ref + ")",
            oracle     = "IMPL" NẾU sc.bug NGƯỢC LẠI "SPEC",
            nguồn      = "AI"
        )
        kết_quả.THÊM(tc)
    TRẢ VỀ kết_quả
```

---

## 7. Khử trùng

```
HÀM KHỬ_TRÙNG(cases):
    đã_thấy <- tập rỗng
    giữ_lại <- rỗng
    VỚI MỖI c TRONG cases:
        # Hai test case chi trung nhau khi chung gui CUNG mot request VA khang dinh CUNG mot
        # dieu, trong CUNG mot nhom ky thuat, VA xuat phat tu CUNG mot precondition.
        khóa <- (c.Category, c.Method, c.Endpoint, c.Request_Body,
                 c.Expected_Status, c.Expected_Assertions, c.Preconditions)
        NẾU khóa KHÔNG thuộc đã_thấy:
            đã_thấy.THÊM(khóa)
            giữ_lại.THÊM(c)
    TRẢ VỀ giữ_lại
```

> **Lỗi em đã mắc và đã sửa ở bước này.** Khóa khử trùng ban đầu chỉ gồm
> `(Method, Endpoint, Request_Body, Expected_Status)` — tức là coi hai case là trùng nhau khi
> chúng gửi cùng một request, **bất kể chúng khẳng định điều gì**. Hậu quả:
>
> - Một case `SCH` ("response 200 khớp schema `{message: string}`") và một case `DOM`
>   ("email hợp lệ trả 200") gửi y hệt nhau nhưng kiểm hai thứ khác hẳn. Case `SCH` bị nuốt:
>   API-1 khai báo 6 case schema nhưng chỉ sinh ra **1**.
> - Hai case `STA` "hủy đơn đang `pending`" và "hủy đơn đang `confirmed`" cùng gọi
>   `PUT /api/orders/:id/cancel` với body rỗng; chúng chỉ khác nhau ở **trạng thái ban đầu**.
>   Case thứ hai bị nuốt: 9 chuyển trạng thái chỉ sinh ra **5**.
>
> Sau khi bổ sung `Category`, `Expected_Assertions` và `Preconditions` vào khóa: tổng số case
> từ 191 lên **225**, và độ phủ bảng chuyển trạng thái của API-2 từ 11/25 lên **20/25**.
>
> Bài học: **công cụ tự động cũng phải được kiểm thử.** Nếu em tin ngay con số đầu tiên thì đã
> báo cáo thiếu 34 test case và một độ phủ state machine sai.

---

## 8. Kiểm tra độ phủ — "công tắc chặn" của toàn bộ bộ sinh

```
HÀM KIỂM_TRA_ĐỘ_PHỦ(spec, cases):
    đếm_theo_nhóm <- ĐẾM(cases theo Category)

    cảnh_báo <- rỗng

    NẾU TỔNG(cases) < 35:
        cảnh_báo.THÊM("CHUA DAT: chi co " + TỔNG(cases)
                      + " case, de bai yeu cau >= 35")

    param_chưa_phủ <- rỗng
    VỚI MỖI ep, p TRONG spec.endpoints:
        NẾU không có case nào nhắc đến p.name:
            param_chưa_phủ.THÊM(ep.key + "." + p.name)

    sec_thiếu <- { SEC-01..07 } \ { c.SEC_Ref : c trong cases }

    ô_trống <- { (a,b) : a,b trong sm.states
                 và không có transition nào phủ (a,b) }

    TRẢ VỀ báo cáo gồm: đếm_theo_nhóm, cảnh_báo,
                        param_chưa_phủ, sec_thiếu, ô_trống
```

---

## 9. Vị trí của con người trong quy trình

Bộ sinh **không** thay thế người kiểm thử. Sau bước 8, con người phải:

1. **Audit**: đọc từng case AI sinh, gắn `VALID` / `INVALID` / `INCOMPLETE`, ghi lý do và sửa lại.
2. **Extend**: thêm >= 5 case mà bộ sinh không thể nghĩ ra, đánh số từ `900`, kèm cột
   `Why_AI_Missed` — rơi vào 4 nhóm:
   - `PROMPT`  — prompt khoanh vùng quá chật (vd chỉ nêu 2 endpoint chính của FR-03)
   - `MODEL`   — AI suy diễn từ hình dạng API thay vì đọc mã nguồn
   - `API`     — bug chỉ lộ ra khi **kết hợp nhiều request**
   - `SPECGAP` — đặc tả không mô tả hành vi này nên AI không có gì để bám vào

   > **Số liệu thực tế của bài này: 9/18 case bổ sung thuộc nhóm `API`.** Đó là giới hạn
   > **cấu trúc** của chính thiết kế ở trên: vòng lặp `VỚI MỖI part TRONG p.partitions` sinh
   > ra các test case **độc lập**, mỗi case một request. Nhưng một nửa số bug nghiêm trọng của
   > hệ thống này chỉ lộ ra khi nối nhiều request lại: kiểu của `price` chỉ sai khi so sánh
   > hai response; đơn hàng chỉ vào được trạng thái `shipping` sau một chuỗi 4 request; một
   > lệnh `PUT` thiếu trường chỉ làm sập máy chủ ở lần `GET` kế tiếp.
   >
   > Hướng mở rộng: bổ sung một trục thứ năm `scenarios[]` khai báo **chuỗi** request kèm
   > khẳng định bậc cao liên kết các bước — xem `report/07_test_generator_design.md` mục 6.
3. **Xác nhận oracle**: quyết định case nào là `@contract` (hợp đồng đúng, dùng cho CI)
   và case nào là `@bug` (phơi bày lỗi thật của SUT, FAIL là đúng).

---

## 10. Độ phức tạp

Gọi `E` = số endpoint, `P` = số param trung bình mỗi endpoint,
`K` = số phân hoạch trung bình mỗi param, `T` = số chuyển trạng thái,
`S` = số ca bảo mật, `C` = số ca schema.

```
So test case sinh ra  =  E * P * K  +  T  +  S  +  C
Do phuc tap thoi gian =  O(E*P*K + T + S + C)
Do phuc tap bo nho    =  O(so test case)
```

Với API-3 (FR-15): `E=5`, `P~2`, `K~6` → khoảng 60 case DOM `+` 9 STA `+` 14 SEC `+` 6 SCH,
sau khử trùng còn khoảng 70–80 case — vượt xa ngưỡng 35 của đề bài.
