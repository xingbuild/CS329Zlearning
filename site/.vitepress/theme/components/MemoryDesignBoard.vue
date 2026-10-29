<script setup lang="ts">
import { ref, computed } from 'vue'

// What / When / How 三问设计盘，选项整理自讲义 lecture07.pdf p.24-28
const DIMS = [
  {
    id: 'what',
    q: 'WHAT · 存什么',
    opts: [
      { id: 'facts', label: '事实（具体/通用）' },
      { id: 'proc', label: '程序（技能/流程）' },
      { id: 'prog', label: '会话进展' },
    ],
  },
  {
    id: 'when',
    q: 'WHEN · 何时触发',
    opts: [
      { id: 'tool', label: 'Agent 工具（按需）' },
      { id: 'bg', label: '后台工人（闲时）' },
      { id: 'event', label: '事件驱动（即时）' },
    ],
  },
  {
    id: 'how',
    q: 'HOW · 放在哪',
    opts: [
      { id: 'fs', label: '文件系统' },
      { id: 'db', label: '数据库（向量/BM25）' },
      { id: 'kg', label: '知识图谱' },
    ],
  },
] as const

type DimId = (typeof DIMS)[number]['id']
const picks = ref<Record<string, string>>({ what: 'facts', when: 'tool', how: 'fs' })

const VERDICTS: Record<string, string> = {
  'facts|tool|fs': '≈ 本课程站的做法：AGENTS.md/进度文件 + 会话按需读写。',
  'proc|bg|fs': '≈ Open Claw：夜间 3 点后台整理，把值得留的写进 MEMORY.md。',
  'facts|event|db': '≈ Mem0 风格：对话事件即时触发，后台工作流 ADD/UPDATE/DELETE/NOOP。',
  'proc|tool|fs': '≈ Voyager / Skill Files：成功轨迹归纳成技能文件，任务来了按需加载。',
  'prog|tool|db': '≈ MemGPT 风格：会话 FIFO 进召回库，agent 自己决定翻档案。',
}
const verdict = computed(() => VERDICTS[`${picks.value.what}|${picks.value.when}|${picks.value.how}`] || '一个自洽的组合——真实系统几乎都是多维混合体，讲义的四个"模式"就是几种被验证过的著名搭配。')
</script>

<template>
  <div class="mdb">
    <div v-for="d in DIMS" :key="d.id" class="dim">
      <div class="dq">{{ d.q }}</div>
      <div class="opts">
        <button v-for="o in d.opts" :key="o.id" type="button" class="wbtn" :aria-pressed="picks[d.id] === o.id"
          @click="picks[d.id] = o.id">{{ o.label }}</button>
      </div>
    </div>
    <div class="hint"><span class="k">你的设计 · </span>{{ verdict }}</div>
  </div>
</template>

<style scoped>
.mdb { display: flex; flex-direction: column; gap: 12px; }
.dim { display: flex; flex-direction: column; gap: 6px; }
.dq { font-size: 13.5px; font-weight: 700; color: var(--vp-c-text-2); }
.opts { display: flex; gap: 8px; flex-wrap: wrap; }
</style>
