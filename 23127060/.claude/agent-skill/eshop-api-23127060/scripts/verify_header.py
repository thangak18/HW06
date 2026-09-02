#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_header.py - Chung minh header X-Student-Id co mat tren MOI request da gui.

  python3 verify_header.py --dir newman --sid 23127060 --out ci/evidence/header_evidence.md

De bai muc 11 (chong gian lan) doi bang chung cho header `X-Student-Id: {StudentID}`, va noi
ro bang chung do la anh chup Postman Console. Anh chup thi khong kiem chung tu dong duoc, va
mot dong console.log chi chung minh script DA CHAY chu chua chung minh header DA DUOC GUI.

Script nay doc thang phan `request.header` ma Newman ghi lai cho tung request that su roi
len duong, nen no tra loi dung cau hoi: co bao nhieu request mang header, gia tri la gi, va
co request nao thieu khong. Anh chup Console van duoc nop kem, nhung day moi la bang chung
kiem chung lai duoc.
"""
import argparse
import collections
import glob
import gzip
import io
import json
import os


def load(path):
    op = gzip.open if path.endswith(".gz") else io.open
    with op(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="newman")
    ap.add_argument("--sid", default="23127060")
    ap.add_argument("--out", default="ci/evidence/header_evidence.md")
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.dir, "*.json")) + glob.glob(os.path.join(a.dir, "*.json.gz")))
    L = ["# Bang chung header `X-Student-Id: %s`" % a.sid, "",
         "> HW06 — SV **Ninh Van Khai — %s** | De bai muc 11 (chong gian lan)" % a.sid, "",
         "Sinh tu `agent-skill/eshop-api-23127060/scripts/verify_header.py`, doc thang phan",
         "`request.header` ma Newman ghi lai cho **tung request that su roi len duong**.", "",
         "| Bao cao Newman | Request da gui | Co header | Thieu header | Gia tri |",
         "|---|---|---|---|---|"]
    tong = collections.Counter()
    sai = []
    for f in files:
        d = load(f)
        co = thieu = 0
        vals = collections.Counter()
        for e in d["run"]["executions"]:
            hs = {h["key"].lower(): h["value"] for h in e["request"].get("header", [])}
            if "x-student-id" in hs:
                co += 1
                vals[hs["x-student-id"]] += 1
                if hs["x-student-id"] != a.sid:
                    sai.append((os.path.basename(f), e["item"]["name"], hs["x-student-id"]))
            else:
                thieu += 1
                sai.append((os.path.basename(f), e["item"]["name"], "(thieu)"))
        L.append("| `%s` | %d | %d | %d | %s |"
                 % (os.path.basename(f), co + thieu, co, thieu,
                    ", ".join("`%s` x%d" % (k, v) for k, v in vals.items()) or "—"))
        tong["co"] += co
        tong["thieu"] += thieu
    L.append("| **Tong** | **%d** | **%d** | **%d** | |"
             % (tong["co"] + tong["thieu"], tong["co"], tong["thieu"]))
    L += ["",
          "**Ket luan: %d/%d request mang header `X-Student-Id: %s`.**"
          % (tong["co"], tong["co"] + tong["thieu"], a.sid), ""]
    if sai:
        L += ["## Request co van de", "", "| Bao cao | Request | Gia tri |", "|---|---|---|"]
        for f, n, v in sai[:50]:
            L.append("| `%s` | %s | %s |" % (f, n[:60], v))
    else:
        L += ["Khong co request nao thieu header hoac mang gia tri khac.", ""]
    L += ["", "## Header duoc chen o dau", "",
          "Trong pre-request script cap **collection** (ap cho moi request, khong the quen):", "",
          "```javascript",
          'const STUDENT_ID = pm.environment.get("studentId") || "%s";' % a.sid,
          'pm.request.headers.upsert({ key: "X-Student-Id", value: STUDENT_ID });',
          'pm.request.headers.upsert({ key: "Accept", value: "application/json" });',
          "",
          "console.log(",
          '  "[HW06][" + STUDENT_ID + "] " +',
          '  pm.request.method + " " + pm.request.url.toString() +',
          '  " | X-Student-Id=" + STUDENT_ID +',
          '  " | " + new Date().toISOString()',
          ");",
          "```", "",
          "Dong `console.log` tren duoc Newman giu lai trong bao cao HTML nho co",
          "`--reporter-htmlextra-logs`, nen bao cao HTML vua la ket qua vua la bang chung."]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("Da ghi %s | %d/%d request co header dung"
          % (a.out, tong["co"], tong["co"] + tong["thieu"]))


if __name__ == "__main__":
    main()
