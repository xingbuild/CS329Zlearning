<script setup lang="ts">
import { ref, computed } from 'vue'

// 多智能体失败分类，整理自讲义 lecture08.pdf p.70-82（Cemri et al. 2025 + 行为问题）
const FAMILIES = [
  {
    id: 'general',
    name: '一般性失败',
    color: '#d97706',
    items: [
      {
        name: '系统设计错',
        symptom: '架构、角色、流程从一开始就设计错了。',
        cause: '规格说明含糊、工具/接口设计不当——工程问题而非协作问题。',
        fix: '先修单 agent 基线再上多 agent（讲义的反复建议）；规格写成可验证的契约。',
      },
      {
        name: 'Agent 间失配',
        symptom: '各 agent 对目标/状态的理解不一致，越干越散。',
        cause: '信息在交接中丢失或变形——每个 agent 只见自己的上下文。',
        fix: '共享状态显式化（Task Ledger / 共享文档）；交接时携带结构化上下文。',
      },
      {
        name: '验证缺位',
        symptom: '产出没人检查，错误结果被下游 agent 当真。',
        cause: '没有验证环节或验证器太弱——pⁿ 在多 agent 间的放大版。',
        fix: '强测试作为协调的锚（Carlini 的第一课）；每步产物可验证再流转。',
      },
    ],
  },
  {
    id: 'coord',
    name: '协调失败',
    color: '#2563eb',
    items: [
      {
        name: '期望错位',
        symptom: 'A 以为 B 会做，B 以为 A 会做——任务没人接。',
        cause: '分工从未显式确认；"默认对方负责"是人类团队的老病。',
        fix: '任务认领显式化（claim 机制）；Task Ledger 记录归属。',
      },
      {
        name: '承诺失信',
        symptom: '答应的事没做/做了一半，下游阻塞。',
        cause: '承诺没有被跟踪；agent 上下文漂移后忘掉承诺。',
        fix: '依赖关系进账本；阻塞可见、可升级（Symphony 的 issue tracker 思路）。',
      },
      {
        name: '通信失败',
        symptom: '消息丢失、过时、或被淹没。',
        cause: '通道过载或协议不清——蜂群里消息爆炸的必然病。',
        fix: '结构化消息协议（A2A）；消息板分区与摘要；关键信息写共享工件而非闲聊。',
      },
    ],
  },
  {
    id: 'behavioral',
    name: '行为问题',
    color: '#dc2626',
    items: [
      {
        name: '从众（多样性塌缩）',
        symptom: '一群 agent "独立"创作，过半都做了光线追踪器或自托管编译器。',
        cause: '同源模型 + 相似提示 → 相关的探索方向；群体失去了多样性这一 MAS 的核心收益。',
        fix: '显式差异化目标/角色/温度；用不信任的多样性（不同模型、不同约束）。',
      },
      {
        name: '不兼容目标 → 武力解决',
        symptom: '一个要求部署 Python、另一个要求 Rust——最终"以武力解决"（改掉对方的成果）。',
        cause: '目标冲突没有谈判与升级机制；agent 只能通过环境动作互相影响。',
        fix: '目标兼容性前置检查；谈判/升级协议（CooperBench 的 Negotiation 模式）；冲突裁决权显式归属。',
      },
      {
        name: '协调的诅咒',
        symptom: '两个 agent 协作，还不如一个 agent 干两份活。',
        cause: 'CooperBench 的实证结论：紧耦合任务上，通信/合并/冲突成本吞噬并行收益。',
        fix: '先测量再拆分——只有"可分离的失败面/子任务"才值得多 agent（讲义 p.14 判据）。',
      },
    ],
  },
]

const fam = ref('coord')
const sel = ref(0)
const curFam = computed(() => FAMILIES.find((f) => f.id === fam.value)!)
const cur = computed(() => curFam.value.items[sel.value])

function switchFam(id: string) {
  fam.value = id
  sel.value = 0
}
</script>

<template>
  <div class="mzoo">
    <div class="row wrap">
      <button v-for="f in FAMILIES" :key="f.id" type="button" class="wbtn" :aria-pressed="f.id === fam"
        @click="switchFam(f.id)">{{ f.name }}（{{ f.items.length }}）</button>
    </div>
    <div class="zoo-body">
      <div class="zoo-list">
        <button v-for="(it, i) in curFam.items" :key="it.name" type="button" class="zoo-item" :aria-pressed="i === sel"
          :style="i === sel ? { borderColor: curFam.color } : {}" @click="sel = i">{{ it.name }}</button>
      </div>
      <div class="zoo-detail">
        <div class="zoo-title" :style="{ color: curFam.color }">{{ curFam.name }} · {{ cur.name }}</div>
        <div class="zoo-row"><span class="zk">症状</span><span>{{ cur.symptom }}</span></div>
        <div class="zoo-row"><span class="zk">根因</span><span>{{ cur.cause }}</span></div>
        <div class="zoo-row"><span class="zk">对策</span><span>{{ cur.fix }}</span></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mzoo { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.zoo-body { display: flex; gap: 14px; align-items: stretch; flex-wrap: wrap; }
.zoo-list { display: flex; flex-direction: column; gap: 6px; flex: none; }
.zoo-item { text-align: left; padding: 8px 14px; border-radius: 8px; border: 1px solid var(--vp-c-divider); background: var(--vp-c-bg); color: var(--vp-c-text-1); font-size: 14.5px; cursor: pointer; min-width: 150px; }
.zoo-item[aria-pressed='true'] { background: var(--vp-c-brand-soft); font-weight: 600; }
.zoo-detail { flex: 1; min-width: 260px; border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 8px; }
.zoo-title { font-weight: 700; font-size: 15.5px; }
.zoo-row { display: flex; gap: 10px; font-size: 14.5px; line-height: 1.65; }
.zk { flex: none; color: var(--vp-c-text-3); font-size: 13px; padding-top: 2px; }
</style>
