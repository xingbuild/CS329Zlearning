#!/bin/bash
# ============================================================
#  精读页双态构建（AGENTS.md §4.1 版权红线的工程化）
#    bash scripts/build.sh        → 摘录模式（默认，CI/公网用）
#    FULL=1 bash scripts/build.sh → 全文模式（本地学习用）
#  机制：FULL=1 且存在 readings/*/full.md 时，临时以其替换 index.md
#        构建完成（或出错）后还原——full.md 永不入库不上网。
# ============================================================
set -e
cd "$(dirname "$0")/.." || exit 1

replaced=()
restore() {
  for f in "${replaced[@]}"; do
    [ -f "$f.bak" ] && mv "$f.bak" "$f"
  done
}
trap restore EXIT

if [ -n "$FULL" ]; then
  for full in l*/readings/*/full.md; do
    [ -f "$full" ] || continue
    idx="$(dirname "$full")/index.md"
    if [ -f "$idx" ]; then
      cp "$idx" "$idx.bak"
      cp "$full" "$idx"
      replaced+=("$idx")
      echo "· 全文模式：$(dirname "$full")"
    fi
  done
  [ ${#replaced[@]} -eq 0 ] && echo "· 全文模式：未发现 full.md（只有摘录源）"
else
  echo "· 摘录模式（公网默认；本地全文请 FULL=1）"
fi

npx vitepress build
