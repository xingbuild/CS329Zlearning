<script setup lang="ts">
import { ref, computed } from 'vue'

// Agent 闭环 · 环形舞台：角色固定站位，数据沿环流动（据讲义 p.29-30 解剖图）
type Role = 'llm' | 'gate' | 'exec' | 'env' | 'crash'
const gateOn = ref(true)
const idx = ref(0)
interface F { role: Role; t: string; feed?: boolean }
const FRAMES = (on: boolean): F[] => on ? [
  { role: 'llm', t: '轮次 1 · 决策：模型生成 tool_call：convert(value="二十五", unit="C")' },
  { role: 'gate', t: '契约闸（schema 校验）：value 需要 float，得到 "二十五" → ❌ 拦下' },
  { role: 'llm', t: '报错回喂：错误信息进入上下文——沿环回到决策位（不是剧情下一集，是控制流回到自身）', feed: true },
  { role: 'llm', t: '轮次 2 · 决策：改发 convert(25, "C") → ✓' },
  { role: 'gate', t: '契约闸：类型契约通过 ✓' },
  { role: 'exec', t: '工具执行（确定性代码）：25 × 9/5 + 32 = 77' },
  { role: 'env', t: '观察回喂：77°F 写入上下文——沿环再回到决策位', feed: true },
  { role: 'llm', t: '轮次 3 · 决策：信息足够 → Finish["77°F"]。循环闭合' },
] : [
  { role: 'llm', t: '轮次 1 · 决策：convert(value="二十五", unit="C")' },
  { role: 'crash', t: '无闸直通 → Python 执行 convert("二十五") → 💥 TypeError' },
  { role: 'crash', t: '确定性代码被概率输出击穿——崩溃在你的产线，模型毫发无伤' },
]
const frames = computed(() => FRAMES(gateOn.value))
const cur = computed(() => frames.value[idx.value])
const ROLES: Record<string, { x: number; y: number; w: number; name: string; sub: string }> = {
  llm: { x: 260, y: 20, w: 180, name: 'LLM 决策', sub: 'decide（概率）' },
  gate: { x: 500, y: 170, w: 150, name: '契约闸', sub: 'validate（确定）' },
  exec: { x: 260, y: 330, w: 180, name: '工具执行', sub: 'execute（确定）' },
  env: { x: 40, y: 170, w: 150, name: '环境/观察', sub: 'observe（回喂）' },
  crash: { x: 500, y: 330, w: 150, name: '💥 崩溃', sub: '无闸下场' },
}
function toggle() { gateOn.value = !gateOn.value; idx.value = 0 }
const activeRole = computed(() => cur.value.role)
const round = computed(() => frames.value.slice(0, idx.value + 1).filter(f => f.t.includes('轮次')).length)
</script>

<template>
  <div class="lp">
    <div class="row wrap">
      <button type="button" class="wbtn" :aria-pressed="gateOn" @click="toggle">{{ gateOn ? '契约闸：开（推荐）' : '契约闸：关' }}</button>
      <button type="button" class="wbtn" :disabled="idx === 0" @click="idx--">◀</button>
      <button type="button" class="wbtn primary" :disabled="idx === frames.length - 1" @click="idx++">下一步 ▶</button>
      <span class="pill brand">轮次：{{ round }}</span>
    </div>
    <svg viewBox="0 0 680 430" width="100%" role="img" aria-label="agent 闭环环形舞台">
      <defs><marker id="lp-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="var(--vp-c-text-3)" /></marker></defs>
      <!-- 环箭头：LLM→闸→执行→环境→LLM -->
      <g v-if="gateOn">
        <line x1="440" y1="70" x2="540" y2="160" class="arr" :class="{ hot: cur.feed && cur.role === 'llm' }" marker-end="url(#lp-a)" />
        <line x1="530" y1="230" x2="420" y2="330" class="arr" marker-end="url(#lp-a)" />
        <line x1="260" y1="380" x2="130" y2="250" class="arr" :class="{ hot: cur.feed && cur.role === 'llm' && idx > 4 }" marker-end="url(#lp-a)" />
        <line x1="115" y1="170" x2="250" y2="80" class="arr hotfeed" :class="{ hot: cur.feed }" marker-end="url(#lp-a)" />
        <text x="180" y="130" class="al">观察回喂 ↺</text>
      </g>
      <g v-else>
        <line x1="440" y1="70" x2="560" y2="330" class="arr crash" marker-end="url(#lp-a)" />
      </g>
      <!-- 角色框 -->
      <g v-for="(r, k) in ROLES" :key="k" :class="{ dim: gateOn === false && k === 'gate' }">
        <rect :x="r.x" :y="r.y" :width="r.w" height="76" rx="12" class="box" :class="{ on: activeRole === k, crashb: k === 'crash' }" />
        <text :x="r.x + r.w / 2" :y="r.y + 32" text-anchor="middle" class="rn">{{ r.name }}</text>
        <text :x="r.x + r.w / 2" :y="r.y + 54" text-anchor="middle" class="rs">{{ gateOn === false && k === 'gate' ? '（已跳过）' : r.sub }}</text>
      </g>
      <text x="340" y="222" text-anchor="middle" class="loop-t">循 环</text>
      <text x="340" y="248" text-anchor="middle" class="loop-s">据讲义 p.29–30 解剖图</text>
    </svg>
    <div class="cur" :class="{ bad: cur.role === 'crash' }">{{ cur.t }}</div>
    <div class="hint"><span class="k">看什么 · </span>四个位置永远不动，动的是数据：决策沿环下探、观察沿环回喂——<b>循环是空间结构，不是时间线</b>。关闸再走一遍：没有环，只有一条直通崩溃的直线。</div>
  </div>
</template>

<style scoped>
.lp { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
svg :deep(text) { font-family: inherit; }
.box { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); stroke-width: 1.5; }
.box.on { stroke: var(--vp-c-brand-1); stroke-width: 2.5; fill: var(--vp-c-brand-soft); }
.box.crashb { stroke: #dc2626; }
.rn { font-size: 16px; font-weight: 700; fill: var(--vp-c-text-1); }
.rs { font-size: 12px; fill: var(--vp-c-text-2); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 1.8; fill: none; }
.arr.hot, .arr.hotfeed.hot { stroke: var(--vp-c-brand-1); stroke-width: 3; }
.arr.crash { stroke: #dc2626; stroke-width: 2.5; }
.dim { opacity: .35; }
.al { font-size: 12px; fill: var(--vp-c-text-2); }
.loop-t { font-size: 18px; font-weight: 700; fill: var(--vp-c-text-3); letter-spacing: 6px; }
.loop-s { font-size: 11.5px; fill: var(--vp-c-text-3); }
.cur { font-size: 14.5px; line-height: 1.7; background: var(--vp-c-brand-soft); border-radius: 9px; padding: 10px 14px; }
.cur.bad { background: rgba(220,38,38,.09); }
</style>
