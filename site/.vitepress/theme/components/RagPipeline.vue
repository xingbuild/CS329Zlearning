<template>
  <div class="rp">
    <svg viewBox="0 0 920 400" width="100%" role="img" aria-label="RAG 双管道：离线索引侧与在线问答侧">
      <defs>
        <marker id="rp-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="var(--vp-c-text-3)" />
        </marker>
      </defs>

      <!-- 离线区 -->
      <rect x="16" y="16" width="888" height="150" rx="14" class="zone off" />
      <text x="36" y="44" class="zt">离线 · 建库（一次或随数据变更）</text>

      <rect x="36" y="66" width="130" height="62" rx="10" class="box" />
      <text x="101" y="92" text-anchor="middle" class="bt">文档库</text>
      <text x="101" y="112" text-anchor="middle" class="bs">PDF / 网页 / 笔记</text>

      <rect x="206" y="66" width="130" height="62" rx="10" class="box" />
      <text x="271" y="92" text-anchor="middle" class="bt">分块</text>
      <text x="271" y="112" text-anchor="middle" class="bs">固定 / 结构 / 上下文增强</text>

      <rect x="376" y="66" width="150" height="62" rx="10" class="box" />
      <text x="451" y="92" text-anchor="middle" class="bt">嵌入 + 索引</text>
      <text x="451" y="112" text-anchor="middle" class="bs">向量（ANN/HNSW）+ BM25</text>

      <rect x="566" y="66" width="150" height="62" rx="10" class="box hl" />
      <text x="641" y="92" text-anchor="middle" class="bt">混合索引库</text>
      <text x="641" y="112" text-anchor="middle" class="bs">语义 + 精确词，各留一路</text>

      <line x1="166" y1="97" x2="200" y2="97" class="arr" marker-end="url(#rp-a)" />
      <line x1="336" y1="97" x2="370" y2="97" class="arr" marker-end="url(#rp-a)" />
      <line x1="526" y1="97" x2="560" y2="97" class="arr" marker-end="url(#rp-a)" />
      <text x="762" y="86" class="note">索引过期 = 答案过期</text>
      <text x="762" y="106" class="note">（失败动物园 · 检索侧）</text>

      <!-- 在线区 -->
      <rect x="16" y="196" width="888" height="188" rx="14" class="zone on" />
      <text x="36" y="224" class="zt">在线 · 问答（每一次提问）</text>

      <rect x="36" y="246" width="110" height="62" rx="10" class="box" />
      <text x="91" y="272" text-anchor="middle" class="bt">问题</text>
      <text x="91" y="292" text-anchor="middle" class="bs">（可改写）</text>

      <rect x="186" y="246" width="150" height="62" rx="10" class="box" />
      <text x="261" y="272" text-anchor="middle" class="bt">混合检索</text>
      <text x="261" y="292" text-anchor="middle" class="bs">向量 ∥ BM25 → RRF 融合</text>

      <rect x="376" y="246" width="150" height="62" rx="10" class="box" />
      <text x="451" y="272" text-anchor="middle" class="bt">重排漏斗</text>
      <text x="451" y="292" text-anchor="middle" class="bs">粗筛千级 → 精排十级</text>

      <rect x="566" y="246" width="140" height="62" rx="10" class="box" />
      <text x="636" y="272" text-anchor="middle" class="bt">Top-k 进上下文</text>
      <text x="636" y="292" text-anchor="middle" class="bs">证据要"聚焦"（L02/L06）</text>

      <rect x="742" y="246" width="140" height="62" rx="10" class="box hl" />
      <text x="812" y="272" text-anchor="middle" class="bt">LLM 生成</text>
      <text x="812" y="292" text-anchor="middle" class="bs">带引用 · 有据作答</text>

      <line x1="146" y1="277" x2="180" y2="277" class="arr" marker-end="url(#rp-a)" />
      <line x1="336" y1="277" x2="370" y2="277" class="arr" marker-end="url(#rp-a)" />
      <line x1="526" y1="277" x2="560" y2="277" class="arr" marker-end="url(#rp-a)" />
      <line x1="706" y1="277" x2="736" y2="277" class="arr" marker-end="url(#rp-a)" />

      <!-- 索引库 → 混合检索 -->
      <line x1="641" y1="128" x2="270" y2="242" class="arr dash" marker-end="url(#rp-a)" />
      <text x="430" y="180" class="al">查询打到离线建好的索引上</text>
    </svg>
    <div class="cap">上排是"入库时"决定的下限（分块、索引），下排是"每次提问"的链路——<b>答案错了先查上排，再查下排</b>（本讲失败动物园给的排查顺序）。</div>
  </div>
</template>

<style scoped>
.rp svg { display: block; }
.rp :deep(text) { font-family: inherit; }
.zone { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); }
.zt { font-size: 13.5px; font-weight: 700; fill: var(--vp-c-text-2); }
.box { fill: var(--vp-c-bg); stroke: var(--vp-c-divider); stroke-width: 1.5; }
.box.hl { stroke: var(--vp-c-brand-1); stroke-width: 2; }
.bt { font-size: 15px; font-weight: 650; fill: var(--vp-c-text-1); }
.bs { font-size: 12px; fill: var(--vp-c-text-2); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 1.8; fill: none; }
.arr.dash { stroke-dasharray: 5 5; }
.al { font-size: 12.5px; fill: var(--vp-c-text-2); }
.note { font-size: 12px; fill: var(--vp-c-text-3); }
.cap { font-size: 13.5px; line-height: 1.75; color: var(--vp-c-text-2); margin-top: 6px; }

/* 窄屏横向滚动查看：桌面容器足够宽不受影响（R6-4） */
.rp { overflow-x: auto; }
.rp svg { min-width: 640px; }
</style>
