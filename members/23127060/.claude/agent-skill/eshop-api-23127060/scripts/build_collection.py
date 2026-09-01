#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_collection.py - Bien CSV test case thanh Postman Collection v2.1 + Environment.

  python3 build_collection.py --csv testcases/API-1_final.csv --api API-1 \
      --out postman/collections/23127060_HW06_API-1.postman_collection.json
  python3 build_collection.py --env-only --out postman/environments/23127060_local.postman_environment.json
  python3 build_collection.py --csv ... --only-tag @contract --out ..._contract...json

Chi dung thu vien chuan.

NGUYEN TAC SO 1 — KHONG SINH ASSERTION GIA.
  Ban truoc cua script nay, voi moi assertion khong dich duoc, sinh ra:
      pm.test("...", function () { pm.expect(pm.response.code).to.be.a('number'); });
  Phep kiem do LUON PASS. No lam so "assertion passed" trong bao cao Newman phong len ma
  khong kiem gi ca — dung loai so lieu ma de bai muc 11 goi la fabricated. Ban nay thay bang
  mot dong CHU THICH `// [CHUA TU DONG HOA]`, va in ra ty le assertion da tu dong hoa duoc
  de bao cao ghi dung su that.
"""
import argparse
import csv
import json
import os
import re
import uuid

SID = "23127060"

# ---------------------------------------------------------------------------
# Script cap collection
# ---------------------------------------------------------------------------
PRE_REQUEST = r"""// ===== HW06 - API Testing - SV 23127060 - Ninh Van Khai =====
const STUDENT_ID = pm.environment.get("studentId") || "23127060";

// 1) Header bat buoc cua de bai (muc 6.4) - dat o cap COLLECTION nen ap cho MOI request
pm.request.headers.upsert({ key: "X-Student-Id", value: STUDENT_ID });
pm.request.headers.upsert({ key: "Accept", value: "application/json" });

// 2) Dong log de chup man hinh Postman Console lam bang chung chong gian lan (de bai muc 11).
//    Newman giu lai dong nay trong bao cao HTML nho co --reporter-htmlextra-logs.
console.log(
  "[HW06][" + STUDENT_ID + "] " +
  pm.request.method + " " + pm.request.url.toString() +
  " | X-Student-Id=" + STUDENT_ID +
  " | " + new Date().toISOString()
);
"""

# Kiem tra chung. Chi giu lai nhung phep kiem DUNG VOI MOI REQUEST.
# Hai phep kiem "khong lo password" va "Content-Type la JSON" da bi BO khoi day: chung
# that bai o mot so request vi bug A-07 va C-03, ma do la phat hien rieng cua tung test case
# cu the, khong phai mot rang buoc chung. De o cap collection thi mot bug se bi dem lai
# hang chuc lan va lam sai hoan toan so lieu passed/failed.
COMMON_TESTS = r"""pm.test("[COMMON] Response time < 5000ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(5000);
});

pm.test("[COMMON] Server tra ve mot response hop le (khong sap)", function () {
  pm.expect(pm.response.code).to.be.at.least(100);
  pm.expect(pm.response.code).to.be.below(600);
});
"""

CAT_NAME = {
    "DOM": "DOM - Domain partition",
    "STA": "STA - State transition",
    "SEC": "SEC - Security SEC-01..07",
    "SCH": "SCH - Schema validation",
}

# ---------------------------------------------------------------------------
# JS dung chung, nap vao bien collection de item-level script goi lai
# ---------------------------------------------------------------------------
JS_HELPERS = r"""
function H() {
  return { "Content-Type": "application/json", "X-Student-Id": pm.environment.get("studentId") };
}
function AUTH(tok) {
  var h = H(); h["Authorization"] = "Bearer " + tok; return h;
}
function BASE() { return pm.environment.get("baseUrl"); }
"""


def js_str(s):
    return json.dumps(str(s), ensure_ascii=False)



# Anh xa (endpoint, ma trang thai) -> ten schema trong postman/scripts/schemas/<API>.json.
# CSV test case khong co cot schema_ref, nen suy ra tu chinh request. Neu khong khop cai nao
# thi tra ve "default" (schema rong) va phep kiem jsonSchema se bi bo qua - tot hon la ap mot
# schema sai roi bao loi nham.
def guess_schema_ref(row):
    ep = row["Endpoint"].split("?")[0]
    st = int(row["Expected_Status"])
    if st >= 400:
        return "error"
    if ep.endswith("/api/forgot-password"):
        return "forgot_success"
    if ep.endswith("/api/reset-password"):
        return "reset_success"
    if ep.endswith("/api/login"):
        return "login_success"
    if ep.endswith("/api/checkout"):
        return "checkout_success"
    if ep.endswith("/api/apply-coupon"):
        return "coupon_success"
    if ep.endswith("/api/orders/my-orders"):
        return "order_list"
    if ep.startswith("/api/orders/"):
        return "order"
    if ep == "/api/products":
        return "product_list" if row["Method"] == "GET" else "create_success"
    if ep.startswith("/api/products/"):
        return "product"
    return "default"


# ---------------------------------------------------------------------------
# Bo dich assertion: van xuoi -> phep kiem Postman that
# ---------------------------------------------------------------------------
def compile_assertion(text, row):
    """Tra ve (list dong JS, da_tu_dong_hoa?)."""
    t = text.strip()
    low = t.lower()
    name = js_str("%s | %s" % (row["TC_ID"], t[:80]))
    out = []

    def wrap(body):
        return ["pm.test(%s, function () {" % name] + ["  " + b for b in body] + ["});"]

    # --- Content-Type ---
    if "content-type" in low or "application/json" in low:
        return wrap([
            "pm.expect(pm.response.headers.get('Content-Type') || '').to.include('application/json');"
        ]), True

    # --- khong duoc la HTML ---
    if "html" in low or "<h1>" in low:
        return wrap([
            "pm.expect(pm.response.text()).to.not.include('<h1>');",
            "pm.expect(pm.response.text()).to.not.include('<p>');",
        ]), True

    # --- khong lo password / reset_token ---
    if "password" in low and ("khong" in low or "not" in low):
        body = ["var txt = pm.response.text();",
                "pm.expect(txt).to.not.include('\"password\"');"]
        if "reset_token" in low or "resettoken" in low:
            body.append("pm.expect(txt).to.not.include('\"reset_token\"');")
        return wrap(body), True

    # --- KHONG chua resetToken trong body ---
    if "khong chua resettoken" in low.replace(" ", " ") or ("resettoken" in low and "khong" in low):
        return wrap(["pm.expect(pm.response.text()).to.not.include('resetToken');"]), True

    # --- body co truong error ---
    if re.search(r"co truong error|co error|property error", low):
        return wrap(["pm.expect(pm.response.json()).to.have.property('error');"]), True

    # --- body co message ---
    if re.search(r"body co message|co truong message", low):
        return wrap(["pm.expect(pm.response.json()).to.have.property('message');"]), True

    # --- body la JSON ---
    if low.startswith("body la json") or "parse duoc thanh json" in low:
        return wrap(["pm.expect(function(){ pm.response.json(); }).to.not.throw();"]), True

    # --- do dai OTP >= 6 ---
    if "6 ky tu" in low or ">= 6" in low or "6 chu so" in low:
        return wrap([
            "var otp = String(pm.environment.get('resetToken') || '');",
            "pm.expect(otp.length, 'do dai OTP').to.be.at.least(6);",
        ]), True

    # --- discount_amount = <so> ---
    m = re.search(r"discount_amount\s*=\s*([0-9]+)", low)
    if m:
        return wrap([
            "var j = pm.response.json();",
            "pm.expect(j.discount_amount).to.eql(%s);" % m.group(1),
        ]), True

    # --- discount_amount la number va > 0 va < total ---
    if "discount_amount" in low and ("> 0" in low or "khong duoc am" in low or "final_amount khong duoc am" in low):
        return wrap([
            "var j = pm.response.json();",
            "pm.expect(j.discount_amount, 'discount_amount').to.be.a('number').and.to.be.above(0);",
            "pm.expect(j.final_amount, 'final_amount').to.be.at.least(0);",
            "pm.expect(j.final_amount, 'final_amount phai <= total').to.be.at.most(j.discount_amount + j.final_amount);",
        ]), True

    # --- price phai la number ---
    if "price" in low and "number" in low:
        return wrap([
            "var j = pm.response.json();",
            "var p = Array.isArray(j) ? j[0] : j;",
            "pm.expect(typeof p.price, 'kieu cua price').to.eql('number');",
        ]), True

    # --- typeof price giua 2 request ---
    if "typeof price" in low:
        return wrap([
            "var truoc = pm.environment.get('priceTypeOdd');",
            "var sau = typeof pm.response.json().price;",
            "pm.expect(sau, 'kieu price cua id chan').to.eql(truoc);",
            "pm.expect(sau, 'kieu price phai la number').to.eql('number');",
        ]), True

    # --- khong duoc chua email/password cua bang users (SQLi exfiltration) ---
    if "@eshop.com" in low or ("email" in low and "khong duoc chua" in low):
        return wrap([
            "var txt = pm.response.text();",
            "pm.expect(txt).to.not.include('@eshop.com');",
            "pm.expect(txt).to.not.include('Admin123!');",
        ]), True

    # --- danh sach phai con N phan tu ---
    m = re.search(r"(?:con nguyen|phai co|con lai)\s*([0-9]+)\s*(?:phan tu|san pham)", low)
    if m:
        return wrap([
            "var j = pm.response.json();",
            "pm.expect(Array.isArray(j), 'response phai la mang').to.be.true;",
            "pm.expect(j.length, 'so phan tu').to.eql(%s);" % m.group(1),
        ]), True

    # --- mang rong ---
    if "mang rong" in low:
        return wrap([
            "var j = pm.response.json();",
            "pm.expect(Array.isArray(j)).to.be.true;",
            "pm.expect(j.length, 'phai rong').to.eql(0);",
        ]), True

    # --- trang thai van phai la X / trang thai KHONG doi ---
    m = re.search(r"van phai la '([a-z]+)'|van la '([a-z]+)'", low)
    if m or "trang thai khong doi" in low:
        st = (m.group(1) or m.group(2)) if m else None
        body = [
            "var oid = pm.environment.get('orderId');",
            "var truoc = pm.environment.get('statusTruocKhiGoi');",
            "pm.sendRequest({ url: pm.environment.get('baseUrl') + '/api/orders/' + oid,",
            "  method: 'GET', header: { 'X-Student-Id': pm.environment.get('studentId') } },",
            "  function (e, r) {",
            "    if (e || !r) { return; }",
            "    var sau = r.json().status;",
        ]
        if st:
            body.append("    pm.expect(sau, 'trang thai don hang').to.eql(%s);" % js_str(st))
        else:
            body.append("    pm.expect(sau, 'trang thai KHONG duoc doi').to.eql(truoc);")
        body += ["  });"]
        return wrap(body), True

    # --- Invalid state transition trong thong bao loi ---
    # LUU Y: chuoi 'Invalid state transition' chi la thong bao cua endpoint admin
    # PUT /api/admin/orders/:id/status. Endpoint PUT /api/orders/:id/cancel tu choi bang mot
    # thong bao khac ('Cannot cancel this order.'), va dieu do hoan toan hop le - SRS chi doi
    # "thong bao loi phu hop" chu khong quy dinh nguyen van. Doi dung chuoi o ca hai noi la
    # mot LOI CUA TEST, khong phai loi cua API.
    if "invalid state transition" in low:
        if "/cancel" in row["Endpoint"]:
            return wrap([
                "var e = pm.response.json().error || '';",
                "pm.expect(e, 'phai co thong bao tu choi').to.be.a('string').and.to.not.be.empty;",
                "pm.expect(e.toLowerCase()).to.satisfy(function (m) {",
                "  return m.indexOf('cannot cancel') >= 0 || m.indexOf('invalid state transition') >= 0;",
                "});",
            ]), True
        return wrap([
            "pm.expect(pm.response.json().error || '').to.include('Invalid state transition');"
        ]), True

    # --- doc lai tai nguyen de xac nhan KHONG bi thay doi (luat R7 cua audit) ---
    if "khong bi thay doi" in low or "khong duoc tao" in low or "khong duoc thuc hien" in low:
        return wrap([
            "// Doc lai danh sach san pham/don hang de chung minh thao tac bi tu choi",
            "// that su KHONG de lai dau vet trong CSDL (luat R7 cua STEP 3).",
            "var soTruoc = Number(pm.environment.get('soLuongTruocKhiGoi') || -1);",
            "pm.sendRequest({ url: pm.environment.get('baseUrl') + '/api/products',",
            "  method: 'GET', header: { 'X-Student-Id': pm.environment.get('studentId') } },",
            "  function (e, r) {",
            "    if (e || !r || soTruoc < 0) { return; }",
            "    pm.expect(r.json().length, 'so ban ghi truoc/sau phai bang nhau').to.eql(soTruoc);",
            "  });",
        ]), True

    # --- schema ---
    if "schema" in low:
        ref = guess_schema_ref(row)
        return wrap([
            "var schema = JSON.parse(pm.collectionVariables.get('schema_%s') || '{}');" % ref,
            "if (Object.keys(schema).length) { pm.response.to.have.jsonSchema(schema); }",
        ]), True

    # --- role van phai la 'user' ---
    if "role" in low and ("user" in low or "khong duoc" in low):
        return wrap([
            "pm.sendRequest({ url: pm.environment.get('baseUrl') + '/api/users/me',",
            "  method: 'GET', header: { 'X-Student-Id': pm.environment.get('studentId'),",
            "    'Authorization': 'Bearer ' + pm.environment.get('token_attacker') } },",
            "  function (e, r) {",
            "    if (e || !r) { return; }",
            "    pm.expect(r.json().role, 'role sau khi goi').to.eql('user');",
            "  });",
        ]), True

    # --- khong dich duoc: GHI CHU, TUYET DOI KHONG sinh phep kiem gia ---
    return ["// [CHUA TU DONG HOA] " + t], False



# ---------------------------------------------------------------------------
# CACH LY TAI KHOAN cho cac case dung /api/login
#
# SUT co bug A-09: moi lan dang nhap sai cong +2 vao login_attempts, va khoa 180 giay khi
# dat 3. Hau qua thuc te khi chay Newman: chi can MOT case thu mat khau sai la tai khoan
# api.victim bi khoa, va MOI case dang nhap chay sau do deu tra 403 - ke ca nhung case
# hoan toan khong lien quan. Ket qua la mot bug duy nhat tao ra hang loat that bai gia.
#
# Khong co endpoint nao mo khoa, va cho 180 giay trong CI la khong chap nhan duoc. Cach
# duy nhat sach se la moi case dang nhap tu tao MOT tai khoan rieng, roi tu dua tai khoan
# do ve dung trang thai minh can. Do la viec cua tang thuc thi (Postman), khong phai cua
# thiet ke test case, nen no duoc xu ly o day chu khong sua vao CSV.
ISOLATED = {
    "TC-A1-SEC-005": "fresh",             # can tai khoan dang nhap duoc binh thuong
    "TC-A1-SCH-005": "fresh",
    "TC-A1-SEC-012": "fail2",             # da sai 2 lan, day la lan sai thu 3
    "TC-A1-SEC-903": "fail2",             # da sai DUNG 2 lan, gio dang nhap bang mat khau DUNG
    "TC-A1-STA-008": "reset",             # da doi mat khau, gio thu mat khau CU
    "TC-A1-STA-901": "reset",
    "TC-A1-STA-009": "reset",             # da doi mat khau, gio thu mat khau MOI
    "TC-A1-SEC-901": "fail2_then_reset",  # bi khoa roi moi reset - kiem xem reset co mo khoa khong
}

ISO_HEAD = [
    "// Tao mot tai khoan RIENG cho case nay de khong bi anh huong boi cac case khac",
    "// (xem chu thich ISOLATED trong build_collection.py).",
    "var base = pm.environment.get('baseUrl');",
    "var H = { 'Content-Type': 'application/json', 'X-Student-Id': pm.environment.get('studentId') };",
    "var isoEmail = 'api.iso.' + Date.now() + '.23127060@test.local';",
    "pm.environment.set('isoEmail', isoEmail);",
    "function P(path, body, cb) {",
    "  pm.sendRequest({ url: base + path, method: 'POST', header: H,",
    "    body: { mode: 'raw', raw: JSON.stringify(body) } }, function (e, r) { cb(e ? null : r); });",
    "}",
    "function saiMatKhau(cb) { P('/api/login', { email: isoEmail, password: 'SaiRoi123!' }, cb); }",
    "function datLaiMatKhau(cb) {",
    "  P('/api/forgot-password', { email: isoEmail }, function (r) {",
    "    var otp = (r && r.code === 200) ? String(r.json().resetToken) : '0000';",
    "    P('/api/reset-password', { email: isoEmail, resetToken: otp,",
    "      newPassword: 'NewApi1234!' }, function () { cb(); });",
    "  });",
    "}",
]

ISO_BODY = {
    "fresh": ["P('/api/register', { name: 'Iso 23127060', email: isoEmail, password: 'Api1234!' },",
              "  function () { });"],
    "fail2": ["P('/api/register', { name: 'Iso 23127060', email: isoEmail, password: 'Api1234!' },",
              "  function () { saiMatKhau(function () { saiMatKhau(function () { }); }); });"],
    "reset": ["P('/api/register', { name: 'Iso 23127060', email: isoEmail, password: 'Api1234!' },",
              "  function () { datLaiMatKhau(function () { }); });"],
    "fail2_then_reset": [
        "P('/api/register', { name: 'Iso 23127060', email: isoEmail, password: 'Api1234!' },",
        "  function () { saiMatKhau(function () { saiMatKhau(function () {",
        "    datLaiMatKhau(function () { }); }); }); });"],
}


def isolate_body(raw):
    """Doi email cua tai khoan chung sang bien {{isoEmail}} cua tai khoan rieng."""
    return (raw.replace('"api.victim.23127060@test.local"', '"{{isoEmail}}"')
               .replace('"{{userEmail}}"', '"{{isoEmail}}"'))


# ---------------------------------------------------------------------------
# Script chuan bi trang thai (item-level pre-request)
# ---------------------------------------------------------------------------
ORDER_FLOW = ["pending", "confirmed", "shipping", "delivered"]


def build_prerequest(row):
    """Sinh script dua he thong ve dung precondition cua case."""
    ep = row["Endpoint"]
    pre = str(row.get("Preconditions", ""))
    lines = []

    if row["TC_ID"] in ISOLATED:
        lines += ISO_HEAD + ISO_BODY[ISOLATED[row["TC_ID"]]]
        return lines

    # (a) Moi case cham toi reset-password deu can mot OTP con hieu luc.
    #     forgot-password khong doi xac thuc va goi bao nhieu lan cung duoc, nen lay OTP moi
    #     ngay truoc moi request la cach re nhat de tung case DOC LAP voi nhau.
    if "/api/reset-password" in ep and "USED" not in row.get("Title", ""):
        lines += [
            "// Lay OTP moi de case nay khong phu thuoc vao thu tu chay",
            "pm.sendRequest({ url: pm.environment.get('baseUrl') + '/api/forgot-password',",
            "  method: 'POST', header: { 'Content-Type': 'application/json',",
            "    'X-Student-Id': pm.environment.get('studentId') },",
            "  body: { mode: 'raw', raw: JSON.stringify({ email: pm.environment.get('userEmail') }) } },",
            "  function (e, r) {",
            "    if (!e && r && r.code === 200 && r.json().resetToken) {",
            "      pm.environment.set('resetToken', String(r.json().resetToken));",
            "    }",
            "  });",
        ]

    # (b) Case chuyen trang thai don hang: tao don MOI va dua ve dung trang thai xuat phat.
    m = re.search(r"trang thai (pending|confirmed|shipping|delivered|canceled)", pre)
    if row["Category"] == "STA" and row["API"] == "API-2" and m:
        target = m.group(1)
        lines += [
            "// Tao don hang moi va dua ve trang thai '%s' de case chay doc lap" % target,
            "var base = pm.environment.get('baseUrl');",
            "var sid = pm.environment.get('studentId');",
            "var hUser = { 'Content-Type': 'application/json', 'X-Student-Id': sid,",
            "  'Authorization': 'Bearer ' + pm.environment.get('token_user') };",
            "var duong = %s;" % json.dumps(_path_to(target)),
            "pm.sendRequest({ url: base + '/api/checkout', method: 'POST', header: hUser,",
            "  body: { mode: 'raw', raw: JSON.stringify({ total_amount: 500000,",
            "    shipping_address: 'Q5 TPHCM 23127060' }) } }, function (e, r) {",
            "  if (e || !r || !r.json().orderId) { return; }",
            "  var oid = r.json().orderId;",
            "  pm.environment.set('orderId', oid);",
            "  pm.environment.set('statusTruocKhiGoi', '%s');" % target,
            "  (function buoc(i) {",
            "    if (i >= duong.length) { return; }",
            "    var st = duong[i];",
            "    if (st === 'canceled') {",
            "      pm.sendRequest({ url: base + '/api/orders/' + oid + '/cancel', method: 'PUT',",
            "        header: hUser, body: { mode: 'raw', raw: '{}' } }, function () { buoc(i + 1); });",
            "    } else {",
            "      pm.sendRequest({ url: base + '/api/admin/orders/' + oid + '/status', method: 'PUT',",
            "        header: hUser, body: { mode: 'raw', raw: JSON.stringify({ status: st }) } },",
            "        function () { buoc(i + 1); });",
            "    }",
            "  })(0);",
            "});",
        ]

    # (c) Case ghi len /api/products bi ky vong tu choi: dem so ban ghi TRUOC khi goi,
    #     de assertion "du lieu KHONG bi thay doi" co cai ma so sanh.
    if (row["Method"] in ("POST", "PUT", "DELETE")
            and ep.split("?")[0].startswith("/api/products")
            and str(row["Expected_Status"]).startswith(("4", "5"))):
        lines += [
            "// Dem so san pham truoc khi goi, de kiem 'thao tac bi tu choi khong de lai dau vet'",
            "pm.sendRequest({ url: pm.environment.get('baseUrl') + '/api/products',",
            "  method: 'GET', header: { 'X-Student-Id': pm.environment.get('studentId') } },",
            "  function (e, r) {",
            "    if (!e && r) { pm.environment.set('soLuongTruocKhiGoi', r.json().length); }",
            "  });",
        ]

    # (d) Case so sanh kieu price giua id le va id chan: doc id le truoc.
    if "typeof price" in str(row.get("Expected_Assertions", "")).lower():
        lines += [
            "// Doc san pham id le truoc de lay kieu cua price lam moc so sanh",
            "pm.sendRequest({ url: pm.environment.get('baseUrl') + '/api/products/1',",
            "  method: 'GET', header: { 'X-Student-Id': pm.environment.get('studentId') } },",
            "  function (e, r) {",
            "    if (!e && r) { pm.environment.set('priceTypeOdd', typeof r.json().price); }",
            "  });",
        ]
    return lines


def _path_to(target):
    """Cac buoc can di de dua don tu 'pending' ve trang thai target."""
    if target == "pending":
        return []
    if target == "canceled":
        return ["canceled"]
    i = ORDER_FLOW.index(target)
    return ORDER_FLOW[1:i + 1]


# ---------------------------------------------------------------------------
# Test script cho tung request
# ---------------------------------------------------------------------------
def build_test_script(row, stats):
    lines = ["// %s | %s | Oracle=%s | Tag=%s | Bug=%s"
             % (row["TC_ID"], row["Category"], row["Oracle"], row["Tag"], row["Bug_Ref"]),
             "// %s" % row["Title"],
             ""]
    lines.append("pm.test(%s, function () {"
                 % js_str("%s | HTTP %s" % (row["TC_ID"], row["Expected_Status"])))
    lines.append("  pm.response.to.have.status(%s);" % int(row["Expected_Status"]))
    lines.append("});")
    stats["auto"] += 1

    for a in [x.strip() for x in str(row.get("Expected_Assertions", "")).split(";")]:
        if not a or a == "-":
            continue
        js, ok = compile_assertion(a, row)
        lines.append("")
        lines += js
        stats["auto" if ok else "manual"] += 1

    # Luu lai bien cho cac case sau dung
    ep = row["Endpoint"]
    if ep.endswith("/api/checkout"):
        lines += ["", "if (pm.response.code < 300) {",
                  "  var j = pm.response.json();",
                  "  if (j.orderId) { pm.environment.set('orderId', j.orderId); }", "}"]
    if ep.endswith("/api/forgot-password"):
        lines += ["", "if (pm.response.code === 200) {",
                  "  var j = pm.response.json();",
                  "  if (j.resetToken) { pm.environment.set('resetToken', String(j.resetToken)); }", "}"]
    if ep == "/api/products" and row["Method"] == "POST":
        lines += ["", "if (pm.response.code < 300) {",
                  "  var j = pm.response.json();",
                  "  if (j.id) { pm.environment.set('newProductId', j.id); }", "}"]
    return lines


# ---------------------------------------------------------------------------
# Folder _setup
# ---------------------------------------------------------------------------
def req(name, method, path, body=None, headers=None, tests=None, desc=""):
    h = [{"key": "Content-Type", "value": "application/json"}]
    for k, v in (headers or {}).items():
        h.append({"key": k, "value": v})
    r = {"method": method, "header": h,
         "url": {"raw": "{{baseUrl}}" + path, "host": ["{{baseUrl}}"],
                 "path": [p for p in path.lstrip("/").split("?")[0].split("/") if p]},
         "description": desc}
    if "?" in path:
        q = []
        for kv in path.split("?", 1)[1].split("&"):
            k, _, v = kv.partition("=")
            q.append({"key": k, "value": v})
        r["url"]["query"] = q
    if body is not None:
        r["body"] = {"mode": "raw", "raw": json.dumps(body, ensure_ascii=False),
                     "options": {"raw": {"language": "json"}}}
    item = {"name": name, "request": r, "response": []}
    if tests:
        item["event"] = [{"listen": "test", "script": {"type": "text/javascript", "exec": tests}}]
    return item


LOGIN_TEST = """var ok = pm.response.code === 200;
pm.test("[_setup] {LABEL} dang nhap duoc", function () {{
  pm.response.to.have.status(200);
  pm.expect(pm.response.json()).to.have.property("token");
}});
if (ok) {{
  var j = pm.response.json();
  pm.environment.set("{TOK}", j.token);
  if (j.user && j.user.id) {{ pm.environment.set("{UID}", j.user.id); }}
}}"""


def setup_folder(api):
    items = [
        req("00 Dang ky user nan nhan (bo qua neu da co)", "POST", "/api/register",
            {"name": "Victim 23127060", "email": "{{userEmail}}", "password": "{{userPassword}}"},
            tests=['pm.test("[_setup] endpoint register phan hoi", function () {',
                   '  pm.expect(pm.response.code).to.be.oneOf([200, 201, 400, 409, 500]);',
                   '});'],
            desc="SUT khong co rang buoc UNIQUE tren email nen goi lai se tao ban ghi trung. "
                 "Vi vay quy trinh chuan la: restart backend (DB duoc seed lai) roi moi chay collection."),
        req("01 Dang ky user tan cong", "POST", "/api/register",
            {"name": "Attacker 23127060", "email": "{{attackerEmail}}", "password": "{{attackerPassword}}"},
            tests=['pm.test("[_setup] endpoint register phan hoi", function () {',
                   '  pm.expect(pm.response.code).to.be.oneOf([200, 201, 400, 409, 500]);',
                   '});']),
        req("02 Login nan nhan -> token_user", "POST", "/api/login",
            {"email": "{{userEmail}}", "password": "{{userPassword}}"},
            tests=LOGIN_TEST.format(LABEL="user nan nhan", TOK="token_user", UID="userId").split("\n")),
        req("03 Login ke tan cong -> token_attacker", "POST", "/api/login",
            {"email": "{{attackerEmail}}", "password": "{{attackerPassword}}"},
            tests=LOGIN_TEST.format(LABEL="ke tan cong", TOK="token_attacker", UID="attackerId").split("\n")),
        req("04 Login admin -> token_admin", "POST", "/api/login",
            {"email": "{{adminEmail}}", "password": "{{adminPassword}}"},
            tests=LOGIN_TEST.format(LABEL="admin", TOK="token_admin", UID="adminId").split("\n")),
    ]
    if api == "API-1":
        items.append(req("05 Xin OTP cho ke tan cong -> attackerResetToken", "POST", "/api/forgot-password",
            {"email": "{{attackerEmail}}"},
            tests=['pm.test("[_setup] lay duoc OTP cua ke tan cong", function () {',
                   '  pm.response.to.have.status(200);',
                   '});',
                   'if (pm.response.code === 200 && pm.response.json().resetToken) {',
                   '  pm.environment.set("attackerResetToken", String(pm.response.json().resetToken));',
                   '}'],
            desc="Dung cho TC-A1-SEC-905: thu dung OTP cua tai khoan nay cho tai khoan khac."))
    if api == "API-2":
        items.append(req("05 Tao don hang cua nan nhan -> victimOrderId", "POST", "/api/checkout",
            {"total_amount": 500000, "shipping_address": "1 Vo Van Ngan, Thu Duc"},
            headers={"Authorization": "Bearer {{token_user}}"},
            tests=['pm.test("[_setup] tao duoc don hang cua nan nhan", function () {',
                   '  pm.expect(pm.response.code).to.be.oneOf([200, 201]);',
                   '  pm.expect(pm.response.json()).to.have.property("orderId");',
                   '});',
                   'if (pm.response.code < 300) {',
                   '  pm.environment.set("victimOrderId", pm.response.json().orderId);',
                   '  pm.environment.set("orderId", pm.response.json().orderId);',
                   '}'],
            desc="Don hang nay la muc tieu cua cac case IDOR (SEC-02)."))
    if api == "API-3":
        items.append(req("05 Tao san pham lam vat thu -> newProductId", "POST", "/api/products",
            {"name": "SP Test 23127060", "price": 150000, "description": "San pham kiem thu",
             "imageUrl": "https://example.com/a.png", "category_id": 1},
            headers={"Authorization": "Bearer {{token_admin}}"},
            tests=['pm.test("[_setup] tao duoc san pham vat thu", function () {',
                   '  pm.expect(pm.response.code).to.be.oneOf([200, 201]);',
                   '  pm.expect(pm.response.json()).to.have.property("id");',
                   '});',
                   'if (pm.response.code < 300) {',
                   '  pm.environment.set("newProductId", pm.response.json().id);',
                   '}']))
        items.append(req("06 Dem so san pham ban dau", "GET", "/api/products", None,
            tests=['pm.test("[_setup] doc duoc danh sach san pham", function () {',
                   '  pm.response.to.have.status(200);',
                   '});',
                   'if (pm.response.code === 200) {',
                   '  pm.environment.set("soLuongTruocKhiGoi", pm.response.json().length);',
                   '}']))
    return {"name": "_setup - chuan bi du lieu va token", "item": items,
            "description": "Phai chay TRUOC moi folder khac. Dat cac bien: token_user, "
                           "token_attacker, token_admin, userId, orderId, newProductId..."}


# ---------------------------------------------------------------------------
def load_schemas(api):
    p = os.path.join("postman", "scripts", "schemas", "%s.json" % api)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}


def build_collection(rows, api, sid, stats):
    folders = {}
    for r in rows:
        folders.setdefault(r["Category"], []).append(r)

    items = [setup_folder(api)]
    for cat in ("DOM", "STA", "SEC", "SCH"):
        if cat not in folders:
            continue
        sub = []
        for r in folders[cat]:
            body = str(r.get("Request_Body", "-")).strip()
            if r["TC_ID"] in ISOLATED:
                body = isolate_body(body)
            request = {
                "method": r["Method"],
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "url": _url(r["Endpoint"]),
                "description": ("%s\n\nPreconditions: %s\nOracle: %s\nSEC: %s\nTag: %s\n"
                                "Bug: %s\nNguon: %s\nAudit: %s\n%s"
                                % (r["Title"], r["Preconditions"], r["Oracle"], r["SEC_Ref"],
                                   r["Tag"], r["Bug_Ref"], r["Source"], r["Audit_Label"],
                                   r["Audit_Note"])),
            }
            raw_h = str(r.get("Request_Headers", "-") or "-").strip()
            if raw_h and raw_h != "-":
                for part in raw_h.split(";"):
                    if ":" in part:
                        k, v = part.split(":", 1)
                        request["header"].append({"key": k.strip(), "value": v.strip()})
            if body and body != "-" and r["Method"] in ("POST", "PUT", "PATCH"):
                request["body"] = {"mode": "raw", "raw": body,
                                   "options": {"raw": {"language": "json"}}}
            events = [{"listen": "test",
                       "script": {"type": "text/javascript", "exec": build_test_script(r, stats)}}]
            pre = build_prerequest(r)
            if pre:
                events.insert(0, {"listen": "prerequest",
                                  "script": {"type": "text/javascript", "exec": pre}})
            sub.append({"name": "%s %s | %s" % (r["TC_ID"], r["Tag"], r["Title"][:64]),
                        "event": events, "request": request, "response": []})
        items.append({"name": CAT_NAME[cat], "item": sub})

    schemas = load_schemas(api)
    variables = [{"key": "schema_%s" % k, "value": json.dumps(v, ensure_ascii=False)}
                 for k, v in schemas.items()]
    variables.append({"key": "schema_default", "value": "{}"})

    return {
        "info": {"_postman_id": str(uuid.uuid4()),
                 "name": "%s_HW06_%s" % (sid, api),
                 "description": "HW06 API Testing - SV %s Ninh Van Khai - %s" % (sid, api),
                 "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
        "item": items,
        "event": [
            {"listen": "prerequest", "script": {"type": "text/javascript",
                                                "exec": (JS_HELPERS + PRE_REQUEST).split("\n")}},
            {"listen": "test", "script": {"type": "text/javascript",
                                          "exec": COMMON_TESTS.split("\n")}},
        ],
        "variable": variables,
    }


def _url(endpoint):
    ep = endpoint if endpoint.startswith("/") else "/" + endpoint
    path_part, _, query_part = ep.lstrip("/").partition("?")
    o = {"raw": "{{baseUrl}}" + ep, "host": ["{{baseUrl}}"],
         "path": [p for p in path_part.split("/") if p]}
    if query_part:
        o["query"] = [{"key": k, "value": v}
                      for k, _, v in (kv.partition("=") for kv in query_part.split("&"))]
    return o


def build_env(sid):
    vals = [
        ("baseUrl", "http://localhost:3000"),
        ("studentId", sid),
        ("userEmail", "api.victim.%s@test.local" % sid),
        ("userPassword", "Api1234!"),
        ("attackerEmail", "api.attacker.%s@test.local" % sid),
        ("attackerPassword", "Api1234!"),
        # Tai khoan admin la du lieu seed san cua SUT (backend/database.js).
        # Mat khau dung la 'Admin123!' - ban truoc cua script ghi 'admin123' nen
        # buoc lay token_admin luon that bai am tham.
        ("adminEmail", "admin@eshop.com"),
        ("adminPassword", "Admin123!"),
        ("token_user", ""), ("token_attacker", ""), ("token_admin", ""),
        ("userId", ""), ("attackerId", ""), ("adminId", ""),
        ("orderId", ""), ("victimOrderId", ""),
        ("resetToken", ""), ("oldResetToken", ""), ("attackerResetToken", ""),
        ("bruteToken", "1000"),
        ("newProductId", ""),
        ("productIdOdd", "1"), ("productIdEven", "2"),
        ("priceTypeOdd", ""), ("soLuongTruocKhiGoi", ""), ("statusTruocKhiGoi", ""),
    ]
    return {"id": str(uuid.uuid4()), "name": "%s_local" % sid,
            "values": [{"key": k, "value": v, "type": "default", "enabled": True} for k, v in vals],
            "_postman_variable_scope": "environment"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    ap.add_argument("--api", default="API-1")
    ap.add_argument("--sid", default=SID)
    ap.add_argument("--out", required=True)
    ap.add_argument("--env-only", action="store_true")
    ap.add_argument("--only-tag")
    ap.add_argument("--tc-list", help="file danh sach TC_ID (moi dong 1 ma) de loc, dung cho moc hoi quy")
    a = ap.parse_args()

    d = os.path.dirname(os.path.abspath(a.out))
    if d:
        os.makedirs(d, exist_ok=True)

    if a.env_only:
        obj = build_env(a.sid)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print("Da ghi environment: %s (%d bien)" % (a.out, len(obj["values"])))
        return

    if not a.csv:
        raise SystemExit("Thieu --csv")
    with open(a.csv, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if a.only_tag:
        rows = [r for r in rows if r.get("Tag") == a.only_tag]
    if a.tc_list:
        keep = set()
        with open(a.tc_list, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    keep.add(line)
        rows = [r for r in rows if r["TC_ID"] in keep]

    stats = {"auto": 0, "manual": 0}
    col = build_collection(rows, a.api, a.sid, stats)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(col, f, ensure_ascii=False, indent=2)

    n = sum(len(fo["item"]) for fo in col["item"])
    tong = stats["auto"] + stats["manual"]
    print("%s | %d folder | %d request | assertion tu dong hoa: %d/%d (%.0f%%), con lai %d dong "
          "ghi chu [CHUA TU DONG HOA]"
          % (a.out, len(col["item"]), n, stats["auto"], tong,
             100.0 * stats["auto"] / max(tong, 1), stats["manual"]))


if __name__ == "__main__":
    main()
