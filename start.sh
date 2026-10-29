#!/bin/bash
# ============================================================
#  Engineering AI Agents · 课程站一键启动
#  用法：终端运行 ./start.sh（或已配置的别名 eaia）
#  行为：停止旧实例 → 构建最新内容 → 起本地服务 → 开浏览器
#  停止：回到终端按 Ctrl+C
# ============================================================

cd "$(dirname "$0")/site" || exit 1
URL="http://localhost:4173"

# 旧实例直接停掉（vitepress preview 缓存启动时的文件映射，必须重启才会 serve 新构建）
pkill -f "vitepress preview" 2>/dev/null && sleep 1

if [ ! -d node_modules ]; then
  echo "首次运行：安装依赖…"
  npm install --no-fund --no-audit || { echo "✗ 依赖安装失败（检查 node/npm）"; exit 1; }
fi

echo "构建最新内容…"
npm run build >/dev/null 2>&1 || { echo "✗ 构建失败：cd site && npm run build 查看错误"; exit 1; }

echo ""
echo "✓ 课程站运行中：$URL （Ctrl+C 停止）"
( sleep 1.5; open "$URL" ) &
exec npx vitepress preview
