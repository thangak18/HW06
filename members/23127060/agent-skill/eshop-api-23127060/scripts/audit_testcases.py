#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_testcases.py - Gan nhan VALID / INVALID / INCOMPLETE cho test case do AI sinh.

  python3 audit_testcases.py --in testcases/API-1_generated.csv --out testcases/API-1_audited.csv
  python3 audit_testcases.py --report          # in bang thong ke cho ca 3 API

De bai muc 6.2 doi: "Label each AI-generated test case VALID / INVALID / INCOMPLETE with
reasoning, and correct the invalid or incomplete ones."

Vi sao dung script thay vi sua tay tung dong:
  225 test case sua tay thi khong the tai lap va khong the kiem chung. O day moi nhan deu
  den tu mot LUAT viet ro rang, bam vao mot cau cu the trong eshop-sut/README.md. Ai doc
  file nay cung kiem tra duoc luat co dung khong, va chay lai cho ra dung ket qua do.
  Phan doi hoi phan doan rieng cho tung case (chu yeu la gan lai ma SEC) nam trong bang
  OVERRIDES ben duoi, moi dong deu kem ly do.

Nhan:
  VALID      buoc, du lieu, ky vong deu dung so voi SRS; chay duoc ngay.
  INVALID    ky vong sai / khong co can cu trong SRS / tham so bia / mau thuan noi tai.
             BAT BUOC sua roi ghi ro da sua gi.
  INCOMPLETE y tuong dung nhung thieu assertion, thieu precondition, hoac oracle chua ro.
             BAT BUOC bo sung.
"""
import argparse
import csv
import os
import re
from collections import Counter, defaultdict

COLUMNS = None  # lay tu file dau vao

# ---------------------------------------------------------------------------
# BANG 1 — Gan lai ma SEC.
#
# Toan bo cot SEC_Ref do AI sinh deu bam theo mot bang SEC SUY DIEN THEO OWASP
# (SEC-01=SQLi, SEC-04=IDOR, SEC-05=role escalation, SEC-07=brute force).
# Bang SEC THAT nam o eshop-sut/README.md muc 9 va khac han:
#
#   SEC-01 Mat khau khong duoc luu plaintext
#   SEC-02 API co tinh bao mat phai yeu cau JWT hop le
#   SEC-03 API Admin phai kiem role='admin', khong chi kiem token ton tai
#   SEC-04 Du lieu user nhap phai duoc escape khi hien thi (stored XSS)
#   SEC-05 Truy van CSDL phai dung Parameterized Query
#   SEC-06 API cap nhat ho so khong duoc cho doi truong role tu client
#   SEC-07 OTP reset phai >= 6 chu so, co thoi han, vo hieu hoa sau khi dung
#
# Vi vay gan nhu moi case SEC deu bi gan sai ma. Day khong phai loi vat: cot SEC_Ref la
# thu duy nhat chung minh do phu bao mat trong bao cao, gan sai la bao cao sai.
# ---------------------------------------------------------------------------
SEC_REMAP = {
    # --- API-1 ---
    "TC-A1-SEC-001": ("SEC-05", "SQLi la vi pham SEC-05 (parameterized query), khong phai SEC-01 (luu mat khau plaintext)."),
    "TC-A1-SEC-002": ("SEC-05", "Nhu tren: SQLi thuoc SEC-05."),
    "TC-A1-SEC-003": ("SEC-07", "Tra thang OTP ra response la loi vong doi OTP -> SEC-07, khong phai SEC-02 (yeu cau JWT)."),
    "TC-A1-SEC-004": ("-", "User enumeration KHONG duoc bat ky ma SEC-01..07 nao phu. Van la test hop le nhung phai de SEC_Ref = '-' thay vi gan bua."),
    "TC-A1-SEC-005": ("SEC-01", "Response login lo truong password chinh la bang chung mat khau duoc luu plaintext -> dung SEC-01."),
    "TC-A1-SEC-006": ("SEC-07", "Reset phai doi OTP hop le -> thuoc vong doi OTP SEC-07, khong phai SEC-03 (kiem role admin)."),
    "TC-A1-SEC-007": ("SEC-07", "'OTP chi hop le cho email da yeu cau' la yeu cau cua SEC-07 + FR-03, khong phai SEC-04 (escape XSS)."),
    "TC-A1-SEC-008": ("SEC-06", "Gui kem truong role dung la SEC-06; SEC-05 la parameterized query."),
    "TC-A1-SEC-009": ("SEC-04", "Payload XSS thuoc SEC-04; SEC-06 chi noi rieng ve truong role."),
    "TC-A1-SEC-010": ("SEC-04", "Nhu tren."),
    "TC-A1-SEC-011": ("SEC-07", "Do token thuoc SEC-07 (entropy OTP) - ma dung, nhung ky vong 429 sai, xem luat R1."),
    "TC-A1-SEC-012": ("-", "Khoa tai khoan sau 3 lan sai la FR-02, khong nam trong SEC-01..07."),
    "TC-A1-SEC-013": ("SEC-07", "Ma dung nhung noi dung case sai, xem luat R1."),
    # --- API-2 ---
    "TC-B2-SEC-001": ("SEC-05", "SQLi -> SEC-05."),
    "TC-B2-SEC-002": ("-", "Khong lo stack trace khong duoc SEC-01..07 phu."),
    "TC-B2-SEC-003": ("SEC-02", "Thieu JWT -> SEC-02; SEC-03 danh rieng cho viec kiem role."),
    "TC-B2-SEC-004": ("SEC-02", "Nhu tren."),
    "TC-B2-SEC-005": ("SEC-02", "Token sai chu ky = token khong hop le -> SEC-02."),
    "TC-B2-SEC-006": ("SEC-02", "GET /api/orders/:id thieu han middleware xac thuc -> vi pham SEC-02. SEC-04 la escape XSS."),
    "TC-B2-SEC-007": ("SEC-02", "Nhu tren."),
    "TC-B2-SEC-008": ("SEC-02", "Nhu tren."),
    "TC-B2-SEC-009": ("SEC-03", "User thuong goi API admin -> dung SEC-03; SEC-05 la parameterized query."),
    "TC-B2-SEC-010": ("SEC-03", "Nhu tren."),
    "TC-B2-SEC-011": ("SEC-04", "XSS -> SEC-04."),
    "TC-B2-SEC-012": ("-", "Mass assignment truong 'status' khong phai 'role' nen khong thuoc SEC-06; day la yeu cau FR-08/FR-10."),
    "TC-B2-SEC-013": ("-", "Han muc su dung coupon la FR-09 dieu kien C5, khong nam trong SEC-01..07."),
    "TC-B2-SEC-014": ("SEC-06", "Da viet lai thanh chuoi leo thang quyen (xem luat R1)."),
    # --- API-3 ---
    "TC-C3-SEC-001": ("SEC-05", "SQLi -> SEC-05."),
    "TC-C3-SEC-002": ("SEC-05", "Nhu tren."),
    "TC-C3-SEC-003": ("SEC-05", "Tra ve thong diep loi SQL la he qua truc tiep cua viec noi chuoi -> van la SEC-05."),
    "TC-C3-SEC-004": ("-", "Xem luat R5: tham so ?debug=true khong ton tai."),
    "TC-C3-SEC-005": ("SEC-02", "Thieu JWT -> SEC-02."),
    "TC-C3-SEC-006": ("SEC-02", "Nhu tren."),
    "TC-C3-SEC-007": ("SEC-02", "Nhu tren."),
    "TC-C3-SEC-008": ("SEC-02", "Token sai chu ky -> SEC-02."),
    "TC-C3-SEC-009": ("SEC-03", "User thuong sua san pham = thieu kiem role -> SEC-03, khong phai SEC-04."),
    "TC-C3-SEC-010": ("SEC-03", "Dung SEC-03; truoc do gan SEC-05."),
    "TC-C3-SEC-011": ("SEC-03", "Nhu tren."),
    "TC-C3-SEC-012": ("SEC-04", "Stored XSS -> SEC-04."),
    "TC-C3-SEC-013": ("-", "Ghi de khoa chinh 'id' khong phai truong 'role' nen khong thuoc SEC-06."),
    "TC-C3-SEC-014": ("SEC-06", "Da viet lai thanh chuoi leo thang quyen (xem luat R1)."),
}

# --- Cac case NGOAI nhom SEC nhung van bi gan ma SEC theo bang suy dien ---
# Cung mot loi he thong: SQLi bi gan SEC-01, XSS bi gan SEC-06, IDOR bi gan SEC-04,
# leo thang quyen bi gan SEC-05. Chung nam rai rac trong nhom DOM/STA nen de bi bo sot
# hon cac case trong nhom SEC.
SEC_REMAP.update({
    "TC-A1-DOM-013": ("SEC-07", "Dung OTP cua tai khoan khac chinh la dieu SEC-07 + FR-03 quy dinh ('OTP chi hop le cho email da yeu cau'), khong phai SEC-04 (escape XSS)."),
    "TC-A1-DOM-022": ("SEC-05", "SQLi -> SEC-05 (parameterized query), khong phai SEC-01 (luu mat khau plaintext)."),
    "TC-A1-DOM-026": ("-", "Do manh mat khau la yeu cau FR-01/FR-03, khong nam trong SEC-01..07. SEC-06 chi noi rieng ve truong role."),
    "TC-A1-DOM-029": ("-", "Nhu tren: do dai mat khau la FR-01, khong phai ma SEC."),
    "TC-A1-DOM-031": ("-", "Nhu tren: yeu cau co chu hoa la FR-01."),
    "TC-A1-DOM-032": ("-", "Nhu tren: yeu cau co chu so la FR-01."),
    "TC-A1-DOM-033": ("-", "Nhu tren: mat khau yeu vi pham FR-01, khong phai ma SEC."),
    "TC-A1-DOM-034": ("SEC-04", "Payload <script> -> SEC-04 (escape du lieu user nhap)."),
    "TC-B2-DOM-022": ("SEC-04", "Payload <script> trong shipping_address -> SEC-04. SRS FR-18 con noi ro dia chi giao hang phai hien thi an toan."),
    "TC-B2-DOM-031": ("SEC-05", "SQLi -> SEC-05."),
    "TC-B2-DOM-039": ("SEC-02", "Lay user_id tu body thay vi tu JWT la vi pham SEC-02 (API bao mat phai dua tren token hop le), khong phai SEC-04."),
    "TC-B2-STA-020": ("SEC-03", "User thuong tu xac nhan don hang = thao tac admin khong kiem role -> SEC-03, khong phai SEC-05."),
    "TC-C3-DOM-009": ("SEC-04", "Stored XSS qua ten san pham -> SEC-04."),
    "TC-C3-DOM-026": ("SEC-04", "URL scheme javascript: la vector XSS khi render -> SEC-04."),
    "TC-C3-DOM-027": ("-", "Path traversal trong imageUrl khong duoc bat ky ma SEC-01..07 nao phu. Van la test hop le, de SEC_Ref = '-'."),
    "TC-C3-DOM-034": ("SEC-05", "SQLi trong path param -> SEC-05."),
    "TC-C3-DOM-037": ("SEC-04", "Stored XSS qua description -> SEC-04."),
    "TC-C3-DOM-045": ("SEC-05", "Lam vo cau SQL bang mot dau nhay don -> bang chung truc tiep cua viec noi chuoi -> SEC-05."),
    "TC-C3-DOM-046": ("SEC-05", "SQLi -> SEC-05."),
    "TC-C3-DOM-047": ("SEC-05", "SQLi UNION SELECT -> SEC-05."),
    "TC-C3-DOM-048": ("SEC-05", "SQLi stacked query -> SEC-05."),
    "TC-C3-DOM-049": ("SEC-04", "Reflected XSS qua tham so search -> SEC-04."),
})

# ---------------------------------------------------------------------------
# BANG 2 — Cac case phai VIET LAI vi ky vong khong co can cu trong SRS,
# hoac vi tham so / trang thai duoc bia ra.
# Moi muc: (nhan, ly do, cac cot can ghi de)
# ---------------------------------------------------------------------------
REWRITE = {
    # ---- R1: ky vong 429 (rate limiting) ----
    "TC-A1-SEC-011": ("INVALID",
        "R1 - Ky vong 429 khong co can cu: khong mot dong nao trong FR-01..FR-24 hay SEC-01..07 "
        "yeu cau rate limiting. AI suy ra tu thoi quen bao mat chung chu khong tu dac ta. "
        "DA SUA: giu nguyen kich ban do 20 gia tri (van la cach chung minh entropy yeu) nhung doi "
        "oracle sang dieu SRS THUC SU noi - SEC-07 doi OTP toi thieu 6 chu so: khang dinh do dai "
        "token >= 6 va khong lan do nao duoc chap nhan.",
        {"Expected_Status": "400",
         "Expected_Assertions": "moi lan do deu tra 400; do dai resetToken lay tu forgot-password phai >= 6 ky tu theo SEC-07",
         "Title": "[SEC-07] Do 20 gia tri token: khong lan nao duoc chap nhan va OTP phai dai >= 6 chu so",
         "Bug_Ref": "A-02"}),
    "TC-A1-SEC-013": ("INVALID",
        "R1 - Ky vong 429 khong co can cu trong SRS (khong co yeu cau gioi han so lan goi). "
        "DA SUA: doi thanh dieu SEC-07 that su quy dinh - OTP phai duoc vo hieu hoa khi bi thay the: "
        "xin OTP lan 2 roi dung lai OTP lan 1.",
        {"Expected_Status": "400",
         "Expected_Assertions": "OTP cap lan 1 phai bi vo hieu hoa sau khi cap OTP lan 2; body co truong error",
         "Title": "[SEC-07] Xin OTP lan 2 thi OTP lan 1 phai bi vo hieu hoa",
         "Technique": "State Transition", "Bug_Ref": "A-04"}),
    "TC-B2-SEC-014": ("INVALID",
        "R1 - Ky vong 429 khong co can cu trong SRS. DA SUA: thay bang chuoi leo thang quyen that "
        "su kiem duoc va vi pham SEC-06 - user thuong tu nang role='admin' qua PUT /api/users/me roi "
        "goi API admin doi trang thai don. Bug X-01 phat hien o STEP 0.",
        {"Expected_Status": "403",
         "Expected_Assertions": "PUT /api/users/me KHONG duoc phep doi role; role sau khi goi van la 'user'; buoc goi API admin sau do phai bi tu choi",
         "Title": "[SEC-06] User thuong tu nang role='admin' roi doi trang thai don hang",
         "Method": "PUT", "Endpoint": "/api/users/me",
         "Request_Body": '{"name":"Attacker 23127060","phone":"0900000000","shipping_address":"Q5","role":"admin"}',
         "Request_Headers": "Authorization: Bearer {{token_attacker}}",
         "Technique": "Privilege Escalation", "Bug_Ref": "X-01", "Tag": "@bug", "Priority": "P0"}),
    "TC-C3-SEC-014": ("INVALID",
        "R1 - Ky vong 429 khong co can cu trong SRS. DA SUA: thay bang chuoi leo thang quyen "
        "SEC-06 -> SEC-03: user thuong tu nang role roi tao san pham.",
        {"Expected_Status": "403",
         "Expected_Assertions": "role sau khi goi PUT /api/users/me van phai la 'user'; POST /api/products sau do phai tra 403",
         "Title": "[SEC-06] User thuong tu nang role='admin' roi tao san pham",
         "Method": "PUT", "Endpoint": "/api/users/me",
         "Request_Body": '{"name":"Attacker 23127060","phone":"0900000000","shipping_address":"Q5","role":"admin"}',
         "Request_Headers": "Authorization: Bearer {{token_attacker}}",
         "Technique": "Privilege Escalation", "Bug_Ref": "X-01", "Tag": "@bug", "Priority": "P0"}),

    # ---- R2: ky vong 409 khong co can cu ----
    "TC-C3-DOM-041": ("INVALID",
        "R2 - Ky vong 409 khong co can cu: SRS FR-15 chi noi 'Admin co the Them/Xem/Sua/Xoa san pham', "
        "khong he dat rang buoc khoa ngoai giua san pham va don hang. AI suy dien tu kinh nghiem CSDL. "
        "DA SUA: ky vong 200 (xoa thanh cong) va bo sung khang dinh san pham thuc su bien mat.",
        {"Expected_Status": "200",
         "Expected_Assertions": "body co message; GET /api/products/1 sau do KHONG duoc tra ve san pham (bug C-04 tra 200 {})",
         "Title": "DELETE /api/products/:id | id = 1 (xoa san pham dang ton tai)",
         "Bug_Ref": "C-08"}),
    "TC-C3-STA-007": ("INVALID",
        "R2 - Ky vong 409 khong co can cu: SRS khong yeu cau ten san pham duy nhat, va cot 'name' "
        "trong database.js khong co rang buoc UNIQUE. DA SUA: ky vong 201 (tao thanh cong) va chuyen "
        "trong tam sang dieu kiem duoc - hai ban ghi phai co id khac nhau.",
        {"Expected_Status": "201",
         "Expected_Assertions": "tao thanh cong; id tra ve khac id cua san pham dau tien; SRS khong cam trung ten",
         "Title": "Tao san pham trung ten voi san pham da co (SRS khong cam)",
         "Tag": "@bug", "Bug_Ref": "C-12"}),

    # ---- R4: mau thuan noi tai ----
    "TC-A1-STA-006": ("INVALID",
        "R4 - Mau thuan noi tai: case danh dau chuyen trang thai HOP LE nhung lai ky vong 400. "
        "Ngoai ra 'EXPIRED' khong phai mot trang thai ma bo sinh dieu khien duoc: SUT khong luu "
        "thoi diem cap OTP nen khong the dua OTP ve trang thai het han qua API. "
        "DA SUA: doi thanh chuyen KHONG hop le ISSUED -> USED_TWICE (dung lai OTP da dung), la dieu "
        "SEC-07 quy dinh ro va kiem duoc hoan toan qua API.",
        {"Expected_Status": "400",
         "Expected_Assertions": "lan reset thu hai voi cung OTP phai bi tu choi; body co truong error",
         "Title": "Chuyen trang thai USED -> USED (dung lai OTP da dung - KHONG hop le)",
         "Preconditions": "Da reset mat khau thanh cong mot lan bang OTP nay",
         "Tag": "@contract", "Bug_Ref": "-"}),
    "TC-C3-STA-009": ("INVALID",
        "R4 - Mau thuan noi tai: danh dau KHONG hop le nhung ky vong 200. Ngoai ra 'IN_SEARCH' khong "
        "phai mot trang thai cua vong doi tai nguyen ma la mot phep doc. "
        "DA SUA: giu phep kiem (san pham da xoa khong duoc xuat hien trong ket qua tim kiem) nhung "
        "phat bieu lai cho dung: ky vong 200 voi mang KHONG chua san pham da xoa.",
        {"Expected_Status": "200",
         "Expected_Assertions": "HTTP 200 voi mang ket qua; mang KHONG duoc chua san pham vua bi xoa",
         "Title": "Sau khi DELETE, san pham khong duoc con trong ket qua GET /api/products?search="}),

    # ---- R5: tham so bia ----
    "TC-C3-SEC-004": ("INVALID",
        "R5 - Tham so bia: `?debug=true` khong ton tai trong api_specification.md lan trong server.js. "
        "AI tu nghi ra mot co debug de test. Test se 'pass' nhung khong chung minh dieu gi vi tham so "
        "bi bo qua hoan toan. DA SUA: bo tham so bia, kiem dung dieu co the kiem - response san pham "
        "khong duoc chua truong nam ngoai schema da dac ta.",
        {"Endpoint": "/api/products/1",
         "Expected_Assertions": "body chi duoc chua dung 6 truong id,name,price,description,imageUrl,category_id; khong co truong noi bo nao khac",
         "Title": "[--] Response san pham khong duoc chua truong nam ngoai schema"}),

    # ---- R3b: ky vong khong co can cu (khong lien quan SEC) ----
    "TC-A1-DOM-035": ("INVALID",
        "R3b - Ky vong 400 khong co can cu: SRS FR-01/FR-03 chi doi mat khau moi THOA DIEU KIEN DO MANH, "
        "khong he cam dat lai trung mat khau cu. AI ap mot chinh sach ma dac ta khong co. "
        "DA SUA: ky vong 200, va them khang dinh mat khau cu van dang nhap duoc (vi no chinh la mat khau moi).",
        {"Expected_Status": "200",
         "Expected_Assertions": "reset thanh cong; SRS khong cam dat lai trung mat khau cu; login bang mat khau do phai thanh cong",
         "Title": "POST /api/reset-password | newPassword = Api1234! (dat lai trung mat khau cu - SRS khong cam)"}),
}

# ---------------------------------------------------------------------------
# BANG 3 — Case co y tuong dung nhung ky vong dua tren suy dien, khong phai dieu
# SRS viet ra. Khong sai den muc INVALID, nhung phai ghi ro oracle la suy dien.
# ---------------------------------------------------------------------------
INFERRED_ORACLE = {
    "TC-A1-DOM-002": "email khong ton tai van tra 200 (chong user enumeration)",
    "TC-A1-DOM-009": "email khong phan biet hoa thuong",
    "TC-A1-DOM-010": "email tu cat khoang trang dau-cuoi",
    "TC-A1-DOM-020": "do dai OTP duoi bien",
    "TC-A1-DOM-021": "do dai OTP tren bien",
}

# Chi nhung assertion THAT SU chung chung. Luu y: assertion mac dinh cua nhom STA
# ("body.error chua Invalid state transition; trang thai KHONG doi") KHONG nam trong day,
# vi ve cuoi cua no da chinh la phep kiem tac dung phu ma luat R7 doi hoi.
GENERIC_ASSERTS = {
    "body la JSON; co truong error",
    "body la JSON; khop schema thanh cong",
}
MUTATING = {"POST", "PUT", "DELETE", "PATCH"}

# Luat R7 chi co nghia khi thao tac bi tu choi CO mot tac dung phu QUAN SAT DUOC.
# Doi chieu tung endpoint voi server.js:
#   - /api/checkout, /api/products, /api/categories, /api/admin/*, /api/orders/:id/cancel,
#     /api/users/me, /api/coupon-usage  -> co INSERT/UPDATE/DELETE, doc lai duoc qua GET.
#   - /api/reset-password                -> UPDATE users.password, kiem duoc bang cach login lai.
#   - /api/apply-coupon                  -> THUAN TINH TOAN, khong ghi gi ca.
#   - /api/forgot-password               -> co ghi reset_token nhung tren nhanh loi thi khong co
#                                           user nao de ma doc lai, nen khong quan sat duoc.
#   - /api/login, /api/register          -> khong phai doi tuong kiem cua 3 API da chon.
# Doi hoi "chung minh thao tac khong xay ra" o hai nhom cuoi la doi hoi mot phep kiem
# khong ton tai -> se bien nhan INCOMPLETE thanh vo nghia.
OBSERVABLE_WRITE = (
    "/api/checkout", "/api/products", "/api/categories", "/api/admin/",
    "/api/orders/", "/api/users/me", "/api/coupon-usage", "/api/reset-password",
)


def has_observable_side_effect(r):
    if r["Method"] not in MUTATING:
        return False
    ep = r["Endpoint"].split("?")[0]
    return any(ep.startswith(x) for x in OBSERVABLE_WRITE)


def audit_row(r):
    """Tra ve (label, note, overrides). Thu tu luat la thu tu uu tien."""
    tc = r["TC_ID"]
    notes = []
    ov = {}
    label = None

    # --- Luat SEC: gan lai ma SEC (ap dung truoc, co the cong don voi luat khac) ---
    if tc in SEC_REMAP:
        new_sec, why = SEC_REMAP[tc]
        if new_sec != r["SEC_Ref"]:
            ov["SEC_Ref"] = new_sec
            notes.append("R3 - Gan sai ma SEC (%s -> %s). %s" % (r["SEC_Ref"], new_sec, why))
            label = "INVALID"

    # --- Luat viet lai (R1, R2, R4, R5, R3b) ---
    if tc in REWRITE:
        lab, why, fixes = REWRITE[tc]
        label = "INVALID"
        notes.append(why)
        ov.update(fixes)

    if label == "INVALID":
        return label, " | ".join(notes), ov

    # --- Luat oracle suy dien ---
    if tc in INFERRED_ORACLE:
        notes.append("R6 - Ky vong '%s' KHONG duoc SRS phat bieu truc tiep; day la suy dien tu "
                     "thong le. DA SUA: ghi ro Oracle = SPEC(suy dien) de nguoi cham phan biet "
                     "duoc voi cac ky vong trich thang tu dac ta." % INFERRED_ORACLE[tc])
        ov["Oracle"] = "SPEC(suy dien)"
        return "INCOMPLETE", " | ".join(notes), ov

    # --- Luat assertion chung chung ---
    a = r["Expected_Assertions"].strip()
    st = int(r["Expected_Status"])
    if a in GENERIC_ASSERTS:
        if has_observable_side_effect(r) and st >= 400:
            notes.append("R7 - Case tu choi mot thao tac GHI nhung chi kiem 'co truong error'. "
                         "Thieu phan quan trong nhat: chung minh THAO TAC DA KHONG XAY RA. Mot API "
                         "tra 400 roi van ghi vao CSDL se pass case nay. DA SUA: bo sung buoc doc "
                         "lai tai nguyen sau khi goi.")
            ov["Expected_Assertions"] = a + "; VA doc lai tai nguyen sau khi goi de xac nhan du lieu KHONG bi thay doi"
            return "INCOMPLETE", " | ".join(notes), ov
        if st < 300:
            notes.append("R8 - Case thanh cong nhung chi kiem 'khop schema'. Thieu khang dinh gia tri "
                         "that su duoc luu dung. DA SUA: bo sung buoc doc lai tai nguyen va so khop "
                         "gia tri vua gui.")
            ov["Expected_Assertions"] = a + "; VA doc lai tai nguyen de xac nhan gia tri luu dung bang gia tri da gui"
            return "INCOMPLETE", " | ".join(notes), ov
        # Con lai: endpoint CHI DOC bi tu choi dau vao xau. "Tra 4xx + co truong error" da la
        # mot phep kiem tron ven vi khong co tac dung phu nao de ma kiem. Khong gan INCOMPLETE.

    # --- Luat thieu precondition cho case phu thuoc bien dong ---
    if "{{" in r["Request_Body"] and r["Preconditions"] in ("SUT da seed", "-", ""):
        notes.append("R10 - Case dung bien Postman ({{...}}) nhung precondition chi ghi 'SUT da seed', "
                     "khong noi bien do duoc dat o dau. Chay doc lap se that bai. DA SUA: ghi ro buoc "
                     "_setup phai chay truoc.")
        ov["Preconditions"] = "Folder _setup da chay xong va da dat cac bien moi truong can thiet"
        return "INCOMPLETE", " | ".join(notes), ov

    return "VALID", ("Buoc, du lieu va ky vong deu doi chieu duoc voi SRS; assertion da cu the; "
                     "chay doc lap duoc sau khi _setup chay xong."), ov


def process(path_in, path_out):
    with open(path_in, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        cols = rd.fieldnames
        rows = list(rd)
    counter = Counter()
    for r in rows:
        label, note, ov = audit_row(r)
        r.update(ov)
        # Bo sinh nhet ma SEC vao dau Title ("[SEC-04] Xem don hang..."). Khi gan lai ma o
        # cot SEC_Ref ma quen sua Title thi bao cao se tu mau thuan voi chinh no.
        if r["Title"].startswith("[SEC-0") or r["Title"].startswith("[--]"):
            r["Title"] = re.sub(r"^\[(SEC-0\d|--)\] ", "[%s] " % r["SEC_Ref"], r["Title"])
        r["Audit_Label"] = label
        r["Audit_Note"] = note
        counter[label] += 1
    os.makedirs(os.path.dirname(os.path.abspath(path_out)), exist_ok=True)
    with open(path_out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    return counter, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src")
    ap.add_argument("--out", dest="dst")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    if a.report:
        grand = Counter()
        print("| API | Tong | VALID | INVALID | INCOMPLETE | %% VALID |")
        print("|---|---|---|---|---|---|")
        for n in (1, 2, 3):
            src = "testcases/API-%d_generated.csv" % n
            dst = "testcases/API-%d_audited.csv" % n
            c, _ = process(src, dst)
            t = sum(c.values())
            grand.update(c)
            print("| API-%d | %d | %d | %d | %d | %.0f%% |"
                  % (n, t, c["VALID"], c["INVALID"], c["INCOMPLETE"], 100.0 * c["VALID"] / t))
        t = sum(grand.values())
        print("| **Tong** | **%d** | **%d** | **%d** | **%d** | **%.0f%%** |"
              % (t, grand["VALID"], grand["INVALID"], grand["INCOMPLETE"], 100.0 * grand["VALID"] / t))
        return

    c, _ = process(a.src, a.dst)
    print("%s -> %s | %s" % (a.src, a.dst, dict(c)))


if __name__ == "__main__":
    main()
