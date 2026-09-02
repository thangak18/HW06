#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_evidence.py — Tach output cua reproduce_bugs.sh thanh tung file theo ma loi

Dung de moi GitHub Issue co mot doan bang chung rieng, thay vi bat nguoi doc
tu do trong file 145 dong.

Tieu de trong script tai hien co dang:
    ### BUG-A1-01 [Critical] SEC-06 - ...
    ### BUG-A2-04/05 [High] ...          <- mot muc phu HAI ma loi

Muc gop se duoc ghi ra ca hai file, vi hai loi do chi tai hien duoc cung nhau.

Usage:
    bash bugs/reproduce_bugs.sh > bugs/evidence/reproduce_output.txt
    python bugs/split_evidence.py
"""

import io
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "bugs", "evidence", "reproduce_output.txt")
OUTDIR = os.path.join(ROOT, "bugs", "evidence", "per_bug")

# "### BUG-A2-04/05 [High] ..."  ->  tien to "BUG-A2-", cac so "04", "05"
HEADER = re.compile(r"^###\s+(BUG-A(\d)-)(\d{2}(?:/\d{2})*)\s")


def bug_ids(prefix, numbers):
    """BUG-A2- + '04/05' -> ['BUG-A2-04', 'BUG-A2-05']"""
    return [prefix + n for n in numbers.split("/")]


def main():
    if not os.path.exists(SRC):
        sys.exit("Chua co %s — chay `bash bugs/reproduce_bugs.sh` truoc" % SRC)

    with io.open(SRC, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    # gom cac dong thuoc ve tung muc
    sections = []          # [(danh_sach_ma_loi, [dong...])]
    current = None
    for line in lines:
        m = HEADER.match(line)
        if m:
            current = (bug_ids(m.group(1), m.group(3)), [line])
            sections.append(current)
        elif current is not None:
            # duong ke ngang la ranh gioi giua hai muc
            if set(line.strip()) == {"-"} and len(line.strip()) > 10:
                current = None
            else:
                current[1].append(line)

    if not sections:
        sys.exit("Khong tim thay muc nao dang '### BUG-...' trong %s" % SRC)

    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)

    header = lines[:4]     # 4 dong dau: SUT, thoi diem, student id
    written = []
    for ids, body in sections:
        # bo cac dong trong o cuoi muc
        while body and not body[-1].strip():
            body.pop()
        for bug in ids:
            path = os.path.join(OUTDIR, bug + ".txt")
            with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(header) + "\n\n" + "\n".join(body) + "\n")
            written.append(bug)

    print("Da ghi %d file vao bugs/evidence/per_bug/" % len(written))
    missing = [b for b in expected_bugs() if b not in written]
    if missing:
        print("CANH BAO: chua co bang chung cho %d ma loi: %s"
              % (len(missing), ", ".join(missing)))
    else:
        print("Du ca 24 ma loi.")


def expected_bugs():
    """24 ma loi theo bugs/BUG_REPORTS.md"""
    return (["BUG-A1-%02d" % i for i in range(1, 6)]
            + ["BUG-A2-%02d" % i for i in range(1, 9)]
            + ["BUG-A3-%02d" % i for i in range(1, 12)])


if __name__ == "__main__":
    main()
