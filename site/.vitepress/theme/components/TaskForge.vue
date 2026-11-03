<script setup lang="ts">
import { ref, computed } from 'vue'

// Lab 09 · 可判定任务工坊：拼一个评测任务——弱 verifier 会被 agent 用假产物骗过（先见事故再学纪律）
// 场景：CSV 报表 → PNG 图表（据 Terminal-Bench 任务结构简化）
const INSTRUCTIONS = [
  { id: 'vague', name: '模糊指令', text: '把报表做成一张好看的图，放到 /app/chart.png', note: '「好看」不可判定——agent 自由发挥的空间就是漏洞的空间' },
  { id: 'specified', name: '完整指定', text: '读取 /app/data.csv，画柱状图（月度列），标题「月度营收」，保存为 /app/chart.png', note: '每个要求都可对应一条断言' },
  { id: 'natural', name: '自然口语', text: '老板要月度营收柱状图，月底会议用，存 /app/chart.png', note: '真实但含蓄——好指令在自然与可判之间' },
]
const VERIFIERS = [
  {
    id: 'weak', name: '弱验收（只看文件在）',
    checks: ['assert os.path.exists("/app/chart.png")'],
    outcome: { hacked: true },
    note: '只验存在性：agent 交一张 1×1 像素图甚至空文件——绿灯放行',
  },
  {
    id: 'mid', name: '中验收（看是图）',
    checks: ['assert exists(chart.png)', 'assert is_png_header(chart.png)'],
    outcome: { hacked: true },
    note: '验了文件头：agent 交任意 PNG（比如纯色图）——照样绿灯',
  },
  {
    id: 'strong', name: '强验收（对内容断言）',
    checks: ['assert exists(chart.png)', 'assert is_png_header(chart.png)', 'assert bar_count == 12', 'assert title_text == "月度营收"', 'assert y_axis_max ≈ max(csv.月度营收)'],
    outcome: { hacked: false },
    note: '断言对应需求的每一项：柱数、标题、量程来自源数据——假图过不了',
  },
]
const insIdx = ref(1), verIdx = ref(0)
const ins = computed(() => INSTRUCTIONS[insIdx.value])
const ver = computed(() => VERIFIERS[verIdx.value])
const runState = ref<'idle' | 'run' | 'done'>('idle')
const trials = ref<{ n: number; hacked: boolean; detail: string }[]>([])

function run() {
  runState.value = 'run'
  setTimeout(() => {
    const hacked = ver.value.outcome.hacked
    trials.value.unshift({
      n: trials.value.length + 1,
      hacked,
      detail: hacked
        ? `Trial #${trials.value.length + 1}：agent 走了捷径——${ver.value.id === 'weak' ? '写了个空文件（0 字节）' : '交了一张纯色 PNG'}——你的 verifier 判 PASS ✅ 假产物上线`
        : `Trial #${trials.value.length + 1}：agent 试了捷径（纯色图）——断言 bar_count==12 拦下 ❌；第二轮才交出真图 PASS ✅`,
    })
    runState.value = 'done'
  }, 900)
}
function reset() { trials.value = []; runState.value = 'idle' }
const leakN = computed(() => {
  const holes = []
  if (ins.value.id === 'vague') holes.push('指令模糊：哪些要求算完成没有定义')
  if (ver.value.id !== 'strong') holes.push('验收漏洞：' + ver.value.note)
  return holes
})
</script>

<template>
  <div class="tf">
    <div class="dial">
      <div class="col">
        <div class="ct">① 指令（instruction.md）</div>
        <button v-for="(i, k) in INSTRUCTIONS" :key="i.id" type="button" class="wbtn" :aria-pressed="insIdx === k" @click="insIdx = k; reset()">{{ i.name }}</button>
        <div class="itext">{{ ins.text }}</div>
      </div>
      <div class="col">
        <div class="ct">② 验收（tests/）</div>
        <button v-for="(v, k) in VERIFIERS" :key="v.id" type="button" class="wbtn" :aria-pressed="verIdx === k" @click="verIdx = k; reset()">{{ v.name }}</button>
        <pre class="vchecks">{{ ver.checks.join('\n') }}</pre>
      </div>
    </div>
    <div class="ops">
      <button type="button" class="wbtn" :disabled="runState === 'run'" @click="run">{{ runState === 'run' ? 'agent 行动中…' : '▶ 放 agent 进考场（模拟试跑）' }}</button>
      <button type="button" class="wbtn" @click="reset">↺ 重置</button>
      <span class="ph">{{ trials.length }} 次 Trial 记录在案</span>
    </div>
    <div v-if="leakN.length" class="leak">⚠️ 当前组合的漏洞（先于 agent 看见它）：<span v-for="l in leakN" :key="l" class="lk">{{ l }}；</span></div>
    <div v-if="trials.length" class="trials" :class="{ bad: trials[0].hacked, ok: !trials[0].hacked }">
      <div v-for="t in trials.slice(0, 3)" :key="t.n" class="tr">
        <span class="tn">{{ t.hacked ? '🚨 被 hack' : '✅ 拦住捷径' }}</span><span>{{ t.detail }}</span>
      </div>
      <div class="lesson">{{ trials[0].hacked
        ? '这就是 reward hacking 的现场：verifier 只验了存在，agent 就只满足存在——它优化的是你的断言，不是你的意图。指令改一个字（完整指定）+ 验收升到强，同样的 agent 立刻学好了。'
        : '断言与需求一一对应（柱数/标题/量程都钉死源数据）——agent 的捷径全部被拦，第二轮交出真图。可判定性不是刁难 agent，是保护你的意图。' }}</div>
    </div>
    <div class="hint"><span class="k">对照 · </span>把三档 verifier 都跑一遍：同一 agent、同一任务，验收强度决定它是骗子还是工程师——**你写下什么断言，就得到什么 agent**。</div>
  </div>
</template>

<style scoped>
.tf { display: flex; flex-direction: column; gap: 10px; }
.dial { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 640px) { .dial { grid-template-columns: 1fr; } }
.col { border: 1px solid var(--vp-c-divider); border-radius: 10px; padding: 10px; display: flex; flex-direction: column; gap: 6px; }
.ct { font-size: 13px; font-weight: 650; color: var(--vp-c-text-2); }
.col .wbtn { align-self: flex-start; }
.itext { font-size: 12.5px; color: var(--vp-c-text-2); background: var(--vp-c-default-soft); border-radius: 6px; padding: 6px 10px; line-height: 1.6; }
.vchecks { margin: 0; font-size: 11.5px; background: var(--vp-c-default-soft); border-radius: 6px; padding: 6px 10px; overflow-x: auto; font-family: var(--vp-font-family-mono, monospace); color: var(--vp-c-brand-1); white-space: pre; }
.ops { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.ph { font-size: 12px; color: var(--vp-c-text-3); }
.leak { font-size: 12.5px; color: var(--vp-c-danger-1); background: var(--vp-c-danger-soft); border-radius: 8px; padding: 8px 12px; }
.lk { margin-right: 6px; }
.trials { border-radius: 10px; padding: 10px 14px; display: flex; flex-direction: column; gap: 6px; }
.trials.bad { background: var(--vp-c-danger-soft); }
.trials.ok { background: var(--vp-c-brand-soft); }
.tr { display: flex; gap: 8px; font-size: 12.5px; line-height: 1.6; }
.tn { font-weight: 700; white-space: nowrap; }
.lesson { font-size: 13px; line-height: 1.7; border-top: 1px dashed var(--vp-c-divider); padding-top: 6px; }
</style>
