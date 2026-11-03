<script setup lang="ts">
import { useRouter } from 'vitepress'

// 全课程技术谱系：问题演进 × 约束（点击节点跳对应讲次）
const NODES = [
  { y: 30, era: '1956–1995 · 符号时代', prob: '智能=手写规则；问题：规则写不完', tech: '符号 agent / 专家系统', cost: '脆弱不可迁移 ｜ 约束：算力匮乏', link: '/l01/' },
  { y: 100, era: '1998–2015 · RL 时代', prob: '循环形式化了；问题：大脑要逐任务训练', tech: 'agent–环境循环 / DQN', cost: '稀疏奖励 ｜ 约束：样本天价', link: '/l01/' },
  { y: 170, era: '2018–2022 · 大脑可插拔', prob: '换任务不用重训了；问题：只会说话', tech: 'in-context learning / GPT-3 ｜ 约束：规模化定律', cost: '知识冻结、幻觉', link: '/l02/' },
  { y: 240, era: '2022 · 会做', prob: '怎么让概率大脑行动？', tech: 'ReAct：推理×行动循环', cost: '输出不可靠 → 契约问题 ｜ 约束：API 经济', link: '/l01/' },
  { y: 310, era: '2023–24 · 定契约', prob: '模型与代码如何互信？', tech: 'Structured I/O / Function Calling ｜ 约束：decoder-only 架构', cost: 'schema 碎片化 → 生态问题', link: '/l04/' },
  { y: 380, era: '2024– · 生态化', prob: '工具一次编写、处处可用？', tech: 'MCP（+ 发现即攻击面）', cost: '信任问题（投毒/影子）', link: '/l04/' },
  { y: 450, era: '2020– · 外挂知识', prob: '参数记忆不够用', tech: 'RAG → Agentic RAG', cost: '召回天花板 / 注入', link: '/l03/' },
  { y: 520, era: '2023– · 工程化', prob: '循环能复用、能可靠吗？', tech: '框架 / Temporal 编排', cost: '抽象税、依赖风险', link: '/l05/' },
  { y: 590, era: '2023– · 有经验', prob: '上下文装不下过去', tech: '记忆架构（存-压-取）', cost: '记什么忘什么（未解）', link: '/l07/' },
  { y: 660, era: '2023– · 成组织', prob: '并行收益 > 协调成本？', tech: '多智能体拓扑（开放问题）', cost: '从众 / 武力 ｜ 约束：token 成本', link: '/l08/' },
  { y: 730, era: '2024– · System 深化', prob: '改系统怎么从手艺变搜索？', tech: '优化：context/weight/agent（L09）', cost: '样本效率 vs 数据饥渴 ｜ 约束：API 权限', link: '/l09/' },
  { y: 800, era: '2025– · Eval 深化', prob: '规则不可写时怎么钉死正确？', tech: '评测即事实源：Terminal-Bench（L10）', cost: '任务会腐烂、会被 hack ｜ 约束：verifier 设计', link: '/l10/' },
  { y: 870, era: '2024– · Data 深化', prob: '数据偷偷教了什么？', tech: '轨迹与环境五来源（L11）', cost: 'reward hack / harness 过拟合 ｜ 约束：真实×规模', link: '/l11/' },
]
const router = useRouter()
function go(p: string) { router.go(p) }
</script>

<template>
  <div class="lm">
    <svg viewBox="0 0 880 950" width="100%" role="img" aria-label="全课程技术谱系：问题演进链，点击节点进入对应讲次">
      <defs><marker id="lm-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="var(--vp-c-text-3)" /></marker></defs>
      <line x1="70" y1="20" x2="70" y2="920" class="axis" marker-end="url(#lm-a)" />
      <text x="30" y="380" class="axis-t" transform="rotate(-90 30 380)">问题在不断演进 →</text>
      <g v-for="n in NODES" :key="n.y" class="node" :tabindex="0" role="link" :aria-label="`进入 ${n.era}`"
        @click="go(n.link)" @keydown.enter="go(n.link)">
        <circle cx="70" :cy="n.y" r="7" class="dot" />
        <rect x="100" :y="n.y - 30" width="750" height="60" rx="10" class="nbox" />
        <text x="118" :y="n.y - 8" class="ne">{{ n.era }}</text>
        <text x="330" :y="n.y - 8" class="np">{{ n.prob }}</text>
        <text x="118" :y="n.y + 16" class="nt">{{ n.tech }}</text>
        <text x="560" :y="n.y + 16" class="nc">代价：{{ n.cost }}</text>
      </g>
      <text x="440" y="935" text-anchor="middle" class="foot">每个技术都是"当时问题的应答"，又用自己的代价孕育下一个问题——点击任一节点进入对应讲次（与首页全景图互补：一图时间，一图空间）</text>
    </svg>
  </div>
</template>

<style scoped>
.lm svg :deep(text) { font-family: inherit; }
.axis { stroke: var(--vp-c-divider); stroke-width: 2; }
.axis-t { font-size: 13px; fill: var(--vp-c-text-3); }
.dot { fill: var(--vp-c-brand-1); cursor: pointer; }
.nbox { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); cursor: pointer; }
.node:hover .nbox { stroke: var(--vp-c-brand-1); stroke-width: 2; }
.ne { font-size: 12.5px; font-weight: 700; fill: var(--vp-c-text-2); }
.np { font-size: 12.5px; fill: var(--vp-c-text-1); font-weight: 600; }
.nt { font-size: 12px; fill: var(--vp-c-brand-1); font-weight: 600; }
.nc { font-size: 12.5px; fill: var(--vp-c-text-3); }
.foot { font-size: 12px; fill: var(--vp-c-text-3); }
.node { cursor: pointer; outline: none; }
.node:focus-visible .nbox { stroke: var(--vp-c-brand-1); stroke-width: 2.5; }

/* 窄屏横向滚动查看：桌面容器足够宽不受影响（R6-4） */
.lm { overflow-x: auto; }
.lm svg { min-width: 880px; }
</style>
