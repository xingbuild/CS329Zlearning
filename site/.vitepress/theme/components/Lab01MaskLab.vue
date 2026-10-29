<script setup lang="ts">
import { ref, computed } from 'vue'

// 掩码解码实验室：迷你文法 {"name":"<字母>","age":<数字>}
// VOCAB 下标即 token id；STATES/TRANSIT 构成手写 NFA
const VOCAB = ['{"', 'name', '":"', ' ', 'Ada', 'Lovelace', 'ada', '",', '"age"', ':', '42', '4', '2', '99', '}', 'true', 'True', '"']
const STATES: Record<string, number[]> = {
  start: [0], key1: [1], nvq: [2], name_v: [3, 4, 5, 6, 7], key2: [8],
  age_c: [9], age_v: [10, 11, 12, 13], close: [14], done: [],
}
const TRANSIT: Record<string, Record<number, string>> = {
  start: { 0: 'key1' }, key1: { 1: 'nvq' }, nvq: { 2: 'name_v' },
  name_v: { 3: 'name_v', 4: 'name_v', 5: 'name_v', 6: 'name_v', 7: 'key2' },
  key2: { 8: 'age_c' }, age_c: { 9: 'age_v' },
  age_v: { 10: 'close', 11: 'age_v', 12: 'age_v', 13: 'age_v' }, close: { 14: 'done' }, done: {},
}
const state = ref('start')
const prefix = ref('')
const mode = ref<'masked' | 'raw'>('masked')
const crashed = ref(false)
const lastNote = ref('就绪')
const visits: Record<string, number> = {}

// 模型偏好（剧本式推进）：name 值 = Ada + 空格 + Lovelace + 收尾；age 值 = Python 习惯想发 true
function pref(): number {
  const s = state.value
  if (s === 'name_v') {
    visits.name_v = (visits.name_v || 0) + 1
    return [4, 3, 5, 7][Math.min(visits.name_v - 1, 3)]
  }
  if (s === 'age_v') return 15 // true —— JSON 非法，戏剧核心
  return (STATES[s] || [])[0]
}
function allowed(t: number) { return (STATES[state.value] || []).includes(t) }
function take(t: number, note: string) {
  prefix.value += VOCAB[t]
  state.value = TRANSIT[state.value][t]
  lastNote.value = note
}
function step() {
  if (state.value === 'done' || crashed.value) return
  const t = pref()
  if (allowed(t)) { take(t, `模型偏好 ${JSON.stringify(VOCAB[t])} ✓ 合法，直接采纳`); return }
  if (mode.value === 'masked') {
    // 掩蔽 ✗ → 从合法集改选（偏好最长者，能收尾就收尾）
    const alt = (STATES[state.value] || []).slice().sort((a, b) => VOCAB[b].length - VOCAB[a].length)[0]
    take(alt, `模型想发 ${JSON.stringify(VOCAB[t])} → 掩蔽 ✗ → 被迫改选合法 token ${JSON.stringify(VOCAB[alt])}`)
  } else {
    prefix.value += VOCAB[t]
    crashed.value = true
    lastNote.value = `裸采样上屏 ${JSON.stringify(VOCAB[t])}`
  }
}
function reset() { state.value = 'start'; prefix.value = ''; crashed.value = false; lastNote.value = '就绪'; visits.name_v = 0 }
function setMode(m: 'masked' | 'raw') { mode.value = m; reset() }

const stateName: Record<string, string> = {
  start: '起点', key1: '等键名', nvq: '等冒号引号', name_v: 'name 取值中', key2: '等 age 键',
  age_c: '等冒号', age_v: 'age 取值中', close: '等右括号', done: '完成 ✓',
}
const done = computed(() => state.value === 'done')
</script>

<template>
  <div class="mlab">
    <div class="row wrap">
      <button type="button" class="wbtn" :aria-pressed="mode === 'masked'" @click="setMode('masked')">掩码 ON（约束解码）</button>
      <button type="button" class="wbtn" :aria-pressed="mode === 'raw'" @click="setMode('raw')">掩码 OFF（裸采样对照）</button>
      <button type="button" class="wbtn primary" :disabled="done || crashed" @click="step">步进（模型偏好）</button>
      <button type="button" class="wbtn" @click="reset">重置</button>
      <span class="pill brand">NFA：{{ crashed ? '❌ 已损坏' : stateName[state] }}</span>
    </div>
    <div class="prefix" :class="{ bad: crashed }">{{ prefix }}<span v-if="!crashed && !done" class="caret">▏</span></div>
    <div v-if="crashed" class="crash">❌ 语法损坏：模型在 age 值处按 Python 习惯发了 <code>true</code>——裸采样的世界没有护栏，这就是失败动物园里那 ~30% 失败率的微观机制。<b>同一套偏好，掩码 ON 时 true 被清零、模型被逼改选数字。</b></div>
    <div v-else-if="done" class="okk">✅ <code>{{ prefix }}</code> —— 语法 100% 合法。注意代价：语义仍不保证（age=99 也合法）→ 现实系统 = 掩码 + 校验闸双层。</div>
    <div v-else class="note">{{ lastNote }}</div>
    <div class="vocab">
      <div v-for="(t, i) in VOCAB" :key="i" class="tok" :class="{ ok: allowed(i) && mode === 'masked', no: !allowed(i) && mode === 'masked' }">{{ t || '␣' }}<span class="mark">{{ mode === 'masked' ? (allowed(i) ? '✓' : '✗') : '' }}</span></div>
    </div>
    <div class="hint"><span class="k">现在看什么 · </span>
      <template v-if="mode === 'raw'">对照模式：同一个模型、同一套偏好——一路步进到 age 值处看它崩；然后切掩码 ON 重走一遍，<b>保证由构造而来，不是模型变乖</b>。</template>
      <template v-else-if="state === 'age_v'">关键时刻就在下一步：模型的 Python 习惯想发 <code>true</code>（词表已标 ✗）——步进看它被逼改道。</template>
      <template v-else>每 token 的 ✓/✗ 即 NFA 掩码：合法集随前缀变化，非法概率清零、剩余重归一化（与温度/截断同族数学）。</template>
    </div>
    <div class="cross">
      <div class="ct">加演 · token × 字符粒度的跨界回退（原著 <code>'ice":'</code> 剧）</div>
      <div class="cb">假设词表里还有 token <code>ce":</code>：当前缀已生成到 <code>...Lovelace</code> 尾部的 <code>ce</code> 时，这个 token 与前缀重叠 2 个字符——<b>越界，整个 token 作废</b>，解码退回单字符 <code>c</code>、<code>e</code>、<code>":</code> 逐字走。XGrammar（2024）解决的正是"token 集合 × 文法状态"的这个求交问题——真实实现比查表掩码难得多。</div>
    </div>
  </div>
</template>

<style scoped>
.mlab { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.prefix { font-family: var(--vp-font-family-mono, monospace); font-size: 15.5px; background: var(--vp-c-default-soft); border-radius: 8px; padding: 8px 14px; min-height: 38px; word-break: break-all; }
.prefix.bad { background: rgba(220,38,38,.1); color: #dc2626; }
.caret { color: var(--vp-c-brand-1); animation: blink 1s step-end infinite; }
@keyframes blink { 50% { opacity: 0; } }
.crash { font-size: 14px; line-height: 1.7; background: rgba(220,38,38,.08); border-radius: 9px; padding: 10px 14px; }
.okk { font-size: 14px; line-height: 1.7; background: rgba(22,163,74,.08); border-radius: 9px; padding: 10px 14px; }
.note { font-size: 13px; color: var(--vp-c-text-2); }
.vocab { display: flex; flex-wrap: wrap; gap: 6px; }
.tok { font-family: var(--vp-font-family-mono, monospace); font-size: 13px; border: 1px solid var(--vp-c-divider); border-radius: 6px; padding: 3px 8px; display: flex; gap: 5px; align-items: center; }
.tok.ok { border-color: #16a34a; color: #16a34a; }
.tok.no { opacity: .38; text-decoration: line-through; }
.mark { font-size: 10.5px; }
.cross { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 10px 14px; }
.ct { font-size: 13.5px; font-weight: 650; margin-bottom: 4px; color: var(--vp-c-brand-1); }
.cb { font-size: 13.5px; line-height: 1.7; color: var(--vp-c-text-2); }
</style>
