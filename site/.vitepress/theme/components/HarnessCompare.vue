<script setup lang="ts">
import { ref, computed } from 'vue'

// 四个开源 harness 的设计取舍，整理自讲义 lecture05.pdf p.82-85
const HARNESSES = [
  {
    id: 'mini',
    name: 'Mini SWE-Agent',
    tagline: '极简研究派',
    rows: [
      ['工具集', '只有 bash 一个工具'],
      ['历史结构', '完全线性——每步只追加消息'],
      ['执行方式', 'subprocess.run：每条命令相互独立、无状态'],
      ['卡死自愈', '无'],
      ['独门取舍', '变量压到最少，适合做受控评测与研究对照'],
    ],
  },
  {
    id: 'openhands',
    name: 'Open Hands',
    tagline: '工程实用派',
    rows: [
      ['工具集', 'bash + 文件 + 浏览器等'],
      ['历史结构', '每步存成一个 JSON 事件落盘，发消息时重建'],
      ['执行方式', '持久 tmux 会话——cd、环境变量、虚拟环境跨命令保留'],
      ['卡死自愈', '同一动作+结果重复 4 次 → 检测器终止运行'],
      ['独门取舍', '事件溯源（可回放）+ 真实终端状态'],
    ],
  },
  {
    id: 'pi',
    name: 'Pi Agent',
    tagline: '刻意简单派',
    rows: [
      ['工具集', '只有 4 个：read / write / edit / bash；系统提示 < 1000 token'],
      ['历史结构', '树——可以回到更早的消息分叉重跑'],
      ['执行方式', '无权限系统：以你启动时的权限运行'],
      ['卡死自愈', '—'],
      ['独门取舍', '无 plan 模式、无子 agent；少即是多'],
    ],
  },
  {
    id: 'openclaw',
    name: 'Open Claw',
    tagline: '常驻人格派',
    rows: [
      ['工具集', '聊天通道 + 定时任务'],
      ['历史结构', '身份由 Markdown 文件构成（AGENTS.md / SOUL.md / MEMORY.md…）注入系统提示'],
      ['执行方式', '单个长驻 Gateway 进程管理所有通道'],
      ['卡死自愈', '心跳机制：每 30 分钟自醒一次，无事则 NO_REPLY'],
      ['独门取舍', '每天凌晨 3 点后台任务整理当日笔记、把值得留的写进 MEMORY.md'],
    ],
  },
]

const cur = ref('openhands')
const item = computed(() => HARNESSES.find((h) => h.id === cur.value)!)
</script>

<template>
  <div class="hc">
    <div class="rail">
      <button v-for="h in HARNESSES" :key="h.id" type="button" class="wbtn" :aria-pressed="h.id === cur"
        @click="cur = h.id">{{ h.name }}</button>
    </div>
    <div class="detail">
      <div class="title">{{ item.name }} <span class="tag">{{ item.tagline }}</span></div>
      <div v-for="r in item.rows" :key="r[0]" class="d-row">
        <span class="dk">{{ r[0] }}</span><span>{{ r[1] }}</span>
      </div>
    </div>
    <div class="hint"><span class="k">看什么 · </span>四个 harness 没有"谁对谁错"——工具数、历史结构、执行方式、自愈，每个维度都是一次取舍；同一模型换 harness 成绩差一大截（harness tax），所以"造 harness"本身就是 agent 工程的核心手艺。</div>
  </div>
</template>

<style scoped>
.hc { display: flex; flex-direction: column; gap: 12px; }
.rail { display: flex; gap: 8px; flex-wrap: wrap; }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 8px; }
.title { font-weight: 700; font-size: 15.5px; }
.tag { font-size: 13px; color: var(--vp-c-brand-1); font-weight: 400; margin-left: 8px; }
.d-row { display: flex; gap: 10px; font-size: 14.5px; line-height: 1.65; }
.dk { flex: none; color: var(--vp-c-text-3); font-size: 13px; min-width: 84px; padding-top: 2px; }
</style>
