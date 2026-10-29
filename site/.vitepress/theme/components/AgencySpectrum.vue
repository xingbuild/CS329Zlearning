<script setup lang="ts">
import { ref, computed } from 'vue'

// Agency 光谱，整理自讲义 lecture05.pdf p.14-16
const LEVELS = [
  {
    id: 'model',
    name: 'Model',
    zh: '模型',
    where: '模型只是更大系统里的一小块',
    flow: '控制流：全在你的程序里',
    frames: 'OpenAI / Anthropic API',
    when: '任务是单点转换（分类、抽取、改写），一步出结果，无多步依赖。',
    risk: '可靠性问题集中在单次调用的输出契约——lab01 的两道闸就够了。',
  },
  {
    id: 'workflow',
    name: 'Workflow / Compound AI System',
    zh: '工作流 / 复合 AI 系统',
    where: '逻辑与编排写在程序里',
    flow: '控制流：代码决定（LLM 在节点里干活）',
    frames: 'DSPy（Signatures/Modules）、LangGraph（State/Nodes/Edges）',
    when: '步骤可预先确定（先检索再生成、先解析再校验），分支条件能写尽。',
    risk: '脆在"下一步取决于观察内容"的场景（L01 剧场②）——那是 agent 的领地。',
  },
  {
    id: 'agent',
    name: 'Agent',
    zh: '智能体',
    where: '循环 + 工具 + 目标',
    flow: '控制流：模型决定',
    frames: 'Harness：Mini SWE-Agent、OpenHands、Pi、Open Claw',
    when: '下一步依赖观察内容、无法预先写尽分支（开放域支持、探索式任务）。',
    risk: '误差复利 pⁿ、无停止规则、成本失控——L01 第四幕的主场。',
  },
]

const cur = ref('workflow')
const item = computed(() => LEVELS.find((l) => l.id === cur.value)!)
</script>

<template>
  <div class="spec">
    <div class="rail">
      <button v-for="l in LEVELS" :key="l.id" type="button" class="wbtn lv" :aria-pressed="l.id === cur"
        @click="cur = l.id">{{ l.zh }} · {{ l.name }}</button>
    </div>
    <div class="detail">
      <div class="d-row"><span class="dk">它是什么</span><span>{{ item.where }}</span></div>
      <div class="d-row"><span class="dk">控制流在哪</span><span><b>{{ item.flow }}</b></span></div>
      <div class="d-row"><span class="dk">典型框架</span><span>{{ item.frames }}</span></div>
      <div class="d-row"><span class="dk">什么时候选它</span><span>{{ item.when }}</span></div>
      <div class="d-row"><span class="dk">主要风险</span><span>{{ item.risk }}</span></div>
    </div>
    <div class="hint"><span class="k">一句判据 · </span>下一步是否取决于观察的内容？确定 → 往左焊死在代码；不确定 → 往右交给模型（L01 第三幕）。</div>
  </div>
</template>

<style scoped>
.spec { display: flex; flex-direction: column; gap: 12px; }
.rail { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.rail::after { content: '→ 自由度递增，可预测性递减'; font-size: 12.5px; color: var(--vp-c-text-3); }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 8px; }
.d-row { display: flex; gap: 10px; font-size: 14.5px; line-height: 1.65; }
.dk { flex: none; color: var(--vp-c-text-3); font-size: 13px; min-width: 108px; padding-top: 2px; }
</style>
