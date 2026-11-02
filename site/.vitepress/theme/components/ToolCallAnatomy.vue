<template>
  <div class="tca">
    <svg viewBox="0 0 920 340" width="100%" role="img" aria-label="一次工具调用的解剖：输入组装 → LLM 一次生成（选工具+填参数）→ 校验 → 执行 → 回喂（概率区与确定区分带）">
      <defs>
        <marker id="tca-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="var(--vp-c-text-3)" />
        </marker>
      </defs>

      <!-- 输入区（代码组装） -->
      <rect x="16" y="30" width="180" height="140" rx="12" class="box det" />
      <text x="106" y="54" text-anchor="middle" class="bt">输入组装 · 代码</text>
      <text x="106" y="76" text-anchor="middle" class="bs">任务 + schema 菜单</text>
      <text x="106" y="94" text-anchor="middle" class="bs">+ 历史观察</text>
      <text x="106" y="112" text-anchor="middle" class="bs">→ 全部进 LLM 上下文</text>
      <text x="106" y="132" text-anchor="middle" class="mono">get_weather(city: string)</text>
      <text x="106" y="156" text-anchor="middle" class="tag">一吃 · 菜单（进上下文）</text>
      <line x1="196" y1="100" x2="226" y2="100" class="arr" marker-end="url(#tca-a)" />

      <!-- 概率区带 -->
      <rect x="228" y="30" width="300" height="140" rx="12" class="zone-llm" />
      <text x="378" y="48" text-anchor="middle" class="ztag">概率区（LLM）</text>
      <circle cx="268" cy="100" r="30" class="llm" />
      <text x="268" y="97" text-anchor="middle" class="bt">LLM</text>
      <text x="268" y="114" text-anchor="middle" class="bs">概率</text>
      <rect x="312" y="56" width="204" height="100" rx="10" class="box" />
      <text x="414" y="76" text-anchor="middle" class="bt">LLM 一次生成</text>
      <text x="414" y="96" text-anchor="middle" class="bs b">① 选工具 + ② 填参数</text>
      <text x="414" y="113" text-anchor="middle" class="bs dim">同一个 tool_call 两字段</text>
      <text x="414" y="132" text-anchor="middle" class="mono">get_weather({"city":</text>
      <text x="414" y="148" text-anchor="middle" class="mono">"Stanford"})</text>
      <text x="378" y="164" text-anchor="middle" class="tag">二吃 · 文法（strict：约束解码在生成中）</text>
      <line x1="528" y1="100" x2="556" y2="100" class="arr" marker-end="url(#tca-a)" />

      <!-- 确定区带 -->
      <rect x="558" y="30" width="346" height="140" rx="12" class="zone-det" />
      <text x="731" y="48" text-anchor="middle" class="ztag">确定性区（代码）</text>
      <rect x="570" y="58" width="106" height="96" rx="10" class="box gate" />
      <text x="623" y="80" text-anchor="middle" class="bt">③ 校验</text>
      <text x="623" y="99" text-anchor="middle" class="bs">类型 / 必填</text>
      <text x="623" y="126" text-anchor="middle" class="tag">三吃 · 闸门</text>
      <line x1="676" y1="106" x2="690" y2="106" class="arr" marker-end="url(#tca-a)" />
      <rect x="692" y="58" width="100" height="96" rx="10" class="box det" />
      <text x="742" y="80" text-anchor="middle" class="bt">④ 执行</text>
      <text x="742" y="99" text-anchor="middle" class="bs">沙箱 · 代码</text>
      <text x="742" y="126" text-anchor="middle" class="bs dim">真函数</text>
      <line x1="792" y1="106" x2="806" y2="106" class="arr" marker-end="url(#tca-a)" />
      <rect x="808" y="58" width="88" height="96" rx="10" class="box det" />
      <text x="852" y="80" text-anchor="middle" class="bt">⑤ 结果</text>
      <text x="852" y="99" text-anchor="middle" class="bs">入上下文</text>
      <text x="852" y="126" text-anchor="middle" class="bs dim">tool 消息</text>

      <!-- 失败回喂（终点 = LLM） -->
      <path d="M 623 154 C 623 212, 300 218, 271 134" class="arr dash bad" marker-end="url(#tca-a)" fill="none" />
      <text x="440" y="224" text-anchor="middle" class="al bad-t">校验失败 → 错误回喂 → LLM 重新生成</text>

      <!-- 观察回喂（终点 = LLM） -->
      <path d="M 852 154 C 852 268, 268 276, 268 134" class="arr dash" marker-end="url(#tca-a)" fill="none" />
      <text x="540" y="286" text-anchor="middle" class="al">观察 → 下一轮 LLM 再生成（①② 或 Finish 自然语言收尾）</text>

      <!-- 图例（三档全覆盖） -->
      <g class="legend">
        <rect x="16" y="212" width="10" height="10" class="sw llmsw" />
        <text x="32" y="222" class="lg">概率区：LLM 生成（含重试与下一轮）</text>
        <rect x="16" y="234" width="10" height="10" class="sw gate" />
        <text x="32" y="244" class="lg">确定性边界：文法 + 闸门</text>
        <rect x="16" y="256" width="10" height="10" class="sw det" />
        <text x="32" y="266" class="lg">确定性执行：沙箱 / 搬运 / 输入组装</text>
      </g>

      <text x="460" y="326" text-anchor="middle" class="foot">模型生成数据，代码解释执行——概率只住在中间那一段</text>
    </svg>

    <div class="detail">
      <div class="drow"><span class="dk llmk">LLM（概率）</span><span>读菜单 → <b>一次生成</b>工具名与参数（①② 是同一 tool_call 的两个字段）；校验失败后的重试、拿到观察后的下一轮（再调工具或 Finish 收尾），也都是它的生成</span></div>
      <div class="drow"><span class="dk gatek">确定性边界</span><span>schema 三吃——事前<b>菜单</b>（进上下文）/ 事中<b>文法</b>（约束解码，包住生成过程）/ 事后<b>闸门</b>（类型与必填校验）</span></div>
      <div class="drow"><span class="dk detk">确定性执行</span><span>沙箱真跑函数（④）；结果包成 tool 消息追加进上下文（⑤，代码搬运）；输入组装同样是代码</span></div>
      <div class="drow"><span class="dk">两个回喂点</span><span>③ 失败 → 错误回喂 → LLM 重新生成；⑤ 观察 → LLM 再生成（①② 或 Finish）——循环的发动机始终是 LLM，管道本身是直的</span></div>
    </div>
  </div>
</template>

<style scoped>
.tca svg { display: block; }
.tca :deep(text) { font-family: inherit; }
.box { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); stroke-width: 1.5; }
.box.gate { stroke: var(--vp-c-brand-1); stroke-width: 2; }
.box.det { stroke: var(--vp-c-green-1, #16a34a); stroke-width: 1.8; }
.zone-llm { fill: var(--vp-c-brand-soft); stroke: var(--vp-c-brand-1); stroke-width: 1.2; stroke-dasharray: 6 4; }
.zone-det { fill: var(--vp-c-default-soft); stroke: var(--vp-c-divider); stroke-width: 1.2; stroke-dasharray: 6 4; }
.llm { fill: var(--vp-c-brand-soft); stroke: var(--vp-c-brand-1); stroke-width: 2; }
.bt { font-size: 14px; font-weight: 650; fill: var(--vp-c-text-1); }
.bs { font-size: 12px; fill: var(--vp-c-text-2); }
.bs.b { font-weight: 650; fill: var(--vp-c-text-1); }
.bs.dim { fill: var(--vp-c-text-3); }
.mono { font-size: 12px; fill: var(--vp-c-brand-1); font-family: var(--vp-font-family-mono, monospace); }
.tag { font-size: 12px; fill: var(--vp-c-text-3); }
.ztag { font-size: 12.5px; font-weight: 650; fill: var(--vp-c-text-2); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 1.8; fill: none; }
.arr.dash { stroke-dasharray: 5 5; }
.arr.bad { stroke: var(--vp-c-danger-1); }
.bad-t { fill: var(--vp-c-danger-1); }
.al { font-size: 12.5px; fill: var(--vp-c-text-2); }
.lg { font-size: 12px; fill: var(--vp-c-text-3); }
.sw { rx: 2; }
.sw.gate { fill: none; stroke: var(--vp-c-brand-1); stroke-width: 2; }
.sw.det { fill: none; stroke: var(--vp-c-green-1, #16a34a); stroke-width: 2; }
.sw.llmsw { fill: var(--vp-c-brand-soft); stroke: var(--vp-c-brand-1); stroke-width: 1.5; }
.foot { font-size: 12.5px; fill: var(--vp-c-text-3); }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 7px; margin-top: 10px; }
.drow { display: flex; gap: 10px; font-size: 13.5px; line-height: 1.65; }
.dk { flex: none; font-size: 12.5px; min-width: 96px; padding-top: 2px; color: var(--vp-c-text-3); }
.dk.llmk { color: var(--vp-c-brand-1); }
.dk.gatek { color: var(--vp-c-brand-1); }
.dk.detk { color: var(--vp-c-green-1, #16a34a); }

/* 窄屏横向滚动查看：桌面容器足够宽不受影响（R6-4 + 1:1 兑现） */
.tca { overflow-x: auto; }
.tca svg { min-width: 920px; }
</style>
