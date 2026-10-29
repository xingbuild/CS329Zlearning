<script setup lang="ts">
import { ref, computed } from 'vue'

// 分布数据取自讲义 lecture02.pdf p.16 / p.18 的真实模型输出
const CTXS = [
  {
    id: 'a',
    label: '上下文 A：“The class was about ___”',
    tokens: [
      ['to', 0.3171], ['as', 0.0491], ['the', 0.036], ['a', 0.033],
      ['two', 0.0147], ['how', 0.0124], ['getting', 0.0101], ['three', 0.01],
      ['time', 0.0091], ['“', 0.0081],
    ] as [string, number][],
  },
  {
    id: 'b',
    label: '上下文 B：“The class was about to ___”',
    tokens: [
      ['be', 0.1501], ['begin', 0.0855], ['go', 0.0627], ['start', 0.0496],
      ['get', 0.039], ['graduate', 0.0342], ['end', 0.0313], ['take', 0.022],
      ['enter', 0.0192], ['become', 0.018],
    ] as [string, number][],
  },
]

type Strat = 'greedy' | 'topk' | 'topp'
const ctxId = ref<'a' | 'b'>('a')
const temp = ref(1)
const strat = ref<Strat>('greedy')
const tally = ref<Record<string, number>>({})
const drawn = ref<string | null>(null)

const ctx = computed(() => CTXS.find((c) => c.id === ctxId.value)!)

const transformed = computed<{ tok: string; p: number }[]>(() => {
  const base = ctx.value.tokens
  // 1) 温度：logit = ln p，除以 T 后 renormalize
  let idx = base.map(([tok, p]) => ({ tok, logit: Math.log(Math.max(p, 1e-12)) }))
  if (strat.value !== 'greedy' || true) {
    idx = idx.map((x) => ({ ...x, logit: x.logit / temp.value }))
  }
  let arr = idx.map((x) => {
    const e = Math.exp(x.logit)
    return { tok: x.tok, p: e }
  })
  // 2) 策略截断
  if (strat.value === 'topk') {
    arr = [...arr].sort((a, b) => b.p - a.p).slice(0, 5)
  } else if (strat.value === 'topp') {
    const sorted = [...arr].sort((a, b) => b.p - a.p)
    let cum = 0
    const keep: typeof arr = []
    for (const it of sorted) {
      keep.push(it)
      cum += it.p
      if (cum >= 0.9) break
    }
    arr = keep
  }
  const Z = arr.reduce((s, x) => s + x.p, 0)
  return arr.map((x) => ({ tok: x.tok, p: x.p / Z }))
})

const greedyTok = computed(() => {
  let best = transformed.value[0]
  for (const x of transformed.value) if (x.p > best.p) best = x
  return best.tok
})

function sample1() {
  const r = Math.random()
  let cum = 0
  for (const x of transformed.value) {
    cum += x.p
    if (r <= cum) {
      drawn.value = x.tok
      tally.value[x.tok] = (tally.value[x.tok] || 0) + 1
      return
    }
  }
}
function sample100() {
  for (let i = 0; i < 100; i++) sample1()
}
function reset() {
  tally.value = {}
  drawn.value = null
}
function switchCtx(id: 'a' | 'b') {
  ctxId.value = id
  reset()
}

const totalDraws = computed(() => Object.values(tally.value).reduce((s, n) => s + n, 0))
</script>

<template>
  <div class="slab">
    <div class="row wrap">
      <button v-for="c in CTXS" :key="c.id" type="button" class="wbtn" :aria-pressed="c.id === ctxId"
        @click="switchCtx(c.id)">{{ c.label }}</button>
    </div>
    <div class="row wrap">
      <button v-for="s in (['greedy', 'topk', 'topp'] as Strat[])" :key="s" type="button" class="wbtn" :aria-pressed="s === strat"
        @click="strat = s; reset()">{{ { greedy: '贪心 argmax', topk: 'Top-k (k=5)', topp: 'Top-p (p=0.9)' }[s] }}</button>
      <label class="temp">温度 T = {{ temp.toFixed(1) }}
        <input v-model.number="temp" type="range" min="0.1" max="2" step="0.1" @input="reset" />
      </label>
    </div>
    <div class="row wrap">
      <button type="button" class="wbtn primary" @click="sample1">采样 1 次</button>
      <button type="button" class="wbtn" @click="sample100">采样 ×100</button>
      <button type="button" class="wbtn" @click="reset">清空记录</button>
      <span v-if="drawn" class="pill brand">刚采到：{{ drawn }}</span>
      <span v-if="totalDraws" class="pill">累计 {{ totalDraws }} 次</span>
    </div>

    <div class="bars">
      <div v-for="x in transformed" :key="x.tok" class="bar-row">
        <span class="btok">{{ x.tok }}</span>
        <div class="btrack">
          <div class="bfill" :style="{ width: Math.max(x.p * 100, 0.6) + '%' }" />
        </div>
        <span class="bp">{{ (x.p * 100).toFixed(1) }}%</span>
        <span class="bfreq">{{ tally[x.tok] ? (tally[x.tok] / Math.max(totalDraws, 1) * 100).toFixed(0) + '%' : '—' }}</span>
      </div>
    </div>

    <div class="hint">
      <span class="k">现在看什么 · </span>
      <template v-if="strat === 'greedy' && temp <= 0.2">温度趋近 0：分布坍缩成尖峰，贪心 = 永远取 argmax（{{ greedyTok }}）——"确定性"的来源。</template>
      <template v-else-if="temp >= 1.6">高温：长尾被抬高，低概率 token 也有出场机会——多样性与不可复现同时到来。</template>
      <template v-else-if="strat === 'topk' || strat === 'topp'">截断策略把分布以外的长尾直接清零、剩余 renormalize——与掩码解码（lab01）是同一族数学：先砍概率质量，再重新归一。</template>
      <template v-else>采样频率列会随次数增多逼近概率列——大数定律就是你付出"概率换多样性"的价格表。</template>
    </div>
  </div>
</template>

<style scoped>
.slab { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.temp { display: flex; align-items: center; gap: 10px; font-size: 14.5px; min-width: 240px; flex: 1; }
.temp input[type='range'] { flex: 1; }
.bars { display: flex; flex-direction: column; gap: 5px; margin-top: 6px; }
.bar-row { display: grid; grid-template-columns: 84px 1fr 58px 52px; gap: 10px; align-items: center; }
.btok { font-size: 14px; text-align: right; font-family: var(--vp-font-family-mono, monospace); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.btrack { height: 16px; background: var(--vp-c-default-soft); border-radius: 5px; overflow: hidden; }
.bfill { height: 100%; background: var(--vp-c-brand-1); border-radius: 5px; transition: width 0.25s ease; }
.bp { font-size: 13px; font-variant-numeric: tabular-nums; color: var(--vp-c-text-2); }
.bfreq { font-size: 13px; font-variant-numeric: tabular-nums; color: var(--vp-c-brand-1); font-weight: 600; }
</style>
