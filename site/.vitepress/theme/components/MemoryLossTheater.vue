<script setup lang="ts">
import { ref, computed } from 'vue'

// 站② · 失忆对照剧场：同一对话流，MemGPT 式记忆管理开/关两种命运（真状态机）
const SCRIPT = [
  { who: 'user', text: '嗨，我叫 Tom，刚搬来镇上。' },
  { who: 'agent', text: '欢迎 Tom！有什么需要帮忙的尽管说。' },
  { who: 'user', text: '附近哪家面包店好吃？' },
  { who: 'agent', text: '集市东头的老皮家最有名，酸面包是招牌。' },
  { who: 'user', text: '我养了一只猫叫 Pi，怕生。' },
  { who: 'agent', text: '记下了——Pi 是只怕生的猫。' },
  { who: 'user', text: '周六镇上有什么活动？' },
  { who: 'agent', text: '周六上午社区大扫除，下午有集市。' },
  { who: 'user', text: '顺便问下，去湖边怎么走？' },
  { who: 'agent', text: '沿主路向西第三个路口北拐，步行十五分钟。' },
  { who: 'user', text: '帮我提醒周五给猫买猫粮。' },
  { who: 'agent', text: '好，周五提醒你买猫粮。' },
  { who: 'user', text: '……聊了这么多，你还记得我叫什么吗？' },
]
const RAM_SIZE = 8
const WRITE_AT = new Set([0, 4]) // 模型决定 core_memory_write 的消息（名字与猫）

const managed = ref(true)
const step = ref(0)
const phase = ref<'idle' | 'playing' | 'quiz' | 'end'>('idle')
const ram = ref<number[]>([])
const evicted = ref<number[]>([])
const archive = ref<number[]>([])
const quizOk = ref<boolean | null>(null)

const cur = computed(() => step.value)
function sleep(ms: number) { return new Promise((r) => setTimeout(r, ms)) }

async function play() {
  ram.value = []; evicted.value = []; archive.value = []; quizOk.value = null
  phase.value = 'playing'
  for (let i = 0; i < SCRIPT.length; i++) {
    step.value = i
    await sleep(700)
    if (managed.value && WRITE_AT.has(i)) {
      archive.value.push(i)
      archive.value = [...archive.value]
      await sleep(300)
    }
    ram.value.push(i)
    ram.value = [...ram.value]
    if (ram.value.length > RAM_SIZE) {
      const out = ram.value.shift()!
      evicted.value.push(out)
      evicted.value = [...evicted.value]
      ram.value = [...ram.value]
    }
  }
  phase.value = 'quiz'
  await sleep(600)
  // 答题：managed → 查档案（写入过 #0）；否则只在 RAM 里找
  quizOk.value = managed.value ? archive.value.includes(0) : ram.value.includes(0)
  phase.value = 'end'
}
function reset() {
  phase.value = 'idle'; step.value = 0
  ram.value = []; evicted.value = []; archive.value = []; quizOk.value = null
}
function msg(i: number) { return SCRIPT[i] }
</script>

<template>
  <div class="mlt">
    <div class="ops">
      <button type="button" class="wbtn" :disabled="phase === 'playing'" @click="play">{{ phase === 'idle' || phase === 'end' ? '▶ 播放对话流' : '…' }}</button>
      <button type="button" class="wbtn" :disabled="phase === 'playing'" @click="reset">↺ 重置</button>
      <div class="sw"><span>记忆管理</span>
        <button type="button" class="wbtn" :aria-pressed="managed" :disabled="phase === 'playing'" @click="managed = !managed">
          {{ managed ? 'MemGPT 式 · 开' : '关闭' }}</button>
      </div>
      <span class="ph">{{ phase === 'idle' ? '待命' : phase === 'playing' ? `播放中 ${cur + 1}/13…` : phase === 'quiz' ? '开始答题…' : quizOk ? '答对了 ✅' : '失忆了 ❌' }}</span>
    </div>

    <div class="stagegrid">
      <div class="pane">
        <div class="pt">工作上下文 · RAM（容量 {{ RAM_SIZE }}，FIFO 淘汰）</div>
        <div class="ram">
          <div v-for="i in ram" :key="i" class="chip" :class="{ cur: i === cur && phase === 'playing' }">
            <span class="cwho">{{ msg(i).who === 'user' ? '👤' : '🤖' }}</span>
            <span class="ctext">{{ msg(i).text }}</span>
          </div>
          <div v-for="n in RAM_SIZE - ram.length" :key="'e' + n" class="chip empty">（空槽）</div>
        </div>
        <div class="pt2">被淘汰（{{ evicted.length }} 条，永久离开上下文）</div>
        <div class="evi">
          <div v-for="i in evicted" :key="i" class="chip gone"><span class="ctext">{{ msg(i).text }}</span></div>
          <div v-if="!evicted.length" class="none">（还没有淘汰）</div>
        </div>
      </div>
      <div class="pane">
        <div class="pt">档案存储 · core_memory（{{ managed ? '模型可写入' : '未启用——淘汰即蒸发' }}）</div>
        <div class="arc">
          <template v-if="managed">
            <div v-for="i in archive" :key="i" class="chip arch">
              <span class="cwr">core_memory_write ←</span>
              <span class="ctext">{{ msg(i).text }}</span>
            </div>
            <div v-if="!archive.length" class="none">（播放中模型会在关键信息处主动写入）</div>
          </template>
          <div v-else class="none big">记忆管理关闭：RAM 满即淘汰，无处可写——最后那道题，靠运气。</div>
        </div>
        <div v-if="phase === 'end'" class="quiz" :class="quizOk ? 'ok' : 'bad'">
          <div class="qq">"你还记得我叫什么吗？"</div>
          <div class="qa">{{ quizOk ? '✅ 档案召回：Tom（第 1 条已被淘汰出 RAM，但写入过档案）' : '❌ RAM 里没有——名字在第 1 条，早被 FIFO 淘汰，且从未写入任何地方' }}</div>
        </div>
      </div>
    </div>

    <div class="hint"><span class="k">机制对位 · </span>RAM 满了 FIFO 无情淘汰（第三幕 MemGPT 分层）；write 是模型的主动决策——记忆操作就是动作空间里的新成员（`core_memory_write`，L01 的 A∪ℒ 再度应验）。同一对话流，两种命运：这就是「上下文窗口 ≠ 记忆」的全部含义。</div>
  </div>
</template>

<style scoped>
.mlt { display: flex; flex-direction: column; gap: 12px; }
.ops { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.sw { display: flex; align-items: center; gap: 4px; font-size: 12px; color: var(--vp-c-text-2); }
.ph { margin-left: auto; font-size: 12px; color: var(--vp-c-text-2); }
.stagegrid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 640px) { .stagegrid { grid-template-columns: 1fr; } }
.pane { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 6px; min-height: 240px; }
.pt { font-size: 12px; font-weight: 600; color: var(--vp-c-text-2); }
.pt2 { font-size: 11px; color: var(--vp-c-text-3); }
.ram { display: flex; flex-direction: column; gap: 3px; min-height: 180px; }
.chip { display: flex; gap: 6px; align-items: center; border-radius: 6px; padding: 3px 8px; font-size: 11.5px; background: var(--vp-c-default-soft); }
.chip.cur { background: var(--vp-c-brand-soft); border: 1px solid var(--vp-c-brand-1); }
.chip.empty { opacity: 0.4; justify-content: center; color: var(--vp-c-text-3); }
.chip.gone { opacity: 0.45; text-decoration: line-through; }
.chip.arch { background: var(--vp-c-brand-soft); border: 1px dashed var(--vp-c-brand-1); }
.cwho { font-size: 12px; }
.ctext { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cwr { font-size: 10px; color: var(--vp-c-brand-1); font-family: var(--vp-font-family-mono, monospace); white-space: nowrap; }
.evi { display: flex; flex-direction: column; gap: 3px; max-height: 90px; overflow-y: auto; }
.arc { display: flex; flex-direction: column; gap: 4px; }
.none { font-size: 12px; color: var(--vp-c-text-3); }
.none.big { font-size: 13px; padding: 12px 0; }
.quiz { border-radius: 8px; padding: 10px; margin-top: auto; }
.quiz.ok { background: var(--vp-c-brand-soft); }
.quiz.bad { background: var(--vp-c-danger-soft); }
.qq { font-size: 13px; font-weight: 600; }
.qa { font-size: 12px; margin-top: 4px; }
</style>
