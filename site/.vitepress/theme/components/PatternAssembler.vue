<script setup lang="ts">
import { ref, computed } from 'vue'

// 模式积木与三场景槽位，判定依据讲义 lecture06 p.14-29（五模式）与思考题 1 参考答案
const BRICKS = [
  { id: 'chain', name: '提示链', icon: '⛓', desc: '固定步骤串联：A 的输出喂 B' },
  { id: 'route', name: '路由', icon: '⑂', desc: '先分类，再按类走不同分支' },
  { id: 'par', name: '并行化', icon: '⇶', desc: '同一任务多路同时跑，再聚合' },
  { id: 'orch', name: '编排者-工人', icon: 'Ⴍ', desc: '拆解派活，工人干完汇总' },
  { id: 'eval', name: '评估者-优化者', icon: '↻', desc: '一个生成一个验收，循环到过' },
  { id: 'react', name: 'ReAct 循环', icon: '⟳', desc: '模型边想边做，观察定去向' },
  { id: 'code', name: '确定性代码', icon: '{}', desc: '纯程序逻辑，不交给模型' },
]

interface Slot { name: string; hint: string; best: string; ok?: string[]; why: string }
interface Scene { id: string; name: string; brief: string; slots: Slot[] }

const SCENES: Scene[] = [
  {
    id: 'ticket',
    name: '客服工单系统',
    brief: '每天上千张工单：退款咨询、技术故障、闲聊混杂，高价值操作前必须合规检查。（思考题 1 的现实版）',
    slots: [
      { name: '① 工单入口分流', hint: '三类工单、三种处理路径', best: 'route', why: '先分类再分叉是路由的定义场景——类别可枚举、路径各异（p.16）。' },
      { name: '② 简单类目处理', hint: '退款政策问答：查政策 → 草拟 → 润色', best: 'chain', why: '步骤固定串联，提示链正身（p.15）。' },
      { name: '③ 复杂工单调查', hint: '要查订单、查物流、查历史工单再汇总', best: 'orch', why: '多个独立子调查并行再汇总——编排者-工人（p.19）。' },
      { name: '④ 高价值操作把关', hint: '退款执行前的合规检查循环', best: 'eval', why: '验收有明确判据（合规清单），评估者-优化者循环到过（p.20）。' },
      { name: '⑤ 退款执行', hint: '调用支付接口真正退钱', best: 'code', why: '纯确定性操作交给模型是引狼入室——讲义军规：退款执行本身是纯代码 workflow（思考题 1 底线）。', ok: [] },
    ],
  },
  {
    id: 'report',
    name: '技术调研报告生成器',
    brief: '给定一个技术选题，产出一份引用多信源、事实经过核查的调研报告。（STORM 的简化版）',
    slots: [
      { name: '① 选题拆解成问题清单', hint: '一个选题拆成 N 个子问题', best: 'orch', ok: ['chain'], why: '编排者拆题派活；简单场景一问一答的提示链也可接受。' },
      { name: '② 多信源检索', hint: 'N 个子问题各自去查，互不依赖', best: 'par', why: '子问题独立、可同时检索——并行化 + 聚合（STORM 的多视角提问）。' },
      { name: '③ 撰写初稿', hint: '把检索结果组织成文', best: 'chain', ok: ['orch'], why: '大纲 → 撰写的固定串联（STORM 的提示链）。' },
      { name: '④ 事实核查', hint: '逐条断言对照信源，不合格重写', best: 'eval', why: '核查有可判定判据（有无信源支持）——评估者-优化者（STORM 的近似实现）。' },
    ],
  },
  {
    id: 'review',
    name: '代码评审机器人',
    brief: '读 PR diff，按团队规约给出分级评审意见：小问题自动改，架构问题写报告。',
    slots: [
      { name: '① diff 定级', hint: '标注级 / 建议级 / 架构级', best: 'route', why: '分级可枚举、各级处理不同——路由。' },
      { name: '② 规约比对', hint: '命名/格式/惯用法逐条对照', best: 'chain', why: '取规约 → 比对 → 出意见，固定串联。' },
      { name: '③ 跨文件影响分析', hint: '改动会波及哪些模块，要边查边定', best: 'react', ok: ['orch'], why: '查什么、够不够，取决于每轮检索结果——观察决定行动，ReAct 的领地（L01 那把刀）。' },
      { name: '④ 意见整合出报告', hint: '汇总所有发现，复查后提交', best: 'eval', ok: ['chain'], why: '复查循环有判据（发现是否真实、建议是否可执行）。' },
    ],
  },
]

const sceneIdx = ref(0)
const scene = computed(() => SCENES[sceneIdx.value])
const picks = ref<Record<string, (string | undefined)[]>>({ [SCENES[0].id]: [] })
const cur = ref(0)
const verdicts = ref<Record<string, ('good' | 'ok' | 'bad' | undefined)[]>>({})
const running = ref(false)
const curRun = ref(-1)

function pick(sceneId: string, slotIdx: number, brick: string) {
  const arr = picks.value[sceneId] || []
  arr[slotIdx] = brick
  picks.value[sceneId] = [...arr]
  if (slotIdx === cur.value && cur.value < scene.value.slots.length - 1) cur.value++
}
function filled(sceneId: string) {
  const arr = picks.value[sceneId] || []
  return arr.filter(Boolean).length
}
function switchScene(i: number) {
  sceneIdx.value = i
  cur.value = 0
}
async function run() {
  running.value = true
  verdicts.value[scene.value.id] = []
  for (let i = 0; i < scene.value.slots.length; i++) {
    curRun.value = i
    await new Promise((r) => setTimeout(r, 420))
    const s = scene.value.slots[i]
    const p = (picks.value[scene.value.id] || [])[i]
    const v = p === s.best ? 'good' : (s.ok && s.ok.includes(p || '')) ? 'ok' : 'bad'
    const arr = verdicts.value[scene.value.id] || []
    arr[i] = v
    verdicts.value[scene.value.id] = [...arr]
  }
  curRun.value = -1
  running.value = false
}
const scoreOf = computed(() => {
  const v = verdicts.value[scene.value.id] || []
  const g = v.filter((x) => x === 'good').length
  const o = v.filter((x) => x === 'ok').length
  return { g, o, total: scene.value.slots.length }
})
</script>

<template>
  <div class="asm">
    <div class="rail">
      <button v-for="(s, i) in SCENES" :key="s.id" type="button" class="wbtn" :aria-pressed="i === sceneIdx"
        @click="switchScene(i)">{{ s.name }}</button>
      <span class="pr">{{ filled(scene.id) }}/{{ scene.slots.length }} 槽已填</span>
    </div>
    <p class="brief">{{ scene.brief }}</p>

    <div class="line">
      <div v-for="(s, i) in scene.slots" :key="s.name" class="slot" :class="{
        cur: i === cur && !running,
        run: i === curRun,
      }" @click="!running && (cur = i)">
        <div class="s-top">
          <span class="s-name">{{ s.name }}</span>
          <span v-if="verdicts[scene.id]?.[i]" class="s-v" :class="verdicts[scene.id][i]">
            {{ verdicts[scene.id][i] === 'good' ? '✓ 正解' : verdicts[scene.id][i] === 'ok' ? '△ 可行' : '✗ 不推荐' }}
          </span>
        </div>
        <div class="s-hint">{{ s.hint }}</div>
        <div class="s-pick">{{ (picks[scene.id] || [])[i] ? BRICKS.find((b) => b.id === (picks[scene.id] || [])[i])!.icon + ' ' + BRICKS.find((b) => b.id === (picks[scene.id] || [])[i])!.name : '（待选积木）' }}</div>
        <div v-if="verdicts[scene.id]?.[i]" class="s-why">{{ s.why }}</div>
      </div>
    </div>

    <div class="box">
      <div class="bt">积木盒 · 点一下填进当前槽（{{ scene.slots[cur]?.name || '—' }}）</div>
      <div class="bricks">
        <button v-for="b in BRICKS" :key="b.id" type="button" class="wbtn brick" :disabled="running"
          :aria-pressed="(picks[scene.id] || [])[cur] === b.id" @click="pick(scene.id, cur, b.id)">
          <span class="bi">{{ b.icon }}</span><span class="bn">{{ b.name }}</span>
        </button>
      </div>
      <div class="bdesc">{{ BRICKS.find((b) => b.id === (picks[scene.id] || [])[cur])?.desc || '七块积木：五工作流模式 + ReAct + 确定性代码（第六块是本实验室特意加的——有些槽最好的积木是「不用模型」）' }}</div>
      <button type="button" class="wbtn runbtn" :disabled="running || filled(scene.id) < scene.slots.length"
        @click="run">{{ filled(scene.id) < scene.slots.length ? `还差 ${scene.slots.length - filled(scene.id)} 个槽` : '▶ 运行评审' }}</button>
      <span v-if="verdicts[scene.id]?.length" class="fs">成绩：{{ scoreOf.g }} 正解 / {{ scoreOf.o }} 可行 / {{ scoreOf.total }} 槽</span>
    </div>

    <div class="hint"><span class="k">判据一句话 · </span>槽位问"这一步的分支能不能预先写尽"（能 → 工作流模式；不能 → ReAct）；涉及钱和权限的执行步，最好的积木是「确定性代码」——模式是半成品，烤熟它的是你的场景（Fowler）。</div>
  </div>
</template>

<style scoped>
.asm { display: flex; flex-direction: column; gap: 10px; }
.rail { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.pr { margin-left: auto; font-size: 12px; color: var(--vp-c-text-2); }
.brief { margin: 0; font-size: 13px; color: var(--vp-c-text-2); }
.line { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; }
.slot { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 4px; cursor: pointer; font-size: 12px; transition: all 0.2s; }
.slot.cur { border-color: var(--vp-c-brand-1); box-shadow: 0 0 0 1px var(--vp-c-brand-1); }
.slot.run { border-color: var(--vp-c-warning-1, #e3af37); background: var(--vp-c-default-soft); }
.s-top { display: flex; justify-content: space-between; gap: 6px; align-items: center; }
.s-name { font-weight: 600; font-size: 13px; }
.s-v { font-size: 11px; white-space: nowrap; }
.s-v.good { color: var(--vp-c-brand-1); }
.s-v.ok { color: var(--vp-c-warning-1, #b8860b); }
.s-v.bad { color: var(--vp-c-danger-1); }
.s-hint { color: var(--vp-c-text-3); }
.s-pick { font-weight: 600; color: var(--vp-c-brand-1); min-height: 18px; }
.s-why { border-top: 1px dashed var(--vp-c-divider); padding-top: 4px; color: var(--vp-c-text-2); }
.box { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 8px; position: sticky; bottom: 0; background: var(--vp-c-bg); }
.bt { font-size: 12px; font-weight: 600; color: var(--vp-c-text-2); }
.bricks { display: flex; flex-wrap: wrap; gap: 6px; }
.brick { display: inline-flex; gap: 4px; align-items: center; }
.bi { font-weight: 700; }
.bdesc { font-size: 12px; color: var(--vp-c-text-3); min-height: 16px; }
.runbtn { align-self: flex-start; }
.fs { font-size: 12px; color: var(--vp-c-brand-1); align-self: flex-end; margin-top: -24px; }
</style>
