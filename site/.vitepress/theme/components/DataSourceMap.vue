<script setup lang="ts">
import { ref } from 'vue'

// 五来源 × 成本/真实/规模矩阵（据讲义 lecture11 五来源与案例数据；价格为论文披露的量级）
const SOURCES = [
  { id: 'human', name: '① 人类演示', cases: 'Mind2Web / OpenCUA', cost: 15, realism: 0.95, scale: '低（万级）', accident: 0.05, note: '真但贵：录音录屏每一步，22.6K 任务已是大规模' },
  { id: 'mine', name: '② 网络挖掘', cases: 'SWE-rebench / AgentTrek', cost: 0.55, realism: 0.85, scale: '中（数万）', accident: 0.15, note: 'issue/教程/视频转轨迹 + 重放验证保留成功' },
  { id: 'syntra', name: '③ 合成轨迹', cases: 'Synatra / OS-Genesis', cost: 0.031, realism: 0.55, scale: '高（10 万+）', accident: 0.35, note: '模型离线写步骤（不执行）——人工成本 3%，但分布偏、有幻觉步骤' },
  { id: 'syntask', name: '④ 合成任务环境', cases: 'SWE-smith / R2E-Gym', cost: 0.004, realism: 0.7, scale: '极高（可无限）', accident: 0.25, note: '注入 bug 自动造任务：50K 任务仅 20 人工时；但任务分布由模板决定' },
  { id: 'sim', name: '⑤ 模拟用户/环境', cases: 'τ-bench / APIGen-MT / DreamGym', cost: 0.1, realism: 0.5, scale: '无限（RL 练习场）', accident: 0.4, note: '无限练习但"学会模拟器的错"——模拟误差直接进权重' },
]
const open = ref('human')
</script>

<template>
  <div class="dsm">
    <div class="rows">
      <div v-for="s in SOURCES" :key="s.id" class="srow" :class="{ on: open === s.id }" :tabindex="0" role="button"
        :aria-pressed="open === s.id" @click="open = s.id" @keydown.enter="open = s.id">
        <div class="sname">{{ s.name }}<span class="scase">{{ s.cases }}</span></div>
        <div class="bars">
          <div class="bl"><span class="bk">成本</span><code class="bv">${{ s.cost }}/条</code></div>
          <div class="bl"><span class="bk">真实</span><div class="track"><div class="fill r" :style="{ width: s.realism * 100 + '%' }" /></div><code class="bv">{{ (s.realism * 100).toFixed(0) }}%</code></div>
          <div class="bl"><span class="bk">事故率</span><div class="track"><div class="fill b" :style="{ width: s.accident * 100 + '%' }" /></div><code class="bv badv">{{ (s.accident * 100).toFixed(0) }}%</code></div>
          <div class="bl"><span class="bk">规模</span><code class="bv">{{ s.scale }}</code></div>
        </div>
        <div v-if="open === s.id" class="snote">{{ s.note }}</div>
      </div>
    </div>
    <div class="hint"><span class="k">矩阵一句话 · </span>没有免费午餐：成本每降一个量级，真实度或事故率就还一笔债——最优解永远是<b>配比</b>（人类演示锚定真实、合成拉开规模、验证器把守质量），而不是全押最便宜的那档（去 Lab 10 亲手配一次）。</div>
  </div>
</template>

<style scoped>
.dsm { display: flex; flex-direction: column; gap: 10px; }
.rows { display: flex; flex-direction: column; gap: 6px; }
.srow { border: 1px solid var(--vp-c-divider); border-radius: 10px; padding: 8px 12px; display: flex; flex-direction: column; gap: 6px; cursor: pointer; outline: none; }
.srow:focus-visible, .srow.on { border-color: var(--vp-c-brand-1); }
.srow.on { background: var(--vp-c-brand-soft); }
.sname { font-weight: 650; font-size: 13.5px; }
.scase { font-weight: 400; font-size: 11.5px; color: var(--vp-c-text-3); margin-left: 8px; }
.bars { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 6px; }
.bl { display: flex; align-items: center; gap: 6px; font-size: 11.5px; }
.bk { color: var(--vp-c-text-3); min-width: 34px; }
.track { flex: 1; height: 8px; background: var(--vp-c-default-soft); border-radius: 999px; overflow: hidden; }
.fill { height: 100%; }
.fill.r { background: var(--vp-c-brand-1); }
.fill.b { background: var(--vp-c-danger-1); }
.bv { font-family: var(--vp-font-family-mono, monospace); font-size: 11px; }
.badv { color: var(--vp-c-danger-1); }
.snote { font-size: 12px; color: var(--vp-c-text-2); border-top: 1px dashed var(--vp-c-divider); padding-top: 4px; }
</style>
