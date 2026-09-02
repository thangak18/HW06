#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_submission.py — Dong goi bai nop HW06 theo dung muc 14 cua de bai

Ten file tuan theo <StudentID>_HW06_AI_API_<SelfAssessedGrade>.zip

Zip giu nguyen cau truc thu muc cua repo thay vi go phang, de moi link tuong
doi trong bao cao van tro dung cho khi giai nen — vi du ci/CI_CD_REPORT.md tro
toi ../../.github/workflows/, va docs/01_API_SELECTION.md tro toi
../../docs/team-api-allocation.md.

Usage:
    python scripts/build_submission.py ..        # diem mac dinh 100
    python scripts/build_submission.py .. 093    # doi diem tu danh gia
"""

import os
import sys
import zipfile

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
GRADE = sys.argv[2] if len(sys.argv) > 2 else "100"
OUT = os.path.join(ROOT, "23127195_HW06_AI_API_%s.zip" % GRADE)

SKIP_DIRS = {"node_modules", "__pycache__", ".git", ".pytest_cache", ".venv", "venv"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}

# Giu nguyen cau truc repo de moi link tuong doi trong bao cao van tro dung cho:
#   23127195/ci/CI_CD_REPORT.md       -> ../../.github/workflows/...
#   23127195/docs/01_API_SELECTION.md -> ../../docs/team-api-allocation.md
INCLUDE = [
    "23127195",
    os.path.join(".github", "workflows", "newman-23127195.yml"),
    os.path.join("docs", "team-api-allocation.md"),
    "README.md",
]


def walk(target):
    p = os.path.join(ROOT, target)
    if os.path.isfile(p):
        yield p
        return
    for dirpath, dirnames, filenames in os.walk(p):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f in SKIP_FILES or f.endswith(".pyc"):
                continue
            yield os.path.join(dirpath, f)


def main():
    if os.path.exists(OUT):
        os.remove(OUT)
    n = total = 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for target in INCLUDE:
            for full in walk(target):
                rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
                z.write(full, rel)
                n += 1
                total += os.path.getsize(full)
    print("File nop : %s" % os.path.basename(OUT))
    print("So file  : %d" % n)
    print("Goc      : %.1f MB" % (total / 1024.0 / 1024))
    print("Sau nen  : %.1f MB" % (os.path.getsize(OUT) / 1024.0 / 1024))


if __name__ == "__main__":
    main()
