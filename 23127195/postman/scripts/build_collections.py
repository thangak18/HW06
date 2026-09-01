#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_collections.py — Postman Collection Builder (HW06 / 23127195)

Doc dac ta test case duoi dang IR (Intermediate Representation) JSON trong
`testcases/*.json` va sinh ra Postman Collection v2.1.0 tuong ung trong
`postman/collections/`.

IR nay cung chinh la dinh dang trung gian ma AI Test Generator (agent-skill)
sinh ra tu API specification — xem `agent-skill/pseudocode/`.

Usage:
    python postman/scripts/build_collections.py
"""

import json
import os
import re
import sys
import uuid

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TC_DIR = os.path.join(ROOT, "testcases")
OUT_DIR = os.path.join(ROOT, "postman", "collections")

NS = uuid.UUID("6f1f9c3e-0000-4000-8000-000000023195")


def det_id(*parts):
    """ID on dinh giua cac lan build -> git diff sach."""
    return str(uuid.uuid5(NS, "|".join(str(p) for p in parts)))


# ---------------------------------------------------------------------------
# Assertion descriptors -> Postman test JS
# ---------------------------------------------------------------------------

def js_str(value):
    return json.dumps(value, ensure_ascii=False)


def assertion_to_js(case_id, idx, a):
    """Chuyen 1 descriptor assertion thanh 1 khoi pm.test(...)."""
    t = a["t"]
    name = a.get("name")

    def block(default_name, body):
        return 'pm.test(%s, function () {\n%s\n});' % (
            js_str(name or default_name),
            "\n".join("    " + line for line in body.strip().split("\n")),
        )

    if t == "status":
        return block(
            "Status code la %s" % a["v"],
            "pm.response.to.have.status(%d);" % a["v"],
        )

    if t == "statusIn":
        return block(
            "Status code thuoc %s" % a["v"],
            "pm.expect(%s).to.include(pm.response.code);" % js_str(a["v"]),
        )

    if t == "hasKey":
        return block(
            "Response co truong '%s'" % a["path"],
            "pm.expect(J()).to.have.nested.property(%s);" % js_str(a["path"]),
        )

    if t == "notHasKey":
        return block(
            "Response KHONG duoc co truong '%s'" % a["path"],
            "pm.expect(J()).to.not.have.nested.property(%s);" % js_str(a["path"]),
        )

    if t == "eq":
        return block(
            "%s == %s" % (a["path"], a["v"]),
            "pm.expect(dig(J(), %s)).to.eql(%s);" % (js_str(a["path"]), js_str(a["v"])),
        )

    if t == "neq":
        return block(
            "%s != %s" % (a["path"], a["v"]),
            "pm.expect(dig(J(), %s)).to.not.eql(%s);" % (js_str(a["path"]), js_str(a["v"])),
        )

    if t == "type":
        return block(
            "Kieu du lieu cua '%s' la %s" % (a["path"], a["v"]),
            "pm.expect(dig(J(), %s)).to.be.a(%s);" % (js_str(a["path"]), js_str(a["v"])),
        )

    if t == "match":
        return block(
            "'%s' khop regex %s" % (a["path"], a["v"]),
            "pm.expect(String(dig(J(), %s))).to.match(new RegExp(%s));"
            % (js_str(a["path"]), js_str(a["v"])),
        )

    if t == "gte":
        return block(
            "%s >= %s" % (a["path"], a["v"]),
            "pm.expect(Number(dig(J(), %s))).to.be.at.least(%s);" % (js_str(a["path"]), a["v"]),
        )

    if t == "lte":
        return block(
            "%s <= %s" % (a["path"], a["v"]),
            "pm.expect(Number(dig(J(), %s))).to.be.at.most(%s);" % (js_str(a["path"]), a["v"]),
        )

    if t == "arrayLen":
        return block(
            "Mang co %s phan tu" % a["v"],
            "pm.expect(J()).to.be.an('array').with.lengthOf(%d);" % a["v"],
        )

    if t == "arrayLenGte":
        return block(
            "Mang co >= %s phan tu" % a["v"],
            "pm.expect(J()).to.be.an('array');\n"
            "pm.expect(J().length).to.be.at.least(%d);" % a["v"],
        )

    if t == "bodyNotMatch":
        return block(
            "Body KHONG lo thong tin khop /%s/" % a["v"],
            "pm.expect(pm.response.text()).to.not.match(new RegExp(%s, 'i'));" % js_str(a["v"]),
        )

    if t == "bodyMatch":
        return block(
            "Body khop /%s/" % a["v"],
            "pm.expect(pm.response.text()).to.match(new RegExp(%s, 'i'));" % js_str(a["v"]),
        )

    if t == "contentTypeJson":
        return block(
            "Content-Type la application/json",
            "pm.expect(pm.response.headers.get('Content-Type') || '')"
            ".to.include('application/json');",
        )

    if t == "schema":
        return block(
            a.get("label", "Response khop JSON Schema cua spec"),
            "var schema = %s;\npm.expect(pm.response.to.have.jsonSchema(schema));"
            % json.dumps(a["v"], ensure_ascii=False, indent=0).replace("\n", " "),
        )

    if t == "responseTimeUnder":
        return block(
            "Response time < %sms" % a["v"],
            "pm.expect(pm.response.responseTime).to.be.below(%d);" % a["v"],
        )

    if t == "exec":
        # Escape hatch: JS tho, dung cho assertion phuc tap (state machine, oracle rieng)
        return a["v"]

    raise ValueError("Unknown assertion type %r in %s" % (t, case_id))


PRELUDE = """// ---- helper (auto-generated by build_collections.py) ----
function J() {
    try { return pm.response.json(); } catch (e) { return {}; }
}
function dig(obj, path) {
    return String(path).split('.').reduce(function (o, k) {
        return (o === undefined || o === null) ? undefined : o[k];
    }, obj);
}
"""


def resolve_snippet(spec, case, key):
    """Cho phep IR dung `preScriptRef` / `postScriptRef` tro toi spec['snippets']."""
    ref = case.get(key + "Ref")
    if ref:
        try:
            return spec["snippets"][ref]
        except KeyError:
            raise ValueError("Snippet %r khong ton tai (case %s)" % (ref, case["id"]))
    return case.get(key)


def build_test_script(case):
    lines = [PRELUDE]
    lines.append("// %s | %s | nguon: %s | audit: %s" % (
        case["id"], case["title"], case.get("source", "AI"),
        case.get("audit", {}).get("label", "-"),
    ))
    if case.get("known_defect"):
        lines.append("// !! Case nay ky vong theo SPEC; SUT hien sai -> %s (test se FAIL co chu dich)"
                     % case["known_defect"])
    for i, a in enumerate(case.get("expect", {}).get("assert", [])):
        lines.append(assertion_to_js(case["id"], i, a))
    for cap in case.get("capture", []):
        setter = {"collection": "pm.collectionVariables.set",
                  "environment": "pm.environment.set",
                  "global": "pm.globals.set"}[cap.get("scope", "collection")]
        expr = js_str(cap["v"]) if "v" in cap else "dig(J(), %s)" % js_str(cap["path"])
        lines.append("%s(%s, %s);" % (setter, js_str(cap["var"]), expr))
    return [l for chunk in lines for l in chunk.split("\n")]


# ---------------------------------------------------------------------------
# Request building
# ---------------------------------------------------------------------------

def build_url(path, query=None):
    raw = "{{baseUrl}}" + path
    url = {
        "raw": raw,
        "host": ["{{baseUrl}}"],
        "path": [p for p in path.strip("/").split("/") if p],
    }
    if query:
        url["query"] = [{"key": k, "value": str(v)} for k, v in query.items()]
        url["raw"] = raw + "?" + "&".join("%s=%s" % (k, v) for k, v in query.items())
    return url


def build_item(spec, case):
    req = case["request"]
    item = {
        "name": "%s %s" % (case["id"], case["title"]),
        "id": det_id(case["id"]),
        "event": [],
        "request": {
            "method": req["method"],
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": build_url(req["path"], req.get("query")),
            "description": (
                "**Ky thuat:** %s\n\n"
                "**Tham so / phan vung:** %s\n\n"
                "**Ky vong theo dac ta:** %s\n\n"
                "**Nguon:** %s | **Audit:** %s — %s"
            ) % (
                case.get("technique", "-"),
                "%s = %s" % (case.get("param", "-"), case.get("partition", "-")),
                case.get("expected_by_spec", "-"),
                case.get("source", "AI"),
                case.get("audit", {}).get("label", "-"),
                case.get("audit", {}).get("reason", "-"),
            ),
        },
    }
    if req.get("auth") == "admin":
        item["request"]["header"].append(
            {"key": "Authorization", "value": "Bearer {{adminToken}}"})
    elif req.get("auth") == "user":
        item["request"]["header"].append(
            {"key": "Authorization", "value": "Bearer {{userToken}}"})
    elif req.get("auth") == "raw":
        item["request"]["header"].append(
            {"key": "Authorization", "value": req["authValue"]})

    for h in req.get("headers", []):
        item["request"]["header"].append(h)

    if "body" in req:
        item["request"]["body"] = {
            "mode": "raw",
            "raw": req["body"] if isinstance(req["body"], str)
            else json.dumps(req["body"], ensure_ascii=False, indent=2),
            "options": {"raw": {"language": "json"}},
        }

    if case.get("preScript"):
        item["event"].append({
            "listen": "prerequest",
            "script": {"type": "text/javascript",
                       "exec": case["preScript"].split("\n")},
        })

    test_exec = build_test_script(case)
    if test_exec:
        item["event"].append({
            "listen": "test",
            "script": {"type": "text/javascript", "exec": test_exec},
        })
    return item


COLLECTION_PREREQUEST = """// ============================================================
// Collection-level Pre-request Script
// Bat buoc theo de bai: MOI request phai mang header X-Student-Id
// Console log duoi day chinh la BANG CHUNG chong gian lan (§11)
// ============================================================
var sid = pm.environment.get('studentId') || pm.collectionVariables.get('studentId');
pm.request.headers.upsert({ key: 'X-Student-Id', value: sid });
pm.request.headers.upsert({ key: 'X-Run-Id', value: pm.variables.replaceIn('{{$guid}}') });

console.log('[X-Student-Id] ' + sid
    + '  ->  ' + pm.request.method + ' ' + pm.request.url.getPath());
"""

COLLECTION_TEST = """// ============================================================
// Collection-level Test Script — assertion ap dung cho MOI request
// ============================================================
pm.test('[GLOBAL] Request mang header X-Student-Id dung dinh dang', function () {
    var sent = pm.request.headers.get('X-Student-Id');
    pm.expect(sent, 'thieu header X-Student-Id').to.be.a('string');
    pm.expect(sent).to.match(/^\\d{8}$/);
});

pm.test('[GLOBAL] Server khong ro ri stack trace / duong dan he thong', function () {
    pm.expect(pm.response.text()).to.not.match(/at Object\\.|node_modules|ECONNREFUSED|\\\\Users\\\\/);
});
"""


def build_collection(spec):
    folders = {}
    order = []
    for case in spec["cases"]:
        group = case.get("group", "Khac")
        if group not in folders:
            folders[group] = {
                "name": group,
                "id": det_id(spec["api_id"], group),
                "item": [],
            }
            order.append(group)
        folders[group]["item"].append(build_item(spec, case))

    return {
        "info": {
            "_postman_id": det_id(spec["api_id"], "collection"),
            "name": "HW06 · 23127195 · %s (%s) — %s" % (
                spec["api_id"], spec["fr"], spec["name"]),
            "description": spec.get("description", ""),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": [folders[g] for g in order],
        "event": [
            {"listen": "prerequest",
             "script": {"type": "text/javascript",
                        "exec": COLLECTION_PREREQUEST.split("\n")}},
            {"listen": "test",
             "script": {"type": "text/javascript",
                        "exec": COLLECTION_TEST.split("\n")}},
        ],
        "variable": [
            {"key": "studentId", "value": "23127195"},
        ],
    }


def main():
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    built = []
    for fname in sorted(os.listdir(TC_DIR)):
        if not fname.endswith("_testcases.json"):
            continue
        with open(os.path.join(TC_DIR, fname), encoding="utf-8") as f:
            spec = json.load(f)
        col = build_collection(spec)
        out = os.path.join(OUT_DIR, spec["collection_file"])
        with open(out, "w", encoding="utf-8") as f:
            json.dump(col, f, ensure_ascii=False, indent=2)
            f.write("\n")
        n_total = len(spec["cases"])
        n_setup = sum(1 for c in spec["cases"] if c.get("setup"))
        n_ai = sum(1 for c in spec["cases"] if c.get("source") == "AI" and not c.get("setup"))
        n_human = sum(1 for c in spec["cases"] if c.get("source") == "HUMAN" and not c.get("setup"))
        built.append((spec["api_id"], os.path.basename(out), n_total, n_setup, n_ai, n_human))
        print("[OK] %-7s -> %-52s  tong=%3d (setup=%d, AI=%d, HUMAN=%d)"
              % (spec["api_id"], os.path.basename(out), n_total, n_setup, n_ai, n_human))
    if not built:
        print("Khong tim thay file IR nao trong %s" % TC_DIR, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
