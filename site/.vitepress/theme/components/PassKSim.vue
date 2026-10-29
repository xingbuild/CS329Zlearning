<script setup lang="ts">
import { ref, computed } from 'vue'

/* pass^k 蒙特卡洛收敛模拟器：验证回路把单轮成功率 p 抬到 1-(1-p)^k */
const p = ref(0.5)
const k = ref(5)
const dist = ref<number[]>([])

function run() {
  const N = 1000
  const d = new Array(k.value + 1).fill(0) // 索引 0..k-1 = 第 i+1 轮通过，k = 全失败
  for (let n = 0; n < N; n++) {
    for (let r = 0; r < k.value; r++) {
      if (Math.random() < p.value) { d[r]++; break }
      if (r === k.value - 1) d[k.value]++
    }
  }
  dist.value = d
}
run()
const theory = computed(() => 1 - Math.pow(1 - p.value, k.value))
const simPass = computed(() => dist.value.length ? 1 - dist.value[dist.value.length - 1] / 1000 : 0)
const maxBar = computed(() => dist.value.length ? Math.max(...dist.value, 1) : 1)
const fmt = (x: number) => (x * 100).toFixed(1).replace(/\.0$/, '') + '%'
</script>

<template>
  <div class="pks">
    <div class="ctl">
      <label>单轮成功率 p（每次写码-修复一轮全绿的概率）
        <input v-model.number="p" type="range" min="0.3" max="0.9" step="0.05" @input="run" />
        <b class="num">{{ (p * 100).toFixed(0) }}%</b>
      </label>
      <label>回路最大轮数 k（验证器允许的尝试次数）
        <input v-model.number="k" type="range" min="1" max="10" step="1" @input="run" />
        <b class="num">{{ k }}</b>
      </label>
    </div>
    <div class="row wrap">
      <button type="button" class="wbtn primary" @click="run">▶ 跑 1000 个任务（蒙特卡洛）</button>
      <span class="pill">一次通过率：{{ fmt(p) }}</span>
      <span class="pill brand">经 {{ k }} 轮回路：理论 {{ fmt(theory) }} · 模拟 {{ fmt(simPass) }}</span>
    </div>
    <div class="bars">
      <div v-for="(d, i) in dist" :key="i" class="bcol">
        <div class="bval">{{ (d / 10).toFixed(0) }}%</div>
        <div class="btrack"><div class="bfill" :class="{ fail: i === k }" :style="{ height: (d / maxBar) * 100 + '%' }" /></div>
        <div class="blab">{{ i === k ? '失败' : `第${i + 1}轮` }}</div>
      </div>
    </div>
    <div class="hint"><span class="k">现在看什么 · </span>柱子回答"任务在第几轮通过"——p={{ (p * 100).toFixed(0) }}% 的模型一次只有 {{ fmt(p) }} 把握，但<b>验证回路 + 重试</b>把总成功率抬到 {{ fmt(theory) }}：这就是 Large Language Monkeys（SWE-bench 采样 250 次、覆盖率 15%→56%）的微观机制，也是左边闭环剧场的概率账单。<b>回路没有让模型变聪明，只是让"不合格的尝试"出不了门。</b></div>
  </div>
</template>

<style scoped>
.pks { display: flex; flex-direction: column; gap: 12px; }
.ctl { display: flex; flex-wrap: wrap; gap: 14px 26px; }
.ctl label { display: flex; align-items: center; gap: 10px; font-size: 14px; flex: 1; min-width: 300px; }
.ctl input[type='range'] { flex: 1; }
.num { min-width: 44px; font-variant-numeric: tabular-nums; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.bars { display: flex; gap: 8px; align-items: flex-end; min-height: 150px; padding: 6px 2px 0; }
.bcol { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.bval { font-size: 11.5px; color: var(--vp-c-text-2); font-variant-numeric: tabular-nums; }
.btrack { width: 100%; height: 110px; background: var(--vp-c-default-soft); border-radius: 6px; display: flex; align-items: flex-end; overflow: hidden; }
.bfill { width: 100%; background: var(--vp-c-brand-1); border-radius: 6px 6px 0 0; transition: height .3s ease; }
.bfill.fail { background: #dc2626; }
.blab { font-size: 11px; color: var(--vp-c-text-3); }
</style>
