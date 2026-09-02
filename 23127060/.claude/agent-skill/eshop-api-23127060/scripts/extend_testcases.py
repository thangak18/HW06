#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extend_testcases.py - Bổ sung test case do NGƯỜI viết, những case bộ sinh AI đã bỏ sót.

  python3 extend_testcases.py            # sinh testcases/API-*_final.csv tu *_audited.csv

Đề bài mục 6.3: "Add at least five test cases of your own that the AI missed - especially
around security and state transitions - and explain why the AI missed them (prompt quality,
model limitations, or characteristics of the API)."

Bốn lý do AI bỏ sót (mỗi case phải chọn đúng 1):
  PROMPT   Prompt không yêu cầu rõ điều đó.
  MODEL    AI suy diễn từ tên/hình dạng API thay vì đọc mã nguồn.
  API      Bug chỉ lộ ra khi KẾT HỢP NHIỀU REQUEST; bộ sinh làm việc trên từng case độc lập.
  SPECGAP  Đặc tả không mô tả hành vi này nên AI không có gì để bám vào.
"""
import csv
import os

COLS = ["TC_ID","API","FR","Category","Technique","Title","Method","Endpoint","Preconditions",
        "Request_Headers","Request_Body","Expected_Status","Expected_Assertions","Oracle",
        "SEC_Ref","Priority","Source","Audit_Label","Audit_Note","Tag","Bug_Ref","Why_AI_Missed"]

BEARER_U = "Authorization: Bearer {{token_user}}"
BEARER_A = "Authorization: Bearer {{token_attacker}}"

# Mỗi phần tử: dict các cột khác mặc định.
EXTRA = [
# ============================== API-1 — FR-03 ==============================
dict(TC_ID="TC-A1-STA-901", API="API-1", FR="FR-03", Category="STA", Technique="State Transition",
     Title="Sau khi reset, mat khau CU phai het hieu luc va mat khau MOI phai dang nhap duoc",
     Method="POST", Endpoint="/api/login",
     Preconditions="Da chay xong chuoi: forgot-password -> reset-password voi newPassword = NewApi1234!",
     Request_Headers="-", Request_Body='{"email":"api.victim.23127060@test.local","password":"Api1234!"}',
     Expected_Status="401",
     Expected_Assertions="login bang mat khau CU tra 401; ngay sau do login bang mat khau MOI tra 200 kem token",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@contract", Bug_Ref="-",
     Why_AI_Missed="API - Bo sinh chi kiem RESPONSE cua reset-password ('Password reset successfully') roi dung lai. "
       "Nhung cau tra loi do khong chung minh mat khau da thuc su doi: SUT co the tra 200 ma khong ghi gi (chinh la "
       "kieu loi C-07/C-08 o API-3). Chi mot chuoi 3 request - reset, login mat khau cu, login mat khau moi - moi "
       "chung minh duoc. Bo sinh lam viec tren tung case doc lap nen khong the tu dung chuoi nay."),

dict(TC_ID="TC-A1-SEC-901", API="API-1", FR="FR-03", Category="SEC", Technique="Broken Access Control",
     Title="[-] Dat lai mat khau thanh cong nhung tai khoan van bi khoa",
     Method="POST", Endpoint="/api/login",
     Preconditions="Tai khoan da bi khoa do dang nhap sai; sau do da reset mat khau thanh cong bang OTP",
     Request_Headers="-", Request_Body='{"email":"api.victim.23127060@test.local","password":"NewApi1234!"}',
     Expected_Status="200",
     Expected_Assertions="dang nhap thanh cong bang mat khau moi; login_attempts phai ve 0 va locked_until phai duoc xoa sau khi reset",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="A-06",
     Why_AI_Missed="API - Bug nam o CHO GIAO NHAU giua hai chuc nang: FR-02 (khoa tai khoan) va FR-03 (dat lai mat "
       "khau). Cau lenh UPDATE trong reset-password chi dat lai password va reset_token, khong dong toi login_attempts "
       "va locked_until. Bo sinh chi doc dac ta cua FR-03 nen khong the biet FR-02 co de lai trang thai gi. Can 5 "
       "request lien tiep (2 lan login sai, forgot, reset, login) moi tai hien duoc."),

dict(TC_ID="TC-A1-SEC-902", API="API-1", FR="FR-03", Category="SEC", Technique="Information Disclosure",
     Title="[SEC-01] GET /api/users/me tra ve ca password lan reset_token",
     Method="GET", Endpoint="/api/users/me",
     Preconditions="Da login, co {{token_user}}",
     Request_Headers=BEARER_U, Request_Body="-", Expected_Status="200",
     Expected_Assertions="body KHONG duoc chua truong password; KHONG duoc chua truong reset_token; "
       "neu password xuat hien dung nguyen van chuoi da gui khi dang ky thi da chung minh vi pham SEC-01",
     Oracle="SPEC", SEC_Ref="SEC-01", Priority="P0", Tag="@bug", Bug_Ref="A-07",
     Why_AI_Missed="PROMPT - Prompt khoanh vung API-1 vao dung hai endpoint forgot-password va reset-password. "
       "Nhung noi ro ri nghiem trong nhat lai la GET /api/users/me: no lam `SELECT * FROM users` roi tra thang ca "
       "ban ghi, ke ca cot reset_token dang con hieu luc. Ke tan cong doc duoc OTP cua chinh minh la vo hai, nhung "
       "no chung minh cot nay chua bao gio duoc coi la bi mat. Bo sinh khong duoc phep buoc ra ngoai pham vi prompt."),

dict(TC_ID="TC-A1-SEC-903", API="API-1", FR="FR-03", Category="SEC", Technique="Boundary / Error Guessing",
     Title="[-] Tai khoan bi khoa ngay sau HAI lan dang nhap sai, trong khi SRS quy dinh ba lan",
     Method="POST", Endpoint="/api/login",
     Preconditions="Tai khoan api.victim vua duoc seed lai, login_attempts = 0. Da goi login sai DUNG HAI lan truoc do",
     Request_Headers="-", Request_Body='{"email":"api.victim.23127060@test.local","password":"Api1234!"}',
     Expected_Status="200",
     Expected_Assertions="sau DUNG hai lan sai, dang nhap bang mat khau DUNG van phai thanh cong (SRS FR-02: chi khoa tu lan sai thu ba)",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="A-09",
     Why_AI_Missed="MODEL - SRS viet 'sai tu 3 lan tro len thi khoa', va bo sinh sinh dung case do: sai 3 lan roi kiem "
       "da khoa chua. Case do PASS, vi sai 3 lan thi qua nhien la khoa. Bug nam o phia con lai cua bien: code cong "
       "+2 moi lan sai nen mo khoa ngay o lan thu HAI. Muon thay phai kiem canh 'chua duoc khoa' chu khong phai canh "
       "'da bi khoa' - AI mac dinh viet case khang dinh dieu dac ta noi, chu khong viet case phu dinh dieu dac ta khong noi."),

dict(TC_ID="TC-A1-SEC-904", API="API-1", FR="FR-03", Category="SEC", Technique="Privilege Escalation",
     Title="[SEC-03] User thuong doc duoc toan bo bang users qua GET /api/admin/users",
     Method="GET", Endpoint="/api/admin/users",
     Preconditions="Da login bang tai khoan thuong api.victim, co {{token_user}}",
     Request_Headers=BEARER_U, Request_Body="-", Expected_Status="403",
     Expected_Assertions="token hop le nhung role = 'user' thi phai bi tu choi 403; khong duoc tra ve danh sach email cua nguoi khac",
     Oracle="SPEC", SEC_Ref="SEC-03", Priority="P0", Tag="@bug", Bug_Ref="X-01",
     Why_AI_Missed="PROMPT - API-1 khong co endpoint admin nao nen bo sinh khong sinh case SEC-03. Nhung luong quen "
       "mat khau van co the bi khai thac qua duong nay: GET /api/admin/users tra ve ca login_attempts va locked_until "
       "cua moi nguoi, cho phep do xem tai khoan nao dang bi khoa. Do phu SEC-03 cua API-1 truoc do la 0 - day la "
       "case lam day khoang trong do bang mot kich ban co that."),

dict(TC_ID="TC-A1-SEC-905", API="API-1", FR="FR-03", Category="SEC", Technique="Error Guessing",
     Title="[SEC-07] OTP cua nguoi nay dung duoc cho email cua nguoi kia neu trung gia tri",
     Method="POST", Endpoint="/api/reset-password",
     Preconditions="Ca hai tai khoan victim va attacker deu da goi forgot-password. Ghi lai OTP cua attacker",
     Request_Headers="-",
     Request_Body='{"email":"api.victim.23127060@test.local","resetToken":"{{attackerResetToken}}","newPassword":"Hacked123!"}',
     Expected_Status="400",
     Expected_Assertions="OTP cua tai khoan khac phai bi tu choi; mat khau cua victim KHONG duoc doi; "
       "voi khong gian chi 9000 gia tri, xac suat hai OTP trung nhau la dang ke nen dieu kien AND email + token la khong du",
     Oracle="SPEC", SEC_Ref="SEC-07", Priority="P0", Tag="@contract", Bug_Ref="A-02",
     Why_AI_Missed="SPECGAP - Dac ta chi noi 'OTP chi hop le cho email da yeu cau', va cau UPDATE cua SUT co ca hai "
       "dieu kien WHERE email = ? AND reset_token = ? nen thoat nhin la dung. Cai dac ta KHONG noi la khong gian OTP "
       "phai du lon de hai nguoi khong trung ma. Voi 4 chu so, chi can 100 nguoi cung dang cho reset la kha nang trung "
       "vuot 40%. AI khong co cau nao trong dac ta de bam vao nen khong sinh case nay."),

# ============================== API-2 — FR-08 ==============================
dict(TC_ID="TC-B2-DOM-901", API="API-2", FR="FR-08", Category="DOM", Technique="Error Guessing",
     Title="Checkout voi total_amount = 1 roi doc lai don hang de xac nhan so tien that su duoc luu",
     Method="GET", Endpoint="/api/orders/{{orderId}}",
     Preconditions="Gio hang co 1 san pham gia 30.000.000d. Da goi POST /api/checkout voi total_amount = 1",
     Request_Headers=BEARER_U, Request_Body="-", Expected_Status="200",
     Expected_Assertions="total_amount cua don hang phai bang tong tinh tu gio hang (30000000), KHONG duoc bang 1; "
       "SRS FR-08: 'Backend phai tu tinh lai tong tien; khong chap nhan gia tri total_amount do client gui len'",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="B-01",
     Why_AI_Missed="API - Bo sinh co case 'total_amount = 1 phai bi tu choi' nhung chi kiem ma tra ve cua chinh "
       "request checkout. SUT tra 200 nen case do da 'phat hien' duoc bug, dung. Nhung no khong do duoc MUC DO thiet "
       "hai. Chi khi doc lai don hang moi thay so 1 that su nam trong CSDL - tuc la mua duoc dien thoai 30 trieu voi "
       "gia 1 dong. Bang chung nay can request thu hai, ma bo sinh chi lam viec tren tung request doc lap."),

dict(TC_ID="TC-B2-DOM-902", API="API-2", FR="FR-08", Category="DOM", Technique="Error Guessing",
     Title="Sau khi thanh toan thanh cong, gio hang phai duoc xoa",
     Method="GET", Endpoint="/api/cart",
     Preconditions="Da them san pham vao gio va goi POST /api/checkout thanh cong",
     Request_Headers=BEARER_U, Request_Body="-", Expected_Status="200",
     Expected_Assertions="gio hang phai la mang rong sau checkout (SRS FR-08: 'Sau thanh toan thanh cong, gio hang duoc xoa')",
     Oracle="SPEC", SEC_Ref="-", Priority="P1", Tag="@bug", Bug_Ref="B-13",
     Why_AI_Missed="PROMPT - Prompt khoanh API-2 vao POST /api/checkout. Nhung mot yeu cau cua FR-08 lai duoc kiem "
       "o mot endpoint KHAC han (GET /api/cart). Bo sinh phan hoach theo endpoint nen khong co cho nao de dat case "
       "'hau qua cua checkout len gio hang'. Day la gioi han cua cach to chuc spec theo endpoint thay vi theo yeu cau."),

dict(TC_ID="TC-B2-STA-901", API="API-2", FR="FR-08", Category="STA", Technique="State Transition (chuoi day du)",
     Title="Chuoi day du pending -> confirmed -> shipping roi USER tu huy: buoc cuoi phai bi chan",
     Method="PUT", Endpoint="/api/orders/{{orderId}}/cancel",
     Preconditions="Don da di het chuoi: tao moi (pending) -> admin confirm -> admin chuyen shipping",
     Request_Headers=BEARER_U, Request_Body="{}", Expected_Status="400",
     Expected_Assertions="phai tra 400; trang thai don van phai la 'shipping' sau khi goi; "
       "SRS FR-10: 'Khi don hang da o trang thai shipping, User khong duoc phep tu huy'",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="B-09",
     Why_AI_Missed="API - Bo sinh phu bang chuyen trang thai theo tung O RIENG LE (0-switch): moi case dat don vao "
       "mot trang thai roi thu mot buoc chuyen. Nhung dua don ve trang thai 'shipping' doi hoi di qua DUNG hai buoc "
       "admin truoc do - mot chuoi 4 request. Muon phu day du phai chuyen sang 1-switch/n-switch coverage, la thu "
       "phai thiet ke tay chu bo sinh khong tu suy ra duoc tu bang trang thai."),

dict(TC_ID="TC-B2-STA-902", API="API-2", FR="FR-08", Category="STA", Technique="State Transition (o tu chuyen)",
     Title="Chuyen tu pending sang chinh pending phai bi tu choi",
     Method="PUT", Endpoint="/api/admin/orders/{{orderId}}/status",
     Preconditions="Don dang o trang thai pending",
     Request_Headers=BEARER_A, Request_Body='{"status":"pending"}', Expected_Status="400",
     Expected_Assertions="body.error chua 'Invalid state transition'; trang thai KHONG doi; "
       "so do FR-10 khong co mui ten nao tu mot trang thai ve chinh no",
     Oracle="SPEC", SEC_Ref="-", Priority="P1", Tag="@contract", Bug_Ref="-",
     Why_AI_Missed="MODEL - Bang chuyen trang thai trong spec liet ke cac cap (from, to) KHAC nhau; 5 o duong cheo "
       "(pending->pending, confirmed->confirmed, ...) bi bo trong vi truc quan chung 'khong phai mot buoc chuyen'. "
       "Do phu STA cua API-2 vi the dung o 20/25. Day dung la loai o hay bi bo sot trong thuc te, va cung la loai o "
       "hay gay loi that (mot request bi gui lai hai lan)."),

dict(TC_ID="TC-B2-SEC-901", API="API-2", FR="FR-08", Category="SEC", Technique="Business Logic Abuse (data-driven)",
     Title="[SEC-02] Bo user_id khoi apply-coupon de dung ma VIP100 qua muc 2 lan cho phep",
     Method="POST", Endpoint="/api/apply-coupon",
     Preconditions="Coupon VIP100 co max_uses_per_user = 2. Chay Collection Runner 3 vong voi data file coupon_abuse.csv",
     Request_Headers="-", Request_Body='{"code":"VIP100","total_amount":500000}',
     Expected_Status="401",
     Expected_Assertions="apply-coupon phai yeu cau JWT va lay user tu token (SRS FR-09 dieu kien C4); "
       "khong duoc lay user_id tu body; vong thu 3 phai bi tu choi vi da het luot",
     Oracle="SPEC", SEC_Ref="SEC-02", Priority="P0", Tag="@bug", Bug_Ref="B-07",
     Why_AI_Missed="MODEL - Bo sinh coi 'thieu tham so bat buoc' la mot lop khong hop le, nen sinh case "
       "'thieu user_id -> phai tra 400/401'. No khong nhan ra rang trong code, THIEU tham so nay lai la duong "
       "vong qua toan bo kiem tra han muc: nhanh `if (user_id)` bi bo qua han. Day la nghich ly 'bo bot du lieu de "
       "duoc nhieu quyen hon', chi thay duoc khi doc ma nguon chu khong suy ra tu hinh dang API."),

dict(TC_ID="TC-B2-SEC-902", API="API-2", FR="FR-08", Category="SEC", Technique="Data Integrity",
     Title="[-] POST /api/coupon-usage ghi nhan luot dung cho mot coupon_id khong ton tai",
     Method="POST", Endpoint="/api/coupon-usage",
     Preconditions="Da login, co {{token_user}}",
     Request_Headers=BEARER_U, Request_Body='{"coupon_id":999999}', Expected_Status="400",
     Expected_Assertions="phai tu choi coupon_id khong ton tai; bang coupon_usage KHONG duoc phat sinh ban ghi rac; "
       "ban ghi rac se lam sai phep dem han muc su dung cua FR-09 dieu kien C5",
     Oracle="SPEC", SEC_Ref="-", Priority="P1", Tag="@bug", Bug_Ref="B-11",
     Why_AI_Missed="SPECGAP - api_specification.md khong he liet ke endpoint POST /api/coupon-usage; no chi xuat hien "
       "trong server.js voi mot dong comment. Bo sinh doc dac ta nen khong biet endpoint nay ton tai. Day la loi "
       "'endpoint khong duoc tai lieu hoa' - loai be mat tan cong ma kiem thu dua tren dac ta khong bao gio cham toi."),

# ============================== API-3 — FR-15 ==============================
dict(TC_ID="TC-C3-SCH-901", API="API-3", FR="FR-15", Category="SCH", Technique="Cross-request Type Consistency",
     Title="Kieu cua truong price phai giong nhau giua san pham id le va id chan",
     Method="GET", Endpoint="/api/products/2",
     Preconditions="Da goi GET /api/products/1 truoc do va luu lai kieu cua truong price",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="typeof price cua id=2 phai bang typeof price cua id=1; ca hai deu phai la number; "
       "GET /api/products (danh sach) cung phai tra price kieu number cho MOI phan tu",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="C-05",
     Why_AI_Missed="API - Moi request rieng le deu hop le: `{\"price\": 30000000}` dung schema, va "
       "`{\"price\": \"28000000\"}` cung la mot JSON hop le. Vi pham chi hien ra khi SO SANH hai response voi nhau. "
       "Bo sinh danh gia tung case doc lap nen khong co cho nao de dat mot khang dinh bac cao hon lien ket hai request. "
       "Neu chi test id le (nhu vi du trong tai lieu hay dung) thi khong bao gio thay bug nay."),

dict(TC_ID="TC-C3-SEC-901", API="API-3", FR="FR-15", Category="SEC", Technique="Destructive Test",
     Title="[SEC-02] Khach vang lai xoa duoc toan bo catalog roi kiem so san pham con lai",
     Method="GET", Endpoint="/api/products",
     Preconditions="Da goi DELETE /api/products/:id cho ca 5 san pham seed MA KHONG kem header Authorization",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="danh sach san pham phai con nguyen 5 phan tu vi cac lenh DELETE khong token dang le phai bi tu choi 401; "
       "neu danh sach rong thi mot nguoi khong dang nhap da xoa sach catalog",
     Oracle="SPEC", SEC_Ref="SEC-02", Priority="P0", Tag="@bug", Bug_Ref="C-01",
     Why_AI_Missed="API - Bo sinh co case 'DELETE khong token -> phai 401', va case do da bat duoc bug. Nhung mot "
       "dong 'expected 401, got 200' trong bao cao khong noi len duoc muc do. Case nay do HAU QUA: sau 5 request "
       "khong xac thuc thi cua hang khong con san pham nao de ban. Cung mot bug, nhung bang chung nay moi du suc "
       "thuyet phuc nguoi ra quyet dinh. Can chuoi 6 request."),

dict(TC_ID="TC-C3-DOM-901", API="API-3", FR="FR-15", Category="DOM", Technique="Partial Update",
     Title="PUT chi gui truong name: cac truong khong gui KHONG duoc bi ghi de thanh null",
     Method="GET", Endpoint="/api/products/{{newProductId}}",
     Preconditions="Da tao san pham day du 5 truong, sau do goi PUT chi voi {\"name\": \"Ten moi 23127060\"}",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="name phai la ten moi; NHUNG price, description, imageUrl, category_id phai giu nguyen gia tri cu, "
       "KHONG duoc bien thanh null; SRS FR-15: 'Khi Sua mot san pham, chi san pham do bi thay doi'",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="C-09",
     Why_AI_Missed="API - Bo sinh phu tung tham so cua PUT mot cach doc lap: gui name sai, gui price sai... Moi case "
       "deu gui DU 5 truong roi doi mot truong. Khong case nao gui THIEU truong, vi 'thieu truong' duoc coi la lop "
       "khong hop le cua chinh truong do chu khong phai mot phep thu ve hanh vi cap nhat mot phan. Can chuoi POST -> "
       "PUT -> GET moi thay duoc 4 truong con lai da bi xoa trang."),

dict(TC_ID="TC-C3-SCH-902", API="API-3", FR="FR-15", Category="SCH", Technique="Content Negotiation",
     Title="Response loi phai la application/json, khong duoc la HTML",
     Method="GET", Endpoint="/api/products?search=%27",
     Preconditions="SUT da seed",
     Request_Headers="-", Request_Body="-", Expected_Status="400",
     Expected_Assertions="header Content-Type phai chua 'application/json'; body phai parse duoc thanh JSON co truong error; "
       "body KHONG duoc chua the HTML nao (<h1>, <p>); khong duoc lo thong diep loi cua tang CSDL",
     Oracle="SPEC", SEC_Ref="-", Priority="P0", Tag="@bug", Bug_Ref="C-03",
     Why_AI_Missed="MODEL - Bo sinh mac dinh moi response cua mot REST API deu la JSON, nen no khang dinh len NOI DUNG "
       "body ma khong bao gio khang dinh len HEADER Content-Type. Khi SUT tra ve HTML, buoc pm.response.json() nem "
       "loi va test that bai voi thong bao 'Unexpected token <' - mot loi trong dan den chan doan sai la 'test bi hong' "
       "chu khong phai 'API vi pham hop dong'. Phai kiem Content-Type TRUOC khi parse."),

dict(TC_ID="TC-C3-DOM-902", API="API-3", FR="FR-15", Category="DOM", Technique="Referential Integrity",
     Title="Tao san pham voi category_id khong ton tai roi doi chieu voi danh sach danh muc",
     Method="GET", Endpoint="/api/categories",
     Preconditions="Da goi POST /api/products voi category_id = 9999",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="danh sach danh muc chi co id 1, 2, 3; san pham vua tao tro toi category_id = 9999 la mot "
       "tham chieu treo; SRS FR-15: 'Danh muc: bat buoc, phai chon tu danh sach co san'",
     Oracle="SPEC", SEC_Ref="-", Priority="P1", Tag="@bug", Bug_Ref="C-10",
     Why_AI_Missed="API - Bo sinh co case 'category_id = 9999 phai bi tu choi'. Nhung de CHUNG MINH day la tham chieu "
       "treo chu khong phai mot danh muc that ma minh khong biet, phai doc bang categories bang mot request thu hai. "
       "Rang buoc toan ven tham chieu ve ban chat noi ve QUAN HE giua hai tai nguyen, khong the kiem trong pham vi "
       "mot request."),

dict(TC_ID="TC-C3-SEC-902", API="API-3", FR="FR-15", Category="SEC", Technique="SQL Injection (data exfiltration)",
     Title="[SEC-05] UNION SELECT qua ?search doc duoc mat khau plaintext trong bang users",
     Method="GET", Endpoint="/api/products?search=%25%27%20UNION%20SELECT%20id%2Cemail%2Cpassword%2Crole%2C1%20FROM%20users--%20",
     Preconditions="SUT da seed; bang users co admin@eshop.com",
     Request_Headers="-", Request_Body="-", Expected_Status="200",
     Expected_Assertions="ket qua tra ve chi duoc chua san pham, KHONG duoc chua chuoi '@eshop.com' hay 'Admin123!'; "
       "so cot cua products (5) trung voi so cot chon tu users nen UNION ghep duoc - day la dieu Parameterized Query "
       "(SEC-05) ngan chan",
     Oracle="SPEC", SEC_Ref="SEC-05", Priority="P0", Tag="@bug", Bug_Ref="C-02",
     Why_AI_Missed="API - Bo sinh co payload UNION SELECT nhung viet chung chung voi 5 cot tuy y. UNION trong SQLite "
       "chi chay khi SO COT KHOP CHINH XAC; doan sai so cot thi chi nhan duoc loi va ket luan nham la 'da duoc bao ve'. "
       "Phai doc database.js dem dung 5 cot cua bang products roi chon dung 5 cot tu users. Do la buoc trinh sat lay "
       "tu MA NGUON, khong the suy ra tu dac ta."),
]

DEFAULTS = dict(Source="HUMAN", Audit_Label="VALID",
                Audit_Note="Case do sinh vien tu viet sau khi doc ma nguon SUT; khong qua bo sinh tu dong.")


def main():
    add = {1: [], 2: [], 3: []}
    for e in EXTRA:
        n = int(e["API"].split("-")[1])
        row = {c: "-" for c in COLS}
        row.update(DEFAULTS)
        row.update(e)
        add[n].append(row)

    for n in (1, 2, 3):
        src = "testcases/API-%d_audited.csv" % n
        dst = "testcases/API-%d_final.csv" % n
        with open(src, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        rows += add[n]
        with open(dst, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            w.writerows(rows)
        h = sum(1 for r in rows if r["Source"] == "HUMAN")
        print("API-%d: %s -> %s | tong %d case (AI %d + HUMAN %d)"
              % (n, src, dst, len(rows), len(rows) - h, h))


if __name__ == "__main__":
    main()
