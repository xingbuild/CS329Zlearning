<template>
  <div class="tca">
    <svg viewBox="0 0 920 250" width="100%" role="img" aria-label="一次工具调用的解剖：选择 → 参数 → 校验 → 执行 → 回喂">
      <defs>
        <marker id="tca-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="var(--vp-c-text-3)" />
        </marker>
      </defs>

      <!-- LLM 起点 -->
      <circle cx="60" cy="70" r="34" class="llm" />
      <text x="60" y="66" text-anchor="middle" class="bt">LLM</text>
      <text x="60" y="84" text-anchor="middle" class="bs">概率</text>

      <!-- 五步 -->
      <rect x="136" y="40" width="130" height="60" rx="10" class="box" />
      <text x="201" y="64" text-anchor="middle" class="bt">① Select</text>
      <text x="201" y="84" text-anchor="middle" class="bs">选工具 ← schema 菜单</text>

      <rect x="300" y="40" width="130" height="60" rx="10" class="box" />
      <text x="365" y="64" text-anchor="middle" class="bt">② Arguments</text>
      <text x="365" y="84" text-anchor="middle" class="bs">填参数 ← 任务与观察</text>

      <rect x="464" y="40" width="150" height="60" rx="10" class="box gate" />
      <text x="539" y="64" text-anchor="middle" class="bt">③ Validate 校验</text>
      <text x="539" y="84" text-anchor="middle" class="bs">schema / 约束解码</text>

      <rect x="648" y="40" width="130" height="60" rx="10" class="box det" />
      <text x="713" y="64" text-anchor="middle" class="bt">④ Execute</text>
      <text x="713" y="84" text-anchor="middle" class="bs">沙箱 · 确定性代码</text>

      <rect x="808" y="40" width="96" height="60" rx="10" class="box" />
      <text x="856" y="64" text-anchor="middle" class="bt">⑤ Result</text>
      <text x="856" y="84" text-anchor="middle" class="bs">回喂上下文</text>

      <line x1="94" y1="70" x2="130" y2="70" class="arr" marker-end="url(#tca-a)" />
      <line x1="266" y1="70" x2="294" y2="70" class="arr" marker-end="url(#tca-a)" />
      <line x1="430" y1="70" x2="458" y2="70" class="arr" marker-end="url(#tca-a)" />
      <line x1="614" y1="70" x2="642" y2="70" class="arr" marker-end="url(#tca-a)" />
      <line x1="778" y1="70" x2="800" y2="70" class="arr" marker-end="url(#tca-a)" />

      <!-- 校验失败回路 -->
      <path d="M 539 100 C 539 148, 365 148, 365 106" class="arr dash bad" marker-end="url(#tca-a)" fill="none" />
      <text x="452" y="158" text-anchor="middle" class="al bad-t">校验失败 → 报错回喂重试（lab01 的修复回路）</text>

      <!-- 结果回到 LLM 的环 -->
      <path d="M 856 100 C 856 216, 60 216, 60 108" class="arr dash" marker-end="url(#tca-a)" fill="none" />
      <text x="458" y="232" text-anchor="middle" class="al">观察进入下一轮 —— L01 的循环，在这里变成一段可审计的流水线</text>

      <!-- 图例 -->
      <g class="legend">
        <rect x="700" y="120" width="10" height="10" class="sw gate" />
        <text x="716" y="130" class="lg">确定性边界（代码保证）</text>
        <rect x="700" y="140" width="10" height="10" class="sw det" />
        <text x="716" y="150" class="lg">确定性执行（概率之外）</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.tca svg { display: block; }
.tca :deep(text) { font-family: inherit; }
.box { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); stroke-width: 1.5; }
.box.gate { stroke: var(--vp-c-brand-1); stroke-width: 2; }
.box.det { stroke: #16a34a; stroke-width: 2; }
.llm { fill: var(--vp-c-brand-soft); stroke: var(--vp-c-brand-1); stroke-width: 2; }
.bt { font-size: 14.5px; font-weight: 650; fill: var(--vp-c-text-1); }
.bs { font-size: 11.5px; fill: var(--vp-c-text-2); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 1.8; fill: none; }
.arr.dash { stroke-dasharray: 5 5; }
.arr.bad { stroke: var(--vp-c-danger, #dc2626); }
.bad-t { fill: var(--vp-c-danger, #dc2626); }
.al { font-size: 12.5px; fill: var(--vp-c-text-2); }
.lg { font-size: 12px; fill: var(--vp-c-text-3); }
.sw { rx: 2; }
.sw.gate { fill: none; stroke: var(--vp-c-brand-1); stroke-width: 2; }
.sw.det { fill: none; stroke: #16a34a; stroke-width: 2; }

/* 窄屏横向滚动查看：桌面容器足够宽不受影响（R6-4） */
.tca { overflow-x: auto; }
.tca svg { min-width: 640px; }
</style>
