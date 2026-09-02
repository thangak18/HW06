#!/usr/bin/env bash
# =============================================================================
# capture_screenshots.sh — Tro giup chup 24 anh loi cho GitHub Issues
#
# De bai muc 6 yeu cau moi issue kem mot anh chup. Script nay khong chup thay
# ban — no chi don tung doan bang chung THAT ra man hinh, moi lan mot loi, de
# ban chi viec bam Win+Shift+S roi luu. Tinh ra khoang 20-30 giay moi loi.
#
# Chuan bi mot lan:
#     bash bugs/reproduce_bugs.sh > bugs/evidence/reproduce_output.txt
#     python bugs/split_evidence.py
#
# Chay:
#     bash bugs/capture_screenshots.sh              # ca 24 loi
#     bash bugs/capture_screenshots.sh BUG-A2-03    # chi mot loi
#
# Voi moi loi: chup vung cua so terminal, luu thanh
#     bugs/screenshots/<MA-LOI>.png
# Ten file phai dung y het ma loi thi buoc dinh vao issue moi tu dong duoc.
# =============================================================================

set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/bugs/evidence/per_bug"
DEST="$ROOT/bugs/screenshots"

if [ ! -d "$SRC" ]; then
    echo "Chua co $SRC — chay truoc:  python bugs/split_evidence.py" >&2
    exit 1
fi
mkdir -p "$DEST"

if [ $# -gt 0 ]; then
    files=""
    for b in "$@"; do files="$files $SRC/$b.txt"; done
else
    files="$(ls "$SRC"/*.txt)"
fi

total=$(echo $files | wc -w)
i=0
for f in $files; do
    bug="$(basename "$f" .txt)"
    i=$((i + 1))

    clear
    echo "==============================================================================="
    printf "  [%d/%d]  %s\n" "$i" "$total" "$bug"
    echo "  Chup xong luu thanh:  bugs/screenshots/$bug.png"
    echo "==============================================================================="
    echo
    cat "$f"
    echo
    echo "-------------------------------------------------------------------------------"
    if [ -f "$DEST/$bug.png" ]; then
        echo "  (da co anh cho ma loi nay — Enter de bo qua, hoac chup de ghi de)"
    fi
    printf "  Bam Win+Shift+S de chup, luu xong bam Enter de sang loi tiep theo... "
    read -r _ < /dev/tty
done

clear
echo "Xong. Kiem tra lai:"
ls -1 "$DEST"/*.png 2>/dev/null | wc -l | xargs printf "  da co %s anh trong bugs/screenshots/\n"
echo
echo "Thieu anh cho cac ma loi sau:"
missing=0
for f in "$SRC"/*.txt; do
    bug="$(basename "$f" .txt)"
    [ -f "$DEST/$bug.png" ] || { echo "  - $bug"; missing=$((missing + 1)); }
done
[ "$missing" -eq 0 ] && echo "  (khong thieu cai nao)"
