<script setup lang="ts">
import { ref, computed } from 'vue'

// 多智能体编排四模式，整理自讲义 lecture08.pdf p.17-24
const TOPOS = [
  {
    id: 'independent',
    name: '独立式 Independent',
    topo: '[Agent1]  [Agent2]  [Agent3]\n    \\        |        /\n     [聚合器/择优]',
    pro: '完全并行，零中间通信开销；各Agent 独立探索',
    con: '互相看不到中间发现——无法据同伴进展调整方向（投票式推理缩放属于此类）',
    cost: '低',
  },
  {
    id: 'centralized',
    name: '中心式 Orchestrator',
    topo: '        [编排者]\n      /    |    \\\n[工人1] [工人2] [工人3]\n      \\    |    /\n        [编排者]',
    pro: '中央监督，协调最简单；Magentic-One 的 Task Ledger 就挂在这里',
    con: '编排者是瓶颈与单点故障；所有信息过它一手（信息也可能被它压缩失真）',
    cost: '中',
  },
  {
    id: 'decentralized',
    name: '去中心式 Swarm',
    topo: '  [A]←→[B]\n   ↕  ×  ↕\n  [C]←→[D]\n（共享消息板，all-to-all，可派生子agent）',
    pro: '大规模并行探索与发现；无单点瓶颈；Carlini 编译器蜂群属于此类',
    cost: '高',
    con: '消息爆炸、从众效应、冲突不断——通信与协调成本最高',
  },
  {
    id: 'hybrid',
    name: '混合式 Hybrid',
    topo: '        [编排者]\n      /    |    \\\n[工人1]←→[工人2]  [工人3]\n（全局有头，局部直连）',
    pro: '全局监督 + 局部直连兼顾；需要清晰的责任与信息共享规则',
    con: '规则设计复杂——谁可以直连谁、何时上报，都要显式约定',
    cost: '中高',
  },
]

const cur = ref('centralized')
const item = computed(() => TOPOS.find((t) => t.id === cur.value)!)
</script>

<template>
  <div class="mtop">
    <div class="rail">
      <button v-for="t in TOPOS" :key="t.id" type="button" class="wbtn" :aria-pressed="t.id === cur"
        @click="cur = t.id">{{ t.name }}</button>
    </div>
    <div class="detail">
      <div class="title">{{ item.name }} <span class="pill brand">通信成本：{{ item.cost }}</span></div>
      <pre class="topo">{{ item.topo }}</pre>
      <div class="d-row"><span class="dk">优点</span><span>{{ item.pro }}</span></div>
      <div class="d-row"><span class="dk">代价</span><span>{{ item.con }}</span></div>
    </div>
    <div class="hint"><span class="k">成本法则 · </span>Single Agent &lt; 中心式 &lt; 蜂群（讲义 p.24）；架构选择取决于任务的可分性——没有万能拓扑。</div>
  </div>
</template>

<style scoped>
.mtop { display: flex; flex-direction: column; gap: 12px; }
.rail { display: flex; gap: 8px; flex-wrap: wrap; }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 8px; }
.title { font-weight: 700; font-size: 15.5px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.topo { margin: 0; background: var(--vp-c-default-soft); border-radius: 8px; padding: 10px 14px; font-size: 12.5px; line-height: 1.6; font-family: var(--vp-font-family-mono, monospace); color: var(--vp-c-text-2); white-space: pre; overflow-x: auto; }
.d-row { display: flex; gap: 10px; font-size: 14.5px; line-height: 1.65; }
.dk { flex: none; color: var(--vp-c-text-3); font-size: 13px; min-width: 40px; padding-top: 2px; }
</style>
