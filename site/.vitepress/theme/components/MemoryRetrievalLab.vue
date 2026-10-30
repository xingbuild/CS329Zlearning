<script setup lang="ts">
import { ref, computed } from 'vue'

// 站① · Generative Agents 三因子检索的真算版：时近 × 重要性 × 相关性加权重排
interface Mem { id: number; text: string; days: number; imp: number; tags: string[] }
const MEMS: Mem[] = [
  { id: 1, text: 'Klaus 在社区聚会上说他年轻时是摄影师，还办过展览', days: 28, imp: 7, tags: ['Klaus', '摄影', '爱好'] },
  { id: 2, text: 'Maria 问我借了 50 欧买种子，说下周还', days: 3, imp: 8, tags: ['Maria', '借钱', '债务'] },
  { id: 3, text: '昨天下大雨，集市摊位少了一半', days: 1, imp: 3, tags: ['天气', '集市'] },
  { id: 4, text: 'Maria 的花园里种了十几种番茄，她说八月最好吃', days: 15, imp: 6, tags: ['Maria', '花园', '番茄'] },
  { id: 5, text: 'Klaus 借走了我的梯子，说修屋顶用', days: 5, imp: 6, tags: ['Klaus', '梯子', '借物'] },
  { id: 6, text: '镇长宣布下个月开始修主路，工期三周', days: 2, imp: 8, tags: ['镇长', '修路', '公告'] },
  { id: 7, text: '和 Maria 约好周五早上去湖边钓鱼', days: 1, imp: 7, tags: ['Maria', '钓鱼', '约定'] },
  { id: 8, text: 'Klaus 的孙子要来镇上过暑假', days: 40, imp: 6, tags: ['Klaus', '孙子', '家庭'] },
  { id: 9, text: 'Maria 做的苹果派在集市上得了第一名', days: 60, imp: 5, tags: ['Maria', '苹果派', '集市'] },
  { id: 10, text: '社区卫生大扫除定在周六上午', days: 2, imp: 5, tags: ['社区', '大扫除', '安排'] },
  { id: 11, text: 'Klaus 说过他的膝盖在阴雨天会疼', days: 12, imp: 4, tags: ['Klaus', '健康'] },
  { id: 12, text: 'Maria 是两年前从城里搬来的', days: 45, imp: 5, tags: ['Maria', '搬来', '背景'] },
  { id: 13, text: '昨晚停电了两小时，据说要检修线路', days: 1, imp: 4, tags: ['停电', '检修'] },
  { id: 14, text: 'Klaus 帮邻居修好了收音机，没收钱', days: 20, imp: 4, tags: ['Klaus', '帮忙', '收音机'] },
  { id: 15, text: 'Maria 在学吉他，想参加秋天的音乐会', days: 8, imp: 6, tags: ['Maria', '吉他', '爱好'] },
  { id: 16, text: '集市的面包摊换了一家，老摊主退休了', days: 6, imp: 3, tags: ['集市', '面包'] },
  { id: 17, text: '镇长征求大家对新建儿童游乐场的意见', days: 30, imp: 7, tags: ['镇长', '游乐场', '公告'] },
  { id: 18, text: 'Klaus 的摄影展老照片挂在社区中心走廊', days: 50, imp: 4, tags: ['Klaus', '摄影', '展览'] },
  { id: 19, text: 'Maria 说她怕狗，路过牧场会绕路', days: 25, imp: 5, tags: ['Maria', '怕狗'] },
  { id: 20, text: '今天早上的面包很新鲜，酸奶卖完了', days: 1, imp: 2, tags: ['面包', '早餐'] },
]

const QUERIES = [
  { id: 'hobby', q: 'Klaus 有什么爱好？', keys: ['Klaus', '爱好'], note: '金标准在 28 天前——纯时近会把它埋掉' },
  { id: 'debt', q: '谁欠我钱？', keys: ['借钱', '债务'], note: '近且重要——三因子都容易找到' },
  { id: 'plan', q: '这几天有什么安排？', keys: ['约定', '安排', '钓鱼'], note: '时近主导的查询' },
  { id: 'event', q: '社区最近有什么大事？', keys: ['镇长', '公告', '修路', '游乐场'], note: '重要公告散在不同时间点' },
]

const qIdx = ref(0)
const query = computed(() => QUERIES[qIdx.value])
const wRec = ref(1), wImp = ref(1), wRel = ref(1)

function recScore(days: number) { return 1 / (1 + days / 7) }
function impScore(imp: number) { return imp / 10 }
function relScore(tags: string[]) {
  const keys = query.value.keys
  const hit = keys.filter((k) => tags.some((t) => t.includes(k) || k.includes(t))).length
  return keys.length ? hit / keys.length : 0
}

const ranked = computed(() => {
  return MEMS.map((m) => {
    const r = recScore(m.days), i = impScore(m.imp), l = relScore(m.tags)
    return { ...m, r, i, l, total: wRec.value * r + wImp.value * i + wRel.value * l }
  }).sort((a, b) => b.total - a.total)
})
const top5 = computed(() => ranked.value.slice(0, 5))
const maxTotal = computed(() => top5.value[0]?.total || 1)

function preset(kind: 'ga' | 'rel' | 'rec') {
  if (kind === 'ga') { wRec.value = 1; wImp.value = 1; wRel.value = 1 }
  if (kind === 'rel') { wRec.value = 0; wImp.value = 0; wRel.value = 1 }
  if (kind === 'rec') { wRec.value = 1; wImp.value = 0; wRel.value = 0 }
}
</script>

<template>
  <div class="mr">
    <div class="qbar">
      <button v-for="(q, i) in QUERIES" :key="q.id" type="button" class="wbtn" :aria-pressed="i === qIdx"
        @click="qIdx = i">{{ q.q }}</button>
      <span class="qnote">{{ query.note }}</span>
    </div>

    <div class="dials">
      <label class="dial">
        <span>时近性 × {{ wRec }}</span>
        <input type="range" min="0" max="3" step="0.5" v-model.number="wRec" />
      </label>
      <label class="dial">
        <span>重要性 × {{ wImp }}</span>
        <input type="range" min="0" max="3" step="0.5" v-model.number="wImp" />
      </label>
      <label class="dial">
        <span>相关性 × {{ wRel }}</span>
        <input type="range" min="0" max="3" step="0.5" v-model.number="wRel" />
      </label>
      <div class="presets">
        <button type="button" class="wbtn" :aria-pressed="wRec === 1 && wImp === 1 && wRel === 1" @click="preset('ga')">GA 默认</button>
        <button type="button" class="wbtn" :aria-pressed="wRec === 0 && wImp === 0" @click="preset('rel')">纯相关</button>
        <button type="button" class="wbtn" :aria-pressed="wImp === 0 && wRel === 0" @click="preset('rec')">纯时近</button>
      </div>
    </div>

    <div class="list">
      <div v-for="(m, i) in top5" :key="m.id" class="mrow" :class="{ first: i === 0 }">
        <span class="rk">#{{ i + 1 }}</span>
        <div class="mmain">
          <div class="mtext">{{ m.text }}</div>
          <div class="mmeta">{{ m.days }} 天前 · 重要性 {{ m.imp }}/10</div>
          <div class="mbar">
            <div class="seg r" :style="{ width: (wRec * m.r / maxTotal * 100) + '%' }" />
            <div class="seg i" :style="{ width: (wImp * m.i / maxTotal * 100) + '%' }" />
            <div class="seg l" :style="{ width: (wRel * m.l / maxTotal * 100) + '%' }" />
          </div>
        </div>
        <span class="mtotal">{{ m.total.toFixed(2) }}</span>
      </div>
    </div>
    <div class="legend">
      <span class="seg-demo r" />时近 × {{ wRec }}　<span class="seg-demo i" />重要性 × {{ wImp }}　<span class="seg-demo l" />相关性 × {{ wRel }}（条内三段即该记忆的得分分解）
    </div>

    <div class="hint"><span class="k">机制对位 · </span>「纯相关」查 Klaus 爱好——28 天前的办展记忆浮上来，但无关的 Klaus 梯子也挤进前排；「纯时近」——今天的面包把人生大事全压下去。三因子相乘/相加才构成「此时此刻值得想起」（复刻检验题：去掉任何一个因子会得什么病，拨一下就看到）。</div>
  </div>
</template>

<style scoped>
.mr { display: flex; flex-direction: column; gap: 12px; }
.qbar { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.qnote { font-size: 12px; color: var(--vp-c-text-3); }
.dials { display: flex; flex-wrap: wrap; gap: 14px; align-items: end; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px; }
.dial { display: flex; flex-direction: column; gap: 4px; font-size: 12px; color: var(--vp-c-text-2); }
.dial input[type='range'] { width: 130px; }
.presets { display: flex; gap: 6px; margin-left: auto; }
.list { display: flex; flex-direction: column; gap: 6px; }
.mrow { display: flex; gap: 10px; align-items: center; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 8px 12px; }
.mrow.first { border-color: var(--vp-c-brand-1); }
.rk { font-size: 12px; color: var(--vp-c-text-3); min-width: 26px; }
.mmain { flex: 1; display: flex; flex-direction: column; gap: 3px; }
.mtext { font-size: 13px; }
.mmeta { font-size: 11px; color: var(--vp-c-text-3); }
.mbar { display: flex; height: 6px; border-radius: 3px; overflow: hidden; background: var(--vp-c-default-soft); }
.seg.r { background: var(--vp-c-brand-1); }
.seg.i { background: var(--vp-c-warning-1, #e3af37); }
.seg.l { background: var(--vp-c-danger-1); }
.mtotal { font-size: 13px; font-weight: 700; min-width: 40px; text-align: right; }
.legend { font-size: 11px; color: var(--vp-c-text-3); }
.seg-demo { display: inline-block; width: 12px; height: 6px; border-radius: 3px; vertical-align: middle; }
</style>
