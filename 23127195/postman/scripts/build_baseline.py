#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_baseline.py — Sinh collection "regression baseline" dung lam CONG CHAN cho CI/CD

Van de: SUT hien co 24 khiem khuyet, nen chay toan bo 144 test case thi pipeline
LUON do. Mot pipeline luon do khong con gia tri canh bao — lap trinh vien se quen
nhin no. Day la ly do dung mo hinh hai tang:

  Tang 1 — BASELINE (bat buoc xanh):
      Chi gom cac test case HIEN DANG DAT, liet ke tuong minh trong
      `ci/baseline_allowlist.json`. Neu mot trong so chung chuyen sang do thi
      nghia la vua co HOI QUY -> pipeline phai do.

  Tang 2 — FULL SUITE (thong tin tham khao):
      Chay ca 144 test case, khong chan build. Bao cao duoc luu lam artifact de
      theo doi tien do sua loi theo thoi gian.

Khi mot khiem khuyet duoc sua, test case tuong ung duoc them vao allowlist va tu
do tro thanh mot phan cua cong chan — bao ve viec sua do khoi bi pha vo lan sau.

Usage:
    python postman/scripts/build_baseline.py                  # dung allowlist san co
    python postman/scripts/build_baseline.py --refresh        # cap nhat allowlist tu
                                                              # ket qua Newman moi nhat
"""

import glob
import io
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TC_DIR = os.path.join(ROOT, "testcases")
OUT_DIR = os.path.join(ROOT, "postman", "collections")
NEWMAN_DIR = os.path.join(ROOT, "newman")
ALLOWLIST = os.path.join(ROOT, "ci", "baseline_allowlist.json")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collections import build_collection  # noqa: E402


def passing_ids_from_newman():
    """Doc bao cao Newman moi nhat -> tap ID cac test case dat toan bo assertion."""
    passed, failed = set(), set()
    for key in ("api1", "api2", "api3"):
        files = sorted(glob.glob(os.path.join(NEWMAN_DIR, "%s_*.json" % key)))
        if not files:
            continue
        with io.open(files[-1], encoding="utf-8") as f:
            run = json.load(f)["run"]
        bad = {fa.get("source", {}).get("name", "").split()[0]
               for fa in run.get("failures", [])}
        for ex in run.get("executions", []):
            tc = ex["item"]["name"].split()[0]
            (failed if tc in bad else passed).add(tc)
    return passed - failed, failed


def refresh_allowlist():
    passed, failed = passing_ids_from_newman()
    if not passed:
        print("Khong doc duoc ket qua Newman nao trong %s" % NEWMAN_DIR, file=sys.stderr)
        return None
    data = {
        "_mo_ta": ("Danh sach test case DANG DAT, dung lam cong chan hoi quy cho CI/CD. "
                   "Mot test case o day chuyen sang FAIL nghia la co hoi quy -> pipeline phai do. "
                   "Khi mot khiem khuyet duoc sua, hay them test case tuong ung vao day."),
        "_cap_nhat": "sinh boi build_baseline.py --refresh",
        "_so_luong": len(passed),
        "test_case_dat": sorted(passed),
        "_test_case_dang_do": sorted(failed),
    }
    os.makedirs(os.path.dirname(ALLOWLIST), exist_ok=True)
    with io.open(ALLOWLIST, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print("[allowlist] cap nhat: %d test case dat, %d dang do" % (len(passed), len(failed)))
    return set(passed)


def load_allowlist():
    if not os.path.exists(ALLOWLIST):
        return None
    with io.open(ALLOWLIST, encoding="utf-8") as f:
        return set(json.load(f)["test_case_dat"])


def main():
    if "--refresh" in sys.argv:
        allow = refresh_allowlist()
    else:
        allow = load_allowlist()
        if allow is None:
            print("Chua co %s — chay lai voi --refresh" % ALLOWLIST, file=sys.stderr)
            return 1
        print("[allowlist] doc %d test case tu ci/baseline_allowlist.json" % len(allow))

    total_kept = 0
    for fname in sorted(os.listdir(TC_DIR)):
        if not fname.endswith("_testcases.json"):
            continue
        with io.open(os.path.join(TC_DIR, fname), encoding="utf-8") as f:
            spec = json.load(f)

        kept = [c for c in spec["cases"] if c.get("setup") or c["id"] in allow]
        n_real = sum(1 for c in kept if not c.get("setup"))
        total_kept += n_real

        spec["cases"] = kept
        spec["collection_file"] = "baseline_" + spec["collection_file"]
        spec["description"] = (
            "CONG CHAN HOI QUY (CI/CD) — %s %s.\n\n"
            "Chi gom cac test case hien dang DAT, liet ke trong ci/baseline_allowlist.json. "
            "Collection nay PHAI xanh. Mot test case chuyen sang do nghia la co hoi quy.\n\n"
            "Sinh tu dong boi postman/scripts/build_baseline.py — dung sua tay."
            % (spec["api_id"], spec["fr"]))

        col = build_collection(spec)
        col["info"]["name"] = "HW06 - 23127195 - BASELINE - %s (%s)" % (spec["api_id"], spec["fr"])
        out = os.path.join(OUT_DIR, spec["collection_file"])
        with io.open(out, "w", encoding="utf-8", newline="") as f:
            f.write(json.dumps(col, ensure_ascii=False, indent=2) + "\n")
        print("[OK] %-52s %3d test case (+%d setup)"
              % (os.path.basename(out), n_real, len(kept) - n_real))

    print("Tong cong chan: %d test case" % total_kept)
    return 0


if __name__ == "__main__":
    sys.exit(main())
