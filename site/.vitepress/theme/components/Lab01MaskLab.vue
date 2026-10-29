<script setup lang="ts">
import { ref, computed } from 'vue'

// 掩码解码实验室（教学版）：手写 schema 专用 NFA，逐 token 步进
// 契约：{"name": "<字母空格>", "age": <数字>}
const VOCAB = ['{"', '"name"', '":', ' ', 'Ada', 'Lovelace', 'ada', 'lov', 'e":', '",', '"age"', ':', '42', '4', '2', '99', '}', 'true', 'True', '"']

// 手写状态机：每个状态给出下一批合法 token id
const STATES: Record<string, number[]> = {
  start: [0],
  key1: [1], name_q: [2], name_v: [3, 4, 5, 6, 7], // name 值：空格/Ada/Lovelace/ada/lov
  name_end: [8], comma: [9], key2: [10], age_c: [11], age_v: [12, 13, 14, 15],
  age_end: [16], done: [],
}
const TRANSIT: Record<string, Record<number, string>> = {
  start: { 0: 'key1' }, key1: { 1: 'name_q' }, name_q: { 2: 'name_v' },
  name_v: { 3: 'name_v', 4: 'name_v', 5: 'name_v', 6: 'name_v', 7: 'name_end' },
  name_end: { 8: 'comma' }, comma: { 9: 'key2' }, key2: { 10: 'age_c' },
  age_c: { 11: 'age_v' }, age_v: { 12: 'age_end', 13: 'age_v', 14: 'age_v', 15: 'age_v' },
  age_end: { 16: 'done' }, done: {},
}
const state = ref('start')
const prefix = ref('')
const picked = ref('')
const showMask = ref(true)

function allowed(tid: number) {
  return (STATES[state.value] || []).includes(tid)
}
function take(tid: number) {
  if (!allowed(tid)) return
  prefix.value += VOCAB[tid]
  picked.value = VOCAB[tid]
  state.value = TRANSIT[state.value][tid]
}
function reset() { state.value = 'start'; prefix.value = ''; picked.value = '' }

const stateName: Record<string, string> = {
  start: '起点', key1: '等键名', name_q: '等冒号', name_v: 'name 取值中',
  name_end: '值收尾 e":', comma: '等逗号', key2: '等 age 键', age_c: '等冒号',
  age_v: 'age 取值中', age_end: '等右括号', done: '完成 ✓',
}
const maskOn = computed(() => (STATES[state.value] || []).length > 0 && showMask.value)
const done = computed(() => state.value === 'done')
</script>

<template>
  <div class="mlab">
    <div class="row wrap">
      <button type="button" class="wbtn primary" :disabled="done" @click="take((STATES[state] || [])[0])">步进（贪心取首个合法 token）</button>
      <button type="button" class="wbtn" @click="reset">重置</button>
      <label class="sw"><input type="checkbox" v-model="showMask" /> 显示掩码</label>
      <span class="pill brand">NFA 状态：{{ stateName[state] }}</span>
    </div>
    <div class="prefix">{{ prefix }}<span class="caret">▏</span></div>
    <div class="vocab">
      <div v-for="(t, i) in VOCAB" :key="i" class="tok" :class="{ ok: allowed(i), no: !allowed(i) && maskOn }"
        @click="take(i)">{{ t || '␣' }}<span class="mark">{{ allowed(i) ? '✓' : (maskOn ? '✗ 掩蔽' : '') }}</span></div>
    </div>
    <div class="hint"><span class="k">现在看什么 · </span>
      <template v-if="state === 'name_v'">注意 <code>lov</code> 合法而 <code>ada</code> 被掩蔽——合法集随前缀变化；若模型"想"输出小写 <code>ada</code>，掩码逼它换道（Ada Lovelace → adalovelace 的原著剧情）。</template>
      <template v-else-if="state === 'age_v'">数字区：<code>true</code>/<code>True</code>/<code>"</code> 全被掩蔽——"保证由构造而来"：语法错不进输出，根本不需要"修复"。</template>
      <template v-else-if="done">生成完毕：这条 JSON 语法 100% 合法——不是模型变乖了，是非法 token 一路被掩掉。代价：语义仍不保证（age=99 也合法）。</template>
      <template v-else>每个 token 上的 ✓/✗ 就是 NFA 掩码：合法 token 的概率重归一化，非法的清零。关闭"显示掩码"感受一下没有边界约束的裸采样。</template>
    </div>
  </div>
</template>

<style scoped>
.mlab { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.sw { display: flex; align-items: center; gap: 6px; font-size: 13.5px; cursor: pointer; }
.prefix { font-family: var(--vp-font-family-mono, monospace); font-size: 16px; background: var(--vp-c-default-soft); border-radius: 8px; padding: 8px 14px; min-height: 38px; }
.caret { color: var(--vp-c-brand-1); animation: blink 1s step-end infinite; }
@keyframes blink { 50% { opacity: 0; } }
.vocab { display: flex; flex-wrap: wrap; gap: 6px; }
.tok { font-family: var(--vp-font-family-mono, monospace); font-size: 13px; border: 1px solid var(--vp-c-divider); border-radius: 6px; padding: 3px 8px; cursor: pointer; display: flex; gap: 5px; align-items: center; }
.tok.ok { border-color: #16a34a; color: #16a34a; background: rgba(22,163,74,.06); }
.tok.no { opacity: .38; text-decoration: line-through; cursor: not-allowed; }
.mark { font-size: 10.5px; }
</style>
