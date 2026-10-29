<script setup lang="ts">
import { ref, computed } from 'vue'

// 场景取自讲义 lecture03.pdf p.25：同一段课程政策文本的三种切法
const SENTENCES = [
  'Grading.',
  'The project milestone is due Week 6, Thursday 11:59pm.',
  'Late days may not be applied to the milestone.',
  'The final report is due Week 10.',
]
const QUERY = '查询：里程碑截止时间？能不能用 late day？'

interface Chunk { parts: number[]; label: string }
type Strat = 'fixed' | 'overlap' | 'structure'

const STRATS: { id: Strat; name: string; chunks: Chunk[]; verdict: string; ok: boolean; note: string }[] = [
  {
    id: 'fixed',
    name: '① 固定大小（50 token，无重叠）',
    chunks: [
      { parts: [0, 1], label: 'chunk 1' },
      { parts: [2, 3], label: 'chunk 2' },
    ],
    verdict: '✗ 关键信息被切散',
    ok: false,
    note: '“截止时间”落在 chunk 1、“late day 不适用”落在 chunk 2——top-1 检索只捞到一半，答案残缺；若边界恰好切在句子中间，还会产生半个句子的坏向量。',
  },
  {
    id: 'overlap',
    name: '② 固定大小 + 10–20% 重叠',
    chunks: [
      { parts: [0, 1], label: 'chunk 1' },
      { parts: [1, 2], label: 'chunk 2（含重叠）' },
      { parts: [2, 3], label: 'chunk 3（含重叠）' },
    ],
    verdict: '△ 能答对，但靠两条命中拼起来',
    ok: true,
    note: '边界处的句子在相邻两块各存一份——没有句子在边界上丢失。代价：索引变大、且同一事实多份向量，可能重复占用 top-k 名额。',
  },
  {
    id: 'structure',
    name: '③ 按结构切（标题/章节边界）',
    chunks: [
      { parts: [0, 1, 2, 3], label: 'chunk 1「Grading」整节' },
    ],
    verdict: '✓ 一个命中块自带完整答案',
    ok: true,
    note: '标题本身就是语义边界——整节政策在同一块里，top-1 即完整。结构切法的前提：文档有可靠结构（Markdown 标题、HTML 节点），对扫描件/长流水文本不适用。',
  },
]

const strat = ref<Strat>('fixed')
const cur = computed(() => STRATS.find((s) => s.id === strat.value)!)
</script>

<template>
  <div class="clab">
    <div class="row wrap">
      <button v-for="s in STRATS" :key="s.id" type="button" class="wbtn" :aria-pressed="s.id === strat"
        @click="strat = s.id">{{ s.name }}</button>
    </div>
    <div class="query">{{ QUERY }}</div>
    <div class="chunks">
      <div v-for="c in cur.chunks" :key="c.label" class="chunk" :class="{ hit: cur.ok }">
        <div class="chunk-label">{{ c.label }}</div>
        <div class="chunk-text">
          <span v-for="p in c.parts" :key="p" class="sent" :class="{ key: p === 1 || p === 2 }">{{ SENTENCES[p] }} </span>
        </div>
      </div>
    </div>
    <div class="hint">
      <span class="k">结果 · </span><b :style="{ color: cur.ok ? '#16a34a' : '#dc2626' }">{{ cur.verdict }}</b>。{{ cur.note }}
    </div>
    <div class="legend"><span class="sent key">关键句（截止时间 / late day）</span></div>
  </div>
</template>

<style scoped>
.clab { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.query { font-size: 14px; color: var(--vp-c-text-2); background: var(--vp-c-default-soft); border-radius: 8px; padding: 6px 12px; align-self: flex-start; }
.chunks { display: flex; flex-direction: column; gap: 8px; }
.chunk { border: 1px solid var(--vp-c-divider); border-radius: 9px; padding: 10px 14px; }
.chunk.hit { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.chunk-label { font-size: 12px; color: var(--vp-c-text-3); margin-bottom: 4px; }
.chunk-text { font-size: 14.5px; line-height: 1.7; }
.sent { margin-right: 4px; }
.sent.key { background: rgba(217, 119, 6, 0.16); color: #b45309; border-radius: 4px; padding: 0 3px; }
.legend { font-size: 12.5px; color: var(--vp-c-text-3); }
</style>
