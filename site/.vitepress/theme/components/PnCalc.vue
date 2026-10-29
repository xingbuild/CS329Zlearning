<script setup lang="ts">
import { ref, computed } from 'vue'

const p = ref(95)
const n = ref(20)

const r = computed(() => Math.pow(p.value / 100, n.value))
const pct = computed(() => (r.value * 100).toFixed(1).replace(/\.0$/, ''))
const barColor = computed(() => (r.value < 0.5 ? '#dc2626' : r.value < 0.8 ? '#d97706' : '#16a34a'))
const caption = computed(() =>
  r.value < 0.5
    ? ' —— 低于抛硬币。这就是「能力 99%」的系统在长任务上翻车的原因。'
    : ''
)
</script>

<template>
  <div class="pn">
    <div class="ctl">
      <label>每步可靠率 p
        <input v-model.number="p" type="range" min="80" max="100" step="0.5" />
        <b class="num">{{ p }}%</b>
      </label>
      <label>步数 n
        <input v-model.number="n" type="range" min="1" max="50" step="1" />
        <b class="num">{{ n }}</b>
      </label>
    </div>
    <div class="out">
      <div class="track"><div class="fill" :style="{ width: pct + '%', background: barColor }" /></div>
      <b class="big">{{ pct }}%</b>
    </div>
    <div class="hint">每步 {{ p }}% 的可靠率，走 {{ n }} 步之后端到端只剩 <b>{{ pct }}%</b>。{{ caption }}</div>
  </div>
</template>

<style scoped>
.pn { display: flex; flex-direction: column; gap: 12px; }
.ctl { display: flex; flex-wrap: wrap; gap: 14px 26px; }
.ctl label { display: flex; align-items: center; gap: 10px; font-size: 14.5px; flex: 1; min-width: 240px; }
.ctl input[type='range'] { flex: 1; }
.num { min-width: 52px; font-variant-numeric: tabular-nums; }
.out { display: flex; align-items: center; gap: 14px; }
.track { flex: 1; height: 9px; background: var(--vp-c-default-soft); border-radius: 999px; overflow: hidden; }
.fill { height: 100%; border-radius: 999px; transition: width 0.25s ease; }
.big { font-size: 20px; font-variant-numeric: tabular-nums; }
</style>
