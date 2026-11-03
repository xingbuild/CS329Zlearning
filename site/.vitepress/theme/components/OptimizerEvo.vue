<script setup lang="ts">
import { ref, computed } from 'vue'

// 优化三时代演进链（L09 版，据讲义 lecture09 Context Optimization 谱系；EvoChain 同构）
// 图内文字红线：卡片只放自足短语；全文在下方面板；三通道齐备
const ERAS = [
  {
    id: 1, era: '时代一 · 手工调优（玄学）',
    bg: 'Prompt 工程靠直觉与传闻——社区流传"加一句深呼吸"式的咒语',
    prob: '改一次靠猜一次，怎么把改系统变成可复现的工程？',
    tech: '顺序实验（Fantastically Ordered：熵探测最优 few-shot 顺序）',
    cost: '搜索空间爆炸（措辞×顺序×示例组合），且换任务就失效',
    next: '能不能不靠人写，让数据自己长出好 prompt？',
    probS: '怎么不靠猜？',
    techS: '顺序/熵实验',
    costS: '代价：组合爆炸',
    nextS: '→ 让数据长出 prompt？',
  },
  {
    id: 2, era: '时代二 · 数据自举（bootstrap）',
    bg: '标注的 few-shot 示例常常不带推理过程（CoT 标注太贵）',
    prob: '没有带推理的标注，怎么获得高质量示例？',
    tech: 'STaR（拒绝采样挖推理轨迹）→ DSPy（bootstrap 成功轨迹当示例 + 随机搜索，胜过人写示例）',
    cost: '只复用已有能力——挖不出模型本来不会的解法',
    next: '能不能让模型看着失败，自己改指令？',
    probS: '没标注怎么办？',
    techS: 'STaR → DSPy 自举',
    costS: '代价：上限=模型自身',
    nextS: '→ 自己改指令？',
  },
  {
    id: 3, era: '时代三 · 反思进化（reflective）',
    bg: 'DSPy 的随机搜索不利用"为什么失败"的信息',
    prob: '怎么把失败经验变成下一版 prompt 的改进方向？',
    tech: 'OPRO（LLM 看历史指令与得分写新指令——"深呼吸"由它发现）→ MIPROv2（bootstrap 示例 + 情境化指令提案 + 贝叶斯代理搜索组合）→ TextGrad（文本反馈梯度）/ GEPA（Pareto 前沿进化）',
    cost: 'prompt 越优化越长——上下文膨胀与过拟合评测的风险',
    next: 'prompt 已到上限时，动权重（第四幕）或让 agent 自己当优化器（第五幕）',
    probS: '失败怎么变方向？',
    techS: 'OPRO → MIPROv2 → GEPA',
    costS: '代价：上下文膨胀',
    nextS: '→ 换杠杆：权重/agent',
  },
]
const cur = ref(1)
const item = computed(() => ERAS.find((e) => e.id === cur.value)!)
function pick(id: number) { cur.value = id }
</script>

<template>
  <div class="oevo">
    <svg viewBox="0 0 860 300" width="100%" role="img" aria-label="prompt 优化三时代演进链（三个可选中时代，选中后下方显示五段全文）">
      <defs><marker id="oe-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="var(--vp-c-text-3)" /></marker></defs>
      <g v-for="(e, i) in ERAS" :key="e.id" class="era" :class="{ on: cur === e.id }"
        :tabindex="0" role="button" :aria-pressed="cur === e.id" :aria-label="e.era"
        @click="pick(e.id)" @keydown.enter="pick(e.id)">
        <rect :x="20 + i * 285" y="40" width="245" height="180" rx="14" class="ebox" />
        <text :x="142 + i * 285" y="72" text-anchor="middle" class="et">{{ e.era }}</text>
        <text :x="142 + i * 285" y="104" text-anchor="middle" class="ep">{{ e.probS }}</text>
        <text :x="142 + i * 285" y="140" text-anchor="middle" class="ech">{{ e.techS }}</text>
        <text :x="142 + i * 285" y="180" text-anchor="middle" class="ec">{{ e.costS }}</text>
        <text :x="142 + i * 285" y="205" text-anchor="middle" class="ec">{{ e.nextS }}</text>
      </g>
      <line x1="268" y1="130" x2="300" y2="130" class="arr" marker-end="url(#oe-a)" />
      <line x1="553" y1="130" x2="585" y2="130" class="arr" marker-end="url(#oe-a)" />
      <text x="430" y="270" text-anchor="middle" class="foot">共同脚本：杠杆从小到大（措辞→示例→指令），每一代的代价孕育下一代（选中任一时代，下方看全文）</text>
    </svg>
    <div class="detail" aria-live="polite">
      <div class="drow"><span class="dk">背景</span><span>{{ item.bg }}</span></div>
      <div class="drow"><span class="dk">根本问题</span><span><b>{{ item.prob }}</b></span></div>
      <div class="drow"><span class="dk">技术应答</span><span>{{ item.tech }}</span></div>
      <div class="drow"><span class="dk">代价（引擎）</span><span>{{ item.cost }}</span></div>
      <div class="drow"><span class="dk">下一代</span><span>{{ item.next }}</span></div>
    </div>
  </div>
</template>

<style scoped>
.oevo { display: flex; flex-direction: column; gap: 10px; overflow-x: auto; }
.oevo svg { min-width: 860px; }
svg :deep(text) { font-family: inherit; }
.ebox { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); stroke-width: 1.5; }
.era { cursor: pointer; outline: none; }
.era:focus-visible .ebox { stroke: var(--vp-c-brand-1); stroke-width: 3; }
.era.on .ebox { stroke: var(--vp-c-brand-1); stroke-width: 2.5; fill: var(--vp-c-brand-soft); }
.et { font-size: 15px; font-weight: 700; fill: var(--vp-c-text-1); }
.ep { font-size: 12.5px; fill: var(--vp-c-text-2); }
.ech { font-size: 12px; fill: var(--vp-c-brand-1); font-weight: 600; }
.ec { font-size: 12px; fill: var(--vp-c-text-3); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 2; fill: none; }
.foot { font-size: 12.5px; fill: var(--vp-c-text-3); }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 7px; }
.drow { display: flex; gap: 10px; font-size: 14px; line-height: 1.65; }
.dk { flex: none; color: var(--vp-c-text-3); font-size: 12.5px; min-width: 82px; padding-top: 2px; }
</style>
