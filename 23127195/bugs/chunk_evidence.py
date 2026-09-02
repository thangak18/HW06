#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chunk_evidence.py — Cat bang chung cua tung ma loi thanh cac phan vua mot man hinh

Man hinh lam bai la 1280x800, cua so terminal chua duoc khoang 24 dong. Vai ma
loi co ban ghi dai hon the (nhieu lenh curl noi tiep). Script nay cat chung
thanh nhieu phan de moi anh chup deu doc duoc tron ven, thay vi thu nho chu
den muc khong doc noi.

Nguyen tac cat:
  - Chi cat o ranh gioi GIUA hai lenh (dong bat dau bang "$ "), khong bao gio
    cat doi mot lenh hay tach lenh khoi response cua no.
  - Moi phan deu mang lai 3 dong meta va dong tieu de "### BUG-..." de tung
    anh tu no da noi ro dang xem ma loi nao.

Ket qua: bugs/evidence/per_bug/chunks/<MA-LOI>.partN.txt

Usage:
    python bugs/chunk_evidence.py
"""

import io
import math
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "bugs", "evidence", "per_bug")
OUT = os.path.join(SRC, "chunks")

WRAP = 80          # so cot cua so terminal
MAX_ROWS = 22      # so dong hien thi toi da moi anh (sau khi da xuong dong)


def rows(line):
    """So dong man hinh mot dong van ban chiem sau khi xuong dong o WRAP cot."""
    return max(1, math.ceil(len(line) / float(WRAP)))


def split_blocks(body):
    """Gom than ban ghi thanh cac khoi khong the tach: moi lenh + output cua no."""
    blocks, cur = [], []
    for line in body:
        # dong bat dau mot lenh moi -> chot khoi truoc do
        if line.startswith("$ ") and cur:
            blocks.append(cur)
            cur = [line]
        else:
            cur.append(line)
    if cur:
        blocks.append(cur)
    return blocks


def chunk(bug, path):
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().rstrip("\n").split("\n")

    meta = lines[:3]                       # SUT / thoi diem / student id
    rest = lines[3:]

    # tach dong tieu de "### BUG-..." ra lam dau de cua moi phan
    head_idx = next((i for i, l in enumerate(rest) if l.startswith("###")), None)
    if head_idx is None:
        header, body = [], rest
    else:
        header = [rest[head_idx]]
        body = rest[head_idx + 1:]

    fixed = sum(rows(l) for l in meta + header) + 2      # 2 dong trong ngan cach
    budget = MAX_ROWS - fixed

    parts, cur, used = [], [], 0
    for blk in split_blocks(body):
        cost = sum(rows(l) for l in blk)
        if cur and used + cost > budget:
            parts.append(cur)
            cur, used = [], 0
        cur.extend(blk)
        used += cost
    if cur:
        parts.append(cur)

    written = []
    for i, part in enumerate(parts, 1):
        tag = "" if len(parts) == 1 else "   (phan %d/%d)" % (i, len(parts))
        text = meta + [""] + [header[0] + tag if header else ""] + part
        name = "%s.part%d.txt" % (bug, i)
        with io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(text).rstrip("\n") + "\n")
        written.append(name)
    return written


def main():
    if not os.path.isdir(SRC):
        sys.exit("Chua co %s — chay `python bugs/split_evidence.py` truoc" % SRC)
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for f in os.listdir(OUT):
        if f.endswith(".txt"):
            os.remove(os.path.join(OUT, f))

    total, multi = 0, []
    for f in sorted(os.listdir(SRC)):
        if not f.endswith(".txt"):
            continue
        bug = f[:-4]
        names = chunk(bug, os.path.join(SRC, f))
        total += len(names)
        if len(names) > 1:
            multi.append("%s (%d phan)" % (bug, len(names)))

    print("Da tao %d file anh can chup, tu 24 ma loi." % total)
    if multi:
        print("Cac ma loi phai cat lam nhieu phan:")
        for m in multi:
            print("  -", m)


if __name__ == "__main__":
    main()
