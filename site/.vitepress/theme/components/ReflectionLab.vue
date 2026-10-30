<script setup lang="ts">
import { ref, computed } from 'vue'

// 站② · 反思对照实验：无反思 / 自评 / 外部反馈 三模式的蒙特卡洛真算
// 概率表依据：Huang et al. 2023（LLMs Cannot Self-Correct Reasoning Yet——自评把对的改错）
const MODES = [
  { id: 'none', name: '无反思', desc: '答完就走', fix: 0, breakIt: 0 },
  { id: 'self', name: '自评反思', desc: '让模型自己检查自己的答案', fix: 0.15, breakIt: 0.22 },
  { id: 'outer', name: '外部反馈', desc: '跑测试 / 对照信源，用外部信号检查', fix: 0.82, breakIt: 0.02 },
]
const P0 = 0.55        // 首答正确率
const N_QUESTIONS = 30 // 每轮题数

interface Round { n: number; none: number; self: number; outer: number }
const rounds = ref<Round[]>([])

const stats = computed(() => {
  if (!rounds.value.length) return null
  const n = rounds.value.length
  const sum = rounds.value.reduce((a, r) => ({ none: a.none + r.none, self: a.self + r.self, outer: a.outer + r.outer }), { none: 0, self: 0, outer: 0 })
  return {
    n,
    none: (sum.none / n / N_QUESTIONS) * 100,
    self: (sum.self / n / N_QUESTIONS) * 100,
    outer: (sum.outer / n / N_QUESTIONS) * 100,
  }
})

function runRound() {
  const acc: Record<string, number> = { none: 0, self: 0, outer: 0 }
  for (const m of MODES) {
    for (let i = 0; i < N_QUESTIONS; i++) {
      let ok = Math.random() < P0
      if (!ok && Math.random() < m.fix) ok = true
      else if (ok && Math.random() < m.breakIt) ok = false
      if (ok) acc[m.id]++
    }
  }
  rounds.value.push({ n: rounds.value.length + 1, ...acc })
}
function reset() { rounds.value = [] }
</script>

<template>
  <div class="rl">
    <div class="ops">
      <button type="button" class="wbtn" @click="runRound">▶ 跑一轮（三模式 × 30 题）</button>
      <button type="button" class="wbtn" @click="reset">↺ 重置</button>
      <span class="rn">已跑 {{ rounds.length }} 轮</span>
    </div>

    <div class="modes">
      <div v-for="m in MODES" :key="m.id" class="mcard">
        <div class="mn">{{ m.name }}</div>
        <div class="md">{{ m.desc }}</div>
        <div class="mp">错题改对率 {{ (m.fix * 100).toFixed(0) }}% · 对题改错率 {{ (m.breakIt * 100).toFixed(0) }}%</div>
        <div v-if="stats" class="mbar-wrap">
          <div class="track"><div class="fill" :class="m.id" :style="{ width: stats[m.id] + '%' }" /></div>
          <div class="mnum">{{ stats[m.id].toFixed(1) }}%</div>
        </div>
        <div v-else class="mempty">未跑</div>
      </div>
    </div>

    <div v-if="rounds.length" class="hist">
      <div class="ht">逐轮正确率（30 题折算）——看噪声与差距</div>
      <div v-for="r in [...rounds].slice().reverse().slice(0, 6)" :key="r.n" class="hr">
        <span class="hn">第 {{ r.n }} 轮</span>
        <span>无反思 {{ r.none }}/30</span>
        <span class="hl">自评 {{ r.self }}/30</span>
        <span class="ho">外反馈 {{ r.outer }}/30</span>
      </div>
    </div>

    <div class="hint"><span class="k">机制对位 · </span>自评的伤不在"改不动错题"（15% 也是改进），在"把对的改错"（22%）——不可判定的信号比没有信号更危险（Huang 2023）。外部反馈赢在可判定：测试结果不会恭维模型。这就是 Reflexion 必须依赖外部信号、而今天 reasoning 模型的"自我修正"其实是 RLVR 内化（L02）的分界线。</div>
  </div>
</template>

<style scoped>
.rl { display: flex; flex-direction: column; gap: 12px; }
.ops { display: flex; gap: 6px; align-items: center; }
.rn { font-size: 12px; color: var(--vp-c-text-2); margin-left: auto; }
.modes { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
.mcard { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 5px; }
.mn { font-weight: 600; font-size: 14px; }
.md { font-size: 12px; color: var(--vp-c-text-2); }
.mp { font-size: 11px; color: var(--vp-c-text-3); }
.mbar-wrap { display: flex; align-items: center; gap: 6px; }
.track { flex: 1; height: 12px; background: var(--vp-c-default-soft); border-radius: 999px; overflow: hidden; }
.fill { height: 100%; transition: width 0.5s; }
.fill.none { background: var(--vp-c-text-3); }
.fill.self { background: var(--vp-c-danger-1); }
.fill.outer { background: var(--vp-c-brand-1); }
.mnum { font-size: 12px; font-weight: 600; min-width: 44px; }
.mempty { font-size: 12px; color: var(--vp-c-text-3); }
.hist { border-top: 1px dashed var(--vp-c-divider); padding-top: 8px; }
.ht { font-size: 12px; font-weight: 600; color: var(--vp-c-text-2); margin-bottom: 4px; }
.hr { display: flex; gap: 14px; font-size: 12px; padding: 2px 0; }
.hn { color: var(--vp-c-text-3); min-width: 52px; }
.hl { color: var(--vp-c-danger-1); }
.ho { color: var(--vp-c-brand-1); }
</style>
