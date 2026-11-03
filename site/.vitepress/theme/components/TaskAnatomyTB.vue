<script setup lang="ts">
</script>

<template>
  <div class="tat">
    <svg viewBox="0 0 920 330" width="100%" role="img" aria-label="Terminal-Bench 任务解剖：instruction 与沙箱（agent 在内行动）+ 隔离的 verifier 环境（对最终状态做可判定验收）">
      <defs><marker id="tat-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--vp-c-text-3)" /></marker></defs>

      <!-- 需求与任务三件套（人写的确定规范） -->
      <rect x="16" y="30" width="180" height="150" rx="12" class="box det" />
      <text x="106" y="52" text-anchor="middle" class="bt">任务三件套 · 人写</text>
      <text x="106" y="74" text-anchor="middle" class="bs">instruction.md（指令）</text>
      <text x="106" y="92" text-anchor="middle" class="bs">task.toml（配置）</text>
      <text x="106" y="110" text-anchor="middle" class="bs">solution/（参考解）</text>
      <text x="106" y="132" text-anchor="middle" class="mono">例：按示意图生成</text>
      <text x="106" y="148" text-anchor="middle" class="mono">/app/out.step 文件</text>
      <text x="106" y="170" text-anchor="middle" class="tag">规范：人写的确定文本</text>
      <line x1="196" y1="105" x2="228" y2="105" class="arr" marker-end="url(#tat-a)" />

      <!-- 概率区：agent 在沙箱环境内行动 -->
      <rect x="230" y="30" width="330" height="150" rx="12" class="zone-llm" />
      <text x="395" y="50" text-anchor="middle" class="ztag">概率区（agent 在沙箱内自由行动）</text>
      <rect x="246" y="60" width="140" height="52" rx="10" class="box" />
      <text x="316" y="80" text-anchor="middle" class="rn">Agent Harness</text>
      <text x="316" y="98" text-anchor="middle" class="rs">读指令 · bash 行动</text>
      <rect x="404" y="60" width="140" height="52" rx="10" class="box" />
      <text x="474" y="80" text-anchor="middle" class="rn">环境沙箱</text>
      <text x="474" y="98" text-anchor="middle" class="rs">Dockerfile 真软件</text>
      <path d="M 386 86 L 404 86" class="arr" marker-end="url(#tat-a)" />
      <path d="M 404 100 L 386 100" class="arr" marker-end="url(#tat-a)" />
      <text x="395" y="136" text-anchor="middle" class="bs">装真实软件与服务（不是 mock）</text>
      <text x="395" y="156" text-anchor="middle" class="tag">轨迹 = 全程可审计记录</text>
      <line x1="560" y1="105" x2="592" y2="105" class="arr" marker-end="url(#tat-a)" />

      <!-- 确定区：隔离的 verifier -->
      <rect x="594" y="30" width="310" height="150" rx="12" class="zone-det" />
      <text x="749" y="50" text-anchor="middle" class="ztag">确定区（verifier 环境隔离）</text>
      <rect x="610" y="60" width="278" height="52" rx="10" class="box gate" />
      <text x="749" y="80" text-anchor="middle" class="rn">tests/ · 可判定验收</text>
      <text x="749" y="98" text-anchor="middle" class="rs">对最终环境状态打分</text>
      <text x="749" y="132" text-anchor="middle" class="mono">assert watertight() ✓</text>
      <text x="749" y="150" text-anchor="middle" class="mono">assert correct_volume() ✓</text>
      <text x="749" y="170" text-anchor="middle" class="tag">PASS / FAIL——没有中间态</text>

      <!-- 两条防线说明 -->
      <path d="M 395 180 C 395 226, 749 226, 749 186" class="arr dash bad" marker-end="url(#tat-a)" fill="none" />
      <text x="560" y="238" text-anchor="middle" class="al bad-t">防线一：verifier 与 agent 环境隔离——agent 够不着打分的地方，改不了自己的成绩单</text>
      <path d="M 749 186 C 749 268, 395 276, 395 184" class="arr dash" marker-end="url(#tat-a)" fill="none" />
      <text x="560" y="298" text-anchor="middle" class="al">防线二：solution/ 参考解先跑一遍——verifier 自己必须先全绿，再放 agent 进考场</text>

      <text x="460" y="322" text-anchor="middle" class="foot">一个任务 = 可复现的考场：同一条指令、同一个镜像、同一套断言——你换来的不是分数，是可比较的分数</text>
    </svg>

    <div class="detail">
      <div class="drow"><span class="dk detk">人写规范</span><span>指令 + 环境镜像 + 参考解：全部是确定性文本，进 git、可 review——"规范"从代码搬进了任务描述</span></div>
      <div class="drow"><span class="dk llmk">agent 概率区</span><span>在沙箱内读指令、用 bash 行动（Terminal-Bench 的世界观：bash 是万能工具）；轨迹全程记录=收据</span></div>
      <div class="drow"><span class="dk gatek">verifier 确定区</span><span>测试只看<b>最终环境状态</b>（outcome），不看过程；与 agent 环境隔离，防篡改</span></div>
      <div class="drow"><span class="dk">两条防线</span><span>隔离（够不着）+ 自证（参考解先全绿）——reward hacking 的两道闸</span></div>
    </div>
  </div>
</template>

<style scoped>
.tat { display: flex; flex-direction: column; gap: 10px; overflow-x: auto; }
.tat svg { min-width: 920px; }
svg :deep(text) { font-family: inherit; }
.box { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); stroke-width: 1.5; }
.box.gate { stroke: var(--vp-c-brand-1); stroke-width: 2; }
.box.det { stroke: var(--vp-c-green-1, #16a34a); stroke-width: 1.8; }
.zone-llm { fill: var(--vp-c-brand-soft); stroke: var(--vp-c-brand-1); stroke-width: 1.2; stroke-dasharray: 6 4; }
.zone-det { fill: var(--vp-c-default-soft); stroke: var(--vp-c-divider); stroke-width: 1.2; stroke-dasharray: 6 4; }
.bt { font-size: 14px; font-weight: 650; fill: var(--vp-c-text-1); }
.bs { font-size: 12px; fill: var(--vp-c-text-2); }
.rn { font-size: 13px; font-weight: 650; fill: var(--vp-c-text-1); }
.rs { font-size: 12px; fill: var(--vp-c-text-2); }
.mono { font-size: 12px; fill: var(--vp-c-brand-1); font-family: var(--vp-font-family-mono, monospace); }
.tag { font-size: 12px; fill: var(--vp-c-text-3); }
.ztag { font-size: 12.5px; font-weight: 650; fill: var(--vp-c-text-2); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 1.8; fill: none; }
.arr.dash { stroke-dasharray: 5 5; }
.arr.bad { stroke: var(--vp-c-danger-1); }
.bad-t { fill: var(--vp-c-danger-1); }
.al { font-size: 12.5px; fill: var(--vp-c-text-2); }
.foot { font-size: 12.5px; fill: var(--vp-c-text-3); }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 7px; }
.drow { display: flex; gap: 10px; font-size: 13.5px; line-height: 1.65; }
.dk { flex: none; font-size: 12.5px; min-width: 88px; padding-top: 2px; color: var(--vp-c-text-3); }
.dk.llmk { color: var(--vp-c-brand-1); }
.dk.gatek { color: var(--vp-c-brand-1); }
.dk.detk { color: var(--vp-c-green-1, #16a34a); }
</style>
