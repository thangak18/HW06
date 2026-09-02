# Pseudocode — Bộ sinh test case API bằng AI

**HW06 · 23127195** · Đi kèm [`../DESIGN.md`](../DESIGN.md) và cài đặt tham chiếu [`generator.py`](./generator.py)

Ký hiệu: `LLM(...)` là chỗ **duy nhất** gọi mô hình ngôn ngữ. Mọi thứ còn lại là mã tất định.

---

## Chương trình chính

```
THUAT_TOAN SinhTestCaseAPI(duong_dan_dac_ta_api, duong_dan_srs, endpoint_can_sinh)

    ── G1: TRÍCH XUẤT (dùng LLM) ──────────────────────────────────────────
    tai_lieu ← doc(duong_dan_dac_ta_api) + doc(duong_dan_srs)

    // Nạp CẢ HAI tài liệu. Yêu cầu bảo mật SEC-01..SEC-07 chỉ nằm ở SRS,
    // không có trong đặc tả API — chỉ nạp một tài liệu là mất toàn bộ
    // chiều bảo mật.

    mo_hinh ← LLM(
        vai_tro   = "kỹ sư kiểm thử, trích xuất đặc tả thành cấu trúc",
        dau_vao   = tai_lieu,
        muc_tieu  = endpoint_can_sinh,
        rang_buoc = "CHỈ trích xuất. KHÔNG sinh test case ở bước này.
                     Mỗi ràng buộc phải kèm trích dẫn nguyên văn từ tài liệu.
                     Nếu tài liệu im lặng về một điểm, ghi 'KHÔNG ĐƯỢC ĐẶC TẢ',
                     TUYỆT ĐỐI không suy đoán."
        lươc_do   = EndpointModel
    )

    KIEM_TRA mo_hinh KHỚP lược_đồ EndpointModel
    KIEM_TRA mọi ràng buộc trong mo_hinh đều có trích dẫn nguồn
        NGƯỢC LẠI → dừng, báo lỗi cho người dùng

    ── G2..G5: SINH (tất định) ────────────────────────────────────────────
    ir ← danh_sách_rỗng()
    ir += SinhPhanVungMien(mo_hinh)          // G2
    ir += SinhChuoiTrangThai(mo_hinh)        // G3
    ir += SinhCaseBaoMat(mo_hinh)            // G4
    ir += SinhCaseLuocDo(mo_hinh)            // G5

    ── G6a: KIỂM TRA (tất định) ───────────────────────────────────────────
    KiemTraIR(ir)

    ── G6b: AUDIT CỦA CON NGƯỜI (thủ công — KHÔNG tự động hoá được) ────────
    ir ← ChoConNguoiAudit(ir)

    ── G6c: BIÊN DỊCH (tất định) ──────────────────────────────────────────
    TRẢ VỀ BienDich(ir)
```

---

## Lược đồ EndpointModel — sản phẩm của G1

```
EndpointModel:
    method            : "GET" | "POST" | "PUT" | "DELETE"
    path              : chuỗi                       // "/api/users/me"
    fr                : chuỗi                       // "FR-04"

    can_xac_thuc      : đúng/sai
    vai_tro_yeu_cau   : "user" | "admin" | không

    tham_so : DANH SÁCH của {
        ten            : chuỗi
        vi_tri         : "body" | "query" | "path" | "header"
        kieu           : "string" | "number" | "boolean" | "array" | "object"
        bat_buoc       : đúng/sai
        rang_buoc      : DANH SÁCH của {
            loai       : "bien" | "mau" | "do_dai" | "enum" | "khoa_ngoai" | "duong"
            gia_tri    : ...                        // {min:10,max:11} · "^0\d{9,10}$" · ...
            trich_dan  : chuỗi                      // NGUYÊN VĂN từ tài liệu — bắt buộc
        }
    }

    may_trang_thai : không HOẶC {
        cac_trang_thai      : DANH SÁCH chuỗi
        trang_thai_ket_thuc : DANH SÁCH chuỗi
        chuyen_hop_le       : DANH SÁCH của (từ, đến, ai_được_phép)
    }

    lươc_do_response : {
        thanh_cong  : lược đồ JSON
        loi         : lược đồ JSON
        truong_cam  : DANH SÁCH chuỗi        // "password", "reset_token", ...
    }

    sec_ap_dung : DANH SÁCH của "SEC-01".."SEC-07"
```

---

## G2 — Sinh phân vùng miền

```
HAM SinhPhanVungMien(mo_hinh)
    cases ← []

    VOI MOI tham_so p TRONG mo_hinh.tham_so:

        // (a) Phân vùng phổ quát — áp cho MỌI tham số, không ngoại lệ
        cases += Case(p, "thiếu trường",  bo_truong(p),       ky_vong = 400 NEU p.bat_buoc)
        cases += Case(p, "giá trị null",  gan(p, null),       ky_vong = 400 NEU p.bat_buoc)
        cases += Case(p, "sai kiểu",      gan(p, kieu_khac(p.kieu)), ky_vong = 400)

        // (b) Phân vùng theo kiểu
        NEU p.kieu = "string":
            cases += Case(p, "chuỗi rỗng",          gan(p, ""))
            cases += Case(p, "chỉ khoảng trắng",    gan(p, "     "))
            //  ↑ tách riêng khỏi "chuỗi rỗng": "   " là TRUTHY trong JavaScript
            //    nên lọt qua phép kiểm tra `if (!x)`. Chính phân vùng này tìm ra BUG-A3-06.
            cases += Case(p, "Unicode tiếng Việt",  gan(p, "Nguyễn Thị Hồng Đào"))
            cases += Case(p, "payload SQLi",        gan(p, "' OR '1'='1' --"))
            cases += Case(p, "payload XSS",         gan(p, "<script>alert(1)</script>"))
            cases += Case(p, "khoảng trắng bao quanh", gan(p, "  " + gia_tri_hop_le(p) + "  "))

        NEU p.kieu = "number":
            cases += Case(p, "bằng 0",              gan(p, 0))
            cases += Case(p, "số âm",               gan(p, -1))
            cases += Case(p, "vượt số nguyên an toàn", gan(p, 2^53 + 1))
            cases += Case(p, "số thực",             gan(p, 1.5))
            cases += Case(p, "chuỗi-số",            gan(p, "123"))
            //  ↑ với API nhận dữ liệu từ CSV, đây là trường hợp MẶC ĐỊNH chứ không
            //    phải trường hợp hiếm — mọi ô CSV đều là chuỗi.

        // (c) Phân vùng theo ràng buộc — BẮT BUỘC, không được bỏ
        VOI MOI rang_buoc c TRONG p.rang_buoc:

            NEU c.loai = "bien":              // BVA đầy đủ 6 điểm
                VOI MOI v TRONG [c.min-1, c.min, c.min+1, c.max-1, c.max, c.max+1]:
                    hop_le ← (c.min ≤ v ≤ c.max)
                    cases += Case(p, "biên " + v, gan(p, v),
                                  ky_vong = 200 NEU hop_le NGUOC_LAI 400,
                                  nguon_ky_vong = c.trich_dan)
                    // Điểm v = c.min là nơi phân biệt cài đặt '>' với '>=' —
                    // chính nó tìm ra BUG-A2-03.

            NEU c.loai = "mau":               // biểu thức chính quy
                cases += Case(p, "khớp mẫu",         gan(p, sinh_khop(c.gia_tri)),    ky_vong=200)
                cases += Case(p, "không khớp",       gan(p, sinh_khong_khop(c.gia_tri)), ky_vong=400)
                cases += Case(p, "khớp một phần",    gan(p, sinh_khop_mot_phan(c.gia_tri)), ky_vong=400)
                cases += Case(p, "khác hoa/thường",  gan(p, doi_hoa_thuong(...)))

            NEU c.loai = "khoa_ngoai":
                cases += Case(p, "khoá tồn tại",     gan(p, id_ton_tai()),   ky_vong=200)
                cases += Case(p, "khoá không tồn tại", gan(p, 999999),       ky_vong=400)
                cases += Case(p, "khoá = 0",         gan(p, 0),              ky_vong=400)
                cases += Case(p, "khoá âm",          gan(p, -1),             ky_vong=400)

    // (d) Với API nhận MẢNG bản ghi (như import CSV) — nhân thêm một chiều
    NEU mo_hinh có tham số kiểu "array":
        cases += Case("mảng rỗng",            gan([]),              ky_vong=400)
        cases += Case("không phải mảng",      gan("chuỗi"),         ky_vong=400)
        cases += Case("mảng chứa phần tử null", gan([hop_le, null]), ky_vong="không 5xx")
        cases += Case("mảng lớn (100 phần tử)", gan(sinh_n(100)),   ky_vong="không timeout")

    TRA VE cases
```

---

## G3 — Sinh chuỗi chuyển trạng thái

```
HAM SinhChuoiTrangThai(mo_hinh)
    NEU mo_hinh.may_trang_thai = không: TRA VE []

    M     ← mo_hinh.may_trang_thai
    cases ← []

    // (a) Mọi cạnh HỢP LỆ
    VOI MOI (tu, den, ai) TRONG M.chuyen_hop_le:
        cases += ChuoiCase(
            duong_dan_toi(M.trang_thai_dau, tu),      // các bước setup để đạt trạng thái `tu`
            hanh_dong(tu → den, boi = ai),
            ky_vong = 200)

    // (b) Mọi cạnh KHÔNG hợp lệ — đây là phần LLM hay bỏ sót nhất
    VOI MOI tu TRONG M.cac_trang_thai:
        VOI MOI den TRONG M.cac_trang_thai:
            NEU (tu, den, *) KHÔNG THUỘC M.chuyen_hop_le:
                cases += ChuoiCase(duong_dan_toi(M.trang_thai_dau, tu),
                                   hanh_dong(tu → den),
                                   ky_vong = 400)

    // (c) Cạnh TỰ LẶP — cấp lại/thực hiện lại cùng một hành động
    VOI MOI s TRONG M.cac_trang_thai:
        cases += ChuoiCase(duong_dan_toi(M.trang_thai_dau, s),
                           lap_lai(hanh_dong_dua_den(s)),
                           ky_vong = "hành động cũ phải bị vô hiệu hoá")
        // LLM vẽ vòng đời theo đường thẳng nên gần như luôn bỏ qua nhánh này.

    // (d) Rời khỏi trạng thái KẾT THÚC
    VOI MOI s TRONG M.trang_thai_ket_thuc:
        VOI MOI den TRONG M.cac_trang_thai \ {s}:
            cases += ChuoiCase(duong_dan_toi(M.trang_thai_dau, s),
                               hanh_dong(s → den),
                               ky_vong = 400)

    // (e) Kiểm chứng bằng cách ĐỌC LẠI — không tin vào message trả về
    VOI MOI c TRONG cases:
        c.assertions += doc_lai_va_xac_nhan_trang_thai(c.trang_thai_ky_vong)
        // "Password reset successfully" không chứng minh mật khẩu đã đổi.
        // Phải đăng nhập lại bằng mật khẩu mới mới là bằng chứng.

    // (f) Bảo toàn trường khi cập nhật MỘT PHẦN
    NEU mo_hinh.method = "PUT" VA |mo_hinh.tham_so| > 1:
        VOI MOI tap_con S ⊂ mo_hinh.tham_so, S ≠ ∅:
            cases += Case("cập nhật một phần: chỉ gửi " + S,
                          gui_chi(S),
                          ky_vong = "các trường ngoài S giữ nguyên giá trị")
        // Chính nhánh này tìm ra BUG-A1-05 (mất dữ liệu âm thầm).

    TRA VE cases
```

---

## G4 — Sinh case bảo mật

```
HAM SinhCaseBaoMat(mo_hinh)
    cases ← []

    NEU mo_hinh.can_xac_thuc:
        cases += Case("không kèm token",              khong_header("Authorization"), 401)
        cases += Case("token rác",                    token("khong-phai-jwt"),       403)
        cases += Case("JWT ký bằng khoá sai",         token(ky_khoa_khac({role:"admin"})), 403)
        cases += Case("JWT thuật toán alg=none",      token(alg_none({role:"admin"})),     403)
        // Hai case cuối là phép thử THẬT SỰ cho việc server có verify chữ ký hay
        // chỉ decode payload. Chúng đòi hiểu biết về cách hiện thực JWT, không suy
        // ra được từ đặc tả — nên LLM hầu như không sinh.

    NEU mo_hinh.vai_tro_yeu_cau = "admin":            // SEC-03
        cases += Case("token của user thường", token_vai_tro("user"), 403)
        cases += ChuoiCase(                            // chuỗi TÁC ĐỘNG
            [thu_thao_tac_bang_quyen_thap()],
            kiem_tra_hau_qua_quan_sat_duoc_tu_ben_ngoai(),
            ky_vong = "không có tác động nào")
        // Dừng ở "API có trả 403 không" là chưa đủ. Phải đi thêm một bước để chứng
        // minh MỨC ĐỘ NGHIÊM TRỌNG — ví dụ hàng do user thường chèn có hiện công
        // khai trên cửa hàng không (BUG-A3-01).

    NEU "SEC-06" THUỘC mo_hinh.sec_ap_dung:           // mass assignment
        VOI MOI truong_dac_quyen f TRONG ["role", "id", "is_admin", "email"]:
            cases += Case("gửi kèm " + f, them_truong(f, gia_tri_dac_quyen),
                          ky_vong = "giá trị không đổi sau khi cập nhật")
            // Mấu chốt: đây là các trường KHÔNG có trong đặc tả. LLM sinh test theo
            // danh sách tham số trong tài liệu nên không bao giờ nghĩ tới việc gửi THÊM.

    NEU "SEC-05" THUỘC mo_hinh.sec_ap_dung:           // SQL injection
        VOI MOI tham_so p kiểu chuỗi:
            cases += Case("SQLi qua " + p.ten, gan(p, "' OR '1'='1' --"),
                          ky_vong = "không rò rỉ lỗi SQL, không bỏ qua xác thực")

    NEU "SEC-01" THUỘC mo_hinh.sec_ap_dung:           // rò rỉ dữ liệu nhạy cảm
        VOI MOI truong f TRONG mo_hinh.lươc_do_response.truong_cam:
            cases += Case("response không được chứa " + f, request_hop_le(),
                          ky_vong = "không có trường " + f)

    // IDOR — mọi tham số mang ý nghĩa định danh
    VOI MOI tham_so p CÓ TÊN KHỚP /(^|_)(id|user_id|owner)$/:
        cases += Case("IDOR qua " + p.ten, gan(p, id_cua_nguoi_khac()),
                      ky_vong = "định danh phải lấy từ token, không từ body")

    TRA VE cases
```

---

## G5 — Sinh case lược đồ

```
HAM SinhCaseLuocDo(mo_hinh)
    S     ← mo_hinh.lươc_do_response
    cases ← []

    cases += Case("response thành công khớp lược đồ", request_hop_le(),
                  assert = khop_luoc_do(S.thanh_cong))

    cases += Case("response lỗi khớp lược đồ", request_khong_hop_le(),
                  assert = khop_luoc_do(S.loi))

    cases += Case("Content-Type là application/json", request_hop_le(),
                  assert = header("Content-Type") chứa "application/json")

    VOI MOI truong f TRONG S.thanh_cong.properties:
        cases += Case("kiểu của " + f + " đúng", request_hop_le(),
                      assert = kieu_cua(f) = S.thanh_cong.properties[f].type)
        // Trường tiền trả về dạng chuỗi thay vì số là lỗi kinh điển: client sẽ
        // NỐI CHUỖI thay vì cộng số.

    // ── Chiều NGƯỢC LẠI — phần hay bị bỏ quên nhất ────────────────────
    cases += Case("KHÔNG có trường ngoài hợp đồng", request_hop_le(),
                  assert = khoa(response) ⊆ khoa(S.thanh_cong.properties))
    // Kiểm tra lược đồ chỉ theo chiều "có đủ trường mong đợi" sẽ không bao giờ
    // phát hiện `SELECT *` vô tình làm rò rỉ cột nhạy cảm. Chính chiều này tìm
    // ra BUG-A1-02 (lộ password và reset_token).

    VOI MOI truong f TRONG S.truong_cam:
        cases += Case("không rò rỉ " + f, request_hop_le(),
                      assert = f KHÔNG THUỘC khoa(response))

    TRA VE cases
```

---

## G6a — Kiểm tra IR

```
HAM KiemTraIR(ir)
    VOI MOI case c TRONG ir:

        KHANG_DINH c.id là duy nhất
        KHANG_DINH c.expected_by_spec khác rỗng
            // Chặn "kỳ vọng neo theo hành vi quan sát được".
        KHANG_DINH c.source THUỘC {"AI", "HUMAN"}
        KHANG_DINH c.audit.label THUỘC {"VALID", "INVALID", "INCOMPLETE"}
        KHANG_DINH c.audit.reason khác rỗng

        // Chặn khiếm khuyết harness đã gặp thật (xem DESIGN.md §5.1)
        VOI MOI assertion a TRONG c.expect.assert:
            NEU a.loai = "exec" VA a.ma CHỨA "pm.sendRequest":
                KHANG_DINH a.ma CHỨA "catch (e) { done(e); }"
                    NGUOC_LAI → LOI("assertion bất đồng bộ không bọc try/catch: " +
                                    "khi FAIL, done() không bao giờ được gọi và " +
                                    "Newman sẽ ÂM THẦM bỏ qua test này")

        // Chặn tác dụng phụ đặt trong pre-request (xem DESIGN.md §5.2)
        NEU c.preScript CHỨA "pm.sendRequest" VA c.preScript ghi biến dùng cho assertion:
            CANH_BAO("nên tách thành request [SETUP] tường minh")

    // Kiểm tra tính đầy đủ theo danh mục quy tắc
    VOI MOI tham_so p TRONG mo_hinh.tham_so:
        VOI MOI phan_vung_bat_buoc pv TRONG danh_muc_cho(p):
            KHANG_DINH tồn tại c TRONG ir với c.param = p VA c.partition = pv
                NGUOC_LAI → LOI("thiếu phân vùng bắt buộc: " + p + " / " + pv)
```

---

## G6b — Audit của con người (thủ công)

```
THU_TUC ChoConNguoiAudit(ir)          // ← KHÔNG tự động hoá được

    VOI MOI case c TRONG ir với c.source = "AI":

        // Câu hỏi 1 — kỳ vọng lấy từ ĐẶC TẢ hay từ HÀNH VI?
        NEU c.expected_by_spec chỉ mô tả lại hành vi hiện tại của hệ thống:
            c.audit ← {label: "INVALID", reason: "kỳ vọng neo theo hành vi, không theo đặc tả"}
            sửa lại kỳ vọng theo đúng tài liệu

        // Câu hỏi 2 — kỳ vọng có QUÁ CHẶT so với điều đặc tả thật sự nói?
        NEU đặc tả im lặng về điểm này NHƯNG c ràng buộc một hành vi cụ thể:
            c.audit ← {label: "INCOMPLETE", reason: "đặc tả không quy định — nới kỳ vọng"}
            nới thành: "không được 5xx" HOẶC liệt kê các status chấp nhận được

        // Câu hỏi 3 — case này có phân loại đúng kỹ thuật không?
        NEU c.technique không khớp với thứ mà case thực sự kiểm:
            c.audit ← {label: "INCOMPLETE", reason: "phân loại sai kỹ thuật"}

        NGUOC_LAI:
            c.audit ← {label: "VALID", reason: <trích dẫn điều khoản đặc tả tương ứng>}

    // Bước MỞ RỘNG — phần chỉ con người làm được
    VOI MOI cau_hoi TRONG [
        "Nếu client chỉ gửi MỘT PHẦN dữ liệu thì sao?",
        "VỊ TRÍ của phần tử lỗi có làm thay đổi kết luận không?",
        "Báo cáo trả về có NHẤT QUÁN với trạng thái thật của cơ sở dữ liệu không?",
        "Có BẤT BIẾN nghiệp vụ nào bắt được mọi cách tính sai không?",
        "Hậu quả nghiệp vụ THẬT SỰ của lỗi này là gì?",
        "Ngữ nghĩa của NGÔN NGỮ CÀI ĐẶT có tạo khe hở nào không?"
    ]:
        ir += case_do_con_nguoi_viet(cau_hoi)      // source = "HUMAN"

    TRA VE ir
```

---

## G6c — Biên dịch

```
HAM BienDich(ir)
    collection ← Collection_v2_1(
        pre_request_cap_collection = [
            gan_header("X-Student-Id", studentId),
            console_log(...)                  // bằng chứng bắt buộc theo §11 của đề bài
        ],
        test_cap_collection = [
            khang_dinh_co_header_X_Student_Id(),
            khang_dinh_khong_ro_ri_stack_trace()
            // Chính assertion này bắt được BUG-A3-09 — một lỗi mà không test case
            // riêng lẻ nào nhắm tới.
        ])

    VOI MOI case c TRONG ir:
        collection.them(Request(
            url        = c.request.path,
            method     = c.request.method,
            body       = c.request.body,
            tests      = [DichAssertion(a) VOI MOI a TRONG c.expect.assert],
            mo_ta      = c.expected_by_spec + " | nguồn: " + c.source +
                         " | audit: " + c.audit.label
        ))

    TRA VE {
        collection : collection,
        excel      : XuatBang(ir),
        tom_tat    : TomTat(ir),
        cong_ci    : LocCaseDangDat(ir)     // cổng chặn hồi quy
    }
    // Một nguồn sự thật duy nhất: bốn hiện vật đều sinh từ IR nên số liệu trong
    // báo cáo không thể lệch với collection.
```

---

## Độ phức tạp

Với một endpoint có `p` tham số, `c` ràng buộc mỗi tham số, và máy trạng thái `s` trạng thái:

| Giai đoạn | Số case sinh ra |
|---|---|
| G2 phân vùng miền | `O(p × (k + 6c))` với `k` ≈ 8 phân vùng phổ quát/theo kiểu |
| G3 chuyển trạng thái | `O(s²)` — mọi cặp (từ, đến) |
| G4 bảo mật | `O(p + |SEC|)` |
| G5 lược đồ | `O(|trường response|)` |

Với API-2 (FR-09): `p = 3`, `c ≈ 2`, `s = 3` → khoảng 39 case do máy sinh, khớp với con số thực tế.
