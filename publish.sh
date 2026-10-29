#!/bin/bash
# ============================================================
#  发布命令：pub（别名指向本脚本）
#  用法：pub "更新说明"          → 自动升末位版本号
#        pub 0.7.0 "更新说明"    → 指定版本号
#  行为：收编未提交变更 → 升版本 → 写 CHANGELOG → commit → push
#        → GitHub Actions 自动构建并部署 Pages
# ============================================================

cd "$(dirname "$0")" || exit 1

# ---- 参数解析 ----
if [[ "$1" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  VER="$1"; shift
else
  base=$(cat VERSION 2>/dev/null || echo "0.0.0")
  VER=$(echo "$base" | awk -F. '{$3=$3+1; print $1"."$2"."$3}')
fi
NOTE="$*"
[ -z "$NOTE" ] && NOTE="例行发布"
DATE=$(date +%F)
SITE_URL="https://xingbuild.github.io/CS329Zlearning/"

# ---- 前置检查 ----
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "✗ 尚未关联远程仓库。请先让代理在线后由助手执行建仓推送，或手动："
  echo "  gh repo create CS329Zlearning --public --source=. --push"
  exit 1
fi

# ---- 收编未提交变更（保持干净）----
if [ -n "$(git status --porcelain)" ]; then
  echo "· 收编未提交的变更…"
  git add -A && git commit -m "wip: 发布前自动收编（v$VER）" >/dev/null
fi

# ---- 版本与记录 ----
echo "$VER" > VERSION
# 在首条 ## 之前插入新条目（前后各留空行）
awk -v ver="## v$VER · $DATE · $NOTE" 'done==0 && /^## / { print ""; print ver; print ""; done=1 } { print }' CHANGELOG.md > CHANGELOG.tmp
mv CHANGELOG.tmp CHANGELOG.md

git add -A
git commit -m "release: v$VER · $NOTE" >/dev/null
echo "✓ v$VER 已提交"

# ---- 推送（Actions 随后自动部署 Pages）----
if git push origin main 2>&1; then
  echo ""
  echo "✓ 已推送。GitHub Actions 正在构建部署，约 1–2 分钟后可访问："
  echo "  $SITE_URL"
  echo "  （进度可用 gh run watch 查看）"
else
  echo "✗ 推送失败（检查代理/网络后重试：git push origin main）"
  exit 1
fi
