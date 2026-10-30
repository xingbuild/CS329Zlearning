<template>
  <div class="tf">
    <svg viewBox="0 0 920 330" width="100%" role="img" aria-label="decoder-only Transformer 数据流：token → 嵌入 → N 层 Transformer Block → LM Head → 词表分布">
      <defs>
        <marker id="tf-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="var(--vp-c-text-3)" />
        </marker>
      </defs>

      <!-- 主流水线 -->
      <rect x="20" y="40" width="120" height="64" rx="10" class="box" />
      <text x="80" y="66" text-anchor="middle" class="bt">输入 tokens</text>
      <text x="80" y="88" text-anchor="middle" class="bs">The class was about</text>

      <rect x="180" y="40" width="140" height="64" rx="10" class="box" />
      <text x="250" y="66" text-anchor="middle" class="bt">嵌入 + 位置</text>
      <text x="250" y="88" text-anchor="middle" class="bs">每个 token → 向量</text>

      <rect x="360" y="24" width="220" height="96" rx="12" class="box hl" />
      <text x="470" y="52" text-anchor="middle" class="bt">Transformer Block</text>
      <text x="470" y="74" text-anchor="middle" class="bs">多头因果自注意力</text>
      <text x="470" y="94" text-anchor="middle" class="bs">FFN · 残差 · LayerNorm</text>
      <text x="470" y="130" text-anchor="middle" class="btag">× N 层</text>

      <rect x="620" y="40" width="130" height="64" rx="10" class="box" />
      <text x="685" y="66" text-anchor="middle" class="bt">LM Head</text>
      <text x="685" y="88" text-anchor="middle" class="bs">Softmax</text>

      <!-- 词表分布（右端） -->
      <g>
        <rect x="784" y="28" width="118" height="88" rx="10" class="box" />
        <text x="843" y="48" text-anchor="middle" class="bs">词表分布</text>
        <rect x="806" y="92" width="14" height="14" class="bar top" />
        <rect x="826" y="98" width="14" height="8" class="bar" />
        <rect x="846" y="100" width="14" height="6" class="bar" />
        <rect x="866" y="101" width="14" height="5" class="bar" />
      </g>

      <line x1="140" y1="72" x2="174" y2="72" class="arr" marker-end="url(#tf-a)" />
      <line x1="320" y1="72" x2="354" y2="72" class="arr" marker-end="url(#tf-a)" />
      <line x1="580" y1="72" x2="614" y2="72" class="arr" marker-end="url(#tf-a)" />
      <line x1="750" y1="72" x2="778" y2="72" class="arr" marker-end="url(#tf-a)" />

      <!-- 逐 token 循环（自回归） -->
      <path d="M 843 120 C 843 190, 80 190, 80 110" class="arr dash" marker-end="url(#tf-a)" fill="none" />
      <text x="460" y="200" text-anchor="middle" class="al">自回归：采出的 token 追加回输入，再来一遍（L01 剧场的"帧"，就是这么来的）</text>

      <!-- 注解区 -->
      <g class="notes">
        <text x="20" y="246" class="nb">· 注意力是唯一"看全局"的机制：每个 token 都能回看之前所有 token（因果掩码保证不偷看未来）</text>
        <text x="20" y="272" class="nb">· O(n²)：序列翻倍，注意力计算翻四倍 —— 长上下文贵的根源（与下表互参）</text>
        <text x="20" y="298" class="nb">· KV Cache：已算过的 K/V 存下来复用，但只认"前缀不变"（见下方 KV Cache 剧场）</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.tf svg { display: block; }
.tf :deep(text) { font-family: inherit; }
.box { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); stroke-width: 1.5; }
.box.hl { stroke: var(--vp-c-brand-1); stroke-width: 2; }
.bt { font-size: 15.5px; font-weight: 650; fill: var(--vp-c-text-1); }
.bs { font-size: 12px; fill: var(--vp-c-text-2); }
.btag { font-size: 12.5px; font-weight: 700; fill: var(--vp-c-brand-1); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 1.8; fill: none; }
.arr.dash { stroke-dasharray: 5 5; }
.al { font-size: 12.5px; fill: var(--vp-c-text-2); }
.bar { fill: var(--vp-c-divider); }
.bar.top { fill: var(--vp-c-brand-1); }
.nb { font-size: 13px; fill: var(--vp-c-text-2); }

/* 窄屏横向滚动查看：桌面容器足够宽不受影响（R6-4） */
.tf { overflow-x: auto; }
.tf svg { min-width: 640px; }
</style>
