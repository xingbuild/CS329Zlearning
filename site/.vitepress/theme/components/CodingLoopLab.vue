<script setup lang="ts">
import { ref, computed } from 'vue'

/* Coding Agent 闭环剧场：概率模型 × 确定性验证回路 → 收敛到正确
   任务：slugify(title) ；五条可判定验收测试；剧本三轮修复 + 无验证器对照 */
interface Round { code: string[]; news: number; results: boolean[]; feed: string }
const TESTS = [
  'slugify("Hello World") === "hello-world"',
  'slugify("Hello, World!") === "hello-world"',
  'slugify("  Multiple   Spaces  ") === "multiple-spaces"',
  'slugify("CS329Z: Agent 课程!") === "cs329z-agent"',
  'slugify("") === ""',
]
const ROUNDS: Round[] = [
  {
    code: [
      'function slugify(s) {',
      '  return s.toLowerCase()',
      '    .replace(/ /g, "-");',
      '}',
    ], news: 4, results: [true, false, false, false, true],
    feed: '3 个断言失败：T2 期望 "hello-world" 得到 "hello,-world!"；T3 得到 "-multiple---spaces-"；T4 得到 "cs329z:-agent-课程!"。错误详情（expected vs got）回喂给模型——失败变成信息。',
  },
  {
    code: [
      'function slugify(s) {',
      '  return s.toLowerCase()',
      '    .replace(/[^a-z0-9]+/g, "-");',
      '}',
    ], news: 1, results: [true, true, false, false, true],
    feed: 'T2 修好了（标点被清）。新失败：T3 得到 "-multiple-spaces-"、T4 得到 "cs329z-agent-"——首尾连字符残留。回喂继续。',
  },
  {
    code: [
      'function slugify(s) {',
      '  return s.toLowerCase()',
      '    .replace(/[^a-z0-9]+/g, "-")',
      '    .replace(/^-+|-+$/g, "");',
      '}',
    ], news: 1, results: [true, true, true, true, true],
    feed: '5/5 全绿——测试作为可判定的验收者宣布完成。这份代码从此是确定性的：同样的输入，永远同样的输出。',
  },
]
type Phase = 'write' | 'exec' | 'test' | 'feed' | 'ship' | 'bug'
const verifierOn = ref(true)
const step = ref(0)
/* 步序（验证器开）：每轮 写→执行→测试→(回喂|交付)；关：写→执行→(宣称完成→带bug交付) */
const seq = computed<Phase[]>(() => {
  if (!verifierOn.value) return ['write', 'exec', 'ship', 'bug']
  const out: Phase[] = []
  ROUNDS.forEach((_, i) => {
    out.push('write', 'exec', 'test')
    out.push(i === ROUNDS.length - 1 ? 'ship' : 'feed')
  })
  return out
})
const cur = computed(() => seq.value[Math.min(step.value, seq.value.length - 1)])
const done = computed(() => step.value >= seq.value.length - 1)
const roundIdx = computed(() => {
  if (!verifierOn.value) return 0
  let n = -1
  seq.value.slice(0, step.value + 1).forEach((p) => { if (p === 'write') n++ })
  return Math.max(n, 0)
})
const shownRounds = computed(() => {
  if (!verifierOn.value) return [ROUNDS[0]]
  return ROUNDS.slice(0, roundIdx.value + 1)
})
function toggle() { verifierOn.value = !verifierOn.value; step.value = 0 }
function reset() { step.value = 0 }

const PHASES: Record<Phase, { name: string; sub: string }> = {
  write: { name: 'LLM 写码', sub: '概率生成' },
  exec: { name: '沙箱执行', sub: '确定性' },
  test: { name: '测试验收', sub: '可判定' },
  feed: { name: '错误回喂', sub: '失败→信息' },
  ship: { name: '交付 ✓', sub: '确定性代码' },
  bug: { name: '带 bug 上线', sub: '💥 无验证器' },
}
</script>

<template>
  <div class="cll">
    <div class="row wrap">
      <button type="button" class="wbtn" :aria-pressed="verifierOn" @click="toggle">{{ verifierOn ? '验证回路：开（闭环）' : '验证回路：关（一次交付）' }}</button>
      <button type="button" class="wbtn" :disabled="step === 0" @click="step--">◀</button>
      <button type="button" class="wbtn primary" :disabled="done" @click="step++">下一步 ▶</button>
      <button type="button" class="wbtn" @click="reset">重置</button>
      <span class="pill brand">第 {{ roundIdx + 1 }} 轮 · {{ verifierOn ? `${ROUNDS[roundIdx].results.filter(Boolean).length}/5 通过` : '未经验证' }}</span>
    </div>

    <!-- 环形舞台：四角色固定，循环是结构 -->
    <svg viewBox="0 0 680 300" width="100%" role="img" aria-label="coding agent 闭环：写码→执行→测试→回喂">
      <defs><marker id="cll-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="var(--vp-c-text-3)" /></marker></defs>
      <g v-if="verifierOn">
        <line x1="200" y1="60" x2="480" y2="60" class="arr" :class="{ hot: cur === 'exec' }" marker-end="url(#cll-a)" />
        <line x1="580" y1="100" x2="580" y2="180" class="arr" :class="{ hot: cur === 'test' }" marker-end="url(#cll-a)" />
        <line x1="480" y1="220" x2="200" y2="220" class="arr" :class="{ hot: cur === 'feed' }" marker-end="url(#cll-a)" />
        <text x="340" y="212" text-anchor="middle" class="al">错误回喂 ↺（控制流回到写码位）</text>
        <line x1="100" y1="180" x2="100" y2="100" class="arr hotobs" :class="{ hot: cur === 'feed' || cur === 'ship' }" marker-end="url(#cll-a)" />
      </g>
      <g v-else>
        <line x1="200" y1="60" x2="480" y2="60" class="arr" :class="{ hot: cur === 'exec' }" marker-end="url(#cll-a)" />
        <line x1="580" y1="100" x2="580" y2="180" class="arr crash" :class="{ hot: cur === 'ship' || cur === 'bug' }" marker-end="url(#cll-a)" />
      </g>
      <g v-for="(p, k) in (verifierOn ? (['write','exec','test'] as Phase[]) : (['write','exec','bug'] as Phase[]))" :key="k">
        <rect :x="20 + k * 240" :y="k === 1 ? 20 : k === 0 ? 20 : 160" width="160" height="80" rx="12"
          class="box" :class="{ on: cur === p, crashb: !verifierOn && p === 'bug' }" style="display: none" />
      </g>
      <!-- 真实角色框（手动定位，避免上面隐藏组的坐标混乱） -->
      <rect x="20" y="20" width="180" height="80" rx="12" class="box" :class="{ on: cur === 'write' }" />
      <text x="110" y="56" text-anchor="middle" class="rn">{{ PHASES.write.name }}</text>
      <text x="110" y="78" text-anchor="middle" class="rs">{{ PHASES.write.sub }}</text>
      <rect x="480" y="20" width="180" height="80" rx="12" class="box" :class="{ on: cur === 'exec' }" />
      <text x="570" y="56" text-anchor="middle" class="rn">{{ PHASES.exec.name }}</text>
      <text x="570" y="78" text-anchor="middle" class="rs">{{ PHASES.exec.sub }}</text>
      <rect x="480" y="160" width="180" height="80" rx="12" class="box" :class="{ on: cur === 'test' }" v-if="verifierOn" />
      <text x="570" y="196" text-anchor="middle" class="rn" v-if="verifierOn">{{ PHASES.test.name }}</text>
      <text x="570" y="218" text-anchor="middle" class="rs" v-if="verifierOn">{{ PHASES.test.sub }}</text>
      <rect x="480" y="160" width="180" height="80" rx="12" class="box crashb" :class="{ on: cur === 'bug' }" v-if="!verifierOn" />
      <text x="570" y="196" text-anchor="middle" class="rn" v-if="!verifierOn">{{ PHASES.bug.name }}</text>
      <text x="570" y="218" text-anchor="middle" class="rs" v-if="!verifierOn">{{ PHASES.bug.sub }}</text>
      <rect x="20" y="160" width="180" height="80" rx="12" class="box" :class="{ on: cur === 'feed' || cur === 'ship' }" v-if="verifierOn" />
      <text x="110" y="196" text-anchor="middle" class="rn" v-if="verifierOn">{{ cur === 'ship' ? '交付 ✓' : '错误回喂' }}</text>
      <text x="110" y="218" text-anchor="middle" class="rs" v-if="verifierOn">{{ cur === 'ship' ? '确定性代码' : '失败→信息' }}</text>
      <text x="340" y="140" text-anchor="middle" class="loop-t">验 证 回 路</text>
    </svg>

    <!-- 左：代码（累积轮次，新增行高亮）；右：测试面板（历史累积） -->
    <div class="main">
      <div class="codes">
        <div v-for="(r, ri) in shownRounds" :key="ri" class="coderound" :class="{ cur: ri === roundIdx }">
          <div class="crh">第 {{ ri + 1 }} 轮代码 <span v-if="ri === roundIdx && cur === 'write'" class="pill brand">生成中…</span></div>
          <pre><code><span v-for="(l, li) in r.code" :key="li" class="ln" :class="{ nw: li >= r.code.length - r.news }">{{ l }}
</span></code></pre>
        </div>
      </div>
      <div class="tests">
        <div class="crh">验收测试（结果按轮累积）</div>
        <div v-for="(t, ti) in TESTS" :key="ti" class="trow">
          <span class="tn">T{{ ti + 1 }}</span><code class="tc">{{ t }}</code>
          <span class="hist">
            <template v-if="!verifierOn"><span class="r unk">?</span></template>
            <template v-else>
              <span v-for="(r, ri) in shownRounds" :key="ri" class="r" :class="r.results[ti] ? 'ok' : 'no'">{{ r.results[ti] ? '✓' : '✗' }}</span>
            </template>
          </span>
        </div>
        <div v-if="!verifierOn && (cur === 'ship' || cur === 'bug')" class="nores">⚠️ 没有测试就没有 ❌——模型自称"写好了"，3 个 bug 随交付上线（对照：开验证回路时第 1 轮同样这份代码，会被当场拦下）。</div>
      </div>
    </div>

    <div class="hint"><span class="k">现在看什么 · </span>
      <template v-if="!verifierOn">对照模式：一次生成直接交付——概率世界的裸奔。切回"验证回路：开"看同样起点怎么被回路修好。</template>
      <template v-else-if="cur === 'feed'">关键帧：失败的不是模型，是被测试**判定**出来的——expected vs got 是确定性信号；它沿环回到写码位，成为下一轮的上下文（Reflexion：反思来自外部信号）。</template>
      <template v-else-if="cur === 'ship'">交付的是确定性代码：输入输出关系被 5 条断言钉死。模型每一步都可能错，但回路保证**验收过线的才出门**——确定性来自验证器，不来自模型。</template>
      <template v-else>左看代码怎么长（新增行高亮），右看测试怎么从 ✗ 变 ✓——两条线都是累积的：过去不消失。</template>
    </div>
  </div>
</template>

<style scoped>
.cll { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
svg :deep(text) { font-family: inherit; }
.box { fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); stroke-width: 1.5; }
.box.on { stroke: var(--vp-c-brand-1); stroke-width: 2.5; fill: var(--vp-c-brand-soft); }
.box.crashb { stroke: #dc2626; }
.rn { font-size: 15px; font-weight: 700; fill: var(--vp-c-text-1); }
.rs { font-size: 11.5px; fill: var(--vp-c-text-2); }
.arr { stroke: var(--vp-c-text-3); stroke-width: 1.8; fill: none; }
.arr.hot, .arr.hotobs.hot { stroke: var(--vp-c-brand-1); stroke-width: 3; }
.arr.crash { stroke: #dc2626; stroke-width: 2.5; }
.al { font-size: 12px; fill: var(--vp-c-text-2); }
.loop-t { font-size: 15px; font-weight: 700; fill: var(--vp-c-text-3); letter-spacing: 4px; }
.main { display: flex; gap: 14px; flex-wrap: wrap; }
.codes { flex: 1.2; min-width: 280px; display: flex; flex-direction: column; gap: 8px; }
.coderound { border: 1px solid var(--vp-c-divider); border-radius: 10px; padding: 8px 12px; opacity: .6; }
.coderound.cur { opacity: 1; border-color: var(--vp-c-brand-1); }
.coderound pre { margin: 0; overflow-x: auto; }
.coderound code { font-size: 12.5px; line-height: 1.6; font-family: var(--vp-font-family-mono, monospace); }
.ln { color: var(--vp-c-text-2); }
.ln.nw { color: var(--vp-c-brand-1); font-weight: 650; }
.tests { flex: 1; min-width: 260px; }
.crh { font-size: 13px; font-weight: 650; color: var(--vp-c-text-2); margin-bottom: 6px; display: flex; gap: 8px; align-items: center; }
.trow { display: flex; gap: 8px; align-items: center; padding: 3px 0; font-size: 12px; }
.tn { font-weight: 700; color: var(--vp-c-text-3); min-width: 24px; }
.tc { font-size: 11.5px; background: none; padding: 0; }
.hist { margin-left: auto; display: flex; gap: 3px; }
.r { font-size: 13px; }
.r.ok { color: #16a34a; }
.r.no { color: #dc2626; }
.r.unk { color: var(--vp-c-text-3); }
.nores { font-size: 13px; line-height: 1.65; background: rgba(220,38,38,.08); border-radius: 8px; padding: 8px 12px; margin-top: 6px; }
</style>
