<script setup lang="ts">
import { ref, computed } from 'vue'

// 站③ · 事件溯源持久执行的浏览器复刻：执行 → 崩溃 → 恢复（开=重放跳过 / 关=全部重来）
const STEPS = [
  { id: 1, name: '拉取订单数据', api: '外部 API ×2' },
  { id: 2, name: '清洗去重', api: '纯代码' },
  { id: 3, name: 'LLM 摘要分析', api: 'LLM 调用 ×3' },
  { id: 4, name: '写入报表', api: '外部 API ×1' },
]

interface Ev { n: number; text: string; kind: 'run' | 'crash' | 'replay' }
const events = ref<Ev[]>([])
const phase = ref<'idle' | 'running' | 'crashed' | 'done'>('idle')
const curStep = ref(0)
const doneSet = ref<Set<number>>(new Set())
const durable = ref(true)
const crashAt = ref(3)
const executed = ref(0)   // 真实执行过的步骤数（成本）
const replayed = ref(0)   // 恢复时重放跳过的步骤数
let evSeq = 0

function sleep(ms: number) { return new Promise((r) => setTimeout(r, ms)) }

async function run() {
  if (phase.value === 'running') return
  const from = phase.value === 'idle' ? 1 : (durable.value ? crashAt.value + 1 : 1)
  if (phase.value === 'crashed' && durable.value) {
    // 持久恢复：先重放已完成事件（快速扫过、跳过执行）
    const done = STEPS.slice(0, crashAt.value)
    for (let i = 0; i < done.length; i++) {
      await sleep(260)
      events.value.push({ n: ++evSeq, text: `重放历史#${done[i].id} ${done[i].name}（已成功，跳过执行）`, kind: 'replay' })
      replayed.value++
    }
  } else if (phase.value === 'crashed' && !durable.value) {
    doneSet.value = new Set()
    events.value.push({ n: ++evSeq, text: '无持久化：状态全丢，从第 1 步重来', kind: 'crash' })
  }
  phase.value = 'running'
  for (let i = from; i <= STEPS.length; i++) {
    curStep.value = i
    await sleep(650)
    executed.value++
    doneSet.value.add(i)
    doneSet.value = new Set(doneSet.value)
    events.value.push({ n: ++evSeq, text: `执行 #${STEPS[i - 1].id} ${STEPS[i - 1].name}（${STEPS[i - 1].api}）→ 成功`, kind: 'run' })
    if (i === crashAt.value && i < STEPS.length) {
      events.value.push({ n: ++evSeq, text: `⚡ worker 进程崩溃（第 ${crashAt.value} 步后）——执行历史已落盘`, kind: 'crash' })
      phase.value = 'crashed'
      return
    }
  }
  curStep.value = 0
  phase.value = 'done'
  events.value.push({ n: ++evSeq, text: '✓ Workflow 完成', kind: 'run' })
}

function reset() {
  events.value = []
  phase.value = 'idle'
  curStep.value = 0
  doneSet.value = new Set()
  executed.value = 0
  replayed.value = 0
}

const running = computed(() => phase.value === 'running')
</script>

<template>
  <div class="dr">
    <div class="ops">
      <button type="button" class="wbtn" :disabled="running || phase === 'done'"
        @click="run">{{ phase === 'crashed' ? '⟳ 恢复' : phase === 'idle' ? '▶ 开始执行' : '…' }}</button>
      <button type="button" class="wbtn" :disabled="running" @click="reset">↺ 重置</button>
      <div class="sw"><span>持久执行</span>
        <button type="button" class="wbtn mini" :aria-pressed="durable" @click="durable = !durable">{{ durable ? 'Temporal 开' : '关（进程内）' }}</button>
      </div>
      <div class="sw"><span>崩溃点</span>
        <button type="button" class="wbtn mini" :aria-pressed="crashAt === 3" :disabled="running || phase !== 'idle'"
          @click="crashAt = 3">第 3 步后</button>
        <button type="button" class="wbtn mini" :aria-pressed="crashAt === 2" :disabled="running || phase !== 'idle'"
          @click="crashAt = 2">第 2 步后</button>
      </div>
      <span class="ph">状态：{{ phase === 'idle' ? '待命' : phase === 'running' ? '执行中…' : phase === 'crashed' ? '已崩溃（历史在服务端）' : '完成 ✓' }}</span>
    </div>

    <div class="flow">
      <div v-for="s in STEPS" :key="s.id" class="node" :class="{
        cur: curStep === s.id && running,
        done: doneSet.has(s.id),
      }">
        <span class="nid">#{{ s.id }}</span>
        <span class="nname">{{ s.name }}</span>
        <span class="napi">{{ s.api }}</span>
      </div>
    </div>

    <div class="cols">
      <div class="log">
        <div class="lt">执行历史（append-only · 服务端落盘）</div>
        <div class="lv">
          <div v-for="e in [...events].reverse()" :key="e.n" class="ev" :class="e.kind">
            <span class="en">#{{ e.n }}</span>
            <span>{{ e.text }}</span>
          </div>
          <div v-if="!events.length" class="ev empty">（空——点「开始执行」）</div>
        </div>
      </div>
      <div class="bill">
        <div class="lt">成本账单</div>
        <div class="b-row"><span class="bk">真实执行</span><span><b>{{ executed }}</b> 步（外部调用都算钱）</span></div>
        <div class="b-row"><span class="bk">重放跳过</span><span>{{ replayed }} 步（读历史，零成本）</span></div>
        <div class="bar-wrap">
          <div class="bar-label">持久版累计执行</div>
          <div class="track"><div class="fill okf" :style="{ width: Math.min(100, (executed / 4) * 100) + '%' }" /></div>
          <div class="bar-num">{{ executed }}/4</div>
        </div>
        <div class="bar-wrap">
          <div class="bar-label">若全程无持久化重跑一次</div>
          <div class="track"><div class="fill badf" :style="{ width: Math.min(100, ((executed + replayed) / 8) * 100) + '%' }" /></div>
          <div class="bar-num">{{ executed + replayed }}/8</div>
        </div>
      </div>
    </div>

    <div class="hint"><span class="k">机制对位 · </span>Workflow 不是"直接执行"，是被 Runtime 记录为事件流并落盘（第四幕事件溯源）；崩溃恢复 = 从历史重放、跳过已成功步——这就是「最小持久执行」：一个事件列表 + 一个 execute(workflow, history)。</div>
  </div>
</template>

<style scoped>
.dr { display: flex; flex-direction: column; gap: 12px; }
.ops { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.sw { display: flex; align-items: center; gap: 4px; font-size: 12px; color: var(--vp-c-text-2); }
.wbtn.mini { padding: 2px 8px; font-size: 12px; }
.ph { margin-left: auto; font-size: 12px; color: var(--vp-c-text-2); }
.flow { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 6px; }
.node { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 8px 10px; display: flex; flex-direction: column; gap: 2px; font-size: 12px; transition: all 0.2s; }
.node.cur { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.node.done { border-color: var(--vp-c-brand-1); }
.node.done .nid::after { content: ' · 完成'; color: var(--vp-c-brand-1); }
.nid { color: var(--vp-c-text-3); font-size: 11px; }
.nname { font-weight: 600; font-size: 13px; }
.napi { color: var(--vp-c-text-3); font-size: 11px; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 640px) { .cols { grid-template-columns: 1fr; } }
.lt { font-size: 12px; font-weight: 600; color: var(--vp-c-text-2); margin-bottom: 6px; }
.log { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; }
.lv { display: flex; flex-direction: column; gap: 3px; max-height: 220px; overflow-y: auto; }
.ev { display: flex; gap: 6px; font-size: 11.5px; font-family: var(--vp-font-family-mono, monospace); padding: 2px 6px; border-radius: 4px; }
.ev.run { color: var(--vp-c-text-2); }
.ev.crash { color: var(--vp-c-danger-1); background: var(--vp-c-danger-soft); }
.ev.replay { color: var(--vp-c-text-3); background: var(--vp-c-default-soft); }
.ev.empty { color: var(--vp-c-text-3); }
.en { color: var(--vp-c-text-3); min-width: 28px; }
.bill { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 6px; }
.b-row { display: flex; gap: 8px; font-size: 12.5px; }
.bk { min-width: 64px; color: var(--vp-c-text-3); }
.bar-wrap { display: flex; align-items: center; gap: 6px; font-size: 11px; }
.bar-label { min-width: 110px; color: var(--vp-c-text-3); }
.track { flex: 1; height: 10px; background: var(--vp-c-default-soft); border-radius: 999px; overflow: hidden; }
.fill { height: 100%; transition: width 0.4s; }
.okf { background: var(--vp-c-brand-1); }
.badf { background: var(--vp-c-danger-1); }
.bar-num { min-width: 32px; text-align: right; }
</style>
