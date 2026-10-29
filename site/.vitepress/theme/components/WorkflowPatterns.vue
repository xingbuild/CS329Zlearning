<script setup lang="ts">
import { ref, computed } from 'vue'

// Anthropic 工作流五模式，整理自讲义 lecture06.pdf p.14-21
const PATTERNS = [
  {
    id: 'chain',
    name: '提示链 Prompt Chaining',
    core: '把大任务分解成一串小步',
    diagram: '[生成大纲] → [写正文] → [校对润色]',
    when: '任务复杂但顺序固定，每步可校验',
    tradeoff: '用延迟换准确率；任何一步失败要考虑回退',
  },
  {
    id: 'route',
    name: '路由 Routing',
    core: '先分类，再分发给合适的模型/提示',
    diagram: '        ┌→ 强模型 + 复杂提示\n[分类器] ─┼→ 弱模型 + 简单提示\n        └→ 拒答/人工',
    when: '任务有清晰类别；想省钱（易例用便宜模型）',
    tradeoff: '分类器错误代价高——它就是新的失败面（L01 剧场①的死法换成路由器）',
  },
  {
    id: 'parallel',
    name: '并行化 Parallelization',
    core: '多线程同时干（分区 Sectioning / 投票 Voting）',
    diagram: '分区：[安全检查] ∥ [正常处理]\n投票：[生成]×N → [聚合取多数]',
    when: '分区：独立子任务；投票：推理时缩放（L02 的 Self-Consistency）',
    tradeoff: '成本 ×N；聚合器成为新的质量瓶颈',
  },
  {
    id: 'orchestrator',
    name: '编排者-工人 Orchestrator-Workers',
    core: '一个 LLM 动态拆任务、派给工人 LLM',
    diagram: '[编排者拆解] ─┬→ [工人1]\n              ├→ [工人2]\n              └→ [汇总合成]',
    when: '子任务的数量与性质无法预先知道',
    tradeoff: '与并行化的差别：子任务是动态生成的——灵活性换可控性',
  },
  {
    id: 'evalopt',
    name: '评估者-优化者 Evaluator-Optimizer',
    core: '生成 → 批评 → 迭代的循环',
    diagram: '[生成器] → 草稿 → [评估者] → 反馈\n   ↑__________________________|',
    when: '反馈清晰可表述、评估者有能力、生成器能据此改进',
    tradeoff: '三条件缺一不可（否则死循环烧钱）；Reflexion 一节会回到这个模式',
  },
]

const cur = ref('chain')
const item = computed(() => PATTERNS.find((p) => p.id === cur.value)!)
</script>

<template>
  <div class="wp">
    <div class="rail">
      <button v-for="p in PATTERNS" :key="p.id" type="button" class="wbtn" :aria-pressed="p.id === cur"
        @click="cur = p.id">{{ p.name.split(' ')[0] }}</button>
    </div>
    <div class="detail">
      <div class="title">{{ item.name }}</div>
      <div class="core">{{ item.core }}</div>
      <pre class="diag">{{ item.diagram }}</pre>
      <div class="d-row"><span class="dk">何时用</span><span>{{ item.when }}</span></div>
      <div class="d-row"><span class="dk">取舍</span><span>{{ item.tradeoff }}</span></div>
    </div>
    <div class="hint"><span class="k">用法 · </span>真实系统是这些基本模式的<b>组合</b>（讲义的 STORM 例子一次用了四个）——Fowler 说模式是"半成品"，你总要按自己的环境把它烤熟。</div>
  </div>
</template>

<style scoped>
.wp { display: flex; flex-direction: column; gap: 12px; }
.rail { display: flex; gap: 8px; flex-wrap: wrap; }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 8px; }
.title { font-weight: 700; font-size: 15.5px; }
.core { font-size: 14.5px; color: var(--vp-c-brand-1); }
.diag { margin: 0; background: var(--vp-c-default-soft); border-radius: 8px; padding: 10px 14px; font-size: 12.5px; line-height: 1.6; font-family: var(--vp-font-family-mono, monospace); color: var(--vp-c-text-2); white-space: pre; overflow-x: auto; }
.d-row { display: flex; gap: 10px; font-size: 14.5px; line-height: 1.65; }
.dk { flex: none; color: var(--vp-c-text-3); font-size: 13px; min-width: 60px; padding-top: 2px; }
</style>
