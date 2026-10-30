<script setup lang="ts">
import { ref, computed } from 'vue'

// 站① · 协调成本计算器：任务 DAG 真执行，三拓扑成本对比（讲义 p.11-14 账本 + p.52-63 协调）
const DAG = [
  { id: 't1', name: '拆题', w: 1, deps: [] },
  { id: 't2', name: '检索 A', w: 2, deps: ['t1'] },
  { id: 't3', name: '检索 B', w: 2, deps: ['t1'] },
  { id: 't4', name: '检索 C', w: 3, deps: ['t1'] },
  { id: 't5', name: '分析', w: 2, deps: ['t2', 't3', 't4'] },
  { id: 't6', name: '写报告', w: 1, deps: ['t5'] },
]
const UNIT_TOKEN = 800 // 每单位工作量的 token

const msgTokens = ref(400)  // 每次协调消息的 token
const conflict = ref(0.15)  // 蜂群冲突率

const totalW = DAG.reduce((a, t) => a + t.w, 0)

interface Result { name: string; delay: number; tokens: number; rework: number; note: string }
const results = computed<Result[]>(() => {
  const mt = msgTokens.value, c = conflict.value
  // 单 agent 基线：全串行
  const sasDelay = totalW
  const sasTokens = totalW * UNIT_TOKEN + 6 * 50
  // 中心式：t2/t3/t4 并行；编排者派 4 活 + 收 4 果 + 集成
  const critPath = 1 + Math.max(2, 2, 3) + 2 + 1 // t1 + max(t234) + t5 + t6 = 7
  const orchMsgs = 9 * mt
  const orchDelay = critPath + 1 // 编排者集成一轮
  const orchTokens = totalW * UNIT_TOKEN + orchMsgs
  // 蜂群：并行自选，冲突 → 返工
  const swarmRework = Math.round(totalW * c * 0.6 * 10) / 10
  const swarmDelay = critPath * (1 + c * 0.4)
  const swarmTokens = totalW * UNIT_TOKEN * (1 + c * 0.6) + 14 * mt * (1 + c)
  // 独立：三线各干各的，最后人工集成
  const indepDelay = 3 + 2 // 各自完成 + 集成两轮
  const indepTokens = totalW * UNIT_TOKEN + 4 * mt + 2 * totalW * UNIT_TOKEN * 0.2 // 集成返工 20%
  return [
    { name: '单 agent 基线', delay: sasDelay, tokens: Math.round(sasTokens), rework: 0, note: '全部串行——没有协调成本，也没有并行收益' },
    { name: '中心式编排', delay: Math.round(orchDelay * 10) / 10, tokens: Math.round(orchTokens), rework: 0, note: '检索三线并行省 3 单位时延，代价是 9 次协调消息' },
    { name: '蜂群（自组织）', delay: Math.round(swarmDelay * 10) / 10, tokens: Math.round(swarmTokens), rework: swarmRework, note: `冲突率 ${(c * 100).toFixed(0)}% 带来返工 ${swarmRework} 单位 + 更密的通信` },
    { name: '独立各自干', delay: indepDelay, tokens: Math.round(indepTokens), rework: 0, note: '零协调也零协同——集成时的重复与缺口最贵' },
  ]
})
const maxDelay = computed(() => Math.max(...results.value.map((r) => r.delay)))
const maxTokens = computed(() => Math.max(...results.value.map((r) => r.tokens)))

const verdict = computed(() => {
  const sas = results.value[0], orch = results.value[1], swarm = results.value[2]
  const orchWin = orch.delay < sas.delay && orch.tokens < sas.tokens * 1.5
  const swarmWin = swarm.delay < sas.delay && swarm.tokens < sas.tokens * 1.5
  return { orchWin, swarmWin }
})
</script>

<template>
  <div class="mc">
    <div class="dials">
      <label class="dial">
        <span>协调消息 token 量：{{ msgTokens }}</span>
        <input type="range" min="100" max="1200" step="50" v-model.number="msgTokens" />
      </label>
      <label class="dial">
        <span>蜂群冲突率：{{ (conflict * 100).toFixed(0) }}%</span>
        <input type="range" min="0" max="0.5" step="0.05" v-model.number="conflict" />
      </label>
      <span class="dag">任务：拆题 → 检索 A/B/C（可并行）→ 分析 → 写报告（共 {{ totalW }} 单位工作，1 单位 ≈ {{ UNIT_TOKEN }} token）</span>
    </div>

    <div class="rows">
      <div v-for="r in results" :key="r.name" class="rrow">
        <div class="rname">{{ r.name }}</div>
        <div class="rbars">
          <div class="rline"><span class="rl">时延</span>
            <div class="track"><div class="fill d" :style="{ width: (r.delay / maxDelay * 100) + '%' }" /></div>
            <span class="rv">{{ r.delay }}</span>
          </div>
          <div class="rline"><span class="rl">token</span>
            <div class="track"><div class="fill t" :style="{ width: (r.tokens / maxTokens * 100) + '%' }" /></div>
            <span class="rv">{{ (r.tokens / 1000).toFixed(1) }}k</span>
          </div>
        </div>
        <div class="rnote">{{ r.note }}</div>
      </div>
    </div>

    <div class="verdict">
      <div class="v-q">讲义判据（p.14）——并行收益盖过协调成本了吗？</div>
      <div class="v-a" :class="verdict.orchWin ? 'ok' : 'bad'">中心式：{{ verdict.orchWin ? '✓ 划算——时延省 ' + (results[0].delay - results[1].delay) + ' 单位，token 溢价可接受' : '✗ 不划算——消息量把并行省的时间全吃掉了，回单 agent 基线' }}</div>
      <div class="v-a" :class="verdict.swarmWin ? 'ok' : 'bad'">蜂群：{{ verdict.swarmWin ? '✓ 划算——冲突可控，自组织在赚' : '✗ 不划算——冲突返工 + 密集通信双杀，这是"协调的诅咒"现场' }}</div>
    </div>

    <div class="hint"><span class="k">机制对位 · </span>把消息 token 拨到 1000+：中心式判据翻红——不是拓扑错了，是"每次交接太贵"；把冲突率拨到 40%：蜂群崩——CooperBench"单 agent 做两份活胜过两 agent 协作"（第四幕）的参数版。**先建强单 agent 基线，为被测量过的瓶颈而拆**（p.13-14）。</div>
  </div>
</template>

<style scoped>
.mc { display: flex; flex-direction: column; gap: 12px; }
.dials { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; }
.dial { display: flex; flex-direction: column; gap: 4px; font-size: 12px; color: var(--vp-c-text-2); }
.dial input[type='range'] { width: 140px; }
.dag { font-size: 12px; color: var(--vp-c-text-3); margin-left: auto; max-width: 300px; }
.rows { display: flex; flex-direction: column; gap: 8px; }
.rrow { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 8px 12px; display: grid; grid-template-columns: 110px 1fr; gap: 4px 12px; }
.rname { font-weight: 600; font-size: 13px; grid-row: span 2; align-self: center; }
.rbars { display: flex; flex-direction: column; gap: 4px; }
.rline { display: flex; align-items: center; gap: 8px; font-size: 11px; }
.rl { color: var(--vp-c-text-3); min-width: 30px; }
.track { flex: 1; height: 10px; background: var(--vp-c-default-soft); border-radius: 999px; overflow: hidden; }
.fill.d { background: var(--vp-c-brand-1); height: 100%; }
.fill.t { background: var(--vp-c-warning-1, #e3af37); height: 100%; }
.rv { min-width: 36px; text-align: right; font-weight: 600; }
.rnote { grid-column: 2; font-size: 11.5px; color: var(--vp-c-text-3); }
.verdict { border: 1px dashed var(--vp-c-divider); border-radius: 8px; padding: 10px 12px; display: flex; flex-direction: column; gap: 5px; }
.v-q { font-size: 12.5px; font-weight: 600; }
.v-a { font-size: 12.5px; }
.ok { color: var(--vp-c-brand-1); }
.bad { color: var(--vp-c-danger-1); }
</style>
