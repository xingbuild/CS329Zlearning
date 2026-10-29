<script setup lang="ts">
import { ref, computed } from 'vue'

// 场景改编自讲义 lecture02.pdf p.168-169：顺序追加 vs 前缀插入（"Actually, ..."）
type Mode = 'append' | 'prepend'

interface Frame {
  tokens: { t: string; state: 'cached' | 'fresh' | 'dead' }[]
  note: string
  cost: number
}

const BASE = ['The', 'class', 'was', 'about']

function framesFor(mode: Mode): Frame[] {
  if (mode === 'append') {
    return [
      { tokens: BASE.map((t) => ({ t, state: 'cached' as const })), note: '已有 4 个 token 完成前向计算，K/V 已进缓存（绿色）——无需重算。', cost: 0 },
      { tokens: [...BASE, { t: 'agents', state: 'fresh' }], note: '追加一个词：只有新 token 需要计算（蓝色），缓存全部命中。KV Cache 的存在就是为了这个。', cost: 1 },
      { tokens: [...BASE, { t: 'agents', state: 'cached' }, { t: '.', state: 'fresh' }], note: '继续追加，依旧只算新增——成本随长度线性增长，历史是免费的。', cost: 2 },
    ]
  }
  return [
    { tokens: BASE.map((t) => ({ t, state: 'cached' as const })), note: '同样的起点：4 个 token 已缓存。', cost: 0 },
    { tokens: [{ t: 'Actually,', state: 'fresh' }, ...BASE.map((t) => ({ t, state: 'dead' }))], note: '在头部插入 “Actually,”：其后所有 token 的位置编码全部改变 → 注意力结果全部失效（红色）。缓存一分钱都没省下。', cost: 5 },
    { tokens: [{ t: 'Actually,', state: 'fresh' }, ...BASE.map((t) => ({ t, state: 'fresh' })), { t: 'agents', state: 'fresh' }], note: '整个序列必须重新 prefill。对话式 agent 每轮在开头塞新指令、或修改历史消息，都在触发这一幕。', cost: 6 },
  ]
}

const mode = ref<Mode>('append')
const idx = ref(0)
const frames = computed(() => framesFor(mode.value))
const cur = computed(() => frames.value[idx.value])

function switchMode(m: Mode) {
  mode.value = m
  idx.value = 0
}
</script>

<template>
  <div class="kv">
    <div class="row wrap">
      <button type="button" class="wbtn" :aria-pressed="mode === 'append'" @click="switchMode('append')">① 顺序追加（append-only）</button>
      <button type="button" class="wbtn" :aria-pressed="mode === 'prepend'" @click="switchMode('prepend')">② 头部插入（“Actually, …”）</button>
    </div>
    <div class="row wrap">
      <button type="button" class="wbtn" :disabled="idx === 0" @click="idx--">◀ 上一步</button>
      <button type="button" class="wbtn primary" :disabled="idx === frames.length - 1" @click="idx++">下一步 ▶</button>
      <span class="pill brand">累计需计算：{{ cur.cost }} 个 token</span>
    </div>
    <div class="stage">
      <span v-for="(tk, i) in cur.tokens" :key="mode + i" class="tk" :class="tk.state">{{ tk.t }}</span>
    </div>
    <div class="hint"><span class="k">现在看什么 · </span>{{ cur.note }}</div>
    <div class="legend">
      <span class="tk cached">缓存命中</span><span class="tk fresh">需计算</span><span class="tk dead">缓存失效</span>
    </div>
  </div>
</template>

<style scoped>
.kv { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.stage { display: flex; flex-wrap: wrap; gap: 8px; padding: 14px; border: 1px dashed var(--vp-c-divider); border-radius: 10px; min-height: 64px; align-items: center; }
.tk { padding: 4px 12px; border-radius: 7px; font-size: 14px; font-family: var(--vp-font-family-mono, monospace); }
.tk.cached { background: rgba(22, 163, 74, 0.14); color: #16a34a; }
.tk.fresh { background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); }
.tk.dead { background: rgba(220, 38, 38, 0.12); color: #dc2626; text-decoration: line-through; }
.legend { display: flex; gap: 10px; flex-wrap: wrap; }
.legend .tk { text-decoration: none; font-size: 12.5px; }
.legend .tk.dead { text-decoration: none; }
</style>
