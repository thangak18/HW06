#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_submission.py - Kiem tra du deliverable truoc khi nen nop Moodle.

  python3 validate_submission.py --root . --sid 23127060

In PASS / WARN / FAIL cho tung muc theo danh sach muc 14 cua de bai.
Exit code 1 neu con muc FAIL.
"""
import argparse
import csv
import glob
import json
import os
import re

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
res = []


def chk(level, name, detail=""):
    res.append((level, name, detail))


def exists_any(root, pattern):
    return sorted(glob.glob(os.path.join(root, pattern)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--sid", default="23127060")
    a = ap.parse_args()
    R = a.root
    SID = a.sid

    # 1. Bao cao chinh MD + PDF
    md = exists_any(R, "report/MAIN_REPORT.md")
    pdf = exists_any(R, "report/MAIN_REPORT.pdf")
    chk(PASS if md else FAIL, "Bao cao chinh (report/MAIN_REPORT.md)")
    chk(PASS if pdf else FAIL, "Bao cao chinh ban PDF (report/MAIN_REPORT.pdf)")

    # 2. Link GitHub repo trong README
    readme = os.path.join(R, "README.md")
    if os.path.exists(readme):
        txt = open(readme, encoding="utf-8").read()
        has_repo = bool(re.search(r"https://github\.com/[\w.-]+/[\w.-]+", txt))
        chk(PASS if has_repo else FAIL, "README.md co link GitHub repo cong khai")
        chk(PASS if "Tu cham" in txt or "Self" in txt or "tu danh gia" in txt.lower()
            else FAIL, "README.md co bang tu danh gia")
        chk(PASS if "summary" in txt.lower() else WARN, "README.md co test summary")
    else:
        chk(FAIL, "README.md ton tai")

    # 3. Postman collections
    cols = exists_any(R, "postman/collections/*.json")
    chk(PASS if len(cols) >= 3 else FAIL,
        "Postman collection >= 3 file", "tim thay %d" % len(cols))
    for c in cols:
        try:
            d = json.load(open(c, encoding="utf-8"))
            n = sum(len(f.get("item", [])) for f in d.get("item", []))
            pre = json.dumps(d.get("event", []), ensure_ascii=False)
            ok_hdr = "X-Student-Id" in pre and SID in pre
            chk(PASS if ok_hdr else FAIL,
                "Pre-request script chen X-Student-Id (%s)" % os.path.basename(c))
            chk(PASS if "console.log" in pre else FAIL,
                "Pre-request co console.log de chup bang chung (%s)" % os.path.basename(c))
            chk(PASS if n >= 35 else WARN,
                "So request trong %s" % os.path.basename(c), "%d request" % n)
        except Exception as e:
            chk(FAIL, "Collection JSON hop le (%s)" % os.path.basename(c), str(e)[:60])

    envs = exists_any(R, "postman/environments/*.json")
    chk(PASS if envs else FAIL, "Postman environment", "%d file" % len(envs))

    data_files = exists_any(R, "postman/data/*.csv")
    chk(PASS if data_files else FAIL,
        "Data file cho data-driven run (postman/data/*.csv)", "%d file" % len(data_files))

    # 4. Newman report
    html = exists_any(R, "newman/*.html")
    js = exists_any(R, "newman/*.json")
    chk(PASS if len(html) >= 3 else FAIL, "Newman HTML report >= 3", "%d file" % len(html))
    chk(PASS if js else FAIL, "Newman JSON report", "%d file" % len(js))

    # 5. Danh sach Postman feature
    pf = os.path.join(R, "report/05_postman_features.md")
    if os.path.exists(pf):
        txt = open(pf, encoding="utf-8").read()
        n = txt.count("|") // 6
        chk(PASS, "Danh sach Postman features", "~%d dong bang" % n)
    else:
        chk(FAIL, "Danh sach Postman features (report/05_postman_features.md)")

    # 6. CI/CD
    ci = os.path.join(R, "ci/CI_CD_REPORT.md")
    chk(PASS if os.path.exists(ci) else FAIL, "Bao cao CI/CD (ci/CI_CD_REPORT.md)")
    ev = exists_any(R, "ci/evidence/*")
    chk(PASS if len(ev) >= 2 else FAIL,
        "Screenshot 2 run CI (1 pass, 1 fail)", "%d file" % len(ev))
    wf = exists_any(R, "../../.github/workflows/*%s*.yml" % SID) or \
        exists_any(R, "ci/*.yml")
    chk(PASS if wf else FAIL, "File workflow GitHub Actions")

    # 7. Excel test case
    xlsx = exists_any(R, "testcases/*.xlsx")
    chk(PASS if xlsx else FAIL, "File Excel test case (testcases/*.xlsx)")

    finals = exists_any(R, "testcases/API-*_final.csv")
    chk(PASS if len(finals) >= 3 else FAIL,
        "CSV test case final cho 3 API", "%d file" % len(finals))
    for f in finals:
        try:
            rows = list(csv.DictReader(open(f, encoding="utf-8-sig")))
            n = len(rows)
            ai = sum(1 for r in rows if r.get("Source") == "AI")
            hu = sum(1 for r in rows if r.get("Source") == "HUMAN")
            unlabeled = sum(1 for r in rows
                            if r.get("Source") == "AI" and not (r.get("Audit_Label") or "").strip())
            base = os.path.basename(f)
            chk(PASS if ai >= 35 else FAIL, "%s: >= 35 case do AI sinh" % base, "AI=%d" % ai)
            chk(PASS if hu >= 5 else FAIL, "%s: >= 5 case tu bo sung" % base, "HUMAN=%d" % hu)
            chk(PASS if unlabeled == 0 else FAIL,
                "%s: moi case AI da duoc gan nhan audit" % base,
                "con %d case chua gan nhan" % unlabeled)
            secs = set(r.get("SEC_Ref") for r in rows)
            missing = [s for s in ["SEC-0%d" % i for i in range(1, 8)] if s not in secs]
            chk(PASS if not missing else WARN,
                "%s: phu du SEC-01..07" % base, "thieu " + ",".join(missing) if missing else "")
            chk(PASS if n else FAIL, "%s: tong %d case" % (base, n))
        except Exception as e:
            chk(FAIL, "Doc duoc %s" % os.path.basename(f), str(e)[:60])

    # 8. Diagram + pseudocode
    dg = exists_any(R, "agent-skill/diagram/*.png") + \
        exists_any(R, "agent-skill/diagram/*.jpg") + \
        exists_any(R, "agent-skill/diagram/*.mmd")
    chk(PASS if dg else FAIL,
        "Diagram bo sinh test (PNG/JPG/Mermaid) - PHAI TU VE, khong dung AI")
    ps = exists_any(R, "agent-skill/pseudocode/*")
    chk(PASS if ps else FAIL, "Pseudocode bo sinh test")
    gen = exists_any(R, "agent-skill/eshop-api-*/scripts/gen_testcases.py")
    chk(PASS if gen else WARN, "Ban hien thuc bo sinh test (gen_testcases.py)")

    # 9. Bug report
    br = os.path.join(R, "bugs/BUG_REPORT.md")
    if os.path.exists(br):
        txt = open(br, encoding="utf-8").read()
        issues = len(re.findall(r"github\.com/[^\s)]+/issues/\d+", txt))
        chk(PASS, "Bug report (bugs/BUG_REPORT.md)")
        chk(PASS if issues >= 3 else FAIL, "Link GitHub Issues trong bug report",
            "%d link" % issues)
    else:
        chk(FAIL, "Bug report (bugs/BUG_REPORT.md)")
    shots = exists_any(R, "bugs/screenshots/*")
    chk(PASS if len(shots) >= 3 else FAIL,
        "Screenshot GitHub Issues + Postman Console", "%d file" % len(shots))

    # 10. AI audit + critique
    aud = os.path.join(R, "ai/audit/AI_AUDIT_REPORT.md")
    chk(PASS if os.path.exists(aud) else FAIL, "AI Audit Report (ai/audit/AI_AUDIT_REPORT.md)")
    chk(PASS if exists_any(R, "ai/audit/*.pdf") else FAIL, "AI Audit Report ban PDF")
    if os.path.exists(aud):
        t = open(aud, encoding="utf-8").read()
        chk(PASS if "I use AI tools for the following tasks" in t else WARN,
            "AI Audit co cau mo dau bat buoc cua de bai")

    log = os.path.join(R, "ai/AI_log.md")
    if os.path.exists(log):
        t = open(log, encoding="utf-8").read()
        n = len(re.findall(r"^##\s*#?\d+", t, re.M))
        chk(PASS if n >= 10 else WARN, "AI_log.md co du entry", "%d entry" % n)
    else:
        chk(FAIL, "ai/AI_log.md")

    cri = os.path.join(R, "ai/critique/AI_CRITIQUE.md")
    if os.path.exists(cri):
        words = len(open(cri, encoding="utf-8").read().split())
        chk(PASS if 200 <= words <= 300 else FAIL,
            "AI Critique dai 200-300 tu", "%d tu" % words)
    else:
        chk(FAIL, "AI Critique (ai/critique/AI_CRITIQUE.md)")
    chk(PASS if exists_any(R, "ai/critique/*.pdf") else FAIL, "AI Critique ban PDF")

    # 11. Git log
    gl = exists_any(R, "git-log/*.txt")
    if gl:
        lines = sum(1 for _ in open(gl[0], encoding="utf-8"))
        chk(PASS if lines >= 10 else WARN, "Git commit log", "%d commit" % lines)
    else:
        chk(FAIL, "Git commit log (git-log/*.txt)")

    # 12. Khong dinh file cua nguoi khac
    leak = []
    for other in ("23127195", "23127259", "member-1", "member-2", "member-3"):
        leak += exists_any(R, "**/*%s*" % other)
    chk(PASS if not leak else FAIL,
        "Khong lan file cua thanh vien khac", ", ".join(leak[:3]))

    # in ket qua
    order = {FAIL: 0, WARN: 1, PASS: 2}
    res.sort(key=lambda x: order[x[0]])
    print("=" * 78)
    print("KIEM TRA BAI NOP HW06 - SV %s" % SID)
    print("=" * 78)
    for lv, name, detail in res:
        print("[%s] %s%s" % (lv, name, ("  -> " + detail) if detail else ""))
    n_fail = sum(1 for r in res if r[0] == FAIL)
    n_warn = sum(1 for r in res if r[0] == WARN)
    n_pass = sum(1 for r in res if r[0] == PASS)
    print("-" * 78)
    print("PASS=%d  WARN=%d  FAIL=%d" % (n_pass, n_warn, n_fail))
    if n_fail:
        print("CHUA DUOC NOP: con %d muc FAIL. De bai: thieu tai lieu bat buoc = 0 diem." % n_fail)
    else:
        print("OK. Nen nop: cd .. && zip -r %s_HW06_AI_API_<3 chu so>.zip %s/ -x '*/.git/*'" % (SID, SID))
    raise SystemExit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
