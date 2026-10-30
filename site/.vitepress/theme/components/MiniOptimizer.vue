<script setup lang="ts">
import { ref, computed } from 'vue'

// 站②的「模型」用概率表模拟（工程保真、教学诚实，同 Lab02 先例）：
// 每个候选 prompt 对每类样本有真实命中率，评估回路 = 伯努利采样 + 确定性判分。
type Kind = 'direct' | 'irony' | 'comparative' | 'jargon'
const KIND_NAME: Record<Kind, string> = { direct: '直白', irony: '讽刺', comparative: '比较级', jargon: '领域术语' }

const SAMPLES: { id: number; text: string; kind: Kind; label: '正面' | '负面' }[] = [
  { id: 1, text: '物流很快，包装完好，非常满意。', kind: 'direct', label: '正面' },
  { id: 2, text: '客服态度差，再也不来了。', kind: 'direct', label: '负面' },
  { id: 3, text: '哇，等了两周才到，真是"惊喜"呢。', kind: 'irony', label: '负面' },
  { id: 4, text: '好一个"智能"客服，问三句答一句。', kind: 'irony', label: '负面' },
  { id: 5, text: '比我家旧的那台好，但没好到值这个价。', kind: 'comparative', label: '负面' },
  { id: 6, text: '比上一代快了一倍，这钱花得值。', kind: 'comparative', label: '正面' },
  { id: 7, text: 'ISP 握手感很稳，驱动开箱即用。', kind: 'jargon', label: '正面' },
  { id: 8, text: '固件刷了三版，丢包率还是高。', kind: 'jargon', label: '负面' },
]

interface Cand {
  id: string
  name: string
  desc: string
  base: Record<Kind, number>
  boosted: Set<Kind>
}

function mkCand(id: string, name: string, desc: string, base: Record<Kind, number>): Cand {
  return { id, name, desc, base: { ...base }, boosted: new Set() }
}

const cands = ref<Cand[]>([
  mkCand('p0', 'P0 · 裸问', '「判断这条评论是正面还是负面」', { direct: 0.9, irony: 0.35, comparative: 0.5, jargon: 0.55 }),
  mkCand('p1', 'P1 · 措辞改进', '「注意讽刺与比较级，先解释再判断」', { direct: 0.9, irony: 0.72, comparative: 0.78, jargon: 0.5 }),
  mkCand('p2', 'P2 · few-shot 槽位版', '指令同 P0，但带示例槽（初始为空）', { direct: 0.85, irony: 0.3, comparative: 0.45, jargon: 0.5 }),
])
const FEWSHOT_CAP: Record<Kind, number> = { direct: 0.95, irony: 0.92, comparative: 0.93, jargon: 0.9 }

// 评估回路状态：每候选累积 (轮次, 命中数) 与最近一轮逐样本明细
const rounds = ref<{ cand: string; hit: number; detail: Record<number, boolean> }[]>([])
const roundNo = computed(() => rounds.value.length / 3 || 0)
const stats = computed(() => {
  const m: Record<string, { runs: number; hits: number; last?: number; detail?: Record<number, boolean> }> = {}
  for (const c of cands.value) m[c.id] = { runs: 0, hits: 0 }
  for (const r of rounds.value) {
    m[r.cand].runs++
    m[r.cand].hits += r.hit
    m[r.cand].last = r.hit
    m[r.cand].detail = r.detail
  }
  return m
})
const best = computed(() => {
  let id = cands.value[0].id
  let top = -1
  for (const c of cands.value) {
    const s = stats.value[c.id]
    const avg = s.runs ? s.hits / s.runs / SAMPLES.length : 0
    if (avg > top) { top = avg; id = c.id }
  }
  return id
})
const bootLog = ref<string[]>([])

function hitRate(c: Cand, kind: Kind) {
  let r = c.base[kind]
  if (c.boosted.has(kind)) r = Math.min(FEWSHOT_CAP[kind], r + 0.2)
  return r
}

function runEval() {
  const batch: { cand: string; hit: number; detail: Record<number, boolean> }[] = []
  for (const c of cands.value) {
    const detail: Record<number, boolean> = {}
    let hit = 0
    for (const s of SAMPLES) {
      const ok = Math.random() < hitRate(c, s.kind)
      detail[s.id] = ok
      if (ok) hit++
    }
    batch.push({ cand: c.id, hit, detail })
  }
  rounds.value.push(...batch)
}

function bootstrap() {
  const b = cands.value.find((c) => c.id === best.value)!
  const s = stats.value[b.id]
  if (!s.detail) { bootLog.value.unshift('先跑一轮评估——bootstrap 需要正确的轨迹做示例。'); return }
  const correctKinds = new Set(SAMPLES.filter((x) => s.detail![x.id]).map((x) => x.kind))
  if (correctKinds.size === 0) { bootLog.value.unshift('这一轮最佳候选全错——没有可用轨迹，再跑几轮。'); return }
  const p2 = cands.value.find((c) => c.id === 'p2')!
  const added: string[] = []
  for (const k of correctKinds) {
    if (!p2.boosted.has(k)) { p2.boosted.add(k); added.push(KIND_NAME[k]) }
  }
  if (added.length === 0) { bootLog.value.unshift('P2 的示例槽已装满这些类型——再跑评估看提升。'); return }
  bootLog.value.unshift(`第 ${roundNo.value} 轮后：取最佳候选「${b.name}」的正确轨迹 ${SAMPLES.filter((x) => s.detail![x.id]).length} 条 → 作为 few-shot 注入 P2，覆盖类型：${added.join('、')}（对应类型命中率 +0.2）`)
}

function reset() {
  rounds.value = []
  bootLog.value = []
  for (const c of cands.value) c.boosted.clear()
}
</script>

<template>
  <div class="opt">
    <div class="ops">
      <button type="button" class="wbtn" @click="runEval">▶ 跑一轮评估（3 候选 × 8 样本）</button>
      <button type="button" class="wbtn" @click="bootstrap">⚡ Bootstrap 注入 P2</button>
      <button type="button" class="wbtn" @click="reset">↺ 重置</button>
      <span class="rn">第 {{ roundNo }} 轮</span>
    </div>

    <div class="cands">
      <div v-for="c in cands" :key="c.id" class="cand" :class="{ top: c.id === best && roundNo > 0 }">
        <div class="ch">
          <span class="cname">{{ c.name }}<span v-if="c.id === best && roundNo > 0" class="crown"> 当前最佳</span></span>
          <span class="cdesc">{{ c.desc }}</span>
        </div>
        <div v-if="c.id === 'p2' && c.boosted.size" class="slots">示例槽：{{ [...c.boosted].map((k) => KIND_NAME[k]).join('、') }}</div>
        <div class="grid">
          <div v-for="s in SAMPLES" :key="s.id" class="cell" :class="{
            hit: stats[c.id]?.detail?.[s.id] === true,
            miss: stats[c.id]?.detail?.[s.id] === false,
          }" :title="`${s.text}（${KIND_NAME[s.kind]}）`">
            <span class="cid">#{{ s.id }}</span>
            <span class="ck">{{ KIND_NAME[s.kind] }}</span>
            <span class="cm">{{ stats[c.id]?.detail?.[s.id] === true ? '✓' : stats[c.id]?.detail?.[s.id] === false ? '✗' : '—' }}</span>
          </div>
        </div>
        <div class="cline">
          <span v-if="stats[c.id]?.runs">本轮 {{ stats[c.id].last }}/8 · 累积平均 {{ (stats[c.id].hits / stats[c.id].runs / SAMPLES.length * 100).toFixed(0) }}%（{{ stats[c.id].runs }} 轮）</span>
          <span v-else>未评估</span>
        </div>
      </div>
    </div>

    <div v-if="bootLog.length" class="blog">
      <div v-for="(l, i) in bootLog.slice(0, 3)" :key="i" class="bl">{{ l }}</div>
    </div>

    <div class="hint"><span class="k">机制对位 · </span>候选生成器（三张卡）→ 评估回路（▶ 按钮：真采样真打分）→ 搜索策略（⚡ bootstrap：正确轨迹注入示例槽）——这就是课文「50 行复刻 Optimizer」的全部零件。多跑几轮看分数波动：单轮分数会骗人，评测要样本量。</div>
  </div>
</template>

<style scoped>
.opt { display: flex; flex-direction: column; gap: 12px; }
.ops { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.rn { font-size: 12px; color: var(--vp-c-text-2); margin-left: auto; }
.cands { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px; }
.cand { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 8px; }
.cand.top { border-color: var(--vp-c-brand-1); }
.ch { display: flex; flex-direction: column; gap: 2px; }
.cname { font-weight: 600; font-size: 14px; }
.crown { font-size: 11px; color: var(--vp-c-brand-1); margin-left: 6px; }
.cdesc { font-size: 12px; color: var(--vp-c-text-2); }
.slots { font-size: 12px; color: var(--vp-c-brand-1); border: 1px dashed var(--vp-c-brand-1); border-radius: 6px; padding: 3px 8px; align-self: flex-start; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; }
.cell { display: flex; flex-direction: column; align-items: center; gap: 1px; border-radius: 6px; padding: 4px 2px; font-size: 11px; background: var(--vp-c-default-soft); }
.cell.hit { background: var(--vp-c-brand-soft); }
.cell.miss { background: var(--vp-c-danger-soft); }
.ck { color: var(--vp-c-text-3); }
.cm { font-weight: 700; }
.cline { font-size: 12px; color: var(--vp-c-text-2); }
.blog { border-top: 1px dashed var(--vp-c-divider); padding-top: 8px; display: flex; flex-direction: column; gap: 4px; }
.bl { font-size: 12px; color: var(--vp-c-text-2); }
</style>
