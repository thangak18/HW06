#!/usr/bin/env bash
# restructure.sh - Doi ten members/member-N -> members/<MSSV> va cai dat goi skill cho 23127060.
#
# DA LOI THOI: nhom da chot bo han `members/`, dua thu muc thanh vien len goc repo.
# Script nay da thi hanh xong va KHONG CAN CHAY LAI. Giu lai lam ghi chep.
# Xem RESTRUCTURE.md.
#
# Chay tai REPO ROOT (thu muc HW06/):
#   bash restructure.sh --dry-run          # xem truoc, khong sua gi
#   bash restructure.sh                    # thuc hien
#   bash restructure.sh --me member-2      # neu ban khong phai member-1
#
set -uo pipefail

DRY=0
ME="member-1"
SID="23127060"
MATE1="23127195"
MATE2="23127259"

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --me) ME="$2"; shift ;;
    --sid) SID="$2"; shift ;;
    *) echo "Tham so la: $1"; exit 1 ;;
  esac
  shift
done

run() {
  if [ "$DRY" = "1" ]; then echo "  [dry] $*"; else eval "$@"; fi
}

if [ ! -d "members" ]; then
  echo "[LOI] khong thay thu muc members/. Hay chay script nay tai repo root (HW06/)."
  exit 1
fi

echo "== B1. Doi ten thu muc thanh vien theo MSSV =="
map_from=("member-1" "member-2" "member-3")
map_to=("$SID" "$MATE1" "$MATE2")
# neu ban khong phai member-1 thi hoan doi cho dung
if [ "$ME" = "member-2" ]; then map_to=("$MATE1" "$SID" "$MATE2"); fi
if [ "$ME" = "member-3" ]; then map_to=("$MATE1" "$MATE2" "$SID"); fi

for i in 0 1 2; do
  f="members/${map_from[$i]}"
  t="members/${map_to[$i]}"
  if [ -d "$f" ]; then
    if [ -d "$t" ]; then
      echo "  [skip] $t da ton tai"
    elif git rev-parse --git-dir >/dev/null 2>&1; then
      run "git mv '$f' '$t'"
      echo "  [ok] git mv $f -> $t"
    else
      run "mv '$f' '$t'"
      echo "  [ok] mv $f -> $t (khong phai git repo)"
    fi
  else
    echo "  [skip] khong thay $f"
  fi
done

MY="members/$SID"

echo "== B2. Tao them cac thu muc con can thiet cho $SID =="
for d in "agent-skill/eshop-api-$SID/references" "agent-skill/eshop-api-$SID/scripts" \
         "ai/interactions" "spec" "postman/scripts/schemas" "_sample_output"; do
  run "mkdir -p '$MY/$d'"
  echo "  [ok] $MY/$d"
done

echo "== B3. Dat workflow CI vao dung cho =="
run "mkdir -p .github/workflows"
if [ -f "$MY/ci/api-tests-$SID.yml" ]; then
  run "cp '$MY/ci/api-tests-$SID.yml' '.github/workflows/api-tests-$SID.yml'"
  echo "  [ok] .github/workflows/api-tests-$SID.yml"
else
  echo "  [warn] chua thay $MY/ci/api-tests-$SID.yml (copy tu goi skill vao truoc)"
fi

echo "== B4. Cai skill cho Claude CLI =="
if [ -d "$MY/agent-skill/eshop-api-$SID" ]; then
  run "mkdir -p .claude/skills"
  run "rm -rf '.claude/skills/eshop-api-$SID'"
  run "cp -r '$MY/agent-skill/eshop-api-$SID' '.claude/skills/eshop-api-$SID'"
  echo "  [ok] .claude/skills/eshop-api-$SID (Claude Code se tu nap)"
fi

echo "== B5. Bo sung .gitignore =="
if [ "$DRY" = "0" ]; then
  touch .gitignore
  for p in "node_modules/" "__pycache__/" "*.pyc" ".DS_Store" "*.sqlite-journal" "/tmp/"; do
    grep -qxF "$p" .gitignore 2>/dev/null || echo "$p" >> .gitignore
  done
fi
echo "  [ok] .gitignore"

echo ""
echo "== XONG =="
echo "Cay thu muc cua ban: $MY"
echo ""
echo "Buoc tiep theo:"
echo "  git add -A"
echo "  git commit -m 'HW06: doi ten thu muc theo MSSV + cai goi agent-skill cho $SID'"
echo ""
echo "Lenh nop bai sau nay:"
echo "  cd members && zip -r ${SID}_HW06_AI_API_001.zip $SID/ -x '*/node_modules/*' '*/.git/*' '*/__pycache__/*'"
