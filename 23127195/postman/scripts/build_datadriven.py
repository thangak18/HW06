#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_datadriven.py — Sinh 3 collection DATA-DRIVEN cho Postman Collection Runner

De bai yeu cau "exercise as many Postman features as you reasonably can", trong do
co "data-driven runs (the Collection Runner with a data file)". Ba collection nay
duoc thiet ke de chay kem file du lieu trong `postman/data/`:

    newman run postman/collections/dd1_phone_partitions.postman_collection.json \
        -e postman/environments/eshop-local.postman_environment.json \
        -d postman/data/api1_phone_partitions.csv

Khac biet so voi 3 collection chinh: o day MOT request duoc chay lai nhieu lan,
moi lan lay mot dong du lieu — dung cho cac bang phan vung / bang quyet dinh co
cau truc lap lai. Ky vong nam ngay trong file du lieu (cot expect_*), nen bo sung
mot phan vung moi chi la them mot dong CSV, khong phai sua collection.

Usage:
    python postman/scripts/build_datadriven.py
"""

import json
import os
import sys
import uuid

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT_DIR = os.path.join(ROOT, "postman", "collections")
NS = uuid.UUID("6f1f9c3e-0000-4000-8000-000000023195")


def det_id(*p):
    return str(uuid.uuid5(NS, "|".join(map(str, p))))


PREREQUEST = """var sid = pm.environment.get('studentId') || '23127195';
pm.request.headers.upsert({ key: 'X-Student-Id', value: sid });
console.log('[X-Student-Id] ' + sid + '  ->  ' + pm.request.method + ' ' + pm.request.url.getPath()
    + '   | iteration ' + (pm.info.iteration + 1));"""

GLOBAL_TEST = """pm.test('[GLOBAL] Request mang header X-Student-Id dung dinh dang', function () {
    pm.expect(pm.request.headers.get('X-Student-Id')).to.match(/^\\d{8}$/);
});"""


def script(kind, code):
    return {"listen": kind,
            "script": {"type": "text/javascript", "exec": code.split("\n")}}


def item(name, method, path, body=None, auth=None, tests="", pre=None, desc=""):
    it = {
        "name": name,
        "id": det_id(name),
        "event": [],
        "request": {
            "method": method,
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": {"raw": "{{baseUrl}}" + path, "host": ["{{baseUrl}}"],
                    "path": [s for s in path.strip("/").split("/") if s]},
            "description": desc,
        },
    }
    if auth:
        it["request"]["header"].append(
            {"key": "Authorization", "value": "Bearer {{%s}}" % auth})
    if body is not None:
        it["request"]["body"] = {"mode": "raw", "raw": body,
                                 "options": {"raw": {"language": "json"}}}
    if pre:
        it["event"].append(script("prerequest", pre))
    if tests:
        it["event"].append(script("test", tests))
    return it


def collection(name, description, items):
    return {
        "info": {"_postman_id": det_id(name), "name": name,
                 "description": description,
                 "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
        "item": items,
        "event": [script("prerequest", PREREQUEST), script("test", GLOBAL_TEST)],
        "variable": [{"key": "studentId", "value": "23127195"}],
    }


# ---------------------------------------------------------------------------
# DD-1 — bang phan vung so dien thoai (FR-04)
# ---------------------------------------------------------------------------

DD1_TEST = """// Ky vong duoc lay tu cot expect_valid cua file CSV
var expectValid = String(pm.iterationData.get('expect_valid')).trim().toLowerCase() === 'yes';
var phone       = pm.iterationData.get('phone');
var partition   = pm.iterationData.get('partition');

pm.test('[' + partition + '] phone=' + JSON.stringify(phone) + ' -> ' +
        (expectValid ? 'phai duoc chap nhan (200)' : 'phai bi tu choi (400)'), function () {
    if (expectValid) {
        pm.expect(pm.response.code, 'so hop le bi tu choi').to.eql(200);
    } else {
        pm.expect(pm.response.code,
            'so KHONG hop le theo FR-04 nhung van duoc chap nhan').to.eql(400);
    }
});

pm.test('Khong tra ve loi may chu (5xx)', function () {
    pm.expect(pm.response.code).to.be.below(500);
});"""

dd1 = collection(
    "HW06 - 23127195 - DD1 - Phan vung so dien thoai (FR-04)",
    "Data-driven: chay POST /api/users/me mot lan cho moi dong trong "
    "postman/data/api1_phone_partitions.csv.\n\n"
    "FR-04: so dien thoai hop le phai bat dau bang so 0 va co 10-11 chu so.\n\n"
    "Chay bang: newman run <collection> -e <environment> -d postman/data/api1_phone_partitions.csv",
    [
        item("[SETUP] Dang ky tai khoan data-driven", "POST", "/api/register",
             body=json.dumps({"name": "DD Tester 23127195", "email": "{{ddEmail}}",
                              "password": "DdTester123!"}, ensure_ascii=False, indent=2),
             tests="pm.test('Dang ky hoac da ton tai', function () {\n"
                   "    pm.expect([200, 500]).to.include(pm.response.code);\n});",
             desc="Chay lai moi vong lap — chap nhan ca truong hop tai khoan da ton tai."),
        item("[SETUP] Dang nhap lay token", "POST", "/api/login",
             body=json.dumps({"email": "{{ddEmail}}", "password": "DdTester123!"},
                             ensure_ascii=False, indent=2),
             tests="pm.test('Dang nhap thanh cong', function () {\n"
                   "    pm.response.to.have.status(200);\n});\n"
                   "pm.collectionVariables.set('ddToken', pm.response.json().token);"),
        item("Cap nhat ho so voi so dien thoai tu file du lieu", "PUT", "/api/users/me",
             body='{\n  "name": "DD Tester 23127195",\n'
                  '  "shipping_address": "227 Nguyen Van Cu, Q5",\n'
                  '  "phone": "{{phone}}"\n}',
             auth="ddToken", tests=DD1_TEST,
             desc="Moi vong lap lay mot gia tri `phone` va ky vong tuong ung tu file CSV."),
    ])

# ---------------------------------------------------------------------------
# DD-2 — bang quyet dinh coupon (FR-09)
# ---------------------------------------------------------------------------

DD2_TEST = """// Bang quyet dinh 5 dieu kien C1-C5 cua FR-09, moi dong CSV la mot to hop
var d        = pm.iterationData;
var code     = d.get('code');
var total    = Number(d.get('total_amount'));
var expSt    = Number(d.get('expect_status'));
var expDisc  = d.get('expect_discount');
var expFinal = d.get('expect_final');
var cond     = d.get('condition');
var note     = d.get('note');

pm.test('[' + cond + '] ' + code + ' / ' + total + ' -> HTTP ' + expSt + '  (' + note + ')',
    function () {
        pm.expect(pm.response.code).to.eql(expSt);
    });

if (String(expDisc).trim() !== '') {
    pm.test('discount_amount = ' + expDisc + ' (cong thuc FR-09)', function () {
        pm.expect(pm.response.json().discount_amount).to.eql(Number(expDisc));
    });
    pm.test('final_amount = ' + expFinal, function () {
        pm.expect(pm.response.json().final_amount).to.eql(Number(expFinal));
    });
    pm.test('Bat bien: 0 <= discount_amount <= total_amount', function () {
        var b = pm.response.json();
        pm.expect(b.discount_amount, 'giam gia am').to.be.at.least(0);
        pm.expect(b.discount_amount, 'giam gia vuot tong don').to.be.at.most(total);
    });
}"""

dd2 = collection(
    "HW06 - 23127195 - DD2 - Bang quyet dinh ma giam gia (FR-09)",
    "Data-driven: bang quyet dinh 5 dieu kien C1-C5 cua FR-09.\n\n"
    "Moi dong trong postman/data/api2_coupon_decision_table.csv la mot to hop dieu kien, "
    "kem ky vong ve status va ve so tien (cot expect_discount / expect_final tinh theo "
    "dung cong thuc trong dac ta).\n\n"
    "Chay bang: newman run <collection> -e <environment> -d postman/data/api2_coupon_decision_table.csv",
    [
        item("[SETUP] Dang nhap lay token", "POST", "/api/login",
             body=json.dumps({"email": "{{userEmail}}", "password": "{{userPassword}}"},
                             ensure_ascii=False, indent=2),
             tests="pm.test('Dang nhap thanh cong', function () {\n"
                   "    pm.response.to.have.status(200);\n});\n"
                   "pm.collectionVariables.set('ddToken', pm.response.json().token);\n"
                   "pm.collectionVariables.set('ddUserId', pm.response.json().user.id);"),
        item("Ap dung ma giam gia theo dong du lieu", "POST", "/api/apply-coupon",
             body='{\n  "code": "{{code}}",\n  "total_amount": {{total_amount}},\n'
                  '  "user_id": {{ddUserId}}\n}',
             auth="ddToken", tests=DD2_TEST,
             desc="Moi vong lap la mot hang cua bang quyet dinh FR-09."),
    ])

# ---------------------------------------------------------------------------
# DD-3 — bang phan vung du lieu import (FR-16)
# ---------------------------------------------------------------------------

DD3_TEST = """// Ky vong so ban ghi duoc chen, lay tu cot expect_inserted cua file CSV
var expIns    = Number(pm.iterationData.get('expect_inserted'));
var partition = pm.iterationData.get('partition');

pm.test('[' + partition + '] inserted phai bang ' + expIns, function () {
    pm.expect(pm.response.code, 'khong duoc tra loi may chu').to.be.below(500);
    pm.expect(Number(pm.response.json().inserted),
        'dong du lieu KHONG hop le theo FR-16 nhung van duoc ghi').to.eql(expIns);
});

if (expIns === 0) {
    pm.test('Phai bao cao ro dong bi loi', function () {
        pm.expect(pm.response.json().errors).to.be.an('array');
        pm.expect(pm.response.json().errors.length,
            'khong bao loi cho dong khong hop le').to.be.at.least(1);
    });
}"""

dd3 = collection(
    "HW06 - 23127195 - DD3 - Phan vung du lieu import (FR-16)",
    "Data-driven: moi dong trong postman/data/api3_import_rows.csv la mot phan vung du lieu "
    "cua mot dong CSV import, kem ky vong ve so ban ghi duoc chen.\n\n"
    "FR-16: name khong duoc rong, price phai la so duong, category_id phai ton tai.\n\n"
    "Chay bang: newman run <collection> -e <environment> -d postman/data/api3_import_rows.csv",
    [
        item("[SETUP] Dang nhap admin", "POST", "/api/login",
             body=json.dumps({"email": "{{adminEmail}}", "password": "{{adminPassword}}"},
                             ensure_ascii=False, indent=2),
             tests="pm.test('Dang nhap admin thanh cong', function () {\n"
                   "    pm.response.to.have.status(200);\n});\n"
                   "pm.collectionVariables.set('ddAdminToken', pm.response.json().token);"),
        item("Import mot dong du lieu tu file", "POST", "/api/admin/import-products",
             body='{\n  "products": [\n    {\n      "name": "{{name}}",\n'
                  '      "price": "{{price}}",\n      "description": "data-driven row",\n'
                  '      "imageUrl": "",\n      "category_id": "{{category_id}}"\n    }\n  ]\n}',
             auth="ddAdminToken", tests=DD3_TEST,
             desc="Moi vong lap import dung mot dong voi mot to hop gia tri khac nhau."),
    ])


def main():
    targets = [
        ("dd1_phone_partitions.postman_collection.json", dd1),
        ("dd2_coupon_decision_table.postman_collection.json", dd2),
        ("dd3_import_rows.postman_collection.json", dd3),
    ]
    for fname, col in targets:
        path = os.path.join(OUT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(col, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("[OK] %s (%d request)" % (fname, len(col["item"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
