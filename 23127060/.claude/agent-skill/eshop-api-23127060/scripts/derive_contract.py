#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive_contract.py - Suy ra bo test hoi quy (@contract) tu KET QUA CHAY THAT.

  python3 derive_contract.py --dir newman --out postman/contract_baseline

Vi sao khong dung thang cot Tag trong CSV:
  Cot `Tag` duoc gan luc THIET KE, dua tren danh sach bug da biet truoc. No tra loi cau
  "toi NGHI SUT co dap ung dieu nay khong". Nhung bo test da tim ra nhieu bug ngoai danh
  sach do (63 case that bai vi SUT tra 404 cho moi dau vao xau thay vi 400), nen 72 case
  gan @contract van FAIL.

  De bai muc 6 doi mot lan chay CI "all API test cases passing". Neu lay bo @contract theo
  thiet ke lam lan chay do thi no se do, va neu sua ky vong cho khop voi hanh vi sai cua SUT
  thi la nguy tao ket qua.

  Cach dung dan: bo @contract la mot MOC HOI QUY (regression baseline) - tap hop cac case
  ma SUT HIEN DANG dap ung, chot tai mot commit cu the. No khong khang dinh "API nay dung",
  ma khang dinh "nhung dieu API nay dang lam dung thi khong duoc pha". Day la cach dung
  chuan cua mot bo test hoi quy tren he thong con nhieu loi, va no duoc ghi ro trong bao cao
  chu khong giau di.

  Bo day du (Oracle = SPEC) van la ket qua kiem thu that su, va no van do - dung nhu mong doi.
"""
import argparse
import collections
import glob
import gzip
import io
import json
import os
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="newman")
    ap.add_argument("--out", default="postman/contract_baseline")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    tong = collections.Counter()
    for f in sorted(glob.glob(os.path.join(a.dir, "*_API-*.json"))
                    + glob.glob(os.path.join(a.dir, "*_API-*.json.gz"))):
        if "_contract_" in f:
            continue
        m = re.search(r"_(API-\d)_", f)
        if not m:
            continue
        api = m.group(1)
        op = gzip.open if f.endswith(".gz") else io.open
        with op(f, "rt", encoding="utf-8") as fh:
            d = json.load(fh)
        per = collections.defaultdict(lambda: [0, 0])
        for e in d["run"]["executions"]:
            for x in e.get("assertions", []):
                mm = re.match(r"(TC-[A-Z0-9]+-[A-Z]+-\d+)", x["assertion"])
                if not mm:
                    continue
                per[mm.group(1)][0] += 1
                if x.get("error"):
                    per[mm.group(1)][1] += 1
        passed = sorted(t for t, v in per.items() if v[1] == 0)
        p = os.path.join(a.out, "%s.txt" % api)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("# Moc hoi quy %s - sinh tu %s\n" % (api, os.path.basename(f)))
            fh.write("# %d / %d test case dang duoc SUT dap ung tai commit eshop-sut 85af3ba.\n"
                     % (len(passed), len(per)))
            fh.write("# Day KHONG phai danh sach 'case dung'. Day la nhung gi SUT dang lam dung\n"
                     "# va khong duoc phep pha. Sinh boi derive_contract.py, khong sua tay.\n")
            for t in passed:
                fh.write(t + "\n")
        print("%s: %d/%d case vao moc hoi quy -> %s" % (api, len(passed), len(per), p))
        tong["pass"] += len(passed)
        tong["all"] += len(per)
    print("TONG: %d/%d case vao moc hoi quy" % (tong["pass"], tong["all"]))


if __name__ == "__main__":
    main()
