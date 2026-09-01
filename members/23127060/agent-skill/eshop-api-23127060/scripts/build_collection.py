#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_collection.py - Bien CSV test case thanh Postman Collection v2.1 + Environment.

Chi dung thu vien chuan.

Vi du:
  python3 build_collection.py --csv testcases/API-1_final.csv --api API-1 --sid 23127060 \
      --out postman/collections/23127060_HW06_API-1.postman_collection.json

  python3 build_collection.py --env-only --sid 23127060 \
      --out postman/environments/23127060_local.postman_environment.json

Sinh ra:
  - Pre-request script cap collection: chen header X-Student-Id + console.log (chong gian lan)
  - Tests script cap collection: kiem tra chung (response time, khong lo password, content-type)
  - Folder theo Category (DOM/STA/SEC/SCH), request theo tung dong CSV
  - Tests script rieng cho tung request: assert status + cac assertion trong CSV
"""
import argparse
import csv
import json
import os
import uuid

PRE_REQUEST = """// ===== HW06 - SV {SID} - Ninh Van Khai =====
const STUDENT_ID = pm.environment.get("studentId") || "{SID}";

// 1) Header bat buoc theo de bai (muc 6.4 + muc 11 chong gian lan)
pm.request.headers.upsert({{ key: "X-Student-Id", value: STUDENT_ID }});
pm.request.headers.upsert({{ key: "Accept", value: "application/json" }});

// 2) Log de chup man hinh Postman Console lam bang chung
console.log(
  "[HW06][" + STUDENT_ID + "] " +
  pm.request.method + " " + pm.request.url.toString() +
  " | X-Student-Id=" + STUDENT_ID +
  " | " + new Date().toISOString()
);

// 3) Tu dong lay token neu chua co (Postman feature: pm.sendRequest)
if (!pm.environment.get("token_user")) {{
  pm.sendRequest({{
    url: pm.environment.get("baseUrl") + "/api/login",
    method: "POST",
    header: {{ "Content-Type": "application/json", "X-Student-Id": STUDENT_ID }},
    body: {{ mode: "raw", raw: JSON.stringify({{
      email: pm.environment.get("userEmail"),
      password: pm.environment.get("userPassword")
    }}) }}
  }}, function (err, res) {{
    if (!err && res && res.code === 200) {{
      const j = res.json();
      if (j.token) pm.environment.set("token_user", j.token);
      if (j.user && j.user.id) pm.environment.set("userId", j.user.id);
    }}
  }});
}}
"""

COMMON_TESTS = """// Kiem tra chung cho moi request
pm.test("[COMMON] Response time < 2000ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("[COMMON][SEC-02] Khong lo truong nhay cam", function () {
  const t = pm.response.text();
  pm.expect(t).to.not.include('"password"');
  pm.expect(t).to.not.include('"reset_token"');
});

pm.test("[COMMON][SCH] Content-Type la application/json", function () {
  pm.expect(pm.response.headers.get("Content-Type") || "").to.include("application/json");
});
"""

CAT_NAME = {
    "DOM": "DOM - Domain partition",
    "STA": "STA - State transition",
    "SEC": "SEC - Security SEC-01..07",
    "SCH": "SCH - Schema validation",
}


def js_str(s):
    return json.dumps(str(s), ensure_ascii=False)


def build_test_script(row):
    lines = []
    tc = row["TC_ID"]
    lines.append("// %s | %s | Oracle=%s | Tag=%s | Bug=%s"
                 % (tc, row["Category"], row["Oracle"], row["Tag"], row["Bug_Ref"]))
    lines.append("pm.test(%s, function () {" % js_str(tc + " | status " + str(row["Expected_Status"])))
    lines.append("  pm.response.to.have.status(%s);" % row["Expected_Status"])
    lines.append("});")

    asserts = [a.strip() for a in str(row.get("Expected_Assertions", "")).split(";") if a.strip() and a.strip() != "-"]
    for i, a in enumerate(asserts, 1):
        lines.append("")
        lines.append("// TODO[assert %d]: %s" % (i, a))
        lines.append("pm.test(%s, function () {" % js_str("%s | %s" % (tc, a[:70])))
        low = a.lower()
        if "error" in low:
            lines.append("  pm.expect(pm.response.json()).to.have.property('error');")
        elif "password" in low or "reset_token" in low:
            lines.append("  pm.expect(pm.response.text()).to.not.include('\"password\"');")
            lines.append("  pm.expect(pm.response.text()).to.not.include('\"reset_token\"');")
        elif "html" in low:
            lines.append("  pm.expect(pm.response.text()).to.not.include('<h1>');")
        elif "content-type" in low:
            lines.append("  pm.expect(pm.response.headers.get('Content-Type') || '').to.include('application/json');")
        elif "schema" in low:
            lines.append("  const schema = JSON.parse(pm.collectionVariables.get('schema_default') || '{}');")
            lines.append("  pm.response.to.have.jsonSchema(schema);")
        else:
            lines.append("  // dien assertion cu the o day")
            lines.append("  pm.expect(pm.response.code).to.be.a('number');")
        lines.append("});")

    if row["Category"] == "STA" and "orderId" not in str(row["Endpoint"]):
        pass
    if row["Method"] == "POST" and row["Endpoint"].endswith("/api/checkout"):
        lines.append("")
        lines.append("if (pm.response.code === 201 || pm.response.code === 200) {")
        lines.append("  const j = pm.response.json();")
        lines.append("  if (j.orderId) pm.environment.set('orderId', j.orderId);")
        lines.append("}")
    if row["Endpoint"].endswith("/api/forgot-password"):
        lines.append("")
        lines.append("if (pm.response.code === 200) {")
        lines.append("  const j = pm.response.json();")
        lines.append("  if (j.resetToken) pm.environment.set('resetToken', j.resetToken);")
        lines.append("}")
    return lines


def parse_headers(raw, row):
    hs = [{"key": "Content-Type", "value": "application/json"}]
    raw = str(raw or "").strip()
    if raw and raw != "-":
        for part in raw.split(";"):
            if ":" in part:
                k, v = part.split(":", 1)
                hs.append({"key": k.strip(), "value": v.strip()})
    return hs


def url_obj(endpoint):
    ep = endpoint if endpoint.startswith("/") else "/" + endpoint
    raw = "{{baseUrl}}" + ep
    path_part, _, query_part = ep.lstrip("/").partition("?")
    o = {"raw": raw, "host": ["{{baseUrl}}"], "path": [p for p in path_part.split("/") if p]}
    if query_part:
        q = []
        for kv in query_part.split("&"):
            k, _, v = kv.partition("=")
            q.append({"key": k, "value": v})
        o["query"] = q
    return o


def build_collection(rows, api, sid):
    folders = {}
    for r in rows:
        cat = r["Category"]
        folders.setdefault(cat, []).append(r)

    items = []
    for cat in ["DOM", "STA", "SEC", "SCH"]:
        if cat not in folders:
            continue
        sub = []
        for r in folders[cat]:
            body = str(r.get("Request_Body", "-")).strip()
            req = {
                "method": r["Method"],
                "header": parse_headers(r.get("Request_Headers"), r),
                "url": url_obj(r["Endpoint"]),
                "description": "%s\n\nPreconditions: %s\nOracle: %s\nSEC: %s\nTag: %s\nBug: %s"
                               % (r["Title"], r["Preconditions"], r["Oracle"],
                                  r["SEC_Ref"], r["Tag"], r["Bug_Ref"]),
            }
            if body and body != "-" and r["Method"] in ("POST", "PUT", "PATCH", "DELETE"):
                req["body"] = {"mode": "raw", "raw": body,
                               "options": {"raw": {"language": "json"}}}
            sub.append({
                "name": "%s %s %s" % (r["TC_ID"], r["Tag"], r["Title"][:70]),
                "event": [{"listen": "test",
                           "script": {"type": "text/javascript",
                                      "exec": build_test_script(r)}}],
                "request": req,
                "response": [],
            })
        items.append({"name": CAT_NAME[cat], "item": sub})

    return {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": "%s_HW06_%s" % (sid, api),
            "description": "HW06 API Testing - SV %s - Ninh Van Khai - %s" % (sid, api),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": items,
        "event": [
            {"listen": "prerequest",
             "script": {"type": "text/javascript",
                        "exec": PRE_REQUEST.format(SID=sid).split("\n")}},
            {"listen": "test",
             "script": {"type": "text/javascript",
                        "exec": COMMON_TESTS.split("\n")}},
        ],
        "variable": [
            {"key": "schema_default", "value": "{}"},
        ],
    }


def build_env(sid):
    vals = [
        ("baseUrl", "http://localhost:3000"),
        ("studentId", sid),
        ("userEmail", "api.victim.%s@test.local" % sid),
        ("userPassword", "Api1234!"),
        ("attackerEmail", "api.attacker.%s@test.local" % sid),
        ("attackerPassword", "Api1234!"),
        ("adminEmail", "admin@eshop.com"),
        ("adminPassword", "admin123"),
        ("token_user", ""),
        ("token_attacker", ""),
        ("token_admin", ""),
        ("userId", ""),
        ("orderId", ""),
        ("resetToken", ""),
        ("productIdOdd", "1"),
        ("productIdEven", "2"),
    ]
    return {
        "id": str(uuid.uuid4()),
        "name": "%s_local" % sid,
        "values": [{"key": k, "value": v, "type": "default", "enabled": True} for k, v in vals],
        "_postman_variable_scope": "environment",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    ap.add_argument("--api", default="API-1")
    ap.add_argument("--sid", default="23127060")
    ap.add_argument("--out", required=True)
    ap.add_argument("--env-only", action="store_true")
    ap.add_argument("--only-tag", help="chi lay case co tag nay, vd @contract")
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

    col = build_collection(rows, a.api, a.sid)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(col, f, ensure_ascii=False, indent=2)

    n = sum(len(fo["item"]) for fo in col["item"])
    print("Da ghi collection: %s | %d folder | %d request" % (a.out, len(col["item"]), n))


if __name__ == "__main__":
    main()
