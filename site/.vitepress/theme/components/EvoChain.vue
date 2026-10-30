<script setup lang="ts">
import { ref, computed } from 'vue'

// 演进链（L04 版）：背景 → 根本问题 → 技术应答 → 代价 → 新问题 → 下一代
const ERAS = [
  {
    id: 1, era: '时代一 · 改模型（2022–23）',
    bg: 'LLM 涌现，但只会说话——它会描述怎么查天气，却查不了',
    prob: '怎么让它"会做"：何时调、调什么、传什么参？',
    tech: 'Toolformer（自监督）→ ToolkenGPT → Gorilla（规模化微调）',
    cost: '每来一个新 API 就要再训练一次——扩展性死局',
    next: '能不能不改模型，让工具去适配模型？',
  },
  {
    id: 2, era: '时代二 · 改协议（2023–24）',
    bg: '逐 API 微调被证伪：工具在爆炸，训练跟不上',
    prob: '任何模型、任何工具，如何即插即用？',
    tech: 'Function Calling：schema 运行时喂给模型 + harness 校验分发（strict/约束解码给"保证"）',
    cost: 'schema 困在各家代码库——工具换个宿主要重写一遍',
    next: '工具能不能"一次编写、处处可用"？',
  },
  {
    id: 3, era: '时代三 · 生态化（2024– ）',
    bg: 'N 个工具 × M 个宿主 = N×M 份重复适配',
    prob: '如何让工具成为网络里可发现的资源？',
    tech: 'MCP：tools/list 运行时发现 + tools/call + 双 auth（FastMCP 可从 OpenAPI 一键生成）',
    cost: '运行时发现打开攻击面——工具投毒、影子工具（Invariant 实测）',
    next: '信任问题：谁来担保工具可信？（正在演进：A2A、验证生态）',
  },
]
const cur = ref(1)
const item = computed(() => ERAS.find((e) => e.id === cur.value)!)
</script>

<template>
  <div class="evo">
    <svg viewBox="0 0 860 300" width="100%" role="img" aria-label="工具使用三时代演进链">
      <defs><marker id="ev-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="var(--vp-c-text-3)" /></marker></defs>
      <g v-for="(e, i) in ERAS" :key="e.id" class="era" :class="{ on: cur === e.id }" @click="cur = e.id">
        <rect :x="20 + i * 285" y="40" width="245" height="180" rx="14" class="ebox" />
        <text :x="142 + i * 285" y="72" text-anchor="middle" class="et">{{ e.era }}</text>
        <text :x="142 + i * 285" y="104" text-anchor="middle" class="ep">{{ e.prob }}</text>
        <text :x="142 + i * 285" y="140" text-anchor="middle" class="ech">{{ e.tech }}</text>
        <text :x="142 + i * 285" y="180" text-anchor="middle" class="ec">代价：{{ e.cost.slice(0, 18) }}…</text>
        <text :x="142 + i * 285" y="205" text-anchor="middle" class="ec">→ {{ e.next.slice(0, 16) }}…</text>
      </g>
      <line x1="268" y1="130" x2="300" y2="130" class="arr" marker-end="url(#ev-a)" />
      <line x1="553" y1="130" x2="585" y2="130" class="arr" marker-end="url(#ev-a)" />
      <text x="430" y="270" text-anchor="middle" class="foot">三时代的共同脚本：技术解决旧问题 → 代价产生新问题 → 新问题定义下一代（点击任一时代看全文）</text>
    </svg>
    <div class="detail">
      <div class="drow"><span class="dk">背景</span><span>{{ item.bg }}</span></div>
      <div class="drow"><span class="dk">根本问题</span><span><b>{{ item.prob }}</b></span></div>
      <div class="drow"><span class="dk">技术应答</span><span>{{ item.tech }}</span></div>
      <div class="drow"><span class="dk">代价（引擎）</span><span>{{ item.cost }}</span></div>
      <div class="drow"><span class="dk">新问题</span><span>{{ item.next }}</span></div>
    </div>
  </div>
</template>

<style scoped>
.evo { display: flex; flex-direction: column; gap: 10px; }
svg :deep(text) { font-family: inherit; }
.ebox { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); stroke-width: 1.5; cursor: pointer; }
.era.on .ebox { stroke: var(--vp-c-brand-1); stroke-width: 2.5; fill: var(--vp-c-brand-soft); }
.et { font-size: 14px; font-weight: 700; fill: var(--vp-c-text-1); }
.ep { font-size: 12px; fill: var(--vp-c-text-2); }
.ech { font-size: 11.5px; fill: var(--vp-c-brand-1); font-weight: 600; }
.ec { font-size: 11px; fill: var(--vp-c-text-3); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 2; fill: none; }
.foot { font-size: 12px; fill: var(--vp-c-text-3); }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 7px; }
.drow { display: flex; gap: 10px; font-size: 14px; line-height: 1.65; }
.dk { flex: none; color: var(--vp-c-text-3); font-size: 12.5px; min-width: 82px; padding-top: 2px; }
</style>
