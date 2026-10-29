<script setup lang="ts">
import { ref, computed } from 'vue'

// Agent 闭环剧场：契约闸开关决定"摄氏度"击穿还是被接住（lab01 step6）
const gateOn = ref(true)
const FRAMES = (on: boolean) => [
  { k: 'user', t: '任务：把 25°C 转成华氏度（工具：convert(value: float, unit: "C"|"F")）' },
  { k: 'act', t: '模型生成 tool_call：convert(value="二十五", unit="C")' },
  on
    ? { k: 'gate', t: '语义闸（schema）：value 需要 float，得到 "二十五" → ❌ 校验失败' }
    : { k: 'code', t: '无闸直通：Python 执行 convert("二十五") → 💥 TypeError: unsupported operand' },
  on
    ? { k: 'gate', t: '报错回喂：「value 必须是数字」→ 模型改发 convert(25, "C") → ✓' }
    : { k: 'bad', t: '确定性代码被概率输出击穿——崩溃发生在你的产线，不是模型那里' },
  on
    ? { k: 'obs', t: '执行 → 77°F → 观察回喂 → Finish。闭环成立的前提：模型生成数据，代码解释执行' }
    : { k: 'bad', t: '对照结论：validate=False 的一次运行，就是"没有确定性边界的 agent"的下场' },
]
const idx = ref(0)
const frames = computed(() => FRAMES(gateOn.value))
const KIND: Record<string, string> = { user: '任务', act: '行动', gate: '闸门', obs: '观察', code: '代码', bad: '结论' }
function toggle() { gateOn.value = !gateOn.value; idx.value = 0 }
</script>

<template>
  <div class="lp">
    <div class="row wrap">
      <button type="button" class="wbtn" :aria-pressed="gateOn" @click="toggle">{{ gateOn ? '契约闸：开（推荐）' : '契约闸：关' }}</button>
      <button type="button" class="wbtn" :disabled="idx === 0" @click="idx--">◀</button>
      <button type="button" class="wbtn primary" :disabled="idx === frames.length - 1" @click="idx++">下一步 ▶</button>
      <span class="meta">{{ idx + 1 }} / {{ frames.length }}</span>
    </div>
    <div class="trace">
      <div v-for="(f, i) in frames.slice(0, idx + 1)" :key="i" class="trow" :class="[f.k, { cur: i === idx }]">
        <span class="knd">{{ KIND[f.k] }}</span><span>{{ f.t }}</span>
      </div>
    </div>
    <div class="hint"><span class="k">看什么 · </span>开闸与关闸各走一遍：同一个模型的同一次"口误"，一边被闸门温柔接住并自我修复，一边直接击穿确定性代码——<b>agent 闭环成立的前提是契约，不是模型能力</b>。</div>
  </div>
</template>

<style scoped>
.lp { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.meta { color: var(--vp-c-text-3); font-size: 12.5px; }
.trace { display: flex; flex-direction: column; gap: 8px; }
.trow { display: flex; gap: 10px; font-size: 14.5px; line-height: 1.65; padding: 6px 10px; border-radius: 8px; opacity: .55; }
.trow.cur { opacity: 1; background: var(--vp-c-brand-soft); }
.trow.bad .knd { color: #dc2626; }
.trow.gate .knd { color: var(--vp-c-brand-1); }
.knd { flex: none; font-size: 12px; min-width: 40px; color: var(--vp-c-text-3); padding-top: 2px; }
</style>
