<script setup lang="ts">
import { ref, computed } from 'vue'

// τ-bench 的 pass^k（Yao et al., 2024）：全部 k 次试验都成功 vs 至少一次成功
const p = ref(0.8)
const k = ref(5)

const passAtK = computed(() => 1 - Math.pow(1 - p.value, k.value))
const passHatK = computed(() => Math.pow(p.value, k.value))
const fmt = (x: number) => (x * 100).toFixed(1).replace(/\.0$/, '') + '%'
</script>

<template>
  <div class="pk">
    <div class="ctl">
      <label>单次成功率 p
        <input v-model.number="p" type="range" min="0.5" max="0.99" step="0.01" />
        <b class="num">{{ (p * 100).toFixed(0) }}%</b>
      </label>
      <label>试验次数 k
        <input v-model.number="k" type="range" min="1" max="10" step="1" />
        <b class="num">{{ k }}</b>
      </label>
    </div>
    <div class="bars">
      <div class="line">
        <span class="lab">pass@k（至少一次成功）</span>
        <div class="track"><div class="fill at" :style="{ width: fmt(passAtK) }" /></div>
        <b class="val">{{ fmt(passAtK) }}</b>
      </div>
      <div class="line">
        <span class="lab">pass^k（全部 k 次都成功）</span>
        <div class="track"><div class="fill hat" :style="{ width: fmt(passHatK) }" /></div>
        <b class="val">{{ fmt(passHatK) }}</b>
      </div>
    </div>
    <div class="hint">
      <span class="k">现在看什么 · </span>
      单次 {{ (p * 100).toFixed(0) }}% 的 agent，跑 {{ k }} 次全过（pass^{{ k }}）只剩 <b>{{ fmt(passHatK) }}</b>——它就是 pⁿ 的评估化身：同一份数学，L01 用它算风险，τ-bench 用它给"可靠性"定价。而 pass@{{ k }}（{{ fmt(passAtK) }}）是研究里的乐观口径：抽 {{ k }} 次挑最好的一次。
    </div>
  </div>
</template>

<style scoped>
.pk { display: flex; flex-direction: column; gap: 12px; }
.ctl { display: flex; flex-wrap: wrap; gap: 14px 26px; }
.ctl label { display: flex; align-items: center; gap: 10px; font-size: 14.5px; flex: 1; min-width: 240px; }
.ctl input[type='range'] { flex: 1; }
.num { min-width: 52px; font-variant-numeric: tabular-nums; }
.bars { display: flex; flex-direction: column; gap: 10px; }
.line { display: grid; grid-template-columns: 190px 1fr 64px; gap: 12px; align-items: center; }
.lab { font-size: 13.5px; color: var(--vp-c-text-2); }
.track { height: 14px; background: var(--vp-c-default-soft); border-radius: 6px; overflow: hidden; }
.fill { height: 100%; border-radius: 6px; transition: width 0.25s ease; }
.fill.at { background: var(--vp-c-brand-1); }
.fill.hat { background: #dc2626; }
.val { font-size: 15px; font-variant-numeric: tabular-nums; }
</style>
