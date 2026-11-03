<script setup lang="ts">
import { ref, computed } from 'vue'

// Lab 10 站① · 数据采购台：固定预算在五来源间配比——账单弹"这笔钱教出什么"
// 价格/真实/事故与 DataSourceMap 同源（讲义案例量级）；问题先行：默认全押最便宜档
const SRC = [
  { id: 'human', name: '人类演示', cost: 15, realism: 0.95, accident: 0.05 },
  { id: 'mine', name: '网络挖掘', cost: 0.55, realism: 0.85, accident: 0.15 },
  { id: 'syntra', name: '合成轨迹', cost: 0.031, realism: 0.55, accident: 0.35 },
  { id: 'syntask', name: '合成任务', cost: 0.004, realism: 0.7, accident: 0.25 },
  { id: 'sim', name: '模拟环境', cost: 0.1, realism: 0.5, accident: 0.4 },
]
const BUDGET = 100
const alloc = ref<Record<string, number>>({ human: 0, mine: 0, syntra: 100, syntask: 0, sim: 0 })
const totalPct = computed(() => Object.values(alloc.value).reduce((a, b) => a + b, 0))
const bill = computed(() => {
  let spend = 0, items = 0, wReal = 0, wAcc = 0
  for (const s of SRC) {
    const money = (alloc.value[s.id] / 100) * BUDGET
    const n = Math.floor(money / s.cost)
    spend += money; items += n
    wReal += n * s.realism; wAcc += n * s.accident
  }
  return {
    spend: +spend.toFixed(1), items,
    realism: items ? +(wReal / items * 100).toFixed(0) : 0,
    accident: items ? +(wAcc / items * 100).toFixed(0) : 0,
    badItems: Math.round(items * (wAcc / (items || 1))),
  }
})
const verdict = computed(() => {
  if (!bill.value.items) return '预算还没分配。'
  if (bill.value.accident >= 30) return `这笔采购教出的模型：${bill.value.accident}% 的训练信号带着事故（约 ${bill.value.badItems.toLocaleString()} 条"有毒"样本）——便宜的数据不是不要钱，是延迟付费（上线后以 hacking/背题的形式回收成本）。`
  if (bill.value.realism >= 80) return `配比偏真实（${bill.value.realism}%）——质量高但只有 ${bill.value.items.toLocaleString()} 条，规模撑不起 weight 优化（数据饥渴，L09 第六幕）。`
  return `折中配比：${bill.value.items.toLocaleString()} 条、真实度 ${bill.value.realism}%、事故率 ${bill.value.accident}%——工程的主流解（真实锚定 + 合成放量 + 验证过滤）。`
})
function preset(kind: 'cheap' | 'quality' | 'mix') {
  if (kind === 'cheap') alloc.value = { human: 0, mine: 0, syntra: 60, syntask: 30, sim: 10 }
  if (kind === 'quality') alloc.value = { human: 95, mine: 5, syntra: 0, syntask: 0, sim: 0 }
  if (kind === 'mix') alloc.value = { human: 20, mine: 25, syntra: 15, syntask: 25, sim: 15 }
}
</script>

<template>
  <div class="dmk">
    <div class="ops">
      <span class="q">预算 $100，在五种来源间分配（默认已全押最便宜的合成轨迹）：</span>
      <button type="button" class="wbtn" @click="preset('cheap')">全押便宜</button>
      <button type="button" class="wbtn" @click="preset('quality')">全押质量</button>
      <button type="button" class="wbtn" @click="preset('mix')">工程折中</button>
    </div>
    <div class="alloc">
      <label v-for="s in SRC" :key="s.id" class="arow">
        <span class="an">{{ s.name }} <code class="ac">${{ s.cost }}/条</code></span>
        <input type="range" min="0" max="100" step="5" v-model.number="alloc[s.id]" />
        <span class="av">{{ alloc[s.id] }}%</span>
      </label>
      <div class="tp" :class="{ over: totalPct > 100 }">分配合计：{{ totalPct }}%{{ totalPct > 100 ? '（超预算！压缩各档）' : totalPct < 100 ? '（还有余量）' : '' }}</div>
    </div>
    <div class="billc">
      <div class="bh">采购账单——这笔钱教出什么</div>
      <div class="bgrid">
        <div class="bi"><b>{{ bill.items.toLocaleString() }}</b><span>条样本</span></div>
        <div class="bi"><b>{{ bill.realism }}%</b><span>加权真实度</span></div>
        <div class="bi bad"><b>{{ bill.accident }}%</b><span>事故率</span></div>
        <div class="bi bad"><b>≈{{ bill.badItems.toLocaleString() }}</b><span>条"有毒"样本</span></div>
      </div>
      <div class="vd" :class="{ bad: bill.accident >= 30 }">{{ verdict }}</div>
    </div>
    <div class="hint"><span class="k">机制对位 · </span>三个预设各跑一遍：全押便宜→事故账单刺眼；全押质量→规模撑不起训练；折中→两头都够但不免费——<b>数据采购的本质是买"真实×规模"的乘积，单看单价必然被咬</b>。</div>
  </div>
</template>

<style scoped>
.dmk { display: flex; flex-direction: column; gap: 10px; }
.ops { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.q { font-size: 13px; font-weight: 600; }
.alloc { border: 1px solid var(--vp-c-divider); border-radius: 10px; padding: 10px 14px; display: flex; flex-direction: column; gap: 6px; }
.arow { display: flex; align-items: center; gap: 10px; font-size: 12.5px; }
.an { min-width: 150px; }
.ac { font-size: 11px; color: var(--vp-c-text-3); }
.arow input[type='range'] { flex: 1; }
.av { min-width: 34px; text-align: right; font-weight: 650; }
.tp { font-size: 12px; color: var(--vp-c-text-2); }
.tp.over { color: var(--vp-c-danger-1); font-weight: 650; }
.billc { border: 1.5px solid var(--vp-c-brand-1); border-radius: 10px; padding: 10px 14px; }
.bh { font-size: 13px; font-weight: 650; margin-bottom: 8px; }
.bgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; }
.bi { display: flex; flex-direction: column; align-items: center; background: var(--vp-c-default-soft); border-radius: 8px; padding: 8px; }
.bi b { font-size: 20px; }
.bi span { font-size: 11px; color: var(--vp-c-text-3); }
.bi.bad b { color: var(--vp-c-danger-1); }
.vd { margin-top: 8px; font-size: 13px; line-height: 1.7; }
.vd.bad { color: var(--vp-c-danger-1); }
</style>
