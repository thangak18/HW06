#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""summarize_newman.py - Doc cac file newman/*.json va sinh bang tong hop ket qua.

  python3 summarize_newman.py --dir newman --out report/06_execution.md

Sinh: bang tong hop moi API + danh sach case FAIL kem ly do, tach ro
"expected failure (@bug)" va "failure that su".
Chi dung thu vien chuan.
"""
import argparse
import glob
import json
import os
import re


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def summarize_one(path):
    d = load(path)
    run = d.get("run", {})
    stats = run.get("stats", {})
    timings = run.get("timings", {})
    execs = run.get("executions", [])

    failures = []
    for e in execs:
        name = (e.get("item", {}) or {}).get("name", "?")
        for a in e.get("assertions", []) or []:
            if a.get("error"):
                failures.append({
                    "item": name,
                    "assertion": a.get("assertion", ""),
                    "message": (a.get("error", {}) or {}).get("message", ""),
                    "expected_bug": "@bug" in name,
                })

    m = re.search(r"_(API-\d)_", os.path.basename(path))
    return {
        "file": os.path.basename(path),
        "api": m.group(1) if m else "?",
        "requests": (stats.get("requests", {}) or {}).get("total", 0),
        "assertions_total": (stats.get("assertions", {}) or {}).get("total", 0),
        "assertions_failed": (stats.get("assertions", {}) or {}).get("failed", 0),
        "duration_ms": timings.get("completed", 0) - timings.get("started", 0)
        if timings.get("completed") else 0,
        "failures": failures,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="newman")
    ap.add_argument("--out", default="report/06_execution.md")
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.dir, "*.json")))
    if not files:
        raise SystemExit("Khong tim thay file newman/*.json. Chay run_newman.sh truoc.")

    rs = [summarize_one(f) for f in files]

    L = []
    L.append("# 6. Ket qua thuc thi (Newman)")
    L.append("")
    L.append("SV: Ninh Van Khai - 23127060")
    L.append("")
    L.append("## 6.1 Bang tong hop")
    L.append("")
    L.append("| File | API | Request | Assertion | Failed | Passed | Ty le pass | Thoi gian |")
    L.append("|---|---|---|---|---|---|---|---|")
    tot_a = tot_f = 0
    for r in rs:
        passed = r["assertions_total"] - r["assertions_failed"]
        rate = (100.0 * passed / r["assertions_total"]) if r["assertions_total"] else 0
        tot_a += r["assertions_total"]
        tot_f += r["assertions_failed"]
        L.append("| %s | %s | %d | %d | %d | %d | %.1f%% | %.1fs |" % (
            r["file"], r["api"], r["requests"], r["assertions_total"],
            r["assertions_failed"], passed, rate, r["duration_ms"] / 1000.0))
    L.append("| **TONG** | | | **%d** | **%d** | **%d** | **%.1f%%** | |" % (
        tot_a, tot_f, tot_a - tot_f,
        (100.0 * (tot_a - tot_f) / tot_a) if tot_a else 0))
    L.append("")

    L.append("## 6.2 Cac assertion FAIL")
    L.append("")
    L.append("> Case gan tag `@bug` FAIL la **dung y do**: no phoi bay loi cua SUT.")
    L.append("> Case `@contract` ma FAIL moi la van de cua bo test.")
    L.append("")
    exp = [f for r in rs for f in r["failures"] if f["expected_bug"]]
    unexp = [f for r in rs for f in r["failures"] if not f["expected_bug"]]

    L.append("### a) Expected failure - phoi bay bug SUT (%d)" % len(exp))
    L.append("")
    if exp:
        L.append("| Test case | Assertion | Thong diep |")
        L.append("|---|---|---|")
        for f in exp:
            L.append("| %s | %s | %s |" % (
                f["item"][:70], f["assertion"][:60], f["message"][:80].replace("|", "/")))
    else:
        L.append("(khong co)")
    L.append("")

    L.append("### b) Unexpected failure - can dieu tra (%d)" % len(unexp))
    L.append("")
    if unexp:
        L.append("| Test case | Assertion | Thong diep |")
        L.append("|---|---|---|")
        for f in unexp:
            L.append("| %s | %s | %s |" % (
                f["item"][:70], f["assertion"][:60], f["message"][:80].replace("|", "/")))
    else:
        L.append("(khong co - tot)")
    L.append("")

    L.append("## 6.3 Bang chung")
    L.append("")
    for r in rs:
        L.append("- `newman/%s` va ban HTML tuong ung" % r["file"])
    L.append("- `bugs/screenshots/postman_console_X-Student-Id.png` (chup tay - HUMAN H4)")
    L.append("")

    d = os.path.dirname(os.path.abspath(a.out))
    if d:
        os.makedirs(d, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("Da ghi %s (%d file newman, %d assertion, %d failed)" % (
        a.out, len(rs), tot_a, tot_f))


if __name__ == "__main__":
    main()
