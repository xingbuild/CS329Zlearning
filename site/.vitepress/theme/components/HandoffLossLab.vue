<script setup lang="ts">
import { ref, computed } from 'vue'

// 站② · 交接信息丢失实验：Handoff 全量 vs Agent-as-Tool 挑 k 条（超几何蒙特卡洛真算）
const FACTS = [
  { id: 1, text: '用户护照号 EA1234567', key: true, rel: 0.98 },
  { id: 2, text: '出行日期 11 月 8 日，返程 15 日', key: true, rel: 0.95 },
  { id: 3, text: '偏好靠窗、经济舱', key: true, rel: 0.9 },
  { id: 4, text: '用户早上聊过天气很冷', key: false, rel: 0.1 },
  { id: 5, text: '用户的猫叫 Pi', key: false, rel: 0.05 },
  { id: 6, text: '上周订过一次火车票', key: false, rel: 0.45 },
  { id: 7, text: '用户喜欢靠前的酒店楼层', key: false, rel: 0.3 },
  { id: 8, text: '常旅客号 CA8899', key: false, rel: 0.6 },
  { id: 9, text: '用户在学吉他', key: false, rel: 0.05 },
  { id: 10, text: '对花生过敏（航司备注）', key: false, rel: 0.4 },
]
const PER_FACT_TOKEN = 120
const RUNS = 60

const k = ref(5)
const strategy = ref<'random' | 'rel'>('rel')
const trials = ref<{ run: number; hit: boolean; picked: number[] }[]>([])

const keyIds = FACTS.filter((f) => f.key).map((f) => f.id)

function pickRandom(): number[] {
  const pool = [...FACTS]
  const out: number[] = []
  for (let i = 0; i < k.value && pool.length; i++) {
    out.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0].id)
  }
  return out
}
function pickRel(): number[] {
  return [...FACTS].sort((a, b) => b.rel - a.rel).slice(0, k.value).map((f) => f.id)
}
function run() {
  trials.value = []
  for (let i = 0; i < RUNS; i++) {
    const picked = strategy.value === 'rel' ? pickRel() : pickRandom()
    trials.value.push({ run: i, hit: keyIds.every((id) => picked.includes(id)), picked })
  }
}
const hitRate = computed(() => trials.value.length ? trials.value.filter((t) => t.hit).length / trials.value.length : null)
const tokenCost = computed(() => k.value * PER_FACT_TOKEN)

// 理论曲线（超几何）：随机策略含全部 3 条关键的概率
function hyperRandom(kk: number) {
  // P(3 关键都在 kk 里) = C(7, kk-3)/C(10, kk)
  const C = (n: number, m: number) => { if (m < 0 || m > n) return 0; let r = 1; for (let i = 0; i < m; i++) r = r * (n - i) / (i + 1); return r }
  return C(7, kk - 3) / C(10, kk)
}
const theory = computed(() => Array.from({ length: 10 }, (_, i) => ({ k: i + 1, p: hyperRandom(i + 1) })))
</script>

<template>
  <div class="hl">
    <div class="dials">
      <label class="dial">
        <span>挑 k 条上下文：{{ k }}</span>
        <input type="range" min="1" max="10" step="1" v-model.number="k" />
      </label>
      <div class="str">
        <span class="strl">挑选策略</span>
        <button type="button" class="wbtn" :aria-pressed="strategy === 'rel'" @click="strategy = 'rel'">按相关性挑</button>
        <button type="button" class="wbtn" :aria-pressed="strategy === 'random'" @click="strategy = 'random'">随机挑</button>
      </div>
      <button type="button" class="wbtn" @click="run">▶ 跑 60 次交接</button>
      <span class="cost">token 成本：{{ tokenCost }}/次（全量 Handoff = {{ 10 * PER_FACT_TOKEN }}）</span>
    </div>

    <div class="facts">
      <div v-for="f in FACTS" :key="f.id" class="fcard" :class="{ key: f.key }">
        <span class="ft">{{ f.text }}</span>
        <span class="fr">相关 {{ f.rel.toFixed(2) }}{{ f.key ? ' · 关键' : '' }}</span>
      </div>
    </div>

    <div v-if="hitRate !== null" class="res">
      <div class="bigrate" :class="hitRate > 0.9 ? 'ok' : hitRate > 0.5 ? 'mid' : 'bad'">
        下游 agent 答对率：{{ (hitRate * 100).toFixed(0) }}%（{{ trials.filter(t => t.hit).length }}/60 次拿到全部三条关键事实）
      </div>
      <div class="sub">省了 {{ (100 - k * 10) }}% 的上下文 token，换来 {{ (hitRate * 100).toFixed(0) }}% 的成功率——这笔账划算吗？</div>
    </div>

    <div class="curve">
      <div class="ct">理论曲线 · 随机挑的答对率随 k 变化（超几何分布）</div>
      <div class="bars">
        <div v-for="t in theory" :key="t.k" class="cbar-wrap">
          <div class="cbar" :style="{ height: Math.max(2, t.p * 56) + 'px' }" :class="{ cur: t.k === k }" />
          <span class="ck" :class="{ cur: t.k === k }">{{ t.k }}</span>
        </div>
      </div>
      <div class="cs">k（挑几条）→ 概率。随机挑要到 k=8 才接近全对；按相关性挑 k=3 即全对——**省 token 的前提是会挑**。</div>
    </div>

    <div class="hint"><span class="k">机制对位 · </span>Handoff 全量跟随（贵但稳）vs Agent-as-Tool 挑着发（省但会漏）——交接处是信息丢失的高发地（第二幕 p.39）。挑上下文本身是个工程动作：相关性排序就是那条分界线。而如果下游需要的 关键事实数 不止 3 条、且你不知道哪几条关键——老老实实全量交接，或者别拆 agent。</div>
  </div>
</template>

<style scoped>
.hl { display: flex; flex-direction: column; gap: 12px; }
.dials { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; }
.dial { display: flex; flex-direction: column; gap: 4px; font-size: 12px; color: var(--vp-c-text-2); }
.dial input[type='range'] { width: 120px; }
.str { display: flex; align-items: center; gap: 4px; font-size: 12px; color: var(--vp-c-text-2); }
.strl { color: var(--vp-c-text-2); margin-right: 2px; }
.cost { font-size: 12px; color: var(--vp-c-text-3); margin-left: auto; }
.facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 6px; }
.fcard { border: 1px solid var(--vp-c-divider); border-radius: 6px; padding: 6px 8px; display: flex; flex-direction: column; gap: 2px; font-size: 12px; background: var(--vp-c-default-soft); }
.fcard.key { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.fr { font-size: 10.5px; color: var(--vp-c-text-3); }
.fcard.key .fr { color: var(--vp-c-brand-1); }
.res { border: 1px dashed var(--vp-c-divider); border-radius: 8px; padding: 10px 12px; }
.bigrate { font-size: 15px; font-weight: 700; }
.bigrate.ok { color: var(--vp-c-brand-1); }
.bigrate.mid { color: var(--vp-c-warning-1, #b8860b); }
.bigrate.bad { color: var(--vp-c-danger-1); }
.sub { font-size: 12px; color: var(--vp-c-text-2); margin-top: 4px; }
.curve { border-top: 1px dashed var(--vp-c-divider); padding-top: 8px; }
.ct { font-size: 12px; font-weight: 600; color: var(--vp-c-text-2); margin-bottom: 6px; }
.bars { display: flex; align-items: flex-end; gap: 8px; height: 64px; }
.cbar-wrap { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.cbar { width: 22px; border-radius: 3px 3px 0 0; background: var(--vp-c-text-3); opacity: 0.5; }
.cbar.cur { background: var(--vp-c-brand-1); opacity: 1; }
.ck { font-size: 10px; color: var(--vp-c-text-3); }
.ck.cur { color: var(--vp-c-brand-1); font-weight: 700; }
.cs { font-size: 11.5px; color: var(--vp-c-text-3); margin-top: 4px; }
</style>
