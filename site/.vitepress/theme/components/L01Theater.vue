<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'

const Q = '问题：除了 Apple Remote，还有什么设备能控制「Apple Remote 最初设计所配套的那个程序」？'

interface Frame {
  k: 'user' | 'thought' | 'act' | 'obs' | 'code' | 'answer' | 'verdict'
  c: string[]
  t: string
  h: string
}

const MODES: Record<string, { owner: string; frames: Frame[] }> = {
  cot: {
    owner: '无循环 · 单次生成',
    frames: [
      { k: 'user', c: ['llm'], t: Q, h: '纯推理模式：模型唯一的信息来源是训练时冻结的参数化记忆——没有任何外部入口。' },
      { k: 'thought', c: ['llm', 'reason'], t: 'Thought：一步步想——Apple Remote 是 Apple TV 的遥控器；Apple TV 可以用 iPhone、iPad、iPod Touch 控制……', h: '推理链本身流畅自洽。问题不在逻辑，在前提：它对「最初配套的程序」的记忆是错的（其实是 Front Row 媒体中心，不是 Apple TV）。' },
      { k: 'answer', c: ['llm'], t: 'Answer：iPhone、iPad、iPod Touch。', h: '幻觉的本质：把参数化记忆当事实输出，而且没有任何机制能发现错误。' },
      { k: 'verdict', c: [], t: '❌ 错误（正确答案：键盘功能键）。环境交互 0 次——它没有「看」，只有「想」。', h: '记住这个结局，切到模式②③对照。' },
    ],
  },
  wf: {
    owner: '代码 · 固定步骤',
    frames: [
      { k: 'user', c: [], t: Q, h: '流水线模式（教学重演）：步骤在写代码时就定死了，LLM 只是被塞进各个槽位里干活。' },
      { k: 'code', c: ['tools'], t: '[代码] 第 1 步（固定）：Search["Apple Remote"] —— 无论问题是什么，第 1 步永远是它。', h: '代码在运行前就决定了所有步骤的顺序。' },
      { k: 'obs', c: ['env', 'memory'], t: 'Obs 1：Apple Remote 于 2005 年 10 月发布……最初设计用于控制 Front Row 媒体中心程序……', h: '流水线至今一切正常。' },
      { k: 'code', c: ['tools'], t: '[代码] 第 2 步（固定）：从 Obs 1 抽取程序名 → Search["Front Row"]', h: '注意：这一步是写死的。代码不会「读懂」将要返回的观察——它只是执行。' },
      { k: 'obs', c: ['env', 'memory'], t: 'Obs 2：未找到 ["Front Row"]。相似条目：[Front Row Seat to Earth（纪录片）、Front Row Motorsports（车队）、Front Row (software)……]', h: '⭐ 全剧场最关键的一帧：正确做法是消歧——改查 "Front Row (software)"。这个决定需要读懂观察的内容，而代码做不到，除非你预先写尽所有分支。' },
      { k: 'code', c: ['tools'], t: '[代码] 第 3 步（固定）：取相似列表第 1 条 → Search["Front Row Seat to Earth"]', h: '机械执行第 1 条——歧义在这一刻变成错误，而且流水线自己毫无察觉。' },
      { k: 'obs', c: ['env'], t: 'Obs 3：一部关于地球科学的纪录片……（与本题无关）', h: '错误继续传播。' },
      { k: 'answer', c: [], t: '[代码] 兜底输出：无法确定，疑似 Apple TV。', h: '每一步都「执行正确」，答案仍然错——这就是死流程。' },
      { k: 'verdict', c: [], t: '❌ 错误。诊断：当下一步取决于观察的内容时，控制流必须交给能「读懂」观察的一方。', h: '现在切到模式③，看同样的歧义撞上循环会发生什么。' },
    ],
  },
  react: {
    owner: '模型 · 边看边决定',
    frames: [
      { k: 'user', c: [], t: Q, h: '同一道题、同一个模型、同一批工具——唯一的变化：下一步由模型在循环里决定（ReAct，讲义 p.36 原例）。' },
      { k: 'thought', c: ['llm', 'reason', 'memory'], t: 'Thought 1：我需要搜索 Apple Remote，找到它最初设计用来控制的程序。', h: '推理是「内部动作」：先改变自己的状态，再决定外部动作。' },
      { k: 'act', c: ['tools'], t: 'Act 1：Search["Apple Remote"]', h: '模型自己选择了工具和参数。' },
      { k: 'obs', c: ['env', 'memory'], t: 'Obs 1：（同前）……最初设计用于控制 Front Row 媒体中心程序……', h: '观察写回上下文——记忆（上下文）在增长，这就是最原始的 agent 记忆。' },
      { k: 'thought', c: ['llm', 'reason', 'memory'], t: 'Thought 2：Apple Remote 最初控制的是 Front Row。我需要搜索 Front Row，看还有什么设备能控制它。', h: '读观察 → 更新计划 → 决定下一个动作。' },
      { k: 'act', c: ['tools'], t: 'Act 2：Search["Front Row"]', h: '同样的搜索动作——但这次是模型自己决定的。' },
      { k: 'obs', c: ['env', 'memory'], t: 'Obs 2：未找到 ["Front Row"]。相似条目：[Front Row Seat to Earth、Front Row Motorsports、Front Row (software)……]', h: '⭐ 同样的歧义撞上来了。流水线在这里必死——看下一帧谁来做决定。' },
      { k: 'thought', c: ['llm', 'reason', 'memory'], t: 'Thought 3：Front Row 没有直接找到。列表里的 "Front Row (software)" 才像媒体中心软件——改搜它。', h: '这就是 agent 的定义性瞬间：模型读懂观察、修改计划、更换动作——控制流在运行时被重写。' },
      { k: 'act', c: ['tools'], t: 'Act 3：Search["Front Row (software)"]', h: '消歧后的搜索——计划已被观察改写。' },
      { k: 'obs', c: ['env', 'memory'], t: 'Obs 3：Front Row 是一款已停产的媒体中心软件……可由 Apple Remote 或键盘功能键控制。', h: '证据到手，可以收敛了。' },
      { k: 'thought', c: ['llm', 'reason'], t: 'Thought 4：Front Row (software) 可由 Apple Remote 或键盘功能键控制。所以答案是键盘功能键。', h: '终答前的最后一步推理。' },
      { k: 'act', c: ['tools'], t: 'Act 4：Finish["键盘功能键"]', h: 'Finish 也是一个工具调用——「停下来」本身同样是模型的决定。' },
      { k: 'verdict', c: [], t: '✅ 正确（键盘功能键）。环境交互 3 次、4 轮循环——模型在 Obs 2 处救回了流水线必死的局。', h: '对照三种模式：能力（同一个 LLM）没变，变的是控制流的归属。这就是 L01 的核心。' },
    ],
  },
}

const KIND_LABEL: Record<string, string> = {
  user: '提问', thought: '思考', act: '行动', obs: '观察', code: '代码', answer: '输出', verdict: '结论',
}
const CHIPS = [
  { id: 'llm', label: 'LLM Core' },
  { id: 'reason', label: '推理' },
  { id: 'memory', label: '记忆' },
  { id: 'tools', label: '工具' },
  { id: 'env', label: '环境' },
]

const mode = ref<keyof typeof MODES>('cot')
const idx = ref(0)
let timer: ReturnType<typeof setInterval> | null = null
const playing = ref(false)

const frames = computed(() => MODES[mode.value].frames)
const cur = computed(() => frames.value[idx.value])
const envCount = computed(() => frames.value.slice(0, idx.value + 1).filter((f) => f.k === 'obs').length)
const visible = computed(() => frames.value.slice(0, idx.value + 1))
const round = computed(() => visible.value.filter((f) => f.k === 'thought').length)

function stopPlay() {
  if (timer) clearInterval(timer)
  timer = null
  playing.value = false
}
function go(m: string, i: number) {
  if (!(m in MODES)) return
  mode.value = m as keyof typeof MODES
  idx.value = Math.max(0, Math.min(i, frames.value.length - 1))
}
function stepTo(m: string, i: number) {
  stopPlay()
  go(m, i)
}
function togglePlay() {
  if (timer) {
    stopPlay()
    return
  }
  if (idx.value === frames.value.length - 1) idx.value = -1
  playing.value = true
  timer = setInterval(() => {
    if (idx.value >= frames.value.length - 1) {
      stopPlay()
      return
    }
    go(mode.value, idx.value + 1)
  }, 1700)
}
onUnmounted(stopPlay)
</script>

<template>
  <div class="theater">
    <div class="row wrap">
      <button v-for="(m, key) in MODES" :key="key" type="button" class="wbtn" :aria-pressed="key === mode"
        @click="stepTo(String(key), 0)">
        {{ { cot: '① 纯推理 CoT', wf: '② 固定流水线 Workflow', react: '③ ReAct Agent' }[key] }}
      </button>
    </div>
    <div class="row wrap">
      <button type="button" class="wbtn" :disabled="idx === 0" @click="stepTo(mode, idx - 1)">◀ 上一步</button>
      <button type="button" class="wbtn primary" :disabled="idx === frames.length - 1" @click="stepTo(mode, idx + 1)">
        下一步 ▶
      </button>
      <button type="button" class="wbtn" @click="togglePlay">{{ playing ? '⏸ 暂停' : '⏵ 自动播放' }}</button>
      <span class="meta">第 {{ idx + 1 }} / {{ frames.length }} 帧 · 环境交互 {{ envCount }} 次</span>
      <span class="pill brand">控制流：{{ MODES[mode].owner }}</span>
    </div>
    <div class="row wrap">
      <span v-for="ch in CHIPS" :key="ch.id" class="chip" :class="{ on: cur.c.includes(ch.id) }">{{ ch.label }}</span>
    </div>
    <div class="row wrap cyc">
      <span class="cyl">循环相位：</span>
      <span class="cy" :class="{ on: cur.k === 'thought' }">思考</span><span class="ca">→</span>
      <span class="cy" :class="{ on: cur.k === 'act' }">行动</span><span class="ca">→</span>
      <span class="cy" :class="{ on: cur.k === 'obs' }">观察</span><span class="ca">↺</span>
      <span class="meta">当前轮次 {{ round }} —— 循环是结构，轨迹只是它的展开</span>
    </div>
    <div class="hint"><span class="k">现在看什么 · </span>{{ cur.h }}</div>
    <div class="trace">
      <div v-for="(f, i) in visible" :key="mode + i" class="trow" :class="[('k-' + f.k), { cur: i === idx, verdict: f.k === 'verdict', ok: f.k === 'verdict' && f.t.startsWith('✅'), bad: f.k === 'verdict' && !f.t.startsWith('✅') }]">
        <span class="kind"><span class="dot" />{{ KIND_LABEL[f.k] }}</span>
        <span class="text">{{ f.t }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.theater { display: flex; flex-direction: column; gap: 9px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.wbtn.primary { background: var(--vp-c-brand-1); border-color: var(--vp-c-brand-1); color: #fff; font-weight: 600; }
.meta { color: var(--vp-c-text-2); font-size: 13px; }
.trace { display: flex; flex-direction: column; gap: 8px; margin-top: 6px; }
.trow { display: flex; gap: 10px; align-items: baseline; opacity: 0.5; }
.trow.cur { opacity: 1; background: var(--vp-c-brand-soft); border-radius: 8px; padding: 6px 10px; margin: 0 -10px; }
.kind { flex: none; font-size: 12px; min-width: 54px; display: inline-flex; align-items: center; gap: 5px; color: var(--vp-c-text-2); }
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--vp-c-text-3); flex: none; }
.k-thought .dot { background: #8b5cf6; }
.k-act .dot { background: #3b82f6; }
.k-obs .dot { background: #d97706; }
.k-code .dot { background: #0d9488; }
.text { font-size: 14.5px; line-height: 1.7; }
.verdict .text { font-weight: 600; }
.verdict.ok .text { color: #16a34a; }
.verdict.bad .text { color: #dc2626; }
.cyc .cy { font-size: 12.5px; padding: 2px 11px; border-radius: 999px; background: var(--vp-c-default-soft); color: var(--vp-c-text-2); }
.cyc .cy.on { background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); font-weight: 700; }
.cyc .ca { color: var(--vp-c-text-3); font-size: 12px; }
.cyc .cyl { font-size: 12.5px; color: var(--vp-c-text-3); }
</style>
