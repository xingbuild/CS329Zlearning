<script setup lang="ts">
import { ref, computed } from 'vue'

// 六张任务卡与判据，整理自讲义 lecture05.pdf p.14 定档表与 p.124-128 最佳实践
interface Card {
  id: string
  name: string
  brief: string
  traits: { k: string; v: string }[]
  answer: 'model' | 'workflow' | 'agent'
  why: string
  durable: boolean
}

const CARDS: Card[] = [
  {
    id: 'invoice',
    name: '发票字段抽取',
    brief: '把 PDF 发票里的金额、日期、税号抽成 JSON，一步出结果。',
    traits: [
      { k: '步骤可预先写尽？', v: '是——单点转换' },
      { k: '下一步依赖观察？', v: '否' },
      { k: '运行时长', v: '秒级' },
      { k: '共享状态', v: '无' },
    ],
    answer: 'model',
    why: '单点转换是 Model 档的定义场景（p.14 左列）；可靠性靠输出契约 + 校验闸（lab01 两道闸），不需要循环。',
    durable: false,
  },
  {
    id: 'news',
    name: '每日新闻早报',
    brief: '先检索昨日要闻，再摘要成 300 字早报——固定两步。',
    traits: [
      { k: '步骤可预先写尽？', v: '是——检索→摘要' },
      { k: '下一步依赖观察？', v: '否——分支写尽' },
      { k: '运行时长', v: '分钟级' },
      { k: '共享状态', v: '低' },
    ],
    answer: 'workflow',
    why: '步骤固定、分支可写尽——控制流留在代码里（p.14）；写成两个节点的图（LangGraph）或两行函数调用都行。',
    durable: false,
  },
  {
    id: 'refund',
    name: '客服退款处理',
    brief: '查订单、查政策、问用户、必要时升级人工——下一步看上一步结果。',
    traits: [
      { k: '步骤可预先写尽？', v: '否' },
      { k: '下一步依赖观察？', v: '是——对话与查询结果决定' },
      { k: '运行时长', v: '分钟级' },
      { k: '共享状态', v: '中（订单/工单）' },
    ],
    answer: 'agent',
    why: '下一步取决于观察内容——L01 那把刀的标准 Agent 侧（p.14 右列）；退款执行本身保持纯代码 workflow。',
    durable: false,
  },
  {
    id: 'pipeline',
    name: '8 小时合规数据管道',
    brief: '拉取→清洗→分析→出报告，每步依赖上一步输出，夜里跑。',
    traits: [
      { k: '步骤可预先写尽？', v: '是——强依赖链条' },
      { k: '下一步依赖观察？', v: '否' },
      { k: '运行时长', v: '小时级（跨"人类时间"）' },
      { k: '共享状态', v: '高（数据库）' },
    ],
    answer: 'workflow',
    why: '控制流确定 → Workflow 档；但时长跨人类时间量级——判据之外还要持久执行（p.92-93），底盘选 Temporal 是加分项。',
    durable: true,
  },
  {
    id: 'research',
    name: '开放域研究助理',
    brief: '"要不要再查、查什么、够不够"由每轮检索结果决定。',
    traits: [
      { k: '步骤可预先写尽？', v: '否——查几轮事先不知道' },
      { k: '下一步依赖观察？', v: '是——检索结果定去向' },
      { k: '运行时长', v: '分钟级' },
      { k: '共享状态', v: '低' },
    ],
    answer: 'agent',
    why: 'Agentic RAG 的三决策（要不要查/查什么/够不够）都在模型手里（L03 第四幕）——Agent 档。',
    durable: false,
  },
  {
    id: 'review',
    name: '代码评审机器人',
    brief: '读 diff → 查编码规约 → 逐条比对 → 出评审报告——流程固定。',
    traits: [
      { k: '步骤可预先写尽？', v: '是——四步管线' },
      { k: '下一步依赖观察？', v: '否（每步输入可预判）' },
      { k: '运行时长', v: '分钟级' },
      { k: '共享状态', v: '低' },
    ],
    answer: 'workflow',
    why: '步骤与分支能写尽 → Workflow 档；硬塞成 agent 只会引入 pⁿ 误差复利——"你可能根本不需要 agent"（p.124）。',
    durable: false,
  },
]

const LEVEL_NAME: Record<string, string> = { model: 'Model', workflow: 'Workflow', agent: 'Agent' }

// 底盘选项按档位给出（选型=先定档，再选语法与基础设施）
const CHASSIS: Record<string, { id: string; name: string; tax: string; note: string }[]> = {
  model: [
    { id: 'raw', name: '裸 prompt 拼字符串', tax: '零依赖', note: '输出没契约——校验闸全靠自己写。' },
    { id: 'so', name: '结构化输出 API + 校验', tax: '零依赖', note: 'schema 一份三吃（L04）——Model 档的正解。' },
  ],
  workflow: [
    { id: 'hand', name: '手写函数调用', tax: '零依赖', note: '两个节点而已——透明、可控、随时可丢。' },
    { id: 'dsp', name: 'DSPy', tax: '低', note: '要 Optimizer 自动调 prompt 时才体现价值（第二幕）。' },
    { id: 'graph', name: 'LangGraph', tax: '低', note: '图复杂（分支/并行/回边多）时语法才划算。' },
    { id: 'temporal', name: '手写 + Temporal', tax: '中', note: '每个外部动作包成 Activity——长时任务的保险。' },
  ],
  agent: [
    { id: 'hand', name: '手写循环（while + 工具表）', tax: '零依赖', note: '<100 行的骨架你已经会了——lab01 闭环。' },
    { id: 'graph', name: 'LangGraph 环', tax: '低', note: '买持久化、流式与条件边管理——语法糖 + 配套。' },
    { id: 'heavy', name: '重框架全家桶', tax: '高', note: '每一层抽象都是别人的决定——A 团队的命运（开场）。' },
  ],
}

const idx = ref(0)
const picks = ref<Record<string, { level?: string; chassis?: string; durable?: boolean }>>({})
const card = computed(() => CARDS[idx.value])
const pick = computed(() => picks.value[card.value.id] || {})
const results = computed(() =>
  CARDS.map((c) => {
    const p = picks.value[c.id] || {}
    if (!p.level) return { c, state: 'todo' as const }
    const ok = p.level === c.answer
    return { c, state: ok ? ('good' as const) : ('off' as const), level: p.level, chassis: p.chassis, durable: p.durable }
  }),
)
const doneCount = computed(() => results.value.filter((r) => r.state !== 'todo').length)

function chooseLevel(lv: string) {
  const id = card.value.id
  const p = picks.value[id] || {}
  picks.value[id] = { ...p, level: lv, chassis: undefined, durable: p.durable }
}
function chooseChassis(cs: string) {
  const id = card.value.id
  const p = picks.value[id] || {}
  picks.value[id] = { ...p, chassis: cs }
}
function toggleDurable() {
  const id = card.value.id
  const p = picks.value[id] || {}
  picks.value[id] = { ...p, durable: !p.durable }
}
</script>

<template>
  <div class="tsd">
    <div class="rail">
      <button v-for="(c, i) in CARDS" :key="c.id" type="button" class="wbtn cardbtn" :aria-pressed="i === idx"
        @click="idx = i">
        <span class="cn">{{ c.name }}</span>
        <span class="cb" :class="results[i].state">{{ results[i].state === 'good' ? '✓' : results[i].state === 'off' ? '✗' : '·' }}</span>
      </button>
      <div class="score">已判 {{ doneCount }}/6</div>
    </div>

    <div class="stage">
      <h4 class="tname">{{ card.name }}</h4>
      <p class="tbrief">{{ card.brief }}</p>
      <div class="traits">
        <div v-for="t in card.traits" :key="t.k" class="tr"><span class="tk">{{ t.k }}</span><span>{{ t.v }}</span></div>
      </div>

      <div class="stepq"><span class="sq">①</span>先定档——控制流归谁？</div>
      <div class="opts">
        <button v-for="lv in ['model', 'workflow', 'agent']" :key="lv" type="button" class="wbtn"
          :aria-pressed="pick.level === lv" @click="chooseLevel(lv)">{{ LEVEL_NAME[lv] }}</button>
      </div>

      <template v-if="pick.level">
        <div class="stepq"><span class="sq">②</span>再选底盘——用什么写？</div>
        <div class="opts">
          <button v-for="cs in CHASSIS[pick.level]" :key="cs.id" type="button" class="wbtn"
            :aria-pressed="pick.chassis === cs.id" @click="chooseChassis(cs.id)">{{ cs.name }}</button>
        </div>
        <div v-if="card.durable" class="opts">
          <button type="button" class="wbtn" :aria-pressed="!!pick.durable" @click="toggleDurable">＋ Temporal 持久执行</button>
        </div>
      </template>

      <div v-if="pick.chassis" class="bill">
        <div class="b-row"><span class="bk">你的定档</span><span><b>{{ LEVEL_NAME[pick.level] }}</b> · 底盘：{{ CHASSIS[pick.level].find((c) => c.id === pick.chassis)?.name }}{{ pick.durable ? ' ＋ Temporal' : '' }}</span></div>
        <div class="b-row"><span class="bk">抽象税</span><span>{{ CHASSIS[pick.level].find((c) => c.id === pick.chassis)?.tax }} · {{ CHASSIS[pick.level].find((c) => c.id === pick.chassis)?.note }}</span></div>
        <div class="b-row"><span class="bk">讲义判据</span><span :class="pick.level === card.answer ? 'ok' : 'off'">{{ pick.level === card.answer ? '✓ 与讲义推荐一致' : '✗ 讲义推荐 ' + LEVEL_NAME[card.answer] + ' 档' }}——{{ card.why }}</span></div>
        <div v-if="card.durable" class="b-row"><span class="bk">持久执行</span><span :class="pick.durable ? 'ok' : 'off'">{{ pick.durable ? '✓ 长时任务的保险买上了（事件溯源，第四幕）' : '⚠ 该任务跨"人类时间"量级——不配持久执行，崩溃即全部重来' }}</span></div>
      </div>
    </div>

    <div class="hint"><span class="k">判据一句话 · </span>先问"下一步是否取决于观察的内容"定档（p.14），再问"图够不够复杂/跑得够不够久"选底盘——顺序反了就是被框架牵着走。</div>
  </div>
</template>

<style scoped>
.tsd { display: flex; flex-direction: column; gap: 12px; }
.rail { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.cardbtn { display: inline-flex; gap: 6px; align-items: center; }
.cn { font-weight: 500; }
.cb { display: inline-flex; width: 18px; height: 18px; align-items: center; justify-content: center; border-radius: 50%; font-size: 11px; }
.cb.good { background: var(--vp-c-brand-1); color: var(--vp-c-white); }
.cb.off { background: var(--vp-c-danger-1); color: var(--vp-c-white); }
.score { margin-left: auto; font-size: 12px; color: var(--vp-c-text-2); }
.stage { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
.tname { margin: 0; font-size: 16px; }
.tbrief { margin: 0; color: var(--vp-c-text-2); font-size: 13px; }
.traits { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 6px; }
.tr { display: flex; gap: 6px; font-size: 12px; padding: 4px 8px; border-radius: 6px; background: var(--vp-c-default-soft); }
.tk { color: var(--vp-c-text-3); white-space: nowrap; }
.stepq { font-size: 13px; font-weight: 600; margin-top: 2px; }
.sq { color: var(--vp-c-brand-1); margin-right: 4px; }
.opts { display: flex; flex-wrap: wrap; gap: 6px; }
.bill { border-top: 1px dashed var(--vp-c-divider); padding-top: 10px; display: flex; flex-direction: column; gap: 6px; }
.b-row { display: flex; gap: 8px; font-size: 13px; }
.bk { min-width: 64px; color: var(--vp-c-text-3); }
.ok { color: var(--vp-c-brand-1); }
.off { color: var(--vp-c-danger-1); }
</style>
