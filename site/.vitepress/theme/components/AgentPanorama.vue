<script setup lang="ts">
import { useRouter } from 'vitepress'

defineProps<{ embedded?: boolean }>()
const router = useRouter()
function go(path: string) {
  router.go(path)
}

const parts = {
  core: { link: '/l02/', title: 'LLM Core', sub: '概率大脑 · 采样与上下文', tag: 'L02' },
  reason: { link: '/l06/', title: '推理与规划', sub: 'Thought · 内部动作', tag: 'L01 / L06' },
  memory: { link: '/l07/', title: '记忆 Memory', sub: '存 · 压 · 取', tag: 'L07' },
  tools: { link: '/l04/', title: '工具 Tools', sub: '检索 · 代码 · API · 浏览器', tag: 'L04（RAG 见 L03）' },
  env: { link: '/l01/', title: '环境 Environment', sub: '浏览器 · 操作系统 · 数据库 · 外部世界', tag: 'L01 · 循环' },
  harness: { link: '/l05/', title: '编排与框架 Harness', tag: 'L05' },
  mas: { link: '/l08/', title: '另一个 Agent', sub: 'A2A 通信 · 组织设计', tag: 'L08' },
}
</script>

<template>
  <div class="pano" :class="{ embedded }">
    <svg viewBox="0 0 920 560" width="100%" role="img" aria-label="Agent 全景解剖图：五大件与八讲对应关系，点击部件进入对应讲次">
      <defs>
        <marker id="ap-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="var(--vp-c-text-3)" />
        </marker>
      </defs>

      <!-- 外层：Harness 框架（L05） -->
      <g class="part" :tabindex="0" role="link" @click="go(parts.harness.link)" @keydown.enter="go(parts.harness.link)">
        <title>编排与框架 · L05</title>
        <rect x="16" y="16" width="888" height="528" rx="18" class="frame" />
        <text x="40" y="48" class="frame-label">{{ parts.harness.title }} — 一切脚手架的外壳</text>
        <text x="40" y="68" class="frame-tag">{{ parts.harness.tag }}</text>
      </g>

      <!-- 推理与规划（上中） -->
      <g class="part" :tabindex="0" role="link" @click="go(parts.reason.link)" @keydown.enter="go(parts.reason.link)">
        <title>推理与规划 · L01/L06</title>
        <rect x="380" y="86" width="170" height="96" rx="12" class="box" />
        <text x="465" y="124" text-anchor="middle" class="bt">{{ parts.reason.title }}</text>
        <text x="465" y="146" text-anchor="middle" class="bs">{{ parts.reason.sub }}</text>
        <text x="465" y="166" text-anchor="middle" class="btag">{{ parts.reason.tag }}</text>
      </g>

      <!-- 另一个 Agent（右上，MAS） -->
      <g class="part" :tabindex="0" role="link" @click="go(parts.mas.link)" @keydown.enter="go(parts.mas.link)">
        <title>多智能体 · L08</title>
        <rect x="668" y="86" width="212" height="96" rx="12" class="box mas" />
        <text x="774" y="124" text-anchor="middle" class="bt">{{ parts.mas.title }}</text>
        <text x="774" y="146" text-anchor="middle" class="bs">{{ parts.mas.sub }}</text>
        <text x="774" y="166" text-anchor="middle" class="btag">{{ parts.mas.tag }}</text>
      </g>

      <!-- 记忆（左） -->
      <g class="part" :tabindex="0" role="link" @click="go(parts.memory.link)" @keydown.enter="go(parts.memory.link)">
        <title>记忆 · L07</title>
        <rect x="72" y="232" width="200" height="112" rx="12" class="box" />
        <text x="172" y="272" text-anchor="middle" class="bt">{{ parts.memory.title }}</text>
        <text x="172" y="294" text-anchor="middle" class="bs">{{ parts.memory.sub }}</text>
        <text x="172" y="314" text-anchor="middle" class="btag">{{ parts.memory.tag }}</text>
      </g>

      <!-- LLM Core（中心） -->
      <g class="part core" :tabindex="0" role="link" @click="go(parts.core.link)" @keydown.enter="go(parts.core.link)">
        <title>LLM Core · L02</title>
        <rect x="380" y="228" width="170" height="120" rx="14" class="box corebox" />
        <text x="465" y="272" text-anchor="middle" class="bt">{{ parts.core.title }}</text>
        <text x="465" y="294" text-anchor="middle" class="bs">{{ parts.core.sub }}</text>
        <text x="465" y="314" text-anchor="middle" class="btag">{{ parts.core.tag }}</text>
      </g>

      <!-- 工具（右） -->
      <g class="part" :tabindex="0" role="link" @click="go(parts.tools.link)" @keydown.enter="go(parts.tools.link)">
        <title>工具 · L04</title>
        <rect x="648" y="232" width="200" height="112" rx="12" class="box" />
        <text x="748" y="272" text-anchor="middle" class="bt">{{ parts.tools.title }}</text>
        <text x="748" y="294" text-anchor="middle" class="bs">{{ parts.tools.sub }}</text>
        <text x="748" y="314" text-anchor="middle" class="btag">{{ parts.tools.tag }}</text>
      </g>

      <!-- 环境（底） -->
      <g class="part" :tabindex="0" role="link" @click="go(parts.env.link)" @keydown.enter="go(parts.env.link)">
        <title>环境 · L01</title>
        <rect x="72" y="438" width="776" height="88" rx="12" class="box" />
        <text x="460" y="476" text-anchor="middle" class="bt">{{ parts.env.title }}</text>
        <text x="460" y="498" text-anchor="middle" class="bs">{{ parts.env.sub }}</text>
        <text x="770" y="476" text-anchor="middle" class="btag">{{ parts.env.tag }}</text>
      </g>

      <!-- 箭头：观察 Obs（环境 → Core） -->
      <line x1="465" y1="438" x2="465" y2="352" class="arr" marker-end="url(#ap-a)" />
      <text x="474" y="400" class="al">观察 Obs</text>

      <!-- 行动 Act（Core → 工具） -->
      <line x1="550" y1="288" x2="644" y2="288" class="arr" marker-end="url(#ap-a)" />
      <text x="597" y="278" text-anchor="middle" class="al">行动 Act</text>

      <!-- 工具 → 环境（执行结果） -->
      <line x1="748" y1="344" x2="748" y2="432" class="arr" marker-end="url(#ap-a)" />
      <text x="758" y="394" class="al">执行 · 结果</text>

      <!-- 记忆 ↔ Core（读写） -->
      <line x1="272" y1="288" x2="376" y2="288" class="arr" marker-start="url(#ap-a)" marker-end="url(#ap-a)" />
      <text x="324" y="278" text-anchor="middle" class="al">读写</text>

      <!-- 推理 ↔ Core（Thought，虚线内部动作） -->
      <line x1="465" y1="182" x2="465" y2="224" class="arr dash" marker-start="url(#ap-a)" marker-end="url(#ap-a)" />
      <text x="380" y="208" text-anchor="end" class="al">Thought</text>

      <!-- Core → 另一 Agent（A2A，点线） -->
      <line x1="556" y1="240" x2="700" y2="150" class="arr dot" marker-end="url(#ap-a)" />
      <text x="626" y="186" text-anchor="middle" class="al">A2A</text>
    </svg>
    <div class="pano-cap">
      概率大脑（L02）以推理驱动循环（L01/L06）：向左读写记忆（L07），向右调用工具（L04；RAG 是第一个工具 L03），向下作用于环境（L01）；外壳由框架与编排包裹（L05），多个 agent 相互通信即多智能体（L08）。
      <b>点击任一部件 → 进入对应讲次。</b>
    </div>
  </div>
</template>

<style scoped>
.pano { margin: 10px 0 4px; }
.pano svg { display: block; }
.pano :deep(text) { font-family: inherit; }
.frame { fill: none; stroke: var(--vp-c-divider); stroke-dasharray: 7 7; }
.frame-label { font-size: 14px; font-weight: 600; fill: var(--vp-c-text-2); }
.frame-tag { font-size: 12px; fill: var(--vp-c-brand-1); font-weight: 600; }
.box { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); stroke-width: 1.5; }
.corebox { fill: var(--vp-c-brand-soft); stroke: var(--vp-c-brand-1); stroke-width: 2; }
.bt { font-size: 19px; font-weight: 700; fill: var(--vp-c-text-1); }
.bs { font-size: 12.5px; fill: var(--vp-c-text-2); }
.btag { font-size: 12px; font-weight: 700; fill: var(--vp-c-brand-1); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 1.8; fill: none; }
.arr.dash { stroke-dasharray: 5 5; }
.arr.dot { stroke-dasharray: 2 6; stroke-linecap: round; }
.al { font-size: 12.5px; fill: var(--vp-c-text-2); }
.part { cursor: pointer; }
.part:focus { outline: none; }
.part:hover .box, .part:focus-visible .box { stroke: var(--vp-c-brand-1); stroke-width: 2.5; }
.part:hover .frame, .part:focus-visible .frame { stroke: var(--vp-c-brand-1); }
.part:hover .bt, .part:focus-visible .bt { fill: var(--vp-c-brand-1); }
.pano-cap { font-size: 13.5px; line-height: 1.75; color: var(--vp-c-text-2); margin-top: 8px; max-width: 760px; }

/* 窄屏横向滚动查看：桌面容器足够宽不受影响（R6-4） */
.pano { overflow-x: auto; }
.pano svg { min-width: 640px; }
</style>
