<script setup lang="ts">
import { ref, computed } from 'vue'

// 提示彩票机（据讲义 lecture09 开场 Poll：PaLM 2-L-IT 真实数据，Yang et al. OPRO）
// 问题先行：先猜 → 揭示 → 体验 prompt 工程的彩票性
const PROMPTS = [
  { id: 'a', label: 'A', text: "Let's think step by step.", score: 71.8 },
  { id: 'b', label: 'B', text: "Take a deep breath and work on this problem step-by-step.", score: 80.2 },
  { id: 'c', label: 'C', text: "Let's combine our numerical command and clear thinking to quickly and accurately decipher the answer.", score: 74.5 },
]
const guess = ref<string | null>(null)
const revealed = ref(false)
const sorted = computed(() => [...PROMPTS].sort((x, y) => y.score - x.score))
const guessedRight = computed(() => guess.value === 'b')
function choose(id: string) { if (!revealed.value) guess.value = id }
function reveal() { revealed.value = true }
function reset() { guess.value = null; revealed.value = false }
</script>

<template>
  <div class="plt">
    <div class="ops">
      <span class="q">同一道数学题、同一个模型（PaLM 2-L-IT），只换这一句开场白——先凭直觉押注哪张卡得分最高：</span>
      <button type="button" class="wbtn" :disabled="!guess || revealed" @click="reveal">揭示真实得分</button>
      <button type="button" class="wbtn" :disabled="!revealed" @click="reset">↺ 再来一次</button>
    </div>
    <div class="cards">
      <button v-for="p in PROMPTS" :key="p.id" type="button" class="pcard" :class="{
        picked: guess === p.id, top: revealed && p.id === sorted[0].id,
      }" :aria-pressed="guess === p.id" @click="choose(p.id)">
        <span class="pl">{{ p.label }}</span>
        <span class="pt">"{{ p.text }}"</span>
        <span class="ps" :class="{ show: revealed }">{{ revealed ? p.score + '%' : '? %' }}</span>
        <span v-if="revealed && p.id === sorted[0].id" class="crown">实际最优</span>
      </button>
    </div>
    <div v-if="revealed" class="verdict" :class="guessedRight ? 'ok' : 'bad'">
      <template v-if="!guessedRight">你的直觉落空了——<b>"深呼吸"这 5 个字值 8.4 个百分点</b>（80.2% 对 71.8%），而没有任何先验能告诉你为什么。这就是 prompt 手工调优的彩票性：不可推导、不可复现、换个任务就重排。</template>
      <template v-else>这次你猜对了——但别高兴：这只是运气。<b>换个任务、换个模型，这个排序立刻失效</b>（OPRO 论文里"深呼吸"只在部分任务赢）。靠猜，每次都要重猜。</template>
      <span class="vk">本讲的根本问题：怎么把"猜"变成<b>带度量的搜索</b>——数据 + 评测 + 优化算法，让改系统本身变成可复现的工程。</span>
    </div>
    <div class="hint"><span class="k">数据出处 · </span>讲义开场 Poll（GSM8K 类任务，PaLM 2-L-IT）；"Take a deep breath" 由 OPRO（LLM as Optimizer, Yang et al. 2024）自动搜索发现——第三幕你会看到：发现这句话的不是人，是优化器。</div>
  </div>
</template>

<style scoped>
.plt { display: flex; flex-direction: column; gap: 10px; }
.ops { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.q { font-size: 13.5px; font-weight: 600; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; }
.pcard { display: flex; flex-direction: column; gap: 6px; align-items: center; text-align: center; border: 1.5px solid var(--vp-c-divider); border-radius: 10px; padding: 12px 10px; background: var(--vp-c-bg-soft); cursor: pointer; transition: all .2s; }
.pcard:hover { border-color: var(--vp-c-brand-1); }
.pcard.picked { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.pcard.top { border-color: var(--vp-c-green-1, #16a34a); }
.pl { font-weight: 700; font-size: 14px; }
.pt { font-size: 12.5px; color: var(--vp-c-text-2); line-height: 1.5; }
.ps { font-size: 20px; font-weight: 700; color: var(--vp-c-text-3); }
.ps.show { color: var(--vp-c-text-1); }
.crown { font-size: 11px; color: var(--vp-c-green-1, #16a34a); font-weight: 700; }
.verdict { border-radius: 10px; padding: 10px 14px; font-size: 13.5px; line-height: 1.7; display: flex; flex-direction: column; gap: 4px; }
.verdict.bad { background: var(--vp-c-danger-soft); }
.verdict.ok { background: var(--vp-c-brand-soft); }
.vk { color: var(--vp-c-text-2); font-size: 12.5px; border-top: 1px dashed var(--vp-c-divider); padding-top: 4px; }
</style>
