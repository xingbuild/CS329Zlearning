<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getProgress } from '../progress'

const props = defineProps<{ ids: string[] }>()
const doneCount = ref(0)
const nextLesson = ref<{ title: string; link: string } | null>(null)

const LESSONS = [
  { id: 'l01', title: 'L01 · Agent 是什么', link: '/l01/' },
  { id: 'l02', title: 'L02 · LLM 作为建筑材料', link: '/l02/' },
  { id: 'l03', title: 'L03 · RAG', link: '/l03/' },
  { id: 'l04', title: 'L04 · 工具使用', link: '/l04/' },
  { id: 'l05', title: 'L05 · 框架与编排', link: '/l05/' },
  { id: 'l06', title: 'L06 · 设计模式', link: '/l06/' },
  { id: 'l07', title: 'L07 · 记忆架构', link: '/l07/' },
  { id: 'l08', title: 'L08 · 多智能体', link: '/l08/' },
]

onMounted(() => {
  const p = getProgress()
  doneCount.value = props.ids.filter((id) => p.includes(id)).length
  const lessonDone = new Set(LESSONS.filter((l) => p.includes(l.id)).map((l) => l.id))
  const next = LESSONS.find((l) => !lessonDone.has(l.id))
  nextLesson.value = next ? { title: next.title, link: next.link } : null
  syncHeroCta(next)
})

// R6-5：hero 主按钮随进度改写（"从 L01 开始" → "继续 → 下一讲"）；找不到按钮或出错则保留静态文案兜底
function syncHeroCta(next?: { title: string; link: string } | null) {
  try {
    const btn = document.querySelector('.VPHero .actions a.VPButton.brand') as HTMLAnchorElement | null
    if (!btn) return
    const p = getProgress()
    const started = p.includes('l01')
    if (started && next) {
      btn.textContent = `继续 → ${next.title}`
      btn.setAttribute('href', next.link)
    } else if (!next) {
      btn.textContent = '复习 → L01 · Agent 是什么'
    }
  } catch { /* 静态 hero 按钮兜底 */ }
}
</script>

<template>
  <div class="hp">
    <div class="track">
      <div class="fill" :style="{ width: (ids.length ? (doneCount / ids.length) * 100 : 0) + '%' }" />
    </div>
    <span class="pill">{{ doneCount }} / {{ ids.length }} 学习单元已完成</span>
    <a v-if="nextLesson" :href="nextLesson.link" class="cta">继续 → {{ nextLesson.title }}</a>
    <span v-else class="pill done-all">✓ 八讲全部完成</span>
  </div>
</template>

<style scoped>
.hp { display: flex; align-items: center; gap: 14px; margin: 18px 0 6px; max-width: 640px; flex-wrap: wrap; }
.track { flex: 1; min-width: 120px; height: 8px; background: var(--vp-c-default-soft); border-radius: 999px; overflow: hidden; }
.fill { height: 100%; background: var(--vp-c-brand-1); border-radius: 999px; transition: width 0.4s ease; }
.cta { font-size: 14px; font-weight: 650; color: var(--vp-c-brand-1); text-decoration: none; border-bottom: 1px dashed var(--vp-c-brand-1); }
.cta:hover { opacity: 0.8; }
.done-all { background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); }
</style>
