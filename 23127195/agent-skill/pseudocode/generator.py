#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generator.py — Cai dat tham chieu cua bo sinh test case API (HW06 / 23127195)

Day la ban hien thuc chay duoc cua thiet ke mo ta trong ../DESIGN.md va
./generator_pseudocode.md.

Ranh gioi trach nhiem:

    G1 (trich xuat dac ta -> EndpointModel)  ->  DO LLM LAM.
        Prompt dung o buoc nay nam trong ../../ai/prompts/. Ket qua la mot file
        JSON dung luoc do EndpointModel. File nay PHAI duoc nguoi kiem tra truoc
        khi dua vao G2.

    G2..G6 (sinh phan vung, chuoi trang thai, bao mat, luoc do, kiem tra)  ->  MA TAT DINH.
        Chinh la file nay. Khong goi LLM o day. Tinh day du den tu DANH MUC QUY TAC,
        khong den tu mo hinh.

Cach chay:
    python agent-skill/pseudocode/generator.py <endpoint_model.json> [-o ir.json]
    python agent-skill/pseudocode/generator.py --demo        # chay tren mo hinh mau FR-04

Dau ra la IR dung dung dinh dang ma postman/scripts/build_collections.py doc duoc,
nen co the noi thang vao duong ong hien co.
"""

import argparse
import json
import os
import re
import sys

MAX_SAFE_INT = 2 ** 53 - 1

SQLI = "' OR '1'='1' --"
XSS = "<script>alert('23127195')</script>"
UNICODE_VN = "Nguyễn Thị Hồng Đào"

# JWT dung cho case bao mat — sinh san, ky bang khoa KHAC voi khoa cua SUT
JWT_WRONG_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                 ".eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg4MjY1MzE3fQ"
                 ".Z7LjnTp0gy4sgW-VSZeS8M8S_u6llyhMLw15h__XSEk")
JWT_ALG_NONE = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpZCI6MSwicm9sZSI6ImFkbWluIn0."


class Ctx:
    """Bo dem sinh ID va gom case."""

    def __init__(self, model):
        self.model = model
        self.cases = []
        self.n = 0

    def add(self, group, title, technique, expected_by_spec, request, assertions,
            param="-", partition="-", sec=None, source="AI", audit_reason=None):
        self.n += 1
        case = {
            "id": "%s-%03d" % (self.model["case_prefix"], self.n),
            "group": group,
            "title": title,
            "technique": technique,
            "param": param,
            "partition": partition,
            "source": source,
            "audit": {
                "label": "VALID",
                "reason": audit_reason or "Sinh tu danh muc quy tac — CHUA duoc nguoi audit.",
            },
            "expected_by_spec": expected_by_spec,
            "request": request,
            "expect": {"assert": assertions},
        }
        if sec:
            case["sec"] = sec
        self.cases.append(case)
        return case


# ---------------------------------------------------------------------------
# Tien ich dung chung
# ---------------------------------------------------------------------------

def valid_value(param):
    """Mot gia tri hop le tieu bieu cho tham so."""
    if "vi_du" in param:
        return param["vi_du"]
    if param["kieu"] == "number":
        for c in param.get("rang_buoc", []):
            if c["loai"] == "bien":
                return c["gia_tri"].get("min", 1)
        return 1
    if param["kieu"] == "array":
        return []
    return "gia-tri-hop-le"


def body_with(model, param_name, value, drop=False):
    """Dung body day du hop le roi thay dung mot truong (hoac bo han truong do)."""
    body = {}
    for p in model["tham_so"]:
        if p["vi_tri"] != "body":
            continue
        if p["ten"] == param_name:
            if drop:
                continue
            body[p["ten"]] = value
        else:
            body[p["ten"]] = valid_value(p)
    return body


def req(model, body=None, auth=None, path=None):
    r = {"method": model["method"], "path": path or model["path"]}
    if body is not None:
        r["body"] = body
    if auth is not None:
        r["auth"] = auth
    elif model.get("can_xac_thuc"):
        r["auth"] = model.get("vai_tro_yeu_cau") or "user"
    return r


def a_status(v):
    return {"t": "status", "v": v}


def a_status_in(vs):
    return {"t": "statusIn", "v": vs}


def a_no_5xx():
    return {"t": "exec", "v": "pm.test('Khong tra loi may chu (5xx)', function () {\n"
                             "    pm.expect(pm.response.code).to.be.below(500);\n});"}


# ---------------------------------------------------------------------------
# G2 — Sinh phan vung mien
# ---------------------------------------------------------------------------

def g2_domain_partitions(ctx):
    model = ctx.model
    group = "Domain Partition"

    for p in model["tham_so"]:
        if p["vi_tri"] != "body":
            continue
        name, kind = p["ten"], p["kieu"]
        g = "%s: %s" % (group, name)
        required = p.get("bat_buoc", False)
        fail = 400 if required else 200

        # (a) phan vung pho quat
        ctx.add(g, "thieu truong %s" % name, "domain-partition",
                "400 Bad Request neu %s la truong bat buoc." % name,
                req(model, body_with(model, name, None, drop=True)),
                [a_status(fail)], param=name, partition="Thieu truong bat buoc")

        ctx.add(g, "%s = null" % name, "domain-partition",
                "400 Bad Request; khong duoc ghi NULL vao co so du lieu.",
                req(model, body_with(model, name, None)),
                [a_status(fail), a_no_5xx()], param=name, partition="Gia tri null")

        wrong = 12345 if kind == "string" else "sai-kieu"
        ctx.add(g, "%s sai kieu du lieu" % name, "domain-partition",
                "400 Bad Request — hop dong API quy dinh %s la %s." % (name, kind),
                req(model, body_with(model, name, wrong)),
                [a_status(400)], param=name, partition="Sai kieu: %s" % type(wrong).__name__)

        # (b) phan vung theo kieu
        if kind == "string":
            for label, val, exp in [
                ("Chuoi rong", "", [a_status(fail)]),
                ("Chi khoang trang", "     ", [a_status(400)]),
                ("Unicode tieng Viet", UNICODE_VN, [a_status_in([200, 400]), a_no_5xx()]),
                ("Khoang trang bao quanh", "  %s  " % valid_value(p),
                 [a_status_in([200, 400]), a_no_5xx()]),
            ]:
                ctx.add(g, "%s: %s" % (name, label.lower()), "domain-partition",
                        "Xem danh muc quy tac phan vung chuoi trong DESIGN.md muc N2.",
                        req(model, body_with(model, name, val)),
                        exp, param=name, partition=label)

        elif kind == "number":
            for label, val, exp in [
                ("Bang 0", 0, [a_status(400)]),
                ("So am", -1, [a_status(400)]),
                ("Vuot so nguyen an toan", MAX_SAFE_INT + 2, [a_no_5xx()]),
                ("So thuc", 1.5, [a_no_5xx()]),
                ("Chuoi-so", "123", [a_no_5xx()]),
            ]:
                ctx.add(g, "%s: %s" % (name, label.lower()), "domain-partition",
                        "Xem danh muc quy tac phan vung so trong DESIGN.md muc N2.",
                        req(model, body_with(model, name, val)),
                        exp, param=name, partition=label)

        # (c) phan vung theo rang buoc — BAT BUOC, khong duoc bo
        for c in p.get("rang_buoc", []):
            cite = c.get("trich_dan", "(khong co trich dan)")

            if c["loai"] == "bien":
                lo, hi = c["gia_tri"].get("min"), c["gia_tri"].get("max")
                points = []
                if lo is not None:
                    points += [(lo - 1, False), (lo, True), (lo + 1, True)]
                if hi is not None:
                    points += [(hi - 1, True), (hi, True), (hi + 1, False)]
                for v, ok in points:
                    ctx.add(g, "%s tai bien %s" % (name, v), "domain-partition",
                            'Trich dan dac ta: "%s"' % cite,
                            req(model, body_with(model, name, v)),
                            [a_status(200 if ok else 400)],
                            param=name, partition="Bien: %s (%s)" % (v, "hop le" if ok else "khong hop le"))

            elif c["loai"] == "do_dai":
                lo, hi = c["gia_tri"].get("min", 0), c["gia_tri"].get("max")
                if hi:
                    for v, ok in [(hi, True), (hi + 1, False)]:
                        ctx.add(g, "%s do dai %d ky tu" % (name, v), "domain-partition",
                                'Trich dan dac ta: "%s"' % cite,
                                req(model, body_with(model, name, "A" * v)),
                                [a_status(200 if ok else 400)],
                                param=name, partition="Do dai %d (%s)" % (v, "hop le" if ok else "vuot bien"))

            elif c["loai"] == "mau":
                pattern = c["gia_tri"]
                for label, val, ok in [
                    ("Khop mau", c.get("vi_du_khop", "0912345678"), True),
                    ("Khong khop mau", c.get("vi_du_khong_khop", "abc"), False),
                    ("Khop mot phan", c.get("vi_du_khop_mot_phan", "091234"), False),
                ]:
                    ctx.add(g, "%s: %s (%s)" % (name, label.lower(), val), "domain-partition",
                            'Trich dan dac ta: "%s" (mau: %s)' % (cite, pattern),
                            req(model, body_with(model, name, val)),
                            [a_status(200 if ok else 400)],
                            param=name, partition=label)

            elif c["loai"] == "khoa_ngoai":
                for label, val, ok in [("Khoa ton tai", 1, True),
                                       ("Khoa khong ton tai", 999999, False),
                                       ("Khoa = 0", 0, False),
                                       ("Khoa am", -1, False)]:
                    ctx.add(g, "%s: %s" % (name, label.lower()), "domain-partition",
                            'Trich dan dac ta: "%s"' % cite,
                            req(model, body_with(model, name, val)),
                            [a_status(200 if ok else 400)],
                            param=name, partition=label)

    # (d) chieu bo sung cho API nhan MANG ban ghi
    arr = next((p for p in model["tham_so"] if p["kieu"] == "array"), None)
    if arr:
        g = "%s: cau truc mang %s" % (group, arr["ten"])
        for label, val, exp in [
            ("Mang rong", [], [a_status(400)]),
            ("Khong phai mang", "chuoi", [a_status(400)]),
            ("Mang chua phan tu null", [{"hop_le": True}, None], [a_no_5xx()]),
        ]:
            ctx.add(g, "%s: %s" % (arr["ten"], label.lower()), "domain-partition",
                    "Danh muc quy tac cho tham so kieu mang — DESIGN.md muc N2.",
                    req(model, {arr["ten"]: val}), exp,
                    param=arr["ten"], partition=label)


# ---------------------------------------------------------------------------
# G3 — Sinh chuoi chuyen trang thai
# ---------------------------------------------------------------------------

def g3_state_transitions(ctx):
    model = ctx.model
    M = model.get("may_trang_thai")
    if not M:
        return
    g = "State Transition"
    states = M["cac_trang_thai"]
    valid = {(t["tu"], t["den"]) for t in M["chuyen_hop_le"]}

    # (a) canh hop le
    for t in M["chuyen_hop_le"]:
        ctx.add(g, "[hop le] %s -> %s" % (t["tu"], t["den"]), "state-transition",
                "Chuyen doi hop le theo may trang thai trong dac ta.",
                req(model, {"_chuyen": "%s->%s" % (t["tu"], t["den"])}),
                [a_status(200)],
                partition="Canh hop le %s -> %s" % (t["tu"], t["den"]))

    # (b) moi canh KHONG hop le
    for a in states:
        for b in states:
            if a != b and (a, b) not in valid:
                ctx.add(g, "[khong hop le] %s -> %s" % (a, b), "state-transition",
                        "Moi chuyen doi khong nam trong may trang thai phai bi tu choi.",
                        req(model, {"_chuyen": "%s->%s" % (a, b)}),
                        [a_status(400)],
                        partition="Canh khong hop le %s -> %s" % (a, b))

    # (c) canh TU LAP — LLM gan nhu luon bo sot
    for s in states:
        ctx.add(g, "[tu lap] thuc hien lai hanh dong dua den %s" % s, "state-transition",
                "Thuc hien lai hanh dong phai vo hieu hoa ket qua cu, khong tao ra hai "
                "ban the cung hop le.",
                req(model, {"_lap_lai": s}),
                [a_status(400)],
                partition="Canh tu lap tai %s" % s)

    # (d) roi khoi trang thai KET THUC
    for s in M.get("trang_thai_ket_thuc", []):
        for b in states:
            if b != s:
                ctx.add(g, "[trang thai ket thuc] %s -> %s" % (s, b), "state-transition",
                        "Trang thai ket thuc khong duoc chuyen sang bat ky trang thai nao khac.",
                        req(model, {"_chuyen": "%s->%s" % (s, b)}),
                        [a_status(400)],
                        partition="Roi trang thai ket thuc %s" % s)

    # (e) bao toan truong khi cap nhat MOT PHAN
    if model["method"] == "PUT":
        body_params = [p["ten"] for p in model["tham_so"] if p["vi_tri"] == "body"]
        if len(body_params) > 1:
            for keep in body_params:
                ctx.add(g, "cap nhat mot phan: chi gui '%s'" % keep, "state-transition",
                        "Cac truong khong duoc gui phai giu nguyen gia tri cu — "
                        "khong duoc ghi de bang NULL.",
                        req(model, {keep: valid_value(
                            next(p for p in model["tham_so"] if p["ten"] == keep))}),
                        [a_status(200), a_no_5xx()],
                        param=keep, partition="Partial update — bao toan truong khong gui")


# ---------------------------------------------------------------------------
# G4 — Sinh case bao mat
# ---------------------------------------------------------------------------

def g4_security(ctx):
    model = ctx.model
    g = "Security"
    sec = model.get("sec_ap_dung", [])
    ok_body = body_with(model, "__none__", None)

    if model.get("can_xac_thuc"):
        ctx.add(g, "khong kem token -> 401", "security",
                "SEC-02: API co tinh bao mat phai yeu cau JWT hop le.",
                {"method": model["method"], "path": model["path"], "body": ok_body},
                [a_status(401)], sec=["SEC-02"], partition="Khong xac thuc")

        for label, tok, note in [
            ("token rac", "Bearer khong-phai-jwt", "Token khong parse duoc"),
            ("JWT ky bang khoa SAI", "Bearer " + JWT_WRONG_KEY,
             "Token dung cau truc nhung chu ky sai — phep thu THAT SU cho viec "
             "server co verify chu ky hay chi decode payload"),
            ("JWT thuat toan alg=none", "Bearer " + JWT_ALG_NONE,
             "Lo hong kinh dien cua thu vien JWT cau hinh sai"),
        ]:
            r = {"method": model["method"], "path": model["path"],
                 "auth": "raw", "authValue": tok, "body": ok_body}
            ctx.add(g, "%s -> 403" % label, "security",
                    "SEC-02: %s." % note, r,
                    [a_status_in([401, 403])], sec=["SEC-02"], partition=note)

    if model.get("vai_tro_yeu_cau") == "admin":
        ctx.add(g, "token cua nguoi dung THUONG -> 403", "security",
                "SEC-03: API Admin phai kiem tra role = 'admin' trong Token, "
                "khong chi kiem tra su ton tai cua Token.",
                req(model, ok_body, auth="user"),
                [a_status(403)], sec=["SEC-03"],
                partition="Xac thuc dung nhung khong du quyen")

    if "SEC-06" in sec:
        for f in ["role", "id", "is_admin", "email"]:
            b = dict(ok_body)
            b[f] = "admin" if f in ("role",) else 1
            ctx.add(g, "mass assignment: gui kem truong '%s'" % f, "security",
                    "SEC-06: khong duoc cho phep thay doi truong dac quyen tu client. "
                    "Luu y: day la truong KHONG co trong dac ta — chinh vi vay ma "
                    "test sinh theo danh sach tham so cua tai lieu khong bao gio cham toi.",
                    req(model, b),
                    [a_no_5xx()], sec=["SEC-06"], param=f,
                    partition="Truong ngoai hop dong API")

    if "SEC-05" in sec:
        for p in model["tham_so"]:
            if p["kieu"] == "string" and p["vi_tri"] == "body":
                ctx.add(g, "SQL injection qua '%s'" % p["ten"], "security",
                        "SEC-05: truy van CSDL phai dung Parameterized Query.",
                        req(model, body_with(model, p["ten"], SQLI)),
                        [a_no_5xx(),
                         {"t": "bodyNotMatch", "v": "SQLITE_|syntax error|near \"",
                          "name": "Khong ro ri loi SQL"}],
                        sec=["SEC-05"], param=p["ten"], partition="Payload SQL injection")

    if "SEC-01" in sec:
        for f in model.get("lươc_do_response", {}).get("truong_cam", []):
            ctx.add(g, "response khong duoc chua '%s'" % f, "security",
                    "SEC-01: khong duoc ro ri du lieu nhay cam trong response.",
                    req(model, ok_body),
                    [{"t": "notHasKey", "path": f}],
                    sec=["SEC-01"], partition="Ro ri du lieu nhay cam")

    # IDOR — moi tham so mang y nghia dinh danh
    for p in model["tham_so"]:
        if re.search(r"(^|_)(id|user_id|owner)$", p["ten"]):
            ctx.add(g, "IDOR qua '%s'" % p["ten"], "security",
                    "Dinh danh chu the phai lay tu JWT, khong duoc lay tu body.",
                    req(model, body_with(model, p["ten"], 1)),
                    [a_no_5xx()], param=p["ten"],
                    partition="Truy cap doi tuong truc tiep khong hop le")


# ---------------------------------------------------------------------------
# G5 — Sinh case luoc do
# ---------------------------------------------------------------------------

def g5_schema(ctx):
    model = ctx.model
    S = model.get("lươc_do_response", {})
    if not S:
        return
    g = "Schema Validation"
    ok_body = body_with(model, "__none__", None)

    if "thanh_cong" in S:
        ctx.add(g, "response thanh cong khop hop dong API", "schema",
                "Response phai khop dung luoc do mo ta trong dac ta API.",
                req(model, ok_body),
                [a_status(200), {"t": "contentTypeJson"},
                 {"t": "schema", "v": S["thanh_cong"]}],
                partition="Response thanh cong")

        for f, spec in S["thanh_cong"].get("properties", {}).items():
            if "type" in spec:
                ctx.add(g, "kieu du lieu cua '%s' la %s" % (f, spec["type"]), "schema",
                        "Truong tien tra ve dang chuoi thay vi so la loi kinh dien "
                        "lam client noi chuoi thay vi cong so.",
                        req(model, ok_body),
                        [{"t": "type", "path": f, "v": spec["type"]}],
                        param=f, partition="Kieu du lieu cua truong")

        allowed = sorted(S["thanh_cong"].get("properties", {}).keys())
        ctx.add(g, "KHONG co truong nao ngoai hop dong API", "schema",
                "Kiem tra luoc do phai theo CA HAI chieu. Chieu 'khong co truong thua' "
                "chinh la cach phat hien SELECT * vo tinh lam ro ri cot nhay cam.",
                req(model, ok_body),
                [{"t": "exec", "v":
                  "pm.test('Khong co truong nao ngoai hop dong API', function () {\n"
                  "    var allowed = %s;\n"
                  "    var extra = Object.keys(pm.response.json()).filter(function (k) {\n"
                  "        return allowed.indexOf(k) === -1;\n"
                  "    });\n"
                  "    pm.expect(extra, 'truong thua: ' + extra.join(', '))"
                  ".to.be.an('array').that.is.empty;\n});"
                  % json.dumps(allowed)}],
                partition="Truong ngoai hop dong (additionalProperties)")

    if "loi" in S:
        ctx.add(g, "response loi khop dinh dang chuan", "schema",
                "Tinh nhat quan cua dinh dang loi la mot phan hop dong API.",
                req(model, {"__khong_hop_le": True}),
                [{"t": "contentTypeJson"}, {"t": "schema", "v": S["loi"]}],
                partition="Response loi")


# ---------------------------------------------------------------------------
# G6a — Kiem tra IR
# ---------------------------------------------------------------------------

def g6a_validate(ir, model):
    errors, warnings = [], []
    seen = set()

    for c in ir:
        if c["id"] in seen:
            errors.append("ID trung: %s" % c["id"])
        seen.add(c["id"])

        if not c.get("expected_by_spec", "").strip():
            errors.append("%s: thieu expected_by_spec (ky vong phai truy vet ve dac ta)" % c["id"])
        if c.get("source") not in ("AI", "HUMAN"):
            errors.append("%s: source phai la AI hoac HUMAN" % c["id"])
        if c.get("audit", {}).get("label") not in ("VALID", "INVALID", "INCOMPLETE"):
            errors.append("%s: thieu nhan audit hop le" % c["id"])
        if not c.get("audit", {}).get("reason", "").strip():
            errors.append("%s: thieu ly do audit" % c["id"])

        # Chan khiem khuyet harness da gap that — xem DESIGN.md muc 5.1
        for a in c.get("expect", {}).get("assert", []):
            if a.get("t") == "exec" and "pm.sendRequest" in a.get("v", ""):
                if "catch (e) { done(e); }" not in a["v"]:
                    errors.append(
                        "%s: assertion bat dong bo khong boc try/catch. Khi assertion FAIL, "
                        "done() khong bao gio duoc goi va Newman se AM THAM bo qua test nay."
                        % c["id"])

        if "pm.sendRequest" in (c.get("preScript") or ""):
            warnings.append(
                "%s: dat tac dung phu trong pre-request script — nen tach thanh "
                "request [SETUP] tuong minh (DESIGN.md muc 5.2)" % c["id"])

    # kiem tra tinh day du theo danh muc quy tac
    for p in model["tham_so"]:
        if p["vi_tri"] != "body":
            continue
        have = {c.get("partition") for c in ir if c.get("param") == p["ten"]}
        for must in ("Thieu truong bat buoc", "Gia tri null"):
            if must not in have:
                errors.append("Thieu phan vung bat buoc: %s / %s" % (p["ten"], must))

    return errors, warnings


# ---------------------------------------------------------------------------
# Mo hinh mau — dung cho --demo
# ---------------------------------------------------------------------------

DEMO_MODEL = {
    "api_id": "DEMO",
    "case_prefix": "TC-GEN",
    "fr": "FR-04",
    "name": "Quan ly ho so ca nhan",
    "method": "PUT",
    "path": "/api/users/me",
    "can_xac_thuc": True,
    "vai_tro_yeu_cau": "user",
    "tham_so": [
        {"ten": "name", "vi_tri": "body", "kieu": "string", "bat_buoc": True,
         "vi_du": "Nguyen Van A",
         "rang_buoc": [{"loai": "do_dai", "gia_tri": {"min": 1, "max": 255},
                        "trich_dan": "Ho Ten la truong bat buoc (FR-04)"}]},
        {"ten": "phone", "vi_tri": "body", "kieu": "string", "bat_buoc": True,
         "vi_du": "0912345678",
         "rang_buoc": [{"loai": "mau", "gia_tri": "^0\\d{9,10}$",
                        "vi_du_khop": "0912345678",
                        "vi_du_khong_khop": "9912345678",
                        "vi_du_khop_mot_phan": "091234567",
                        "trich_dan": "So dien thoai hop le: bat dau bang so 0, tu 10-11 chu so"}]},
        {"ten": "shipping_address", "vi_tri": "body", "kieu": "string", "bat_buoc": False,
         "vi_du": "227 Nguyen Van Cu, Q5"},
    ],
    "may_trang_thai": None,
    "lươc_do_response": {
        "thanh_cong": {"type": "object", "required": ["message"],
                       "properties": {"message": {"type": "string"}}},
        "loi": {"type": "object", "required": ["error"],
                "properties": {"error": {"type": "string"}}},
        "truong_cam": ["password", "reset_token", "login_attempts"],
    },
    "sec_ap_dung": ["SEC-01", "SEC-02", "SEC-05", "SEC-06"],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model", nargs="?", help="duong dan file EndpointModel JSON (san pham cua G1)")
    ap.add_argument("-o", "--out", help="ghi IR ra file (mac dinh: in ra man hinh)")
    ap.add_argument("--demo", action="store_true", help="chay tren mo hinh mau FR-04")
    args = ap.parse_args()

    if args.demo:
        model = DEMO_MODEL
    elif args.model:
        with open(args.model, encoding="utf-8") as f:
            model = json.load(f)
    else:
        ap.error("can mot file EndpointModel, hoac dung --demo")

    ctx = Ctx(model)
    g2_domain_partitions(ctx)     # G2
    g3_state_transitions(ctx)     # G3
    g4_security(ctx)              # G4
    g5_schema(ctx)                # G5

    errors, warnings = g6a_validate(ctx.cases, model)   # G6a

    from collections import Counter
    tech = Counter(c["technique"] for c in ctx.cases)
    print("=" * 68, file=sys.stderr)
    print("Bo sinh test case API — %s (%s)" % (model["name"], model["fr"]), file=sys.stderr)
    print("=" * 68, file=sys.stderr)
    print("  G2 domain partition : %3d case" % tech["domain-partition"], file=sys.stderr)
    print("  G3 state transition : %3d case" % tech["state-transition"], file=sys.stderr)
    print("  G4 security         : %3d case" % tech["security"], file=sys.stderr)
    print("  G5 schema           : %3d case" % tech["schema"], file=sys.stderr)
    print("  ----------------------------", file=sys.stderr)
    print("  TONG                : %3d case" % len(ctx.cases), file=sys.stderr)
    print("", file=sys.stderr)
    print("  G6a kiem tra IR     : %d loi, %d canh bao"
          % (len(errors), len(warnings)), file=sys.stderr)
    for e in errors[:10]:
        print("     [LOI]     %s" % e, file=sys.stderr)
    for w in warnings[:5]:
        print("     [CANH BAO] %s" % w, file=sys.stderr)
    print("", file=sys.stderr)
    print("  >> BUOC TIEP THEO (G6b): con nguoi PHAI audit tung case, gan nhan", file=sys.stderr)
    print("     VALID/INVALID/INCOMPLETE va bo sung cac case may khong sinh duoc.", file=sys.stderr)
    print("     Xem DESIGN.md muc 4 — 34/144 case cua bai nay do con nguoi them,", file=sys.stderr)
    print("     va chung tim ra 6/24 loi.", file=sys.stderr)
    print("=" * 68, file=sys.stderr)

    ir = {
        "api_id": model["api_id"],
        "fr": model["fr"],
        "name": model["name"],
        "collection_file": "generated_%s.postman_collection.json" % model["api_id"].lower(),
        "description": "Sinh tu dong boi agent-skill/pseudocode/generator.py — CHUA audit.",
        "cases": ctx.cases,
    }
    out = json.dumps(ir, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as f:
            f.write(out + "\n")
        print("Da ghi IR ra %s" % args.out, file=sys.stderr)
    else:
        print(out)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
