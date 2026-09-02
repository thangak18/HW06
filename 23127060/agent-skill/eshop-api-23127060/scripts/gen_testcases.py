#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_testcases.py - Bộ sinh test case API tự động từ API spec máy đọc được.

Đây chính là hiện thực của AI-driven API test generator (HW06 mục 7, G9.5).
Chỉ dùng thư viện chuẩn của Python.

Cách dùng:
  python3 gen_testcases.py --spec spec/api-3.json --out testcases/API-3_generated.csv
  python3 gen_testcases.py --spec spec/api-3.json --only DOM --out testcases/API-3_generated.csv
  python3 gen_testcases.py --spec spec/api-3.json --only STA --out out.csv --append
  python3 gen_testcases.py --spec spec/api-1.json --stats

Kiến trúc (khớp với diagram + pseudocode trong agent-skill/):
  PARSE -> NORMALISE -> 4 RULE ENGINES (DOM/STA/SEC/SCH) -> DEDUP -> COVERAGE -> EMIT
"""
import argparse
import csv
import json
import os
import re
from collections import Counter, OrderedDict

COLUMNS = [
    "TC_ID", "API", "FR", "Category", "Technique", "Title", "Method", "Endpoint",
    "Preconditions", "Request_Headers", "Request_Body", "Expected_Status",
    "Expected_Assertions", "Oracle", "SEC_Ref", "Priority", "Source",
    "Audit_Label", "Audit_Note", "Tag", "Bug_Ref", "Why_AI_Missed",
]

CATS = ["DOM", "STA", "SEC", "SCH"]

# Bang nay bam theo eshop-sut/README.md muc 9 "Yeu cau Bao mat" (ban that),
# KHÔNG phải bảng SEC suy diễn theo OWASP. Xem report/00_environment.md mục 4.
SEC_DEFAULT_ASSERT = {
    "SEC-01": "response KHONG chua truong password (du plaintext hay hash); mat khau khong duoc luu plaintext",
    "SEC-02": "tra 401 khi thieu token / 403 khi token sai; du lieu KHONG bi doc hay thay doi",
    "SEC-03": "tra 403 khi token hop le nhung role != 'admin'; hanh dong admin KHONG duoc thuc hien",
    "SEC-04": "payload HTML/script khong duoc luu tho; server tra ve ban da escape hoac tu choi (4xx)",
    "SEC-05": "truy van dung parameterized query: payload SQLi bi coi la chuoi tim kiem thuong, khong doi ngu nghia cau lenh; khong tra HTML loi DB",
    "SEC-06": "truong role trong body bi bo qua; role cua tai khoan sau khi goi van la 'user'",
    "SEC-07": "OTP dai >= 6 chu so, het han sau thoi gian quy dinh, va khong dung lai duoc lan thu hai",
}


def jdump(obj):
    if obj is None:
        return "-"
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def mk_row(**kw):
    row = OrderedDict((c, "") for c in COLUMNS)
    row.update(kw)
    for c in COLUMNS:
        if row[c] == "" or row[c] is None:
            row[c] = "" if c in ("Audit_Label", "Audit_Note", "Why_AI_Missed") else "-"
    return row


def body_with(base, name, value, drop=False):
    b = dict(base or {})
    if drop:
        b.pop(name, None)
    else:
        b[name] = value
    return b


def gen_domain(spec):
    rows = []
    api = spec["api_id"]
    pref = spec["tc_prefix"]
    n = 0
    for ep in spec["endpoints"]:
        base_body = ep.get("valid_body", {})
        for p in ep.get("params", []):
            for part in p.get("partitions", []):
                n += 1
                where = p.get("in", "body")
                if where == "body":
                    body = body_with(base_body, p["name"], part.get("value"),
                                     drop=part.get("omit", False))
                    endpoint = ep["path"]
                elif where == "query":
                    body = base_body if ep["method"] != "GET" else None
                    endpoint = ep["path"] + "?" + p["name"] + "=" + str(part.get("value"))
                else:
                    endpoint = ep["path"].replace(":" + p["name"], str(part.get("value")))
                    body = base_body if ep["method"] in ("POST", "PUT") else None

                valid = part.get("valid", False)
                shown = "<thieu key>" if part.get("omit") else jdump(part.get("value"))[:40]
                title = "%s %s | %s = %s (%s)" % (
                    ep["method"], ep["path"], p["name"], shown,
                    part.get("desc", part["id"]))
                rows.append(mk_row(
                    TC_ID="TC-%s-DOM-%03d" % (pref, n),
                    API=api, FR=spec["fr"], Category="DOM",
                    Technique=part.get("technique", "BVA" if part.get("boundary") else "EP"),
                    Title=title,
                    Method=ep["method"], Endpoint=endpoint,
                    Preconditions=ep.get("preconditions", "SUT da seed"),
                    Request_Headers=ep.get("headers", "-"),
                    Request_Body=jdump(body),
                    Expected_Status=part.get(
                        "expected_status",
                        ep.get("success_status", 200) if valid else 400),
                    Expected_Assertions=part.get(
                        "assertions",
                        "body la JSON; khop schema thanh cong" if valid
                        else "body la JSON; co truong error"),
                    Oracle=part.get("oracle", "SPEC"),
                    SEC_Ref=part.get("sec", "-"),
                    Priority=part.get("priority", "P1" if valid else "P2"),
                    Source="AI",
                    Tag=part.get("tag", "@bug" if part.get("bug") else "@contract"),
                    Bug_Ref=part.get("bug", "-"),
                ))
    return rows


def gen_state(spec):
    rows = []
    sm = spec.get("state_machine")
    if not sm:
        return rows
    api = spec["api_id"]
    pref = spec["tc_prefix"]
    n = 0
    for t in sm.get("transitions", []):
        n += 1
        allowed = t.get("allowed", False)
        default_assert = ("trang thai sau khi goi = " + t["to"]) if allowed else (
            "body.error chua Invalid state transition; trang thai KHONG doi")
        rows.append(mk_row(
            TC_ID="TC-%s-STA-%03d" % (pref, n),
            API=api, FR=spec["fr"], Category="STA",
            Technique="State Transition",
            Title="Chuyen trang thai %s -> %s (%s)" % (
                t["from"], t["to"], "hop le" if allowed else "KHONG hop le"),
            Method=t.get("method", "PUT"),
            Endpoint=t.get("endpoint", sm.get("endpoint", "-")),
            Preconditions="Doi tuong dang o trang thai " + t["from"] + ". " + t.get("preconditions", ""),
            Request_Headers=t.get("headers", "Authorization: Bearer {{token_user}}"),
            Request_Body=jdump(t.get("body", {"status": t["to"]})),
            Expected_Status=t.get("expected_status", 200 if allowed else 400),
            Expected_Assertions=t.get("assertions", default_assert),
            Oracle=t.get("oracle", "SPEC"),
            SEC_Ref=t.get("sec", "-"),
            Priority=t.get("priority", "P0" if t.get("bug") else "P1"),
            Source="AI",
            Tag="@bug" if t.get("bug") else "@contract",
            Bug_Ref=t.get("bug", "-"),
        ))
    return rows


def gen_security(spec):
    rows = []
    api = spec["api_id"]
    pref = spec["tc_prefix"]
    n = 0
    for s in spec.get("security", []):
        n += 1
        sec = s["sec"]
        rows.append(mk_row(
            TC_ID="TC-%s-SEC-%03d" % (pref, n),
            API=api, FR=spec["fr"], Category="SEC",
            Technique=s.get("technique", "Security Testing"),
            Title="[" + sec + "] " + s["title"],
            Method=s.get("method", "POST"),
            Endpoint=s["endpoint"],
            Preconditions=s.get("preconditions", "SUT da seed"),
            Request_Headers=s.get("headers", "-"),
            Request_Body=jdump(s.get("body")),
            Expected_Status=s.get("expected_status", 400),
            Expected_Assertions=s.get("assertions", SEC_DEFAULT_ASSERT.get(sec, "-")),
            Oracle=s.get("oracle", "SPEC"),
            SEC_Ref=sec,
            Priority=s.get("priority", "P0"),
            Source="AI",
            Tag="@bug" if s.get("bug") else "@contract",
            Bug_Ref=s.get("bug", "-"),
        ))
    return rows


def gen_schema(spec):
    rows = []
    api = spec["api_id"]
    pref = spec["tc_prefix"]
    n = 0
    for sc in spec.get("schema_cases", []):
        n += 1
        rows.append(mk_row(
            TC_ID="TC-%s-SCH-%03d" % (pref, n),
            API=api, FR=spec["fr"], Category="SCH",
            Technique="JSON Schema Validation",
            Title=sc["title"],
            Method=sc.get("method", "GET"),
            Endpoint=sc["endpoint"],
            Preconditions=sc.get("preconditions", "SUT da seed"),
            Request_Headers=sc.get("headers", "-"),
            Request_Body=jdump(sc.get("body")),
            Expected_Status=sc.get("expected_status", 200),
            Expected_Assertions=sc.get(
                "assertions",
                "Content-Type application/json; body khop jsonSchema " + str(sc.get("schema_ref", "-"))),
            Oracle=sc.get("oracle", "SPEC"),
            SEC_Ref=sc.get("sec", "-"),
            Priority=sc.get("priority", "P1"),
            Source="AI",
            Tag="@bug" if sc.get("bug") else "@contract",
            Bug_Ref=sc.get("bug", "-"),
        ))
    return rows


def dedup(rows):
    """Bo case trung LAP THAT SU.

    Truoc day khoa dedup chi gom (method, endpoint, body, status) nen mot case SCH va
    mot case DOM cung goi 1 request nhung khang dinh hai thu khac han nhau bi gop lam
    mot -> mat trang case SCH (api-1 tu 6 case SCH con 1). Hai case chi la trung lap khi
    chung gui CUNG mot request VA khang dinh CUNG mot dieu, trong CUNG mot nhom ky thuat,
    VA xuat phat tu CUNG mot precondition. Precondition la bat buoc trong khoa: hai case
    "huy don dang pending" va "huy don dang confirmed" goi y het nhau (PUT /orders/:id/cancel,
    body rong) va chi phan biet duoc bang trang thai ban dau.
    """
    seen = set()
    out = []
    for r in rows:
        key = (r["Category"], r["Method"], r["Endpoint"], r["Request_Body"],
               str(r["Expected_Status"]), r["Expected_Assertions"], r["Preconditions"])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def coverage(spec, rows):
    lines = []
    cats = Counter(r["Category"] for r in rows)
    lines.append("So case theo nhom: " + ", ".join(
        "%s=%d" % (k, cats.get(k, 0)) for k in CATS))
    lines.append("Tong: %d" % len(rows))

    all_params = []
    for ep in spec["endpoints"]:
        for p in ep.get("params", []):
            all_params.append(p["name"])
    covered = set()
    for r in rows:
        if r["Category"] == "DOM":
            m = re.search(r"\| (\S+) = ", r["Title"])
            if m:
                covered.add(m.group(1))
    miss = sorted(set(all_params) - covered)
    lines.append("Tham so CHUA phu DOM: " + (", ".join(miss) if miss else "(khong)"))

    need = set("SEC-0%d" % i for i in range(1, 8))
    have = set(r["SEC_Ref"] for r in rows if str(r["SEC_Ref"]).startswith("SEC-"))
    lines.append("Ma SEC CHUA phu: " + (", ".join(sorted(need - have)) or "(du 7)"))

    sm = spec.get("state_machine")
    if sm:
        s = len(sm.get("states", []))
        lines.append("O bang chuyen trang thai da test: %d / %d" % (cats.get("STA", 0), s * s))

    if len(rows) < 35:
        lines.append("CANH BAO: chua du 35 case. Bo sung partition/transition/payload vao spec roi chay lai.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out")
    ap.add_argument("--only", choices=CATS, action="append")
    ap.add_argument("--append", action="store_true")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()

    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)
    spec.setdefault("tc_prefix", spec["api_id"].replace("API-", "A"))

    want = a.only or CATS
    rows = []
    if "DOM" in want:
        rows += gen_domain(spec)
    if "STA" in want:
        rows += gen_state(spec)
    if "SEC" in want:
        rows += gen_security(spec)
    if "SCH" in want:
        rows += gen_schema(spec)
    rows = dedup(rows)

    if a.stats or not a.out:
        print(coverage(spec, rows))
        return

    d = os.path.dirname(os.path.abspath(a.out))
    if d:
        os.makedirs(d, exist_ok=True)
    exists = os.path.exists(a.out) and a.append
    with open(a.out, "a" if exists else "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        if not exists:
            w.writeheader()
        for r in rows:
            w.writerow(r)

    with open(a.out, encoding="utf-8-sig") as f:
        total = sum(1 for _ in csv.DictReader(f))
    print("Da ghi %d case (%s) vao %s | tong file: %d" % (len(rows), "+".join(want), a.out, total))
    print(coverage(spec, rows))


if __name__ == "__main__":
    main()
